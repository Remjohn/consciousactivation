---
tech_spec_id: "TS-CMF-132"
title: "Canonical Stage Artifacts, Human Approval, and Reviewer Protocol"
story_id: "13.13"
story_title: "Canonical Stage Artifacts, Human Approval, and Reviewer Protocol"
epic_id: 13
epic_title: "OpenMontage-Inspired Production Orchestration Adapters"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-13.13"
pipeline_stage: "stage artifact validation, review, and approval"
entry_object: "StageArtifactReviewRequest"
exit_object: "StageArtifactApprovalReceipt"
validation_contract: "artifact schema, receipt links, reviewer finding severity, human approval policy, waiver, replayability"
required_receipt: "StageArtifactApprovalReceipt"
runtime_target: "Python / Pydantic v2 / review workflow / approval gate / evaluation receipts / Operations Board"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-132: Canonical Stage Artifacts, Human Approval, and Reviewer Protocol

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory spec protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Review, rejection, and routing mandates. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Verifiable artifact mandate. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` | Product owner for FR-CMF-13.13. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/00_AGENT_START_HERE.md` | CMF-local Python/DSPy/Pi runtime boundary and repository ownership rule. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Canonical object spine and state-machine constraints for pipeline artifacts. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Interview-first expression capture, narrative induction, and extraction constraints. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Expression Moment, archetype routing, route candidate, and package-routing constraints. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis, guest workspace, micro-semiotic, and initial asset package requirements. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Creative pipeline, scene program, composition handoff, and render-stage requirements. |
| `THE CMF STUDIO/PROJECT_STRUCTURE.md` | Ensures all adapters write inside the CMF project folder, not the legacy reference repo. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-012-consent-and-source-review-surface.md` | Review surface precedent. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-040-revision-and-reconstruction-audit.md` | Revision/audit dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-092-composition-eval-fixtures-and-operator-approval-workbench.md` | Approval workbench dependency. |
| `THE CMF STUDIO/src/ccp_studio/services/review_decision_service.py` | Existing review decision owner. |
| `THE CMF STUDIO/src/ccp_studio/services/review_state_service.py` | Existing review state owner. |
| `THE CMF STUDIO/src/ccp_studio/services/approval_gate_service.py` | Existing approval blocker owner. |
| `THE CMF STUDIO/src/ccp_studio/services/evaluation_receipt_service.py` | Evaluation receipt owner. |
| `THE CMF STUDIO/src/ccp_studio/workflows/review_workflow.py` | Existing review workflow owner. |
| `OpenMontage AGENT_GUIDE.md` | Reference pattern for reviewer stage and human approval policy. |

## 2. Overview

Every CMF production stage must produce canonical artifacts that can be validated, reviewed, approved, repaired, and replayed. OpenMontage's schema-validated artifacts and reviewer protocol are useful, but CMF needs stricter doctrine-aware review and human approval boundaries.

Canonical stage artifacts include `ResearchBrief`, `InterviewBriefV2`, `ExpressionIngredientInventory`, `ContentSequenceProgram`, `SceneSpec`, `AssetManifest`, `EditDecisionList`, `CompositionRuntimeBinding`, `ProviderJobReport`, `RenderReport`, `EvaluationReceipt`, `ApprovalPacket`, and `PublishingIntent`. A stage cannot complete unless its artifact validates against Pydantic/JSON Schema, links required receipts, and records review outcome.

Reviewer logic is doctrine-aware. Critical findings block. Suggestions become warnings. Repeated repair loops escalate to operator decision. Human approval policy is declared per stage and visible before execution. Creative stages pause for approval; mechanical stages may continue only when prior approvals and gates are satisfied. Models and agents may recommend, but operators approve public truth, final creative direction, publishing readiness, and waivers.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-132-001 | `CanonicalStageArtifact` | Typed artifact record with artifact type, schema ref, object hash, receipts, and owning stage. |
| DEP-CMF-132-002 | `StageArtifactReviewRequest` | Review request bundling artifact, source refs, doctrine/eval receipts, and approval policy. |
| DEP-CMF-132-003 | `ReviewerFinding` | Finding with severity, evidence, doctrine/primitive refs, repair command, and blocker policy. |
| DEP-CMF-132-004 | `HumanApprovalPolicy` | Declares required approval role, waiver policy, and auto-continue rules. |
| DEP-CMF-132-005 | `StageArtifactApprovalReceipt` | Receipt proving validation, review findings, approval, waiver, or rejection state. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/review_decisions.py` | Add canonical artifact, review request, reviewer finding, approval policy, and receipt models. |
| `src/ccp_studio/services/review_decision_service.py` | Own reviewer finding creation, severity rules, and approval decisions. |
| `src/ccp_studio/services/review_state_service.py` | Surface artifact, findings, blockers, waivers, and approvals. |
| `src/ccp_studio/services/approval_gate_service.py` | Block stage completion, final approval, publishing, or waiver gaps. |
| `src/ccp_studio/services/evaluation_receipt_service.py` | Link eval receipts to review and approval receipts. |
| `src/ccp_studio/workflows/review_workflow.py` | Run artifact review workflow and route human approvals. |
| `src/ccp_studio/api/v1/review_decisions.py` | Add artifact review, approve, reject, waive, and repair endpoints. |
| `POST /api/v1/review-decisions/artifacts`, `POST /api/v1/review-decisions/artifacts/{artifact_id}/review`, `POST /api/v1/review-decisions/artifacts/{artifact_id}/approve`, `POST /api/v1/review-decisions/artifacts/{artifact_id}/waive`, `GET /api/v1/review-decisions/artifacts/{artifact_id}` | Exact API routes for canonical artifact review, human approval, waiver, and inspection. |
| `src/ccp_studio/repositories/review_decisions.py` | Persist findings, approvals, waivers, and receipts. |
| Postgres tables: `canonical_stage_artifacts`, `stage_artifact_review_requests`, `reviewer_findings`, `stage_artifact_approval_receipts`, `approval_waivers` | Durable storage for stage artifacts, review packets, findings, human decisions, and waivers. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-SOC-001` | Verifiable Artifact | Every stage artifact and approval is hash-backed and receipt-linked. |
| `EXP-FBK-001` | Actionable Rejection | Findings include severity, evidence, and repair command. |
| `EXP-PRG-001` | Inline Routing SLA | Stage completion routes through review/approval policy. |
| `EXP-FRC-006` | Frictionless Block | Operators see exact blocker and waiver policy. |
| `EXP-TRS-004` | Cinematic Meaning | Reviewer blocks source distortion and false creative meaning. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M02: Cinematic Meaning Rule | Phase 4 Story 2.1 | `EXP-TRS-004` | Reviewer blocks source distortion, false story meaning, and flat composition mismatches. |
| Phase4-M03: Inline Routing SLA | Phase 4 Story 3.1 | `EXP-PRG-001` | Stage completion resolves review and approval policy inline. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Reviewer findings include evidence and repair command. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Approval receipt links artifact hash, eval receipts, findings, and human decision. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Artifact validation precedes review. | Reviewers should inspect valid structured artifacts, not malformed state. |
| Review severity controls workflow. | Critical findings block; warnings inform; suggestions do not halt. |
| Human approval policy is per stage. | Creative/public-truth stages require stronger human control than mechanical steps. |
| Waivers are explicit receipts. | Risk acceptance must be replayable. |

## 4. Implementation Plan

1. Add canonical artifact, review request, finding, approval policy, and approval receipt contracts.
2. Add registry of stage artifact types and required schemas.
3. Extend review workflow to validate artifact schema before review.
4. Add doctrine-aware reviewer rules for source truth, primitive receipts, consent, composition promise, brand context, and public truth.
5. Add human approval policy evaluation per manifest stage.
6. Add approval, rejection, waiver, and repair command APIs.
7. Block stage completion when artifact is invalid, critical finding exists, required human approval is missing, or waiver is not allowed.
8. Add Operations Board and review workbench read models.
9. Add tests for artifact validation, severity routing, approval policy, waiver, and replay.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class CanonicalStageArtifact(BaseModel):
    schema_version: Literal["cmf.canonical_stage_artifact.v1"]
    artifact_id: str
    artifact_type: Literal[
        "ResearchBrief", "InterviewBriefV2", "ExpressionIngredientInventory",
        "ContentSequenceProgram", "SceneSpec", "AssetManifest",
        "EditDecisionList", "CompositionRuntimeBinding", "ProviderJobReport",
        "RenderReport", "EvaluationReceipt", "ApprovalPacket", "PublishingIntent"
    ]
    stage_id: str
    schema_ref: str
    object_ref: str
    object_sha256: str
    receipt_refs: list[str] = Field(default_factory=list)


class ReviewerFinding(BaseModel):
    finding_id: str
    severity: Literal["suggestion", "warning", "critical"]
    evidence_ref: str
    doctrine_ref: str | None = None
    primitive_refs: list[str] = Field(default_factory=list)
    issue: str
    repair_command: str
    blocks_stage_completion: bool


class StageArtifactApprovalReceipt(BaseModel):
    schema_version: Literal["cmf.stage_artifact_approval_receipt.v1"]
    receipt_id: str
    artifact_id: str
    review_status: Literal["approved", "needs_revision", "rejected", "waived"]
    findings: list[ReviewerFinding] = Field(default_factory=list)
    approved_by: str | None = None
    waiver_reason: str | None = None
    receipt_sha256: str
```

## 6. Backward Compatibility Fallback

Existing review decisions remain valid for historical artifacts. New production stages must register canonical artifacts and review policy before completion. If an artifact type is unknown, the stage is blocked until a schema ref is registered or the artifact is routed to a human queue as noncanonical evidence.

If review service is unavailable, creative/public-truth stages block. Mechanical stages may continue only if manifest policy allows and prior gates passed.

## 7. Tasks

| Task | Owner Area | Output |
|---|---|---|
| T132-01 | Contracts | Add canonical artifact, review request, finding, policy, approval receipt. |
| T132-02 | Registry | Add canonical artifact type and schema registry. |
| T132-03 | Review Workflow | Validate artifact then run reviewer logic. |
| T132-04 | Approval Gates | Block stage completion/final approval/publishing on missing review. |
| T132-05 | API | Add approve, reject, waive, repair endpoints. |
| T132-06 | Review UI | Surface findings, evidence, severity, and approval policy. |
| T132-07 | Tests | Add validation, severity, approval, waiver, replay tests. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR / Test Evidence |
|---|---|---|---|
| AC132-01 | Stage completion requires canonical artifact validation and required receipts. | Stage marks complete with a free-text summary only. | Phase5-M01; artifact validation test. |
| AC132-02 | Critical reviewer findings block stage completion. | SceneSpec with fabricated quote is approved as warning. | Phase4-M02; critical finding test. |
| AC132-03 | Findings include evidence and repair command. | Reviewer says "weak" without evidence ref or action. | Phase4-M05; finding payload test. |
| AC132-04 | Human approval policy is enforced per stage. | Final creative direction auto-approves without operator. | Phase4-M03; approval policy test. |
| AC132-05 | Waivers are explicit and policy-bound. | Operator bypasses source-lineage failure without waiver receipt. | Phase5-M01; waiver receipt test. |

## 9. Dependencies

| Dependency | Type | Required Status |
|---|---|---|
| `TS-CMF-012` | Review surface | Review UI precedent. |
| `TS-CMF-040` | Revision audit | Repair/revision path. |
| `TS-CMF-092` | Approval workbench | Composition review integration. |
| `review_decision_service.py` | Existing service | Extend. |
| `approval_gate_service.py` | Existing service | Enforce. |
| `evaluation_receipt_service.py` | Existing service | Link eval receipts. |

## 10. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Contract tests | Artifact, finding, approval policy, and receipt models validate. |
| Schema tests | Unknown artifact type or missing schema blocks completion. |
| Reviewer tests | Critical/warning/suggestion severity routes correctly. |
| Approval tests | Required human approval blocks auto-completion. |
| Waiver tests | Waivers require allowed policy and receipt. |
| Replay tests | Approval receipt reconstructs artifact hash, findings, eval refs, and human decision. |
