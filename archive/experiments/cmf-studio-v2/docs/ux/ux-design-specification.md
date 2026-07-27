---
workflowType: "cmf-adapted-ux-design"
status: "draft-canonical"
project_name: "CMF STUDIO"
authoring_agent: "GOV-UXDESGN-AG"
created_at: "2026-06-22"
source_agent: "bmad/.bmad/bmm/agents/ux-designer.md"
output_folder: "THE CMF STUDIO/docs/ux"
inputDocuments:
  - "THE CMF STUDIO/docs/prd/modules/PRD_INDEX.md"
  - "THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md"
  - "THE CMF STUDIO/docs/prd/modules/PRD_CMF_02_Pipeline_Agent_Orchestration.md"
  - "THE CMF STUDIO/docs/prd/modules/PRD_CMF_03_Workspace_Commercial_Consent_Source.md"
  - "THE CMF STUDIO/docs/prd/modules/PRD_CMF_04_Legacy_Primitives_JIT_Spec_Governance.md"
  - "THE CMF STUDIO/docs/prd/modules/PRD_CMF_05_Brand_Genesis_Context.md"
  - "THE CMF STUDIO/docs/prd/modules/PRD_CMF_06_Interview_Expression_Routing.md"
  - "THE CMF STUDIO/docs/prd/modules/PRD_CMF_07_Editing_Composition_Rendering.md"
  - "THE CMF STUDIO/docs/prd/modules/PRD_CMF_08_Evaluation_Review_Publishing_Memory.md"
  - "THE CMF STUDIO/docs/prd/modules/PRD_CMF_09_Non_Functional_Requirements.md"
  - "THE CMF STUDIO/docs/prd/modules/PRD_CMF_10_Agent_Factory_Runtime.md"
  - "THE CMF STUDIO/docs/cmf-studio-pipeline-map.md"
  - "THE CMF STUDIO/docs/epics.md"
  - "THE CMF STUDIO/docs/ui/cmf-eval-workbench.md"
  - "THE CMF STUDIO/docs/evals/07-eval-registry-and-workbench-architecture.md"
  - "THE CMF STUDIO/docs/cmf-studio-agent-factory-registry.md"
  - "THE CMF STUDIO/docs/cmf-studio-agent-factory-architecture.md"
  - "THE CMF STUDIO/docs/cmf-studio-agent-intelligence-contract.md"
---

# CMF STUDIO UI/UX Design Specification

## 1. Executive Summary

CMF Studio is an interview-first expression operating system. The UI must therefore behave less like a content calendar and more like a governed production cockpit. Its job is to make complex creative work calm, inspectable, and safe: the Operator should always know which production object is active, which stage owns it, which agent or service is responsible, which proof is missing, and which human decision can move the work forward.

The first screen should be the usable product surface, not a landing page. CMF users arrive to operate brands, sessions, assets, reviews, agents, workers, and approvals. The interface should be dense but legible, with restrained visual styling, high information scent, strong status language, and fast drill-down from high-level pipeline health to exact evidence.

The core experience is:

```text
Brand workspace
-> guest workspace
-> Monthly Interview Brief
-> Interview / Complete Expression Session
-> pipeline control tower
-> active object surface
-> evidence and validation panels
-> command actions
-> receipts and blockers
-> review, approval, publishing, memory, or recovery
```

The UI has two first-class surfaces:

- PWA Control Tower: full evidence, production, agent, review, memory, and operations interface.
- Telegram Operator Cockpit: compact notification and quick-action leaf surface for safe, low-complexity decisions, always deep-linking back to the exact PWA object state.

## 2. Product Vision From A UX Perspective

The product should feel like a factory floor with a clear chain of custody, not like a blank AI chat box. The Operator should experience CMF Studio as a system that carries the mental load of source truth, routing, creative lineage, primitive quality, render operations, and approval safety.

The main UX promise:

```text
I can guide one brand cycle end to end without losing the source, the reason, the proof, or the approval boundary.
```

The UI must protect the project's differentiators:

- interview quality begins before recording through CRAL/SCRE, Context Premise, Matrix of Edging, Emotional DNA, Voice DNA, and Narrative State Induction;
- extraction happens at two levels: from the guest before/during the session and from the transcript/source after recording;
- JIT Skill Compilers are saturation-bound induction, extraction, routing, and eval compilers, not generic few-shot prompt snippets;
- primitives, SDA/SFL, CBAR, and legacy CMF intelligence are production quality standards;
- Ideogram 4 `CompositionJob` JSON is composition lineage, not an optional prompt detail;
- evaluation receipts and human review are release gates;
- Neo4j is an inspectable rebuildable projection, not the canonical state store.

## 3. Primary Users

| User | Needs | UX Implication |
|---|---|---|
| Owner / Admin | Workspace health, roles, commercial scope, readiness, safety | High-level dashboard with entitlement, role, blocker, and release status |
| Operator | Run brand cycles, interviews, routing, reviews, revisions | Object-first Control Tower with guided next valid actions |
| Reviewer | Approve, reject, revise, hold, or escalate with evidence | Review Workbench with source, consent, evals, blockers, and revision history |
| Migration Steward | Convert legacy intelligence into typed assets, fixtures, evals | Migration surface with source hash, target contract, eval target, status, reviewer |
| Production Steward | Manage scenes, providers, renders, workers, assets | Production board with job receipts, costs, retry/cancel/resume, output lineage |
| Publishing Approver | Confirm publishing intent and Publer scheduling | Publishing surface with approved asset, platform variants, schedule, receipt |
| Agent Supervisor / Builder | Inspect role specs, tools, skills, evals, readiness | Agent Factory Workbench with persona codes, active object scope, readiness gates |

Guests are indirectly served through source capture, consent, and interview experience. The guest-facing experience must be human and simple; the complex factory machinery belongs in the Operator UI.

## 4. Experience Principles

| Principle | Requirement |
|---|---|
| Proof before preview | Final media preview never appears without source, consent, route, eval, and receipt context nearby |
| Object-first navigation | Every page centers one active object or a filtered set of objects with stage state |
| Guest isolation | Every object is visibly scoped to brand workspace, guest/client, session, and package |
| Stage visibility | The canonical pipeline stage is visible in headers, filters, and receipts |
| Human authority | Approval, publishing, consent changes, and memory admission are explicit human-gated actions |
| Calm density | The UI is compact and operational, not marketing-like or decorative |
| Evidence symmetry | Telegram and PWA reference the same object IDs, state, commands, and receipts |
| Primitive quality | Primitive obligations and failures are reviewable, not hidden in evaluator prose |
| Agent accountability | Agent actions show persona code, role, input, output, tools, evals, and receipt |
| Rebuildable memory | Memory and Neo4j views show evidence, event source, and projection status |

## 5. Information Architecture

### 5.1 Global Navigation

The PWA should use a persistent left rail on desktop and a compact bottom or drawer navigation on mobile.

Primary sections:

| Section | Purpose |
|---|---|
| Control Tower | Brand workspace status, pipeline health, active work, blockers, next actions |
| Guests | Guest/client workspaces, consent, sessions, source artifacts, asset packages, and production state |
| Pipeline | Stage map, object spine, orchestration runs, stage execution plans |
| Brand Genesis | Brand Context Version, acting library, rig, micro-semiotic anchors, locks |
| Research | CRAL/SCRE, source evidence, Context Premise, Audience Reality, claim safety |
| Interview | Interview prep, Narrative State Induction, Matrix of Edging, live guidance, recording setup |
| Extraction | Expression Moments, transcript alignment, JIT skill records, route candidates |
| Packages | Guest Asset Packs, Monthly Asset Engine planning, valid formats only |
| Production | Complete Editing Sessions, SceneSpec, CompositionJob, visual research, provider jobs, renders |
| Evals | Eval target selection, run queue, receipts, primitive failures, blockers |
| Review | Evidence-rich review, revision commands, approval, rejection, Voice-DNA Boost requests |
| Publishing | Publishing Intent, platform variants, Publer jobs, schedule receipts |
| Memory | Memory admission, corrections, rejected patterns, Neo4j projection views |
| Agent Factory | Departments, persona registry, role specs, tools, skills, hooks, readiness evals |
| Operations | Workers, queues, costs, failures, recovery actions, readiness checks |

### 5.2 Object Header

Every object detail page should share a common header:

| Field | Examples |
|---|---|
| Brand and guest scope | organization, brand workspace, guest/client, active Brand Context Version |
| Active object | `ExpressionMoment`, `AssetPackageItem`, `ContentAsset`, `SceneSpec`, `RenderOutput`, `EvaluationReceipt` |
| Content asset code | `CEL-CLDNTA-S01-GAP-SV-CSC-001-V01` |
| Stage | canonical stage number and label |
| State | draft, ready, running, blocked, review-ready, approved, superseded |
| Responsible entity | agent/service code such as `REV-REVWBCH-AG` |
| Validation contract | required proof before command execution |
| Required receipt | receipt expected for successful transition |
| Open blockers | hard failures, missing evidence, consent mismatch |
| Next valid actions | command buttons permitted for current role and state |

## 6. Core Surface Requirements

### 6.1 Control Tower

Purpose: show the operator what needs attention now.

Required regions:

- workspace health strip;
- active brand selector;
- active guest/client selector;
- content asset code search;
- content format filters;
- commercial entitlement display limited to `$29/week` trial Guest Asset Pack and `$99/month` Monthly Asset Engine;
- pipeline progress by stage;
- open blockers and stale objects;
- recent commands and receipts;
- active agents and running workflows;
- review queue;
- provider/render queue;
- Telegram notification state.
- monthly entry artifact: `Interview Brief`;
- fallback source-ingestion path: existing interview transcript/video, only when no new interview will be conducted.

Primary actions:

- generate Monthly Interview Brief;
- open active object;
- open guest workspace;
- ingest existing interview transcript/video when no new interview will be conducted;
- filter by content format;
- resume workflow;
- inspect blocker;
- run readiness check;
- open review queue;
- open operations recovery.

The Control Tower must not introduce new customer-facing offers, credit bundles, tiers, or newsletters.

### 6.1A Guest and Brand Workspace Management

Purpose: prevent Operators from confusing guests, brands, sessions, source files, assets, approvals, and memory.

Required views:

- brand workspace list and active workspace switcher;
- guest/client list inside each brand workspace;
- guest profile with consent, source artifacts, sessions, Voice DNA, Emotional DNA, Interview Asset Contracts, Expression Moments, Asset Package Specs, content assets, approvals, publishing intents, and memory;
- session timeline for each guest;
- asset package board per guest;
- cross-guest compilation warning and approval flow when a future workflow intentionally combines guests;
- guest-scoped search and filters.

Required hierarchy:

```text
organization
-> brand_workspace
-> guest
-> expression_session
-> asset_package
-> content_asset
-> asset_version
```

Every queue row, card, Telegram payload, review screen, export, and Publer draft must show enough brand/guest scope to avoid ambiguity.

### 6.1B Content Asset Codes

Every content asset must expose a readable content asset code in addition to internal IDs.

Code shape:

```text
{BRD}-{GST}-{SES}-{PKG}-{FMT}-{SEQ}-V{VER}
```

Example:

```text
CEL-CLDNTA-S01-GAP-SV-CSC-001-V01
```

This code means Conscious Elite, Claude Ntahuga, session 01, Guest Asset Pack, Short Video - Cinematic Story Commentary, first asset, version 01.

The code must appear in:

- Control Tower rows;
- asset package cards;
- SceneSpec and Render Contract headers;
- Review Workbench;
- EvaluationReceipt panels;
- Telegram quick review;
- Publer draft metadata;
- memory admission records;
- downloaded/exported file names.

### 6.2 Pipeline Map

Purpose: make the factory readable end to end.

The pipeline page should visualize:

```text
Legacy Migration
-> Workspace / Consent / Brand Setup
-> Brand Genesis
-> Research / Context
-> Monthly Interview Brief
-> Interview Intelligence
-> Complete Expression Session
-> Extraction
-> Routing / Package Planning
-> Complete Editing Session
-> Scene / Composition / Assets
-> Rendering
-> Evaluation / Review / Approval
-> Publishing
-> Memory / Neo4j Projection
```

Each stage tile must show:

- active object count;
- blocked object count;
- responsible department and agents;
- required input objects;
- emitted output objects;
- required receipts;
- common failure codes.

Clicking a stage opens a filtered work queue. Clicking an object opens its detail page.

### 6.3 Brand Genesis Workspace

Purpose: lock a reusable creative universe before production.

Required views:

- Brand Genesis session overview;
- consent and source media quality;
- Brand Context Version inspector;
- 64-state acting library review;
- paper-cut rig review;
- micro-semiotic anchor library;
- Voice DNA and Emotional DNA panels;
- repair/reject/approve/lock controls.

The Brand Context lock must be visually distinct. Downstream production pages must show which locked version they consume.

### 6.4 Research and Context Workspace

Purpose: turn evidence into interview-useful pressure.

Required views:

- CRAL/SCRE research snapshot;
- evidence list with provenance, quality, recency, and fact/inference type;
- Guest Dossier;
- Audience Reality Brief;
- Context Premise candidates;
- Audience Deep Trigger Map;
- claim safety review;
- cultural/semiotic notes;
- adversarial evidence critique.

The UI must separate evidence from inference. Unsupported claims must appear as blockers or review notes, not as normal content.

### 6.5 Interview Preparation and Live Guidance

Purpose: support better source expression before editing exists.

For the normal monthly cycle, this is the first production artifact surface. The Operator starts by generating the Monthly Interview Brief / Interview Asset Contract pack. Package planning, editing, rendering, and publishing are downstream of the interview unless the guest already has an existing interview and no new interview will be conducted.

Required preparation views:

- Interviewer Resonance Context;
- Matrix of Edging pressure map;
- Narrative State Map;
- First-Line Anchors;
- Depth Anchors;
- Interview Asset Contracts;
- recording setup checklist;
- consent and source capture readiness.

Alternate entry path:

- existing interview transcript/video ingestion is available only when no new interview will be conducted;
- the UI must label this as a fallback source-ingestion path, not the default monthly entry path;
- existing-interview ingestion still flows through transcript alignment, Expression Moment extraction, routing, evals, review, and package planning.

Live guidance must be calm and sparse:

- current anchor;
- follow-up suggestion;
- repair prompt for shallow or centroid answers;
- source/capture health;
- timestamp marker;
- consent status;
- session quality warning.

Live guidance must not overwhelm the human interview. It should support presence, not replace it.

### 6.6 Extraction and Expression Moment Review

Purpose: convert transcript and source artifacts into routable expression.

Required views:

- transcript and source media side by side;
- expression moment candidate list;
- quote boundaries and timestamps;
- anchor hit evidence;
- guest-level induction rationale;
- transcript-level extraction rationale;
- primitive activations and coalition candidates;
- JIT Skill invocation record;
- approve, split, merge, annotate, hold, or reject controls.

Each Expression Moment card should show:

- source quote;
- timestamp range;
- routeability score;
- depth and anti-centroid status;
- primitive refs;
- claim safety status;
- linked Interview Asset Contract;
- extraction receipt.

### 6.7 Routing and Package Planner

Purpose: decide what valid assets should be produced.

Required views:

- archetype route candidates;
- derivative routes: short video, carousel, visual poll, tweet-like quote, meme, Super Visual, reaction seed, CMF render mode;
- Guest Asset Pack plan;
- Monthly Asset Engine plan;
- unsupported route warnings;
- package feasibility and dependencies.

The format selector must only show valid CMF formats. Newsletters must not appear.

Required content-format families:

| Family | Codes | UI representation |
|---|---|---|
| Short Videos | `SV-CSC`, `SV-EDU`, `SV-FRB`, `SV-RRC` | four required video slots when source supports them |
| Carousels | `CAR-LST`, `CAR-JUX` | multi-slide package lane |
| Visual Polls | `VPL-WYR`, `VPL-VRS` | choice/poll package lane |
| Tweet-Like Quotes | `TWQ-STD`, `TWQ-IMG` | quote card package lane |
| Memes | `MEM-INC`, `MEM-REL` | meme mechanism package lane |
| Super Visuals | `SPV-CON`, `SPV-SYM`, `SPV-PRM` | premium single-frame visual lane |
| Reaction Seeds | `RCT-SEED` | reaction package lane |

The four short-video formats are:

- Cinematic Story Commentary;
- Educational Explainer;
- Challenger / Frame Breaker;
- Reaction / Recognition Clip.

The package planner must show missing, ready, blocked, in production, in review, approved, published, or skipped-with-reason states per format slot.

### 6.8 Complete Editing Session and SceneSpec Lab

Purpose: preserve why an asset exists and how it should be produced.

Required views:

- Complete Editing Session overview;
- source expression lineage;
- route receipt;
- locked Brand Context Version;
- SceneSpec editor/viewer;
- Creative State inspector;
- Render Contract inspector;
- revision policy;
- evaluation requirements;
- scene containers, components, subsystems, and asset-roll plan.

SceneSpec UI must treat source lineage, Brand Context Version, route, and eval requirements as non-optional.

### 6.9 Composition and Asset Workbench

Purpose: coordinate composition, visual research, provider outputs, and layer manifests.

Required views:

- Ideogram 4 `CompositionJob` JSON viewer;
- composition plate preview;
- composition analysis;
- text-space and identity-boundary warnings;
- SVRE/Aurore visual research query;
- visual candidates with source, license, symbolic role, emotional mode, brand fit, and direct-use/composition-reference status;
- provider job queue;
- asset candidate scoring;
- layer manifest.

The UI must preserve the CompositionJob JSON structure. It should be inspectable, diffable across revisions, and linked to downstream provider jobs and render outputs.

### 6.10 Provider, GPU Worker, and Render Operations

Purpose: make external and deterministic execution visible and recoverable.

Required views:

- provider capability registry;
- provider job list with status, inputs, outputs, prompt hash, model/workflow version, cost, retries;
- self-hosted ComfyUI Docker worker queue;
- GPU tier, cloud provider, Docker image, workflow hash, checkpoint, cost, shutdown state;
- Remotion and Motion Canvas render jobs;
- audio, caption, timeline, EDL, and mix lineage;
- retry, resume, cancel, compensate, or quarantine controls.

RunningHub must not appear as an execution route. The ComfyUI route is self-hosted Docker on AWS or Google Cloud with 24GB or 32GB VRAM.

### 6.11 Eval Workbench

Purpose: make quality gates visible before review and approval.

Required views:

- eval target selection;
- eval run queue;
- receipt inspector;
- primitive failure inspector;
- blocker panel;
- review read model link.

The canonical chain is:

```text
Eval registries
-> eval target selection
-> eval run command
-> EvaluationReceipt
-> approval blocker
-> review read model
```

Primitive failure cards must include:

- primitive ref or family;
- source evidence refs;
- expected activation;
- observed failure;
- related Matrix pass;
- related route or SceneSpec;
- approval blocker code;
- repair recommendation.

The Workbench must not score locally or approve from evaluator output alone.

### 6.12 Evidence-Rich Review Workbench

Purpose: help reviewers make grounded decisions.

Required panels:

- preview;
- source quote;
- transcript segment;
- timestamp;
- archetype route;
- Brand Context Version;
- selected assets;
- render output;
- evaluation receipts;
- primitive failures;
- consent state;
- revision history;
- approval blockers;
- repair recommendations.

Primary commands:

- approve;
- reject;
- request revision;
- escalate;
- request eligible Voice-DNA Boost;
- hold for consent/source repair.

Approval must be disabled when hard blockers exist. The disabled state must explain the blocker and show the required repair action.

### 6.13 Publishing Intent Desk

Purpose: schedule only approved assets through Publer.

Required views:

- approved asset;
- platform variants;
- caption and metadata;
- schedule proposal;
- Publer draft/job state;
- publishing receipt;
- duplicate scheduling warning;
- final human confirmation.

Publer is an adapter. The UI must not imply Publer owns approval or canonical publishing truth.

### 6.14 Memory and Neo4j Projection Workspace

Purpose: admit useful evidence-backed memory and inspect relationships.

Required views:

- memory candidate queue;
- evidence refs;
- confidence;
- consent compatibility;
- route and review outcome;
- correction, reversal, expiry, quarantine commands;
- Neo4j projection status;
- graph relationship explorer;
- projection lag, checkpoint, rebuild controls.

Graph views are inspection surfaces. Any state-changing action must return to Command Bus-backed commands.

### 6.15 Agent Factory Workbench

Purpose: make agent intelligence and authority inspectable.

Required views:

- department registry;
- persona code registry;
- AgentRoleSpec catalog;
- SubAgentRoleSpec catalog;
- hook registry;
- extension registry;
- stable skill and JIT skill bindings;
- tool capability registry;
- eval bindings;
- readiness eval findings;
- ADK/Agents CLI adapter export and drift status.

Every agent detail page must show:

- persona code;
- display name;
- department;
- goal;
- fit rationale;
- active object scope;
- entry objects;
- exit objects;
- allowed tools;
- blocked actions;
- stable skills;
- JIT skill modes;
- sub-agent bindings;
- hook bindings;
- memory policy;
- eval obligations;
- required receipts;
- readiness eval status;
- generated adapter hash.

The Agent Factory UI must make it obvious that agents are not prompts. They are accountable runtime contracts.

### 6.16 Operations Board

Purpose: recover the system without hidden scripts.

Required views:

- workflow queue;
- provider failures;
- render failures;
- worker availability;
- cost pressure;
- stale objects;
- failed hooks;
- failed evals;
- recovery actions;
- operational readiness checks;
- restore drills and projection rebuild status.

Recovery commands must record receipts and preserve lineage.

## 7. Telegram Operator Cockpit

Telegram is a compact leaf surface. It can notify, summarize, and accept low-risk quick actions only when evidence sufficiency permits.

Telegram payloads must include:

- preview when available;
- object type and ID;
- brand and route;
- source snippet;
- consent status;
- evaluation summary;
- blocker status;
- required action;
- current object version;
- PWA deep link.

Telegram must deep-link to PWA when:

- evidence is conflicting;
- hard blockers exist;
- consent changed;
- source truth is disputed;
- identity or likeness evaluation fails;
- primitive failure requires inspection;
- approval would be public or high-risk;
- object state changed after notification.

Telegram quick actions must use the same Command Bus, role checks, idempotency, and receipt writing as PWA.

## 8. State, Commands, and Receipts

### 8.1 UI State Model

UI state should be generated from backend read models, not recreated locally.

Required read model families:

| Read Model | Surface |
|---|---|
| `WorkspaceControlTowerState` | Control Tower |
| `GuestWorkspaceState` | Guest/client management |
| `PipelineStageReadModel` | Pipeline map and stage queues |
| `BrandContextReviewState` | Brand Genesis |
| `InterviewPreparationState` | Interview prep |
| `LiveInterviewGuidanceState` | Live guidance |
| `ExpressionMomentReviewState` | Extraction |
| `AssetPackagePlanningState` | Packages |
| `ContentAssetFormatRegistryState` | Content format selector and package lanes |
| `CompleteEditingSessionState` | SceneSpec Lab |
| `CompositionAssetWorkbenchState` | Composition and asset research |
| `ProviderRenderOpsState` | Provider/render operations |
| `EvalWorkbenchState` | Eval Workbench |
| `ReviewEvidenceState` | Review Workbench |
| `PublishingIntentState` | Publishing Intent |
| `MemoryProjectionState` | Memory and Neo4j |
| `AgentFactoryState` | Agent Factory |
| `OperationsBoardState` | Operations |

### 8.2 Command Pattern

Every state-changing UI action should follow:

```text
user action
-> command preview
-> role and state validation
-> submit command
-> optimistic pending state only when safe
-> command result
-> receipt link
-> updated read model
```

Dangerous or public actions require explicit confirmation:

- approval;
- publishing intent confirmation;
- consent changes;
- Brand Context lock;
- memory admission;
- worker shutdown;
- destructive recovery;
- adapter activation;
- agent activation.

### 8.3 Receipt Trail

Every object page should include a receipt trail drawer with:

- command receipts;
- stage execution receipts;
- skill invocation records;
- provider job receipts;
- render receipts;
- evaluation receipts;
- review decisions;
- approval events;
- publishing receipts;
- memory admission receipts;
- projection events.

Every receipt shown in UI should include both internal IDs and readable codes when available, especially `content_asset_id`, `content_asset_code`, `brand_workspace_code`, `guest_code`, `format_family_code`, `format_subtype_code`, and `asset_version`.

## 9. Visual and Interaction Direction

CMF Studio should use a restrained operational interface:

- neutral base;
- high-contrast text;
- semantic status colors;
- compact tables and inspector panels;
- icons for repeated tools and commands;
- stable dimensions for boards, cards, counters, and controls;
- no decorative hero pages, gradient orbs, or marketing composition;
- previews should show real output, not atmospheric placeholders;
- page sections should be unframed layouts or full-width bands, with cards reserved for repeated objects, modals, and framed tools.

Suggested visual language:

| Token | Direction |
|---|---|
| Radius | 6px to 8px for cards and panels |
| Typography | compact interface scale, no viewport-scaled type |
| Layout | left rail, top object header, inspector drawers, resizable split panes |
| Status | neutral, ready, running, blocked, failed, review-ready, approved, superseded |
| Data density | tables for queues, cards for object candidates, drawers for evidence |
| Motion | subtle state changes only; avoid expressive animation in work surfaces |

## 10. Accessibility and Responsiveness

Accessibility requirements:

- all review, approval, rejection, revision, and publishing confirmation actions must be keyboard accessible;
- status must not rely on color alone;
- evaluation receipts must be readable text artifacts;
- dense tables need row focus, filters, and screen-reader labels;
- destructive or public actions need clear confirmation and recovery status;
- long transcript/evidence views need anchors, search, and timestamp navigation.

Responsive requirements:

| Viewport | Behavior |
|---|---|
| Desktop | full Control Tower, split panes, tables, inspectors, side-by-side source/review |
| Tablet | collapsible rail, stacked inspectors, preserved primary actions |
| Mobile PWA | object status, focused review, simple commands, deep links |
| Telegram | compact notification and quick action only |

Complex evidence review remains PWA-first. Telegram cannot replace the Review Workbench.

## 11. Surface-To-Story Trace

| UX Surface | Story / Spec Anchors |
|---|---|
| Control Tower | Story 1.2, Story 1.5, Story 1.6, TS-CMF-004 |
| Guest Workspace Management | PRD-CMF-03.01, PRD-CMF-06, content asset code registry |
| Pipeline Map | Story 1.6, TS-CMF-002 |
| Role and Command UI | Story 1.3, TS-CMF-005 |
| Commercial Display | Story 1.4, TS-CMF-006 |
| Consent and Source Review | Story 2.5, TS-CMF-012 |
| Legacy/Migration Workbench | Story 3.1, Story 3.2, Story 3.5 |
| JIT Skill Governance | Story 3.3, Story 11.5, TS-CMF-015, TS-CMF-066 |
| Brand Genesis | Epic 4, PRD-CMF-05 |
| Research and Context | Epic 5, PRD-CMF-06, TS-CMF-028 |
| Interview and Live Guidance | Epic 5, Epic 6, PRD-CMF-06 |
| Expression Moment Review | Story 6.4 |
| Content Format Registry and Asset Codes | Story 6.5, Story 6.6, Story 9.4, content asset code registry |
| SceneSpec and Composition | Epic 7, PRD-CMF-07, TS-CMF-037 |
| Ideogram CompositionJob | Story 7.3, PRD-CMF-07.03 |
| Provider and ComfyUI Ops | Epic 8, TS-CMF-045, TS-CMF-046 |
| Eval Workbench | Story 9.1, TS-CMF-050, eval architecture doc |
| Review Workbench | Story 9.2, Story 9.3, Story 9.4, TS-CMF-051 |
| Telegram Quick Review | Story 9.6, TS-CMF-055 |
| Publishing Intent | Story 9.5 |
| Memory Review | Story 10.2 |
| Neo4j Projection | Story 10.3 |
| Operations Board | Story 10.4, Story 10.5, Story 10.6 |
| Agent Factory | Epic 11, TS-CMF-062 through TS-CMF-069 |

## 12. Implementation Handoff

The UI should be implemented after generated TypeScript contracts exist for the relevant backend Pydantic objects. Frontend components should consume read models and command contracts rather than inventing local domain models.

Initial UI build order:

1. App shell, auth, brand scope, generated contract client.
2. Guest workspace management and active brand/guest scope selector.
3. Control Tower read model with Monthly Interview Brief as the primary monthly entry action.
4. Research, Context Premise, Matrix of Edging, and Interview Brief preparation.
5. Pipeline stage map and object queues.
6. Existing-interview transcript/video ingestion fallback for cycles without a new interview.
7. Expression moment review and transcript/source alignment.
8. Asset Package board with content-format lanes.
9. Evidence-rich review surface and eval receipt viewer.
10. Telegram deep-link parity for review.
11. Agent Factory registry inspector.
12. Provider/render operations board.
13. SceneSpec and composition workbench.
14. Memory/projection and recovery surfaces.

This is a build order, not a reduced product scope. The full documented system remains the release target.

## 13. UX Acceptance Criteria

- PWA and Telegram render the same canonical object state, command IDs, brand ID, role checks, and receipts.
- Control Tower shows brand status, roles, entitlement, recent commands, blockers, and production health.
- Control Tower shows the Monthly Interview Brief as the primary monthly artifact and labels existing-interview transcript/video ingestion as the fallback path for cycles with no new interview.
- Guest workspaces isolate consent, sessions, source artifacts, packages, content assets, approvals, publishing intents, and memory per guest.
- Every content asset displays a readable content asset code with brand, guest, session, package, format, sequence, and version.
- Package Planner represents short videos, carousels, visual polls, tweet-like quotes, memes, Super Visuals, and reaction seeds as distinct valid format families.
- The four short-video slots are Cinematic Story Commentary, Educational Explainer, Challenger / Frame Breaker, and Reaction / Recognition Clip.
- Every object detail page shows active object, stage, validation contract, responsible agent/service, required receipt, blockers, and next valid actions.
- Review pages expose source quote, transcript segment, timestamps, route, Brand Context Version, selected assets, render output, evaluation receipts, revisions, and consent state.
- Approval is disabled when lineage, consent, source truth, identity, evaluation, platform, or format blockers exist.
- Telegram cannot approve complex or conflicting review states.
- Eval Workbench exposes target selection, run queue, receipt history, primitive failures, blockers, and review read model links.
- Agent Factory pages show persona code, role contract, tools, skills, memory policy, eval obligations, receipts, and readiness eval status.
- Ideogram 4 `CompositionJob` JSON remains inspectable and linked to downstream composition/render lineage.
- Pricing UI shows only `$29/week` trial Guest Asset Pack and `$99/month` Monthly Asset Engine.
- Unsupported formats, including newsletters, do not appear in route/package selection.
- Neo4j graph views are marked as projections and cannot mutate canonical state directly.

## 14. Open UX Decisions

These should be resolved through future Grill-Me UX passes:

1. Whether the first Control Tower default view should prioritize active blockers, active sessions, or review queue.
2. Whether the first Control Tower default should group by brand, guest, pipeline stage, or content-format lane.
3. How much live interview guidance should be visible without distracting the Operator.
4. Whether SceneSpec editing should be form-first, split-pane JSON-first, or visual-inspector-first.
5. Which Agent Factory readiness findings need to appear in the main Control Tower.
6. Which Telegram quick-review object types are safe enough for in-chat decisions.
