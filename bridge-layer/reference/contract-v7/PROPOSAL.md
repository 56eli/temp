# Proposal — the bridge standard, cut to fit, and the box fixed at the cause

**Outcome, 2026-10-25 19:49Z:** approved, all eight decisions, with one refinement — "only sentences i said
verbatim" (decision 5). Built the same evening; see `## What was built` below and `BOXES.md` for the
measurements. The text after this heading is the proposal as reviewed, unedited.

## What was built

| proposed | built |
|---|---|
| one normative file with a machine block | `CONTRACT.md` — prose plus one fenced `toml` block; declared, parsed by `tools/check.py` |
| delete the fixture; can-fail by mutating an adapter | `adapters/_proxy.py`: `accept_all`, `bad_sig`, `bad_log`; `run.py --selftest` requires each to be caught |
| delete `README`, `CHANGELOG`, `OWNERS`, `ADAPTER.md`, `boxes.toml` | deleted; useful lines are in `CONTRACT.md`'s header and its adapter section |
| ~20 arms, live seams plus log replay | **28 arms at the cut** (historical) — the eight simulator arms are gone, replaced by four log arms; the suite is 38 arms today, after the review's ten additions and R7's withdrawal of C12 |
| seven `[P]` rules stay `[P]` | unchanged, and `RULINGS.md` now states the bar explicitly |
| adopt "a cancellation outlives its obligation" | C32, plus `[retention]` in the block and a log arm that catches it |
| fix F1–F6 on sb2 in two commits | F1–F5 and R2's reminder cadence, two restarts; **F6 not done** — it is a missing key (the operator's act) and a rule trade, so it needs one word |
| adapters for the other two boxes | `adapters/_peer.py` plus two thin wrappers; not deployed, no mount exists here |

**Package size:** 19 files / 2,348 lines → **12 files / 1,711 lines**, then **15 files / 2,754 lines** after the review repairs and the R7 pass (ten arms and the machinery that makes an unmeasured rule fail), of which the normative document is one
file (`CONTRACT.md`) and the reviewer's page is one (`REVIEW.md`). Each item names the
root cause it removes and the proof that it worked, and every claim about the live box is a
measurement taken on 2026-10-25 between 18:00Z and 20:08Z from inside container `sb2`.

## What the operator asked for

> Lightweight solution to bridge problem - yes · Wants to have reliable functionality - yes · Wants to
> have root-cause fixes - yes

Three wishes, in tension: a standard small enough to read, behaviour reliable enough to trust, and
no patchwork. This proposal resolves the tension by keeping the standard's *claims* few and its
*checks* automated, and by fixing the box's defects at their cause rather than at their symptom.

## 1. The honest inventory

What exists on branch `agent/bridge-contract-v7-2026-10-25` (commit `aba0a8e`): 19 files, 2,348 lines.
What is load-bearing: the contract, the rulings, the deployment sheet, and one suite that can be
pointed at another box. What is not:

| part | lines | why it is not load-bearing |
|---|---|---|
| `conformance/reference/bridge_ref.py` + 30 mutants | ~520 | a **second implementation** of the bridge, kept to prove the suite can fail; two things to maintain instead of one |
| `tools/generate.py` + `conformance/generated/` | ~270 | exists to keep prose and machine form in agreement — a problem created by having two forms |
| `README.md`, `CHANGELOG.md`, `OWNERS`, `conformance/ADAPTER.md` | ~230 | four documents around one standard; the useful sentences fit in a header |
| seven state-machine arms | ~90 | report SKIP on every live box; no live bridge has a simulator |
| `conformance/boxes.toml` | ~25 | a machine form of what `BOXES.md` already says |

## 2. The cut — one normative file, one tool, twenty arms

**Delete the duplication instead of generating across it.** One file, `CONTRACT.md`, holds the
prose *and* a single fenced `toml` block that is the machine form: rules, codes, record words,
transitions, the notice string. A 60-line `tools/check.py` reads that block and does four jobs which
currently need three files: verify the code against the declarations, verify the arm list, emit the
manifest, and refuse an undeclared code or record word. Two forms that must agree become one form
read twice.

**Prove can-fail without a second implementation.** A broken adapter is ten lines. `run.py --selftest`
runs every arm against three deliberately wrong adapters (accepts everything; signs wrongly; ignores
the cancellation) and requires each to be caught. The fixture and its 30 mutants go. The property
survives — a gate that cannot fail is still not a gate — and the maintenance cost drops to three
small functions.

**Result:** 19 files → 8, 2,348 lines → about 900, of which the normative text is one page.

```
CONTRACT.md                  normative prose + the machine block, one owner, real history
RULINGS.md                   the operator's words; the only override
BOXES.md                     what each box actually runs — allowed to differ
conformance/run.py           the black-box suite (38 arms today; this map is the cut, historical)
conformance/adapters/{sb2,debugger,bugger}.py   ten lines each, no shared daemon (R4)
tools/check.py               declarations, manifest, undeclared-word gate
```

## 3. The box, fixed at the cause

Six defects measured today. Each row: the cause, the fix, the proof. None is a patch on a patch.

| # | defect, measured | root cause | fix | proof |
|---|---|---|---|---|
| F1 | a request answered 2026-10-22 23:28Z fired a reminder on 2026-10-25 19:32Z, and the pane ticker at 19:33Z | `accepted` and `answered` are two 200-entry rings evicting independently (`bridge.py:378-381`, `:537`), so the cancellation can be evicted while the obligation survives (`due_notices`, `:566-574`; ticker, `:606-615`) | one ledger with **age**-based retention, and a notice cancelled by `handled` as well as `answered` | a grep over the real log: no `notice*` or `ticker-held` event whose id is in `handled` |
| F2 | an instruction of 1,801 characters is typed as 1,800, silently (`bridge.py:153`) | `sanitize()` both validates and normalises | the truncation was fixed on the spot; the length *rule* was built and then withdrawn by R7 (historical: `too_long` is abolished, C12 `[X]`) | an arm sends 1,801 characters and requires it delivered whole; the box's own suite has the same arm |
| F3 | 120 `unattributed` answers in the log: a reply posted with no request id, leaving the request open | `reply.py` posts first and correlates afterwards | refuse to post without an open request id; `--force` posts and records the force | arm: a reply with an unknown id exits non-zero and posts nothing |
| F4 | a message pinging this bot **and** a third party is accepted, and `<@361033318273384449>` reaches the pane; a foreign role is accepted too | `addressing()` returns `addressed` on the first positive test (`bridge.py:133-136`) | one predicate over all mentions: self, then third-party users, then roles, no early return | two arms from the suite, red today, green after |
| F5 | two codes differ from the contract: `dm_channel_undefined` → `dm_stranger`, `empty_instruction` → `empty` | the two codes predate the contract | rename both, one commit, both spellings in the deployment sheet for a transition period | the code-vocabulary arm |
| F6 | three notices today, each `notice_unsigned_not_injected`: the operator is alarmed, the agent gets nothing | no signing key was provisioned (the key creation is refused by a safety rule; the operator's act) | until a key exists, the notice says so once at startup, and the pane reminder is delivered unsigned **labelled** `sig=none` rather than withheld | start the bridge without a key and read the pane line |

F1 and F2 are the two that cost the operator directly: one interrupted him at 19:32Z for a request
answered three days earlier, the other can truncate his instruction mid-sentence with no record.

## 4. What stays cut, on the operator's word

- v6's in-flight journal, 65-minute queue and recovery path: deleted by R3.
- The 10/60-minute notice pair: deleted by R2 (20 minutes from entry, until an outcome).
- A shared daemon or shared state: forbidden by R4 (bugger's box is on another host).
- Restyling three boxes for symmetry: the deployment sheet exists so they may differ.

## 5. Order, effort, risk

| step | what | effort | risk |
|---|---|---|---|
| 1 | the cut: one file, one tool, twenty arms, fixture deleted | ~2 h | low — documents and test scaffolding; no bridge behaviour changes |
| 2 | F1, F2, F5 on sb2 (one commit) | ~40 min | low; F1 touches only pruning and two predicates |
| 3 | F3, F4, F6 on sb2 (one commit) | ~40 min | medium — F4 changes what is accepted; measured after, live, with a real ping as the test |
| 4 | adapters for `debugger` and `bugger` | ~1 h | low — one small file on each host, no code change to their bridges |
| 5 | notice key on sb2 | 5 min, the operator's act | none |

Steps 1–3 are PR-only until the operator says install, and every install is a lease, dropped at the
end. No other box is modified in steps 1–3.

## 6. The eight decisions

Recommended default in bold; each is a yes/no.

1. **Cut to one normative file with an embedded machine block** (kills the two-form agreement problem). *yes*
2. **Delete the reference fixture; prove can-fail by mutating an adapter** (`--selftest`). *yes*
3. **Delete `README`, `CHANGELOG`, `OWNERS`, `ADAPTER.md`, `boxes.toml`**; their useful lines move into the contract's header and `BOXES.md`. *yes*
4. **Twenty arms, not thirty** — every live seam plus log replay; state-machine arms return when a box has a simulator. *yes*
5. **The seven `[P]` rules stay `[P]`** until a box disputes one; a sentence from the operator raises any of them to `[R]`. *yes*
6. **Adopt one new rule: cancellation outlives obligation** — the general form of F1, so the other two boxes are bound by the same sentence. *yes*
7. **Fix F1–F6 on sb2 in two commits**, F1 and F2 first. *yes*
8. **Adapters for the other two boxes now, their code untouched.** *yes*

## 7. What the operator can check afterwards, without trusting me

- `python3 tools/check.py` → one file's declarations match the code, or it fails.
- `python3 conformance/run.py --box sb2` → the arms that were red are green, and `--selftest` shows
  the suite still catches three broken adapters.
- A grep over the last 18,446 real records → no `notice*` or `ticker-held` event whose id is in `handled`.
- One live ping from him, and one instruction of 1,801 characters, which must be refused by name.

### After the first outside review (2026-10-25 20:2xZ)

Another host read the package without running the sb2 box and filed seven findings. Six reproduced here; the
seventh (its own `bridge.py`) is not mounted, so only its mechanism was confirmed. The repairs were accepted as
root causes rather than patches, and two of them changed the shape of the artefact:

- **a rule with no arm is now a build failure.** `tools/check.py` checks rules → arms as well as arms → rules, and
  `[scope]` excuses a rule only with a sentence the checker will read. Ten arms were needed to satisfy it (C2, C14,
  C16, C21, C23, C25, C26, C27, C30, C31): 29 → 39 arms at that point (historical), 38 after R7 withdrew C12, and
  38 today: the independent review's cadence arm replaced nothing and one arm moved from C19 to C20.
- **an unmeasured rule now fails the run.** Exit 2 for a skip the command did not allow. This is the boundary that
  made the old table of 22 passes and 6 skips look like a verdict when it was a wish.
- **C19 was split**, because shape and signature were one rule that needed a key; the shape is measurable always,
  and on sb2 it is now red, which is the first time the defect the sheet admitted has had an arm about it.
- three rules were reworded where they contradicted each other (C25 vs R3, the cadence list vs R2, abolished words
  vs C18), and the adapter interface became a declared list of nine operations with a probe.

The cost is visible and worth naming: the suite is 38 arms, and on the one box measured here it reports 26
passed, 3 failed and 9 skipped. That is the honest reading, and the reason the artefact exists.

### R7 — the operator read the checklist and changed five rules (2026-10-25 20:41Z)

A ping to the bot is now a sufficient address and other mentions are content (C5 rewritten, raised to `[R]`); the
`foreign_role` code is abolished, because a role the bot does not hold is not an address to the bot and "the
sentence doesn't make sense" was the right assessment of it; the length rule is withdrawn (C12 → `[X]`, `too_long`
abolished) because a Discord message is already the bound; and the reminder now goes to the pane as well as the
channel, in the operator's own neutral wording. The box has not been changed to match, so three arms are red and
each names one change. `RULINGS.md` R7 carries the words verbatim.

**Correction, dated:** the commit `79b91a1` message says the package is "12 files, 1,9xx lines". That was written
before the count was taken; measured after: 14 files, 2,485 lines. The commit message stands as written and this
line is the record, because a message amended after the fact is a message nobody can check.

### R7 in the box, and one defect the replay found (2026-10-25 20:51-20:55Z)

The operator authorised the box changes ("you may also fix your own bridge"). Three were the rulings: accept a bot
ping whatever else it mentions, stop emitting the abolished codes, and speak the reminder in his own sentence. A
fourth was necessary once `verify.py` parsed a line shape that no longer existed.

The fifth was not planned. Restarting the bridge to load the first four produced **343 `unattributed` records in one
burst**: `apply_answers()` began at `state['answers_offset'] = 0`, so every historical answer was re-read, and because
R3 closes the backlog at startup almost every one then matched "no accepted instruction with that id" — false when it
was answered, and 336 records exist in the file. The offset now starts at the end of the file, and the box's own
suite pins it (`t_restart_does_not_replay_answer_history`). History is not news; the same principle as the log arms
measuring from the last `start`.

Measured after, **historical** — 20:55Z, `code_identity 15848ebb73b5dd72`, superseded by R8 later that evening:

| what | result at 20:55Z (historical) |
|---|---|
| conformance | `28 passed, 0 failed, 9 skipped` at 20:55Z, `code_identity 15848ebb73b5dd72` (historical) |
| box suite | `62 passed, 0 failed` at 20:55Z (historical) |
| log replay | `19,385 records, 230 violations in 15 classes` at 20:55Z, whole file, every one written by code since replaced |

The current result is in `REVIEW.md` and `BOXES.md` and is not repeated here, because a document that quotes a number
twice is a document that will disagree with itself.

### R8 — the restart window (2026-10-25 21:02Z)

"i don't want a restarting bridge to relay messages that are older than the bridge restart." One function now sets
the window in four places: `last_ids` cleared so the first poll baselines instead of asking for anything older, the
held queue dropped rather than drained, and the receipts and answers offsets taken at the current end of their files —
plus the idle clock. Measured at 21:03:50Z: the records after the restart are `start`, `restart-window`
(`cleared_channels=2, dropped_held=0`), `binding`, `baseline` ×2, and nothing else. The cost is stated in RULINGS.md
rather than discovered later: a message arriving during the restart gap is older than the process and is not relayed.
