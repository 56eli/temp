# Rulings — the operator's words, and nothing but

This file overrides `CONTRACT.md`. It is not a summary of what the operator meant, and it is not a
record of what an implementer understood. Nothing enters this file without the operator's own
words and the date they were said. If a rule in `CONTRACT.md` has no entry here, it is either a
mechanical consequence or a proposal; the tag on it says which.

**Provenance of the quotes below.** Each was copied from the channel or the issue comment named
beside it, at the date given. Where a quote reached this file through another agent's comment
(issue `56eli/botrunner#218` is a mirror — every comment in it is posted by `56eli` on behalf of an
agent), the comment id is named so the words can be checked against their source.

---

## 2026-10-25 — the adoption of this contract

> GO AHEAD AND BUILD — SCOPE LOCKED TO: The clean fix, first part. Make the contract an artefact in
> the repository with one owner and real history, split into three files: a short normative contract
> (the exact grammar of the line typed into a pane, the refusal-code enum, the receipt vocabulary,
> the state transitions, the notice signature string), a per-box deployment sheet that is allowed to
> differ, and a rulings log where your verbatim words are the only thing that can override the
> contract. Second part — make conformance measurable rather than eyeballed. …

Source: operator message `1563987905763090433`, 2026-10-25 18:49Z, guild `1489236876736069662`,
channel `1561512381480181860`.

**What this adopts.** The five normative artefacts named above, the three-file split, the shared
black-box suite, and the generated manifest. Everything normative in `CONTRACT.md` rests either on
this instruction or on one of the rulings below.

## R8 — a restart is a new window, and nothing older is relayed

> yeah fix the restart items if you haven't. i don't want a restarting bridge to relay messages that are older than
> the bridge restart

Source: operator message `1564021358768160849`, 2026-10-25 21:02Z.

Encoded as **C24 extended** and as one function, `restart_window(state)`, with four effects and one stated cost:

| window | before R8 | after |
|---|---|---|
| inbound | `last_ids` persisted, so a restart asked Discord for messages newer than the last one it saw — including messages sent while the process was down | `last_ids` is cleared: the first poll of each channel baselines on the newest message and logs `baseline`, so nothing older is read |
| held queue | persisted and drained after a restart | dropped and counted (`restart-window` records `dropped_held`) |
| answers file | read from offset 0, so every historical answer was re-read (343 `unattributed` records in one burst at 20:51Z) | offset starts at the current end |
| receipts file | same class of defect, smaller blast radius | offset starts at the current end |
| idle clock | resumed from the previous process | set to the restart instant |

**The cost, said out loud:** a message that arrives *during* the restart gap is older than the process, so it is not
relayed. The operator chose silence over a relay of something stale, and the choice is recorded here rather than
discovered later.

## R7 — a ping to the bot is a sufficient address, and the reminder goes to the agent

Operator message `1564016114160115845`, 2026-10-25 20:41Z, answering the checklist item by item. Verbatim, only
the items that changed a rule:

> 8. It DOES NOT refuse a message that pings the bot and someone else, and names the other party. Any ping to bot
> is a valid request further specific with message contents addressing individual parties for custom requests.

> 9. "It refuses a foreign role mention, and says it was the role." the sentence doesn't make sense. How could a
> bot be mentioned by a role it doesn't possess?

> 10. redundant

> 13. any instruction is one discord message long at max so this is redundant

> 27. ... Actually reminders to the agent are a good thing because sometimes agents forget to answer. The reminder
> message could be something neutral like "BRIDGE REMINDER: A discord message hasn't been answered by you yet. The
> owner is still waiting for an answer on discord. If you are still working on the task you can finish it first,
> otherwise report back on discord."

> 36. However this one says it DOES deliver a reminder. Inconsistent

Encoded as five changes, each a record rather than a deletion:

| item | ruling | what changed |
|---|---|---|
| 8 | a bot ping is sufficient; other mentions are content | **C5 rewritten and raised to `[R]`.** Both refusals withdrawn: bot-ping-plus-stranger and bot-ping-plus-foreign-role. The arm `gate_bot_ping_with_others_accepted` replaces them and requires the other mentions to survive into the instruction |
| 9 | "how could a bot be mentioned by a role it doesn't possess?" | **`foreign_role` abolished.** It never described a real event: an unheld role is not an address to the bot, so a message carrying one is simply not addressed to the bot — `pinged_nobody` already says that |
| 10 | redundant | the item is gone; with C5 rewritten there is no "stranger" to except |
| 13 | a Discord message is already the bound | **C12 withdrawn (`[X]`), `too_long` abolished**, `[instruction]` keeps Discord's 2,000 only as a reference. `sanitise` still folds whitespace and still must not shorten: the truncation defect stays a defect whether or not a length rule exists |
| 27 + 36 | reminders to the agent are wanted | **C22 amended**: channel *and* pane. **C19's template replaced** with the operator's neutral sentence, keeping the request id and the `sig` field. Item 36 was inconsistent only because item 27 was wrong |

Note on item 9, since the question deserves an answer rather than an edit: Discord's `mention_roles` lists the roles
the *author typed* into the message, whether or not the recipient holds them. So `<@&X>` where X is not this bot's
role does reach the bridge as a role mention — but it addresses somebody else, not this bot. The earlier rule
refused it, which is the reading the operator called senseless, and he is right: the bot was never mentioned.

## R6 — the pane reminder is internal communication, so deliver it

> just allow the pane reminder, it's internal communication

Source: operator message `1564006392778592297`, 2026-10-25 20:03Z.

**Encoded as C20, raised from `[P]` to `[R]`, and as `[notice].no_key = "inject_labelled_unsigned"`.** With no
signing key the pane reminder is delivered, marked `sig=none` in the line itself; the channel reminder is
unchanged. This supersedes the earlier rule that no key means no injection: withholding a reminder the agent
needs, to protect a proof nobody was reading, was the wrong trade. The marker stays, because a signed line
proves the bridge wrote it and an unsigned one proves nothing — a reader must be able to tell which it holds.

## R5 — the cut, and no rule claimed as a ruling without the words

> 1. yes one normative file 2. yes delete the fixture 5. yes only sentences i said verbatim 6. yes to outliving 7. yes fix and restart bridge, don't restart anything else 8. yes diagnostics adapter

Source: operator message `1564002873191440426`, 2026-10-25 19:49Z.

**What this adopts.** One normative file (`CONTRACT.md`, prose and machine form together); the reference
fixture deleted, can-fail proved by mutating an adapter; **only verbatim sentences are rulings** — so the
seven rules in the table below stay `[P]` and the table stays; the new rule C32 ("a cancellation outlives
its obligation"); the six box fixes with a bridge restart and nothing else restarted; adapters for the
other two boxes as diagnostics only.

## R1 — an acknowledgement is posted at acceptance, before delivery

> 1) Yes i specifically want the "<@847445853584883712> on it." message to be posted when a prompt goes in, even queued.

Source: issue `56eli/botrunner#218`, comment `6353798060`, "Owner rulings, 2026-10-23".

**Encoded as C21.** Once per message id, at acceptance. Text is the operator's, verbatim; a
paraphrase is a defect, not a style.

## R2 — a reminder every 20 minutes from prompt entry, until an outcome

> 2) If the prompt came in via the bridge, then the bridge should remind every 20 minutes past prompt entry for you to answer on discord and turn off the reminder.

Source: same comment.

**Encoded as C22, and it supersedes v6 §3.** From **entry**, not from delivery — a prompt that never
reaches a turn still reminds. The reminder is a Discord post; it stops the moment any outcome exists.
This replaces the earlier 10-minute and 60-minute notices; those two sentences are hereby deleted,
not kept alongside.

## R3 — a restart skips the backlog

> 3) skip all new messages on restart, i will re-send them.

Source: same comment.

**Encoded as C24.** At startup the cursor moves to the newest message and every non-terminal request
is closed as `abandoned_restart`, silently. The trade is the operator's, stated by him in the same
ruling: **a crash loses in-flight prompts.** v6's in-flight `begin`/`done` journal, its 65-minute
queue lifetime and its "did you receive X" recovery path are deleted rather than reworded.

## R4 — E11 is the same setup on another machine

> 4) assume that E11 has the same setup as you on a different machine

Source: same comment.

**Encoded as the adapter boundary, not as a clause.** No rule may assume a shared process; a box is
reached by an adapter command (`conformance/run.py`, section ADAPTER), so `bugger`'s box is testable from here — and until somebody mounts that box's `bridge.py`, untested.

---

## Not on record — rules an implementer called rulings, with no words to show

Listed so that no future reader mistakes testimony for a quote. Each is currently tagged `[P]` in
`CONTRACT.md`'s `[rules]` block, which means: arguable, and cheap to change.

| rule | claimed as a ruling by | what is actually on record |
|---|---|---|
| C2 — silence for anything not addressed | `debugger`, `#218/6324678441` item 6 | an implementer's list of which sections were "operator rulings"; no quote |
| C4 — a role mention addresses the bot | v6 §1 (written by `bugger`) | the 93-second role-ping incident and the fix; no ruling quoted |
| C19 — the notice's signed line format | v6 §3 (written by `bugger`) | R2 establishes *that* a reminder exists, not how it is signed |
| C20 — no key ⇒ no injection | v6 §3 | an implementation decision, twice independently made; no ruling quoted |
| C23 — a reminder is not an answer | `bugger`, `#218/6353798060` | the operator distinguishes canned notices from answers; he never ruled the mechanism |
| C30 — three supervision axes | v6 §4 (written by `bugger`) | the operator ruled that supervision must survive a logout, per `#218` §4; the three axes are an implementer's decomposition |
| `thread_not_in_scope` | `sb2`, `#218/6347397857` | an incident (an instruction posted in a thread never arrived) and a proposal; no ruling |

**No row here may be raised by inference.** The operator's answer of 2026-10-25 19:49Z — "only sentences i
said verbatim" — makes the bar explicit: a rule is `[R]` when his words are above, and not otherwise.

If the operator wants any of these raised to `[R]`, the act is a sentence from him, added above with
its date — not an edit to the table.
