# Observability Plan

Emit immutable `ST-01.04:OutcomeVerified` or `ST-01.04:OutcomeRejected` evidence
with `run_id`, `story_id`, evaluation identity/hash, contract identity/hash, Source
Lock and Evidence Index identity/hash, authority identity, version, provenance,
typed outcome, consequence, gap/conflict counts, coverage counts and failure context.

The evaluation event, completion receipt and observation outbox entry are one atomic
commit. Post-commit sink failure retains a retryable outbox item and returns the
committed receipt. Replay returns the same evidence without duplication.
