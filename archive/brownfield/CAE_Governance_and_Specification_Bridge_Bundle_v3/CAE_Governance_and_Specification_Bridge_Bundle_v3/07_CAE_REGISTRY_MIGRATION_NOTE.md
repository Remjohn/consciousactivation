# CAE Registry Migration Note v2.0

## Purpose

This note establishes the brownfield treatment of inherited Primitive, SDA, and SFL registries.

## Registry law

Canonical registry records are data assets, not prose concepts.

When a registry already exists:

1. inventory it;
2. preserve identity;
3. validate schema;
4. validate crosswalks;
5. expose it through typed query access;
6. add migration records for defects;
7. only then integrate it into CAE runtime.

## Required migration fields

Each migrated record should carry:

```yaml
source_registry:
source_id:
source_version:
source_path:
source_hash:
canonical_id:
migration_status:
lineage_preserved:
validation_status:
crosswalk_status:
known_gaps: []
replacement_id: null
migration_notes:
```

## Integrity checks

Minimum automated checks:

- duplicate canonical IDs;
- broken references;
- invalid family IDs;
- missing versions;
- missing provenance;
- malformed schemas;
- incompatible geometry ranges;
- crosswalk targets that do not exist;
- failure corpus references without corresponding canonical functions/families;
- version regressions.

## Runtime doctrine

Runtime systems should read canonical registries through a query/resolution layer rather than copying YAML contents into prompts or mutable runtime records.

Example conceptual functions:

```text
get_sda_invariant(id)
get_representation_geometry(id)
get_archetypal_geometry(id)
get_species_grammar(id)
get_sfl_function(id)
get_sfl_function_family(id)
get_sfl_crosswalk(source, target)
get_primitive(id)
find_eligible_primitives(constraints)
```

These functions are semantic APIs. Their output should be typed, version-aware, and receipt-able.

## Known SFL migration anomaly

If the inherited failure corpus references function-family IDs not present in the inherited family registry, treat this as a **registry integrity defect**.

Required action:

- do not invent records;
- identify the missing lineage source;
- determine whether records were omitted, renumbered, or superseded;
- create a migration mapping if authoritative evidence exists;
- otherwise quarantine affected failure cases;
- add a regression test preventing silent reintroduction.
