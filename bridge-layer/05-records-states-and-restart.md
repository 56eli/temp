# 05 — Records, states, restart, and the answer path

*[agent: 2026-10-31 — sb3. Rules C18, C21–C27, C31, C32; record examples are from the live sb3 log.]*

## The event log

One append-only JSONL file, `<state_dir>/events.jsonl`, mode `0600`:

```json
{"ts":"2026-10-31T15:09:24Z","event":"accepted","id":"1566106827123466301","chars":432,"dm":false}
{"ts":"2026-10-31T15:09:25Z","event":"injected","id":"1566106827123466301"}
{"ts":"2026-10-31T15:09:52Z","event":"heartbeat","pid":322,"uptime_s":275404,"loop":true}
```

* `ts` is UTC, second precision, `Z`.
* `event` is from the closed vocabulary in the contract (see §02). The recorder **throws** on an
  undeclared or abolished word, so a typo is a crash, not log noise.
* `id` is the Discord message id for anything about a request.
* Records are appended with `O_APPEND`, so a torn last line is possible after a crash; readers skip
  unparsable lines rather than failing.

A healthy chain for one request, measured live:

```
accepted            the gate let it in, ack posted
injected            the line is in the pane
reply               reply.js queued the answer (chars, parts)
delivered           the loop posted it to Discord
answered            the request is closed
receipt-written     the receipt was recorded
```

`injected` is **transport evidence only**: it proves the bytes reached the pane, nothing about
whether the model saw them. A receipt is not an answer; the bridge can prove delivery to the pane,
never comprehension.

## The lifecycle

```
                accepted ──▶ held ──▶ injected
                    │          │          │
                    │          │          ▼
                    │          │       delivered ──▶ answered (terminal)
                    │          │          │
                    └──────────┴──────────┴──▶ abandoned_restart (terminal)
```

The declared transitions (v7 `[states].transitions`):

```
new→accepted   accepted→held   held→accepted   held→injected   accepted→injected
injected→delivered   delivered→answered
accepted|held|injected|delivered→abandoned_restart
delivered→no-receipt   no-receipt→answered   no-receipt→abandoned_restart
delivered→answered-with-receipt   delivered→answered-without-receipt
injected→answered-with-receipt    injected→answered-without-receipt
injected-queued→answered-with-receipt / answered-without-receipt
injected-queued→delivered   held→injected-queued   injected→injected-queued
```

Terminal words are `answered` and `abandoned_restart`. Terminals are final (C27): a second answer
for the same id is not a second outcome, it is `--force` territory and remains unposted unless the
request is still open.

> **Reminder words are a trap in v7.** `reminder` and `reminder_unsigned` are listed in `ladder` but
> have no transitions, so a live reminder makes the replay report
> `injected → reminder_unsigned` and `reminder_unsigned → delivered` as illegal. Measured on sb3 on
> 2026-10-31 (4 violations in 20,556 records). Decide the fix (drop them from `ladder`, or add the
> two edges) before you make `log_transitions_legal` a release gate.

## Start, and the restart window (C24 / R3 / R8)

At startup the recorder writes, in this order:

```json
{"event":"start","code_identity":"8bc1b4517fa72e83","pid":322,"covers":["loop","reply_tool","notice_verifier"]}
{"event":"restart-window","cleared_channels":2,"dropped_held":0,"replayed_answers":0}
{"event":"abandoned_restart","id":"..."}          // one per non-terminal request known to the log
{"event":"binding","bot_id":"...","operator_id":"...","channel_id":"..."}
{"event":"baseline","channel_id":"...","id":null}
```

The operator's ruling (R3): *"skip all new messages on restart, i will re-send them."* R8 sharpened
it: *"i don't want a restarting bridge to relay messages that are older than the bridge restart."*
Encoded as four effects and one stated cost:

| what | before R8 | after |
|---|---|---|
| inbound cursor (`last_ids`) | persisted; a restart asked for messages newer than the last one seen, including ones sent while the process was down | **cleared**; the first poll baselines on the newest message |
| held queue | persisted and drained after restart | **dropped** and counted (`dropped_held`) |
| answers file offset | read from 0, so every historical answer was re-read (measured: 343 `unattributed` records in one burst at 2026-10-25 20:51Z) | starts at **current end** |
| receipts offset | same class of defect | starts at current end |
| idle clock | resumed | restart instant |

**The cost, said out loud:** a message that arrives *during* the restart gap is older than the
process, so it is not relayed. A crash loses in-flight prompts. That is the ruling's trade, not a
defect to paper over. `held` lives in memory only, which is why C25 ("drained later in the same
process life") does not contradict C24.

## Retention (C32)

The rule is not "keep N records". It is: **the record that closes a request is retained at least as
long as the one that opens it, and either record closes it.** The defect this removes was two maps
with independent 200-entry rings: for an old request the closing record was evicted first, the
request looked open again, and a reminder fired three days late (measured 2026-10-25T19:32Z, a
request answered 2026-10-22 re-fired after 4,103 minutes). Retention is by **age**, not by an
arbitrary count that happens to be equal. If you implement retention as "parse the log and keep a
window", make the window long enough that a request cannot outlive its own closing record — or do
what the reference does and keep no window at all, deriving state from the in-memory map.

## The answer path

The agent's only write path is the reply tool:

```sh
node reply.js <request-id> "<text>" [--force]
```

Exit codes: `0` queued, `2` usage, `4` refused (nothing queued, nothing will be posted).

What it checks, in order:

1. **`--force` is a trailing flag only.** A standalone `--force` inside the answer text is content.
2. **Is the loop live?** It reads the log's last `heartbeat`; older than 90 s (3× the 30 s beat) or
   absent ⇒ exit 4, "the loop is not live - nothing was queued and nothing will be posted". This is
   deliberate: a dead loop drops the queue at the next start, so "queued" would be a lie.
3. **Is the request open?** It replays the log for that id: `accepted` opens, `answered` or
   `abandoned_restart` closes. No open request ⇒ exit 4.
4. **Append** `{ts, reply_to, text, forced?}` to `<state_dir>/answers.jsonl`.

The loop tails that file by byte offset every second. For each answer:

* unknown id, or terminal request ⇒ `unattributed` record, **nothing posted**;
* no postable channel ⇒ `unattributed`;
* otherwise ⇒ `reply` (chars, parts), `delivered`, post, then `answered` + `receipt-written`.

**The ordering matters.** `delivered` is written *before* the post resolves in the reference code;
`answered` after it resolves. If you change this, keep the invariant that a request whose answer
failed to post is never marked answered — the reference logs the failure to stderr and leaves the
request open, which is the safer direction but does mean a post failure needs an operator.

Long answers: Discord caps one message at 2,000 characters. The bridge has no length *rule* (C12
withdrawn); splitting is transport framing. The reference splits at 1,990 at a paragraph, line, or
space boundary and records `parts`. Every outbound message is sent with
`allowedMentions: { parse: [] }`, so an answer can never ping anyone, even if it quotes a mention.

## Idempotency

* One message id is one request (C26). The gate runs on every `messageCreate`; the in-memory map
  refuses a second `accepted` for the same id. There is no persisted "seen" set — the restart window
  is the recovery story, by design.
* A reply for an already-answered id does nothing (C27) unless forced, and a forced reply is
  recorded as `unattributed` rather than posted.
* Two loops on one token are prevented by a writer lock, not by idempotency (see §07).

## What the log is for

It is the only durable memory, and it is what makes a silent bridge diagnosable without attaching a
debugger. The runbook in §07 is a sequence of greps against this file. Two practical consequences:

* **Do not rotate it destructively** without preserving the last `start` record: the conformance
  log arms open their window at the last `start`.
* **Do not add words ad hoc.** `log_words_declared` and the recorder's throw both enforce the closed
  set; a new word is a contract change with an arm, not a debug print.
