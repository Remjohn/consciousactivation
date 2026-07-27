# ST-01.03 Bundle Reproduction Report

Date: 2026-07-17  
Classification: `HISTORICAL_CANONICALIZATION_MISMATCH`

## Scope

This report supplements, but does not rewrite, the original ST-01.03 capsule manifest,
validation report, implementation authorization, file-change manifest, or PASS Story
Completion Receipt.

## Immutable-input verification

All 18 manifest entries were re-read from their repository-relative paths. Every file
matches both its recorded byte count and recorded SHA-256. No immutable-input drift was
found.

```yaml
immutable_inputs: 18
sha256_matches: 18
byte_count_matches: 18
missing_inputs: 0
changed_inputs: 0
```

The original capsule-manifest file remains byte-identical at:

`e18e07a758fe4d6672281f445ea2cf71acedbe6142e333023e4b9d09ea6f14e7`

The original completion receipt remains byte-identical at:

`f1111552cd01be92302e87ae19ac707926880b6f0d931df03df26f4842687d4c`

## Digest reproduction

The manifest declares:

`sha256(sorted(path + ':' + sha256 + newline))`

Applying that declaration as UTF-8 without BOM, with forward-slash paths sorted by
ordinal path value and one terminal LF per entry, produces:

`e54abd34d119e4bc1bb383c9c5df84c18155c2c65267e4dffe0f9375045beb0c`

The manifest and original receipt instead record:

`457ce102e1eee99200f178fda3615399890bbe68851e9dd57d374bb5ffe3cb8a`

## Canonicalization search

Four hundred plausible payload variants were tested. The search covered:

- manifest order and ordinal path order;
- exact, forward-slash, backslash, capsule-relative, and basename path forms;
- `path:hash`, `path:hash:bytes`, `hash:path`, hash-only, concatenated,
  pipe-delimited, and NUL-delimited records;
- LF, CRLF, and no record delimiter;
- terminal delimiter included and omitted;
- compressed and formatted JSON array serialization;
- path/hash, path/hash/byte-count, hash/path, and full-entry JSON field order; and
- UTF-8 encoding without BOM.

None reproduced the historical recorded digest. Repository search found no retained
historical bundle-generation script or payload snapshot for ST-01.03. The precise
historical algorithm is therefore unrecoverable from current evidence.

## Root cause

Because every governed input byte and individual digest remains exact, this is not
immutable-input drift. It is an aggregation-layer recording or undocumented
canonicalization defect created at capsule issuance. The defect does not alter the
Story outcome, source implementation, tests, dependency evidence, or completion
artifacts.

## Future canonical rule

Future line-based capsule bundles use
`cmf-capsule-bundle/path-sha256-lines-v1`:

1. normalize every repository-relative path to `/`;
2. require lowercase 64-character SHA-256 values;
3. sort records by UTF-8 ordinal path value;
4. encode each record exactly as `path:sha256\n`;
5. concatenate all records, including the final LF;
6. encode as UTF-8 without BOM; and
7. hash the resulting bytes with SHA-256.

Any other algorithm must have a distinct version identifier and a retained payload or
reproducible implementation.
