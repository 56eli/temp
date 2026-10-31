# 10 — Feature menu: what you need, what you can skip

*[agent: 2026-10-31 — sb3. This is the requested "features they may or may not need" list. Verdicts
are advice, not authority; the rule ids point at the normative text.]*

Read the tiers as: **Tier 0** — without this you have a different thing, not this layer. **Tier 1** —
take it unless you have a reason not to; the failures it prevents are the ones that cost trust.
**Tier 2** — genuinely optional, pick per environment. **Tier 3** — skip on a first build; they are
answers to problems you may not have.

---

## Tier 0 — the irreducible core

| # | feature | rule | what it buys | if you skip it |
|---|---|---|---|---|
| 1 | **A gate with a closed refusal-code set** | C3, C13, C29 | every non-instruction has a name; silence is diagnosable | you get "the bridge is broken" instead of "wrong_channel" |
| 2 | **Operator pin by id, in code** | C6, R9 | an app transfer, team change or careless config edit cannot add an author | a second human can instruct your agent by editing JSON |
| 3 | **One eligible channel + the operator's DM** | C8, C10 | the surface is bounded; DMs get their own diagnosis | every channel the bot is in becomes an instruction surface |
| 4 | **Address by mention (bot or a role it holds)** | C4, C5, C7 | unambiguous "this is for you"; other mentions stay content | you must parse intent from text, which fails silently |
| 5 | **One-line pane injection with the message id** | C14–C17 | the agent sees a request, not a chat log; the id is the handle for the answer | multi-line prompts, mention markup and control chars reach the model |
| 6 | **Ack once, keyed by message id** | C21 | the human knows the order landed, before any work | silence while the agent thinks, and double-acks after a poll overlap |
| 7 | **Reply tool by request id** | C18 | `delivered`/`answered` exist only through one path; an answer to nothing is refused | answers can be posted that belong to no request, leaving requests open |
| 8 | **Append-only event log in a closed vocabulary** | C18, C29 | a silent bridge is debuggable with `grep`; conformance can judge history | you are back to attaching a debugger |
| 9 | **Terminal state is final** | C27 | a late or duplicate answer is a decision, not a second outcome | double posts, double receipts, and a request that "reopens" |
| 10 | **One message id = one request** | C26 | dedupe without a database | a poll overlap acks and injects twice |
| 11 | **Heartbeat written by the loop** | C30 | distinguishes "process gone" from "loop stopped" | a hung pane looks exactly like a healthy bridge |
| 12 | **Single-writer lock** | C30 (operational word) | two loops on one token cannot double-post | the worst failure mode in the estate's history: silent duplication |

**The smallest useful bridge** is #1–#8 plus #11. #9–#12 are cheap and each removes a whole class of
"it worked, then it didn't" bug reports.

---

## Tier 1 — take unless you have a reason not to

| # | feature | rule | what it buys | cost / risk | skip if |
|---|---|---|---|---|---|
| 13 | **Restart window (relay nothing older than the process)** | C24, R3, R8 | no stale instruction replay after a crash; no burst of historical answers | an instruction arriving during the gap is lost — stated, chosen | you can tolerate replay, and can prove your queue is idempotent (harder than it sounds) |
| 14 | **Reminder every 20 min from entry, channel + pane** | C22, R2, R7 | the one signal that separates "thinking" from "never saw it" | periodic noise for long tasks; two sinks to keep in sync | nobody waits on the answer (batch jobs, logs) |
| 15 | **Reminder is not an answer** | C23 | the answer slot stays honest; reminders cannot close a request | one extra rule to keep | never — this is a five-line invariant |
| 16 | **Retention: closing record outlives opening record** | C32 | stops a 3-day-old answered request from re-firing a reminder | a little thought about pruning | you keep state forever in memory, which is what the reference does |
| 17 | **Held queue in memory** | C25 | a pane that is briefly gone does not drop the instruction | dies with the process (by design) | your pane is always up and injection cannot fail (it can) |
| 18 | **Supervisor that distinguishes startup failure from crash** | C30 | no 2-second hot loop behind a "healthy" session | a few lines of shell | you have systemd `Restart=always` **and** read `NRestarts` |
| 19 | **Code identity on every start** | C31 | a fix and a restart are distinguishable; runs can quote what they measured | a hash over four files | you deploy immutably and can name the image digest instead |
| 20 | **Deployment sheet that is allowed to differ** | `BOXES.md` | boxes can be correct *and* different; drift becomes a row, not a bug | one document to maintain | you run exactly one box |
| 21 | **Contract as one file with a machine block** | C1, C28 | code and rules cannot disagree; the checker can read both | one file to own, commits to make | you enjoy two sources of truth |
| 22 | **Conformance suite + adapter seam** | C28, `[adapter]` | every claim is measurable from outside | writing a 9-op adapter; keeping arms green | you do not intend to change the layer again (you will) |

---

## Tier 2 — genuinely optional, choose per environment

| # | feature | rule | take it if | skip it if | what you lose |
|---|---|---|---|---|---|
| 23 | **Role-mention addressing** | C4 | an ops role should be able to page the agent | the bot has no dedicated role | one of two address forms; the bot's own `<@id>` still works |
| 24 | **DM lane for the operator** | C8, C10 | the operator wants a private channel | the channel is the only surface you want | private instructions; DMs then become `wrong_channel` (acceptable, but say so) |
| 25 | **Peer lane (other bots may instruct)** | C7 | you have an orchestrator bot that issues work | any bot author should be refused | agent-to-agent instructions; the default (empty peers) is safer |
| 26 | **Thread policy** | `thread_not_in_scope` (optional code) | threads under the channel should be a separate, named refusal | threads should just be `wrong_channel` | a distinct diagnosis; nothing functional |
| 27 | **Attachments** | C33 (branch head only) | people paste logs, images, patch files | text is enough | file input; attachment-only messages are refused `empty` |
| 28 | **Signed notices (HMAC key)** | C19, C20 | you need to prove a reminder came from the bridge | you trust the pane's own input path | the signed half of C20; you keep the shape and `sig=none` (R6) |
| 29 | **Multi-part answers (split at 1,990)** | transport | answers exceed 2,000 chars (they often do) | your answers are short | long answers are rejected by Discord, or truncated by you (worse) |
| 30 | **Mass-mention suppression on outbound** | transport | always — an answer must never ping `@everyone` | never skip | a quoted mention pings the channel |
| 31 | **Config written back at first ready** | convenience | you want `bot_id`/roles discovered rather than typed | you prefer a static config | two fields to fill by hand |
| 32 | **`run.sh` control verbs** | ops | start/stop/status is done by humans | your supervisor is the only interface | a status command that can tell "session up" from "loop live" |
| 33 | **Log replay (`--log`)** | C28 | you have history and want to audit it | your log is young | a whole-log audit; the live arms still work |

---

## Tier 3 — skip on a first build

| # | feature | why it is in the contract, and why you may not want it yet |
|---|---|---|
| 34 | **`answered-with-receipt` / `answered-without-receipt` / `no-receipt` states** | They support a receipt mechanism the reference box does not use (it writes `receipt-written` after `answered`). The transition table legalises them so other boxes can. Adopt only if you actually have a receipt path; otherwise they are vocabulary you never write. |
| 35 | **`injected-queued`, `injected_held`, `ticker-*`, `peer_filed`, `repair-*`, `expired`** | Words from other boxes' histories, declared so logs stay comparable. The Node reference emits none of them. Declaring a word costs nothing; emitting one you do not need costs clarity. |
| 36 | **A shared multi-tenant bridge** | `docs/COMMS-LAYER.md` describes one bridge routing for many bots. It was designed 2026-09-28 and **never built**; the deployed layer is one process per agent. Read it as history, not as an option you are missing. |
| 37 | **A reference implementation kept for can-fail** | v7 deleted it in favour of three mutant adapters. Maintaining two implementations is the cost the cut removed. |
| 38 | **Generated manifests / codegen between prose and machine form** | Also deleted: one file read twice replaced a generator plus a generated artefact plus a comparator. |
| 39 | **A "security agent" in the bridge** | Explicitly rejected in the 2026-09-28 design: the bridge must make no model call and spend no per-message tokens. Keep verdicts mechanical. |
| 40 | **Length limits, content filters, per-bot pacing** | The first is withdrawn (R7); the second is a different layer's job; the third is a problem you have at a scale this layer was not built for. |

---

## Decisions the contract deliberately leaves to you

These are not features; they are choices each deployment must make and *write down* somewhere. The
`BOXES.md` deployment sheet exists for exactly this.

| choice | the contract says | br1's answer |
|---|---|---|
| supervisor | three axes must have evidence (C30) | tmux + `supervise.sh` on two boxes, systemd on one, systemd user unit + doctor on another |
| retention window | closing record ≥ opening record (C32) | in-memory map, no pruning; the whole log replays |
| thread policy | optional code, may be absent | absent: a thread is `wrong_channel` |
| peers | a set, may be empty (C7) | empty on all four |
| notice key | may be absent; then label unsigned (C20/R6) | absent on the boxes measured; one box has a key |
| attachments | C33 on the head, not in v7 | not deployed |
| log rotation | not specified | none; append-only files |
| what happens on post failure | not specified | logged to stderr, request left open, no retry |

## A "take this, skip that" starter

If you want the smallest conformant thing that still earns trust:

```
TAKE:  1–12 (core), 13 (restart window), 14–16 (reminders + retention), 18–19 (supervisor, identity),
       21–22 (one-file contract + the gate/log arms of the suite), 27 only if you need files,
       29–30 (transport), 32 (status)
SKIP:  23–26 (role/DM/peers/threads) until asked, 28 (signing) until you have a key store,
       31 (config write-back) if you like static configs, 33–40
```

That list is six small files, one contract, one shell supervisor, and an adapter — roughly what the
devcage implementation is (12 files, ~1,700 lines including tests).
