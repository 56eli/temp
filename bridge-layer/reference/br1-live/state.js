'use strict';

// The record of what the bridge did. It writes only declared words, and it writes the `start` record
// from which every conformance window opens (C24/C31). The file is the only durable memory: a restart
// deliberately forgets in-flight work.
const fs = require('fs');
const path = require('path');
const { WORDS, ABOLISHED_WORDS, LADDER, TERMINAL, codeIdentity } = require('./bridge');

function utc() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
}

class Recorder {
  constructor(cfg) {
    this.cfg = cfg;
    this.dir = cfg.state_dir || '/home/dev/.local/state/bridge';
    this.logPath = cfg.log || path.join(this.dir, 'events.jsonl');
    this.answersPath = cfg.answers || path.join(this.dir, 'answers.jsonl');
    this.requests = new Map();
    this.answersOffset = 0;
    this.lastIds = new Set();
    this.startedAt = Date.now();
    this.ensure();
  }

  ensure() {
    fs.mkdirSync(this.dir, { recursive: true, mode: 0o700 });
    try { fs.chmodSync(this.dir, 0o700); } catch (_) { /* not ours to change */ }
    for (const p of [this.logPath, this.answersPath]) {
      fs.mkdirSync(path.dirname(p), { recursive: true, mode: 0o700 });
      if (!fs.existsSync(p)) fs.writeFileSync(p, '', { mode: 0o600 });
      try { fs.chmodSync(p, 0o600); } catch (_) { /* ignore */ }
    }
    this.answersOffset = fs.statSync(this.answersPath).size;
  }

  write(event, fields = {}) {
    if (!WORDS.has(event)) throw new Error(`undeclared record word: ${event}`);
    if (ABOLISHED_WORDS.has(event)) throw new Error(`abolished record word: ${event}`);
    const rec = { ts: utc(), event, ...fields };
    fs.appendFileSync(this.logPath, JSON.stringify(rec) + '\n', { mode: 0o600 });
    return rec;
  }

  // ------------------------------------------------------------ restart (C24/R3/R8)

  start() {
    const prior = this.readAll();
    const lastBy = new Map();
    for (const rec of prior) {
      if (rec.id && LADDER.has(rec.event)) lastBy.set(String(rec.id), rec);
    }
    const abandoned = [...lastBy.entries()]
      .filter(([, rec]) => !TERMINAL.has(rec.event))
      .map(([id]) => id);

    this.write('start', {
      code_identity: codeIdentity(),
      pid: process.pid,
      covers: ['loop', 'reply_tool', 'notice_verifier'],
    });
    this.write('restart-window', {
      cleared_channels: 2,
      dropped_held: this.requests.size,
      replayed_answers: 0,
    });
    // R8: both file offsets start at the end, so history is not news.
    this.answersOffset = fs.statSync(this.answersPath).size;
    this.requests.clear();
    this.lastIds.clear();
    for (const id of abandoned) {
      this.write('abandoned_restart', { id });
    }
    this.write('binding', {
      bot_id: this.cfg.bot_id || null,
      operator_id: this.cfg.operator_id || null,
      channel_id: this.cfg.channel_id || null,
    });
    this.write('baseline', { channel_id: this.cfg.channel_id || null, id: null });
    return { abandoned };
  }

  readAll() {
    try {
      return fs
        .readFileSync(this.logPath, 'utf8')
        .split('\n')
        .filter(Boolean)
        .map((line) => {
          try { return JSON.parse(line); } catch (_) { return null; }
        })
        .filter(Boolean);
    } catch (_) {
      return [];
    }
  }

  // ------------------------------------------------------------ requests

  has(id) {
    return this.requests.has(String(id));
  }

  get(id) {
    return this.requests.get(String(id)) || null;
  }

  accepted(msg, instruction) {
    const id = String(msg.id);
    if (this.requests.has(id)) return null; // C26: one message id is one request
    const req = {
      id,
      instruction,
      entryAt: Date.now(),
      state: 'accepted',
      terminal: false,
      reminders: 0,
      dm: !!msg.dm,
      channel: msg.channel || null,
      channelId: msg.channel_id || null,
      operatorId: this.cfg.operator_id || null,
    };
    this.requests.set(id, req);
    this.write('accepted', { id, chars: instruction.length, dm: !!msg.dm });
    return req;
  }

  refused(msg, code) {
    this.write('refused', { id: String(msg.id || ''), code });
  }

  held(id) {
    const req = this.get(id);
    if (!req || req.terminal) return;
    req.state = 'held';
    this.write('held', { id: String(id) });
  }

  injected(id) {
    const req = this.get(id);
    if (!req || req.terminal) return;
    req.state = 'injected';
    this.write('injected', { id: String(id) });
  }

  delivered(id) {
    const req = this.get(id);
    if (!req || req.terminal) return;
    // `held` never reaches `delivered` directly; draining the queue is what injects it.
    if (req.state === 'held') this.injected(id);
    req.state = 'delivered';
    this.write('delivered', { id: String(id) });
  }

  reply(id, text, parts = 1) {
    this.write('reply', {
      reply_to: String(id),
      chars: String(text || '').length,
      parts: Number(parts) || 1,
    });
  }

  receiptWritten(id) {
    this.write('receipt-written', { id: String(id) });
  }

  answered(id, text) {
    const req = this.get(id);
    if (!req || req.terminal) return;
    req.terminal = true;
    req.state = 'answered';
    this.write('answered', { id: String(id), chars: String(text || '').length });
  }

  unattributed(id) {
    this.write('unattributed', { id: String(id), reply_to: String(id) });
  }

  reminder(id, minutes, signed) {
    const req = this.get(id);
    if (!req || req.terminal) return;
    req.reminders += 1;
    this.write(signed ? 'reminder' : 'reminder_unsigned', { id: String(id), minutes: Number(minutes) });
  }

  heartbeat() {
    this.write('heartbeat', {
      pid: process.pid,
      uptime_s: Math.floor((Date.now() - this.startedAt) / 1000),
      loop: true,
    });
  }

  pending() {
    return [...this.requests.values()].filter((r) => !r.terminal);
  }

  // ------------------------------------------------------------ answers written by the reply tool

  drainAnswers() {
    let stat;
    try { stat = fs.statSync(this.answersPath); } catch (_) { return []; }
    if (stat.size < this.answersOffset) this.answersOffset = 0; // truncation is a new file
    if (stat.size === this.answersOffset) return [];
    const fd = fs.openSync(this.answersPath, 'r');
    const buf = Buffer.alloc(stat.size - this.answersOffset);
    fs.readSync(fd, buf, 0, buf.length, this.answersOffset);
    fs.closeSync(fd);
    this.answersOffset = stat.size;
    const out = [];
    for (const line of buf.toString('utf8').split('\n')) {
      if (!line.trim()) continue;
      try { out.push(JSON.parse(line)); } catch (_) { /* a torn line is not an answer */ }
    }
    return out;
  }
}

module.exports = { Recorder, utc };
