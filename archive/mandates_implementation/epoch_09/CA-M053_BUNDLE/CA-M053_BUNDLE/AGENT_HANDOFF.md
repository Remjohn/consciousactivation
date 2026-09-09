# CA-M053 — CSEB Golden Benchmark Certification

## Mandate ID & Title

**Mandate ID:** `CA-M053`  
**Title:** CSEB Golden Benchmark Certification  
**Requirement / Invariant:** `INV-BENCH-001`

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/pipeline/src/cmf_pipeline/benchmarks/cseb_suite.py` | Added a deterministic CSEB golden-benchmark engine with five certification dimensions (semantic, governance, operational, economic, human), versioned golden cases, strict basis-point tolerance policies, deterministic dataset hashing, signed `ModelCertificationReceipt` issuance/verification, expiry/model/revision binding, placeholder-hash rejection, and fail-closed routing admission. | `INV-BENCH-001`: a model is routable only with a current, correctly signed CSEB certification bound to the expected model/version and current benchmark/golden-dataset revisions; score-only or dummy-hash proof is insufficient. |
| `tests/pipeline/test_ca_m053_cseb_benchmark.py` | Added 17 self-contained tests covering all five dimensions, strict tolerance failure, case-set integrity, certificate issuance, JSON round-trip, signature tampering, expiry, model/revision mismatch, missing receipt, the required dummy-hash false-proof countercase, valid routing admission, and deterministic dataset revision binding. | Positive, negative, false-proof, and receipt-integrity predicates execute against the CSEB implementation at the mandated pipeline file boundary. |

## Files Added and Files Modified

### Files Added

- `services/pipeline/src/cmf_pipeline/benchmarks/cseb_suite.py` — new CA-M053 implementation surface. The `benchmarks` directory did not previously contain a CSEB suite.
- `tests/pipeline/test_ca_m053_cseb_benchmark.py` — new mandate-specific positive/negative certification test suite.

### Files Modified

None.

Rationale: the uploaded repository does not contain a pre-existing CSEB suite or CA-M053 test at the user-specified paths, so the implementation is additive and does not require unrelated edits.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

From the repository root, copy the two bundled files to these exact destinations:

```text
CA-M053_BUNDLE/services/pipeline/src/cmf_pipeline/benchmarks/cseb_suite.py
    -> services/pipeline/src/cmf_pipeline/benchmarks/cseb_suite.py

CA-M053_BUNDLE/tests/pipeline/test_ca_m053_cseb_benchmark.py
    -> tests/pipeline/test_ca_m053_cseb_benchmark.py
```

No database migration is required. No deployment topology or external provider configuration is introduced by these files.

The CSEB suite is deterministic and provider-agnostic: a caller supplies observed candidate outputs, the suite evaluates them against the versioned golden reference set, and `CertificationRoutingGate.require(...)` must be called before governed routing. The receipt is HMAC-SHA256 signed using an operator-supplied signing secret and is bound to model identity/version, benchmark revision, golden-dataset revision, and dataset digest.

Post-apply verification:

```bash
pytest -q tests/pipeline/test_ca_m053_cseb_benchmark.py
python -m py_compile services/pipeline/src/cmf_pipeline/benchmarks/cseb_suite.py
```

## Test Command (exact pytest/test command to verify)

```bash
pytest -q tests/pipeline/test_ca_m053_cseb_benchmark.py
```

## Expected Test Results (number of automated tests, all passing)

**17 automated tests, 17 passing, 0 failing.**

Observed sandbox result:

```text
.................                                                        [100%]
17 passed in 0.12s
```

## Evidence and limitations

Evidence classes: `TEST`, `EXECUTABLE`, `SCHEMA`.

The implementation proves deterministic golden-set scoring, strict score tolerances, cryptographic receipt integrity, expiry/revision/model binding, and fail-closed routing admission within the CSEB boundary.

The required false-proof countercase is explicitly covered: a perfect benchmark score plus an apparently valid 64-character dummy hash is rejected because no valid signed certification exists.

Environment fidelity limitation: the uploaded archive does not contain `.git` metadata, so an exact repository commit SHA cannot be captured from this artifact. The implementation was tested directly in the extracted repository and the mandate-specific suite passed 17/17.

The checked-in CA-M053 mandate document names a broader canonical primary surface (`tests/test_model_benchmarks.py` and `packages/ca_runtime/src/ca_runtime/agent_invocation.py`), while the execution request supplied for this task explicitly names the two pipeline paths delivered above. This bundle follows the supplied execution file boundary and does not broaden scope into the runtime package.

Operator decision remains external to this handoff: **APPROVE**, **REJECT**, or **DEFER**.
