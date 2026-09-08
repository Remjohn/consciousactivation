# Epoch 05 Walkthrough — Gate Resumption, Receipts & Policy Binding

**Status:** Verified and committed  
**Date:** 2026-09-08  
**Result:** 173 passed, 2 skipped (Windows symlink privilege), 0 failed

## Mandates applied

| Mandate | Requirement / Invariant | Destination surfaces |
|---|---|---|
| CA-M003 | FR-003 / INV-SUB-001 | `packages/ca_runtime/src/ca_runtime/subject_constitution.py` |
| CA-M020 | FR-020 | `services/interview/.../reaction_receipts.py` |
| CA-M022 | FR-022 / FR-ELIC-002 | `services/interview/.../adaptive_remediation.py` |
| CA-M025 | FR-POL-001 | `packages/ca_runtime/src/ca_runtime/campaign_auth_policy.py` |
| CA-M028 | FR-POL-002 / INV-POL-001 | `packages/ca_runtime/src/ca_runtime/policy_revision_binding.py` |
| CA-M041 | INV-GATE-002 | `packages/ca_runtime/src/ca_runtime/gate_resumption.py` |
| CA-M048 | INV-SEC-001 | `packages/ca_runtime/src/ca_runtime/sandbox.py` + `agent_invocation.py` merge |

## Integration notes

- CA-M048 is the only bundle that modified an existing file (`agent_invocation.py`). The `tool:default-` bypass was removed while preserving prior CA-M038 / Epoch 04 content.
- CA-M003 signing now mints signatures before constructing frozen+slots records; amendment receipt IDs are post-sign linkage metadata.
- CA-M020 reaction payloads are mapped into the ca_contracts no-float canonical subset; media coordinates are duration-validated via CA-M021.
- CA-M048 Windows: `echo` launches via a shell=False Python printer when POSIX `echo` is absent; symlink escape tests skip when the process lacks symlink privilege.

## Test matrix

| Mandate | Suite | Result |
|---|---|---|
| CA-M003 | `tests/cae/test_ca_m003_subject_constitution.py` | PASS |
| CA-M020 | `tests/phase4/test_ca_m020_reaction_receipts.py` | PASS |
| CA-M022 | `tests/phase4/test_ca_m022_adaptive_remediation.py` | PASS |
| CA-M025 | `tests/wave04/test_ca_m025_campaign_auth_policy.py` | PASS |
| CA-M028 | `tests/wave04/test_ca_m028_policy_revision_binding.py` | PASS |
| CA-M041 | `tests/cae/test_ca_m041_gate_resumption.py` | PASS |
| CA-M048 | `tests/cae/test_ca_m048_sandbox.py` | PASS (2 skipped: symlink privilege) |

### Unified command

```bash
python -m pytest -q \
  tests/cae/test_ca_m003_subject_constitution.py \
  tests/phase4/test_ca_m020_reaction_receipts.py \
  tests/phase4/test_ca_m022_adaptive_remediation.py \
  tests/wave04/test_ca_m025_campaign_auth_policy.py \
  tests/wave04/test_ca_m028_policy_revision_binding.py \
  tests/cae/test_ca_m041_gate_resumption.py \
  tests/cae/test_ca_m048_sandbox.py
```

**Unified result:** `173 passed, 2 skipped in ~40s`
