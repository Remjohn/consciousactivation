# TS-01: Governed Lifecycle And Target Profiles

Status: `SPEC_RATIFIED_PENDING_STORY_MAPPING`

## Traceability

- Owned: FR-001 through FR-008; NFR-REL-002; NFR-SEC-003.
- Decisions: D001, D002, D004, D005, D006, D010, D025, D027, D029, D033.
- Supporting NFRs: NFR-REL-001, NFR-REL-003, NFR-TRACE-002, NFR-OBS-001.

## Responsibility And Authority

Own run identity, target selection, legal lifecycle transitions, actor authorization, waivers, checkpoints, resume, and product-boundary enforcement. It does not own evidence semantics, Genesis recommendations, evaluation scores, generated target behavior, or implementation authorization criteria.

Deterministic code validates and applies transitions. Agents may request transitions with evidence. Humans approve waivers, constitutional transitions, prototype authorization, and implementation authorization.

## Modules And Components

| Module | Responsibility |
|---|---|
| `domain/run.py` | Run aggregate, state, target, and invariants |
| `domain/target_profile.py` | Versioned Atomic Content, Visual Asset Editor, and Delegation profiles |
| `application/run_commands.py` | Command handlers and transaction boundary |
| `application/authority.py` | Actor/action authorization |
| `application/checkpoints.py` | Resume and checkpoint selection |
| `api/runs.py`, `cli/runs.py` | Command/query surfaces over application services |

## Canonical Data Structures

`Run { run_id, target_profile_ref, lifecycle_state, stream_version, source_lock_ref?, harness_ir_ref?, workflow_ref?, active_checkpoint_ref?, created_by, created_at }`

`TargetProfile { profile_id, version, target_kind, required_sources, lifecycle_edges, required_artifacts, evaluation_gates, compiler_id, certification_scope }`

Lifecycle states are `CREATED`, `SOURCE_DIAGNOSTIC`, `SOURCE_LOCKED`, `VISUAL_UNDERSTANDING`, `SATURATED`, `ATOMICITY_RATIFICATION`, `GENESIS`, `ARCHITECTURE_COMPILED`, `EVALUATING`, `REPAIR_REQUIRED`, `READY_FOR_AUTHORIZATION`, `PROTOTYPE_AUTHORIZED`, `IMPLEMENTATION_AUTHORIZED`, `CAPSULE_ISSUED`, `CERTIFIED`, `FAILED`, and `CANCELLED`.

Every edge declares prerequisites, allowed actors, resulting invalidations, required receipts, and target-profile applicability. No caller can set state directly.

## APIs, Commands, Events, Persistence

- Commands: `CreateRun`, `SelectTargetProfile`, `RequestTransition`, `GrantLifecycleWaiver`, `ResumeRun`, `CancelRun`.
- Queries: `GetRun`, `ListAvailableActions`, `GetCheckpoint`, `GetTransitionHistory`.
- Events: `RunCreated`, `TargetProfileSelected`, `LifecycleTransitioned`, `LifecycleWaiverGranted`, `CheckpointCreated`, `RunResumed`, `RunCancelled`.
- Persistence: event stream keyed by `run_id`; snapshot every 100 events and at human gates; target profiles stored as immutable versioned artifacts.
- Concurrency: expected stream version is mandatory. Duplicate command IDs return the prior result.

## Dependency, Invalidation, Idempotency, And Resume

Target selection precedes source diagnostics and is immutable after source lock unless a human-authorized fork is created. An upstream source or atomicity change invalidates downstream checkpoints according to dependency edges. Resume selects the newest checkpoint whose input hashes and policy versions still match; human decisions are replayed from receipts, never re-asked automatically.

Every command carries a unique idempotency key. Repeating a completed command returns its original event and receipt identities; a reused key with different payload is rejected.

## Security And Isolation

Profiles declare source/tool/network grants. Authority enforcement is server-side and deny-by-default. Waivers require signer, rationale, affected gates, scope, and expiry. Delegation and editor profiles may compile contracts but cannot grant runtime permissions to external production systems.

## Observability, Cost, And Performance

Emit transition latency, blocked-transition reason, checkpoint size, replay count, waiver count, and operator intervention. Transition validation target is p95 under 250 ms excluding external receipt lookup; resume target is p95 under 5 seconds for 10,000 events, subject to Release 1 performance calibration.

## Failures And Recovery

Illegal transitions return typed `TransitionRejected` without events. Concurrency conflicts return current stream version. Missing profile versions quarantine the run. Corrupt snapshots fall back to event replay and emit an incident. Expired waivers block the next affected transition.

## Acceptance Tests

1. Creating a run without one explicit target fails.
2. Omitted target never defaults silently.
3. Every legal transition emits one event and one receipt.
4. Illegal edges and unauthorized actors leave state unchanged.
5. Resume does not repeat ratified human decisions.
6. Changing a locked source requires a governed fork and downstream invalidation.
7. Editor and Delegation profiles cannot activate external production behavior.
8. Event replay reproduces the same state and checkpoint eligibility.

## Implementation Tasks

1. Define run, target-profile, transition, authority, and waiver schemas.
2. Implement pure transition and invalidation evaluators.
3. Implement the ratified PostgreSQL event-stream repository and snapshot model after the implementation-readiness gate passes.
4. Add command/query API and CLI adapters.
5. Seed three target profiles with Atomic Content as primary.
6. Add unit, concurrency, replay, authority, and boundary tests.

## V1.2 Constitutional Alignment Patch

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Select a conversational category profile without creating a fourth compilation target | lifecycle_and_target_profile_owner | The Atomic Content Harness target owns category-profile selection; external content harnesses own conversational execution | `TargetProfile` plus `governance/CONVERSATIONAL_PROFILE_REGISTRY.yaml` | Reject unknown profile, false certification, or profile/target conflation | run creation fixtures for `reelcast_expression` and `interview_expression` | Four profiles select deterministically, remain `UNCERTIFIED`, and cannot activate external runtimes | Additive fifth-category profiles; three existing compilation target IDs remain unchanged |

## Non-Goals And Migration

No workflow scheduling, evidence parsing, target runtime, or V2.1 state import is owned here. V2.1 migration remains not applicable.
