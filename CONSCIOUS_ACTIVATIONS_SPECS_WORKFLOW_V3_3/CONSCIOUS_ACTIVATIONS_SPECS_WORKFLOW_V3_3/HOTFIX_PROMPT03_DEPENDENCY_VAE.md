# Hotfix V3.2 — Prompt 03 Dependency-Stage and VAE Write-Authority Correction

## Why Prompt 03 stopped

The controller followed two conflicting rules:

1. The lifecycle Skill said upstream accepted/build receipts were required, without distinguishing WRITE, ACCEPTANCE, and BUILD dependency stages.
2. Prompt 03 explicitly prohibited acceptance during the writing factory.

This made 118 ordinary specification dependencies impossible to satisfy while 57 of 60 specs remained queued.

A second conflict placed `TS-VAE-BOUND-001` in `02_VISUAL_ASSET_EDITOR/docs/tech-specs/`, while the current VAE `AGENTS.md` permits writes only under `docs/constitutional-alignment/` and `PROGRAM_STATUS_EXPORT.yaml`.

## Correct law

- WRITE dependencies are satisfied by a hash-pinned upstream draft, accepted spec, or governed write-time contract seed.
- ACCEPTANCE dependencies are enforced at independent re-audit and hash lock.
- BUILD dependencies are enforced only before implementation.
- Specs are written in topological waves, parallel inside each wave.
- Disallowed product-local specs are written as Program Control cross-product proposals and remain non-buildable until product adoption.

## Immediate next action

Run `PROMPT 02B — Spec Writing Dependency and Repository Authority Correction`, then rerun corrected Prompt 03.

Do not rerun Prompt 01 or broad Prompt 02 when their existing receipts and source locks still validate.
