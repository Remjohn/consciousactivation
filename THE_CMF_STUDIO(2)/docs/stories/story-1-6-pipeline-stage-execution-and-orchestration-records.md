---
story_id: "1.6"
story_title: "Pipeline Stage Execution and Orchestration Records"
epic_id: 1
epic_title: "Governed Workspace and Production Spine"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-01.06"
  - "FR-CMF-03.07"
  - "FR-CMF-10.06"
pipeline_stage: "all stages"
entry_object: "active object and requested action"
exit_object: "`OrchestrationRun`, `StageExecutionPlan`, receipt"
validation_contract: "stage/object/actor validation"
required_receipt: "stage execution receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 1.6: Pipeline Stage Execution and Orchestration Records

**Epic:** 1 - Governed Workspace and Production Spine
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-01.06, FR-CMF-03.07, FR-CMF-10.06 |
| Canonical Pipeline Stage | all stages |
| Entry Object | active object and requested action |
| Exit Object | `OrchestrationRun`, `StageExecutionPlan`, receipt |
| Validation Contract | stage/object/actor validation |
| Required Receipt | stage execution receipt |
| Source PRD | `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` |
| Source Architecture | `docs/architecture.md` |
| Source Pipeline Map | `docs/cmf-studio-pipeline-map.md` |
| Source Legacy Inventory | `docs/migration/legacy-inventory.md` |

## Epic Context

**Epic Goal:** Create the governed product spine that lets the CMF team operate multiple brands, roles, commands, commercial entitlements, receipts, and PWA/Telegram surfaces over the same canonical state.

**Covers:** FR-CMF-01.01 through FR-CMF-01.07.

**User Value:** Owners, Admins, Operators, and commercial administrators can run production without cross-brand leakage, pricing drift, or separate state machines.

**Technical Context:** `contracts/tenancy.py`, `contracts/commercial.py`, `/api/v1/organizations`, `/api/v1/brands`, `/api/v1/auth`, Command Bus, `organizations`, `brand_workspaces`, `role_assignments`, `commercial_entitlements`, `command_log`, `domain_events`, `audit_receipts`.

**CBAR Failure Scenario:** If the system treats workspace setup as generic CRUD, then Telegram actions, provider jobs, memory, and publishing can mutate the wrong brand or expose the wrong offer. The story set therefore locks brand scope and command receipts before creative workflows begin.

## Story Definition

As an Operator or agent supervisor, I want every autonomous or workflow-driven action to run inside a canonical pipeline stage with explicit orchestration records, so that Pi and specialist agents can operate without skipping consent, source truth, brand locks, routing, evaluation, approval, publishing, memory, or projection boundaries.

**Acceptance Criteria:**

- Given a state-changing pipeline action is requested, when orchestration begins, then the system opens or resumes an `OrchestrationRun` linked to organization, brand, actor, active object, and requested outcome.
- Given a stage is selected, when `StageExecutionPlan` is created, then it records canonical PRD pipeline stage, entry object, expected exit object, allowed actor/service, required inputs, blocked actions, and downstream proof obligation.
- Given execution is about to start, when the `ValidationContract` is recorded, then it defines success, failure, thresholds, forbidden skips, required evidence, and required receipts before any worker, DSPy program, provider adapter, renderer, or workflow acts.
- Given Pi dispatches work to a specialist agent, DSPy program, provider adapter, renderer, or workflow, when handoff occurs, then an `AgentHandoffPacket` carries active object, source evidence, upstream receipts, allowed actions, blocked actions, and required downstream receipt.
- Given a JIT Skill compiler is invoked inside the run, when it returns, then `SkillInvocationRecord` stores source context, registry snapshot, compiler fingerprint, contrastive prompt layer, critic result, synthesis result, and eval state.
- Given a stage succeeds, fails, partially completes, blocks, or needs human judgment, when execution closes, then the system records a success receipt, `FailureReceipt`, `FrictionReceipt`, or `HumanHandoffRequest` and only advances when the receipt satisfies the validation contract.
- Given Pi attempts to skip a pipeline stage, mutate canonical state directly, approve its own output, publish externally, or treat Neo4j as canonical truth, when validation runs, then execution is blocked.

**Technical Notes:** Implement `contracts/orchestration.py`, `/api/v1/orchestration`, `OrchestrationRunWorkflow`, `orchestration_runs`, `stage_execution_plans`, `validation_contracts`, `agent_handoff_packets`, `skill_invocation_records`, `failure_receipts`, `friction_receipts`, and `human_handoff_requests`. Command Bus remains the mutation boundary; durable workflows own retries, waits, and resumability.

**Legacy and Primitive Mapping:** Legacy Pi extension principles from `InteractComp`, `TillDone`, `DamageControl`, `ModelRouter`, `TeamOrchestrator`, `SystemSelect`, and `MemoryFolder`, updated for Python/Pydantic/DSPy/Pi. Active families: SAF, FBK, BUS, STR.

**Prerequisites:** Stories 1.1 through 1.5.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
