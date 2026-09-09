# CA-M029 — No-Unanchored-Invention Invariant

## Mandate ID & Title

**Mandate ID:** `CA-M029`  
**Mandate Title:** `No-Unanchored-Invention Invariant`  
**Requirement / Invariant:** `FR-029` / `INV-NO-INVENT-001`  
**Requested target:** sentence-level composition grounding against admitted evidence and exact verbatim sources.

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/no_unanchored_invention.py` | Added a fail-closed sentence-level composition gate with content-addressed evidence resolution, revision/digest verification, exact verbatim quote verification, explicit versioned connective allow-listing, and `BLOCK` / `FLAG` / `PURGE` enforcement. | Every substantive sentence must have independently resolved admitted evidence plus a verified verbatim anchor occurring in that sentence, or an explicitly authorised connective transformation. One failed sentence blocks the whole composition admission. |
| `tests/wave04/test_ca_m029_no_unanchored_invention.py` | Added 12 self-contained acceptance tests covering positive grounding, stale references, quote tampering, anti-centroid failure, paragraph-level borrowing false proof, connective policy, purge/flag behavior, forged boolean metadata, mapping input, sentence extraction, and contract constants. | The real content-addressed `InterviewRepository` lookup path is exercised; unsupported sentences fail closed and the false-proof countercase cannot pass by coverage or metadata alone. |

## Files Added and Files Modified (with exact relative repository destination paths and rationale)

### Files Added

1. `packages/ca_runtime/src/ca_runtime/no_unanchored_invention.py`  
   **Rationale:** The requested M029 runtime surface did not exist in the supplied repository snapshot. This file implements the hard grounding predicate and preserves evidence lineage in the audit result.

2. `tests/wave04/test_ca_m029_no_unanchored_invention.py`  
   **Rationale:** The requested M029 test surface did not exist in the supplied repository snapshot. This file provides the mandate-specific executable proof suite.

### Files Modified

None.

No migration, API, release, distribution, outcome, memory, or adjacent canonical-question files were modified.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

From the repository root, copy the two bundle paths exactly into the same relative destinations:

```text
CA-M029_BUNDLE/packages/ca_runtime/src/ca_runtime/no_unanchored_invention.py
    -> packages/ca_runtime/src/ca_runtime/no_unanchored_invention.py

CA-M029_BUNDLE/tests/wave04/test_ca_m029_no_unanchored_invention.py
    -> tests/wave04/test_ca_m029_no_unanchored_invention.py
```

No database migration is required for this bounded implementation.

Install the package dependencies using the repository's normal package setup before running the suite. The runtime package declares `psycopg` as a dependency; the supplied archive's execution environment did not contain that wheel.

```bash
python -m pip install -e packages/ca_contracts -e packages/ca_runtime
```

Then run the focused mandate test exactly as shown below.

The M029 implementation is designed to consume an existing canonical resolver exposing `get_object_by_sha(object_id, sha256)` such as the interview repository. It does not create a second evidence authority.

## Test Command (exact pytest/test command to verify)

```bash
pytest -q tests/wave04/test_ca_m029_no_unanchored_invention.py
```

## Expected Test Results (number of automated tests, all passing)

**Expected:** `12 passed`.

**Observed in the supplied sandbox:** `12 passed in 0.13s` for the exact focused command.

The broader Wave 04 command was also attempted:

```bash
pytest -q tests/wave04
```

That collection could not start because the uploaded execution environment is missing repository dependencies (`psycopg`, and subsequently `ca_delegation_rc4`). Those are environment prerequisites unrelated to the M029 implementation. This limitation is recorded rather than bypassed.

## Verification and Evidence Package

| Evidence class | Locator | What it proves |
|---|---|---|
| `DOCUMENT` | `docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_04/06_CA_MANDATE_029.md` | M029 scope, hard semantic-unit predicate, exact-verbatim expectation, fail-closed requirement, false-proof countercase, and prohibited expansion. |
| `REGISTRY_SOURCE` | `services/interview/src/conscious_activations_interview_expression/repository.py:get_object_by_sha` | Canonical content-addressed evidence lookup by object id + exact SHA-256. |
| `EXECUTABLE` | `packages/ca_runtime/src/ca_runtime/no_unanchored_invention.py:verify_evidence_reference` | Independent reference identity, payload digest, admission state, and quote-hash verification. |
| `EXECUTABLE` | `packages/ca_runtime/src/ca_runtime/no_unanchored_invention.py:audit_sentences` | Sentence-by-sentence hard gate; one failed material sentence makes the composition non-admissible. |
| `EXECUTABLE` | `packages/ca_runtime/src/ca_runtime/no_unanchored_invention.py:require_admitted_composition` | Release-safe compilation path that raises on the first failed grounding unit. |
| `TEST` | `tests/wave04/test_ca_m029_no_unanchored_invention.py:test_unanchored_factual_sentence_is_fatal_even_when_other_sentences_are_grounded` | Anti-centroid proof: 80%/most-grounded coverage does not compensate for one invented sentence. |
| `TEST` | `tests/wave04/test_ca_m029_no_unanchored_invention.py:test_forged_anchored_boolean_is_not_a_grounding_authority` | `anchored=true` metadata and confidence do not constitute grounding authority. |
| `TEST` | `tests/wave04/test_ca_m029_no_unanchored_invention.py:test_real_content_addressed_lookup_rejects_stale_revision` | Exact content-addressed revision/digest mismatch fails closed. |
| `TEST` | `tests/wave04/test_ca_m029_no_unanchored_invention.py:test_mutated_quote_fails_even_when_object_metadata_is_present` | Verbatim quote tampering fails against the admitted evidence object. |

## False-proof countercase result

**PASS / rejected as required.** A grounded sentence followed by a polished, plausible but unanchored factual sentence produces `admitted == False`, and `require_admitted_composition()` raises `NoUnanchoredInventionError`.

## Residual limitations

1. The gate deliberately requires an exact verbatim anchor for an `EVIDENCE_BACKED` sentence. A semantic paraphrase without an exact quoted anchor is not deterministically provable by this runtime surface and must instead be represented as an explicitly authorised connective transformation or otherwise specified upstream.
2. The supplied source archive contains no `.git` metadata. Therefore an exact upstream **git commit SHA cannot be truthfully captured from the uploaded snapshot**. The bundle records this rather than inventing one.
3. The complete Wave 04 suite could not be collected in the sandbox because required third-party repository dependencies are absent.

## Completion / operator decision request

The M029 bounded implementation and focused executable evidence are complete. **Operator approval/rejection is still required** for `CA-M029`; green M029 tests do not infer operator approval.
