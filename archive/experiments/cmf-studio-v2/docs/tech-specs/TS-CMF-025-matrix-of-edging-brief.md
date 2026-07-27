---
tech_spec_id: "TS-CMF-025"
title: "Matrix of Edging Brief"
story_id: "5.3"
story_title: "Matrix of Edging Brief"
epic_id: 5
epic_title: "Interview Intelligence and Narrative State Induction"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-5-3-matrix-of-edging-brief.md"
fr_ids:
  - "FR-CMF-05.03"
  - "FR-CMF-05.07"
pipeline_stage: "3 / 4"
entry_object: "dossier and audience reality"
exit_object: "MatrixOfEdgingBrief"
validation_contract: "collision and specificity gate"
required_receipt: "Matrix receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / durable workflows / DSPy"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-025: Matrix of Edging Brief

**Status:** Ready for Development  
**Story:** `5.3 - Matrix of Edging Brief`  
**Implementation Boundary:** Matrix of Edging compiler, primitive candidate packets, coalition signatures, edge products, collision/specificity evaluation, and Matrix receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-5-3-matrix-of-edging-brief.md` | Story source and acceptance criteria. |
| `docs/epics.md` | Epic 5 story dependency and stage trace. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-05.03 and FR-CMF-05.07 authority. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Matrix of Edging eight-pass product description. |
| `THE CMF STUDIO/Matrix of Edging.md` | Core Matrix doctrine: pressure field, broad signal, primitive spaces, coalition signature, edge product. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Matrix integration with Narrative State Induction. |
| `docs/architecture.md` | Matrix compiler and interview planning objects. |
| `docs/cmf-studio-pipeline-map.md` | Research to interview-intelligence sub-workflow. |
| `docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md` | Collision, compression, specificity, and anti-generic evaluation laws. |
| `docs/migration/legacy-inventory.md` | Cognitive primitives, SDA/SFL registries, and narrative intelligence fixtures. |

## 2. Overview

Implement `MatrixOfEdgingBrief` as the controlled tension-selection object between research/context compilation and interview asset contracts. The Matrix does not create reckless extremity. It finds meaningful pressure: broad primary signals, tension sites, primitive candidates, coalition signatures, edge products, likely failure points, and route implications.

The compiler must preserve the distinction between primitive spaces and edges. Primitives are candidate generators; edges emerge from evidence, primitive activations, and weighted interactions. Generic tension language fails the gate.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-05.03 | Produce Matrix of Edging briefs with broad primary signals, tension sites, primitive candidates, coalition signatures, edge products, and likely failure points. | Matrix compiler, eight-pass output, primitive packets, coalition signatures, edge product schema. |
| FR-CMF-05.07 | Evaluate interview plans for saturation, collision strength, anti-centroid risk, specificity, and routeability before a session starts. | RSCS evaluator, Matrix quality gate, failure reasons, and Matrix receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 3 / 4 - Research into interview intelligence |
| Entry Object | dossier and audience reality |
| Exit Object | `MatrixOfEdgingBrief` |
| Validation Contract | collision and specificity gate |
| Required Receipt | Matrix receipt |

### Legacy Intelligence Mapping

- The Matrix source states: research field -> primitive spaces -> candidate survival -> coalition signature -> edge product.
- Cognitive primitives and SDA/SFL registries are migrated as typed registries and fixtures, not imported at runtime.
- RSCS laws govern saturation, collision, compression, and anti-generic evaluation.
- Matrix outputs feed Interview Asset Contracts and later route/evaluation memory.

## 4. Implementation Plan

1. Add contracts for `MatrixOfEdgingBrief`, `BroadPrimarySignal`, `TensionSite`, `PrimitiveCandidatePacket`, `CoalitionSignature`, `EdgeProduct`, `MatrixFailurePoint`, and `MatrixEvaluationReceipt`.
2. Implement `MatrixOfEdgingCompiler` with eight named passes: research, provocation, authentication, primitive, coalition, edge, routing, benchmark.
3. Add evaluator for saturation, collision strength, specificity, anti-centroid risk, routeability, and unsupported evidence.
4. Persist Matrix briefs with input artifact hashes and output receipt.
5. Make Matrix outputs required inputs for contract compilation when a content-intended interview deck is generated.
6. Attach failure points and route implications to pre-induction review.

## 5. Primary Output Schema

```python
from enum import Enum
from pydantic import BaseModel, Field


class MatrixPass(str, Enum):
    RESEARCH = "research"
    PROVOCATION = "provocation"
    AUTHENTICATION = "authentication"
    PRIMITIVE = "primitive"
    COALITION = "coalition"
    EDGE = "edge"
    ROUTING = "routing"
    BENCHMARK = "benchmark"


class TensionSite(BaseModel):
    tension_site_id: str
    statement: str
    evidence_ids: list[str] = Field(min_length=1)
    collision_type: str
    magnitude_score: float = Field(ge=0, le=1)
    speculative: bool = False


class PrimitiveCandidatePacket(BaseModel):
    primitive_candidate_id: str
    primitive_family: str
    primitive_ref: str
    evidence_ids: list[str]
    survival_rationale: str
    weakness: str | None = None


class CoalitionSignature(BaseModel):
    coalition_signature_id: str
    primitive_candidate_ids: list[str] = Field(min_length=2)
    interaction_rationale: str
    route_implications: list[str]


class EdgeProduct(BaseModel):
    edge_product_id: str
    name: str
    tension_site_ids: list[str]
    coalition_signature_id: str
    anti_centroid_pressure: str
    expected_expression_state: list[str]


class MatrixOfEdgingBrief(BaseModel):
    matrix_brief_id: str
    brand_id: str
    guest_dossier_id: str
    audience_reality_brief_id: str
    context_premise_id: str
    broad_primary_signals: list[str]
    tension_sites: list[TensionSite]
    primitive_candidates: list[PrimitiveCandidatePacket]
    coalition_signatures: list[CoalitionSignature]
    edge_products: list[EdgeProduct]
    likely_failure_points: list[str]
    route_implications: list[str]
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `CompileMatrixOfEdgingBriefCommand`, `EvaluateMatrixCollisionCommand`, `RejectGenericMatrixBriefCommand`, `ApproveMatrixBriefCommand`, `RecordMatrixBenchmarkCommand` |
| Events | `MatrixBriefCompiled`, `MatrixBriefEvaluated`, `MatrixBriefRejected`, `MatrixBriefApproved`, `MatrixBenchmarkRecorded` |
| Workflow | `InterviewPreparationWorkflow.stage3_4_compile_matrix` |
| Receipt | `MatrixReceipt` with input context IDs, pass outputs, evaluator scores, failure points, and reviewer state |

Matrix outputs must be immutable after approval. Changes create a new Matrix brief version linked to the same research snapshot or a newer one.

## 7. Backward Compatibility and Migration Fallback

Legacy Matrix and primitive material becomes fixture, registry, and evaluation source. If a primitive family has not yet been migrated, the compiler can mark a primitive candidate as `unresolved_registry_ref`, but that candidate cannot become an approved route anchor until registry validation exists.

If the Matrix brief is too generic, the workflow returns to evidence/context saturation rather than drafting around weak pressure.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Provocation vs. manipulation | Matrix creates pressure selection, not scripted coercion. | Pre-induction shows edge rationale and avoid-list. |
| Primitive candidates vs. edge products | Schema separates primitive candidate packets from emergent edge products. | Contract compiler references edge product ID plus primitive packet IDs. |
| Useful tension vs. generic hook | RSCS gate rejects weak specificity and generic tension. | Matrix receipt includes saturation/collision/specificity scores. |

## 9. Tasks

- Add Matrix contracts and persistence models.
- Implement `MatrixOfEdgingCompiler` DSPy module with explicit pass outputs.
- Add RSCS evaluator for saturation, collision, compression specificity, and anti-genericity.
- Add command handlers and review endpoints.
- Add Matrix receipt writer and immutable versioning.
- Add fixtures from Matrix source and cognitive primitive inventory.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Compiler emits all eight Matrix pass outputs. | Brief only contains a list of hooks. |
| AC2 | Unsupported tension sites are speculative and cannot anchor questions. | A question is anchored to a tension site with no evidence. |
| AC3 | Likely failure points show how to avoid centroid answers. | Operator review lacks any anti-centroid warning. |
| AC4 | Primitive candidates remain traceable to the brief. | Route compiler receives primitive labels without candidate IDs. |
| AC5 | Generic Matrix output fails RSCS specificity. | Brief could be produced without guest/audience evidence. |

## 11. Dependencies

- TS-CMF-023 Research Fields and Evidence Capture.
- TS-CMF-024 Guest Dossier, Audience Reality, Context Premise, and Resonance.
- TS-CMF-014 registry conversion and evals.
- TS-CMF-015 JIT skill compiler saturation and contrast.
- TS-CMF-017 intentional orchestration migration contracts.

## 12. Testing Strategy


Unit tests:

- Unit tests for Matrix schema and pass completeness.
- DSPy tests requiring all passes to produce typed outputs.
- RSCS evaluator tests against generic, unsupported, and high-specificity examples.
- Workflow tests proving approved Matrix IDs feed Interview Asset Contract compilation.
- Regression fixtures from Matrix of Edging source and primitive registry examples.
- Permission tests for brand-scoped Matrix read/write access.

Integration tests:

- Workflow test from `dossier and audience reality` to `MatrixOfEdgingBrief` through pipeline stage `3 / 4`.
- Command Bus test proving `Matrix receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Emit compiler/evaluator metrics for collision score, specificity score, routeability score, and rejection reasons.
- Log every Matrix version with input hashes and approved reviewer.
- Recovery: regenerate from a richer context snapshot or manually revise rejected pass output.
- Rollback: supersede Matrix version and invalidate dependent draft contracts, preserving prior receipt lineage.

## Doctrine-Driven Test Harness Binding

This spec must be verified through TS-CMF-077 before implementation is considered complete. The test plan for this spec must identify the documented doctrine sources it depends on, the operational invariants those sources imply, the primitive or eval obligations that apply to its outputs, and the negative fixtures that prove forbidden shortcuts are blocked. Passing tests must emit or validate the required receipt chain, and any hard failure must map to an approval blocker when this spec touches review, rendering, publishing, memory, agents, adapters, or operator actions.

Minimum binding requirements:

- cite source doctrine or registry refs used by this spec;
- declare contract, workflow, receipt, and read-model invariants;
- include at least one negative or drift fixture for every forbidden shortcut named in the spec;
- prove required receipts are emitted, immutable, reconstructable, and linked to pipeline stage state;
- expose failed doctrine, primitive, or eval obligations as blocker-ready test output.

## 14. Spec Audit Receipt

| Field | Value |
|---|---|
| Tech Spec ID | TS-CMF-025 |
| Story | 5.3 |
| Requirement Trace | FR-CMF-05.03, FR-CMF-05.07 |
| Pipeline Trace | Stages 3 / 4, dossier/audience reality to MatrixOfEdgingBrief |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No generic hooks, no primitive/edge collapse, no legacy runtime coupling, no manipulation framing |

