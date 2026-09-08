# CA-M020 Agent Handoff

## Mandate

- **Mandate ID:** CA-M020
- **Invariant:** FR-020
- **Title:** Reaction Receipts as First-Class Evidence
- **Source snapshot:** `codebase_clean(1).zip` supplied for this execution
- **Test execution status:** Tests were **not run**, per execution instruction.
- **Static validation:** Python AST parsing / bytecode compilation only; no test suite was executed.
- **Commit SHA:** Not available in this bundle-only execution. Apply the files and commit in the repository to obtain the authoritative post-apply SHA.

## Summary table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/interview/src/conscious_activations_interview_expression/reaction_receipts.py` | Added a first-class `ReactionReceiptEvidenceService` that mints `reaction_receipt` evidence tokens only when an exact CA-M021 media coordinate is bound to an exact source-package revision. Hash proofs cover source package, sovereign media digest, coordinates, actor identity, actor timestamp, reaction payload, and supporting observation refs. Added independent verification plus compatibility aliases. | A receipt cannot be admitted without verifiable sovereign media coordinates; changing the actor timestamp, coordinates, reaction content, source-package ref, or media digest invalidates the content address/proof. Re-verification re-resolves the exact source revision and media asset, preventing source dissociation. |
| `tests/phase4/test_ca_m020_reaction_receipts.py` | Added CA-M020 executable acceptance coverage at the actual `InterviewRepository` / `InterviewExpressionApplication` persistence boundary, including positive, negative, tamper, dissociation, idempotency, and regression cases. | Demonstrates first-class persistence, cryptographic verification, fail-closed rejection of unlinked/dissociated/out-of-bounds reactions, and refusal to trust a `linked` boolean in place of coordinates. |

## Exact paste instructions

This bundle contains only the two authorized paths below.

1. Add `CA-M020_BUNDLE/services/interview/src/conscious_activations_interview_expression/reaction_receipts.py` as:
   `services/interview/src/conscious_activations_interview_expression/reaction_receipts.py`

2. Add `CA-M020_BUNDLE/tests/phase4/test_ca_m020_reaction_receipts.py` as:
   `tests/phase4/test_ca_m020_reaction_receipts.py`

No existing repository file is replaced by this bundle.

## Manual post-apply commands

No database migration is required.

After applying the files, run the targeted acceptance suite manually:

```bash
pytest -q tests/phase4/test_ca_m020_reaction_receipts.py
```

For the service package's broader reaction regression coverage, run manually as a separate repository check:

```bash
pytest -q tests/phase4/test_ts_int_006_reaction.py
```

These commands were **not executed** during this bundle build.

## Automated tests included

- `test_receipt_schema_contains_first_class_identity_timestamp_and_media_proof`
- `test_valid_reaction_is_admitted_and_verifies_against_exact_source_revision`
- `test_receipt_ref_is_content_addressed_and_survives_idempotent_replay`
- `test_unlinked_reaction_annotation_cannot_be_upgraded_by_a_boolean_flag`
- `test_mismatched_media_digest_is_rejected_before_persistence`
- `test_out_of_bounds_coordinates_are_rejected_fail_closed`
- `test_tampered_actor_timestamp_cannot_verify_as_the_original_receipt`
- `test_tampered_coordinates_cannot_verify_as_the_original_receipt`
- `test_source_media_dissociation_is_rejected_even_when_a_link_flag_is_present`
- `test_observation_refs_are_first_class_supporting_edges_not_substitutes_for_media_binding`
- `test_legacy_boolean_metadata_cannot_replace_required_coordinate_proof`

## Residual limitations

The implementation uses SHA-256 canonical content-addressing and proof verification. This provides tamper-evident integrity and prevents dissociation from the exact persisted source/media references, but it is **not a public-key signature** and therefore does not independently prove actor authenticity. The current repository has no existing signing-key / signature contract, and this mandate does not authorize inventing one.

The module is intentionally additive because the mandate's authorized file boundary names `reaction_receipts.py` and its CA-M020 acceptance suite. Existing legacy `ReactionEvidenceService` behavior in `reaction.py` is not modified by this bundle; consumers should use `ReactionReceiptEvidenceService` as the CA-M020 receipt admission boundary.
