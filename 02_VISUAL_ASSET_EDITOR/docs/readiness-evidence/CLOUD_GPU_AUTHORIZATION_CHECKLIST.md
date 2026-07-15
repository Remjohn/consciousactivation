# Cloud GPU Authorization Checklist

Status: `awaiting_operator_authorization`  
Classification: `non_production_readiness_proof`

No paid cloud resource may be created from this package alone. The operator must complete and approve every item below. Secrets remain outside the repository.

## Identity and scope

- [ ] Approved provider and exact account/tenant are named.
- [ ] Approved project/subscription and region are named.
- [ ] A temporary credential reference and its least-privilege scope are recorded; no credential value is committed.
- [ ] The runtime workload identity and proof-controller identity are distinct where the provider permits it.
- [ ] The approving human and authorization receipt are recorded.

## Resource and cost authority

- [ ] One permitted GPU SKU/class is named and meets the 12 GiB VRAM proof floor plus any higher model requirement.
- [ ] Maximum worker count is one.
- [ ] Currency, hourly ceiling, total ceiling, and hard-stop method are explicit.
- [ ] The identity allowed to cancel jobs and destroy resources is named.
- [ ] Paid-resource provisioning is explicitly authorized for this proof run.

## Runtime and network

- [ ] The exact OCI digest is approved and matches the self-hosted plan.
- [ ] ComfyUI commit, custom-node lock, Python lock, resource manifest, workflow and plan hashes are approved.
- [ ] Startup package installation is disabled.
- [ ] Ingress and egress allowlists are explicit; public IP use is approved or denied.
- [ ] TLS and private-endpoint requirements are recorded.

## Storage, queue, and recovery

- [ ] Input, output, checkpoint, event, queue and dead-letter endpoint references are supplied.
- [ ] Versioning, encryption, content-hash verification, retention and cleanup are enabled.
- [ ] At-least-once delivery, idempotency, fencing, visibility timeout and maximum attempts are configured.
- [ ] Provider fallback is separately authorized and has its own identity/cost ceiling.
- [ ] Accepted artifacts and receipts survive worker teardown and fallback.

## Closeout

- [ ] Ephemeral worker and disks will be destroyed after evidence capture.
- [ ] Temporary credentials will be revoked.
- [ ] Retained proof objects and expiration date will be inventoried.
- [ ] A sanitized cost, cancellation, result-retrieval and cleanup receipt will be committed.

If any item is incomplete, cloud execution remains `BLOCKED` and no resource is provisioned.

