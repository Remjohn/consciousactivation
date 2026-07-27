# BD-004 archive security report

Recorded: 2026-07-16  
Evidence classification: `PASS_WITH_RECORDED_LIMITATIONS`

## Immutable archive

- Path: `D:\Work\Conscious_Rivers\THE CMF STUDIO\VISUAL SYNTAX BUILDER (2).zip`
- Expected and observed SHA-256: `403bd07f8ca3feae94a991b16a08270fb799ffea87a05ab108163b4e1dee37b0`
- Size: `355,535,097` bytes
- Central-directory entries: `1,434` (`1,275` files and `159` directories)
- Archive comment: absent

The scanner opened the immutable archive in place. It did not extract any member into the Builder repository. Every member was streamed through SHA-256 and CRC/read validation.

## Safety checks

| Check | Governed limit or rule | Observed | Result |
|---|---|---:|---|
| Whole-archive identity | Exact expected SHA-256 | Exact | `PASS` |
| Path traversal | No absolute, drive-qualified, NUL, or `..` member | 0 | `PASS` |
| Exact normalized path collision | None | 0 | `PASS` |
| Case-insensitive collision | None | 0 | `PASS` |
| Symlink or special file | None | 0 | `PASS` |
| Encrypted member | None | 0 | `PASS` |
| Unsupported compression | Stored or DEFLATE only | 0 | `PASS` |
| Malformed decoded filename | None | 0 | `PASS` |
| CRC/read failure | None | 0 | `PASS` |
| Entry-count bomb guard | At most 10,000 | 1,434 | `PASS` |
| Total expanded-size guard | At most 2 GiB | 360,654,246 | `PASS` |
| Largest-member guard | At most 512 MiB | 14,259,109 | `PASS` |
| Overall expansion ratio | At most 50:1 | 1.01559:1 | `PASS` |
| Highest member ratio | At most 100:1 | 14.18328:1 | `PASS` |

The one nested ZIP member, `VISUAL SYNTAX BUILDER/Content Formats/format08_poetic_quote_theatre.zip`, was inspected in memory without extraction. Its SHA-256 is `3e01a5edf6b5b13e364c756a7f79aa0dca94ff27b7b3a250b1175e0f90a54446`. It contains 40 entries and 34 files, expands to 14,319,022 bytes at 1.004903:1, and has zero traversal paths, collisions, symlinks, special files, encryption, or malformed central-directory conditions. Recursion stopped after this governed first nested level.

## Integrity and ambiguity findings

- Six duplicate-content groups cover 17 regular files. There are no duplicate member paths. Repeated carousel and supervisual images must not be counted as independent examples.
- The archive contains both `CMF_FORMAT_BUILDER_WORKSTREAM_BLUEPRINT_V1_1` and a V1.2 Format 06/07 update. Coexistence is historical, but a consumer must select version deliberately.
- Generated `.pytest_cache`, `__pycache__`, and `.pyc` members are non-source ephemera and cannot support an evidence conclusion.
- Text scanning found semantic/runtime uses of words such as ?authority? and ?permission?, but no archive ownership, copyright license, redistribution grant, or Builder usage-adoption statement.
- The package contains code and binary media. Qualification does not authorize execution of archived code or media redistribution.

## Security conclusion

The exact bytes are technically safe for bounded read-only development inspection under the recorded limits. That technical result does not grant usage authority. Admission as `development_only_non_certifying_reference_corpus` remains `BLOCKED_OPERATOR_AUTHORITY` until the separate operator decision is truthfully executed and hash-bound.

