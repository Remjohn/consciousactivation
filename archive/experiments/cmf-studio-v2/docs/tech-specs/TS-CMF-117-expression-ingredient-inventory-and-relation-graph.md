---
tech_spec_id: "TS-CMF-117"
title: "Expression Ingredient Inventory and Relation Graph"
story_id: "12.4"
story_title: "Expression Ingredient Inventory"
epic_id: 12
epic_title: "Conscious Sequencing and Expression Acquisition"
status: "ready-for-development"
created_at: "2026-06-25"
source_story: "CCP Conscious Sequencing and Expression Acquisition Engine V1 bundle"
pipeline_stage: "7 / 8 / 9"
entry_object: "Closed Complete Expression Session, aligned transcript, recording artifacts, approved Expression Moments, InterviewBriefV2, LiveIngredientCoverageState"
exit_object: "ExpressionIngredientInventory, IngredientRelation graph, IngredientGap list, pickup plan, inventory freeze receipt"
validation_contract: "source segment integrity, ingredient quality scoring, relation graph validity, primitive tagging, approval status, gap planning"
required_receipt: "ExpressionIngredientInventoryFreezeReceipt"
runtime_target: "Python / Pydantic v2 / DSPy extraction / source alignment / review workbench"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-117: Expression Ingredient Inventory and Relation Graph

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory CMF/ERA3 spec protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Phase 4 CBAR mandates for source integrity and actionable rejection. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Phase 5 CBAR mandates for verifiable artifacts. |
| `THE CMF STUDIO/docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md` | Phase 4 adversarial audit trail. |
| `THE CMF STUDIO/docs/architecture/cbar_audits/CBAR_Audit_Phase5_Growth.md` | Phase 5 adversarial audit trail. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_12_Conscious_Sequencing_Expression_Acquisition.md` | Product owner for FR-CMF-12.04. |
| `THE CMF STUDIO/CCP_CONSCIOUS_SEQUENCING_AND_EXPRESSION_ACQUISITION_ENGINE_V1_BUNDLE/ccp_conscious_sequence_engine_v1/01_MASTER_SPEC.md` | Ingredient classes, quality dimensions, relation types, and inventory role. |
| `.../02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Inventory state machine, invariants, and events. |
| `.../03_RUNTIME_WORKFLOWS.md` | Post-session extraction and relation compilation workflow. |
| `.../05_EVALUATION_GOVERNANCE_AND_LEARNING.md` | Inventory gates and hard failures. |
| `.../models/sequence_engine_models.py` | `SourceSegment`, `ExpressionIngredient`, `IngredientQualityScores`, `IngredientRelation`, `IngredientGap`, `ExpressionIngredientInventory`. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-031-anchor-hit-and-expression-moment-candidate-detection.md` | Upstream Expression Moment candidate dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-032-expression-moment-review-and-boundary-control.md` | Source boundary and approval dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-033-archetype-and-asset-derivative-routing.md` | Route compatibility dependency. |
| `src/ccp_studio/services/expression_session_service.py` | Session artifact and state source. |

## 2. Overview

This spec creates the post-session ingredient inventory that sequence compilers can actually trust. Instead of treating the transcript as raw material forever, CMF extracts approved expression ingredients with source segments, quality scores, primitive tags, edge products, archetype compatibility, asset compatibility, relation edges, and gap recommendations.

The inventory is the pantry between interview and content sequence. Only approved ingredients can be used as human-expression material in a final `ContentSequenceProgram`.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-117-001 | `SourceSegment` | Speaker, recording artifact, transcript text, start/end tick, and source hash. |
| DEP-CMF-117-002 | `IngredientQualityScores` | Ten bounded quality scores for each ingredient. |
| DEP-CMF-117-003 | `ExpressionIngredient` | Source-grounded approved or rejected expression ingredient. |
| DEP-CMF-117-004 | `IngredientRelation` | Directed relation between two inventory ingredients. |
| DEP-CMF-117-005 | `IngredientGap` | Missing, weak, source, visual, or research gap requiring action. |
| DEP-CMF-117-006 | `ExpressionIngredientInventory` | Frozen inventory snapshot for sequence compilation. |
| DEP-CMF-117-007 | `ExpressionIngredientInventoryFreezeReceipt` | Receipt proving inventory freeze and source integrity. |
| DEP-CMF-117-008 | `IngredientGraphReadModel` | Projected graph view derived from frozen inventory and relation rows. |

### Existing Backend Integration

| Python Owner | Database Table(s) | API Route(s) | Migration / Backfill Behavior |
|---|---|---|---|
| `src/ccp_studio/services/expression_ingredient_inventory_service.py` | `expression_ingredient_inventories`, `expression_ingredients`, `ingredient_gaps` | `POST /api/cmf/expression-sessions/{id}/ingredient-inventory/extract`, `POST /api/cmf/ingredient-inventories/{id}/freeze` | New inventory tables keyed by expression session and brief. |
| `src/ccp_studio/services/ingredient_relation_graph_service.py` | `ingredient_relations`, `ingredient_graph_read_models` | `POST /api/cmf/ingredient-inventories/{id}/relations/compile`, `GET /api/cmf/ingredient-inventories/{id}/graph` | Stores relation edges in Postgres; optional Neo4j projection is read-only and rebuildable. |
| `src/ccp_studio/services/expression_moment_service.py` | `expression_moments`, `expression_moment_reviews` | existing review routes | Inventory extraction reads only approved moments or flagged candidates for review. |
| `src/ccp_studio/services/evaluation_receipt_service.py` | `receipt_chain`, `evaluation_receipts`, `approval_blockers` | shared receipt writer | Writes inventory freeze receipt and source-integrity blockers. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-PER-003` | Phase4-M01 | Ingredient approval requires source segment and reviewer-visible evidence. |
| `EXP-FBK-001` | Phase4-M05 | Rejected ingredients name exact quote, speaker, timestamp, and repair reason. |
| `EXP-SOC-001` | Phase5-M01 | Frozen inventory and graph projections are verifiable artifacts. |
| `EXP-TRS-004` | Phase4-M02 | Ingredient roles preserve story meaning and cannot flatten emotional truth. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M01: Intelligence-Gated Intercept Rule | Phase 4 Story 1.1 | `EXP-PER-003` | Ingredient approval is blocked without source segment and source-alignment evidence. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Inventory failures identify exact quote, timestamp, role, and repair action. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Frozen inventory, graph edges, and gaps are hash-backed receipt-chain artifacts. |

### Receipt Chain Guard

| Receipt | Table | Action | Idempotency Key | Required Hashes |
|---|---|---|---|---|
| `ExpressionIngredientInventoryFreezeReceipt` | `receipt_chain` | `expression_ingredient_inventory.frozen` | `ingredient_inventory_id + inventory_sha256` | inventory hash, source alignment hashes, expression moment receipt hashes |

### Ingredient Classes

| Class | Meaning |
|---|---|
| `human_expression` | Guest or interviewer expression captured in source session. |
| `research_evidence` | Approved external evidence, CRAL finding, audience evidence, or source citation. |
| `audience_reality` | Context Premise, comments, objections, recognition signals, or audience language. |
| `visual` | Approved visual asset, memory object, scene plate, proof object, or non-human contextual asset. |
| `brand_continuity` | Brand memory, signature worldview, micro-semiotic anchor, voice/visual DNA evidence. |

### Quality Dimensions

```text
specificity
emotional_density
truth_density
audience_relevance
clipability
explanatory_completeness
evidence_strength
visual_routeability
source_integrity
brand_fit
```

### Relation Types

```text
opens_question
adds_stake
provides_clue
complicates
contradicts
reframes
answers
provides_proof
humanizes
creates_future_value
transitions
```

### Hard Failures

| Failure | Consequence |
|---|---|
| Unclear speaker | Ingredient rejected. |
| Missing timestamp | Ingredient rejected. |
| Synthetic text presented as guest speech | Inventory freeze blocked. |
| Distorted quotation | Ingredient rejected and repair required. |
| Raw unresolved trauma routed without safety approval | Inventory freeze blocked. |
| Source-integrity failure | Ingredient cannot become available for compilation. |

### Graph Ownership and Reconciliation

The relation graph is persisted in Postgres tables `ingredient_relations` and `ingredient_graph_read_models`. Neo4j projection is allowed only as a rebuildable read model for exploration and query performance. The frozen inventory remains the canonical source of truth.

When an inventory revision supersedes a prior snapshot:

1. a new `ExpressionIngredientInventory` version is created;
2. relation edges are recomputed for the new inventory hash;
3. the prior graph read model remains immutable but is marked `superseded`;
4. Neo4j projection jobs delete and rebuild projection nodes by `ingredient_inventory_id + inventory_sha256`.

### Gate Verdict Semantics

| Verdict | Rule | Receipt Behavior |
|---|---|---|
| `PASS` | Ingredient or inventory meets source and quality gates. | Write evaluation receipt and allow review/freeze. |
| `PROVISIONAL` | Ingredient has usable signal but needs human review or pickup. | Keep as candidate; do not allow sequence compilation. |
| `FAIL` | Source integrity, quote fidelity, or quality gate fails. | Write blocker with exact quote/timestamp. |
| `BLOCKED` | Synthetic guest claim, missing speaker, missing timestamp, or unsafe trauma route. | Stop inventory freeze. |

## 4. Implementation Plan

1. Add `src/ccp_studio/services/expression_ingredient_inventory_service.py`.
2. Add DSPy programs: `ExpressionIngredientExtractor`, `IngredientRoleClassifier`, `IngredientQualityEvaluator`, `IngredientRelationCompiler`, and `GapAndPickupPlanner`.
3. Bind extraction to aligned transcript, speaker diarization, recording artifact IDs, source ticks, and approved Expression Moments.
4. Classify ingredients using the active Expression Ingredient Registry.
5. Score all quality dimensions and produce hard-failure blockers.
6. Compile relation graph across approved and provisional ingredients.
7. Detect missing, weak, source-integrity, visual, and research gaps.
8. Add human review statuses: extracted, auto_evaluated, human_reviewed, approved, rejected, needs_repair.
9. Freeze inventory only after hard gates pass and operator approval is recorded.
10. Export approved ingredients to `ContentSequenceProgramCompiler`.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class ExpressionIngredientInventoryFreezeReceipt(BaseModel):
    schema_version: Literal["cmf.expression_ingredient_inventory_freeze_receipt.v1"]
    receipt_id: str
    ingredient_inventory_id: str
    expression_session_id: str
    interview_brief_id: str
    approved_ingredient_ids: list[str]
    rejected_ingredient_ids: list[str]
    gap_count: int
    unexpected_high_value_ingredient_ids: list[str] = Field(default_factory=list)
    inventory_sha256: str
    source_alignment_receipt_refs: list[str]
    expression_moment_receipt_refs: list[str]
    blocker_codes: list[str] = Field(default_factory=list)
    operator_status: Literal["approved", "needs_revision", "rejected"]


class IngredientGraphReadModel(BaseModel):
    schema_version: Literal["cmf.ingredient_graph_read_model.v1"]
    ingredient_inventory_id: str
    nodes: list[dict]
    edges: list[dict]
    gap_nodes: list[dict]
    strongest_sequence_candidates: list[str]
```

The canonical inventory must preserve the bundle fields for `SourceSegment`, `IngredientQualityScores`, `ExpressionIngredient`, `IngredientRelation`, `IngredientGap`, and `ExpressionIngredientInventory`.

## 6. Workflow

```text
session_closed
-> align_transcript_and_media
-> load_approved_expression_moments
-> extract_candidate_ingredients
-> classify_roles_and_classes
-> score_quality_dimensions
-> attach_primitives_edges_archetype_asset_compatibility
-> compile_relation_graph
-> detect_gaps_and_pickups
-> operator_review
-> freeze_inventory
```

Ingredient state:

```text
extracted
-> auto_evaluated
-> human_reviewed
-> approved
```

Alternate states:

```text
rejected
needs_repair
repaired
reviewed
```

## 7. API, Service, and Event Contracts

| Contract | Shape |
|---|---|
| `POST /api/cmf/expression-sessions/{id}/ingredient-inventory/extract` | Creates inventory draft. |
| `POST /api/cmf/ingredient-inventories/{id}/evaluate` | Runs quality and source gates. |
| `POST /api/cmf/ingredient-inventories/{id}/relations/compile` | Builds relation graph. |
| `POST /api/cmf/ingredient-inventories/{id}/review` | Operator approves/rejects/repairs ingredients. |
| `POST /api/cmf/ingredient-inventories/{id}/freeze` | Freezes inventory and emits receipt. |
| `GET /api/cmf/ingredient-inventories/{id}/graph` | Returns graph read model. |

Events:

```text
ExpressionIngredientExtracted
ExpressionIngredientAutoEvaluated
ExpressionIngredientApproved
IngredientRelationCompiled
IngredientGapDetected
PickupRequested
ExpressionIngredientInventoryFrozen
```

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | Mandate / Test Evidence |
|---|---|---|---|
| AC1 | A human-expression ingredient cannot exist without speaker, source segment, recording artifact, transcript text, and hash. | A quote is approved with transcript text but no speaker or timestamp. | Phase4-M01, `EXP-PER-003`; source integrity test. |
| AC2 | External and visual ingredients require approved external source refs or asset refs. | A research claim is stored as evidence with no CRAL or source reference. | Phase5-M01, `EXP-SOC-001`; evidence ref test. |
| AC3 | Inventory freeze is blocked by unclear speaker, missing timestamp, distorted quote, synthetic guest claim, or source-integrity failure. | A synthetic paraphrase is presented as guest speech and inventory still freezes. | Phase4-M05, `EXP-FBK-001`; hard-failure test. |
| AC4 | Relation graph only references ingredients in the same inventory snapshot. | A graph edge points from the current inventory to a superseded ingredient ID. | Phase5-M01, `EXP-SOC-001`; graph reconciliation test. |
| AC5 | Gap recommendations must be pickup, research, visual_request, substitute, waive, or abandon_sequence. | A missing role creates a vague "fix later" gap with no action type. | Phase4-M05, `EXP-FBK-001`; gap enum test. |
| AC6 | Approved ingredients are immutable after inventory freeze. | An operator edits source text inside a frozen ingredient row. | Phase5-M01, `EXP-SOC-001`; immutability test. |

## 9. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Source integrity tests | Missing speaker/timestamps/hash blocks approval. |
| Synthetic claim negative tests | Synthetic text cannot become guest speech. |
| Quality scoring tests | All ten dimensions are present and bounded 0..1. |
| Relation graph tests | Invalid ingredient IDs and cycles with no semantic relation are blocked. |
| Gap tests | Missing mandatory roles create pickup or abandon recommendations. |
| Freeze tests | Frozen inventory cannot mutate; revision creates new version. |

## 10. Doctrine-Driven Test Harness Binding

The harness must evaluate:

```text
ingredient_source_integrity
quote_fidelity
primitive_tag_validity
edge_product_traceability
audience_relevance_source_support
brand_fit_and_voice_dna
trauma_safety_route_check
```

Hard failures block inventory freeze.

## Spec Audit Receipt

| Check | Status |
|---|---|
| Uses approved source evidence instead of raw prompt interpretation | Pass |
| Preserves Expression Moment review and boundary control | Pass |
| Creates graph-ready ingredients for sequence compilation | Pass |
| Blocks fabricated or distorted guest meaning | Pass |
| Emits frozen inventory receipt before downstream compilation | Pass |
