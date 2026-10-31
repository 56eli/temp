#!/usr/bin/env node
'use strict';

// The conformance seam. It speaks JSON on stdin/stdout and drives the same functions the loop uses:
// no second implementation of a rule lives here.
const {
  CFG,
  gate,
  renderLine,
  signNotice,
  noticeLine,
  verifyNotice,
  REMINDER_EVERY_S,
  WORDS,
  ABOLISHED_WORDS,
  EMITTED_CODES,
  CONTRACT,
} = require('./bridge');

function handle(req) {
  const op = req.op;
  switch (op) {
    case 'config':
      return {
        operator_id: CFG.operator_id,
        bot_id: CFG.bot_id,
        role_ids: CFG.role_ids || [],
        guild_id: CFG.guild_id,
        channel_id: CFG.channel_id,
        reminder_every_s: REMINDER_EVERY_S,
        pane: CFG.pane,
      };
    case 'classify': {
      const msg = req.msg || {};
      const cfg = req.cfg || CFG;
      return gate(msg, cfg, !!msg.dm);
    }
    case 'line':
      return { line: renderLine(req.msg_id, req.text, req.ts) };
    case 'sign': {
      const sig = signNotice(req.msg_id, req.minutes, req.ts, req.key_hex);
      return { line: noticeLine(req.msg_id, req.minutes, req.ts, sig) };
    }
    case 'verify':
      return verifyNotice(req.line, req.key_hex, req.ts);
    case 'vocabulary':
      return { words: [...WORDS].filter((w) => !ABOLISHED_WORDS.has(w)) };
    case 'codes':
      return { codes: EMITTED_CODES };
    case 'log':
      return { path: CFG.log || require('path').join(CFG.state_dir || '/home/dev/.local/state/bridge', 'events.jsonl') };
    case 'supervision':
      return {
        axes: CONTRACT.supervision.axes,
        evidence: CONTRACT.supervision.evidence,
      };
    default:
      return { error: `unknown op ${op}` };
  }
}

let raw = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (d) => { raw += d; });
process.stdin.on('end', () => {
  let out;
  try {
    out = handle(JSON.parse(raw || '{}'));
  } catch (err) {
    out = { error: `${err.name}: ${err.message}` };
  }
  process.stdout.write(JSON.stringify(out) + '\n');
});
