---
title: "CMF STUDIO Architecture MCDA Evaluation"
evaluated_artifact: "docs/architecture.md"
source_of_truth:
  - "THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md"
  - "THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md"
supporting_artifacts:
  - "docs/migration/legacy-inventory.md"
  - "docs/cmf-studio-pipeline-map.md"
  - "THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md"
  - "lab/Harness_and_Orchestration_Architecture/ccp_biological_orchestration_model_v_1.md"
  - "lab/Specs_and_Architecture_Documentation/JIT_Skill_Compiler_Architecture.docx.md"
  - "docs/architecture/FR39_Core_Orchestration_11_Pi_Extensions.md"
  - "docs/architecture/april_updates/ERA3_Epic_and_Story_Writing_Protocol.md"
  - "docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md"
  - "docs/architecture/april_updates/PROMPT_Spec_Build.md"
  - "docs/architecture/april_updates/PROMPT_Spec_Audit.md"
evaluation_date: "2026-06-21"
criteria_count: 12
pre_repair_weighted_score_10: 8.74
pre_repair_weighted_score_100: 87.4
post_repair_weighted_score_10: 9.36
post_repair_weighted_score_100: 93.6
status: "architecture-ready-after-repair"
---

# CMF STUDIO Architecture MCDA Evaluation

## Evaluation Standard

This MCDA evaluates whether `docs/architecture.md` can govern implementation, epics, stories, and tech specs after the PRD repair. The repaired PRD is the source of truth for product scope, pipeline authority, FR modules, commercial boundaries, and valid content formats. The Product Brief and Legacy Inventory supply upstream strategy and migration obligations. The pipeline map supplies orchestration readability.

The architecture is judged against RSCS-style signal quality: saturated source grounding, retention of useful collision, compression without loss of critical structure, and reality contact through enforceable contracts, workflows, receipts, tests, and boundaries.

## Scoring Summary

| Criterion | Weight | Pre-Repair Score | Weighted | Post-Repair Score | Weighted |
|---|---:|---:|---:|---:|---:|
| 1. Alignment with repaired PRD and Product Brief | 9 | 8.8 | 79.2 | 9.5 | 85.5 |
| 2. Python/Pydantic/DSPy/Pi runtime integrity | 10 | 9.5 | 95.0 | 9.6 | 96.0 |
| 3. Canonical pipeline, stage ownership, and object spine | 12 | 7.1 | 85.2 | 9.4 | 112.8 |
| 4. Agent orchestration and autonomy boundaries | 9 | 8.0 | 72.0 | 9.3 | 83.7 |
| 5. Legacy intentional orchestration fidelity | 8 | 9.0 | 72.0 | 9.3 | 74.4 |
| 6. JIT Skill compiler and spec compiler architecture | 8 | 8.2 | 65.6 | 9.3 | 74.4 |
| 7. CRAL, Context Premise, Emotional DNA, Voice DNA coverage | 7 | 9.2 | 64.4 | 9.3 | 65.1 |
| 8. Scene reproducibility, Ideogram 4, and CMF asset engines | 8 | 9.3 | 74.4 | 9.4 | 75.2 |
| 9. Provider, GPU worker, and renderer boundaries | 8 | 9.4 | 75.2 | 9.4 | 75.2 |
| 10. Data, state, memory, Neo4j, and recovery architecture | 8 | 9.2 | 73.6 | 9.3 | 74.4 |
| 11. Security, consent, approval, and publishing safety | 6 | 9.1 | 54.6 | 9.2 | 55.2 |
| 12. Downstream epic/story/tech-spec readiness | 7 | 7.8 | 54.6 | 9.2 | 64.4 |
| **Total** | **100** |  | **874.0** |  | **936.3** |

**Pre-repair verdict:** strong architecture with correct runtime doctrine, provider boundaries, legacy migration framing, and FR coverage. The main issue was not missing content; it was missing an explicit architecture-level stage execution contract mirroring the repaired PRD pipeline. That gap could let downstream agents build by service area instead of by production stage, object handoff, validation contract, and receipt.

**Post-repair verdict:** architecture-ready. The architecture now carries pipeline-stage execution rules, stage-to-workflow/component mapping, required orchestration objects, and a Python/DSPy/Pi-compatible tech-spec compiler workflow.

## Criterion Findings

### 1. Alignment With Repaired PRD And Product Brief

The architecture already aligns on full-system scope, pricing guardrails, valid formats, Python-first runtime, Neo4j projection, ComfyUI worker, and no direct legacy runtime import. The repaired PRD added a canonical product pipeline that was not yet represented as an architecture control surface.

Repair action: added a pipeline execution architecture section and updated handoff rules so architecture now inherits the PRD pipeline authority.

### 2. Python/Pydantic/DSPy/Pi Runtime Integrity

The architecture is strong here. Python owns the harness, Pydantic owns contracts, DSPy owns structured reasoning, Pi orchestrates through approved tools and typed commands, and TypeScript remains a leaf runtime.

Residual watch: package version notes should be re-verified during implementation lockfile creation, because external version facts are time-sensitive.

### 3. Canonical Pipeline, Stage Ownership, And Object Spine

This was the largest pre-repair weakness. The architecture had a logical topology and domain chain, but did not yet provide an execution matrix for the 15 PRD stages, their workflows, entry/exit objects, and proof obligations.

Repair action: inserted `4.5 Canonical Pipeline Execution Architecture`, including stage-to-workflow mapping and required architectural proof for every stage.

### 4. Agent Orchestration And Autonomy Boundaries

The architecture had good Pi and Command Bus constraints, but needed the explicit orchestration objects from the pipeline map: `OrchestrationRun`, `StageExecutionPlan`, `ValidationContract`, `AgentHandoffPacket`, `SkillInvocationRecord`, `FailureReceipt`, `FrictionReceipt`, and `HumanHandoffRequest`.

Repair action: added AD-014 and dedicated object requirements in product module, data, workflow, testing, and project-structure sections.

### 5. Legacy Intentional Orchestration Fidelity

The architecture already treats legacy CCF/CMF modules as intentional orchestration modules with organism layer, upstream packets, downstream artifacts, gates, and proof obligations. This is a strong point.

Residual watch: migration stories must preserve this depth instead of merely copying file names into a ledger.

### 6. JIT Skill Compiler And Spec Compiler Architecture

The architecture includes JIT Skills, but the tech-spec section was still too generic. The Legacy Inventory says ERA3/BMad workflows are mandatory, but must be updated for Python-first DSPy architecture. The architecture needed a clearer internal spec compiler shape.

Repair action: expanded Tech Spec rules into a Python/DSPy/Pi-compatible spec compiler workflow with `SpecWritingProtocol`, `TechSpecWorkflow`, `TechSpecCompiler`, CBAR gates, files-read receipts, pipeline-stage mapping, contracts, commands, workflows, tests, and legacy migration context.

### 7. CRAL, Context Premise, Emotional DNA, And Voice DNA Coverage

Coverage is strong in research/interview architecture. CRAL/SCRE, Context Premise, Audience Deep Trigger Map, Emotional DNA, Voice DNA, Matrix of Edging, and TTT are modeled as contracts and DSPy programs.

Residual watch: downstream stories must distinguish audience-side Context Premise from guest/coach Emotional DNA and Voice DNA.

### 8. Scene Reproducibility, Ideogram 4, And CMF Asset Engines

Architecture strongly preserves `CompositionJob`, SceneSpec, provider receipts, render manifests, CMF scene containers/components/subsystems, asset roles, SVRE/Aurore, and deterministic renderer routes.

Residual watch: tech specs must define exact Pydantic fields for scene reproducibility, not only name the objects.

### 9. Provider, GPU Worker, And Renderer Boundaries

Architecture correctly uses GPT Image 2, Flux 2 Klein 9b, Qwen-Image-Layered, SAM3, LavaSR, MOSS-TTS, Remotion, Motion Canvas, and self-hosted ComfyUI Docker on AWS/Google Cloud GPU. RunningHub is excluded.

Residual watch: cost, retry, checkpoint, and shutdown tests must be included in provider specs.

### 10. Data, State, Memory, Neo4j, And Recovery Architecture

Architecture correctly puts PostgreSQL/events/contracts/object storage/receipts as canonical state and Neo4j as rebuildable projection. Recovery and projection rebuild workflows exist.

Repair action: added orchestration table families and projection-aware proof obligations so pipeline-stage state can be audited independently of Neo4j.

### 11. Security, Consent, Approval, And Publishing Safety

Security and consent rules are strong. The architecture blocks provider processing and publishing without consent and approval. Publer remains an adapter, not authority.

Residual watch: implementation must model consent as versioned state gates, not only security middleware.

### 12. Downstream Epic/Story/Tech-Spec Readiness

Pre-repair architecture was readable but could still produce tech specs by package or API group rather than by product stage and proof obligation.

Repair action: updated handoff rules so every epic, story, and tech spec must cite FR module, PRD pipeline stage, entry/exit object, command, workflow, receipt, tests, and legacy sources where applicable.

## Repair Backlog

| Priority | Issue | Action | Status |
|---:|---|---|---|
| 1 | PRD pipeline not mirrored as architecture execution contract | Add canonical pipeline execution architecture section | Completed |
| 2 | Orchestration objects not explicit enough | Add AD-014 and required orchestration objects/contracts/tables/workflows/tests | Completed |
| 3 | Tech-spec rules still too generic for CMF | Expand into Python/DSPy/Pi spec compiler workflow using legacy BMAD/ERA3 mechanics | Completed |
| 4 | Downstream agents could decompose by services instead of product stages | Add stage-to-workflow/component mapping and handoff requirements | Completed |
| 5 | Project tree missing orchestration/spec-compiler locations | Add contract, workflow, DSPy, and test locations | Completed |

## Downstream Mandates

Epics, stories, and tech specs must now obey both the PRD pipeline authority and the architecture execution contract:

1. Name the FR-CMF module.
2. Name the canonical pipeline stage.
3. Name the entry object and exit object.
4. Name the command, workflow, DSPy program, deterministic service, provider adapter, or renderer that owns execution.
5. Define the `ValidationContract` or equivalent precondition gate.
6. Define the receipt proving completion, failure, block, human handoff, or quarantine.
7. Cite legacy sources and migration targets when legacy intelligence is used.
8. Include CBAR failure pressure and test evidence.

This makes BMAD the planning workflow shell while the implemented architecture remains Python/Pydantic/DSPy/Pi and CMF-specific.
