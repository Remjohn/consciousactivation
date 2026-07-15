# Cloud GPU Execution Runbook

Status: `not_authorized_for_execution`  
Classification: `non_production_readiness_proof`

This is a provider-neutral proof runbook. The operator must supply the provider-specific CLI or infrastructure command set and approve paid resource creation. It does not authorize Stage 5 or production deployment.

## 1. Validate authorization

Complete `CLOUD_GPU_REQUIREMENTS.yaml` and `CLOUD_GPU_AUTHORIZATION_CHECKLIST.md`. Verify the active identity against the approved account, project, region, credential reference, GPU class, worker count, and cost ceiling. Stop if the provider reports a different scope.

Never paste secrets into a command transcript. Resolve the credential reference through the approved external secret manager.

## 2. Bind immutable inputs

Verify that the cloud worker uses the same Visual Production Plan, workflow hash, OCI digest, ComfyUI commit, node/Python locks and resource-manifest hash as the accepted self-hosted proof input. Provider bootstrap code may differ but must be digest pinned and may not change contract behavior.

Reject mutable tags, startup installation, missing resource hashes, or migrations that guess runtime identity.

## 3. Create proof-scoped infrastructure

Using the operator-approved commands:

1. Create or select versioned input, output and checkpoint object locations.
2. Create or select the proof queue, event stream and dead-letter path.
3. Bind the least-privilege worker identity.
4. Apply ingress/egress restrictions and hard cost controls.
5. Provision no more than one permitted GPU worker.

Record sanitized provider request IDs, resource IDs, policy hashes and timestamps. Provisioning is invalid without a cost boundary and cancellation authority.

## 4. Attest the worker

Before job admission, collect GPU/VRAM, driver, OCI digest, ComfyUI commit, custom-node lock, Python lock, resource inventory, workflow and storage/queue connectivity. Compare each value with the approved input record. Quarantine the worker on any mismatch.

## 5. Execute the shared plan

Upload content-addressed inputs, submit the same Format 02 plan with a unique idempotency key, and observe quote, queue, lease, start, checkpoint and output-commit events. Retrieve the candidate and receipts through object storage, not an untracked local path.

Record provider-neutral job ID, provider job ID, API request/response, event order, checkpoint, output hashes, latency, GPU seconds and itemized cost. A parseable response without enforced immutable bindings fails.

## 6. Timeout and cancellation

Run a bounded cancellation case on a fresh job. Invoke the approved cancellation authority, observe `CANCELLATION_REQUESTED` then `CANCELLED`, confirm no partial output promotion, and record the final provider charge. Also confirm the configured timeout causes a terminal, observable state.

## 7. Retrieve and compare

Retrieve result, event, checkpoint, cost and compute receipts. Compare the cloud plan and semantic input hashes with the self-hosted run. Hardware-specific latency may differ; the provider-neutral plan and enforced semantic fields may not.

## 8. Cleanup

Terminate the worker, delete ephemeral disks, revoke temporary credentials, close queue leases, and apply the approved proof-object retention policy. Confirm accepted proof objects and receipts remain retrievable. Record zero active GPU workers and the final cost.

Only observed evidence may update `CLOUD_GPU_PROOF.md`; otherwise its status remains blocked.
