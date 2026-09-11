# CAE App-Completion Ledger

**Version:** 1.0.0  
**Authority:** Mandate CA-SPEC-02 (`docs/cae/gemini_execution/26_CA_SPEC_02_PRD_RECONCILIATION_AND_APP_COMPLETION_SPECS_MANDATE.md`)  
**Date:** 2026-08-26  
**Status:** RATIFIED BASELINE  
**Classification:** Governing Audit Ledger (Track A)

---

## 1. Executive Summary

This ledger enumerates every required capability, subsystem contract, and integration bridge necessary to transition the Conscious Activations platform from its current state (relational tenancy live on PostgreSQL staging, model-backed reasoning live in pipeline, headless API operational) to a fully operable, end-to-end multi-tenant application.

Every capability is mapped to:
1. **Live Brownfield Code Anchors** (verified via direct filesystem probes).
2. **Governing Constitutions & Functional Requirements** (v1.2 PRD F01–F30, Master Constitutions `MC-CAE-*`, and TS-APP specs).
3. **Target Implementation Specification** (authored under `docs/cae/specs/current/` at `TS-CAE-TEN-001` depth).
4. **Master Sequencing Row** (mapped to `MASTER_SEQUENCING_PLAN.md` and `docs/PRD/CURRENT.md` §1.14).
5. **Operator Decision Governance** (flagged as `OPEN_DECISION` where policy choices are required).

---

## 2. Master Capability Matrix

| Cap ID | Capability Domain | Subsystem / Layer | Governing Law / PRD Ref | Live Code Anchor (Probe-Verified) | Implementation Spec | Sequencing Row | Current Operational Status |
|---|---|---|---|---|---|---|---|
| **CAP-TWC-01** | Workspace Tenancy & RLS Isolation | `ca_runtime` / `api` | `MC-CAE-WS-001`, `MEM-001`, `OPR-001`, `F01` | `api/routers/v1_tenancy.py:51..285`, `packages/ca_runtime/src/ca_runtime/workspace_core.py:40..170` | `SPEC-TWC-UI-001` | Phase 0-B / 1-B | **POSTGRES_AUTHORITATIVE_STAGING_ONLY** (Backend live; UI pending) |
| **CAP-TWC-02** | Workspace & Member Management UI | `apps/web` | `FR-APP-001..003`, `TS-APP-UI-001` | `apps/web/src/routes/workspace/index.tsx:1..17` (placeholder) | `SPEC-TWC-UI-001` | Phase 0-B / 1-B | **SPECIFIED** (Screen layouts, state hooks, error envelopes ready for build) |
| **CAP-GST-01** | Guest Registration & Research Ingestion | `api` / `apps/web` | `FR-APP-004..005`, `F21`, `F22` | `api/routers/interview_composer.py:44..122`, `apps/web/src/routes/interviews/compose.tsx:13..60` | `SPEC-GST-UI-001` | Phase 1-B | **BUILT & GATED** (API live; UI multi-step flow requires tenant context binding) |
| **CAP-GST-02** | Guest Psychological Profile Context | `apps/web` / `AIR` | `FR-APP-006`, `F28`, `F30` | `apps/web/src/components/interview-composer/ResearchPanel.tsx:1..120` | `SPEC-GST-UI-001` | Phase 1-B | **SPECIFIED** (Context viewer, authority assertion modal, URL/file binding) |
| **CAP-BRF-01** | Model-Backed Inference Engine | `cmf_pipeline` | `CA-UPTL-01`, `F07`, `Sequencing 1-A` | `services/pipeline/src/cmf_pipeline/reasoning/model_reasoning_engine.py:279..375` | `SPEC-BRF-001` | Phase 1-A | **DONE & VERIFIED** (Remote OpenAI/Gemini client, structured JSON parser, SHA-256 receipts) |
| **CAP-BRF-02** | Activative Brief Generation Flow | `api` / `AIR` / `apps/web` | `FR-APP-007..009`, `F21`, `F28..30` | `api/routers/interview_composer.py:124..180`, `apps/web/src/components/interview-composer/BriefPanel.tsx:48..156` | `SPEC-BRF-001` | Phase 2-A | **SPECIFIED** (Model reasoning integration for tension hypothesis & question matrix) |
| **CAP-STU-01** | Studio Build & RPC Bridge | `services/studio` / `api` | `F19`, `F26`, `F27`, `TS-APP-API-006` | `services/studio/package.json:6..12`, `services/studio/src/rpc.ts:1..90`, `api/services/studio_bridge.py:9..60` | `SPEC-STU-001` | Phase 0-C | **SPECIFIED** (Build repair pipeline, crash isolation, RPC error envelope) |
| **CAP-STU-02** | Operator Revision Compiler Integration | `api` / `services/studio` | `F26`, `TS-CAS-AUT-001` | `api/routers/revisions.py:25..120` | `SPEC-STU-001` | Phase 1-B | **SPECIFIED** (Bridged execution to `compileNaturalLanguageRevision`) |
| **CAP-CMP-01** | Blocker 2: Capability Metadata Synthesis | `cmf_pipeline` / `api` | `F02`, `TS-APP-BRIDGE-001 §4` | `api/routers/campaigns.py:129..177`, `services/pipeline/src/cmf_pipeline/intake/harness_compiler.py:130..180` | `SPEC-CMP-002` | Phase 0-F / 1-C | **SPECIFIED** (Dynamic synthesis from `CapabilityOwnershipGraph`, eliminating hardcoded `{}`) |
| **CAP-CMP-02** | Blocker 5: Workflow Graph Binding | `cmf_pipeline` / `api` | `F03`, `F05`, `TS-APP-BRIDGE-001 §4` | `api/routers/campaigns.py:275..304`, `services/pipeline/src/cmf_pipeline/workflow/application/compiler.py:45..150` | `SPEC-CMP-002` | Phase 0-F / 1-C | **SPECIFIED** (Workflow compilation binding, eliminating hardcoded `workflow=None`) |
| **CAP-HAR-01** | Pilot Harness Definition & Library Export | `cmf_builder` / `api` | `F02`, `F09`, `F12`, `F24` | `services/builder/src/cmf_builder/domain/portable_export.py:30..120`, `api/routers/harnesses.py:40..110` | `SPEC-HAR-001` | Phase 0-E | **SPECIFIED** (Manifest for `CAR-LST-Olympics-4-5-10`, Stage 1/2 verification, library population) |
| **CAP-HAR-02** | Entry-Point-B Campaign Integration Run | `api` / `cmf_pipeline` | `F20`, `F21`, `F23`, `F24` | `api/routers/campaigns.py:230..305`, `services/pipeline/src/cmf_pipeline/batch/service.py:30..110` | `SPEC-HAR-001` | Phase 3 | **SPECIFIED** (End-to-end integration harness, media intake, batch compilation) |

---

## 3. Subsystem Detailed Gap & Transition Ledger

### 3.1 Workspace & Tenancy Subsystem (`CAP-TWC-01`, `CAP-TWC-02`)
- **Current State:** The backend tenancy schema is fully deployed to Supabase PostgreSQL staging under schema `cae`. 23 base tables exist with forced RLS. `api/routers/v1_tenancy.py` exposes 7 operations. However, the frontend (`apps/web/src/routes/workspace/index.tsx`) renders a static `PlaceholderPage`.
- **Target State:** Interactive React workspace console providing:
  1. Workspace switcher & global context state provider (`WorkspaceProvider`).
  2. Workspace creation modal (`POST /api/v1/workspaces`).
  3. Membership management table with role assignment (`POST /api/v1/workspaces/{id}/memberships`).
  4. Tenant operator view with global cross-workspace enumeration (`GET /api/v1/workspaces`).
- **Governing Spec:** [`SPEC-TWC-UI-001.md`](file:///d:/Work/consciousactivation/docs/cae/specs/current/SPEC-TWC-UI-001.md).

### 3.2 Guest & Context Subsystem (`CAP-GST-01`, `CAP-GST-02`)
- **Current State:** Backend `POST /api/interviews/compose/research` accepts multipart uploads and creates `GuestResearchPackage`. Frontend `apps/web/src/routes/interviews/compose.tsx` has basic form fields but lacks workspace tenancy context headers, authority scope selectors, and preview of uploaded source documents.
- **Target State:** Comprehensive guest onboarding and context ingestion flow:
  1. Tenant-scoped guest registration with operator authority assertion.
  2. Document drag-and-drop with SHA-256 client-side preview.
  3. Structured source URL array ingestion with regex validation.
  4. Live read-back display of registered guest packages (`GET /api/interviews/compose/research/{id}`).
- **Governing Spec:** [`SPEC-GST-UI-001.md`](file:///d:/Work/consciousactivation/docs/cae/specs/current/SPEC-GST-UI-001.md).

### 3.3 Interview Brief & Reasoning Subsystem (`CAP-BRF-01`, `CAP-BRF-02`)
- **Current State:** `ModelReasoningEngine` is built and verified (`services/pipeline/src/cmf_pipeline/reasoning/model_reasoning_engine.py`). However, `api/routers/interview_composer.py::create_brief` still requires operator hand-entry of all tension hypotheses, matrix seeds, and planned questions. Brand voice resolution (`resolve_brand_voice_refs`) 404s due to unpopulated brand context.
- **Target State:** Integrated AI-assisted brief composer:
  1. Automated tension hypothesis and psychological role matrix generation via `ModelReasoningEngine.infer()`.
  2. Fallback handling for unpopulated brand contexts (`OPEN_DECISION: Brand Context Optionality`).
  3. Production of cryptographically signed immutable reasoning receipts (`receipt_sha256`).
  4. Interactive brief review and editing UI in `apps/web/src/components/interview-composer/BriefPanel.tsx`.
- **Governing Spec:** [`SPEC-BRF-001.md`](file:///d:/Work/consciousactivation/docs/cae/specs/current/SPEC-BRF-001.md).

### 3.4 Studio Repair & Bridge Subsystem (`CAP-STU-01`, `CAP-STU-02`)
- **Current State:** `api/services/studio_bridge.py` executes `node services/studio/dist/rpc.js`. Because `services/studio/dist/` is unbuilt in git, any call to `/api/revisions` crashes immediately with `StudioBridgeCrash`.
- **Target State:** Deterministic build and RPC bridge architecture:
  1. Standardized build pipeline (`npm run build` in `services/studio`) generating `dist/rpc.js` and `dist/index.js`.
  2. Robust error boundary in `StudioBridge` converting exit code 1 / timeout / syntax errors into TS-APP-API-004 compliant HTTP 502/504 errors.
  3. RPC command handlers for `compileNaturalLanguageRevision` and `validateCampaignDraft`.
  4. Automated build verification tests in CI.
- **Governing Spec:** [`SPEC-STU-001.md`](file:///d:/Work/consciousactivation/docs/cae/specs/current/SPEC-STU-001.md).

### 3.5 Campaign Boundary & Blocker Resolution Subsystem (`CAP-CMP-01`, `CAP-CMP-02`)
- **Current State:** `api/routers/campaigns.py::_try_compile_harness` hardcodes `capability_metadata={}` (tripping Blocker 2) and `workflow=None` (tripping Blocker 5), returning `BRIDGE_BLOCKED` and a hardcoded misleading error message.
- **Target State:** Complete campaign harness compilation bridge:
  1. Synthesis of `capability_metadata` using `CapabilityOwnershipGraph` matching harness requirements.
  2. Projection of `workflow` graph via `RuntimeWorkflowCompiler` into intake contracts.
  3. Detailed error categorization returning exact blocker field (`field`, `reason`) on validation failure.
  4. Full lifecycle progression from `DRAFT` $\rightarrow$ `INTAKE_COMPILED` $\rightarrow$ `ACTIVE`.
- **Governing Spec:** [`SPEC-CMP-002.md`](file:///d:/Work/consciousactivation/docs/cae/specs/current/SPEC-CMP-002.md).

### 3.6 Pilot Harness & Integration Subsystem (`CAP-HAR-01`, `CAP-HAR-02`)
- **Current State:** Stage 1 (observation) and Stage 2 (composition spec) are 49/49 verified, but 0/49 `manifest.json` files exist in `CA_HARNESS_LIBRARY_ROOT`.
- **Target State:** End-to-end verified pilot harness and campaign run:
  1. Authoring and export of pilot harness `CAR-LST-Olympics-4-5-10` into `CA_HARNESS_LIBRARY_ROOT`.
  2. Verification via `cmf-builder inspect` and `/api/harnesses` endpoint.
  3. Execution of full Entry-Point-B campaign creation, compilation, and batch rendering.
  4. Automated integration test asserting zero regression across the vertical slice.
- **Governing Spec:** [`SPEC-HAR-001.md`](file:///d:/Work/consciousactivation/docs/cae/specs/current/SPEC-HAR-001.md).

---

## 4. Ratified Decision Register (Operator Gate Decisions — 2026-08-26)

| Decision ID | Spec Reference | Summary of Operator Choice | Ratified Decision & Governing Discipline | Gate Status |
|---|---|---|---|---|
| **DEC-TWC-001** | `SPEC-TWC-UI-001` §14 | Default Workspace on Initial User Login | **Auto-create personal workspace approved**: Display name derived from account identity (e.g. `"${user.name}'s Workspace"` or `${account.email}`), NOT literal `"Default Workspace"`. All creations flow via typed core with immutable receipts. | `ACCEPTED_AS_AMENDED` |
| **DEC-GST-001** | `SPEC-GST-UI-001` §14 | Guest File Upload Size Limits & Transfer Architecture | **Granular Per-Class Tiers (AMENDED v2)**: Documents 50MB (PDF/DOCX/TXT/MD), Compressed audio 500MB (M4A/MP3), WAV 1GB, Video 4GB default via `CA_MEDIA_MAX_VIDEO_MB` env override. Direct presigned Supabase Storage uploads with chunked transfer (zero API buffering >100MB). Mandatory SHA-256 validation & quarantine per `FR-CAE-TEN-010/011`. | `ACCEPTED_AS_AMENDED` |
| **DEC-BRF-001** | `SPEC-BRF-001` §14 | Brand Context Reference Enforcement & Two-Mode Discipline | **Zero Silent Fallback**: Absence of `brand_ref` permitted with output marked `unbranded: true`; requested-but-missing brand ref is a hard typed error (`BRAND_CONTEXT_NOT_FOUND`). | `ACCEPTED_AS_AMENDED` |
| **DEC-STU-001** | `SPEC-STU-001` §14 | Node Subprocess Persistence & Timeout Configuration | **Per-Call Subprocesses Approved**: Timeout becomes env-configurable via `CA_STUDIO_RPC_TIMEOUT_SECONDS` (default 10s). | `ACCEPTED_AS_AMENDED` |
| **DEC-CMP-001** | `SPEC-CMP-002` §14 | Default Workflow Role Topology & ANALYST Node Contract | **Canonical 4-Node Topology (AMENDED v2)**: `HUNTER` $\rightarrow$ `COMPOSER` $\rightarrow$ `ANALYST` $\rightarrow$ `COMMANDER` (mirroring `demo.py` plus one node). `ANALYST` node: reads draft + editorial contracts + evidence spans; emits `SemanticAssessment` (read-only); epistemic inputs to human gate; violations route through `repair_laws` back to `COMPOSER`. | `ACCEPTED_AS_AMENDED` |
| **DEC-HAR-001** | `SPEC-HAR-001` §14 | Pilot Harness Selection for Stage 3 Integration Gate | **`CAR-LST-Olympics-4-5-10` Approved**: Pilot-first rule honored; multi-track video harnesses deferred until single-pilot baseline vertical slice is operational. | `ACCEPTED` |


---

## 5. Audit & Traceability Certification

This ledger has been verified against the live repository state as of 2026-08-26. All cited files, line ranges, and architectural relationships reflect actual source code rather than hypothetical designs.
