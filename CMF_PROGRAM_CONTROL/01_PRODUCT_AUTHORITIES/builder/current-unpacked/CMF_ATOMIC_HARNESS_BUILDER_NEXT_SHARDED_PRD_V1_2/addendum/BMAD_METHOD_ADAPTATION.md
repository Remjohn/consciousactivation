---
title: BMAD Method Adaptation for the Builder Program
product: CMF Atomic Harness Builder Next
version: 0.3.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---

# BMAD Method Adaptation for the Builder Program

This program uses BMAD's current document-separation and traceability discipline without replacing CMF doctrine or the deeper Era 3 technical-specification practices.

## Adopted BMAD principles

- The PRD is feature-centered and keeps globally stable FR identifiers.
- Features describe product behavior and testable consequences; technical mechanisms move to Architecture or addendum material.
- A canonical decision log is maintained separately from the polished PRD.
- Architecture is a required input before epic and story creation.
- All FRs, NFRs, Architecture requirements, and Control Tower UX requirements are extracted before epic design.
- Epics are organized around independently valuable outcomes, not technical layers.
- Every FR maps to an epic and every story maps to requirements.
- Stories are sized for one development-agent context, rely only on prior stories, and use Given/When/Then acceptance criteria.
- Final planning validation checks complete coverage, architecture compliance, story quality, file churn, and dependency direction.

## CMF extensions

The Builder program adds traceability that generic PRD workflows do not require:

```text
33 Product Decisions
→ FRs and NFRs
→ Architecture mechanisms and contracts
→ user-value epics
→ vertical stories
→ feature technical specifications
→ acceptance tests and benchmark cases
→ runtime events and receipts
→ downstream harness certification
```

It also requires explicit coverage for:

- Visual Syntax First and knowledge-status integrity;
- four category constitutions and format profiles;
- Activative Sequencing Intelligence;
- canonical skill ecology and JIT capsule compilation;
- protected benchmarks and hard gates;
- Repair and Invalidation Graphs;
- event-sourced observability;
- V2.1 brownfield migration;
- downstream harness-effectiveness proof.

## Document ordering

1. This PRD package
2. Builder Architecture and ADRs
3. Control Tower UX contract
4. Epics and Stories with complete coverage map
5. Per-feature technical specifications
6. Implementation-readiness audit
7. Development and reference-harness certification
