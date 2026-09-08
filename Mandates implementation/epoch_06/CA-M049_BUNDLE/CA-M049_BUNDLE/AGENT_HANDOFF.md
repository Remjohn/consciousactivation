# AGENT HANDOFF — CA-M049
## Program Registry Immutability Requirement / INV-REG-001

**Mandate ID:** `CA-M049`
**Wave:** 06
**Canon question:** Q48
**Invariant:** `INV-REG-001`
**Status:** EXECUTION COMPLETE — Operator decision required (see §6)

---

## 1. Summary Table

| File Changed / Created | What Changed | Invariant Proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/program_registry.py` | **MODIFIED** — Added `ProgramStatus.RELEASED`; `IMMUTABLE_STATUSES` (`RELEASED`, `ACTIVE`); `ProgramImmutabilityError` and `ProgramDigestMismatchError`; `ProgramPackage.is_immutable()`, `with_status()`, `pinned_digests()` (MappingProxyType); `ProgramManifest.with_status()`; `ProgramRegistry.release()`, `verify_package_integrity()`, `get_pinned_digests()`, `freeze()`; strengthened `register()` to reject any overwrite of immutable identities even with `allow_overwrite=True`; discovery path skips overwrite of immutable identities when digests differ; `preflight(..., require_integrity=)` returns and optionally verifies pinned digests. | INV-REG-001: same-version overwrite of RELEASED/ACTIVE rejected at register path; digests pinned; integrity verification fails closed on byte mutation; new version registration leaves prior release untouched. |
| `tests/cae/test_ca_m049_program_registry.py` | **NEW FILE** — 21 acceptance tests covering G1–G9 gates and false-proof defence. | All gates; FP satisfied (register path itself enforces invariant, not merely an in-memory dict). |

---

## 2. Files Added and Files Modified

### Files Modified

| Relative path | Rationale |
|---|---|
| `packages/ca_runtime/src/ca_runtime/program_registry.py` | Primary surface for INV-REG-001: durable identity immutability, digest pinning, release promotion, integrity verification. |

### Files Added

| Relative path | Rationale |
|---|---|
| `tests/cae/test_ca_m049_program_registry.py` | Self-contained unit/integration proof for CA-M049 / INV-REG-001. |

No other repository files were modified. `program_state_runtime.py` was inspected; it already consumes `ProgramRegistry.get_program` and does not require a schema change for this mandate’s bounded scope (digest fields already exist on `ProgramPackage`).

---

## 3. Exact Paste Instructions

These files must replace/create at the exact repo-relative paths shown below. No other files are touched.

### File 1 — Modified (replace)

```
packages/ca_runtime/src/ca_runtime/program_registry.py
```

**Action:** Replace the existing `program_registry.py` with `CA-M049_BUNDLE/packages/ca_runtime/src/ca_runtime/program_registry.py`.

### File 2 — New test file (create)

```
tests/cae/test_ca_m049_program_registry.py
```

**Action:** Copy `CA-M049_BUNDLE/tests/cae/test_ca_m049_program_registry.py` into the repository at that path.

---

## 4. Manual Post-Apply Commands

```bash
# 1. Ensure ca_runtime / ca_contracts are importable
pip install -e packages/ca_contracts -e packages/ca_runtime --break-system-packages
# OR: export PYTHONPATH=packages/ca_runtime/src:packages/ca_contracts/src

# 2. Verify imports
python -c "from ca_runtime.program_registry import ProgramRegistry, ProgramStatus, ProgramImmutabilityError; print(ProgramStatus.RELEASED)"

# 3. Run the CA-M049 test suite
pytest tests/cae/test_ca_m049_program_registry.py -v

# 4. Optional regression
pytest tests/phase2/test_program_registry.py -v
```

No database migrations are required. No schema SQL changes. No npm scripts.

---

## 5. Test Command

```bash
pytest tests/cae/test_ca_m049_program_registry.py -v
```

---

## 6. Expected Test Results

**21 automated tests, all passing.**

| Class | Tests | Purpose |
|---|---|---|
| `TestGate1_FirstRegistrationPinsDigests` | 2 | First register + conflict without overwrite |
| `TestGate2_ReleasePreservesPins` | 1 | RELEASED promotion preserves digests |
| `TestGate3_SameVersionOverwriteRejected` | 3 | RELEASED/ACTIVE overwrite rejected; IMMUTABLE_STATUSES |
| `TestGate4_NewVersionAcceptedWithoutAlteringOld` | 1 | New version does not mutate prior release |
| `TestGate5_DigestMismatchDetection` | 2 | verify_package_integrity pass/fail |
| `TestGate6_PreflightPinningAndIntegrity` | 2 | Preflight pins + require_integrity |
| `TestGate7_FrozenModels` | 3 | Pydantic frozen models + with_status |
| `TestGate8_RegistryFreeze` | 1 | registry.freeze() blocks register |
| `TestGate9_DiscoveryRespectsImmutability` | 1 | Discovery will not overwrite RELEASED with different bytes |
| `TestFalseProof_RegisterPathEnforcesInvariant` | 2 | FP: register() path itself enforces INV-REG-001 |
| `TestEdgeCases` | 3 | not-found, quarantine, inspect flag |

Observed sandbox result: `21 passed`.

---

## 7. Operator Decision Request

Approve or reject `CA-M049` based on proof that released program packages are immutable by identity/version and that executions are pinned to exact `manifest_sha256` and `package_sha256` at the canonical registry/initialization boundary.

**Evidence classes exercised:** `EXECUTABLE`, `TEST`, `REGISTRY_SOURCE`.

**Limitations recorded:** In-memory registry only (no durable DB table in this mandate’s bounded surface); filesystem package roots must remain available for `verify_package_integrity(recompute_from_disk=True)`. Legacy packages with unknown byte identity are not auto-backfilled.
