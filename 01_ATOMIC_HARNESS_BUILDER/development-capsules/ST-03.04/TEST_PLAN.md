# Test plan

Run with `PYTHONPATH=src`, deterministic clocks/UUIDv7 providers, the completed repository-owned synthetic fixture, and the in-memory development/test adapter. Network, external runtimes, filesystem artifact publication, model calls, and task execution are prohibited.

Create at least 26 independently named tests across:

1. exact active HarnessIR and ST-03.03 receipt linkage;
2. exact 8/3/10 artifact inventory and complete atomic manifest;
3. human Markdown readability, canonical JSON parsing, and explicit non-executable status;
4. source-node selectors and governed metadata preservation for every projection;
5. deterministic bytes/hashes/manifest/receipt in two fresh contexts;
6. compiler/config/timestamp/content-hash completeness and timestamp-in-config determinism;
7. manual drift quarantine with HarnessIR non-mutation;
8. missing/altered/invalidated IR, undeclared node reads, incomplete inventory, conflict, secret/external reference, authority, concurrency, idempotency, and injected atomic failure;
9. event replay, repeat-command replay, and upstream descendant invalidation;
10. observations and receipt fields;
11. exact source set, standard-library-only imports, no schema/dependency/external imports, no Workflow IR, no ST-03.05/Atomic Harness/Capsule/Control Tower behavior.

Required commands:

- `$env:PYTHONPATH='src'; python -m pytest -q tests/stories/st_03_04`
- `$env:PYTHONPATH='src'; python -m pytest -q tests/stories/st_01_01`
- `$env:PYTHONPATH='src'; python -m pytest -q tests/stories/st_01_01_synthetic_proof`
- `$env:PYTHONPATH='src'; python -m pytest -q tests/stories/st_01_02`
- `$env:PYTHONPATH='src'; python -m pytest -q tests/stories/st_02_05`
- `$env:PYTHONPATH='src'; python -m pytest -q tests/stories/st_03_03`
- `$env:PYTHONPATH='src'; python -m pytest -q`

Passing thresholds: all mandatory tests pass with no skips; preimplementation `112/112` passes; the Story suite has at least 26 tests; architecture tests pass; two fresh-context Story reruns are deterministic; receipt/capsule/hash/file-scope validation passes.
