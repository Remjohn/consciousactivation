# CAE Monorepo Directory Map

Authoritative directory layout for the Conscious Activation Engine (CAE) monorepo:

```text
consciousactivation/
├── AGENTS.md                  # Authoritative navigation & engineering rules for AI agents
├── README.md                  # Architecture, 17-stage causal pipeline & quickstart
├── FOLDER_MAP.md              # Current directory map
├── pyproject.toml             # Python package paths & pytest configuration
│
├── packages/                  # Core CAE Runtime Packages
│   ├── ca_runtime/            # SQLite CAS StateM, leasing, agent host runner, sandboxing
│   ├── ca_contracts/          # Immutable schemas, step contracts, gate definitions
│   └── ca_delegation_rc4/     # Delegation boundary contracts
│
├── services/                  # Operational Subsystem Services
│   ├── pipeline/              # Media chunking, evidence DAG, EDL synthesis, FFmpeg rendering
│   ├── interview/             # Verbatim Whisper capture, exact anchor coordinates, collision matrix
│   ├── interview-intelligence/# Question resolver, format matchmaking, yield gating
│   ├── air/                   # Activative Intelligence & brand genesis runtime
│   ├── builder/               # Atomic harness compiler & domain models (imported by ca_runtime)
│   └── vae/                   # Visual Asset Editor adapter (imported by ca_runtime)
│
├── api/                       # FastAPI Gateway Application
│   ├── main.py                # Server entrypoint mounting all routers
│   └── routers/               # /convergence, /campaigns, /programs, /interviews, etc.
│
├── apps/                      # Frontend Applications
│   └── web/                   # Vite / React 18 / TanStack Router operator web UI
│
├── agents/                    # Canonical Agent Packages (Hunter, Analyst, Composer, Commander)
├── programs/                  # Domain Program Specifications & Workflows
├── tests/                     # Automated Test Suites (e2e, cae, phase4, pipeline)
├── docs/                      # Authoritative PRD, UI specifications, and Architecture
├── governance/                # Canonical constitutions, protocols, and alignment ledgers
├── scratch/                   # Authoritative test execution scripts (run_single_test.py)
│
└── archive/                   # Archived Legacy Codebases & Bundles (Historical Only)
    ├── brownfield/            # Superseded brownfield drafts & chat archives
    ├── mandates_implementation/# Ingested and merged epoch mandate bundles
    ├── specs/                 # Historical PRD v1.2 drafts
    ├── stage1_output/         # Transient compiler outputs
    ├── tmp_stage2/            # Transient compiler artifacts
    ├── temp_zips/             # Historic delivery zip extractions
    └── atomic_harnesses_visual_syntax/ # Specimen reference images
```
