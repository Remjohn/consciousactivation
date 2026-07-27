# Self-Hosted GPU Setup Runbook

Status: `awaiting_operator_runtime`  
Classification: `non_production_readiness_proof`

This runbook prepares one self-hosted Docker GPU worker for the already approved Format 02 proof. It is not production deployment guidance. The current GTX 960M/2 GiB environment is `not_proof_capable` unless a new recorded preflight disproves the existing evidence.

## 1. Operator inputs

Before provisioning, complete every null field in `SELF_HOSTED_GPU_REQUIREMENTS.yaml` in a separately reviewed execution-input record. Supply exact OS, Docker, NVIDIA runtime, OCI digest, ComfyUI commit, custom-node lock, Python lock, model/VAE/LoRA hashes, workflow hash, and storage/queue endpoints. Store credentials in an external secret manager and place only credential references in evidence.

The minimum admission floor is one supported NVIDIA GPU with 12 GiB VRAM, 32 GiB host RAM, and 250 GiB free proof storage. The preferred profile is 24 GiB VRAM, 64 GiB RAM, and 500 GiB storage. The selected workflow or resource manifest may require more.

## 2. Host preflight

Run and retain unredacted machine-readable output in the controlled evidence store; commit only sanitized evidence:

```powershell
nvidia-smi --query-gpu=name,uuid,driver_version,memory.total --format=csv
docker version
docker info
docker run --rm --gpus all <OPERATOR_APPROVED_GPU_PROBE_IMAGE_BY_DIGEST> nvidia-smi
```

Fail closed if GPU passthrough, the Docker Linux engine, required VRAM, storage, or the driver/runtime compatibility check fails.

## 3. Verify immutable runtime

```powershell
docker pull <REGISTRY>/<REPOSITORY>@sha256:<DIGEST>
docker image inspect <REGISTRY>/<REPOSITORY>@sha256:<DIGEST>
```

Compare the observed digest with the approved input. Inside an isolated one-shot container, emit the ComfyUI commit, Python lock hash, custom-node inventory, and mounted resource hashes. Reject mutable-tag-only bindings, startup installs, unhashed nodes, writable model mounts, or unexpected resources.

## 4. Prepare proof mounts

Create operator-owned, proof-scoped input, output, checkpoint, log, and scratch locations. Inputs and resources are read-only; outputs and checkpoints are content addressed. Bind the proof worker to the scoped object-storage, queue, and secret-manager identities. Network access is denied except for the approved endpoints.

## 5. Start the worker

Use the operator-approved compose or orchestration file whose hash is recorded in the execution receipt. The launch must bind the exact OCI digest, resource manifest, adapter-port mapping, concurrency `1`, and proof scope. Do not install dependencies during startup.

```powershell
docker compose -f <APPROVED_COMPOSE_FILE> up -d
Invoke-RestMethod <PROOF_ADAPTER_BASE_URL>/healthz
Invoke-RestMethod <PROOF_ADAPTER_BASE_URL>/readyz
```

## 6. Submit the pinned plan

Submit `reference-slice/FORMAT02_MINIMAL_COACH_THEATRE/proofs/format02_visual_production_plan.json` through the logical proof adapter with an idempotency key and the exact workflow/resource manifest references. Save the sanitized request, response, ordered events, checkpoints, output hashes, latency, and local cost calculation.

Poll status and events using the routes in the requirements YAML. Retrieve the result only after `OutputCommitted`. A success without the matching runtime attestation and output hash is invalid.

## 7. Exercise cancellation

Submit a fresh proof job, wait for `RUNNING`, request cancellation, and retain `CANCELLATION_REQUESTED` and terminal `CANCELLED` evidence. Verify that no partial output is promoted and that checkpoints follow the retention rule.

## 8. Closeout

Stop and remove proof containers, revoke scoped leases, inventory retained proof objects, and record cleanup. Do not delete accepted proof artifacts or their receipts. Run the acceptance matrix and update `LOCAL_GPU_PROOF.md` only from observed evidence.

