# CAE M29 Execution Report: Research Knowledge Extraction + Canonicalization + OKF

**Status:** COMPLETE — OPERATOR-RATIFICATION-REQUESTED  
**Date:** 2026-08-31  
**Commit SHA:** `e5cd35ed6448f8454aa3a4a1d20e75563723ecb8`  
**Governing Mandate:** `M29_research_knowledge_extraction_canonicalization_okf.md`  
**PRD Section:** `docs/PRD/CURRENT.md` (§1.4 Tenancy & App Layer)

---

## 1. Executive Summary

CAE Phase 3 Mandate M29 establishes the **Research Knowledge Extraction + Canonicalization + OKF Program** (`research_canonicalization_program` v1.0.0) as an operator-addressable, multi-agent reasoning Program package and state machine runtime.

The implementation reconciles the live research knowledge authority (`20_PHASE3_CANONICALIZATION_MODEL.md`, `21_PHASE3_KNOWLEDGE_RUNTIME_CONTRACT.md`, `22_PHASE3_RESEARCH_RETRIEVAL_MATRIX.md`, `24_PHASE3_PROGRAM_STATE_HOOKS_MATRIX.md`) with the universal program state machine engine (`program_state_runtime.py`, `state_lifecycle.py`), resolving and strictly enforcing:
1. **Semantic Transformation Chain:** Raw Research Sources $\rightarrow$ Extraction (`HUNTER`) $\rightarrow$ Knowledge Candidates $\rightarrow$ Relationship Classification & Canonicalization (`ANALYST`) $\rightarrow$ Canonical Knowledge Nodes $\rightarrow$ OKF Markdown Bundle Projection (`COMPOSER`) $\rightarrow$ Operator Adjudication & Knowledge Commitment (`COMMANDER`).
2. **Protected Evidence Immutability & Provenance:** Raw research sources (`ResearchSourceRecord`, `RawObservation`) are immutable protected records with SHA-256 payload digests and URI origins. Canonical nodes maintain cryptographic lineage hashes (`source_evidence_hashes`, `source_record_refs`). Attempting to mutate raw sources raises `SourceImmutabilityViolationError` fail-closed.
3. **Anti-False-Merge Validation:** Homonyms and distinct entities with identical or similar terminology (e.g. "Gemini AI" vs "Project Gemini NASA") are preserved as distinct canonical nodes (`DISTINCT`), preventing destructive or false-merge corruptions.
4. **Contradiction Detection & Commander Adjudication Gate:** Opposing assertions between candidates generate explicit `CONTRADICTORY` relationship edges. Committing knowledge with unadjudicated contradictions fails closed (`ContradictionAdjudicationRequiredError`) unless explicitly adjudicated by a Commander operator decision.
5. **Node Retraction & Re-expression Versioning:** Outdated or refuted canonical nodes are retracted (`lifecycle_status="retracted"`), and updated definitions instantiate re-expressed versioned nodes (e.g., `_v2`) referencing `supersedes_node_id` with continuous audit trail.
6. **Open Knowledge Format (OKF) Bundle Generation:** Exports compliant `cmf-okf-research-knowledge-1.0` bundles with YAML frontmatter, `index.md`, `concepts/`, `entities/`, and composite SHA-256 bundle hashes.
7. **Four Authority Lanes Preservation:** Strict lane separation: `HUNTER` for extraction, `ANALYST` for relationship classification, `COMPOSER` for OKF projection, and `COMMANDER` for attachment, adjudication, commitment, retraction, and repair.

---

## 2. Baseline Authority Read Set & Evidence

### Read Set Reported
1. `docs/cae/CAE_Phase3_Production_Mandate_Bundle_v2/00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`
2. `docs/cae/CAE_Phase3_Production_Mandate_Bundle_v2/00_CONTROL/08_INITIAL_PROGRAM_INVENTORY.md`
3. `docs/cae/CAE_Phase3_Production_Mandate_Bundle_v2/00_CONTROL/20_PHASE3_CANONICALIZATION_MODEL.md`
4. `docs/cae/CAE_Phase3_Production_Mandate_Bundle_v2/00_CONTROL/21_PHASE3_KNOWLEDGE_RUNTIME_CONTRACT.md`
5. `docs/cae/CAE_Phase3_Production_Mandate_Bundle_v2/00_CONTROL/22_PHASE3_RESEARCH_RETRIEVAL_MATRIX.md`
6. `docs/cae/CAE_Phase3_Production_Mandate_Bundle_v2/00_CONTROL/24_PHASE3_PROGRAM_STATE_HOOKS_MATRIX.md`
7. `docs/cae/CAE_Phase3_Production_Mandate_Bundle_v2/00_CONTROL/26_PHASE3_EXTERNAL_REFERENCE_READS.md`
8. `docs/cae/CAE_Phase3_Production_Mandate_Bundle_v2/03_PHASE_3_INTELLIGENCE_AND_PROGRAMS/M28_research_source_ingestion_identity.md`
9. `docs/cae/CAE_Phase3_Production_Mandate_Bundle_v2/03_PHASE_3_INTELLIGENCE_AND_PROGRAMS/M29_research_knowledge_extraction_canonicalization_okf.md`
10. `docs/cae/CAE_Phase3_Production_Mandate_Bundle_v2/03_PHASE_3_INTELLIGENCE_AND_PROGRAMS/M29_GEMINI_ACTIVATION.md`
11. `services/vae/contracts/schemas/okf_projection.schema.json`
12. `services/vae/prd/05-features/F17-steering-intelligence-cmf-okf-retrieval.md`
13. `services/vae/knowledge/cmf-okf-profile/README.md`
14. `services/vae/knowledge/cmf-okf-profile/index.md`
15. `services/vae/knowledge/cmf-okf-profile/character-visible-action.md`
16. `docs/PRD/CURRENT.md`
17. `packages/ca_runtime/src/ca_runtime/workspace_core.py`
18. `packages/ca_runtime/src/ca_runtime/workspace_guest_program.py`
19. `packages/ca_runtime/src/ca_runtime/program_registry.py`
20. `packages/ca_runtime/src/ca_runtime/program_state_runtime.py`
21. `packages/ca_runtime/src/ca_runtime/state_lifecycle.py`
22. `packages/ca_runtime/src/ca_runtime/tenancy.py`
23. `packages/ca_runtime/src/ca_runtime/agent_team.py`
24. `packages/ca_runtime/src/ca_runtime/hook_runtime.py`
25. `tests/cae/test_workspace_guest_program.py`

---

## 3. Implementation Details

### 3.1 State Machine Grammar (`RESEARCH_CANONICALIZATION_STATE_MACHINE_V1`)
- **Initial State:** `INITIAL`
- **Terminal State:** `KNOWLEDGE_COMMITTED`
- **Transitions:**
  1. `attach_sources` (`INITIAL` $\rightarrow$ `SOURCES_ATTACHED`): Lane `COMMANDER`, trigger `cae.research.attach_sources@1.0.0`, preconditions `("workspace_active", "operator_authorized")`, side effect `LOCAL_STATE_WRITE`.
  2. `extract_candidates` (`SOURCES_ATTACHED` $\rightarrow$ `CANDIDATES_EXTRACTED`): Lane `HUNTER`, trigger `cae.research.extract_candidates@1.0.0`, preconditions `("workspace_active", "sources_attached", "lane_hunter")`, side effect `LOCAL_STATE_WRITE`.
  3. `canonicalize_candidates` (`CANDIDATES_EXTRACTED` $\rightarrow$ `CANONICALIZED`): Lane `ANALYST`, trigger `cae.research.canonicalize@1.0.0`, preconditions `("workspace_active", "candidates_extracted", "lane_analyst")`, side effect `LOCAL_STATE_WRITE`.
  4. `project_okf_bundle` (`CANONICALIZED` $\rightarrow$ `OKF_PROJECTED`): Lane `COMPOSER`, trigger `cae.research.project_okf@1.0.0`, preconditions `("workspace_active", "nodes_canonicalized", "lane_composer")`, side effect `LOCAL_STATE_WRITE`.
  5. `commit_canonical_knowledge` (`OKF_PROJECTED` $\rightarrow$ `KNOWLEDGE_COMMITTED`): Lane `COMMANDER`, trigger `cae.research.commit_knowledge@1.0.0`, preconditions `("workspace_active", "okf_bundle_projected", "contradictions_adjudicated")`, side effect `TRANSACTIONAL_COMMIT`.
  6. `repair_canonicalization` (`REPAIRING` $\rightarrow$ `SOURCES_ATTACHED`): Lane `COMMANDER`, trigger `cae.research.repair@1.0.0`, preconditions `("workspace_active", "operator_authorized")`, side effect `TRANSACTIONAL_COMMIT`.

### 3.2 Program Package Files
- `programs/research_canonicalization_program/program_manifest.yaml`
- `programs/research_canonicalization_program/CAE.md`
- `programs/research_canonicalization_program/instructions.md`
- `programs/research_canonicalization_program/skills/knowledge_candidate_extractor/SKILL.md`
- `programs/research_canonicalization_program/skills/canonical_relationship_classifier/SKILL.md`
- `programs/research_canonicalization_program/skills/okf_bundle_projector/SKILL.md`

### 3.3 Core Runtime Modules
- `packages/ca_runtime/src/ca_runtime/research_canonicalization_program.py`: `ResearchCanonicalizationProgramCoordinator`, `KnowledgeCandidate`, `CanonicalRelationship`, `CanonicalKnowledgeNode`, `OKFDocument`, `OKFKnowledgeBundle`, `AdjudicationDecision`, `ResearchCanonicalizationSnapshot`, and fail-closed exception taxonomy (`ResearchCanonicalizationProgramError`, `FalseMergeViolationError`, `ContradictionAdjudicationRequiredError`, `SourceProvenanceMissingError`, `NodeRetractedError`, `OKFValidationError`, `SourceImmutabilityViolationError`, `WorkspaceScopeViolationError`).
- `packages/ca_runtime/src/ca_runtime/program_state_runtime.py`: Added `get_canonical_research_canonicalization_state_machine()` and registered in `UniversalProgramStateRuntime.__init__`.
- `packages/ca_runtime/src/ca_runtime/__init__.py`: Exported all new coordinator classes, domain models, error types, and state machine getters.

---

## 4. Verification Evidence

### 4.1 Test Commands & Results
- **Dedicated Suite:**
  ```bash
  python -m pytest tests/cae/test_research_canonicalization_program.py -v
  ```
  Result: **10 passed in 1.96s**
  - `test_program_package_discovery_and_manifest` (PASSED)
  - `test_state_machine_grammar_and_transitions` (PASSED)
  - `test_full_canonicalization_lifecycle_e2e` (PASSED)
  - `test_controlled_corpus_alias_and_duplicate_resolution` (PASSED)
  - `test_false_merge_rejection_homonyms` (PASSED)
  - `test_contradiction_detection_and_commander_adjudication` (PASSED)
  - `test_okf_bundle_generation_and_export` (PASSED)
  - `test_source_provenance_immutability_and_lineage` (PASSED)
  - `test_node_retraction_and_reexpression_lifecycle` (PASSED)
  - `test_cross_workspace_and_authority_lane_denial` (PASSED)

- **Complete CAE Suite:**
  ```bash
  python -m pytest tests/cae -v
  ```
  Result: **206 passed in 90.96s (0 regressions across all suites)**

---

## 5. Non-Negotiable Compliance Matrix

| Rule | Status | Verification Detail |
|---|---|---|
| CAE remains authoritative | COMPLIANT | All state and mutations are governed by CAE state machine and typed operations. |
| Four Authority Lanes preserved | COMPLIANT | Strict lane checks (`COMMANDER`, `HUNTER`, `ANALYST`, `COMPOSER`) enforced at every transition. |
| Passive flat skills | COMPLIANT | 3 flat skills added without nesting or skill-to-skill calls. |
| Protected evidence immutability | COMPLIANT | Raw sources indexed with SHA-256; mutations rejected with `SourceImmutabilityViolationError`. |
| Anti-False-Merge Validation | COMPLIANT | Homonyms kept as distinct canonical nodes; false merges rejected. |
| Contradiction Adjudication | COMPLIANT | Unadjudicated contradictions block commitment (`ContradictionAdjudicationRequiredError`). |
| Node Retraction & Lineage | COMPLIANT | Retractions mark status; re-expression creates versioned nodes with `supersedes_node_id`. |
| OKF Curated Representation | COMPLIANT | Markdown + YAML frontmatter bundles with composite SHA-256 digests. Supabase/Postgres remains operational authority. |
| Deterministic receipts | COMPLIANT | Every transition emits a cryptographically verified transition receipt and causal trace. |

---

## 6. PRD Update & Operator Decision Request

`docs/PRD/CURRENT.md` (§1.4 Tenancy & App Layer) has been updated and dated `2026-08-31`.

**Operator Action Requested:**
Review and ratify the M29 execution report and evidence.
