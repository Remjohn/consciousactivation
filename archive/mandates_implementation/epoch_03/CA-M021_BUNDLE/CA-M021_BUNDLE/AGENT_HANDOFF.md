# AGENT HANDOFF — CA-M021 — Anchor Hits as Exact Coordinate References

**Mandate ID:** `CA-M021`  
**Wave:** `03`  
**Requirement:** `FR-ANCH-001`  
**Status delivered:** IMPLEMENTATION COMPLETE — awaiting Operator approve/reject

---

## 1. Summary Table

| File | What Changed | Invariant Proven |
|------|-------------|-----------------|
| `services/interview/src/conscious_activations_interview_expression/anchor_coordinates.py` | **NEW FILE** — introduces `AnchorCoordinateService`, `require_exact_anchor_coordinates`, `reject_approximate_anchor`, and `validate_coordinates_within_source`. Defines the eight exact coordinate fields required by FR-ANCH-001: `byte_offset_start`, `byte_offset_end`, `frame_number_start`, `frame_number_end`, `microsecond_start`, `microsecond_end`, `media_asset_id`, `media_sha256`. | FR-ANCH-001: exact coordinate fields are required; approximate ms-only spans are fail-closed rejected. |
| `services/interview/src/conscious_activations_interview_expression/application.py` | **MODIFIED** — added `from .anchor_coordinates import AnchorCoordinateService` import and `self.anchor_coordinates = AnchorCoordinateService(self.repository)` on the application wiring. No other line changed. | Service is reachable from the canonical application boundary. |
| `tests/phase4/test_ca_m021_anchor_coordinates.py` | **NEW FILE** — 26 tests covering schema evidence, positive path, negative/fail-closed path, regression of adjacent services (CA-M015 verbatim, existing anchor-hit), integration via real domain boundary, and the mandate-required false-proof countercase. | All proof classes listed in mandate §9 are satisfied. |

---

## 2. Exact Paste Instructions

Apply each file at the **exact repo-relative path shown below**.  
No other files are modified.

### File 1 — New implementation

```
services/interview/src/conscious_activations_interview_expression/anchor_coordinates.py
```

Replace: _does not exist_ → create at that path.

### File 2 — Updated application wiring

```
services/interview/src/conscious_activations_interview_expression/application.py
```

Replace the existing `application.py` in full with the bundle copy.  
The only change is the addition of two lines:

```python
from .anchor_coordinates import AnchorCoordinateService
# … (in __init__) …
self.anchor_coordinates = AnchorCoordinateService(self.repository)
```

### File 3 — New test suite

```
tests/phase4/test_ca_m021_anchor_coordinates.py
```

Replace: _does not exist_ → create at that path.

---

## 3. Manual Post-Apply Commands

No database migration is required.  `AnchorCoordinateService` uses the
existing `ie_objects` / `ie_edges` tables from
`0001_interview_expression.sql`; `object_type = "anchor_coordinate"` is a
new discriminator value that the generic store already handles.

After applying the files, verify the Python package imports are clean:

```bash
cd <repo-root>
python -c "from conscious_activations_interview_expression.anchor_coordinates import AnchorCoordinateService; print('OK')"
```

---

## 4. New Automated Tests Included in the Bundle

File: `tests/phase4/test_ca_m021_anchor_coordinates.py`

### SCHEMA

| Test | Proof class |
|------|-------------|
| `test_anchor_coordinate_schema_fields_are_present` | SCHEMA — all eight exact fields present in stored payload |
| `test_anchor_coordinate_mandate_id_stamped` | SCHEMA — CA-M021 mandate_id stamped on payload and receipt |

### EXECUTABLE — positive path

| Test | Proof class |
|------|-------------|
| `test_exact_coordinates_with_known_duration_are_accepted` | EXECUTABLE positive — valid coords accepted, duration_bound_checked=True |
| `test_exact_coordinates_audio_only_stream_no_frame_numbers_accepted_when_same_frame` | EXECUTABLE positive — frame_start == frame_end allowed |
| `test_multiple_evidence_refs_are_accepted_and_sorted` | EXECUTABLE positive — evidence refs sorted deterministically |
| `test_limitations_are_forwarded_when_caller_supplies_them` | EXECUTABLE positive — limitations array preserved |
| `test_duration_in_microseconds_is_preferred_over_milliseconds` | EXECUTABLE positive — duration_us wins over duration_ms |
| `test_idempotent_admission_returns_same_object` | EXECUTABLE positive — same idempotency_key returns same object |

### EXECUTABLE — negative / fail-closed path

| Test | Proof class |
|------|-------------|
| `test_approximate_millisecond_span_is_rejected` | EXECUTABLE negative — ms-only span → FR_ANCH_001_APPROXIMATE_ANCHOR_REJECTED |
| `test_free_text_interpretive_string_is_rejected` | EXECUTABLE negative — string → FR_ANCH_001_INTERPRETIVE_ANCHOR_REJECTED |
| `test_missing_byte_offset_field_is_rejected` | EXECUTABLE negative — structural field missing |
| `test_missing_frame_number_field_is_rejected` | EXECUTABLE negative — structural field missing |
| `test_missing_microsecond_field_is_rejected` | EXECUTABLE negative — structural field missing |
| `test_inverted_byte_span_is_rejected` | EXECUTABLE negative — FR_ANCH_001_INVERTED_BYTE_SPAN |
| `test_inverted_microsecond_span_is_rejected` | EXECUTABLE negative — FR_ANCH_001_INVERTED_MICROSECOND_SPAN |
| `test_frame_number_end_less_than_start_is_rejected` | EXECUTABLE negative — FR_ANCH_001_INVERTED_FRAME_SPAN |
| `test_microsecond_end_exceeds_source_duration_is_rejected` | EXECUTABLE negative — FR_ANCH_001_EXCEEDS_SOURCE_DURATION |
| `test_coordinate_referencing_wrong_media_asset_id_is_rejected` | EXECUTABLE negative — FR_ANCH_001_MEDIA_NOT_IN_PACKAGE |
| `test_coordinate_referencing_wrong_media_sha256_is_rejected` | EXECUTABLE negative — FR_ANCH_001_MEDIA_NOT_IN_PACKAGE |
| `test_extra_field_in_coordinates_is_rejected` | EXECUTABLE negative — field schema enforcement |
| `test_non_sha256_media_digest_is_rejected` | EXECUTABLE negative — SHA-256 format enforcement |
| `test_zero_length_byte_span_is_rejected` | EXECUTABLE negative — inverted byte span when end==start |
| `test_zero_length_microsecond_span_is_rejected` | EXECUTABLE negative — inverted µs span when end==start |
| `test_stale_source_package_ref_is_rejected` | EXECUTABLE negative — FR_ANCH_001_PROVENANCE_ERROR |
| `test_anchor_kind_empty_string_is_rejected` | EXECUTABLE negative — empty anchor_kind rejected |

### FALSE-PROOF countercase (mandate §9 required)

| Test | Proof class |
|------|-------------|
| `test_millisecond_start_end_pair_labelled_anchor_is_explicitly_rejected` | FALSE-PROOF — the countercase the mandate names: a start/end ms pair labelled "anchor" must not be admitted |

### REGRESSION — adjacent behaviour

| Test | Proof class |
|------|-------------|
| `test_existing_anchor_hit_via_expression_service_still_works` | REGRESSION — `ExpressionGovernanceService.create_anchor_hit` unbroken |
| `test_verbatim_evidence_service_still_works` | REGRESSION — `VerbatimEvidenceService.admit` unbroken |

### INTEGRATION — real domain boundary

| Test | Proof class |
|------|-------------|
| `test_list_for_source_returns_all_committed_coordinates` | INTEGRATION — list_for_source returns all admitted records |
| `test_get_by_ref_returns_exact_payload` | INTEGRATION — get() returns stored payload by ref |
| `test_validation_block_records_exact_coordinate_flags` | INTEGRATION — validation block carries all CA-M021 flags |
| `test_receipt_contains_exact_object_ref` | INTEGRATION — receipt object_ref matches stored sha256 |

---

## 5. Residual Limitations

1. **Byte offsets are not derived from ffprobe index in tests** — the test
   fixture declares byte offsets arithmetically from µs.  In production, byte
   offsets must be derived from the sovereign container's packet index (e.g.
   via `ffprobe -show_packets`).  The domain contract enforces that these
   fields must be *present and non-zero*, but the mandate deliberately does not
   implement media indexing infrastructure (mandate §5, out of scope).

2. **duration_us not populated by MediaInspector** — `media.py`'s
   `_ffprobe()` output does not yet include `duration_us`; it stores only
   `duration_ms`.  The `AnchorCoordinateService` falls back to `duration_ms`
   when `duration_us` is absent and records `SOURCE_DURATION_UNKNOWN_CANNOT_ENFORCE_BOUND`
   only when neither is present.  Adding `duration_us` to the ffprobe output
   is recommended but is outside this mandate's file boundary.

3. **Yield gating and authorization policy not implemented** — per mandate §5,
   this is explicitly out of scope and belongs to Q23–Q24.

---

## 6. Operator Decision Request

**Approve or reject CA-M021?**

Evidence that Anchor Hits specify exact stream byte offsets, frame numbers,
and microsecond timestamps — and that approximate or interpretive forms are
rejected fail-closed — is located at:

- Implementation: `services/interview/src/conscious_activations_interview_expression/anchor_coordinates.py`
- Application wiring: `services/interview/src/conscious_activations_interview_expression/application.py`
- Tests (26): `tests/phase4/test_ca_m021_anchor_coordinates.py`

The false-proof countercase (`test_millisecond_start_end_pair_labelled_anchor_is_explicitly_rejected`)
confirms that the approximate form is rejected, not silently accepted.
