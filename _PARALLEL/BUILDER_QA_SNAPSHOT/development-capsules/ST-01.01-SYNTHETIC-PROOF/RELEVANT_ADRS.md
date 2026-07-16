# Relevant accepted ADRs

- `ADR-001 — Product Boundary and Modular Monolith`: preserve the Builder as the product and keep final Harness execution and external product behavior outside this branch.
- `ADR-005 — Human, Agent, and Code Authority`: human confirmation activates the planning amendment; a second exact human phrase is still required before implementation. Code enforces only declared authority.
- `ADR-009 — Skill Ecology and JIT Capsules`: use the approved, versioned, hash-pinned empty registry only for deterministic code-owned proof capabilities; undeclared skills fail closed.
- `ADR-013 — Target Compilers and External Boundaries`: retain `atomic_content_harness` as an existing target and do not implement VAE or Delegation runtime behavior.

Exact files:

- `docs/architecture/adr/ADR-001-PRODUCT-BOUNDARY-AND-MODULAR-MONOLITH.md`
- `docs/architecture/adr/ADR-005-HUMAN-AGENT-CODE-AUTHORITY.md`
- `docs/architecture/adr/ADR-009-SKILL-ECOLOGY-AND-JIT-CAPSULES.md`
- `docs/architecture/adr/ADR-013-TARGET-COMPILERS-AND-EXTERNAL-BOUNDARIES.md`

All four ADRs remain accepted and unmodified. This capsule provides a bounded application of their existing authority; it does not amend them.
