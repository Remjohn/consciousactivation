# CA-M014 Agent Handoff

## Summary

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/pipeline/src/cmf_pipeline/media/chunking.py` | Added deterministic source-coordinate media window construction, explicit predecessor/successor and overlap metadata, whole-frame boundary retention, fail-closed overlap reconciliation, timestamp validation, source-frame continuity checks, and immutable stitched output. | FR-014: adjacent windows preserve continuous acoustic/video frame context; overlap is reconciled by source identity plus exact timing/payload digest; gaps, conflicts, reordered windows, missing continuity links, and unsupported reconstructed content are rejected. |
| `tests/phase6/test_ca_m014_cross_window_chunking.py` | Added adversarial and positive unit coverage for boundary preservation, deterministic stitching, conflicting overlap, dropped boundary frames, reordered windows, missing continuity relations, unsupported reconstruction, audio/video identity, and timestamp preservation. | Executable evidence covers the mandate's required positive path and fail-closed cases without modifying source bytes or inventing missing content. |

## Exact paste instructions

Replace/create these repository paths exactly:

1. `CA-M014_BUNDLE/services/pipeline/src/cmf_pipeline/media/chunking.py`
   -> `services/pipeline/src/cmf_pipeline/media/chunking.py`

2. `CA-M014_BUNDLE/tests/phase6/test_ca_m014_cross_window_chunking.py`
   -> `tests/phase6/test_ca_m014_cross_window_chunking.py`

No other repository files are included or authorized for modification by this bundle.

## Manual post-apply commands

Per operator instruction, **tests were not run**.

After applying the two files, run the repository's normal CA-M014 verification command when the operator permits execution, for example:

`pytest tests/phase6/test_ca_m014_cross_window_chunking.py`

Environment limitation: the supplied source archive is not a Git checkout and contains no `.git` directory, so an exact post-change Git commit SHA cannot be captured from this execution environment. The implementing agent/operator must capture the SHA after the files are applied and committed.

## Automated tests included

- `test_sliding_windows_preserve_boundary_frame_whole_and_explicit_overlap`
- `test_stitch_is_deterministic_and_deduplicates_overlap_by_source_identity`
- `test_duplicate_overlap_with_changed_timestamp_or_payload_fails_closed`
- `test_missing_boundary_frame_fails_closed_instead_of_smoothing`
- `test_reordered_windows_fail_even_if_the_frame_sets_are_identical`
- `test_missing_continuity_relation_fails_closed`
- `test_dropped_source_frame_is_rejected_after_overlap_reconciliation`
- `test_unsupported_fabricated_reconstruction_cannot_enter_the_media_contract`
- `test_audio_and_video_keep_independent_source_identity_and_timestamp_order`
- `test_single_window_requires_no_overlap_and_preserves_exact_source_frames`
- `test_boundary_frame_is_never_split_or_retimed_by_windowing`

## Verification record

- Command executed: archive inspection only; no test command executed.
- Environment identity: uploaded `codebase_clean.zip`, extracted for inspection; no Git metadata present.
- Fixture identity: deterministic in-test synthetic `MediaFrame` sequence with stable source indices, integer microsecond PTS/durations, and fixed payload digests.
- Observed result: implementation and test artifacts were generated; tests intentionally not executed per instruction.
- Exact property proved by code inspection: source-coordinate identity, explicit window order/overlap, whole-frame boundary retention, deterministic overlap deduplication, timestamp equality for duplicate frames, and fail-closed continuity validation.
- Limitation: unexecuted tests do not constitute runtime proof; the archive does not expose a Git commit SHA; payload digest validation proves identity consistency, not the truth of an external media file unless the ingestion path supplies and verifies the digest.
- Operator gate: CA-M014 operator approval and authorization of CA-M015 remain required by the mandate. This bundle does not assert that gate has been granted.
