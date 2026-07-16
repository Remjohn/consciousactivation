# Observability Plan

Emit `ST-03.01:QuestionPackageCompiled`, `ST-03.01:OutcomeVerified`, typed rejection,
replay and invalidation observations with run, Story, graph/package/receipt identity,
authority, versions, Source Lock, saturation and Draft Model provenance, ready/locked
counts, selected decision, outcome and failure context. Commit success observations
through the atomic outbox; sink failure remains retryable and never reports a false
uncommitted result.
