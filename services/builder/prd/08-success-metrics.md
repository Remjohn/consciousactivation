---
title: PRD 08 — Success Metrics and Counter-Metrics
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
section: 08
---

# 8. Success Metrics and Counter-Metrics

Exact numeric thresholds that require empirical calibration remain Architecture and benchmark work. The PRD defines what must be measured and which failures can never be averaged away.

## Primary and secondary metrics

| ID | Metric | Target or definition |
| --- | --- | --- |
| SM-01 | Unsupported constitutional decision rate | 0 critical unsupported decisions in any release-gate reference run; target <1% material decisions requiring post-implementation correction. |
| SM-02 | Atomicity classification accuracy | Meet the category-specific threshold on protected merge/split/variant/family cases; no critical boundary error in the primary reference harness. |
| SM-03 | Visual-syntax accuracy | Meet protected benchmark thresholds for salient component recall, relationship accuracy, composition-variable classification, and cross-specimen invariant precision. |
| SM-04 | Implementation invention rate | Fewer than 5% of implementation-blocking decisions are invented outside the authorized Development Capsule in the reference slice. |
| SM-05 | First-pass implementation readiness | At least 90% of Development Capsule acceptance checks pass before implementation begins; all blockers are explicit. |
| SM-06 | Skill behavioral lift | Every required production skill or adaptation demonstrates statistically meaningful lift over its no-guidance control on its target behavior. |
| SM-07 | JIT context efficiency | Required capsules meet their phase completeness criteria while reducing irrelevant or inactive context against the monolithic baseline. |
| SM-08 | Downstream harness effectiveness | Each certified profile meets its category-native baseline on accuracy, Activative fidelity, role/reaction integrity, Expression Moment provenance where applicable, wrong-reading rate, first-pass acceptance, latency, and cost per accepted output. |
| SM-09 | Repair localization | At least 90% of benchmarked failures are repaired without rerunning unaffected constitutional or evidence phases. |
| SM-10 | Run observability completeness | 100% of mandatory lifecycle, semantic-lineage, Reaction Receipt, Expression Moment, external handoff, repair, benchmark, waiver, and authorization transitions produce valid events and receipts. |
| SM-11 | Builder release stability | Required stochastic benchmark dimensions meet both mean and minimum thresholds with bounded variance across fresh-context repetitions. |
| SM-12 | V2.1 migration safety | No retained V2.1 capability regresses without an approved deprecation or replacement receipt; all existing supported artifacts are readable or migratable. |
| SM-13 | Workflow autonomous completion rate | Measure the percentage of reference and transfer runs that complete all non-human-gated nodes without unplanned operator intervention while preserving every hard gate. |
| SM-14 | Workflow route accuracy | The selected workflow profile must match expert-labeled request, risk, target, and incident classes on protected routing cases, with zero critical hotfix-versus-normal-flow errors. |
| SM-15 | Workflow failure containment | 100% of benchmarked node failures preserve locked evidence, ratified decisions, protected cases, and unaffected branch state. |
| SM-16 | Cost and latency per authorized capsule | Track p50/p95 end-to-end and per-node latency, deterministic compute, model tokens, retries, and total cost for each authorized Development Capsule and workflow profile. |

## Counter-metrics — do not optimize

| ID | Counter-metric | Why it is dangerous |
| --- | --- | --- |
| SM-C01 | Artifact count | More generated documents are not evidence of quality and must not be optimized. |
| SM-C02 | Question count | A larger Genesis tree is not intrinsically better; ask only dependency-relevant decisions. |
| SM-C03 | Canonical skill count | Skill proliferation is a failure mode, not a success metric. |
| SM-C04 | Total context tokens | Consuming more context must not be mistaken for deeper understanding. |
| SM-C05 | Composite score alone | A high average must never conceal a hard evidentiary, constitutional, atomicity, or contract failure. |
| SM-C06 | Automation percentage | More autonomous decisions are not better when authority should remain human or deterministic. |
| SM-C07 | Agent and sandbox count | More agents, candidates, worktrees, or sandboxes do not imply a better workflow and must not be optimized independently of accepted quality and cost. |
| SM-C08 | Fastest candidate completion | The first finished candidate must not win unless it also satisfies the declared quality, evidence, contract, and authorization gates. |

## Hard-gate principle

The Builder may calculate composite trend scores, but the following classes remain non-compensable: unsupported constitutional decisions, critical evidence failures, wrong atomicity, contract contradictions, silent knowledge promotion, untested required skills, benchmark leakage, false readiness, category flattening, and anti-goal violations.
