# CAE Multi-Epoch Execution Plan: Remaining Epochs (Epoch 5 to Epoch 9)

> **Status Update**: 
> - ✅ **Epoch 1**: Ingested & Verified (`9985a6af`) — 121/121 tests passed.
> - ✅ **Epoch 2**: Ingested & Verified (`515bdf3f`) — 139/139 tests passed.
> - ✅ **Epoch 3**: Ingested & Verified (`ff98713f`) — 7 mandates verified.
> - ✅ **Epoch 4**: Ingested & Verified (`c7fc9036`) — 6 mandates verified.
> - ✅ **Epoch 5**: Ingested & Verified — 7 mandates, 173 passed / 2 skipped.
> - 🎯 **Current Active Target**: **Epoch 6** (7 Mandates).

---

## Epoch Overview Matrix (Remaining Pipeline)

| Epoch | Theme / Subsystem Focus | Mandates Count | Target Functional Requirements & Invariants | Primary Codebases Affected |
| :--- | :--- | :---: | :--- | :--- |
| **Epoch 5** (Complete) | **Gate Resumption, Receipts & Policy Binding** | 7 | `FR-003`, `FR-020`, `FR-022`, `FR-POL-001`, `FR-POL-002`, `INV-GATE-002`, `INV-SEC-001` | `packages/ca_runtime`, `services/pipeline`, `services/interview` |
| **Epoch 6** (Active) | **Memory Write-Back, CAS Concurrency & Registry** | 7 | `FR-008`, `FR-023`, `FR-024`, `FR-AUTH-001`, `INV-MEM-001`, `INV-CAS-001`, `INV-REG-001` | `packages/ca_runtime`, `services/interview-intelligence`, `services/pipeline` |
| **Epoch 7** | **Merkle Receipts, Composition & Isolation** | 6 | `FR-029`, `FR-REL-001`, `INV-MRK-001`, `INV-ISO-001`, `INV-ECON-001`, `INV-VOICE-001` | `packages/ca_runtime`, `services/pipeline`, `services/interview` |
| **Epoch 8** | **Distribution, Replay, Preemption & Evidence DAG** | 7 | `FR-DIST-001`, `FR-OUT-001`, `INV-RPL-001`, `INV-REC-001`, `INV-CTRL-001`, `INV-DAG-001`, `INV-TEL-001` | `packages/ca_runtime`, `services/pipeline` |
| **Epoch 9** | **Autonomous Collisions, Benchmarking & Live Proof** | 4 | `INV-BENCH-001`, `INV-AUTO-001`, `INV-WAL-001`, `INV-PROOF-001` | `packages/ca_runtime`, `tests/e2e`, `services/pipeline` |

---

## Detailed Epoch Schedules

### Epoch 5: Gate Resumption, Receipts & Policy Binding (COMPLETE)
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
