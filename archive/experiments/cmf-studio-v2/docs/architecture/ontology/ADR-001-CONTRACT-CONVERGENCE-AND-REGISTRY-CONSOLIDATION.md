# ADR-001: Contract Convergence and Registry Consolidation

Status: accepted

Date: 2026-06-30

## Context

CMF Studio has accumulated powerful but scattered contracts, registries, visual methods, provider rules, primitive systems, and production-stage objects. This makes it hard for agents, operators, providers, and evals to agree on the same vocabulary. The ontology and glossary are now promoted from reference material into canonical architecture artifacts.

## Decision

The Master Ontology and Glossary V1 are canonical. The repo now carries a canonical contract kernel under `src/ccp_studio/contracts/` and canonical registry namespaces under `registries/canonical/`.

Old contracts are adapted instead of deleted. Existing objects such as primitive triads, still visual programs, provider jobs, and composition contracts can continue to work while services project them toward canonical V1 contracts.

Registries are consolidated under `registries/canonical` so production systems can resolve namespaces through a stable manifest and crosswalk instead of reading scattered legacy folders directly.

For short-form workflows, `16:9` is source-only. It may be used as interview footage, B-roll, archive, or source reference, but it must be recomposed into a delivery frame such as `9:16`, `1:1`, or `4:5`.

Provider jobs require source reference, primitive binding, style route, frame profile, composition role, and eval requirements. This prevents loose prompt generation, style averaging, arbitrary metaphors, and untraceable visual outputs.

## Consequences

- Canonical contracts are additive and backward-compatible.
- Legacy contracts need adapters and projections before full migration.
- Provider-facing objects must be source-backed and eval-gated.
- Visual routes become production constraints, not generic style preferences.
- Future contract moves require a migration ADR.
