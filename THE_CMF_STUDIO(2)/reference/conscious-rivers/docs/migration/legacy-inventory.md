# Legacy Repository Inventory & Migration Ledger

> [!IMPORTANT]
> **Target Architecture Paradigm:** Python-first Harness using Pydantic, DSPy, and Pi Coding Agent orchestration, with TypeScript restricted to the PWA, Telegram Mini App, Remotion/Motion Canvas, and generated contract consumers.
> 
> This inventory implements the Greenfield Rule. The legacy repository serves as a read-only registry, doctrine, fixture, example, and provider-code source. No legacy code is imported directly into the production CMF Studio runtime.

## 1. Executive Summary: The Interview-First Pivot (CMF STUDIO)

Following the Claude Ntahuga project, it became evident that the highest barrier for introverted clients is recording themselves effectively. To prevent robotic delivery and repetitive AI scripts, **CMF Studio** shifts to an **Interview-First** offer. A human guides the performance, and the AI extracts, edits, and routes the content.

To support this, the greenfield CMF Studio requires extracting specific legacy assets that govern human connection, Voice DNA, expression extraction, and CMF editing. All assets will be migrated to the new Python-first Harness, where Pydantic serves as the contract authority, DSPy handles the complex reasoning (like extracting expressions from an interview without losing the human voice), and Pi orchestrates.

---

## 2. Comprehensive Directory & Component Inventory

The legacy repository contains a total of **1686 files**. Below is the exhaustive breakdown of these files by architectural folder structure, explicitly mapped to their future in the CMF Studio Interview-First workflow:

### 2.1 Harness Core & CMF Engine (`src/ccp/harness/cmf`)
* **Total Files:** 123 files (assembler modules, ComfyUI workflows, web app files).
* **Key Files to Keep/Reference for Interview-First:**
  * **ComfyUI JSON templates** (e.g., `Wan 2.2 i2v.json`, `qwen-image-layered-image2image.json`) under `comfyui-workflows` will be copied directly to worker assets to be called by the self-hosted ComfyUI Docker GPU worker adapter.
  * **Core engines** (`audio_engine.py`, `caption_engine.py`, `timeline_generator.py`, `i2v_client.py`) will serve as **reference implementations** for porting their Edit Decision List (EDL) layout, audio ducking mathematics (crucial for separating the interviewer's voice), and caption rendering into the new Python-first CMF engine.
* **To Deprecate:** The old API and Fastify app shell in `web` (replaced by greenfield Python FastAPI).

### 2.2 Cognitive Primitives (`src/ccp/harness/primitives`)
* **Total Files:** 244 YAML primitives (Meaning Plane and Experience Plane).
* **Key Files to Keep:** **All of them.** These are the psychological primitives (such as humor, persuasion, and delivery filters) that allow the human interviewer to structure the interview premise and extract genuine performance. We will migrate them into versioned JSON/YAML assets validated by Pydantic models in the Python core.

### 2.3 SDA & SFL Registries (`sda/` & `sfl/`)
* **Total Files:** 44 files (Ontologies, grammar, compression rules, failure corpus).
* **Key Files to Keep:** **All of them.**
  * `sda/registry_manifest.yaml`: Maps primitives to existential invariants and representation geometries.
  * `sfl/registry_manifest.yaml`: Enforces audio frequency profiles, compression, and scoring models (essential for ensuring the extracted interview audio meets CMF Sonic standards).
  * `sfl/failure_corpus`: Retained to run automated adversarial tests against our new audio composition outputs.

### 2.4 Narrative Intelligence (`src/ccp/harness/intelligence`)
* **Total Files:** 416 files.
* **Key Files to Keep/Reference for Interview-First:**
  * **96 Archetype Prompts** (`✨ Connection Story`, `✨ Transformation Story`, etc.) in `archetype_prompts/core`: These will be deconstructed into DSPy-ready templates for the `ContextPremiseCompiler` and `InterviewAssetContractCompiler`.
  * **139 files across 34 Creative Subsystems (CS-001 to CS-034)** in `subsystems`: We will keep these structured folders and validate their `config.json` and `rules.yaml` specs using the new Pydantic Registry compiler.
  * **Master schemas, research papers, and guides** in `schemas` and `research`: Retained under our reference documentation to construct the Interview deck compiler and scoring gates.

### 2.5 Domain Logic models & Services (`src/ccp/models` & `src/ccp/services`)
* **Total Files:** 34 files.
* **Key Files to Reference:** Python schemas (e.g., `voice_dna_models.py`, `anti_draft_calibrator.py`, `adapter_registry_models.py`, and `receipt_chain.py`) will guide our database schema designs in SQLAlchemy v2.0 and Pydantic v2. These are strictly required to ensure the final edited narrative doesn't sound like a generic AI script by checking against the client's actual speech patterns.

### 2.6 The Architectural Blueprint & Spec Protocols (`docs/architecture/` & `docs/methodology/`)
* **Total Files:** The crown jewels of the CCP system, including all `april_updates`, `spec updates`, and core architecture briefs.
* **Key Files to Keep/Reference:**
  * **ERA3 Spec Writing & Audit Protocols:** `docs/architecture/april_updates/` contains the absolute source of truth for how specs are created (`ERA3_Epic_and_Story_Writing_Protocol.md`, `PROMPT_Spec_Build.md`, `PROMPT_Spec_Audit.md`). These are MANDATORY pre-requisites for how the CMF Studio will orchestrate agents to build software.
  * **CRAL & Visual Research Engines:** `Sovereign_CRAL_Research_Engine_Architecture_Brief.md`, `Sovereign_Visual_Research_Engine_TechSpec_V1.md` define the sovereign boundaries of how the agents conduct visual and context research autonomously.
  * **Cognitive & Identity Architectures:** `Proprietary_Cognitive_Architecture_Manifesto.md`, `identity_engine_architecture.md`, and `Jim_Rohn_AI_Voice_Coach_Communication_Framework.md` dictate how we model user identity beyond generic prompts.
  * **Master System Ledger:** `CCP_MASTER_SYSTEM_LEDGER.md` and `CCP_Technical_Architecture.md` serve as the map of the territory.
  * **CBAR Enforcement:** `docs/architecture/spec updates/CBAR_Constraint_Based_Adversarial_Reasoning_Epics_Stories.md` and `docs/methodology/CBAR_Constraint_Based_Adversarial_Reasoning.md` (from CCF) form the bedrock of our adversarial testing and tech spec constraints.
  * **TTT (Tone & Temperature Tracker):** `docs/ttt.md` is the essential framework for interviewing and extracting specific client states (Level 01 to 09) using transition grammar.

### 2.7 BMAD Workflows & Lab Specifications (`bmad/` & `lab/`)
* **Total Files:** 486 BMAD files and 55 Lab files.
* **Key Files to Keep/Reference:**
  * **Tech Specs Workflow Execution:** `bmad/bmad-bmm-workflows-create-tech-spec.md` and `bmad/bmad-bmm-agents-tech-writer.md` will execute the ERA3 protocols defined above.
  * `lab/Voice_Doctrines_and_First_Principles/Voice_DNA_Framework.md`: Core doctrine for modeling epistemic signatures.
  * `lab/Core_Experience_and_Programs/Conscious_Reactions_Source_of_Truth.md`: Maps out solo, debate, and jury formats.

---

## 3. Migration Ledger (Wave 0)

The migration ledger details the tracking fields for the highest-value legacy modules crucial for the Interview-First offer, including the vital tech spec generation engines.

### `docs/architecture/april_updates/ERA3_Epic_and_Story_Writing_Protocol.md`

- **Legacy Type:** `architecture_protocol`
- **Registry Family / Domain:** `Agentic Architecture & Spec Writing`
- **Canonicality Confidence:** `High`
- **Source Owner:** `CMF Engineering`
- **Runtime Language:** `Markdown`
- **Valuable Mechanics:** The mandatory pre-requisite for all tech specs. Ensures specs are grounded in user stories and Epics rather than abstract system design. This governs how CMF Studio will generate its own specs.
- **Known Defects / Limitations:** Requires strict adherence to the BMAD two-pass pipeline.
- **Migration Target (Python Package):** `ccp_studio.bmad.workflows`
- **Pydantic Contract Target:** `ccp_studio.contracts.bmad.SpecWritingProtocol`
- **DSPy Program Target:** `ccp_studio.dspy_programs.EpicStoryCompiler`
- **TypeScript Leaf Target (if any):** `N/A`
- **Fixture Target:** `tests/fixtures/era3_epic_golden.json`
- **Evaluation Target:** `tests/evals/spec_audit_gate.py`
- **Status:** `pending_migration_design`
- **Reviewer:** `Jean-Pierre`
- **Content Hash (SHA-256):** `deee4e2e`

---

### `bmad/bmad-bmm-workflows-create-tech-spec.md`

- **Legacy Type:** `workflow_document`
- **Registry Family / Domain:** `Agentic Architecture & Spec Writing`
- **Canonicality Confidence:** `High`
- **Source Owner:** `CMF Engineering`
- **Runtime Language:** `Markdown`
- **Valuable Mechanics:** The exact multi-agent workflow for researching, drafting, and auditing technical specifications, including CBAR constraint gates, acting as the foundation for how CMF Studio will write its own specs.
- **Known Defects / Limitations:** Relies on older generation context; needs updating for the Python-first DSPy architecture.
- **Migration Target (Python Package):** `ccp_studio.bmad.workflows`
- **Pydantic Contract Target:** `ccp_studio.contracts.bmad.TechSpecWorkflow`
- **DSPy Program Target:** `ccp_studio.dspy_programs.TechSpecCompiler`
- **TypeScript Leaf Target (if any):** `N/A`
- **Fixture Target:** `tests/fixtures/bmad_tech_spec_workflow.json`
- **Evaluation Target:** `tests/evals/bmad_workflow_completeness.py`
- **Status:** `pending_migration_design`
- **Reviewer:** `Jean-Pierre`
- **Content Hash (SHA-256):** `cb713264`

---

### `src/ccp/harness/intelligence/gates/cbar_scene_builder_gate_pack.runtime.json`

- **Legacy Type:** `cbar_gate_pack`
- **Registry Family / Domain:** `Auditing Constraints`
- **Canonicality Confidence:** `High`
- **Source Owner:** `CMF Intelligence`
- **Runtime Language:** `JSON`
- **Valuable Mechanics:** Defines the 4-part CBAR questions (Tension → Failure Scenario → Resolution Demand → Downstream Proof) that must be resolved before a tech spec or scene is committed.
- **Known Defects / Limitations:** Needs conversion to Pydantic v2 schemas.
- **Migration Target (Python Package):** `ccp_studio.intelligence.gates`
- **Pydantic Contract Target:** `ccp_studio.contracts.gates.CBARGatePack`
- **DSPy Program Target:** `ccp_studio.dspy_programs.CBARAuditor`
- **TypeScript Leaf Target (if any):** `N/A`
- **Fixture Target:** `tests/fixtures/cbar_gate_pack_golden.json`
- **Evaluation Target:** `tests/evals/cbar_audit_integrity.py`
- **Status:** `pending_migration_design`
- **Reviewer:** `Jean-Pierre`
- **Content Hash (SHA-256):** `f1f69ecf`

---

### `docs/ttt.md`

- **Legacy Type:** `methodology_document`
- **Registry Family / Domain:** `Interview Tonal Management`
- **Canonicality Confidence:** `High`
- **Source Owner:** `CMF R&D`
- **Runtime Language:** `Markdown`
- **Valuable Mechanics:** Defines Tonal/Temperature levels (01-09), Transition Grammar, and Identity Anchors used to extract performance from introverted clients during CMF Studio interviews.
- **Known Defects / Limitations:** Theoretical framework; needs mapping to actionable DSPy evaluation prompts.
- **Migration Target (Python Package):** `ccp_studio.intelligence.ttt`
- **Pydantic Contract Target:** `ccp_studio.contracts.ttt.TonalTemperatureProfile`
- **DSPy Program Target:** `ccp_studio.dspy_programs.TTTTransitionEvaluator`
- **TypeScript Leaf Target (if any):** `N/A`
- **Fixture Target:** `tests/fixtures/ttt_transition_grammar.json`
- **Evaluation Target:** `tests/evals/ttt_range_eval.py`
- **Status:** `pending_migration_design`
- **Reviewer:** `Jean-Pierre`
- **Content Hash (SHA-256):** `762995bc`

---

### `src/ccp/harness/cmf/assembler/audio_engine.py`

- **Legacy Type:** `engine_module`
- **Registry Family / Domain:** `Audio Composition`
- **Canonicality Confidence:** `High`
- **Source Owner:** `CMF Core Team`
- **Runtime Language:** `Python`
- **Valuable Mechanics:** Crucial for ducking the interviewer's voice and isolating the client's performance (Demucs separator) to support the Interview-First workflow.
- **Known Defects / Limitations:** Tightly coupled to local shell execution of Demucs.
- **Migration Target (Python Package):** `ccp_studio.harness.cmf.audio`
- **Pydantic Contract Target:** `ccp_studio.contracts.cmf.RenderContract`
- **DSPy Program Target:** `N/A`
- **TypeScript Leaf Target (if any):** `apps/remotion-renderer`
- **Fixture Target:** `tests/fixtures/audio_timeline_edl_golden.json`
- **Evaluation Target:** `tests/evals/audio_ducking_volume_check.py`
- **Status:** `pending_migration_design`
- **Reviewer:** `Jean-Pierre`
- **Content Hash (SHA-256):** `34f4e738`

---

### `src/ccp/services/anti_draft_calibrator.py`

- **Legacy Type:** `service_module`
- **Registry Family / Domain:** `Voice DNA Verification`
- **Canonicality Confidence:** `High`
- **Source Owner:** `CMF Core Team`
- **Runtime Language:** `Python`
- **Valuable Mechanics:** Ensures the final edited narrative doesn't sound like a generic AI script by checking against the client's actual speech patterns.
- **Known Defects / Limitations:** Slow execution times due to synchronous API calls.
- **Migration Target (Python Package):** `ccp_studio.services.calibration`
- **Pydantic Contract Target:** `ccp_studio.contracts.calibration.CalibrationReport`
- **DSPy Program Target:** `ccp_studio.dspy_programs.AntiDraftCalibrationProgram`
- **TypeScript Leaf Target (if any):** `N/A`
- **Fixture Target:** `tests/fixtures/voice_dna_calibration_samples.json`
- **Evaluation Target:** `tests/evals/anti_draft_calibration_test.py`
- **Status:** `pending_migration_design`
- **Reviewer:** `Jean-Pierre`
- **Content Hash (SHA-256):** `b7a00c63`

---
