---
title: PRD 05 — Feature Index
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
section: '05'
feature_count: 18
functional_requirement_count: 210
---

# 5. Features and Functional Requirements

The product is decomposed into coherent behavioral features. Functional Requirements use globally stable IDs so downstream Architecture, Epics, Stories, technical specifications, tests, events, and receipts can reference them even when feature grouping evolves.

| Feature | Title | FR range | FRs | Governing decisions |
| --- | --- | --- | --- | --- |
| F01 | [Governed Product Lifecycle and Run Constitution](F01-governed-product-lifecycle.md) | FR-001–FR-008 | 8 | D001, D002, D004, D006, D025, D027, D033 |
| F02 | [Configured Evidence Workspace, Source Lock, and Saturation](F02-configured-evidence-workspace.md) | FR-009–FR-018 | 10 | D003, D005, D006, D007, D022, D023, D028 |
| F03 | [Visual Syntax First and Draft Activative Understanding](F03-visual-syntax-first.md) | FR-019–FR-031 | 13 | D003, D007, D011, D012, D013, D014, D030, D031 |
| F04 | [Atomicity Classification and Draft Harness Model](F04-atomicity-draft-harness-model.md) | FR-032–FR-040 | 9 | D008, D009, D010, D011, D030, D031, D033 |
| F05 | [Dependency-Driven Genesis and Human Authority](F05-dependency-driven-genesis.md) | FR-041–FR-050 | 10 | D002, D009, D010, D011, D019, D025, D027, D028 |
| F06 | [Canonical Harness IR and Artifact Compiler](F06-canonical-harness-ir.md) | FR-051–FR-059 | 9 | D003, D011, D014, D017, D018, D025, D029, D033 |
| F07 | [Capability Ownership, Modules, Phases, Contexts, and Contracts](F07-capability-module-phase-contract.md) | FR-060–FR-071 | 12 | D012, D013, D014, D015, D019, D026, D033 |
| F08 | [Reference, SPR, and Minimum Complete Context](F08-reference-spr-context.md) | FR-072–FR-080 | 9 | D016, D017, D018, D019, D020, D033 |
| F09 | [Canonical Skill Ecology and Skill Design Compiler](F09-canonical-skill-ecology.md) | FR-081–FR-090 | 10 | D012, D016, D017, D021, D033 |
| F10 | [Skill Composition Recipes and Deterministic JIT Execution Capsules](F10-skill-composition-jit-capsules.md) | FR-091–FR-102 | 12 | D017, D018, D019, D020, D021, D033 |
| F11 | [Behavioral Evaluation, Benchmark Portfolio, Maturity, and Scorecards](F11-behavioral-evaluation-benchmarks.md) | FR-103–FR-116 | 14 | D003, D021, D022, D023, D024, D027, D032 |
| F12 | [Event-Sourced Harness Control Tower and Observability](F12-harness-control-tower.md) | FR-117–FR-126 | 10 | D024, D025, D026, D027, D029 |
| F13 | [Repair, Invalidation, Readiness, and Implementation Authorization](F13-repair-readiness-authorization.md) | FR-127–FR-136 | 10 | D003, D019, D021, D024, D025, D026, D027, D033 |
| F14 | [Canonical Format Categories, Format Profiles, and Activative Sequencing](F14-format-categories-sequencing.md) | FR-137–FR-150 | 14 | D004, D007, D008, D013, D030, D031, D032, D033 |
| F15 | [Traceable Development Capsule and Implementation Handoff](F15-development-capsule-handoff.md) | FR-151–FR-159 | 9 | D001, D003, D011, D015, D021, D027, D029, D032 |
| F16 | [Controlled V2.1 Migration, Compatibility, and Release Governance](F16-v2-migration-release.md) | FR-160–FR-169 | 10 | D003, D022, D024, D028, D032, D033 |
| F17 | [Three Explicit Compilation Target Profiles](F17-three-compilation-targets.md) | FR-170–FR-180 | 11 | D001, D004, D005, D006, D011, D013, D027, D029, D032, D033 |
| F18 | [Builder Workflow Runtime and Agentic Execution Factory](F18-builder-workflow-runtime.md) | FR-181–FR-210 | 30 | D001, D002, D003, D006, D011, D012, D013, D014, D015, D017, D018, D019, D020, D021, D022, D023, D024, D025, D026, D027, D028, D029, D032, D033 |

## Requirements discipline

- Requirements state **capabilities and observable consequences**, not implementation technologies.
- Brownfield context identifies what V2.1 or the prior system already provides and the required delta.
- Architecture owns technical mechanisms and public interfaces.
- Epics group requirements into independently valuable outcomes after Architecture is approved.
- Stories must fit one development-agent context, avoid future dependencies, and carry Given/When/Then acceptance criteria.
