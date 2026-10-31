# 04 — The line and the pane

*[agent: 2026-10-31 — sb3. Rules C14–C17; the injection code is `reference/br1-live/bot.js`.]*

## The line

The bridge types **exactly one line** into the agent's pane:

```
[discord:addressed {ts} msg={msg}] {text}\n
```

Example, the instruction that produced this pack (seen in the agent's own prompt header at
2026-10-31T15:09:24Z):

```
[discord:addressed 2026-10-31T15:09:24Z msg=1566106827123466301] Your single task is to gather all relevant information on the bridge layer standard ...
```

Normative grammar (`[line].directive_grammar`):

```regex
^\[discord:(?P<kind>addressed) (?P<ts>\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ) msg=(?P<msg>[0-9]+)\](?: (?P<text>[^\r\n]*))?\n$
```

Note what the grammar *is*: one fixed kind word, a second-precision UTC timestamp, a numeric message
id, and an optional single-line text. A parser that accepts more or less than this is not
conformant (C15). The timestamp format is `%Y-%m-%dT%H:%M:%SZ` — no milliseconds, `Z`, not `+00:00`.

Why the id is the Discord message id (C16): the human already has it, the agent sees it, the log
records it, and the reply tool takes it as its only handle. There is no second id space to get
wrong.

## Sanitising the text

```js
String(text ?? '')
  .replace(/[\u0000-\u0008\u0009\u000B\u000C\u000E-\u001F\u007F]/g, '')  // control chars (incl. tab)
  .replace(/[\r\n]+/g, ' ')                                              // newlines → space
  .replace(/[ \t]+/g, ' ').trim()
```

Three properties a re-implementation must keep:

1. **One line.** A multi-line prompt is flattened before it is typed. A literal `\n` inside the text
   would make the pane scroll, and a terminal may treat some control characters as movement.
2. **No shortening.** Firmware v7 has no length rule (C12 withdrawn). Sanitising must not truncate,
   silently or otherwise. The defect that motivated C12 was an 1,801-character instruction delivered
   as 1,800 with no record.
3. **Whitespace folded, not removed.** `one\ntwo` becomes `one two`, not `onetwo`.

## Injection (reference: tmux)

```js
execFileSync('tmux', ['has-session', '-t', target], { stdio: 'ignore' })   // else held
execFileSync('tmux', ['send-keys', '-t', target, '-l', text])              // literal text
execFileSync('tmux', ['send-keys', '-t', target, 'Enter'])                 // the Enter key
```

Four things this gets right that a naive version does not:

* **`-l` sends text, not key names.** Without `-l`, a prompt containing `C-c` or `Up` is
  interpreted as keystrokes.
* **The trailing newline is the Enter key, not text.** `send-keys -l "...\n"` types a literal newline
  into the pane's input buffer; it does not submit. Send the text without its trailing newline, then
  send `Enter` as a key.
* **Anchor the target.** tmux resolves an exact name first, then by **prefix**, so `spac` can match
  `spac3` (or `spac2` first). Every target in the shipped scripts is written `=name` (here
  `=spac3:0.0`; `=` forces exact). Note that `has-session` accepts a session target that `send-keys`
  will reject as "can't find pane" — so the failure path must log tmux's own stderr, not "Command
  failed".
* **A failure is not an error, it is a hold.** If the pane is gone, the instruction is kept in memory
  and retried every 5 s for the life of the process (`held` → `injected`), and a restart closes it as
  `abandoned_restart` (C25/C24). Nothing is dropped silently while the process lives.

## What the pane must be

The pane is a **live agent session, not a shell**. The line is typed into whatever is reading that
pane; if it is a shell, the instruction becomes a command. Two operational rules follow, and they
are in the estate's bridge page because people got this wrong:

* never point two bridges at one pane;
* never type one agent's instruction into another agent's pane.

## Attachments (contract head only — not deployed on br1)

C33 (approved 2026-10-26 11:57Z, commit `16e4acd`) extends the line without changing its grammar:

```js
const lineText = [instruction, ...paths.map(p => `[attachment ${p}]`)].filter(Boolean).join(' ');
renderLine(message.id, lineText, message.createdAt)
```

* the file is fetched and written under `state_dir/attachments/<message_id>/` with mode `0600`;
* the file name is sanitised (`[^A-Za-z0-9._-]` → `_`, capped at 120 chars);
* the pane line carries **absolute paths**, one `[attachment <path>]` per file;
* `empty` now means *no text and no attachment*;
* the gate carries an `attachments` array on the message shape.

This is the clean way to grow the line: a bracketed addition the agent can parse, no change to the
directive, and a per-message directory that prevents collisions. If you implement it, also copy the
C11 rewording ("no text **and** no attachment") and the new arm.

## Common mistakes

| mistake | symptom |
|---|---|
| typing text and newline in one `-l` send | instruction sits unsubmitted in the pane |
| unanchored tmux target | instruction lands in the wrong seat's pane |
| truncating to a "safe" length | instruction silently shortened; no record |
| injecting the raw Discord content | mention tokens and markup reach the model; the agent sees a chat log, not a request |
| sending reminders without the notice shape | the agent cannot tell a reminder from a message, and scrolls past it |
| reusing the ack as an answer | request stays open; reminders fire (C23) |
