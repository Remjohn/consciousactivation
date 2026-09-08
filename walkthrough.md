# Epoch 06 Walkthrough — Memory Write-Back, CAS Concurrency & Registry

**Status:** Verified and committed (`fc60d8c4`)  
**Date:** 2026-09-08  
**Result:** 135 passed, 0 failed (100% pass rate)

## Mandates applied

| Mandate | Requirement / Invariant | Destination surfaces |
|---|---|---|
| CA-M008 | FR-008 / FR-PORT-001 | `packages/ca_runtime/src/ca_runtime/frozen_portfolio.py` |
| CA-M023 | FR-023 / INV-YIELD-001 | `services/interview-intelligence/src/cae_interview_intelligence/yield_gating.py` |
| CA-M024 | FR-024 | `services/interview-intelligence/src/cae_interview_intelligence/preliminary_auth.py` |
| CA-M026 | FR-AUTH-001 | `packages/ca_runtime/src/ca_runtime/auth_decision_receipts.py` |
| CA-M032 | INV-MEM-001 | `packages/ca_runtime/src/ca_runtime/memory_writeback.py` |
| CA-M042 | INV-CAS-001 | `packages/ca_runtime/src/ca_runtime/sqlite_cas_transitions.py`<br>`packages/ca_runtime/src/ca_runtime/program_state_runtime.py` |
| CA-M049 | INV-REG-001 | `packages/ca_runtime/src/ca_runtime/program_registry.py` |

## Integration notes

- **Exact Source-to-Destination Mappings**: All 7 bundles from `Mandates implementation/epoch_06/` were ingested following their respective `AGENT_HANDOFF.md` instructions.
- **Modified Existing Files**:
  - `packages/ca_runtime/src/ca_runtime/program_state_runtime.py`: Integrated atomic SQLite CAS transitions (`cas_update_program_state_aggregate`) within `BEGIN IMMEDIATE` transaction boundaries, raising typed version mismatch errors.
  - `packages/ca_runtime/src/ca_runtime/program_registry.py`: Enforced program immutability rules (`ProgramStatus.RELEASED`, `IMMUTABLE_STATUSES`), preventing overwrite of active/released program identities and pinning package/manifest SHA-256 digests.
- **Disjoint Subsystems**: Other mandates introduced modular, self-contained files across `ca_runtime` and `interview-intelligence` with zero conflicting merges.
- **Persistence & Cryptographic Verification**:
  - CA-M008 enforces frozen campaign content portfolio contracts with deterministic digest verification before evidence admission.
  - CA-M023 and CA-M024 implement fail-closed yield gating and preliminary auth policies with structured deficit reports.
  - CA-M026 and CA-M032 provide durable SQLite stores with append-only trigger guards, HMAC signatures, and transactional CAS writebacks.

## Test matrix

| Mandate | Invariant | Test Suite | Tests | Result |
|---|---|---|:---:|:---:|
| CA-M008 | FR-008 / FR-PORT-001 | `tests/cae/test_ca_m008_frozen_portfolio.py` | 48 | PASS (48/48) |
| CA-M023 | FR-023 / INV-YIELD-001 | `tests/interview_intelligence/test_ca_m023_yield_gating.py` | 16 | PASS (16/16) |
| CA-M024 | FR-024 | `tests/interview_intelligence/test_ca_m024_preliminary_auth.py` | 19 | PASS (19/19) |
| CA-M026 | FR-AUTH-001 | `tests/wave04/test_ca_m026_auth_receipts.py` | 18 | PASS (18/18) |
| CA-M032 | INV-MEM-001 | `tests/wave05/test_ca_m032_memory_writeback.py` | 9 | PASS (9/9) |
| CA-M042 | INV-CAS-001 | `tests/cae/test_ca_m042_sqlite_cas.py` | 4 | PASS (4/4) |
| CA-M049 | INV-REG-001 | `tests/cae/test_ca_m049_program_registry.py` | 21 | PASS (21/21) |
| **Total** | | | **135** | **PASS (135/135, 100%)** |

### Unified command

```bash
python -m pytest -q \
  tests/cae/test_ca_m008_frozen_portfolio.py \
  tests/interview_intelligence/test_ca_m023_yield_gating.py \
  tests/interview_intelligence/test_ca_m024_preliminary_auth.py \
  tests/wave04/test_ca_m026_auth_receipts.py \
  tests/wave05/test_ca_m032_memory_writeback.py \
  tests/cae/test_ca_m042_sqlite_cas.py \
  tests/cae/test_ca_m049_program_registry.py
```

**Unified result:** `135 passed in 72.54s (100% pass rate)`

---

# Epoch 07 Walkthrough — Grounding, Release Integrity, Receipts, Isolation, Economics & Voice DNA

**Status:** Verified and committed
**Date:** 2026-09-08
**Result:** 113 passed, 0 failed, 2 environment-capability skips

## Mandates applied

| Mandate | Requirement / Invariant | Exact destination surfaces |
|---|---|---|
| CA-M029 | FR-029 / INV-NO-INVENT-001 | `packages/ca_runtime/src/ca_runtime/no_unanchored_invention.py`<br>`tests/wave04/test_ca_m029_no_unanchored_invention.py` |
| CA-M030 | FR-REL-001 / INV-REL-001 | `packages/ca_runtime/src/ca_runtime/release_manifest.py`<br>`tests/wave04/test_ca_m030_release_manifest.py` |
| CA-M043 | INV-MRK-001 | `packages/ca_runtime/src/ca_runtime/merkle_receipt_chain.py`<br>`tests/cae/test_ca_m043_merkle_receipts.py` |
| CA-M047 | INV-ISO-001 | `packages/ca_runtime/src/ca_runtime/workspace_isolation.py`<br>`tests/cae/test_ca_m047_workspace_isolation.py` |
| CA-M051 | INV-ECON-001 | `packages/ca_runtime/src/ca_runtime/agent_invocation.py`<br>`packages/ca_runtime/src/ca_runtime/program_state_runtime.py`<br>`tests/pipeline/test_ca_m051_quota_engine.py` |
| CA-M052 | INV-VOICE-001 | `services/collision-intelligence/src/cae_collision_intelligence/composer.py`<br>`packages/ca_runtime/src/ca_runtime/collision_hypothesis_program.py`<br>`tests/phase4/test_ca_m052_voice_dna.py` |

## Integration notes

- **Exact Source-to-Destination Mappings:** All six bundles from `Mandates implementation/epoch_07/` were applied according to their `AGENT_HANDOFF.md` files.
- **Existing-file replacements:** CA-M051 replaced the canonical `agent_invocation.py` and `program_state_runtime.py` surfaces; CA-M052 replaced the canonical collision composer and hypothesis-program surfaces. No destination was shared by multiple Epoch 07 bundles, so no cross-bundle merge was required.
- **Bounded implementations:** No migrations or unrelated API/storage surfaces were added. The handoff-defined runtime boundaries and mandate-specific tests were preserved exactly.
- **Syntax and hygiene:** All 14 mandate files passed `py_compile`/`compileall`; `git diff --check` passed.

## Test matrix

| Mandate | Invariant | Focused test suite | Collected | Result |
|---|---|---|:---:|---:|
| CA-M029 | FR-029 / INV-NO-INVENT-001 | `tests/wave04/test_ca_m029_no_unanchored_invention.py` | 12 | PASS (12/12) |
| CA-M030 | FR-REL-001 / INV-REL-001 | `tests/wave04/test_ca_m030_release_manifest.py` | 14 | PASS (14/14) |
| CA-M043 | INV-MRK-001 | `tests/cae/test_ca_m043_merkle_receipts.py` | 26 | PASS (26/26) |
| CA-M047 | INV-ISO-001 | `tests/cae/test_ca_m047_workspace_isolation.py` | 39 | PASS (37/37 executed); 2 skipped |
| CA-M051 | INV-ECON-001 | `tests/pipeline/test_ca_m051_quota_engine.py` | 14 | PASS (14/14) |
| CA-M052 | INV-VOICE-001 | `tests/phase4/test_ca_m052_voice_dna.py` | 10 | PASS (10/10) |
| **Unified Epoch 07** | | all six suites above | **115** | **113 passed, 0 failed, 2 skipped** |

### Additional CA-M052 affected regressions

```text
17 passed
```

The complete command also covered:

```text
tests/collision_intelligence/test_collision_composition.py
tests/collision_intelligence/test_four_world_intersection.py
tests/collision_intelligence/test_collision_domain_contracts.py
tests/collision_intelligence/test_collision_adversarial_cases.py
```

### Unified command

```bash
pytest -q \
  tests/wave04/test_ca_m029_no_unanchored_invention.py \
  tests/wave04/test_ca_m030_release_manifest.py \
  tests/cae/test_ca_m043_merkle_receipts.py \
  tests/cae/test_ca_m047_workspace_isolation.py \
  tests/pipeline/test_ca_m051_quota_engine.py \
  tests/phase4/test_ca_m052_voice_dna.py
```

**Unified result:** `113 passed, 0 failed, 2 skipped in 31.29s`.

The two skips are the M047 cross-workspace and cross-campaign symlink-alias cases. Windows returned `WinError 1314` because this host does not grant symbolic-link creation and Developer Mode is disabled; the tests retain their fail-closed assertions and are not altered or suppressed.

---

# Epoch 08 Walkthrough — Distribution, Attribution, Replay, Recovery, Control, DAG & Telemetry

**Status:** Verified and committed
**Date:** 2026-09-08
**Result:** 89 passed, 0 failed (100% pass rate for all seven Epoch 08 mandate suites)

## Mandates applied

| Mandate | Requirement / Invariant | Exact destination surfaces |
|---|---|---|
| CA-M031 | FR-DIST-001 | `packages/ca_runtime/src/ca_runtime/distribution_delivery.py`<br>`tests/wave04/test_ca_m031_distribution_delivery.py` |
| CA-M032b | FR-OUT-001 | `packages/ca_runtime/src/ca_runtime/outcome_attribution.py`<br>`tests/wave04/test_ca_m032b_outcome_attribution.py` |
| CA-M044 | INV-RPL-001 | `packages/ca_runtime/src/ca_runtime/replay_engine.py`<br>`tests/cae/test_ca_m044_replay_engine.py` |
| CA-M045 | INV-REC-001 | `packages/ca_runtime/src/ca_runtime/zombie_reconciler.py`<br>`tests/cae/test_ca_m045_zombie_reconciler.py` |
| CA-M046 | INV-PREEMPT-001 | `packages/ca_runtime/src/ca_runtime/operator_preemption.py`<br>`packages/ca_runtime/src/ca_runtime/program_operator_runtime.py`<br>`packages/ca_runtime/src/ca_runtime/agent_host_runner.py`<br>`api/routers/programs.py`<br>`tests/cae/test_ca_m046_operator_preemption.py` |
| CA-M050 | INV-DAG-001 | `services/pipeline/src/cmf_pipeline/evidence/__init__.py`<br>`services/pipeline/src/cmf_pipeline/evidence/dag.py`<br>`tests/pipeline/test_ca_m050_evidence_dag.py` |
| CA-M054 | INV-TELEM-001 | `packages/ca_runtime/src/ca_runtime/factory_observability.py`<br>`packages/ca_runtime/src/ca_runtime/program_operator_runtime.py`<br>`tests/cae/test_ca_m054_telemetry_flywheel.py` |

## Integration notes

- **Exact mappings:** M031, M032b, M044, M045, M046, and M050 were applied from their handoffs without alternate paths.
- **M054 authority decision:** The operator approved the canonical Q53 scope (`INV-TELEM-001`) rather than the conflicting pipeline reference (`INV-TEL-001`). Implementation is therefore bounded to runtime telemetry and genuine operator gate capture in `factory_observability.py` and `program_operator_runtime.py`.
- **M054 behavior:** The canonical runtime now exposes six telemetry classes, redacted content-addressed events, attributable `HumanResolutionEpisode` records, eligible chosen/rejected preference derivatives, manifest verification, and read-only training exports. Missing alternatives remain recorded but are never promoted into synthetic preference data.
- **Syntax and hygiene:** All Epoch 08 implementation/test files passed compilation; `git diff --check` passed.

## Test matrix

| Mandate | Invariant | Handoff/mandate test suite | Tests | Result |
|---|---|---|:---:|---:|
| CA-M031 | FR-DIST-001 | `tests/wave04/test_ca_m031_distribution_delivery.py` | 11 | PASS (11/11) |
| CA-M032b | FR-OUT-001 | `tests/wave04/test_ca_m032b_outcome_attribution.py` | 12 | PASS (12/12) |
| CA-M044 | INV-RPL-001 | `tests/cae/test_ca_m044_replay_engine.py` | 10 | PASS (10/10) |
| CA-M045 | INV-REC-001 | `tests/cae/test_ca_m045_zombie_reconciler.py` | 9 | PASS (9/9) |
| CA-M046 | INV-PREEMPT-001 | `tests/cae/test_ca_m046_operator_preemption.py` | 11 | PASS (11/11) |
| CA-M050 | INV-DAG-001 | `tests/pipeline/test_ca_m050_evidence_dag.py` | 26 | PASS (26/26) |
| CA-M054 | INV-TELEM-001 | `tests/cae/test_ca_m054_telemetry_flywheel.py` | 10 | PASS (10/10) |
| **Unified Epoch 08** | | all seven suites above | **89** | **PASS (89/89, 100%)** |

### Targeted handoff regressions

- CA-M031 + CA-M030 release manifest: **25 passed**.
- CA-M032b + CA-M030 release manifest: **26 passed**.
- CA-M054 affected direct regressions: `tests/cae/test_program_operator_runtime.py` **12 passed** and `tests/cae/test_m63_unified_factory_commands_read_only_observability.py` **9 passed**.
- The separately run legacy M68 persistence suite had **3 passed / 5 failed** on unchanged state-version expectations (`expected v2/v3`, runtime returns v1/v2). It is outside the Epoch 08 mandate suite and no Epoch 08 change touched the state-version implementation; the failures were recorded rather than weakened.

### Unified command

```bash
pytest -q \
  tests/wave04/test_ca_m031_distribution_delivery.py \
  tests/wave04/test_ca_m032b_outcome_attribution.py \
  tests/cae/test_ca_m044_replay_engine.py \
  tests/cae/test_ca_m045_zombie_reconciler.py \
  tests/cae/test_ca_m046_operator_preemption.py \
  tests/pipeline/test_ca_m050_evidence_dag.py \
  tests/cae/test_ca_m054_telemetry_flywheel.py
```

**Unified result:** `89 passed in 23.06s (100% pass rate)`.
