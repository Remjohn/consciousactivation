# Implementation scope

Implement one deterministic Builder-internal compiler that consumes the exact active ST-04.03 Phase Graph plus the hash-pinned synthetic handoff input and atomically emits:

- immutable phase-context contracts and an aggregate Context Graph;
- one versioned typed phase-to-phase handoff contract;
- a content-addressed internal handoff graph and receipt;
- ownership, authority, provenance, compatibility, mutation and invalidation validation;
- replay-safe observations, idempotency, conflict rejection and descendant-only invalidation.

The compiler declares context; it does not choose minimum-complete context, calculate budgets, load or unload runtime data, execute phases, or hand data to an external product. BD-014 remains open for external-product branches.
