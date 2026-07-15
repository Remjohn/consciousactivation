# ADR-008: Visual Inference And Knowledge Status

Status: `ACCEPTED`

Owners: Visual architecture, category steward, and benchmark team. Trace: D007, D008, D023, D030, D031; TS-03, TS-04. Blockers: BD-004, BD-007.

## Context

Visual Syntax First requires deterministic geometry and bounded multimodal inference without collapsing observation into meaning. Provider accuracy, cost, privacy, and category performance must be measured rather than assumed.

## Decision

Use a provider-neutral `VisualInferencePort` with task-specific typed outputs. Run deterministic normalization/geometry first, then bounded provider parsing, independent validation, and cross-specimen induction. Store measured observations, deterministic derivations, hypotheses, human decisions, and generated proposals as distinct knowledge statuses.

Provider selection remains empirical: compare at least two adapters plus the deterministic baseline on protected Format 02 cases. No provider receives canonical write authority.

## Alternatives

- One fixed model embedded in domain code: rejected for portability and evaluation.
- Model-only parsing: rejected because geometry/provenance must be deterministic.
- Human-only annotation: rejected as the only production path due cost and repeatability, but retained for goldens/adjudication.
- Free-form model text: rejected because typed contracts and confidence are mandatory.

## Interfaces, Data, And Errors

`parse(task, artifacts, ontology, output_schema, budget) -> ProviderObservation`. Records include provider/model/policy/capsule identity, evidence references, confidence, alternatives, latency, and cost. Errors include decode, schema, low confidence, provider disagreement, privacy restriction, budget, and provider unavailable.

## Authority, Security, And Determinism

Adapters receive only authorized derived media. PII/redaction occurs before remote calls. Raw output is non-authoritative. Ontology/category changes require human ratification.

## Consequences

Positive: replaceable providers, measurable quality, and protected knowledge integrity. Cost: adapter/evaluation work, multiple passes, and uncertain thresholds until prototype results.

## Observability, Performance, Migration

Measure geometry error, temporal boundary error, schema repair, agreement, calibration, latency, tokens, cost, and cache reuse. Parser/model version changes invalidate dependent parses and maturity. No legacy parser migration applies.

## V1.2 Constitutional Alignment Amendment

The accepted provider-bounded inference decision is unchanged. Visual Syntax First is the harness-development evidence order; Activation First is the runtime semantic order.

| Implementation owner | Component boundary | Data / contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- |
| visual_architecture_and_category_steward | Parser emits observation/function hypotheses only; runtime visual semantics must enter from a frozen Activative Intelligence Pack | knowledge status, syntax evidence, Activative pack ref, Visual Semantic Pack, Visual Narrative Program | Reject semantic promotion, runtime-order inversion, or downstream invention | dual-order, rich-lineage, and provider-disagreement fixtures | Development parsing precedes hypotheses while runtime chain remains Activation First and source-backed | Clarifies current decision; existing observations remain valid and need no reclassification unless authority was over-promoted |

## Verification

Golden and adversarial cases verify coordinate fidelity, BBOX/WHY separation, temporal syntax, disagreement handling, label isolation, provider failure, and category-native quality.
