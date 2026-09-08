# Remaining Epochs (3 to 9) — Copy-Paste Prompt Blocks

---

## Epoch 3: Anchoring, Workflows & Pre-Production Sealing

### Mandate 1/7 (Epoch 3)
Mandate ID: CA-M006
Mandate Title: Activative to Elicitation Linking
Requirement / Invariant: FR-006
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/activative_elicitation_link.py, tests/cae/test_ca_m006_activative_elicitation_link.py
Core Acceptance Criteria & Invariant Rule: Establish deterministic, bidirectional linking between activative triggers and interview elicitation steps with trace hashing. Must fail closed if an elicitation branch cannot be traced to an authorized activative origin.

---

### Mandate 2/7 (Epoch 3)
Mandate ID: CA-M011
Mandate Title: Sealed Pre-Production Pack
Requirement / Invariant: FR-PREP-001
Target Subsystem / Files: services/pipeline/src/cmf_pipeline/preproduction/sealer.py, tests/phase6/test_ca_m011_preproduction_pack.py
Core Acceptance Criteria & Invariant Rule: Enforce cryptographic sealing of pre-production assets (prompts, model manifests, media references, parameters) before downstream rendering begins. Reject any pipeline stage attempt to execute against an unsealed or modified pack.

---

### Mandate 3/7 (Epoch 3)
Mandate ID: CA-M014
Mandate Title: Cross-Window Chunking Protection
Requirement / Invariant: FR-014
Target Subsystem / Files: services/pipeline/src/cmf_pipeline/media/chunking.py, tests/phase6/test_ca_m014_cross_window_chunking.py
Core Acceptance Criteria & Invariant Rule: Prevent semantic clipping and lost audio/video boundary frames across media sliding windows with deterministic overlap stitching and timestamp alignment. Window boundaries must preserve continuous phonetic and acoustic context.

---

### Mandate 4/7 (Epoch 3)
Mandate ID: CA-M016
Mandate Title: Grounded Collision Tension Matrix
Requirement / Invariant: FR-016
Target Subsystem / Files: services/interview/src/conscious_activations_interview_expression/collision_matrix.py, tests/phase4/test_ca_m016_collision_matrix.py
Core Acceptance Criteria & Invariant Rule: Compute multidimensional collision tension scores across audience belief structures and subject genesis territory. All score matrices must be bounded, mathematically normalized [0.0, 1.0], and explainable by cited verbatim anchor coordinates.

---

### Mandate 5/7 (Epoch 3)
Mandate ID: CA-M021
Mandate Title: Anchor Hits Exact Coordinates
Requirement / Invariant: FR-ANCH-001
Target Subsystem / Files: services/interview/src/conscious_activations_interview_expression/anchor_coordinates.py, tests/phase4/test_ca_m021_anchor_coordinates.py
Core Acceptance Criteria & Invariant Rule: Map all extracted verbatim quotes, emotional cues, and reaction anchors to exact microsecond and sample-accurate coordinate spans in the master source media. Reject any anchor whose boundary timestamps exceed raw source duration.

---

### Mandate 6/7 (Epoch 3)
Mandate ID: CA-M035
Mandate Title: Workflow Dispatcher Runtime
Requirement / Invariant: INV-DISP-002
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/workflow_dispatch.py, tests/cae/test_ca_m035_workflow_dispatch.py
Core Acceptance Criteria & Invariant Rule: Orchestrate multi-stage program pipelines with idempotency keys, state rollback, step retry limits, and distributed lease lifecycle tracking. Prevent duplicate step execution and guarantee state consistency across failures.

---

### Mandate 7/7 (Epoch 3)
Mandate ID: CA-M037
Mandate Title: Agent Invocation Host Runner
Requirement / Invariant: INV-HOST-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/agent_host_runner.py, tests/cae/test_ca_m037_agent_host_runner.py
Core Acceptance Criteria & Invariant Rule: Execute external LLM and tool invocations inside an isolated runtime container with strict wall-clock timeout and byte quota limits. Enforce structured input sanitization, provider failover fallback, and deterministic token accounting.

---
---

## Epoch 4: Evidence Admission, Lineage & Gate Halting

### Mandate 1/6 (Epoch 4)
Mandate ID: CA-M007
Mandate Title: Activative Strategic Execution Object
Requirement / Invariant: FR-007
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/strategic_execution.py, tests/cae/test_ca_m007_strategic_execution.py
Core Acceptance Criteria & Invariant Rule: Validate that strategic execution payloads contain full upstream lineage ancestry (genesis, tensions, convergence receipt) and cannot be instantiated without signed operator intent.

---

### Mandate 2/6 (Epoch 4)
Mandate ID: CA-M017
Mandate Title: Multi-Dimensional Evidence Admission
Requirement / Invariant: FR-EV-001
Target Subsystem / Files: services/interview/src/conscious_activations_interview_expression/evidence_admission.py, tests/phase4/test_ca_m017_evidence_admission.py
Core Acceptance Criteria & Invariant Rule: Gate media, quote, and claim admission across confidence, corroboration count, and verbatim fidelity thresholds. Evidence below minimum admission confidence must be quarantined and barred from downstream generation.

---

### Mandate 3/6 (Epoch 4)
Mandate ID: CA-M018
Mandate Title: Hierarchical Context Lineage
Requirement / Invariant: FR-CTX-001
Target Subsystem / Files: services/interview/src/conscious_activations_interview_expression/context_lineage.py, tests/phase4/test_ca_m018_context_lineage.py
Core Acceptance Criteria & Invariant Rule: Construct and validate hierarchical parent-child context trees with immutable revision hashes and cycle detection. Prevent orphaned nodes and enforce immutable provenance references across all sub-contexts.

---

### Mandate 4/6 (Epoch 4)
Mandate ID: CA-M019
Mandate Title: Expression Moments Semantic Bridge
Requirement / Invariant: FR-SEM-001
Target Subsystem / Files: services/interview/src/conscious_activations_interview_expression/semantic_bridge.py, tests/phase4/test_ca_m019_semantic_bridge.py
Core Acceptance Criteria & Invariant Rule: Bridge raw spoken utterances with high-level conceptual activation vectors without hallucinated intermediary frames. Reject any semantic transformation that alters the core emotional polarity or subject stance.

---

### Mandate 5/6 (Epoch 4)
Mandate ID: CA-M039
Mandate Title: Deterministic Output Contract & Self-Repair
Requirement / Invariant: INV-OUT-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/output_contract_repair.py, tests/cae/test_ca_m039_output_repair.py
Core Acceptance Criteria & Invariant Rule: Enforce strict JSON/Pydantic schema validation on all program outputs. Apply bounded, deterministic AST self-repair to malformed LLM responses, and fail closed if repair cannot achieve 100% schema compliance.

---

### Mandate 6/6 (Epoch 4)
Mandate ID: CA-M040
Mandate Title: Gate Milestone Suspension Contract
Requirement / Invariant: INV-GATE-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/gate_suspension.py, tests/cae/test_ca_m040_gate_suspension.py
Core Acceptance Criteria & Invariant Rule: Safely halt and suspend pipeline execution whenever gate invariant thresholds (quality, safety, policy) are violated. Persist durable suspension state records and emit alerts without corrupting in-flight program state.

---
---

## Epoch 5: Gate Resumption, Receipts & Policy Binding

### Mandate 1/7 (Epoch 5)
Mandate ID: CA-M003
Mandate Title: Subject Constitution Lifecycle & Exception Handling
Requirement / Invariant: FR-003
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/subject_constitution.py, tests/cae/test_ca_m003_subject_constitution.py
Core Acceptance Criteria & Invariant Rule: Implement immutable Subject Constitution versioning, amendment workflows, and exception handling protocols. Prohibit direct field mutations on signed constitutions and record all amendment receipts.

---

### Mandate 2/7 (Epoch 5)
Mandate ID: CA-M020
Mandate Title: Reaction Receipts First-Class Evidence
Requirement / Invariant: FR-020
Target Subsystem / Files: services/interview/src/conscious_activations_interview_expression/reaction_receipts.py, tests/phase4/test_ca_m020_reaction_receipts.py
Core Acceptance Criteria & Invariant Rule: Upgrade interactive reaction events into cryptographically verifiable evidence tokens with actor timestamps and hash proofs. Ensure receipts cannot be forged, retroactively altered, or dissociated from source media.

---

### Mandate 3/7 (Epoch 5)
Mandate ID: CA-M022
Mandate Title: Adaptive Elicitation Remediation
Requirement / Invariant: FR-022
Target Subsystem / Files: services/interview/src/conscious_activations_interview_expression/adaptive_remediation.py, tests/phase4/test_ca_m022_adaptive_remediation.py
Core Acceptance Criteria & Invariant Rule: Trigger dynamic interview branch remediation when tension or evidence yields drop below statistical significance. Inject targeted follow-up prompts without breaking conversational coherence or constitution boundaries.

---

### Mandate 4/7 (Epoch 5)
Mandate ID: CA-M025
Mandate Title: Campaign Auth Policy (Production)
Requirement / Invariant: FR-POL-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/campaign_auth_policy.py, tests/wave04/test_ca_m025_campaign_auth_policy.py
Core Acceptance Criteria & Invariant Rule: Enforce role-based authorization, tier constraints, and spend budget thresholds for production-tier campaign execution runs. Reject unauthenticated or over-budget execution requests with descriptive denial receipts.

---

### Mandate 5/7 (Epoch 5)
Mandate ID: CA-M028
Mandate Title: Policy Revisions Execution Binding
Requirement / Invariant: FR-POL-002
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/policy_revision_binding.py, tests/wave04/test_ca_m028_policy_revision_binding.py
Core Acceptance Criteria & Invariant Rule: Bind active policy revision hashes directly to program execution leases and dispatch payloads. Invalidate and abort in-flight executions if the binding detects policy drift or stale policy snapshots.

---

### Mandate 6/7 (Epoch 5)
Mandate ID: CA-M041
Mandate Title: Reactive Gate Resumption & Receipts
Requirement / Invariant: INV-GATE-002
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/gate_resumption.py, tests/cae/test_ca_m041_gate_resumption.py
Core Acceptance Criteria & Invariant Rule: Handle asynchronous operator approvals and policy overrides to resume suspended pipeline gates. Generate immutable, non-repudiable approval receipts before releasing pipeline suspension locks.

---

### Mandate 7/7 (Epoch 5)
Mandate ID: CA-M048
Mandate Title: Path Traversal & Tool Sandbox
Requirement / Invariant: INV-SEC-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/sandbox.py, tests/cae/test_ca_m048_sandbox.py
Core Acceptance Criteria & Invariant Rule: Enforce strict path canonicalization, workspace root containment, and tool execution sandboxing. Block directory traversal attacks (`../`), symlink escapes, and unauthorized filesystem/network operations.

---
---

## Epoch 6: Memory Write-Back, CAS Concurrency & Registry

### Mandate 1/7 (Epoch 6)
Mandate ID: CA-M008
Mandate Title: Frozen Content Portfolio
Requirement / Invariant: FR-008
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/frozen_portfolio.py, tests/cae/test_ca_m008_frozen_portfolio.py
Core Acceptance Criteria & Invariant Rule: Freeze validated portfolio content manifests into immutable snapshots. Disallow any downstream mutation or format reallocation once portfolio milestone validation passes.

---

### Mandate 2/7 (Epoch 6)
Mandate ID: CA-M023
Mandate Title: Deterministic Portfolio Yield Gating
Requirement / Invariant: FR-023
Target Subsystem / Files: services/interview-intelligence/src/cae_interview_intelligence/yield_gating.py, tests/interview_intelligence/test_ca_m023_yield_gating.py
Core Acceptance Criteria & Invariant Rule: Enforce minimum viable narrative yield metrics and diversity thresholds before unlocking downstream media assembly programs. Fail closed with structured gap reports if yield is insufficient.

---

### Mandate 3/7 (Epoch 6)
Mandate ID: CA-M024
Mandate Title: Preliminary Auth Policy
Requirement / Invariant: FR-024
Target Subsystem / Files: services/interview-intelligence/src/cae_interview_intelligence/preliminary_auth.py, tests/interview_intelligence/test_ca_m024_preliminary_auth.py
Core Acceptance Criteria & Invariant Rule: Enforce pre-flight permission checks and resource quota validation for exploratory, drafting, and non-production pipeline executions.

---

### Mandate 4/7 (Epoch 6)
Mandate ID: CA-M026
Mandate Title: Durable Auth Decision Receipts
Requirement / Invariant: FR-AUTH-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/auth_decision_receipts.py, tests/wave04/test_ca_m026_auth_receipts.py
Core Acceptance Criteria & Invariant Rule: Record tamper-evident cryptographic receipts for all authorization grants, denials, and operator overrides. Receipts must contain actor identity, decision reason, policy hash, and timestamp.

---

### Mandate 5/7 (Epoch 6)
Mandate ID: CA-M032
Mandate Title: Governed Memory Write-Back
Requirement / Invariant: INV-MEM-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/memory_writeback.py, tests/wave05/test_ca_m032_memory_writeback.py
Core Acceptance Criteria & Invariant Rule: Govern automated agent write-back into shared workspace memory. Enforce schema conformance, merge consensus, conflict rejection, and provenance tracking for all persisted memory items.

---

### Mandate 6/7 (Epoch 6)
Mandate ID: CA-M042
Mandate Title: Atomic CAS SQLite Transitions
Requirement / Invariant: INV-CAS-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/sqlite_cas_transitions.py, tests/cae/test_ca_m042_sqlite_cas.py
Core Acceptance Criteria & Invariant Rule: Implement optimistic concurrency control with SQLite compare-and-swap (CAS) transactions for program state transitions. Reject concurrent writes with version mismatch exceptions and guarantee zero lost updates.

---

### Mandate 7/7 (Epoch 6)
Mandate ID: CA-M049
Mandate Title: Program Registry Immutability
Requirement / Invariant: INV-REG-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/program_registry.py, tests/cae/test_ca_m049_program_registry.py
Core Acceptance Criteria & Invariant Rule: Enforce read-only immutable registration for compiled program manifests and execution graphs. Prevent runtime tampering, unauthorized program patching, or manifest overwrites.

---
---

## Epoch 7: Merkle Receipts, Composition & Isolation

### Mandate 1/6 (Epoch 7)
Mandate ID: CA-M029
Mandate Title: No-Unanchored-Invention Invariant
Requirement / Invariant: FR-029
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/no_unanchored_invention.py, tests/wave04/test_ca_m029_no_unanchored_invention.py
Core Acceptance Criteria & Invariant Rule: Audit every generated creative claim and narrative sentence against verified verbatim and evidence sources. Automatically purge or flag any sentence that introduces unanchored facts or hallucinations.

---

### Mandate 2/6 (Epoch 7)
Mandate ID: CA-M030
Mandate Title: Immutable Release Manifest
Requirement / Invariant: FR-REL-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/release_manifest.py, tests/wave04/test_ca_m030_release_manifest.py
Core Acceptance Criteria & Invariant Rule: Bundle final campaign outputs into an immutable, cryptographically signed release manifest containing SHA-256 digests, license metadata, and full provenance trees.

---

### Mandate 3/6 (Epoch 7)
Mandate ID: CA-M043
Mandate Title: Merkle Receipt Chaining
Requirement / Invariant: INV-MRK-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/merkle_receipt_chain.py, tests/cae/test_ca_m043_merkle_receipts.py
Core Acceptance Criteria & Invariant Rule: Construct cryptographic Merkle trees connecting upstream raw evidence, intermediate gate decisions, and final distribution deliverables into a single verifiable root hash.

---

### Mandate 4/6 (Epoch 7)
Mandate ID: CA-M047
Mandate Title: Multi-Tenant Workspace Isolation
Requirement / Invariant: INV-ISO-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/workspace_isolation.py, tests/cae/test_ca_m047_workspace_isolation.py
Core Acceptance Criteria & Invariant Rule: Guarantee strict cryptographic, database, and filesystem isolation between distinct workspace tenants and campaigns. Prevent cross-tenant data leaks and state leakage.

---

### Mandate 5/6 (Epoch 7)
Mandate ID: CA-M051
Mandate Title: Model Economics & Quotas
Requirement / Invariant: INV-ECON-001
Target Subsystem / Files: services/pipeline/src/cmf_pipeline/economics/quota_engine.py, tests/pipeline/test_ca_m051_quota_engine.py
Core Acceptance Criteria & Invariant Rule: Track real-time token spend, provider rate limits, and workspace cost quotas with hard budget caps. Halt program dispatch when quotas are exhausted and emit budget overrun receipts.

---

### Mandate 6/6 (Epoch 7)
Mandate ID: CA-M052
Mandate Title: Subject Constitution Voice DNA
Requirement / Invariant: INV-VOICE-001
Target Subsystem / Files: services/interview/src/conscious_activations_interview_expression/voice_dna.py, tests/phase4/test_ca_m052_voice_dna.py
Core Acceptance Criteria & Invariant Rule: Extract acoustic and linguistic DNA features to ensure synthetic speech and tone strictly conform to the Subject Constitution. Reject synthesized outputs with unacceptable voice drift scores.

---
---

## Epoch 8: Distribution, Replay, Preemption & Evidence DAG

### Mandate 1/7 (Epoch 8)
Mandate ID: CA-M031
Mandate Title: External Distribution Delivery
Requirement / Invariant: FR-DIST-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/distribution_delivery.py, tests/wave04/test_ca_m031_distribution_delivery.py
Core Acceptance Criteria & Invariant Rule: Handle idempotent delivery to external publishing platforms and CDNs with exponential backoff, retry tracking, and signed delivery receipts.

---

### Mandate 2/7 (Epoch 8)
Mandate ID: CA-M032b
Mandate Title: Outcome Measurement Attribution
Requirement / Invariant: FR-OUT-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/outcome_attribution.py, tests/wave04/test_ca_m032b_outcome_attribution.py
Core Acceptance Criteria & Invariant Rule: Ingest post-distribution performance and audience conversion metrics, linking outcome yield directly back to specific tension collision anchors and creative components.

---

### Mandate 3/7 (Epoch 8)
Mandate ID: CA-M044
Mandate Title: Persisted Replay Verification Engine
Requirement / Invariant: INV-RPL-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/replay_engine.py, tests/cae/test_ca_m044_replay_engine.py
Core Acceptance Criteria & Invariant Rule: Provide full deterministic pipeline replay from persisted event logs and cached model responses, verifying bit-for-bit output reproducibility.

---

### Mandate 4/7 (Epoch 8)
Mandate ID: CA-M045
Mandate Title: Worker Restart & Zombie Lease Reconcile
Requirement / Invariant: INV-REC-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/zombie_reconciler.py, tests/cae/test_ca_m045_zombie_reconciler.py
Core Acceptance Criteria & Invariant Rule: Detect crashed or orphaned worker processes and expired program leases, safely reclaiming locks and resuming execution without state corruption or duplicate runs.

---

### Mandate 5/7 (Epoch 8)
Mandate ID: CA-M046
Mandate Title: Real Operator Control & Preemption
Requirement / Invariant: INV-CTRL-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/operator_preemption.py, tests/cae/test_ca_m046_operator_preemption.py
Core Acceptance Criteria & Invariant Rule: Provide real-time operator control commands (pause, drain, cancel, resume, force-kill) with instantaneous lock preemption and execution state preservation.

---

### Mandate 6/7 (Epoch 8)
Mandate ID: CA-M050
Mandate Title: Cryptographic Evidence DAG
Requirement / Invariant: INV-DAG-001
Target Subsystem / Files: services/pipeline/src/cmf_pipeline/evidence/dag.py, tests/pipeline/test_ca_m050_evidence_dag.py
Core Acceptance Criteria & Invariant Rule: Build a directed acyclic graph linking all temporal evidence moments, transcripts, tension matrices, and synthesized media blocks with cryptographic parent-hash verification.

---

### Mandate 7/7 (Epoch 8)
Mandate ID: CA-M054
Mandate Title: Unified Telemetry Flywheel
Requirement / Invariant: INV-TEL-001
Target Subsystem / Files: services/pipeline/src/cmf_pipeline/telemetry/flywheel.py, tests/pipeline/test_ca_m054_telemetry_flywheel.py
Core Acceptance Criteria & Invariant Rule: Aggregate structured telemetry, execution latencies, token consumption, and failure diagnostics across all pipeline services into a unified observability pipeline.

---
---

## Epoch 9: Autonomous Collisions, Benchmarking & Live Proof

### Mandate 1/4 (Epoch 9)
Mandate ID: CA-M053
Mandate Title: CSEB Golden Benchmark Certification
Requirement / Invariant: INV-BENCH-001
Target Subsystem / Files: services/pipeline/src/cmf_pipeline/benchmarks/cseb_suite.py, tests/pipeline/test_ca_m053_cseb_benchmark.py
Core Acceptance Criteria & Invariant Rule: Execute the Conscious Activation Evaluation Benchmark against golden ground-truth reference sets. Verify compliance scores against strict tolerance bounds.

---

### Mandate 2/4 (Epoch 9)
Mandate ID: CA-M055
Mandate Title: Autonomous Collision Approval Gate
Requirement / Invariant: INV-AUTO-001
Target Subsystem / Files: services/pipeline/src/cmf_pipeline/collision/autonomous_gate.py, tests/pipeline/test_ca_m055_autonomous_gate.py
Core Acceptance Criteria & Invariant Rule: Enable autonomous high-confidence collision approvals under strict policy scoring thresholds without manual human intervention. Fail closed to manual review if confidence is borderline.

---

### Mandate 3/4 (Epoch 9)
Mandate ID: CA-M056
Mandate Title: SQLite WAL Concurrency & Tuning
Requirement / Invariant: INV-WAL-001
Target Subsystem / Files: packages/ca_runtime/src/ca_runtime/sqlite_tuning.py, tests/cae/test_ca_m056_sqlite_tuning.py
Core Acceptance Criteria & Invariant Rule: Configure and verify WAL mode, busy timeout policies, memory-mapped I/O sizing, and background checkpointing for high-concurrency multi-worker SQLite state stores.

---

### Mandate 4/4 (Epoch 9)
Mandate ID: CA-M057
Mandate Title: Live End-to-End Proof Harness
Requirement / Invariant: INV-PROOF-001
Target Subsystem / Files: tests/e2e/test_live_e2e_proof_harness.py
Core Acceptance Criteria & Invariant Rule: Execute the complete 17-stage Conscious Activation pipeline end-to-end from raw audience & subject genesis inputs to verified final release distribution in a live test run.
