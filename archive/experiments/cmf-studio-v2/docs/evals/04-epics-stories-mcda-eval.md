---
title: "CMF STUDIO Epics and Stories MCDA Evaluation"
evaluated_artifact: "docs/epics.md"
source_of_truth:
  - "THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md"
  - "docs/architecture.md"
supporting_artifacts:
  - "THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md"
  - "docs/migration/legacy-inventory.md"
  - "docs/cmf-studio-pipeline-map.md"
  - "docs/evals/02-prd-mcda-eval.md"
  - "docs/evals/03-architecture-mcda-eval.md"
evaluation_date: "2026-06-21"
criteria_count: 12
pre_repair_weighted_score_10: 8.51
pre_repair_weighted_score_100: 85.1
post_repair_weighted_score_10: 9.29
post_repair_weighted_score_100: 92.9
status: "story-ready-after-repair"
---

# CMF STUDIO Epics and Stories MCDA Evaluation

## Evaluation Standard

This MCDA evaluates whether `docs/epics.md` can generate implementation story files and downstream tech specs without losing CMF's repaired product architecture. The repaired PRD requires every epic and story to map to a canonical pipeline stage, entry object, exit object, allowed actor/service, validation contract, and receipt. The repaired architecture adds AD-014, `OrchestrationRun`, `StageExecutionPlan`, `ValidationContract`, `AgentHandoffPacket`, `SkillInvocationRecord`, `FailureReceipt`, `FrictionReceipt`, `HumanHandoffRequest`, and `TechSpecCompilerWorkflow`.

The evaluation applies the RSCS quality filter: source saturation, collision retention, dense compression, and reality contact through executable contracts, tests, receipts, and failure examples.

## Scoring Summary

| Criterion | Weight | Pre-Repair Score | Weighted | Post-Repair Score | Weighted |
|---|---:|---:|---:|---:|---:|
| 1. FR coverage completeness | 10 | 9.4 | 94.0 | 9.5 | 95.0 |
| 2. Value-oriented epic structure | 8 | 9.1 | 72.8 | 9.2 | 73.6 |
| 3. Story implementation readiness | 9 | 8.7 | 78.3 | 9.1 | 81.9 |
| 4. PRD pipeline traceability | 12 | 6.8 | 81.6 | 9.4 | 112.8 |
| 5. Architecture execution contract and orchestration objects | 10 | 6.9 | 69.0 | 9.3 | 93.0 |
| 6. Legacy intentional orchestration and JIT skill fidelity | 9 | 9.2 | 82.8 | 9.3 | 83.7 |
| 7. CRAL, Context Premise, Emotional DNA, and Voice DNA coverage | 7 | 9.1 | 63.7 | 9.2 | 64.4 |
| 8. Scene reproducibility, Ideogram 4, SVRE/Aurore, and asset engines | 8 | 9.3 | 74.4 | 9.4 | 75.2 |
| 9. Provider, Neo4j, commercial, and content-format guardrails | 8 | 9.2 | 73.6 | 9.3 | 74.4 |
| 10. Acceptance criteria, CBAR pressure, and failure examples | 7 | 8.9 | 62.3 | 9.1 | 63.7 |
| 11. Downstream tech-spec readiness | 7 | 7.7 | 53.9 | 9.2 | 64.4 |
| 12. Full-system, no-MVP scope discipline | 5 | 9.0 | 45.0 | 9.3 | 46.5 |
| **Total** | **100** |  | **851.4** |  | **928.6** |

**Pre-repair verdict:** strong FR and legacy coverage, but not yet safe enough for story-file and tech-spec generation after the PRD/architecture repairs. The gap was structural: stories carried technical notes and prerequisites, but did not yet carry explicit pipeline-stage traces, entry/exit object traces, validation contracts, receipts, or orchestration-object coverage.

**Post-repair verdict:** story-ready. The epics now include an epic-to-pipeline trace, story-to-pipeline trace matrix, orchestration story, repaired spec workflow story, and updated handoff rules.

## Criterion Findings

### 1. FR Coverage Completeness

The epics already cover all 10 FR-CMF modules and all 77 PRD sub-requirements. This is one of the artifact's strongest areas.

Repair action: updated FR coverage for the new orchestration story while preserving the 77-subrequirement map.

### 2. Value-Oriented Epic Structure

The ten epics remain value-oriented: workspace governance, consent, migration intelligence, Brand Genesis, interview intelligence, expression sessions, editing sessions, rendering, review/publishing, and memory/recovery. The foundation epic is justified because CMF cannot safely deliver value without command, tenant, receipt, and state discipline.

### 3. Story Implementation Readiness

The stories already include user story phrasing, BDD criteria, technical notes, legacy/primitive mapping, and prerequisites. They are more implementation-ready than typical planning stories.

Repair action: added story-level pipeline traceability and orchestration records so each story can become a dev-ready story file without guessing its stage lane.

### 4. PRD Pipeline Traceability

This was the largest pre-repair weakness. The repaired PRD requires every story to map to a canonical pipeline stage, entry object, exit object, validation contract, and receipt. The previous epics were organized by FR module, but not yet by pipeline lane.

Repair action: added `3.1 Epic-to-Pipeline Trace` and `3.2 Story-to-Pipeline Trace Matrix`.

### 5. Architecture Execution Contract And Orchestration Objects

The previous artifact referenced Pi and Command Bus, but did not yet include AD-014's required orchestration objects as story scope.

Repair action: added Story 1.6 for `OrchestrationRunWorkflow`, `StageExecutionPlan`, `ValidationContract`, `AgentHandoffPacket`, `SkillInvocationRecord`, `FailureReceipt`, `FrictionReceipt`, and `HumanHandoffRequest`.

### 6. Legacy Intentional Orchestration And JIT Skill Fidelity

The existing epics strongly represent legacy migration, JIT Skills, anti-draft calibration, intentional orchestration, organism layers, emitted packets, downstream consumers, and proof obligations.

Residual watch: individual generated story files must retain this depth and not collapse "legacy mapping" into a file-name citation only.

### 7. CRAL, Context Premise, Emotional DNA, And Voice DNA Coverage

Epic 5 and Story 5.6 represent this well, with CRAL/SCRE, Context Premise, Audience Deep Trigger Map, Emotional DNA, Voice DNA, Matrix of Edging, and root-down induction. The artifact correctly rejects persona summaries and unsupported psychological certainty.

### 8. Scene Reproducibility, Ideogram 4, SVRE/Aurore, And Asset Engines

Epics 7 and 8 are strong: `CompositionJob`, SceneSpec, scene containers/components/subsystems, asset rolls, SVRE/Aurore, ComfyUI worker, Remotion/Motion Canvas, audio/caption/timeline manifests, and provider receipts are represented.

### 9. Provider, Neo4j, Commercial, And Content-Format Guardrails

The stories use GPT Image 2, Flux 2 Klein 9b, self-hosted ComfyUI Docker GPU worker, Neo4j as rebuildable projection, `$29/week` and `$99/month`, and valid registry-based content formats. No newsletters or MVP framing are introduced.

### 10. Acceptance Criteria, CBAR Pressure, And Failure Examples

The artifact includes strong failure examples for consent, brand scope, route support, provider receipts, projection lag, approval blockers, and recovery. The repair added orchestration-stage mismatch, missing validation contract, and missing spec trace as additional failure categories.

### 11. Downstream Tech-Spec Readiness

The previous Story 3.5 was directionally correct but too generic after architecture repair. It did not yet require `FilesReadReceipt`, `RequirementTrace`, `PipelineStageTrace`, `SpecAuditReceipt`, or `TechSpecCompilerWorkflow`.

Repair action: upgraded Story 3.5 and handoff rules to align with the architecture's Python/DSPy/Pi-compatible tech-spec workflow.

### 12. Full-System, No-MVP Scope Discipline

The artifact preserves full-system scope and dependency ordering without using deferral buckets. It does not introduce MVP, newsletters, extra pricing tiers, or hidden phases.

## Repair Backlog

| Priority | Issue | Action | Status |
|---:|---|---|---|
| 1 | Story set lacked explicit PRD pipeline-stage traceability | Add epic-to-pipeline and story-to-pipeline trace matrices | Completed |
| 2 | AD-014 orchestration objects not covered by a story | Add Story 1.6 for pipeline execution and orchestration records | Completed |
| 3 | Tech-spec story did not reflect repaired architecture workflow | Upgrade Story 3.5 with `TechSpecCompilerWorkflow`, files-read, FR trace, pipeline trace, CBAR, and audit receipt | Completed |
| 4 | Handoff rules did not require validation contracts and receipts | Update handoff to story files and tech specs | Completed |
| 5 | Architecture integration table did not include pipeline execution contract | Add coverage for AD-014, orchestration objects, and TechSpecCompilerWorkflow | Completed |

## Downstream Mandates

Generated story files must inherit:

1. FR-CMF IDs.
2. Canonical pipeline stage.
3. Entry object and exit object.
4. Allowed actor, command, service, workflow, DSPy program, provider adapter, or renderer.
5. `ValidationContract` or equivalent stage precondition.
6. Required receipt.
7. Legacy source and migration target where relevant.
8. CBAR failure pressure and tests.

Generated tech specs must then use `TechSpecCompilerWorkflow`, not a generic backend template.
