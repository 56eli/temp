# 02 — The contract

*[agent: 2026-10-31 — sb3. The normative text is `reference/contract-v7/CONTRACT.md`; this is a guide
to reading it, not a substitute.]*

## One artefact, one owner, real history

`CONTRACT.md` is a prose document with exactly one fenced ```toml block at the end. The prose is for
a human; the block is for a machine; they are the same file so they cannot disagree. The code loads
the block at start:

```js
const text = fs.readFileSync(target, 'utf8');
const block = text.match(/```toml\n([\s\S]*?)\n```/);
return { contract: require('@iarna/toml').parse(block[1]), path: target };
```

and then derives everything it enforces from it — refusal codes, record words, the pane grammar, the
notice grammar and cadence, the state ladder. Nothing in the code restates a rule in a second place;
a field the block does not declare is a defect, not a default.

The file's own governance is a rule (`C1`): **one owner writes it, changes are commits, never edits
to a document living in a chat.** v1–v6 of this standard lived in a single GitHub issue comment that
anyone could edit; three boxes implemented one text three ways, and every revision arrived at the
other two as a bug report. That history is the argument for the shape.

## Tags: what is the operator's word, what is derived, what is a proposal

Every rule carries one of three tags:

| tag | meaning | who may change it |
|---|---|---|
| `[R]` | **ruling** — the operator's words, quoted verbatim in `RULINGS.md` with a date and source id | only the operator, with new words |
| `[M]` | **mechanical** — a consequence of a ruling, or of how the platform works | anyone, with a commit |
| `[P]` | **proposal** — an implementer's choice, arguable and marked as such | anyone, with a commit |
| `[X]` | withdrawn by the operator, kept in the file as a record | nobody revives it without new words |

`RULINGS.md` is the only override, and it contains **only** quotes. A rule claimed as a ruling
without a quote is listed under "Not on record" and stays `[P]`. You can adopt the whole standard
without adopting this governance, but if you keep the tags you get the one property that matters:
you can always tell a requirement from a preference.

## The rule inventory (v7 as deployed, plus C33 from the devcage branch)

Rules marked ★ also have a contract "section" in the block. The arm column names the conformance
arms that measure the rule; every rule has at least one arm or is excused in `[scope]`.

### Gate — is this message an instruction? (§1)

| rule | tag | text (condensed) | arm(s) |
|---|---|---|---|
| C1 | M | one owner writes the file; changes are commits | excused: verified by git, not by a box (`[scope]`) |
| C2 | P | a message that is not addressed is silence: nothing in the channel, one refusal recorded | `unaddressed_is_silence` |
| C3 | M | an instruction passes every addressing test, in `[addressing].order`; a refusal is one declared code, named after the test that failed | `gate_operator_accepted` |
| C4 | P | a mention of one of the bot's roles addresses it exactly as a mention of the bot | `gate_role_mention_accepted` |
| C5 ★ | R | a ping to the bot is a sufficient address; other user/role mentions are content, never grounds for refusal | `gate_no_mention_refused`, `gate_stranger_only_refused`, `gate_role_only_refused`, `gate_bot_ping_with_others_accepted` |
| C6 | M | the author of an instruction is the operator | `gate_other_author_refused` |
| C7 | M | a bot author is refused unless it is a declared peer on the peer lane | `gate_bot_author_refused` |
| C8 | M | an instruction arrives in the eligible channel or the operator's DM | `gate_wrong_channel_refused` |
| C9 | M | when a guild id is configured, the message's guild must match | `gate_wrong_guild_refused` |
| C10 | M | a DM from anyone but the operator is refused `dm_stranger` | `gate_dm_stranger_refused` |
| C11 | M | nothing after the addressing prefix (and, head, no attachment) → `empty` | `gate_empty_refused` |
| C12 | X | **withdrawn 2026-10-25**: a Discord message is already the bound; no length rule | none by design |
| C13 | M | two causes never share a code; an abolished code is never emitted | `codes_are_distinct` |
| C33 ★ | R | an addressed message with an attachment is an instruction; the file is stored and its path named in the pane line (devcage branch `16e4acd` only — **not** on the contract branch, **not** deployed) | `gate_attachment_accepted` |

### The line — what reaches the pane (§2)

| rule | tag | text | arm(s) |
|---|---|---|---|
| C14 ★ | M | the bridge types exactly one line: directive, text, one newline | `line_is_one_line` |
| C15 ★ | M | `[line].directive_grammar` is normative: more or less is non-conformant | `line_grammar_round_trip` |
| C16 | M | the id in the directive is the instruction's Discord message id | `directive_carries_message_id` |
| C17 ★ | M | no newline inside the line: control characters removed, newlines become spaces | `line_flattens_multiline` |

### Records — what may be written about a request (§3)

| rule | tag | text | arm(s) |
|---|---|---|---|
| C18 ★ | M | write only `[receipts]` minus `abolished`; `injected` is transport evidence only | `vocabulary_is_closed`, `log_words_declared` |
| C29 | M | a refusal code or record word not in the file fails a gate | `codes_are_declared` |

### States, ack, reminders, restart (§4–§6)

| rule | tag | text | arm(s) |
|---|---|---|---|
| C19 ★ | P | the notice has one declared **shape** (operator's sentence + id + minutes + `sig` = 64 hex or `none`), measurable with no key | `notice_shape_declared` |
| C20 | R | a signature is verified as a whole in constant time; truncated/invented/cross-class refused; no key ⇒ delivered labelled `sig=none` | `notice_signature_verifies`, `notice_truncated_signature_refused`, `notice_cross_class_refused`, `no_key_means_labelled_unsigned` |
| C21 ★ | R | the first thing posted for an accepted prompt is the acknowledgement, once, keyed by message id | `ack_once_before_answer` |
| C22 ★ | R | remind every 20 min from **entry** until a terminal record, in the channel **and** the pane | `notice_cadence_matches_box`, `log_no_abolished_reminder` |
| C23 | M | a reminder is not an answer: it never occupies the answer slot | `reminder_is_not_an_answer` |
| C24 ★ | R | a restart closes every non-terminal request silently; nothing older than the process is relayed | `log_transitions_legal` |
| C25 | M | an instruction that cannot be injected yet is held in memory and drained later; it dies with the process | `no_orphan_holds` |
| C26 | M | one message id is one request, however often the poller sees it | `one_message_one_request` |
| C27 | M | a terminal state is final; a late answer is not a second outcome | `terminal_is_final` |

### Retention, supervision, identity, proof

| rule | tag | text | arm(s) |
|---|---|---|---|
| C28 | M | every arm is declared, checked against the suite, and shown failing against a deliberate defect | `manifest_covers_every_arm`, `--selftest` |
| C30 ★ | M | supervision covers three axes — process gone, loop stopped, no turn — each with its own evidence | `supervision_axes` |
| C31 ★ | M | the running code reports its identity, covering the loop, the reply tool and the notice verifier | `identity_reported` |
| C32 ★ | R | a cancellation outlives its obligation: the closing record is retained at least as long as the opening one, and either record closes the request | `log_reminder_after_answer_refused` |

## Closed vocabularies

The block is a set of *closed* sets. This is the property that makes logs machine-checkable.

**Refusal codes** (9 declared, 8 emitted by the Node box; `thread_not_in_scope` is a declared
optional gap):

```
bot_author  other_author  wrong_guild  wrong_channel
thread_not_in_scope (optional)  dm_stranger  pinged_nobody  pinged_other_user  empty
```

Abolished, readable in old logs and never emitted: `too_long` (C12 withdrawn), `foreign_role`
(C5 amended — a role the bot does not hold is not an address to the bot, so there is nothing to
diagnose).

**Record words** — three groups:

* `forward = [accepted, injected, delivered, answered]` — the four words about a request's progress;
  `injected` is transport evidence, `delivered`/`answered` exist only through the reply tool.
* `event` — every word a bridge may write, including `injected-queued`, `injected_held`,
  `reminder`, `reminder_unsigned`, `answered-with-receipt`, `answered-without-receipt`,
  `abandoned_restart`, `refused`, `held`, `expired`, `ticker-injected`, `notice_unsigned_not_injected`.
* `operational` — words about the bridge rather than a request: `heartbeat`, `start`,
  `restart-window`, `binding`, `baseline`, `reply`, `receipt-written`, `unattributed`, `ignored`,
  `writer-lock-refused`, `peer_filed`, `ticker-held`, `repair-*`, `repaired`.
* `abolished = [notice10, notice60]` — replaced by `reminder` at C22; a box that still writes them
  is a finding, not a vocabulary error.

**State ladder** — the words the transition table governs, and the terminal set:

```
ladder   = accepted, injected, injected-queued, injected_held, delivered, answered,
           reminder, reminder_unsigned, answered-with-receipt, answered-without-receipt,
           held, expired, abandoned_restart
terminal = answered, abandoned_restart
```

> **Known defect in v7 (measured, not theory).** The prose above `[states]` says notices are side
> events and are "excluded rather than legalised", but `reminder` and `reminder_unsigned` *are* in
> `ladder`, and the `transitions` table contains **no** edge into or out of them. A box that fires a
> reminder and then delivers therefore replays as illegal. Measured on the live sb3 log on
> 2026-10-31: 4 violations in 2 classes across 20,556 records. Two possible fixes: drop the reminder
> words from `ladder` (matching the prose), or add `[injected, reminder_unsigned]` and
> `[reminder_unsigned, delivered]` (matching practice). Pick one before you rely on
> `log_transitions_legal`.

## The `[scope]` escape hatch, and why it is one line

A rule that cannot be measured from outside a box is named in `[scope].not_measured_by_an_arm` with
a sentence explaining why. In v7 there is exactly one: C1, "a rule about this file's own history: it
is verified by git and by review, not by a box". The checker refuses an excuse shorter than a
sentence, refuses one for a rule that has an arm, and refuses an unknown rule id. The point is that
a gap is a **visible commit**, not an omission.

## The adapter declaration

```
ops = [config, classify, sign, verify, line, vocabulary, log, codes, supervision]
```

Each op maps to a callable in the box's own code. `tools/check.py --adapters` runs every adapter
through every op, so "the adapter exists" is a claim about a reachable seam. If your implementation
has no renderer seam, answer `null` and the arm becomes SKIP — honest, and the exit code makes you
name it (`--allow-skips`).

## Changing the contract

1. A rule is `[R]` only if the operator said it. Quote the words, with date and source id, in
   `RULINGS.md`; append, never rewrite.
2. Change the prose and the block in the same commit. `python3 tools/check.py` must pass.
3. If a rule is withdrawn, leave it `[X]` with the operator's name and date; abolish any code or
   word it owned (`abolished = {...}`) instead of deleting it. Old logs stay readable; current code
   cannot emit it.
4. If a code or word is added, add an arm. A rule with no arm is a build failure.
5. Do not edit a quote to match new behaviour. Append a dated correction.
