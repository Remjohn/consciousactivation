# AGENTS.md — Repository Guidance for AI Agents

Welcome to the **Conscious Activation Engine (CAE)** codebase. This document is the **authoritative navigation map** for AI agents (Antigravity, Cursor, Claude, ChatGPT, etc.) working in this repository.

---

## 1. Active Codebase vs. Legacy Archives

This repository was developed through multiple iterations. **Do NOT scan or edit legacy archive folders** unless explicitly instructed by the operator.

### 🟢 ACTIVE DIRECTORIES (Authoritative Source of Truth)

| Directory | Subsystem / Purpose | Key Entrypoints & Models |
| :--- | :--- | :--- |
| **`packages/ca_runtime/`** | **Core CAE Runtime Engine** (Leasing, CAS, StateM, Workflow Dispatch, Agent Runner, Policies, Sandboxing, Receipts) | `src/ca_runtime/program_state_runtime.py`<br>`src/ca_runtime/workflow_dispatch.py`<br>`src/ca_runtime/sqlite_cas_transitions.py`<br>`src/ca_runtime/agent_host_runner.py`<br>`src/ca_runtime/sandbox.py` |
| **`services/pipeline/`** | **Media, Evidence & Benchmark Pipeline** (Evidence Moments, Video Chunking, Evidence DAG, Token Quotas, CSEB Benchmarks) | `src/cmf_pipeline/media/chunking.py`<br>`src/cmf_pipeline/evidence/dag.py`<br>`src/cmf_pipeline/economics/quota_engine.py`<br>`src/cmf_pipeline/benchmarks/cseb_suite.py` |
| **`services/interview/`** | **Interview & Expression Engine** (Verbatim Whisper Capture, Anchor Hits Coordinates, Collision Tension Matrix, Voice DNA) | `src/conscious_activations_interview_expression/verbatim.py`<br>`src/conscious_activations_interview_expression/anchor_coordinates.py`<br>`src/conscious_activations_interview_expression/collision_matrix.py` |
| **`services/interview-intelligence/`** | **Interview Intelligence & Gating** (Question Resolver, Format Matchmaking, Yield Gating, Preliminary Auth) | `src/cae_interview_intelligence/yield_gating.py`<br>`src/cae_interview_intelligence/preliminary_auth.py`<br>`src/cae_interview_intelligence/question_resolver.py` |
| **`api/`** | **FastAPI Gateway Application** (REST endpoints for convergence, campaigns, programs, workflows, harnesses) | `api/main.py`<br>`api/routers/convergence.py`<br>`api/routers/programs.py`<br>`api/routers/campaigns.py` |
| **`apps/web/`** | **React / Vite / TanStack Router Web UI** (Control Tower, Program Operator, Interview Composer, Campaign New) | `src/routes/operator/index.tsx`<br>`src/routes/campaigns/$campaignId.tsx`<br>`src/routes/interviews/compose/index.tsx`<br>`src/components/layout/Sidebar.tsx` |
| **`tests/`** | **Automated Test Suites** (cae, phase4, phase6, wave04, wave05, pipeline, e2e) | `tests/e2e/test_live_e2e_proof_harness.py`<br>`tests/cae/`<br>`tests/pipeline/` |

---

### 🔴 DO NOT SCAN / LEGACY DIRECTORIES (Ignore During Normal Work)

The following directories contain obsolete brownfield prototypes, legacy transcripts, or superseded specifications. **Avoid scanning them to preserve context window tokens:**

- `Conscious Activation Engine Brownfield/` (superseded brownfield codebase)
- `archive/` (historical archives)
- `services/builder/`, `services/delegation/`, `services/studio/`, `services/vae/` (legacy decoupled service prototypes; consolidated into `ca_runtime` and `cmf_pipeline`)
- `Mandates implementation/` (completed bundle staging; all files are already merged into the codebase)
- `temp_zips/`, `tmp_stage2/`, `stage1_output/` (transient build artifacts)

---

## 2. Core Architectural Laws

When modifying or extending this codebase, adhere strictly to these non-negotiable laws:

1. **Causal Invariance (No-Unanchored-Invention):**
   - Downstream realization cannot invent upstream meaning.
   - All creative claims, quotes, and media segments must resolve to verified `evidence_moment` records or verbatim transcripts.
2. **Fail-Closed Governance:**
   - If a gate, policy, or schema validation check fails or encounters an ambiguous state, it must fail closed (raise an exception or return a blocked status receipt), never fail open.
3. **Receipts & Monotonic State:**
   - State transitions must occur via SQLite Compare-And-Swap (`cas_update_program_state_aggregate`).
   - Every consequential decision, gate approval, or lease dispatch produces an immutable, cryptographically hashed receipt.
4. **Never Modify Tests to Force Passes:**
   - Test assertions reflect normative contract invariants. Never weaken, comment out, or delete assertions to make a test pass. Fix the underlying implementation or fixture gap.

---

## 3. Authoritative Testing Instructions

Due to monorepo package structures on Windows, run tests using the repository's dedicated runner:

```bash
# Run any individual test file or group of files:
python scratch/run_single_test.py tests/e2e/test_live_e2e_proof_harness.py

# Or via pytest directly with asyncio disabled:
pytest -p no:asyncio tests/cae/test_ca_m002_convergence_gate.py
```

---

## 4. Key Reference Documents

- **Architecture:** [`docs/cae/Architecture.md`](file:///d:/Work/consciousactivation/docs/cae/Architecture.md)
- **Operator UI Specification:** [`docs/cae/UI.md`](file:///d:/Work/consciousactivation/docs/cae/UI.md)
- **Canonical PRD & Master Addendum:** [`docs/PRD/CURRENT.md`](file:///d:/Work/consciousactivation/docs/PRD/CURRENT.md)
- **Product Brief (Theory & Pillars):** [`docs/cae/CAE_Product_Brief/`](file:///d:/Work/consciousactivation/docs/cae/CAE_Product_Brief/)
- **Integration Walkthrough & Verification Proofs:** [`walkthrough.md`](file:///d:/Work/consciousactivation/walkthrough.md)
