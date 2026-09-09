# CA-M055 — Autonomous Collision Approval Gate

## Mandate ID & Title

**Mandate ID:** CA-M055  
**Mandate Title:** Autonomous Collision Approval Gate  
**Requirement / Invariant:** INV-AUTO-001

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/pipeline/src/cmf_pipeline/collision/autonomous_gate.py` | Added a deterministic, configurable collision policy gate with strict per-dimension thresholds, weighted aggregate thresholding, borderline-to-manual routing, fail-closed validation, and SHA-256 approval receipts bound to collision evidence and policy. | High-confidence collisions are autonomously approved only when every required score and the aggregate score meet policy; borderline or insufficient evidence cannot silently become an autonomous approval. |
| `tests/pipeline/test_ca_m055_autonomous_gate.py` | Added self-contained positive, boundary, borderline, rejection, malformed-input, false-proof, determinism, receipt-lineage, and custom-policy tests. | INV-AUTO-001 is executable at the named pipeline boundary, including the required high-confidence false-proof countercase. |

## Files Added and Files Modified

### Files Added

- `services/pipeline/src/cmf_pipeline/collision/autonomous_gate.py` — New CA-M055 implementation because the supplied repository snapshot had no existing autonomous collision approval gate at the mandated target path.
- `tests/pipeline/test_ca_m055_autonomous_gate.py` — New mandate-specific test suite because the supplied repository snapshot had no CA-M055 test at the mandated target path.

### Files Modified

None.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

Copy the two files from this bundle to the exact relative repository destinations shown above, preserving package paths. No database migration or schema change is required; the implementation is pure deterministic policy evaluation and receipt hashing.

From the repository root, run:

```bash
python -m pytest -q tests/pipeline/test_ca_m055_autonomous_gate.py
```

For an additional syntax check:

```bash
python -m compileall -q services/pipeline/src/cmf_pipeline/collision/autonomous_gate.py
```

The test module loads the gate implementation directly to isolate CA-M055 verification from unrelated `cmf_pipeline` package bootstrap dependencies.

## Test Command

```bash
python -m pytest -q tests/pipeline/test_ca_m055_autonomous_gate.py
```

## Expected Test Results (number of automated tests, all passing)

**20 automated tests, all passing.**

The suite verifies:

- autonomous approval for high-confidence collisions;
- inclusive exact-threshold behavior;
- borderline dimension and aggregate routing to manual review;
- hard rejection for scores materially below policy;
- fail-closed handling of missing, unknown, non-finite, boolean, and out-of-range scores;
- rejection of confidence-only false proofs where another policy dimension fails;
- refusal to grant autonomous approval through `require_autonomous_approval` when manual review is required;
- deterministic receipts for identical evidence;
- receipt binding to collision identity and policy configuration;
- invalid policy construction and higher-bar custom policies.

## Evidence / Authority Note

The repository contains an older checked-in CA-M055 mandate at `docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_07/07_CA_MANDATE_055.md` that defines CA-M055 as Q54 / `INV-COLL-002` with a mandatory human hypothesis approval gate. The later repository execution schedule and prompt-reference block independently define CA-M055 as the supplied `INV-AUTO-001` autonomous scoring gate targeting `services/pipeline/src/cmf_pipeline/collision/autonomous_gate.py`. This is a material authority discrepancy. The implementation follows the supplied CA-M055 mandate details and the later execution schedule; the discrepancy should be resolved by repository governance before promotion.

The uploaded repository archive has no usable `.git` metadata, so an exact commit SHA cannot be captured from the supplied snapshot.

**Operator decision required:** APPROVE, REJECT with findings, or DEFER pending named remediation.
