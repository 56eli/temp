# What the bridge does — a checklist

39 items, in the order a message travels. Each names its rule, and the third column is what the conformance
suite says about the one box measured here (`sb2`, 2026-10-25 20:5xZ) — **measured**, **skip** (no seam on that box),
or **red**; **hand** means verified by hand with a recorded command but no arm; **unarmed** means neither, and is a
gap named rather than hidden. A checklist item nobody measures is a wish, which is why the third column exists.

## The gate — whether a message is an instruction at all

| # | the bridge … | rule | sb2 |
|---|---|---|---|
| 1 | accepts instructions only from the operator | C6 | measured |
| 2 | refuses a bot author, unless it is a declared peer on the peer lane | C7 | measured |
| 3 | accepts only in its eligible channel, or in the operator's DM with it | C8 | measured |
| 4 | requires the guild id to match when one is configured | C9 | measured |
| 5 | refuses a DM from anyone but the operator, as `dm_stranger` | C10 | measured |
| 6 | treats a mention of one of its own roles exactly like a mention of the bot | C4 | measured |
| 7 | runs every addressing test, in the declared order, and needs all of them | C3 | measured |
| 8 | It accepts a message that pings the bot *and* other users or roles, and carries those mentions into the instruction as content | C5, R7 | measured |
| 9 | It refuses only a message that does not address it, and says who was addressed instead | C5 | measured |
| 10 | is silent when not addressed: nothing in the channel, one refusal on the record | C2 | measured |
| 11 | refuses an instruction with nothing after the addressing prefix, as `empty` | C11 | measured |
| 12 | gives each refusal exactly one cause, and two causes never share a code | C5, C13 | measured |
| 13 | types exactly one line: the directive, then the text, then one newline | C14 | skip: no renderer seam |
| 14 | matches the declared line grammar exactly — more or less means non-conformant | C15 | skip: no renderer seam |
| 15 | puts the instruction's own Discord message id in the directive, so a reply can name it | C16 | skip: no renderer seam |
| 16 | removes control characters and flattens newlines, so the pane sees one line | C17 | skip: no renderer seam |
| 17 | writes only the writable words: declared, minus the abolished ones | C18 | measured |
| 18 | treats `injected` as transport evidence, never as an answer | C18 | unarmed |
| 19 | writes `delivered` and `answered` only through the reply tool, by request id | C18 | unarmed |
| 20 | refuses to post an answer whose request id it does not hold | C18 | hand: `refused: no instruction … rc=4`, 2026-10-25 19:5xZ |
| 21 | records the refusal as well as the acceptance, so silence leaves a trace | C2, C29 | unarmed |
| 22 | treats one Discord message id as one request, however often the poller sees it | C26 | measured |
| 23 | acknowledges once, keyed by message id, and before any answer | C21 | measured |
| 24 | reminds every twenty minutes from prompt *entry* until a terminal record exists | C22, R2 | hand + box suite: the conformance arm asserts only that the abolished words are gone |
| 25 | It puts reminders in the channel *and* in the pane, because an agent that forgets to answer needs the cue | C22 | unarmed |
| 26 | never treats a reminder as an answer, and never fills the answer slot with one | C23 | measured |
| 27 | holds an instruction it cannot inject yet, and drains it later in the same process life | C25 | measured |
| 28 | closes every non-terminal request silently at startup, as `abandoned_restart` | C24, R3 | measured |
| 29 | loses in-flight prompts on a crash — that trade is the ruling's, not a bug | C24 | measured |
| 30 | relays nothing older than its own start: the first poll baselines, the held queue is dropped, and both files resume at their end | C24, R3, R8 | measured |
| 31 | treats a terminal state as final: a late answer is not a second outcome | C27 | measured |
| 32 | retains the record that closes a request at least as long as the one that opens it | C32, R4 | measured |
| 33 | writes the reminder in your own sentence, with the id and the minutes, and the machine fields in the bracket | C19, R7 | measured |
| 34 | verifies a whole signature in constant time, and refuses a truncated or cross-class one | C20 | skip: no key on this box |
| 35 | It delivers the pane reminder with no key, marked `sig=none` | C20, R6 | measured |
| 36 | distinguishes a signed line from an unsigned one, so a reader knows what they hold | C20, R6 | measured, for the unsigned half |
| 37 | reports that a heartbeat proves the loop and never the process | C30 | skip: supervised by the runner |
| 38 | reports the identity of its running code at start, so a fix can be told from a restart | C31 | measured |
| 39 | is measured by a suite where `SKIP` is never `PASS`, and an unmeasured rule fails the run | C28, C29 | measured |

## What the bridge does **not** do

- **It does not know what you intended.** It acknowledges with `on it.` and reminds every twenty minutes; neither
  is agreement to a design. The reminder is the checkpoint — it is the moment to ask "is what is about to be built
  even the thing I meant?", and the bridge cannot ask it for you.
- It does not merge, install, or take a privilege lease on its own; those wait for a sentence from the operator.
- It does not post outside its channel, and it does not speak when it was not addressed.
- It does not recover an in-flight instruction after a restart. R3 chose silence over replay.

## How to use this list

Measured 2026-10-25 21:03Z, the 39 divide: **27 measured** · **6 skip** · **4 unarmed** · **2 hand**.

Not measured, by number: skip 13, 14, 15, 16, 34, 37 · unarmed 18, 19, 21, 25 · hand 20, 24.

An item with a rule id can be argued with by quoting the id; `CONTRACT.md` carries the rule and `RULINGS.md` says
whether it is the operator's words or an implementer's proposal. An item marked *skip* is not satisfied, it is
unmeasured — the command that accepts it must name it (`--allow-skips`). An item marked *red* is a defect with an
arm pointed at it, which is the only kind of defect that can be fixed and proved fixed.
