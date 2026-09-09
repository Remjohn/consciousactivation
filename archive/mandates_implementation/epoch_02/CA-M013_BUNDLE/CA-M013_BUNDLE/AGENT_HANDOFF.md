# CA-M013 Agent Handoff

## Mandate identification

- Mandate: `CA-M013`
- Repository mandate document: `docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_02/05_CA_MANDATE_013.md`
- Canonical question: `Q13`
- Canonical mandate title in repository: `Temporal Evidence Anchoring`
- Scope completed: temporal evidence object creation, exact source-time mapping, fail-closed source resolution, lineage/provenance, read-only operator projection, and direct automated coverage.
- Adjacent scopes deliberately not implemented: Q14 continuity/chunking, Q15 verbatim governance, Q16 Collision formation, broad UI redesign, production authorization.

## Summary table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/pipeline/src/cmf_pipeline/application.py` | Instantiates and exposes `TemporalEvidenceMomentService` as `PipelineApplication.evidence_moments`. | Temporal anchoring is a runtime service at the Pipeline boundary rather than a presentation-only or test-only artifact. |
| `services/pipeline/src/cmf_pipeline/media/__init__.py` | Exports `TemporalEvidenceMomentService` from the canonical media surface. | The new temporal evidence service is reachable through the existing Pipeline media boundary without creating a parallel package. |
| `services/pipeline/src/cmf_pipeline/media/evidence.py` | Adds canonical `evidence_moment` creation, exact microsecond/native-timebase conversion, source digest/registration binding, stream identity, transcript-span retention, fail-closed validation, fresh-source resolution, lineage edges, and read-only projection. | `FR-TIME-001`: floating/unanchored evidence is inadmissible; exact source coordinates must resolve against sovereign source bytes and their declared stream/timebase. |
| `services/pipeline/contracts/schemas/evidence_moment.schema.json` | Adds executable JSON Schema for the persisted `evidence_moment` object. | Canonical temporal evidence shape, provenance, source authority, exact coordinate fields, and validation receipt fields are structurally governed. |
| `tests/phase6/test_ca_m013_temporal_evidence.py` | Adds schema, exact-boundary, multi-stream, missing-source, missing/negative/reversed-coordinate, invalid-timebase, precision-loss, out-of-bounds, source-mismatch, operator-projection, and false-proof tests. | Positive paths establish source-resolvable timing; negative paths enforce fail-closed behavior for the mandated failure modes and the floating-quote false-proof. |

## Exact paste instructions

Replace/add the following repository paths exactly:

1. Replace `services/pipeline/src/cmf_pipeline/application.py` with the bundled file at `services/pipeline/src/cmf_pipeline/application.py`.
2. Replace `services/pipeline/src/cmf_pipeline/media/__init__.py` with the bundled file at `services/pipeline/src/cmf_pipeline/media/__init__.py`.
3. Add `services/pipeline/src/cmf_pipeline/media/evidence.py` from the bundled file at `services/pipeline/src/cmf_pipeline/media/evidence.py`.
4. Add `services/pipeline/contracts/schemas/evidence_moment.schema.json` from the bundled file at `services/pipeline/contracts/schemas/evidence_moment.schema.json`.
5. Add `tests/phase6/test_ca_m013_temporal_evidence.py` from the bundled file at `tests/phase6/test_ca_m013_temporal_evidence.py`.

No other repository paths are included in this bundle.

## Manual post-apply commands

No database migration is required; evidence moments use the existing Pipeline object store and lineage-edge tables.

The requested test run was intentionally **not executed** in this agent session.

Run after paste/apply:

```text
pytest tests/phase6/test_ca_m013_temporal_evidence.py
```

The test fixture requires `ffmpeg`/`ffprobe`, consistent with the existing Phase 6 media fixture.

## Automated tests included

- `test_evidence_moment_schema_and_projection_are_executable`
- `test_exact_boundary_resolves_to_native_source_ticks`
- `test_multi_stream_anchors_are_explicit_and_resolve_independently`
- `test_missing_source_fails_closed`
- `test_missing_negative_and_reversed_coordinates_fail_closed` (parameterized)
- `test_invalid_timebase_fails_closed`
- `test_unrepresentable_microsecond_coordinate_fails_without_rounding`
- `test_out_of_bounds_anchor_fails_closed`
- `test_source_mismatch_is_rejected_after_canonical_object_is_forged`
- `test_false_proof_quote_without_anchor_is_unadmissible`

## Verification record

- Static Python parse/compile check: completed for every bundled `.py` file.
- JSON parse check: completed for the bundled schema.
- Test suite: **not run**, per execution instruction.
- Source repository `.git` metadata: not present in the supplied archive, so an exact post-implementation git commit SHA could not be captured without inventing one.
- CAE control-state update / operator decision: not performed in the supplied archive because the archive has no writable VCS/control-state integration available to capture a genuine post-commit SHA. The mandate's explicit operator gate remains required.

## Coordinate contract

- Canonical persisted coordinate unit: integer microseconds (`start_offset_us`, `end_offset_us`).
- Each coordinate must map exactly to an integer tick in the declared source stream rational timebase.
- Source stream identity is explicit via ordinal, ffprobe stream index, and codec type.
- Source registration and sovereign media digest are populated from the verified source registration; caller-supplied alternate source digests are not trusted.
- Resolution performs a fresh `ffprobe` read and re-checks source bytes, stream identity, native timebase, interval ordering, and source-duration bounds.
- No timestamp is silently rounded, shifted, or substituted.
- Transcript/character span is retained only as an attached lineage span; it does not replace temporal coordinates.

## Operator gate

`CA-M013` remains subject to the mandate's required operator decision: approve CA-M013 and authorize CA-M014, confirming the temporal-anchor contract as the evidence coordinate root.
