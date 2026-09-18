# Work Order — translatechan letter 002: the 36-distinct rebuild

**Repo:** [56eli/translatechan](https://github.com/56eli/translatechan) — zero-backend static reading site for Classical Chinese Chan literature, published from `main` `/docs`
**Date:** 2026-09-18
**To:** the translatechan orchestrator and its dispatch agents
**From:** the project's reviewer (a memo to its own governance)
**Owner directive (2026-09-18):** **36 DISTINCT layout variations** — variants 1–2 kept; variants 3–35 rebuilt **from scratch, each on a NEW skeleton**; variant 36 rebuilt **faithfully from the owner's zip archive**. The current 36 squashed a good template into the bad skeleton — it does not survive.
**Reference pin:** `main` = `9af86f22714074d443125f02747c24cf39bf373b` ("Merge PR #83 — Layout 36 … The Chan Room", 2026-09-18 09:56:19 +0000). Every `file:line` reference below resolves at this commit unless a different sha is named.
**This letter only specifies.** The translatechan agents implement; the owner merges and rates. This letter authors no code, edits no target file, and opens no pull request in the target.

**Red Action Law — no personal values, ever.** A red (prohibited) action for any order from this desk: it must never assert a personal value, taste, preference, or opinion — no aesthetic verdict, no judgment of quality dressed up as fact. Everything below is either a verified fact (with a target-side anchor) or the owner's stated mandate. The law is mostly non-applicable here — this order handles no personal data — but it is stated and kept regardless. Per the project's own law, layout quality is the owner's call alone (`.orchestrator/RULING_WEBSITE_2026-09-14.md`: agents are "NOT CAPABLE TO JUDGE THE WEBSITE … 100% relying on my feedback"), so this letter specifies structure, budgets, and gates — never taste. The owner rates; that rating is the only quality signal this order recognizes.

---

## 1. Context and verified facts

Phase 5 shipped the entire layout fleet in about ten hours: 33 agent-implemented variants (the redo of 3–7, then bundles 8–15, 16–25, 26–35) plus the owner's hand-ported variant 36, through PR #79–#83, all inside `app.css` / `app.js` and their `docs/` mirror. Text integrity was never touched — every required text-integrity gate stayed green with counts byte-identical to before the window — so nothing here is a source/corpus problem. What the owner judged is the presentation: all 33 agent variants are permutations of **one shared skeleton**, differentiated by inventing CSS class names rather than by changing structure. The owner, the project's sole judge of the site, has judged the 36-template implementation botched and mandated the rebuild this order carries.

The failure was structural, not cosmetic. Because every variant restyled the same DOM, "distinctness" collapsed into copy-paste: roughly half of `app.css` is a byte-identical rule body restated under a new scope. Because the one gate that could see the legibility floor was switched off and double-swallowed, a known red floor shipped four times. And because the merge-to-publish loop ran in minutes with no pre-merge checkpoint, the owner never rated a single layout before the count was complete — the fleet optimized for the switcher count, not for owner-rated quality. The rebuild reverses every one of these by construction: new skeletons, a floor/distinctness acceptance gate, a required CI check, and an owner rating before each next batch.

| # | Verified fact and target-side anchors | Evidence |
|---|---|---|
| F1 | **33 agent variants are CSS-class permutations of one shared skeleton.** All families restyle the same base DOM (`.site-shell`, `.shell-lintel`, `.room-nav`, `.nav-tab-btn`); the switcher applies `data-design` on `<html>` (`app.js:646`), persists via `translatechan_design_variant` (`app.js:647`), and re-renders seen rooms on switch (`app.js:660–666`). The 36-key switcher list is the `DESIGN_VARIANTS` array (`app.js:601–637`); the input allowlist hardcodes keys 1–36 (`app.js:642–644`). `app.css` grew `3,348 → 13,845` lines and `app.js` `5,326 → 8,723` lines across PR #79–#83. | Verified at the pin: read `app.js:601–666` and `wc -l app.css app.js` (= 13,845 / 8,723) in a `main` clone @ `9af86f2`. Per-PR growth from the window diffs of PR #79–#83. |
| F2 | **Distinctness collapsed into copy-paste.** Of **3,187** selector/body rules parsed from `app.css` at the pin, **1,609 (~50%) share an exact byte-identical declaration body** with at least one other rule; the identical `.room-nav` body is restated under **29** variant scopes, alongside `.gongan-catalogue-head{display:none}` ×28 and `.corpus-selector-list.sidebar-panel{max-height:11rem;overflow-y:auto}` ×27. **423 bespoke class names** were invented across the 33 agent variants vs **13** for the owner's variant 36. | Verified at the pin: rule-grammar parse of `app.css` @ `9af86f2` (`re.findall(r'([^{}]+)\{([^{}]*)\}')`) reproduced 3,187 rules and 1,609 (50%) shared bodies, and the modal `.room-nav` body 29×; bespoke-class census per family selectors at `9af86f2`. |
| F3 | **Per-variant depth collapsed as the switcher count grew.** CSS+JS depth per variant fell **~770 lines (3–7) → ~523 (8–15) → ~269 (16–25)** (26–35 recovered to ~424), while the owner's single variant 36 carries ~2,120 lines. Every PR title records the switcher count as the milestone ("switcher 1–15 / 1–25 / 1–35 / 1-36"); the last agent batch self-labels "final batch **before review**". | Verified: per-family line attribution over `app.css`/`app.js` @ `9af86f2`; PR titles/timestamps of #79–#83. |
| F4 | **The legibility floor went red at the first bundle and stayed red through four merges.** The site's own harness declares a 0.72rem floor — "N10: citation metadata legibility floor — no sub-11px source text" (`scripts/smoke_test.mjs:157–159`), implemented as a whole-file grep that throws on any `font-size: 0.62rem`. At the pin `app.css` contains **25 × `font-size: 0.62rem`** (e.g. `app.css:6366, 6557, 7294`); **zero** existed before the window. Sub-floor declarations overall grew **60 → 225**. Introduction per bundle: PR #79 **+5** (@ `9bf4b33`), #80 **+7** → 12 (@ `c5b0495`), #81 **+4** → 16 (@ `ff8dc08`), #82 **+9** → 25 (@ `d831745`), #83 **+0** (@ `3f777a7`); window base `ffa139a` = 0. | Verified at the pin: `grep -c 'font-size: 0.62rem' app.css` → 25 @ `9af86f2`; sub-0.72rem census → 225; floor string read at `scripts/smoke_test.mjs:157–159`. Per-bundle counts from `git show <sha>:app.css` at the named merge commits. |
| F5 | **The only gate that could catch it was switched off and double-swallowed.** Per the owner's experimenting ruling (`.orchestrator/RULING_GATES_EXPERIMENT_2026-09-14.md` — text-integrity gates stay ON, presentation is allowed to break while experimenting), the two presentation steps carry `continue-on-error: true` **and** an `|| echo` guard (`.github/workflows/quality.yml:52–60` mirror-diff, `:62–65` smoke), so a red smoke test reads `success` in the CI jobs view. The one presentation-adjacent gate kept on, `scripts/test_website_ruling.py`, enforces the *law* by reading governance prose — it never opens `app.css`/`app.js`/`index.html`. | Verified at the pin: read `quality.yml:52–68` and `scripts/test_website_ruling.py` @ `9af86f2`; smoke reproduces `exit 1` offline while the main-CI job reports the step green. |
| F6 | **No pre-merge owner rating ever happened.** The site's own variant protocol requires "one variant per PR <2h … owner picks which numbers to implement first **after rating 1-10**" (`.orchestrator/LAYOUT_VARIANTS_2026-09-14.md`), and its prompt records the bind that "untested PRs have to be merged first" (`.orchestrator/prompts/025-phase5-five-design-switcher.md`). What executed was 8–10 variants per PR merged in minutes — PR #79 23:56:48→00:05:12 (~8 min), #80 00:40:32→00:42:41 (~2 min), #81 01:33:45→08:10:49 (~6 h 37 m, overnight), #82 08:55:21→09:03:49 (~8 min), #83 09:45:17→09:56:21 (~11 min) — leaving no window for a 1–10 round-trip; none is recorded in `.orchestrator/STATE.md` or `sessions/`. | Verified: PR created/merged timestamps for #79–#83; the two governing docs read @ `9af86f2`; `STATE.md`/`sessions/` carry no Phase-5 rating or progress entry. |
| F7 | **Variant 36 is mechanically clean yet assimilated the owner's zip into the shared skeleton.** The owner's zip prototype ("The Chan Room", a React/Vite/TypeScript app) sits at the repo root as `chan-buddhism-digital-library.zip` (**293,147 B**, @ `9af86f2`). The current v36 was ported as a **pure append** at the end of `app.css` (+916/−0) under `:root[data-design="36"]`, registered as switcher key 36 (`app.js:637`), applying the same `data-design` (`app.js:646`) and the same `resetLayoutRuntime()` teardown (`app.js:672–694`) as the agent fleet — i.e. it reproduced the *look* but adopted the fleet's *skeleton and switcher*, with 0 inline styles, 0 floor violations, and 13 new classes. | Verified at the pin: `app.css` tail numstat (+916/−0) and `:root[data-design="36"]` scope; `app.js:637, 646, 672–694`; `ls -l chan-buddhism-digital-library.zip` → 293,147 B; PR #83. |

The owner is the sole judge of the result. This order changes *how* variants get built and gated; it does not and cannot declare any resulting layout good — that verdict is reserved to the owner's 1–10 rating (§2, item 7).

## 2. The work order

This is a directive to the orchestrator and its agents. Items 1–4 must complete **before any layout code**; items 5–8 are the rebuild itself. The owner merges and rates.

### PHASE 0 — before any layout code

**1. The Design Grid — 33 slots, six structural axes, every combination unique.**
Author a design grid covering the 33 rebuild slots (variants 3–35). Each slot is a unique combination across exactly these six structural axes:

- **nav paradigm** (e.g. top lintel / bottom tab bar / side rail / hamburger drawer / none-scroll)
- **reading-area DOM structure** (e.g. single continuous column / paginated chapters / side-by-side panes / card stream)
- **information-architecture order** (e.g. English-first-then-source / dossier-first / teacher-first)
- **density model** (e.g. sparse single-idea / comfortable default / compact reference)
- **typography scale system** (one declared scale; every step ≥ the 0.72rem floor)
- **interaction/disclosure model** (e.g. native `<details>` / expand-on-hover / modal / two-step)

**No axis-combination may be reused across slots** — the six-tuple of every slot must be unique in the grid. This is the direct cure for F1/F2: distinctness is decided at the structural-axis level *before* implementation, not by inventing class names after. Commit the grid to the project's own `.orchestrator/` (its governance home) and **present it to the owner for approval**.

> **⛔ STOP: no rebuild starts before the owner approves the grid.**

**2. The acceptance script — dependency-free, in `scripts/`, per-variant PASS/FAIL with `file:line` evidence.**
Write one acceptance script the project owns (suggested name `scripts/check_layout_variant.py`; the exact name and language are yours, but it must run with the system's existing `python3`/`node` and require **no new dependency** — the project is registry-free by design). For a given rebuilt variant `N` it checks, against the variant's `[data-design="N"]` scope and appended blocks:

- **(a) Legibility floor** — no `font-size` below **0.72rem** introduced within the variant's scope (the per-scope enforcement of the floor the smoke harness already encodes globally at `scripts/smoke_test.mjs:157–159`).
- **(b) Inline-style invariants** — `style=` attribute count stays **0** and the `style.setProperty` census stays at the existing **4** sites; the rebuild adds none.
- **(c) Weight budget** — the variant's own CSS+JS contribution ≤ **40 KB** (a per-variant ceiling against the fleet's bloat, F2).
- **(d) Structural distinctness** — no rule body duplicated across variant scopes above a small threshold; shared-DOM deltas quantified; class-namespace reuse measured (this is the anti-F2 gate).
- **(e) Isolation** — the variant is a **pure append** to the `app.css` / `app.js` tails; neighboring variants' bytes are untouched; it is idempotent on re-apply; and it hooks the shared teardown path (`resetLayoutRuntime`, `app.js:672–694`) rather than inventing a parallel one.

The script prints **per-variant PASS/FAIL with `file:line` evidence** for every check, so each PR can quote the verdict verbatim (item 6).

**3. CI wiring — the acceptance script becomes a required check on layout-touching PRs.**
Wire the acceptance script into `.github/workflows/quality.yml` so it runs as a **required** check on any PR that touches the layout files (`app.css`, `app.js`, `index.html`, and the `docs/` mirror). For **rebuilt** variants it **replaces** the `continue-on-error` presentation steps (currently `quality.yml:53, 60, 63–65`): a red floor or a distinctness failure must *fail the PR*, not read green. **Variants 1–2 and the base shell are grandfathered** (owner ruling: floor cleanup deferred) — the script's floor/distinctness enforcement scopes to the rebuilt scopes, not to variant 1's base or variant 2's kept accordion. This **amends `.orchestrator/RULING_GATES_EXPERIMENT_2026-09-14.md` narrowly**: presentation gates *return* for rebuilds as per-variant acceptance checks, while free experimentation elsewhere continues. The required text-integrity gates (`quality.yml:38–50, 68`) are untouched and remain required.

> **⛔ STOP again: the script and the new CI check must run green on a canary — the project's choice of one grid slot — before any batch begins.** The canary is where a grid/budget/CI conflict is caught and brought to the owner *before* the fleet grows, not after.

### PHASE 1 — the rebuild batches

**5. Batch 0 = variant 36 alone, rebuilt faithfully from the owner's zip.**
Rebuild variant 36 ("The Chan Room") from `chan-buddhism-digital-library.zip`, reproducing the zip's **visual system on its own structure** — **not** assimilated into the shared skeleton (that assimilation is the specific failure of the current v36, F7). **No zip code ships verbatim** unless the owner's original directive said so: this is a *faithful implementation of the visual system*, with **native structures preserved** (the prototype's own DOM idioms, e.g. native `<details>`-style disclosure, carried over rather than flattened into the base shell's idioms). Variant 36 must pass the acceptance script (item 2) like every other rebuild. It **replaces the current v36 in the switcher when the owner rates it acceptable** — not before.

**6. Batches 1–8: four variants each, in grid order (`3,4,5,6` → … → `32,33,34,35`).**
For each variant in a batch:

- Build it on a **NEW skeleton per its grid slot** — the slot's six-axis combination must be **structurally real**: the DOM structure actually changes (nav paradigm, reading-area structure, IA order, density, disclosure), not a CSS reskin of the shared shell. A "new class namespace over the old DOM" is exactly the F1/F2 failure and fails item 2(d).
- Keep **pure-append isolation** (item 2(e)): append-only to the `app.css`/`app.js` tails, neighbors byte-untouched, idempotent, shared teardown.
- Hold the **floors and budgets** (item 2(a)–(c)).
- **Quote the acceptance script output per variant, verbatim, in the batch PR.**

**The switcher count is a non-metric.** Progress is owner-rated quality, batch by batch — the opposite of the fleet's count-as-milestone anti-pattern (F3). A batch that grows the switcher by four but earns no owner rating is not progress.

**7. Rating gates — the owner rates 1–10 before the next batch starts.**
The owner rates every variant in a batch 1–10 **before the next batch begins**. **Any variant rated < 6 is rebuilt from scratch** — from a fresh grid slot (or the same slot re-approached) — **never patched.** Batch cadence follows the owner's pace: **no schedule pressure, no count milestones** (those produced F3/F6).

**8. Carried notes (close them cleanly in your governance).**
- **The legibility regression cures itself.** The floor check in the acceptance script (item 2(a)) plus the restored required CI check (item 3) mean a sub-floor `font-size` fails the PR by construction — the F4 condition cannot ship again in a rebuilt variant.
- **The previously-promised common-qualities gate extension is SUPERSEDED by this script.** `.orchestrator/COMMON_QUALITIES_2026-09-14.md` (Enforcement) promised that `test_website_ruling.py` "will be extended to check for common qualities"; that extension never landed. This acceptance script supersedes it — record the supersession in your governance so the promised item is closed, not left dangling.

## 3. Acceptance criteria per variant (each independently checkable)

A rebuilt variant is acceptable only when **all** of the following hold:

1. **Unique grid combination implemented structurally** — the variant realizes its slot's six-axis tuple as a real DOM-structure change, and that tuple is unique across the approved grid.
2. **Acceptance script PASS for that variant** — floor (a), inline-style invariants (b), weight (c), structural distinctness (d), and isolation (e) all PASS, with `file:line` evidence.
3. **Suites green** — the required text-integrity gates (`quality.yml:38–50, 68`) pass unchanged.
4. **Switcher intact** — the variant registers in the switcher and applies/tears down through the existing mechanism (`app.js:601–694`) without breaking any other variant.
5. **Neighbors byte-untouched** — the diff is a pure append; no other variant's scope or the base shell changed.
6. **Quoted script output in the PR** — the batch PR quotes the acceptance script's verbatim PASS output for the variant.
7. **Owner rating recorded** — the owner's 1–10 rating is recorded before the next batch.
8. **< 6 ⇒ rebuild** — a variant rated below 6 is rebuilt from scratch from a fresh grid slot (or the same slot re-approached), never patched.

## 4. Explicitly out of scope

These are excluded from this order (future, separate work, or owner-deferred):

- **Variants 1–2 and the base shell** — untouched; the floor cleanup there is deferred by the owner (grandfathered, item 3).
- **Text integrity / corpus / scripts** — the Chinese corpus, translation/status machinery, and the W1/source-review suites are hard law and are **not** part of this presentation rebuild; their required gates simply keep passing.
- **New runtime dependencies** — the project is registry-free and zero-backend by design; the rebuild adds none.
- **Any base-file refactor beyond pure appends** — `app.css` / `app.js` receive appends only; no reorganization, dedup, or consolidation of existing rules (the dead copy-paste weight of F2 is a separate consolidation decision for the owner, not this order).
- **Ratings-file / infrastructure niceties** — owner-deferred; the rating is *recorded* (item 7) but no new ratings ledger or tooling is required by this order.

**This letter never authors code.** It specifies; the translatechan agents implement; the owner merges and rates.

## 5. Verification and runbook

Run from a clean `main` checkout with the system's existing `python3` / `node` (≥ the versions already used by the project). **No `npm install`, no new dependency, no browser, no credential** — the project is registry-free by design. The text-integrity suite must stay green throughout; it is unchanged by this order.

**Before batches (Phase 0):** the orchestrator commits the design grid to `.orchestrator/` and obtains owner approval (item 1); lands the acceptance script (item 2); wires it as a required check on layout-touching PRs (item 3); and runs it green on one canary slot (item 4).

**Per rebuilt variant `N` (Phase 1):**

```bash
# 1. Acceptance (the Phase-0 script; suggested invocation):
python3 scripts/check_layout_variant.py N
#    → expect per-check PASS with file:line evidence (floor / invariants / weight /
#      distinctness / isolation). Quote this output verbatim in the batch PR.

# 2. Required text-integrity gates — exactly as your CI runs them (quality.yml:38-50, 68):
python3 -m py_compile scripts/*.py
python3 scripts/validate_data.py
python3 scripts/build_data_bundle.py
python3 scripts/test_source_preservation.py
python3 scripts/test_source_review_rules.py
python3 scripts/test_website_ruling.py

# 3. Isolation proof — the variant is a pure append; neighbors byte-untouched:
git diff --stat                       # appends only at the app.css / app.js tails
grep -c 'style=' index.html           # stays 0 (inline-style invariant)
#    Confirm no rule under another variant's [data-design="M"] scope changed.
```

The existing whole-file floor grep (`scripts/smoke_test.mjs:157–159`) and the mirror/artifact check remain as they are; the new per-scope floor and distinctness enforcement live in the acceptance script, which is the required gate for rebuilds (item 3).

---

## Appendix A — Worked example (one fictional rebuild, end to end)

A fictional walk to prove every requirement above is executable as written. The variant, its output, and its rating are **illustrative**; the commands, gates, and file anchors are the real ones at the pin. (The acceptance script is a Phase-0 deliverable, so its output here is the *shape* to expect, not a real run.)

**Slot (fictional), say grid slot `v9` — "bottom-nav / single-column / progressive-disclosure", expanded to the six axes:** nav paradigm = *bottom tab bar*; reading-area DOM structure = *single continuous scroll column*; IA order = *English first, source/context after*; density model = *sparse, one unit per screen-height*; typography = *one declared scale, min 0.72rem*; interaction/disclosure = *progressive disclosure via native `<details>`*.

1. **Grid** — the orchestrator records `v9`'s six-tuple in the grid committed to `.orchestrator/`; the uniqueness check confirms no other slot shares that tuple. **Owner approves the grid** → the Phase-0 STOP (item 1) lifts.
2. **Canary already green** (item 4) → batch work may begin. `v9` is in batch 2 (`7,8,9,10`).
3. **Implement** `v9` on a NEW skeleton: a real bottom-nav `<nav>` and a single-column reading flow with native `<details>` folds — appended to the `app.css` / `app.js` tails under `:root[data-design="9"]`, idempotent, hooking `resetLayoutRuntime` (`app.js:672–694`), adding no inline style and no new `setProperty`.
4. **Acceptance** — `python3 scripts/check_layout_variant.py 9`. Illustrative PASS shape:

   ```text
   variant 9  floor:a PASS   (min font-size 0.78rem in [data-design="9"] scope; app.css:nnnn)
   variant 9  invariants:b PASS (style= 0; setProperty census 4; +0 added)
   variant 9  weight:c PASS    (14.2 KB CSS+JS ≤ 40 KB)
   variant 9  distinctness:d PASS (no rule body shared with another scope; 0 duplicated bodies; 11 new classes in ns v9-*)
   variant 9  isolation:e PASS (pure append; neighbors byte-untouched; idempotent; resetLayoutRuntime hooked)
   RESULT variant 9: PASS
   ```

5. **Suites green** — the six required text-integrity gates (§5) pass unchanged.
6. **PR** — the batch-2 PR quotes the verbatim PASS block for `7,8,9,10`; its `git diff --stat` shows appends only (`[data-design="8"]`/`[data-design="10"]` byte-untouched); the new required CI check passes.
7. **Rating** — the owner rates each of `7,8,9,10` out of 10. If `v9` earns **7** → accepted. Had it earned **5** (< 6) → `v9` is **rebuilt from scratch** under a fresh grid slot, never patched.
8. **Next batch** — batch 3 (`11,12,13,14`) starts only after all four of batch 2's ratings are recorded. The switcher count is irrelevant to this decision.

---

**Delivery:** one self-contained order. The orchestrator and its agents execute it in the target repository on their own branches; the owner approves the grid, merges each batch, and records the 1–10 ratings. Nothing in this letter touches the target, authors code, or asserts a quality judgment — that judgment is, by the project's own law, the owner's alone.
