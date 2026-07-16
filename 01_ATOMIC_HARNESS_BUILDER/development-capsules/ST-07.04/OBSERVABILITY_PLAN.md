# Observability Plan

Emit deterministic Story-scoped observations for validation start, dimension evaluation, committed PASS report, idempotent replay, typed rejection and descendant invalidation.

Every success event includes run, Story, command, definition and validation report identities/hashes; target/profile; validation dimension count; artifact/section counts; authority; lineage; internal compatibility; external compatibility disposition; certification state; outcome and replay state.

Failure events include typed failure code and bounded context without secrets, protected material, local paths or external runtime data. Failed atomic commits persist no observations. Invalidation events identify the upstream definition invalidation and preserve historical reproduction state.

Evidence is supplied by acceptance, failure, replay/invalidation and architecture tests and summarized in the completion observability artifact.
