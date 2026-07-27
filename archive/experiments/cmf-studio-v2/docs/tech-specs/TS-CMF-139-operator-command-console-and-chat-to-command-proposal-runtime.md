---
tech_spec_id: "TS-CMF-139"
title: "Operator Command Console and Chat-to-Command Proposal Runtime"
story_id: "15.4"
story_title: "Give Operators a Governed Command Interface"
epic_id: 15
epic_title: "Operator Operations Runtime and Agentic Control"
status: "ready-for-development"
created_at: "2026-06-26"
fr_ids:
  - "FR-CMF-01"
  - "FR-CMF-03"
  - "FR-CMF-09"
  - "FR-CMF-10"
pipeline_stage: "operator command, command proposal, evidence preview, and confirmation"
entry_object: "OperatorChatMessage, CommandIntentDraft, BrandGuestScopeState"
exit_object: "CommandProposal, UiCommandEnvelope, CommandProposalReceipt"
validation_contract: "intent classification, allowed command types, evidence preview, human confirmation, no direct mutation from chat"
required_receipt: "CommandProposalReceipt"
runtime_target: "React command console / FastAPI / Pydantic v2 / Command Bus / PiAgentGateway optional"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-139: Operator Command Console and Chat-to-Command Proposal Runtime

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture.md` | Defines that chat traces are not durable state and commands mutate through Command Bus. |
| `THE CMF STUDIO/docs/cmf-studio-intelligence-operating-model.md` | Defines intelligence as governed goals, standards, protocols, tools, memory, and constitutions. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-070-ui-architecture-and-operator-experience.md` | Parent UI architecture for commands and receipts. |
| `THE CMF STUDIO/src/ccp_studio/api/v1/operator_ui.py` | Existing command creation and submit endpoints. |
| `THE CMF STUDIO/src/ccp_studio/contracts/operator_ui.py` | `UiCommandEnvelope`, scope, and receipt contracts. |
| `THE CMF STUDIO/src/ccp_studio/services/operator_ui_service.py` | Command creation and validation service owner. |
| `THE CMF STUDIO/src/ccp_studio/services/agent_gateway.py` | Optional Pi/agent routing if chat asks for agentic work. |
| `THE CMF STUDIO/operator-web/src/App.jsx` | Current UI has buttons but no command console. |

## 2. Overview

The Operator needs a command surface, not only buttons. CMF Studio is a factory with many teams, stages, revisions, and approvals. Operators should be able to type things like "repair the Claude reaction clip using stronger source quote evidence", "run primitive eval on this carousel", or "prepare Telegram review for asset GAP-SV-RRC-003", and the system should translate that into a safe command proposal.

This is not a free-form chatbot that edits production state. The command console is a governed interface that classifies intent, resolves active scope, finds allowed command types, prepares a structured proposal, shows evidence and blockers, and asks for confirmation before building a `UiCommandEnvelope`. If the request needs agentic analysis, it routes through Pi/Agent Gateway and returns a proposal receipt; it still cannot mutate without Command Bus validation.

The console must be designed for operations: command history, proposal previews, receipts, blockers, revision targets, and object deep links. It should help the operator control the factory without turning chat into an untraceable state machine.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-139-001 | `OperatorCommandConsole` | Frontend panel for natural-language command requests and history. |
| DEP-CMF-139-002 | `CommandIntentClassifier` | Server-side deterministic or LLM-assisted classifier constrained by command registry. |
| DEP-CMF-139-003 | `CommandProposal` | Structured proposal before envelope creation. |
| DEP-CMF-139-004 | `CommandProposalReceipt` | Receipt proving how intent became command proposal or blocker. |
| DEP-CMF-139-005 | `CommandConfirmationPolicy` | Determines whether proposal can be submitted, needs more evidence, or needs PWA review. |
| DEP-CMF-139-006 | `CommandConsoleReadModel` | Displays proposals, history, receipts, and command status. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `api/v1/operator_ui.py` | Add `/commands/propose` and `/commands/history`. |
| `contracts/operator_ui.py` | Add command console proposal/read-model contracts. |
| `services/operator_ui_service.py` | Add intent-to-proposal logic and command registry lookup. |
| `services/command_bus.py` | Remains final validation and mutation boundary. |
| `services/agent_gateway.py` | Optional path for complex agentic proposals. |

### ADR-05 Primitive Implementation

When the requested command targets creative, interview, extraction, routing, composition, or review work, the proposal must include primitive/eval obligations. The console must not allow "make it better" without converting it into target, blocker, primitive, or evidence-based repair instructions.

### CBAR Mandate Enforcement

| CBAR Mandate | Implementation Rule |
|---|---|
| Phase4-M05 Actionable Rejection | Ambiguous chat requests return clarification blocker and suggested command options. |
| Phase4-M04 Frictionless Block | Missing scope, stale object, or hard blocker prevents submission but explains next action. |
| Phase5-M01 Verifiable Artifact | Every proposal and submission has receipt ids. |

## 4. PRD and FR-CMF Requirement Trace

| Requirement | Implementation Meaning |
|---|---|
| FR-CMF-01 | Scope, role, and commercial policy are checked before proposal submission. |
| FR-CMF-03 | Intent classification uses command registry and generated contracts. |
| FR-CMF-09 | Review, approval, rejection, eval, and revision commands are evidence-based. |
| FR-CMF-10 | Operations and recovery can be driven through the console with receipts. |

## 5. Canonical Pipeline Stage Trace

The console can target any pipeline stage, but it must resolve an active object and command type for that stage. If the operator asks for a cross-stage action, the service decomposes it into proposals or routes to Pi for a staged plan.

## 6. Greenfield Integration and Legacy Migration Context

The command console may reference migrated command patterns from older BMAD/ERA3 workflows, but only as registries or prompt templates transformed into CMF command proposals. It must not execute old repository scripts.

## 7. Architecture Component Map

| Component | Owner | Responsibility |
|---|---|---|
| `CommandConsolePanel` | Frontend | Message entry, proposal preview, command history, receipts. |
| `CommandProposalService` | Backend | Classify intent, resolve scope, build proposal. |
| `CommandRegistryReader` | Backend | List command types, required payload fields, allowed stages, and actor permissions. |
| `ProposalEvidenceBuilder` | Backend | Attach current read model, blockers, and receipt refs. |
| `CommandConfirmationModal` | Frontend | Require human confirmation before submit. |

## 8. Implementation Plan

1. Add `CommandProposal` contracts.
2. Add `/api/v1/operator-ui/commands/propose`.
3. Implement proposal creation: normalize message, resolve active scope, classify target stage/object, match allowed command type, build payload draft, attach evidence refs and blockers, and write `CommandProposalReceipt`.
4. Add frontend command console route or drawer.
5. Show proposal details: command type, scope, object version, payload, evidence, blockers, and receipt expectations.
6. Require operator confirmation before creating/submitting `UiCommandEnvelope`.
7. Add Pi routing for complex requests that need multi-agent planning.
8. Add command history and receipt linking.

## 9. Primary Pydantic Output Schema

```python
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field

class OperatorChatMessage(BaseModel):
    schema_version: Literal["cmf.operator_chat_message.v1"] = "cmf.operator_chat_message.v1"
    message_id: UUID
    operator_user_id: UUID
    brand_workspace_id: UUID
    guest_id: UUID | None = None
    active_object_type: str | None = None
    active_object_id: UUID | None = None
    text: str = Field(min_length=1, max_length=4000)
    created_at: datetime

class CommandProposal(BaseModel):
    schema_version: Literal["cmf.command_proposal.v1"] = "cmf.command_proposal.v1"
    proposal_id: UUID
    source_message_id: UUID
    proposed_command_type: str | None = None
    active_object_type: str | None = None
    active_object_id: UUID | None = None
    brand_workspace_id: UUID
    guest_id: UUID | None = None
    payload_draft: dict = Field(default_factory=dict)
    evidence_refs: list[str] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    next_valid_actions: list[str] = Field(default_factory=list)
    proposal_status: Literal["ready_for_confirmation", "needs_scope", "blocked", "needs_agent_plan"]

class CommandProposalReceipt(BaseModel):
    schema_version: Literal["cmf.command_proposal_receipt.v1"] = "cmf.command_proposal_receipt.v1"
    receipt_id: UUID
    proposal_id: UUID
    classifier_version: str
    matched_command_type: str | None = None
    confidence: float = Field(ge=0, le=1)
    created_at: datetime
```

## 10. Commands, Events, Workflows, and Receipts

| Object | Requirement |
|---|---|
| `OperatorChatMessage` | Input only, not canonical mutation. |
| `CommandProposal` | Structured proposed action. |
| `CommandProposalReceipt` | Proof of classification and evidence binding. |
| `UiCommandEnvelope` | Created only after confirmation. |
| `operator.command.proposed` | Event for proposal creation. |
| `operator.command.confirmed` | Event for envelope creation. |

## 11. DSPy Programs, JIT Skills, or Deterministic Services

Intent classification should prefer deterministic command registry matching. LLM/DSPy assistance is allowed only to map language to existing command types and must return Pydantic-validated proposals. It may not invent command types.

## 12. Provider, Renderer, Projection, or Worker Boundaries

The console does not call providers/renderers. It proposes commands that backend services execute through normal boundaries.

## 13. CBAR Constraint Pass

| Constraint | Pass Condition |
|---|---|
| Tension | Operators need conversational speed; production needs typed control. |
| Failure Scenario | Chat says "approve all" and system approves mixed guest assets. |
| Resolution Demand | Proposal service resolves scope and blocks multi-object unsafe approval. |
| Downstream Proof | Proposal and command receipts show scope, object, command type, and outcome. |

## 14. Acceptance Criteria with Failure Examples

| AC | Acceptance Criteria | Failure Example | CBAR |
|---|---|---|---|
| AC139-01 | Chat message never mutates state directly. | "reject this" changes review state before confirmation. | Phase1-M05 |
| AC139-02 | Proposal includes active scope and object version. | Command draft lacks guest id. | Phase4-M04 |
| AC139-03 | Unknown command intent returns suggestions, not hallucinated command. | LLM invents `make_better_asset`. | Phase4-M05 |
| AC139-04 | Confirmation creates `UiCommandEnvelope`. | Proposal directly calls domain service. | Phase5-M01 |
| AC139-05 | Agent planning path returns proposal receipt and handoff refs. | Complex request disappears into chat log. | Phase3-M04 |

## 15. Dependencies

| Dependency | Required Before Build |
|---|---|
| TS-CMF-001 | Command envelope and bus. |
| TS-CMF-070 | Operator UI architecture. |
| TS-CMF-136 | API client and generated contracts. |
| TS-CMF-137 | Backend composition root. |
| TS-CMF-138 | Optional Pi/agent proposal path. |

## 16. Testing Strategy

| Test Type | Required Tests |
|---|---|
| Unit | Classifier maps known phrases to command types. |
| Unit | Ambiguous commands produce blockers. |
| Integration | Proposal to confirmation to command envelope to receipt. |
| Negative | Direct mutation from chat is impossible. |
| UI | Console shows proposal, evidence, blockers, and receipt. |

## 17. Observability, Recovery, and Rollback

1. Store command proposal receipts for audit.
2. Redact secrets and provider credentials from chat logs.
3. Allow proposal discard without side effects.
4. Disable LLM-assisted classification through settings if it misroutes.

## 18. Spec Audit Receipt

| Field | Value |
|---|---|
| Spec id | TS-CMF-139 |
| Protocol | CMF/ERA3 18-section spec |
| Chat direct mutation | Prohibited |
| Command proposal receipt | Required |
| Human confirmation | Required |
| Status | ready-for-development |
