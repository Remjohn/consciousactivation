---
title: Assumptions and Open Questions
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
assumption_count: 8
open_question_count: 6
---

# Assumptions and Open Questions

## Assumptions

- **A-01:** The validated Atomic Harness Builder architecture remains the upstream authority.
- **A-02:** Format 02 Visual Asset Demands and Visual Syntax fixtures can be curated before implementation authorization.
- **A-03:** A VLM or evaluator ensemble can be benchmarked sufficiently for limited production; specific model choice remains an Architecture decision.
- **A-04:** At least one local/self-hosted and one cloud GPU environment can run the required ComfyUI workflow and model stack.
- **A-05:** The separate Delegation PRD will finalize cross-product schema ownership and compatibility policy.
- **A-06:** CMF-OKF v1 will remain compatible with the minimal OKF 0.1 format while adding CMF-specific fields and typed edges.
- **A-07:** Routine source-provenance classification can be deterministic without a dedicated rights workcell.
- **A-08:** Remotion remains the downstream composition owner for the Format 02 reference path; the Visual Asset Editor returns assets and geometry, not final edited shorts.

## Open questions

### OQ-01 — Which exact Format 02 atomic production promise and specimen set will be the canonical Release 1 benchmark target?

Owner: Product/Format 02 Architecture; block: Architecture finalization.

### OQ-02 — Which image-generation base model and VLM evaluator should be the initial benchmark controls?

Owner: Visual Runtime/Evaluation Architecture; block: compute proof.

### OQ-03 — Which cloud GPU provider and object-storage implementation should Architecture select?

Owner: Infrastructure Architecture; block: implementation, not PRD.

### OQ-04 — Which shared contract fields will be finalized by the Delegation PRD versus editor-internal schemas?

Owner: Delegation product planning; block: cross-product implementation.

### OQ-05 — What protected labeled dataset size is sufficient for initial evaluator and recurrence certification?

Owner: Evaluation Architecture; block: limited-production gate.

### OQ-06 — Which character identity or visual-language gap should be used for the Release 1 capability-development proof?

Owner: Format 02/Visual Runtime; block: capability-development story.
