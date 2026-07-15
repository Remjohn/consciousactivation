# TS-VAE-09 Asynchronous Service and Control Tower

Status: draft for architecture validation  
Implementation authorization: no

## 1. Specification identity

- Features: F10, F18, F19
- Owned FRs: FR-073 through FR-080; FR-137 through FR-152
- Owned NFRs: NFR-OBS-001 through NFR-OBS-005; NFR-SEC-001 through NFR-SEC-005; NFR-UX-001 through NFR-UX-005
- Decisions: D013, D021, D022, D023
- Components: `VaeService`, `DelegationContractPort`, `RuntimeCoordinator`, `ExecutionEventStore`, `Outbox`, `ProjectionBuilder`, `ControlTowerProjectionPort`, policy-first supervisory API

## 2. Evidence read

VAE F10/F18/F19, submission/event/result schemas, service/reference fixtures, readiness/prohibition contracts, Stage 1 findings; Delegation 25-schema family, message registry, external lifecycle, authority/principal matrices, SLOs, failures, conformance/resilience cases, contract ownership register, and Format 02 expected Control Tower projection.

## 3. Problem, solution, and scope

Long-running visual production needs durable asynchronous execution, idempotency, checkpoints, cancellation, backpressure, typed public events, and an inspectable operator surface. The solution is an event-sourced VAE runtime exposed only through Delegation-owned public contracts and projected into the existing Harness Control Tower. The VAE does not create a second shared authority store.

In scope: VAE admission fact, async service, internal runtime nodes/events, append-only event store, checkpoints, retries, cancellation, backpressure, result emission, Delegation adapters, Control Tower read models, telemetry, security, and operator policies. Out of scope: owning public lifecycle/schemas, routine manual GPU/ComfyUI control, final consumption acknowledgement, or duplicating the Builder Workflow Runtime.

## 4. Reference architecture and responsibilities

`vae-control-plane` is a modular service with transactional command handling, editor-local event records, outbox, repositories, and projections. It registers VAE node types with `WorkflowRuntimePort`; the pinned Builder runtime remains the orchestration foundation once available.

| Component | Responsibility |
|---|---|
| `DelegationContractPort` | Consume/emit pinned Delegation messages and conformance metadata; no schema fork. |
| `VaeService` | Authorize internal command dispatch from validated external facts and expose status/result references. |
| `RuntimeCoordinator` | Execute plan DAG, enforce state/node dependencies, checkpoint, retry, cancel, invalidate, terminate. |
| `ExecutionEventStore` | Append editor-local events with optimistic concurrency, correlation, causation, and hashes. |
| `Outbox` | Atomically publish internal events and Delegation message intents after state commit. |
| `ProjectionBuilder` | Build execution, budget, candidate, evaluation, asset, compute, and exception read models. |
| `ControlTowerProjectionPort` | Extend existing Control Tower read-model/event API; no command or authority ownership. |

## 5. Canonical runtime models and state

`Execution`: execution ID, exact demand/plan/compatibility/budget refs, current private state version, terminal reason, cancellation/supersession fences, timestamps, and event sequence.

`NodeExecution`: node/attempt IDs, type/actor, dependencies, input/output refs, capability/runtime bundle, status, retry/quality-round classification, timeout, checkpoint, invalidation generation, budget reservations, and receipt refs.

`ExecutionEvent`: event ID, aggregate ID/version, event type/version, correlation/causation, actor/principal, occurred/recorded times, immutable payload ref/hash, and trace/audit refs.

Private execution states: `ADMITTED`, `PLANNING`, `ROUTING`, `QUEUED`, `PRODUCING`, `EVALUATING`, `REPAIRING`, `PROMOTING`, `PACKAGING`, `WAITING_BUDGET`, `WAITING_AMENDMENT`, `WAITING_HUMAN`, `CANCELLING`, `SUCCEEDED`, `FAILED`, `CANCELLED`, `SUPERSEDED`.

These never appear as arbitrary shared lifecycle values. The VAE emits stable facts such as `execution_started`, `progress_checkpointed`, `budget_required`, `amendment_required`, `capability_gap`, `result_ready`, or `cancellation_completed`; Delegation owns public projection.

## 6. Public and internal interfaces

All public payloads are Delegation-owned: envelope, demand, submission, submission receipt, event, budget messages, cancellation, conflict/amendment, supersession/invalidation, result, failure, and notices. Stage 3 supplies generated bindings and compatibility tests.

VAE internal service interface:

```text
admit(validated_submission, negotiated_profile) -> VaeAdmissionFact
get_execution(execution_id) -> ExecutionProjection
request_internal_cancel(execution_id, validated_cancellation_ref) -> CancellationDisposition
resume(execution_id, checkpoint_ref, trigger_ref) -> ResumeReceipt
emit_result(execution_id, accepted_asset_refs) -> VaeProductionResultFact
stream_internal_events(execution_id, after_sequence) -> ExecutionEvent[]
```

VAE admission fact is signed by VAE; Delegation may issue the public receipt over protocol validation plus that fact. VAE result contains production acceptance only. The local `authorized_for_composition` field is forbidden; downstream authorization exists in Delegation result acknowledgement.

Queue delivery is at-least-once. Commands are exactly-once in effect through idempotency key + aggregate version + transactional event/outbox. Per-execution ordering is strict; cross-execution ordering is not required. Out-of-order facts buffer within a bounded window or reject without illegal transition.

## 7. Runtime, retries, cancellation, and terminal behavior

Each plan node has explicit dependency, actor, timeout, infrastructure retry policy, checkpoint, invalidation tags, and budget. Ready nodes run with dependency-safe bounded parallelism. Successful nodes checkpoint immutable outputs.

Infrastructure retry reuses the same plan/bindings and does not consume quality rounds. Quality rerun requires TS-VAE-07 repair. Cancellation/supersession sets a fencing generation immediately, prevents new leases/promotion, allows declared atomic work to checkpoint, then emits disposition. Backpressure reports queue/capacity/delay and never reduces quality.

Terminal internal states are success, failed typed exception, cancelled, and superseded. External completion still requires Content Harness result acknowledgement through Delegation.

## 8. Control Tower and observability contract

Required read models:

- demand/authority/compatibility summary without mutable semantic controls;
- public Delegation lifecycle plus private VAE phase clearly separated;
- Visual Production Plan graph, node status, checkpoints, invalidation, and receipts;
- candidate comparison and independent evaluation evidence;
- asset lineage, usage context, supersession/revocation;
- Budget Program, estimate/actual, reservations, candidates, repairs, cost;
- queue/worker/runtime health, failures, retries, recovery, SLOs;
- typed conflicts, amendment/budget/cancellation/human exception packages;
- audit chain and exact version/hash drill-down;
- cross-run quality, evaluator, repair, recurrence, cost, and operations analytics.

Controls are policy-first: choose eligible program, cancel, approve VAE-owned internal replan where authorized, inspect evidence, or resolve a typed exception. There are no routine prompt, seed, LoRA strength, mask, graph, or model-file controls.

Projection freshness target follows Delegation p99 <= 5 seconds; critical invalidation/revocation p99 <= 10 seconds. Every displayed status links to evidence/event sequence and exposes stale/error state. Accessibility requires keyboard operation, semantic labels, focus order, non-color status indicators, and screen-reader evidence summaries.

## 9. Cross-cutting production contract

| Concern | Required behavior |
|---|---|
| VPP IR | Runtime executes one exact plan version; amendments/repairs create new versions and invalidation generations. |
| APIs/queues/events | Transport-neutral Delegation adapter; transactional event/outbox; replayable internal stream; stable public facts only. |
| Provider/ComfyUI/Docker locks | Node inputs reference TS-VAE-03 artifacts/bundles and TS-VAE-04 OCI image digests; runtime never edits them. |
| GPU/storage | TS-VAE-04 owns worker jobs; control plane stores refs/receipts and scoped object links. |
| Deterministic/VLM | Lifecycle/dependencies/idempotency/budget/authority are deterministic. VLM exists only in registered planning/evaluation nodes. |
| Budget/candidates | TS-VAE-05 reservation required; Control Tower exposes policy and evidence, not hidden spend. |
| Evaluation/repair | TS-VAE-06/07 nodes remain separate from materializer and have explicit quality-round state. |
| Idempotency/checkpoints | Submission, command, event, node, outbox, and projection checkpoints are distinct and durable. Idempotent duplicate is not hostile replay. |
| Observability/cost | OpenTelemetry-compatible traces/metrics/logs plus immutable event/receipt refs; no evidence-free status. |
| Security/isolation | Principal/scopes from Delegation; least privilege, tenant isolation, signed refs, secret redaction, audit, rate/size limits. |
| Migration/rollback | Event/upcaster and projection versions are explicit; deployments use expand/migrate/contract; rollback preserves writer compatibility and replays projections. |

## 10. Failure and recovery

Failures map to Delegation taxonomy with VAE diagnostics refs. Audit/event-store transaction failure fails safe before effect. Outbox/bus failure retries after commit while preserving order. Projection failure rebuilds from events. Runtime restart resumes from event/checkpoint state. Object/worker failure follows TS-VAE-04. Evaluator/repair failures follow TS-VAE-06/07.

Submission duplicates return existing execution/receipt; replayed signed messages in an invalid state reject/audit. Cancellation-result and supersession-worker races use fencing and precedence receipts. No late stale output can promote.

## 11. Security and data governance

Authenticate Delegation principals and verify protocol validation result; authorize every command by principal, demand ownership, lifecycle, and policy. Separate service, worker, evaluator, operator, and projection credentials. Use encrypted transport/storage, content integrity, scoped object references, deny-by-default network, secret manager injection, and tamper-evident audit refs.

Untrusted notes, media, callbacks, model outputs, and external diagnostics are validated/sanitized. Callback destinations are allowlisted and signed. Logs never contain secrets, signed URLs, raw protected prompts, or unrelated tenant data. Retention/legal hold and incident quarantine are specified per artifact class.

## 12. Compatibility, migration, and rollback

The VAE consumes the published Delegation package by version. The current 0.1.0-draft is design-only. Shared schema changes are handled by generated bindings/adapters in Stage 3, not local edits. Event versions have upcasters; projections can rebuild. Database changes use backward-compatible phases, migration receipts, backup/restore proof, and rollback rehearsal.

The upstream Control Tower projection API remains a blocker until pinned; this spec defines the additive read model but prohibits a substitute authority store.

## 13. Implementation plan

1. Define internal command/event/execution/node/checkpoint/projection schemas and repository ports.
2. Implement transactional aggregate/event/outbox/idempotency foundation through the pinned Builder runtime adapter.
3. Implement Delegation package adapter, VAE admission/result facts, public event mapping, and conformance fixtures.
4. Implement node scheduler, dependency parallelism, timeouts, infrastructure retries, cancellation/supersession fencing, and recovery.
5. Integrate plan, registry/compiler, compute, budget, evaluator, repair, asset services.
6. Implement Control Tower projection/read API and policy-first operator commands.
7. Add telemetry, SLOs, security, audit, migrations, backup/restore, chaos, and rollback tests.

## 14. Given/When/Then acceptance criteria

1. Given a valid submission retried after timeout, when admitted, then the same execution/receipt is returned and no duplicate run starts.
2. Given an out-of-order progress event before admission, when handled, then no illegal public lifecycle transition occurs.
3. Given an internal node status, when external event emits, then only a registered stable fact is exposed.
4. Given event-bus outage after state commit, when service recovers, then outbox delivers in order without duplicate effect.
5. Given service restart during production, when replay completes, then the same execution resumes from committed checkpoints.
6. Given cancellation racing with result completion, when fencing applies, then precedence is receipted and stale promotion is impossible.
7. Given a VAE-produced result, when serialized, then it contains production acceptance and no downstream consumption authorization.
8. Given a projection lag/failure, when Control Tower renders, then status is marked stale/error rather than presented as current.
9. Given rollback of service/projection, when prior compatible version starts, then historical events remain readable and projections rebuild.

## 15. Testing strategy

Unit-test aggregate transitions, ordering, idempotency, outbox, node readiness, timeouts, fencing, and projections. Contract-test all VAE-produced/consumed Delegation messages and authority mutations. Integration-test runtime adapters, repositories, object refs, callbacks, Control Tower, and restart. Fault-inject bus/store/worker/evaluator/projection failures and race cases. Run security, load/SLO, migration/rollback, accessibility, and all Delegation conformance plus Format 02 end-to-end scenarios.

## 16. Constitutional alignment V1.1 addendum

The service boundary accepts only a Delegation-validated message whose mandatory constitutional behavior is enforceable by the pinned generated binding and negotiated profile. Successful parsing is insufficient. Admission records the canonical demand hash plus a constitutional-enforceability receipt from TS-VAE-01.

Internal commands carry immutable references to the Composition Asset Pack and evaluation profile; they do not copy or mutate public demand objects. Public events and results expose only fields authorized by the pinned Delegation release. Private projections may show lineage completeness, applicability, hard-gate outcomes, responsible layers, and missing-evidence blockers, but they do not expose mutable semantic controls.

Control Tower evidence includes the status of constitutional intake, activation/narrative/feature/wrong-reading/no-text gates, repair responsibility, and the exact owner/version/hash for each authoritative reference. Operators may inspect and route exceptions but cannot edit Recognition Carrier, viewer role, Activation Contract, Visual Narrative Program, Feature Contracts, T/V request, or locks.

Contract tests reject a parseable message when any mandatory semantic layer is unavailable to the adapter, cannot be losslessly preserved, or cannot be enforced by the negotiated VAE profile.

## 17. Non-goals

- A new Builder Workflow Runtime or disconnected Control Tower authority store.
- Public exposure of ComfyUI graphs, prompts, model details, or internal node states.
- Routine manual production approval or low-level operator controls.
- Treating VAE production acceptance as downstream composition acknowledgement.
