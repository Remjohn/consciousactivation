---
tech_spec_id: "TS-CMF-001"
title: "Contract Kernel and Command Spine"
story_id: "1.1"
story_title: "Contract Kernel and Command Spine"
epic_id: 1
epic_title: "Governed Workspace and Production Spine"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-1-1-contract-kernel-and-command-spine.md"
fr_ids:
  - "FR-CMF-01.03"
  - "FR-CMF-01.06"
pipeline_stage: "1 / cross-cutting"
entry_object: "command request"
exit_object: "command log, event, audit receipt"
validation_contract: "command envelope and brand scope"
required_receipt: "audit receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / PostgreSQL"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-001: Contract Kernel and Command Spine

**Status:** Ready for Development  
**Story:** `1.1 - Contract Kernel and Command Spine`  
**Implementation Boundary:** Python contract kernel, Command Bus, command log, domain event outbox, and audit receipt writer.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority for full-system scope, Python-first harness, Pi orchestration, and commercial/production posture. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-01.03 and FR-CMF-01.06 source authority plus canonical PRD pipeline rules. |
| `docs/architecture.md` | Architecture decisions for Command Bus mutation boundary, canonical events, audit receipts, and tenant isolation. |
| `docs/cmf-studio-pipeline-map.md` | Pipeline trace source for command entry and receipt exit. |
| `docs/migration/legacy-inventory.md` | Legacy read-only doctrine, receipt chain references, Python/Pydantic/DSPy/Pi migration target. |
| `docs/stories/story-1-1-contract-kernel-and-command-spine.md` | Story acceptance criteria and handoff requirements. |
| `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Legacy 10-section tech-spec spine adapted for CMF greenfield specs. |
| `docs/architecture/spec updates/CBAR_Constraint_Based_Adversarial_Reasoning_Epics_Stories.md` | CBAR structure used for the tension and downstream proof sections. |

## 2. Overview

### Problem Statement

CMF STUDIO has PWA, Telegram, Pi, DSPy, provider callbacks, renderers, migration workers, approval flows, publishing, memory admission, and Neo4j projection builders all acting on shared production objects. If these surfaces mutate state through separate code paths, brand isolation, consent, commercial policy, idempotency, auditability, and recovery become unreliable.

### Solution

Implement a Python-first Command Bus and contract kernel. Every state-changing request is wrapped in a Pydantic `CommandEnvelope`, validated through a fixed validation chain, persisted in `command_log`, emitted as a canonical domain event, and closed with an `AuditReceipt`. Consumers can be PWA, Telegram, Pi, DSPy programs, durable workflows, provider webhooks, renderers, or recovery jobs, but the mutation boundary is one path.

### Scope

In scope:

- Pydantic v2 command, actor, tenant, result, domain event, idempotency, and audit receipt contracts.
- Command Bus validation order and handler interface.
- PostgreSQL persistence for command log, domain events, audit receipts, and idempotency records.
- FastAPI command submission endpoint and internal service entry point.
- Generated TypeScript contract output for UI consumers.
- Contract tests and integration tests proving brand scope, permission, idempotency, and audit receipts.

Out of scope:

- Feature-specific command handlers beyond reference examples.
- UI forms, Telegram command wording, or provider-specific adapters.
- Neo4j graph writes. Neo4j may receive projected events later, but it is not a mutation authority.
- Legacy runtime coupling to old runtime code.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-01.03 | Every command, query, receipt, upload, render job, and memory admission binds to active brand context. | `CommandEnvelope.organization_id`, `brand_id`, `actor`, `BrandScopeGuard`, repository predicates, and tenant-scoped command log. |
| FR-CMF-01.06 | Every mutating command is idempotent, permission-checked, tenant-scoped, and receipt-writing. | Validation chain, `idempotency_key`, `CommandHandler` contract, `DomainEventEnvelope`, `AuditReceipt`, and transaction boundary. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `1 / cross-cutting` |
| Entry Object | `command request` |
| Exit Object | `command log`, `domain event`, `audit receipt` |
| Allowed Actors / Services | PWA, Telegram Bot, Pi Orchestrator, DSPy workflow, deterministic service, provider webhook adapter, recovery job |
| Validation Contract | Command envelope and brand scope |
| Required Receipt | Audit receipt |
| Forbidden Shortcut | Direct table mutation, direct object storage state mutation, provider callback side effects outside the Command Bus |

### Legacy Intelligence Mapping

The legacy repository is used as read-only design intelligence only. Receipt-chain references inform audit receipt shape, but production code must be implemented in the new Python package. This spec creates greenfield equivalents under the CMF runtime:

- `ccp_studio.contracts.commands`
- `ccp_studio.contracts.events`
- `ccp_studio.contracts.receipts`
- `ccp_studio.services.command_bus`
- `ccp_studio.services.audit_receipts`
- `ccp_studio.repositories.command_log`
- `ccp_studio.api.v1.commands`

TypeScript may consume generated contracts, but it does not define command semantics.

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `CommandEnvelope` | Typed carrier for every state-changing request. |
| `CommandBus` | Single mutation gateway, validation coordinator, idempotency resolver, event/receipt writer. |
| `CommandHandler` | Feature-specific business logic behind the command boundary. |
| `BrandScopeGuard` | Verifies organization and brand scope before a handler runs. |
| `PolicyValidator` | Runs role, consent, commercial, provider, and cost checks. |
| `IdempotencyService` | Returns prior result on replay and prevents duplicate side effects. |
| `DomainEventOutbox` | Emits canonical event records for workflows, projections, analytics, and recovery. |
| `AuditReceiptWriter` | Writes the required audit receipt with correlation IDs and evidence links. |

### Technical Decisions

- Use Pydantic v2 as source-of-truth contract authority.
- Use PostgreSQL canonical state and outbox records.
- Use one database transaction per accepted command, including command log update, domain event creation, and audit receipt creation.
- Use generated TypeScript clients from Python contracts.
- Do not let Pi, DSPy, Telegram, provider adapters, renderers, memory services, or Neo4j projection code bypass this boundary.

## 4. Implementation Plan

### Workstream A: Contract Package

Create the base command, actor, tenant, event, receipt, and result contracts. Include strict schema versioning, enum-safe command status, and serializable payload types.

### Workstream B: Command Bus Core

Implement `CommandBus.submit(envelope)` with the fixed validation chain:

1. Schema version.
2. Authentication.
3. Role permission.
4. Organization and brand scope.
5. Object existence.
6. State transition.
7. Consent policy.
8. Cost and quota policy.
9. Idempotency.
10. Provider policy when relevant.
11. Human confirmation when required.
12. Receipt writer readiness.

### Workstream C: Persistence and Transaction Boundary

Add database tables and repositories for `command_log`, `domain_events`, `audit_receipts`, and `idempotency_records`. The accepted command path must be atomic: a handler cannot commit business state unless the command log, event, and receipt are also persisted.

### Workstream D: API and Internal Entrypoints

Expose `/api/v1/commands` for external command submission and an internal Python service method for durable workflows, Pi, DSPy programs, provider webhooks, and recovery jobs.

### Workstream E: Contract Generation

Add a generated TypeScript contract artifact for PWA and Telegram consumers. The generated artifact is read-only for frontend packages.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ActorType(str, Enum):
    human = "human"
    pi = "pi"
    dspy_program = "dspy_program"
    provider_webhook = "provider_webhook"
    workflow = "workflow"
    recovery_job = "recovery_job"


class CommandStatus(str, Enum):
    accepted = "accepted"
    rejected = "rejected"
    succeeded = "succeeded"
    failed = "failed"
    replayed = "replayed"
    quarantined = "quarantined"


class ActorContext(BaseModel):
    actor_id: UUID
    actor_type: ActorType
    role_ids: list[str] = Field(default_factory=list)
    tool_name: str | None = None
    session_id: UUID | None = None


class CommandEnvelope(BaseModel):
    schema_version: Literal["cmf.command.v1"]
    command_id: UUID
    command_type: str
    organization_id: UUID
    brand_id: UUID
    actor: ActorContext
    idempotency_key: str
    correlation_id: UUID
    payload: dict[str, Any]
    requested_at: datetime
    source_surface: str


class ValidationResult(BaseModel):
    passed: bool
    code: str
    message: str
    evidence: dict[str, Any] = Field(default_factory=dict)


class CommandResult(BaseModel):
    command_id: UUID
    status: CommandStatus
    result_payload: dict[str, Any] = Field(default_factory=dict)
    validation_results: list[ValidationResult]
    domain_event_id: UUID | None = None
    audit_receipt_id: UUID | None = None


class DomainEventEnvelope(BaseModel):
    schema_version: Literal["cmf.domain_event.v1"]
    event_id: UUID
    event_type: str
    organization_id: UUID
    brand_id: UUID
    command_id: UUID
    correlation_id: UUID
    aggregate_type: str
    aggregate_id: UUID
    payload: dict[str, Any]
    occurred_at: datetime


class AuditReceipt(BaseModel):
    schema_version: Literal["cmf.audit_receipt.v1"]
    receipt_id: UUID
    command_id: UUID
    organization_id: UUID
    brand_id: UUID
    actor_id: UUID
    action: str
    status: CommandStatus
    policy_checks: list[ValidationResult]
    event_id: UUID | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `SubmitCommand`, `ReplayCommand`, reference `SwitchActiveBrandCommand`, reference `RecordConsentCommand` |
| Events | `CommandAccepted`, `CommandRejected`, `CommandSucceeded`, `CommandFailed`, `DomainEventRecorded`, `AuditReceiptWritten` |
| Workflows | Command Bus transaction workflow; outbox dispatch workflow |
| Receipts | `AuditReceipt` for every accepted or rejected state-changing request |

## 7. Backward Compatibility and Migration Fallback

There is no legacy runtime compatibility mode. If migrated legacy logic needs to mutate state, it must be wrapped as a new Python command handler. If a legacy runtime coupling is detected in production runtime code, CI fails.

Fallback behavior:

- Missing brand scope returns `BRAND_SCOPE_VIOLATION`.
- Missing idempotency key returns `IDEMPOTENCY_KEY_REQUIRED`.
- Receipt writer unavailable returns `RECEIPT_WRITER_UNAVAILABLE` and prevents handler execution.
- Duplicate idempotency key returns the previous `CommandResult` without duplicate side effects.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Product velocity wants every surface to write directly; CMF safety requires one governed mutation path. |
| UX / Ops Failure Scenario | A Telegram approval, Pi action, or provider webhook mutates the wrong brand, creating cross-brand leakage and an unprovable audit trail. |
| Resolution Demand | Command Bus authority takes precedence. Every state-changing action must enter as a typed command with tenant, actor, idempotency, and receipt requirements. |
| Downstream Proof | Tests must prove direct mutation is blocked, missing brand scope fails, replay does not duplicate side effects, and accepted commands always produce event plus receipt. |

## 9. Tasks

- Define command, actor, event, idempotency, validation, and audit receipt contracts.
- Implement Command Bus submission, validation chain, handler registry, and idempotency service.
- Add PostgreSQL migrations for command log, domain events, idempotency records, and audit receipts.
- Add repositories with mandatory organization and brand predicates.
- Expose `/api/v1/commands` and internal service entrypoint.
- Add reference handlers for active brand switching and consent recording.
- Generate TypeScript consumer contracts.
- Add CI rule blocking direct state mutation outside approved repository and command paths.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Any state-changing request accepted by FastAPI is wrapped in `CommandEnvelope`. | A route writes `brand_context_versions` directly from request JSON. |
| AC2 | Validation runs in the specified order before handler execution. | Provider policy runs before tenant scope and leaks existence of another brand object. |
| AC3 | Successful command writes command log, domain event, and audit receipt with one correlation ID. | Business state changes but `audit_receipts` has no row. |
| AC4 | Idempotency replay returns previous result without duplicate side effects. | Replayed publish command creates a second publishing intent. |
| AC5 | Missing brand scope fails with `BRAND_SCOPE_VIOLATION`. | Command with `organization_id` only is accepted. |

## 11. Dependencies

Internal:

- `ccp_studio.contracts.tenancy`
- `ccp_studio.repositories.organizations`
- `ccp_studio.repositories.brands`
- `ccp_studio.auth.role_policy`
- SQLAlchemy v2 session management
- PostgreSQL migration tooling

External:

- FastAPI
- Pydantic v2
- PostgreSQL
- TypeScript contract generator selected by architecture

## 12. Testing Strategy

Unit tests:

- Pydantic validation for required command fields.
- Validation chain order.
- Brand scope guard.
- Idempotency key replay.
- Receipt writer failure blocks execution.

Integration tests:

- `/api/v1/commands` accepts a valid command and writes all canonical records.
- Replay of the same idempotency key returns the original result.
- Cross-brand command fails.
- Direct handler execution without Command Bus is unavailable from public API.

Safety tests:

- Static import guard for legacy runtime packages.
- Static route scan for unauthorized write paths.
- Projection builder cannot mutate canonical tables.

## 13. Observability, Recovery, and Rollback

- Emit structured logs with `command_id`, `correlation_id`, `organization_id`, `brand_id`, and `actor_id`.
- Add metrics for command acceptance, rejection, replay, failure, and receipt latency.
- Recovery job can reconcile command logs with missing domain events or receipts, but cannot invent business success. It must quarantine ambiguous records.
- Rollback uses compensating commands, never direct table edits.

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
| Files Read Receipt | Complete |
| Requirement Trace | FR-CMF-01.03, FR-CMF-01.06 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Read-only receipt-chain and greenfield doctrine |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python command spine; Pi only via typed commands |
| TypeScript Boundary | Generated consumers only |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

