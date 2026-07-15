# Relevant Accepted ADRs

- **ADR-001 — Product boundary and modular monolith:** Builder compiles governed packages; external runtimes remain outside this repository.
- **ADR-002 — Separate Harness IR and Workflow IR:** the definition references the governed Phase Graph/execution plan and does not implement workflow runtime or collapse distinct IR families.
- **ADR-003 — Authoritative state and artifact storage:** immutable identity, atomic commit, replay, invalidation, and historical reproduction apply.
- **ADR-004 — Deterministic compilation and schema evolution:** canonical bytes, versioned contracts, same-input equality, changed-input identity, and compatibility behavior apply.
- **ADR-005 — Human, agent, code, and external authority:** compilation, ratification, mutation, and downstream ownership remain explicit and fail closed.
- **ADR-013 — Target compilers and external boundaries:** three target kinds remain distinct; this capsule activates only the generic `atomic_content_harness` path and imports no VAE or Delegation runtime.

ADR-014 and ADR-018 remain relevant to the later Format 02 reference branch only and are not activated here.

