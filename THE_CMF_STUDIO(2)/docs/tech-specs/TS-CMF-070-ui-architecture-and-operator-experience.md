---
tech_spec_id: "TS-CMF-070"
title: "UI Architecture and Operator Experience"
story_id: "cross-cutting-ui-architecture"
story_title: "Operator Experience UI Architecture"
epic_id: "cross-cutting"
epic_title: "PWA, Telegram, Review, Agent Factory, and Operator Surfaces"
status: "ready-for-development"
created_at: "2026-06-22"
source_story: "THE CMF STUDIO/docs/ux/ux-design-specification.md"
fr_ids:
  - "FR-CMF-01"
  - "FR-CMF-02"
  - "FR-CMF-05"
  - "FR-CMF-06"
  - "FR-CMF-09"
  - "FR-CMF-10"
module_requirement_ids:
  - "PRD-CMF-03.01"
  - "PRD-CMF-03.02"
  - "PRD-CMF-03.03"
  - "PRD-CMF-06.07"
  - "PRD-CMF-06.08"
  - "PRD-CMF-06.09"
  - "PRD-CMF-06.10"
  - "PRD-CMF-10.00"
  - "PRD-CMF-10.01"
  - "PRD-CMF-10.02"
pipeline_stage: "operator UI overlay across stages 1-14"
entry_object: "scoped operator session"
exit_object: "governed UI state and command submission"
validation_contract: "brand/guest scope, generated contracts, command parity, receipt visibility"
required_receipt: "UiStateBuildReceipt / UiActionReceipt / linked domain receipt"
runtime_target: "TypeScript PWA, Telegram Mini App leaf surface, generated TypeScript contracts, FastAPI read models"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-070 - UI Architecture and Operator Experience

## 1. Files Read

- `THE CMF STUDIO/docs/ux/ux-design-specification.md`
- `THE CMF STUDIO/docs/content-asset-code-and-format-registry.md`
- `THE CMF STUDIO/docs/prd/modules/PRD_CMF_03_Workspace_Commercial_Consent_Source.md`
- `THE CMF STUDIO/docs/prd/modules/PRD_CMF_06_Interview_Expression_Routing.md`
- `THE CMF STUDIO/docs/prd/modules/PRD_CMF_10_Agent_Factory_Runtime.md`
- `THE CMF STUDIO/docs/tech-specs/README.md`
- `THE CMF STUDIO/docs/tech-specs/TS-CMF-004-organization-and-brand-workspace-lifecycle.md`
- `THE CMF STUDIO/docs/tech-specs/TS-CMF-007-pwa-and-telegram-state-parity.md`
- `THE CMF STUDIO/docs/tech-specs/TS-CMF-034-guest-asset-pack-spec-generation.md`
- `THE CMF STUDIO/docs/tech-specs/TS-CMF-051-evidence-rich-review-surface.md`
- `THE CMF STUDIO/docs/tech-specs/TS-CMF-055-telegram-quick-review-with-evidence.md`
- `THE CMF STUDIO/docs/tech-specs/TS-CMF-069-adk-agents-cli-adapter-export-and-drift-gate.md`

## 2. Overview

The CMF Studio UI is an operator cockpit for a governed interview-first media factory. It is not a separate source of domain truth and it is not a generic content dashboard. The UI must make brand scope, guest scope, active object lineage, valid commands, blockers, receipts, and agent responsibility visible across the full pipeline.

The operator experience is built around this chain:

```text
organization
-> brand_workspace
-> guest
-> expression_session
-> asset_package
-> content_asset
-> asset_version
```

Every page, queue row, review panel, Telegram payload, export, and Publer draft must make enough of that chain visible for an operator to avoid confusing guests, brands, sessions, packages, and versions.

The UI has two first-class surfaces:

- PWA Control Tower: the full operating surface for workspace management, pipeline state, production, evaluation, review, publishing, memory, and Agent Factory inspection.
- Telegram Operator Cockpit: a compact leaf surface for notifications and safe quick actions, always backed by the same Command Bus, read models, role checks, and receipts as the PWA.

For the normal monthly production cycle, the UI must treat the Monthly Interview Brief / Interview Asset Contract pack as the first generated artifact. Existing interview transcript/video ingestion is an alternate source-ingestion entry path only when no new interview will be conducted. The Control Tower must not frame asset package generation, editing, or rendering as the first production action when a new interview is planned.

## 3. Context for Development

### 3.1 Requirement Trace

This spec implements the UX architecture required by:

- `PRD-CMF-03.01`: governed multi-brand workspace, guest workspace isolation, and active brand/guest context.
- `PRD-CMF-03.02`: role and command governance across PWA and Telegram.
- `PRD-CMF-03.03`: commercial policy limited to `$29/week` trial Guest Asset Packs and `$99/month` Monthly Asset Engine.
- `PRD-CMF-06.07`: dual-layer extraction from the guest and from transcript/source evidence.
- `PRD-CMF-06.08`: Expression Moment review with evidence, induction context, primitives, and route rationale.
- `PRD-CMF-06.09`: archetype and asset routing with readable content asset codes and valid format families.
- `PRD-CMF-06.10`: Guest Asset Pack planning without fabricated unsupported assets.
- `PRD-CMF-10.00`: persona code standard for agents, sub-agents, hooks, extensions, skills, registries, and evals.
- `PRD-CMF-10.01`: AgentRoleSpec visibility and runtime accountability.
- `PRD-CMF-10.02`: SubAgentRoleSpec visibility and delegation boundaries.

### 3.2 Pipeline Stage Trace

The UI overlays the canonical pipeline rather than owning it:

```text
Workspace / Consent / Brand Setup
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
-> Operations / Recovery / Agent Factory
```

Each surface must show:

- active stage;
- active object;
- responsible agent, service, extension, or human role;
- required validation contract;
- required receipt;
- open blockers;
- next valid commands.

### 3.3 Legacy Intelligence Mapping

The UI must preserve visibility for the legacy intelligence that makes CMF different from ordinary generative tooling:

- CRAL/SCRE research processes;
- Context Premise;
- Matrix of Edging;
- Emotional DNA and Voice DNA;
- Narrative State Induction;
- Interview Asset Contracts;
- Expression Moment extraction;
- primitive coalitions and quality standards;
- JIT Skill Compiler records;
- Ideogram 4 `CompositionJob` JSON lineage;
- SVRE/Aurore visual research;
- scene reproducibility and asset/render provenance;
- evidence-backed memory and Neo4j rebuildable projections.

These items are not hidden backend details. They must appear where they are operationally relevant: research, interview prep, extraction, routing, SceneSpec, composition, evaluation, review, Agent Factory, memory, and operations.

## 4. Architecture Principles

1. UI state is read-model state, not canonical domain state.
2. All state-changing actions go through the Command Bus or an approved durable workflow command.
3. PWA and Telegram use the same backend state, command contracts, role checks, idempotency keys, and receipt model.
4. Domain contracts are generated from backend source contracts. The frontend must not duplicate Pydantic domain models by hand.
5. Every mutating UI action returns a receipt or links to the domain receipt emitted by the underlying workflow.
6. Every view is scoped by organization, brand workspace, and, when relevant, guest.
7. Every content asset shows a readable content asset code in addition to internal IDs.
8. Review and approval controls are disabled when hard blockers exist.
9. Telegram can accelerate safe actions but cannot replace evidence-rich PWA review.
10. Agent Factory UI treats agents as accountable runtime contracts, not prompt cards.

## 5. Target UI Architecture

### 5.1 Runtime Layers

```text
Generated TypeScript Contracts
-> API and Read Model Client
-> Auth, Role, Brand, and Guest Scope Providers
-> Command Client and Receipt Queue
-> Event / Read Model Refresh Layer
-> Surface Modules
-> Evidence, Blocker, and Receipt Components
-> PWA Shell and Telegram Leaf Consumers
```

### 5.2 Layer Responsibilities

| Layer | Responsibility | Cannot Do |
|---|---|---|
| Generated TypeScript Contracts | Provide typed DTOs, commands, receipts, enums, and read models generated from backend contracts | Invent local domain truth |
| API and Read Model Client | Fetch scoped read models, submit commands, poll or subscribe for updates | Bypass scope, role, or command validation |
| Scope Providers | Hold active organization, brand workspace, guest, role, and session context | Infer cross-guest access implicitly |
| Command Client | Submit validated command envelopes with idempotency and correlation IDs | Mutate local state as if canonical |
| Receipt Queue | Display pending, succeeded, failed, and linked domain receipts | Hide failed or partial command outcomes |
| Surface Modules | Render Control Tower, Guests, Pipeline, Packages, Review, Evals, Agent Factory, Operations | Mix data from different brands or guests |
| Evidence Components | Render source quote, timestamps, transcript, consent, evals, primitive failures, render lineage | Approve or rewrite evidence |
| Telegram Leaf Consumers | Notify and perform safe quick actions through same command pathway | Approve complex/conflicting evidence states |

## 6. Information Architecture

### 6.1 Global Navigation

The PWA shell requires these primary sections:

| Section | Purpose |
|---|---|
| Control Tower | Workspace health, active work, blockers, receipts, running workflows, review queue |
| Guests | Brand-scoped guest/client workspaces, sessions, consent, assets, approvals, memory |
| Pipeline | Stage map, object queues, orchestration runs, validation contracts, responsible actors |
| Brand Genesis | Brand Context Version, acting library, rig, micro-semiotic anchors, locks |
| Research | CRAL/SCRE, source evidence, Context Premise, Audience Reality, claim safety |
| Interview | Interview prep, Matrix of Edging, Narrative State Induction, recording readiness |
| Extraction | Transcript/source alignment, Expression Moments, primitive activations, routeability |
| Packages | Guest Asset Packs, Monthly Asset Engine plans, valid content-format lanes |
| Production | Complete Editing Session, SceneSpec, CompositionJob, render contract, assets |
| Evals | Eval target selection, run queue, receipts, primitive failures, approval blockers |
| Review | Evidence-rich review, approvals, rejections, revision requests, Voice-DNA Boost requests |
| Publishing | Publishing Intent, platform variants, Publer adapter jobs, schedule receipts |
| Memory | Memory admission, corrections, rejections, Neo4j projection views |
| Agent Factory | Departments, persona codes, role specs, sub-agents, hooks, skills, evals, adapter exports |
| Operations | Workers, queues, provider failures, cost pressure, recovery actions, readiness checks |

### 6.2 Object Header Contract

Every detail surface must render a shared object header:

```yaml
object_header:
  organization_id: uuid
  brand_workspace_id: uuid
  brand_workspace_code: string
  guest_id: uuid | null
  guest_code: string | null
  active_object_type: string
  active_object_id: uuid
  active_object_code: string | null
  content_asset_code: string | null
  pipeline_stage_key: string
  lifecycle_state: string
  responsible_entity_code: string
  validation_contract_id: uuid | null
  required_receipt_type: string
  blocker_count: integer
  next_valid_commands: CommandActionSummary[]
```

If a page cannot render its object header, it must not render production actions.

## 7. Core Read Models

### 7.1 OperatorShellState

```yaml
OperatorShellState:
  operator_user_id: uuid
  active_role_key: string
  organization_scope:
    organization_id: uuid
    organization_name: string
  active_brand_workspace:
    brand_workspace_id: uuid
    brand_workspace_code: string
    display_name: string
    status: active | suspended | archived
  active_guest:
    guest_id: uuid | null
    guest_code: string | null
    display_name: string | null
  navigation_sections: SurfaceRouteDefinition[]
  unread_notifications: integer
  pending_receipts: UiReceiptSummary[]
  blocking_alerts: BlockerSummary[]
  generated_contract_version: string
```

### 7.2 BrandGuestScopeState

```yaml
BrandGuestScopeState:
  organization_id: uuid
  brand_workspace_id: uuid
  brand_workspace_code: string
  guest_id: uuid | null
  guest_code: string | null
  expression_session_id: uuid | null
  asset_package_id: uuid | null
  content_asset_id: uuid | null
  scope_kind: organization | brand_workspace | guest | session | package | asset
  scope_is_commandable: boolean
  scope_blockers: BlockerSummary[]
```

### 7.3 WorkspaceControlTowerState

```yaml
WorkspaceControlTowerState:
  shell: OperatorShellState
  commercial_summary:
    allowed_customer_offers:
      - "$29/week trial Guest Asset Pack"
      - "$99/month Monthly Asset Engine"
    forbidden_offer_warnings: string[]
  monthly_entry_artifact: interview_brief
  primary_monthly_command_type: generate_monthly_interview_brief
  fallback_entry_artifact: existing_interview_transcript_video
  fallback_entry_rule: "Use existing interview transcript/video ingestion only when no new interview will be conducted."
  pipeline_stage_summaries: PipelineStageSummary[]
  active_guest_workspaces: GuestWorkspaceSummary[]
  active_asset_packages: AssetPackageSummary[]
  review_queue: ReviewQueueSummary
  evaluation_queue: EvaluationQueueSummary
  provider_render_queue: ProviderRenderQueueSummary
  agent_activity: AgentActivitySummary[]
  recent_commands: CommandReceiptSummary[]
  stale_or_blocked_objects: BlockerSummary[]
```

### 7.4 GuestWorkspaceState

```yaml
GuestWorkspaceState:
  brand_workspace_id: uuid
  brand_workspace_code: string
  guest_id: uuid
  guest_code: string
  display_name: string
  consent_state: ConsentStateSummary
  source_artifacts: SourceArtifactSummary[]
  voice_dna_refs: string[]
  emotional_dna_refs: string[]
  interview_briefs: InterviewBriefSummary[]
  expression_sessions: ExpressionSessionSummary[]
  interview_asset_contracts: InterviewAssetContractSummary[]
  expression_moments: ExpressionMomentSummary[]
  asset_packages: AssetPackageSummary[]
  content_assets: ContentAssetSummary[]
  approvals: ApprovalSummary[]
  publishing_intents: PublishingIntentSummary[]
  memory_entries: MemoryEntrySummary[]
  blockers: BlockerSummary[]
```

### 7.5 ContentAssetCodeParts

```yaml
ContentAssetCodeParts:
  brand_workspace_code: string
  guest_code: string
  session_code: string
  package_code: GAP | MAE | CUS
  format_code: string
  sequence_number: string
  version_number: string
  rendered_code: string
```

The rendered code format is:

```text
{BRD}-{GST}-{SES}-{PKG}-{FMT}-{SEQ}-V{VER}
```

Example:

```text
CEL-CLDNTA-S01-GAP-SV-CSC-001-V01
```

### 7.6 ContentAssetFormatRegistryState

```yaml
ContentAssetFormatRegistryState:
  format_families:
    - family_code: SV
      display_name: Short Video
      subformats:
        - code: SV-CSC
          display_name: Cinematic Story Commentary
        - code: SV-EDU
          display_name: Educational Explainer
        - code: SV-FRB
          display_name: Challenger / Frame Breaker
        - code: SV-RRC
          display_name: Reaction / Recognition Clip
    - family_code: CAR
      display_name: Carousel
    - family_code: VPL
      display_name: Visual Poll
    - family_code: TWQ
      display_name: Tweet-Like Quote
    - family_code: MEM
      display_name: Meme
    - family_code: SPV
      display_name: Super Visual
    - family_code: RCT
      display_name: Reaction Seed
  forbidden_formats:
    - newsletter
```

### 7.7 AssetPackageBoardState

```yaml
AssetPackageBoardState:
  brand_workspace_id: uuid
  guest_id: uuid
  asset_package_id: uuid
  package_code: GAP | MAE | CUS
  package_display_name: string
  expression_session_id: uuid | null
  route_receipt_id: uuid
  lanes: ContentFormatLane[]
  unsupported_or_skipped_assets: SkippedAssetSummary[]
  readiness_state: draft | ready | blocked | in_production | in_review | approved | published
  blockers: BlockerSummary[]
```

### 7.8 ReviewEvidenceState

```yaml
ReviewEvidenceState:
  review_object_id: uuid
  review_object_type: string
  content_asset_code: string | null
  brand_context_version_id: uuid | null
  source_quote: string | null
  transcript_timestamp_range: string | null
  source_artifact_refs: string[]
  expression_moment_id: uuid | null
  route_receipt_id: uuid | null
  scene_spec_id: uuid | null
  composition_job_id: uuid | null
  render_output_id: uuid | null
  evaluation_receipts: EvaluationReceiptSummary[]
  primitive_failures: PrimitiveFailureSummary[]
  consent_state: ConsentStateSummary
  approval_blockers: BlockerSummary[]
  next_valid_review_commands: CommandActionSummary[]
```

### 7.9 AgentFactoryState

```yaml
AgentFactoryState:
  departments: DepartmentSummary[]
  agents: AgentRoleSpecSummary[]
  sub_agents: SubAgentRoleSpecSummary[]
  hooks: HookSpecSummary[]
  extensions: ExtensionSpecSummary[]
  skills: SkillBindingSummary[]
  jit_skill_modes: JitSkillModeSummary[]
  eval_bindings: EvalBindingSummary[]
  adapter_exports: AdapterExportSummary[]
  readiness_findings: AgentReadinessFindingSummary[]
```

## 8. Command and Receipt Contracts

### 8.1 UiCommandEnvelope

```yaml
UiCommandEnvelope:
  command_id: uuid
  idempotency_key: string
  correlation_id: uuid
  requested_by_user_id: uuid
  requested_role_key: string
  organization_id: uuid
  brand_workspace_id: uuid
  guest_id: uuid | null
  active_object_type: string
  active_object_id: uuid
  command_type: string
  command_payload: object
  source_surface: pwa | telegram
  source_route: string
  generated_contract_version: string
  expected_object_version: string | null
```

### 8.2 UiActionReceipt

```yaml
UiActionReceipt:
  receipt_id: uuid
  command_id: uuid
  correlation_id: uuid
  source_surface: pwa | telegram
  status: accepted | rejected | failed | succeeded | linked_to_domain_receipt
  domain_receipt_id: uuid | null
  domain_receipt_type: string | null
  active_object_type: string
  active_object_id: uuid
  content_asset_code: string | null
  validation_results: ValidationResultSummary[]
  blockers: BlockerSummary[]
  emitted_events: EventSummary[]
  created_at: datetime
```

### 8.3 UiStateBuildReceipt

```yaml
UiStateBuildReceipt:
  receipt_id: uuid
  read_model_name: string
  organization_id: uuid
  brand_workspace_id: uuid
  guest_id: uuid | null
  source_event_checkpoint: string
  contract_version: string
  projection_version: string
  build_status: current | stale | partial | failed
  missing_dependencies: string[]
  created_at: datetime
```

Read model build receipts are useful for debugging stale UI state. They do not replace domain receipts.

## 9. Surface Implementation Requirements

### 9.1 App Shell and Scope

The app shell must:

- require organization and brand workspace before production data loads;
- show active brand workspace and active guest when a guest-scoped object is open;
- prevent commands when scope is missing, stale, or mismatched;
- show role, commandability, and generated contract version;
- expose receipt drawer globally;
- expose content asset code search globally.

### 9.2 Control Tower

The Control Tower must show:

- active workspace status;
- active guest/client context when selected;
- primary monthly artifact: `Interview Brief`;
- primary monthly command: `generate_monthly_interview_brief`;
- fallback existing-interview ingestion path, labeled as available only when no new interview will be conducted;
- commercial entitlement display limited to `$29/week` and `$99/month`;
- pipeline stage health;
- blockers by severity;
- stale objects;
- active workflows and agents;
- review queue;
- eval queue;
- provider/render queue;
- recent commands and receipts.

It must not show unsupported tiers, credit systems, newsletter offers, generic content packages, or asset package generation as the first production action when a new interview is planned.

### 9.3 Guest Workspace

The Guest Workspace must isolate:

- consent state;
- source artifacts;
- sessions;
- Voice DNA and Emotional DNA references;
- Interview Asset Contracts;
- Expression Moments;
- Asset Package Specs;
- content assets;
- approvals;
- publishing intents;
- memory entries.

Cross-guest compilation requires explicit approved workflow state. A global loose asset list is not allowed as an operator default.

### 9.4 Pipeline Map

The Pipeline Map must render each canonical stage with:

- active object count;
- blocked object count;
- responsible department and agents;
- entry object types;
- exit object types;
- required receipts;
- common blocker codes;
- drill-down to filtered queues.

### 9.5 Package Planner

The Package Planner must render valid format lanes:

- short videos: `SV-CSC`, `SV-EDU`, `SV-FRB`, `SV-RRC`;
- carousels: `CAR-LST`, `CAR-JUX`;
- visual polls: `VPL-WYR`, `VPL-VRS`;
- tweet-like quotes: `TWQ-STD`, `TWQ-IMG`;
- memes: `MEM-INC`, `MEM-REL`;
- Super Visuals: `SPV-CON`, `SPV-SYM`, `SPV-PRM`;
- reaction seeds: `RCT-SEED`.

Each lane item must show content asset code, source Expression Moment, route receipt, readiness, blocker state, version, and review state.

### 9.6 Evidence-Rich Review

Review surfaces must show:

- preview;
- content asset code;
- brand and guest scope;
- source quote;
- transcript segment and timestamp;
- source artifact references;
- route receipt;
- Brand Context Version;
- SceneSpec and CompositionJob references when relevant;
- render output;
- evaluation receipts;
- primitive failures;
- consent state;
- revision history;
- approval blockers;
- next valid review commands.

Approval must be disabled when hard blockers exist. The disabled state must identify the blocker and required repair.

### 9.7 Eval Workbench

The Eval Workbench must show:

- eval target selection;
- eval run command;
- eval queue;
- EvaluationReceipt history;
- primitive failure inspector;
- approval blocker state;
- review read model link.

Primitives are the production quality standard. The UI must render primitive failures as first-class review evidence, not as hidden evaluator prose.

### 9.8 Composition and Production

Composition and production surfaces must show:

- Complete Editing Session;
- SceneSpec;
- Creative State;
- Render Contract;
- Ideogram 4 `CompositionJob` JSON;
- composition diffs across revisions;
- SVRE/Aurore visual research candidates;
- provider jobs;
- self-hosted ComfyUI Docker worker state;
- Remotion and Motion Canvas render jobs;
- provider job receipts;
- render receipts;
- asset lineage.

The UI must preserve and display `CompositionJob` JSON structure because it is a key reproducibility object.

### 9.9 Agent Factory

Agent Factory surfaces must show:

- department registry;
- persona code registry using `DDD-XXXXXXX-TT`;
- AgentRoleSpec catalog;
- SubAgentRoleSpec catalog;
- hook registry;
- extension registry;
- stable skill and JIT skill bindings;
- tool capability registry;
- eval bindings;
- readiness findings;
- ADK/Agents CLI adapter exports;
- adapter drift gates.

Every agent detail page must show:

- persona code;
- display name;
- production goal;
- fit rationale;
- active object scope;
- entry objects;
- exit objects;
- allowed tools;
- stable skills;
- JIT skill modes;
- sub-agent bindings;
- hooks;
- memory policy;
- blocked actions;
- eval obligations;
- required receipts;
- readiness status.

### 9.10 Telegram Operator Cockpit

Telegram messages must include:

- object type and ID;
- content asset code when applicable;
- brand and guest scope;
- source snippet;
- consent status;
- eval summary;
- blocker status;
- current object version;
- required action;
- PWA deep link.

Telegram must force PWA review when:

- hard blockers exist;
- evidence is conflicting;
- consent changed;
- identity or likeness evaluation fails;
- primitive failures require inspection;
- approval would be public or high-risk;
- object state changed after notification.

## 10. Backward Compatibility and Migration Fallback

- Existing PWA/Telegram surfaces must be wrapped behind the generated command and read-model contracts before adding new production actions.
- If generated TypeScript contracts are missing for a surface, the surface may render read-only placeholder state but cannot expose mutation commands.
- If a read model is stale, the UI must show stale status and block public approval, publishing, memory admission, and irreversible recovery commands.
- If Telegram and PWA state disagree, Telegram actions must be rejected and deep-link to the PWA object state.
- If content asset code generation fails, review, publishing, export, Publer scheduling, and memory admission must block until a valid readable code is generated.
- Neo4j graph views remain projections. Any graph-derived action must route through Command Bus-backed commands.

## 11. CBAR Constraint Pass

| Tension | Risk | Resolution Demand | Downstream Proof |
|---|---|---|---|
| Preview speed vs source truth | Operators approve attractive assets without checking evidence | Review UI keeps source, consent, evals, blockers, and receipts adjacent to preview | ReviewEvidenceState and ApprovalReceipt |
| Multi-brand velocity vs guest confusion | Assets are approved or published under wrong guest | Scope header, content asset code, guest workspace isolation, and command validation | BrandGuestScopeState and UiActionReceipt |
| Telegram convenience vs blind approval | Quick actions approve complex states without evidence | Telegram forces PWA for blockers, conflicts, consent changes, and public/high-risk approval | Telegram rejection receipt and PWA deep link |
| Frontend convenience vs canonical state | UI mutates state locally or invents domain types | Generated contracts, command client, read models, and receipt queue | Contract tests and command receipts |
| Agent autonomy vs prompt opacity | Agent outputs appear without responsibility or eval trail | Agent Factory UI shows role specs, tools, skills, memory policy, evals, receipts, and adapter hashes | Agent readiness findings and adapter export receipts |
| Format richness vs offer drift | UI exposes unsupported formats or extra pricing | Content-format registry controls lanes; pricing display is limited to two approved offers | Format registry snapshot and entitlement read model |

## 12. Tasks

1. Add generated TypeScript contract package consumption for UI DTOs, commands, receipts, enums, and read models.
2. Implement shell-level auth, role, organization, brand workspace, and guest scope providers.
3. Implement Command Client with idempotency keys, correlation IDs, generated contract version, expected object version, and receipt handling.
4. Implement global receipt drawer and stale read-model warnings.
5. Implement Control Tower using `WorkspaceControlTowerState`.
6. Implement Guest Workspace using `GuestWorkspaceState`.
7. Implement content asset code formatting and global search.
8. Implement Package Planner lanes from `ContentAssetFormatRegistryState`.
9. Implement Evidence-Rich Review using `ReviewEvidenceState`.
10. Implement Eval Workbench primitive failure and blocker panels.
11. Implement Agent Factory registry and role-spec inspector.
12. Implement Telegram payload renderer and quick-action submitter using the same command envelope.
13. Add route guards that block production commands when brand, guest, version, consent, or contract state is invalid.
14. Add accessibility support for keyboard review, revision, approval, rejection, and publishing confirmation flows.

## 13. Acceptance Criteria

1. The PWA refuses to load production actions without organization and brand workspace scope.
2. Guest-scoped data never appears without brand and guest identifiers in the page header or object row.
3. Every content asset row and review view shows a readable content asset code when an asset exists.
4. Package Planner shows only valid CMF content formats and never shows newsletters.
5. Pricing UI shows only `$29/week` trial Guest Asset Pack and `$99/month` Monthly Asset Engine.
6. All mutating UI actions submit a `UiCommandEnvelope` and produce a `UiActionReceipt` or linked domain receipt.
7. Approval is disabled when consent, source truth, identity, evaluation, primitive, platform, format, or stale-state blockers exist.
8. Telegram quick actions use the same command pathway as PWA and reject stale or complex review states.
9. Agent Factory pages show persona code, role contract, tool access, skills, memory policy, eval obligations, required receipts, and readiness status.
10. Ideogram 4 `CompositionJob` JSON is inspectable, diffable across revisions, and linked to provider/render lineage.
11. UI domain types are generated from backend contracts or imported from generated contract packages; hand-authored duplicate domain models fail contract review.
12. Neo4j projection views cannot mutate canonical state directly.

## 14. Failure Examples

| Failure | Expected System Response |
|---|---|
| Operator opens a content asset from another brand through stale URL | UI shows scope mismatch and blocks commands |
| Telegram approval arrives after object version changed | Command rejected with stale object receipt and PWA deep link |
| Package Planner tries to add newsletter route | Format registry rejects route and UI shows unsupported format blocker |
| Review page lacks source quote or consent state | Approval controls disabled until read model is complete |
| Content asset lacks readable code | Review, publishing, export, Publer draft, and memory admission blocked |
| UI attempts direct write to read model endpoint | Endpoint rejects mutation and logs contract violation |
| Agent Factory adapter hash differs from active spec hash | Adapter activation blocked by drift gate |

## 15. Dependencies

- `TS-CMF-001-contract-kernel-command-spine.md`
- `TS-CMF-002-pipeline-stage-orchestration-records.md`
- `TS-CMF-004-organization-and-brand-workspace-lifecycle.md`
- `TS-CMF-005-role-based-production-permissions.md`
- `TS-CMF-007-pwa-and-telegram-state-parity.md`
- `TS-CMF-034-guest-asset-pack-spec-generation.md`
- `TS-CMF-050-evaluation-receipt-generation.md`
- `TS-CMF-051-evidence-rich-review-surface.md`
- `TS-CMF-053-approval-blockers.md`
- `TS-CMF-055-telegram-quick-review-with-evidence.md`
- `TS-CMF-062-persona-code-registry-and-validation.md`
- `TS-CMF-063-agentrolespec-and-departmentspec-runtime.md`
- `TS-CMF-064-subagentrolespec-and-delegation-boundaries.md`
- `TS-CMF-065-hookspec-and-extensionspec-lifecycle-contracts.md`
- `TS-CMF-066-skillbinding-and-jit-skill-mode-binding.md`
- `TS-CMF-067-agent-readiness-evals.md`
- `TS-CMF-068-pi-harness-tool-registry.md`
- `TS-CMF-069-adk-agents-cli-adapter-export-and-drift-gate.md`

## 16. Testing Strategy

### 16.1 Unit Tests

- content asset code rendering;
- scope provider behavior;
- route guards;
- command envelope creation;
- receipt queue state transitions;
- package lane filtering;
- blocker panel rendering;
- Telegram payload formatting;
- Agent Factory role-spec summary rendering.

### 16.2 Contract Tests

- generated TypeScript contracts match backend read-model and command schemas;
- UI command envelopes validate against backend command contract;
- read model snapshots validate against generated TypeScript types;
- forbidden local duplicate domain models are detected by lint or contract review.

### 16.3 Integration Tests

- PWA command submission -> Command Bus -> domain receipt -> read model refresh.
- Telegram quick action -> same Command Bus -> same validation -> receipt.
- brand/guest isolation across Control Tower, Guest Workspace, Package Planner, Review, and Publishing.
- approval blocker disables approval in PWA and rejects Telegram approval.
- stale read model blocks approval and publishing.

### 16.4 E2E Tests

- Operator selects brand workspace, opens guest, opens package, reviews content asset, requests revision, then sees receipt trail update.
- Reviewer attempts approval with primitive blocker and is blocked with repair action.
- Telegram message for stale object rejects quick approval and opens exact PWA object link.
- Agent supervisor opens Agent Factory, inspects agent role spec, sees readiness blocker, and cannot activate drifted adapter.

### 16.5 Accessibility Tests

- keyboard navigation through queues, detail pages, review actions, revision request, rejection, approval, and publishing confirmation;
- status labels are not color-only;
- receipt and blocker panels are screen-reader readable;
- focus returns to action source after modal confirmation or error.

## 17. Observability, Recovery, and Rollback

Every UI command log must include:

- source surface;
- route;
- organization ID;
- brand workspace ID;
- guest ID when present;
- active object type and ID;
- content asset code when present;
- command ID;
- idempotency key;
- correlation ID;
- expected object version;
- generated contract version;
- receipt ID;
- result status.

Recovery requirements:

- stale read-model banner with refresh and receipt inspection;
- failed command retry only when idempotency and backend state allow it;
- Telegram stale-action rejection with PWA deep link;
- generated contract rollback by version pin;
- feature flags for new surfaces without bypassing command validation;
- error boundary that preserves route, scope, and correlation ID for support.

## Doctrine-Driven Test Harness Binding

This spec must be verified through TS-CMF-077 before implementation is considered complete. The test plan for this spec must identify the documented doctrine sources it depends on, the operational invariants those sources imply, the primitive or eval obligations that apply to its outputs, and the negative fixtures that prove forbidden shortcuts are blocked. Passing tests must emit or validate the required receipt chain, and any hard failure must map to an approval blocker when this spec touches review, rendering, publishing, memory, agents, adapters, or operator actions.

Minimum binding requirements:

- cite source doctrine or registry refs used by this spec;
- declare contract, workflow, receipt, and read-model invariants;
- include at least one negative or drift fixture for every forbidden shortcut named in the spec;
- prove required receipts are emitted, immutable, reconstructable, and linked to pipeline stage state;
- expose failed doctrine, primitive, or eval obligations as blocker-ready test output.

## 18. Spec Audit Receipt

```yaml
spec_audit_receipt:
  spec_id: TS-CMF-070
  status: ready-for-development
  files_read_count: 12
  pipeline_trace_present: true
  legacy_inventory_considered: true
  cbar_pass_present: true
  generated_contract_requirement_present: true
  command_bus_requirement_present: true
  guest_workspace_isolation_present: true
  content_asset_code_requirement_present: true
  valid_format_registry_present: true
  telegram_parity_present: true
  agent_factory_visibility_present: true
  no_newsletters: true
  no_extra_pricing_offers: true
```
