---
tech_spec_id: "TS-CMF-075"
title: "Operator Composition and Template Approval Workbench"
story_id: "ui-2"
story_title: "Operator Composition and Template Approval Workbench"
epic_id: "cross-cutting"
epic_title: "PWA, Review, Evals, and Operator Surfaces"
status: "ready-for-development"
created_at: "2026-06-23"
source_story: "conversation-approved major update after TS-CMF-073"
fr_ids:
  - "FR-CMF-03.01"
  - "FR-CMF-07.02"
  - "FR-CMF-09.01"
  - "FR-CMF-09.03"
pipeline_stage: "operator UI overlay for stages 9-12"
entry_object: "scoped operator session and composition read model"
exit_object: "approved or rejected composition/template command receipt"
validation_contract: "guest/brand scope, preview lineage, JSON diff, eval blockers, receipt visibility"
required_receipt: "UiActionReceipt plus linked domain receipt"
runtime_target: "TypeScript web app / generated contracts / FastAPI read models / Command Bus"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-075: Operator Composition and Template Approval Workbench

**Status:** Ready for Development  
**Implementation Boundary:** UI workbench for reviewing scene-template bindings, composition JSON, rendered previews, eval blockers, and render readiness before production templates are built.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/tech-specs/TS-CMF-070-ui-architecture-and-operator-experience.md` | General operator UI architecture. |
| `docs/tech-specs/TS-CMF-072-scene-template-runtime-binding-for-reaction-clips.md` | Scene-template binding read model. |
| `docs/tech-specs/TS-CMF-073-canonical-composition-json-registry-and-preview-approval.md` | Composition approval workflow. |
| `docs/ux/ux-design-specification.md` | UX structure and operator experience requirements. |
| `docs/content-asset-code-and-format-registry.md` | Content asset code and format visibility. |

## 2. Overview

The operator needs a UI workbench before implementation of final templates. This surface makes the composition review process visible and safe: the operator can compare preview images, inspect composition JSON, verify old scene-template binding, see guest/brand scope, read eval blockers, and approve or reject through the Command Bus.

The workbench prevents CMF from confusing guests, approving unbound JSON, or rendering a template that lacks scene intelligence.

## 3. Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-03.01 | Brand and guest workspace isolation. | Workbench object header and scoped read models. |
| FR-CMF-07.02 | SceneSpec and composition lineage visible. | Binding, JSON, preview, and render contract panels. |
| FR-CMF-09.01 | Evidence-rich review with blockers. | Blocker panel and eval receipt visibility. |
| FR-CMF-09.03 | Approval commands produce receipts. | Approve/reject commands return UI and domain receipts. |

## 4. Implementation Plan

1. Add `CompositionApprovalReadModel`, `SceneTemplateBindingSummary`, `CompositionPreviewSummary`, and `CompositionApprovalBlocker`.
2. Build web app route for `Production > Composition Workbench`.
3. Render side-by-side preview and JSON inspector with hash/diff.
4. Show brand workspace, guest, content asset code, expression moment, route, SceneSpec, binding, and eval receipts.
5. Disable approval when blockers exist.
6. Submit approve/reject/supersede commands through generated command client.

## 5. Primary Read Model

```typescript
type CompositionApprovalReadModel = {
  organizationId: string;
  brandWorkspaceId: string;
  guestId: string;
  contentAssetCode: string;
  expressionMomentId: string;
  reactionTemplateCode: string;
  sceneSpecId: string;
  sceneTemplateBinding: SceneTemplateBindingSummary;
  compositionJson: unknown;
  compositionJsonHash: string;
  previewArtifacts: CompositionPreviewSummary[];
  evalReceipts: EvaluationReceiptSummary[];
  approvalBlockers: CompositionApprovalBlocker[];
  nextValidCommands: CommandActionSummary[];
};
```

## 6. Required UI Panels

| Panel | Purpose |
|---|---|
| Object Header | Brand, guest, asset code, stage, responsible actor, blocker count. |
| Preview Gallery | PNG/video previews rendered from JSON with hashes. |
| JSON Inspector | Canonical composition JSON, schema validation, diff from prior version. |
| Scene Binding Panel | Runtime asset, scene template ID, container, component, effects, CLS, text policy. |
| Beat Sync Panel | Question, guest reaction, state change, reveal/lock timing. |
| Eval and Blocker Panel | Primitive, scene, composition, text, safe-area, and source-lineage blockers. |
| Command Footer | Approve, reject, request revision, supersede, open render readiness. |

## 7. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `ApproveCompositionTemplateCommand`, `RejectCompositionTemplateCommand`, `RequestCompositionRevisionCommand`, `SupersedeCompositionTemplateCommand` |
| Events | Domain events from TS-CMF-073 plus UI action receipt events |
| Workflow | Operator approval overlay for stages 9-12 |
| Receipt | `UiActionReceipt` linked to `CompositionTemplateApprovalReceipt` |

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Fast UI approvals vs evidence | Approval requires JSON, preview, binding, eval status, and scope. | Button disabled until blockers clear. |
| Visual taste vs production truth | UI presents scene binding and JSON hash beside preview. | Approval receipt stores all hashes. |
| Multi-guest work vs confusion | Every panel inherits object header scope. | Read model refuses missing guest/brand context. |

## 9. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Workbench renders brand/guest/content asset scope. | Operator sees preview with no guest. |
| AC2 | Preview links to source composition JSON hash. | Preview image cannot be traced. |
| AC3 | Scene-template binding panel is present. | Operator approves without old scene-builder lineage. |
| AC4 | Approval disabled when blockers exist. | Operator approves missing background-removal plan. |
| AC5 | Approve/reject emits UI receipt plus domain receipt. | Button mutates local state only. |

## 10. Testing Strategy

- Component tests for required panels and missing-data states.
- Read-model contract tests generated from backend schemas.
- Command submission tests for approve/reject/revision/supersede.
- Blocker UI tests proving disabled actions.
- Visual regression checks for desktop and mobile operator views.

## Doctrine-Driven Test Harness Binding

This spec must be verified through TS-CMF-077 before implementation is considered complete. The test plan for this spec must identify the documented doctrine sources it depends on, the operational invariants those sources imply, the primitive or eval obligations that apply to its outputs, and the negative fixtures that prove forbidden shortcuts are blocked. Passing tests must emit or validate the required receipt chain, and any hard failure must map to an approval blocker when this spec touches review, rendering, publishing, memory, agents, adapters, or operator actions.

Minimum binding requirements:

- cite source doctrine or registry refs used by this spec;
- declare contract, workflow, receipt, and read-model invariants;
- include at least one negative or drift fixture for every forbidden shortcut named in the spec;
- prove required receipts are emitted, immutable, reconstructable, and linked to pipeline stage state;
- expose failed doctrine, primitive, or eval obligations as blocker-ready test output.

## 11. Spec Audit Receipt

| Field | Value |
|---|---|
| Tech Spec ID | TS-CMF-075 |
| Requirement Trace | FR-CMF-03.01, FR-CMF-07.02, FR-CMF-09.01, FR-CMF-09.03 |
| Pipeline Trace | UI overlay for stages 9-12 |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No approval without guest scope, no approval without scene binding, no local UI mutation as source truth |
