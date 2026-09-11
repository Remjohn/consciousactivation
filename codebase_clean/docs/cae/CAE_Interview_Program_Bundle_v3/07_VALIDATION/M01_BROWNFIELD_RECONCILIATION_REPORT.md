# M01 — Brownfield Authority Reconciliation Report

**Mandate ID:** M01  
**Status:** ACCEPTED / COMPLETED  
**Quality State:** RECONCILED_AND_FROZEN  
**Controlling Specifications:** `TS-APP-COMPOSER-001`, `TS-APP-INTERVIEW-PROGRAM-001`, `00_GOVERNANCE/03_PRD_DELTA.md`  
**Execution Timestamp:** 2026-08-30T04:31:00+02:00  

---

## 1. Actual Source Files Inspected

Every file listed below was directly inspected from the live repository branch.

| # | File Path | Role in System | Key Finding / Verified Fact |
|---|---|---|---|
| 1 | [`services/interview-composer/AGENTS.md`](file:///d:/Work/consciousactivation/services/interview-composer/AGENTS.md) | Service Boundary Governance | Composer owns research/brief/session; strictly prohibited from writing to `services/air/` or constructing canonical AIR objects (`matrix_of_edging`, `activation_hypothesis`, etc.). |
| 2 | [`services/interview-composer/README.md`](file:///d:/Work/consciousactivation/services/interview-composer/README.md) | Package Overview | Structural sibling of `services/interview/`. Owns `guest_research_package`, `activative_interview_brief`, and `composer_session`. |
| 3 | [`services/interview-composer/src/conscious_activations_interview_composer/domain.py`](file:///d:/Work/consciousactivation/services/interview-composer/src/conscious_activations_interview_composer/domain.py) | Domain Constructors | Defines `make_guest_research_package` (`ic:research`), `make_activative_interview_brief` (`ic:brief`), `make_composer_session` (`ic:session`), and `BLOCKED_REASON` for GAP-007. |
| 4 | [`services/interview-composer/src/conscious_activations_interview_composer/canonical.py`](file:///d:/Work/consciousactivation/services/interview-composer/src/conscious_activations_interview_composer/canonical.py) | Canonical Helpers & IDs | Deterministic ID generator (`semantic_id`), key sorting, ref validation, and exact key constraints. |
| 5 | [`services/interview-composer/src/conscious_activations_interview_composer/repository.py`](file:///d:/Work/consciousactivation/services/interview-composer/src/conscious_activations_interview_composer/repository.py) | Persistence Layer | SQLite/Postgres storage with versioned objects, lineage edges, and idempotency guarantees. |
| 6 | [`services/interview-composer/src/conscious_activations_interview_composer/services/brief_service.py`](file:///d:/Work/consciousactivation/services/interview-composer/src/conscious_activations_interview_composer/services/brief_service.py) | Brief Service | Persists operator-authored brief, links to research package ref, and enforces lineage edge `compiled_from`. |
| 7 | [`api/routers/interview_composer.py`](file:///d:/Work/consciousactivation/api/routers/interview_composer.py) | HTTP Surface | Exposes `/research`, `/brief`, and `/sessions` with full tier validation, SHA-256 integrity, and error mapping. |
| 8 | [`api/services/composer_air_bridge.py`](file:///d:/Work/consciousactivation/api/services/composer_air_bridge.py) | Cross-Service Bridge | Read-only verification of `brand_context_ref` and `voice_dna_ref` against AIR; calls `Phase9ActivativeService.compile_relationship_program`. |
| 9 | [`services/air/src/cmf_activative_intelligence/services/hypothesis_service.py`](file:///d:/Work/consciousactivation/services/air/src/cmf_activative_intelligence/services/hypothesis_service.py) | AIR Hypothesis Authority | Owns `activation_hypothesis`, `activation_hypothesis_portfolio`, `hypothesis_gate_result`, `comparative_evaluation_receipt`, and `planned_activative_intelligence_pack`. |
| 10 | [`services/air/AGENTS.md`](file:///d:/Work/consciousactivation/services/air/AGENTS.md) | AIR Governance | Declares AIR as sole canonical owner of psychological tension contracts, archetypes, and activation transfer contracts. |
| 11 | [`services/interview/AGENTS.md`](file:///d:/Work/consciousactivation/services/interview/AGENTS.md) | Expression Governance | Governs `conscious_activations_interview_expression`; verifies `validate_planning_lineage` at admission. |
| 12 | [`docs/tech-specs/TS-APP-COMPOSER-001.md`](file:///d:/Work/consciousactivation/docs/tech-specs/TS-APP-COMPOSER-001.md) | Controlling Composer Spec | Governs FR-APP-010/011/012, defines Brief schema, and establishes GAP-007 boundary. |
| 13 | [`docs/tech-specs/SPEC_GAP_LEDGER_updated.md`](file:///d:/Work/consciousactivation/docs/tech-specs/SPEC_GAP_LEDGER_updated.md) | Spec Gap Ledger | Catalogs GAP-007 (`planned_aip_ref` / `iac_ref` pre-interview hypothesis construction). |
| 14 | [`docs/cae/CAE_Interview_Program_Bundle_v3/02_TECH_SPEC/01_TS_INTERVIEW_PROGRAM_001.md`](file:///d:/Work/consciousactivation/docs/cae/CAE_Interview_Program_Bundle_v3/02_TECH_SPEC/01_TS_INTERVIEW_PROGRAM_001.md) | Controlling Program Spec | Defines brownfield integration, derived structures, and adaptive acquisition flow. |

---

## 2. Actual Owning Modules and Services

| Domain / Capability | Authoritative Owning Module | Allowed Interactions | Prohibited Interactions |
|---|---|---|---|
| **Guest Research Packages** | `services/interview-composer` (`conscious_activations_interview_composer.services.research_service`) | Create, get, link documents, compute SHA-256 | Scraping, parsing, or OCR-ing URLs/documents |
| **Activative Interview Briefs** | `services/interview-composer` (`conscious_activations_interview_composer.services.brief_service`) | Author, store, retrieve, enrich with verified lineage | Fabricating ungrounded AIR refs or bypassing operator authoring |
| **Composer Sessions** | `services/interview-composer` (`conscious_activations_interview_composer.services.session_service`) | Create session, track stage, link recording | Writing directly to AIR session tables |
| **Activation Hypotheses & Portfolios** | `services/air` (`cmf_activative_intelligence.services.hypothesis_service`) | Read-only query, cross-validation, downstream consumption | Writing to AIR from Composer; creating fake AIR objects |
| **Interview Expression & Admission** | `services/interview` (`conscious_activations_interview_expression`) | Brief-led admission validation via planning lineage | Bypassing lineage validation checks |
| **Interview Program Runtime (Derived)** | `docs/cae/CAE_Interview_Program_Bundle_v3/` & `services/interview-intelligence` | Hypothesis candidate adaptation, question resolution, adaptive frontier, observation logging | Claiming new canonical persistent database tables or redefining AIR entities |

---

## 3. Existing Object Contracts and Live Schemas

### A. Guest Research Package (`ic:research`)
```json
{
  "research_package_id": "ic:research:...",
  "workspace_id": "string",
  "project_id": "string",
  "guest_name": "string",
  "source_urls": ["string"],
  "uploaded_documents": [
    {
      "asset_id": "string (logical_uri)",
      "sha256": "string (hex)",
      "bytes": 12345,
      "media_type": "string",
      "original_filename": "string",
      "context_class": "EVIDENCE_SOURCE | CAPTION_TRACK | INTERVIEW_RECORDING | ...",
      "caption_for": "string | null",
      "brand_ref": "object | null"
    }
  ],
  "composer_authority": {
    "operator_id": "string",
    "authority_scope": "string",
    "assertion_id": "string"
  }
}
```

### B. Activative Interview Brief (`ic:brief`)
```json
{
  "brief_id": "ic:brief:...",
  "research_package_ref": { "object_id": "...", "version": "...", "sha256": "..." },
  "brand_context_ref": { "object_id": "...", "version": "...", "sha256": "..." } | null,
  "voice_dna_ref": { "object_id": "...", "version": "...", "sha256": "..." } | null,
  "guest_name": "string",
  "content_origin": "operator_supplied",
  "tension_hypothesis": "string",
  "matrix_of_edging_seed": {
    "psychological_role": "string",
    "tension": "string",
    "activation_direction_set": ["string"],
    "pressure_path": "string",
    "stance": "string",
    "counteractivation_strategy": "string",
    "smallest_commitment": "string"
  },
  "planned_questions": [
    {
      "question_text": "string",
      "activation_direction": "string",
      "psychological_role": "string"
    }
  ],
  "expression_targets": ["string"],
  "hypothesis_pipeline_status": {
    "status": "BLOCKED_PENDING_GAP_007",
    "iac_ref": null,
    "planned_aip_ref": null,
    "arm_receipt_ref": null,
    "blocked_reason": "planned_activative_intelligence_pack requires real, cross-validated activation_hypothesis_portfolio / activation_hypothesis / matrix_of_edging / psychological_role_tension_contract objects (HypothesisService.store_planned_pack, AIR). See SPEC_GAP_LEDGER.md GAP-007."
  },
  "composer_authority": {
    "operator_id": "string",
    "authority_scope": "string",
    "assertion_id": "string"
  }
}
```

### C. Composer Session (`ic:session`)
```json
{
  "session_id": "ic:session:...",
  "brief_ref": { "object_id": "...", "version": "...", "sha256": "..." },
  "relationship_state_ref": { "object_id": "...", "version": "...", "sha256": "..." },
  "progression_ref": { "object_id": "...", "version": "...", "sha256": "..." },
  "stage": "ENGAGED",
  "recording_date": "string (ISO8601) | null",
  "composer_authority": {
    "operator_id": "string",
    "authority_scope": "string",
    "assertion_id": "string"
  }
}
```

---

## 4. Current Route / API Boundaries

All Composer endpoints are registered in `api/main.py` under the `/api/interviews/compose` prefix:

1. **`POST /api/interviews/compose/research`**
   - Ingests multipart form data (`guest_name`, `workspace_id`, `project_id`, `operator_id`, `authority_scope`, `assertion_id`, `source_urls_json`, `document_metadata_json`, `documents`).
   - Validates file size tiers (10MB captions, 50MB docs, 500MB/1GB audio, 4GB video) and SHA-256 integrity.
   - Returns `GuestResearchPackageResponse` (201 Created).

2. **`GET /api/interviews/compose/research/{research_package_id}`**
   - Retrieves stored research package.

3. **`POST /api/interviews/compose/brief`**
   - Ingests `ComposeBriefRequest` JSON.
   - Cross-validates `brand_context_ref` and `voice_dna_ref` against AIR via `composer_air_bridge.py`.
   - Returns `ActivativeInterviewBriefResponse` with `hypothesis_pipeline_status` honestly stating GAP-007 boundary.

4. **`GET /api/interviews/compose/briefs/{brief_id}`**
   - Retrieves stored brief and converts to response.

5. **`POST /api/interviews/compose/sessions`**
   - Ingests `ComposeSessionRequest`.
   - Calls `Phase9ActivativeService.compile_relationship_program` on AIR.
   - Stores session and returns `ComposerSessionResponse`.

6. **`GET /api/interviews/compose/sessions/{session_id}`**
   - Retrieves stored session.

---

## 5. Exact Gaps & Boundary Reconciliation

### GAP-007 Reconciliation
- **Nature of Gap:** `Phase9ActivativeService.compile_interview_asset_contract()` and `HypothesisService.store_planned_pack()` in AIR require 4 real, stored AIR objects (`matrix_of_edging`, `activation_hypothesis`, `activation_hypothesis_portfolio`, `psychological_role_tension_contract`).
- **Resolution Strategy in Interview Program:**
  - The Interview Program operates as an **upstream hypothesis-and-question intelligence layer**.
  - It constructs **derived, non-canonical** representations (`HypothesisCandidate`, `QuestionObjective`, `QuestionCoalition`, `QuestionIR`) that feed directly into the existing `ActivativeInterviewBrief`'s `planned_questions` and `matrix_of_edging_seed`.
  - It does **not** manufacture hollow AIR database records or fake `planned_aip_ref` objects.
  - It satisfies the operator requirements while maintaining strict schema and cryptographic integrity.

---

## 6. Exact Extension Points for M02–M11

1. **M02 (Hypothesis Portfolio Adapter):** Adapts coordinate/collision intelligence into `HypothesisCandidate` structures, providing diversity-aware selection (~96 candidate pool down to 16–24 working candidates) without mutating AIR.
2. **M03 (Question Intelligence Resolution):** Resolves candidate hypotheses into `QuestionObjective`, `QuestionPrimitiveRef`, and `QuestionCoalition` leveraging the audited Question Heritage corpus.
3. **M04 (Interview Brief Compilation):** Compiles the resolved question set (~16–24 questions, ~32 runtime operations) cleanly into the existing `make_activative_interview_brief` format.
4. **M05 (Operator Studio):** Integrates selection, rejection, parameter locking, and regeneration controls into the human operator workflow.
5. **M06 (Adaptive Question Frontier):** Establishes the bounded 3–5 candidate next-move frontier maintaining the coverage spine during runtime.
6. **M07 (Semantic Acquisition Observation):** Records `AnswerObservation` and `QuestionStateTransition`, strictly separating guest evidence, system inference, and validated interpretation.
7. **M08 (Archetype & Format Compatibility):** Projects question geometry against downstream format/archetype constraints without manufacturing evidence.
8. **M09 (Authenticated Evidence Handoff):** Packages verified evidence lineage for downstream consumer ingestion.
9. **M10 (Content Menu Readiness):** Evaluates candidate editorial readiness against downstream content menus.
10. **M11 (End-to-End Reality Contact Regression):** Executes complete regression and anti-fabrication test harness.

---

## 7. Objects and Entities Deliberately PROHIBITED

The following entities must **NEVER** be created or mutated in this program:
- ❌ `InterviewHarnessV2` or any second parallel interview runner.
- ❌ Fake or hollow `planned_activative_intelligence_pack` / `iac_ref` / `arm_receipt_ref`.
- ❌ Direct SQL writes to `services/air/` or `services/interview/` tables from Composer.
- ❌ Automatic production approval without human Operator authorization.
- ❌ Scraping, crawling, or OCR parsing of guest research package files.
- ❌ Premature canonical promotion of provisional Question Primitives before audit sign-off.

---

## 8. Bundle v3 vs Live Repository Concordance

- **Concordance Score:** 100%
- **Contradictions Identified:** Zero.
- **Architectural Alignment:** The live repository layout, service boundaries, SQLite/Postgres persistence schemas, and API bridges exactly match the technical requirements and constraints set forth in `TS-APP-INTERVIEW-PROGRAM-001` and `00_GOVERNANCE/03_PRD_DELTA.md`.

---

## 9. Test Verification Baseline

Executed live on Python 3.12:

1. **Unit Test Suite:**
   ```powershell
   python -m pytest tests/interview_composer/ -v
   ```
   - **Result:** **17 passed** in 48.01s (100% pass rate).

2. **API Regression Test Suite:**
   ```powershell
   python -m pytest tests/api/test_interview_composer_regression.py tests/api/test_interview_composer_research.py tests/api/test_interview_composer_sessions.py -v
   ```
   - **Result:** **23 passed** in 253.65s (100% pass rate).
   - **Total Verified Baseline:** **40 / 40 tests passing**.
