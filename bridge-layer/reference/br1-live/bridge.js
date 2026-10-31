'use strict';

// The contract is the only source of the rules, codes, words and shapes. Nothing below restates a
// rule in a second place: a field here that the contract does not declare is a defect, not a default.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const CONTRACT_CANDIDATES = [
  process.env.BRIDGE_CONTRACT,
  path.join(__dirname, 'contract', 'CONTRACT.md'),
  path.join(__dirname, '..', 'bridge-contract', 'CONTRACT.md'),
].filter(Boolean);

function loadContract(file) {
  const target = file || CONTRACT_CANDIDATES.find((p) => fs.existsSync(p));
  if (!target) {
    throw new Error('CONTRACT.md not found; set BRIDGE_CONTRACT or install services/bridge-contract');
  }
  const text = fs.readFileSync(target, 'utf8');
  const block = text.match(/```toml\n([\s\S]*?)\n```/);
  if (!block) throw new Error(`${target}: no toml block`);
  return { contract: require('@iarna/toml').parse(block[1]), path: target };
}

const loaded = loadContract();
const CONTRACT = loaded.contract;
const CONTRACT_PATH = loaded.path;

const REMINDER_EVERY_S = Number(CONTRACT.notice.every_s);
const OPTIONAL_CODES = new Set(CONTRACT.codes.optional || []);
const ABOLISHED_CODES = new Set(Object.keys(CONTRACT.codes.abolished || {}));
const CONTRACT_CODES = Object.keys(CONTRACT.codes).filter(
  (k) => typeof CONTRACT.codes[k] === 'string' && k !== 'rule'
);
// What this box can actually emit. The thread code is optional and this box has no thread surface,
// so it is honest not to list it; the arm subtracts the declared optional gap.
const EMITTED_CODES = CONTRACT_CODES.filter((c) => !OPTIONAL_CODES.has(c) && !ABOLISHED_CODES.has(c));

const WORDS = new Set([
  ...(CONTRACT.receipts.event || []),
  ...(CONTRACT.receipts.operational || []),
  ...(CONTRACT.receipts.forward || []),
]);
const ABOLISHED_WORDS = new Set(CONTRACT.receipts.abolished || []);
const LADDER = new Set(CONTRACT.states.ladder || []);
const TERMINAL = new Set(CONTRACT.states.terminal || []);

const CONFIG_CANDIDATES = [
  process.env.BRIDGE_CONFIG,
  path.join(__dirname, 'config.json'),
].filter(Boolean);

function loadConfig(file) {
  const target = file || CONFIG_CANDIDATES.find((p) => fs.existsSync(p));
  if (!target) return {};
  return JSON.parse(fs.readFileSync(target, 'utf8'));
}

// R9 (operator, 2026-10-25 23:05Z): the only human author is Geo, 847445853584883712.
// This is a pin, not a default: a config that names anyone else is refused at load, and the
// application owner is never consulted as a fallback. "Only ever listen to Geo" must survive
// an app transfer, a team change, and a careless config edit.
const OPERATOR_ID = '847445853584883712';

const CFG = loadConfig();
if (CFG.operator_id && String(CFG.operator_id) !== OPERATOR_ID) {
  throw new Error(
    `config operator_id ${CFG.operator_id} is not the pinned operator ${OPERATOR_ID} (R9)`
  );
}
CFG.operator_id = OPERATOR_ID;
const CONFIG_PATH = CONFIG_CANDIDATES.find((p) => fs.existsSync(p)) || null;

function saveConfig(cfg) {
  if (!CONFIG_PATH) return;
  const tmp = `${CONFIG_PATH}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(cfg, null, 2) + '\n', { mode: 0o600 });
  fs.renameSync(tmp, CONFIG_PATH);
}

// ---------------------------------------------------------------- time

function formatTs(ts) {
  if (ts === undefined || ts === null || ts === '') return new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
  if (ts instanceof Date) return ts.toISOString().replace(/\.\d{3}Z$/, 'Z');
  if (typeof ts === 'number' || /^\d+$/.test(String(ts))) {
    return new Date(Number(ts) * 1000).toISOString().replace(/\.\d{3}Z$/, 'Z');
  }
  const s = String(ts);
  if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/.test(s)) return s;
  return new Date(s).toISOString().replace(/\.\d{3}Z$/, 'Z');
}

function unixTs(ts) {
  if (ts === undefined || ts === null || ts === '') return Math.floor(Date.now() / 1000);
  if (typeof ts === 'number') return Math.trunc(ts);
  const s = String(ts);
  if (/^\d+$/.test(s)) return parseInt(s, 10);
  return Math.floor(new Date(s).getTime() / 1000);
}

// ---------------------------------------------------------------- the line (C14-C17)

function sanitize(text) {
  // C17: control characters removed, newlines become spaces. A tab is control too; keeping it would
  // make the pane see something the grammar calls text but a terminal calls movement.
  return String(text === undefined || text === null ? '' : text)
    .replace(/[\u0000-\u0008\u0009\u000B\u000C\u000E-\u001F\u007F]/g, '')
    .replace(/[\r\n]+/g, ' ');
}

function escapeRe(s) {
  return String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function stripAddressed(content, botId, roleIds) {
  let out = String(content || '');
  out = out.replace(new RegExp(`<@!?${escapeRe(botId)}>`, 'g'), ' ');
  for (const role of roleIds) out = out.replace(new RegExp(`<@&${escapeRe(role)}>`, 'g'), ' ');
  return out.replace(/[ \t]+/g, ' ').trim();
}

function renderLine(msgId, text, ts) {
  return CONTRACT.line.directive_template
    .replace('{ts}', formatTs(ts))
    .replace('{msg}', String(msgId))
    .replace('{text}', sanitize(text));
}

// ---------------------------------------------------------------- the gate (C2-C13)

function refuse(code) {
  return { action: 'refuse', code, instruction: null };
}

function gate(msg, cfg = CFG, dm = !!(msg && msg.dm)) {
  const m = msg || {};
  const author = String((m.author && m.author.id !== undefined ? m.author.id : m.author) || '');
  const isBot = !!(m.author && m.author.bot);
  const peers = new Set((cfg.peers || []).map(String));
  const operator = String(cfg.operator_id || '');
  const botId = String(cfg.bot_id || '');
  const roleIds = (cfg.role_ids || []).map(String);

  // C7 first: a bot author is refused unless it is a declared peer on the peer lane.
  if (isBot && !peers.has(author)) return refuse('bot_author');
  // C10 before C6 in the declared order: a stranger's DM is diagnosed as the DM cause.
  if (dm && author !== operator) return refuse('dm_stranger');
  if (!isBot && author !== operator && !peers.has(author)) return refuse('other_author');
  // C9: a configured guild must match. A DM has no guild, and C8 made the DM a lane, not a channel.
  if (!dm && cfg.guild_id && String(m.guild_id || '') !== String(cfg.guild_id)) return refuse('wrong_guild');
  if (!dm && String(m.channel_id || '') !== String(cfg.channel_id)) return refuse('wrong_channel');

  const mentions = (m.mentions || []).map((x) => String(x && x.id !== undefined ? x.id : x));
  const mentionedRoles = (m.mention_roles || []).map(String);
  const addressed = mentions.includes(botId) || mentionedRoles.some((r) => roleIds.includes(r));
  if (!addressed) {
    const others = mentions.filter((id) => id !== botId && id !== operator);
    return refuse(others.length ? 'pinged_other_user' : 'pinged_nobody');
  }

  const content = String(m.content !== undefined ? m.content : m.text || '');
  const instruction = stripAddressed(content, botId, roleIds);
  if (!instruction) return refuse('empty');
  return { action: 'accept', code: null, instruction };
}

// ---------------------------------------------------------------- the notice (C19-C20)

function noticeKey() {
  const file = CFG.notice_key || '/etc/spacebridge/notice.key';
  try {
    const raw = fs.readFileSync(file);
    const trimmed = raw.toString('utf8').trim();
    return trimmed ? Buffer.from(trimmed, 'utf8') : null;
  } catch (_) {
    return null;
  }
}

function keyFromHex(keyHex) {
  if (keyHex === undefined || keyHex === null || keyHex === '') return null;
  const buf = Buffer.from(String(keyHex), 'hex');
  return buf.length ? buf : null;
}

function noticeCanonical(msgId, minutes, ts) {
  return CONTRACT.notice.canonical
    .replace('{msg}', String(msgId))
    .replace('{minutes}', String(minutes))
    .replace('{unix}', String(unixTs(ts)));
}

function signNotice(msgId, minutes, ts, keyHex) {
  const key = keyHex === undefined ? noticeKey() : keyFromHex(keyHex);
  if (!key) return 'none';
  return crypto.createHmac('sha256', key).update(noticeCanonical(msgId, minutes, ts)).digest('hex');
}

function noticeLine(msgId, minutes, ts, sig) {
  return CONTRACT.notice.line_template
    .replace('{msg}', String(msgId))
    .replace('{minutes}', String(minutes))
    .replace('{ts}', String(unixTs(ts)))
    .replace('{sig}', sig || 'none');
}

function verifyNotice(line, keyHex, ts) {
  const raw = String(line || '').replace(/[\r\n]+$/, '');
  // The contract writes Python named groups; JS spells them the other way around.
  const shape = new RegExp(CONTRACT.notice.shape_grammar.replace(/\(\?P</g, '(?<'));
  const m = raw.match(shape);
  if (!m) return { rc: 1, status: 'shape' };
  if (m.groups.sig === 'none') return { rc: 1, status: 'unsigned' };
  const key = keyHex === undefined ? noticeKey() : keyFromHex(keyHex);
  if (!key) return { rc: 1, status: 'no-key' };
  const want = crypto
    .createHmac('sha256', key)
    .update(noticeCanonical(m.groups.msg, m.groups.minutes, m.groups.ts))
    .digest('hex');
  const got = m.groups.sig;
  const ok =
    got.length === want.length &&
    crypto.timingSafeEqual(Buffer.from(got, 'utf8'), Buffer.from(want, 'utf8'));
  return ok ? { rc: 0, status: 'ok' } : { rc: 1, status: 'signature' };
}

// ---------------------------------------------------------------- identity (C31)

function codeIdentity() {
  const files = ['bridge.js', 'bot.js', 'reply.js', 'state.js']
    .map((f) => path.join(__dirname, f))
    .filter((f) => fs.existsSync(f));
  const h = crypto.createHash('sha256');
  for (const f of files) h.update(fs.readFileSync(f));
  return h.digest('hex').slice(0, 16);
}

module.exports = {
  CONTRACT,
  CONTRACT_PATH,
  CFG,
  OPERATOR_ID,
  CONFIG_PATH,
  loadConfig,
  saveConfig,
  REMINDER_EVERY_S,
  WORDS,
  ABOLISHED_WORDS,
  LADDER,
  TERMINAL,
  CONTRACT_CODES,
  EMITTED_CODES,
  OPTIONAL_CODES,
  ABOLISHED_CODES,
  gate,
  refuse,
  sanitize,
  renderLine,
  formatTs,
  unixTs,
  signNotice,
  noticeLine,
  verifyNotice,
  noticeCanonical,
  codeIdentity,
};
