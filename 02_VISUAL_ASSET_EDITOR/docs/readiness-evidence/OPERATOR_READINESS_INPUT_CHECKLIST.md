# Operator Readiness Input Checklist

Status: `awaiting_external_inputs`  
Classification: `non_production_readiness_proof`  
Stage 5: `NOT AUTHORIZED`

This checklist is the handoff between the completed proof design and external execution. Do not place secret values in this repository; record only external credential references and sanitized receipts.

## Operator must provide or approve

- [ ] Evaluator provider/deployment, exact model or weight identity/digest, API/runtime version, region/endpoint reference, deterministic settings, separate producer/evaluator identities, credential reference, cost/data-retention terms, and human selection approval.
- [ ] At least 30 unique, rights-cleared and adjudicated Format 02 calibration cases covering every family in `CALIBRATION_CORPUS_REQUEST.yaml`.
- [ ] Protected-set owner, custodian, approved size, disjoint cases, storage/credential references, seal attestation and run authority.
- [ ] Self-hosted host identity and a GPU meeting the 12 GiB proof floor or any higher selected-model requirement; OS, Docker, NVIDIA runtime and storage evidence.
- [ ] Exact OCI digest, ComfyUI commit/version, custom-node and Python locks, model/VAE/LoRA/control-resource hashes, workflow hash and Visual Production Plan hash.
- [ ] Cloud provider, account/project, region, temporary credential reference, permitted GPU class, hard cost ceilings, network policy, worker/cancellation identities, storage/queue endpoints, retention and cleanup approval.
- [ ] Minimal object-storage, queue, event, checkpoint and dead-letter endpoints with versioning, hashing, idempotency and fencing settings.
- [ ] Prior pinned known-good runtime/evaluator baseline and authority to rehearse interruption, fallback and rollback.
- [ ] Explicit approval before any paid cloud resource is provisioned.

## Codex can generate after inputs exist

- [x] Input schemas, operator runbooks, logical proof ports and acceptance matrices in this package.
- [ ] Sanitized immutable input manifests and preflight reports from operator-supplied values.
- [ ] Hash inventories, request/response templates, event/receipt validation and discrepancy reports.
- [ ] Calibration, false-positive/false-negative, threshold-candidate and protected-run reports from observed labeled evidence.
- [ ] Local/cloud comparison, recovery/rollback and Format 02 evidence reports from real execution artifacts.
- [ ] Updated readiness verdicts after every non-compensable gate is rerun.

Codex cannot select an unauthorized evaluator, invent labels or thresholds, create missing credentials, approve spend, claim unseen execution, or authorize Stage 5.

## External infrastructure required

| Resource | Required state |
|---|---|
| Independent evaluator | Selected and immutable identity/version supplied; credentials separate from producer |
| Self-hosted Docker GPU worker | Real worker meets admission floor and passes all 16 acceptance tests |
| Cloud Docker GPU worker | Authorized provider scope, exact runtime, hard budget, cancellation and cleanup |
| Object storage | Versioned, content addressed, encrypted and independently retrievable |
| Queue and status events | At-least-once delivery with idempotency, fencing, terminal states and dead-lettering |
| Checkpoint store | Versioned, hash verified and portable between approved workers |
| External secret manager | Short-lived or workload credentials; repository contains references only |
| Protected-set store | Custodian-controlled, sealed, blinded and inaccessible to tuning |

## Still unavailable now

- Evaluator selection, immutable identity and credentials.
- Governed adjudicated calibration corpus and sealed protected set.
- Final empirically calibrated thresholds and evaluator certification.
- A proof-capable self-hosted worker; the observed GTX 960M/2 GiB host is `not_proof_capable`.
- Authorized cloud identity, GPU allocation and cost/cancellation authority.
- Executed storage/queue/checkpoint, recovery, provider-fallback and rollback evidence.
- Live governed evidence for `SRC-001` and `SRC-009`.
- Formal implementation authorization; readiness remains `FAIL` and Stage 5 remains closed.

## Exact next command after all inputs are supplied

First run the repository package validator from the repository root:

```powershell
python -B proofs/evaluator/validate_evaluator_foundation.py
```

Then send Codex this exact execution command:

> Execute the Visual Asset Editor external readiness preflight using the completed inputs referenced by `docs/readiness-evidence/OPERATOR_READINESS_INPUT_CHECKLIST.md`. Validate identities, hashes, credentials by reference, cost authority, infrastructure reachability and protected-set custody only. Do not provision paid resources, run proof workloads, begin Stage 5, or change the readiness verdict during preflight. Report every missing or mismatched input and stop.

Only after that preflight reports `PASS` may the operator separately authorize the local proof, paid cloud proof, recovery rehearsal and protected-set run. No such execution is authorized by this checklist.
