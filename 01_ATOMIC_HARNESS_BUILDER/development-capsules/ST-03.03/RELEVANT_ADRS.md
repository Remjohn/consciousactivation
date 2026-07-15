# Governing ADRs

## ADR-002 — Separate canonical Harness IR and Builder Workflow IR

Path: `docs/architecture/adr/ADR-002-SEPARATE-HARNESS-IR-AND-WORKFLOW-IR.md`  
SHA-256: `4d29f9dbe84946f56d8529533dd3be6208378c3eadfee32257bf69617fe1ce09`

This is the Story-owned architecture decision. Harness IR and Workflow IR have separate identities, schemas, migrations, compilers, and authority. Harness IR rejects worker, queue, retry, sandbox, and deployment state.

## ADR-004 — Deterministic compilation and schema evolution

Path: `docs/architecture/adr/ADR-004-DETERMINISTIC-COMPILATION-AND-SCHEMA-EVOLUTION.md`  
SHA-256: `e2cd894d1db6f165c4952cd7126924d1a6761e3c232f1dbd5e4e120dc8fcb71b`

Canonical serialization, content hashes, immutable identities, explicit compatibility/migration registries, atomic snapshots, and golden vectors govern the implementation. Artifact-set compilation remains outside this Story.

## ADR-005 — Human-agent-code authority

Path: `docs/architecture/adr/ADR-005-HUMAN-AGENT-CODE-AUTHORITY.md`  
SHA-256: `783835d294590b52737f841adf59f588bce41bbae4fd3d2e0b7ddcc425aaf92e`

The prior human ratification supplies semantic authority. Deterministic code compiles exact governed values; no agent, evaluator, external actor, or direct caller may promote or replace them.

All accepted ADRs remain unchanged. This capsule does not supersede an ADR.
