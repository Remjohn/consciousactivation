# Format 02 Evaluation Prompt Template

Classification: `non_production_readiness_proof`

Evaluate only observable evidence against the immutable demand and the supplied constitutional contracts. Do not infer missing intent, source provenance, Feature Contract meaning, or wrong-reading permissions.

For each applicable dimension, return one categorical label from `clear_pass`, `borderline`, `clear_fail`, `uncertain`, or `not_applicable`, plus concise evidence. Evaluate each wrong-reading lock individually. Report Feature Contract reference preservation separately from realization compliance. Run delete-caption/no-text evaluation only when its applicability rule is true.

If any required input, evaluator identity, program identity, or evidence context is unresolved, abstain and fail closed. Do not convert categorical findings into a production threshold. Identify the earliest responsible layer and whether repair is VAE-owned, upstream-owned, or an infrastructure retry.

Output must preserve candidate identity, demand identity, evaluator/program pins, applicability decisions, all findings, gate results, responsible-layer routing, and uncertainty. This template confers no certification or production authority.
