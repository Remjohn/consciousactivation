# CA-M012 — Q12 Sovereign Media Byte Supremacy

## Implementation handoff

Baseline repository commit captured from `docs/PRD/CURRENT.md`:

`9b039a2c156c0c2f5cfc12ead24cf406cbececd1`

The supplied archive contains no `.git` directory, so the SHA could not be independently verified with `git rev-parse` inside the execution workspace. The SHA above is the latest explicit repository-code verification SHA found in the supplied repository documentation.

### Summary table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/pipeline/src/cmf_pipeline/media/source.py` | Added content-addressed sovereign source identity, immutable source-media ref, repository-backed registration/ref verification, physical byte verification, lineage edges, and operator provenance projection. | Source identity is derived from exact bytes, not filename/URL; downstream consumers can prove the current file still equals the registered sovereign bytes; derivatives cannot become source by declaration. |
| `services/pipeline/src/cmf_pipeline/domain/errors.py` | Added dedicated fail-closed source integrity and source lineage validation errors. | Source-byte mismatch and broken immutable lineage are explicit validation failures rather than suppressed conditions. |
| `services/pipeline/src/cmf_pipeline/media/edl.py` | Requires a physical source path, verifies the registered source before EDL compilation, and embeds source identity/digest/integrity evidence in the EDL. | An EDL cannot be compiled from a substituted or changed source, and the EDL retains the exact sovereign source binding. |
| `services/pipeline/src/cmf_pipeline/media/program.py` | Requires a physical source path, verifies source bytes before program compilation, enforces SOURCE_SEGMENT registration consistency, and embeds source identity/digest/integrity evidence in the program/projection. | The canonical edit program is downstream of verified sovereign bytes; a mismatched source registration cannot be hidden inside a source segment. |
| `services/pipeline/src/cmf_pipeline/media/ffmpeg_adapter.py` | Requires repository-backed source verification before rendering; rejects missing/forged/stale lineage; records source identity/digest, authority, derivative kind, and processing revision on the rendered artifact. | A stale EDL or proxy file cannot produce a seemingly valid derivative; rendered output remains explicitly derivative and linked to the exact source bytes. |
| `services/pipeline/src/cmf_pipeline/media/evaluation.py` | Requires matching source registration, source identity, digest, and source authority across program and EDL; records source provenance on evaluation evidence. | Evaluation cannot collapse mismatched source lineages into one result. |
| `services/pipeline/src/cmf_pipeline/media/__init__.py` | Exposed the sovereign source authority constant and updated media service exports. | The source-authority vocabulary is shared by the scoped media services. |
| `services/pipeline/src/cmf_pipeline/phase6_demo.py` | Updated the Phase 6 reference execution to use exact registration refs, source-path verification, and repository-backed rendering. | The executable demo follows the same byte-verified lineage path as production-facing media services in scope. |
| `packages/ca_runtime/src/ca_runtime/video_edit_program.py` | Minimal supporting repair: persisted source path is forwarded to EDL/program compilation; renderer is initialized only after the repository-backed pipeline app exists. | The current coordinator cannot bypass CA-M012 verification while invoking the scoped pipeline media services. |
| `services/pipeline/contracts/schemas/source_media_identity.schema.json` | Added a strict contract for the content-addressed sovereign source identity. | A sovereign identity explicitly carries its byte digest and cannot declare itself a derivative. |
| `services/pipeline/contracts/schemas/source_media_registration.schema.json` | Added required source-media identity/digest/authority fields. | A source registration must identify the exact sovereign byte identity it registers. |
| `services/pipeline/contracts/schemas/word_boundary_edl.schema.json` | Added required source-media identity/digest/authority/integrity fields. | The EDL contract requires direct source provenance. |
| `services/pipeline/contracts/schemas/video_edit_program.schema.json` | Added required source-media identity/digest/authority/integrity fields. | The canonical program contract requires direct source provenance. |
| `services/pipeline/contracts/schemas/rendered_video_artifact.schema.json` | Added required source/derivative lineage fields, derivative classification, and processing revision. | A rendered artifact is structurally a derivative tied to an exact source identity/digest. |
| `services/pipeline/contracts/schemas/rendered_video_evaluation.schema.json` | Added required source/derivative lineage fields and source authority. | Evaluation evidence cannot omit the source evidence root. |
| `services/pipeline/contracts/schemas/CONTRACT_REGISTRY.json` | Registered `source_media_identity` as a Phase 6 contract and incremented the Phase 6 contract count. | The new source identity contract is part of the governed schema surface rather than an unregistered side channel. |
| `tests/phase6/test_ca_m012_source_media.py` | Added nine mandate-specific positive/negative tests covering identity stability, retrieval, schema validity, changed bytes, digest mismatch, missing lineage, proxy substitution, stale derivative binding, supersession history, and operator provenance. | The scoped CA-M012 fail-closed boundary is executable, including the required false-proof cases. |
| `tests/phase6/test_video_program_edl.py` | Updated direct tests to register a real source and pass the exact immutable registration ref/source path. | Existing EDL/program behavior now exercises the real source-integrity boundary. |
| `tests/phase6/test_ffmpeg_and_bindings.py` | Updated direct render/binding integration to use the repository-backed renderer and exact source ref/path. | Existing media integration remains green while retaining sovereign byte lineage. |

## Exact paste instructions

The bundle root mirrors the repository paths. From the repository root, replace/create each path below with the identically named file in this bundle:

- `services/pipeline/src/cmf_pipeline/media/source.py`
- `services/pipeline/src/cmf_pipeline/domain/errors.py`
- `services/pipeline/src/cmf_pipeline/media/edl.py`
- `services/pipeline/src/cmf_pipeline/media/program.py`
- `services/pipeline/src/cmf_pipeline/media/ffmpeg_adapter.py`
- `services/pipeline/src/cmf_pipeline/media/evaluation.py`
- `services/pipeline/src/cmf_pipeline/media/__init__.py`
- `services/pipeline/src/cmf_pipeline/phase6_demo.py`
- `packages/ca_runtime/src/ca_runtime/video_edit_program.py`
- `services/pipeline/contracts/schemas/source_media_identity.schema.json` (new file)
- `services/pipeline/contracts/schemas/source_media_registration.schema.json`
- `services/pipeline/contracts/schemas/word_boundary_edl.schema.json`
- `services/pipeline/contracts/schemas/video_edit_program.schema.json`
- `services/pipeline/contracts/schemas/rendered_video_artifact.schema.json`
- `services/pipeline/contracts/schemas/rendered_video_evaluation.schema.json`
- `services/pipeline/contracts/schemas/CONTRACT_REGISTRY.json`
- `tests/phase6/test_ca_m012_source_media.py` (new file)
- `tests/phase6/test_video_program_edl.py`
- `tests/phase6/test_ffmpeg_and_bindings.py`

Do not copy `AGENT_HANDOFF.md` into the repository; it is the bundle-level handoff document.

No database migration is required by this implementation. The existing governed `PipelineRepository.store_object(...)` command path is reused for source identity/registration persistence, and existing pipeline command-result persistence supplies the mutation receipt/idempotency record. Source identity is stored as a new pipeline object type, not a second media registry.

## Manual post-apply commands

Run the scoped verification from the repository root in the normal project environment:

```bash
PYTHONPATH="packages/ca_contracts/src:packages/ca_runtime/src:packages/ca_delegation_rc4/src:services/air/src:services/pipeline/src:services/interview/src" pytest -q tests/phase6 tests/cae/test_video_edit_program.py tests/phase4/test_m43_video_edit_cmf_runtime.py
```

Expected result for the supplied execution workspace: `29 passed`.

A normal installed environment should provide the project dependencies declared by the repository. In the supplied execution workspace, network access was unavailable and `psycopg` was not installed, so the verification run used an ephemeral test-only `psycopg` import stub; no stub files are included in this bundle and no repository dependency files were changed.

## Automated tests included in this bundle

New CA-M012 tests in `tests/phase6/test_ca_m012_source_media.py`:

- `test_stable_content_addressed_identity_and_retrieval`
- `test_source_identity_schema_and_registration_schema_are_executable`
- `test_changed_source_bytes_fail_closed_before_derivative_processing`
- `test_registration_digest_mismatch_is_rejected_even_when_reference_shape_is_valid`
- `test_derivative_without_source_lineage_is_rejected`
- `test_proxy_substitution_fails_against_registered_content_digest`
- `test_stale_derivative_binding_is_blocked_at_render_time`
- `test_historical_source_reference_survives_supersession`
- `test_operator_provenance_projection_distinguishes_source_from_derivative`

The updated existing direct tests are:

- `tests/phase6/test_video_program_edl.py::test_word_boundary_edl_and_program`
- `tests/phase6/test_video_program_edl.py::test_reorder_denied`
- `tests/phase6/test_ffmpeg_and_bindings.py::test_ffmpeg_source_led_render`
- `tests/phase6/test_phase6_demo_schemas.py::test_phase6_demo` (not modified, but included in the passing verification set)
- all tests in `tests/cae/test_video_edit_program.py`
- all tests in `tests/phase4/test_m43_video_edit_cmf_runtime.py`

## Verification evidence and limitations

Environment observed during execution:

- Python: `3.13.5`
- pytest: `9.0.2`
- jsonschema: `4.26.0`
- ffmpeg: `7.1.5`
- ffprobe: `7.1.5`
- Uploaded repository archive: no `.git` metadata
- PostgreSQL client package `psycopg`: unavailable in the isolated environment; an ephemeral import stub was used only so the SQLite-scoped pipeline tests could import the coordinator/runtime modules.

Observed verification:

```text
19 passed  tests/phase6
29 passed  tests/phase6 tests/cae/test_video_edit_program.py tests/phase4/test_m43_video_edit_cmf_runtime.py
```

The key content identity rule is:

```text
source-media:<source_media_sha256>
```

The source identity object stores the exact byte digest and byte count. Registration, EDL, VideoEditProgram, rendered video, and rendered-video evaluation carry an immutable `source_media_ref` plus the exact `source_media_sha256`. The FFmpeg renderer re-hashes the physical source path immediately before any derivative is produced and fails closed on mismatch.

The false-proof case is executable: a source file changed after ingestion can leave existing registration/EDL metadata internally consistent while the actual bytes differ; the renderer refuses to generate the derivative, so a polished downstream result cannot silently become valid evidence.

No temporal anchoring, continuity, verbatim/quote semantics, Collision formation, production authorization, or release semantics were added.

## Operator gate

**Decision required:** approve `CA-M012` and authorize `CA-M013`; confirm that the content-addressed source identity/digest is accepted as the sovereign evidence root. Until that decision is recorded in CAE control state, the dependent mandate remains unauthorized.
