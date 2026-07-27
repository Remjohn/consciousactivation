# CRC-403 Operator Inputs

Status: `WAITING_FOR_OPERATOR_INFRASTRUCTURE`  
Classification: `non_production_readiness_proof`  
Stage 5 and production implementation: `NOT AUTHORIZED`

Provide the following concrete values before any external proof. Secret values must remain in an external secret manager, workload identity, keychain, or operator-controlled environment. Supply only credential references and sanitized identities to the repository or Codex transcript.

## 1. Evaluator and calibration

| Required value | Operator response |
|---|---|
| Evaluator provider | `<provider>` |
| Deployment mode | `<managed_api | private_endpoint | isolated_self_hosted>` |
| Endpoint/service reference | `<non-secret stable reference>` |
| Exact model identifier | `<model-id>` |
| Exact model version/release | `<version>` |
| Weight digest or provider release identity | `<sha256 or immutable provider identity>` |
| Runtime/API version | `<exact version>` |
| Approved invocation method | `<API operation, CLI/client reference, and input/output contract>` |
| Evaluator principal | `<identity reference>` |
| Producer principal | `<different identity reference>` |
| Credential reference | `<secret-manager URI, workload identity, keychain entry, or environment-variable name>` |
| Region and retention policy | `<region; policy reference>` |
| Deterministic settings | `<seed/temperature/schema mode or provider equivalent>` |
| Rate, concurrency and cost limits | `<limits>` |
| Evaluation/product authority approval receipt | `<receipt reference>` |
| Governed calibration corpus | `<manifest path/URI and SHA-256; at least 30 adjudicated unique cases>` |
| Protected-set seal | `<custodian, manifest URI/hash, seal receipt, access authority>` |
| Non-compensable gate approval | `<decision receipt>` |

The repository already supplies the profile, evaluation program, prompt, schemas, rubric, provisional seed, protected-set procedure, error-analysis procedure and threshold-calibration procedure. Do not recreate them.

## 2. Self-hosted proof worker

| Required value | Operator response |
|---|---|
| Machine/endpoint | `<machine identity and reachable endpoint>` |
| OS/kernel or WSL version | `<exact versions>` |
| GPU and UUID | `<model; UUID>` |
| VRAM | `<GiB; minimum 12, or higher model requirement>` |
| Host RAM and free proof storage | `<GiB; minimum 32 and 250>` |
| NVIDIA driver/CUDA compatibility | `<exact versions>` |
| Docker/Compose/NVIDIA runtime | `<exact versions>` |
| Worker OCI image | `<registry/repository@sha256:digest>` |
| ComfyUI identity | `<repository and exact commit/version>` |
| Custom-node and Python locks | `<paths/URIs and SHA-256 values>` |
| Model, VAE, LoRA and control resources | `<read-only mount references and SHA-256 values>` |
| ComfyUI API workflow | `<path/URI and SHA-256>` |
| Proof adapter base URL | `<health, readiness, submit, status, events, cancel, result mapping>` |
| Worker identity/credential reference | `<non-secret reference>` |

The observed GTX 960M/2 GiB environment is `not_proof_capable` and cannot satisfy this input.

## 3. Cloud worker and spend authority

| Required value | Operator response |
|---|---|
| Cloud provider | `<provider>` |
| Account/project/subscription | `<identity>` |
| Region | `<region>` |
| Permitted GPU type/SKU | `<exact SKU; at least 12 GiB VRAM or higher model requirement>` |
| Maximum worker count | `1` |
| Credential reference | `<non-secret scoped reference>` |
| Worker/workload identity | `<identity reference>` |
| Cost ceiling | `<currency; hourly maximum; total maximum; hard-stop method>` |
| Network policy | `<ingress/egress allowlist; public/private endpoint decision>` |
| Cancellation authority | `<authorized identity and operation>` |
| Cleanup/retention policy | `<worker, disk, credential and evidence retention rules>` |
| Paid-resource authorization receipt | `<explicit approval reference>` |

The cloud runtime must use the same semantic plan, workflow, OCI, ComfyUI, node, Python and resource hashes proven by the self-hosted worker.

## 4. Storage, queue and checkpoints

| Required value | Operator response |
|---|---|
| Object-storage provider/endpoint | `<provider and endpoint reference>` |
| Input/output/checkpoint/evidence containers | `<versioned container references>` |
| Encryption key reference | `<non-secret key reference>` |
| Queue/job transport | `<provider, endpoint, queue/topic>` |
| Status-event endpoint | `<stream/topic reference>` |
| Dead-letter endpoint | `<reference>` |
| Visibility timeout/heartbeat/max attempts | `<values>` |
| Proof controller, worker and evaluator identities | `<scoped references>` |
| Cancellation operation | `<operation reference>` |
| Checkpoint and result retention | `<policy>` |

The transport must provide at-least-once delivery with idempotency and fencing, ordered status evidence, hash-verified checkpoints, cancellation, and content-addressed result retrieval.

## 5. Approved Format 02 inputs

Approve or replace each exact source reference. Any replacement requires its own governed path/URI and SHA-256.

| Candidate source fixture | Current SHA-256 | Approval/Replacement |
|---|---|---|
| `reference-slice/FORMAT02_MINIMAL_COACH_THEATRE/contracts/visual_asset_demand.reference.yaml` | `sha256:d64e030f4c85ae190a304302155c4873731e0e7ac42e6fa78e345e2e607317d6` | `<approval receipt or replacement>` |
| `reference-slice/FORMAT02_MINIMAL_COACH_THEATRE/contracts/visual_production_plan.reference.yaml` | `sha256:5b8acfb1b16a18ab829ed434b3fa98ffddb5dcd6a9ade801c7554feccf0a4b31` | `<approval receipt or replacement>` |
| `reference-slice/FORMAT02_MINIMAL_COACH_THEATRE/contracts/visual_quality_evaluation.reference.yaml` | `sha256:78f651192194b1daed2b70c2136b99b9a07073226294e4f5c42c65faaf339bd7` | `<approval receipt or replacement>` |
| Controlled character/source fixture | `<operator-approved URI/path and SHA-256>` | `<rights/consent and proof-use approval>` |

The two existing SVGs are controlled fixture evidence, not GPU-produced candidates. They may be approved as calibration examples but cannot satisfy the real compute proof.

## 6. Recovery authority

Provide the fault-injection window, authorized interrupter/canceller identity, checkpoint-restore authority, alternate-provider fallback authority and budget, failed-runtime-promotion fixture, prior known-good runtime/evaluator baseline, rollback approver, accepted-artifact preservation set, and cleanup approval.

After every field above is complete, issue only the P1 command in `CRC403_EXECUTION_COMMANDS.md`. Do not authorize P2-P5 in the same instruction.

