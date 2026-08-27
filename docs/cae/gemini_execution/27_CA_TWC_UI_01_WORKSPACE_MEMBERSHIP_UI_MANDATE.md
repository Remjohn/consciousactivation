# Gemini Execution Mandate — Phase 27 / CA-TWC-UI-01

**Status:** `DRAFT — BLOCKED UNTIL OPERATOR AUTHORIZES THIS MANDATE`  
**Phase ID:** `CA-TWC-UI-01`  
**Title:** Workspace & Membership Management UI (Track B Implementation #1 of SPEC-TWC-UI-001)  
**Execution classification:** Bounded implementation of one accepted specification: React UI surfaces bound to the existing `/api/v1/workspaces` router; first-login personal-workspace auto-creation via Supabase Auth identity; no schema changes, no new aggregate authority, no other spec's surface touched  
**Required prior decision:** “Authorize CA-TWC-UI-01 to implement accepted SPEC-TWC-UI-001 exactly as amended, as the first Track B mandate.”  
**Required completion gate:** `IMPLEMENT -> VERIFY -> OPERATOR_REVIEW`; GST-UI implementation begins only under a separately authorized mandate.

## 1. Authority, purpose, and boundary

CA-TWC-UI-01 is governed by the CAE Governance & Specification Bridge Bundle v3 and inherits: accepted CA-SPEC-02 records; `SPEC-TWC-UI-001.md` **as amended at the operator gate (DEC-TWC-001 amended v2)**; ratified constitutions `CA-CAN-01A_*`; TS-APP-API-004 §5 error-envelope conventions; and the established live-probe evidence protocol.

**Purpose:** make workspaces real for a human being. After this phase, an authenticated user can open the app, land in their personal workspace, create additional workspaces, add and remove members, and see receipts proving every mutation — all through `/api/v1/workspaces` backed by the typed core, with zero direct database access from the browser.

The permitted transition is:

```text
accepted SPEC-TWC-UI-001 (no UI for tenancy today)
  -> workspace management screens (list / create / detail / members)
  -> first-login auto-create via Supabase Auth identity
  -> integration + hard-negative tests green
  -> OPERATOR_REVIEW

GST/Guest context UI, brief flow, Studio repair,
campaign boundary, harness pilot: NOT_STARTED (each needs its own mandate)
```

## 2. Mandatory reading

Before planning or editing, the executing agent SHALL read in full:

1. `docs/cae/specs/current/SPEC-TWC-UI-001.md` — the entire ratified spec including amendments; this mandate implements it verbatim, and any deviation requires an explicit recorded reason.
2. `api/routers/v1_tenancy.py` (complete), `packages/ca_runtime/src/ca_runtime/workspace_core.py`, relevant Pydantic models, and `api/main.py` mounting.
3. `apps/web/src/`: routing structure, existing API client conventions (`src/api/*`), component patterns, and vitest setup.
4. Governing constitutions: `CA-CAN-01A_WORKSPACE.yaml`, `CA-CAN-01A_WORKSPACE_MEMBERSHIP.yaml`, `CA-CAN-01A_OPERATOR_ACCESS_GRANT.yaml`.
5. Error-envelope contract: `TS-APP-API-004` §5; legacy lesson: `KNOWN_LEGACY_TEST_DEBT.md` rows caused by missing `error_code` fields.
6. Supabase Auth boundary notes as stated in the spec’s identity section.

## 3. Exact scope

1. **Workspace list & creation screen:** render workspaces for the current identity from `GET /api/v1/workspaces`; create via modal form (name validated client-side per spec rules); display live lifecycle status per workspace.
2. **First-login auto-create (DEC-TWC-001 amended):** on initial authenticated session, invoke auto-create so the user lands inside their personal workspace; display name derived from account identity (`"{user.name}'s Workspace"` pattern per amendment); literal `"Default Workspace"` string prohibited; duplicate-safe (re-entry must not create doubles).
3. **Workspace detail screen:** overview panel; member roster (`GET .../memberships`) with role badges; add-member flow (invite by identity input per spec); revoke/remove membership with confirmation dialog; operator-grant view where permitted (read-only listing if grants are out of this router’s write scope — check spec; do not invent endpoints).
4. **Client state discipline:** tenant context (active workspace selection) held client-side and sent on every tenancy request; switching workspace refetches scoped data; zero cross-workspace data rendering (constitution locality).
5. **Error handling per TS-APP-API-004 §5:** every failure path renders the server-provided `error_code`; unmapped errors show generic fallback plus logged code. No silent swallowing.
6. **Tests:** vitest unit tests for components/state; API-boundary tests using mocked or fixture transport covering each endpoint contract, including ≥5 spec hard negatives (invalid name, duplicate slug/membership, unauthorized actor, suspended workspace action, malformed payload). Full repo suites green afterward.

## 4. Evidence protocol (live-probe mandatory)

Every dynamic claim commits verbatim artifacts: exact commands, raw test output pasted unedited into the evidence record; component screenshots only supplement, never substitute, failing/passing test text; counts computed in-session. The validator MUST execute probes (run tests, assert file presence of implemented routes/components referenced by evidence). Presence-only checks are non-compliant. Reviewer must be able to re-run everything byte-for-byte. No invented ratifications: operator decisions appear only when quoted verbatim from operator text.

## 5. Authorized artifacts and prohibitions

Gemini MAY create or update only:

- UI source under `apps/web/src/**` strictly for: routes/pages/components/API-client functions implementing SPEC-TWC-UI-001;
- matching additions to `apps/web/src/api/*` client module;
- tests under `apps/web/src/**/*.test.*` / `tests/web/` and `tests/api/test_v1_tenancy.py` extensions;
- `docs/cae/implementation/CAE_TWC_UI_01_COMPLETION_RECORD.md` plus one probe-executing validator under `scripts/cae/audit/verify_ca_twc_ui_01.py`;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md` (status line only).

Gemini SHALL NOT: modify backend routers, typed core, models, migrations, schema, staging database, `.env`, authorities, or receipts EXCEPT where SPEC-TWC-UI-001 explicitly names a required, minimal backend gap (if discovered: stop and record as `BLOCKED_ON_OPERATOR_INPUT` rather than improvising); touch guest/context/brief/studio/campaign/harness surfaces (later Track B mandates); begin SPEC-GST-UI-001 work; introduce direct Supabase client DB access in the UI; print or commit secrets.

## 6. Adversarial challenges (each must be answered in the Completion Record)

1. UI renders cross-workspace data after a switch because stale cache wasn’t invalidated. — State-discipline tests required.
2. Auto-create fires twice (double-mount/race) producing duplicate workspaces. — Idempotency test required.
3. A failure path shows a raw exception instead of the typed `error_code`. — Every documented error code has a rendered-state test.
4. Component tests mock away the API contract so a shape change passes silently. — Boundary tests must parse real response fixtures.
5. “Done” claimed while repo suites are red. — Full-suite output pasted.
6. Evidence record contains hand-written outputs rather than executed ones. — Reviewer reproduction required byte-for-byte.
7. Scope creeps into guest screens or brief flow. — Any such file touched invalidates the mandate.
8. Backend gaps get patched silently instead of escalated. — Escalation route mandated above.

## 7. Completion, rollback, and operator gate

Completion requires: all five scope items implemented; all tests green including hard negatives; live-probe evidence committed; validator passing against the committed tree; control state updated. Sections A–H completion record in the established form, including reviewer-independence declaration.

**Rollback:** revertable commits; no persistent-environment mutation occurs in this phase beyond synthetic API-created rows that must be receipted and purged with count read-backs if staging was used for verification.

Gemini SHALL request exactly:

> **Accept CA-TWC-UI-01 as the completed Workspace & Membership Management UI implementing ratified SPEC-TWC-UI-001 (auto-create per DEC-TWC-001 amended v2, constitution-conformant isolation, receipt-backed mutations, all tests green) — and authorize CA-GST-UI-01 (Track B #2, Guest Registration & Context UI) mandate drafting only?**

It SHALL stop after this question.

## 8. Gemini activation prompt (approximately 270 words)

You are the CAE governed execution agent for `CA-TWC-UI-01 — Workspace & Membership Management UI`. Blocked until the operator authorizes it. Read ratified SPEC-TWC-UI-001 as amended end-to-end, the v1 tenancy router and typed core it binds to, the web app’s routing and API-client patterns, governing constitutions, TS-APP-API-004 §5 error envelope, and the live-probe evidence rules from mandates 23–26.

Implement exactly five things: the workspace list-and-create screen; first-login auto-create deriving the display name from account identity with idempotent re-entry; the workspace-detail screen with member roster, add/remove flows, and grant visibility per spec; strict client tenant-context discipline with refetch-on-switch and zero cross-workspace leakage; and typed error rendering for every documented error_code per TS-APP-API-004 §5.

Bind exclusively through `/api/v1/workspaces`; the browser never touches the database directly. Cover each endpoint and hard negative with tests whose assertions use real response fixtures. If you discover a genuine backend gap the spec requires, stop that item as BLOCKED_ON_OPERATOR_INPUT with the exact gap isolated — do not patch servers silently.

Commit verbatim command outputs and read-backs as evidence; validators must execute probes; never write an operator ratification you were not given. No guest/brief/studio/campaign/harness work, no migrations or staging mutations, no secrets printed. Run the full suite, paste results, commit only allowed artifacts, request the exact Section 7 decision, and stop.
