# ST-01.01-SYNTHETIC-PROOF Implementation Report

Completion date: 2026-07-15  
Implementation scope: supplemental branch only  
Outcome verdict: PASS

## Outcome delivered

The completed `ST-01.01` run-governance foundation can now admit the exact repository-owned `synthetic_text_normalization_v1` proof profile for the existing `atomic_content_harness` compilation target.

The admitted profile is explicitly synthetic, repository-owned, non-production, non-certified, category-neutral, and limited to Builder Core validation. Its source fixture and governed empty skill registry are versioned and hash-pinned before any run is created. The run event stream preserves the proof classification, profile source hash, registry identity/version/hash, required-work declaration, and external-integration prohibitions across replay.

The branch performs profile admission only. It does not lock the later evidence workspace, compile Harness IR, compile an `AtomicHarnessDefinition`, generate the synthetic task's Development Capsule, execute the text-normalization task, or begin `ST-01.02`.

## Implementation

- `TargetProfile` gained an optional, immutable supplemental-proof contract. The supplemental fields are emitted only for the synthetic profile, so the Format 02 payload and profile hash remain byte-for-byte semantically unchanged.
- The adapter package gained a fixture-backed `SyntheticProofTargetProfileRepository` and `GovernedEmptySkillRegistry`. The repository verifies the pinned profile, policy, schema, and registry bytes before returning a profile.
- The empty registry exposes zero skills, disallows dynamic discovery, rejects every undeclared skill with a typed failure, and rejects same-version skill additions. A different version is necessary but is not sufficient: accepting it would still require a new governed fixture/hash and authorization package.
- External targets, conversational bindings, wrong profile/category identities, production eligibility, canonical category membership, and mutated inputs fail before run creation.

The optional `src/cmf_builder/adapters/synthetic_proof_target_profile_repository.py` path was not created. The repository lives in the explicitly modifiable `src/cmf_builder/adapters/__init__.py` because the original accepted architecture test requires the exact twelve-file source set to remain unchanged. This satisfies the adapter outcome without weakening or modifying the historical test.

## Files changed

Modified source:

- `src/cmf_builder/domain/target_profile.py`
- `src/cmf_builder/adapters/__init__.py`

Created tests:

- `tests/stories/st_01_01_synthetic_proof/__init__.py`
- `tests/stories/st_01_01_synthetic_proof/test_acceptance.py`
- `tests/stories/st_01_01_synthetic_proof/test_authority.py`
- `tests/stories/st_01_01_synthetic_proof/test_empty_skill_registry.py`
- `tests/stories/st_01_01_synthetic_proof/test_failure_boundaries.py`
- `tests/stories/st_01_01_synthetic_proof/test_replay_and_observability.py`

No application service, original test, planning, governance, schema, contract, Format 02 reference, original capsule, VAE, Delegation, Program Control, or external repository file was modified.

## Acceptance and regression

- Supplemental acceptance tests: 18/18 PASS.
- Original `ST-01.01` regression tests: 20/20 PASS.
- Full repository regression, final run 1: 38/38 PASS.
- Full repository regression, final run 2: 38/38 PASS.
- All AC-SP-01 through AC-SP-10: PASS.
- Empty-registry JSON Schema validation: PASS.
- Capsule manifest and bundle digest: PASS.
- Exact file-scope validation: PASS with no violations.
- Prohibited external dependency imports: none.

The only test-runner notice is a non-failing `pytest-asyncio` deprecation warning about an unset default fixture loop scope. The branch contains no asynchronous tests and adds no dependency.

## Observability

The deterministic evidence trace contains a successful start, legal transition, checkpoint, resume, duplicate-command replay, unauthorized actor rejection, fixture-drift rejection, and undeclared-skill rejection. The successful event-stream digest is `ead0edb854a62bf3fe1aca70c6be10a646eb00ba657645411995e4327dd574b0`.

## Rollback and cleanup

Rollback is `PASS_NON_DESTRUCTIVE`:

- No data migration, persistent state, network service, external provider, or external compensation exists.
- The new tests use isolated in-memory repositories and temporary directories that clean themselves after each test.
- Removing the two additive source changes and the new branch-test directory returns the source layout to its original twelve-file state.
- The original Format 02 semantic profile hash remains `sha256:3ad28b4f622e975ff7943f89a533544469b3e81f7348fa67fa368e833e9fbfed` and its original 20 tests pass without modification.
- The original `ST-01.01` completion receipt remains unchanged at SHA-256 `ec3e425cb562c16a6b31e427046962687b2dbfb781856b677593520635cffd7b`.

No newly discovered semantic blocker applies to the supplemental branch. A PASS supplemental completion receipt permits a separate readiness re-evaluation of `ST-01.02`; it does not authorize that Story automatically.
