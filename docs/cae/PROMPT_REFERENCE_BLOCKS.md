# Remaining Epochs (5 to 9) — Copy-Paste Prompt Blocks & Model Allocation Guide

> **Integration Status:**
> - ✅ **Epoch 1**: Verified & Committed (`9985a6af`)
> - ✅ **Epoch 2**: Verified & Committed (`515bdf3f`)
> - ✅ **Epoch 3**: Verified & Committed (`ff98713f`)
> - ✅ **Epoch 4**: Verified & Committed (`c7fc9036`)
> - 🎯 **Current Active Target**: **Epoch 5** (7 Mandates)

---

## Model Allocation Strategy (To Save Tokens on Claude)
Claude typically has tighter rate/token limits than ChatGPT or Grok. To optimize throughput and avoid token starvation:
- **Assign to Claude (Top 3 per Epoch):** Mandates that are self-contained, contract-focused, schema/receipt oriented, or mathematical logic with minimal sprawling codebase dependencies.
- **Assign to ChatGPT / Grok (Remaining Mandates):** Mandates requiring broader multi-file edits, complex state-machine runtime wiring, or heavy testing fixtures.

---

## Epoch 5: Gate Resumption, Receipts & Policy Binding (ACTIVE)

### 🎯 Top 3 Mandates Recommended for Claude (Lowest Token Demand):
1. **`CA-M020` (Reaction Receipts First-Class Evidence)**: Highly self-contained cryptographic receipt dataclass, SHA-256 hashing, and tamper-evident proof methods. Very low token footprint.
2. **`CA-M028` (Policy Revisions Execution Binding)**: Concise lease-to-hash verification binding; validates policy snapshot alignment on dispatch with minimal lines of code.
3. **`CA-M025` (Campaign Auth Policy Production)**: Clean, bounded rule evaluation checking caller roles and spend thresholds against structured models.

---

### Mandate 1/7: CA-M003
Mandate ID: CA-M003  
Mandate Title: Subject Constitution Lifecycle & Exception Handling  
Requirement / Invariant: FR-003  
Model Recommendation: ChatGPT / Grok (Medium token demand; requires full lifecycle state transitions)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/subject_constitution.py, tests/cae/test_ca_m003_subject_constitution.py  
Core Acceptance Criteria & Invariant Rule: Implement immutable Subject Constitution versioning, amendment workflows, and exception handling protocols. Prohibit direct field mutations on signed constitutions and record all amendment receipts.

---

### Mandate 2/7: CA-M020
Mandate ID: CA-M020  
Mandate Title: Reaction Receipts First-Class Evidence  
Requirement / Invariant: FR-020  
Model Recommendation: 🌟 Claude (Top 1 Lowest Token Demand — pure cryptographic receipt dataclass and hashing)  
Target Subsystem / Files: services/interview/src/conscious_activations_interview_expression/reaction_receipts.py, tests/phase4/test_ca_m020_reaction_receipts.py  
Core Acceptance Criteria & Invariant Rule: Upgrade interactive reaction events into cryptographically verifiable evidence tokens with actor timestamps and hash proofs. Ensure receipts cannot be forged, retroactively altered, or dissociated from source media.

---

### Mandate 3/7: CA-M022
Mandate ID: CA-M022  
Mandate Title: Adaptive Elicitation Remediation  
Requirement / Invariant: FR-022  
Model Recommendation: ChatGPT / Grok (Higher token demand; dynamic prompt branch remediation logic)  
Target Subsystem / Files: services/interview/src/conscious_activations_interview_expression/adaptive_remediation.py, tests/phase4/test_ca_m022_adaptive_remediation.py  
Core Acceptance Criteria & Invariant Rule: Trigger dynamic interview branch remediation when tension or evidence yields drop below statistical significance. Inject targeted follow-up prompts without breaking conversational coherence or constitution boundaries.

---

### Mandate 4/7: CA-M025
Mandate ID: CA-M025  
Mandate Title: Campaign Auth Policy (Production)  
Requirement / Invariant: FR-POL-001  
Model Recommendation: 🌟 Claude (Top 3 Lowest Token Demand — self-contained role & spend validation rules)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/campaign_auth_policy.py, tests/wave04/test_ca_m025_campaign_auth_policy.py  
Core Acceptance Criteria & Invariant Rule: Enforce role-based authorization, tier constraints, and spend budget thresholds for production-tier campaign execution runs. Reject unauthenticated or over-budget execution requests with descriptive denial receipts.

---

### Mandate 5/7: CA-M028
Mandate ID: CA-M028  
Mandate Title: Policy Revisions Execution Binding  
Requirement / Invariant: FR-POL-002  
Model Recommendation: 🌟 Claude (Top 2 Lowest Token Demand — lightweight hash binding check on dispatch payloads)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/policy_revision_binding.py, tests/wave04/test_ca_m028_policy_revision_binding.py  
Core Acceptance Criteria & Invariant Rule: Bind active policy revision hashes directly to program execution leases and dispatch payloads. Invalidate and abort in-flight executions if the binding detects policy drift or stale policy snapshots.

---

### Mandate 6/7: CA-M041
Mandate ID: CA-M041  
Mandate Title: Reactive Gate Resumption & Receipts  
Requirement / Invariant: INV-GATE-002  
Model Recommendation: ChatGPT / Grok (Medium token demand; gate suspension unlock and approval routing)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/gate_resumption.py, tests/cae/test_ca_m041_gate_resumption.py  
Core Acceptance Criteria & Invariant Rule: Handle asynchronous operator approvals and policy overrides to resume suspended pipeline gates. Generate immutable, non-repudiable approval receipts before releasing pipeline suspension locks.

---

### Mandate 7/7: CA-M048
Mandate ID: CA-M048  
Mandate Title: Path Traversal & Tool Sandbox  
Requirement / Invariant: INV-SEC-001  
Model Recommendation: ChatGPT / Grok (Medium token demand; path security checks and extensive jail-escape tests)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/sandbox.py, tests/cae/test_ca_m048_sandbox.py  
Core Acceptance Criteria & Invariant Rule: Enforce strict path canonicalization, workspace root containment, and tool execution sandboxing. Block directory traversal attacks (`../`), symlink escapes, and unauthorized filesystem/network operations.

---
---

## Epoch 6: Memory Write-Back, CAS Concurrency & Registry

### 🎯 Top 3 Mandates Recommended for Claude (Lowest Token Demand):
1. **`CA-M008` (Frozen Content Portfolio)**: Focused snapshot serialization and freeze lock validation. Pure state freezing with no external networking.
2. **`CA-M026` (Durable Auth Decision Receipts)**: Standardized cryptographic receipt model with actor identity, hash chaining, and append-only store.
3. **`CA-M024` (Preliminary Auth Policy)**: Clean pre-flight quota and permission verification gate with minimal lines of code.

---

### Mandate 1/7: CA-M008
Mandate ID: CA-M008  
Mandate Title: Frozen Content Portfolio  
Requirement / Invariant: FR-008  
Model Recommendation: 🌟 Claude (Top 1 Lowest Token Demand — clean snapshot serialization and freeze locking)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/frozen_portfolio.py, tests/cae/test_ca_m008_frozen_portfolio.py  
Core Acceptance Criteria & Invariant Rule: Freeze validated portfolio content manifests into immutable snapshots. Disallow any downstream mutation or format reallocation once portfolio milestone validation passes.

---

### Mandate 2/7: CA-M023
Mandate ID: CA-M023  
Mandate Title: Deterministic Portfolio Yield Gating  
Requirement / Invariant: FR-023  
Model Recommendation: ChatGPT / Grok (Medium token demand; multi-metric narrative yield math)  
Target Subsystem / Files: services/interview-intelligence/src/cae_interview_intelligence/yield_gating.py, tests/interview_intelligence/test_ca_m023_yield_gating.py  
Core Acceptance Criteria & Invariant Rule: Enforce minimum viable narrative yield metrics and diversity thresholds before unlocking downstream media assembly programs. Fail closed with structured gap reports if yield is insufficient.

---

### Mandate 3/7: CA-M024
Mandate ID: CA-M024  
Mandate Title: Preliminary Auth Policy  
Requirement / Invariant: FR-024  
Model Recommendation: 🌟 Claude (Top 3 Lowest Token Demand — straightforward pre-flight permission/quota gate)  
Target Subsystem / Files: services/interview-intelligence/src/cae_interview_intelligence/preliminary_auth.py, tests/interview_intelligence/test_ca_m024_preliminary_auth.py  
Core Acceptance Criteria & Invariant Rule: Enforce pre-flight permission checks and resource quota validation for exploratory, drafting, and non-production pipeline executions.

---

### Mandate 4/7: CA-M026
Mandate ID: CA-M026  
Mandate Title: Durable Auth Decision Receipts  
Requirement / Invariant: FR-AUTH-001  
Model Recommendation: 🌟 Claude (Top 2 Lowest Token Demand — self-contained cryptographic decision receipt schema)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/auth_decision_receipts.py, tests/wave04/test_ca_m026_auth_receipts.py  
Core Acceptance Criteria & Invariant Rule: Record tamper-evident cryptographic receipts for all authorization grants, denials, and operator overrides. Receipts must contain actor identity, decision reason, policy hash, and timestamp.

---

### Mandate 5/7: CA-M032
Mandate ID: CA-M032  
Mandate Title: Governed Memory Write-Back  
Requirement / Invariant: INV-MEM-001  
Model Recommendation: ChatGPT / Grok (High token demand; consensus merge logic and workspace memory conflict handling)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/memory_writeback.py, tests/wave05/test_ca_m032_memory_writeback.py  
Core Acceptance Criteria & Invariant Rule: Govern automated agent write-back into shared workspace memory. Enforce schema conformance, merge consensus, conflict rejection, and provenance tracking for all persisted memory items.

---

### Mandate 6/7: CA-M042
Mandate ID: CA-M042  
Mandate Title: Atomic CAS SQLite Transitions  
Requirement / Invariant: INV-CAS-001  
Model Recommendation: ChatGPT / Grok (Medium token demand; SQLite compare-and-swap concurrency loops)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/sqlite_cas_transitions.py, tests/cae/test_ca_m042_sqlite_cas.py  
Core Acceptance Criteria & Invariant Rule: Implement optimistic concurrency control with SQLite compare-and-swap (CAS) transactions for program state transitions. Reject concurrent writes with version mismatch exceptions and guarantee zero lost updates.

---

### Mandate 7/7: CA-M049
Mandate ID: CA-M049  
Mandate Title: Program Registry Immutability  
Requirement / Invariant: INV-REG-001  
Model Recommendation: ChatGPT / Grok (Medium token demand; manifest registry registration and locking)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/program_registry.py, tests/cae/test_ca_m049_program_registry.py  
Core Acceptance Criteria & Invariant Rule: Enforce read-only immutable registration for compiled program manifests and execution graphs. Prevent runtime tampering, unauthorized program patching, or manifest overwrites.

---
---

## Epoch 7: Merkle Receipts, Composition & Isolation

### 🎯 Top 3 Mandates Recommended for Claude (Lowest Token Demand):
1. **`CA-M030` (Immutable Release Manifest)**: Clean Pydantic packaging schema, SHA-256 digest computation, and signature formatting. Very low token demand.
2. **`CA-M043` (Merkle Receipt Chaining)**: Standard, self-contained binary Merkle tree algorithm (leaf hashing, node pairing, inclusion proof generation). Pure computer science logic.
3. **`CA-M051` (Model Economics & Quotas)**: Direct token counting, arithmetic rate limits, and budget ceiling enforcement.

---

### Mandate 1/6: CA-M029
Mandate ID: CA-M029  
Mandate Title: No-Unanchored-Invention Invariant  
Requirement / Invariant: FR-029  
Model Recommendation: ChatGPT / Grok (High token demand; sentence-level claim extraction and verbatim verification)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/no_unanchored_invention.py, tests/wave04/test_ca_m029_no_unanchored_invention.py  
Core Acceptance Criteria & Invariant Rule: Audit every generated creative claim and narrative sentence against verified verbatim and evidence sources. Automatically purge or flag any sentence that introduces unanchored facts or hallucinations.

---

### Mandate 2/6: CA-M030
Mandate ID: CA-M030  
Mandate Title: Immutable Release Manifest  
Requirement / Invariant: FR-REL-001  
Model Recommendation: 🌟 Claude (Top 1 Lowest Token Demand — release package manifest schema and digest calculation)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/release_manifest.py, tests/wave04/test_ca_m030_release_manifest.py  
Core Acceptance Criteria & Invariant Rule: Bundle final campaign outputs into an immutable, cryptographically signed release manifest containing SHA-256 digests, license metadata, and full provenance trees.

---

### Mandate 3/6: CA-M043
Mandate ID: CA-M043  
Mandate Title: Merkle Receipt Chaining  
Requirement / Invariant: INV-MRK-001  
Model Recommendation: 🌟 Claude (Top 2 Lowest Token Demand — self-contained algorithmic Merkle tree and audit proofs)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/merkle_receipt_chain.py, tests/cae/test_ca_m043_merkle_receipts.py  
Core Acceptance Criteria & Invariant Rule: Construct cryptographic Merkle trees connecting upstream raw evidence, intermediate gate decisions, and final distribution deliverables into a single verifiable root hash.

---

### Mandate 4/6: CA-M047
Mandate ID: CA-M047  
Mandate Title: Multi-Tenant Workspace Isolation  
Requirement / Invariant: INV-ISO-001  
Model Recommendation: ChatGPT / Grok (Medium token demand; cross-tenant boundary and directory isolation checks)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/workspace_isolation.py, tests/cae/test_ca_m047_workspace_isolation.py  
Core Acceptance Criteria & Invariant Rule: Guarantee strict cryptographic, database, and filesystem isolation between distinct workspace tenants and campaigns. Prevent cross-tenant data leaks and state leakage.

---

### Mandate 5/6: CA-M051
Mandate ID: CA-M051  
Mandate Title: Model Economics & Quotas  
Requirement / Invariant: INV-ECON-001  
Model Recommendation: 🌟 Claude (Top 3 Lowest Token Demand — straightforward token spend tracking and budget caps)  
Target Subsystem / Files: services/pipeline/src/cmf_pipeline/economics/quota_engine.py, tests/pipeline/test_ca_m051_quota_engine.py  
Core Acceptance Criteria & Invariant Rule: Track real-time token spend, provider rate limits, and workspace cost quotas with hard budget caps. Halt program dispatch when quotas are exhausted and emit budget overrun receipts.

---

### Mandate 6/6: CA-M052
Mandate ID: CA-M052  
Mandate Title: Subject Constitution Voice DNA  
Requirement / Invariant: INV-VOICE-001  
Model Recommendation: ChatGPT / Grok (High token demand; acoustic and linguistic DNA feature scoring algorithms)  
Target Subsystem / Files: services/interview/src/conscious_activations_interview_expression/voice_dna.py, tests/phase4/test_ca_m052_voice_dna.py  
Core Acceptance Criteria & Invariant Rule: Extract acoustic and linguistic DNA features to ensure synthetic speech and tone strictly conform to the Subject Constitution. Reject synthesized outputs with unacceptable voice drift scores.

---
---

## Epoch 8: Distribution, Replay, Preemption & Evidence DAG

### 🎯 Top 3 Mandates Recommended for Claude (Lowest Token Demand):
1. **`CA-M045` (Worker Restart & Zombie Lease Reconcile)**: Concise scanner detecting expired timestamps and resetting leases. Minimal logic footprint.
2. **`CA-M046` (Real Operator Control & Preemption)**: Direct command dispatching for execution state flags (pause, drain, cancel, resume).
3. **`CA-M050` (Cryptographic Evidence DAG)**: Standard directed acyclic graph data structure with parent hash pointers and cycle checks.

---

### Mandate 1/7: CA-M031
Mandate ID: CA-M031  
Mandate Title: External Distribution Delivery  
Requirement / Invariant: FR-DIST-001  
Model Recommendation: ChatGPT / Grok (Medium token demand; external publishing client with exponential backoff)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/distribution_delivery.py, tests/wave04/test_ca_m031_distribution_delivery.py  
Core Acceptance Criteria & Invariant Rule: Handle idempotent delivery to external publishing platforms and CDNs with exponential backoff, retry tracking, and signed delivery receipts.

---

### Mandate 2/7: CA-M032b
Mandate ID: CA-M032b  
Mandate Title: Outcome Measurement Attribution  
Requirement / Invariant: FR-OUT-001  
Model Recommendation: ChatGPT / Grok (Medium token demand; post-distribution telemetry correlation math)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/outcome_attribution.py, tests/wave04/test_ca_m032b_outcome_attribution.py  
Core Acceptance Criteria & Invariant Rule: Ingest post-distribution performance and audience conversion metrics, linking outcome yield directly back to specific tension collision anchors and creative components.

---

### Mandate 3/7: CA-M044
Mandate ID: CA-M044  
Mandate Title: Persisted Replay Verification Engine  
Requirement / Invariant: INV-RPL-001  
Model Recommendation: ChatGPT / Grok (High token demand; bit-for-bit execution replayer with completion mocking)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/replay_engine.py, tests/cae/test_ca_m044_replay_engine.py  
Core Acceptance Criteria & Invariant Rule: Provide full deterministic pipeline replay from persisted event logs and cached model responses, verifying bit-for-bit output reproducibility.

---

### Mandate 4/7: CA-M045
Mandate ID: CA-M045  
Mandate Title: Worker Restart & Zombie Lease Reconcile  
Requirement / Invariant: INV-REC-001  
Model Recommendation: 🌟 Claude (Top 1 Lowest Token Demand — compact expired lease scanner and cleanup)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/zombie_reconciler.py, tests/cae/test_ca_m045_zombie_reconciler.py  
Core Acceptance Criteria & Invariant Rule: Detect crashed or orphaned worker processes and expired program leases, safely reclaiming locks and resuming execution without state corruption or duplicate runs.

---

### Mandate 5/7: CA-M046
Mandate ID: CA-M046  
Mandate Title: Real Operator Control & Preemption  
Requirement / Invariant: INV-CTRL-001  
Model Recommendation: 🌟 Claude (Top 2 Lowest Token Demand — concise operator signal handler and lock preemption)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/operator_preemption.py, tests/cae/test_ca_m046_operator_preemption.py  
Core Acceptance Criteria & Invariant Rule: Provide real-time operator control commands (pause, drain, cancel, resume, force-kill) with instantaneous lock preemption and execution state preservation.

---

### Mandate 6/7: CA-M050
Mandate ID: CA-M050  
Mandate Title: Cryptographic Evidence DAG  
Requirement / Invariant: INV-DAG-001  
Model Recommendation: 🌟 Claude (Top 3 Lowest Token Demand — clean DAG data structure with hash pointers)  
Target Subsystem / Files: services/pipeline/src/cmf_pipeline/evidence/dag.py, tests/pipeline/test_ca_m050_evidence_dag.py  
Core Acceptance Criteria & Invariant Rule: Build a directed acyclic graph linking all temporal evidence moments, transcripts, tension matrices, and synthesized media blocks with cryptographic parent-hash verification.

---

### Mandate 7/7: CA-M054
Mandate ID: CA-M054  
Mandate Title: Unified Telemetry Flywheel  
Requirement / Invariant: INV-TEL-001  
Model Recommendation: ChatGPT / Grok (Medium/high token demand; multi-service telemetry aggregation)  
Target Subsystem / Files: services/pipeline/src/cmf_pipeline/telemetry/flywheel.py, tests/pipeline/test_ca_m054_telemetry_flywheel.py  
Core Acceptance Criteria & Invariant Rule: Aggregate structured telemetry, execution latencies, token consumption, and failure diagnostics across all pipeline services into a unified observability pipeline.

---
---

## Epoch 9: Autonomous Collisions, Benchmarking & Live Proof

### 🎯 Top 2 Mandates Recommended for Claude (Lowest Token Demand):
1. **`CA-M056` (SQLite WAL Concurrency & Tuning)**: Smallest surface area; sets PRAGMAs, WAL configuration parameters, and concurrency locks.
2. **`CA-M055` (Autonomous Collision Approval Gate)**: Concise policy threshold evaluator and automated approval decision logic.

*(Note: `CA-M053` and `CA-M057` are large benchmark suites and end-to-end integration proof harnesses; assign them to ChatGPT or Grok).*

---

### Mandate 1/4: CA-M053
Mandate ID: CA-M053  
Mandate Title: CSEB Golden Benchmark Certification  
Requirement / Invariant: INV-BENCH-001  
Model Recommendation: ChatGPT / Grok (High token demand; benchmark certification suite across golden datasets)  
Target Subsystem / Files: services/pipeline/src/cmf_pipeline/benchmarks/cseb_suite.py, tests/pipeline/test_ca_m053_cseb_benchmark.py  
Core Acceptance Criteria & Invariant Rule: Execute the Conscious Activation Evaluation Benchmark against golden ground-truth reference sets. Verify compliance scores against strict tolerance bounds.

---

### Mandate 2/4: CA-M055
Mandate ID: CA-M055  
Mandate Title: Autonomous Collision Approval Gate  
Requirement / Invariant: INV-AUTO-001  
Model Recommendation: 🌟 Claude (Top 2 Lowest Token Demand — clean scoring threshold gate with fail-closed logic)  
Target Subsystem / Files: services/pipeline/src/cmf_pipeline/collision/autonomous_gate.py, tests/pipeline/test_ca_m055_autonomous_gate.py  
Core Acceptance Criteria & Invariant Rule: Enable autonomous high-confidence collision approvals under strict policy scoring thresholds without manual human intervention. Fail closed to manual review if confidence is borderline.

---

### Mandate 3/4: CA-M056
Mandate ID: CA-M056  
Mandate Title: SQLite WAL Concurrency & Tuning  
Requirement / Invariant: INV-WAL-001  
Model Recommendation: 🌟 Claude (Top 1 Lowest Token Demand — targeted PRAGMA settings, connection tuning, and locks)  
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/sqlite_tuning.py, tests/cae/test_ca_m056_sqlite_tuning.py  
Core Acceptance Criteria & Invariant Rule: Configure and verify WAL mode, busy timeout policies, memory-mapped I/O sizing, and background checkpointing for high-concurrency multi-worker SQLite state stores.

---

### Mandate 4/4: CA-M057
Mandate ID: CA-M057  
Mandate Title: Live End-to-End Proof Harness  
Requirement / Invariant: INV-PROOF-001  
Model Recommendation: ChatGPT / Grok (Highest token demand; massive 17-stage live end-to-end integration harness)  
Target Subsystem / Files: tests/e2e/test_live_e2e_proof_harness.py  
Core Acceptance Criteria & Invariant Rule: Execute the complete 17-stage Conscious Activation pipeline end-to-end from raw audience & subject genesis inputs to verified final release distribution in a live test run.
