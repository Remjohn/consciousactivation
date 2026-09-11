# CAE-M060 Product E2E Fixture & Runtime Test Harness

This directory contains the deterministic product-boundary proof harness for `CAE-M060` / `INV-PROOF-REAL-001`.

## What it executes

The harness uses the repository's actual `ProgramRegistry`, `ProgramOperatorRuntimeService`, `UniversalProgramStateRuntime`, canonical `research_canonicalization_program` state machine, and durable `SqliteProgramStateStore`. It seeds immutable source/media fixture references into an isolated workspace, executes the declared research transitions, captures receipts and checkpoints, and requires the declared `canonical_knowledge_commit_gate` to suspend the run fail-closed.

The harness deliberately does **not** turn the repository's declared `RESEARCH_CANONICALIZATION_HARNESS_V1` identifier into a new fake runtime binding. The existing brownfield baseline records that a separate executable binding for this identifier is absent. The proof therefore measures the real operator/state boundary that is executable today and records the missing binding as a limitation.

Only import-time compatibility shims for optional repository application packages that are absent from the clean archive are used. No CAE runtime stage, provider, distribution service, or state transition is mocked.

## State and evidence contract

The intended state transition is:

`CLEAN -> SEED -> EXECUTE -> ASSERT -> COLLECT -> CLEAN`

The verified product checkpoint path is:

`INITIAL -> SOURCES_ATTACHED -> CANDIDATES_EXTRACTED -> CANONICALIZED -> OKF_PROJECTED -> AWAITING_APPROVAL`

Each clean run records a stable semantic checkpoint signature plus run-specific receipt identities. Re-running without clean reset is rejected so an old aggregate cannot manufacture a false PASS.

The negative fixture omits `false_merge_verified`; CAE preflight must reject it before an aggregate is created, and the diagnostic is persisted as failed evidence.

## Commands

Run one real product-boundary proof:

```bash
python -m pytest -q tests/e2e/test_product_e2e_fixture.py
```

Run the harness twice from clean workspaces and compare deterministic checkpoints:

```bash
python tests/e2e/test_product_e2e_fixture.py repeat --artifact-root .cae-m060-artifacts/repeat
```

Run the intentionally failing fixture:

```bash
python tests/e2e/test_product_e2e_fixture.py negative --workspace-root .cae-m060-artifacts/negative
```

Clean only the controlled fixture namespace (failed evidence is preserved under `<name>.failed/`):

```bash
python tests/e2e/test_product_e2e_fixture.py clean-reset .cae-m060-artifacts/negative
```

## Fidelity boundary

Measured: real CAE runtime dispatch, real SQLite persistence, canonical transition validation, authority lanes, durable gate suspension, checkpoint determinism, receipt identity, clean-state protection, and negative preflight behavior.

Not measured: production PostgreSQL, external inference-provider reachability, native OpenChatCut execution, human approval quality, or the missing standalone executable binding for `RESEARCH_CANONICALIZATION_HARNESS_V1`.

Operator validation remains required for the mandate disposition.
