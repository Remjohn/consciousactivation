# Mandate ID & Title

**Mandate ID:** `CAE-M062`  
**Canonical repository mandate:** `CAE-M0062` — Cinematic Corpus Ingestion and Scene Organization  
**Requirement / Invariant:** `INV-CINEMA-CORPUS-001`

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/asset-intelligence/src/cae_asset_intelligence/corpus.py` | Added governed cinematic corpus models, deterministic media/scene IDs, authorization and SHA-256 verification, stable time-range validation, contextual-caption hook, transcript/dialogue metadata, canonical `AssetAnnotation` projection, scene search index, immutable INGESTED/INDEXED/QUARANTINED receipt handling. | Authorized bytes only; exact source hash and scene ranges are validated; scenes remain compatible with the existing AssetAnnotation doctrine; state and provenance are explicit. |
| `services/asset-intelligence/src/cae_asset_intelligence/corpus_store.py` | Added controlled derived filesystem storage for scene records, immutable receipts, deterministic scene-index rebuild/search, and exact source/time verification. | Reindex is idempotent; derived records cannot be silently overwritten; wrong bytes or stale time ranges are rejected without deleting failed evidence. |
| `services/asset-intelligence/src/cae_asset_intelligence/__init__.py` | Exported the M062 corpus contracts and storage boundary without creating a second asset ontology. | Existing `AssetAnnotation`, rights and insert-role doctrine remains the canonical semantic object. |
| `tests/asset_intelligence/test_cinematic_corpus_m062.py` | Added 11 M062-focused integration/unit tests using the existing real H.264/AAC fixture `tests/api/fixtures/synthetic_interview.mp4`; covers authorization, hash mismatch, workspace isolation, stable IDs, idempotent reindex, search, scene-boundary rejection, annotation compatibility, caption generation hook, state receipt, and immutability. | False-proof and isolation cases are actively rejected; positive governed-media path produces searchable, timestamped, stable scenes and immutable receipts. |

## Files Added and Files Modified

**Added**

- `services/asset-intelligence/src/cae_asset_intelligence/corpus.py` — new scoped M062 ingestion/scene/index/receipt boundary.
- `services/asset-intelligence/src/cae_asset_intelligence/corpus_store.py` — new derived corpus/index/receipt persistence boundary.
- `tests/asset_intelligence/test_cinematic_corpus_m062.py` — M062 verification suite.

**Modified**

- `services/asset-intelligence/src/cae_asset_intelligence/__init__.py` — exports the new bounded subsystem API.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

No database migration is required. The implementation is filesystem-backed derived storage and does not alter the existing canonical asset ontology or upstream schemas.

Copy these files from this bundle into the repository at the exact paths above, preserving the existing `services/asset-intelligence/` package and tests. Do **not** copy the bundle root directory itself into the repository.

The implementation expects the existing governed media fixture at:

`tests/api/fixtures/synthetic_interview.mp4`

That repository fixture was inspected as a real 6.000-second H.264/AAC video; SHA-256 used by the evidence run:

`60e179c1a0a96d1949943c84f80a1ad9f6d380d86917052d878faf6ad010483a`

Post-apply setup/verification:

```bash
python -m compileall -q services/asset-intelligence/src tests/asset_intelligence/test_cinematic_corpus_m062.py
```

No migrations or external services are required for the scoped tests.

The derived runtime namespace is supplied by the caller, e.g. `SceneCorpusStore(<derived-corpus-root>)`; source media bytes remain external and are never scraped or copied by this implementation.

## Test Command (exact pytest/test command to verify)

```bash
PYTHONPATH=services/asset-intelligence/src:services/production-program/src pytest -q tests/asset_intelligence tests/production_program
```

## Expected Test Results (number of automated tests, all passing)

**32 automated tests, 32 passing, 0 failing.**  
Execution environment: Python 3.13.5, pytest 9.0.2, Pydantic 2.13.4.

The M062-only additions comprise 11 tests; the combined scoped Asset Intelligence + Production Program regression command is 32/32 green.

## Evidence, limitations, and operator gate

**What the verifier actually measures:** authorization approval/workspace/source-version alignment; SHA-256 equality between supplied bytes and authorized source identity; scene range positivity, ordering, non-overlap, and source-duration bounds; contextual caption validation through the existing AssetAnnotator; rights evidence for `CLEARED`; deterministic scene/index IDs; immutable receipt persistence; exact source hash and declared time-range checks before retrieval use.

**What it does not measure:** visual semantic truth of the caption, whether a scene boundary is aesthetically optimal, legal conclusions about fair use/copyright, frame-level timestamp synchronization against an external edit decision list, or remote-media ownership. Those remain upstream human/model authority or operator decisions.

**False-proof countercase:** the test mutates one byte of the inspected real MP4 while retaining the original approved authorization hash. The ingest is quarantined and no scene records are emitted. A separate verifier test rejects a stale scene range even when the media bytes are correct.

**Environment-fidelity limitation:** a repository-wide `pytest -q` run was attempted but failed during collection because the uploaded sandbox environment lacks unrelated repository dependencies (notably `psycopg`) and contains pre-existing collection/import failures. Those failures are outside the permitted M062 file boundary and were not repaired or hidden. Acceptance evidence is therefore the exact scoped command above.

**State model:** `SOURCE_ACCEPTED` is represented by the explicit approval/hash/version precondition; successful projection yields immutable `INGESTED`, successful derived reindex yields a separate immutable `INDEXED` receipt, and failed validation yields immutable `QUARANTINED` evidence. Actor is the execution agent; validators are the authorization/hash/boundary/rights/index checks; recovery is repair-and-reingest or removal of derived index records only.

**Control/commit evidence:** sandbox execution commit `f420ae22f01a878cf905f63c97e07e483ca34a28` (`feat(asset-intelligence): add governed cinematic corpus ingest`). The uploaded repository did not contain a usable upstream git history, so this is the exact local execution commit for the four scoped changes.

**Operator decision required:** Do you accept M0062 and authorize M0064?

`ACCEPT → AUTHORIZE NEXT`  
`ACCEPT WITH LIMITATIONS → AUTHORIZE NEXT`  
`REPAIR → RETURN TO CURRENT MANDATE`  
`BLOCK → DO NOT PROCEED`
