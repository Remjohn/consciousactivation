---
title: PRD 00 — Document Purpose and Authority
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
section: '00'
---

# 0. Document Purpose and Authority

This sharded Product Requirements Document defines **CMF Atomic Harness Builder Next**, the production-hardening evolution of the existing CMF Atomic Harness Spec Builder V2.1.

The product is a **human-governed harness-development compiler**. It transforms an evidence-saturated atomic candidate into an implementation-authorized Development Capsule containing a typed Harness IR, constitutional specifications, phase-local JIT Skills and composition recipes, an executable Builder Workflow Runtime, module and runtime contracts, evaluation and repair systems, implementation artifacts, observability configuration, and readiness receipts. It does **not** implement the final production harness.

## Intended readers

- CMF product and harness architects;
- Builder maintainers and technical architects;
- format-category stewards;
- JIT Skill and evaluation maintainers;
- implementation leads and coding agents;
- reviewers, ratifiers, and release authorities.

## Authority model

The product uses three complementary authorities:

1. **Deterministic tooling** owns source locking, indexing, schema validation, graph transitions, compilation, dependency resolution, context selection, receipts, and other mechanically checkable work.
2. **Agents and typed model programs** own bounded investigation, semantic inference, multimodal parsing, recommendations, and creative transformations inside authorized phases.
3. **Humans** own constitutional, creative-policy, risk, waiver, and irreversible architectural decisions.

## Document system

This package separates product intent from downstream technical realization:

- `prd/` contains product behavior, globally stable Functional Requirements, cross-cutting Non-Functional Requirements, scope, success metrics, and anti-goals.
- `governance/` contains the 33-decision register, requirement registry, source register, category and target registries, product constitution, and traceability maps.
- `addendum/` preserves architecture-rich context, prior-system lessons, JIT Skill history, and brownfield details that should inform Architecture without bloating the main PRD.
- `handoff/` defines the required next artifacts: Architecture, Epics and Stories, feature technical specifications, and implementation-readiness validation.
- `validation/` contains mechanical checks for IDs, coverage, links, source integrity, and anti-placeholder discipline.

## Stable identifiers

- Product decisions: `D001`–`D033`
- User journeys: `UJ-01`–`UJ-14`
- Features: `F01`–`F18`
- Functional Requirements: `FR-001`–`FR-210`
- Non-Functional Requirements: namespaced `NFR-*`
- Success metrics: `SM-*`; counter-metrics: `SM-C*`
- Anti-goals: `AG-*`
- Assumptions: `A-*`; open questions: `OQ-*`; risks: `R-*`

The glossary is binding. Downstream documents must use its terms exactly or propose a governed glossary change.

## Current phase

This PRD is **draft for review**. The 33-question product-constitution session is complete, and the approved workflow-runtime delta is incorporated without changing the 33 locked decisions. Architecture, UX/control-tower design, epics, stories, and per-feature technical specifications are intentionally downstream.
