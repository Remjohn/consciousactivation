---
title: Success Metrics and Counter-Metrics
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
metric_count: 18
---

# Success Metrics and Counter-Metrics

### SM-01 — End-to-end autonomous completion rate

**Class:** Primary

**Definition/target:** At least 90% of in-scope Format 02 production demands complete without human intervention after the limited-production learning period.

### SM-02 — Semantic hard-gate pass precision

**Class:** Primary

**Definition/target:** At least 98% of accepted assets satisfy expert-labeled semantic and Activative requirements; no known constitutional failure is accepted.

### SM-03 — Composition effectiveness

**Class:** Primary

**Definition/target:** At least 92% of accepted assets pass composition-context evaluation and downstream composition validation without asset regeneration.

### SM-04 — First-pass candidate acceptance

**Class:** Secondary

**Definition/target:** Measure and improve the percentage of demands with at least one passing candidate in the initial portfolio; do not optimize by lowering gates.

### SM-05 — Median quality-repair rounds

**Class:** Secondary

**Definition/target:** Median at or below one for mature in-scope workflows, with a constitutional maximum of three.

### SM-06 — Recovery success

**Class:** Primary

**Definition/target:** At least 99% of injected recoverable infrastructure failures resume or fail over without loss of committed state or quality-round corruption.

### SM-07 — Asset reproducibility

**Class:** Primary

**Definition/target:** 100% of accepted assets preserve sufficient pinned identity to reconstruct plan, workflow, compute, model, LoRA, controls, evaluator, and lineage.

### SM-08 — Budget conformance

**Class:** Secondary

**Definition/target:** At least 95% of completed runs remain within selected Budget Program cost and wall-clock ceilings, excluding explicit approvals.

### SM-09 — Evaluator hard-failure recall

**Class:** Primary

**Definition/target:** Production evaluator profiles meet release-specific hard-failure recall and false-rejection thresholds on protected labeled cases.

### SM-10 — Repair precision

**Class:** Primary

**Definition/target:** At least 90% of successful repairs modify the labeled responsible layer while preserving all expert-labeled frozen properties.

### SM-11 — Syntax-aware recurrence accuracy

**Class:** Primary

**Definition/target:** VLM recurrence verdicts meet the protected benchmark threshold across beneficial, productive, redundant, fatiguing, and contradictory cases.

### SM-12 — Memory retrieval usefulness

**Class:** Secondary

**Definition/target:** Retrieved knowledge improves or preserves quality and cost over no-memory control without increasing authority violations.

### SM-13 — Cost per accepted asset

**Class:** Secondary

**Definition/target:** Track by family, workflow, Budget Program, and repair round; optimize only after hard quality gates are maintained.

### SM-14 — Human exception rate

**Class:** Secondary

**Definition/target:** Routine production exception rate trends below 5% in certified scope without suppressing valid conflict or capability-gap reporting.

### SM-C1 — Raw candidate count

**Class:** Counter

**Definition/target:** Do not optimize for producing more candidates; candidate count is a budgeted means, not product value.

### SM-C2 — Number of models, LoRAs, workflows, or agents

**Class:** Counter

**Definition/target:** Do not treat registry size or compute fan-out as evidence of capability.

### SM-C3 — Standalone aesthetic score

**Class:** Counter

**Definition/target:** Do not optimize beauty independently of semantic, Activative, composition, continuity, and editability requirements.

### SM-C4 — Zero human intervention at any cost

**Class:** Counter

**Definition/target:** Do not hide legitimate authority, capability, conflict, or degraded-result exceptions to make automation statistics look better.
