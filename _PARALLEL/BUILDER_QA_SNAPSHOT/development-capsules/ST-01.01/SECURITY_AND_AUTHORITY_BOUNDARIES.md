# Security and Authority Boundaries

## Actor authority

- Deterministic code validates commands, transitions, profile identity, stream version, idempotency and checkpoint validity.
- A human Harness Architect/operator may create and resume a run only through an exact scoped grant.
- Lifecycle waivers require an authenticated human authority, exact scope, rationale, affected gates, risk, expiry and receipt.
- Agents may propose commands but cannot grant authority, ratify decisions, waive gates, issue implementation authorization, or commit state directly.
- Evaluators, VAE and Delegation actors have no command authority in this Story.

Every denial is attributable and observable. Denial must not append an authoritative event or disclose credentials, protected evidence or internal policy data beyond the typed reason needed for correction.

## Deny-by-default resource boundary

The implementation has no network, secret, database, subprocess worker, external source, Human Reaction data or protected benchmark access. It may read only the governed input files listed in `ALLOWED_FILE_SCOPE.yaml` and write only exact implementation/test/completion paths.

If a target/profile implies Human Reaction input, VAE realization, Delegation execution, external contract compilation, protected evaluation or production certification, the command fails closed. HD-006 and HD-007 are non-applicable because the authorized Format 02 path collects no Human Reaction material and performs no conversational certification; this does not resolve or waive those decisions for conversational profiles.

## Product and constitutional boundary

- Format 02 is `contract_compatible`, not benchmarked, limited-production certified or production certified.
- `visual_asset_editor` and `content_asset_delegation_contract` are structural target identities only.
- Delegation `1.1.0-rc.4` is the active program pin but is not a direct ST-01.01 dependency and is not imported, copied or locally forked.
- No generated harness logic, creative logic, evidence semantics, profile compiler, workflow engine, Control Tower, VAE or Delegation runtime is permitted.
- This package cannot change full Release 1 or full-product readiness from `FAIL`.

## Implementation authority

Capsule validation establishes bounded readiness, not permission to modify code. Only the exact human phrase in `IMPLEMENTATION_AUTHORIZATION.yaml`, received after this package is issued and while hashes remain valid, authorizes the bounded implementation turn. Any hash, scope, authority or dependency change invalidates that authorization and requires a new disposition.

