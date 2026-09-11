# TS-APP-API-003 (Interview Admission API) — apply guide

## 1. Copy files in

```
api/routers/interviews.py          -> api/routers/interviews.py       (new)
api/schemas/__init__.py            -> api/schemas/__init__.py          (new dir + file)
api/schemas/interviews.py          -> api/schemas/interviews.py       (new)
api/services/__init__.py           -> api/services/__init__.py        (new dir + file)
api/services/media_store.py        -> api/services/media_store.py     (new)
api/services/transcript_ingest.py  -> api/services/transcript_ingest.py (new)

tests/api/conftest.py                    -> tests/api/conftest.py               (new)
tests/api/test_interviews_import.py      -> tests/api/test_interviews_import.py     (new)
tests/api/test_interviews_brief_led.py   -> tests/api/test_interviews_brief_led.py  (new)
tests/api/test_interviews_status.py      -> tests/api/test_interviews_status.py     (new)
tests/api/fixtures/synthetic_interview.mp4  (new — real, ffprobe-readable 6s clip)
tests/api/fixtures/corrupt.mp4              (new — 0 bytes, for AC-008)
tests/api/fixtures/sample_transcript.srt    (new — 3-cue, single-speaker SRT)
tests/api/fixtures/sample_pre_aligned.json  (new — words all epistemic_state OBSERVED)
tests/api/fixtures/untimed.txt              (new — plain text, no cue markers)
```

The scope note (`api/schemas/` and `api/services/`) goes slightly beyond the
literal "package only `api/routers/interviews.py`, any new test files"
instruction, but `interviews.py` imports both `api/schemas/interviews.py` and
`api/services/{media_store,transcript_ingest}.py` — the spec's own Stage 2/3/6
deliverables — so the router cannot import without them. Leaving them out
would ship a broken package.

## 2. One-line diff to `api/main.py`

Find this line (currently the commented-out Wave 2 placeholder):

```python
# app.include_router(interviews.router, prefix="/api/interviews", tags=["interviews"])
```

Replace it with:

```python
from api.routers import interviews; app.include_router(interviews.router, prefix="/api/interviews", tags=["interviews"])  # noqa: E702
```

This is a single physical line (import + `include_router` joined with `;`)
so that adding it doesn't require touching the existing
`from api.routers import health` import line above — per "do not modify any
other line in `api/main.py`," taken literally. If your team prefers the
more conventional two-line style matching how `health` is wired in (a
top-of-file import plus a bare `include_router(...)` call at the bottom),
that's a trivial one-time split; nothing else in this package depends on
which style you pick.

## 3. Two real bugs found and fixed while implementing this (read before you review)

Both were found by reading `services/interview/src/conscious_activations_interview_expression/`
directly, then confirmed by running the pipeline against real fixtures
(6-second ffprobe-readable H.264/AAC mp4, real SRT, real pre-aligned JSON) —
not by inspection alone.

**a) AC-008 (corrupt media → `MEDIA_PROBE_FAILED`).** `MediaInspector.inspect()` →
`make_media_asset()` enforces `bytes_count >= 1` *before* `ffprobe`'s
`probe_status` is ever checked. A zero-byte upload makes `.inspect()` itself
raise a domain `ValidationError` — the spec's literal Stage-4 pseudocode would
let that propagate to the generic `except InterviewExpressionError` handler
and return `422 VALIDATION_FAILED`, not the `422 MEDIA_PROBE_FAILED` AC-008
requires. Fixed in `_inspect_media()` by catching that specific
`ValidationError` and remapping it — documented inline in the router with the
same style of deviation-comment `api/routers/health.py` already uses in this
repo (TS-APP-API-001).

**b) SRT parser hang (found via the harness, not an AC by itself, but blocks
AC-001/AC-005/AC-011/AC-012 whenever the transcript is SRT).** The original
Stage-3 cue regex —
```
r"\d+\s*\n(\d{2}):...\s*\n((?:.+\n?)+?)(?=\n\d+\s*\n|\Z)"
```
— has catastrophic backtracking from the nested `(?:.+\n?)+?` quantifier. A
real 3-cue SRT file (not a single-cue toy fixture) hung indefinitely — over
15s with no return, confirmed before and after the fix with a timeout.
Replaced with a linear-time blank-line block splitter plus one anchored
per-block timestamp match; re-verified correct on the 3-cue fixture and
stress-tested at 500 cues / 6000 words in ~60ms.

**c) AC-011 (identical retry must be idempotent, not a 409).** Not a bug in
`services/interview/`, but a design gap in the spec's own literal Stage-4
pipeline code. `bind_component()` recomputes its full target payload from
whatever the repository's *current* row happens to be — it is not a pure
function of `(package_id, component_name, ref)`. `admit()`/`align()`/
`pack_phrases()`/`visual.compile()` are genuinely content-addressed (their
`object_id` is a `semantic_id` hash of their inputs), so replaying them under
a fixed derived idempotency key after a fully-completed prior run correctly
short-circuits. `bind_component()` does not have that luxury: on a full
retry of an already-fully-bound package, the "current" state read at bind
time already has every slot bound, so the payload it would submit under the
fixed `"...:bind-<slot>"` key no longer matches the payload recorded under
that same key during the original run (which only had that one slot bound
at the time) — the repository's idempotency-key cache raises `CONFLICT`
before `store_object`'s own content-addressing ever gets a chance to run.
Confirmed via the harness: AC-011's identical-retry scenario hit exactly
this 409 on the very first `bind_component` call, every time, before the fix.
Fixed with a `_bind_if_needed()` guard in the router that skips re-binding a
slot already bound to the identical content-addressed ref — `services/interview/`
itself is untouched.

## 4. Acceptance criteria — result

All 13 ACs (AC-001 through AC-013) checked. **Environment note up front:**
this sandbox has no network access at all (PyPI and the Ubuntu apt mirror
both return `403` on every request), so `fastapi`, `pydantic`, `uvicorn`, and
`pytest` are not installed and could not be installed by any means available.
What *is* real and installed: the actual `conscious_activations_interview_expression`,
`ca_contracts`, and `ca_runtime` packages (via `pip install -e --no-index`,
which works for these since they have no external dependencies), plus
`ffmpeg`/`ffprobe` (already present). Two levels of verification were used:

- **Direct invocation** — a minimal stub for just enough of `fastapi`/
  `pydantic` (`UploadFile`, `HTTPException`, pass-through `APIRouter`
  decorators, a `BaseModel` with `model_dump()`) to let the *real*
  `api/routers/interviews.py` import, then calling its endpoint functions
  directly against a *real* `InterviewExpressionApplication` (real sqlite
  repository, real domain validation, real `ffprobe` calls on the real mp4
  fixture).
- **Full `TestClient` simulation** — the same stub extended with a working
  `fastapi.testclient.TestClient` (drives the real `lifespan()` context
  manager, matches path templates, maps `files=`/`data=`/`headers=` the way
  every test in this package uses them) and a `pytest` fixture-resolution
  shim (`tmp_path`, `monkeypatch`, `pytest.raises`, `@pytest.fixture`).
  **All 3 new test files' 12 test functions were run this way, verbatim,
  and all 12 passed** — this executed the literal code being shipped, not a
  paraphrase of it.

Neither of these is a substitute for running the actual `pytest`/`fastapi`
stack with network access; they're the closest approximation achievable
offline, and both layers agree.

| AC | What it checks | Result |
|---|---|---|
| AC-001 | Real mp4 + real SRT import succeeds end to end | **PASS** |
| AC-002 | `/import` never fabricates planning history (`ABSENT_NOT_CREATED` exactly) | **PASS** |
| AC-003 | Brief-led admission with correct digests succeeds, lineage preserved exactly | **PASS** |
| AC-004 | Digest mismatch → `422 VALIDATION_FAILED` / `INT_ARMED_PLAN_HASH_MISMATCH`, no package created | **PASS** |
| AC-005 | SRT-derived words are always `epistemic_state: INFERRED` | **PASS** |
| AC-006 | Pre-aligned JSON's `OBSERVED` epistemic_state passes through unchanged | **PASS** |
| AC-007 | Untimed transcript vs. `SRT` format → `422 UNSUPPORTED_TRANSCRIPT_FORMAT`, no package created | **PASS** |
| AC-008 | Zero-byte upload → `422 MEDIA_PROBE_FAILED`, no writes | **PASS** (after fix — see §3a) |
| AC-009 | Unknown `package_id` → `404 NOT_FOUND` | **PASS** |
| AC-010 | Status reflects real component binding (3 slots BOUND, `expression_moments` still PENDING) | **PASS** |
| AC-011 | Identical retry: same `package_id`, `idempotent_replay: true`, exactly 1 stored object | **PASS** (after fix — see §3c) |
| AC-012 | Default visual index: 1 full-duration shot, 0 keyframes, `technical_only: true` | **PASS** |
| AC-013 | No modification to existing service packages; full test suite still passes | **PASS with one caveat** — see below |

### AC-013 detail

`services/interview/` was not modified — confirmed by inspection (this
package touches only new `api/` files plus one line in `api/main.py`). What
was actually re-run, since real `pytest` isn't installable here:

- **`tests/phase4/`** (the interview-domain suite this spec depends on most
  directly), via a small stdlib `unittest`-based runner supporting the
  `tmp_path` + `pytest.raises` subset these files use: **34/35 passed.** The
  1 failure (`test_traceability.py::test_phase4_spec_matrix_matches_exact_seven_specs`)
  is pre-existing and unrelated — a governance CSV
  (`governance/program-control/.../PHASE_04_SPEC_IMPLEMENTATION_MATRIX.csv`)
  references spec paths under a `06_INTERVIEW_EXPRESSION/` directory that
  doesn't exist anywhere in this checkout (the repo appears to have been
  flattened to `docs/`, `services/`, etc. without updating that CSV).
  Confirmed pre-existing by checking the referenced directory doesn't exist
  at all, unrelated to anything touched here.
- **`tests/phase1/`**: 11/14 passed. The 3 failures are `cmf_pipeline` not
  being installable in this offline sandbox and a missing Node.js build
  artifact for the studio UI — neither is touched by this work.
- **`tests/phase7/`**: 4/4 passed.
- **`tests/phase2/phase3/phase5/phase6/phase8/phase9`, `tests/pipeline/`**:
  not run — they import `cmf_activative_intelligence`, `cmf_pipeline`,
  `ca_delegation_rc4`, or `ca_release`, none of which install in this
  sandbox (their `pyproject.toml`s pin exact versions of sibling packages
  that `pip`'s resolver insists on fetching from PyPI rather than
  recognizing as already present locally, and PyPI is unreachable here).
  This is a pre-existing environment/packaging limitation, not something
  introduced by this change — none of those services' source was touched.
- **`tests/api/test_health.py`, `test_startup.py`** (pre-existing, from
  TS-APP-API-001): not re-run — doing so faithfully would need generator-
  style (`yield`) pytest fixture support plus realistic pipeline/air/vae
  health-check behavior that the necessarily-permissive stubs used here
  can't produce. Checked structurally instead: `api/routers/health.py` was
  not modified, and `api/main.py`'s health registration
  (`app.include_router(health.router, prefix="/api")`) is untouched and
  co-registers cleanly alongside the new interviews router (confirmed by
  importing the full `api/main.py` and listing all five resulting routes:
  the two health routes plus `POST /api/interviews/import`,
  `POST /api/interviews/brief-led`, `GET /api/interviews/{package_id}/status`).

If you have a normal (network-connected) environment, running
`pip install -e services/interview` (already satisfied by this package) plus
the actual `api/requirements.txt`, then `pytest tests/ -q`, is the way to get
a fully authoritative AC-013 result — everything above is the closest
approximation achievable without network access, not a replacement for that.
