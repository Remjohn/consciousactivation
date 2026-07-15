# Self-Hosted GPU Acceptance Tests

Status: `not_executed`  
Classification: `non_production_readiness_proof`

Every required test is non-compensable. Record command, timestamp, actor, sanitized output location, and receipt hash. A parsed configuration does not count as execution proof.

| ID | Test | Pass evidence |
|---|---|---|
| SHG-001 | Host identity | Pinned OS, kernel/WSL, CPU, RAM, GPU, UUID, driver and VRAM inventory |
| SHG-002 | Admission floor | At least 12 GiB VRAM, 32 GiB RAM and 250 GiB free proof storage, plus any higher model requirement |
| SHG-003 | Docker health | Healthy Linux engine and exact engine/Compose versions |
| SHG-004 | GPU passthrough | Digest-pinned probe container observes the expected GPU and VRAM |
| SHG-005 | OCI binding | Observed image digest equals the approved digest; mutable tag is not authoritative |
| SHG-006 | ComfyUI binding | Runtime reports the approved ComfyUI commit/version |
| SHG-007 | Node and Python locks | Runtime inventory matches both lockfile hashes with no startup install |
| SHG-008 | Resource integrity | Model, VAE, LoRA and control-resource hashes match; mounts are read-only |
| SHG-009 | Workflow integrity | ComfyUI API workflow and Visual Production Plan hashes match the submission |
| SHG-010 | Isolation | Least-privilege identity, scoped secrets and approved network allowlist are observed |
| SHG-011 | Health/readiness | Every required health item passes before job admission |
| SHG-012 | Job lifecycle | Idempotent submission yields ordered state/events through `OutputCommitted` |
| SHG-013 | Checkpoint | A content-addressed checkpoint is persisted and retrievable |
| SHG-014 | Result | Candidate and receipt hashes match retrieved objects; latency and cost are recorded |
| SHG-015 | Cancellation | A running job reaches `CANCELLED` without promoting partial output |
| SHG-016 | Repeatability | A second controlled run preserves immutable bindings and produces a complete receipt |

## Mandatory rejection cases

- The current GTX 960M/2 GiB host remains `not_proof_capable` unless all admission and execution tests pass on newly observed evidence.
- Reject mutable image tags, missing hashes, unhashed custom nodes, startup installs, shared long-lived credentials, unexpected network access, or writable resource mounts.
- Reject a job that can be submitted but cannot enforce the pinned workflow and resource identities.
- Reject a nominal success without ordered events, output commit, compute receipt, cost, and latency.

Acceptance requires `16/16 PASS`; otherwise the self-hosted compute proof remains open.
