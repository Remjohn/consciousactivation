# ADR-010: Benchmark Governance And Maturity

Status: `ACCEPTED`

Owners: Evaluation governance and architecture. Trace: D003, D021, D022, D023, D024, D026, D027, D032; TS-10, TS-13. Blockers: BD-004, BD-008.

## Context

Structural checks cannot prove behavior. Skills, capsules, phases, workflows, and Builder outputs need repeated, independent, category-appropriate evidence. Generator access to protected labels would invalidate release claims.

## Decision

Use a layered versioned corpus with public/development/protected cases, exact subject identity, no-guidance controls, repeated fresh-context trials, isolated evaluators, multidimensional scorecards, hard gates, and maturity receipts. Separate label custody and credentials from generator/runtime access. Human governance ratifies rubrics and thresholds after Format 02 calibration.

## Alternatives

- One aggregate quality score: rejected because it hides hard failures.
- Evaluator in generator context: rejected due bias and leakage.
- Static field-presence validation: rejected as behavioral evidence.
- Thresholds invented before runs: rejected by A-004 and BD-008.

## Interfaces, Data, And Errors

`CorpusStore`, `CaseAssigner`, `EvaluationRunner`, `EvaluatorPort`, `ScorecardCompiler`, `MaturityRegistry`. Errors include label leakage, subject mismatch, evaluator unavailable, incomplete repetitions, rubric incompatibility, hard-gate failure, and statistical uncertainty.

## Authority, Security, And Determinism

Case assignment, identity, aggregation, and gates are deterministic. Labels are encrypted and separately authorized. Evaluators do not see hidden generator context. Only evaluation governance can change labels/rubrics/thresholds.

## Consequences

Positive: defensible maturity and bounded production claims. Cost: corpus custody, repeated-run expense, statistical analysis, and slower promotion.

## Observability, Performance, Migration

Report distributions, confidence intervals, stability, control lift, cost/latency, disagreement, leakage attempts, and downstream outcomes. Corpus/rubric/threshold changes stale receipts. General certification remains deferred until transfer evidence exists.

## V1.2 Constitutional Alignment Amendment

The accepted isolated benchmark decision is unchanged and its portfolio expands to the fifth category.

| Implementation owner | Component boundary | Data / contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- |
| evaluation_governance_and_architecture | Builder orchestrates isolated evaluation; human governance owns protected labels, rubrics, and thresholds | `ConstitutionalEvaluationReceipt` with activation, role, reaction, expression, visual, narrative, wrong-reading, lineage, syntax, and boundary dimensions | Leakage revokes receipts; any non-compensable failure blocks promotion | conversational protected cases, repeated fresh contexts, hard-gate and leakage fixtures | General certification names exact versions across all five categories and cannot inherit from Format 02 alone | Extends BD-008/HD-007; existing Format 02 corpus and maturity receipts remain valid only for their declared scope |

## Verification

Security tests prove label isolation. Identity tests bind evaluated artifacts. Statistical/gate tests cover repeatability, hard failures, resume, leakage revocation, and Format 02 sequence fidelity.
