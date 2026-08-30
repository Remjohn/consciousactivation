# CAE Interview Program Integration Bundle v3

**Document class:** IMPLEMENTATION PROGRAM BUNDLE
**Version:** 3.0.0-draft
**Status:** PROPOSED — PRD/TECH-SPEC RATIFICATION REQUIRED BEFORE BUILD AUTHORITY
**Build authority:** false
**Date:** 2026-08-30

## Purpose

This bundle defines the next brownfield engineering increment for the CAE Interview Program. It is intentionally **specification-first**: implementation mandates are derived from approved product/technical requirements and existing repository authority. The bundle does not authorize Gemini or another implementation agent to invent missing ontology, service ownership, or runtime contracts.

## Core product thesis

The Interview Program is a **semantic-acquisition program** that uses a bounded hypothesis portfolio and controlled question intelligence to help a Guest surface authentic, high-resolution human evidence that is useful for downstream narrative, archetype, format, and production work.

The target operating pattern is:

`upstream intelligence + current audience state + guest territory + world signal + format/archetype intent`
`→ collision/hypothesis candidates (~96 planning target)`
`→ diversified Operator selection (16–24 planning target)`
`→ Question Program / bounded adaptive interview`
`→ authenticated evidence`
`→ content candidates`
`→ downstream production.

The numeric values are planning targets, not hard quotas.

## Brownfield constitutional rule

Do not build a second Interview Composer or a second canonical interview ontology.

The live repository currently gives `services/interview-composer` ownership of the Guest Research Package, Activative Interview Brief, and Composer Session, while AIR owns deeper activation objects. The existing Composer tech spec treats the Brief as a central integration boundary. Those existing boundaries remain authoritative. See the source register in `00_GOVERNANCE/01_SOURCE_AUTHORITY_REGISTER.md`.

## Object-conservation rule

The bundle does **not** authorize new canonical objects named:

- `ContentHypothesis`
- `QuestionProgram`
- `QuestionSystem`
- `InterviewHarnessV2`

A requirement must first be represented through existing CAE/AIR objects, existing Brief fields, or derived/view/runtime structures. A new canonical object requires a separate constitution/promotion decision outside this bundle.

## What v3 fixes from v2

1. Inserts a real PRD delta and product requirement mapping before engineering mandates.
2. Adds the missing Question Intelligence cross-book synthesis stage and makes it a prerequisite to Question implementation.
3. Defines the 12 Research / Activation Dimensions as a **provisional coordinate model**, not a new canonical ontology.
4. Defines the collision → hypothesis → question geometry contract without canonizing `ContentHypothesis`.
5. Defines 96→16–24 portfolio selection as a diversity-aware selection problem.
6. Makes Question-to-Composition compatibility an explicit contract.
7. Defines a richer derived Question IR and Answer Observation / State Transition model.
8. Adds an Operator Studio product/technical specification rather than treating its UI as only a mandate.
9. Adds a repository-native master execution plan and mandate dependency graph.
10. Rewrites Gemini prompts to follow the existing repository pattern: one bounded task/run, read-first, exact current source inspection, explicit stop gates, exact evidence, and no invented symbols.
11. Separates **planned**, **implemented**, and **verified** claims.
12. Adds a final documentation-consistency and PRD-maintenance gate.

## Bundle contents

### 00_GOVERNANCE
- manifest and authority register
- decision register
- proposed PRD delta

### 01_SYNTHESIS
- Question Intelligence synthesis
- hypothesis coordinate/collision contract
- portfolio selection contract

### 02_TECH_SPEC
- Interview Program technical specification
- Operator Studio technical specification
- derived schemas for hypothesis adaptation, Question IR, answer observation, and content compatibility
- mandate contract

### 03_EXECUTION_PLAN
- master implementation plan
- dependency graph
- implementation matrix

### 04_MANDATES
- M01–M11 implementation mandates derived from the accepted specs

### 05_GEMINI_ACTIVATION
- one execution prompt per mandate
- common mandate execution protocol

### 06_OPERATOR_GATES
- stage gates and acceptance questions

### 07_VALIDATION
- acceptance matrix
- reality-contact protocol
- reward-hacking/false-proof tests
- documentation integrity protocol

### 08_EXAMPLES
- worked hypothesis-to-question example
- worked adaptive routing example

## Important status statement

This bundle is a **build plan and implementation specification package**. It does not claim that M01–M11 have been executed. No implementation completion claim is valid until repository evidence, tests, runtime traces, and operator gates are satisfied.
