# 01 — Architecture

*[agent: 2026-10-31 — sb3, read from the running code, the contract package, and `docs/BRIDGES.md`]*

## The problem it solves

An agent runs inside a terminal pane. The human is on Discord. Neither should have to poll the
other, and the connection must not turn into "the agent reads raw Discord": that would put channel
traffic, other bots, strangers and mention noise into the model's context, and it would let anything
in the channel become an instruction.

So there is one small process between them that:

1. decides **what is an instruction** (the gate) and stays silent otherwise;
2. turns an instruction into **one typed line**, so the agent sees a request, not a chat;
3. gives every request an **id** that both sides can name (the Discord message id);
4. records **what happened**, in a closed vocabulary, so "it went silent" is diagnosable;
5. gives the agent a **single command** to answer, and refuses answers that belong to nothing;
6. reminds, acknowledges, and supervises — cheaply, without a model call.

## Components

| component | file (Node reference impl.) | job |
|---|---|---|
| contract loader | `bridge.js` | finds and parses the `toml` block in `CONTRACT.md`; derives codes, words, grammars, cadence, ladder. Throws if the file is missing. |
| gate + line + notice | `bridge.js` | pure functions: `gate()`, `renderLine()`, `signNotice()`, `noticeLine()`, `verifyNotice()`. No I/O except reading the notice key and config. |
| recorder | `state.js` | the only writer of the event log; owns the request map, the restart window, the answer-file offset, the heartbeat. |
| loop | `bot.js` | Discord gateway client; on message → gate → ack → inject; timers for held drain, answer drain, reminders, heartbeat; single-writer lock. |
| reply tool | `reply.js` | CLI: validate the request id, append to the answer queue. Exit 0 queued / 2 usage / 4 refused. |
| adapter | `adapter.js` | JSON-on-stdio seam for the conformance suite; calls the same functions the loop calls. |
| supervisor | `supervise.sh` | restarts the loop; deliberately dumb; proves only "process gone". |
| control script | `run.sh` | `start|stop|status|probe`; distinguishes session up from loop live; refuses to start without a token. |
| contract | `contract/CONTRACT.md` | normative rules, prose + machine block, one file. |
| conformance suite | `conformance/run.py`, `conformance/adapters/*` | black-box arms against any box via an adapter command. |
| checker | `tools/check.py` | blocks ⇄ arms ⇄ prose ⇄ documents must agree. |

## Data flow

### Inbound (human → agent)

```
Discord gateway  ──▶ messageCreate
                       │ ignore own id, system messages
                       ▼
                    messageShape()            ids, mentions, guild, channel, dm, content
                       ▼
                    gate(shape, cfg, dm)      closed set of refusal codes, or accept+instruction
                       ├── refuse ──▶ recorder.refused(id, code)     (silence in channel)
                       └── accept
                             ▼
                    recorder.accepted()       dedupe by message id (C26)
                             ▼
                    send(channel, ack)        "<@operator> on it." (mentions suppressed)
                             ▼
                    renderLine()              "[discord:addressed <ts> msg=<id>] <text>\n"
                             ▼
                    inject()                  tmux send-keys -l <text> ; send-keys Enter
                       ├── ok   ──▶ recorder.injected()
                       └── fail ──▶ recorder.held()   retried every 5 s, same process life
```

### Outbound (agent → human)

```
agent            reply.js <id> "<text>"        reads the log: is <id> open? is the loop live?
                       │ exit 4 and posts nothing if not (unless --force)
                       ▼
                 answers.jsonl  (append, one JSON object per line)
                       ▼
loop (every 1 s) drainAnswers()  reads from a byte offset to EOF
                       ▼
                 recorder.get(id)  ── no request / terminal ──▶ recorder.unattributed()  (not posted)
                       ▼
                 splitContent(text, 1990)      transport framing; C12 is withdrawn, there is no length rule
                       ▼
                 channel.send(..., allowedMentions: { parse: [] })
                       ▼
                 recorder.reply / delivered / answered / receipt-written
```

### Reminders (timer → both sinks)

```
every 20 min from entry, per open request:
    sign = HMAC-SHA256(key, "kind=notice;msg=..;minutes=..;ts=<unix>")   or "none"
    line = "<operator's sentence> (request <id>, <minutes> minutes) ... [kind=notice ts=.. sig=..]"
    post to the channel  +  inject into the pane
    record "reminder" (signed) or "reminder_unsigned"
```

## Why it is shaped this way

These are the design decisions that a re-implementation should copy or consciously reject; each is
argued in `reference/contract-v7/` (RULINGS, PROPOSAL, REVIEW).

| decision | reason | where |
|---|---|---|
| one contract file holding prose **and** a machine block | two forms drift; a generator plus a generated artefact is more code than the problem. One file read twice cannot disagree. | `[governance]`, `tools/check.py` |
| message id **is** the request id | the human, the agent and the log all already have it; a reply can name it with no lookup. | C16 |
| a *closed* refusal-code set, one cause per code | "it refused" is not a diagnosis; a code names the test that failed. | C3, C13, C29 |
| a *closed* record-word set, with `abolished` history | a retired word cannot come back by accident, and a log replay can flag an invention. | C18, C29 |
| restart forgets in-flight work | replaying a stale instruction is worse than losing it; the operator chose silence explicitly. | C24, R3, R8 |
| reminders from **entry**, not from delivery | a prompt that never reached a turn is exactly the one that needs reminding. | C22, R2 |
| reminders in the pane **and** the channel | the pane cue is for the agent; the channel post is for the human. | C22, R7 |
| unsigned reminders are delivered, labelled | withholding a reminder to protect a proof nobody reads was the wrong trade. | C20, R6 |
| one process per bot/token/pane, no shared daemon | boxes live in different containers and on different hosts; R4 forbids assuming a shared process. | `[adapter]`, R4 |
| black-box measurement through an adapter command | "an adapter exists" was a claim about a file; nine ops make it a claim about a seam. | `[adapter]` |
| can-fail proof by mutating an adapter | a suite that cannot go red is decoration; three mutants replace a second implementation. | C28, `--selftest` |
| identity of the running code on every `start` | a fix and a restart look identical from outside; a hash tells them apart. | C31 |

## Topology

One bridge per (bot token, pane). The boxes differ only in deployment (`BOXES.md` is the sheet that
is *allowed* to differ):

| axis | examples on br1 |
|---|---|
| supervisor | tmux-hosted loop; systemd `Type=simple`; systemd user unit + doctor timer |
| survives logout | `Linger=yes` on two boxes; unverified on one |
| loop-stopped detection | heartbeat age threshold; a watchdog that exits; a separate doctor unit |
| notice key | absent on three boxes, present on one |
| pane target | tmux session name per seat |

Nothing in the contract requires a particular supervisor. What it requires is that **three failure
axes each have their own evidence** (C30) — see `07-supervision-and-operations.md`.

## Scale and resource shape

Measured on sb3: one `node` process, a gateway WebSocket, four timers (1 s, 5 s, 5 s, 30 s), two
append-only files, no database. The event log grows by one heartbeat every 30 s (≈2,880 lines/day)
plus request records; sb3's file was 20,556 lines after ~3 days. This is a low-RAM design; the
original multi-tenant proposal (`docs/COMMS-LAYER.md`) is a *different, unbuilt* design — see
`11-porting-notes.md` §"What this is not".
