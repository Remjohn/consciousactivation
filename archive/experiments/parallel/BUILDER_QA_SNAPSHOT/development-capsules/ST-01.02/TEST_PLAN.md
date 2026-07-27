# Deterministic Test Plan

Use Python 3.12 standard-library `unittest`/`pytest` discovery and only
repository-local fixtures plus runtime-created temporary files.

Required suites:

1. `test_acceptance.py`: happy-path synthetic run, exact profile/candidate,
   lifecycle to `SOURCE_LOCKED`, lock attachment, receipt, and all ten GWT IDs.
2. `test_source_identity.py`: file/directory/ZIP descriptors; SHA-256 and
   aggregate determinism; same bytes/different paths; portable provenance;
   byte change creates a new lock and invalidation link.
3. `test_archive_and_path_safety.py`: traversal, absolute members, symlink,
   case collision, executable, nested archive, ratio/size/count/depth overflow,
   malformed ZIP, missing path, wrong hash, and no extraction/mutation.
4. `test_authority_and_idempotency.py`: human/code exact grants, agent/external
   denial, expiry, stale stream version, exact replay, and reused command ID with
   different payload.
5. `test_observability_and_rollback.py`: required success/rejection events and
   fields; no event/lock on rejection; deterministic receipt hashes; rollback
   and temporary-data cleanup.
6. `test_architecture_boundary.py`: domain imports no application/adapters;
   standard-library-only source tree; no external product/runtime modules; no
   category/target registry or contract-schema changes.

Mandatory regression:

- `tests/stories/st_01_01`: 20/20 must pass.
- `tests/stories/st_01_01_synthetic_proof`: 18/18 must pass.
- All ST-01.02 tests must pass twice from a clean test context.

Required validation:

- JSON parsing and semantic validation of `SYNTHETIC_SOURCE_PROFILE.json`.
- SHA-256 verification of both completion receipts, both capsule manifests, the
  synthetic target fixture, empty registry policy/fixture/receipt, and this
  capsule manifest.
- Exact changed-file allowlist check.
- AST import-boundary check and proof of no new dependency.
- Source pre/post byte hashes and directory entry sets match.

Skipped mandatory tests, nondeterministic output, an out-of-scope path, or a
failed regression forces completion verdict `FAIL`.
