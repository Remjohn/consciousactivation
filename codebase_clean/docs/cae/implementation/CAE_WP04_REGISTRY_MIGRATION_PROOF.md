# CAE WP-04 Registry Migration Proof

**Work package:** WP-04 — SDA / SFL / Primitive registries and crosswalks
**Status:** `COMPLETE_PENDING_OPERATOR_REVIEW`
**Environment:** Supabase staging PostgreSQL 17.6
**Date:** 2026-08-24

## Bounded objective

Import inherited registry inputs as immutable, version-aware data assets, not
as prompt text or a replacement for existing service authority. The package
does not interpret or repair source concepts.

| Input source | Imported records | Result |
|---|---:|---|
| Supplied SDA ZIP | 13 | 13 imported; no internal reference defect found |
| Supplied SFL ZIP | 28 | 23 imported; 5 affected failure assets quarantined |
| AIR Primitive snapshot | 243 | 241 imported; 2 duplicate-identity records quarantined |

## What changed

- Added immutable staging tables for registry import runs, snapshots, source
  records, resolved/unresolved references, integrity issues, and an append-only
  reference-classifier disposition ledger.
- Imported raw YAML text, parsed payload, archive/source hashes, original IDs,
  source paths, explicit record versions where supplied, and inherited
  registry-version context where a record has no explicit version.
- Added a typed read-only `RegistryResolver` which requires a pinned snapshot
  ID and refuses missing, quarantined, or ambiguous identities.

Migration checksums:

| Migration | SHA-256 | Result |
|---|---|---|
| `0005_cae_registry_authority` | `9a7724013676b08cc4f0cb454bfb7aef0d075a90cbd58808cb59fd718a8d1793` | Applied |
| `0006_cae_registry_reference_classifier_correction` | `20c6f9605ff3f9f372a763a6dc327cc15ba3651ce03a6d6a86a5eb4425670a7f` | Applied |
| `0007_cae_registry_reference_classifier_v2` | `94352d602539bfe44071a204b665facafa53b453d334c3c597245bd7ee301447` | Applied |

## Integrity findings retained, not repaired

1. SFL failure assets reference absent `SFL-FAM-005`, `006`, `007`, `009`, and
   `012`. Six such target references occur across five failure assets. Those
   assets are retained but quarantined; no family ID was invented or remapped.
2. The AIR Primitive inventory declares 243 rows but contains two separate
   files with source ID `EXP-TRG-001`. Both raw records are retained and
   quarantined. A resolver refuses that ambiguous ID.
3. Twenty-three SFL records lack an explicit per-record version. Their exact
   raw source and the containing manifest version are retained; this is a
   review finding, not a synthesized record version.
4. The initial generic extractor over-classified 486 Primitive-document
   identity fields as references. Those immutable audit rows remain available,
   but append-only dispositions exclude all 486 from the active graph. The
   active graph contains 67 actual SDA/SFL relationships and six unresolved
   internal references.

## Executed proof

`python scripts/cae/verify_wp04_registry_migration.py` proved:

- source counts and archive/source hashes equal the declared migration input;
- lineage is preserved on every imported record;
- active resolver access succeeds for `SDA-INV-001` and `SFL-FAM-001` only
  when their exact snapshot is named;
- missing `SFL-FAM-005` and duplicate `EXP-TRG-001` are rejected rather than
  silently selected;
- registry rows reject direct mutation in a forced-rollback transaction;
- RLS is enabled on all six registry tables;
- all applied migration checksums still match their staging ledger entries.

## What was not proven

- No existing AIR, API, or SQLite service reads this resolver yet.
- No SDA/SFL rule is used to validate a semantic assessment yet; WP-03’s
  lifecycle proof remains deliberately registry-neutral until a later bounded
  AIR integration package.
- No source record was corrected, superseded, or granted a missing family or
  version. The accountable lineage source for these defects is still needed.
- This is staging integration evidence, not production cutover or semantic
  quality proof.

## Exact operator decision

**Promote WP-04 and authorize WP-05 to reconcile PRD/FR/Tech-Spec contracts
against the now-versioned registry authority, while keeping all quarantined
records unavailable to runtime resolution and making no legacy-service cutover?**
