---
tech_spec_id: "TS-CMF-076"
title: "Open Source Integration Adapter Evaluation and Import Plan"
story_id: "platform-1"
story_title: "Open Source Integration Adapter Evaluation and Import Plan"
epic_id: "platform"
epic_title: "Runtime Integrations, Research, Video Editing, and Adapter Governance"
status: "ready-for-development"
created_at: "2026-06-23"
source_story: "conversation-approved open-source integration planning"
fr_ids:
  - "FR-CMF-08.02"
  - "FR-CMF-08.08"
  - "FR-CMF-10.05"
pipeline_stage: "cross-stage integration governance"
entry_object: "IntegrationCandidate"
exit_object: "IntegrationAdapterDecisionReceipt"
validation_contract: "license, architecture fit, security, reproducibility, contract boundary, doctrine fit"
required_receipt: "IntegrationAdapterDecisionReceipt"
runtime_target: "Python adapter registry / TypeScript leaf adapters / worker services / eval registry"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-076: Open Source Integration Adapter Evaluation and Import Plan

**Status:** Ready for Development  
**Implementation Boundary:** Governed evaluation and adapter planning for open-source projects that may support CMF research, video editing, visual editing, memory, search, renderer UI, and reaction-template implementation.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/tech-specs/TS-CMF-043-deterministic-remotion-and-motion-canvas-rendering.md` | Renderer boundary. |
| `docs/tech-specs/TS-CMF-049-svre-aurore-and-asset-research-engine-routing.md` | Research and search boundary. |
| `docs/tech-specs/TS-CMF-068-pi-harness-tool-registry.md` | Tool registry and Pi harness boundary. |
| `docs/tech-specs/TS-CMF-069-adk-agents-cli-adapter-export-and-drift-gate.md` | Agent adapter export and drift boundary. |
| User-provided open-source candidate list | Projects to evaluate before import or adapter build. |

## 2. Overview

Open-source projects can accelerate CMF, but they must not become uncontrolled dependencies or replace CMF doctrine. Each project is evaluated as one of four outcomes:

- adapter now;
- fixture or reference only;
- experimental lab only;
- reject/block.

The decision must be explicit and receipt-backed. We borrow useful primitives, UI patterns, renderer components, search mechanisms, or editing capabilities only when they fit CMF contracts.

## 3. Candidate Categories

| Category | Candidate Projects | Possible CMF Use |
|---|---|---|
| Reaction UI / template references | `apps/react-debate`, `react-tierlist`, `react-ranking-quiz`, `react-blind-rank`, `react-elimination`, `react-authority-quiz`, `react-mirror-quiz` | Remotion/Motion Canvas mechanic components and preview patterns. |
| Video editing / timeline | `openvideodev/react-video-editor`, `openvideodev/openvideo`, `OmniShotCut`, `video-use`, `yt-short-clipper`, `AI-Youtube-Shorts-Generator` | Timeline UI, clip selection, video editing automation, fixture comparison. |
| Animation / visual systems | `Manim`, `hyperframes`, `stretchystudio`, `see-through` | Explanatory animation, scene frames, transparent-layer workflows, visual references. |
| Search / research | `searxng`, `Gen-Searcher`, `last30days-skill`, `Open-Generative-AI` | SVRE/Aurore research, trend/context retrieval, query routing fixtures. |
| Memory / agents | `delta-Mem`, `SCAIL-2` | Memory candidate patterns, agentic research references, eval inspiration. |

## 4. Evaluation Criteria

Each candidate must be scored across these criteria:

1. License compatibility.
2. Runtime fit with Python/DSPy/Pi and TypeScript leaf boundary.
3. Contractability through Pydantic/JSON schema.
4. Reproducibility and receipt support.
5. Security and sandboxability.
6. Data privacy and guest/brand isolation.
7. Fit with interview-first doctrine.
8. Fit with SceneSpec and composition JSON.
9. Fit with primitive/eval gates.
10. Maintenance risk.
11. Adapter complexity.
12. Differentiation value for CMF.

## 5. Primary Contracts

```python
class IntegrationCandidate(BaseModel):
    candidate_id: str
    source_ref: str
    category: str
    proposed_use: str
    license_summary: str | None
    runtime_boundary: str
    risk_notes: list[str]


class IntegrationAdapterDecision(BaseModel):
    candidate_id: str
    decision: Literal["adapter_now", "reference_only", "lab_only", "blocked"]
    scorecard: dict[str, float]
    adapter_contracts_required: list[str]
    prohibited_uses: list[str]
    rationale: str
```

## 6. Adapter Boundary Rules

| Rule | Requirement |
|---|---|
| No direct uncontrolled import | Production use requires adapter, tests, receipts, and dependency review. |
| No doctrine replacement | Open-source tool cannot own CMF route, SceneSpec, eval, or approval truth. |
| No hidden state | Adapter state must be reconstructable or captured in receipts. |
| No guest leakage | Tools must operate inside brand/guest scoped workspace. |
| No UI-only truth | React/video editor components cannot become canonical timeline or composition truth. |

## 7. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `RegisterIntegrationCandidateCommand`, `RunIntegrationFitEvalCommand`, `ApproveIntegrationAdapterCommand`, `RejectIntegrationCandidateCommand` |
| Events | `IntegrationCandidateRegistered`, `IntegrationFitEvalCompleted`, `IntegrationAdapterApproved`, `IntegrationCandidateRejected` |
| Workflow | Adapter governance before dependency import or production tool execution |
| Receipt | `IntegrationAdapterDecisionReceipt` |

## 8. Initial Decision Bias

| Candidate Area | Starting Bias |
|---|---|
| Existing reaction apps | Adapter/reference now for deterministic UI mechanics, not production domain truth. |
| `react-video-editor` / `openvideo` | Strong candidate for operator timeline UI patterns and possible leaf editing UI. |
| `OmniShotCut` / `video-use` | Lab evaluation for automated editing workflows and video-understanding assist. |
| `Manim` | Reference/lab for explanatory animations; likely not first renderer for reaction clips. |
| `searxng` / `Gen-Searcher` | Strong candidate for SVRE/Aurore research routing after privacy and deployment review. |
| `delta-Mem` | Reference for memory architecture only until CMF memory contracts are mapped. |

## 9. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Speed from existing projects vs CMF sovereignty | Adapter decisions are explicit and receipt-backed. | Integration decision receipt stores scorecard and prohibited uses. |
| Powerful editing tools vs source truth | Tools consume CMF contracts; they do not own domain state. | Adapter tests prove contract boundaries. |
| Open-source convenience vs security | License/security/privacy review before import. | Blocker prevents dependency addition without receipt. |

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Every candidate has a decision receipt before production import. | Repo copied into production without license review. |
| AC2 | Adapter now decisions list required contracts and tests. | Tool is used through ad hoc shell command. |
| AC3 | Reference-only projects cannot execute in production. | Lab-only clipper runs on guest data. |
| AC4 | UI tools cannot become canonical composition source. | Timeline UI JSON replaces CMF composition JSON. |
| AC5 | Scorecards include doctrine and primitive fit. | Candidate chosen only because it is popular. |

## 11. Testing Strategy

- Scorecard unit tests for required criteria.
- Adapter boundary tests for state, receipts, and guest scope.
- License/security metadata presence tests.
- Contract tests for each approved adapter.
- Regression tests proving production cannot call blocked or lab-only candidates.

## Doctrine-Driven Test Harness Binding

This spec must be verified through TS-CMF-077 before implementation is considered complete. The test plan for this spec must identify the documented doctrine sources it depends on, the operational invariants those sources imply, the primitive or eval obligations that apply to its outputs, and the negative fixtures that prove forbidden shortcuts are blocked. Passing tests must emit or validate the required receipt chain, and any hard failure must map to an approval blocker when this spec touches review, rendering, publishing, memory, agents, adapters, or operator actions.

Minimum binding requirements:

- cite source doctrine or registry refs used by this spec;
- declare contract, workflow, receipt, and read-model invariants;
- include at least one negative or drift fixture for every forbidden shortcut named in the spec;
- prove required receipts are emitted, immutable, reconstructable, and linked to pipeline stage state;
- expose failed doctrine, primitive, or eval obligations as blocker-ready test output.

## 12. Spec Audit Receipt

| Field | Value |
|---|---|
| Tech Spec ID | TS-CMF-076 |
| Requirement Trace | FR-CMF-08.02, FR-CMF-08.08, FR-CMF-10.05 |
| Pipeline Trace | Cross-stage integration governance |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No uncontrolled repo import, no open-source doctrine replacement, no guest data through lab tools |
