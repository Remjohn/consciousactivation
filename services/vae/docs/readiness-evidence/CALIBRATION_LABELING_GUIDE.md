# Calibration Labeling Guide

Status: `ready_for_operator_corpus`  
Classification: `non_production_readiness_proof`

This guide produces human reference labels for the Format 02 evaluator. It does not define final thresholds and does not certify an evaluator.

## Roles and blinding

Each case is labeled independently by at least two trained annotators and resolved by an adjudicator. Annotators receive the pinned authority context and rubric version, but not another annotator's result or the evaluator-under-test output. The evaluator under test may not author the reference label.

## Case-level decision

Choose exactly one:

- `accept`: semantic, feature, composition and technical obligations survive all applicable gates.
- `targeted_repair`: the defect is specific, VAE-owned and repairable without changing upstream intent.
- `upstream_repair_required`: the VAE cannot safely repair the authoritative semantic or Feature Contract input.
- `reject_non_repairable`: the result violates a non-compensable obligation or cannot be repaired within the approved proof.

Do not use a high score in one dimension to excuse a wrong-reading lock, identity drift, wrong visible action, missing required lineage, Feature Contract mutation, or an applicable no-text/delete-caption failure.

## Dimension labels

For each applicable dimension—zero-second hook, pattern-match strength, pattern-interrupt strength, viewer-role clarity, activation direction, prediction gap, payoff, affinity, anticipation residue, anti-cliché strength, wrong-reading risk, Feature Contract compliance and delete-caption/no-text survival—record:

1. `meets`, `does_not_meet`, `uncertain`, or `not_applicable`;
2. image region or whole-image evidence;
3. concise authority-linked rationale;
4. confidence: `high`, `medium`, or `low`;
5. responsible layer and repairability.

No numeric cutoff is implied by these categorical labels.

## Required failure families

- Wrong visible action: depicted behavior conflicts with the Activation Contract or T/V route.
- Identity drift: controlled character identity, DNA or approved premise is materially altered.
- Composition failure: hierarchy, viewer role, hook or narrative program cannot be read as required.
- Technical defect: corrupt output, clipping, seams, anatomy artifact, invalid dimensions or similar production failure.
- Wrong-reading lock violation: label every violated lock separately; never collapse to a generic semantic failure.
- No-text/delete-caption failure: removing text destroys the required activation when the gate applies.
- Feature Contract failure: realization mutates or fails authoritative semantic feature intent.
- Interview-lineage failure: required provenance is missing for `interview_expression`, or provenance is invented for another source kind.

## Recurrence

Label repeated structure `beneficial_recurrence` only when it strengthens recognition, activation, payoff or controlled anticipation without flattening novelty. Label `redundant_recurrence` when repetition adds no semantic value or weakens pattern interrupt, anti-cliché strength or affinity. Cite the compared cases.

## Repair responsibility

- `vae_realization`: composition, render, technical production, feasibility finding or realization receipt.
- `content_harness`: authoritative feature intent or semantic requirement.
- `delegation_boundary`: invalid or unenforceable request/result contract.
- `evaluator_program`: rubric, applicability, program bug or unsupported output.
- `infrastructure`: runtime, transport, storage or compute defect; this does not consume a quality-repair round.
- `not_repairable_in_scope`: no authorized layer can repair within this proof.

## Adjudication and audit

Retain both original labels, disagreement codes, adjudicator decision, rationale, rubric/version pins and timestamps. Do not silently overwrite labels. Review false positives and false negatives by family, severity, responsible layer and evaluator/program version. Cases with unresolved authority ambiguity are excluded from threshold calibration and logged as blockers.

