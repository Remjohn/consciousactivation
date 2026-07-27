# ADR-018: Format 02 Asset Demand Boundary

Status: `ACCEPTED`

Owners: Product lead and cross-product architecture. Trace: D004, D014, D030, D032; TS-11, TS-15. Blockers: BD-011, BD-014.

## Context

Format 02 may need character/background/pose/expression assets, but Release 1 must not depend on or implement Visual Asset Editor production behavior. It still needs to prove typed demand and semantic non-mutation boundaries where asset interaction affects the harness.

## Decision

Use a contract-tested stub `AssetDemandPort` backed by approved fixtures. Builder compiles demand contracts and validates responses/provenance but does not generate/edit assets. The port may be omitted only if product authority proves the reference slice has no asset dependency.

## Alternatives

- Build/integrate production Visual Asset Editor: rejected by frozen product boundary and Release 1 scope.
- Ignore asset needs: rejected if it makes the reference path non-representative.
- Free-form file exchange: rejected because provenance and semantic authority are untestable.

## Interfaces, Data, And Errors

`AssetDemand { semantic_intent_ref, asset_kind, constraints, continuity_state, provenance_requirements, content_owned_fields }`; `AssetResponse { demand_ref, asset_refs, provenance, compatibility, warnings }`. Errors include unsupported demand, semantic mutation, missing provenance, incompatible version, and unavailable fixture.

## Authority, Security, And Determinism

Content-owned semantic intent is immutable downstream. Fixtures are hash-locked and non-executable. No editor credentials/network enter Builder.

## Consequences

Positive: realistic boundary proof without cross-product implementation. Cost: interface snapshots, fixtures, and contract tests that may later evolve with the editor owner.

## Observability, Performance, Migration

Record demand/response identities, compatibility, provenance, latency, and boundary violations. Replacing the stub with an external adapter requires contract equivalence and a new/updated ADR.

## V1.2 Constitutional Alignment Amendment

The accepted stubbed Asset Demand boundary is unchanged and now requires explicit activation-first visual lineage.

| Implementation owner | Component boundary | Data / contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- |
| format_02_slice_and_cross_product_architecture | Builder validates demand/response fixtures only; editor and Delegation runtimes remain external | Asset Demand refs to Activative Intelligence Pack, Visual Semantic Pack, Visual Narrative Program, feature contracts, Composition Asset Pack, Visual Syntax handoff, and T/V route request | Reject missing lineage, semantic mutation, absent provenance, incompatible version, or runtime code | enriched fixture round-trip, hash/provenance, semantic non-mutation, and no-editor-code tests | Every demand resolves exact upstream semantic/narrative refs and the stub proves boundary behavior without execution | Additive fixture/schema version; no production editor dependency or ADR-014 scope change |

## Delegation RC3 Demand Addendum

The stub now targets the exact RC3 Visual Asset Demand 1.1 contract. All required semantic domains remain structured, and wrong-reading locks are monotonic across demand derivation.

| Implementation owner | Component boundary | Data / contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- |
| format_02_slice_and_cross_product_architecture | Builder emits demand and inheritance constraints; VAE realizes them; Delegation owns the wire schema | RC3 Visual Asset Demand, `ACTIVATIVE_LINEAGE_MAPPING.yaml`, `WRONG_READING_LOCK_INHERITANCE.yaml` | Reject missing/flattened lineage, empty locks, removed/weakened inherited locks, or in-place relaxation | 14-field lineage, generic-notes prohibition, parent-subset, stricter derivative, and new-version relaxation tests | A valid stub demand preserves each required artifact in its RC3 field and every derivative contains all parent locks | Existing fixtures require additive remapping to RC3; relaxation creates a new upstream demand version; no VAE or Delegation implementation enters Builder |

## Verification

Tests cover valid demand, missing/invalid provenance, semantic mutation, incompatible version, external unavailability, and proof that no editor runtime code exists in Builder.
