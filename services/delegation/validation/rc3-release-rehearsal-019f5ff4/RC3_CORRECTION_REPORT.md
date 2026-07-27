# Delegation 1.1.0-rc.3 Identity and Packaging Correction Report

Date: 2026-07-14  
Correction class: RELEASE_IDENTITY_AND_PACKAGING  
Contract-behavior change: NONE  
Production authorization: false

## Correction

The three stale distributed package declarations are corrected to the current
candidate identity. All generated registries, compatibility fixtures, package
metadata, manifests, and receipts are regenerated from the canonical producer
sources. Generated Python and TypeScript bindings now expose explicit package,
protocol, Visual Asset Demand, and compatibility-profile version constants.

The shipped identity validator scans every UTF-8 release file and every JSON or
YAML `package_version` declaration. It rejects stale active package identities
and permits predecessor identifiers only in explicitly marked historical
changelog or rejection evidence.

## Intentionally distinct version axes

- Package release: `1.1.0-rc.3`
- Delegation envelope protocol: `1.0`
- Compatibility profile: `1.0`
- Visual Asset Demand contract: `1.1`
- All other unchanged message/schema versions: `1.0`

## Semantic preservation

No schema behavior, field requirement, authority owner, lifecycle transition,
adapter effect, migration transformation, or engine behavior was changed.
Regression gates pin the RC2 Visual Asset Demand schema, example, migrations,
and Format 02 boundary scenarios by SHA-256. Source-kind, interview provenance,
Expression Moment and Reaction Receipt lineage, wrong-reading-lock,
parse-without-enforcement, lifecycle, replay, cancellation, amendment,
supersession, replacement, and Delegation Set tests remain mandatory.

## Publication boundary

This candidate is local and unsigned. Trust roots, signing, owner ratification,
and operational integration remain external blockers. Production authorization
remains false.
