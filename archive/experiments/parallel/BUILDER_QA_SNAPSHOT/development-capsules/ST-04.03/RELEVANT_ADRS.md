# Governing ADRs

- `ADR-001 — Product Boundary And Modular Monolith`: preserve domain/application/adapter boundaries; the phase graph is a product contract, not a service topology.
- `ADR-002 — Separate Harness IR And Workflow IR`: compile declarative phase relationships only; do not execute, schedule, retry, route, or deploy them.
- `ADR-004 — Deterministic Compilation And Schema Evolution`: canonical serialization, hashes, immutable identities, atomic commits, receipts, and invalidation are mandatory.
- `ADR-005 — Human-Agent-Code Authority`: deterministic Builder code compiles; required gates and authority cannot be bypassed through topology.

All four ADRs are accepted. BD-001 remains resolved by the human-ratified Architecture Preservation Contract.
