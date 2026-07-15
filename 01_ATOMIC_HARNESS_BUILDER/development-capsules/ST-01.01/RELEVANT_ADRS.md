# Relevant Accepted ADRs

## Direct implementation decisions

### ADR-001 — Product Boundary and Modular Monolith

Source: `docs/architecture/adr/ADR-001-PRODUCT-BOUNDARY-AND-MODULAR-MONOLITH.md`

Use strict domain, application, and adapter boundaries. Domain code is deterministic and imports no adapters. Application commands are the transaction and authority seam. No VAE, Delegation, generated-harness, provider, or workflow-runtime behavior may enter the Story.

### ADR-003 — Authoritative State and Artifact Storage

Source: `docs/architecture/adr/ADR-003-AUTHORITATIVE-STATE-AND-ARTIFACT-STORAGE.md`

Preserve event-stream, optimistic-concurrency, idempotency, snapshot, and replay semantics behind ports. This bounded Story uses a deterministic in-memory adapter for verification only. It does not claim production persistence parity, create PostgreSQL migrations, or authorize a production store.

### ADR-005 — Human-Agent-Code Authority

Source: `docs/architecture/adr/ADR-005-HUMAN-AGENT-CODE-AUTHORITY.md`

Every command has a primary actor class. Deterministic code validates and commits; only properly granted human authority may waive, ratify, or authorize. Unauthorized requests return typed denial and append no authoritative event.

### ADR-014 — Format 02 Release 1 Reference

Source: `docs/architecture/adr/ADR-014-FORMAT-02-RELEASE-1-REFERENCE.md`

Bind this capsule to Format 02 under 2D Character Animation. Reference status does not imply benchmarking or certification. Other categories and external targets remain structural and non-executable in this bounded slice.

## Compatibility and negative-boundary decisions

- ADR-002 (`docs/architecture/adr/ADR-002-SEPARATE-HARNESS-IR-AND-WORKFLOW-IR.md`): no Harness IR or Workflow IR is introduced by this Story; run state must not become hidden workflow state.
- ADR-006 (`docs/architecture/adr/ADR-006-WORKFLOW-ENGINE-ADAPTER.md`): no workflow engine or Temporal dependency is permitted.
- ADR-013 (`docs/architecture/adr/ADR-013-TARGET-COMPILERS-AND-EXTERNAL-BOUNDARIES.md`): external target identities may be recognized structurally; Builder must not activate external target runtimes.
- ADR-017 (`docs/architecture/adr/ADR-017-RELEASE-1-WORKFLOW-PROFILES.md`): workflow-profile implementation is later scope and is not required by ST-01.01.

All referenced ADRs remain accepted and unmodified by this capsule.

