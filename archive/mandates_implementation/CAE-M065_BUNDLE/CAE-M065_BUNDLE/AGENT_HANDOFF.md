# CAE-M065 — Native OpenChatCut Runtime and Timeline Handoff

## Mandate ID & Title

**Mandate ID:** CAE-M065 (the repository mandate document uses the canonical file prefix `M0065` / title `CAE-M0065`)

**Mandate Title:** Native OpenChatCut Runtime and Timeline Handoff

**Requirement / Invariant:** `INV-VIDEO-RUNTIME-001`

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/pipeline/src/cmf_pipeline/media/openchatcut.py` | Added the CAE-side OpenChatCut Streamable HTTP MCP adapter. It initializes and identifies the runtime, targets/creates a project, imports CAE media, opens an edit session, creates native multi-track lanes, maps CAE output/source ranges to OpenChatCut frames, submits validated native edit commands, reviews/applies the draft, verifies native timeline readback, and stores a CAE runtime handoff receipt. | CAE remains authoritative through an immutable `program_ref`; source bytes are checked against the CAE sovereign digest before import; native track/item identity, output timing, source in-point/duration, and semantic role mappings are verified or the handoff fails closed. |
| `services/pipeline/src/cmf_pipeline/media/__init__.py` | Exported the OpenChatCut runtime adapter/config/error surface from the pipeline media package. | Makes the runtime bridge part of the existing video-edit integration surface without changing the canonical program format. |
| `services/pipeline/src/cmf_pipeline/application.py` | Exposed `PipelineApplication.openchatcut` using environment-driven OpenChatCut MCP configuration. | Existing compiled CAE Video Edit Programs can be handed to the real runtime without moving authority into the editor. |
| `tests/phase6/test_m065_openchatcut_runtime.py` | Added self-contained tests for frame-exact mapping, MCP/SSE parsing, native multi-track handoff flow, semantic-role/media bindings, source-cut verification, runtime-unavailable receipt blocking, and source-byte digest fail-closed behavior. | 6/6 M0065-focused automated tests pass. The tests do not claim to substitute for live OpenChatCut acceptance proof. |

## Files Added and Files Modified

### Files Added

- `services/pipeline/src/cmf_pipeline/media/openchatcut.py` — New CAE-to-OpenChatCut runtime adapter and governed handoff receipt implementation.
- `tests/phase6/test_m065_openchatcut_runtime.py` — New M0065 integration/unit test coverage.

### Files Modified

- `services/pipeline/src/cmf_pipeline/media/__init__.py` — Export the new adapter surface.
- `services/pipeline/src/cmf_pipeline/application.py` — Add `PipelineApplication.openchatcut` runtime adapter wiring.

No database migration is required. The handoff receipt is stored using the existing `pipeline_objects` persistence model and linked to the canonical `video_edit_program` through an existing edge mechanism.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

1. Apply the four repository files from this bundle at these exact repository destinations:

```text
services/pipeline/src/cmf_pipeline/media/openchatcut.py
services/pipeline/src/cmf_pipeline/media/__init__.py
services/pipeline/src/cmf_pipeline/application.py
tests/phase6/test_m065_openchatcut_runtime.py
```

2. No migration file should be applied for M0065.

3. In an environment with the repository's normal Python dependencies installed, run the M0065-focused test:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q tests/phase6/test_m065_openchatcut_runtime.py
```

4. For live native-runtime acceptance, run OpenChatCut from source on Node.js 24.x, then expose its Streamable HTTP MCP endpoint. The current OpenChatCut endpoint is:

```text
http://localhost:5199/api/external-mcp/mcp
```

Set:

```bash
export OPENCHATCUT_MCP_URL=http://localhost:5199/api/external-mcp/mcp
export OPENCHATCUT_APPROVAL_MODE=auto
# export OPENCHATCUT_MCP_TOKEN=...   # only when the runtime is configured to require bearer authentication
```

Start OpenChatCut in its checkout using its normal runtime setup:

```bash
npm install
npm run dev
```

5. Invoke the already-compiled CAE Video Edit Program through the application surface. The program ID must be an existing canonical `video_edit_program` object, and every selected CAE media reference used by the program must have a local path supplied in `media_paths`:

```bash
export VIDEO_PROGRAM_ID='video-edit-program:...'
export CAE_SOURCE_REF='source-registration:...'
export CAE_SOURCE_PATH='/absolute/path/to/sovereign/source.mp4'

PYTHONPATH=services/pipeline/src:packages/ca_runtime/src python - <<'PY'
import os
from cmf_pipeline.application import PipelineApplication

app = PipelineApplication()
receipt = app.openchatcut.handoff(
    os.environ['VIDEO_PROGRAM_ID'],
    media_paths={
        os.environ['CAE_SOURCE_REF']: os.environ['CAE_SOURCE_PATH'],
    },
    idempotency_key=f"cae-m0065:{os.environ['VIDEO_PROGRAM_ID']}",
)
print(receipt['payload'])
PY
```

For a program containing `APPROVED_ASSET`/`AUDIO` elements, add each referenced `artifact_ref.object_id` to the same `media_paths` mapping before invoking `handoff`.

6. Live acceptance is evidenced only when the resulting CAE receipt reports all of the following:

```text
state = EXECUTED
verification.timeline_fidelity = NATIVE_TIMELINE_VERIFIED
runtime_identity.server_name = openchatcut
review_status = applied
```

The receipt's `track_map`, `asset_map`, `imported_media_sha256`, and `verification.verified_elements` are the authoritative CAE-side handoff evidence. The OpenChatCut timeline is not promoted to system-of-record status.

## Test Command (exact pytest/test command to verify)

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q tests/phase6/test_m065_openchatcut_runtime.py
```

## Expected Test Results (number of automated tests, all passing)

**6 automated tests — all passing (6 passed, 0 failed).**

The sandbox used for this execution did not contain a running OpenChatCut process at `localhost:5199`, and outbound package/network access was unavailable. Therefore the live native-runtime execution criterion is **not proven in this sandbox** and must remain `BLOCKED` until the real OpenChatCut runtime is started and the live handoff receipt reaches `EXECUTED` with `NATIVE_TIMELINE_VERIFIED`.

The sandbox also could not collect two pre-existing broader video suites because their repository environment is missing unrelated dependencies (`psycopg` and `ca_delegation_rc4`). Those dependencies and tests are outside the M0065 file boundary and were not modified.

**Current M0065 control state in this sandbox:** `BLOCKED` for environment fidelity, not for the adapter's mandate-focused automated test suite.

**Rollback:** remove the four files above. No database rollback is needed; only invalidate/delete any generated OpenChatCut project/session created by a live handoff, while preserving the CAE program and any failed receipt/evidence.

**Operator gate:**

> Do you accept M0065 and authorize M0066?
>
> ACCEPT | ACCEPT WITH LIMITATIONS | REPAIR | BLOCK
