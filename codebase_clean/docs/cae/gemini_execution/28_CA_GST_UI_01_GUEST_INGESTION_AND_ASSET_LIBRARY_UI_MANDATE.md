# Gemini Execution Mandate — Phase 28 / CA-GST-UI-01

**Status:** `DRAFT — BLOCKED UNTIL OPERATOR AUTHORIZES THIS MANDATE`  
**Phase ID:** `CA-GST-UI-01`  
**Title:** Guest Ingestion & Asset Library UI (Track B Implementation #2 of SPEC-GST-UI-001)  
**Execution classification:** Bounded implementation of one accepted specification: React UI surfaces in `apps/web` bound to `/api/interviews/compose/research` (and direct presigned storage endpoints per `DEC-GST-001 v2`); tenant workspace injection from `WorkspaceContext`; no database schema changes, no new aggregate authority, no other spec's surface touched  
**Required prior decision:** “Authorize CA-GST-UI-01 to implement accepted SPEC-GST-UI-001 exactly as amended by DEC-GST-001 v2, as the second Track B mandate.”  
**Required completion gate:** `IMPLEMENT -> VERIFY -> OPERATOR_REVIEW`; Brief UI implementation begins only under a separately authorized mandate.

## 1. Authority, purpose, and boundary

CA-GST-UI-01 is governed by the CAE Governance & Specification Bridge Bundle v3 and inherits: accepted CA-SPEC-02 records; `SPEC-GST-UI-001.md` **as amended by DEC-GST-001 v2** (tiered upload limits, direct presigned storage uploads, SHA-256 verification and quarantine, authority attestation); ratified constitutions `CA-CAN-01B_GUEST.yaml` and `CA-CAN-01B_MEDIA_ASSET.yaml`; TS-APP-API-004 §5 error-envelope conventions; and the established live-probe evidence protocol.

**Purpose:** enable operators and producers to register guest profiles, attach reference URLs, upload research documents and rich media assets with strict integrity verification, attest to operator authority, and inspect immutable research packages—all scoped strictly to the active tenant workspace.

The permitted transition is:

```text
accepted SPEC-GST-UI-001 (basic un-scoped ResearchPanel stub)
  -> guest registration & context ingestion screens (profile / URLs / tiered upload / authority modal)
  -> direct presigned upload orchestration with client SHA-256 integrity calculation
  -> research package read-back inspection view with hash verification
  -> integration + hard-negative tests green (HN-GST-01..05)
  -> OPERATOR_REVIEW

BRF (Brief UI), STU (Studio UI), CMP (Campaign UI), HAR (Harness UI): NOT_STARTED
```

## 2. Mandatory reading

Before planning or editing, the executing agent SHALL read in full:

1. `docs/cae/specs/current/SPEC-GST-UI-001.md` — the entire ratified spec including amendments (`DEC-GST-001 v2`); this mandate implements it verbatim.
2. `api/routers/interview_composer.py`, `api/schemas/interview_composer.py`, and `api/services/media_store.py`.
3. `apps/web/src/routes/interviews/compose.tsx`, `apps/web/src/components/interview-composer/ResearchPanel.tsx`, and `apps/web/src/context/WorkspaceContext.tsx`.
4. Governing constitutions: `CA-CAN-01B_GUEST.yaml` and `CA-CAN-01B_MEDIA_ASSET.yaml`.
5. Error-envelope contract: `TS-APP-API-004 §5`.

## 3. Exact scope

1. **Guest Registration Surface (FR-APP-004):** capture guest identity (`guest_name`, `project_id`) with automatic injection of `workspace_id` from active `WorkspaceContext`.
2. **Research Context & Source URL Management (FR-APP-005):** interactive URL input list with live syntax validation and deduplication.
3. **Tiered Upload & Asset Dropzone (DEC-GST-001 v2):** drag-and-drop file upload zone enforcing per-class limits (Documents: 50MB, Compressed audio: 500MB, WAV audio: 1GB, Video: 4GB), presigned storage upload handling with progress indicators, and client-side SHA-256 hash calculation.
4. **Operator Authority Scope Attestation Modal (FR-APP-006):** explicit operator attestation dialog capturing `operator_id`, `authority_scope`, and `assertion_id` prior to package finalization.
5. **Research Package Read-Back Inspector:** detailed read-back view rendering package ID, revision, registered URLs, and uploaded assets with byte sizes and SHA-256 checksums.
6. **Error Handling per TS-APP-API-004 §5:** render structured error envelopes with error badges for all rejection modes (`GUEST_NAME_INVALID`, `MEDIA_SIZE_EXCEEDED`, `MEDIA_HASH_MISMATCH`, `AUTHORITY_REQUIRED`, `WORKSPACE_NOT_FOUND`).
7. **Tests:** comprehensive vitest unit and integration suites covering all components, API client contracts, and hard negatives HN-GST-01 through HN-GST-05. Full repo test suites must remain 100% green.

## 4. Evidence protocol (live-probe mandatory)

Every dynamic claim commits verbatim artifacts: exact commands, raw test output pasted unedited into the evidence record; component screenshots only supplement, never substitute, failing/passing test text; counts computed in-session. The validator MUST execute probes (run tests, assert file presence of implemented routes/components referenced by evidence). Presence-only checks are non-compliant. Reviewer must be able to re-run everything byte-for-byte. No invented ratifications: operator decisions appear only when quoted verbatim from operator text.

## 5. Authorized artifacts and prohibitions

Gemini MAY create or update only:

- UI source under `apps/web/src/**` strictly for: routes/pages/components/API-client functions implementing SPEC-GST-UI-001;
- matching additions to `apps/web/src/api/*` client module;
- tests under `apps/web/src/**/*.test.*` / `tests/web/` and `tests/api/` router test extensions;
- `docs/cae/implementation/CAE_GST_UI_01_COMPLETION_RECORD.md` plus one probe-executing validator under `scripts/cae/audit/verify_ca_gst_ui_01.py`;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md` (status line only).

Gemini SHALL NOT: modify backend schemas, migrations, staging database, `.env`, authorities, or receipts EXCEPT where SPEC-GST-UI-001 explicitly names a required, minimal backend gap (if discovered: stop and record as `BLOCKED_ON_OPERATOR_INPUT` rather than improvising); touch brief/studio/campaign/harness surfaces (later Track B mandates); begin SPEC-BRF-001 work; introduce direct Supabase client DB access in the UI; print or commit secrets.

## 6. Adversarial challenges (each must be answered in the Completion Record)

1. Uploaded file exceeds tier limit or fails MIME type validation. — Inline pre-flight validation test required (`HN-GST-02`).
2. Client sends spoofed or corrupted SHA-256 checksum. — Hash verification rejection and quarantine test required (`HN-GST-03`).
3. Guest package is submitted without operator authority attestation. — Modal gating and API 422 rejection test required (`HN-GST-05`).
4. Research package created under one workspace leaks into another workspace. — Strict tenant isolation test required (`HN-GST-04`).
5. A failure path shows an unhandled exception instead of the typed `error_code`. — TS-APP-API-004 §5 error envelope test required.
6. “Done” claimed while repo suites are red. — Full-suite output pasted.
7. Scope creeps into brief generation or studio screens. — Any such file touched invalidates the mandate.
8. Backend gaps get patched silently instead of escalated. — Escalation route mandated above.

## 7. Completion, rollback, and operator gate

Completion requires: all six scope items implemented; all tests green including hard negatives; live-probe evidence committed; validator passing against the committed tree; control state updated. Sections A–H completion record in the established form, including reviewer-independence declaration.

**Rollback:** revertable commits; no persistent-environment mutation occurs in this phase beyond synthetic API-created rows that must be receipted and purged with count read-backs if staging was used for verification.

Gemini SHALL request exactly:

> **Accept CA-GST-UI-01 as the completed Guest Ingestion & Asset Library UI implementing ratified SPEC-GST-UI-001 (tiered uploads per DEC-GST-001 v2, presigned direct upload, SHA-256 verification, operator authority attestation, all tests green) — and authorize CA-BRF-UI-01 (Track B #3, Brief Ingestion & Generation UI) mandate drafting only?**

It SHALL stop after this question.

## 8. Gemini activation prompt (approximately 270 words)

You are the CAE governed execution agent for `CA-GST-UI-01 — Guest Ingestion & Asset Library UI`. Blocked until the operator authorizes it. Read ratified SPEC-GST-UI-001 as amended by DEC-GST-001 v2 end-to-end, the interview composer router and media store services it binds to, the web app’s routing and API-client patterns, governing constitutions CA-CAN-01B_GUEST and CA-CAN-01B_MEDIA_ASSET, TS-APP-API-004 §5 error envelope, and the live-probe evidence rules from mandates 23–27.

Implement exactly six things: the guest profile registration form with automatic active workspace injection; the interactive source URL manager with format validation; the tiered asset upload dropzone with per-class limits (Docs 50MB, Audio 500MB/1GB, Video 4GB) and presigned direct upload orchestration; client-side SHA-256 hash calculation and integrity validation; the operator authority scope attestation modal; and the read-back research package inspector rendering verified assets and hashes.

Bind through `/api/interviews/compose/research`; the browser never touches the database directly. Cover each endpoint and hard negative (HN-GST-01..05) with tests whose assertions use real response fixtures. If you discover a genuine backend gap the spec requires, stop that item as BLOCKED_ON_OPERATOR_INPUT with the exact gap isolated — do not patch servers silently.

Commit verbatim command outputs and read-backs as evidence; validators must execute probes; never write an operator ratification you were not given. No brief/studio/campaign/harness work, no migrations or staging mutations, no secrets printed. Run the full suite, paste results, commit only allowed artifacts, request the exact Section 7 decision, and stop.
