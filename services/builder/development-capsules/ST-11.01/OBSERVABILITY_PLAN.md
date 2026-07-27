# Observability Plan

Emit deterministic observations for generation start, each section validation, commit, replay, rejection, invalidation and historical load.

Every observation includes `run_id`, `story_id`, artifact identity, authority identity, version, provenance, outcome, failure context, correlation/causation/command IDs, target/profile identity, stream version, AtomicHarnessDefinition identity, ST-07.04 validation identity, Development Capsule identity/hash/receipt, section count, reference count, obligation count, compatibility, classification and replay status.

Payloads must be free of secrets, mutable timestamps, random data and absolute machine paths. Rejection observations may not imply committed state.
