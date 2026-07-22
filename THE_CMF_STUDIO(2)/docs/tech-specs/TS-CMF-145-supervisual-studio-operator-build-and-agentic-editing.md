---
tech_spec_id: "TS-CMF-145"
title: "SuperVisual Studio Operator Build and Agentic Editing"
story_id: "15.10"
story_title: "Build the SuperVisual Studio Workbench"
epic_id: 15
epic_title: "Operator Operations Runtime and Agentic Control"
status: "ready-for-development"
created_at: "2026-06-27"
fr_ids:
  - "FR-CMF-07"
  - "FR-CMF-09"
  - "FR-CMF-10"
  - "FR-CMF-14.04"
  - "FR-CMF-14.05"
  - "FR-CMF-14.06"
  - "FR-CMF-14.07"
  - "FR-CMF-14.08"
  - "FR-CMF-14.09"
pipeline_stage: "context intake, content planning, SuperVisual creation, editing, review, approval, export, and scheduling handoff"
entry_object: "SuperVisualStudioCreateRequest"
exit_object: "SuperVisualStudioApprovalAndExportReceipt"
validation_contract: "context source selection, Content Planning Agents Team, JIT Skill Compiler, script/composition draft, editable copy/family/composition/layers/prompts/assets/text/primitives/export, command proposal, revision tracking, approval, download, scheduling handoff"
required_receipt: "SuperVisualStudioActionReceipt"
runtime_target: "React operator-web / FastAPI / Pydantic v2 / Command Bus / Pi Agent Gateway / JIT Skill Compiler / Still Visual Runtime API / Skia export / Scheduler handoff"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-145: SuperVisual Studio Operator Build and Agentic Editing

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/tech-specs/README.md` | Confirms the current spec sequence ends at TS-CMF-144 and that this workbench is a new component spec. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md` | Parent single-image and SuperVisual engine requirement. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-102-supervisual-composition-families-and-primitive-triad-contracts.md` | SuperVisual family and primitive contract precedent. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-133-still-visual-composition-program-manifest-and-stage-orchestration.md` | Still visual program manifest and stage orchestration dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-134-supervisual-visual-grammar-atlas-router-and-primitive-feel-matrix.md` | SuperVisual grammar atlas, route receipt, and primitive feel matrix dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-135-still-visual-runtime-api-review-read-model-and-approval-workbench.md` | Runtime API, review, approval, revision, and export dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-136-operator-web-api-client-and-generated-contract-binding.md` | Generated TypeScript contract and API client dependency for operator-web. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-138-pi-harness-agent-command-routing-and-delegation-runtime.md` | Pi/agent delegation dependency for agentic edits. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-139-operator-command-console-and-chat-to-command-proposal-runtime.md` | Chat-to-command proposal dependency for operator feedback. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-140-revision-update-and-repair-workflow-runtime.md` | Repair plan and revision receipt dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-142-live-operations-event-stream-and-read-model-sync.md` | Live status and read-model sync dependency. |
| `THE CMF STUDIO/docs/ux/mockups/supervisual-compositions/_supervisual-compositions.draft.json` | Current SuperVisual mockup composition draft registry. |
| `THE CMF STUDIO/docs/ux/mockups/supervisual-compositions/_supervisual-composition-contact-sheet.png` | Visual approval board proving initial composition families exist as references. |

## 2. Overview

SuperVisual Studio is the operator-facing workbench for producing specific SuperVisuals from structured context. It is not a generic image prompt box and it is not a static gallery. It is the place where a content asset becomes a real production object: context is selected, agents plan the asset, JIT Skills compile the script and composition, the visual route is chosen, layers and prompts are materialized, primitives are evaluated, the operator edits, agents repair, and the final image is approved, downloaded, exported, or sent to scheduling.

The Studio must support two valid context modes:

1. `InterviewBrief + InterviewTranscript`: the preferred CMF interview-first source mode.
2. `VideoTranscriptOnly`: fallback mode when no fresh interview brief exists and the source is an existing interview, video, webinar, podcast, or clip transcript.

All context-to-content decisions are managed by the Content Planning Agents Team. The UI may expose simple buttons, but every production action must become a command with scope, target, evidence, receipt, and approval state. When the operator types feedback like "make this sharper", the system must convert that feedback into a structured edit command that names the affected copy, visual family, composition, layer plan, prompt, generated asset, text placement, primitive gap, or export target.

The operator must be able to inspect and edit the following before approval:

1. copy;
2. visual family;
3. composition route;
4. layer plan;
5. provider prompts;
6. generated assets;
7. text placement;
8. primitive coverage;
9. eval blockers;
10. final export format and scheduling readiness.

## 3. Product Requirement

SuperVisual Studio must let a CMF operator create a finished still visual asset from interview intelligence without leaving the factory workflow. The operator starts from a guest workspace, selects an approved context source, and asks the system to produce one or more specific SuperVisuals. The Content Planning Agents Team reads the context bundle, identifies source-backed signals, applies target-audience context premises, routes the asset through the JIT Skill Compiler, and produces a `SuperVisualContentPlan` containing thesis, hook, copy, caption angle, visual family, primitive obligations, and composition intent. The router then proposes a SuperVisual family such as contrast card, symbolic proof card, quote proof, poll-style visual, meme, documentary social card, or reaction still.

The Studio must show the operator a live workbench, not a black-box result: editable text, route candidates, composition JSON, layer stack, provider prompts, generated assets, source evidence, primitive checks, preview render, export options, and approval blockers. The operator can manually edit fields or write feedback into the command console. Feedback becomes a structured proposal, routed to the right agent or tool, tracked through receipts, and reflected back into the read model. A SuperVisual is complete only when the render, primitive eval, approval receipt, export receipt, and optional schedule handoff exist.

## 4. Canonical User Flow

```text
Brand Workspace
  -> Select Guest / Brand Scope
  -> Select Context Source
     -> Interview Brief + Interview Transcript
     -> Video Transcript Only
  -> Generate SuperVisual Plan
  -> Review Content Planning Agent Output
  -> Choose SuperVisual Target
  -> Route Visual Family + Composition
  -> Materialize Layer Plan + Provider Prompts
  -> Generate / Import Assets
  -> Render Preview
  -> Edit Manually or Request Agent Fix
  -> Run Primitive + Doctrine Evals
  -> Approve
  -> Download / Export
  -> Send to Scheduling
```

The UI must never hide which object is active. The header must show guest workspace, content asset code, active context source, current SuperVisual id, route id, render version, approval state, and last receipt id.

## 5. Component Map

| Component | Responsibility | Required Output |
|---|---|---|
| `ContextSourceSelector` | Selects `InterviewBrief + InterviewTranscript` or `VideoTranscriptOnly`, validates guest scope, and displays source evidence. | `SuperVisualContextBundle` |
| `ContentPlanningAgentPanel` | Shows agent team status, extracted signals, target audience context premises, route candidates, and JIT Skill Compiler output. | `SuperVisualContentPlan` |
| `SuperVisualBriefComposer` | Edits asset objective, thesis, hook, caption, platform, content format, and operator notes. | `SuperVisualBriefDraft` |
| `FamilyAndCompositionRouter` | Routes to visual family, composition grammar, primitive feel profile, and alternates. | `SuperVisualRouteReceipt` |
| `LayerPlanWorkbench` | Shows editable layer stack, zones, source media, generated media, text zones, brand marks, and micro-semiotic anchors. | `SuperVisualLayerPlan` |
| `PromptAndProviderWorkbench` | Shows provider prompts, provider job state, model/provider choice, asset lineage, and regeneration commands. | `ProviderJobPlan` |
| `CanvasPreviewAndTextPlacement` | Provides final preview, safe-area grid, text nudge/edit controls, source/asset overlays, and render version comparison. | `SuperVisualPreviewState` |
| `PrimitiveEvalPanel` | Displays primitive roles, exact primitive ids, doctrine checks, blockers, warnings, and suggested repairs. | `EvaluationReceipt` |
| `AgentQuickEditConsole` | Converts operator feedback into a safe command proposal, then submits through Command Bus after confirmation. | `CommandProposalReceipt` |
| `ExportApprovalScheduler` | Approves, downloads, exports, packages, and sends approved assets to scheduling. | `SuperVisualStudioApprovalAndExportReceipt` |

## 6. Data Contracts

### 6.1 SuperVisualStudioCreateRequest

```python
class SuperVisualStudioCreateRequest(BaseModel):
    workspace_id: str
    guest_id: str
    requested_by: str
    context_mode: Literal["interview_brief_and_transcript", "video_transcript_only"]
    interview_brief_id: str | None = None
    transcript_id: str
    video_asset_id: str | None = None
    target_platforms: list[Literal["instagram", "linkedin", "youtube_community", "x", "telegram"]]
    requested_supervisual_count: int = 1
    operator_intent: str | None = None
    required_primitive_ids: list[str] = []
```

Validation rules:

1. `guest_id` must match all selected source objects.
2. `interview_brief_id` is required in `interview_brief_and_transcript` mode.
3. `transcript_id` is always required.
4. `operator_intent` may guide planning but cannot replace source evidence.
5. At least three primitives must be selected or assigned by the planning route before approval.

### 6.2 SuperVisualContextBundle

```python
class SuperVisualContextBundle(BaseModel):
    context_bundle_id: str
    workspace_id: str
    guest_id: str
    context_mode: str
    interview_brief_ref: ArtifactRef | None
    transcript_ref: ArtifactRef
    video_asset_ref: ArtifactRef | None
    selected_source_excerpts: list[SourceExcerpt]
    expression_moments: list[ExpressionMomentRef]
    target_audience_context_premises: list[ContextPremiseRef]
    brand_context_ref: ArtifactRef
    voice_visual_dna_ref: ArtifactRef | None
    created_receipt_id: str
```

The context bundle is immutable for a Studio run. If the operator changes context, the system creates a new bundle and preserves lineage.

### 6.3 SuperVisualContentPlan

```python
class SuperVisualContentPlan(BaseModel):
    content_plan_id: str
    context_bundle_id: str
    planning_agent_code: str
    jit_skill_receipt_id: str
    asset_intent: str
    thesis: str
    hook_options: list[str]
    copy_blocks: list[CopyBlock]
    caption_angle: str | None
    candidate_visual_families: list[VisualFamilyCandidate]
    recommended_family_id: str
    required_primitives: list[PrimitiveObligation]
    source_evidence_refs: list[SourceExcerptRef]
    blockers: list[PlanningBlocker]
```

The content plan is where script and composition are first born from context engineering and JIT Skills. It must include source evidence and primitive obligations before routing can proceed.

### 6.4 SuperVisualEditableDraft

```python
class SuperVisualEditableDraft(BaseModel):
    draft_id: str
    content_plan_id: str
    visual_family_id: str
    composition_template_id: str
    composition_json: dict
    layer_plan: list[LayerSpec]
    text_zones: list[TextZoneSpec]
    prompt_plan: list[ProviderPromptSpec]
    generated_assets: list[GeneratedAssetRef]
    primitive_eval_state: PrimitiveEvalState
    render_ref: ArtifactRef | None
    revision_index: int
```

The draft may be edited by the operator or by agent commands. Accepted draft changes become new revisions; rejected draft changes stay in history but do not mutate the approved candidate.

### 6.5 SuperVisualEditCommand

```python
class SuperVisualEditCommand(BaseModel):
    command_id: str
    draft_id: str
    actor_id: str
    actor_type: Literal["operator", "agent", "sub_agent"]
    edit_target: Literal[
        "copy",
        "visual_family",
        "composition",
        "layer_plan",
        "prompt_plan",
        "generated_asset",
        "text_placement",
        "primitive_eval",
        "export_settings",
    ]
    instruction: str
    structured_patch: dict | None
    requires_agent_execution: bool
    expected_receipt_type: str
```

Every quick edit from chat must become this command or a rejected command proposal with a blocker.

### 6.6 SuperVisualStudioReadModel

```python
class SuperVisualStudioReadModel(BaseModel):
    studio_run_id: str
    workspace_id: str
    guest_id: str
    asset_code: str | None
    context_bundle: SuperVisualContextBundle
    content_plan: SuperVisualContentPlan | None
    active_draft: SuperVisualEditableDraft | None
    route_receipts: list[str]
    provider_job_receipts: list[str]
    render_receipts: list[str]
    eval_receipts: list[str]
    revision_receipts: list[str]
    approval_state: Literal["not_started", "drafting", "rendered", "blocked", "ready_for_approval", "approved", "exported", "scheduled"]
    blockers: list[ApprovalBlocker]
    available_actions: list[str]
```

The React UI must render from this read model, not from static fixture state, except in explicit fixture mode.

## 7. Agent Team Responsibilities

| Agent Code | Actor | Responsibility | Authority Boundary |
|---|---|---|---|
| `PLN-CONTENT-AG` | Content Planning Agent | Converts context into asset intent, source-backed signal, thesis, hook, copy direction, and visual target. | Cannot approve or export. |
| `CTX-PREMISE-SA` | Context Premise Sub-Agent | Extracts target audience premises from source context, comments, audience conversations, and brand audience rules. | Cannot invent unsupported audience claims. |
| `JIT-SKLCMPR-SA` | JIT Skill Compiler Sub-Agent | Compiles SuperVisual-specific script/composition instructions from context, primitives, archetype, and output family. | Cannot bypass primitive obligations. |
| `RTE-SPVROUT-AG` | SuperVisual Routing Agent | Selects visual family, composition grammar, alternates, and route blockers. | Cannot render without route receipt. |
| `CMP-LAYPLAN-SA` | Layer Plan Sub-Agent | Produces and repairs composition JSON, layer plan, text zones, and provider asset slots. | Cannot change source evidence. |
| `GEN-ASSETGN-AG` | Asset Generation Agent | Plans Ideogram/Qwen/Skia/provider jobs and registers generated asset lineage. | Cannot final-render without deterministic compilation path. |
| `EVL-PRIMTST-SA` | Primitive Eval Sub-Agent | Evaluates primitive coverage, doctrine compliance, source truth, and approval blockers. | Cannot waive blockers. |
| `OPR-REVWCHK-AG` | Operator Review Agent | Packages review state, suggested fixes, and approval readiness for the operator. | Cannot approve for the human. |
| `PUB-SCHEDUL-AG` | Scheduling Agent | Creates schedule handoff only after approval and export receipts exist. | Cannot schedule unapproved assets. |

## 8. UI Requirements

### 8.1 Primary Layout

The SuperVisual Studio screen must use a workbench layout:

1. left rail: guest workspace, active context, asset code, history, and run status;
2. center: canvas preview with safe-area grid, version compare, and text placement controls;
3. right rail: edit panels for copy, visual family, composition, layers, prompts, generated assets, primitives, and export;
4. bottom rail: command console, action timeline, receipts, and live agent status.

### 8.2 Required Buttons

The UI must provide these command-backed actions:

1. `Create SuperVisual`;
2. `Generate Plan`;
3. `Route Family`;
4. `Materialize Layers`;
5. `Generate Assets`;
6. `Render Preview`;
7. `Run Primitive Eval`;
8. `Request Agent Fix`;
9. `Approve`;
10. `Download`;
11. `Export Package`;
12. `Send to Schedule`.

Buttons must not mutate static UI state. They must create a command, submit it, receive a receipt, and update the read model.

### 8.3 Agent Quick Edit Console

The prompt box should support feedback like:

```text
Make the contrast sharper but keep the guest's exact quote and do not change the primitive route.
```

The system must respond with:

1. proposed edit target;
2. affected draft fields;
3. required agent/tool;
4. expected receipts;
5. blockers if any;
6. confirmation action.

The operator should see a tracking row such as:

```text
proposed -> confirmed -> queued -> executing -> rendered -> evaluated -> ready for review
```

## 9. Editing Boundaries

| Editable Area | Operator Edit | Agent Edit | Required Validation |
|---|---|---|---|
| Copy | Direct text edit with versioning. | Rewrite proposal from source excerpts. | Source quote integrity and length budget. |
| Visual Family | Select alternate family. | Route recommendation. | SuperVisual atlas route receipt. |
| Composition | Select composition template or adjust composition JSON fields. | Composition repair. | Template schema, safe area, primitive role coverage. |
| Layer Plan | Reorder, enable, disable, replace, or repair layers. | Layer plan regeneration. | Layer schema, asset lineage, render compatibility. |
| Prompts | Edit provider prompts and regenerate assets. | Provider prompt repair. | Provider responsibility policy and prompt lineage. |
| Generated Assets | Regenerate, replace, approve, or reject individual assets. | Asset generation job. | Asset provenance, guest scope, consent, brand fit. |
| Text Placement | Drag, nudge, resize, or reflow text zones. | Text placement optimization. | Safe-area, text budget, legibility, platform crop. |
| Primitives | Select, inspect, or request primitive repair. | Eval and repair suggestion. | At least three primitive roles satisfied for approval. |
| Export | Choose platform and file variant. | Export package build. | Approval receipt, render hash, export receipt. |

## 10. API Requirements

The Studio should compose existing still visual endpoints from TS-CMF-135 and add a Studio-specific read model facade.

| Route | Method | Purpose |
|---|---|---|
| `/api/v1/supervisual-studio/runs` | `POST` | Create Studio run from context source. |
| `/api/v1/supervisual-studio/runs/{run_id}` | `GET` | Return `SuperVisualStudioReadModel`. |
| `/api/v1/supervisual-studio/runs/{run_id}/plan` | `POST` | Invoke Content Planning Agents Team and JIT Skill Compiler. |
| `/api/v1/supervisual-studio/runs/{run_id}/route` | `POST` | Route visual family and composition. |
| `/api/v1/supervisual-studio/runs/{run_id}/drafts/{draft_id}/edit` | `POST` | Submit structured edit command. |
| `/api/v1/supervisual-studio/runs/{run_id}/agent-fix/propose` | `POST` | Convert operator feedback into command proposal. |
| `/api/v1/supervisual-studio/runs/{run_id}/render` | `POST` | Render preview through still visual runtime. |
| `/api/v1/supervisual-studio/runs/{run_id}/evaluate` | `POST` | Run primitive and doctrine evals. |
| `/api/v1/supervisual-studio/runs/{run_id}/approve` | `POST` | Create approval receipt. |
| `/api/v1/supervisual-studio/runs/{run_id}/download` | `POST` | Create downloadable export artifact. |
| `/api/v1/supervisual-studio/runs/{run_id}/schedule` | `POST` | Send approved export to scheduling handoff. |

Routes that mutate must pass through Command Bus or produce an equivalent command receipt. Direct service mutation from React is forbidden.

## 11. Command Types

The command registry must include:

1. `create_supervisual_from_interview_context`;
2. `create_supervisual_from_video_transcript`;
3. `generate_supervisual_content_plan`;
4. `route_supervisual_family`;
5. `change_supervisual_family`;
6. `change_supervisual_composition`;
7. `revise_supervisual_copy`;
8. `revise_supervisual_layer_plan`;
9. `revise_supervisual_provider_prompt`;
10. `regenerate_supervisual_asset`;
11. `move_supervisual_text_zone`;
12. `run_supervisual_primitive_eval`;
13. `approve_supervisual`;
14. `download_supervisual_export`;
15. `schedule_supervisual`.

Each command requires workspace scope, guest scope, active draft or run id, actor id, expected receipt type, and permission check.

## 12. Primitive and Doctrine Gates

Approval is blocked unless all required checks pass:

1. at least three primitive roles are satisfied;
2. every primitive has an exact registry id;
3. primitive claims are grounded in the selected context bundle;
4. source quotes are not altered without explicit paraphrase state;
5. composition family matches the intended content meaning;
6. text is legible in platform crop;
7. asset lineage exists for generated media;
8. render hash and export hash are recorded;
9. guest workspace scope is valid;
10. approval receipt exists before scheduling.

Warnings can be waived only when the blocker is declared waiver-eligible by the eval registry. Source truth, guest scope, consent, primitive minimums, and render reproducibility are hard blockers.

## 13. Export and Scheduling

The Studio must support:

1. preview download for review with watermark and draft state;
2. final download after approval without draft watermark;
3. export package containing image, metadata, source refs, composition JSON, render hash, provider lineage, eval receipt, and approval receipt;
4. scheduling handoff with platform, caption, asset id, approval receipt, and publication window.

Scheduling cannot accept draft renders. If the operator clicks `Send to Schedule` before approval, the UI must show the missing blocker and offer `Run Eval` or `Approve` if eligible.

## 14. Acceptance Criteria

1. Operator can create a SuperVisual Studio run from `InterviewBrief + InterviewTranscript`.
2. Operator can create a SuperVisual Studio run from `VideoTranscriptOnly`.
3. Content Planning Agents Team produces a source-backed `SuperVisualContentPlan`.
4. JIT Skill Compiler produces script/composition instructions tied to primitives and visual family.
5. Operator can edit copy, visual family, composition, layer plan, prompts, generated assets, text placement, primitives, and export target.
6. Operator feedback in the chat console becomes a structured command proposal with receipt tracking.
7. The UI displays current command status, receipts, blockers, evals, and available actions.
8. Rendered previews are generated from the still visual runtime, not static image mocks.
9. Approval is blocked until primitive, doctrine, source, scope, render, and export gates pass.
10. Operator can download an approved export.
11. Operator can send an approved export to scheduling.
12. Every action is reconstructable from receipts and read models.

## 15. Test Plan

### Unit Tests

1. Validate `SuperVisualStudioCreateRequest` for both context modes.
2. Reject mismatched guest ids across context sources.
3. Reject plan generation without transcript.
4. Reject approval without three primitive roles.
5. Reject scheduling without approval receipt.
6. Validate command proposal mapping from natural-language feedback.

### Integration Tests

1. Create run -> generate plan -> route family -> materialize draft -> render -> eval -> approve -> download.
2. Create run from video transcript only and confirm interview brief is not required.
3. Submit quick edit feedback and confirm `SuperVisualEditCommand` targets the right field.
4. Regenerate a generated asset and confirm lineage is preserved.
5. Move a text zone and confirm safe-area validation runs.
6. Export approved image and verify metadata package includes composition JSON and receipts.

### UI Tests

1. The Studio screen renders context source, canvas, edit panels, command console, and receipts.
2. Buttons create commands instead of mutating local mock data.
3. Live event stream updates run status.
4. Approval blockers are visible and actionable.
5. Download button is disabled until approval or clearly marked as draft-preview download.
6. Schedule button is disabled until export readiness passes.

### Negative Fixtures

1. Empty transcript.
2. Missing Brand Context.
3. Cross-guest source objects.
4. Unsupported visual family.
5. Primitive minimum failure.
6. Provider job without lineage.
7. Free-form prompt requesting unsupported mutation.
8. Schedule request before approval.

## 16. Implementation Sequence

1. Add backend contracts and facade routes for `SuperVisualStudioReadModel`.
2. Wire Studio commands into the operator command registry.
3. Add React route/screen for SuperVisual Studio.
4. Replace static SuperVisual mockups with fixture mode and live API mode.
5. Implement context source selector and content planning panel.
6. Implement editable draft panels for copy, family, composition, layers, prompts, assets, text, primitives, and export.
7. Wire command console quick edits to command proposal endpoints.
8. Wire render, eval, approval, download, export, and schedule actions.
9. Add tests, fixtures, and visual regression coverage.

## 17. Non-Goals

1. This spec does not replace the lower still visual runtime specs.
2. This spec does not authorize loose image prompting without structured context.
3. This spec does not make static mockup boards production output.
4. This spec does not allow chat to mutate production state directly.
5. This spec does not allow scheduling unapproved assets.
