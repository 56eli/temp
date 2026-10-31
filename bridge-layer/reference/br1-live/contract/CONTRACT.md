# The bridge contract, v7

One artefact, one owner, real history. The prose below is for a reader; the block at the end is for a
machine; they are the same file so they cannot disagree. A behaviour that is not in this file does not
exist, and a gate fails on it (C29).

| file | job |
|---|---|
| `CONTRACT.md` | this contract: the rules, and the machine form of them |
| `RULINGS.md` | the operator's words — the only thing that can override a rule |
| `BOXES.md` | the deployment sheet: how each box meets these rules, and which were measured |
| `conformance/` | a black-box suite that drives any box through an adapter command |
| `REVIEW.md` | how to review this: reading order, the claims and how to check each, and what is not claimed |
| `PROPOSAL.md` | the plan the operator approved on 2026-10-25, and what was built against it (history) |

Tags: **[R]** a ruling, quoted verbatim in `RULINGS.md`; **[M]** a mechanical consequence of one;
**[P]** a proposal by an implementer, arguable and marked as such. Only a sentence from the operator
turns a `[P]` into an `[R]`.

## 1. The gate

Rules: C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C13. (C12 was withdrawn by R7 and is kept here as a record.)

A message is an instruction only if it passes every test, in `[addressing].order`. The author must be
the operator (C6); a bot author is refused unless it is a declared peer (C7); the channel must be the
eligible one or the operator's DM (C8) and the guild must match when one is configured (C9).

**A ping to the bot is a sufficient address (C5, R7).** Other user mentions and role mentions in the same message
are *content*: a request that names three meatbags for three different jobs is a normal request, and the agent reads
the mentions out of the text. This reverses the earlier rule, which refused such a message — that rule was written
after a stranger's `<@id>` reached the pane, and refusing the whole instruction was the wrong repair for it. What
reaches the pane is the text, and the text is what the operator wrote.

Only a message that does *not* address this bot is refused, and then the code says who it addressed instead: a user
makes it `pinged_other_user`, no address token at all makes it `pinged_nobody`. The operator's own id is never a
stranger. `foreign_role` is abolished (R7): a role this bot does not hold is not an address to the bot, so there is
nothing to diagnose.

There is no bridge-side length rule (C12 withdrawn by R7): a Discord message is already the bound. `sanitise` folds
whitespace and must still not shorten anything — silent shortening was the defect C12 was written after, and it
stays a defect whether or not a length rule exists.

## 2. The line

Rules: C14, C15, C16, C17.

The bridge types exactly one line into the pane, matching `[line].directive_grammar`: the directive,
the request id, the text on one line, one trailing newline. The id is the Discord message id, so a
reply can name it.

## 3. Records

Rules: C18, C29.

A bridge writes only the *writable* words — `[receipts]` minus `[receipts].abolished` — about a request.
`abolished` is history: readable in an old log, never writable by current code, so a retired word cannot come
back by accident. `injected` is transport evidence;
`delivered` and `answered` exist only through the reply tool, by request id. An answer carrying an id
the bridge does not hold is refused rather than posted, because it leaves the request it answers open.

## 4. States, acknowledgement, reminder, restart

Rules: C19, C20, C21, C22, C23, C24, C25, C26, C27.

Rulings R1–R3, quoted in `RULINGS.md`: acknowledge once, keyed by message id (C21); remind every 20
minutes from prompt *entry* until a terminal record exists, in the channel and never in the pane
(C22, amended by R7 so the reminder goes to the pane as well as the channel: "reminders to the agent are a good
thing because sometimes agents forget to answer"); at startup close every non-terminal request silently as
`abandoned_restart` (C24). R8 makes the window explicit: "i don't want a restarting bridge to relay messages that
are older than the bridge restart" — so `last_ids` is cleared (the next poll baselines instead of asking for
anything older), the held queue is dropped rather than drained, and the receipts and answers offsets start at the
current end of their files. The cost is stated rather than hidden: an instruction that arrives during the restart gap
is older than the process and is not relayed. A crash
loses in-flight prompts — that trade is the ruling's, not a defect to paper over.

C25 is not the opposite of C24, and the earlier text read as if it were: `held` lives in the process's
memory, so a restart closes it because the memory is gone. Held instructions are drained later *in the life
they arrived in*; that is the whole of the promise.

The reminder cadence is a formula, not a list: the n-th reminder is due at `n * [notice].every_s` after entry,
with no upper bound, so a box that reminds at 80 minutes is conformant rather than unnameable. `examples` in the
block are examples, and `[notice].minutes` is not a bound.

## 5. Retention

Rules: C32.

The record that closes a request is kept at least as long as the record that opens it, and either
record closes it. Two maps with equal retention evict the closing record first whenever the request is
old, so an answered request looks open again and its reminder fires — measured 2026-10-25T19:32Z, a
request answered three days earlier re-fired. Retention by age, not by a count that happens to match.

## 6. The notice

Rules: C19, C20.

Two rules were one, and that is why the rule about the notice's *shape* could be violated by the one box the
deployment sheet measured while no arm went red about it: shape and signature were written as a single rule that
needed a key.

C19 is the shape, and it is measurable on every box, key or no key. The shape is the operator's own sentence of
2026-10-25 20:41Z — "BRIDGE REMINDER: A discord message hasn't been answered by you yet …" — with the request id and
the minutes in the sentence and the machine fields in the trailing bracket: `[kind=notice ts=… sig=…]`.
`[notice].shape_grammar` is that sentence, matched exactly, because a reminder an agent cannot recognise at a glance
is a reminder it will scroll past. C20 is the signature: if a key is provisioned, verification compares the whole
signature in constant time, and a truncated, invented or cross-class signature is refused.

With no key the pane reminder is still delivered, marked `sig=none` in the line itself (R6: "just allow
the pane reminder, it's internal communication"). The marker is the point: a signed line proves the bridge
wrote it, an unsigned one proves nothing, and a reader must be able to tell which it is holding. R7 settled the
other half of the question — the reminder goes to the **pane as well as the channel**, because "reminders to the
agent are a good thing because sometimes agents forget to answer".

## 7. Supervision and identity

Rules: C30, C31.

Supervision covers three axes — process gone, loop stopped, no turn — each with its own evidence. A
heartbeat proves the loop, never the process. The running code reports its identity over the loop, the
reply tool and the notice verifier, and the set is named here so two boxes cannot differ silently.

## 8. Proof

Rules: C1, C28, C29.

Every arm in the block is implemented in `conformance/run.py` and declared here; `tools/check.py`
fails when the two disagree in either direction, and it also fails when a rule has no arm at all — the
direction that was missing, and the reason C14, C16, C21, C23, C25, C26, C27, C30 and C31 went unmeasured
while the suite was green. A rule that cannot be measured from outside a box is named in `[scope]` with its
reason; the checker refuses an excuse shorter than a sentence and refuses one for a rule that has an arm.

`SKIP` is never a pass, and the exit code is where that has to be true, because a machine reads nothing else:

| code | meaning |
|---|---|
| 0 | every declared arm ran and passed; skips only where `--allow-skips` names the rule |
| 1 | at least one arm failed |
| 2 | an arm was skipped that the command did not allow — an unmeasured rule is not a satisfied one |

The allowance is a command, not a setting, so a run that accepts a gap says so where the run is read. Can-fail is
shown by `run.py --selftest`: a proxy flips one answer from a real box, and the suite must go red.

A box is reached through one command with nine declared operations (`[adapter].ops`, each mapped to a callable in
the box's own code), and `tools/check.py --adapters` runs every adapter through every one of them. Without that, "an
adapter exists" was a claim about a file rather than about a seam — and the refusal-code check guessed at source
text instead of asking the box what it can emit.

## The machine form

```toml
version = "7"
date = "2026-10-25"
supersedes = "v6 (issue 56eli/botrunner#218, comment 6327219361, 2026-10-21T21:55Z)"

[governance]
# C1 — one owner, real history, and the ruling log is the only override.
owner = "sb2 (rebugger) — single writer; changes are commits, never edits to a document living in a chat"
# Every rule here is adopted by the operator's instruction of 2026-10-25 ("GO AHEAD AND BUILD — SCOPE
# LOCKED TO …", quoted verbatim in RULINGS.md). Only the rules tagged [R] also carry a verbatim ruling
# of their own; a rule claimed as a ruling by an implementer, without the words, is tagged [P] and listed
# under "not on record" in RULINGS.md.
rulings_file = "RULINGS.md"
proposal_marker = "[P]"

[rules]
# The registry: every rule the contract has, in one sentence each, tagged [R] ruling,
# [M] mechanical consequence, or [P] proposal. CONTRACT.md must contain exactly these ids;
# tools/check.py refuses a registry and a document that disagree in either direction.
C1 = "[M] one owner writes this file, and changes are commits — never edits to a document living in a chat"
C2 = "[P] a message that is not addressed is silence: the bridge says nothing, refuses nothing in the channel, and records one refusal"
C3 = "[M] a message is an instruction only if every addressing test in `[addressing].order` passes, and a refusal is one of `[codes]`, distinct, and named after the test that failed"
C4 = "[P] a mention of one of this bot's roles addresses it exactly as a mention of the bot does"
C5 = "[R] a ping to the bot is a sufficient address: other user mentions and role mentions in the same message are content for the request, never grounds for a refusal (operator, 2026-10-25 20:41Z)"
C6 = "[M] the author of an instruction is the operator"
C7 = "[M] a bot author is refused unless it is a declared peer on the peer lane"
C8 = "[M] an instruction arrives in the eligible channel or in the operator's DM with this bot"
C9 = "[M] when a guild id is configured, the message's guild must match"
C10 = "[M] a DM from anyone but the operator is refused as `dm_stranger`"
C11 = "[M] an instruction with no text after the addressing prefix is refused as `empty`"
C12 = "[X] withdrawn by the operator, 2026-10-25 20:41Z: a Discord message is already the bound, so a length refusal is a rule about nothing"
C13 = "[M] two different causes never share one code, and a code that is abolished is never emitted"
C14 = "[M] the bridge types exactly one line into the pane: the directive, then the text, then one newline"
C15 = "[M] `[line].directive_grammar` is normative: matching more or less than it means not conformant"
C16 = "[M] the id in the directive is the Discord message id of the instruction, so a reply can name it"
C17 = "[M] the typed line carries no newline inside it: control characters are removed and newlines become spaces"
C18 = "[M] a bridge records only the writable words in `[receipts]` (declared minus abolished), and `injected` is transport evidence only"
C19 = "[P] a pane reminder has one declared shape — the operator's neutral sentence of 2026-10-25 20:41Z, the request id, and a `sig` field that is 64 lowercase hex or the literal `none` — and the shape is measurable without any key"
C20 = "[R] a *signature* is verified as a whole in constant time; a truncated, invented or cross-class one is refused, and with no key the reminder is delivered with `sig=none`"
C21 = "[R] the first thing posted for an accepted prompt is the acknowledgement, once, keyed by message id"
C22 = "[R] a reminder is posted every 20 minutes from prompt entry until a terminal event exists, in the channel *and* in the pane: the pane reminder is the agent's cue to answer, and reminders to the agent are wanted (operator, 2026-10-25 20:41Z)"
C23 = "[M] a reminder is not an answer: it never occupies the answer slot of a request"
C24 = "[R] a restart closes every non-terminal request silently, and nothing older than the process is relayed: the first poll re-baselines, the held queue is dropped, and both file offsets start at the end (R3 + R8)"
C25 = "[M] an accepted instruction that cannot be injected yet is held in memory and drained later; it lives and dies with the process, so R3's silent close on restart is not a contradiction"
C26 = "[M] one Discord message id is one request, however many times the poller sees it"
C27 = "[M] a terminal state is final; a late answer is not a second outcome for the same request"
C28 = "[M] every arm is declared in this file, checked against the suite that implements it, and shown failing against a deliberate defect"
C29 = "[M] a refusal code or record word that is not in this file fails a gate"
C30 = "[M] supervision covers three axes — process gone, loop stopped, no turn — and each has its own evidence"
C32 = "[R] a cancellation outlives its obligation: the record that closes a request is retained at least as long as the record that opens it, and either record closes it"
C31 = "[M] the running code reports its identity, covering the loop, the reply tool and the notice verifier"

# ---------------------------------------------------------------- addressing (C2–C13)

[addressing]
rule = "C3"
# C3 — an instruction is a message that passes every test below, in this order.
# Two lanes, each with its own first test, then the content tests in one shared order:
#   bot_author -> (DM: dm_stranger | channel: other_author, wrong_guild, wrong_channel, thread_not_in_scope)
#   -> pinged_nobody -> pinged_other_user -> empty
# R7 removed two entries: `too_long` (a Discord message is already the bound) and `foreign_role` (a role the bot
# does not hold is not an address to the bot, so there is nothing to diagnose).
order = [
  "bot_author",
  "dm_stranger",
  "other_author",
  "wrong_guild",
  "wrong_channel",
  "thread_not_in_scope",
  "pinged_nobody",
  "pinged_other_user",
  "empty",
]
mention_keys = ["mentions", "mention_roles"]
dm_allowed = true

# C5 as amended by R7 (operator, 2026-10-25 20:41Z): "Any ping to bot is a valid request". A message that
# mentions this bot is an instruction whatever else it mentions — the other mentions are content the agent reads,
# and a custom request aimed at named parties is a normal case, not a refusal. Only a message that does *not*
# address this bot is refused, and then the code says who it addressed instead.
[addressing.not_addressed]
users = "pinged_other_user"
none = "pinged_nobody"

[codes]
rule = "C5"
# C5 — a refusal names exactly one of these. The set is closed: a box may not invent one,
# and two causes may not collapse into one code.
# `optional` is a declared capability gap, not a waiver: a box with no thread rules cannot emit
# `thread_not_in_scope`, and the code-set arm reads this list instead of hard-coding the exception.
optional = ["thread_not_in_scope"]
# Abolished: still readable in old logs, never emitted by current code, and the checker refuses an emitting box.
abolished = { too_long = "C12 withdrawn 2026-10-25 20:41Z: one Discord message is the bound", foreign_role = "C5 amended 2026-10-25 20:41Z: a role the bot does not hold is not an address to the bot at all, so the diagnosis has no meaning" }
bot_author = "[M] the author is a bot other than a declared peer"
other_author = "[M] the author is not the operator"
wrong_guild = "[M] the message's guild id is not the configured guild"
wrong_channel = "[M] the channel is neither the eligible channel nor the operator's DM"
thread_not_in_scope = "[P] a thread under the eligible channel is not an ordering surface (#218/6347397857)"
dm_stranger = "[R] a DM from anyone but the operator"
pinged_nobody = "[M] neither this bot nor one of its roles was mentioned"
pinged_other_user = "[M] a user who is neither this bot nor the operator was mentioned"
empty = "[M] nothing remains after the addressing prefix is stripped"

[instruction]
# The bound is the platform's: one Discord message, capped by Discord at 2,000 characters. There is no bridge-side
# length rule to state, and truncating to one was the defect C12 was written about before being withdrawn.
rule = "C12"
max_instruction_chars = 2000  # Discord's own cap, for reference only; nothing is refused for length

# ---------------------------------------------------------------- the line (C14–C17)

[line]
rule = "C14"
# C14 — the bridge types one line into the pane: a bracketed directive, the request id,
# the text, and exactly one trailing newline. Nothing else is ever typed.
directive_template = "[discord:addressed {ts} msg={msg}] {text}\n"
# C15 — the grammar is normative: a parser that accepts anything this does not match, or
# rejects anything it does, is not conformant.
directive_grammar = '^\[discord:(?P<kind>addressed) (?P<ts>\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ) msg=(?P<msg>[0-9]+)\](?: (?P<text>[^\r\n]*))?\n$'
ts_format = "%Y-%m-%dT%H:%M:%SZ"
# C17 — the text is one line: control characters are removed, newlines become spaces,
# and a multi-line prompt is flattened before it is typed.
sanitise = { strip_controls = true, newlines_to_space = true }

# ---------------------------------------------------------------- records (C18)

[receipts]
rule = "C18"
# C18 — a bridge records only these words about a request.
forward = ["accepted", "injected", "delivered", "answered"]
# Every word a bridge may write about a request, including the ones that are not a state.
# A word outside this list is not a record, it is an invention (C29).
# Of the forward words, `injected` is transport evidence only; `delivered` and `answered`
# exist only through the reply tool, by request id.
event = ["accepted", "injected", "injected-queued", "injected_held", "delivered", "answered", "reminder", "reminder_unsigned", "answered-with-receipt", "answered-without-receipt", "abandoned_restart", "refused", "held", "expired", "ticker-injected", "notice10", "notice60", "notice_unsigned_not_injected"]
# Words about the bridge rather than about a request. Declared because a box must be able to say what
# it is doing; measured from the sb2 log on 2026-10-25, which wrote 29 words in total.
operational = ["heartbeat", "start", "restart-window", "binding", "baseline", "dm_channel", "reply", "receipt-written", "unattributed", "ignored", "writer-lock-refused", "peer_filed", "ticker-held", "repair-no-payload", "repair-held", "repaired"]
# Words a ruling abolished. R2 replaced the 10-minute and 60-minute pair with one reminder at 20 minutes,
# so a box that still writes these has not implemented the ruling — a finding, not a vocabulary error.
abolished = ["notice10", "notice60"]   # both were replaced by "reminder" at C22

# ---------------------------------------------------------------- states (C22–C27)

[states]
rule = "C24"
# C24 — the request lifecycle under R3: a restart closes the backlog silently, so there is
# no recovery state, no in-flight journal, and no replay. This table is what the log replay
# checks a box's own records against; no box is asked to simulate anything.
initial = "new"
# The words the transition table governs. Notices and tickers are side events — they say something
# happened around a request, not that the request moved — so they are excluded rather than legalised.
ladder = ["accepted", "injected", "injected-queued", "injected_held", "delivered", "answered", "reminder", "reminder_unsigned", "answered-with-receipt", "answered-without-receipt", "held", "expired", "abandoned_restart"]
terminal = ["answered", "abandoned_restart"]
transitions = [
  ["new", "accepted"],
  ["accepted", "held"],
  ["held", "accepted"],
  ["held", "injected"],
  ["accepted", "injected"],
  ["injected", "delivered"],
  ["delivered", "answered"],
  ["accepted", "abandoned_restart"],
  ["held", "abandoned_restart"],
  ["injected", "abandoned_restart"],
  ["delivered", "abandoned_restart"],
  ["delivered", "no-receipt"],
  ["no-receipt", "answered"],
  ["no-receipt", "abandoned_restart"],
  ["delivered", "answered-with-receipt"],
  ["delivered", "answered-without-receipt"],
  ["injected", "answered-with-receipt"],
  ["injected", "answered-without-receipt"],
  ["injected-queued", "answered-with-receipt"],
  ["injected-queued", "answered-without-receipt"],
  ["injected-queued", "delivered"],
  ["held", "injected-queued"],
  ["injected", "injected-queued"],
]

[ack]
rule = "C21"
# C21 — R1: the first thing posted for an accepted prompt is the acknowledgement, once,
# keyed by message id. Channel and DM text are ruled; do not paraphrase them.
channel_text = "<@{operator_id}> on it."
dm_text = "On it."
keyed_by = "message id"

[reminder]
rule = "C22"
# C22 — R2: remind every 20 minutes from prompt entry (not from delivery), until a terminal
# event exists. The reminder is a channel post; it is never injected into the pane.
every_s = 1200
from_state = "accepted"
stop_on = ["answered", "abandoned_restart"]
sink = "channel"
first_after_s = 1200

# ---------------------------------------------------------------- notice signature (C19–C20)

[notice]
rule = "C19"
# C19 — a notice is a signed, self-describing line. Without a key nothing is injected (C20).
# The operator's own sentence, 2026-10-25 20:41Z, with the request id and the minutes it names, and the three
# machine fields at the end so a reader can tell a signed line from an unsigned one.
line_template = '''BRIDGE REMINDER: A discord message hasn't been answered by you yet (request {msg}, {minutes} minutes). The owner is still waiting for an answer on discord. If you are still working on the task you can finish it first, otherwise report back on discord. [kind=notice ts={ts} sig={sig}]'''
canonical = "kind=notice;msg={msg};minutes={minutes};ts={unix}"
algorithm = "hmac-sha256"
encoding = "lowercase-hex"
hex_len = 64
compare = "constant-time, whole string"
# The cadence is a formula, not a list: the n-th reminder is due at n * every_s after entry, with no upper bound.
# A list here would have made an R2-conformant box at 80 minutes non-conformant for want of a declared value.
every_s = 1200
step = "n * every_s from entry, n = 1, 2, 3, ... with no upper bound"
examples = [20, 40, 60, 80, 100]
# [R] operator, 2026-10-25 20:03Z ("just allow the pane reminder, it's internal communication"): with no key
# the pane line is delivered and labelled `sig=none`, so the reader knows it is unauthenticated. The channel
# reminder is unchanged, and the injection is recorded as `reminder_unsigned`.
no_key = "inject_labelled_unsigned"
unsigned_marker = "sig=none"
# C19 — the shape. Measurable on every box, key or no key: the three costume fields are a parser's job, not a
# signature's. `sig` is 64 lowercase hex or the literal `none`; both are conformant, and a reader can tell which.
shape_grammar = '''^BRIDGE REMINDER: A discord message hasn't been answered by you yet \(request (?P<msg>[0-9]+), (?P<minutes>[0-9]+) minutes\)\. The owner is still waiting for an answer on discord\. If you are still working on the task you can finish it first, otherwise report back on discord\. \[kind=notice ts=(?P<ts>[0-9]+) sig=(?P<sig>[0-9a-f]{64}|none)\]$'''
shape_fields = ["kind", "msg", "minutes", "ts", "sig"]

# ---------------------------------------------------------------- supervision and identity (C30–C31)

[selftest]
# C28 — the can-fail proof without a second implementation: a proxy adapter flips one answer from a real
# box, and the suite must go red. Three mutations, three defects, one small file.
mutants = ["accept_all", "bad_sig", "bad_log"]
# `bad_log` is a doctored record stream, not an adapter: a reminder after an answer in the same transcript.

[scope]
# C28's companion: a rule is either measured by an arm or named here with the reason it cannot be measured from
# outside a box. Parking a rule here is a visible commit, not an omission — and the checker refuses an excuse
# shorter than a sentence, so the list cannot decay into "not covered".
not_measured_by_an_arm = { C1 = "a rule about this file's own history: it is verified by git and by review, not by a box, and tools/check.py reads the commit log for it" }

[adapter]
# C28 — a box is a command, and "an adapter exists" must be a claim about a reachable seam rather than a file.
# Each operation maps to one callable in the box's own code; an operation the box lacks answers `null` and the arm
# it feeds is SKIP. `tools/check.py --adapters` runs every adapter through every operation.
ops = ["config", "classify", "sign", "verify", "line", "vocabulary", "log", "codes", "supervision"]
callables = { config = "the box's own config/operator file, plus its reminder cadence constant", classify = "gate(msg, cfg, dm=)", sign = "notice line builder", verify = "notice verifier", line = "pane line renderer", vocabulary = "the record-word set the box may write", log = "the path of the box's own log", codes = "the refusal codes the box can emit, as data", supervision = "the three supervision axes and their evidence" }
fixtures = { stranger = "361033318273384449", foreign_role = "999999999999999999" }

[supervision]
rule = "C30"
# C30 — three failure axes, each with its own evidence. A heartbeat proves the loop, never the process.
axes = ["process_gone", "loop_stopped", "no_turn"]
evidence = { process_gone = "NRestarts / a supervisor log line", loop_stopped = "heartbeat age against a threshold the loop cannot reach honestly", no_turn = "delivered with no answered inside the reminder window" }

[retention]
rule = "C32"
# C32 — the operator's ruling, 2026-10-25: "yes to outliving". The root cause it removes: two maps with
# the same retention evict the closing record first whenever the request is old, so an answered request
# looks open again and its reminder fires. Measured 2026-10-25T19:32Z: a request answered 2026-10-22
# re-fired after 4,103 minutes. `closes` lists the records either of which finishes a request.
closes = ["answered", "handled"]
keeps = "the closing record's retention is greater than the opening record's"
opening = "accepted"

[identity]
rule = "C31"
# C31 — the running code reports what it is, and the set is named here so two boxes cannot differ.
covers = ["loop", "reply_tool", "notice_verifier"]
reported_in = ["start", "boot"]

# ---------------------------------------------------------------- arms (C28)

[[arm]]
name = "gate_operator_accepted"
rule = "C3"
kind = "gate"

[[arm]]
name = "gate_role_mention_accepted"
rule = "C4"
kind = "gate"

[[arm]]
name = "gate_no_mention_refused"
rule = "C5"
kind = "gate"

[[arm]]
name = "gate_stranger_only_refused"
rule = "C5"
kind = "gate"

[[arm]]
name = "gate_role_only_refused"
rule = "C5"
kind = "gate"

[[arm]]
name = "gate_other_author_refused"
rule = "C6"
kind = "gate"

[[arm]]
name = "gate_bot_author_refused"
rule = "C7"
kind = "gate"

[[arm]]
name = "gate_wrong_channel_refused"
rule = "C8"
kind = "gate"

[[arm]]
name = "gate_wrong_guild_refused"
rule = "C9"
kind = "gate"

[[arm]]
name = "gate_dm_stranger_refused"
rule = "C10"
kind = "gate"

[[arm]]
name = "gate_empty_refused"
rule = "C11"
kind = "gate"

[[arm]]
name = "gate_bot_ping_with_others_accepted"
rule = "C5"
kind = "gate"

[[arm]]
name = "codes_are_distinct"
rule = "C13"
kind = "gate"

[[arm]]
name = "line_grammar_round_trip"
rule = "C15"
kind = "line"

[[arm]]
name = "line_flattens_multiline"
rule = "C17"
kind = "line"

[[arm]]
name = "vocabulary_is_closed"
rule = "C18"
kind = "vocabulary"

[[arm]]
name = "notice_shape_declared"
rule = "C19"
kind = "notice"

[[arm]]
name = "notice_signature_verifies"
rule = "C20"
kind = "notice"

[[arm]]
name = "notice_truncated_signature_refused"
rule = "C20"
kind = "notice"

[[arm]]
name = "notice_cross_class_refused"
rule = "C20"
kind = "notice"

[[arm]]
name = "no_key_means_labelled_unsigned"
rule = "C20"
kind = "notice"

[[arm]]
name = "log_reminder_after_answer_refused"
rule = "C32"
kind = "log"

[[arm]]
name = "log_transitions_legal"
rule = "C24"
kind = "log"

[[arm]]
name = "notice_cadence_matches_box"
rule = "C22"
kind = "notice"

[[arm]]
name = "log_no_abolished_reminder"
rule = "C22"
kind = "log"

[[arm]]
name = "log_words_declared"
rule = "C18"
kind = "log"

[[arm]]
name = "manifest_covers_every_arm"
rule = "C28"
kind = "derived"

[[arm]]
name = "codes_are_declared"
rule = "C29"
kind = "derived"
[[arm]]
name = "unaddressed_is_silence"
rule = "C2"
kind = "gate"

[[arm]]
name = "line_is_one_line"
rule = "C14"
kind = "line"

[[arm]]
name = "directive_carries_message_id"
rule = "C16"
kind = "line"

[[arm]]
name = "ack_once_before_answer"
rule = "C21"
kind = "log"

[[arm]]
name = "reminder_is_not_an_answer"
rule = "C23"
kind = "log"

[[arm]]
name = "no_orphan_holds"
rule = "C25"
kind = "log"

[[arm]]
name = "one_message_one_request"
rule = "C26"
kind = "log"

[[arm]]
name = "terminal_is_final"
rule = "C27"
kind = "log"

[[arm]]
name = "identity_reported"
rule = "C31"
kind = "log"

[[arm]]
name = "supervision_axes"
rule = "C30"
kind = "supervision"
```
