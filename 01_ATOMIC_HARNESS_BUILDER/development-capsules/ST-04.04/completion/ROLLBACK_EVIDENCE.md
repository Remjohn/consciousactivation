# ST-04.04 rollback evidence

Verdict: `PASS`

The in-memory adapter's injected atomic-commit failure was exercised independently at Phase Handoff Graph compilation, internal handoff issuance, and receiver decision. Each rejected command preserved the predecessor stream version and left zero partial graph, handoff, decision, receipt, event, or command record. Failure observations remained diagnostic only.

An authorized upstream boundary reopen from a completed accepted handoff emitted exactly nine linked events: boundary reopen, Draft Harness Model invalidation, Harness IR invalidation, artifact-set invalidation, constitutional-validation invalidation, capability-ownership invalidation, responsibility-module invalidation, Phase Graph invalidation, and Phase Handoffs invalidation. The run advanced atomically from stream version 19 to 28. The active handoff graph and its affected issued handoff then failed closed, while historical graph, handoff, decision, receipt, and canonical bytes remained reproducible.

Source rollback is additive. Remove the two new source modules and six new ST-04.04 test files, then restore these exact pre-Story hashes:

- `src/cmf_builder/domain/run.py`: `fdd62507300b610bb403240a1ddade98cf395dd50c7d91a557555279a1a5d1c3`
- `src/cmf_builder/application/atomicity_commands.py`: `fdc295d5e11afb2dd6274129564d73ea3283b55ed89b953cfea14da4bbc23fbd`
- `src/cmf_builder/application/ports.py`: `7af965583be39dc6073b0dc6930d75af172877e642d3726d5f2903144acccc6b`
- `src/cmf_builder/adapters/in_memory_run_repository.py`: `14e48cc75b73c8c010d5c1af9b0dc945a71c7f953518c2ad9c1e7aa82ec1a899`
- `tests/stories/st_01_01/test_architecture_boundary.py`: `57a24fe72bd4d532d36a64a63fbb1f22c73c8518baa8813f037c407a7b7cdb8f`
- `tests/stories/st_01_01_synthetic_proof/test_failure_boundaries.py`: `ed41b927843e3e8d13ea81c1ef372a8fcbef2be323b5a93e16ea56abdcd80bd4`
- `tests/stories/st_01_02/test_architecture_boundary.py`: `e40230f21db34b848ff32cc4f35ecde6d02433c3163bf6137da293f67e5ff75e`
- `tests/stories/st_02_05/test_architecture_boundary.py`: `fff0a7e315f42eb0e26fd811f0f7e2b514fcf99286b900e458323153a8c76658`
- `tests/stories/st_03_03/test_architecture_boundary.py`: `ab2645f04147d3c00bbc159ae13fceae837634322710dde4b9f851e991e316c1`
- `tests/stories/st_03_04/test_architecture_boundary.py`: `07c677973b6d31611094d0ada76130283ba068ddd88fcdbdea75d7a5c1d1863b`
- `tests/stories/st_03_05/test_architecture_boundary.py`: `47eec850ebb80b870f2c65eb2a9ea4a8bdcf12135fddd459ce4977af702491c9`
- `tests/stories/st_04_01/test_architecture_boundary.py`: `49214feb46088a4f3a163c7b852680ab67dfc86c6f2ca726c2000c20224dceaf`
- `tests/stories/st_04_02/test_architecture_boundary.py`: `23e909fcc0c1b0dbd1f47061d2b78950bc05c6c35a13a6703f400d197af429e7`
- `tests/stories/st_04_03/test_architecture_boundary.py`: `9662d5eea8767a66f8321e39bcdc040bddbc551d978c5b203ed830aca7148fdc`

After restoration, rerun the predecessor `292/292` suite. No database, schema, dependency, transport, network, VAE, Delegation, Program Control, runtime, published-artifact, or external-system cleanup is required.
