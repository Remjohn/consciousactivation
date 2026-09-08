# CAE Multi-Epoch Execution Plan: Remaining Epochs (Epoch 3 to Epoch 9)

This document details the schedule, functional requirements, invariant constraints, target subsystems, and core objectives for all remaining execution epochs (**Epoch 3 through Epoch 9**).

---

## Epoch Overview Matrix

| Epoch | Theme / Subsystem Focus | Mandates Count | Target Functional Requirements & Invariants | Primary Codebases Affected |
| :--- | :--- | :---: | :--- | :--- |
| **Epoch 3** | **Anchoring, Workflows & Pre-Production Sealing** | 7 | `FR-006`, `FR-PREP-001`, `FR-014`, `FR-016`, `FR-ANCH-001`, `INV-DISP-002`, `INV-HOST-001` | `packages/ca_runtime`, `services/pipeline`, `services/interview` |
| **Epoch 4** | **Evidence Admission, Lineage & Gate Halting** | 6 | `FR-007`, `FR-EV-001`, `FR-CTX-001`, `FR-SEM-001`, `INV-OUT-001`, `INV-GATE-001` | `packages/ca_runtime`, `services/pipeline`, `services/interview` |
| **Epoch 5** | **Gate Resumption, Receipts & Policy Binding** | 7 | `FR-003`, `FR-020`, `FR-022`, `FR-POL-001`, `FR-POL-002`, `INV-GATE-002`, `INV-SEC-001` | `packages/ca_runtime`, `services/pipeline`, `services/interview` |
| **Epoch 6** | **Memory Write-Back, CAS Concurrency & Registry** | 7 | `FR-008`, `FR-023`, `FR-024`, `FR-AUTH-001`, `INV-MEM-001`, `INV-CAS-001`, `INV-REG-001` | `packages/ca_runtime`, `services/interview-intelligence`, `services/pipeline` |
| **Epoch 7** | **Merkle Receipts, Composition & Isolation** | 6 | `FR-029`, `FR-REL-001`, `INV-MRK-001`, `INV-ISO-001`, `INV-ECON-001`, `INV-VOICE-001` | `packages/ca_runtime`, `services/pipeline`, `services/interview` |
| **Epoch 8** | **Distribution, Replay, Preemption & Evidence DAG** | 7 | `FR-DIST-001`, `FR-OUT-001`, `INV-RPL-001`, `INV-REC-001`, `INV-CTRL-001`, `INV-DAG-001`, `INV-TEL-001` | `packages/ca_runtime`, `services/pipeline` |
| **Epoch 9** | **Autonomous Collisions, Benchmarking & Live Proof** | 4 | `INV-BENCH-001`, `INV-AUTO-001`, `INV-WAL-001`, `INV-PROOF-001` | `packages/ca_runtime`, `tests/e2e`, `services/pipeline` |

---

## Detailed Epoch Schedules

### Epoch 3: Anchoring, Workflows & Pre-Production Sealing
**Goal:** Establish immutable pre-production packaging, exact coordinate audio/video anchor hits, collision tension matrices, and distributed host runner dispatching.

| Mandate ID | Mandate Title | Requirement / Invariant | Target Subsystem / Files | Core Acceptance Criteria & Invariant Rule |
| :--- | :--- | :--- | :--- | :--- |
| **`CA-M006`** | Activative to Elicitation Linking | `FR-006` | `packages/ca_runtime/src/ca_runtime/activative_elicitation_link.py` | Guarantees deterministic linking between activative triggers and interview elicitation steps with bi-directional trace hashing. |
| **`CA-M011`** | Sealed Pre-Production Pack | `FR-PREP-001` | `services/pipeline/src/cmf_pipeline/preproduction/sealer.py` | Enforces cryptographic sealing of pre-production assets before downstream rendering; fails closed on missing assets. |
| **`CA-M014`** | Cross-Window Chunking Protection | `FR-014` | `services/pipeline/src/cmf_pipeline/media/chunking.py` | Prevents semantic clipping and lost boundary frames across media sliding windows with deterministic overlap stitching. |
| **`CA-M016`** | Grounded Collision Tension Matrix | `FR-016` | `services/interview/src/conscious_activations_interview_expression/collision_matrix.py` | Computes collision tension scores across audience-subject divergence axes; enforces strict mathematical normalization. |
| **`CA-M021`** | Anchor Hits Exact Coordinates | `FR-ANCH-001` | `services/interview/src/conscious_activations_interview_expression/anchor_coordinates.py` | Maps verbatim quotes and reaction cues to exact microsecond/sample-accurate coordinates in the master media stream. |
| **`CA-M035`** | Workflow Dispatcher Runtime | `INV-DISP-002` | `packages/ca_runtime/src/ca_runtime/workflow_dispatch.py` | Orchestrates multi-stage program pipelines with idempotency keys, state rollback, and distributed lease lifecycle tracking. |
| **`CA-M037`** | Agent Invocation Host Runner | `INV-HOST-001` | `packages/ca_runtime/src/ca_runtime/agent_host_runner.py` | Executes external LLM / tool invocations inside an isolated runtime container with strict wall-clock timeout and byte quota limits. |

---

### Epoch 4: Evidence Admission, Lineage & Gate Halting
**Goal:** Implement multi-dimensional evidence admission, contextual hierarchy lineage, semantic bridge moments, and gate suspension mechanisms.

| Mandate ID | Mandate Title | Requirement / Invariant | Target Subsystem / Files | Core Acceptance Criteria & Invariant Rule |
| :--- | :--- | :--- | :--- | :--- |
| **`CA-M007`** | Activative Strategic Execution Object | `FR-007` | `packages/ca_runtime/src/ca_runtime/strategic_execution.py` | Validates that strategic execution payloads contain complete lineage ancestry and cannot be instantiated without signed intent. |
| **`CA-M017`** | Multi-Dimensional Evidence Admission | `FR-EV-001` | `services/interview/src/conscious_activations_interview_expression/evidence_admission.py` | Gates media and claim admission across confidence, corroboration, and verbatim fidelity thresholds. |
| **`CA-M018`** | Hierarchical Context Lineage | `FR-CTX-001` | `services/interview/src/conscious_activations_interview_expression/context_lineage.py` | Implements hierarchical parent-child context trees with immutable revision hashing and cycle detection. |
| **`CA-M019`** | Expression Moments Semantic Bridge | `FR-SEM-001` | `services/interview/src/conscious_activations_interview_expression/semantic_bridge.py` | Bridges raw spoken utterances with high-level conceptual activation vectors without hallucinated intermediary frames. |
| **`CA-M039`** | Deterministic Output Contract & Self-Repair | `INV-OUT-001` | `packages/ca_runtime/src/ca_runtime/output_contract_repair.py` | Enforces strict JSON/Pydantic schema validation on program outputs with deterministic AST repair on malformed model payloads. |
| **`CA-M040`** | Gate Milestone Suspension Contract | `INV-GATE-001` | `packages/ca_runtime/src/ca_runtime/gate_suspension.py` | Safely pauses pipeline execution when gate invariant thresholds are violated, storing durable suspension receipts. |

---

### Epoch 5: Gate Resumption, Receipts & Policy Binding
**Goal:** Deploy reactive gate resumption, audit receipts, subject constitution exception lifecycles, and security sandboxing.

| Mandate ID | Mandate Title | Requirement / Invariant | Target Subsystem / Files | Core Acceptance Criteria & Invariant Rule |
| :--- | :--- | :--- | :--- | :--- |
| **`CA-M003`** | Subject Constitution Lifecycle | `FR-003` | `packages/ca_runtime/src/ca_runtime/subject_constitution.py` | Implements immutable subject constitution versioning, amendment workflows, and exception handling protocols. |
| **`CA-M020`** | Reaction Receipts First-Class Evidence | `FR-020` | `services/interview/src/conscious_activations_interview_expression/reaction_receipts.py` | Upgrades interactive reaction events into cryptographically verifiable evidence tokens with actor timestamps. |
| **`CA-M022`** | Adaptive Elicitation Remediation | `FR-022` | `services/interview/src/conscious_activations_interview_expression/adaptive_remediation.py` | Triggers dynamic interview branch remediation when tension or evidence yields drop below statistical significance. |
| **`CA-M025`** | Campaign Auth Policy (Production) | `FR-POL-001` | `packages/ca_runtime/src/ca_runtime/campaign_auth_policy.py` | Validates role-based authorization and budget thresholds for production-tier campaign execution runs. |
| **`CA-M028`** | Policy Revisions Execution Binding | `FR-POL-002` | `packages/ca_runtime/src/ca_runtime/policy_revision_binding.py` | Binds active policy revision hashes directly to program execution leases, rejecting stale policy contexts. |
| **`CA-M041`** | Reactive Gate Resumption & Receipts | `INV-GATE-002` | `packages/ca_runtime/src/ca_runtime/gate_resumption.py` | Handles asynchronous operator approvals to resume suspended pipeline gates with non-repudiable approval receipts. |
| **`CA-M048`** | Path Traversal & Tool Sandbox | `INV-SEC-001` | `packages/ca_runtime/src/ca_runtime/sandbox.py` | Enforces strict path canonicalization and syscall restrictions to prevent container escapes and directory traversal. |

---

### Epoch 6: Memory Write-Back, CAS Concurrency & Registry
**Goal:** Implement frozen content portfolio yield gates, governed memory persistence, atomic SQLite compare-and-swap transitions, and immutable registry.

| Mandate ID | Mandate Title | Requirement / Invariant | Target Subsystem / Files | Core Acceptance Criteria & Invariant Rule |
| :--- | :--- | :--- | :--- | :--- |
| **`CA-M008`** | Frozen Content Portfolio | `FR-008` | `packages/ca_runtime/src/ca_runtime/frozen_portfolio.py` | Freezes portfolio content manifests preventing downstream mutations once validation milestones pass. |
| **`CA-M023`** | Deterministic Portfolio Yield Gating | `FR-023` | `services/interview-intelligence/src/cae_interview_intelligence/yield_gating.py` | Enforces minimum viable narrative yield metrics before unlocking downstream media assembly programs. |
| **`CA-M024`** | Preliminary Auth Policy | `FR-024` | `services/interview-intelligence/src/cae_interview_intelligence/preliminary_auth.py` | Implements pre-flight authorization checks for exploratory and non-production pipeline executions. |
| **`CA-M026`** | Durable Auth Decision Receipts | `FR-AUTH-001` | `packages/ca_runtime/src/ca_runtime/auth_decision_receipts.py` | Stores tamper-evident cryptographic receipts for all authorization grants, denials, and overrides. |
| **`CA-M032`** | Governed Memory Write-Back | `INV-MEM-001` | `packages/ca_runtime/src/ca_runtime/memory_writeback.py` | Governs automated agent write-back into shared workspace memory with schema validation and merge consensus. |
| **`CA-M042`** | Atomic CAS SQLite Transitions | `INV-CAS-001` | `packages/ca_runtime/src/ca_runtime/sqlite_cas_transitions.py` | Implements optimistic concurrency control with SQLite compare-and-swap transactions for program states. |
| **`CA-M049`** | Program Registry Immutability | `INV-REG-001` | `packages/ca_runtime/src/ca_runtime/program_registry.py` | Enforces read-only immutable registration for compiled program manifests and execution graphs. |

---

### Epoch 7: Merkle Receipts, Composition & Isolation
**Goal:** Deliver the No-Unanchored-Invention invariant, immutable release manifests, Merkle receipt verification trees, multi-tenant isolation, and voice DNA.

| Mandate ID | Mandate Title | Requirement / Invariant | Target Subsystem / Files | Core Acceptance Criteria & Invariant Rule |
| :--- | :--- | :--- | :--- | :--- |
| **`CA-M029`** | No-Unanchored-Invention Invariant | `FR-029` | `packages/ca_runtime/src/ca_runtime/no_unanchored_invention.py` | Audits every generated content sentence against verified verbatim and evidence sources, purging unanchored claims. |
| **`CA-M030`** | Immutable Release Manifest | `FR-REL-001` | `packages/ca_runtime/src/ca_runtime/release_manifest.py` | Packages final campaign outputs into an immutable, signed manifest with complete Merkle proof trees. |
| **`CA-M043`** | Merkle Receipt Chaining | `INV-MRK-001` | `packages/ca_runtime/src/ca_runtime/merkle_receipt_chain.py` | Constructs cryptographic Merkle DAGs connecting upstream raw evidence to final distribution deliverables. |
| **`CA-M047`** | Multi-Tenant Workspace Isolation | `INV-ISO-001` | `packages/ca_runtime/src/ca_runtime/workspace_isolation.py` | Guarantees strict cryptographic and database isolation between distinct workspace tenants and campaigns. |
| **`CA-M051`** | Model Economics & Quotas | `INV-ECON-001` | `services/pipeline/src/cmf_pipeline/economics/quota_engine.py` | Tracks real-time token spend, rate limits, and provider quotas with fail-safe budget enforcement. |
| **`CA-M052`** | Subject Constitution Voice DNA | `INV-VOICE-001` | `services/interview/src/conscious_activations_interview_expression/voice_dna.py` | Extracts acoustic and linguistic DNA features to ensure synthetic speech synthesis conforms strictly to the Subject Constitution. |

---

### Epoch 8: Distribution, Replay, Preemption & Evidence DAG
**Goal:** Build external distribution adapters, outcome attribution, deterministic replay engines, zombie lease recovery, operator preemption, and unified telemetry.

| Mandate ID | Mandate Title | Requirement / Invariant | Target Subsystem / Files | Core Acceptance Criteria & Invariant Rule |
| :--- | :--- | :--- | :--- | :--- |
| **`CA-M031`** | External Distribution Delivery | `FR-DIST-001` | `packages/ca_runtime/src/ca_runtime/distribution_delivery.py` | Handles idempotent delivery to third-party endpoints with automated exponential backoff and delivery receipts. |
| **`CA-M032b`** | Outcome Measurement Attribution | `FR-OUT-001` | `packages/ca_runtime/src/ca_runtime/outcome_attribution.py` | Ingests post-distribution conversion metrics and correlates outcome yield with specific creative tension moments. |
| **`CA-M044`** | Persisted Replay Verification Engine | `INV-RPL-001` | `packages/ca_runtime/src/ca_runtime/replay_engine.py` | Allows full bit-for-bit pipeline replay from stored event logs and cached model completions to verify determinism. |
| **`CA-M045`** | Worker Restart & Zombie Lease Reconcile | `INV-REC-001` | `packages/ca_runtime/src/ca_runtime/zombie_reconciler.py` | Detects orphaned worker processes and expired leases, reclaiming program execution locks safely. |
| **`CA-M046`** | Real Operator Control & Preemption | `INV-CTRL-001` | `packages/ca_runtime/src/ca_runtime/operator_preemption.py` | Provides real-time operator control commands (pause, drain, cancel, resume) with instantaneous lock preemption. |
| **`CA-M050`** | Cryptographic Evidence DAG | `INV-DAG-001` | `services/pipeline/src/cmf_pipeline/evidence/dag.py` | Builds a directed acyclic graph linking all temporal evidence moments, interview transcripts, and synthesized media blocks. |
| **`CA-M054`** | Unified Telemetry Flywheel | `INV-TEL-001` | `services/pipeline/src/cmf_pipeline/telemetry/flywheel.py` | Aggregates structured trace telemetry, latency metrics, and failure diagnostics across all pipeline services. |

---

### Epoch 9: Autonomous Collisions, Benchmarking & Live Proof
**Goal:** Finalize golden benchmark certification (CSEB), autonomous collision approval gates, SQLite WAL concurrency optimizations, and live end-to-end integration tests.

| Mandate ID | Mandate Title | Requirement / Invariant | Target Subsystem / Files | Core Acceptance Criteria & Invariant Rule |
| :--- | :--- | :--- | :--- | :--- |
| **`CA-M053`** | CSEB Golden Benchmark Certification | `INV-BENCH-001` | `services/pipeline/src/cmf_pipeline/benchmarks/cseb_suite.py` | Runs the standardized Conscious Activation Evaluation Benchmark against golden ground-truth test sets. |
| **`CA-M055`** | Autonomous Collision Approval Gate | `INV-AUTO-001` | `services/pipeline/src/cmf_pipeline/collision/autonomous_gate.py` | Enables autonomous high-confidence collision approvals under strict policy scoring without manual human intervention. |
| **`CA-M056`** | SQLite WAL Concurrency & Tuning | `INV-WAL-001` | `packages/ca_runtime/src/ca_runtime/sqlite_tuning.py` | Configures WAL mode, busy timeouts, mmap sizing, and checkpointing for high-throughput multi-worker concurrency. |
| **`CA-M057`** | Live End-to-End Proof Harness | `INV-PROOF-001` | `tests/e2e/test_live_e2e_proof_harness.py` | Executes the complete 17-stage pipeline from raw audience/subject inputs to verified distribution delivery in a live integration run. |
