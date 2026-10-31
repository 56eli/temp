#!/usr/bin/env node
'use strict';

// The reply tool. C18: `delivered` and `answered` exist only by request id, through this command.
// It refuses an id the loop does not hold, so an unattributed answer cannot be posted by accident.
const fs = require('fs');
const path = require('path');
const { CFG } = require('./bridge');

function usage() {
  process.stderr.write('usage: reply.js <message-id> <text> [--force]\n');
}

function main(argv) {
  // Only a TRAILING --force is the flag: a legitimate standalone "--force" inside the answer text
  // must not be swallowed (argv.includes removed every occurrence).
  const force = argv.length > 1 && argv[argv.length - 1] === '--force';
  const args = force ? argv.slice(0, -1) : argv;
  if (args.length < 2) {
    usage();
    return 2;
  }
  const id = String(args[0]);
  const text = args.slice(1).join(' ');
  if (!text.trim()) {
    usage();
    return 2;
  }
  const logPath = CFG.log || path.join(CFG.state_dir || '/home/dev/.local/state/bridge', 'events.jsonl');
  let open = false;
  try {
    for (const line of fs.readFileSync(logPath, 'utf8').split('\n')) {
      if (!line.trim()) continue;
      let rec;
      try { rec = JSON.parse(line); } catch (_) { continue; }
      if (String(rec.id) !== id) continue;
      if (rec.event === 'accepted') open = true;
      if (rec.event === 'answered' || rec.event === 'abandoned_restart') open = false;
    }
  } catch (_) {
    open = false;
  }
  // C18 is about the loop that holds the request, not about a file that still mentions it: with the
  // loop dead, an id the log shows open would be dropped on the next start() as abandoned_restart, so
  // reporting "queued" would be a promise nothing keeps. The heartbeat is the loop's own evidence.
  let hbAgeS = null;
  try {
    let last = null;
    for (const line of fs.readFileSync(logPath, 'utf8').split('\n')) {
      if (!line.trim()) continue;
      let rec;
      try { rec = JSON.parse(line); } catch (_) { continue; }
      if (rec.event === 'heartbeat' && rec.ts) last = Date.parse(rec.ts);
    }
    if (last) hbAgeS = Math.round((Date.now() - last) / 1000);
  } catch (_) { hbAgeS = null; }
  const staleAfter = 90; // 3 x the loop's 30 s heartbeat
  if (hbAgeS === null || hbAgeS > staleAfter) {
    if (!force) {
      process.stderr.write(
        `refused: the loop is not live (${hbAgeS === null ? 'no heartbeat record' : `last heartbeat ${hbAgeS}s ago`}) ` +
        '- nothing was queued and nothing will be posted' + '\n'
      );
      return 4;
    }
    process.stderr.write(`warning: the loop is not live (${hbAgeS === null ? 'no heartbeat record' : `last heartbeat ${hbAgeS}s ago`}) - recording only\n`);
  }
  if (!open && !force) {
    // C18: no open request means no answer slot. Exit 4 is the documented refusal.
    process.stderr.write(`refused: no open request ${id} (use --force to record anyway)\n`);
    return 4;
  }
  const answers = CFG.answers || path.join(CFG.state_dir || '/home/dev/.local/state/bridge', 'answers.jsonl');
  fs.mkdirSync(path.dirname(answers), { recursive: true, mode: 0o700 });
  const rec = { ts: new Date().toISOString(), reply_to: id, text, forced: force ? true : undefined };
  fs.appendFileSync(answers, JSON.stringify(rec) + '\n', { mode: 0o600 });
  process.stdout.write(`queued answer for ${id} (${text.length} chars)\n`);
  return 0;
}

process.exitCode = main(process.argv.slice(2));
