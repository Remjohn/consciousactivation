---
title: "CMF Studio 9-Step Execution Plan"
status: "draft-canonical"
created_at: "2026-06-22"
owner: "Codex / PM-Architecture Execution"
requires_legacy_inventory: true
source_files:
  - "docs/migration/legacy-inventory.md"
  - "THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md"
  - "THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md"
  - "docs/prd/modules/PRD_INDEX.md"
  - "docs/prd/modules/PRD_CMF_01_Strategy_Scope_Release_Gates.md"
  - "docs/prd/modules/PRD_CMF_02_Pipeline_Agent_Orchestration.md"
  - "docs/prd/modules/PRD_CMF_03_Workspace_Commercial_Consent_Source.md"
  - "docs/prd/modules/PRD_CMF_04_Legacy_Primitives_JIT_Spec_Governance.md"
  - "docs/prd/modules/PRD_CMF_05_Brand_Genesis_Context.md"
  - "docs/prd/modules/PRD_CMF_06_Interview_Expression_Routing.md"
  - "docs/prd/modules/PRD_CMF_07_Editing_Composition_Rendering.md"
  - "docs/prd/modules/PRD_CMF_08_Evaluation_Review_Publishing_Memory.md"
  - "docs/prd/modules/PRD_CMF_09_Non_Functional_Requirements.md"
  - "docs/prd/modules/PRD_CMF_10_Agent_Factory_Runtime.md"
  - "reference/conscious-rivers/docs/prd/modules/PRD_02_CCF_Content_Factory.md"
  - "reference/conscious-rivers/docs/prd/modules/PRD_08_Conscious_Primitives.md"
  - "docs/architecture/Sovereign_CRAL_Research_Engine_TechSpec_V1.md"
  - "docs/architecture/Sovereign_Visual_Research_Engine_TechSpec_V1.md"
  - "docs/cmf-studio-pipeline-map.md"
  - "docs/cmf-studio-agent-factory-architecture.md"
  - "docs/cmf-studio-intelligence-operating-model.md"
---

# CMF Studio 9-Step Execution Plan

## 1. Operating Decision

CMF Studio execution starts from the Factory, not from a flat agent list. The pipeline, primitives, research engines, registries, JIT compilers, receipts, and review surfaces define what the agents are allowed to do.

The core production chain is:

```text
SCRE / CRAL Sovereign Signal Discovery
-> CRALFindingRegistry and ResearchSnapshot
-> Context Premise, Audience Reality, Audience Deep Trigger Map
-> Matrix of Edging
-> JIT Skill Compiler
-> Expression Extraction
-> Route Candidate
-> Eval target selection
-> Eval run command
-> EvaluationReceipt
-> approval blocker
-> Review Workbench read model
```

The parallel visual branch is:

```text
SceneSpec / CompositionJob / AssetResearchQuery
-> SVRE / Aurore
-> VisualCandidate and AssetResearchManifest
-> Provider job
-> Render output
-> EvaluationReceipt
-> Review Workbench
```

Primitives are the production quality standard. Evaluations must not only score generic dimensions such as style or platform fit. They must validate whether the intended primitive candidates, primitive coalitions, edge products, anti-centroid pressure, source evidence, and route obligations actually survived into the artifact under review.

## 1A. Product Module Prerequisite

Before runtime implementation, CMF Studio must treat the following modular PRDs as the product contract for this work:

- `docs/prd/modules/PRD_INDEX.md`
- `docs/prd/modules/PRD_CMF_01_Strategy_Scope_Release_Gates.md`
- `docs/prd/modules/PRD_CMF_02_Pipeline_Agent_Orchestration.md`
- `docs/prd/modules/PRD_CMF_03_Workspace_Commercial_Consent_Source.md`
- `docs/prd/modules/PRD_CMF_05_Brand_Genesis_Context.md`
- `docs/prd/modules/PRD_CMF_07_Editing_Composition_Rendering.md`
- `docs/prd/modules/PRD_CMF_09_Non_Functional_Requirements.md`
- `docs/prd/modules/PRD_CMF_06_Interview_Expression_Routing.md`
- `docs/prd/modules/PRD_CMF_04_Legacy_Primitives_JIT_Spec_Governance.md`
- `docs/prd/modules/PRD_CMF_08_Evaluation_Review_Publishing_Memory.md`
- `docs/prd/modules/PRD_CMF_10_Agent_Factory_Runtime.md`

These modules define Feature Requirements, epics, and stories for the interview-first intelligence layer. Architecture, tech specs, agent contracts, and backend code must trace back to them.

The most important correction is PRD-11: JIT Skill Compilers are adapted to generate Interview Briefs as a primary output. Legacy script-writing skills remain source doctrine and fixture material, but the north-star use case is now interview preparation, narrative induction, contrastive questioning, expression extraction lenses, and evaluation support.

## 2. Step 1 - Canonical Methodology Implementation Map

Objective: define where CMF methodologies enter runtime, where they should not enter, and which contracts make them executable.

Sources:
- `docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md`
- `reference/conscious-rivers/docs/prd/modules/PRD_08_Conscious_Primitives.md`
- `THE CMF STUDIO/Matrix of Edging.md`
- `docs/tech-specs/TS-CMF-025-matrix-of-edging-brief.md`
- `docs/tech-specs/TS-CMF-015-jit-skill-compiler-saturation-and-contrast.md`

Outputs:
- `docs/methodology/CMF_Methodology_Implementation_Map.md`
- Methodology bindings for agent specs.
- Eval obligations tied to primitive families, Matrix passes, and RSCS laws.

Detailed plan:
1. Map RSCS saturation, collision, compression, and evaluation to CRAL, Context Premise, Matrix, extraction, routing, SceneSpec, and review.
2. Map meaning primitives and experience primitives to production quality gates.
3. Define where methodology becomes executable contract, where it remains advisory, and where it is explicitly banned.
4. Create a primitive quality gate vocabulary used by eval registries and the Review Workbench.

Acceptance checks:
- Every methodology entry names a runtime object, responsible agent, and evaluation surface.
- Primitive quality checks are connected to eval definitions, not only prose.
- No method can bypass source truth, consent, registry validity, or human review.

## 3. Step 2 - Research Spine and Eval Registry Architecture

Objective: make research and evaluation registries explicit before building agents.

Sources:
- `docs/architecture/Sovereign_CRAL_Research_Engine_TechSpec_V1.md`
- `docs/architecture/Sovereign_Visual_Research_Engine_TechSpec_V1.md`
- `reference/conscious-rivers/docs/prd/modules/PRD_02_CCF_Content_Factory.md`
- `docs/prd/modules/PRD_INDEX.md`
- `src/ccp_studio/contracts/registry.py`
- `src/ccp_studio/contracts/evaluation_receipts.py`

Outputs:
- `docs/evals/07-eval-registry-and-workbench-architecture.md`
- Backend `EvalDefinition`, `EvalTargetSelection`, `EvalRunCommand`, and `EvalSuggestion` contracts.
- Command Bus registrations for eval run commands.

Detailed plan:
1. Define SCRE/CRAL as the textual sovereign research engine: SearXNG category routing, seven CRAL moment executors, autocomplete polling, Finding-Linked Source Cache, Epistemic Friction Swarm, and CRAL finding registry.
2. Define SVRE/Aurore as the visual sovereign research engine: SearXNG visual categories, Pinterest/source search, T-Score, known-person validity, licensing tier, and source win-rate logic.
3. Define eval registries: eval definitions, target bindings, threshold profiles, fixture and counterexample packs, benchmark profiles, run policies, and UI suggestions.
4. Make primitive obligations first-class in eval definitions. Each target can require primitive refs, primitive families, matrix passes, coalition evidence, and edge-product checks.
5. Connect eval target selection to eval run commands, immutable EvaluationReceipts, approval blockers, and review read models.

Acceptance checks:
- Search API is named as self-hosted SearXNG through SCRE/SVRE. Serper/Tavily are legacy-deprecated only.
- Evaluation target selection can answer: "Which evals must run for this object, route, stage, and primitive obligation?"
- EvalReceipts remain immutable and never grant approval by themselves.

## 4. Step 3 - Eval Workbench UI Specification

Objective: define the reviewer-facing surface where eval registries, receipts, blockers, and primitive failures are legible.

Sources:
- `docs/tech-specs/TS-CMF-050-evaluation-receipt-generation.md`
- `docs/tech-specs/TS-CMF-051-evidence-rich-review-surface.md`
- `docs/tech-specs/TS-CMF-053-approval-blockers.md`
- `src/ccp_studio/contracts/review_state.py`

Outputs:
- `docs/ui/cmf-eval-workbench.md`
- UI read-model requirements for registry browser, eval run queue, receipt comparison, primitive failure expansion, blocker resolution, and PWA/Telegram handoff.

Detailed plan:
1. Define workbench panels for eval registry, target selection, run commands, receipt history, primitive failures, approval blockers, and repair suggestions.
2. Ensure UI never performs scoring locally. It displays backend read models and submits commands.
3. Add primitive-specific failure cards: missing primitive evidence, coalition collapse, edge-product drift, anti-centroid flattening, route mismatch, unsupported primitive ref.
4. Define operator actions: run required evals, request revision, compare rerun, inspect blocker, open PWA deep link, approve only through governed review commands.

Acceptance checks:
- A reviewer can see why an asset failed by primitive, evidence, route, and repair action.
- Telegram can summarize low-risk status, but PWA remains required for complex evidence review.

## 5. Step 4 - Agent Intelligence Contract

Objective: define how each agent uses intelligence: standards, primitives, rules, tools, protocols, memory, skills, constitutions, and evals.

Sources:
- `docs/cmf-studio-agent-factory-architecture.md`
- `docs/cmf-studio-intelligence-operating-model.md`
- `docs/tech-specs/TS-CMF-002-pipeline-stage-orchestration-records.md`
- `src/ccp_studio/contracts/orchestration.py`
- `src/ccp_studio/contracts/agent_gateway.py`

Outputs:
- `docs/cmf-studio-agent-intelligence-contract.md`
- `AgentRoleSpec`, `IntelligenceProfile`, `MethodologyBinding`, `EvalBinding`, `MemoryAccessPolicy`, `ToolCapabilitySpec`, and `HookSpec` definitions.

Detailed plan:
1. Define agents as named accountable role contracts, not prompt personas.
2. Define sub-agents as bounded specialist contracts owned by an agent or department.
3. Define hooks as lifecycle checks before and after model, tool, workflow, and command execution.
4. Define extensions as adapter packages that expose tools, workflows, provider actions, or deployment surfaces.
5. Define how intelligence is governed: constitutions set will, primitives set quality standards, memory supplies admitted evidence, tools perform actions, evals inspect outcomes.

Acceptance checks:
- Every agent can state goal, department, fit rationale, allowed tools, skills, primitive obligations, eval bindings, memory policy, and receipts.
- Pi remains orchestrator through the Python Agent Gateway. Google ADK/Agents CLI may be generated adapter output, not source of truth.

## 6. Step 5 - Skill System Contract

Objective: separate stable operational skills from JIT skill compilers, and make JIT skill use fit the current extraction and induction workflow.

Sources:
- `docs/tech-specs/TS-CMF-015-jit-skill-compiler-saturation-and-contrast.md`
- `src/ccp_studio/contracts/skills.py`
- legacy JIT Skill Compiler docs listed in the Legacy Inventory
- `reference/conscious-rivers/docs/prd/modules/PRD_02_CCF_Content_Factory.md`

Outputs:
- `docs/cmf-studio-skill-system-contract.md`
- Stable skill and JIT skill manifest shapes.
- JIT modes for research distillation, Context Premise, narrative induction, interview engineering, expression extraction, route comparison, and evaluation support.

Detailed plan:
1. Define stable operational skills for repeated agent operations such as source review, registry lookup, command proposal, and blocker inspection.
2. Define JIT skill compilers for saturation-bound creative intelligence: extraction, narrative induction, interview engineering, contrastive prompting, anti-draft calibration, primitive coalition tests, Voice DNA, and evaluation support.
3. Require `SaturationContextBundle` and `SkillInvocationRecord` for every JIT run.
4. Block JIT output from affecting extraction, routing, or approval unless evidence, contrast, and anti-draft gates pass.

Acceptance checks:
- Not all skills are JIT.
- JIT skill compilers are not reduced to final-output writing prompts.
- JIT outputs are evidence-cited and evaluable.

## 7. Step 6 - Agent Factory Registry

Objective: turn the Factory architecture into a registry that implementation can load, audit, and adapt.

Sources:
- `docs/cmf-studio-agent-factory-architecture.md`
- `docs/cmf-studio-pipeline-map.md`
- `docs/architecture.md`

Outputs:
- `docs/cmf-studio-agent-factory-registry.md`
- First executable team registry for the research-to-review slice.

Detailed plan:
1. Define Factory departments, department-owned objects, and stage ownership.
2. Register first executable team: SCRE/CRAL Research Agent, Evidence Critic, Context Premise Agent, Matrix of Edging Agent, JIT Skill Compiler Agent, Expression Extraction Agent, Route Candidate Agent, Eval Registry Agent, Evaluation Agent, Review Workbench Agent, and Pi Orchestrator.
3. For each agent, define goal, fit rationale, inputs, outputs, skills, tools, hooks, evals, and receipt obligations.
4. Define adapter fields for Google ADK/Agents CLI export after Python source contracts exist.

Acceptance checks:
- Factory registry is readable end to end.
- Agent boundaries follow the pipeline rather than arbitrary model personas.
- No agent can invent routes, formats, primitives, or eval standards outside active registries.

## 8. Step 7 - Core Documentation Repair

Objective: link the PRD, architecture, pipeline map, agent docs, eval docs, and methodology docs into one non-conflicting canon.

Sources:
- `docs/architecture.md`
- `docs/cmf-studio-pipeline-map.md`
- `docs/cmf-studio-agent-factory-architecture.md`
- `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md`
- all new docs from steps 1-6

Outputs:
- Architecture and pipeline references to the 9-step execution plan.
- Explicit CRAL/SCRE research spine in the pipeline map.
- Explicit primitive-as-quality-standard statement in architecture.

Detailed plan:
1. Add the new execution docs to architecture frontmatter references.
2. Repair the pipeline map stage names so CRAL/SCRE is visible, not hidden under generic research.
3. Add eval registry and Review Workbench references to the evaluation stage.
4. Preserve Ideogram 4 `CompositionJob` JSON as composition lineage.

Acceptance checks:
- A reader can find CRAL, Context Premise, Matrix of Edging, JIT Skill Compiler, Expression Extraction, Route Candidate, Eval Receipt, and Review Workbench by scanning the pipeline map.
- Serper/Tavily appear only as deprecated legacy APIs.

## 9. Step 8 - Backend Eval Registry Slice

Objective: implement the missing first half of the eval chain in Python.

Sources:
- `src/ccp_studio/contracts/evaluation_receipts.py`
- `src/ccp_studio/services/evaluation_receipt_service.py`
- `src/ccp_studio/api/v1/evaluations.py`
- `src/ccp_studio/contracts/registry.py`
- `tests/cmf_studio/test_evaluation_receipt_generation.py`

Outputs:
- `src/ccp_studio/contracts/eval_registry.py`
- `src/ccp_studio/repositories/eval_registry.py`
- `src/ccp_studio/services/eval_registry.py`
- `src/ccp_studio/api/v1/eval_registry.py`
- `tests/cmf_studio/test_eval_registry_workbench.py`

Detailed plan:
1. Add eval definition contracts with primitive obligations.
2. Add target bindings for object type, pipeline stage, route refs, primitive refs, and threshold profile.
3. Add target selection and suggestion read models for UI.
4. Add eval run command that selects required evals and delegates receipt generation.
5. Add tests proving primitive obligations influence target selection, failed primitive evals create blockers, and review read models expose failures.

Acceptance checks:
- Eval target selection is executable without hand-picked evaluator lists.
- Failed primitive quality checks can create hard failures and approval blockers.
- Existing EvaluationReceipt behavior stays immutable.

## 10. Step 9 - First Agentic Production Slice

Objective: prepare the first end-to-end Factory slice that can later be wired into Pi and agent runtime.

Slice:

```text
SCRE/CRAL research request
-> CRALFindingRegistry / ResearchSnapshot
-> Context Premise
-> Matrix of Edging
-> JIT Skill Compiler
-> Expression Moment
-> Route Candidate
-> Eval target selection
-> Eval run command
-> EvaluationReceipt
-> approval blocker
-> Review Workbench read model
```

Detailed plan:
1. Create agent role specs for each owner in the slice.
2. Bind tools and stable skills to each agent.
3. Bind JIT compiler modes where saturation and contrast are required.
4. Bind eval registry definitions to every emitted object.
5. Expose review read models for human inspection before any approval.
6. Defer ADK/Agents CLI export until the Python contracts and registries are loadable.

Acceptance checks:
- The slice can be reasoned about end to end without hidden prompts.
- Every object has source evidence, primitive obligations, eval targets, and review authority.
- Human approval remains the final state transition.

