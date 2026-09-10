# CAE-M060 — Product E2E Fixture & Runtime Test Harness

## Mandate ID & Title

**Mandate ID:** `CAE-M060`  
**Mandate Title:** Product E2E Fixture & Runtime Test Harness  
**Requirement / Invariant:** `INV-PROOF-REAL-001`

The campaign source document in the repository is `docs/cae/CAE_Operational_Product_Campaign_M0058_M0068_v1/mandates/M0060_CA_PRODUCT_E2E_FIXTURE_RUNTIME_TEST_HARNESS_MANDATE.md`; the requested execution/bundle identifier is `CAE-M060`.

## Summary Table (File changed | What changed | Invariant proven)

| File changed | What changed | Invariant proven |
| --- | --- | --- |
| `tests/e2e/test_product_e2e_fixture.py` | Added a clean, isolated fixture workspace; seeded immutable source/media fixture references; real `ProgramRegistry` discovery/preflight; real `ProgramOperatorRuntimeService` dispatch; real `UniversalProgramStateRuntime` + `SqliteProgramStateStore` transition execution; durable gate checkpoint; receipt/evidence collection; deterministic two-run comparison; explicit false-proof reuse rejection; intentionally failing fixture; CLI `run`, `repeat`, `negative`, and `clean-reset` commands. | `INV-PROOF-REAL-001`: the proof reaches the actual CAE operator/state runtime boundary, persists state/receipts, defeats stale-workspace false proof, and fails closed on invalid preconditions. |
| `tests/e2e/README.md` | Added developer/CI instructions, evidence/fidelity boundary, state/checkpoint contract, and exact run/reset commands. | Makes the executable proof repeatable and documents what is and is not measured. |

## Files Added and Files Modified (with exact relative repository destination paths and rationale)

### Files Added

`tests/e2e/test_product_e2e_fixture.py`  
Rationale: this is the mandate's target fixture/harness file. It contains the fixture builder, runtime health checks, checkpoint assertions, evidence/receipt collector, deterministic repeat runner, negative fixture, and clean-reset command.

`tests/e2e/README.md`  
Rationale: required developer README for using the harness in development and CI without relying on undocumented setup.

### Files Modified

None. The existing `tests/e2e/test_live_e2e_proof_harness.py` was inspected but intentionally not modified or used as the M060 proof source because its external-boundary fixtures are test-owned local HTTP servers and the M0058 baseline classifies that evidence as `MOCKED` for production-provider/distribution reachability.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

Paste/copy the two bundled files into an existing repository checkout preserving these exact paths:

```text
tests/e2e/test_product_e2e_fixture.py
tests/e2e/README.md
```

No database migration, schema migration, application-code change, or production setup script is required for M060. The fixture creates its own SQLite database and seed/evidence directories under a controlled workspace at execution time.

Post-apply verification:

```bash
python -m pytest -q tests/e2e/test_product_e2e_fixture.py
```

Repeat deterministic proof:

```bash
python tests/e2e/test_product_e2e_fixture.py repeat --artifact-root .cae-m060-artifacts/repeat
```

Intentionally failing fixture:

```bash
python tests/e2e/test_product_e2e_fixture.py negative --workspace-root .cae-m060-artifacts/negative
```

Clean the controlled failure workspace while retaining failed evidence:

```bash
python tests/e2e/test_product_e2e_fixture.py clean-reset .cae-m060-artifacts/negative
```

## Test Command (exact pytest/test command to verify)

```bash
python -m pytest -q tests/e2e/test_product_e2e_fixture.py
```

Additional direct harness verification executed in the sandbox:

```bash
python tests/e2e/test_product_e2e_fixture.py repeat --artifact-root /tmp/cae_m060_final/repeat
python tests/e2e/test_product_e2e_fixture.py negative --workspace-root /tmp/cae_m060_final/negative
python tests/e2e/test_product_e2e_fixture.py clean-reset /tmp/cae_m060_final/negative
```

## Expected Test Results (number of automated tests, all passing)

**5 automated pytest tests; 5 passed, 0 failed.**

The direct repeat harness also returned `status: PASS`, `runs: 2`, and `receipt_identity_distinct: true`. The negative fixture returned `status: EXPECTED_FAILURE` with `ProgramTransitionBlockedError` and `aggregates_after_failure: 0`. Clean reset removed the controlled workspace and preserved `failure.json` under the sibling `.failed` namespace.

## Evidence / verification boundary

**What the verifier actually measures:** clean workspace creation; deterministic seed material and source/media fixture digests; real ProgramRegistry package resolution and preflight; real operator `/run` entrypoint; real canonical research state-machine transitions; real authority-lane enforcement; durable SQLite aggregate/lease/transition state; declared gate suspension; per-run receipt identity; deterministic semantic checkpoints across two independent clean runs; and fail-closed preflight failure for a missing required precondition.

**What it does not measure:** production PostgreSQL connectivity, an external inference provider, native OpenChatCut execution, human approval quality, or the missing standalone executable binding/package for the declared `RESEARCH_CANONICALIZATION_HARNESS_V1` identifier documented by the brownfield baseline.

**False-proof countercase:** reusing a previous SQLite workspace and reporting an old aggregate as a PASS. The fixture rejects any non-clean workspace and checks for zero pre-existing aggregates before dispatch; independent successful runs also have distinct run receipt identities while sharing the same stable semantic checkpoint signature.

**Environment-fidelity requirement:** the local proof is `E3_PRODUCTION_SHAPED`: actual CAE runtime/state authority with durable SQLite. Production-readiness claims require the governed production service environment and its optional dependencies.

**Operator validation required:** `True`. M060 stops at the existing `canonical_knowledge_commit_gate` with a persisted `AWAITING_APPROVAL` checkpoint; no operator decision is fabricated by the test.

## State transition evidence

```text
CLEAN → SEED → EXECUTE → ASSERT → COLLECT → CLEAN
```

Verified product checkpoint path:

```text
INITIAL → SOURCES_ATTACHED → CANDIDATES_EXTRACTED → CANONICALIZED → OKF_PROJECTED → AWAITING_APPROVAL
```

The durable SQLite transition ledger contains four product transitions plus the persisted gate-suspension transition. The gate is a real runtime boundary and is intentionally left fail-closed pending governed human approval.

## Source/control-state note

The uploaded archive has no `.git` metadata. The M0058 baseline records source Git commit basis `c41b68394ba8d1435c3cbb62b08f38908bbd3737`, but explicitly states that the archive cannot cryptographically attest to that commit. No unrelated repository control-state file was changed under M060 because the mandate's file boundary is limited to `tests/e2e/`, fixture utilities, and the proof harness subsystem. The exact source commit available from the governing baseline is therefore recorded as provenance, not as an attested post-apply commit.

## Operator Gate

Do you accept M060 and authorize M0061?

`ACCEPT → AUTHORIZE NEXT`  
`ACCEPT WITH LIMITATIONS → AUTHORIZE NEXT`  
`REPAIR → RETURN TO CURRENT MANDATE`  
`BLOCK → DO NOT PROCEED`
