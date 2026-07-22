# Visual Asset Editor Readiness Closure Plan

Updated: 2026-07-15  
Authority: Visual Asset Editor PRD V1.1 and Activative Intelligence Constitution V1.1  
Current implementation-readiness verdict: **FAIL**  
Stage 5: **NOT AUTHORIZED**

Delegation `1.1.0-rc.4` is pinned and passes the bounded local contract-integration gate as `local_unsigned_release_candidate`, including portable derivative-lock inheritance. This does not certify the evaluator, prove compute or recovery, restore unavailable sources, approve the product/architecture, or confer production trust.

## Prioritized closure sequence

| Priority | Closure work | Required evidence | Owner / approver | Exit rule |
|---:|---|---|---|---|
| 1 | Evaluator calibration and certification | Executed calibration, arbitration and protected-set reports for every applicable dimension, responsible layer, hard gate, wrong-reading lock and conditional no-text route | Evaluation authority and product authority | Profile advances from `specified_not_certified` only after every evidence package and gate passes |
| 2 | Evaluator and program version pins | Immutable evaluator provider/model or weight digest, API/runtime, prompt/program/template digest, deterministic settings, credential boundary and independent-producer proof | Evaluation authority | Every receipt resolves exact evaluator and program identities and fails closed on drift |
| 3 | Labeled calibration corpus | Versioned manifest, provenance/consent, constitutional references, adjudicated labels, ambiguity notes, balance, reviewer agreement and digest | Evaluation authority and data steward | Approved reproducible development/calibration partitions cover all required profile slices |
| 4 | Protected regression set | Sealed manifest/digest, non-overlap proof, access controls and golden/borderline/adversarial/repair/wrong-reading/no-text cases | Evaluation and release authorities | Set remains untuned, executes under release controls and produces retained evidence |
| 5 | Threshold and non-compensable-gate decisions | Approved per-dimension thresholds, precedence, uncertainty/arbitration, false-positive/false-negative limits, affinity terminology/alias policy and rollback triggers | Evaluation and product authorities | No score can compensate for a failed constitutional gate; all decisions are versioned and empirically justified |
| 6 | Local GPU compute proof | Pinned OCI image, OS/Python/CUDA/driver, ComfyUI and node digests, model/VAE/LoRA digests, GPU profile, deterministic controls, security/isolation, cost and restart receipts | VAE platform owner | Representative Format 02 workload passes execution, cancellation, checkpoint, restart, evaluation and receipt validation locally |
| 7 | Cloud GPU compute proof | Pinned cloud provider/adapter/profile, image parity, quote/cost/isolation, credentials, checkpoint portability, failover and local/cloud equivalence receipts | VAE platform owner | Identical production ports pass representative execution and failover without semantic or receipt drift |
| 8 | Recovery proof | Selected database/object/queue/event versions, migrations, fault harness, duplicate/replay/fencing/race/outage cases, backup and restore receipts | VAE platform owner and Builder owner | Recovery point/time objectives, idempotency and exact state restoration pass executable scenarios |
| 9 | Rollback proof | Last-known-good runtime/evaluator/contract/capability bundle, compatibility window, migration reversal/forward-fix plan, retained artifacts and rehearsal receipt | Release authority and platform/evaluation owners | A controlled rehearsal restores the exact accepted baseline without lineage, contract or audit loss |
| 10 | Unavailable source evidence | Exact registered-path or governed replacement evidence for `SRC-001` and `SRC-009`, matching SHA-256 values, provenance and source-register/availability receipt | Source owners and release curator | Both sources are available and independently hash-verified; no historical manifest is rewritten to conceal absence |
| 11 | Formal implementation-authorization gates | Signed/versioned PRD approval, architecture validation, Builder integration evidence, real Format 02 producer/consumer/acknowledgement proof, budget/benchmark approval, production-trusted contract decision and complete Development Capsule | Product, architecture, Delegation, Builder and release authorities | GATE-IA-001 through GATE-IA-010 all report PASS in one fresh immutable readiness receipt |

## Contract and provenance conditions retained

- Keep `delegation-contracts@1.1.0-rc.4` pinned to the exact release and manifest hashes in `contracts/integration/DELEGATION_CONTRACT_PIN.yaml` for bounded local evidence.
- Keep trust status `local_unsigned_release_candidate`; a signed/published successor requires a new independent consumer validation and explicit adoption decision.
- Never fall back to rejected `1.1.0-rc.1`, parse-only compatibility, inferred source classification, invented interview provenance, weakened wrong-reading locks, or VAE mutation of Feature Contract intent.
- Preserve the historical PRD manifest. Use `validation/CONSTITUTIONAL_ALIGNMENT_MANIFEST.json` for intentionally amended alignment and integration artifacts.
- Treat the producer source-manifest hash as source-only provenance. It is not distributed or receipt-covered, and the current mutable producer checkout drift does not extend release trust.

## Status transition

Progress on one priority does not waive later priorities. Batch D remains **FAIL** while any applicable closure item or implementation-authorization gate is incomplete. Stage 5 may begin only after a new evidence-backed implementation-readiness verdict is exactly **PASS** and explicit authorization is recorded.

## Non-production evidence sandbox execution — 2026-07-14

The authorized Readiness Evidence Sandbox did not start Stage 5 or change the implementation verdict. All reusable scripts are labeled `non_production_readiness_proof`.

| Priority | Evidence produced | Current result | Remaining closure |
|---:|---|---|---|
| 1 | Annotation rubric, 12-case provisional seed and validation | `insufficient_evidence` | Select/pin evaluator; adjudicate labels; calibrate and obtain authority approval |
| 2 | Fail-closed evaluator/program pin contract | Contract PASS; candidate unbound | Immutable evaluator/program/credential pins |
| 3 | Corpus schema and required seed families | Provisional foundation PASS | Governed provenance, human adjudication, balance and approved digest |
| 4 | Protected-set schema | Unsealed design only | Independent cases, non-overlap proof, access control and seal |
| 5 | Gate, error-analysis, threshold and affinity proposals | No thresholds invented | Empirical decisions and authority approval |
| 6 | Host/Docker probe | FAIL | Runnable pinned Docker GPU/ComfyUI/model/workflow bundle |
| 7 | Cloud client/identity probe | FAIL | Authorized immutable cloud worker and full execution evidence |
| 8 | Ten-event recovery contract simulation | Simulation PASS; runtime FAIL | Real worker/queue/storage interruption and restore rehearsal |
| 9 | Rollback contract plus failed-promotion simulation | Simulation PASS; runtime FAIL | Prior runtime/evaluator bundle and real rollback rehearsal |
| 10 | Explicit availability record | FAIL | `SRC-001` and `SRC-009` governed evidence |
| 11 | Fixture-only Format 02 contract chain | Partial PASS; real path FAIL | Pinned workflow, certified evaluator, real acceptance/consumer and formal approvals |

Evidence is indexed in `docs/readiness-evidence/READINESS_EVIDENCE_INDEX.md`. The current implementation-readiness verdict remains **FAIL**.

## Readiness Evidence Closure rerun — 2026-07-15

| Area | New evidence | Verdict | Remaining closure |
|---|---|---|---|
| CRC-401 | Repository-local non-forking precedence reference validates all canonical Program Control authority hashes | Local `PASS`; Program Control reconciliation `resolved` | No further CRC-401 reconciliation action; readiness remains governed by the other open gates |
| CRC-402 | Complete 5 × 8 Feature Contract matrix plus two positive and three negative fixtures | Local `PASS`; zero production-certification claims; Program Control reconciliation `resolved` | No further CRC-402 reconciliation action; no production certification is inferred |
| Evaluator | Proof program and prompt pinned; 12-case calibration seed retained; six disjoint protected candidate slots added; explicit no-threshold and no-confusion-analysis reports | `FAIL` — `specified_not_certified` / `insufficient_evidence` | Bind evaluator identity, adjudicate corpus, seal protected set, calibrate, approve gates/affinity and rehearse rollback |
| Local GPU | Fresh GPU/Docker probe and bounded Docker Desktop retry | `FAIL` | Docker Linux GPU engine, pinned runtime, weights, workflow and execution receipt |
| Cloud GPU | Fresh AWS identity probe | `FAIL` | Authorized credentials, worker, immutable runtime, storage/queue/cancel/cost/result evidence |
| Recovery/rollback | RC4-linked ten-event invariant simulation rerun | Simulation `PASS`; executable proof `FAIL` | Real worker/queue/storage interruption, restore, fallback and rollback rehearsal |
| Format 02 | RC4 demand, boundary, derivative locks, plan, controlled portfolio, repair and result chain validate | Fixture chain `PASS`; real path `FAIL` | Pinned ComfyUI execution, certified evaluator, real acceptance and downstream consumer |

The closure plan remains active. Stage 5 is not authorized.

## External readiness inputs and proof execution package — 2026-07-15

The operator handoff package is complete under `docs/readiness-evidence/`. It translates the existing proof contracts into bounded input requirements, runbooks and acceptance procedures; it adds no broad production specification and authorizes no execution or spend.

| Package | Files | Handoff state | Operator closure needed |
|---|---:|---|---|
| Evaluator | 3 | `awaiting_operator_selection` | Select and pin an authorized independent evaluator, credential reference and deployment mode |
| Self-hosted GPU | 3 | `awaiting_operator_runtime` | Supply a proof-capable host and immutable Docker/ComfyUI/resource/workflow bindings; current GTX 960M/2 GiB is `not_proof_capable` |
| Cloud GPU | 3 | `awaiting_operator_authorization` | Supply provider/account/project/region, scoped credential reference, GPU class, hard cost ceiling, cancellation and cleanup authority |
| Storage, queue and recovery | 3 | `awaiting_operator_endpoints` | Supply versioned object storage, fenced at-least-once queue, events, checkpoints and a rollback baseline |
| Calibration corpus | 3 | `awaiting_operator_corpus` | Supply at least 30 unique governed/adjudicated cases and a custodian-sealed protected set |
| Consolidated operator checklist | 1 | `awaiting_external_inputs` | Complete every external input, run package validation, then request preflight only |

The package intentionally leaves evaluator/model, provider, credentials, runtime/resource hashes, protected-set size and final thresholds unselected. Credential values are forbidden in the repository. The 12 GiB minimum and 24 GiB preferred GPU/VRAM figures are conservative single-job proof-admission sizing, not production capacity or certification; any selected model/workflow requirement may raise the floor.

The next authorized action is operator completion of the external input records followed by the exact non-provisioning preflight command in `docs/readiness-evidence/OPERATOR_READINESS_INPUT_CHECKLIST.md`. The readiness verdict remains **FAIL** and Stage 5 remains **NOT AUTHORIZED**.
