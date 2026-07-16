# TS-14: Builder Workflow Runtime And Agentic Execution Factory

Status: `SPEC_RATIFIED_PENDING_STORY_MAPPING`

## Traceability

- Owned: FR-181 through FR-210.
- Owned NFRs: NFR-REL-004; NFR-PERF-002 through NFR-PERF-004; NFR-SEC-004; NFR-PORT-002; NFR-ARCH-002; NFR-TEST-001; NFR-WORKFLOW-001 through NFR-WORKFLOW-012.
- Decisions: D001-D003, D006, D010-D029, D032, D033. D028 applies only to future Workflow IR evolution, not absent V2.1 migration.

## Responsibility And Authority

Own canonical Builder Workflow IR, actor assignment, typed nodes/edges, workflow compilation, profiles, deterministic routing, manual shadow capture, code/agent separation, capsule-bound agent execution, node validation, structured feedback, root-cause routing, retry/timeout/circuit-breaker policy, checkpoints/resume, sandboxing, least privilege, bounded parallelism/candidate races, model/compute routing, evaluator isolation, human gates, queues, telemetry, public-seam/fault tests, CI promotion, version/rollback, incident workflows, and workflow economics.

It orchestrates Builder work only. Harness Phase Graphs are outputs for downstream harnesses. A workflow cannot hide inside one skill, unrestricted agent session, or UI process.

## Modules And Components

`workflow/ir.py`, `workflow/profiles.py`, `workflow/compiler.py`, `workflow/router.py`, `workflow/scheduler.py`, `workflow/executors/{code,agent,human,hybrid}.py`, `workflow/checkpoints.py`, `workflow/sandbox.py`, `workflow/validation.py`, `workflow/incidents.py`, `adapters/temporal.py`, and `adapters/in_memory_workflow.py`.

## Canonical Data Structures

- `WorkflowIR { workflow_id, version, profile_ref, nodes, edges, conditions, budgets, human_gates, promotion_status, source_graph_hashes }`
- `WorkflowNode { node_id, actor_kind, input_contracts, output_contracts, validator_refs, capability_refs, capsule_recipe_ref?, retry_policy, timeout, sandbox_policy_ref, budget, idempotency_scope }`
- `WorkflowEdge { producer, consumer, condition, payload_contract, invalidation, feedback_policy? }`
- `WorkflowProfile { profile_id, version, trigger, target_scope, workflow_ref, routing_predicate, certification }`
- `Checkpoint { run_id, workflow_hash, completed_nodes, output_hashes, stream_positions, resumable_at }`
- `SandboxPolicy { image_or_environment, mounts, tools, network_allowlist, secret_refs, resource_limits, disposal }`
- `NodeResult { node_id, attempt, input_hash, output_hash?, validation, cost, latency, failure? }`

Production profiles are immutable and promoted through `DRAFT`, `SHADOWED`, `TESTED`, `PRODUCTION`, `DEPRECATED`, `REVOKED`.

## APIs, Commands, Events, Persistence

- Commands: `RegisterWorkflowProfile`, `CompileWorkflow`, `RouteWorkflow`, `StartWorkflow`, `SignalHumanGate`, `RetryNode`, `CancelWorkflow`, `ResumeWorkflow`, `PromoteWorkflow`, `RollbackWorkflow`, `StartIncidentWorkflow`.
- Queries: profiles, routes, queues, node state, checkpoints, budgets, sandboxes, attempts, incidents.
- Events: `WorkflowRouted`, `WorkflowStarted`, `NodeQueued`, `NodeStarted`, `NodeValidated`, `NodeFailed`, `RetryScheduled`, `HumanGateOpened`, `HumanGateResolved`, `CheckpointCommitted`, `WorkflowCompleted`, `WorkflowRolledBack`, `IncidentOpened`.
- Persistence: Workflow IR/profile registry in authoritative state; domain workflow events in Run Ledger; engine adapter stores operational scheduling history but is not canonical product truth.
- Engine port: `start`, `signal`, `cancel`, `query`, `replay`, and `migrate` using typed workflow/node identities.

## Dependency, Invalidation, Idempotency, Resume

Workflow compiler consumes lifecycle, capability, phase, context, contract, dependency, repair, and authorization graphs. Nodes execute only when all required validated inputs exist. Node idempotency key is `(run, workflow_hash, node, attempt_policy, input_hash)`. Checkpoint commits output hashes and events atomically. Resume verifies workflow/profile compatibility and replays only incomplete or invalidated nodes. Feedback edges are bounded and terminate in escalation.

Parallel execution is limited to dependency-independent nodes and declared resource budgets. Candidate races require the same input contract, independent sandboxes, quality gates, cost caps, and deterministic selection policy.

## Actor, Security, And Isolation Model

- Deterministic node: transformations, schemas, graph operations, routing, compilation, validation, receipts.
- Agent node: bounded inference with exact evaluated capsule and output schema.
- Human gate: constitutional, policy, risk, waiver, irreversible architecture, authorization.
- Hybrid node: agent proposal followed by deterministic validation and declared human decision where required.

Sandbox grants are deny-by-default. Evidence is read-only. Secrets are ephemeral references. Network, tools, repositories, protected labels, and write paths are explicit. Evaluators cannot see generator hidden context. Node disposal removes transient credentials and workspaces while retaining receipt hashes.

## Observability, Cost, And Performance

Emit queue wait, node/end-to-end p50/p95 latency, attempts, retries, circuit state, sandbox startup/disposal, model/token/tool cost, validation failures, intervention, cache hits, critical path, parallelism, first-pass pass rate, and cost per authorized capsule. Budgets are checked before dispatch; overflow pauses or routes to human approval.

## Failures And Recovery

Typed failure classes include contract, validation, provider, timeout, budget, sandbox, authority, dependency, checkpoint, event, and incident. Structured context returns only to the responsible node. Lost engine state is reconstructed from canonical events/checkpoints. Partial parallel failure preserves successful independent results. Circuit breakers stop repeated provider/system failure. Hotfix workflows cannot mutate protected evidence or decisions.

## Acceptance Tests

1. Workflow IR rejects missing actors, contracts, validators, bounds, or terminal states.
2. Manual Format 02 shadow events compile into a reviewable profile before automation.
3. Deterministic and agent executors cannot substitute for each other silently.
4. Agent output is quarantined until node validation passes.
5. Retry, timeout, circuit breaker, and feedback loops are bounded.
6. Checkpoint resume produces the same externally observable outputs and events.
7. Sandbox escape, undeclared tool/network/secret access, and protected-label access fail.
8. Fault tests cover malformed contracts, provider outage, lost event, stale checkpoint, sandbox termination, and partial parallel failure.
9. Promotion requires end-to-end, fault, security, replay, benchmark, and rollback receipts.
10. Monolithic skill-owned production workflows fail architecture and readiness.

## Implementation Tasks

1. Ratify engine, persistence, isolation, and mandatory profiles.
2. Define Workflow IR, profile, node, edge, checkpoint, sandbox, result, and incident schemas.
3. Implement compiler, graph validator, router, scheduler policy, and in-memory test runtime.
4. Implement code, agent, human, and hybrid executors with validator boundary.
5. Implement durable engine adapter, checkpoints, resume, promotion, rollback, and incidents.
6. Capture and replay the Format 02 manual shadow workflow.
7. Add public-seam integration, fault, security, cost, replay, and promotion tests.

## V1.2 Constitutional Alignment Patch

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Route Activative Call → Reaction Receipt → Expression Moment → recompile/elevate/close | workflow_runtime_owner | Builder orchestrates validation and handoff nodes; external content harness executes human interaction | typed nodes, bounded transitions, consent gate, lineage receipt, terminal disposition | Missing policy/receipt blocks; retry is bounded; scripted guest landing is a constitutional violation | deterministic route, resume, withdrawal, and failure-injection fixtures | Every turn transition is receipted, resumable, and owned with no hidden monolithic skill | Additive workflow profile nodes; existing visual workflow profiles remain unchanged |
| Route activation-first visual handoff without executing downstream products | workflow_runtime_owner | Builder ends at versioned external handoff | semantic/narrative/composition/T/V/delegation contract refs | External execution attempt fails deny-by-default | forbidden credential/network and handoff-resume tests | Terminal Builder state contains validated handoff only | No Visual Asset Editor or Delegation runtime is introduced |

## Non-Goals And Migration

No general software factory, maximum-agent objective, final harness execution, or V2.1 workflow migration is included. Future Workflow IR versions require explicit migration and rollback.
