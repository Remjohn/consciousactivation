# TS-VAE-04 Containerized Visual Compute Fabric

Status: draft for architecture validation  
Implementation authorization: no

## 1. Specification identity

- Feature: F12
- Owned FRs: FR-089 through FR-096
- Owned NFRs: NFR-COMPUTE-001 through NFR-COMPUTE-005
- Decision: D015
- Components: `ComputeScheduler`, `WorkerRegistry`, `ComputeFabricPort`, `ArtifactMountService`, local/cloud worker adapters, `RecoveryCoordinator`

## 2. Evidence read

VAE F08/F10/F12 shards; plan, compatibility, Budget Program, readiness, and benchmark artifacts; Format 02 release proof; Delegation failure taxonomy, budget/cancellation lifecycle, resilience cases; Stage 1 inventory confirming no current Docker/GPU assets.

## 3. Problem, solution, and scope

Visual production must run reproducibly on local/self-hosted and cloud GPUs while preserving exact runtime/model state, isolation, budget, checkpoints, and recovery. The solution is a provider-neutral compute fabric with immutable runtime profiles and leased jobs. Workers have no canonical planning or acceptance authority.

In scope: worker/runtime registry, OCI/container contract, scheduling, model mounts, storage, lease/heartbeat, cancellation, retry/failover, local/cloud equivalence, receipts, and fault isolation. Out of scope: plan compilation, candidate selection, evaluation authority, cloud-provider procurement, or mutable interactive ComfyUI sessions.

## 4. Architecture and models

Release 1 uses one logical control-plane scheduler and multiple replaceable worker adapters. A certified runtime profile includes OCI image digest, ComfyUI commit, custom-node lock, Python dependency lock, CUDA/driver constraints, GPU/VRAM class, CPU/RAM/scratch limits, network policy, mounted resource policy, health probes, output contract, and certification evidence.

`ComputeJob`: job ID, execution/plan/stage/artifact refs, capability bundle, input object refs/hashes, output declarations, resource request, budget reservation, priority/deadline, idempotency key, attempt/failover policy, tenant/security context, and cancellation token.

`WorkerLease`: worker/profile/provider/region, lease token hash, acquired/expiry/heartbeat, reserved resources, attempt ID, and fencing epoch.

`ComputeReceipt`: exact image/runtime/resource locks, start/end, GPU/CPU/RAM/storage/network measurements, inputs/outputs with hashes, provider job ID, checkpoints, logs/traces, exit/failure code, retry relation, and cost.

Canonical metadata/events are persisted through control-plane repositories; large immutable inputs, outputs, masks, graphs, logs, and receipts use S3-compatible content-addressed storage. Workers use scoped pre-signed access and cannot list unrelated objects.

## 5. State machine and flows

Job states: `CREATED`, `QUOTED`, `RESERVED`, `QUEUED`, `LEASED`, `PULLING`, `RUNNING`, `CHECKPOINTING`, `SUCCEEDED`, `RETRYABLE_FAILED`, `TERMINAL_FAILED`, `CANCELLATION_REQUESTED`, `CANCELLED`, `ORPHANED`, `RECOVERING`.

Fencing prevents a lost worker and replacement worker from committing the same attempt. Only the current lease epoch may commit outputs. Output promotion requires hash verification and a success receipt; late outputs from cancelled/superseded jobs are quarantined as evidence.

Local/cloud flow: scheduler resolves eligible runtime profiles -> obtains deterministic quote -> reserves budget -> enqueues job -> worker leases -> verifies image/resources/inputs -> executes compiled artifact -> checkpoints -> uploads immutable outputs -> emits receipt -> scheduler commits result and releases reservation.

## 6. Interfaces, APIs, queues, events, and adapters

```text
quote(job_spec, runtime_candidates) -> ComputeQuote[]
submit(job_spec, selected_profile, budget_reservation) -> ComputeJobRef
lease(worker_identity, capabilities) -> WorkerLease | none
heartbeat(lease, progress, measurements) -> LeaseStatus
checkpoint(lease, checkpoint_manifest) -> CheckpointRef
complete(lease, output_manifest, receipt) -> CommitResult
fail(lease, failure_fact) -> RetryOrTerminalDecision
cancel(job_ref, authority_ref) -> CancellationDisposition
```

Queue delivery is at-least-once; job effect is exactly-once by idempotency, lease fencing, and output commit transaction. Events: `ComputeQuoted`, `JobQueued`, `WorkerLeased`, `JobStarted`, `CheckpointCommitted`, `JobRecovered`, `JobFailed`, `JobCancelled`, `OutputCommitted`, `WorkerQuarantined`.

Adapters implement the same port for local Docker GPU and one cloud GPU provider. Provider IDs never leak into plan IR or Delegation contracts; receipts retain them for operations/cost.

## 7. Cross-cutting production contract

| Concern | Required behavior |
|---|---|
| Visual Production Plan IR | Job references exact stage and compiled artifact; worker cannot replan. |
| ComfyUI/registries | Only TS-VAE-03 validated artifacts and digest-pinned bundles execute. |
| Docker/custom nodes | Image digest and lock manifests are verified before lease enters RUNNING; no startup installation. |
| Model/VAE/LoRA storage | Read-only digest-addressed mounts, cache verification, no worker mutation. |
| Deterministic/VLM | Scheduler/worker lifecycle is deterministic. Generation may be stochastic only through receipted seed/parameter policy. VLM evaluation is a separate job/adapter. |
| Budget/candidates | Reservation precedes queueing; actual usage debits TS-VAE-05; overrun stops at safe boundary. |
| Evaluation/repair | Worker returns candidates only. Acceptance/repair are separate nodes. |
| Idempotency/checkpoints | Job key includes artifact, inputs, stage, candidate, and attempt policy. Checkpoints are immutable and hash-verified. |
| Observability/cost | Per-job traces, queue/lease/runtime/cache metrics, health, resource/cost receipt, and failure family. |
| Security/isolation | Rootless/non-privileged container, read-only root, scoped mounts, device limits, deny-by-default network, no host socket, secrets via ephemeral injection. |
| Migration/rollback | Runtime profiles are immutable. New image/driver/node versions create new profiles; active jobs retain old profile; rollback reselects prior certified digest. |

## 8. Scheduling and recovery rules

1. Eligibility filters capability, runtime compatibility, certification, security, region/data policy, VRAM, deadline, and budget before optimization.
2. Ranking may consider expected completion, reliability, cache locality, cost, and recovery risk; quality requirements remain fixed.
3. A worker must attest profile and resource hashes before receiving protected inputs.
4. Provider timeout, worker loss, GPU reset, container crash, and transient storage outage are infrastructure failures and do not consume quality rounds.
5. Retry uses the same compiled artifact and creative bindings unless a typed repair/replan creates a new plan version.
6. Successful checkpoints and outputs are reused only after hash and compatibility validation.
7. Missing custom node/model, digest mismatch, isolation violation, or corrupted cache quarantines the worker/profile and blocks retry there.
8. Cancellation stops new work immediately and reaches the next declared atomic checkpoint for active kernels; late promotion is forbidden.
9. Backpressure exposes queue depth, eligible capacity, and expected delay; it cannot route to uncertified capability or reduce evaluation.
10. Local/cloud equivalence requires the same logical inputs/artifact and semantically equivalent outputs/receipts, not bit-identical stochastic pixels.

## 9. Failure, degradation, and operational targets

Use Delegation codes `GPU_UNAVAILABLE`, `CONTAINER_START_FAILED`, `MODEL_LOAD_FAILED`, `CUSTOM_NODE_MISSING`, `PROVIDER_TIMEOUT`, `OBJECT_STORAGE_UNAVAILABLE`, and `WORKER_LOST`. Internal codes add `LEASE_FENCED`, `RUNTIME_ATTESTATION_FAILED`, `CACHE_INTEGRITY_FAILED`, and `OUTPUT_COMMIT_CONFLICT`.

Recoverable failures retry within plan and budget limits, then fail over to a compatible certified profile. No compatible profile produces `CAPABILITY_GAP`. Isolation/integrity failures block and trigger an incident. Recovery target is at least 99% for injected recoverable failures without committed-state loss or quality-round corruption.

## 10. Performance, security, and storage

Scheduler metrics cover queue p50/p95/p99, lease latency, cold start, model load, execution, checkpoint, upload, cache hit, GPU utilization, failure/recovery, and cost. Resource limits are hard cgroup/device limits. Object retention separates temporary candidates, accepted masters, evidence, and security quarantine; deletion follows lifecycle/hold policy and never erases required historical proof.

No worker receives long-lived cloud credentials. External network is disabled unless a runtime profile explicitly allowlists an endpoint required by a certified adapter. Logs redact prompts, secrets, signed URLs, and protected media.

## 11. Implementation plan

1. Define runtime, worker, job, lease, checkpoint, output, quote, and receipt schemas.
2. Implement control-plane repository, transactional queue/outbox adapter, fencing, and commit protocol through `WorkflowRuntimePort`.
3. Build one immutable local GPU image/profile from TS-VAE-03 locks.
4. Implement S3-compatible artifact mounts, cache verification, and scoped access.
5. Implement local adapter, then one cloud adapter against the same conformance contract.
6. Add health/quarantine, cancellation, retry/failover, budget debit, and telemetry.
7. Run cold/warm, fault-injection, isolation, local/cloud equivalence, migration, and rollback proof.

## 12. Given/When/Then acceptance criteria

1. Given a mutable image tag, when a job is submitted, then it is rejected before queueing.
2. Given a worker with a mismatched custom-node hash, when it attests, then it is quarantined and receives no inputs.
3. Given duplicate queue delivery, when workers lease, then fencing permits one committed output only.
4. Given worker loss after a checkpoint, when recovery runs, then execution resumes from the checkpoint with the same artifact/bindings and no quality round consumed.
5. Given cancellation racing with completion, when the cancellation precedence applies, then stale output cannot be promoted and a disposition receipt preserves evidence/cost.
6. Given budget exhaustion, when the next atomic boundary is reached, then work checkpoints and requests authorization rather than silently degrading.
7. Given local and cloud certified profiles, when the Format 02 job runs, then both return valid receipts and contract-equivalent output manifests.
8. Given rollback to a prior runtime profile, when a compatible historical job is replayed, then its locks and receipt identity are reproducible.

## 13. Testing strategy

Unit-test eligibility, ranking, leases, fencing, idempotency, metering, and cancellation. Integration-test OCI/runtime attestation, resource mounts, object store, worker protocol, local/cloud adapters, and outbox. Fault-inject crash, GPU loss, timeout, bus/storage outage, corrupt cache, missing node, duplicate/out-of-order events, and late completion. Run isolation scans, performance/cost benchmarks, and Format 02 reference execution.

## 14. Non-goals

- A general cloud abstraction or support for every GPU provider.
- Mutable pet workers, interactive production sessions, or manual graph repair.
- Worker-owned planning, evaluation, promotion, lifecycle, or Delegation authority.
- Production certification before one local and one cloud proof pass.
