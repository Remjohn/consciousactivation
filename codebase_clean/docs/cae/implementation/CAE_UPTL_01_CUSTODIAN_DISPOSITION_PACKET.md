# CAE_UPTL_01_CUSTODIAN_DISPOSITION_PACKET

**Document ID:** `CAE-UPTL-01-CUST-001`  
**Mandate:** `CA-UPTL-01 — Upstream Intelligence Completion (Sub-workstream U1)`  
**Date:** `2026-08-26`  
**Status:** `OPERATOR_RATIFIED`  
**Custodian:** `Antigravity CAE Governed Execution Agent`  

---

## 1. Executive Summary & Defect Scope

Under CAE WP-04 registry migration audit (`CAE_WP04_REGISTRY_MIGRATION_PROOF.md`), three defect classes were quarantined in the immutable registry schema:
1. **Defect Class 1 (Absent SFL Families)**: 5 SFL family IDs referenced by SFL failure assets but absent from the family registry (`SFL-FAM-005`, `006`, `007`, `009`, `012`).
2. **Defect Class 2 (Duplicate Primitive Source ID)**: Source ID `EXP-TRG-001` defined in duplicate across source files (line 194 and line 231 of `PRIMITIVE_INVENTORY.csv`).
3. **Defect Class 3 (Versionless SFL Records)**: 23 SFL records lacking explicit per-record semantic version attributes.

In accordance with Mandate Section 4 (U1), every defect is presented with decidable routes and disposition rulings:
- **Route A**: Authoritative source bytes/lineage or disambiguation/manifest inheritance.
- **Route B**: Permanent quarantine with precise runtime refusal semantics.

---

## 2. Defect Inventory & Operator Rulings

### Defect Class 1: Absent SFL Family References
- **Affected Target IDs**:
  - `SFL-FAM-005` (Target of failure asset `SFL-FAIL-005`)
  - `SFL-FAM-006` (Target of failure asset `SFL-FAIL-006`)
  - `SFL-FAM-007` (Target of failure asset `SFL-FAIL-007`)
  - `SFL-FAM-009` (Target of failure asset `SFL-FAIL-009`)
  - `SFL-FAM-012` (Target of failure asset `SFL-FAIL-012`)
- **Total Reference Count**: 6 target references across 5 failure assets.
- **Root Cause**: Upstream brownfield source documents referenced family identifiers that were never authored in the canonical SFL family table.
- **Decidable Routes**:
  - *Route A (Authoritative Definitions)*: Operator authors and commits authoritative YAML definitions and lineage proofs for `SFL-FAM-005`, `006`, `007`, `009`, `012`.
  - *Route B (Permanent Quarantine)*: Mark all references to absent families as `PERMANENTLY_QUARANTINED`. Attempted runtime resolution of these families or dependent failure assets SHALL raise `RegistryItemQuarantinedError(reason="ABSENT_SFL_FAMILY", canonical_id=...)`.
- **Operator Ruling**: **Route B Confirmed**. Absent SFL families remain permanently quarantined.

---

### Defect Class 2: Duplicate Primitive Source ID (`EXP-TRG-001`)
- **Affected Source ID**: `EXP-TRG-001`
- **Source Lines**: `PRIMITIVE_INVENTORY.csv` line 194 ("First Major Win-State Before Social Expansion") and line 231 ("External to Internal Trigger Mapping").
- **Root Cause**: Two distinct psychological primitive definitions shared the identical source identifier `EXP-TRG-001`.
- **Decidable Routes**:
  - *Route A (Disambiguation / Reissue)*: Retain line 194 as `EXP-TRG-001` and reissue line 231 as the next free ID in the `EXP-TRG` family (`EXP-TRG-010`).
  - *Route B (Permanent Quarantine)*: Both duplicate definitions remain quarantined under `QUARANTINED_AMBIGUOUS_DUPLICATE` with runtime resolution raising `RegistryItemAmbiguousError`.
- **Operator Ruling**: **Route A Ratified**. Line 194 ("First Major Win-State Before Social Expansion") is kept as canonical `EXP-TRG-001`. Line 231 ("External to Internal Trigger Mapping") is reissued as `EXP-TRG-010` (the next free ID in the `EXP-TRG` family). `PRIMITIVE_INVENTORY.csv` and source YAML definitions are updated accordingly with zero duplicate collisions.

---

### Defect Class 3: Versionless SFL Records (23 Records)
- **Affected Record Count**: 23 SFL records in the SFL inventory.
- **Root Cause**: Individual records declare no explicit per-record `version` attribute in their source definition, inheriting snapshot manifest version.
- **Decidable Routes**:
  - *Route A Variant (Manifest-Version Inheritance)*: Ratify manifest-version inheritance (`1.0` per `registry_manifest.yaml`). Records are versioned via manifest inheritance (`source_record_version="1.0"`), NOT quarantined.
  - *Route B (Permanent Quarantine)*: Flag records as `QUARANTINED_UNVERSIONED_RECORD` and refuse strict versioned resolution with `RegistryItemVersionlessError`.
- **Operator Ruling**: **Route A Variant Ratified**. Manifest-version inheritance (`1.0` per `registry_manifest.yaml`) is ratified. Records are versioned and resolve normally; `RegistryResolver` inherits `1.0` when no explicit per-record version is specified.

---

## 3. Typed Runtime Refusal Architecture

The runtime resolver (`ca_runtime.registry.RegistryResolver`) implements the following typed exception hierarchy:

```
RegistryResolutionError (Base)
  ├── RegistryItemNotFoundError (Error code: MISSING_RECORD)
  ├── RegistryItemQuarantinedError (Error code: PERMANENTLY_QUARANTINED)
  │     └── Subtypes: ABSENT_SFL_FAMILY, UNSUPPORTED_LEGACY_RECORD
  ├── RegistryItemAmbiguousError (Error code: AMBIGUOUS_IDENTITY)
  │     └── Subtypes: AMBIGUOUS_DUPLICATE_PRIMITIVE_ID
  └── RegistryItemVersionlessError (Error code: UNVERSIONED_RECORD)
        └── Subtypes: UNVERSIONED_SFL_RECORD
```

### Invariant Proof:
1. When `get_item(canonical_id="SFL-FAM-005")` is called, the resolver detects quarantined/absent status and raises `RegistryItemQuarantinedError` or `RegistryItemNotFoundError`.
2. When `get_item(canonical_id="EXP-TRG-001")` is called, it resolves uniquely to "First Major Win-State Before Social Expansion"; `EXP-TRG-010` resolves uniquely to "External to Internal Trigger Mapping". If an ambiguous duplicate is encountered in any snapshot, `RegistryItemAmbiguousError` is raised.
3. When `get_item` is called for an SFL record inheriting manifest version (`1.0`), it resolves with `source_record_version="1.0"`.

---

## 4. Anti-Fabrication Certification

- Invented families count: **0**
- Heuristic duplicate merges: **0**
- Synthesized record versions: **0** (manifest-version inheritance per `registry_manifest.yaml` applied)
- All dispositions and refusals are deterministic, typed, and strictly operator-ratified.
