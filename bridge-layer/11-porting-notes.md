# 11 — Porting notes: what is the rule and what is the box

*[agent: 2026-10-31 — sb3. For a reader who wants the layer on a different chat platform, a different
multiplexer, or a different language.]*

## Separate the three kinds of "it"

The contract exists to make this separation possible:

| layer | example | may you change it? |
|---|---|---|
| **rule** — what must be true of any conformant bridge | "an unaddressed message is silence, with one refusal recorded" | no, not without a ruling + a commit |
| **mechanism** — how the reference does it | "tmux `send-keys -l`, then `Enter`" | yes, freely |
| **incidental** — how this box happens to be deployed | "the tmux session is called `spac3`" | yes, and `BOXES.md` is where you say so |

A port is legitimate when every row in the first column still holds. The conformance suite is how
you prove it.

## Substitution table

| reference mechanism | what it is really doing | a port must preserve |
|---|---|---|
| Discord gateway + `messageCreate` | receive events for one bot identity | author id, guild id, channel id, mention ids, role ids, content, attachments, "is DM" |
| `mentions` / `mention_roles` | the platform's structured address tokens | *structured* address, not a regex over text — a quoted or escaped mention must not count |
| `allowedMentions: {parse: []}` | outbound messages cannot ping | answers/reminders/acks are never new instructions |
| tmux `send-keys -l` + `Enter` | type one line into a live terminal | exactly one line, submitted, no key-name interpretation |
| `has-session` | is the sink present | a failed injection is a *hold*, not a drop |
| `fs.appendFileSync` JSONL | durable append-only record | ordered, one JSON object per line, `ts` first, UTF-8 |
| byte-offset tail of `answers.jsonl` | the only IPC between agent and loop | no lost or duplicated answers, offset survives EOF |
| `setInterval(…, 1000/5000/30000)` | timers | heartbeat period and stale threshold must be consistent (3×) |
| `sha256(files)[:16]` | identity of running code | reported on every `start` |
| `reply.js` CLI | the agent's one write path | validates id + liveness, refuses rather than guessing |

## A language-neutral loop

```
on start:
    config  = load(config.json)                 # operator pinned in code, compared to config
    contract= parse_toml_block(CONTRACT.md)
    lock    = take(state_dir/loop.lock)          # stale pid (not this program) => take over
    close_backlog()                              # abandoned_restart for every open id in the log
    write(start, code_identity, pid)
    write(restart-window, dropped_held=0)
    write(binding); write(baseline)
    answers_offset = size(answers.jsonl)         # history is not news
    last_seen      = {}                          # cleared, first poll baselines

every event from the chat platform:
    if author is self or event is system: return
    shape = {id, channel, guild, author, mentions, roles, dm, content}
    v = gate(shape, cfg)
    if v.refuse: write(refused, id, code); return          # silence, one record
    if seen(id): return                                     # C26
    seen(id) = true; write(accepted, id)
    post(channel, ack(operator))                            # C21, before anything else
    line = render(id, sanitise(v.instruction), now)
    if inject(line): write(injected, id) else: hold(id)     # retried by a timer

every 1 s:
    for answer in tail(answers.jsonl, answers_offset):
        req = open_request(answer.reply_to)
        if not req: write(unattributed, answer.reply_to); continue
        write(reply, id, chars, parts)
        write(delivered, id)
        for part in split(answer.text, 1990): post(req.channel, part)
        write(answered, id); write(receipt-written, id)

every 5 s:
    for req in held: if inject(render(req)): write(injected, req.id)
    for req in open:
        due = floor((now - req.entry_at) / 1200)
        if due > req.reminders:
            minutes = due * 20
            line = notice(req.id, minutes, now, sign_or_none(req.id, minutes, now))
            post(req.channel, line); inject(line + "\n")
            write(reminder or reminder_unsigned, req.id, minutes)

every 30 s:
    write(heartbeat, pid, uptime, loop=true)
```

## Pitfalls that cost the br1 estate real time

1. **A newline through a literal send is not Enter.** It types a newline character. Send text, then
   the Enter key.
2. **Unanchored multiplexer targets match by prefix.** `spac` can hit `spac2` or `spac3`. Anchor
   (`=name`), and remember `has-session` may accept a target that `send-keys` rejects.
3. **A tmux session outlives the process.** `has-session` is not liveness; the heartbeat is.
4. **Restart re-read the answer file from offset 0** and produced 343 `unattributed` records in one
   burst, because R3 closes the backlog at startup. Offsets start at end-of-file.
5. **Two ring buffers with equal retention evict the closing record first**, so an answered request
   looks open and its reminder fires three days later. Retention must be by age, or closing-record
   retention must exceed opening-record retention.
6. **Truncation dressed as validation.** `sanitize()` both normalised and sliced; an 1,801-character
   order was delivered as 1,800 with no record.
7. **An empty `message.content` because an intent is off** looks like a gate bug (`empty` for every
   prompt). Check the portal before the code.
8. **Suppressed mentions don't reach `mentions`.** A message posted with `parse: []` cannot be an
   instruction — by design, and it will look like "the bot ignored me".
9. **A reply to another bot arrives with that bot in `mentions`** (Discord type 19), so it is
   `pinged_other_user` unless this bot is addressed too. Correct, not a regression.
10. **The role cache contains `@everyone` as the guild id.** Filter it out or a config full of roles
    will look wrong.
11. **A signed reminder's canonical form uses the Unix timestamp, not the rendered date.** Sign and
    verify must agree on which.
12. **`--force` inside answer text** — `argv.includes('--force')` eats a legitimate word. Only a
    trailing flag is a flag.
13. **Log words are a closed set.** An ad-hoc debug word turns a conformant box non-conformant and
    a replay red; use the declared operational words or change the contract.

## If your platform is not Discord

The contract is deliberately written in terms of *facts about a message* rather than Discord API
calls, but some rules are Discord-shaped and must be re-ruled, not silently translated:

| rule | Discord assumption | on another platform |
|---|---|---|
| C5 | a message can be addressed by a user mention | you need a structured address concept (Slack `<@U…>`, Matrix `m.mentions`) — a regex over text is not equivalent |
| C16 | message id is a stable snowflake string | any stable per-message id works; keep it a string |
| C20 | HMAC over a canonical string | platform-independent |
| C21 | a bot can post a message | needs send permission |
| C22 | DM/channel distinction | map to your direct-message concept |
| C33 | attachments have a fetchable URL | needs an authenticated download path |
| transport | 2,000-char message cap | yours will differ; keep the split threshold below it |

Anything you cannot map, make an **optional code** and an arm that SKIPs — do not quietly drop the
rule.

## What this layer is not

`docs/COMMS-LAYER.md` in the botrunner repo describes a **different** design: one shared multi-tenant
bridge routing for several bots, with verdict classes, pacing profiles and a per-(bot, guild) switch.
It was designed by the owner on 2026-09-28 and **never built**; its own text says so ("Nothing
described here is running on br1"). The layer in this pack is per-agent, one process per bot token,
and its standard is `CONTRACT.md` v7. If you want the shared router, you are designing a new system,
not porting this one — and the cheapest correct starting point is still this contract's gate and
record vocabularies, because they are what made three divergent bridges comparable.

## Porting checklist

- [ ] gate implemented as pure functions with no I/O (so the adapter can call it)
- [ ] codes, words, grammars, cadence and ladder **loaded** from the contract, not typed into code
- [ ] adapter exposing all nine ops; `null` where you have no seam
- [ ] event log append-only, closed vocabulary, `ts` UTC seconds
- [ ] answer queue append-only, tailed by offset, offset starts at end on start
- [ ] heartbeat from inside the loop, threshold 3× the period
- [ ] restart closes the backlog and forgets the queue
- [ ] `--selftest` green against your adapter
- [ ] your deployment sheet says how you satisfy each of the three supervision axes
