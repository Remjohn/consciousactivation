# Prompt 02 Source-Gate Hotfix — P02-SRC-001

## Cause

The AHP exact source-reuse crosswalk classifies `SRC-EXT-001` as `reference_only`, but three historical spec assignment briefs list it under a “Mandatory files and sources to read” heading. Prompt 02 V3 treated every unresolved named path as blocking, so it incorrectly promoted an optional research reference into a required source gate.

## Correct disposition

Unless the operator supplies and hash-locks the exact PDF, classify `SRC-EXT-001` as `DEFERRED_REFERENCE`. Record a source-gap notice, prohibit claims attributed to the missing paper, and allow the affected specifications to proceed using their current authoritative and implementation sources.

Affected specs:

- `TS-AHP-007`
- `TS-AHP-008`
- `TS-PM-001`

## Rerun rule

Rerun Prompt 02 validation after adding the operator decision below. Prompt 03 may start only when Prompt 02 passes with no unresolved **required** source path.
