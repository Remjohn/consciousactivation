# ADR-015: No V2.1 Migration Baseline

Status: `ACCEPTED`

Owners: Architecture and repository authority. Trace: D028 disposition; FR-160 through FR-166; NFR-COMPAT-001; implementation baseline.

## Context

The PRD describes V2.1 as historical brownfield context, but no V2.1 source, schemas, package, workflows, or tests exist inside this repository. Inferring compatibility from documentation or an external sibling directory would create fictional migration obligations.

## Decision

Classify V2.1 implementation migration and compatibility as not applicable for the current repository. Design Builder Next directly from current authority. Preserve future migration hooks for Builder Next schema evolution, but do not implement V2.1 aliases, importers, dual compilation, or regression suites.

## Alternatives

- Reconstruct V2.1 from PRD descriptions: rejected as invented behavior.
- Treat an adjacent unversioned directory as repository baseline: rejected because it is outside the repository authority and delivery boundary.
- Delete all historical references: rejected because they remain architectural context and source-register history.

## Interfaces, Data, And Errors

No V2.1 import interface exists. An attempted legacy import returns `LegacyBaselineUnavailable` with the required evidence list. The invalidation trigger is an authoritative repository-local package with verifiable identity and ownership.

## Authority, Security, And Determinism

Only product/repository authority can add the baseline and reopen migration. External files are never consumed implicitly.

## Consequences

Positive: honest greenfield scope and no invented compatibility. Cost: retained V2.1 behavior may later require re-planning if authoritative artifacts arrive.

## Observability, Performance, Migration

Record no migration telemetry until reopened. On trigger, invalidate FR/NFR classifications, architecture traceability, ADR status, and affected specs before code changes.

## Verification

Repository inventory and CI assert no V2.1 compatibility claim or importer without an approved baseline manifest and source hash.

