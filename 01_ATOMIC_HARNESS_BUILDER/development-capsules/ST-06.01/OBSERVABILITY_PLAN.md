# Observability Plan

Emit deterministic observations for category-binding commit, replay, and rejection.
Every observation records story ID, command ID, Harness identity/version, actor,
category or `NOT_APPLICABLE`, registry version/hash, binding identity/hash, outcome,
failure code, and correlation/causation IDs. The completion receipt must bind focused
and full-regression results to these observations.

