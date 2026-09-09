# CA-M032b — Outcome Measurement Attribution

## Mandate ID & Title

**Mandate ID:** CA-M032b  
**Mandate Title:** Outcome Measurement Attribution  
**Requirement / Invariant:** FR-OUT-001  
**Core invariant:** Post-distribution performance and audience conversion observations must be attributable to the exact distributed release and to explicit tension collision anchors and creative components; campaign name and latest-release heuristics are not permitted.

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/outcome_attribution.py` | Added the bounded outcome event schema, exact release/delivery receipt validation, revision-specific causal reference validation, normalized performance/conversion yield math, append-only attribution store, deterministic JSON persistence/reload, release/anchor/component queries, trace output, duplicate-event idempotency, and conflict detection. | Accepted observations carry exact `release_id`, `release_manifest_sha256`, `distribution_receipt_id`, tension-anchor refs, creative-component refs, and optional audience refs; unresolved/mutated references fail closed; stored records are digest-checked and raw attribution cannot authorize a causal interpretation. |
| `tests/wave04/test_ca_m032b_outcome_attribution.py` | Added 12 self-contained tests covering positive attribution, unknown/mutated releases, failed distribution, two releases under one campaign, unresolved lineage, event idempotency/conflict, persistence/reload, traceability, yield aggregation/correlation, and metric normalization. | Executable proof covers the positive path, fail-closed countercases, the campaign-name/latest-release false proof, persistence integrity, and explicit separation between attribution and causal interpretation. |

## Files Added and Files Modified

**Files Added**

- `packages/ca_runtime/src/ca_runtime/outcome_attribution.py` — new CA-M032b runtime attribution boundary. The clean repository snapshot had no existing module at this exact destination.
- `tests/wave04/test_ca_m032b_outcome_attribution.py` — new mandate-specific unit/integration-style test suite.

**Files Modified**

- None outside the two mandate-target paths. The supplied repository archive contained no Git metadata, so repository commit history could not be inspected and no commit was created in the extracted sandbox.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

1. From the repository root, copy these two bundle files to the exact destinations shown below, replacing/adding only those paths:
   - `CA-M032b_BUNDLE/packages/ca_runtime/src/ca_runtime/outcome_attribution.py` → `packages/ca_runtime/src/ca_runtime/outcome_attribution.py`
   - `CA-M032b_BUNDLE/tests/wave04/test_ca_m032b_outcome_attribution.py` → `tests/wave04/test_ca_m032b_outcome_attribution.py`
2. No database migration is required by this bounded implementation. Outcome attribution persistence is provided as an append-only JSON store by the new runtime module; integrating that store with a deployment-specific database remains outside the mandate file boundary.
3. Install/activate the repository's normal Python test environment. The mandate test loads the target module directly so an unrelated optional `psycopg` import from `ca_runtime.__init__` does not prevent the bounded suite from executing in a minimal sandbox.
4. No other repository files should be changed as part of this mandate.
5. The implementation expects the incoming release manifest and distribution receipt to expose the existing repository-native fields `release_id`, `manifest_sha256`, `receipt_id`, `release_manifest_sha256`, and a successful `delivery_status=DELIVERED`. Where a concrete CA-M031 `DeliveryReceipt` object is supplied, its existing `verify(signing_secret)` method can also be invoked by passing `distribution_receipt_signing_secret`.

## Test Command (exact pytest/test command to verify)

```bash
pytest -q tests/wave04/test_ca_m032b_outcome_attribution.py tests/wave04/test_ca_m030_release_manifest.py
```

Optional compile check:

```bash
python -m py_compile packages/ca_runtime/src/ca_runtime/outcome_attribution.py tests/wave04/test_ca_m032b_outcome_attribution.py
```

## Expected Test Results (number of automated tests, all passing)

**CA-M032b focused suite:** 12 automated tests, **12 passed**.  
**CA-M030 release-manifest regression suite:** 14 automated tests, **14 passed**.  
**Combined verification:** 26 automated tests, **26 passed (100%)**.

### Evidence and limitations

- **EXECUTABLE:** exact-release attribution, fail-closed identity/digest checks, causal-lineage checks, two-release contrastive proof, idempotent duplicate handling, conflict rejection, persistence/reload, trace query, and yield/correlation math are exercised by the 12 CA-M032b tests.
- **SCHEMA:** `SCHEMA_VERSION = ca-outcome-attribution/v1`; required event fields and revision-specific causal references are validated by the runtime constructors.
- **PERSISTENCE:** `OutcomeAttributionStore.save()` / `load()` prove deterministic JSON round-trip and record digest preservation.
- **REGISTRY_SOURCE:** the implementation reuses the existing release-manifest and CA-M031 delivery receipt field names instead of creating a second release namespace.
- **DOCUMENT:** the implementation follows CA-M032/Q31 constraints in `docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_04/09_CA_MANDATE_032.md`, especially exact release attribution and rejection of campaign/latest-release joins.
- **LIMITATION:** the supplied archive is a clean source snapshot without `.git`, so an exact repository commit SHA is unavailable. No commit SHA is claimed. A deployment/operator should capture the applying repository commit after these files are pasted.
- **LIMITATION:** this bounded mandate does not wire a new database table/API/UI. It provides the canonical attribution module, append-only persistence representation, and query/trace boundary inside the mandated file paths. Any separate production storage adapter would require explicit scope authorization.

## Operator decision request

**Approve or reject CA-M032b** based on the executable evidence above. The green test suite is evidence of the declared bounded runtime behavior; it is not, by itself, an inferred Operator approval.
