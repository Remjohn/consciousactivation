# CA-M015 Agent Handoff

## Implementation status

CA-M015 is implemented at the Interview Expression evidence boundary as a source-bound, immutable `verbatim_evidence` object and a downstream composition guard. The governing mandate file in this repository snapshot is `docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_02/07_CA_MANDATE_015.md` (Verbatim Spoken Capture Integrity). The user-supplied label “Evaluation & Guardrails Engine” does not match that governing mandate title; this bundle follows the repository mandate by ID.

Two environment limitations remain intentionally unclaimed: this uploaded snapshot has no `.git` metadata, so an exact commit SHA cannot be captured; and the required `docs/cae/cae_master_57_question_convergence_canon.md` Q15 authority file is absent from the snapshot. No CAE control-state update or operator approval is fabricated. Tests were not run, per the execution instruction.

## Summary

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/interview/src/conscious_activations_interview_expression/verbatim.py` | Added canonical `verbatim_evidence` admission service with exact codepoint slicing, source-media digest pinning, source-span bounds, transcript digest, alignment/phrase lineage, immutable revision storage, and mandate receipt. | A quoted span is admitted only when `quote_text == transcript_text[character_start:character_end]`, the transcript digest matches, the source package/media identity matches, the temporal span is bounded, and all pinned lineage resolves. Semantic similarity is never used as proof. |
| `services/interview/src/conscious_activations_interview_expression/application.py` | Exposed the verbatim evidence service on the application boundary. | Verbatim admission is available through the governed Interview Expression application rather than as an ad-hoc side path. |
| `services/interview/src/conscious_activations_interview_expression/inventory.py` | Changed asset-package quote composition to consume only validated `verbatim_evidence`; selected phrase references are checked by full pinned ref, including revision/digest. | Downstream quote text cannot be regenerated from phrase text, summaries, or similarity; missing/stale/mismatched evidence fails closed. |
| `services/interview/src/conscious_activations_interview_expression/schemas.py` | Registered the `verbatim-evidence` object schema name/id field. | The canonical evidence object has an explicit schema registry entry. |
| `services/interview/src/conscious_activations_interview_expression/demo.py` | Updated the development demo to admit verbatim evidence before asset inventory compilation. | The reference flow does not bypass CA-M015 before downstream quote composition. |
| `tests/phase4/test_ca_m015_verbatim_capture.py` | Added positive, negative, revision, provenance, editorial-drift, downstream-composition, exact-whitespace, and media-bound tests. | The required hard negatives and lineage failures are encoded as automated checks. |
| `tests/phase4/test_ts_int_005_inventory.py` | Updated the existing inventory integration test to supply canonical verbatim evidence. | Existing inventory behavior remains guarded by the new evidence admission boundary. |

## Exact paste instructions

Replace or add the following repository paths with the files at the same relative paths in this bundle. Each file is complete; no patching or merging is required.

1. `CA-M015_BUNDLE/services/interview/src/conscious_activations_interview_expression/verbatim.py` -> `services/interview/src/conscious_activations_interview_expression/verbatim.py` (new file).
2. `CA-M015_BUNDLE/services/interview/src/conscious_activations_interview_expression/application.py` -> `services/interview/src/conscious_activations_interview_expression/application.py`.
3. `CA-M015_BUNDLE/services/interview/src/conscious_activations_interview_expression/inventory.py` -> `services/interview/src/conscious_activations_interview_expression/inventory.py`.
4. `CA-M015_BUNDLE/services/interview/src/conscious_activations_interview_expression/schemas.py` -> `services/interview/src/conscious_activations_interview_expression/schemas.py`.
5. `CA-M015_BUNDLE/services/interview/src/conscious_activations_interview_expression/demo.py` -> `services/interview/src/conscious_activations_interview_expression/demo.py`.
6. `CA-M015_BUNDLE/tests/phase4/test_ca_m015_verbatim_capture.py` -> `tests/phase4/test_ca_m015_verbatim_capture.py` (new file).
7. `CA-M015_BUNDLE/tests/phase4/test_ts_int_005_inventory.py` -> `tests/phase4/test_ts_int_005_inventory.py`.

No other repository paths are part of the CA-M015 implementation bundle.

## Manual post-apply commands

No database migration is required. The implementation reuses the existing immutable `ie_objects`, idempotency, and edge stores.

Run the new and affected tests after applying the bundle (not run by this agent because the operator explicitly prohibited running tests):

```text
python -m pytest -q tests/phase4/test_ca_m015_verbatim_capture.py tests/phase4/test_ts_int_005_inventory.py
```

Optional syntax-only check equivalent to the validation performed before packaging:

```text
python -m py_compile services/interview/src/conscious_activations_interview_expression/verbatim.py services/interview/src/conscious_activations_interview_expression/application.py services/interview/src/conscious_activations_interview_expression/inventory.py services/interview/src/conscious_activations_interview_expression/schemas.py services/interview/src/conscious_activations_interview_expression/demo.py tests/phase4/test_ca_m015_verbatim_capture.py tests/phase4/test_ts_int_005_inventory.py
```

Before declaring the mandate complete in the CAE control plane, restore/consult the missing Master Convergence Canon Q15 authority document, record the exact repository commit SHA, execute the tests above, and update the authorized mandate state/receipt according to the repository governance procedure. Do not mark CA-M015 approved solely from this bundle.

## New automated tests included

- `test_exact_spoken_capture_preserves_disfluency_and_source_lineage`
- `test_same_meaning_grammar_cleanup_is_rejected_as_editorial_drift`
- `test_material_punctuation_change_is_rejected_even_when_character_span_is_valid`
- `test_exact_whitespace_is_part_of_verbatim_identity`
- `test_source_span_beyond_media_duration_is_rejected`
- `test_stale_transcript_digest_is_rejected_before_admission`
- `test_stale_character_span_is_rejected_from_current_transcript`
- `test_source_media_digest_mismatch_is_rejected`
- `test_source_span_lineage_mismatch_is_rejected`
- `test_missing_phrase_lineage_is_rejected`
- `test_evidence_revision_preserves_previous_revision`
- `test_downstream_inventory_rejects_unanchored_quote_material`
- `test_downstream_inventory_consumes_canonical_verbatim_text_not_phrase_text`

Existing integration test updated: `test_inventory_only_consumes_approved_moments`.

## Evidence record

| Field | Record |
|---|---|
| Environment | Uploaded `codebase_clean.zip`, extracted repository snapshot; no `.git` metadata present. |
| Commands actually run | Static Python AST parsing of all seven changed Python files; file/path inspection. No test command was run. |
| Fixture | Existing phase-4 synthetic interview support, with exact transcript text `I thought success meant control. Um then I learned to listen.` and a source media digest pinned to the admitted source package. |
| Property targeted | Exact character/codepoint equality, source media identity, source temporal anchor, transcript digest, phrase/alignment lineage, immutable historical revision, and downstream canonical consumption. |
| Result | Syntax parsing passed for all seven changed Python files. Test execution evidence is intentionally absent. |
| Limitation | The implementation validates transcript/evidence lineage but does not independently prove that a derivative transcript is acoustically correct against media bytes. The mandated acceptance run must establish that separately. |

## Operator gate

The CA-M015 mandate requires this decision after verification:

> Approve CA-M015 and authorize CA-M016; confirm that verbatim evidence is accepted as a grounded input for Collision formation.

No CA-M016 work is included in this bundle, and no Collision-formation discovery or implementation is performed here.
