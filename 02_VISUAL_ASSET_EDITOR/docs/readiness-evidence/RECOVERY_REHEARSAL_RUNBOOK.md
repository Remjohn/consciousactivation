# Recovery and Rollback Rehearsal Runbook

Status: `awaiting_external_runtime`  
Classification: `non_production_readiness_proof`

This rehearsal exercises the minimal proof topology only. It does not promote a runtime or authorize production recovery behavior.

## Preconditions

- The local and cloud workers have passed their immutable-runtime preflight.
- Object storage, queue, events, cancellation, checkpoints, scoped identities and cost boundaries are approved.
- The same Format 02 plan/workflow/resource hashes are accepted for both workers.
- A prior pinned runtime profile and its known-good receipts are recorded as the rollback baseline.
- Accepted artifact and receipt hashes are captured before any failure injection.

## Scenario 1 — Worker interruption and checkpoint recovery

1. Submit a proof job with a unique idempotency key.
2. Wait for `RUNNING` and a durable `CheckpointCommitted` event.
3. Interrupt the worker without cancelling the logical job.
4. Observe lease expiry and `ORPHANED` or `RETRYABLE_FAILED`.
5. Start a compatible worker and restore only from the hash-verified checkpoint.
6. Observe `RECOVERING`, `JobRecovered`, and eventual terminal state.

Pass evidence: interruption time, lease/fencing tokens, checkpoint hash, restored runtime/workflow hashes, ordered events and final receipt.

## Scenario 2 — Infrastructure retry versus quality repair

Cause a retryable infrastructure failure after submission. Verify that the controller increments infrastructure-attempt count but leaves semantic quality-repair round unchanged. Duplicate delivery must not create a second promoted result.

Pass evidence: before/after counters, duplicate-delivery trace, fencing decision and single output commit.

## Scenario 3 — Provider fallback

1. Interrupt the active provider after a portable checkpoint.
2. Confirm fallback authority, cost boundary and target runtime attestation.
3. Restore the identical plan/workflow/resources on the alternate worker.
4. Complete the logical job under the original idempotency lineage.

Pass evidence: source and target provider IDs, checkpoint portability, identical semantic hashes, new infrastructure-attempt receipt and no quality-round consumption.

## Scenario 4 — Failed runtime-profile promotion

Stage, but do not authorize, a candidate runtime profile containing a controlled failed acceptance condition. Verify that it is quarantined, receives no new proof jobs and never changes the active pin.

Pass evidence: candidate/active profile hashes, failed gate, quarantine event and unchanged active routing.

## Scenario 5 — Rollback to prior pinned runtime

Route the next proof job to the prior known-good runtime profile. Verify its OCI, ComfyUI, lock, resource and workflow hashes before execution. Produce a new rollback receipt that references the failed candidate without adopting it.

## Scenario 6 — Preservation audit

Re-hash every pre-rehearsal accepted asset, Asset Result, production-acceptance record, simulated consumption acknowledgement and usage receipt. Verify object versions, retention and retrieval after interruption, fallback and cleanup.

## Evidence and verdict

Capture sanitized request/response records, ordered events, state transitions, checkpoint manifests, compute/cost receipts, retry counters, promotion/rollback decisions and before/after preservation hashes. Each scenario is non-compensable.

Recovery readiness passes only when all six scenarios pass on real external runtimes. Simulation remains useful evidence but cannot substitute for observed worker interruption, checkpoint restoration, provider fallback and rollback.
