#!/usr/bin/env node
'use strict';

// The devcage loop. It owns the Discord connection, the pane, the acknowledgement, the reminder and
// the answer drain. Every rule it applies comes from ./bridge.js, which reads CONTRACT.md.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { Client, GatewayIntentBits, Partials } = require('discord.js');
const {
  CFG,
  CONTRACT,
  gate,
  renderLine,
  signNotice,
  noticeLine,
  REMINDER_EVERY_S,
  saveConfig,
} = require('./bridge');
const { Recorder } = require('./state');

const cfg = CFG;
const recorder = new Recorder(cfg);
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.DirectMessages,
  ],
  partials: [Partials.Channel],
});

function logLine(...parts) {
  process.stderr.write(`${new Date().toISOString()} ${parts.join(' ')}\n`);
}

function token() {
  const file = cfg.token_file || '/home/dev/.config/bridge/bot.token';
  if (process.env.BRIDGE_BOT_TOKEN) return process.env.BRIDGE_BOT_TOKEN.trim();
  const t = fs.readFileSync(file, 'utf8').trim();
  if (!t) throw new Error(`${file} is empty`);
  return t;
}

// One loop, one gateway. A second bot.js on the same token would ack, inject and post twice, and
// reply.js would look correct from both. CONTRACT.md declares the word `writer-lock-refused` for this
// case. A lock naming a pid that is not a live bot.js is stale (crash, container restart) and is taken
// over, so a reboot never needs a human hand on a lock file.
function liveLoopHolding(lockPath) {
  let pid = 0;
  try {
    pid = Number(fs.readFileSync(lockPath, 'utf8').trim());
  } catch (_) {
    return 0;
  }
  if (!pid || pid === process.pid) return 0;
  try {
    // The pid alone is not the process: pid reuse would otherwise make a stranger the lock holder.
    if (!fs.readFileSync(`/proc/${pid}/cmdline`, 'utf8').includes('bot.js')) return 0;
  } catch (_) {
    return 0;
  }
  return pid;
}

function takeLock() {
  const stateDir = cfg.state_dir || '/root/.pi/bridge/state';
  fs.mkdirSync(stateDir, { recursive: true, mode: 0o700 });
  const lockPath = path.join(stateDir, 'loop.lock');
  const holder = liveLoopHolding(lockPath);
  if (holder) {
    recorder.write('writer-lock-refused', { pid: holder, path: lockPath });
    process.stderr.write(`${new Date().toISOString()} another loop holds ${lockPath} (pid ${holder}); exiting\n`);
    process.exit(2);
  }
  fs.writeFileSync(lockPath, String(process.pid), { mode: 0o600 });
  process.on('exit', () => {
    try {
      if (fs.readFileSync(lockPath, 'utf8').trim() === String(process.pid)) fs.unlinkSync(lockPath);
    } catch (_) { /* not ours any more */ }
  });
}

function inject(line) {
  const target = cfg.pane || 'seat';
  try {
    execFileSync('tmux', ['has-session', '-t', target], { stdio: 'ignore' });
  } catch (_) {
    return false;
  }
  try {
    // C14: the line ends in one newline. A literal newline through `-l` is text, not the Enter key,
    // so send the text without it and then press Enter. One line reaches the pane, and it is submitted.
    const text = String(line).replace(/\r?\n$/, '');
    execFileSync('tmux', ['send-keys', '-t', target, '-l', text], { stdio: 'ignore' });
    execFileSync('tmux', ['send-keys', '-t', target, 'Enter'], { stdio: 'ignore' });
    return true;
  } catch (err) {
    // tmux's own words, not "Command failed": `-t =spac` is a session target has-session accepts and
    // send-keys rejects with "can't find pane", and that distinction has to survive into the log.
    const why = err && err.stderr ? String(err.stderr).trim() : err.message;
    logLine('inject failed:', why, '| target:', target);
    return false;
  }
}

function messageShape(message) {
  return {
    id: message.id,
    channel_id: message.channelId,
    guild_id: message.guildId,
    author: { id: message.author.id, bot: !!message.author.bot },
    mentions: [...message.mentions.users.values()].map((u) => ({ id: u.id, bot: !!u.bot })),
    mention_roles: [...message.mentions.roles.keys()],
    dm: message.channel.isDMBased(),
    content: message.content,
    thread_parent_id: message.channel.isThread() ? message.channel.parentId : null,
    // The gate needs ids; the answer path needs somewhere to post. Keep the live channel object.
    channel: message.channel,
  };
}

function splitContent(text, limit = 1990) {
  // Discord caps one message at 2000 characters. The bridge has no length *rule* (C12 is withdrawn);
  // this is transport framing, so an answer is split at a paragraph, line or space boundary.
  let rest = String(text || '');
  const out = [];
  while (rest.length > limit) {
    let cut = rest.lastIndexOf('\n\n', limit);
    if (cut < limit / 2) cut = rest.lastIndexOf('\n', limit);
    if (cut < limit / 2) cut = rest.lastIndexOf(' ', limit);
    if (cut <= 0) cut = limit;
    out.push(rest.slice(0, cut));
    rest = rest.slice(cut).replace(/^\s+/, '');
  }
  if (rest) out.push(rest);
  return out;
}

async function send(channel, text) {
  // Answers and reminders are information, never a new instruction: no pings escape.
  const parts = splitContent(text);
  for (const part of parts) {
    await channel.send({ content: part, allowedMentions: { parse: [] } });
  }
  return parts.length;
}

function scheduleHeld() {
  for (const req of recorder.pending()) {
    if (req.state !== 'held') continue;
    const line = renderLine(req.id, req.instruction, req.entryAt / 1000);
    if (inject(line)) recorder.injected(req.id);
  }
}

function drainAnswers() {
  for (const answer of recorder.drainAnswers()) {
    const id = String(answer.reply_to || answer.id || '');
    const req = recorder.get(id);
    if (!req || req.terminal) {
      // C18: an answer with no open request is recorded, never posted.
      recorder.unattributed(id);
      continue;
    }
    const target = req.channel || client.channels.cache.get(String(req.channelId || ''));
    if (!target) {
      // C18: an answer with no postable channel is still not an answer.
      recorder.unattributed(id);
      continue;
    }
    recorder.reply(id, answer.text, splitContent(answer.text).length);
    recorder.delivered(id);
    send(target, answer.text)
      .then(() => {
        recorder.answered(id, answer.text);
        recorder.receiptWritten(id);
      })
      .catch((err) => logLine('answer post failed:', err.message));
  }
}

function remind() {
  const now = Date.now();
  for (const req of recorder.pending()) {
    if (req.state === 'held') continue;
    const due = Math.floor((now - req.entryAt) / (REMINDER_EVERY_S * 1000));
    if (due <= req.reminders) continue;
    const minutes = due * (REMINDER_EVERY_S / 60);
    const sig = signNotice(req.id, minutes, Math.floor(now / 1000));
    const line = noticeLine(req.id, minutes, Math.floor(now / 1000), sig);
    // C22: the reminder is a channel post *and* the agent's pane cue. R6: no key is labelled, not withheld.
    send(req.channel, line).catch((err) => logLine('reminder post failed:', err.message));
    inject(line + '\n');
    recorder.reminder(req.id, minutes, sig !== 'none');
  }
}

client.once('ready', async () => {
  try {
    cfg.bot_id = client.user.id;
    // R9: the operator is pinned by bridge.js to 847445853584883712. The application owner is
    // deliberately not consulted: a transferred app or a different team must not add an author.

    if (cfg.guild_id) {
      const guild = await client.guilds.fetch(String(cfg.guild_id));
      const me = await guild.members.fetch(client.user.id);
      // C4: a mention of one of this bot's roles addresses it exactly like a mention of the bot.
      // @everyone carries the guild id as its role id and is in this cache. A plain @everyone sets
      // mentions.everyone, not mention_roles, so keeping it here only makes config.json misleading.
      cfg.role_ids = [...new Set([...(cfg.role_ids || []), ...me.roles.cache.keys()])]
        .filter((id) => String(id) !== String(cfg.guild_id));
    }
    if (cfg.channel_id) await client.channels.fetch(String(cfg.channel_id));
    saveConfig(cfg);
    const { abandoned } = recorder.start();
    recorder.heartbeat();
    logLine(`ready as ${client.user.tag} (${cfg.bot_id}); operator ${cfg.operator_id}; abandoned ${abandoned.length}`);
  } catch (err) {
    logLine('startup failed:', err.stack || err.message);
    process.exitCode = 1;
    client.destroy();
  }
});

client.on('messageCreate', async (message) => {
  if (message.author.id === client.user.id) return;
  if (message.system) return;
  const shape = messageShape(message);
  const verdict = gate(shape, cfg, shape.dm);
  if (verdict.action !== 'accept') {
    // C2: silence in the channel, one refusal on the record. The refusal carries no instruction.
    recorder.refused(shape, verdict.code);
    return;
  }
  const req = recorder.accepted(shape, verdict.instruction);
  if (!req) return; // C26: the same message id is the same request
  const text = shape.dm
    ? CONTRACT.ack.dm_text
    : CONTRACT.ack.channel_text.replace('{operator_id}', String(cfg.operator_id));
  try {
    await send(message.channel, text); // C21: acknowledged before the pane and before any answer
  } catch (err) {
    logLine('ack failed:', err.message);
  }
  const line = renderLine(message.id, verdict.instruction, message.createdAt);
  if (inject(line)) recorder.injected(message.id);
  else recorder.held(message.id);
});

setInterval(scheduleHeld, 5000);
setInterval(drainAnswers, 1000);
setInterval(remind, 5000);
setInterval(() => recorder.heartbeat(), 30000);

client.on('error', (err) => logLine('discord error:', err.message));
process.on('unhandledRejection', (err) => logLine('unhandled:', err && err.stack ? err.stack : String(err)));
process.on('SIGTERM', () => { client.destroy(); process.exit(0); });
process.on('SIGINT', () => { client.destroy(); process.exit(0); });

takeLock();
logLine(`starting; contract ${CONTRACT.version} at ${require('./bridge').CONTRACT_PATH}`);
client.login(token()).catch((err) => {
  logLine('login failed:', err.message);
  process.exit(1);
});
