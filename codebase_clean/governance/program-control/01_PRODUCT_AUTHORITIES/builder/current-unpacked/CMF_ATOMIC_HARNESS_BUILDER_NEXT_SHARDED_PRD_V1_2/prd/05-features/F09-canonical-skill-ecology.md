---
title: F09 — Canonical Skill Ecology and Skill Design Compiler
product: CMF Atomic Harness Builder Next
version: 0.3.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F09
governing_decisions:
- D012
- D016
- D017
- D021
- D033
user_journeys:
- UJ-05
- UJ-07
- UJ-08
- UJ-11
functional_requirement_count: 10
---

# F09 — Canonical Skill Ecology and Skill Design Compiler

**User outcome:** A JIT Skill Maintainer can discover, reuse, adapt, design, compile, and evaluate capabilities without skill sprawl or monolithic prompt documents.

## Description

This feature turns the existing CCP skill doctrine into a canonical capability ecology. It preserves the original CCSB separation between strategic Skill Design Brief and modular implementation while incorporating progressive disclosure, leading words, behavioral testing, and atomic-harness ownership.

## Brownfield baseline

The current system contains real umbrella skills, a detailed Skill Authoring Guide, canonical reasoning modules, Hunter/Analyst/Composer/Commander lanes, and a CCSB design. It lacks one authoritative capability registry, a typed skill IR, consistent distinction between illustrated and production-ready skills, and automated behavioral gates.

## Required product delta

Create a maturity-gated Skill Capability Registry, capability-gap analysis, typed Skill Design Brief compiler, harness adaptations, progressively disclosed packages, and eval-bound artifact identity.

## Traceability

- **Decisions:** D012, D016, D017, D021, D033
- **User journeys:** UJ-05, UJ-07, UJ-08, UJ-11
- **Cross-cutting NFRs:** NFR-EVAL-001, NFR-EVAL-002, NFR-TRACE-003, NFR-MAINT-002, NFR-PORT-001

## Functional Requirements

### FR-081 — Maintain a Canonical Skill Capability Registry

**Requirement:** The Builder must maintain a versioned registry of reusable procedural capabilities with stable IDs, names, responsibilities, input and output contracts, authority lane, failure modes, reasoning modules, maturity, artifact availability, and evaluation receipts.

**Consequences (testable):**

- The registry distinguishes packaged, reference-illustrated, capability-illustrated, experimental, tested, stable, deprecated, and superseded entries.
- A runtime cannot treat a merely illustrated skill as production-ready.

**Traceability:** Decisions D017, D021; journeys UJ-08.

### FR-082 — Organize canonical skills by authority lane

**Requirement:** Every canonical skill must declare its Hunter, Analyst, Composer, or Commander lane without turning the lane into a monolithic agent or nested skill hierarchy.

**Consequences (testable):**

- The lane describes authority and responsibility, not autonomous identity.
- Flat skills remain orchestrator-invoked and independently testable.

**Traceability:** Decisions D012, D017; journeys UJ-05.

### FR-083 — Track skill maturity and plasticity

**Requirement:** Canonical skills and adaptations must use governed maturity states with promotion, change, regression, deprecation, and migration rules.

**Consequences (testable):**

- Stable skills cannot be behaviorally changed without required regression coverage.
- New skills begin in draft or evaluation-pending state.

**Traceability:** Decisions D021; journeys UJ-08.

### FR-084 — Run a formal skill necessity and capability-gap test

**Requirement:** Before creating a JIT Skill, the Builder must determine whether deterministic code, a schema, validator, tool, inline instruction, external reference, human decision, existing canonical skill, or adapter can reliably satisfy the capability.

**Consequences (testable):**

- A rejected skill candidate records the chosen alternative owner.
- A new canonical skill requires evidence that no approved capability covers the need.

**Traceability:** Decisions D012, D017, D033; journeys UJ-05, UJ-08.

### FR-085 — Prefer reuse, adaptation, or adapter composition

**Requirement:** The Builder must attempt exact canonical reuse, harness-local ecological adaptation, or a bounded adapter before authorizing a new canonical capability.

**Consequences (testable):**

- Adaptations preserve the canonical skill's procedural DNA and declare local mutations.
- Overlapping canonical skills trigger redundancy review rather than silent duplication.

**Traceability:** Decisions D017; journeys UJ-08.

### FR-086 — Compile a typed Skill Design Brief

**Requirement:** Every new or materially adapted skill must begin from a reviewable structured brief covering intent, target, context, trigger or program invocation, inputs, action, method, modules, constraints, output artifact, success criteria, failure evidence, and runtime budgets.

**Consequences (testable):**

- The brief remains legible to a product owner before SKILL.md generation.
- Dynamic values are parameterized and no instance-specific content is promoted into the reusable capability.

**Traceability:** Decisions D017, D019; journeys UJ-08.

### FR-087 — Use leading words as tested behavioral anchors

**Requirement:** A skill may declare one or more compact leading words or phrases only when they encode a clear behavioral prior, reduce instruction duplication, and are evaluated against the target failure mode.

**Consequences (testable):**

- The test measures behavioral adoption rather than phrase repetition.
- Weak or colliding leading words are removed through no-op and variance testing.

**Traceability:** Decisions D017, D021; journeys UJ-08.

### FR-088 — Compile portable progressively disclosed skill packages

**Requirement:** The Builder must compile the typed skill definition into a compact SKILL.md plus only justified references, schemas, scripts, examples, templates, evaluation cases, and a manifest.

**Consequences (testable):**

- The main SKILL.md contains the active procedure and checkable completion criteria.
- Heavy or branch-specific reference is loaded through governed context pointers.

**Traceability:** Decisions D016, D017; journeys UJ-07, UJ-08.

### FR-089 — Bind skill packages to evaluation assets

**Requirement:** Every skill package must identify its baseline controls, positive cases, adversarial cases, counterexamples, scoring rubric, maturity requirements, and latest evaluation receipt.

**Consequences (testable):**

- A required production skill without an eligible receipt blocks authorization.
- The evaluated package hash matches the package available to capsule compilation.

**Traceability:** Decisions D021; journeys UJ-08.

### FR-090 — Detect skill no-ops, sediment, and redundancy

**Requirement:** The Builder must analyze whether skill content changes behavior over control, duplicates canonical meaning, contains stale or unreachable branches, or repeats guidance already enforced by code or contracts.

**Consequences (testable):**

- No-op guidance is removed or converted into a stronger tested mechanism.
- The registry preserves one source of truth for each canonical procedural capability.

**Traceability:** Decisions D017, D021, D033; journeys UJ-08.

## Known failure and edge conditions

- A new skill is generated for every model phase.
- A runtime-compiled prompt is promoted into the canonical registry.
- A stable skill is rewritten offline without failure evidence.
- A giant SKILL.md embeds every branch and reference.
- The agent repeats a leading word but the target behavior does not improve.

## Explicitly out of scope

- Making the Skill Registry a universal marketplace.
- Treating skills as autonomous agents.
- Encoding deterministic calculations or routing as prose when code can own them.
