---
title: "CMF STUDIO PRD MCDA Evaluation"
evaluated_artifact: "THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md"
source_of_truth: "THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md"
supporting_artifacts:
  - "docs/migration/legacy-inventory.md"
  - "docs/cmf-studio-pipeline-map.md"
  - "THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md"
  - "THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md"
  - "THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md"
  - "THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md"
  - "THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md"
  - "lab/Harness_and_Orchestration_Architecture/ccp_biological_orchestration_model_v_1.md"
  - "lab/Specs_and_Architecture_Documentation/JIT_Skill_Compiler_Architecture.docx.md"
evaluation_date: "2026-06-21"
criteria_count: 12
pre_repair_weighted_score_10: 8.57
pre_repair_weighted_score_100: 85.7
post_repair_weighted_score_10: 9.31
post_repair_weighted_score_100: 93.1
status: "spec-ready-after-repair"
---

# CMF STUDIO PRD MCDA Evaluation

## Evaluation Standard

This MCDA evaluates whether the PRD can safely guide architecture, epics, stories, and tech specs for the full CMF STUDIO system. The repaired Product Brief is the authority. The Legacy Inventory is mandatory context, especially where legacy modules carry intentional orchestration rather than isolated features. The pipeline map is used as a readability and agent-handoff reference.

The scoring applies the RSCS signal-distillation filter: saturation before compression, collision over smoothing, dense signal over shallow coverage, and reality contact through documented source constraints.

## Scoring Summary

| Criterion | Weight | Pre-Repair Score | Weighted | Post-Repair Score | Weighted |
|---|---:|---:|---:|---:|---:|
| 1. Alignment with repaired Product Brief | 9 | 8.5 | 76.5 | 9.4 | 84.6 |
| 2. Functional requirement completeness and granularity | 11 | 9.4 | 103.4 | 9.5 | 104.5 |
| 3. Legacy inventory and intentional orchestration fidelity | 9 | 8.8 | 79.2 | 9.4 | 84.6 |
| 4. Pipeline clarity, sub-workflows, agents, and handoffs | 12 | 6.7 | 80.4 | 9.4 | 112.8 |
| 5. Dual extraction and Narrative State Induction clarity | 8 | 9.2 | 73.6 | 9.3 | 74.4 |
| 6. CRAL, Context Premise, Emotional DNA, and Voice DNA coverage | 8 | 8.9 | 71.2 | 9.1 | 72.8 |
| 7. Scene reproducibility, Ideogram 4, and CMF asset engines | 9 | 9.2 | 82.8 | 9.3 | 83.7 |
| 8. JIT Skill Compiler, anti-draft, and contrastive extraction coverage | 8 | 8.8 | 70.4 | 9.2 | 73.6 |
| 9. Provider, GPU worker, renderer, and asset assembly boundaries | 7 | 9.3 | 65.1 | 9.3 | 65.1 |
| 10. Commercial, content-format, and full-system scope governance | 7 | 7.7 | 53.9 | 9.3 | 65.1 |
| 11. Data, state, memory, Neo4j, and recovery boundaries | 6 | 9.0 | 54.0 | 9.1 | 54.6 |
| 12. Downstream architecture, epic, story, and tech-spec readiness | 6 | 7.8 | 46.8 | 9.2 | 55.2 |
| **Total** | **100** |  | **857.3** |  | **931.0** |

**Pre-repair verdict:** strong content density, but not yet clean enough for downstream autonomous agent work because the end-to-end pipeline was not visible as a readable spine and residual wave/minimum-release language conflicted with the user's full-system rule.

**Post-repair verdict:** spec-ready. The PRD now exposes the canonical pipeline, stage map, agent topology, object spine, Pi orchestration rules, and full-system build-gate language needed for architecture, epics, stories, and tech specs.

## Criterion Findings

### 1. Alignment With Repaired Product Brief

The PRD already matched the repaired Product Brief on interview-first positioning, Python/Pydantic/DSPy/Pi runtime, self-hosted ComfyUI, GPT Image 2, Flux 2 Klein 9b, Neo4j as projection, Publer publishing, and no newsletters. The gap was that the Product Brief had been repaired with a canonical pipeline section while the PRD still presented the pipeline mostly through prose, journeys, and FR modules.

Repair action: inserted a canonical PRD pipeline and agent orchestration map aligned to the repaired Product Brief and `docs/cmf-studio-pipeline-map.md`.

### 2. Functional Requirement Completeness And Granularity

The PRD is strong here. It contains ten FR modules with 77 detailed sub-requirements, active intelligence sources, acceptance criteria seeds, anti-pattern prevention, and downstream architecture constraints. This follows the older CCP PRD module style better than a normal BMad PRD.

Residual watch: downstream stories must not flatten these FR modules into generic SaaS tickets.

### 3. Legacy Inventory And Intentional Orchestration Fidelity

The PRD references the Legacy Inventory and preserves major families: CMF engine references, cognitive primitives, SDA/SFL registries, archetype prompts, creative subsystems, Voice DNA, CBAR, ERA3/BMad, TTT, ComfyUI templates, JIT Skill compilers, and spec governance. It also explicitly says legacy modules must preserve why they were built.

Repair action: strengthened the PRD with a pipeline section that treats legacy modules as orchestration-bearing modules whose ordering, gates, emitted packets, and proof obligations matter.

### 4. Pipeline Clarity, Sub-Workflows, Agents, And Handoffs

This was the largest pre-repair weakness. The PRD had the full chain in several places, but it did not give agents a single readable map of stages, handoffs, product objects, and autonomy boundaries. Autonomous agents still need a shared operating map; otherwise they may optimize local tasks while breaking source lineage, consent, routeability, or scene reproducibility.

Repair action: added a canonical stage map from Build Gate 0 legacy migration through memory and Neo4j projection, plus team topology, object spine, and Pi harness rules.

### 5. Dual Extraction And Narrative State Induction Clarity

The PRD clearly distinguishes extraction from the guest through Narrative State Induction and extraction from transcript/source artifacts through Expression Moment extraction. FR-CMF-05 and FR-CMF-06 are strong and grounded in V9/V9.1.

Residual watch: tech specs must keep "expression state" separate from "content archetype" and "asset derivative."

### 6. CRAL, Context Premise, Emotional DNA, And Voice DNA Coverage

Coverage is present and product-specific. The PRD includes CRAL/SCRE, Context Premise, Audience Deep Trigger Map, Emotional DNA, Voice DNA, Matrix of Edging, and root-down induction. It correctly rejects persona summaries and tone imitation.

Repair action: connected these systems to the explicit pipeline stage for research, context engineering, and interview intelligence so they are not buried as features.

### 7. Scene Reproducibility, Ideogram 4, And CMF Asset Engines

The PRD is strong on Complete Editing Sessions, `CompositionJob`, Ideogram as Composition Director, legacy beat-fingerprint/manifest lineage, SceneSpec, RenderContract, LayerManifest, AnimationPlan, provider metadata, and final text rendered outside Ideogram.

Residual watch: architecture must define the exact contract boundaries for SceneSpec, CompositionJob, RenderContract, LayerManifest, AnimationPlan, ProviderJobReceipt, and EvaluationReceipt.

### 8. JIT Skill Compiler, Anti-Draft, And Contrastive Extraction Coverage

The PRD now treats JIT skill modules as a moat rather than prompt snippets. It includes saturation context, anti-genericity checks, contrastive prompting, critic/synthesis logic, Voice DNA, CRAL routing, fingerprint archives, and evaluation receipts.

Repair action: linked JIT compilers into the pipeline as a cross-cutting compilation role used by induction, extraction, routing, drafting, evaluation, and learning.

### 9. Provider, GPU Worker, Renderer, And Asset Assembly Boundaries

The PRD correctly states that ComfyUI is a self-hosted Docker GPU worker on AWS or Google Cloud with 24GB or 32GB VRAM, not RunningHub. It names GPT Image 2 and Flux 2 Klein 9b correctly, and places providers behind contracts and receipts.

Residual watch: tech specs must prevent provider adapters from mutating canonical state or hiding retries/costs.

### 10. Commercial, Content-Format, And Full-System Scope Governance

The PRD correctly includes only `$29/week` trial Guest Asset Packs and `$99/month` Monthly Asset Engine, and explicitly excludes newsletters. The pre-repair issue was residual "9-wave," "Wave 0," and "Minimum Releasable Full System" language, which could be misread as an MVP or phased deferral model.

Repair action: replaced residual wave/minimum language with dependency-ordered full-system build gates and Full-System Release Candidate terminology.

### 11. Data, State, Memory, Neo4j, And Recovery Boundaries

The PRD clearly states PostgreSQL/canonical events as authoritative, memory as evidence-backed and reversible, and Neo4j as a rebuildable relationship projection. It also includes provider recovery, queue visibility, checkpointing, idempotency, and operational readiness checks.

Residual watch: architecture should specify projection lag behavior and rebuild tests early.

### 12. Downstream Architecture, Epic, Story, And Tech-Spec Readiness

The PRD contains downstream architecture constraints inside every FR module, but the pre-repair version lacked a single pipeline spine that epics and stories could map against. That created risk that stories would be organized by UI or service names instead of production stages and proof obligations.

Repair action: added the canonical pipeline section and governance rule requiring FRs, epics, stories, architecture, and tech specs to map back to pipeline stages, product objects, and proof receipts.

## Repair Backlog

| Priority | Issue | Action | Status |
|---:|---|---|---|
| 1 | Pipeline clarity not centralized in PRD | Add canonical product pipeline, stage map, agent topology, object spine, and Pi autonomy rules | Completed |
| 2 | Residual wave/phase/minimum-release wording | Replace with Build Gate and Full-System Release Candidate language | Completed |
| 3 | Agent autonomy could be misread as replacing pipeline discipline | Add rule: agents can act autonomously only inside typed stage lanes and cannot reorder consent, source, routing, approval, or publishing gates | Completed |
| 4 | Product Brief repair not fully reflected in PRD | Align PRD to repaired Product Brief canonical pipeline and commercial/scope language | Completed |
| 5 | Downstream story/spec traceability risk | Add governance language requiring mapping from FRs to pipeline stages, objects, receipts, and source docs | Completed |

## Downstream Mandates

The next architecture and epic/story repairs must use the repaired PRD as the governing artifact. Every downstream module should answer:

1. Which canonical pipeline stage owns this behavior?
2. Which product object enters the stage and which object exits?
3. Which agent, sub-agent, JIT skill, DSPy program, deterministic service, provider adapter, or durable workflow is allowed to act?
4. Which validation contract must exist before execution?
5. Which receipt proves the stage completed or failed honestly?
6. Which human approval, consent, lineage, or publishing gate can block the action?

This is the practical meaning of "agent team autonomy" for CMF STUDIO: agents may operate inside well-specified lanes, but the pipeline defines the lanes, handoffs, proof obligations, and recovery semantics.
