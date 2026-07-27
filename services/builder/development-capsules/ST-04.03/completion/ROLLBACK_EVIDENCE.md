# ST-04.03 rollback evidence

Verdict: `PASS`

The in-memory adapter's injected atomic-commit failure was exercised before persistence. The rejected command left the predecessor stream at version 15 and produced zero phase graphs, zero phase receipts, zero phase events, and zero command records. Payload-conflicting repeats also failed without mutating the completed immutable result.

An authorized upstream boundary reopen from a completed Phase Graph emitted exactly eight linked events: boundary reopen, Draft Harness Model invalidation, Harness IR invalidation, artifact-set invalidation, constitutional-validation invalidation, capability-ownership invalidation, responsibility-module invalidation, and Phase Graph invalidation. The run advanced atomically from stream version 16 to 24. Active Phase Graph consumption then failed closed, while historical graph bytes remained reproducible.

Source rollback is additive. Remove the two new source modules and six new Story test files, then restore these exact pre-Story hashes:

- `src/cmf_builder/domain/run.py`: `a0c5d285fefacf79336903d91d80ff44ae92977e31586749f0bae86117d65b0a`
- `src/cmf_builder/application/atomicity_commands.py`: `425144aa8eacef2490232a15e04b58787b3c18b66c4603fa7b119a38c54983dc`
- `src/cmf_builder/application/ports.py`: `14f775e5d45658f33305ee034cd2824d11a60b85f5d8d0fb4c6b6e4cee2673ff`
- `src/cmf_builder/adapters/in_memory_run_repository.py`: `3ff40541718b9133fa91c6b637bfb72458cff491b2f4eb93f05e9d1f084ad0d6`
- `tests/stories/st_01_01/test_architecture_boundary.py`: `cdede93bbfc670cb56a032fe85c6dfc034524964e3d553f9d3679736026008b3`
- `tests/stories/st_01_01_synthetic_proof/test_failure_boundaries.py`: `bc8cda77ce58edd5920ffa17f95d234380497556d9551a0bb0303e6596596d4d`
- `tests/stories/st_01_02/test_architecture_boundary.py`: `21a6d4cf9f25229bb8a94076fce3e69b3b40b7c98571ea00bae82fc6c65cc6be`
- `tests/stories/st_02_05/test_architecture_boundary.py`: `0e71687a8c04f589d1a77337dd0921e22a1ae8d212fea4c6be59e965b86a0362`
- `tests/stories/st_03_03/test_architecture_boundary.py`: `6292df08ad5509f41da0bce70dc6509c2ac8e9a3f6f9f1f80967aca1de0a8eae`
- `tests/stories/st_03_04/test_architecture_boundary.py`: `655da3608862e83427b2c42d8a3c0bee22c0940b16f3a59daec9610b2819d570`
- `tests/stories/st_03_05/test_architecture_boundary.py`: `c0c6e8aaf64f9f1c724a8d9b117adff863f4f19cee09fbd5fcafbedfe57a37ae`
- `tests/stories/st_04_01/test_architecture_boundary.py`: `a1a6097a1ac69a632e9d66051fc46f291e37a363306e66127f0a47224b4b62c4`
- `tests/stories/st_04_02/test_architecture_boundary.py`: `b8b994b1b773adb843dd7dad33d01c7453318bc007853a8937cee0375a23e8cd`

After restoration, rerun the predecessor `256/256` suite. No database, schema, dependency, network, VAE, Delegation, Program Control, runtime, or published-artifact cleanup is required.
