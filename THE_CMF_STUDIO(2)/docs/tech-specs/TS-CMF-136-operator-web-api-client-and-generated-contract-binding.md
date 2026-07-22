---
tech_spec_id: "TS-CMF-136"
title: "Operator Web API Client and Generated Contract Binding"
story_id: "15.1"
story_title: "Bind the React Operator Web App to CMF Contracts"
epic_id: 15
epic_title: "Operator Operations Runtime and Agentic Control"
status: "ready-for-development"
created_at: "2026-06-26"
fr_ids:
  - "FR-CMF-01"
  - "FR-CMF-03"
  - "FR-CMF-07"
  - "FR-CMF-09"
  - "FR-CMF-10"
pipeline_stage: "operator surface, scope selection, command creation, review, and receipts"
entry_object: "OperatorShellState, WorkspaceControlTowerState, ReviewEvidenceState"
exit_object: "UiCommandEnvelope, UiActionReceipt, UiStateBuildReceipt"
validation_contract: "generated client parity, brand scope, guest scope, stale object detection, command envelope creation, receipt display"
required_receipt: "UiActionReceipt"
runtime_target: "React / TypeScript generated consumers / FastAPI / Pydantic v2 / Command Bus"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-136: Operator Web API Client and Generated Contract Binding

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Defines ERA3 spec structure and CBAR acceptance rules. |
| `THE CMF STUDIO/docs/architecture.md` | Defines CMF Python-first architecture, PWA/Telegram surfaces, Command Bus boundary, and 18-section protocol. |
| `THE CMF STUDIO/docs/tech-specs/README.md` | Shows the current dependency ledger and operator UI notes through TS-CMF-135. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-070-ui-architecture-and-operator-experience.md` | Parent operator-facing PWA, Telegram, command, receipt, guest workspace, review, eval, and Agent Factory UI architecture. |
| `THE CMF STUDIO/src/ccp_studio/api/v1/operator_ui.py` | Existing Operator UI FastAPI route owner. |
| `THE CMF STUDIO/src/ccp_studio/contracts/operator_ui.py` | Existing `OperatorShellState`, `WorkspaceControlTowerState`, `UiCommandEnvelope`, and `UiActionReceipt` contracts. |
| `THE CMF STUDIO/src/ccp_studio/services/operator_ui_service.py` | Existing service that creates UI command envelopes and action receipts. |
| `THE CMF STUDIO/src/ccp_studio/services/command_bus.py` | Command Bus boundary for all mutations. |
| `THE CMF STUDIO/operator-web/src/App.jsx` | Current React app shell, screens, local state, and mock action buttons. |
| `THE CMF STUDIO/operator-web/src/data.js` | Current mock data source that must become fixture/demo mode only. |
| `THE CMF STUDIO/operator-web/design-qa.md` | Records current frontend verification status and screenshot blocker. |

## 2. Overview

The first React Operator Web App gives CMF Studio a usable cockpit shape, but it is not yet a production surface. It reads from local mock data, changes state locally, and does not submit commands, refresh read models, or display immutable receipts from the backend. This spec turns the app into a true CMF operator surface by binding it to generated contract consumers and the existing FastAPI Operator UI routes.

The product rule is simple: an operator click is not a mutation. An operator click becomes a typed command proposal, then a `UiCommandEnvelope`, then a Command Bus submission, then a `UiActionReceipt`, then a read-model refresh. Local optimistic UI may show pending state, but it must never claim production success without a receipt.

This spec also protects guest and brand scope. Every guest needs a workspace and data boundary, and operators must not confuse one guest with another. The web app therefore must fetch `OperatorShellState` and `WorkspaceControlTowerState` from the backend, show active brand/guest scope in every commandable area, and block commands when the expected object version is stale or the selected object belongs to another workspace.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-136-001 | `OperatorWebApiClient` | Typed browser-side client for Operator UI endpoints. |
| DEP-CMF-136-002 | Generated contract package | TypeScript consumers generated from Pydantic/OpenAPI, not hand-maintained duplicate schemas. |
| DEP-CMF-136-003 | `OperatorShellState` | Source of truth for active operator, role, organization, brand workspace, guest, routes, notifications, and blockers. |
| DEP-CMF-136-004 | `WorkspaceControlTowerState` | Source of truth for control tower dashboard data. |
| DEP-CMF-136-005 | `UiCommandEnvelope` | Required envelope for every UI-originated command. |
| DEP-CMF-136-006 | `UiActionReceipt` | Required proof for accepted, rejected, failed, succeeded, or linked domain actions. |
| DEP-CMF-136-007 | `UiStateBuildReceipt` | Required proof that a UI read model was built from current source state. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `api/v1/operator_ui.py` | Add CORS-safe, auth-aware endpoints for all current app screens or confirm existing route coverage. |
| `services/operator_ui_service.py` | Provide production data instead of fixture-only responses. |
| `contracts/operator_ui.py` | Add missing fields required by the current React app only through Pydantic-first contract changes. |
| `operator-web/src` | Replace direct `data.js` imports with API calls and fixture fallback gated by environment. |
| `operator-web/src/api` | New API client and typed hooks. |

### ADR-05 Primitive Implementation

The UI must not invent its own primitive, doctrine, or blocker labels. It displays primitive/eval evidence from read models:

1. `ReviewEvidenceState.primitive_failures`.
2. `UiBlockerSummary`.
3. `EvaluationReceipt` summaries exposed by review/eval APIs.
4. Composition primitive triads when the active object is a composition-bearing asset.

### CBAR Mandate Enforcement

| CBAR Mandate | Implementation Rule |
|---|---|
| Phase1-M01 Optimistic Render | The UI may show pending state immediately after submission, but must label it as pending until a receipt returns. |
| Phase1-M05 Deterministic Override | A stale object version blocks mutation and forces read-model refresh. |
| Phase3-M04 Telemetry Surfacing | Command status, blockers, and receipts must be visible in the active workflow. |
| Phase4-M04 Frictionless Block | Blocked commands expose required action, not a dead button. |
| Phase4-M05 Actionable Rejection | Rejected command receipts include the reason and next valid command options. |
| Phase5-M01 Verifiable Artifact | Operator success state is backed by `UiActionReceipt` or linked domain receipt. |

## 4. PRD and FR-CMF Requirement Trace

| Requirement | Implementation Meaning |
|---|---|
| FR-CMF-01 | Enforce organization, brand workspace, role, commercial policy, and guest scope on every UI command. |
| FR-CMF-03 | Use generated contracts and spec governance, not hand-wired frontend schemas. |
| FR-CMF-07 | Display composition, render, and revision state only from canonical read models. |
| FR-CMF-09 | Surface eval, review, approval, rejection, and publishing blockers with receipts. |
| FR-CMF-10 | Feed operations, recovery, memory, and projection states into the operator cockpit. |

## 5. Canonical Pipeline Stage Trace

| Stage | UI Responsibility |
|---|---|
| Brand Context | Load locked brand and guest scope before command creation. |
| Research and Interview Brief | Show monthly Interview Brief as first artifact and block transcript-first shortcuts unless fallback rule applies. |
| Expression and Routing | Display source lineage, expression moments, and asset package route state. |
| Composition and Render | Display composition jobs, timing state, provider jobs, render state, and preview eligibility. |
| Eval and Review | Display primitive, doctrine, approval blockers, and next valid review commands. |
| Publishing and Memory | Display publishing intent and memory admission state after approval. |

## 6. Greenfield Integration and Legacy Migration Context

The legacy inventory remains a source of intelligence, not production runtime. The current React app is a greenfield surface under `THE CMF STUDIO/operator-web`. It must not import code or assets from `D:\Work\The Conscious Coaching Factory` directly. Any legacy visual references, reaction templates, or composition rules must arrive through CMF registries, contracts, or API read models.

## 7. Architecture Component Map

| Component | Owner | Build Obligation |
|---|---|---|
| `OperatorWebApiClient` | Frontend | Wrap GET/POST calls, attach auth headers, parse typed responses, surface API errors. |
| `GeneratedContracts` | Build tooling | Generate TypeScript types from FastAPI OpenAPI or Pydantic schema export. |
| `ScopeProvider` | Frontend | Maintain active `OperatorShellState`, brand workspace, guest, and object version. |
| `CommandClient` | Frontend | Create and submit `UiCommandEnvelope` via `/api/v1/operator-ui/commands` and `/submit`. |
| `ReceiptStore` | Frontend | Store and display pending receipts until read model refresh confirms state. |
| `FixtureMode` | Frontend | Keep `data.js` only for design demos and disconnected screenshots. |

## 8. Implementation Plan

1. Add `operator-web/src/api/client.ts` or `client.js` with base URL, auth header injection, typed request helpers, and error normalization.
2. Add generated contract build script: `npm run contracts:generate`, writing to `operator-web/src/generated/cmf-contracts`.
3. Add environment variables: `VITE_CMF_API_BASE_URL`, `VITE_CMF_FIXTURE_MODE`, and `VITE_CMF_CONTRACT_VERSION`.
4. Replace top-level `data.js` imports with hooks: `useOperatorShellState`, `useControlTowerState`, `useContentFormats`, `useReviewEvidence`, and `useAgentFactoryState`.
5. Add `ScopeProvider` and require active scope before commandable UI renders.
6. Convert action buttons to command creators: `New Interview Brief`, `Request Revision`, `Approve`, `Reject`, `Open Composition`, and `Run Eval`.
7. Add command preview modal showing active scope, command payload, expected object version, blockers, and receipt expectations.
8. Submit commands through `/api/v1/operator-ui/commands/submit`.
9. Show pending receipt state and refresh affected read model on terminal status.
10. Preserve mock data only behind fixture mode and label fixture mode visibly.

## 9. Primary Pydantic Output Schema

```python
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field

class OperatorWebClientConfig(BaseModel):
    schema_version: Literal["cmf.operator_web_client_config.v1"] = "cmf.operator_web_client_config.v1"
    api_base_url: str = Field(min_length=1)
    generated_contract_version: str = Field(min_length=1)
    fixture_mode_enabled: bool = False
    command_timeout_ms: int = Field(default=30000, ge=1000)
    event_stream_enabled: bool = True

class OperatorWebCommandDraft(BaseModel):
    schema_version: Literal["cmf.operator_web_command_draft.v1"] = "cmf.operator_web_command_draft.v1"
    draft_id: UUID
    command_type: str = Field(min_length=1)
    active_object_type: str = Field(min_length=1)
    active_object_id: UUID
    brand_workspace_id: UUID
    guest_id: UUID | None = None
    expected_object_version: str | None = None
    payload_preview: dict = Field(default_factory=dict)
    blocker_codes: list[str] = Field(default_factory=list)
    created_at: datetime

class OperatorWebReadModelBindingReceipt(BaseModel):
    schema_version: Literal["cmf.operator_web_read_model_binding_receipt.v1"] = "cmf.operator_web_read_model_binding_receipt.v1"
    receipt_id: UUID
    route_key: str = Field(min_length=1)
    read_model_schema: str = Field(min_length=1)
    contract_version: str = Field(min_length=1)
    source_receipt_ids: list[UUID] = Field(default_factory=list)
    built_at: datetime
```

## 10. Commands, Events, Workflows, and Receipts

| Object | Requirement |
|---|---|
| `UiCommandEnvelope` | Created before any mutation leaves the browser. |
| `UiActionReceipt` | Displayed after submit and persisted in recent command log. |
| `UiStateBuildReceipt` | Returned with each major read-model load where backend supports it. |
| `operator.command.pending` | UI local event only, never canonical state. |
| `operator.command.receipted` | UI event when backend receipt arrives. |
| `operator.scope.changed` | Triggers read-model refetch and command draft discard. |

## 11. DSPy Programs, JIT Skills, or Deterministic Services

No DSPy or JIT skill is allowed inside the browser. The frontend can request a command draft or proposal, but all intelligence execution must happen server-side behind contracts and the Command Bus.

## 12. Provider, Renderer, Projection, or Worker Boundaries

The web app never calls Ideogram, Qwen, SAM3, ComfyUI, Remotion, Motion Canvas, FFmpeg, Telegram, Publer, or Neo4j directly. It calls CMF APIs only. Render previews, provider statuses, and projections arrive as read-model fields with receipt references.

## 13. CBAR Constraint Pass

| Constraint | Pass Condition |
|---|---|
| Tension | Operator wants fast actions; system requires proof-backed mutation. |
| Failure Scenario | `Request Revision` updates a local asset card but no backend receipt exists. |
| Resolution Demand | Button creates and submits a `UiCommandEnvelope`, then waits for `UiActionReceipt`. |
| Downstream Proof | Recent command log shows receipt id, command id, active object, status, and blockers. |

## 14. Acceptance Criteria with Failure Examples

| AC | Acceptance Criteria | Failure Example | CBAR |
|---|---|---|---|
| AC136-01 | Production mode fetches shell state from `/api/v1/operator-ui/shell`. | App boots from `data.js` without API attempt. | Phase5-M01 |
| AC136-02 | Every commandable action creates a `UiCommandEnvelope`. | `Approve` directly toggles React state. | Phase1-M05 |
| AC136-03 | Active brand and guest scope are visible before command submission. | Operator approves Adele asset while Claude remains selected. | Phase4-M04 |
| AC136-04 | Stale expected object version blocks submission. | Revision command succeeds against old review evidence. | Phase1-M05 |
| AC136-05 | Receipt status is displayed after submission. | UI says "Done" without receipt id. | Phase5-M01 |
| AC136-06 | Fixture mode is explicit and disabled by default in production builds. | Mock content appears as live operations data. | Phase3-M04 |
| AC136-07 | Generated contract version mismatch blocks startup with a clear error. | UI silently drops fields from backend. | Phase4-M05 |

## 15. Dependencies

| Dependency | Required Before Build |
|---|---|
| TS-CMF-001 | Command spine and command envelope contracts. |
| TS-CMF-007 | PWA and Telegram state parity. |
| TS-CMF-051 | Evidence-rich review surface. |
| TS-CMF-055 | Telegram quick review parity. |
| TS-CMF-070 | Operator UI architecture. |
| TS-CMF-132 | Canonical artifact review protocol. |
| TS-CMF-135 | Still visual runtime review API patterns. |

## 16. Testing Strategy

| Test Type | Required Tests |
|---|---|
| Contract generation | Generated TypeScript compiles against OpenAPI/Pydantic schema export. |
| Unit | API client normalizes success, validation error, auth error, and stale object error. |
| Component | Command buttons open command preview and do not mutate local state before receipt. |
| Integration | Mock FastAPI returns shell/read model; frontend renders live state. |
| Negative | Fixture mode disabled causes failure if API is unreachable. |
| E2E | Operator changes guest scope, creates revision command, receives receipt, and review queue refreshes. |

## 17. Observability, Recovery, and Rollback

1. Log API request correlation ids and command ids in browser diagnostics.
2. Show a non-destructive retry option for failed read-model loads.
3. Preserve unsent command drafts locally only until scope changes.
4. Rollback by setting `VITE_CMF_FIXTURE_MODE=true` for design demos, never production.
5. If receipt retrieval fails after submission, show `accepted_unknown_terminal_state` and poll command status.

## 18. Spec Audit Receipt

| Field | Value |
|---|---|
| Spec id | TS-CMF-136 |
| Protocol | CMF/ERA3 18-section spec |
| Files read declared | Yes |
| FR-CMF trace declared | Yes |
| Pipeline trace declared | Yes |
| Command Bus boundary | Preserved |
| Legacy direct import | Prohibited |
| Primitive/eval evidence | Read-model only |
| Approval/revision receipts | Required |
| Status | ready-for-development |
