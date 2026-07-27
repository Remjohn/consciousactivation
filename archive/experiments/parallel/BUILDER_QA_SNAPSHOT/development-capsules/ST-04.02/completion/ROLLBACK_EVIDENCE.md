# ST-04.02 rollback evidence

Verdict: `PASS`

The in-memory adapter's injected atomic-commit failure was exercised before persistence. The rejected command left the predecessor stream at version 14 and produced zero module graphs, zero module receipts, zero module events, and zero command records. A payload-conflicting repeat also failed without replacing or mutating the completed immutable result.

An authorized upstream boundary reopen from a completed module graph emitted exactly seven linked events: boundary reopen, Draft Harness Model invalidation, Harness IR invalidation, artifact-set invalidation, constitutional-validation invalidation, capability-ownership invalidation, and responsibility-module invalidation. The run advanced atomically from stream version 15 to 22. Active module consumption then failed closed, while historical graph bytes remained reproducible.

Source rollback is additive and requires no migration or external cleanup. Remove the two new source modules and six new Story test files, then restore the following exact pre-Story hashes:

- `src/cmf_builder/domain/run.py`: `dadb3326945bb5d4251f9c4239651961df4f04496550a10fcf5925ef680c6f8b`
- `src/cmf_builder/application/atomicity_commands.py`: `8cd7214ae29a0296dad3500fb3162cf89e817ce364aead77c0c9249afc2b57fc`
- `src/cmf_builder/application/ports.py`: `f7f9da93a5fbfc40f1788298b97da66c7a9aa9fc491ef143faa47935366e5d74`
- `src/cmf_builder/adapters/in_memory_run_repository.py`: `8c8ebcb50e1535a7d5447831c726c4adc10693655b0a5176c576738b95ecf05b`
- `tests/stories/st_01_01/test_architecture_boundary.py`: `6b3d7a73328641b1cb874bebeea811251d443fa5d93da329e4bcf1af791c69c3`
- `tests/stories/st_01_01_synthetic_proof/test_failure_boundaries.py`: `c2c0dc8b0985c212ff5f98334bd72369e940e697171ba98aac4d33e5dbf8d99d`
- `tests/stories/st_01_02/test_architecture_boundary.py`: `bee45dfe5de5092347dcafbff2939ceeec586ff274de89429e5b1c4b19f9073b`
- `tests/stories/st_02_05/test_architecture_boundary.py`: `10f6990ac541dd81c3fee9265f5de1c11e81f62f8e186c0f482c994bd43a2a84`
- `tests/stories/st_03_03/test_architecture_boundary.py`: `005c47d281e912d15f07b1f0259b0ecee11b76814a05de64309724611101de4f`
- `tests/stories/st_03_04/test_architecture_boundary.py`: `7909f8ab55aa96a0c6102f4639d25ed85074cd847728cc43b80ce644305661db`
- `tests/stories/st_03_05/test_architecture_boundary.py`: `674f2787566a4a5f9ee3f17c63fc770eafb4a2138babc6fdbabe451c3fa19636`
- `tests/stories/st_04_01/test_architecture_boundary.py`: `1bb978fafdb477dde5d6b42d67e7c65823ee15fecd81ae04f8202b1590ff3091`

After restoration, rerun the predecessor `221/221` suite. No database, schema, dependency, network, VAE, Delegation, Program Control, published artifact, or production-state rollback is required.
