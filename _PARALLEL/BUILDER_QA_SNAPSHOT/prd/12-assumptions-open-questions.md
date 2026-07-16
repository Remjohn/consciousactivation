---
title: PRD 12 — Assumptions and Open Questions
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
section: '12'
---

# 12. Assumptions and Open Questions

## Assumptions

- **A-001:** V2.1 remains the operational baseline throughout the first migration increments.
- **A-002:** The five canonical categories are Short-Form Edited Video, 2D Character Animation, Carousels, Supervisuals, and Conversational Activation / Human Expression; D031 remains historical evidence and the V1.2 constitutional amendment defines its current effect.
- **A-003:** Pi is the primary authoring and Control Tower environment, but core IR and compilation logic remain adapter-bounded.
- **A-004:** Exact performance and behavioral thresholds will be calibrated against baseline and reference-harness runs rather than invented in the PRD.
- **A-005:** OpenSpec remains a generated implementation-governance view, not the canonical source of truth.
- **A-006:** The first release may structurally support all target types and categories without claiming their production certification.
- **A-007:** The Builder Workflow Runtime is part of the Builder product, while generated harness Phase Graphs remain outputs compiled for downstream harness implementations.
- **A-008:** Release 1 automation is derived from a recorded manual shadow workflow for the selected reference harness rather than invented solely from diagrams.

## Open questions

### OQ-001

**Question:** Which atomic harness is the Release 1 primary reference: F04 Progressive Blind Ranking, CAR Visual Design Audit Tutorial, or another candidate?

**Disposition:** Owner: Product lead; resolve before Architecture finalization.

### OQ-002

**Question:** Which canonical category constitution is production-complete first?

**Disposition:** Owner: Product lead and category steward; expected to follow reference-harness selection.

### OQ-003

**Question:** Which storage technologies implement the Harness IR, event ledger, artifact registry, and benchmark receipts?

**Disposition:** Owner: Architecture; PRD constrains behavior, not technology.

### OQ-004

**Question:** Which multimodal model policy or ensemble provides the first Visual Syntactic Parsing implementation?

**Disposition:** Owner: Architecture and benchmark team.

### OQ-005

**Question:** How are protected benchmark labels governed, access-controlled, and changed?

**Disposition:** Owner: Evaluation governance.

### OQ-006

**Question:** What exact quantitative thresholds define production maturity for each score dimension?

**Disposition:** Owner: Benchmark calibration after baseline runs.

### OQ-007

**Question:** What is the exact Pi custom-UI implementation surface and deployment model for the Control Tower?

**Disposition:** Owner: UX/Architecture.

### OQ-008

**Question:** Which existing capabilities seed version 1 of the Canonical Skill Capability Registry, and which are only illustrated references?

**Disposition:** Owner: Skill architecture audit.

### OQ-009

**Question:** How broadly should legacy Design Briefs such as Achievement Story be migrated into archetype constitutions, composition recipes, and binding schemas in Release 1?

**Disposition:** Owner: Product lead and migration steward.

### OQ-010

**Question:** Does the first reference slice require a production Visual Asset Editor dependency, a stubbed delegation boundary, or no asset delegation?

**Disposition:** Owner: Product lead after reference-harness selection.

### OQ-011

**Question:** Which workflow-runtime technology, queue, and state-machine implementation should execute the Builder Workflow IR?

**Disposition:** Owner: Architecture; compare Pi extensions, local process orchestration, durable workflow engines, and adapter boundaries.

### OQ-012

**Question:** What isolation policy should use worktrees, containers, or stronger sandboxes for each node and implementation story class?

**Disposition:** Owner: Architecture and security; calibrate against source sensitivity, tool risk, cost, and reproducibility.

### OQ-013

**Question:** Which initial workflow profiles are mandatory in Release 1 beyond new harness compilation and benchmark regression?

**Disposition:** Owner: Product lead and Builder maintainer; decide after the reference shadow workflow.
