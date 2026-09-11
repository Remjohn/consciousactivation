# Conscious Activation Engine (CAE)

[![Architecture](https://img.shields.io/badge/Architecture-CAE--ARCH--001-blue.svg)](docs/cae/Architecture.md)
[![UI Contract](https://img.shields.io/badge/UI--Contract-CAE--UI--001-green.svg)](docs/cae/UI.md)
[![Status](https://img.shields.io/badge/Mandates-58%2F58%20Verified%20(100%25)-success.svg)](walkthrough.md)
[![E2E Harness](https://img.shields.io/badge/E2E--Harness-17--Stage%20Verified-brightgreen.svg)](tests/e2e/test_live_e2e_proof_harness.py)

**Conscious Activation Engine (CAE)** is an evidence-grounded production system that transforms audience intelligence, structured subject interviews, source media, collision hypotheses, and operator decisions into broadcast-grade multi-format narrative activations.

Its supreme causal law is **No-Unanchored-Invention**: downstream creative realization cannot invent upstream meaning. Every claim, quote, and creative beat must be rooted in immutable evidence, signed receipts, and monotonic state histories.

---

## The 17-Stage Causal Pipeline

CAE operates an invariant-checked, sequential 17-stage causal production lifecycle:

```
[01. Audience Context] ──► [02. Research & Evidence] ──► [03. Subject Baseline] ──► [04. Narrative Architecture]
                                                                                               │
[08. Collision Analysis] ◄── [07. Evidence Capture] ◄── [06. Structured Elicitation] ◄── [05. Declarative PreProd]
        │
        ▼
[09. Canonicalization] ──► [10. Composition] ──► [11. AIR Rendering] ──► [12. Human Authorization]
                                                                                     │
[16. Traceability] ◄── [15. Outcome Attribution] ◄── [14. Distribution] ◄── [13. Release Manifest]
        │
        ▼
[17. Memory Write-back]
```

Every stage enforces declared inputs, admission predicates, cryptographic state hashes, and immutable decision receipts.

---

## Monorepo Layout

```
consciousactivation/
├── api/                    # FastAPI REST Application (Convergence, Campaigns, Programs, Workflows)
├── apps/
│   └── web/                # React / Vite / TanStack Router UI (Control Tower, Operator, Composer)
├── packages/
│   └── ca_runtime/         # Core CAE Runtime (Leasing, CAS, StateM, Dispatch, Sandbox, Receipts)
├── services/
│   ├── pipeline/           # Media chunking, Evidence moments, DAG, Economics/Quotas, CSEB Benchmark
│   ├── interview/          # Verbatim transcription, Anchor coordinates, Collision tension matrix
│   └── interview-intelligence/ # Format matchmaking, Question resolution, Yield gating, Preliminary auth
├── docs/                   # Authoritative Specifications (Architecture.md, UI.md, Product Brief, PRD)
├── tests/                  # Unified Test Suites (E2E Live Proof Harness, CAE, Pipeline, Phase4, Phase6)
└── infra/                  # Docker Compose and deployment configurations
```

> **For AI Agents:** Review [`AGENTS.md`](AGENTS.md) before performing file scans or codebase modifications.

---

## Getting Started

### 1. Prerequisites
- **Python 3.12+**
- **Node.js 20+** & **npm**
- **Docker & Docker Compose** (optional, for full containerized stack)

### 2. Environment Configuration
Copy the sample environment file and configure credentials:
```bash
cp .env.example .env
```
Ensure `CAE_SUPABASE_DATABASE_URL` and your LLM provider API keys (OpenAI, Anthropic, Gemini, Grok) are set.

### 3. Running the Backend API
```bash
# Install root package dependencies in editable mode
pip install -e packages/ca_runtime
pip install -e services/pipeline
pip install -e services/interview
pip install -e services/interview-intelligence

# Start the FastAPI gateway server
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be available at: `http://localhost:8000/docs`.

### 4. Running the Web UI
```bash
cd apps/web
npm install
npm run dev
```
The Operator Web UI will be available at: `http://localhost:5173`.
- **`/operator`**: Program Operator execution console, preemption, and run inspection.
- **`/campaigns`**: Campaign overview and 17-stage Control Tower.
- **`/interviews/compose`**: Interactive interview composer.
- **`/harnesses`**: Certified format harness library.

---

## Running Automated Verification & Tests

CAE includes an end-to-end test suite enforcing all 58 mandate invariants.

```bash
# Run the 17-Stage Live End-to-End Proof Harness:
python scratch/run_single_test.py tests/e2e/test_live_e2e_proof_harness.py

# Run targeted subsystem test suites:
python scratch/run_single_test.py tests/cae/test_ca_m002_convergence_gate.py
python scratch/run_single_test.py tests/pipeline/test_ca_m050_evidence_dag.py
python scratch/run_single_test.py tests/phase4/test_ca_m016_collision_matrix.py

# Run the golden benchmark certification (CSEB):
python scratch/run_single_test.py tests/pipeline/test_ca_m053_cseb_benchmark.py
```

---

## Canonical Authority & Documentation
- **[Architecture Specification (`CAE-ARCH-001`)](docs/cae/Architecture.md):** Complete physical system design and convergence map.
- **[Operator UI Contract (`CAE-UI-001`)](docs/cae/UI.md):** Control surface rules, invariants, and navigation structure.
- **[Canonical PRD & Addendum](docs/PRD/CURRENT.md):** Product Requirements Document including the 58-Mandate Master Addendum.
- **[Product Brief](docs/cae/CAE_Product_Brief/):** The 17-chapter theoretical and strategic foundation of Conscious Activations.
- **[Walkthrough & Verification Receipts](walkthrough.md):** Detailed pass logs, commit SHAs, and test matrices across Epochs 01–09.
