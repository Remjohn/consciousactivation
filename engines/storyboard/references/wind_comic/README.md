# M0074 isolated Wind Comic storyboard reference

This is a surgical, dependency-free reference adapter, not a Wind Comic port.

It exists to let a later CAE integration compose proven mechanics without reverse-engineering the extraction intent. The adapter is pure Python and does not call providers, write canonical CAE state, or define semantic meaning.

## Covered

- shot-keyed pull-sheet export/import and changed-field proposals;
- derived timing treated as audit data, not an editable round-trip field;
- deterministic shot timeline overlap/span/duration audits;
- sketch-lock declarations with source SHA-256 and CAE-supplied style/scene lineage refs;
- deterministic scene/style anchor consistency checks;
- immutable operator feedback/revision append semantics;
- authorization + stale-baseline checks before proposal compilation.

## CAE handoff contract

The caller supplies canonical storyboard/timeline data and CAE authority/freshness evidence. The adapter returns a proposal, validation report, or receipt-shaped digest. Canonical persistence, receipts, promotion, and external runtime proof remain CAE responsibilities.

See `SOURCE_MAPPING.md` for the exact upstream commit, files, adopted behavior, and exclusions.
