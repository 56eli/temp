# 08 — Conformance: measuring a bridge from outside

*[agent: 2026-10-31 — sb3. Files: `reference/contract-v7/conformance/run.py`, `tools/check.py`.]*

## The idea

Every claim about a bridge should be checkable by someone who does not trust the implementer and does
not read the implementation. So the standard ships a suite that:

* drives a **box** through a command that speaks JSON on stdin/stdout — no import of internals, no
  shared state, so it works across containers and hosts;
* has **38 arms**, each declared in the contract block and each keyed to a rule id;
* returns three states: pass, fail, **SKIP** — and SKIP is never a pass;
* proves it can fail (`--selftest`).

```
python3 conformance/run.py --list                    # the arms and the rule each enforces
python3 conformance/run.py --box <name>              # measure a box
python3 conformance/run.py --box <name> --allow-skips C20
python3 conformance/run.py --box <name> --selftest   # can-fail: mutations must turn green arms red
python3 conformance/run.py --log <events.jsonl>      # replay a box's own records
python3 tools/check.py                               # block ⇄ arms ⇄ prose ⇄ documents agree
python3 tools/check.py --adapters                    # every adapter answers every declared op
python3 tools/check.py --source <file>               # heuristic scan for refusal literals
```

## Exit codes, because a machine reads only this one

| code | meaning |
|---|---|
| 0 | every declared arm ran and passed; skips only where `--allow-skips` names the rule |
| 1 | at least one arm failed |
| 2 | an arm was skipped that the command did not allow — **an unmeasured rule is not a satisfied one** |

The allowance is a *command*, not a setting, so a run that accepts a gap says so where the run is
read. `--allow-skips` takes **rule ids**, not arm names (nine arms can share seven rule ids).

## The adapter protocol

One process invocation per operation. Input is one JSON object on stdin; output is one JSON object
on stdout; any non-zero exit or non-JSON output is an adapter error (the arm fails, it does not pass).

| op | request fields | response |
|---|---|---|
| `config` | — | `{operator_id, bot_id, role_ids[], guild_id, channel_id, reminder_every_s?}` |
| `classify` | `msg`, `cfg` | `{action: accept|refuse, code, instruction}` |
| `sign` | `msg_id`, `minutes`, `ts`, `key_hex?` | `{line}` |
| `verify` | `line`, `key_hex?`, `ts` | `{rc, status}` |
| `line` | `msg_id`, `text`, `ts` | `{line}` |
| `vocabulary` | — | `{words: [...]}` (the words the box may write) |
| `log` | — | `{path}` (a path the suite can read **on its own host**) |
| `codes` | — | `{codes: [...]}` (refusal codes the box can emit, as data) |
| `supervision` | — | `{axes: [...], evidence: {...}}` |

An op the box cannot answer returns `null`/an error, and the arms it feeds become SKIP. That is how
a box without a renderer seam reports honestly instead of pretending.

A `classify` exchange, recorded live against sb3:

```
$ echo '{"op":"classify","msg":{"id":"1","channel_id":"…","guild_id":"…",
         "author":{"id":"847445853584883712","bot":false},
         "mentions":[{"id":"1564946284094292069"}],"mention_roles":[],
         "dm":false,"content":"<@1564946284094292069> status"}}' | node adapter.js
{"action":"accept","code":null,"instruction":"status"}
```

### Three adapter shapes, all the same protocol

| shape | example | how |
|---|---|---|
| in-process | `sb2.py` | import the box's own module, call its gate/verifier |
| sibling container | `devcage.py` | `docker exec -i -u dev <container> node /home/dev/bridge/adapter.js`; for `log`, `docker cp` the file to a host temp path |
| remote / mounted | `_peer.py` | point `PI_PEER_HOME` at a directory holding the box's `bridge.py` |

The Node implementation goes one step further: it ships `adapter.js` **inside the box**, so the
adapter is a thin `node …` call and never a re-implementation. That is the shape to copy. A
`python3 -c` one-liner is enough:

```python
import json, subprocess, sys
req = json.load(sys.stdin)
p = subprocess.run(["node", "/path/to/bridge/adapter.js"], input=json.dumps(req),
                   capture_output=True, text=True, timeout=120)
print(p.stdout or json.dumps({"error": p.stderr[:200]}))
```

## The arms

Grouped by kind (38 in v7; the head adds `gate_attachment_accepted` for 39):

**Gate (13)** — `gate_operator_accepted`, `gate_role_mention_accepted`,
`gate_bot_ping_with_others_accepted`, `gate_no_mention_refused`, `gate_stranger_only_refused`,
`gate_role_only_refused`, `gate_other_author_refused`, `gate_bot_author_refused`,
`gate_wrong_channel_refused`, `gate_wrong_guild_refused`, `gate_dm_stranger_refused`,
`gate_empty_refused`, `codes_are_distinct`, `unaddressed_is_silence`.

**Line (4)** — `line_is_one_line`, `line_grammar_round_trip`, `line_flattens_multiline`,
`directive_carries_message_id`.

**Notice (5)** — `notice_shape_declared`, `notice_signature_verifies`,
`notice_truncated_signature_refused`, `notice_cross_class_refused`,
`no_key_means_labelled_unsigned`, plus `notice_cadence_matches_box`.

**Records / log (11)** — `vocabulary_is_closed`, `log_words_declared`,
`log_no_abolished_reminder`, `log_transitions_legal`, `log_reminder_after_answer_refused`,
`ack_once_before_answer`, `reminder_is_not_an_answer`, `no_orphan_holds`,
`one_message_one_request`, `terminal_is_final`, `identity_reported`.

**Derived (3)** — `manifest_covers_every_arm`, `codes_are_declared`, `supervision_axes`.

The **log arms read the box's own records from the last `start` record**, not a fixed time window.
That is deliberate: a box that was just fixed must not be judged on records written by previous code.
A box with no `start` record has no window and the log arms SKIP.

## can-fail (`--selftest`)

Three mutants, one small proxy adapter (`_proxy.py`):

| mutant | mutation | must turn red |
|---|---|---|
| `accept_all` | every message is an instruction | the gate arms |
| `bad_sig` | every signature verifies; sign returns a fixed digest | the notice arms |
| `bad_log` | a doctored record stream (a reminder after an answer, an invented word) | the log replay |

Arms that were **already red** on the real box are excluded from the proof: a mutation must turn a
*green* arm red, or the can-fail claim is measuring the box's own defect. Live run on sb3,
2026-10-31: `SELFTEST PASSED` — `bad_sig` caught by 2 arms, `bad_log` by 2 violations.

## The checker reads the documents too

`tools/check.py` verifies, and fails on:

* a declared arm with no implementation, and an implementation not declared (both directions);
* an arm citing a rule id that does not exist;
* **a rule with no arm** — unless it is excused in `[scope]` with a sentence, or withdrawn `[X]`;
* a withdrawn rule with no operator/date, or one that still has an arm;
* a code abolished and still declared or still in `addressing.order`;
* a code in `order` but not declared, or declared but never ordered;
* a forward word not in `event`; a terminal state that is not an event word;
* prose that does not name every rule;
* **document claims**: a stated `N arms/rules/codes` must match the block; an arm name must exist; an
  abolished code may not appear as current; a measurement line must carry a time and a code identity;
  two documents may not quote different results for the same box; the checklist tally must equal its
  own table. History lines are exempt only with one of four words (`historical`, `(history)`,
  `abolished`, `withdrawn`).

Measured 2026-10-31 on an extracted copy: `CHECK PASSED: 38 arms, 32 rules, 9 codes, one file`.
One caveat: the C1 check runs `git log` for `CONTRACT.md`, so a copy outside a git repository fails
C1 only. In this measurement I initialised a throwaway repo in `/tmp` to satisfy it — disclosed
because it is the difference between "the package is wrong" and "the copy has no history".

## Adopting the suite without adopting everything

1. **Start with the gate arms and the log word-set arm.** They need only a `classify` and a `log`
   op, and they catch the two defects that matter most: accepting what should be refused, and
   inventing vocabulary.
2. **Add `line` + `codes` + `vocabulary`.** These turn three prose claims into measurements.
3. **Leave the notice signature arms skipped until you have a key**, and name `C20` in
   `--allow-skips`. Do not delete them.
4. **Wire `--selftest` into CI**, not `--box` — a live box needs a live deployment; the mutants need
   nothing.
5. **Run `tools/check.py` in CI on the contract package itself.** It is the only thing that keeps
   the documents honest as they age.
