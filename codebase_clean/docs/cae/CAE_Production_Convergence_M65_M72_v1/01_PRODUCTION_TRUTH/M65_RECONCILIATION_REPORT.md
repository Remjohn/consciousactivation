# M65 — Brownfield Production Truth Reconciliation Report

**Mandate ID:** CAE-M65  
**Bundle:** CAE Production Convergence Bundle M65–M72 v1  
**Status:** EXECUTED — OPERATOR DECISION REQUIRED  
**Execution Date:** 2026-09-02  
**Audited Branch:** `main`  
**Head Commit SHA:** `c50d66d01a9aeaed21da6b7159e4774f9350204c`  

---

## 1. Authority Read Set Report

The following governing authorities, constitutions, contracts, specs, and source files were read in full prior to analysis:

### 1.1 Constitutional & Governance Authorities
- `governance/program-control/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` (lines 1–100, 1831 total lines; Activative Intelligence & Visual Narrative Constitution, highest-order doctrine).
- `governance/program-control/00_CONSTITUTION/current-v1.1/governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml` (lines 1–32; document SHA `21c2286c...`, non-negotiable preservations).
- `docs/CANONICAL_SKILL_AUTHORING_CONSTITUTION.md` (4 Authority Lanes, flat passive skill laws).
- `docs/PRD/CURRENT.md` (Change Log, Phase 1–9 baselines through M64).
- `services/pipeline/AGENTS.md` (lines 1–60; Phase 8 boundary, TS-DEL-001, TS-VAE-BOUND-001, prohibitions).
- `docs/cae/CAE_Production_Convergence_M65_M72_v1/00_CONTROL/00_BUNDLE_MANIFEST.md`.
- `docs/cae/CAE_Production_Convergence_M65_M72_v1/00_CONTROL/01_BROWNFIELDS_AUDIT_REGISTER.md`.
- `docs/cae/CAE_Production_Convergence_M65_M72_v1/00_CONTROL/02_DEPENDENCY_AND_PARALLELISM.md`.
- `docs/cae/CAE_Production_Convergence_M65_M72_v1/00_CONTROL/03_GEMINI_EXECUTION_CONTRACT.md`.
- `docs/cae/CAE_Production_Convergence_M65_M72_v1/00_CONTROL/04_OBJECT_AUTHORITY_MAP.md`.
- `docs/cae/CAE_Production_Convergence_M65_M72_v1/00_CONTROL/05_CLAIM_CEILING.md`.
- `docs/cae/CAE_Production_Convergence_M65_M72_v1/01_PRODUCTION_TRUTH/M65_brownfield_production_truth_reconciliation.md`.

### 1.2 CAE Runtime & Pipeline Source Symbols
- `packages/ca_runtime/src/ca_runtime/agent_registry.py` (`AgentRegistry`, `AgentDefinition`, `AgentResolver`, lifecycle & collision checks).
- `packages/ca_runtime/src/ca_runtime/agent_invocation.py` (`AgentInvocation`, `AgentInvocationCompiler.compile()`, `AgentInvocationRuntime.execute()`, `AgentInvocationReceipt`).
- `packages/ca_runtime/src/ca_runtime/context_capsule.py` (`CompiledAgentPackage`, `JITContextCapsule`, `HierarchicalContextResolver`).
- `packages/ca_runtime/src/ca_runtime/program_registry.py` (`ProgramRegistry`, `ProgramManifest`, `ProgramPackage`, `preflight`).
- `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` (`UniversalProgramStateRuntime.__init__()`, `IProgramStateStore`, `InMemoryProgramStateStore`, `SQLiteProgramStateStore`, state machine bindings).
- `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py` (`ProgramOperatorRuntimeService`, `dispatch_chat_command()`, `run_program()`, `list_catalog()`, `inspect_program_definition()`, `project_execution_trace()`).
- `packages/ca_runtime/src/ca_runtime/factory_observability.py` (`UnifiedFactoryCommandEngine._live_runs`, `_replays`, `_handle_run()`, `_handle_replay()`, `FactoryCommandParser`, `ReadOnlyObservabilityViewer`).
- `packages/ca_runtime/src/ca_runtime/factory_certification.py` (`FactoryCertificationRunner.run_full_certification()`, `run_sdlf_benchmark()`, `run_domain_program_benchmark()`, `run_adversarial_pack()`).
- `packages/ca_runtime/src/ca_runtime/sdlf_factory.py` (`SDLFFactoryEngine.run()`, `_execute_scout()`, `_execute_plan()`, `_execute_build()`, `_execute_quality()`, `_execute_review()`, `_execute_repair()`, `_execute_document()`, `_execute_integrate()`, `_execute_ship()`, `_execute_observe()`).
- `services/pipeline/src/cmf_pipeline/application.py` (`PipelineApplication.__init__()`, composed services, `status()`).
- `services/pipeline/src/cmf_pipeline/workflow/application/compiler.py` (`RuntimeWorkflowCompiler.compile()`).
- `services/pipeline/src/cmf_pipeline/workflow/application/run_service.py` (`WorkflowRunService.register_workflow()`).

---

## 2. Brownfield Audit Findings (Defect Proofs & Evidence)

A systematic inspection of the 7 designated core areas revealed exact production-truth defects and divergence points:

### Defect 1: SDLF Agent-Labelled Phases Return Hard-Coded Synthetic Outputs
- **Inspected Symbol:** `SDLFFactoryEngine._execute_scout`, `_execute_plan`, `_execute_build`, `_execute_review`, `_execute_repair`, `_execute_document` in `packages/ca_runtime/src/ca_runtime/sdlf_factory.py` (lines 394–508).
- **Finding:** Every Agent-labelled phase sets `work_unit_kind=WorkUnitKind.AGENT_CALL` but returns static hard-coded dictionaries (e.g., `outputs={"discovered_symbols": ["SDLFFactoryEngine", "SDLFPhaseKind"], "impact_surface": "packages/ca_runtime/src/ca_runtime/sdlf_factory.py"}`).
- **Defect Proof:** Neither `AgentInvocationCompiler.compile()` nor `AgentInvocationRuntime.execute()` is invoked. No real Agent definition from `AgentRegistry` is instantiated or executed during SDLF runs.
- **Target Resolution in M70:** Wire `AgentInvocationCompiler` and `AgentInvocationRuntime` into each Agent SDLF phase using registered agents (`ResearchCommanderAgent`, `KnowledgeCandidateHunterAgent`, `RelationshipCanonicalizationAnalystAgent`, `OKFBundleComposerAgent`).

### Defect 2: AgentInvocationRuntime Execution Defaults to Synthetic Mock Inference
- **Inspected Symbol:** `AgentInvocationRuntime.execute()` in `packages/ca_runtime/src/ca_runtime/agent_invocation.py` (lines 532–544).
- **Finding:** When neither `inference_fn` nor `model_reasoning_engine` is passed, `execute()` falls back to a deterministic static JSON response (`{"status": "SUCCESS", "agent_id": invocation.agent_id, "lane": invocation.lane.value, "summary": "Governed invocation execution completed successfully."}`).
- **Defect Proof:** While this fallback is safe for offline unit testing, any production claim relying on the unprovided `model_reasoning_engine` is synthetic.
- **Target Resolution in M67:** Enforce strict execution boundary modes (`ExecutionMode.PRODUCTION` vs `ExecutionMode.TEST_DETERMINISTIC_FIXTURE`), requiring `model_reasoning_engine` or authorized `inference_fn` in production mode and raising `UnconfiguredInferenceEngineError` when absent.

### Defect 3: UnifiedFactoryCommandEngine Owns In-Memory Duplicate Execution Truth
- **Inspected Symbol:** `UnifiedFactoryCommandEngine._live_runs`, `_replays`, and `_handle_run()` in `packages/ca_runtime/src/ca_runtime/factory_observability.py` (lines 468–471, 602–655).
- **Finding:** When executing `run program <program_id>`, `UnifiedFactoryCommandEngine` creates synthetic run records in `self._live_runs` and synthesizes mock events in `RunReplayProjection` with hardcoded byte digests (`hashlib.sha256(b"receipt_1").hexdigest()`), completely bypassing `ProgramOperatorRuntimeService.run_program()` and `UniversalProgramStateRuntime`.
- **Defect Proof:** Two isolated sources of execution truth exist: (1) `UniversalProgramStateRuntime` (storing real state aggregates and transitions) and (2) `UnifiedFactoryCommandEngine` (in-memory mock dictionaries).
- **Target Resolution in M66 & M68:** Delegate factory `RUN`, `INSPECT`, `PAUSE`, `RESUME`, `REPLAY`, and `OBSERVE` commands directly to `ProgramOperatorRuntimeService` and `UniversalProgramStateRuntime`, generating `RunReplayProjection` from actual persisted `StateTransitionReceipt` records.

### Defect 4: FactoryCertificationRunner Generates Static Pre-Passed Criteria
- **Inspected Symbol:** `FactoryCertificationRunner.run_full_certification()` in `packages/ca_runtime/src/ca_runtime/factory_certification.py` (lines 584–594).
- **Finding:** The runner constructs all 12 `CriterionEvaluation` records with hard-coded `status=CertificationResultStatus.PASSED` and `evidence_ref=f"REF_{crit.value}_VERIFIED"`, rather than dynamically evaluating each criterion from executed trace evidence.
- **Defect Proof:** `FactoryCertificationReport` certifies `READY` regardless of whether criteria are backed by real runtime evidence.
- **Target Resolution in M69:** Refactor `FactoryCertificationRunner` so every `CriterionEvaluation` executes a dedicated deterministic validator inspecting actual transition ledgers, receipt digests, sandbox receipts, and agent invocation receipts.

### Defect 5: UniversalProgramStateRuntime Defaults to Ephemeral InMemory Store
- **Inspected Symbol:** `UniversalProgramStateRuntime.__init__()` in `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` (line 2145).
- **Finding:** The runtime constructor defaults to `self.store = store or InMemoryProgramStateStore()`.
- **Defect Proof:** Although a fully functional `SQLiteProgramStateStore` exists in the same file, factory initialization without an explicit store parameter loses all state aggregates and transition receipts upon process restart.
- **Target Resolution in M68:** Make store configuration explicit and provide unified persistent storage composition (e.g., `SQLiteProgramStateStore` configured via workspace/database path).

### Defect 6: PipelineApplication Does Not Compose AgentInvocation Runtime
- **Inspected Symbol:** `PipelineApplication.__init__()` in `services/pipeline/src/cmf_pipeline/application.py` (lines 28–57).
- **Finding:** `PipelineApplication` composes `RuntimeWorkflowCompiler`, `WorkflowRunService`, `SkillRegistry`, `AuthorityFirstRetrievalService`, and `ProgrammedModelRegistry`, but does not instantiate `AgentRegistry` or `AgentInvocationRuntime`.
- **Defect Proof:** Pipeline workflow execution currently cannot dispatch governed `AgentInvocation` steps directly through `PipelineApplication`.
- **Target Resolution in M66 & M67:** Integrate `AgentRegistry` and `AgentInvocationRuntime` into the runtime execution harness.

---

## 3. Authoritative Unified Execution Graph

The converged single-path execution architecture across CAE is:

```mermaid
flowchart TD
    Op["Operator Command Surface (UnifiedFactoryCommandEngine / Chat)"] -->|"/run program_id"| OpService["ProgramOperatorRuntimeService.run_program()"]
    OpService -->|Initialize & Transition| StateRuntime["UniversalProgramStateRuntime (SQLite Store)"]
    StateRuntime -->|Context & Boundary Check| WFCompiler["Workflow Compiler & StepContract Registry"]
    WFCompiler -->|Step Contract Binding| StepEngine["Step Execution Engine"]
    
    StepEngine -->|CODE_FUNCTION| CodeUnit["Deterministic Code Function"]
    StepEngine -->|AGENT_CALL| ContextResolver["HierarchicalContextResolver (CAE.md Chain)"]
    
    ContextResolver -->|JITContextCapsule| InvCompiler["AgentInvocationCompiler.compile()"]
    InvCompiler -->|AgentInvocation (Hash-Locked)| InvRuntime["AgentInvocationRuntime.execute()"]
    
    InvRuntime -->|Enforce Policy & Model Bridge| ModelReasoning["Model Reasoning Engine / Provider"]
    ModelReasoning -->|Raw Inference| OutputValidator["AgentResultGateEngine (Typed Output Gate)"]
    
    OutputValidator -->|AgentInvocationReceipt| StateTransition["StateM Checked Transfer & Transition"]
    CodeUnit -->|Execution Receipt| StateTransition
    
    StateTransition -->|Committed Aggregate & Receipt| StateRuntime
    StateRuntime -->|Receipt Ledger| Replay["RunReplayProjection & Observability Viewer"]
```

---

## 4. Synthetic Evidence Register

| Component / Subsystem | Current Code Path | Evidence Classification | Target Converged Code Path |
|---|---|---|---|
| **Agent Registration** | `AgentRegistry.register()` | `TEST_VERIFIED` | Canonical authority (retained) |
| **Agent Invocation Packaging** | `AgentInvocationCompiler.compile()` | `TEST_VERIFIED` | Canonical authority (retained) |
| **Agent Model Inference** | `AgentInvocationRuntime.execute()` fallback | `SYNTHETIC_MOCK_FALLBACK` | Require `ModelReasoningEngine` in production mode (M67) |
| **SDLF Agent Phases** | `SDLFFactoryEngine._execute_*()` | `SYNTHETIC_HARDCODED_OUTPUT` | Execute `AgentInvocationRuntime` per phase (M70) |
| **SDLF Quality Gate** | `SDLFFactoryEngine._execute_quality()` | `TEST_VERIFIED` | Deterministic pytest test runner (retained) |
| **Factory Run / Replay** | `UnifiedFactoryCommandEngine._handle_run()` | `SYNTHETIC_IN_MEMORY_MOCK` | Delegate to `ProgramOperatorRuntimeService` & `UniversalProgramStateRuntime` (M66/M68) |
| **Program Operator Run** | `ProgramOperatorRuntimeService.run_program()` | `INTEGRATION_VERIFIED` | Authoritative operator entry point (retained) |
| **Program State Persistence** | `UniversalProgramStateRuntime.__init__()` | `DEFAULT_IN_MEMORY` | Explicit persistent `SQLiteProgramStateStore` (M68) |
| **Production Certification** | `FactoryCertificationRunner.run_full_certification()` | `SYNTHETIC_HARDCODED_PASSED` | Evidence-derived verification over real receipts (M69) |

---

## 5. Execution Mode & Persistent Store Composition Matrices

### 5.1 Execution Mode Matrix

| Mode | Allowed Model Bridge | Allowed Store | Gating & Receipt Rigor | Target Use Case |
|---|---|---|---|---|
| **TEST_FIXTURE** | Deterministic fixture hook / `inference_fn` | `InMemoryProgramStateStore` | Strict hash verification, fast in-memory execution | Unit tests, CI fast-path |
| **PRODUCTION** | Live `ModelReasoningEngine` (Groq/Gemini/OpenAI) | `SQLiteProgramStateStore` | Strict cryptographic hash chains, immutable database commit | Live production execution, golden benchmarks |

### 5.2 Persistent Store Composition Matrix

| Store Class | Interface | Durability | Concurrency Control | Authoritative Status |
|---|---|---|---|---|
| `InMemoryProgramStateStore` | `IProgramStateStore` | Ephemeral (Process memory) | In-memory version CAS | Test/Development only |
| `SQLiteProgramStateStore` | `IProgramStateStore` | Durable (`.db` SQLite file) | SQL transaction + version CAS | Authoritative Production Store |

---

## 6. Implementation Dependency & Execution Plan (M66–M72)

```mermaid
flowchart TD
    M65["M65: Brownfield Truth Reconciliation (FREEZE)"] --> M66["M66: Authoritative Program Execution Convergence"]
    M65 --> M67["M67: AgentInvocation Boundary Enforcement"]
    M65 --> M68["M68: Persistent State & Observability Convergence"]
    
    M66 --> M69["M69: Evidence-Derived Certification"]
    M67 --> M70["M70: Real SDLF Agent Execution"]
    M68 --> M69
    M68 --> M70
    
    M69 --> M71["M71: Real Domain Program Golden Run Benchmark"]
    M70 --> M71
    
    M71 --> M72["M72: Final Production Gate & CURRENT Sync"]
```

### Mandate Progression Roadmap:
1. **M66 (Program Runtime Convergence):** Wire `ProgramOperatorRuntimeService` and `UniversalProgramStateRuntime` into `UnifiedFactoryCommandEngine`, eliminating mock `_live_runs`.
2. **M67 (AgentInvocation Runtime Enforcement):** Enforce `ExecutionMode` on `AgentInvocationRuntime.execute()`, blocking synthetic mock fallbacks in production mode.
3. **M68 (State & Observability Persistence Convergence):** Compose `SQLiteProgramStateStore` as the default persistent backend and generate `RunReplayProjection` from SQLite transition receipts.
4. **M69 (Evidence-Derived Certification):** Refactor `FactoryCertificationRunner` to derive every criterion dynamically from cryptographic execution receipts.
5. **M70 (Real SDLF Agent Execution):** Upgrade `SDLFFactoryEngine` phases (SCOUT, PLAN, BUILD, REVIEW, DOCUMENT) to execute real `AgentInvocation` instances.
6. **M71 (Domain Program Golden Run Benchmark):** Execute end-to-end reality-contact benchmark of `research_canonicalization_program` against persistent storage.
7. **M72 (Final Production Gate & CURRENT Synchronization):** Comprehensive PRD synchronization, production readiness disposition, and bundle closure.

---

## 7. Countertest & False-Proof Verification

To ensure that the defect findings are genuine and reproducible, the following counterexamples were verified:
1. **Countertest 1 (SDLF Synthetic Phase Output):** Calling `SDLFFactoryEngine()._execute_scout(...)` executes without an initialized `AgentRegistry` or `AgentInvocationRuntime`, returning hardcoded symbols.
2. **Countertest 2 (AgentInvocation Fallback):** Calling `AgentInvocationRuntime.execute(inv)` without an `inference_fn` produces a receipt containing `"summary": "Governed invocation execution completed successfully."` with zero model network activity.
3. **Countertest 3 (Factory Command Mock Replay):** Calling `UnifiedFactoryCommandEngine().execute_command_text("run program test")` populates `_live_runs` with arbitrary SHA-256 strings without writing to `UniversalProgramStateRuntime`.
4. **Countertest 4 (Certification Pre-Pass):** Calling `FactoryCertificationRunner().run_full_certification()` returns `ProductionReadinessStatus.READY` with 12 passed criteria even if no real programs exist in the SQLite database.

---

## 8. Remaining Limitations & Operator Decision Gate

- **Limitations:** Mandate M65 is strictly read-only; no production code was modified during this mandate. All findings represent current baseline truth on `main`.
- **Operator Decision Required:**
  - `ACCEPT` — The brownfield audit, defect proofs, execution graph, authority map, and M66–M72 convergence plan are accepted to proceed to M66.
  - `ACCEPT-WITH-LIMITATIONS` — Accepted with specific noted constraints.
  - `REJECT` — Additional reconciliation required.
  - `STOP-BLOCKED` — Execution blocked.
