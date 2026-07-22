---
tech_spec_id: "TS-CMF-137"
title: "Production FastAPI Composition Root and Command Handler Wiring"
story_id: "15.2"
story_title: "Wire the Backend as One Production Application"
epic_id: 15
epic_title: "Operator Operations Runtime and Agentic Control"
status: "ready-for-development"
created_at: "2026-06-26"
fr_ids:
  - "FR-CMF-01"
  - "FR-CMF-03"
  - "FR-CMF-09"
  - "FR-CMF-10"
pipeline_stage: "application composition, command enforcement, service registration, and API readiness"
entry_object: "ApplicationSettings, ServiceContainer, CommandBus"
exit_object: "CmfStudioApplication, CommandHandlerRegistryReceipt"
validation_contract: "single production composition root, all command handlers registered, route dependencies configured, no default test-token services"
required_receipt: "CommandHandlerRegistryReceipt"
runtime_target: "FastAPI / Python / Pydantic v2 / dependency injection / Command Bus"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-137: Production FastAPI Composition Root and Command Handler Wiring

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture.md` | Defines Command Bus as mutation boundary and PWA/Telegram/Pi as surfaces over one object model. |
| `THE CMF STUDIO/docs/tech-specs/README.md` | Current ledger shows many implemented services that need composition. |
| `THE CMF STUDIO/src/ccp_studio/services/command_bus.py` | Existing bus currently creates an in-memory reference bus with only reference command handlers. |
| `THE CMF STUDIO/src/ccp_studio/services/*_service.py` | Many domain services expose `register_*_command_handlers` functions. |
| `THE CMF STUDIO/src/ccp_studio/api/v1/operator_ui.py` | Operator UI route dependency owner. |
| `THE CMF STUDIO/src/ccp_studio/api/v1/telegram_review.py` | Telegram review route requires configured service. |
| `THE CMF STUDIO/src/ccp_studio/api/v1/webhooks/telegram.py` | Current webhook defaults to `test-token` and local in-memory surface action service. |
| `THE CMF STUDIO/src/ccp_studio/services/surface_action_service.py` | Telegram/PWA surface command adapter owner. |
| `THE CMF STUDIO/src/ccp_studio/services/telegram_review_service.py` | Telegram review service and command handler owner. |
| `THE CMF STUDIO/src/ccp_studio/services/agent_factory_service.py` | Agent Factory service dependency for operations state. |

## 2. Overview

CMF Studio now has many backend contracts and service modules, but the runtime must be assembled into one production application. The current codebase contains a reference `create_in_memory_command_bus()` path and multiple API modules that instantiate default services locally. That is useful for tests, but it is not the production harness. A production operator UI, Telegram integration, Pi harness, review workflow, and provider runtime need the same service graph and the same Command Bus.

This spec defines the composition root: a single application builder that constructs settings, repositories, policies, services, command handlers, routers, webhook dependencies, and health checks. The composition root must register every production command handler explicitly and emit a `CommandHandlerRegistryReceipt` proving what command types are available.

This is the backend counterpart to TS-CMF-136. Without it, the React app can call APIs, but those APIs may still route to isolated in-memory services or fail because dependencies are not configured. With it, UI, Telegram, Pi, workflows, and provider webhooks all mutate through the same command enforcement path.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-137-001 | `ApplicationSettings` | Environment-derived settings for auth, Telegram, storage, provider flags, CORS, fixture mode, and event streaming. |
| DEP-CMF-137-002 | `ServiceContainer` | Owns repositories, policies, services, workflows, gateways, and adapters. |
| DEP-CMF-137-003 | `CommandHandlerRegistryReceipt` | Lists registered command types, handler owners, schema versions, and readiness findings. |
| DEP-CMF-137-004 | `create_cmf_app` | Production FastAPI app factory. |
| DEP-CMF-137-005 | `configure_api_dependencies` | Sets `set_*_service` functions for routers. |
| DEP-CMF-137-006 | `configure_command_bus` | Registers all domain command handlers. |

### Existing Backend Integration

The composition root must include the handler registration functions already present across services, including workspace, role, commercial, consent, brand genesis, brand context, research, pre-induction, interview contract, expression session, extraction, routing, asset package, complete editing session, scene spec, composition, deterministic rendering, provider operations, evaluation, review state, review decision, approval gate, telegram review, publishing, memory, projection, operations board, workflow recovery, operational readiness, revision, rejection memory, and reaction editing template handlers.

### ADR-05 Primitive Implementation

Primitive and doctrine checks are not composition-root logic. The root wires services that enforce them. It must fail readiness if eval registries, primitive triads, or doctrine harness services are disabled in a production profile.

### CBAR Mandate Enforcement

| CBAR Mandate | Implementation Rule |
|---|---|
| Phase1-M05 Deterministic Override | There is one production command path. Local test buses cannot be used by production routers. |
| Phase3-M04 Telemetry Surfacing | Handler registry and service readiness are exposed through operations health. |
| Phase4-M04 Frictionless Block | Missing service configuration fails startup or readiness, not runtime operator action. |
| Phase5-M01 Verifiable Artifact | Handler registry receipt proves which commands are live. |

## 4. PRD and FR-CMF Requirement Trace

| Requirement | Implementation Meaning |
|---|---|
| FR-CMF-01 | Workspace, role, commercial, and scope policies must be wired into command validation. |
| FR-CMF-03 | Spec governance and registry conversion services must be part of readiness. |
| FR-CMF-09 | Review, approval, publishing, and Telegram services share one command path. |
| FR-CMF-10 | Operations, recovery, memory, and projection services run from the same application graph. |

## 5. Canonical Pipeline Stage Trace

The composition root spans all stages. It does not execute pipeline stages itself; it ensures stage services and command handlers are available and centrally enforced.

## 6. Greenfield Integration and Legacy Migration Context

The production root must live inside `THE CMF STUDIO/src/ccp_studio`. It may load migrated registries and worker assets stored in the CMF project folder. It must not import runtime code from the old Conscious Coaching Factory folders.

## 7. Architecture Component Map

| Component | File Target | Responsibility |
|---|---|---|
| `ApplicationSettings` | `src/ccp_studio/config.py` or `app/settings.py` | Typed env/config object. |
| `ServiceContainer` | `src/ccp_studio/app/container.py` | Build and expose services. |
| `command_registry.py` | `src/ccp_studio/app/command_registry.py` | Register command handlers and create receipt. |
| `create_cmf_app` | `src/ccp_studio/app/main.py` | Build FastAPI app, routers, CORS, auth, dependencies. |
| `health.py` | `api/v1/health.py` | Surface readiness and handler registry status. |

## 8. Implementation Plan

1. Add `ApplicationSettings` with explicit production, development, test, and fixture profiles.
2. Add `ServiceContainer` that constructs repositories, policies, services, workflows, and gateways.
3. Replace route-level default service globals with `set_*_service` calls from the composition root.
4. Replace default Telegram `test-token` usage with settings-derived token and explicit dev-only fallback.
5. Build `configure_command_bus(container)` and register all known `register_*_command_handlers`.
6. Emit `CommandHandlerRegistryReceipt` after registration.
7. Add `/api/v1/health/readiness` showing service readiness, command handler count, missing handlers, and fixture mode.
8. Add startup failure for production profile if Telegram service is unset while Telegram routes enabled, Operator UI service is fixture-only, Command Bus has only reference handlers, or eval/doctrine/primitive registries are unavailable.
9. Add test app factory that can opt into in-memory repositories without pretending to be production.

## 9. Primary Pydantic Output Schema

```python
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field

class ApplicationSettings(BaseModel):
    schema_version: Literal["cmf.application_settings.v1"] = "cmf.application_settings.v1"
    profile: Literal["production", "development", "test", "fixture"]
    api_base_url: str
    allowed_origins: list[str] = Field(default_factory=list)
    telegram_enabled: bool = False
    telegram_bot_token_configured: bool = False
    event_stream_enabled: bool = True
    fixture_mode_enabled: bool = False

class CommandHandlerRegistration(BaseModel):
    command_type: str = Field(min_length=1)
    handler_owner: str = Field(min_length=1)
    service_owner: str = Field(min_length=1)
    schema_ref: str | None = None

class CommandHandlerRegistryReceipt(BaseModel):
    schema_version: Literal["cmf.command_handler_registry_receipt.v1"] = "cmf.command_handler_registry_receipt.v1"
    receipt_id: UUID
    profile: Literal["production", "development", "test", "fixture"]
    registered_handlers: list[CommandHandlerRegistration]
    missing_required_handlers: list[str] = Field(default_factory=list)
    readiness_status: Literal["ready", "degraded", "blocked"]
    created_at: datetime
```

## 10. Commands, Events, Workflows, and Receipts

| Object | Requirement |
|---|---|
| `CommandHandlerRegistryReceipt` | Written on startup and exposed in readiness. |
| `operations.readiness.checked` | Emitted when readiness is evaluated. |
| `application.fixture_mode.enabled` | Emitted when fixture mode is active. |
| `command_bus.handler_missing` | Hard readiness blocker in production. |

## 11. DSPy Programs, JIT Skills, or Deterministic Services

The composition root wires DSPy/JIT services but does not execute them. Any service that invokes DSPy must still return Pydantic-validated output and mutate only through commands.

## 12. Provider, Renderer, Projection, or Worker Boundaries

Provider adapters, render workers, Telegram, Publer, and Neo4j projections are injected as adapters. They cannot instantiate their own Command Bus or write directly to canonical state.

## 13. CBAR Constraint Pass

| Constraint | Pass Condition |
|---|---|
| Tension | Many services exist; production must behave like one system. |
| Failure Scenario | Telegram route uses one in-memory bus while PWA uses another. |
| Resolution Demand | Composition root injects the same bus and services into every route. |
| Downstream Proof | Health route exposes a registry receipt showing handlers and service readiness. |

## 14. Acceptance Criteria with Failure Examples

| AC | Acceptance Criteria | Failure Example | CBAR |
|---|---|---|---|
| AC137-01 | Production app factory wires Operator UI, Telegram, surface actions, Agent Factory, and command routes from one container. | Router creates isolated service at import time. | Phase1-M05 |
| AC137-02 | Command Bus registry includes all implemented domain handlers required by current specs. | Only `SubmitCommand` is registered. | Phase5-M01 |
| AC137-03 | Production startup blocks default Telegram `test-token`. | Webhook accepts dev token in production. | Phase4-M04 |
| AC137-04 | Readiness fails if primitive/eval registries are missing. | Renderer accepts assets with no eval backend. | Phase4-M04 |
| AC137-05 | Test app factory is explicitly named and cannot be selected by production env. | Fixture profile silently used in production. | Phase4-M05 |
| AC137-06 | Handler registry receipt is queryable. | Operator cannot know which actions are live. | Phase3-M04 |

## 15. Dependencies

| Dependency | Required Before Build |
|---|---|
| TS-CMF-001 | Command Bus and command envelope foundations. |
| TS-CMF-003 | Spec governance and Python/DSPy/Pi boundaries. |
| TS-CMF-050 | Evaluation receipts. |
| TS-CMF-055 | Telegram quick review service. |
| TS-CMF-059 | Operations board. |
| TS-CMF-060 | Workflow recovery actions. |
| TS-CMF-070 | Operator UI architecture. |
| TS-CMF-136 | Frontend API client expects stable backend composition. |

## 16. Testing Strategy

| Test Type | Required Tests |
|---|---|
| Unit | `configure_command_bus` registers expected command types. |
| Unit | Production profile rejects test Telegram token and fixture services. |
| Integration | `create_cmf_app(profile="development")` serves operator, Telegram, surface, health, and agent routes. |
| Negative | Missing `TelegramReviewService` blocks Telegram readiness. |
| Contract | Readiness response validates against `CommandHandlerRegistryReceipt`. |
| Regression | Route dependencies use container-provided services, not import-time defaults. |

## 17. Observability, Recovery, and Rollback

1. Log startup registry receipt id.
2. Include readiness status in operations board.
3. Allow development profile to run with in-memory repositories, but show degraded status.
4. Roll back by disabling Telegram or provider routes through settings, not by deleting handlers.
5. If a handler registration fails, mark readiness blocked and list missing command types.

## 18. Spec Audit Receipt

| Field | Value |
|---|---|
| Spec id | TS-CMF-137 |
| Protocol | CMF/ERA3 18-section spec |
| Files read declared | Yes |
| FR-CMF trace declared | Yes |
| Pipeline trace declared | Yes |
| Command Bus boundary | Central requirement |
| Legacy direct import | Prohibited |
| Startup readiness | Required |
| Status | ready-for-development |
