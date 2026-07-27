# Implementation scope

Implement additive, category-neutral support that consumes the exact active accepted ST-04.04 internal handoff and the hash-pinned synthetic context input, validates a versioned reference registry and loading policies, compiles the minimum complete context for both phases, applies explicit token/latency/cost budgets, and emits a deterministic complete manifest and receipt.

The implementation must preserve all predecessor identities, authority, provenance, replay, idempotency, invalidation, and atomic rollback. It may calculate and validate context contracts but may not load remote content, call a model, retrieve data, execute a phase, discover skills, compile a JIT capsule, or use conversation history as context.
