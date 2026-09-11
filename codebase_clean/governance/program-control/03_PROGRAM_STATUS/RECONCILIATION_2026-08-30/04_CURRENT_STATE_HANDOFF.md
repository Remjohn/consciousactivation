# CAE Current-State Handoff & Freeze Record

- **Mandate ID**: `CA-CSR-04` (Final Verification, Freeze & Runtime-Convergence Handoff)
- **Frozen Date**: `2026-08-30`
- **Repository Commit**: `3a92a8394fa6d73973a6ad5d0b5a3fe1f95ed76a`
- **Canonical PRD Version**: `0.3.0` (`docs/PRD/CURRENT.md`)
- **Authority Ledger**: `governance/program-control/03_PROGRAM_STATUS/RECONCILIATION_2026-08-30/01_CURRENT_STATE_LEDGER.yaml`
- **Verdict**: `PASS_WITH_LIMITATIONS`

---

## 1. VERIFIED_NOW (Fully Evidenced & Passing)

The following subsystems and capabilities are verified by direct physical code inspection and 298 passing unit/integration tests:

1. **CAE Tenancy & Isolation Core**:
   - PostgreSQL staging authority (`MC-CAE-WS-001/MEM-001/OPR-001`).
   - 23 base tables under schema `cae` with Row-Level Security (RLS) policies enforced.
   - 121 passing tests in `tests/cae/` verifying workspace context, isolation boundaries, and typed runtime operations.
2. **CAE Interview Program (Mandates M01–M11)**:
   - Dynamic Adaptive Question Frontier (`frontier_service.py`) across 4 lifecycle states.
   - Contextual Question Resolution (`resolution_engine.py`) grounded in live transcript tokens.
   - Semantic Acquisition (`semantic_acquisition.py`) mapping responses to domain hypotheses.
   - Composition Compatibility (`composition_compatibility.py`) checking downstream harness constraints.
   - Cryptographic Evidence Handoff (`evidence_handoff.py`) binding transcript spans to candidate generation.
   - Candidate Menu Utility Ranking (`candidate_menu.py`) avoiding quota forcing.
   - Verified with 80 passing tests in `tests/interview_intelligence/` and 16 in `tests/interview_composer/` (96 total).
3. **Editorial Intelligence Architecture (11 Dedicated Services)**:
   - 11 standalone services (`world-intelligence` through `outcome-intelligence`) implementing all 17 core objects from `CAE_EDITORIAL_OBJECT_REGISTER.md`.
   - Verified with 81 passing tests across `tests/*_intelligence/` and `tests/production_program/`.
4. **Anti-Collapse Invariants**:
   - Distinct entity types strictly enforced: `ResearchSignal` != `CollisionHypothesis`, `EvidenceSegment` != `MediaAsset`, `ContentCandidate` != `EditorialStoryboard`, `SemanticProgram` != `CompositionIR`.

---

## 2. VERIFIED_PARTIAL (Working Subsystems with Gated Integration)

1. **Pipeline Application & Workflow Scheduler**:
   - `services/pipeline/src/cmf_pipeline/workflow/` contains real `DeterministicScheduler` and `RuntimeWorkflowCompiler`.
   - Gated from live campaign creation due to Blocker 2 and Blocker 5 in `api/routers/campaigns.py`.
2. **Stage 1 & Stage 2 Visual Syntax Pipeline**:
   - Stage 1 vision-model observations and Stage 2 composition spec compilation verified for 49 harnesses.
   - Gated from live production ingestion due to harness library export and manifest generation pending.
3. **Studio RPC Bridge**:
   - `services/studio/dist/rpc.js` exists and exposes JSON stdin/stdout dispatching.
   - Gated from web frontend due to decoupled TypeScript types in `apps/web`.

---

## 3. OPEN_BLOCKERS

1. **Blocker 2 (Capability Metadata)**:
   - Location: `api/routers/campaigns.py::_try_compile_harness`
   - Cause: `capability_metadata={}` is hardcoded, causing any harness with declared capabilities to fail intake validation.
2. **Blocker 5 (Workflow Graph)**:
   - Location: `api/routers/campaigns.py::_try_compile_harness`
   - Cause: `workflow=None` is hardcoded, requiring runtime caller-supplied workflow derivation.
3. **VAE API Door & Delegation Invocation**:
   - Location: `api/main.py` and `services/pipeline/src/cmf_pipeline/delegation/service.py`
   - Cause: `/api/vae` router is not mounted, and `PipelineApplication.configure_visual_delegation()` is uncalled in live API wiring.
4. **Known Legacy Test Debt**:
   - 7 pre-existing legacy test failures outside CAE domain catalogued in `KNOWN_LEGACY_TEST_DEBT.md`.

---

## 4. UNVERIFIED_CLAIMS (Superficial or Missing Implementations)

1. **Dense / Graph / Visual Retrieval**:
   - Lexical retrieval is verified (`AuthorityFirstRetrievalService`), but vector embeddings, knowledge graphs, and multimodal retrieval are not implemented in runtime code.
2. **Automated Audio-to-Transcript (ASR)**:
   - Transcription ingestion is verified for `PRE_ALIGNED_JSON` and `SRT`, but automatic Whisper/ASR transcription is not implemented.

---

## 5. OPERATOR_DECISIONS_REQUIRED

1. **Campaign Creation Bridge Resolution**:
   - Authorize resolution of Blocker 2 (`capability_metadata`) and Blocker 5 (`workflow`) in `api/routers/campaigns.py` to bridge Builder harness exports to Pipeline execution.
2. **VAE Integration Pathway**:
   - Decide whether to mount `/api/vae` and wire `configure_visual_delegation()` in `PipelineApplication`.
3. **Studio Frontend Convergence**:
   - Decide whether to unify `apps/web` domain types with `services/studio`.

---

## 6. NEXT_RUNTIME_CONVERGENCE_CANDIDATES (Planning Input Only)

> [!NOTE]
> This section is strictly planning input and does **not** authorize execution. Any runtime work must be authorized under a separate governed mandate program.

1. **Candidate 1: Campaign Creation Bridge Wiring (Blocker 2 & 5)**
   - Connect `RuntimeWorkflowCompiler` and `CapabilityOwnershipGraph` into `api/routers/campaigns.py::_try_compile_harness`.
2. **Candidate 2: Live VAE Delegation Router Mount**
   - Mount `/api/vae` in `api/main.py` and invoke `configure_visual_delegation()` in API startup dependencies.
3. **Candidate 3: Legacy Test Debt Remediation**
   - Resolve the 7 catalogued legacy test failures in `KNOWN_LEGACY_TEST_DEBT.md`.
4. **Candidate 4: Studio Domain Package Monorepo Consumption**
   - Refactor `apps/web` to consume compiled types and validators directly from `services/studio`.
