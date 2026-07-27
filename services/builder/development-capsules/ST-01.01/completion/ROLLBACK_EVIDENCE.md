# ST-01.01 Rollback Evidence

Verdict: `PASS_NON_DESTRUCTIVE`

The Story implementation is additive. Before implementation, neither `src/` nor `tests/` existed in this Builder workspace; the test-first run confirmed five import failures because `cmf_builder` was absent. The implementation created only the 12 source and eight test paths authorized by the capsule. It introduced no database, migration, dependency manifest, service, remote side effect, schema, registry mutation, deployment or durable production state.

## Demonstration

1. With `src` absent from the Python import boundary, `importlib.util.find_spec('cmf_builder')` returned `None`. Result: `PASS_MODULE_ABSENT`.
2. With only the additive `src` directory restored to the import boundary, `cmf_builder.__version__` resolved to `1.2.0-st01.01`. Result: `PASS_IMPLEMENTATION_REENABLED`.
3. The full 20-test suite then passed twice in clean `-B` contexts, with no bytecode or test cache created.
4. All four governed registry/schema inputs retained the capsule-pinned hashes.

No file was deleted or moved because `ALLOWED_FILE_SCOPE.yaml` explicitly sets `file_deletion_allowed: false`. The non-destructive import-boundary proof demonstrates the same rollback boundary without violating that prohibition.

## Rollback set

Rollback removes only the 12 `src/cmf_builder/` files and eight `tests/` files listed in `FILE_CHANGE_MANIFEST.yaml`, after separate human approval for deletion or a reversible version-control operation. Completion evidence and governed inputs remain historical receipts. No data migration or compensating external action is required.

## Cleanup

- `__pycache__` directories: 0
- `.pyc` files: 0
- network/service resources: 0
- database or artifact-store resources: 0
- external product mutations: 0

