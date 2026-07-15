# RC4 Release File Diff From RC3

Date: 2026-07-15  
Comparison: immutable release roots `1.1.0-rc.3` and `1.1.0-rc.4`  
RC3 files: 147  
RC4 files: 164  
Unchanged paths: 105  
Added paths: 19  
Removed paths: 2  
Changed paths: 40

The complete RC4 per-file byte and SHA-256 inventory is
`delegation-contracts/1.1.0-rc.4/HASH_INVENTORY.json`; the release manifest and
receipt cover that inventory, manifest, and all remaining released bytes.

## Added paths

- `compatibility/migrations/derivative-lock-inheritance-v0-to-v1.json`
- `contracts/examples/derivative-lock-inheritance.example.json`
- `contracts/schemas/derivative-lock-inheritance.schema.json`
- `fixtures/compatibility/derivative-locks/adapter.expected.json`
- `fixtures/compatibility/derivative-locks/adapter.source.json`
- `fixtures/compatibility/derivative-locks/ambiguous-derivation.invalid.json`
- `fixtures/compatibility/derivative-locks/authorized-new-demand-relaxation.valid.json`
- `fixtures/compatibility/derivative-locks/exact-inheritance.valid.json`
- `fixtures/compatibility/derivative-locks/legacy-unclassified.input.json`
- `fixtures/compatibility/derivative-locks/lock-removal.invalid.json`
- `fixtures/compatibility/derivative-locks/lock-weakening.invalid.json`
- `fixtures/compatibility/derivative-locks/missing-parent-evidence.invalid.json`
- `fixtures/compatibility/derivative-locks/semantic-shortcut.invalid.json`
- `fixtures/compatibility/derivative-locks/stricter-addition.valid.json`
- `HASH_INVENTORY.json`
- `RC3_CONVERGENCE_REJECTION_REPORT.md`
- `RC4_CORRECTION_REPORT.md`
- `validators/cmf_delegation_validators/derivative_locks.py`
- `validators/tests/test_derivative_locks.py`

## Removed paths

The predecessor-specific evidence files below are not copied into RC4; they
remain in their immutable predecessor releases and repository history.

- `RC2_CONVERGENCE_REJECTION_REPORT.md`
- `RC3_CORRECTION_REPORT.md`

## Changed paths

- `BASELINE_STATUS.md`
- `CLEAN_ROOM_VALIDATION_REPORT.json`
- `compatibility/manifest.json`
- `compatibility/profile.json`
- `compatibility/README.md`
- `COMPATIBILITY_MANIFEST.yaml`
- `CONTRACT_CHANGELOG.md`
- `contracts/authority-registry.json`
- `contracts/examples/compatibility-manifest.example.json`
- `contracts/generated/python/cmf_delegation_contracts/__init__.py`
- `contracts/generated/python/cmf_delegation_contracts/types.py`
- `contracts/generated/typescript/index.ts`
- `contracts/lifecycle.json`
- `contracts/package.json`
- `contracts/pyproject.toml`
- `contracts/README.md`
- `contracts/registry.json`
- `contracts/release-manifest.json`
- `contracts/schemas/compatibility-manifest.schema.json`
- `fixtures/compatibility/constitutional/aip-lineage.expected.json`
- `fixtures/compatibility/constitutional/evaluator-gap.invalid.json`
- `fixtures/compatibility/constitutional/source-provenance-parse-only.invalid.json`
- `fixtures/compatibility/constitutional/wrong-reading-unsupported.invalid.json`
- `fixtures/compatibility/direct/compatible.expected.json`
- `fixtures/compatibility/direct/compatible.input.json`
- `fixtures/format02/manifest.json`
- `fixtures/format02/scenarios/SCN-09.json`
- `fixtures/README.md`
- `protocol/cmf_delegation_protocol/engine.py`
- `protocol/README.md`
- `protocol/tests/test_reference_protocol.py`
- `RELEASE_RECEIPT.json`
- `validators/cmf_delegation_validators/__init__.py`
- `validators/cmf_delegation_validators/compatibility.py`
- `validators/cmf_delegation_validators/release_identity.py`
- `validators/pyproject.toml`
- `validators/README.md`
- `validators/run_release_validation.py`
- `validators/tests/test_contracts.py`
- `validators/tests/test_release_identity.py`

## Behavioral boundary

The changed compatibility and migration fixtures reflect RC4 package identity
and the new derivative-lock compatibility domain. The Visual Asset Demand
schema and example remain byte-identical to the pinned RC2/RC3 semantic
baseline. No lifecycle transition, existing authority rule, source-kind rule,
interview provenance rule, acceptance rule, or acknowledgement rule changed.
