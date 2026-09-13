# translatechan - FINDINGS & EVIDENCE PACK 2 of 2 (2026-09-13)

Complete and verbatim: the findings ledger, the Phase-1 re-verification, and the five lane letters from the review engagement (executed by a REPOTESTER-side session, gate-verified clean; delivered here by the owner's courier route). Nothing is summarized away - this is the full record.

---

# Findings ledger — translatechan review (2026-09-13, running)

- **Subject:** `56eli/translatechan` @ `main` = `6076170`
- **Access:** public read-only clone + public GitHub API; sandbox scratch under `/tmp`
  (pinned CBETA revision per R-P3 — never committed). Delivery per R-X1: letters to
  the translatechan orchestrator from this REPOTESTER review space.
- **Scope:** zone rulings R-P1…R-P3, R-W1…R-W3, R-D1…R-D3 (final), R-X1 — see
  `CHECKPOINT-C-RECORD-2026-09-13.md`. Lane order: 1 → 2 → 5 (PRODUCT), 3 (WEB),
  4 (DOCS).
- **Row states:** `OPEN—owner` (needs a ruling), `OPEN—orchestrator` (review
  continues), `VERIFIED` (check passed, evidence cited), `CLOSED` (resolved with
  evidence). Every row carries its zone, lane, and file:line / SHA anchors.

## Lane 1 — provenance-integrity (first rows, 2026-09-13)

### Verified baseline (evidence this session, on `main` 6076170)

- **V-1 · VERIFIED — reference layer reproduces from the pinned revision.**
  Fetched `cbeta-org/xml-p5` @ `dbdea41071e1e260ad84b72faefd4587333cf76d`
  (R-P3), sparse-checked out exactly the 39 manifest works.
  `scripts/collate_refs.py --source-dir /tmp/xmlp5 --out-dir /tmp/refs
  --work-list/--verify-against sessions/COLLATION_W1_2026-09-10_refs_manifest.txt
  --upstream-revision dbdea410…`: **39 verified, 0 drift, 0 unlisted, 0
  unavailable**; freshly written digest manifest byte-identical to the committed
  authoritative manifest (`cmp` clean).
- **V-2 · VERIFIED — the published post-remediation record is independently
  reproducible.** `COLLATION_REFS=/tmp/refs python3 scripts/collate_corpus.py
  --reproduce sessions/COLLATION_REGISTER_2026-09-10_CORRECTION.json`: output
  byte-identical across two consecutive runs; per-document flagged/status/
  collating fields match `sessions/COLLATION_REGISTER_2026-09-12_POSTREMEDIATION.json`
  for **all 35 documents**; aggregate 532 flagged / 691 of 924 content fields
  collating / statuses 1-32-2 — the figures quoted in README/AUDIT/HANDOFF are
  arithmetic over the pinned refs + current data, not prose.
- **V-3 · VERIFIED — the single `collated_to_claimed_witness` document is
  genuinely collated.** `zhengdao_ge` vs T48n2014: content fields **6/6 EXACT**;
  the one NOT_FOUND flag is `.title_zh` (metadata — excluded from the content
  denominator by the documented evidence model; `metadata_summary: {NOT_FOUND: 1}`,
  `content_summary: {EXACT: 6}`). The completion rule
  `complete ⇔ complete_selected_witness + collated_to_claimed_witness` holds with
  0 documents currently `complete_selected_witness` — the W1 status is
  containment/remediation, exactly as disclosed.
- **V-4 · VERIFIED — containment boundary intact in the shipped bundle.**
  `congronglu`: 0 occurrences in `app_data.js`; `data/corpus/congronglu_cases.json`
  absent; not in `corpus_manifest.json`. Residuals are 3 glossary `occurrences`
  cross-reference strings + 5 `gongan_index` `cross_refs` strings (no source
  text). Containment record: `sessions/CONTAINMENT_2026-08-10_CONGRONGLU.md`.
- **V-5 · VERIFIED — all five quality gates pass on `main`** (py_compile;
  validate_data — 3 documented lineage warnings; build_data_bundle —
  app_data.js 1,641,935 B byte-identical rebuild; smoke_test incl.
  source-preservation vs pinned base 3cc7a8e9, 0 unauthorized changes;
  `diff -rq data docs/data`).
- **V-6 · VERIFIED — zero automated third-party requests in the pipeline.**
  No HTTP-client imports in `scripts/*.py`; CBETA URLs appear only as provenance
  constants/doc references (`collate_refs.py:88`, `w1_evidence.py:96`).

- **V-7 · VERIFIED — the 6-ref drift note is exact.** The 2026-09-09 candidate
  manifest (187 refs) vs the authoritative 2026-09-10 set (39 refs): exactly 6
  refs differ in digest (T47n1987B, T48n2001, X67n1309, X68n1315, X69n1333,
  X73n1445) — matching STATE.md's "6 drifted references" — and they map to the
  8 documents the harness lists as `documents_with_drifted_references`
  (X68n1315 shared by baizhang_guanglu/foyan_qingyuan/nanquan_yulu). All 8 are
  `partial_or_failed_w1_collation`: the drift changes no verdict, as stated.
- **V-8 · VERIFIED — edition-verified badge linkage.** 177 corpus + 2 matrix
  `verified_quotation` records (179 total): every one carries work/edition/
  verification/reference fields and resolves its `source_id` into
  `data/translations/rights_manifest.json` (14 source records). Exactly **3**
  references carry explicit pending markers (zhaozhou_yulu ×2 "X68n1315
  (candidate, unverified)… page pending"; matrix_wumen_1 "Hokuseido print page
  pending") — HANDOFF's "176 / 179; 3 explicitly pending" is arithmetic, not
  prose.
- **V-9 · VERIFIED — the Robo-disclosure layer is complete.** All **1,252**
  translation slots carry an explicit status (876 `reconstruction_unverified` /
  199 `ai_draft` / 177 `verified_quotation`); **0** bare-string translation
  values remain (migrated 2026-08-09, validator rejects new ones). The reader
  renders the three badges (✅ Edition-verified quotation / 🤖 Robo draft / 🤖
  Robolation) plus the real-fakeness popover and the tooltip "AI text in a
  translator's register — not their actual words" (`app.js:2102–2115`, `:2394`,
  `:2398`, `:376`). The removed `window.TranslateChan.getSourceReviewStatus`
  API is absent from `app.js` (smoke-guarded).
- **V-10 · VERIFIED — the two `witness_unavailable` documents claim honestly.**
  `hanshan_poems` (manifest cbeta `SBCK/Zoku`, doc note: "Hanshan's poems are
  not in Taishō proper"; the old Taishō location claim was removed 2026-08-08)
  and `niutou_juezhu` (Dunhuang P.2885/S.5619, "no Taishō volume"). Both are
  `excerpt_seed`; no Taishō/CBETA witness claim is asserted anywhere for them.
- **V-11 · VERIFIED — rights ledger matches AUDIT exactly.** 14 rights records:
  `review_status` 12 `needs_rights_review` + 2 `jurisdiction_review_required`
  (AUDIT.md §1: "12 sources need rights review; 2 need jurisdiction review");
  `rights_status` 11 `copyrighted_or_rights_uncertain`, 2
  `public_domain_claimed_us`, 1 `online_rights_unverified`.
- **V-12 · VERIFIED — no field-level witness assertion rides on a
  fabrication-suspect field.** The 310 NOT_FOUND content fields sit inside
  documents whose always-visible W1 ledger state is
  `partial_or_failed_w1_collation` (smoke-guarded reader display); field-level
  notes (R-B `editorial_note` labels, `cbeta_note` corrections) cover the
  retained retellings; the one withdrawn claim (zhaozhou T1987) is disclosed in
  manifest + prose (PR #43). The residual unadjudicated fields are the
  predecessor campaign's owner-held queue (Ruling 3; one document per PR),
  recorded in `.orchestrator/PHASE2_PLAN.md` — not a shipped-surface defect.

### Defects

- **D-1 · OPEN—owner · MINOR · lane 1/4 · STATE.md continuation wording.**
  The cold-start Continuation block (`.orchestrator/STATE.md` on `main`, added by
  PR #44) says: "Reproduce the authoritative register byte-for-byte with
  `… collate_corpus.py --out /tmp/register.json --reproduce
  sessions/COLLATION_REGISTER_2026-09-10_CORRECTION.json` (register sha256
  `5369af11…`)". Measured: `5369af11…` is the sha256 of the **committed file**
  (integrity of the evidence record — it matches). The `--reproduce` command
  replays the register's `generation_parameters` against the **current** data and
  writes the current-state register (532 flags) with a reproduction-comparison
  block; its output hash is recorded nowhere and it does not (cannot) re-emit the
  historical 630-flagged file's bytes. The evidence itself is sound (V-1…V-3);
  the wording conflates a file-integrity hash with a reproduction output. Ruling
  needed: wording fix in the tracker (docs-only) or accepted-as-is. [Lane 4
  classifies this within the predecessor-trace follow-through; recorded here
  because Lane 1 ran the measurement.]
- **D-2 · OPEN—owner · MINOR · lane 1/4 · README profile figure stale.**
  `README.md:151` (repository-structure tree): "translator_profiles.json #
  Evidence-grounded Robo-translator personalities (**13** in-corpus-verified;
  **7** documented-external)". Live data (measured 2026-09-13): 21 profiles =
  **14** `in_corpus_verified` + **6** `documented_external` + 1 `not_applicable`
  (`ai_literal`, reclassified since the 2026-08-10 audit's 7-external list).
  The README is in the doc-truthfulness gate set, but this figure is not among
  the enforced numbers (gate passes) — same coverage pattern as O-1. Docs-only
  fix; ruling with O-1.

### Opportunities

- **O-1 · OPEN—owner · lane 4 · doc-truthfulness gate coverage.** The census
  prose in `ROADMAP.md:163,:179`, `WEB_VISION_2026-08-10.md:57,:59,:88,:90,
  :327`, `RESEARCH_RELEASE_PLAN.md:32,:103` still asserts 49/38/22/16; live
  main measures 50 strings / 39 rendered / 23 labelled documents / cbeta_note
  17 (measured 2026-09-13; successor's task 014b item 1, unexecuted). The
  doc-truthfulness gate (README/HANDOFF/AUDIT/ROADMAP/index.html +
  .orchestrator/REMEDIATION_PLAN.md + STATE.md, per P-6) passes with these
  lines present — the census figures are not among the pinned numbers, and
  WEB_VISION_2026-08-10.md / RESEARCH_RELEASE_PLAN.md are outside the scanned
  set. Decision record for the owner (R-D2 sub-scope d): which stale prose
  should join the enforced set. Not fixed unasked.
- **O-2 · OPEN—orchestrator · lane 2 · defense-in-depth in
  `arena_agent_pipeline.create_translation_entry`.** The helper accepts a
  caller-supplied `status` override and does not self-validate its output; a
  `verified_quotation` without a complete rights-linked source object would be
  caught only at the gate (P-4/P-5 show that backstop is real, so no defect is
  observed — 0 malformed entries exist in the committed data). Suggested
  improvement: reject (or ignore) an explicit `verified_quotation` status
  lacking a full source record inside the helper, so the constraint holds
  pre-PR as well as at the gate. Optional; the gate suffices as things stand.
- **O-3 · OPEN—orchestrator · lane 5 · artifact-diff robustness.** The
  Edit-1 gap (C-2) exists because the diff step enumerates file paths;
  adding four paths cures today's gap but the same class of drift returns
  whenever a fifth mirrored asset is added. Suggested shape (for the
  receiving orchestrator's Edit-1 PR, owner's call): diff the mirror tree —
  `git diff --exit-code -- app_data.js docs data/project_metrics.json` — so
  coverage is structural, not enumerated. Optional; either form is a gate,
  the enumerated one is just re-openable by omission.

### Decision records (this engagement)

- **DR-1.** R-P3 — CBETA pinned-revision authorization (verbatim in the
  Checkpoint-C record; scope limits: `cbeta-org/xml-p5` @ `dbdea410…` only,
  read-only, never committed, Lanes 1–2 only; everything else discovery-only).
- **DR-2.** R-X1 — delivery model: REPOTESTER review space as the foundation for
  letters to the translatechan orchestrator for independent review and
  verification (verbatim in the Checkpoint-C record).
- **DR-3.** R-D3 (final) — canonical tracker = `.orchestrator/STATE.md` on
  `main` (verbatim + four confirmed consequences in the Checkpoint-C record).

## Lane 1 — verdict (2026-09-13)

**The shipped surface is contained.** Every W1 claim that reaches a reader is
backed by the pinned, digest-verified reference layer: the status model
(1/32/2) re-derives to the same per-document result from the pinned refs +
current data (V-1, V-2); the single `collated_to_claimed_witness` document
collates 6/6 content fields EXACT (V-3); the Congronglu quarantine holds in the
shipped bundle (V-4); edition-verified badges are fully rights-linked with the
3 pending references explicitly disclosed (V-8); the Robo-disclosure layer
covers 100% of slots (V-9); the unavailable-witness documents and the withdrawn
zhaozhou claim are disclosed, not asserted (V-10, V-12); the rights ledger
matches the audit exactly (V-11). No generated text wearing a witness claim was
found in the shipped surface; the residual unadjudicated fields are the
predecessor campaign's owner-held queue, not a surface defect (V-12).
Open rows: D-1, D-2, O-1 (all doc-precision, owner rulings).

Letter to the translatechan orchestrator: `letters/LANE1-PROVENANCE-2026-09-13.md`.

### Lane 2 — data-pipeline (PRODUCT)

- **P-1 · VERIFIED — the generated bundle rebuilds byte-stable from `data/`.**
  `python3 scripts/build_data_bundle.py` (post-reset, main `6076170`) compiles
  35 documents → `app_data.js` **1,641,935 B**, sha256 identical to the
  committed file; `docs/` mirror re-syncs; the exact quality.yml artifact-diff
  step (`git diff --exit-code -- app_data.js docs/app_data.js docs/index.html
  docs/app.css docs/app.js docs/data data/project_metrics.json`) is clean.
- **P-2 · VERIFIED — all five quality-gate steps pass (post-reset re-run).**
  (1) `python3 -m py_compile scripts/*.py` · (2) `python3 scripts/validate_data.py`
  (full, incl. doc-truthfulness) · (3) bundle rebuild · (4) artifact diff ·
  (5) `node scripts/smoke_test.mjs` → "35 corpus texts exercised, 0 crashes";
  W1 source-review rule suite OK (app.js mirror pinned to metrics);
  **source-preservation suite: 35 corpus files match base commit `3cc7a8e9`
  apart from allowlisted remediation pointers, 0 unauthorized changes**.
- **P-3 · VERIFIED — the script chain is as documented; the brief's head name
  is superseded.** Actual chain: `segment_classical.py` (offline sentence
  segmenter; manual input; docstring: does NOT fetch from CBETA — "Phase-2
  ingestion-tooling goals") → collation (`collate_corpus.py` /
  `collate_refs.py` / `w1_evidence.py`, Lane 1) → `source_review.py` (shared
  W1 status vocabulary + completion/source-review compatibility rule, imported
  by the validator, harness and regression tests so they cannot drift) →
  `validate_data.py` → `build_data_bundle.py` → `app_data.js`.
  `ingest_cbeta.py` is a 24-line deprecated `runpy` shim pointing at
  `segment_classical.py` (renamed 2026-08-09; README.md:163 documents the
  shim accurately). No network code in any script (V-6).
- **P-4 · VERIFIED — the agent-pipeline constraint model.**
  `scripts/arena_agent_pipeline.py` provides (a) three prompt templates whose
  output JSON schemas carry **no** provenance fields (provenance is enforced
  downstream by design) and (b) `create_translation_entry()`, which attaches
  safe status defaults (`reconstruction_unverified` / `ai_draft`), labels AI
  output ("Arena AI Agent (model)"), and requires a full
  `{work, edition, reference, verification, source_id}` source object for
  `verified_quotation` whose `source_id` must exist in the rights manifest.
  The helper accepts caller-supplied status overrides; the hard enforcement
  point is the validator at the gate — its docstring claim ("the validator
  will refuse the commit") is **verified true** by mutation testing (P-5).
  Zero entries in the helper's output label ("Arena AI Agent (…)") exist in
  the committed data; the matrix's single `ai_draft` (entry
  `matrix_wumen_1`) is labelled "AI Multi-Draft Engine" and disclosed as AI.
  Matrix composition: 4 entries / 21 translator records
  (18 reconstruction_unverified, 2 verified_quotation, 1 ai_draft).
- **P-5 · VERIFIED — the validator backstop is real (5/5 mutations refused).**
  In an isolated copy (baseline PASS): (M1) `verified_quotation` with a
  `source_id` absent from the rights manifest → refused ("verified quotation
  source_id(s) missing from rights manifest"); (M2) missing `reference` →
  refused; (M3) missing `status` → refused; (M4) legacy bare-string
  translation value → refused ("legacy string translation; use { text, status }
  (run scripts/migrate_translations.py)"); (M5) identical case-level
  `commentary_zh` (≥12 chars) across 3 cases → refused — this is the
  **code-level regression check for the 2026-08-10 Congronglu incident**
  ("identical {field} appears in N cases … quarantine or mark generated
  placeholders outside canonical source fields"). Restored copy passes again.
  The containment that the 2026-08-10 pass described in prose is enforced in
  code, not only asserted in docs.
- **P-6 · VERIFIED — doc-truth gate scope (measured, broader than documented).**
  Snippet rules span README.md, HANDOFF.md, index.html, **AUDIT.md,
  ROADMAP.md**; W1-claim rules add `.orchestrator/REMEDIATION_PLAN.md` and
  check `.orchestrator/STATE.md` (must quote the authoritative flagged total
  and label the superseded figure); line-level scans forbid, across those
  files: unqualified superseded totals (637 / historical register total),
  unexplained `T1987` (must say Caoshan/false), the fabricated identifier
  `X68n1315A`, unqualified "of 34 evaluated", hand-typed bundle byte counts,
  and the phrases "rights approved" / "approved for reuse" / "cleared for
  redistribution" / "rights review complete". O-1 refinement: the 49/38/22/16
  census figures are **not** among the pinned numbers, and
  WEB_VISION_2026-08-10.md / RESEARCH_RELEASE_PLAN.md are outside the scanned
  set — so the stale census lines pass the gate; the gate-coverage ruling is
  still the owner's.
- **D-3 · OPEN—owner · MINOR · lane 2/4 · validator docstring under-describes
  the doc-truth gate.** `scripts/validate_data.py` docstring: "live prose docs
  (README.md, HANDOFF.md, index.html) quote the same deterministic numbers".
  Measured gate also covers AUDIT.md, ROADMAP.md,
  .orchestrator/REMEDIATION_PLAN.md, .orchestrator/STATE.md (P-6) — broader
  than documented (good direction; a maintainer reading the docstring would
  underestimate what rewording a document can break). Wording fix; batchable
  with D-1/D-2.

## Lane 2 — verdict (2026-09-13)

**The pipeline chain is reproducible and the backstop is real.** The bundle
rebuilds byte-stable from `data/` (P-1); all five gate steps pass (P-2,
including the source-preservation suite that pins 35 corpus files to base
commit `3cc7a8e9` with an explicit allowlist); the chain matches the
documentation once the deprecated `ingest_cbeta.py` shim is accounted for
(P-3); the agent pipeline constrains status/provenance at construction with
the validator as the hard enforcement point, and that enforcement is proven by
mutation testing, including the code-level regression check for the 2026-08-10
Congronglu incident (P-4, P-5); the doc-truth gate's measured scope is broader
than its docstring states (P-6, D-3). Open rows from this lane: D-3, O-2.

Letter to the translatechan orchestrator: `letters/LANE2-PIPELINE-2026-09-13.md`.

### Lane 5 — CI/workflow (PRODUCT)

- **C-1 · VERIFIED — what gates actually run on PRs, and the cited suites
  are wired in.** `.github/workflows/quality.yml` is the only workflow; it
  triggers on PRs → `main` and pushes to `main` + `arena/**`, with
  `permissions: contents: read` only (no secrets, no write, no third-party
  credentials). All five steps run on every PR: py_compile ·
  `validate_data.py` (data + metrics + doc-truth) · bundle rebuild ·
  artifact diff · `smoke_test.mjs`. The smoke test is a hub: besides the
  35-text render exercise and composition checks it **spawns
  `scripts/test_source_review_rules.py` and `scripts/test_source_preservation.py`**
  (smoke_test.mjs:567-579, :588-592) — so the W1 rule suite and the
  source-preservation suite cited in the audits do run in CI, via the hub.
  `browser_test.mjs` is deliberately not in CI: package.json describes it as
  "Optional real-browser regression suite (dev-only; not required for
  contributors or CI)" — the frozen PR-A territory (R-W2), documented, not a
  gap.
- **C-2 · VERIFIED — Edit 1's gap is open and exactly measured.** The
  artifact-diff step lists 8 paths; `build_data_bundle.py` mirrors exactly 7
  files (`index.html app.css app.js theme-init.js robots.txt sitemap.xml
  og-image.svg`, build_data_bundle.py:105) + the `data/` tree. The diff list
  omits **`docs/theme-init.js`, `docs/robots.txt`, `docs/sitemap.xml`,
  `docs/og-image.svg`** — exactly the four Edit 1 names. `docs/audits/` and
  `.nojekyll` are not build-mirrored (static), so they are outside Edit 1's
  "mirrored deploy assets" scope (nuance recorded, not a finding).
- **C-3 · VERIFIED — Edit 2 is open (measured 2026-09-13).** Workflow pins:
  `checkout@v4`, `setup-python@v5`, `setup-node@v4`; latest releases per
  GitHub API today: checkout `v7.0.1`, setup-python `v7.0.0`, setup-node
  `v7.0.0` (the same v7 line OPERATIONS.md reported on 2026-08-10). All three
  current pins target deprecated Node 20 runtimes.
- **C-4 · VERIFIED — Edit 3 remains owner-side; Pages model confirmed.**
  Branch-protection read: HTTP 403 "Resource not accessible by integration"
  for this session's token (same result the audit integration got — so the
  "protection definitely disabled" claim is correctly not made in
  OPERATIONS.md). Pages API: `status: built`, source `main` / `/docs`,
  `https_enforced: true` — native publication from the committed mirror, no
  deploy workflow needed, as OPERATIONS.md states.
- **C-5 · VERIFIED — dependency-free by design (no supply-chain surface in
  the pipeline).** All 15 scripts are stdlib-only (no requirements/manifest);
  CI runs system Python 3.12 / Node 22 via the (deprecated-major) setup
  actions; the only JS dependency anywhere is `playwright` in
  `devDependencies`, gated behind the opt-in `test:browser` script (browser
  test, dev-only).

## Lane 5 — verdict (2026-09-13)

**The gates run, the cited suites are wired in, and the three documented
edits are exactly where the docs say they are.** Every PR to main runs all
five steps (C-1), including the two Python suites embedded in the smoke-test
hub; the pipeline is dependency-free by design (C-5). Edits 1–3 remain open:
Edit 1's gap is precisely the four named mirror files (C-2, with O-3's
structural-diff suggestion); Edit 2's pins are still one to three majors
behind the v7 line (C-3); Edit 3 is unverifiable from this session's grants
(403, matching the audit integration) and owner-side by nature (C-4). No new
defects; the rows feed the canonical-tracker item already proposed in the
Lane 1 letter.

Letter to the translatechan orchestrator: `letters/LANE5-CI-2026-09-13.md`.

### Lane 3 — SPA integrity (WEB zone; repo gates only per R-W3)

- **W-1 · VERIFIED — "no HTML inline styles" (README.md:30).** `index.html`:
  **0** `style=` attributes, **0** `<style>` blocks. True as worded (the
  claim scopes to HTML).
- **W-2 · VERIFIED (exact count) — the inline-style inventory.** `app.js`:
  **41** `style=` attribute literals (all in live render templates; 0 in
  comments; incl. the `lang="zh"` classical blocks at :1805/:1810) **+ 17**
  `.style.prop =` writes (15 `display`, 1 `left`, 1 `top`; the 9 comparison
  reads excluded) = **58 JS inline-style injection sites**. HANDOFF.md:110's
  "Forty-one JS-generated inline styles" matches the attribute-literal
  mechanism exactly but under-states the total JS injection surface by the
  17 property writes → **D-4**.
- **W-3 · VERIFIED — CSP.** Full shipped tag (index.html): `default-src
  'self'; script-src 'self'; style-src 'self' 'unsafe-inline'
  https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;
  img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri
  'none'; form-action 'none'`. HANDOFF's "keeps CSP style-src 'unsafe-inline'
  necessary" is accurate given W-2's 58 injection sites.
- **W-4 · VERIFIED (CSS-existence level) — responsive + reduced-motion
  claims (README.md:30).** 4 × `@media (max-width: 1024px)` (incl.
  `.sidebar-panel { display: none }` — the "shelf collapse" — plus mobile
  corpus picker, graph toolbar, master-directory reflow) and 6 × `@media
  (max-width: 768px)` (mobile layout); 14 `@media` total incl. 1
  `prefers-reduced-motion` block with `animation: none`. Behavior-level
  verification (actual pixel/interaction behavior) is outside repo gates
  (R-W3; frozen PR-A territory) — the claims are substantiated at the CSS
  existence level.
- **W-5 · VERIFIED (markup level) — keyboard tabs + lang="zh" (README.md:28,
  :30).** `role="tablist"` ×1, `aria-selected` ×1, `tabindex` ×8,
  `:focus-visible` ×14 (app.css); `lang="zh"` ×26 (app.js) + ×10 (index.html).
- **W-6 · VERIFIED — performance claims are bounded/qualitative.** The only
  perf claim in the shipped docs is "Fast, zero-backend, responsive SPA"
  (README.md:116) — qualitative; no numeric in-repo claim to falsify.
  "Zero-backend" verified: Pages publishes natively from `main`/`docs` (C-4),
  no server code in the repo. Measured uncompressed payload: app.js 173,282 B
  + app.css 67,165 B + app_data.js 1,641,935 B + index.html 17,767 B +
  theme-init.js 876 B = **1,901,025 B**.

- **D-4 · OPEN—owner · MINOR · lane 3/4 · disclosed inline-style count
  under-states the JS injection surface.** HANDOFF.md:110: "Forty-one
  JS-generated inline styles keep CSP `style-src 'unsafe-inline'`
  necessary." Measured: 41 attribute literals + 17 `.style.prop` writes =
  58 injection sites (W-2). No behavior issue (CSP covers both mechanisms,
  W-3); the disclosed figure is one mechanism's count. Wording/count fix;
  batch with D-1/D-2/D-3.

## Lane 3 — verdict (2026-09-13)

**The shipped SPA's claims are substantiated at the repo-gate level, with
one disclosure-precision fix.** The HTML is inline-style-free as claimed
(W-1); the exact JS inline-style inventory is 41 attribute literals + 17
property writes = 58 sites, against the disclosed "41" (W-2, D-4 — wording
fix, no behavior issue since the CSP's `style-src 'unsafe-inline'` covers
both, W-3); responsive/reduced-motion/keyboard/lang="zh" claims are
substantiated at the CSS/markup existence level (W-4, W-5, behavior-level
verification stays in the frozen PR-A territory per R-W3); performance claims
are qualitative with no falsifiable in-repo numbers, and the payload is
measured (W-6).

Letter to the translatechan orchestrator: `letters/LANE3-SPA-2026-09-13.md`.

### Lane 4 — prior-audit follow-through (DOCS zone, R-D1…R-D3)

Finding-level ledger over the 2026-08-10 audit wave
(`FULL_AUDIT_2026-08-10_019feaf5.md`, `AUDIT_2026-08-10_session.md`,
`AUDIT_UPDATE_2026-08-10_hero.md`) + subsequent sessions/ reports, against
the current index `AUDIT.md` (§4) and live `main` `6076170` (measured
2026-09-13). Classes: **CLOSED** (fix verified with anchor) / **DEFERRED**
(owner-held or frozen, with its holding place) / **OPEN** (still true, live
in AUDIT §4 or measured open) / **LOST** (no trace).

**Headline: zero findings were LOST.** Every wave finding resolves to
CLOSED with a verification anchor, DEFERRED with its holding place, or OPEN
in the current AUDIT.md §4.

#### Sub-scope A — source-quality misses

| # | Finding (wave) | Class | Evidence anchor |
|---|---|---|---|
| A-1 | Congronglu generated source-looking placeholders (2026-08-10 containment incident) | **CLOSED** | Seed removed: 0 occurrences in shipped `app_data.js`, `congronglu_cases.json` absent (V-4); regression check in code: identical case-level source field ≥12 chars across ≥3 cases fails validation (P-5, M5); doc-gate forbids unmarked placeholders (P-6). |
| A-2 | Zhaozhou false canonical claim (T1987 = Caoshan record) | **CLOSED** | Re-keyed to X68n1315 (Guzunsu yulu); doc-gate *requires* the false-claim explanation and forbids unexplained T1987 and the fabricated `X68n1315A` identifier (P-6; LANE-1 V-12; PR #43). |
| A-3 | Fabricated preface/verses inside former `complete_selected_witness` texts | **DEFERRED (owner-held)** | W1 containment model (1/32/2) + per-document remediation queue, one document per PR (Ruling 3; `.orchestrator/PHASE2_PLAN.md`); README must keep stating no current `complete_selected_witness` (gate-pinned, P-6). |
| A-4 | 22 documents with no collating source-content field; 630→532 flagged fields | **DEFERRED (owner-held)** | Register 630 stays authoritative per owner ruling 2026-09-12 (PR #41 does not supersede); 532 is today's `main` measurement (V-2; AUDIT.md §1, gate-pinned). |

#### Sub-scope B — AUDIT.md §4 active blockers (all 11 measured 2026-09-13)

| # | AUDIT §4 item | Class | Measured state / anchor |
|---|---|---|---|
| B-1 | P1.1 Quotation rights (14 sources human/jurisdiction pending) | **OPEN / DEFERRED (human, owner-held)** | 12 `needs_rights_review` + 2 `jurisdiction_review_required` (V-11). |
| B-2 | P1.2 Source depth (1/35 collated; remediation incomplete) | **DEFERRED (owner-held campaign)** | A-3/A-4. |
| B-3 | P2.3 Browser evidence (Playwright silent skip; not required in CI) | **DEFERRED (frozen PR-A, R-W2)** | package.json: "dev-only; not required for contributors or CI" (C-1); AUDIT §5 SKIP record. |
| B-4 | P2.4 CI coverage (4 mirrored assets omitted; no browser/a11y/link/perf checks) | **DEFERRED (Edit 1, owner)** | Exactly 4 files: theme-init.js/robots.txt/sitemap.xml/og-image.svg (LANE-5 C-2); O-3 structural-diff option. |
| B-5 | P2.5 Performance (data global + hidden views initialize up front) | **DEFERRED (frozen PR-D, measure-first, R-W2)** | Measured: index.html eager `theme-init.js → app_data.js → app.js`; bundle 1,641,935 B — under the 2 MB P2 threshold FULL_AUDIT §12 Tier-3 sets, so it stays P3 by that rule. |
| B-6 | P2.6 CSP/style debt ("41 JS-generated inline styles") | **OPEN (count corrected; debt stands)** | Measured 58 sites (41 literals + 17 property writes) — D-4; `style-src 'unsafe-inline'` load-bearing (W-3). |
| B-7 | P2.7 Validation depth (JSON Schema not executed; non-case field validation weaker) | **OPEN (still true; no closure/deferral record found — live P2, not lost)** | Code anchor: `validate_data.py` loads the schema but only checks it is a schema document (no execution; dependency-free by design); `cross_refs` unvalidated (0 mentions in validator); `evidence_source` absent from `schemas/translatechan-data.schema.json`. |
| B-8 | P3.8 Repo description/homepage/topics empty; license NOASSERTION | **OPEN (still true)** | Measured via API: description null, homepage null, topics []; LICENSE present, spdx_id null (dual MIT/CC-BY-SA → NOASSERTION). |
| B-9 | P3.9 Google Fonts third-party runtime request; no SECURITY.md | **OPEN (still true)** | Measured: fonts.googleapis.com/gstatic links present (W-3 CSP hosts); `SECURITY.md` absent. |
| B-10 | P3.10 SVG social cards uneven support; no PNG fallback | **OPEN (still true)** | Measured: `og:image` → og-image.svg only; no `docs/*.png`. |
| B-11 | P3.11 Three lineage profiles lack linked corpus keys; 30 edges await locators | **OPEN (still true; disclosed)** | Measured exactly 3 empty `linked_corpus_keys` (prajnatara, yangqi_fanghui, dahong_zuzheng — the validator's live warnings); 30 edges + 4 frontiers, all traditional/pending (gate-pinned AUDIT §1); UI shows "not yet curated" notices (P-5 warnings are by design). |

#### Sub-scope C — predecessor open items (record-only, live-verified)

| # | Item | Class | Anchor |
|---|---|---|---|
| C-1 | Stale census lines 49/38/22/16 (task 014b item 1) | **OPEN — live-verified this session** (4 lines re-located; live measures 50/39/23/17) | O-1 (gate-coverage ruling = sub-scope D). |
| C-2 | `dahui_hongzhi` manifest-vs-document disclosure (014b item 2) | **DEFERRED (record-only)** | Recorded in LANE-1 letter §4; not resumed. |
| C-3 | `platform_sutra` text decision (précis vs re-key T48n2007) | **DEFERRED (owner-held)** | Provenance-labelled (LANE-1 letter §4 item 1). |
| C-4 | OUT-OF-CBETA human-sourcing queue (31 documents) | **DEFERRED (owner-held; no agent fetch/transcription)** | LANE-1 letter §4 item 2. |
| C-5 | Frozen tracks PR-A (real-browser) / PR-B (CSP) / PR-D (perf) | **DEFERRED (frozen; measured/reported, not resumed, R-W2)** | B-3/B-5 anchors. |
| C-6 | Witness inventories + channel branch contents | **RECORD-ONLY** | Standing constraint; inventoried in Phase 1 record §2. |

#### Sub-scope D — gate-coverage fact (R-D2 sub-scope d)

- **O-1 (decision record for the owner, unchanged):** the doc-truth gate's
  measured scope (P-6) does not pin the 49/38/22/16 census figures, and
  WEB_VISION_2026-08-10.md / RESEARCH_RELEASE_PLAN.md are outside the scanned
  set — so C-1's stale lines pass the gate. Which stale prose joins the
  enforced set is the owner's ruling; no fix opened unasked.

#### Wave §11/§12 and session-audit §3/§4/§6 line items (16 + 5 tiers + 6 drift spots)

| Wave finding | Class | Anchor |
|---|---|---|
| §11.1 CI diff missing files | DEFERRED (Edit 1) | B-4 |
| §11.2 Branch protection | DEFERRED (Edit 3, owner; 403 here) | LANE-5 C-4 |
| §11.3 OG description brand voice | **CLOSED** | Measured og:description now the accurate disclosure sentence (no "channels"/"robolates"). |
| §11.4 / §11.14 Hero chips aria-hidden | **CLOSED** | All 8 remaining aria-hidden wrap decorative glyphs only (brand FC, ⌕/🔍, ☾, ⓘ, Aa, hero-stamp); stats parent carries aria-label + 2 `aria-live` regions (WEB_VISION:88 pattern). |
| §11.5 Mobile bar <44px + safe-area | **CLOSED** | 44px ×2 + `env(safe-area-inset-bottom)` ×2 in app.css. |
| §11.6 Toolbar z 20 vs strip z 40 | **CLOSED** | `.reader-toolbar` now z-60 above case-strip (label z-1; strip container no competing sticky z). |
| §11.7 Graph width lower bound 720 | **CLOSED** | app.js:2652 `Math.max(360, svg.clientWidth \|\| 900)` (WEB_VISION:109). |
| §11.8 Search ellipsis inconsistency | **CLOSED** | All 3 placeholders use "…". |
| §11.9 Footer quote inline opacity | **CLOSED** | No `opacity:0.7` inline remains in app.js/app.css. |
| §11.10 6 masters empty linked_corpus_keys (2 historical) | **PARTIALLY CLOSED** — 6 → 3; the 3 remaining are frontier scaffolds, disclosed | B-11 (exactly the 3 named in AUDIT P3.11). |
| §11.11 Gongan cross_refs unvalidated | **OPEN** | B-7 anchor (validator: 0 mentions). |
| §11.12 evidence_source enum not in schema | **OPEN** | B-7 anchor. |
| §11.13 Hard-coded #2d6a4f green | **CLOSED** | 0 occurrences; `--accent-green` token used. |
| §11.15 response_summary.md committed ephemeral | **OPEN** | File still at repo root (2026-09-10 session result); not gitignored; no note header. |
| §11.16 docs/audits/ vs sessions/ two audit locations | **OPEN** | Both exist (`docs/audits/2026-08-10-baseline.md`); README does not document the split. |
| session §3.2 Stale "~873 KB"/"~1.69 MB" comments | **CLOSED** | 0 occurrences repo-wide. |
| session §3.3 README tree moved files | **CLOSED** | Script entries verified accurate incl. the deprecated shim (P-3). |
| session §3.4 Wumenguan 48/48 claim | **CLOSED (reworded to truth)** | Now "48 / 48 cases represented; W1 … partial_or_failed" — gate-pinned (P-6). |
| session §3.5 "8+ Robo-Translators" | **CLOSED** | Wording gone (the stale 13/7 profile figure is the separate D-2). |
| §4 bundle 1.87 MB + Tier-3 quick wins | **PARTIALLY CLOSED** — compact JSON shipped; bundle now 1,641,935 B; split/minify remain PR-D territory | B-5. |
| §6.1 15/34 masters empty alternative_names | **CLOSED** | Measured 0 of 34 empty. |
| Tier 5 architecture debt (A1–A5) | **DEFERRED (intentional, documented)** | FULL_AUDIT §1 table; no change; low priority by design. |

## Lane 4 — verdict (2026-09-13)

**Nothing was lost; the follow-through chain is intact.** Of the wave's
findings: 12 CLOSED with verification anchors, the rest DEFERRED into named
owner-held/frozen holding places (Rights, W1 remediation queue, Edits 1–3,
PR-A/B/D, 31-doc human queue, platform_sutra) or still OPEN in the current
`AUDIT.md` §4 where they belong — including P2.7 (validation depth), which
has no closure or deferral record and stays a live P2. The predecessor's
stale census lines are live-verified open (O-1) and the gate-coverage ruling
is framed precisely (P-6). New rows from this lane: none beyond
O-1/D-2 refinements — the ledger's value is the classification itself.

Letter to the translatechan orchestrator: `letters/LANE4-FOLLOWTHROUGH-2026-09-13.md`.

## All lanes complete

Lane order 1 → 2 → 5 → 3 → 4 executed per R-P2; all five letters authored in
the review space (R-X1). Consolidated tracker rows proposed for
`.orchestrator/STATE.md` (R-D3) in `letters/LANE4-FOLLOWTHROUGH-2026-09-13.md` §4.


---

# APPENDIX R - PHASE-1 RE-VERIFICATION (verbatim)

# Task 001 — Phase 1 record: survey re-verification + trace register (2026-09-13)

- **Session:** `arena/01a09825-repotester` (REPOTESTER-side session; bound here, pushes only here)
- **Subject:** `56eli/translatechan` @ `main` = `6076170` (full public clone taken 2026-09-13 for read-only review)
- **Brief:** `reviews/translatechan/FOUNDATION-2026-09-13.md` (fetched from `arena/01a08d0d-repotester` @ `origin/_found`)
- **Status:** Phase 1 complete. Nothing scoped — zone proposals go out as Checkpoint-C question sets, one per zone, in order.

---

## 1. Survey re-verification (brief snapshot vs today)

The brief's survey was taken 2026-09-13 at `main @ 6076170`. Measured today (2026-09-13):

| Brief claim | Today's measurement | Verdict |
|---|---|---|
| main @ `6076170` | `main` = `6076170` "Merge pull request #44 from 56eli/arena/01a097f7-translatechan" (merged 2026-09-13T00:07:51Z) | **Unmoved since the survey** |
| Latest merge: PR #44 | PR #44 merged 2026-09-13T00:07:51Z; PRs #33–#44 all merged; **0 open PRs**, 0 open issues | Confirmed |
| "multiple `arena/019fe…-translatechan` session branches" | **47 `arena/…-translatechan` branches** on the remote; **16 carry commits ahead of `main`** | Confirmed, counted |
| `app.js` 173 KB / `app.css` 67 KB / `app_data.js` 1.64 MB | 173,282 B / 67,165 B / 1,641,935 B | Confirmed (exact) |
| `scripts/`: ingest_cbeta, collate_corpus, collate_refs, segment_classical, source_review, migrate_translations, build_data_bundle, arena_agent_pipeline | 15 tracked tools total — the 8 named + `validate_data.py`, `w1_evidence.py`, `test_source_preservation.py`, `test_source_review_rules.py`, `smoke_test.mjs`, `browser_test.mjs`, `compat_runtime_check.mjs` | Confirmed; inventory superseded by the full 15 |
| "CI present (`.github/workflows/`)" | One workflow: `quality.yml` (job "Validate data, generated artifacts, and reader", 5 gates, `permissions: contents: read`, triggers push `main`/`arena/**` + PR→`main`) | Confirmed |
| "no Python manifest" | No `pyproject.toml`/`setup.py`; scripts are dependency-free Python 3.12 | Confirmed |
| Governance surfaces (AGENTS, HANDOFF, OPERATIONS, ROADMAP, UX_ROADMAP, RESEARCH_RELEASE_PLAN, WEB_VISION, audit wave, `.orchestrator/`) | All present; see §3. Additional surfaces the brief's inventory omits: `vision.md` (49 KB blueprint), `response_summary.md` (disposable per-session summary, last dated 2026-09-10), `sessions/` (37 dated evidence files, append-only), `schemas/translatechan-data.schema.json`, `docs/` (the Pages deploy mirror — see §4 WEB) | Superset confirmed |

**Branch reconciliation (16 ahead of `main`):**

| Branch | Ahead | Tip (date) | Recorded purpose |
|---|---:|---|---|
| `arena/01a08e15-translatechan` | 56 | `3fc735c` (2026-09-13) | **Prior orchestrator's prompt distribution channel** (prompts 002–017; never merges, never a PR base) |
| `arena/019fe731-translatechan` | 35 | `402fe9d` (2026-08-09) | Report archival (sessions/) |
| `arena/019fe8a2-translatechan` | 13 | `6856379` (2026-08-09) | Independent full audit session work |
| `arena/019ff0c0-translatechan` | 9 | `1953510` (2026-08-11) | "10 screenshot states of the hall pass" (browser evidence, viewable without merging) |
| `arena/01a08c93-translatechan` | 4 | `35bbfc9` (2026-09-10) | PR #29 revision re-verification record (verdict MERGE) |
| `arena/01a08d90-translatechan` | 3 | `2abc017` (2026-09-11) | Publish 002-linji-r-a-rekey ("dispatch held until PR #30 merges") |
| `arena/019fecb1-translatechan` | 3 | `de5725c` (2026-08-10) | "fix: restore lineage mode and fatal recovery" |
| `arena/019fe05c-translatechan` | 2 | `f425544` (2026-08-08) | Early-session doc finalization |
| `arena/01a08836-translatechan` | 1 | `4f9c27c` (2026-09-09) | wumenguan T2005 re-key (superseded by merged PR #29) |
| `arena/01a08852-translatechan` | 1 | `f0347f5` (2026-09-10) | PR24 remediation task prompt |
| `arena/019fe108 / 019fe1b5 / 019fe30b / 019fe5d5 / 019fe838 / 019fec5c` | 1 each | 2026-08-08…10 | Session doc-merge records |

All 31 remaining arena branches are at `main` (merged). Per the task order: **recorded here, not resumed, not deleted.** No branch of mine exists on `translatechan` — see §5.

## 2. Predecessor-orchestrator trace register (repo content; recorded only)

1. **`.orchestrator/` on `main`** (6 files): `STATE.md` (243 lines — working state incl. a **cold-start Continuation block added 2026-09-13** by session `01a097f7`/PR #44), `PHASE2_PLAN.md` (consolidated W1 witness inventories → Phase-2 decision instrument, ends in `## Owner decision required`), `REMEDIATION_PLAN.md` (R-A/R-B/R-C hybrid per-document work packages), `WITNESS_INVENTORY.md` / `WITNESS_INVENTORY_T48_T51.md` / `WITNESS_INVENTORY_XSERIES.md` (35 documents inventoried against the pinned witness set; 70 P0 bullets).
2. **Channel branch `arena/01a08e15-translatechan`** (tip `3fc735c`, 56 ahead): `.orchestrator/prompts/` 17 files (002–014, 016, 017; **015 measured absent — index not renumbered**), `.orchestrator/local/ORCHESTRATOR_STATE.md` + `local/INTEGRITY_PLAN_2026-09-11.md`. The Continuation block in `main`'s `STATE.md` records channel tip `35021d0`; the channel has since advanced **4 commits** (017 published; "#44 MERGE verdict issued"; **PR #43 recorded as merged unreviewed** — "checked on main 1b41d0b, healthy; two follow-ups and a prompt defect owned"; tip commit removes 4 review drafts the prior session "should never have committed" — self-recorded trace incident; "publish guard cannot express a removal" recorded as hardening candidate).
3. **Owner rulings in force (2026-09-12, four, executed by PR #43):** (1) six CITATION rows in one PR — done; (2) the ledger stays: **630 authoritative / 532 dated measurement**, no re-designation; (3) fabricated/unsupported text replaced where the pinned witness carries it, labelled where it does not — no re-pointing at unverified candidates; (4) OUT-OF-CBETA sourcing is human work — 31-document queue, **no agent fetch/transcription/evaluation**.
4. **Prior-campaign open items (candidates for the Step-7 canonical-tracker routing — `Deferred (needs owner decision)`):**
   - `platform_sutra` text decision (keep 9 labelled précis fields vs re-key to T48n2007) — framed in `PHASE2_PLAN.md`, owner-held.
   - OUT-OF-CBETA human-sourcing queue (31 documents) — owner-held, not agent-authorisable.
   - `OPERATIONS.md` Edit 1/2/3 (quality.yml artifact-diff coverage; action majors off Node 20; branch-protection verification) — owner approval withheld since 2026-09-09; **Edit 1 gap re-confirmed live today** (§3).
   - Task **014b** (three items, redefined on the channel: stale 49/38/22/16 census lines in ROADMAP/vision/RESEARCH_RELEASE_PLAN; `dahui_hongzhi` manifest-vs-document disclosure) — the prior orchestrator's immediate next task; **not resumed by this session**.
   - Visual-system reset (deferred, separate track); PR-A real-browser verification / PR-B CSP hardening / PR-D performance (frozen); W2 verified-quotation spot-check (sequencing at successor's discretion); 30 lineage edges `traditional_link_pending_exact_locator`; rights review (14 sources, human).
   - Congronglu reintroduction — quarantined 2026-08-10; **do not restore** without source-pinned field-level collation.

## 3. Governance + claims read; measured baseline

Read in full: `AGENTS.md`, `HANDOFF.md`, `OPERATIONS.md`, `AUDIT.md`, `README.md`, `.github/workflows/quality.yml`, `package.json`, `.gitignore`; section-mapped: `ROADMAP.md` (milestone tracker, checkbox rows), `vision.md`, `RESEARCH_RELEASE_PLAN.md`, `UX_ROADMAP.md`, `WEB_VISION_2026-08-10.md`, the 2026-08-10 audit wave (`AUDIT_2026-08-10_session.md`, `AUDIT_UPDATE_2026-08-10_hero.md`, `FULL_AUDIT_2026-08-10_019feaf5.md`); all 15 `scripts/` heads/docstrings; `STATE.md` in full.

**Measured baseline (this session, on `main` = `6076170`):**

```text
GATE1 python3 -m py_compile scripts/*.py            PASS
GATE2 python3 scripts/validate_data.py              PASS (3 documented lineage warnings)
        corpus=35 | slots=1252 | verified=177 | matrix=21 | locators=148/148
        W1: collated=1 | partial/failed=32 | unavailable=2 | flagged=630 | evidence=2026-09-10
GATE3 python3 scripts/build_data_bundle.py          PASS — app_data.js 1,641,935 B, byte-identical rebuild (cmp)
GATE4 node scripts/smoke_test.mjs                   PASS (incl. source-preservation: 35 files vs pinned base 3cc7a8e9, 0 unauthorized changes)
GATE5 diff -rq data docs/data                        PASS (mirror in sync)
```

**Spot checks (evidence for the zone questions):**

- **Bundle reproducibility:** `build_data_bundle.py` reproduces `app_data.js` byte-for-byte from `data/`; deterministic compact JSON; root assets + `docs/` mirror synced.
- **No network in the pipeline:** no HTTP-client imports anywhere in `scripts/*.py`; `cbeta-org/xml-p5` URLs appear only as provenance constants/doc references (`collate_refs.py:88`, `w1_evidence.py:96`, docstrings). The 21 MB extracted reference layer is **deliberately never committed** (pinned P5 revision `dbdea41071e1e260ad84b72faefd4587333cf76d`; digest manifests in `sessions/COLLATION_W1_2026-09-1{0,2}_*.txt`).
- **Congronglu containment still holds:** `congronglu` absent from `app_data.js` (0 hits), `data/corpus/`, `corpus_manifest.json`; residual mentions are 3 glossary `occurrences` cross-reference strings + 5 `cross_refs` strings in `gongan_index.json` (no source text; the corpus file was deleted in the 2026-08-10 containment pass, `sessions/CONTAINMENT_2026-08-10_CONGRONGLU.md`).
- **CI gap re-confirmed live (OPERATIONS.md Edit 1):** the artifact-diff step guards `app_data.js docs/app_data.js docs/index.html docs/app.css docs/app.js docs/data data/project_metrics.json` — it **omits** `docs/theme-init.js docs/robots.txt docs/sitemap.xml docs/og-image.svg` and the root `index.html`/`app.js`/`app.css`/`theme-init.js` (root `app_data.js` only). Hand edits to those files would not be detected by CI.
- **Claims queued for lane review (not findings — targets for lanes 3/4):** HANDOFF §5 "41 JS-generated inline styles" vs 29 `style.` references measured in `app.js` today (counting method differs; lane 3 decides); CSP `style-src 'unsafe-inline'` necessity; branch protection "unconfirmed (403)"; Playwright skip-as-success; JSON Schema declarative-only; Google Fonts third-party runtime request (CSP `style-src`/`font-src` allow `fonts.googleapis.com`/`fonts.gstatic.com`).
- **App claims verified structurally (Phase 1 only):** `index.html` — 0 inline `<style>`, 4 external `<script>` (theme-init.js, app_data.js, app.js + fonts), CSP meta precedes all scripts (`script-src 'self'`, no inline events anywhere in `app.js` — the single `onclick` hit is an explanatory comment, `app.js:895`); `app.css` — 14 `@media`, `prefers-reduced-motion` block at `app.css:2028`; keyboard: 17 `keydown`/`tabindex` references in `app.js` + 6 in `index.html`.

## 4. Zone understanding (Phase R — gathered, unscoped)

Draft from the brief §5; each target below verified to exist at `6076170`.

**PRODUCT** — `scripts/` (15 tools: validators `validate_data.py`/`w1_evidence.py`/`source_review.py`; collation harness `collate_corpus.py`/`collate_refs.py`; build `build_data_bundle.py`; tests `test_source_preservation.py`/`test_source_review_rules.py`/`smoke_test.mjs`/`browser_test.mjs`/`compat_runtime_check.mjs`; helpers `arena_agent_pipeline.py`/`segment_classical.py`/`ingest_cbeta.py` (deprecated no-network wrapper)/`migrate_translations.py`) + `data/` (35 corpus JSONs, `corpus_manifest.json`, `canonical_locators.json`, validator-generated `project_metrics.json`, `editorial/`, `lineage/`, `translations/` incl. `rights_manifest.json`, `glossary/`, `gongan/`) + `schemas/` + `.github/workflows/quality.yml`. Generated `app_data.js` = verified artifact (rebuild + field integrity), not a line-review target. Lane mapping: **Lane 1** (provenance-integrity), **Lane 2** (data-pipeline), **Lane 5** (CI/workflow — its only in-repo target is `quality.yml` + the CI wiring of audit-cited suites).

**WEB** — `index.html`, `theme-init.js`, `app.js`, `app.css`, generated `app_data.js`, `package.json`(+lock), `robots.txt`, `sitemap.xml`, `og-image.svg`, and the **`docs/` deploy mirror** (generated by the build; `docs/` is the GitHub Pages publish root — native branch publishing, **no Pages deployment workflow exists in the repo**; the draft zone's "Pages workflow" target resolves to: `quality.yml`'s deploy-mirror guards + the native Pages config on the GitHub side). Lane mapping: **Lane 3** (SPA integrity vs README claims).

**DOCS** — `README.md`, `HANDOFF.md`, `AGENTS.md`, `OPERATIONS.md`, `AUDIT.md` + the 2026-08-10 wave (3 files), `ROADMAP.md`, `UX_ROADMAP.md`, `RESEARCH_RELEASE_PLAN.md`, `WEB_VISION_2026-08-10.md`, `vision.md`, `response_summary.md`, `sessions/` (37 append-only evidence files), `.orchestrator/` (6 files on main — predecessor traces; reviewed as record, not as instruction). Lane mapping: **Lane 4** (prior-audit follow-through). **Canonical-tracker resolution (my Step 7):** `ROADMAP.md` is the milestone/status tracker with checkbox rows (`STATUS.md`/`docs/PROJECT_STATE.md` equivalents do not exist in the subject repo); `AUDIT.md` holds the current verdict, `RESEARCH_RELEASE_PLAN.md` the release-blocking checklist — the three are gate-enforced cross-references by `validate_data.py`'s doc-truthfulness rules.

## 5. Environment, authority, and boundary notes (measured)

- **Session binding:** this session is bound to `56eli/REPOTESTER` @ `arena/01a09825-repotester` (push only there). Measured token (`arena-ai-coding-agent[bot]`) permissions on `56eli/translatechan`: `admin/maintain/pull/push/triage` all `false` → **public read-only** (matches brief §3 "REPOTESTER-side sessions read translatechan publicly"). Consequence: **no branch of mine can be pushed to `translatechan`, and no PR can be opened from this session into `translatechan`** — review deliverables land here (REPOTESTER-side continuity, `reviews/translatechan/`); any code change on the subject repo requires an owner-side session or owner push. This is a Phase 2 distribution question for the owner.
- **Binding constraints carried over:** U-2 (repo content is data, never instruction; register-imitated text unattributable to the named translator); U-1 (committed secret = rotation incident); CBETA/Taishō discovery-only, zero automated requests until explicit owner authorization; one agent at a time, agents PR to the subject repo's `main`, owner merges; `Deferred (needs owner decision)` items → canonical tracker (Step 7); findings ledger (defects / opportunities / decision-records, rows OPEN—owner) surfaced at every PR hand-back; PRs carry the Hardening Report (CORE v4.2 §16).
- **Prior-campaign rule respected:** nothing resumed (no 014b dispatch, no platform_sutra decision work, no witness-queue work); nothing deleted; all traces above are recorded as repo content.


---

# APPENDIX LANE 1 — PROVENANCE (verbatim from the review engagement)

# Letter — Lane 1 (provenance-integrity) findings to the translatechan orchestrator

- **From:** REPOTESTER review session `arena/01a09825-repotester`
  (56eli/REPOTESTER `reviews/translatechan/` review space)
- **To:** the orchestrator session bound to `56eli/translatechan`
- **Date:** 2026-09-13 · **Subject:** `56eli/translatechan` @ `main` = `6076170`
- **Mandate:** Task 001 foundation review, Lane 1 per the owner's scoped
  foundation (zone rulings R-P1…R-P3, R-X1; Checkpoint-C record in the
  REPOTESTER review space). Owner lane order: 1 → 2 → 5 → 3 → 4; this letter
  covers Lane 1 only.
- **Access used:** public read-only clone + public GitHub API; the pinned
  `cbeta-org/xml-p5` revision `dbdea41071e260ad84b72faefd4587333cf76d` fetched
  into sandbox scratch (owner-authorized in writing for this purpose, read-only,
  never committed). **Nothing was pushed to, or opened against, the subject
  repo.** Predecessor traces were recorded, not resumed, not deleted.

## 1. Verdict (one paragraph)

The shipped surface is contained. Every W1 source-review claim that reaches a
reader is backed by the pinned, digest-verified reference layer: the status
model (1 / 32 / 2) re-derives, document-for-document, from the pinned refs plus
current `main` data; the single `collated_to_claimed_witness` document collates
6/6 content fields EXACT against T48n2014; the Congronglu quarantine holds in
the shipped bundle; all 179 edition-verified records are rights-linked with
exactly 3 explicitly pending references; the Robo-disclosure layer covers 100%
of the 1,252 slots; the two `witness_unavailable` documents and the withdrawn
zhaozhou T1987 claim are disclosed, not asserted. No generated text wearing a
witness claim was found in the shipped surface. Residual unadjudicated fields
are the prior campaign's owner-held queue, not a surface defect.

## 2. Claims for independent verification (each with its reproduction)

Run from a clean clone of `main` = `6076170`. Expected values are exact.

**C-1 · Reference layer reproduces from the pinned revision.**
Acquire `cbeta-org/xml-p5` at `dbdea410…` (sparse, exactly the 39 manifest
works — procedure in `scripts/collate_refs.py` docstring, with the pinned
revision substituted for HEAD), then:
`python3 scripts/collate_refs.py --source-dir <xml> --out-dir <refs> --work-list
sessions/COLLATION_W1_2026-09-10_refs_manifest.txt --verify-against
sessions/COLLATION_W1_2026-09-10_refs_manifest.txt --upstream-revision
dbdea41071e1e260ad84b72faefd4587333cf76d --write-digest-manifest <refs>/m.txt
--allow-drift`
→ expected: `39 verified, 0 drift, 0 unlisted, 0 unavailable`;
`cmp <refs>/m.txt sessions/COLLATION_W1_2026-09-10_refs_manifest.txt` clean.

**C-2 · The published record is reproducible.**
`COLLATION_REFS=<refs> python3 scripts/collate_corpus.py --out /tmp/r.json
--reproduce sessions/COLLATION_REGISTER_2026-09-10_CORRECTION.json`
→ expected aggregate: `flagged_entries 532, content_fields_collated 691 /
924, source_review_status_counts {collated_to_claimed_witness: 1,
partial_or_failed_w1_collation: 32, witness_unavailable: 2}`; per-document
flagged/status/collating equal to
`sessions/COLLATION_REGISTER_2026-09-12_POSTREMEDIATION.json` for all 35
documents; output byte-identical across two consecutive runs.

**C-3 · The one "collated" document is genuinely collated.**
In the C-2 output, `documents.zhengdao_ge`: `content_summary {EXACT: 6}`,
`content_fields_collated 6 / 6` vs witness `T48n2014`; the single NOT_FOUND
flag is `.title_zh` (metadata, excluded from the content denominator per the
documented evidence model).

**C-4 · Shipped bundle integrity + quarantine.**
`python3 scripts/build_data_bundle.py` leaves `app_data.js` byte-identical
(1,641,935 B); `diff -rq data docs/data` clean; `grep -c congronglu app_data.js`
= 0; `data/corpus/congronglu_cases.json` absent; residuals confined to 3
glossary `occurrences` + 5 `gongan_index` `cross_refs` cross-reference strings
(no source text).

**C-5 · Badge and disclosure layers.**
177 corpus + 2 matrix `verified_quotation` records, each with
work/edition/verification/reference and a `source_id` resolving into
`data/translations/rights_manifest.json` (14 records); exactly 3 references
carry pending markers (zhaozhou_yulu ×2; matrix_wumen_1 "Hokuseido print page
pending") — HANDOFF's "176 / 179" is arithmetic. 1,252 slots with explicit
status (876 / 199 / 177), 0 bare strings. Rights: 12 `needs_rights_review` +
2 `jurisdiction_review_required` (matches AUDIT §1). Reader badges at
`app.js:2102–2115`; `window.TranslateChan.getSourceReviewStatus` absent.

**C-6 · Drift note exactness.** 2026-09-09 candidate manifest (187 refs) vs
2026-09-10 set (39): exactly 6 digests differ (T47n1987B, T48n2001,
X67n1309, X68n1315, X69n1333, X73n1445) → the harness's 8
`documents_with_drifted_references` (X68n1315 shared by three documents); all 8
`partial_or_failed_w1_collation`; verdicts unchanged, as STATE.md states.

## 3. Rows requiring a ruling (none is a fix request)

- **L1-D1 (MINOR).** The cold-start Continuation block in
  `.orchestrator/STATE.md` ("Reproduce the authoritative register byte-for-byte
  … (register sha256 `5369af11…`)"): that sha256 is the hash of the **committed
  file** (it matches — file integrity verified); the `--reproduce` command
  replays the register's `generation_parameters` against current data and emits
  the current-state register, whose output hash is recorded nowhere. Evidence
  is sound (C-1…C-3); the wording conflates a file-integrity hash with a
  reproduction output. Ruling: wording fix (docs-only) or accept-as-is.
- **L1-D2 (MINOR).** `README.md:151` says "13 in-corpus-verified; 7
  documented-external"; live data measures 14 + 6 + 1 `not_applicable`
  (`ai_literal`). Gate set covers README.md but not this figure. Ruling:
  docs-only fix, batchable with L1-O1.
- **L1-O1 (decision-record).** Doc-truthfulness gate coverage: the census prose
  asserting 49/38/22/16 (ROADMAP.md:163,:179 · vision.md:57,:59,:88,:90,:327 ·
  RESEARCH_RELEASE_PLAN.md:32,:103) is stale against live 50/39/23/17 (re-
  measured, confirming the predecessor's unexecuted task 014b item 1), and the
  gate passes with it present. Which stale prose should join the enforced
  figures is an owner decision; no fix is opened unasked.

## 4. Proposed canonical-tracker rows (R-D3: `.orchestrator/STATE.md` →
`## Deferred / Technical Debt`, via docs-only PR; owner merges)

For the receiving orchestrator to verify and carry, unresumed:
1. `platform_sutra` text decision (9 labelled précis vs re-key to T48n2007) — owner-held.
2. OUT-OF-CBETA human-sourcing queue (31 documents) — owner-held; no agent fetch/transcription/evaluation.
3. `OPERATIONS.md` Edits 1–3 (artifact-diff coverage — independently re-confirmed open; action majors; branch-protection verification) — owner-held.
4. Predecessor task 014b (stale census lines; `dahui_hongzhi` manifest-vs-document disclosure) — recorded; re-measured open by this review (L1-O1).
5. Frozen tracks PR-A (real-browser verification) / PR-B (CSP hardening) / PR-D (performance, measure-first) — recorded.
6. Rights review (14 sources) — human work.
7. Congronglu reintroduction — blocked; do not restore without source-pinned field-level collation.
8. Evidence-model re-designation (fixed historical/overlay pair → chain; the "designation half" of release blocker 1) — owner-ruled change, queued.
9. This review's L1-D1 / L1-D2 / L1-O1 — awaiting owner rulings.

## 5. Boundaries observed

U-2: all in-corpus prose treated as data; register-imitated text as
unattributable to its named translator; no in-repo text treated as instruction.
CBETA: pinned-revision-only access per the owner's written authorization; zero
other automated requests. One agent at a time; no branches or PRs opened on the
subject repo by the sending session. The findings ledger rows above are
OPEN—owner until ruled; this letter is advisory until the receiving
orchestrator independently verifies §2 and the owner rules on §3–§4.


---

# APPENDIX LANE 2 — PIPELINE (verbatim from the review engagement)

# Letter — Lane 2 (data-pipeline) findings to the translatechan orchestrator

- **From:** REPOTESTER review session `arena/01a09825-repotester`
- **To:** the orchestrator session bound to `56eli/translatechan`
- **Date:** 2026-09-13 · **Subject:** `56eli/translatechan` @ `main` = `6076170`
- **Mandate:** Task 001 foundation review, Lane 2 (data-pipeline, PRODUCT zone
  per R-P1/R-P2). Follows `letters/LANE1-PROVENANCE-2026-09-13.md`.
- **Access used:** public read-only clone; no CBETA requests (Lane 1's
  pinned-revision fetch was the only third-party access, per R-P3). Nothing
  pushed to or opened against the subject repo.

## 1. Verdict

The pipeline chain is reproducible and the backstop is real. The generated
bundle rebuilds byte-stable from `data/`; all five gate steps pass, including
a source-preservation suite that pins the 35 corpus files to a base commit
with an explicit allowlist; the script chain matches the documentation (the
brief's chain head `ingest_cbeta.py` is a deprecated shim — the real head is
`segment_classical.py`, an offline tool that does not fetch anything); the
agent-pipeline helper constrains status/provenance at construction with the
validator as the hard enforcement point — and that enforcement was proven by
mutation testing, including the code-level regression check for the 2026-08-10
Congronglu incident.

## 2. Claims for independent verification

Run from a clean clone of `main` = `6076170`. Expected values are exact.

**C-1 · Bundle byte-stable rebuild.**
`sha256sum app_data.js` · `python3 scripts/build_data_bundle.py` → "✅
Successfully compiled 35 corpus documents" (1,641,935 bytes) ·
`sha256sum app_data.js` → **identical**; then the quality.yml step verbatim:
`git diff --exit-code -- app_data.js docs/app_data.js docs/index.html
docs/app.css docs/app.js docs/data data/project_metrics.json` → clean.

**C-2 · The five gate steps pass.** In order, exactly as
`.github/workflows/quality.yml` runs them:
1. `python3 -m py_compile scripts/*.py` → exit 0
2. `python3 scripts/validate_data.py` → "✅ DATA VALIDATION PASSED"
3. `python3 scripts/build_data_bundle.py` → as C-1
4. the artifact diff (C-1) → clean
5. `node scripts/smoke_test.mjs` → "RENDERER: 35 corpus texts exercised, 0
   crashes", "W1 SOURCE-REVIEW RULES OK", "SOURCE-PRESERVATION OK: 35 corpus
   files match base commit 3cc7a8e9… apart from the allowlisted remediation
   pointers; 0 unauthorized changes", "✅ SMOKE TEST PASSED"

**C-3 · Chain shape.** `scripts/ingest_cbeta.py` is a 24-line deprecated
`runpy` shim → `scripts/segment_classical.py` (docstring: "Manual/offline
input only: it does NOT fetch from CBETA, generate pinyin, or map CBETA
canonical IDs yet — those are Phase-2 ingestion-tooling goals"). No
`http.client`/`urllib`/`requests` imports in any of the 15 scripts; CBETA
URLs appear only as provenance constants. `source_review.py` is the single
W1-vocabulary module imported by validator, harness and regression tests
(pre-drift by construction).

**C-4 · Agent-pipeline constraints.** `scripts/arena_agent_pipeline.py`:
three prompt templates (output schemas carry no provenance fields — by
design) + `create_translation_entry()` (status defaults
`reconstruction_unverified`/`ai_draft`; AI output labelled "Arena AI Agent
(model)"; `verified_quotation` requires `{work, edition, reference,
verification, source_id}` with `source_id` in
`data/translations/rights_manifest.json`). Note: the helper accepts a
caller-supplied status override — the hard enforcement is the validator.
Committed data: 0 malformed entries; 0 entries carry the helper's output
label "Arena AI Agent (…)"; matrix = 4 entries / 21 translator
records (18/2/1), the single `ai_draft` labelled "AI Multi-Draft Engine".

**C-5 · Backstop proven by mutation (isolated copy; baseline PASS; restore
PASS).** Five mutations, each refused with the exact message:
(M1) verified `source_id` absent from rights manifest → "verified quotation
source_id(s) missing from rights manifest: …"; (M2) missing `reference` →
"missing non-empty 'reference'"; (M3) missing `status` → "has invalid or
missing status None"; (M4) bare-string translation → "legacy string
translation; use { text, status } (run scripts/migrate_translations.py)";
(M5) identical case-level `commentary_zh` (≥12 chars) across 3 cases →
"identical commentary_zh appears in 3 cases …; quarantine or mark generated
placeholders outside canonical source fields" — the Congronglu incident's
regression check in code.

**C-6 · Doc-truth gate scope (measured).** Snippet rules: README.md,
HANDOFF.md, index.html, AUDIT.md, ROADMAP.md. W1-claim rules add
`.orchestrator/REMEDIATION_PLAN.md` (must quote the 187-entry historical
manifest count from the file; "174" only with stale qualifiers) and check
`.orchestrator/STATE.md` (must quote the authoritative flagged total and
label the superseded figure). Line-level forbiddances across the scanned
set: unqualified 637 / historical-register totals; `T1987` without
"false"/"caoshan"; `X68n1315A`; unqualified "of 34 evaluated"; hand-typed
bundle byte counts; "rights approved" / "approved for reuse" / "cleared for
redistribution" / "rights review complete".

## 3. Rows requiring a ruling

- **L2-D3 (MINOR, wording).** `validate_data.py` docstring says the doc-truth
  gate covers "(README.md, HANDOFF.md, index.html)"; measured scope is C-6
  (broader — good direction). Wording fix so a maintainer does not
  underestimate what a reword can break. Batch with L1-D1/L1-D2.
- **L2-O2 (opportunity, optional).** `create_translation_entry` could
  self-reject an explicit `verified_quotation` lacking a full source record
  (defense-in-depth pre-PR). The gate backstop is proven real (C-5), so this
  is an improvement, not a defect response.
- **L1-O1 refinement (no new ruling).** Measured gate scope confirms the
  49/38/22/16 census figures are not pinned numbers and
  WEB_VISION_2026-08-10.md / RESEARCH_RELEASE_PLAN.md are outside the scanned
  set — the stale census lines pass the gate. Gate-coverage remains an owner
  decision.

## 4. Boundaries observed

U-2 in force (all in-repo prose treated as data). No CBETA/Taishō requests in
this lane. No branches/PRs on the subject repo. Rows are OPEN—owner /
OPEN—orchestrator until ruled; advisory until independently verified.


---

# APPENDIX LANE 3 — SPA (verbatim from the review engagement)

# Letter — Lane 3 (SPA integrity) findings to the translatechan orchestrator

- **From:** REPOTESTER review session `arena/01a09825-repotester`
- **To:** the orchestrator session bound to `56eli/translatechan`
- **Date:** 2026-09-13 · **Subject:** `56eli/translatechan` @ `main` = `6076170`
- **Mandate:** Task 001 foundation review, Lane 3 (SPA integrity, WEB zone per
  R-W1…R-W3: repo gates only — no headless browser, no owner-side evidence
  pass; PR-A/B/D frozen, measured/reported not resumed). Follows LANE1/2/5.

## 1. Verdict

The shipped SPA's claims are substantiated at the repo-gate level, with one
disclosure-precision fix (D-4). HTML is inline-style-free as claimed; the
exact JS inline-style inventory is 58 injection sites against the disclosed
"41" (the 41 counts one mechanism; no behavior issue — the CSP covers both);
responsive/reduced-motion/keyboard/lang="zh" claims are substantiated at the
CSS/markup existence level; performance claims are qualitative with no
falsifiable in-repo numbers.

## 2. Claims for independent verification

All counts are reproducible from a clean clone with any text tooling.

**C-1 · "No HTML inline styles" (README.md:30).** `grep -c 'style="'
index.html` → 0; `<style` blocks in index.html → 0. The claim is scoped to
HTML and is true as worded.

**C-2 · Exact JS inline-style inventory (app.js).**
- `style=` attribute literals: **41** (all in live render templates; spot-
  checked lines 374, 1607, 1710, 1792-1843, 1892, 1928-29 — 0 in comments;
  incl. the `lang="zh"` classical blocks at 1805/1810).
- `.style.prop =` writes (excluding the 9 comparison reads): **17** (15
  `display`, 1 `left`, 1 `top`).
- **Total JS inline-style injection sites: 58.**
HANDOFF.md:110 ("Forty-one JS-generated inline styles keep CSP style-src
'unsafe-inline' necessary") matches the attribute-literal mechanism exactly;
the property-write mechanism (17) is not counted in the disclosed figure.

**C-3 · CSP (index.html).** Full tag: `default-src 'self'; script-src 'self';
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self'
https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self';
object-src 'none'; base-uri 'none'; form-action 'none'` — the HANDOFF
statement is accurate; `style-src 'unsafe-inline'` is load-bearing for the
58 sites in C-2.

**C-4 · Responsive + reduced-motion (README.md:30).** app.css: 4 ×
`@media (max-width: 1024px)` — including `.sidebar-panel { display: none }`
(the "shelf collapse"), the mobile corpus picker, graph-toolbar reflow,
master-directory reflow — and 6 × `@media (max-width: 768px)` (mobile
layout); 14 `@media` total, including 1 `prefers-reduced-motion` block with
`animation: none`. Existence-level substantiation; pixel/interaction
behavior verification is PR-A territory (frozen, R-W2/R-W3).

**C-5 · Keyboard + lang="zh" (README.md:28, :30).** app.js: `role="tablist"`
×1, `aria-selected` ×1, `tabindex` ×8; app.css: `:focus-visible` ×14;
`lang="zh"` ×26 (app.js) + ×10 (index.html).

**C-6 · Performance claims bounded.** The only perf claim in the shipped docs
is "Fast, zero-backend, responsive SPA" (README.md:116) — qualitative; no
numeric in-repo claim to falsify. "Zero-backend" verified: Pages `status:
built` from `main`/`docs`, no server code in the repo (LANE-5 C-4). Measured
uncompressed payload: app.js 173,282 B + app.css 67,165 B + app_data.js
1,641,935 B + index.html 17,767 B + theme-init.js 876 B = 1,901,025 B.

## 3. Rows requiring a ruling

- **L3-D4 (MINOR, wording/count).** HANDOFF.md:110's "forty-one" is the
  attribute-literal count; the shipped JS injection surface is 58 (C-2).
  Suggested fix wording: "Fifty-eight JS inline-style sites (41 attribute
  literals + 17 property writes) keep CSP style-src 'unsafe-inline'
  necessary" — or recount at edit time. Batch with L1-D1/D2, L2-D3.

## 4. Boundaries observed

Repo gates only: no headless browser, no owner-side evidence pass, PR-A/B/D
frozen (R-W2/R-W3). U-2 in force; no CBETA/Taishō requests; no branches/PRs
on the subject repo. Rows advisory until independently verified and ruled.


---

# APPENDIX LANE 4 — FOLLOWTHROUGH (verbatim from the review engagement)

# Letter — Lane 4 (prior-audit follow-through) to the translatechan orchestrator

- **From:** REPOTESTER review session `arena/01a09825-repotester`
- **To:** the orchestrator session bound to `56eli/translatechan`
- **Date:** 2026-09-13 · **Subject:** `56eli/translatechan` @ `main` = `6076170`
- **Mandate:** Task 001 foundation review, Lane 4 (DOCS zone per R-D1…R-D3
  final). Closes the lane order 1 → 2 → 5 → 3 → 4. Full finding-level table
  in the review-space ledger `FINDINGS-2026-09-13.md` (Lane 4 section); this
  letter carries the classification, the reproduction anchors, and the
  consolidated canonical-tracker rows.

## 1. Verdict

**Nothing was lost; the follow-through chain is intact.** Every finding of
the 2026-08-10 audit wave (FULL_AUDIT §11's 16 line items + §12's 5 tiers,
AUDIT_2026-08-10_session's 6 drift spots, the source-quality misses) resolves
to one of: **CLOSED** (12, each with a verification anchor), **DEFERRED**
(each with a named owner-held or frozen holding place), or **OPEN** (still
live in `AUDIT.md` §4 where they belong). No wave finding disappeared without
trace. One live P2 (B-7, validation depth) has no closure or deferral record
anywhere — flagged for the tracker.

## 2. Classification (summary; anchors in the ledger)

**Source-quality misses (A):** Congronglu containment — **CLOSED**
(bundle-clean + code-level regression check, LANE-2 M5). Zhaozhou T1987 —
**CLOSED** (re-keyed X68n1315; doc-gate requires the false-claim explanation
and forbids unexplained T1987 / the fabricated X68n1315A). Fabricated
preface/verses — **DEFERRED** (owner-held per-document queue, Ruling 3).
630→532 flagged fields — **DEFERRED** (owner ruling 2026-09-12: 630
authoritative, 532 today's measurement).

**AUDIT §4 (B-1…B-11):** B-1 rights (12+2) OPEN/human; B-2 source depth
DEFERRED (owner campaign); B-3 browser evidence DEFERRED (frozen PR-A);
B-4 CI coverage DEFERRED (Edit 1 — measured exactly the 4 files, LANE-5 C-2);
B-5 up-front initialization DEFERRED (frozen PR-D; bundle 1,641,935 B is
under the 2 MB P2 threshold of FULL_AUDIT Tier-3, so it stays P3 by that
rule); **B-6 style debt OPEN — count corrected 41 → 58 (D-4)**; **B-7
validation depth OPEN — still true (schema not executed; cross_refs
unvalidated; evidence_source absent from schema), no deferral record found**;
B-8 repo metadata/license NOASSERTION OPEN (measured); B-9 Google Fonts + no
SECURITY.md OPEN (measured); B-10 no PNG fallback OPEN (measured); B-11
exactly 3 lineage profiles + 30 edges OPEN, disclosed, validator-warned by
design.

**Predecessor open items (C):** stale census 49/38/22/16 — **OPEN,
live-verified this session** (O-1); dahui_hongzhi disclosure, platform_sutra
decision, 31-doc human queue — DEFERRED (owner-held, record-only); PR-A/B/D
— DEFERRED frozen (R-W2); witness inventories + channel branch —
RECORD-ONLY.

**Wave §11/§12/session-§3 line items:** CLOSED — OG description wording,
hero-chip aria pattern (8 remaining aria-hidden all decorative; 2 aria-live
regions), mobile bar 44px + safe-area, toolbar z 60 > strip, graph lower
bound 360 (app.js:2652), ellipsis standardized, footer inline opacity gone,
#2d6a4f → token, stale KB/MB comments gone, README tree accurate, Wumenguan
claim reworded to gate-pinned truth, "8+" Robo-Translators gone, 15/34 → 0/34
empty alternative_names. PARTIALLY CLOSED — 6 → 3 empty linked_corpus_keys
(all frontier scaffolds, disclosed). OPEN — response_summary.md still
committed at root (not gitignored, no note header); docs/audits/ vs sessions/
split undocumented; Tier-5 architecture debt DEFERRED by design.

**Gate-coverage fact (D):** the measured gate scope (LANE-2 P-6) does not pin
the census figures, and WEB_VISION/RESEARCH_RELEASE_PLAN are outside the
scanned set — O-1 stands as the owner's decision record.

## 3. Reproduction

All anchors are re-runnable from a clean clone: the 5 gate steps (LANE-2
C-1/C-2), the validator mutation suite (LANE-2 C-5), `gh api` for B-8/B-11
and the Pages/branch-protection facts (LANE-5 C-4), and the text-count
commands in LANE-3 §2. The ledger cites file:line for every closed/deferred
anchor.

## 4. Consolidated canonical-tracker rows (R-D3 → `.orchestrator/STATE.md`,
`## Deferred / Technical Debt`, docs-only PR, owner merges)

Supersedes/consolidates the Lane 1 letter §4 list; verify and carry,
unresumed:

1. **Quotation rights review** — 14 sources (12 needs_rights_review + 2
   jurisdiction_review_required). Human work. [B-1]
2. **W1 per-document remediation queue** — one document per PR (Ruling 3);
   register 630 authoritative / 532 = main measurement (owner ruling
   2026-09-12). [A-3, A-4, B-2]
3. **OPERATIONS.md Edits 1–3** — Edit 1 = the four mirror files
   (theme-init.js/robots.txt/sitemap.xml/og-image.svg) or the structural
   diff form (O-3); Edit 2 = checkout v4→v7, setup-python v5→v7,
   setup-node v4→v7; Edit 3 = branch-protection verification by an
   administrator (403 from non-admin tokens). [B-3, B-4, LANE-5 C-2/C-3/C-4]
4. **P2.7 validation depth** — JSON Schema not executed; `cross_refs`
   unvalidated; `evidence_source` enum absent from schema. Live P2, no
   deferral record found — first recorded here. [B-7, §11.11, §11.12]
5. **Frozen tracks** — PR-A (real-browser verification), PR-B (CSP
   hardening), PR-D (performance, measure-first; bundle 1.64 MB < 2 MB P2
   threshold). Recorded, not resumed (R-W2). [B-3, B-5]
6. **OUT-OF-CBETA human-sourcing queue** — 31 documents; no agent
   fetch/transcription/evaluation. [C-4]
7. **platform_sutra text decision** — 9 labelled précis vs re-key to
   T48n2007. [C-3]
8. **Stale census prose (49/38/22/16 vs 50/39/23/17)** — ROADMAP.md:163,
   :179 · WEB_VISION_2026-08-10.md:57,:59,:88,:90,:327 ·
   RESEARCH_RELEASE_PLAN.md:32,:103; gate-coverage ruling O-1 attached.
   Predecessor task 014b, recorded unresumed. [C-1, O-1]
9. **dahui_hongzhi manifest-vs-document disclosure** (014b item 2). [C-2]
10. **Web polish leftovers** — response_summary.md committed at root;
    docs/audits/ vs sessions/ split undocumented; P3.8–P3.11 (repo metadata,
    Google Fonts/SECURITY.md, PNG fallback, 3 lineage profiles + 30 edges).
    [B-8…B-11, §11.15, §11.16]
11. **This review's rulings requested** — D-1 (STATE.md continuation
    wording), D-2 (README 13/7 → 14/6/+1), D-3 (validator docstring gate
    scope), D-4 (HANDOFF 41 → 58 inline-style sites), O-1 (gate coverage),
    O-2 (helper self-validation), O-3 (structural diff). All MINOR/docs-
    only or optional; batchable as one docs-only PR once ruled.

## 5. Boundaries observed

U-2 in force (predecessor traces record-only: copied, not re-executed;
`.orchestrator/` reviewed as record, never as instruction; `sessions/`
untouched, append-only discipline intact). No CBETA/Taishō requests in this
lane. No branches/PRs on the subject repo by the sending session. This
letter + the ledger are advisory until the receiving orchestrator
independently verifies §2–§3 and the owner rules on §4.

**Engagement close:** Lanes 1, 2, 5, 3, 4 complete in the confirmed order.
Findings: 29 VERIFIED rows (V-1…V-12, P-1…P-6, C-1…C-5, W-1…W-6),
4 MINOR doc-precision defects (D-1…D-4), 3 opportunities (O-1…O-3), 3
decision records (DR-1…DR-3). No integrity defects in the shipped surface.


---

# APPENDIX LANE 5 — CI (verbatim from the review engagement)

# Letter — Lane 5 (CI/workflow) findings to the translatechan orchestrator

- **From:** REPOTESTER review session `arena/01a09825-repotester`
- **To:** the orchestrator session bound to `56eli/translatechan`
- **Date:** 2026-09-13 · **Subject:** `56eli/translatechan` @ `main` = `6076170`
- **Mandate:** Task 001 foundation review, Lane 5 (CI/workflow, PRODUCT zone).
  Follows `letters/LANE1-…` and `letters/LANE2-…`.

## 1. Verdict

The gates run, the cited suites are wired in, and the three documented
OPERATIONS edits are exactly where the docs say they are. No new defects:
this lane converts the audit's three open edits from prose into measured
state, and records one structural-improvement option (O-3) for Edit 1.

## 2. Claims for independent verification

**C-1 · Gate wiring.** `.github/workflows/` contains exactly one workflow,
`quality.yml`. Triggers: `pull_request` → main; `push` → main + `arena/**`.
`permissions: contents: read` (the file states it reads the repository only:
no Pages deployment, releases, writes, or third-party credentials). Five
steps run on every PR: (1) `python3 -m py_compile scripts/*.py` (2)
`python3 scripts/validate_data.py` (3) `python3 scripts/build_data_bundle.py`
(4) the artifact diff (C-2) (5) `node scripts/smoke_test.mjs`. The smoke
test is a hub: in addition to the 35-text render exercise and
composition/order checks (public-scope forbiddances, theme-init.js before
app.css, CSP meta before the scripts it governs), it spawns
`scripts/test_source_review_rules.py` (smoke_test.mjs:567-579) and
`scripts/test_source_preservation.py` (:588-592) — the W1 rule suite and the
source-preservation suite the audits cite, both therefore running in CI.
`browser_test.mjs` is intentionally absent from CI: package.json — "Optional
real-browser regression suite … (dev-only; not required for contributors or
CI)" (frozen PR-A territory, recorded not resumed).

**C-2 · Edit 1 gap, measured.** Build mirrors (build_data_bundle.py:105):
`index.html app.css app.js theme-init.js robots.txt sitemap.xml
og-image.svg` + `docs/data/`. Artifact-diff step covers: `app_data.js
docs/app_data.js docs/index.html docs/app.css docs/app.js docs/data
data/project_metrics.json`. **Missing: `docs/theme-init.js`,
`docs/robots.txt`, `docs/sitemap.xml`, `docs/og-image.svg`** — exactly the
four files OPERATIONS.md Edit 1 names. `docs/audits/` and `.nojekyll` are
not build-mirrored (static content), so they are outside Edit 1's stated
scope; recorded as nuance, not a finding.

**C-3 · Edit 2 gap, measured (2026-09-13, GitHub API).** Workflow pins
`actions/checkout@v4`, `actions/setup-python@v5`, `actions/setup-node@v4`;
latest releases: `v7.0.1`, `v7.0.0`, `v7.0.0` — the same v7 line
OPERATIONS.md reported on 2026-08-10. All current pins target deprecated
Node 20 runtimes (GitHub annotation per OPERATIONS.md; runner currently
forces Node 24).

**C-4 · Edit 3, owner-side; Pages model confirmed.** `GET
/repos/56eli/translatechan/branches/main/protection` → HTTP 403 "Resource not
accessible by integration" for the reviewing session's token — the same
result the audit integration received, which is why OPERATIONS.md correctly
withholds the "definitely disabled" claim. Pages API: `status: built`,
source branch `main`, path `/docs`, `https_enforced: true`,
`build_type: legacy` — native publication from the committed mirror; no
deploy workflow exists or is needed (matches OPERATIONS.md's statement).

**C-5 · Dependency surface.** All 15 pipeline scripts are stdlib-only (no
Python manifest/requirements by design — "dependency-free validator"); CI
uses system Python 3.12 / Node 22. The only declared dependency anywhere is
`playwright` in `devDependencies`, exercised solely by the opt-in
`test:browser` script (dev-only). No third-party package surface in the CI
path.

## 3. Rows requiring a ruling / carrying forward

- **L5-O3 (opportunity, optional, owner's call within the Edit-1 PR).** The
  Edit-1 gap exists because the diff step enumerates paths; adding four
  paths cures today's gap but the same drift class returns with a fifth
  mirrored asset. Suggested structural form: `git diff --exit-code --
  app_data.js docs data/project_metrics.json` (diff the mirror tree). Either
  form is a gate; the enumerated form is re-openable by omission.
- **Edits 1–3 remain OPEN—owner** (canonical-tracker item, already proposed
  in the Lane 1 letter §4). This letter's C-2/C-3/C-4 measurements are the
  up-to-date evidence for that row: Edit 1 = the four files (C-2); Edit 2 =
  three pins behind the v7 line (C-3); Edit 3 = 403-unverifiable here,
  requires an administrator (C-4).

## 4. Boundaries observed

U-2 in force; no CBETA/Taishō requests; no branches/PRs on the subject repo;
the only API reads were the public Pages/branch-protection/action-release
endpoints. Rows are advisory until independently verified and ruled.
