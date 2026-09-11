# PRD → Tech Spec → Plan → Mandate → Gemini Execution Process

This bundle follows the repository-native ordering observed in the current PRD, Composer tech spec, mandate precedent, and one-harness execution prompt.

## Stage 1 — PRD authoring

The product requirement is written or revised first. The current PRD explicitly requires durable changes to be reflected in the same session and records verified/unverified state.

Output: accepted PRD delta or updated PRD section.

## Stage 2 — Brownfield technical specification

The technical spec identifies exact authorities, current code state, dependencies, output paths, acceptance criteria, and gaps. It may explicitly preserve unknowns rather than inventing missing source text.

Output: accepted technical specification.

## Stage 3 — Master execution plan

The plan turns the spec into bounded implementation units with dependencies, outputs, verification, and operator gates.

Output: frozen workstream/mandate sequence.

## Stage 4 — Mandate

Each mandate is one bounded engineering change. A mandate must name the problem, verified current state, exact change boundary, authorized/prohibited work, tests, evidence, and stop conditions.

Output: `Mxx_*.md`.

## Stage 5 — Gemini activation

The activation prompt is the execution wrapper for one mandate. It follows the established one-run discipline: load authority, inspect current state, plan, execute, reread, verify, report, stop. It does not decide architecture outside the mandate.

Output: execution receipt, changed files, tests, evidence, claim state, commit.

## Stage 6 — Operator gate

The Operator accepts, rejects, or blocks the result. Acceptance is based on actual evidence, not the presence of a green status or a receipt.

## Stage 7 — Documentation maintenance

When execution changes durable product or technical truth, the relevant PRD/spec/gap surfaces are updated in the same session according to repository convention.
