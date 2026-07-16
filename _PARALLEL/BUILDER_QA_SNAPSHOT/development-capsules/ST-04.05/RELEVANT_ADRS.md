# Governing ADRs

- `ADR-001 — Product Boundary And Modular Monolith`: preserve domain/application/adapter boundaries; context compilation is Builder-owned product behavior, not an external service.
- `ADR-002 — Separate Harness IR And Workflow IR`: compile declarative context artifacts only; do not execute phases or workflows.
- `ADR-004 — Deterministic Compilation And Schema Evolution`: canonical serialization, content identities, atomic commits, receipts, compatibility, and invalidation are mandatory.
- `ADR-005 — Human-Agent-Code Authority`: deterministic code validates and commits; subordinate actors cannot approve or mutate governed context.
- `ADR-009 — Skill Ecology And JIT Capsules`: use the approved empty registry only as an immutable synthetic input; do not implement skill registry or JIT capsule behavior.

All five ADRs are accepted. BF-AM-006 closes BD-010 only for this bounded synthetic Core mode.
