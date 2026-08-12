# Failure Taxonomy — Visual Syntax Reconstruction Analyst

## Error Codes

| Error Code                        | Description                                                                                    |
|-------------------------------------|--------------------------------------------------------------------------------------------------|
| `ROLE_PRIMITIVE_TYPE_MISMATCH`      | A `primitive_type` value was used as `slide_role`. Confirmed prior defect — see `_build-materials/tests/regression_cases.md` Case 1 for real fixtures. |
| `PRIMITIVE_ROLE_TYPE_MISMATCH`      | A `slide_role` value was used as `primitive_type`.                                              |
| `ZONE_PRIMITIVE_INCOMPATIBLE`       | A primitive's declared zone is not in the canonical zone registry.                              |
| `DANGLING_EVIDENCE_REF`             | An `evidence_refs` entry does not resolve to a real observation `object_id`.                     |
| `INSUFFICIENT_EVIDENCE`             | An inference has an empty `evidence_refs` array.                                                |
| `UNSUPPORTED_ANCHOR_CLAIM`          | A persistent-anchor claim has no evidence identifying the frames supporting persistence.         |
| `DUPLICATE_ID`                      | Two observation objects share an `object_id` within the same harness.                            |
| `SYNTAX_HASH_MISMATCH`              | The recorded `syntax_hash` does not equal a fresh canonicalization of the same syntax fields.    |
| `DEDUP_COUNT_INCONSISTENT`          | The deduplicated entry count does not equal the number of distinct `syntax_hash` values.          |
| `INVALID_CANDIDATE_PROMOTION`       | A `NOVEL_CANDIDATE` was recorded as `CANONICAL` without an out-of-band registry update event.     |
| `SOURCE_INTEGRITY_MISMATCH`         | `source_zip_sha256_recorded` does not equal the bytes actually analyzed. Technical only — carries no licensing implication. |
| `UNDOCUMENTED_PIPELINE_DEVIATION`   | The vision model/tool used differs from the documented default pipeline and was not flagged.      |
