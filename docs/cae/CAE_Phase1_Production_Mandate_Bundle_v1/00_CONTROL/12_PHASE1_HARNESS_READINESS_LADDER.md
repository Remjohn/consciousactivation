# Phase 1 — Harness & Atomic Harness Readiness Ladder

**Status:** RATIFIED — OPERATOR-APPROVED  
**Governing Mandate:** `CAE-M03` (Phase 1)  
**Constitutional Reference:** `00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`  

---

## 1. Core Architectural Principle
A Harness or Atomic Harness may **never** be classified as ready or usable from documentation, authoring prompts, or filesystem existence alone. Every Harness exists on a strictly verifiable 10-rung readiness ladder, maintaining total separation between authoring specifications, distribution packages, pipeline intake schemas, and runtime execution projections.

---

## 2. The 10-Rung Readiness Ladder

| Rung | Level Name | Formal Definition & Entry Criteria | Required Proof / Verification Artifact |
| :---: | :--- | :--- | :--- |
| **1** | `AUTHORED` | Raw visual reference bundles, specimen image sequences, and process documentation exist in `atomic_harnesses_visual_syntax/`. | File directory containing sequential visual frames (`01.jpg`, `02.jpg`, ...) and format documentation. |
| **2** | `SCHEMATIZED` | Stage 1 structural extraction report and Stage 2 syntax specification generated with zone definitions and layout constraints. | `stage1_output/<harness_id>_STAGE1_REPORT.json` and `stage1_output/specs/<harness_id>_STAGE2_SPEC.json`. |
| **3** | `COMPILED` | Valid `operator_manifest.json` parsed and built into an in-memory/sqlite `PortableAtomicHarnessDefinition`. | Ingestion and build via `cmf_builder.cli build` producing valid `record_kind == "atomic_harness_definition"`. |
| **4** | `REGISTERED` | Exported into a standalone distribution archive containing `atomic_harness_definition.json` with canonical SHA-256 hash. | Archive located at `${CA_HARNESS_LIBRARY_ROOT}/<definition_id>.zip` with verified integrity. |
| **5** | `LOADABLE` | Discovered, parsed, and queryable by the API layer (`GET /api/harnesses`, `GET /api/harnesses/{id}`). | HTTP 200 OK responses from `api/routers/harnesses.py` returning `HarnessSummary` and `HarnessDetail`. |
| **6** | `RUNNABLE` | Bridged via `compile_portable_to_intake()` into the 14-key `AtomicHarnessDefinitionIntake` shape and admitted to Pipeline. | `cmf_pipeline.intake.definition_intake.AtomicHarnessDefinitionIntake.validate()` passes with zero blocker exceptions. |
| **7** | `STATE-VERIFIED` | Bound to typed CAE state aggregates (`cae.harness_template`, `cae.harness_run`) and governed transitions. | State machine transition assertions pass under `CA-CAN-01C_HARNESS_RUN.yaml` and `MC-CAE-RUN-001`. |
| **8** | `RECEIPT-VERIFIED` | Generates immutable, cryptographically verifiable execution receipts (MCDA, CBAR, evaluation receipts). | Receipts persisted in `cae.receipt` with matching hash lineage and evidence citations. |
| **9** | `OPERATOR-VERIFIED` | Supervised end-to-end execution verified and ratified by a human operator. | Interactive run telemetry and explicit operator acceptance record. |
| **10**| `PRODUCTION-CANDIDATE`| Meets all production gates, invariant assertions, and certification criteria (`production_ready: true`, `certified: true`). | Complete production qualification and certification approval. |

---

## 3. Four Harness Projections & Separation of Concerns

1. **Authoring Manifest (`operator_manifest.json`):**
   - Authored specification containing task goals, atomic boundaries, and `activative_input` citations (`source_premise_ref` through `evaluation_contract_ref` and `wrong_reading_locks`).
2. **Distribution Package (`PortableAtomicHarnessDefinition`):**
   - 32-key immutable export bundle created by Builder CLI, containing category binding, mode, and cryptographic hash lineage.
3. **Pipeline Intake (`AtomicHarnessDefinitionIntake`):**
   - 14-key runtime intake shape validated by Pipeline intake compiler; generic modes and deferred categories (`format02`) are rejected.
4. **Execution Workflow Projection (`RuntimeWorkflowCompiler`):**
   - Concrete directed acyclic graph (DAG) composed of nodes, edges, capability bindings, and typed CAE state mutations.

---

## 4. Current Repository Inventory Ledger

### Cataloged Visual Harnesses (49 Total)
- **Carousels (37 Harnesses):** Currently at **Rung 2 (`SCHEMATIZED`)** with complete Stage 1 reports and Stage 2 specs.
- **SuperVisuals (12 Harnesses):** Currently at **Rung 2 (`SCHEMATIZED`)** with complete Stage 1 reports and Stage 2 specs.
- **Video & Theatre Formats:** Currently at **Rung 1 (`AUTHORED`)** (`format01`, `format03`, `format04`, `format05`).
- **Deferred Formats:** `format02_living_commentary` (**Rung 1**, deferred by architectural policy).

### Tested Synthetic & Expression Harnesses
- `operator-manifest-activative-expression`: **Rung 6 (`RUNNABLE`)**
- `operator-manifest-generic-summary`: **Rung 5 (`LOADABLE`)** (Mode gate prevents Rung 6).
- `synthetic_text_normalization_v1`: **Rung 5 (`LOADABLE`)**

---

## 5. Pilot Harness Selection

- **Selected Candidate:** `CAR-LST-Olympics-4-5-10` (Carousel Listicle, 10 slides)
- **Current Rung:** Rung 2 (`SCHEMATIZED`)
- **Advancement Goal:** Complete manifest authoring, Builder packaging, and intake compilation to achieve Rung 6 (`RUNNABLE`).

