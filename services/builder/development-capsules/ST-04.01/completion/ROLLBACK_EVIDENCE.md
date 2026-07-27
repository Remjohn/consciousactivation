# ST-04.01 rollback evidence

Verdict: `PASS`

The in-memory adapter's injected atomic-commit failure was exercised before persistence. The command produced zero new run events, zero capability graphs, zero capability receipts, and zero command records. Payload-conflicting repeats also failed without replacing the completed immutable result.

An authorized upstream boundary reopen produced exactly six linked events: boundary reopen, Draft Harness Model invalidation, Harness IR invalidation, artifact-set invalidation, constitutional-validation invalidation, and capability-ownership invalidation. Active graph consumption then failed closed, while the historical graph remained byte-reproducible.

Source rollback is non-destructive and requires no migration or external cleanup. Remove the two new source modules and six new Story test files, then restore these pre-Story hashes:

- `src/cmf_builder/domain/run.py`: `4f598510a183a141e20dd57c691d830c3808c074f674384dfe171559dd11407b`
- `src/cmf_builder/application/atomicity_commands.py`: `231f101f58892b8ad0781b8f62a74076523c98eef7a0a66ab3907ffbea390759`
- `src/cmf_builder/application/ports.py`: `88d7bb1714a5194c13713b7f6b739840ef4dd364de91c6f4f684f22492b2a41f`
- `src/cmf_builder/adapters/in_memory_run_repository.py`: `c0444dff8bf5e93e4aa88928ed765a8c0886535389f4074492ac7c7112882e8b`
- `tests/stories/st_01_01/test_architecture_boundary.py`: `0bf21e32d9071519a244a91986d87b008a5295e78cf8869641053d8b4e609a96`
- `tests/stories/st_01_01_synthetic_proof/test_failure_boundaries.py`: `0a8cf22617a923c2cb7dd499a592f76ee00d1ff7de34723d963d6f232f14a5c7`
- `tests/stories/st_01_02/test_architecture_boundary.py`: `7615d33af7ba24a3681c0d81ace1cd1bae456f45837a8fc9dd5b90dc68f88781`
- `tests/stories/st_02_05/test_architecture_boundary.py`: `abe682265f88345b3da0e969a82d3e13972309b384d363a9b870274d7a1117fd`
- `tests/stories/st_03_03/test_architecture_boundary.py`: `1770cefc878822b80c6f78da2cbfc533c3fc585c9a581d83d2df66d31c888f19`
- `tests/stories/st_03_04/test_architecture_boundary.py`: `2f037f679e968b698827795252130662053c4862e77989501e692d66841c67c6`
- `tests/stories/st_03_05/test_architecture_boundary.py`: `f44f703434c7deece612400f4c3a6260b216eceaf9e18bfd6d704381d212e3bb`

After restoration, rerun the original `186/186` predecessor regression set. No database, schema, dependency, network, VAE, Delegation, Program Control, or published-artifact rollback is required.
