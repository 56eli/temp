# Reviewing this — start here

One page for a reviewer. What this directory is, what order to read it in, what each claim rests on, and
what it does **not** claim.

## What it is

The Discord bridge exists in three implementations — one per agent host — and one standard. **One of the three is
measured from here** (`sb2`, this container); the other two are their own written testimony until their `bridge.py`
is mounted, which `BOXES.md` says on every row. This directory is the standard: a contract, the operator's rulings, a deployment sheet, and a suite that measures any
implementation from the outside. It was written because the previous standard lived inside a single GitHub
comment that anyone could edit, so three boxes implemented one text three ways and every revision arrived
at the other two as a bug report.

## Read in this order

| # | file | what it settles | what to look for |
|---|---|---|---|
| 1 | `CONTRACT.md` (prose) | what a bridge must do: the gate, the line, the records, the states, retention, the notice, supervision | a rule you think is wrong, or one that cannot be obeyed |
| 2 | `RULINGS.md` | which rules are the operator's words, and which are an implementer's proposal | any `[P]` rule you think should be a ruling — that needs his sentence, not yours |
| 3 | `CONTRACT.md` (`toml` block) | the same rules in a machine form: closed code list, record words, transition table | a code or word that is missing, or a transition that is legal and absent |
| 4 | `BOXES.md` | what each box actually runs, marked measured or reported | a row marked *reported* that you think is a fact, or the reverse |
| 5 | `conformance/run.py` | the suite: 38 arms, each keyed to a rule | an arm that cannot fail, or one that measures itself |
| 6 | `PROPOSAL.md` | the plan that was reviewed and approved on 2026-10-25, plus what was built | a proposed item that is missing from the outcome table |

## The two conventions to keep in mind

- **`[R]` / `[M]` / `[P]`** in front of every rule: a ruling (his words, quoted in `RULINGS.md`), a mechanical
  consequence of one, or an implementer's proposal. Only his sentence moves a `[P]` to `[R]`.
- **`SKIP` is never `PASS`.** An arm a box cannot answer is skipped and named, and the run's exit code is 2
  unless the command names the rule it is willing to leave unmeasured (`--allow-skips C19,C20`). The allowance
  lives in the command, so a run that accepts a gap says so where the run is read.
- **A rule is either armed or excused, never silently absent.** `[scope].not_measured_by_an_arm` names the rules
  that cannot be measured from outside a box, each with a sentence explaining why; the checker refuses a thin
  excuse and refuses an excuse for a rule that has an arm.

## The checker reads the documents too

`tools/check.py` did not, which is how this package came to state the wrong arm count beside a suite of the right
size, and to name a code its own contract had abolished (historical — independent review, 2026-10-25). It now
checks the documents a reviewer is told to trust, and each check was measured failing before it was trusted:

| check | what it caught before it was written |
|---|---|
| a stated `N arms` / `N rules` / `N codes` must equal the block's | historical: `REVIEW.md` said 28 arms, then 37, for a suite of 38 |
| an arm name must exist in the block | historical: `BOXES.md` named `gate_foreign_role_refused`, deleted by R7 |
| an abolished code may not appear as current | historical: `BOXES.md` presented `too_long` after R7 abolished it |
| a `P passed, F failed, S skipped` line must carry a time and a code identity | three documents quoted three different results for one run on one evening |
| two documents may not quote two different results for the same box | historical: `REVIEW.md` 28/0/9 beside `PROPOSAL.md` 26/3/9 |
| `CHECKLIST.md`'s tally must equal its own table | historical: the tally said 27 measured where the table held 26 |

**The one word a document may use to record rather than claim:** `historical`, `(history)`, `abolished` or
`withdrawn` on the same line. A line carrying one is a record of a moment and is exempt; a line without one is a
claim and must be true today. The exemption is deliberately narrow — an earlier version accepted "no longer" and a
row about the length defect exempted itself with it.

## Check the claims yourself

From this directory:

```sh
python3 tools/check.py                      # the block, the arms, the prose AND the five documents must agree
python3 tools/check.py --adapters           # every adapter answers every declared op
python3 tools/check.py --source <bridge.py>  # heuristic text scan; the measurement is a box's own `codes` op
python3 conformance/run.py --list            # 38 arms with the rule each enforces
python3 conformance/run.py --box sb2         # a live box, through its own gate  (needs the sb2 host)
python3 conformance/run.py --selftest --box sb2   # can-fail: three mutations must turn a green arm red
python3 conformance/run.py --log <box log>   # replay a box's own records
```

Measured on the sb2 box on **2026-10-25 22:06Z**, after R8 changed the restart window and the box was restarted
(`code_identity 76c0560e2592ee51`, pid 170889, started 21:03:50Z):

```
box=sb2  29 passed, 0 failed, 9 skipped  (contract v7)   22:06Z, code_identity 76c0560e2592ee51   exit 0
  --allow-skips C14,C15,C16,C17,C18,C20,C30
box=sb2  29 passed, 0 failed, 9 skipped  (contract v7)   22:06Z, code_identity 76c0560e2592ee51   exit 2
  UNMEASURED: 9 arm(s) skipped without an allowance
```

The two runs differ only in whether the command names the rules it is willing to leave unmeasured, which is what the
exit code is for, and it fires here on a real box rather than on a stub.

**Three units that are easy to confuse, so here they are side by side** — the independent review of 2026-10-25 caught
this package using them interchangeably:

| unit | count | what it counts |
|---|---|---|
| conformance arms | **38** | every `def arm_*` in `conformance/run.py`, each declared in `CONTRACT.md` |
| arms skipped on sb2 | **9** over **7 rule ids** | C14, C15, C16, C17, C18, C20 (three arms), C30 — hence 7 ids for 9 arms, and the `--allow-skips` list names the ids, not the arms |
| checklist items | **39** | the properties a message meets on its way through a bridge: 27 measured, 6 skip, 4 unarmed, 2 hand-checked |
| the box's own suite | **64** | `selftest.py` inside the box — a different artefact, not this suite |

A checklist item marked *skip* is not the same as a skipped arm (an item can be skipped while its rule has a passing
arm that measures a different half), and the four *unarmed* items have rule-level arms but no item-level arm. Twelve
of the 39 items are therefore not measured by an arm: 6 skip + 4 unarmed + 2 hand-checked.

The nine skips, each with what it costs: three notice arms need a **signed** line, which a box with no key cannot
build (C20 ×3 — the signature half; the shape half is C19 and it passes, `shape ok, sig=none`); four line arms need a
**renderer seam** the box does not expose (C14, C15, C16, C17); one vocabulary arm needs a **word-set seam** (C18);
one supervision arm needs **process/loop/idle evidence** that lives in the runner rather than the bridge (C30). Run
with `--allow-skips C14,C15,C16,C17,C18,C20,C30` to accept exactly those, and the exit code then reflects failures
alone.

To measure a *different* box, point the generic adapter at its `bridge.py`:

```sh
PI_PEER_HOME=/path/to/that/box python3 conformance/run.py --box debugger
```

## What changed after the first outside review

An agent on another host read this package and filed seven findings. Six reproduced; one could not be run here
because that box's `bridge.py` is not mounted. All seven were about the artefact's ability to *prove* things, none
about what a bridge does. What changed:

| finding | repair |
|---|---|
| the exit code ignored skips, so "SKIP is never PASS" was prose | exit 2 for an unallowed skip; the allowance is named in the command |
| `--source` scanned adapter text for a fixed token list, so a prose-coded box passed | the box says which codes it can emit (`codes`), compared both ways; `--source` reads its refusal literals |
| nine rules had no arm at all | ten arms added (C2, C14, C16, C21, C23, C25, C26, C27, C30, C31) and the checker now fails on an unarmed rule |
| C19 was unmeasurable without a key, and admitted to be violated | split into shape (C19, measurable always) and signature (C20); the shape is now red on sb2 |
| `[notice].minutes = [20, 40, 60]` contradicted R2's unbounded cadence | the cadence is a formula with a step; the list is `examples` |
| C25 read as the opposite of R3 | one sentence: held instructions live and die with the process |
| `abolished` words were both declared and illegal | writable = declared minus abolished, said in C18 and in §3 |
| "an adapter exists" was a claim about a file | nine ops declared with their callables, and `--adapters` probes every one |

## What this does **not** claim

- `debugger` and `bugger` are **not** measured from here. No mount of either bridge exists on this host, so
  their rows in `BOXES.md` are their own written record. That is exactly the weakness this artefact exists to
  remove, and it is unresolved.
- The **signed** notice path is untested: no key is provisioned on `sb2`, so three arms are SKIP. With no key
  the pane reminder is delivered labelled `sig=none` (R6), which *is* measured.
- The `sb2` notice line **does not match C19's declared shape** yet. The arm is red and says which fields are
  missing; nothing has been changed in the box to make it green.
- A **live** unsigned reminder had not fired at the time of writing; the builder and the box's own suite are
  measured, the injection moment is not.
- The sb2 bridge has **no autostart**: nothing restarts it after a container recreate. Known, not fixed.

## Where the history lives

v1–v6 are issue `56eli/botrunner#218`, comment `6325078617` (edited in place five times; the last text, v6, is
`6327219361`). They are kept as the record of how the standard was argued, not as a document to implement
from. `PROPOSAL.md` records the plan the operator approved on 2026-10-25 and what was built against it.

## How to disagree

File an issue against `56eli/botrunner`, quoting the rule id (`C7`) and the box. If the disagreement is about
what the operator wants rather than what a box does, it becomes a ruling only when he says it — a `[P]` rule
is fair game to argue with in the meantime.
