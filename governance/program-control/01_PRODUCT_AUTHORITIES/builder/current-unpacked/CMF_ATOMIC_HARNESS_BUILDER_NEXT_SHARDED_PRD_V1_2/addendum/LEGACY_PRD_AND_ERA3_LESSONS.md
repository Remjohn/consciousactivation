---
title: Legacy PRD and Era 3 Lessons Retained
product: CMF Atomic Harness Builder Next
version: 0.3.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---

# Legacy PRD and Era 3 Lessons Retained

The prior modular PRDs and Era 3 protocols contain strengths that remain binding inputs to the next phases.

## Retained product-writing strengths

- State the architectural correction and the failure it resolves.
- Distinguish what already exists, what must be adapted, what must be retained, what is obsolete, and what requires removal.
- Preserve doctrine, non-negotiable laws, failure examples, and backward-compatibility implications.
- Connect qualitative mandates to concrete mechanisms, acceptance criteria, and tests.
- Treat brownfield repository evidence as a first-class design input.

## Retained technical-specification strengths

Every feature technical specification should identify:

- files and evidence read;
- problem, solution, scope, and excluded scope;
- existing implementation and integration points;
- architecture and requirement traceability;
- technical decisions and alternatives;
- states, contracts, events, errors, degradation, and fallback;
- implementation tasks and story mapping;
- exact acceptance criteria with positive and failure examples;
- unit, contract, integration, benchmark, adversarial, and migration tests.

## Retained implementation-planning strengths

- Stories must be grounded in real system behavior and existing code paths.
- Technical specifications are written after stories so implementation scope has a concrete user or operator outcome.
- Stable doctrine is not rewritten through offline batch refactoring; changes follow observed execution failures and regression evidence.

## Improvements introduced by this PRD

- one canonical Harness IR instead of duplicated document truth;
- global FR/NFR IDs and complete decision coverage;
- stricter separation of PRD, Architecture, Epics/Stories, and technical specifications;
- smaller vertical stories instead of multi-system story monoliths;
- category-native parsing and sequencing requirements;
- skill/capsule terminology and maturity clarity;
- explicit observability and downstream-performance accountability.
