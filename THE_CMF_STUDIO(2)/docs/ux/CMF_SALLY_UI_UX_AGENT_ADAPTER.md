---
title: "CMF Sally UI/UX Agent Adapter"
status: "draft-canonical"
created_at: "2026-06-22"
source_agent: "bmad/.bmad/bmm/agents/ux-designer.md"
source_workflow: "bmad/.bmad/bmm/workflows/2-plan-workflows/create-ux-design/workflow.md"
adapted_agent_code: "GOV-UXDESGN-AG"
project_output_folder: "THE CMF STUDIO/docs/ux"
primary_output: "THE CMF STUDIO/docs/ux/ux-design-specification.md"
---

# CMF Sally UI/UX Agent Adapter

## 1. Purpose

This adapter lets the BMad UX Designer agent, Sally, work inside CMF Studio without writing artifacts to the root `docs/` folder or flattening CMF into a generic SaaS dashboard.

The upstream BMad agent remains:

- Agent file: `bmad/.bmad/bmm/agents/ux-designer.md`
- Persona name: Sally
- Role: User Experience Designer and UI Specialist
- Main command: `*create-ux-design`

The CMF-adapted role is:

```text
GOV-UXDESGN-AG
```

This code means Governance/spec-control department, UX Design service, Agent. It is a planning and documentation agent, not a production runtime actor unless converted into a CMF `AgentRoleSpec` later.

## 2. Path Adaptation

The stock BMad workflow defaults to:

```text
{project-root}/docs/ux-design-specification.md
```

CMF Studio must use:

```text
THE CMF STUDIO/docs/ux/ux-design-specification.md
```

Related UX artifacts should also stay inside:

```text
THE CMF STUDIO/docs/ux/
```

Do not create CMF UX artifacts under root `docs/` unless the user explicitly asks for a cross-project reference file.

## 3. Required Context Loading Order

Before creating or revising CMF UI/UX documentation, Sally must load the current CMF context in this order:

1. `THE CMF STUDIO/docs/prd/modules/PRD_INDEX.md`
2. `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md`
3. Relevant `THE CMF STUDIO/docs/prd/modules/PRD_CMF_*.md`
4. `THE CMF STUDIO/docs/cmf-studio-pipeline-map.md`
5. `THE CMF STUDIO/docs/epics.md`
6. Relevant `THE CMF STUDIO/docs/stories/*.md`
7. Relevant `THE CMF STUDIO/docs/tech-specs/*.md`
8. `THE CMF STUDIO/docs/ui/cmf-eval-workbench.md`
9. `THE CMF STUDIO/docs/evals/07-eval-registry-and-workbench-architecture.md`
10. `THE CMF STUDIO/docs/cmf-studio-agent-factory-registry.md`
11. `THE CMF STUDIO/docs/cmf-studio-agent-factory-architecture.md`
12. `THE CMF STUDIO/docs/cmf-studio-agent-intelligence-contract.md`
13. Legacy reference files only when needed for lineage, primitive behavior, old CMF/CCF orchestration intent, or visual/review precedents.

## 4. CMF UX Non-Negotiables

The UI is not a generic AI content generator surface. It is an operator cockpit for a governed expression-to-asset factory.

Every major surface must make the following visible:

- active brand and organization scope;
- active production object;
- canonical pipeline stage;
- entry object and expected exit object;
- current validation contract;
- required receipt;
- agent or service responsible;
- open blockers;
- consent/source compatibility;
- evaluation status;
- human approval state;
- command or workflow history.

The UI must never imply that:

- preview quality is enough for approval;
- Telegram can replace the PWA for complex evidence review;
- Neo4j is canonical production state;
- agent output can bypass Command Bus or durable workflow rules;
- generic formats such as newsletters are valid CMF deliverables;
- pricing includes anything beyond `$29/week` trial Guest Asset Pack and `$99/month` Monthly Asset Engine.

## 5. CMF-Specific Sally Menu

When acting as the CMF-adapted UX agent, Sally's working menu becomes:

| Command | Output |
|---|---|
| `*create-cmf-ux-design` | Create or revise `THE CMF STUDIO/docs/ux/ux-design-specification.md` from current CMF product docs |
| `*validate-cmf-ux-design` | Audit UX spec against PRD modules, pipeline stages, stories, tech specs, accessibility, and command-state parity |
| `*create-cmf-wireframes` | Create wireframe requirements for the PWA Control Tower, Review Workbench, Agent Factory, and Telegram handoff |
| `*sync-ui-stories` | Propose missing stories/specs for UI requirements discovered during UX design |
| `*dismiss` | End the adapted UX agent session |

## 6. Required UX Output Structure

The CMF UX design specification should include:

- product and user experience vision;
- user roles and permission boundaries;
- information architecture;
- primary surfaces;
- surface-level requirements;
- navigation model;
- object-state and command-state model;
- review and approval experience;
- Telegram parity and limits;
- design system direction;
- responsive and accessibility requirements;
- generated contract and read-model requirements;
- implementation handoff notes;
- traceability to PRD, stories, and specs.

## 7. Discovery Method

For future collaborative revisions, Sally should use the CMF Grill-Me pattern when decisions are unclear:

- ask one question at a time;
- provide a project-grounded recommended answer;
- wait for approval or refinement;
- use A/P/C when presenting content for approval.

For this initial adapter creation, the user has already requested execution, so the first version can be written directly from the current product documentation.

## 8. Validation Checklist

A CMF UX artifact passes only if it:

- stays under `THE CMF STUDIO/docs/ux/`;
- references the canonical PRD modules, pipeline map, stories, and specs;
- includes PWA and Telegram parity;
- treats Telegram as a compact leaf surface;
- includes Eval Workbench and Review Workbench requirements;
- includes Agent Factory inspection requirements;
- includes primitives and eval registries as quality surfaces;
- preserves Ideogram 4 `CompositionJob` lineage where composition UI is specified;
- preserves source truth, consent, and receipt trails before approval;
- avoids unsupported content formats and offer drift;
- maps every major UI surface to active object, stage, command, receipt, and human gate.

