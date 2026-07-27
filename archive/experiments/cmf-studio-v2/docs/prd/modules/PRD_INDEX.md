---
type: prd-index
project: CMF STUDIO
status: canonical
source_prd: 05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md
last_updated: 2026-06-25
supersedes:
  - CCP modular PRD index copied from reference workspace
legacy_lineage_folder: reference/conscious-rivers/docs/prd/modules
---

# CMF STUDIO PRD Module Index

## Purpose

This index is the canonical router for CMF STUDIO product requirements. The source of truth is the current CMF Studio PRD, modularized into project-native `PRD_CMF_*` files.

The old CCP modules are lineage evidence only:

- `reference/conscious-rivers/docs/prd/modules/PRD_02_CCF_Content_Factory.md`
- `reference/conscious-rivers/docs/prd/modules/PRD_03_CMF_Media_Factory.md`
- `reference/conscious-rivers/docs/prd/modules/PRD_08_Conscious_Primitives.md`

They should be read when migration reasoning, primitive lineage, CCF/CMF orchestration intent, or legacy eval behavior is needed. They are not canonical CMF Studio PRD modules.

## Canonical Module Registry

| Module | File | Covers | Primary Current PRD Sections |
|---|---|---|---|
| PRD-CMF-01 | `PRD_CMF_01_Strategy_Scope_Release_Gates.md` | Product center, full-system release, success, pricing, release blockers | Executive Summary, Success Criteria, Product Scope |
| PRD-CMF-02 | `PRD_CMF_02_Pipeline_Agent_Orchestration.md` | Pipeline stage map, object spine, agent topology, Pi orchestration rules | Canonical Product Pipeline and Agent Orchestration Map |
| PRD-CMF-03 | `PRD_CMF_03_Workspace_Commercial_Consent_Source.md` | Workspace, roles, pricing, consent, source, likeness, voice | FR-CMF-01, FR-CMF-02 |
| PRD-CMF-04 | `PRD_CMF_04_Legacy_Primitives_JIT_Spec_Governance.md` | Legacy migration, primitives, registries, JIT skills, spec governance | Legacy Migration Acceptance Gate, FR-CMF-03 |
| PRD-CMF-05 | `PRD_CMF_05_Brand_Genesis_Context.md` | Brand Genesis, acting library, rig, micro-semiotic anchors, Brand Context Version | FR-CMF-04 |
| PRD-CMF-06 | `PRD_CMF_06_Interview_Expression_Routing.md` | Research, Context Premise, Matrix of Edging, induction, sessions, extraction, routing, Guest Asset Packs | FR-CMF-05, FR-CMF-06 |
| PRD-CMF-07 | `PRD_CMF_07_Editing_Composition_Rendering.md` | Complete Editing Sessions, SceneSpec, Ideogram 4 composition JSON, provider jobs, rendering, assembly | FR-CMF-07, FR-CMF-08 |
| PRD-CMF-08 | `PRD_CMF_08_Evaluation_Review_Publishing_Memory.md` | Evaluation receipts, review workbench, publishing intent, Publer, memory, Neo4j, operations | FR-CMF-09, FR-CMF-10 |
| PRD-CMF-09 | `PRD_CMF_09_Non_Functional_Requirements.md` | Performance, recovery, privacy, scalability, integrations, reproducibility, accessibility, maintainability | Non-Functional Requirements |
| PRD-CMF-10 | `PRD_CMF_10_Agent_Factory_Runtime.md` | Agents, sub-agents, hooks, extensions, skills, JIT skills, intelligence contracts, departments | Agent topology and agent-factory docs |
| PRD-CMF-12 | `PRD_CMF_12_Conscious_Sequencing_Expression_Acquisition.md` | Sequencing registries, Interview Brief V2 procurement, live ingredient coverage, expression inventory, content sequence programs, package sequencing, learning | Conscious Sequencing and Expression Acquisition bundle |
| PRD-CMF-13 | `PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` | Pipeline manifests, stage director skills, tool registry, provider scoring, checkpoints, reference video intake, real-footage retrieval, runtime locking, QA, cost governance | OpenMontage-inspired CMF-native production orchestration adapters |

## Functional Requirement Router

| FR | Canonical Module |
|---|---|
| FR-CMF-01 Workspace, Tenant, Role, and Commercial Governance | PRD-CMF-03 |
| FR-CMF-02 Consent, Source, Likeness, and Voice Governance | PRD-CMF-03 |
| FR-CMF-03 Legacy Migration, JIT Skill Intelligence, and Spec Governance | PRD-CMF-04 |
| FR-CMF-04 Brand Genesis and Brand Context Versioning | PRD-CMF-05 |
| FR-CMF-05 Research, Interview Intelligence, and Narrative State Induction | PRD-CMF-06 |
| FR-CMF-06 Complete Expression Sessions, Extraction, Routing, and Guest Asset Packs | PRD-CMF-06 |
| FR-CMF-07 Complete Editing Sessions, Scene Reproducibility, and Composition Control | PRD-CMF-07 |
| FR-CMF-08 Provider, Renderer, GPU Worker, and Asset Assembly Operations | PRD-CMF-07 |
| FR-CMF-09 Evaluation, Review, Approval, and Publishing Intent | PRD-CMF-08 |
| FR-CMF-10 Memory, Neo4j Projection, Operations, and Recovery | PRD-CMF-08 |
| FR-CMF-12.01 Sequencing Contract Kernel | PRD-CMF-12 |
| FR-CMF-12.02 Interview Brief V2 Procurement | PRD-CMF-12 |
| FR-CMF-12.03 Live Ingredient Coverage | PRD-CMF-12 |
| FR-CMF-12.04 Expression Ingredient Inventory | PRD-CMF-12 |
| FR-CMF-12.05 Content Sequence Program Compiler | PRD-CMF-12 |
| FR-CMF-12.06 Sequence Eval, Package Sequencing, and Learning | PRD-CMF-12 |
| FR-CMF-13.01 OpenMontage Reference Adapter Governance | PRD-CMF-13 |
| FR-CMF-13.02 CMF Production Pipeline Manifest Registry | PRD-CMF-13 |
| FR-CMF-13.03 Stage Director Skill Contract Binding | PRD-CMF-13 |
| FR-CMF-13.04 Capability Tool Registry and Provider Menu | PRD-CMF-13 |
| FR-CMF-13.05 Scored Provider Selector and Capability Router | PRD-CMF-13 |
| FR-CMF-13.06 Brand-Scoped Project Workspace and Checkpoint Runtime | PRD-CMF-13 |
| FR-CMF-13.07 Reference Video and Existing Footage Intake Adapter | PRD-CMF-13 |
| FR-CMF-13.08 Real-Footage Corpus and Source Media Retrieval Adapter | PRD-CMF-13 |
| FR-CMF-13.09 Render Runtime Selection and Locking | PRD-CMF-13 |
| FR-CMF-13.10 Pre-Compose Delivery Promise and Slideshow Risk Gate | PRD-CMF-13 |
| FR-CMF-13.11 Post-Render Self-Review and Media QA Gate | PRD-CMF-13 |
| FR-CMF-13.12 Budget, Cost, and Resource Governance | PRD-CMF-13 |
| FR-CMF-13.13 Canonical Stage Artifacts, Human Approval, and Reviewer Protocol | PRD-CMF-13 |

## Usage Rule

Agents, architects, spec writers, and implementers should load:

1. the current main PRD;
2. this index;
3. the relevant `PRD_CMF_*` module;
4. the relevant story, tech spec, eval, registry, or legacy lineage file.

Old CCP PRDs may inform migration decisions, but new CMF requirements must be written against the `PRD_CMF_*` module family.

## Boundary Rule

Do not reintroduce old CCP module names as canonical requirements. If a legacy PRD concept remains valuable, transform it into one of:

- CMF product requirement;
- Pydantic contract;
- registry entry;
- DSPy program;
- JIT Skill Compiler;
- fixture;
- eval target;
- worker asset;
- reference-only lineage note.

