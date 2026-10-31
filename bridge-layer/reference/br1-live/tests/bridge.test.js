'use strict';

const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const { spawnSync } = require('child_process');
const os = require('os');
const path = require('path');

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'bridge-devcage-test-'));
const configPath = path.join(tmp, 'config.json');
fs.writeFileSync(configPath, JSON.stringify({
  operator_id: '847445853584883712',
  bot_id: '100000000000000002',
  role_ids: ['100000000000000003'],
  guild_id: '100000000000000004',
  channel_id: '100000000000000005',
  pane: 'seat',
  peers: [],
  token_file: path.join(tmp, 'token'),
  state_dir: path.join(tmp, 'state'),
  log: path.join(tmp, 'state', 'events.jsonl'),
  answers: path.join(tmp, 'state', 'answers.jsonl'),
}));
process.env.BRIDGE_CONFIG = configPath;

const B = require('../bridge');
const { Recorder } = require('../state');

const CFG = B.CFG;
const STRANGER = '361033318273384449';
const FOREIGN_ROLE = '999999999999999999';

function msg(over = {}) {
  const m = {
    id: '1563900000000000001',
    channel_id: CFG.channel_id,
    guild_id: CFG.guild_id,
    author: { id: CFG.operator_id, bot: false },
    mentions: [{ id: CFG.bot_id, bot: true }],
    mention_roles: [],
    dm: false,
    content: `<@${CFG.bot_id}> status`,
    ...over,
  };
  return m;
}

test('C3/C6: operator ping accepted, instruction stripped', () => {
  assert.deepStrictEqual(B.gate(msg()), { action: 'accept', code: null, instruction: 'status' });
});

test('C4: a mention of the bot role is an address', () => {
  const out = B.gate(msg({ mentions: [], mention_roles: [CFG.role_ids[0]], content: `<@&${CFG.role_ids[0]}> status` }));
  assert.strictEqual(out.action, 'accept');
});

test('C5/R7: a bot ping plus a stranger is accepted and the stranger survives as content', () => {
  const out = B.gate(msg({
    mentions: [{ id: CFG.bot_id }, { id: STRANGER }],
    mention_roles: [FOREIGN_ROLE],
    content: `<@${CFG.bot_id}> <@${STRANGER}> <@&${FOREIGN_ROLE}> do it`,
  }));
  assert.strictEqual(out.action, 'accept');
  assert.match(out.instruction, new RegExp(STRANGER));
});

// ---- the three arms this work order is accepted on (C5/R7: a ping to this bot is a sufficient address;
// every other mention in the same message is content and must survive into the instruction).
test('gate_bot_ping_with_others_accepted', () => {
  const OTHER_BOT = '1562477564822425650'; // a real bot in the eligible guild, refused only as an author
  const out = B.gate(msg({
    mentions: [{ id: CFG.bot_id, bot: true }, { id: OTHER_BOT, bot: true }],
    mention_roles: [FOREIGN_ROLE],
    content: `<@${CFG.bot_id}> <@${OTHER_BOT}> <@&${FOREIGN_ROLE}> do it`,
  }));
  assert.strictEqual(out.code, null, `refused: ${out.code}`);
  assert.strictEqual(out.action, 'accept');
  // the other party is still in the instruction, markup and all - not stripped, not a reason to refuse
  assert.ok(out.instruction.includes(`<@${OTHER_BOT}>`), `other user lost: ${out.instruction}`);
  assert.ok(out.instruction.includes(`<@&${FOREIGN_ROLE}>`), `other role lost: ${out.instruction}`);
  assert.ok(!out.instruction.includes(`<@${CFG.bot_id}>`), `own address not stripped: ${out.instruction}`);
});

test('gate_stranger_only_refused', () => {
  const out = B.gate(msg({
    mentions: [{ id: STRANGER, bot: false }],
    mention_roles: [],
    content: `<@${STRANGER}> status`,
  }));
  assert.strictEqual(out.action, 'refuse');
  assert.strictEqual(out.code, 'pinged_other_user');
});

test('gate_no_mention_refused', () => {
  assert.strictEqual(B.gate(msg({ mentions: [], mention_roles: [], content: 'status' })).code, 'pinged_nobody');
  // a role this bot does not hold is not an address to it (R7), and a role is not a user either
  assert.strictEqual(B.gate(msg({ mentions: [], mention_roles: [FOREIGN_ROLE], content: 'status' })).code, 'pinged_nobody');
});

test('C5: a message that never pinged the bot is refused with who it addressed', () => {
  assert.strictEqual(B.gate(msg({ mentions: [], mention_roles: [], content: 'status' })).code, 'pinged_nobody');
  assert.strictEqual(B.gate(msg({ mentions: [{ id: STRANGER }], mention_roles: [], content: `<@${STRANGER}> status` })).code, 'pinged_other_user');
  assert.strictEqual(B.gate(msg({ mentions: [], mention_roles: [FOREIGN_ROLE], content: `<@&${FOREIGN_ROLE}> status` })).code, 'pinged_nobody');
});

test('C7/C6/C10/C8/C9/C11: distinct refusals', () => {
  assert.strictEqual(B.gate(msg({ author: { id: '9', bot: true } })).code, 'bot_author');
  assert.strictEqual(B.gate(msg({ author: { id: STRANGER, bot: false } })).code, 'other_author');
  assert.strictEqual(B.gate(msg({ dm: true, guild_id: null, channel_id: '9', author: { id: STRANGER, bot: false } })).code, 'dm_stranger');
  assert.strictEqual(B.gate(msg({ channel_id: '9' })).code, 'wrong_channel');
  assert.strictEqual(B.gate(msg({ guild_id: '9' })).code, 'wrong_guild');
  assert.strictEqual(B.gate(msg({ content: `<@${CFG.bot_id}>` })).code, 'empty');
});

test('C14-C17: one line, id carried, newlines flattened', () => {
  const line = B.renderLine('1563900000000000002', 'one\ntwo\rthree', '2026-10-25T12:00:00Z');
  assert.ok(line.endsWith('\n'));
  assert.strictEqual(line.split('\n').length, 2);
  assert.match(line, /one two three/);
  assert.match(line, /msg=1563900000000000002/);
  const grammar = new RegExp(B.CONTRACT.line.directive_grammar.replace(/\(\?P</g, '(?<'));
  assert.ok(grammar.test(line));
});

test('C19/C20: notice shape, signature, truncation and cross-class', () => {
  const key = '11'.repeat(32);
  const unsigned = B.noticeLine('7', 20, 1792710000, B.signNotice('7', 20, 1792710000, null));
  assert.match(unsigned, /sig=none/);
  const shape = new RegExp(B.CONTRACT.notice.shape_grammar.replace(/\(\?P</g, '(?<'));
  assert.ok(shape.test(unsigned));

  const sig = B.signNotice('7', 20, 1792710000, key);
  assert.strictEqual(sig.length, 64);
  const signed = B.noticeLine('7', 20, 1792710000, sig);
  assert.deepStrictEqual(B.verifyNotice(signed, key, 1792710000), { rc: 0, status: 'ok' });

  const truncated = signed.replace(/sig=[0-9a-f]{64}/, 'sig=' + '0'.repeat(63));
  assert.notStrictEqual(B.verifyNotice(truncated, key, 1792710000).rc, 0);
  const flipped = signed.replace(/sig=([0-9a-f]{63})([0-9a-f])/, (_, a, b) => 'sig=' + a + (b === '0' ? '1' : '0'));
  assert.notStrictEqual(B.verifyNotice(flipped, key, 1792710000).rc, 0);
  assert.notStrictEqual(B.verifyNotice('[BRIDGE kind=instruction msg=7 minutes=20 ts=1792710000 sig=' + '0'.repeat(64) + ']', key, 1792710000).rc, 0);
});

test('C18/C29: the box emits declared words and codes, and not the optional thread code', () => {
  assert.deepStrictEqual([...B.WORDS].filter((w) => !B.WORDS.has(w)), []);
  assert.ok(B.EMITTED_CODES.every((c) => B.CONTRACT_CODES.includes(c)));
  assert.ok(!B.EMITTED_CODES.includes('thread_not_in_scope'));
  const missing = B.CONTRACT_CODES.filter((c) => !B.EMITTED_CODES.includes(c) && !B.OPTIONAL_CODES.has(c));
  assert.deepStrictEqual(missing, []);
});

test('C21/C24/C25/C26/C27/C32: the record ladder is legal and a restart closes it', () => {
  const rec = new Recorder({ ...CFG, state_dir: path.join(tmp, 'state2'), log: path.join(tmp, 'state2', 'events.jsonl'), answers: path.join(tmp, 'state2', 'answers.jsonl') });
  rec.start();
  const m = msg({ id: '42' });
  assert.ok(rec.accepted(m, 'status'));
  assert.strictEqual(rec.accepted(m, 'status'), null); // C26
  rec.held('42');
  rec.injected('42');
  rec.delivered('42');
  rec.reply('42', 'done');
  rec.answered('42', 'done');
  rec.reminder('42', 20, false);
  assert.strictEqual(rec.get('42').reminders, 0); // terminal: no reminder after an answer

  const rows = rec.readAll();
  const events = rows.map((r) => r.event);
  assert.ok(events.includes('start'));
  assert.ok(events.includes('accepted'));
  assert.ok(!events.includes('notice10'));
  const words = new Set(events);
  assert.ok([...words].every((w) => B.WORDS.has(w)));
  // A new process closes the open request and writes a fresh start window.
  const rec2 = new Recorder({ ...CFG, state_dir: path.join(tmp, 'state3'), log: rec.logPath, answers: rec.answersPath });
  const { abandoned } = rec2.start();
  assert.deepStrictEqual(abandoned, []);
});


test('R9: a config naming another operator fails closed', () => {
  const bad = path.join(tmp, 'bad-operator.json');
  fs.writeFileSync(bad, JSON.stringify({ ...CFG, operator_id: '999999999999999999' }));
  const entry = path.join(__dirname, '..', 'bridge.js');
  const r = spawnSync(process.execPath, ['-e', 'require(process.env.BRIDGE_TEST_ENTRY)'], {
    env: { ...process.env, BRIDGE_CONFIG: bad, BRIDGE_TEST_ENTRY: entry },
    encoding: 'utf8',
  });
  assert.notStrictEqual(r.status, 0, 'a non-Geo operator must not load');
  assert.match(String(r.stderr), /not the pinned operator/);
});
