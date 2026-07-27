# Format 02 Historical Archive Recovery Report

**Search date:** 2026-07-15  
**Mode:** read-only recovery and validation  
**Verdict:** `EXACT_ARCHIVE_RECOVERED`

## Recovered archive

The historical Format 02 archive was recovered at:

`D:\Work\Conscious_Rivers\THE CMF STUDIO\VISUAL SYNTAX BUILDER (2).zip`

| Property | Recorded expectation | Recovered value | Result |
|---|---:|---:|---|
| Format | ZIP archive | ZIP archive | `MATCH` |
| SHA-256 | `403bd07f8ca3feae94a991b16a08270fb799ffea87a05ab108163b4e1dee37b0` | `403bd07f8ca3feae94a991b16a08270fb799ffea87a05ab108163b4e1dee37b0` | `EXACT` |
| Size | 355,535,097 bytes | 355,535,097 bytes | `EXACT` |
| Archive entries | 1,434 | 1,434 | `EXACT` |
| File entries | 1,275 | 1,275 | `EXACT` |
| ZIP CRC validation | valid archive required | every member passed | `PASS` |

The archive is complete, readable, unencrypted, and contains no failed CRC member. Its ZIP uses stored and deflated members and has no archive comment.

## Authority metadata used for recovery

The search key was assembled from the existing, unchanged evidence records:

- `docs/planning/FORMAT02_CORPUS_EVIDENCE_AUDIT.yaml`
- `docs/planning/FORMAT02_CORPUS_OPERATOR_INPUT_REQUEST.md`
- BD-004 planning and blocker records
- Builder and cross-product manifests, status exports, and source registers

Those records identify the historical register name `VISUAL SYNTAX BUILDER (2)(2).zip`, the former path `/mnt/data/VISUAL SYNTAX BUILDER (2)(2).zip`, the expected SHA-256, size, entry counts, and three protected internal members. A current Visual Asset Editor source register identifies the repository-local source name as `VISUAL SYNTAX BUILDER (2).zip`. The missing extra `(2)` is a filename-copy discrepancy, not an archive-identity discrepancy: hash, size, entry count, file count, and protected-member evidence all match exactly.

## Search scope and method

The recovery search covered:

- the complete Atomic Harness Builder repository;
- Program Control product-authority, shared-evidence, cross-repository contract, archive, and status areas;
- release and reference material under `D:\Work\CONSCIOUS_ACTIVATIONS`;
- repository-local archive, backup, import, source, retained-package, and migration locations found under the workspace;
- the metadata-linked local source repository `D:\Work\Conscious_Rivers`, including `THE CMF STUDIO`.

Across the two searched roots, 36 ZIP archives were enumerated: 9 under `D:\Work\CONSCIOUS_ACTIVATIONS` and 27 under `D:\Work\Conscious_Rivers`. No other accessible archive format was returned by the archive-extension search. Candidate selection used exact and partial filenames, the recorded byte size, central-directory paths, Format 02 markers, and protected-member names. Seventeen plausible candidates were then fully SHA-256 hashed, CRC-tested, and content-inspected. Filename alone was never accepted as proof.

The complete candidate record is in `docs/planning/FORMAT02_ARCHIVE_CANDIDATES.csv`.

## Protected-member validation

All three protected internal members recorded by the evidence package are present in the recovered archive and independently match their recorded hashes:

| Internal member | SHA-256 | Result |
|---|---|---|
| `docs/architecture/visual-sonic-composition-syntax/FORMAT02_MINIMAL_COACH_THEATRE.md` | `30475c0f1c5e2118d8baf211a35240093bb2e630b54ddef6e18d7aa094d9f38f` | `EXACT` |
| `registries/canonical/skills/format02_scene_syntax.select/SKILL.md` | `dc0c27239bfd0d94035879bb3b0663917547e2cf592c7a1c9095b24fd559efe3` | `EXACT` |
| `registries/canonical/visual_sonic_composition_syntax/format02_ingredient_identities.json` | `f2451088ca913d3e06582b7274dfffecb0cd36748151d1e020dd31fd9c2b8097` | `EXACT` |

## Format 02 content inspection

The exact archive contains the expected Format 02 doctrine and source corpus material:

- 82 Format 02-related archive entries, of which 76 are files;
- 73 files under `Content Formats/format02_minimal_coach_theatre/`;
- two reference MP4 files;
- 68 extracted JPG frames;
- one PNG reference;
- four Markdown files;
- one JSON registry file;
- the protected doctrine, scene-syntax skill, and ingredient-identity registry listed above.

This is positive recovery evidence for the historical corpus package. The archive does **not** contain a separately named governed `SourceProfile` artifact. Archive recovery therefore does not by itself establish the current source-profile governance, licensing/usage authority, benchmark status, or production certification required for corpus adoption.

## Other plausible candidates

Three candidates contain material related to the recovered archive but fail exact archive identity:

1. `CCP_VISUAL_SONIC_COMPOSITION_SYNTAX_DOCTRINE_V1_INTEGRATION_BUNDLE.zip` contains the three protected doctrine/registry members with exact member hashes, but only 52 files and no source media. It is a valid doctrine subset, not the historical corpus archive.
2. `VISUAL_SYNTAX_BUILDER.zip` is a valid but materially divergent package. It has 1,170 files; compared after removing the common top-level folder, it is missing 1,074 exact-archive paths and contains 969 paths not in the exact archive. Its Format 02 protected members and media subset are present, but its whole-archive hash and structure differ.
3. `VISUAL_SYNTAX_BUILDER.zip` with the underscore filename (`VISUAL_SYNTAX_BUILDER.zip`) is a valid near-copy containing 1,274 of the 1,275 exact-archive files. It has no changed or extra normalized member and is missing only `Content Formats/format08_poetic_quote_theatre.zip`. Its hash still does not match, so it is a partial candidate rather than the authoritative historical archive.

All remaining candidates are readable but unrelated product-authority snapshots, working-copy bundles, or downstream Format 02 integration packages. No damaged plausible candidate was found.

## Governance boundary

This report recovers and validates historical evidence only. It does not:

- adopt the recovered package as the governed Builder corpus;
- create or approve a Format 02 source profile;
- assert benchmark or production-certification status;
- change BD-004, any Story dependency, or any Story readiness classification;
- modify the existing evidence audit or operator-input request.

`ST-01.02` readiness is intentionally unchanged. A separate governed adoption decision must determine whether this exact archive, together with operator-supplied authority and source-profile evidence, can satisfy the Format 02 BD-004 sub-scope.

## Verdict

`EXACT_ARCHIVE_RECOVERED`

The recovered path, whole-file SHA-256, byte size, ZIP structure, entry counts, protected-member hashes, and full CRC validation establish exact historical archive identity. No automatic corpus adoption is authorized by this result.
