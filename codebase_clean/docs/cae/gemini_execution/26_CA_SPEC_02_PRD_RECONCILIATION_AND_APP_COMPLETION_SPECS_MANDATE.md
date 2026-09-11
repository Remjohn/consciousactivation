# Gemini Execution Mandate — Phase 26 / CA-SPEC-02

**Status:** `DRAFT — BLOCKED UNTIL OPERATOR AUTHORIZES THIS MANDATE`  
**Phase ID:** `CA-SPEC-02`  
**Title:** PRD Reconciliation & App-Completion Specification Package (Track A)  
**Execution classification:** Documentation and specification-authoring phase: reconcile `docs/PRD/CURRENT.md` to phase-25 truth, author missing implementation specs for the app-completion backlog, and subject every spec to an enforceable quality gate; no runtime code changes, no schema/staging changes, no implementation of anything specified  
**Required prior decision:** “Accept CA-TWC-01 as completed and authorize CA-SPEC-02 for PRD/spec reconciliation and app-completion spec authoring with quality-gate enforcement only.”  
**Required completion gate:** `AUTHOR -> VERIFY -> OPERATOR_REVIEW`; Track B implementation mandates are written only after the operator accepts individual specs.

## 1. Authority, purpose, and boundary

CA-SPEC-02 is governed by the CAE Governance & Specification Bridge Bundle v3 and inherits: accepted WP-00 through CA-TWC-01 records; ratified constitutions `CA-CAN-01A/B/C` and `CA-CAN-02_*`; `PRD-CAE-TEN-001`, its 15 FRs, and `TS-CAE-TEN-001`; the legacy `TS-APP-*` spec set (`docs/tech-specs/`, superseded-for-status, authoritative-for-detail); `docs/MASTER_SEQUENCING_PLAN.md`; and `docs/cae/gemini_execution/00_GEMINI_12_PHASE_EXECUTION_PROGRAM.md`.

**Purpose:** the operator’s goal is an app that is fully ready — workspace, guest, and guest context addable from the UI, flowing into real intelligence outputs. Two obstacles stand between here and there, both documentation-shaped:

1. `docs/PRD/CURRENT.md` (v0.2.8-draft, last verified against code **2026-08-14**) predates all 25 CAE phases and is now materially false about system state — violating its own §1.12 rule (“updates… in the same session… or the work is not considered done”).
2. The remaining app surface (tenancy UI, guest/context flow, brief generation, Studio repair, campaign-run wiring, harness pilot) has **no current implementation specs** — legacy TS-APP specs predate the governed stack, and no spec binds new UI to `/api/v1/workspaces`.

This mandate produces: one reconciled PRD, one authoritative remaining-work ledger, and a set of implementation-grade specs — each passing a measurable quality gate before it may be queued for implementation.

The permitted transition is:

```text
stale PRD + scattered/unowned specs
  -> S1: CURRENT.md reconciled through phase 25 (its own §1.12 rule)
  -> S2: app-completion gap inventory (authoritative remaining-work ledger)
  -> S3: author implementation specs for approved backlog items
  -> S4: quality-gate audit of every spec (rubric-scored, independent lane)
  -> OPERATOR_REVIEW (accept/reject/amend each spec individually)

Track B implementation: NOT_STARTED (separate mandates, one accepted spec each)
```

## 2. Mandatory reading

Before planning or editing, the executing agent SHALL read in full:

1. `docs/PRD/CURRENT.md` — every section, especially §1.1 changelog discipline, §1.3a/§1.3b, §1.4/§1.4a/§1.4b, §1.7 gap ledger, §1.10 decisions, §1.12 maintenance rule, §1.13 override, §1.14 sequencing table.
2. `docs/MASTER_SEQUENCING_PLAN.md` and its per-workstream agent briefs.
3. All 25 CAE execution records under `docs/cae/gemini_execution/` and their completion records under `docs/cae/implementation/` — at minimum the control state, TWC-01 records, UPTL-01 records, and `KNOWN_LEGACY_TEST_DEBT.md`.
4. `api/routers/v1_tenancy.py`, `packages/ca_runtime/src/ca_runtime/workspace_core.py`, `services/pipeline/src/cmf_pipeline/reasoning/model_reasoning_engine.py`, `api/main.py`, `apps/web/src/` routing structure.
5. Legacy specs: `TS-APP-API-001..007`, `TS-APP-UI-001..004`, `TS-APP-COMPOSER-001`, `TS-APP-BRIDGE-001`, `TS-APP-SETUP-001`.
6. Constitutions and FRs relevant to each S3 target (at minimum `CA-CAN-01A_WORKSPACE/MEMBERSHIP/OPERATOR_*`, `FR-CAE-TEN-001..015`).
7. Git history and working-tree state, identifying commits actually inspected.

## 3. Exact scope: four sub-workstreams

### S1 — CURRENT.md reconciliation (surgical, not rewrite)

Update CURRENT.md to phase-25 truth under its own rules: append a dated changelog entry citing evidence records; update §1.4/§1.4a rows whose status changed (F17/F28/F29/F30 generation logic now exists behind services via U2 engine; tenancy core live on Postgres staging; `/api/v1/workspaces` mounted); update §1.7 gap-ledger rows closed by phases 23–25; annotate §1.14 sequencing rows completed (1-A done, 2-A done) versus open (0-A..0-G, 1-B, 1-C, 2-B, 3); record the `CLAIMS_UNVERIFIED_BY_OPERATOR` status of phases 20–22 and their supersession by CA-TWC-01; reference `KNOWN_LEGACY_TEST_DEBT.md`. Do NOT delete or rewrite historical sections — append-and-amend per §1.12. Preserve every still-open finding (Studio `dist/rpc.js`, Blocker 2/5, VAE route absence) with their evidence trails intact.

### S2 — App-completion gap inventory (the “what remains” ledger)

Produce `CAE_APP_COMPLETION_LEDGER.md`: every user-visible capability required for the operator’s definition of “app fully ready,” cross-referenced against (a) live code state, (b) existing specs, (c) governing constitutions/FRs, (d) Sequencing Plan rows. Each row carries: capability, current state (verified citation), owning spec (existing or to-be-authored in S3), dependencies, and estimated bounded scope. Minimum expected rows include: create/manage Workspaces from UI; invite/manage members; register Guest + context from UI; generate interview brief from guest context (via reasoning engine); view brief; campaign creation unblocked (Blocker 2/5); pilot harness runnable end-to-end; Studio bridge repaired. The ledger governs S3 scope — items not in the ledger are not specced.

### S3 — Implementation spec authoring

Author implementation-grade specs for each S2 row lacking one, using the 14-section structure proven by `TS-CAE-TEN-001` (purpose/scope; references; objects & authority; functional requirements; API contracts with exact request/response shapes; data model deltas; UI behavior; error taxonomy; test plan with hard negatives; evidence plan; allowlist of files; risks; rollback; open questions). Expected minimum set:

- `SPEC-TWC-UI-001` — Workspace & membership management screens bound to `/api/v1/workspaces` (create/list/detail/members/grants).
- `SPEC-GST-UI-001` — Guest registration & context screens (workspace-local guest, context fields per constitution, synthetic-data mode).
- `SPEC-BRF-001` — Interview Brief generation flow: guest context → typed operation → U2 reasoning engine → receipted structured brief surfaced via API/UI; epistemic fields `UNVERIFIED`.
- `SPEC-STU-001` — Studio build repair (row 0-C): produce `services/studio/dist/rpc.js`, verify `/revisions` bridge end-to-end.
- `SPEC-CMP-002` — Campaign boundary resolution (rows 0-F + 1-C): decide-and-implement shape for `capability_metadata` sourcing and `workflow` derivation at `_try_compile_harness`; correct the misreporting exception handler to surface `exc.field`/`exc.reason`; wire `WorkflowRunService.create_run()`.
- `SPEC-HAR-001` — Pilot harness manifest (row 0-E pilot-first rule): ONE harness authored through Builder CLI into the real library path, runnable through the resolved campaign boundary.

Every spec MUST cite: governing constitutions/FRs, exact existing code anchors (file:line, verified in-session), the S2 ledger row it fulfills, and its verification method per requirement. Specs propose decisions where the operator must decide (flagged as `OPEN_DECISION` items); they do not silently choose.

### S4 — Spec quality & precision gate (blocking)

Every S3 spec passes a scored rubric before reaching the operator. Rubric dimensions (each scored PASS/FAIL with cited evidence):

1. **Verifiability:** every SHALL has a named verification method (test, probe, or observable behavior) — no requirement without a way to check it.
2. **Anchor precision:** every code citation resolves to a real file/line in the working tree, verified in-session (probe-executed, not asserted).
3. **Traceability:** every requirement maps to a constitution/FR/ledger-row citation that exists at the cited path.
4. **Ambiguity ban:** zero occurrences of “should”, “as appropriate”, “etc.”, “TBD”, or unspecified plural nouns in normative text (OPEN_DECISION flags are the sole escape hatch, and each names the decider).
5. **Contract completeness:** API shapes fully specified (fields, types, status codes, error envelope per TS-APP-API-004 §5 conventions); no endpoint described in prose alone.
6. **Test plan hardness:** each spec includes ≥5 hard negatives — inputs or behaviors that must be *rejected* — with expected rejection mechanism.
7. **Scope honesty:** explicit non-goals and out-of-boundary lists present; no silent scope assumptions.
8. **Independence:** specs authored by the implementation-proposing agent are audited against this rubric by a distinct review pass (self-audit prohibited), with scores recorded in the evidence record.

A spec failing any dimension returns to S3 with the failure cited. The quality-gate results ship as `CAE_SPEC_02_QUALITY_GATE_RESULTS.md`.

## 4. Evidence protocol (live-probe mandatory)

Applies as in Mandates 23–25, adapted to authoring: every code citation verified by an in-session probe (file exists at path:line; symbol greps pasted); every count (specs, ledger rows, rubric dimensions) computed not asserted; CURRENT.md amendments cite the evidence records they summarize; rubric scores include the probe commands used. Validators introduced here execute probes; presence-only checks are non-compliant.

## 5. Authorized artifacts and prohibitions

Gemini MAY create or update only:

- `docs/PRD/CURRENT.md` (append-and-amend per §1.12 only);
- `docs/cae/implementation/CAE_APP_COMPLETION_LEDGER.md`;
- `docs/cae/specs/current/SPEC-TWC-UI-001.md`, `SPEC-GST-UI-001.md`, `SPEC-BRF-001.md`, `SPEC-STU-001.md`, `SPEC-CMP-002.md`, `SPEC-HAR-001.md`;
- `docs/cae/implementation/CAE_SPEC_02_QUALITY_GATE_RESULTS.md`;
- `docs/cae/implementation/CAE_SPEC_02_COMPLETION_RECORD.md`;
- one probe-executing validator under `scripts/cae/audit/verify_ca_spec_02.py`;
- pure/local tests under `tests/cae/` for validator structure only;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md` (status line only).

Gemini SHALL NOT: implement any application/runtime/UI code for anything specified; alter migrations, staging, `.env`, authorities, or receipts; modify ratified constitutions or FRs (route proposed changes to the operator); begin Track B mandates; treat any legacy `TS-APP-*` spec as current-status authority while reconciling; or mark any spec “accepted” — acceptance belongs exclusively to the operator, per spec.

## 6. Adversarial challenges (each must be answered in the Completion Record)

1. CURRENT.md reconciliation quietly rewrites history instead of appending — diffs must show preservation of prior findings.
2. The ledger invents capabilities the operator never asked for, or omits ones already promised elsewhere — cross-check against PRD §1.14, Sequencing Plan, and this mandate’s minimum rows.
3. Specs smuggle in implementation choices reserved for the operator — every non-obvious choice flagged `OPEN_DECISION`.
4. Code citations point at files that moved or symbols that don’t exist — probe-verified citations only.
5. Rubric scoring grades its own homework — independent audit pass required, scores shown with probe commands.
6. Ambiguity hides inside examples rather than requirements text — scan normative sections specifically.
7. A spec duplicates or contradicts a constitution — contradiction routed to operator, never self-resolved.
8. Quality gate waived “because the spec looked fine” — all eight dimensions scored for all six specs, no exemptions.
9. Track B work sneaks into commits — any runtime file touched invalidates the mandate.
10. Test debt register silently shrinks — diff against prior version required.

## 7. Completion, rollback, and operator gate

CA-SPEC-02 completes only when: S1 reconciliation lands with preserved history; the S2 ledger covers the full app-completion surface; all S3 specs exist at 14-section depth; all S4 rubric scores are PASS with probe evidence (or failures explicitly cycled back and resolved); the validator passes; and the control state records `APP_COMPLETION_SPECS_READY_FOR_OPERATOR_REVIEW`.

The Completion Record provides Sections A–H in the established form, including reviewer independence and falsification routes.

**Rollback:** documentation-only; revert commits suffice. No system state mutated.

Gemini SHALL request exactly:

> **Review the six app-completion specs individually: accept, amend, or reject each; resolve the OPEN_DECISION flags you own; confirm the CURRENT.md reconciliation and completion ledger as accurate; and name which accepted spec becomes the first Track B implementation mandate — with no implementation beginning until that naming?**

It SHALL stop after this question.

## 8. Gemini activation prompt (approximately 270 words)

You are the CAE governed execution agent for `CA-SPEC-02 — PRD Reconciliation & App-Completion Specifications`. Blocked until the operator accepts CA-TWC-01 and authorizes this mandate. Read all of docs/PRD/CURRENT.md including its §1.12 amendment discipline, MASTER_SEQUENCING_PLAN.md, the 25-phase execution record chain, KNOWN_LEGACY_TEST_DEBT.md, the live tenancy/reasoning/router sources, and the legacy TS-APP spec set.

Sub-workstreams in order. S1: surgically bring CURRENT.md to phase-25 truth — dated changelog entry, amended status rows, appended corrections; never delete historical findings; preserve open defects like Studio dist and Blockers 2/5 with their evidence trails. S2: build the app-completion ledger — every capability between here and an operable app, cross-referenced to live code, specs, constitutions, and sequencing rows. S3: author six implementation specs at TS-CAE-TEN-001 depth (workspace UI, guest/context UI, brief-generation flow, Studio repair, campaign boundary resolution, pilot harness), each citing probe-verified code anchors and governing law, flagging operator-owned choices as OPEN_DECISION. S4: run the eight-dimension quality gate on every spec — verifiability, anchor precision, traceability, ambiguity ban, contract completeness, hard-negative depth, scope honesty, independent audit; failures cycle back until passing.

Live-probe evidence rules apply to citations and counts; validators must execute probes. No runtime code, schema, staging, or Track B work; no ratified-document edits; no self-granted acceptance. Commit only allowed artifacts, request the exact Section 7 per-spec decision, and stop.
