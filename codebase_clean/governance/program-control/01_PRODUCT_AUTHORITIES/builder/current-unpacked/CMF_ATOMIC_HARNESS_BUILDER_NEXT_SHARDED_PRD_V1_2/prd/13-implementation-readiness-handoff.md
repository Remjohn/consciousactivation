---
title: PRD 13 — Implementation-Readiness Handoff
product: CMF Atomic Harness Builder Next
version: 0.3.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
section: '13'
---

# 13. Implementation-Readiness Handoff

This PRD is complete enough to enter **Architecture**, not implementation. The next workflow must preserve stable IDs and resolve technical mechanisms without rewriting product behavior.

## Required Architecture outputs

- canonical Harness IR schema, mutation model, storage, versioning, and migration;
- lifecycle, phase, context, contract, reference-loading, dependency, repair, and authorization graph architecture;
- Builder Workflow IR, Workflow Profile Registry, Actor Assignment Matrix, router, scheduler, node executor, isolation, CI promotion, rollback, and incident architecture;
- deterministic control-plane boundaries and typed model-program interfaces;
- Visual Syntactic Parsing and category-adapted temporal parsing architecture;
- Canonical Skill Capability Registry, skill compiler, recipe compiler, and JIT Execution Capsule compiler;
- benchmark, protected-case, evaluator, and maturity architecture;
- event schema, Run Ledger, artifact registry, read models, and Pi Control Tower architecture;
- V2.1 compatibility, dual-run, migration, and deprecation architecture;
- Development Capsule build and validation architecture;
- deployment, security, privacy, access, and operational constraints.

Architecture must map every significant mechanism to FR/NFR IDs and identify technical requirements that must enter Epic and Story planning.

## Epics and Stories prerequisites

The epic workflow must read the complete PRD, approved Architecture, and Control Tower UX contract when available. It must:

1. extract every FR and NFR without summarizing away detail;
2. extract Architecture and UX implementation requirements;
3. create a complete requirements inventory and coverage map;
4. organize epics around independently valuable operator or downstream outcomes, not technical layers;
5. size stories for one development-agent context;
6. prohibit future-story dependencies;
7. use Given/When/Then acceptance criteria, including edge and failure cases;
8. validate complete FR/NFR/Architecture/UX coverage before implementation readiness.

## Feature technical specifications

After approved epics and stories, each major feature receives a technical specification containing:

- mapped FRs, NFRs, decisions, stories, and source evidence;
- files and existing V2.1 behavior read;
- problem, solution, scope, and excluded scope;
- architecture traceability and public interfaces;
- states, flows, contracts, events, error and degradation behavior;
- observability, authority, security, budgets, and compatibility;
- implementation tasks tied to stories;
- positive, negative, failure, benchmark, and adversarial acceptance examples;
- unit, contract, integration, behavioral, and regression test plans.

## Readiness rule

Implementation may begin only after the PRD, Architecture, Epics/Stories, required feature specifications, benchmark design, Control Tower UX contract, and traceability audit have passed their respective gates. Release 1 may receive a narrowly scoped prototype authorization where a declared empirical question cannot be resolved through documentation alone.


## Constitutional alignment requirements

Architecture and technical specifications must cite `governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`, distinguish harness-development Visual Syntax First from runtime Activation First, support the Conversational Activation / Human Expression category, preserve Activative Intelligence and Expression Moment lineage, and prove that generated visual demands carry Visual Semantic, Visual Narrative, Feature Contract, somatic-route, and wrong-reading context.
