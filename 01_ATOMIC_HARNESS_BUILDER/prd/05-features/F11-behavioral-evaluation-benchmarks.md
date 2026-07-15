---
title: F11 — Behavioral Evaluation, Benchmark Portfolio, Maturity, and Scorecards
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F11
governing_decisions:
- D003
- D021
- D022
- D023
- D024
- D027
- D032
user_journeys:
- UJ-08
- UJ-11
- UJ-12
functional_requirement_count: 14
---

# F11 — Behavioral Evaluation, Benchmark Portfolio, Maturity, and Scorecards

**User outcome:** The Builder team can prove which capabilities and Builder versions improve real harness design and downstream performance, while preventing averages from concealing critical failures.

## Description

This feature makes 'best' empirical. It evaluates each skill layer, the Builder specification output, implementation friction, and the resulting harness using real, adversarial, transfer, and protected cases with repeated-run stability.

## Brownfield baseline

V2.1 has structural validation and readiness receipts, and the Activative bundle has reference evaluators and goldens, but the current checks are not a full behavioral benchmark and some evaluators rely on field-presence heuristics rather than semantic quality.

## Required product delta

Create layered skill evaluation, staged benchmark targets, protected corpora, controlled mutations, multidimensional scorecards, hard gates, repeated fresh-context statistics, and downstream feedback ingestion.

## Traceability

- **Decisions:** D003, D021, D022, D023, D024, D027, D032
- **User journeys:** UJ-08, UJ-11, UJ-12
- **Cross-cutting NFRs:** NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-TRACE-003

## Functional Requirements

### FR-103 — Evaluate every skill-system layer

**Requirement:** The Builder must define distinct evaluation suites for Canonical Skills, harness adaptations, composition recipes, JIT capsules, and end-to-end phase behavior.

**Consequences (testable):**

- A passing canonical skill does not automatically certify a faulty harness adaptation.
- Evaluation failures route to the responsible layer.

**Traceability:** Decisions D021, D026; journeys UJ-08.

### FR-104 — Require a no-guidance control

**Requirement:** Behavior-shaping skills and prompt guidance must be compared with a realistic control that omits the candidate guidance.

**Consequences (testable):**

- If the control does not exhibit the target failure, the Builder flags the skill's necessity claim.
- Improvements are reported as deltas, not only absolute scores.

**Traceability:** Decisions D021; journeys UJ-08.

### FR-105 — Run repeated fresh-context trials

**Requirement:** Important stochastic evaluations must execute multiple fresh-context repetitions per variant and record mean, minimum, variance, failure frequency, and confidence estimates.

**Consequences (testable):**

- Single lucky runs cannot support maturity promotion.
- The evaluation manifest declares repetition count and randomization policy.

**Traceability:** Decisions D021, D024; journeys UJ-08, UJ-12.

### FR-106 — Generate positive, adversarial, missing-evidence, and pressure cases

**Requirement:** Skill and phase suites must include correct applications, near-misses, counterexamples, insufficient inputs, contradictions, tempting irrelevant context, and pressure to violate a rule.

**Consequences (testable):**

- The suite tests whether the capability knows when not to apply.
- Pressure scenarios require the agent to act rather than merely recite doctrine.

**Traceability:** Decisions D021, D023; journeys UJ-08.

### FR-107 — Promote maturity only through stored receipts

**Requirement:** Draft, evaluation_pending, experimental, tested, stable, deprecated, and superseded maturity transitions must require target-specific evaluation evidence and regression policies.

**Consequences (testable):**

- A required skill below the target's maturity threshold blocks full authorization.
- A stable skill change triggers all required dependent regressions.

**Traceability:** Decisions D021, D027; journeys UJ-08.

### FR-108 — Verify evaluated artifact identity

**Requirement:** The evaluation system must bind exact source IR, skill package, adaptation, recipe, capsule, compiler, model policy, dataset, and scoring versions.

**Consequences (testable):**

- The shipped artifact hash matches the evaluated artifact hash.
- A changed dependency invalidates the applicable receipt.

**Traceability:** Decisions D021; journeys UJ-08.

### FR-109 — Maintain a staged benchmark portfolio

**Requirement:** The Builder must use one mandatory primary reference harness, contrasting transfer harnesses, and later Visual Asset Editor and Delegation targets before general certification.

**Consequences (testable):**

- Release 1 cannot claim generality beyond its passed reference slice.
- Transfer targets are selected for materially different visual, sequencing, runtime, or asset grammars.

**Traceability:** Decisions D022, D032; journeys UJ-12.

### FR-110 — Maintain a layered versioned benchmark corpus

**Requirement:** Each benchmark target must contain real specimens, expert goldens, known failures, adversarial near-misses, incomplete or contradictory evidence, controlled mutations, transfer cases, and protected release cases.

**Consequences (testable):**

- Every case has stable IDs, expected behavior, scoring rules, and source provenance.
- Protected labels are not exposed to the Builder during ordinary development runs.

**Traceability:** Decisions D023; journeys UJ-12.

### FR-111 — Generate controlled mutation tests

**Requirement:** The benchmark system must support one-variable mutations such as preserving topic while changing grammar, preserving grammar while changing topic, removing a sequence invariant, swapping semantic polarity, or injecting irrelevant style evidence.

**Consequences (testable):**

- The expected decision explains which invariant changed.
- Mutation cases test causal understanding rather than visual similarity.

**Traceability:** Decisions D023; journeys UJ-02, UJ-03, UJ-12.

### FR-112 — Protect release-gate benchmark integrity

**Requirement:** Protected benchmark access, label changes, scoring changes, and case retirement must be governed, versioned, and audited.

**Consequences (testable):**

- A release report discloses any benchmark change since the baseline.
- Known answer leakage is a hard release failure.

**Traceability:** Decisions D023, D024; journeys UJ-12.

### FR-113 — Score independent quality dimensions

**Requirement:** Builder evaluation must report evidence understanding, visual and temporal understanding, atomicity, product architecture, skill system, evaluation and repair quality, implementation readiness, and downstream performance as separate dimensions.

**Consequences (testable):**

- The full scorecard remains visible even when a composite trend score is calculated.
- Target profiles may define additional category-specific dimensions.

**Traceability:** Decisions D024; journeys UJ-12.

### FR-114 — Enforce hard release gates

**Requirement:** Critical unsupported decisions, evidence failures, wrong atomicity, contract contradictions, silent rewrites, untested required skills, benchmark leakage, false readiness, and anti-goal violations must fail release regardless of average score.

**Consequences (testable):**

- Each hard gate maps to a test or review receipt.
- A high composite score cannot override a failed hard gate.

**Traceability:** Decisions D024, D033; journeys UJ-12.

### FR-115 — Report repeated-run stability

**Requirement:** Release reports must include distribution and dominant failure patterns for stochastic dimensions rather than a single run score.

**Consequences (testable):**

- Thresholds may include minimum and variance limits in addition to mean score.
- A highly variable candidate can fail despite a strong best run.

**Traceability:** Decisions D024; journeys UJ-12.

### FR-116 — Ingest downstream implementation and harness results

**Requirement:** The Builder benchmark system must accept implementation questions, spec deltas, test failures, latency and cost, repair rounds, first-pass acceptance, human preference, wrong-reading outcomes, and certification results linked to the Builder version that produced the capsule.

**Consequences (testable):**

- Builder quality can be compared causally across releases.
- Downstream evidence updates benchmarks through governed online refinement rather than unreviewed batch rewrites.

**Traceability:** Decisions D003, D022, D028; journeys UJ-11, UJ-12.

## Known failure and edge conditions

- A skill is approved because its Markdown looks complete.
- One successful run is presented as proof.
- A composite average hides a wrong atomicity decision.
- Protected benchmark answers enter development context.
- A Builder release is evaluated only on structural artifact counts.

## Explicitly out of scope

- Training foundation models.
- Optimizing benchmarks without domain-expert governance.
- Defining final numeric thresholds before baseline calibration.
