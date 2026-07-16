# Governing ADRs

- `ADR-001 — Product Boundary And Modular Monolith`: preserve strict domain/application/adapter boundaries; modules represent cohesive product responsibility, not services or horizontal database/API/UI/router/agent layers.
- `ADR-002 — Separate Harness IR And Workflow IR`: module outputs remain Harness product architecture and contain no Builder worker, queue, retry, sandbox, or deployment state.
- `ADR-004 — Deterministic Compilation And Schema Evolution`: use canonical serialization, content hashes, immutable identities, atomic commits, explicit compatibility, and receipt-backed invalidation.
- `ADR-005 — Human-Agent-Code Authority`: deterministic Builder code validates and commits; owner-kind and failure ownership remain explicit; agents or externals cannot acquire authority through module topology.

All four ADRs are accepted. BD-001 was resolved by the human ratification of the Architecture Preservation Contract on 2026-07-14.
