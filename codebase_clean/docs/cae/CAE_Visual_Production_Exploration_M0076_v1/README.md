# M0076 — Exploratory Canvas Reference

This directory is an isolated behavioral extraction for DramaClaw-style visual exploration. It is **not** a second CAE storyboard authority and does not persist, invoke, or mutate canonical CAE production state.

## Boundary

Allowed: campaign extraction/reference artifacts, an isolated exploration reference component, and focused tests.

Not included: UI, database migrations, runtime/MCP integrations, canonical storyboard changes, model gateway changes, asset/retrieval authority changes, or copied DramaClaw source.

## Design invariants

1. Exploration is reversible and revisioned.
2. Agent canvas commands require explicit operator approval and deterministic validation.
3. Node history is immutable; restore records a new action rather than rewriting history.
4. Locked nodes reject mutation.
5. Stale revision commands reject without mutation.
6. Branches are descriptors over exploration state, not canonical state.
7. A run operation records an exploration proposal only.
8. Promotion creates a request with canonical references, provenance, and an operator receipt; it does not mutate canonical state.
9. The reference is pure in-memory code so it cannot silently become a second persistence or authority layer.

See `DRAMACLAW_UPSTREAM_TO_CAE_MAPPING.md` for source paths, license boundary, adopted/excluded behavior, and evidence classifications.
