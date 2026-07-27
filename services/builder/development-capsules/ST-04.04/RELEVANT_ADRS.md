# Governing ADRs

- `ADR-001 — Product Boundary And Modular Monolith`: preserve domain/application/adapter boundaries; handoffs are governed product contracts, not service topology.
- `ADR-002 — Separate Harness IR And Workflow IR`: compile declarative internal context and handoff contracts only; do not execute or orchestrate them.
- `ADR-004 — Deterministic Compilation And Schema Evolution`: canonical serialization, immutable identities, compatibility, atomic commits, receipts and invalidation are mandatory.
- `ADR-005 — Human-Agent-Code Authority`: ownership and mutation authority must be explicit and fail closed.
- `ADR-013 — Target Compilers And External Boundaries`: external-product handoffs remain out of scope and BD-014 remains open; no shared schema is copied or forked.

All five ADRs are accepted. BF-AM-005 authorizes only the Builder-internal handoff mode without BD-014; it does not authorize an external-product branch.
