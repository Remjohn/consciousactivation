# Deterministic test plan

The implementation must add tests before or alongside production changes and run them from a clean checkout-compatible environment.

1. `test_acceptance.py` covers AC-SP-01 through AC-SP-04 and AC-SP-10, including stable IDs, required-work order, checkpoint/resume, idempotent replay, and the explicit stop boundary.
2. `test_authority.py` covers authorized versus unauthorized actors, governed transition authority, and no mutation on denial.
3. `test_failure_boundaries.py` parameterizes changed fixture bytes, wrong profile ID, wrong target, production eligibility, canonical category membership, registry-hash mismatch, and attempts to introduce each prohibited integration.
4. `test_replay_and_observability.py` proves event/transition parity, required audit fields, deterministic correlation, no duplicate event on replay, and a stable evidence serialization hash.
5. `test_empty_skill_registry.py` validates the fixture against `empty-skill-registry.schema.json`, proves `skills` is exactly empty, and proves undeclared or dynamic skill use fails closed.
6. The unchanged `tests/stories/st_01_01` suite must remain 20/20 PASS.
7. The full repository regression suite must pass with zero new failures.
8. YAML and JSON parse validation must cover every capsule input, the policy, fixture, disposition, receipts, manifest, and authorization record.
9. Hash validation must recompute every entry in `CAPSULE_MANIFEST.json`, the synthetic target-profile fixture, the empty registry, and the original completion receipt.
10. File-scope validation must compare the completion change manifest with the exact allowlist and fail on any unlisted path.

Tests must use fixed IDs, clocks, fixture bytes, actor identities, and serialization ordering. Network, external provider, GPU, VAE, Delegation runtime, and Format 02 corpus access are forbidden. A skipped mandatory test is a failure.
