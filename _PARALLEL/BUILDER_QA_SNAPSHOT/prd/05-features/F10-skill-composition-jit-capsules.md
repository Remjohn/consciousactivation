---
title: F10 — Skill Composition Recipes and Deterministic JIT Execution Capsules
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F10
governing_decisions:
- D017
- D018
- D019
- D020
- D021
- D033
user_journeys:
- UJ-07
- UJ-08
- UJ-11
functional_requirement_count: 12
---

# F10 — Skill Composition Recipes and Deterministic JIT Execution Capsules

**User outcome:** A generated harness can compile a reproducible, phase-local prompt/program context from approved skills, adaptations, bindings, evidence, references, and contracts at the moment it is needed.

## Description

This feature preserves the original CCP JIT idea—resolving dependent variables and archetype or format branches into a final compiled execution program—while replacing one large monolith with typed, phase-local capsules.

## Brownfield baseline

The Achievement Story Design Brief and CCSB architecture already describe invariant blocks, runtime variables, module composition, compilation gates, and final assembled skills. The new architecture must distinguish durable capabilities from ephemeral execution contexts and make assembly deterministic and receipted.

## Required product delta

Create harness-local adaptations, composition recipes, runtime binding schemas, deterministic assembly, dependency and precedence resolution, degradation policies, context manifests, capsule identity, and unload rules.

## Traceability

- **Decisions:** D017, D018, D019, D020, D021, D033
- **User journeys:** UJ-07, UJ-08, UJ-11
- **Cross-cutting NFRs:** NFR-REL-001, NFR-PERF-002, NFR-PERF-003, NFR-TRACE-003, NFR-PORT-002

## Functional Requirements

### FR-091 — Represent harness-local skill adaptations

**Requirement:** The Harness IR must define how a canonical skill's ontology, procedure, completion criteria, references, failure modes, and evaluation mutate for one atomic harness without creating a new canonical skill identity.

**Consequences (testable):**

- The adaptation records its canonical base version and local delta.
- Changes outside the allowed adaptation surface require canonical skill review.

**Traceability:** Decisions D017; journeys UJ-07, UJ-08.

### FR-092 — Define Skill Composition Recipes

**Requirement:** The Builder must compile reusable recipes declaring the canonical skills, adaptations, reasoning modules, reference branches, runtime bindings, output contracts, and evaluation hooks required for a phase or execution path.

**Consequences (testable):**

- Recipes are parameterized and contain no instance-specific resolved values.
- The recipe compiler validates compatibility among all selected components.

**Traceability:** Decisions D017; journeys UJ-07.

### FR-093 — Compile runtime binding schemas

**Requirement:** Every recipe must declare required, optional, conditional, derived, and forbidden runtime variables; their types; sources; authority; dependencies; defaults; and missing-value behavior.

**Consequences (testable):**

- A missing required binding is detected before prompt assembly.
- Hardcoded instance values cannot replace declared dynamic inputs.

**Traceability:** Decisions D019; journeys UJ-07.

### FR-094 — Assemble capsules through deterministic code

**Requirement:** The generated harness must use a deterministic JIT compiler—not a free-form model decision—to select authorized skills, versions, branches, references, bindings, contracts, and context for a ready phase.

**Consequences (testable):**

- Identical compiler inputs produce the same capsule bytes or an explicit nondeterminism receipt.
- The execution model cannot choose to omit a required skill or load an unauthorized branch.

**Traceability:** Decisions D018; journeys UJ-07.

### FR-095 — Resolve binding dependencies before compilation

**Requirement:** The JIT compiler must topologically resolve upstream contracts, human decisions, deterministic derived values, and conditional variables before assembling instructions.

**Consequences (testable):**

- Circular dependencies block with a traceable diagnostic.
- A downstream binding is recomputed when an upstream value changes.

**Traceability:** Decisions D019; journeys UJ-07.

### FR-096 — Apply typed authority and precedence rules

**Requirement:** The compiler must resolve conflicts using field-specific authority and precedence rules rather than a generic prompt-time judgment.

**Consequences (testable):**

- A ratified constitutional value cannot be overridden by an unratified runtime suggestion.
- Every conflict resolution or block is receipted.

**Traceability:** Decisions D019; journeys UJ-07, UJ-09.

### FR-097 — Enforce approved degradation policies

**Requirement:** When a value or reference is unavailable, the compiler may continue only through a target- and field-specific degradation policy that defines substitutes, quality impact, provisional status, and authorization ceiling.

**Consequences (testable):**

- The model cannot invent a required missing value.
- Degraded capsules are visibly marked and cannot exceed their allowed readiness state.

**Traceability:** Decisions D019, D027; journeys UJ-07.

### FR-098 — Compile Minimum Complete Context

**Requirement:** The compiler must assemble the smallest complete authorized context for the active phase using the Context Budget Policy and Reference and Loading Graph.

**Consequences (testable):**

- Inactive archetype, format, or evaluator branches are excluded.
- All completion criteria and required evidence remain present.

**Traceability:** Decisions D020; journeys UJ-07.

### FR-099 — Emit a complete JIT capsule package

**Requirement:** Each compilation must produce a typed Execution Capsule, compiled instructions or program input, context manifest, resolved binding manifest, output-contract binding, and compilation receipt.

**Consequences (testable):**

- The package can be executed without consulting hidden conversation history.
- A reviewer can inspect every included and excluded component.

**Traceability:** Decisions D018, D020; journeys UJ-07.

### FR-100 — Bind exact versions and hashes

**Requirement:** The capsule must record canonical skill versions, adaptation versions, recipe version, reference hashes, evidence lock, model policy, compiler version, output contract, and compiled prompt or program hash.

**Consequences (testable):**

- Evaluation and production can prove they used the same capsule identity.
- Changing any bound input yields a distinct capsule identity.

**Traceability:** Decisions D018, D021; journeys UJ-08.

### FR-101 — Treat capsules as ephemeral phase-local artifacts

**Requirement:** A JIT Execution Capsule must declare its owning phase, lifetime, unload policy, downstream exposure, and prohibition against automatic canonical promotion.

**Consequences (testable):**

- Downstream phases receive the typed output contract rather than inherited capsule context by default.
- Expired capsules remain auditable but are not reused under changed bindings.

**Traceability:** Decisions D017, D020; journeys UJ-07.

### FR-102 — Preserve deterministic assembly and bounded stochastic execution

**Requirement:** The runtime architecture must keep context selection, dependency resolution, validation, and routing deterministic while assigning only the bounded semantic or creative transformation to the model program.

**Consequences (testable):**

- The capability ownership map can identify which part of an execution was stochastic.
- Critical orchestration cannot migrate into prompt prose without an approved architecture delta.

**Traceability:** Decisions D012, D018, D033; journeys UJ-05, UJ-07.

## Known failure and edge conditions

- The agent freely decides what context to include.
- A fixed prompt loads every possible branch.
- A missing binding is filled with plausible invented content.
- A capsule is reused after upstream decisions change.
- A compiled capsule is registered as a canonical skill without a capability-gap process.

## Explicitly out of scope

- Executing the final model call inside the Builder specification product.
- Selecting one mandatory model provider.
- Promoting every legacy design brief unchanged into a runtime capsule.
