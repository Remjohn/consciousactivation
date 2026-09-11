---
title: F08 — Reference, SPR, and Minimum Complete Context
product: CMF Atomic Harness Builder Next
version: 0.3.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F08
governing_decisions:
- D016
- D017
- D018
- D019
- D020
- D033
user_journeys:
- UJ-05
- UJ-06
- UJ-07
- UJ-08
functional_requirement_count: 9
---

# F08 — Reference, SPR, and Minimum Complete Context

**User outcome:** Each model-driven phase receives exactly the authoritative doctrine, references, evidence, and creative priming needed for its current responsibility—no more and no less.

## Description

This feature formalizes progressive disclosure and prevents context sediment. It distinguishes canonical references, branch-specific resources, SPR packs, runtime bindings, and phase outputs, and governs their loading and influence.

## Brownfield baseline

Current CMF skills and briefs contain rich doctrine and large contextual packages, but loading behavior is often expressed in prose or broad dependency lists. V2.1 does not yet compile context budgets and must-not-influence rules into each harness runtime.

## Required product delta

Create a reference registry, loading graph, phase context policies, SPR governance, budget ranking, approved compression/retrieval behavior, and auditable context manifests.

## Traceability

- **Decisions:** D016, D017, D018, D019, D020, D033
- **User journeys:** UJ-05, UJ-06, UJ-07, UJ-08
- **Cross-cutting NFRs:** NFR-PERF-002, NFR-PERF-003, NFR-TRACE-001, NFR-SEC-002, NFR-MAINT-002

## Functional Requirements

### FR-072 — Maintain a versioned reference registry

**Requirement:** The Builder must register doctrine, ontologies, registries, examples, counterexamples, templates, provider guidance, rights rules, and SPR resources with stable IDs, versions, hashes, owners, authority, and content roles.

**Consequences (testable):**

- A required reference cannot be named only in prose or by an unregistered ghost variable.
- Reference updates have dependency impact and migration visibility.

**Traceability:** Decisions D016, D019; journeys UJ-07.

### FR-073 — Support explicit loading policies

**Requirement:** Each reference must use a declared loading mode such as always, phase_local, skill_local, conditional, retrieval_only, human_only, or forbidden_at_runtime.

**Consequences (testable):**

- A reference loads only in permitted phases and conditions.
- The compilation receipt explains why each loaded reference was selected.

**Traceability:** Decisions D016; journeys UJ-07.

### FR-074 — Define influence boundaries for references

**Requirement:** References must be able to declare the decisions or outputs they may inform and the domains they must not influence.

**Consequences (testable):**

- A visual parsing ontology cannot determine business strategy or coach identity.
- An evaluator does not receive a creative SPR unless its evaluation protocol explicitly requires it.

**Traceability:** Decisions D016, D021; journeys UJ-06, UJ-08.

### FR-075 — Compile progressive disclosure pointers

**Requirement:** Canonical skills and phase instructions must inline only universally required procedure and use typed context pointers for branch-specific or heavy reference material.

**Consequences (testable):**

- Inactive branches do not consume capsule context.
- A missing required pointer target blocks compilation rather than being improvised.

**Traceability:** Decisions D016, D017, D020; journeys UJ-07.

### FR-076 — Govern SPR as phase-local creative priming

**Requirement:** The Builder must treat Sparse Priming Representation as a conditional creative-presence resource loaded only after evidence, meaning, authority, and wrong-reading locks required by the phase are resolved.

**Consequences (testable):**

- SPR may influence authorized creative search but not rewrite evidence or constitutional decisions.
- SPR is excluded from independent evaluation unless the evaluation design explicitly measures its effect.

**Traceability:** Decisions D016, D017, D030; journeys UJ-06, UJ-07.

### FR-077 — Compile a Context Budget Policy per phase

**Requirement:** Every model-driven phase must declare hard and soft token, latency, and cost budgets, required versus optional context classes, compression permissions, retrieval policies, and budget-failure behavior.

**Consequences (testable):**

- A phase's budget is visible before execution.
- Budget rules are target, category, and model-policy aware.

**Traceability:** Decisions D020; journeys UJ-07.

### FR-078 — Rank context by functional necessity

**Requirement:** The JIT compiler must prioritize phase responsibility, output contract, ratified decisions, bindings, canonical procedure, harness adaptation, direct evidence, constraints, conditional references, examples, and enrichment in that order unless the profile specifies a justified override.

**Consequences (testable):**

- Optional examples cannot displace required evidence or contracts.
- The context manifest records priority decisions.

**Traceability:** Decisions D020; journeys UJ-07.

### FR-079 — Block rather than silently truncate required context

**Requirement:** If required context exceeds the approved budget, the Builder must block and recommend phase splitting, typed compression, retrieval, deduplication, reference redesign, model-policy change, or an authorized budget increase.

**Consequences (testable):**

- Required text is never cut mid-procedure without an approved compiler rule.
- The blocker identifies which resources caused the overflow.

**Traceability:** Decisions D020, D033; journeys UJ-07, UJ-09.

### FR-080 — Emit a complete context manifest

**Requirement:** Every JIT Execution Capsule must list included, excluded, summarized, retrieved, and compressed resources; their hashes; their token contribution; and the rationale for each decision.

**Consequences (testable):**

- A reviewer can reproduce the capsule's context selection.
- Excluded future-phase or evaluator resources are visible rather than silently ignored.

**Traceability:** Decisions D018, D020, D025; journeys UJ-07, UJ-09.

## Known failure and edge conditions

- All available references are loaded because they might be useful.
- An SPR pack influences evidence interpretation.
- Required doctrine is silently summarized below its binding precision.
- A capsule exceeds its context budget without an event.

## Explicitly out of scope

- Authoring every reference resource inside the Builder PRD.
- Using context size as a proxy for intelligence.
- Allowing phase implementers to bypass registered loading rules.
