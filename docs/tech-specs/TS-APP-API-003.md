---
spec_id: TS-APP-API-003
title: Interview Admission API
document_class: TECH_SPEC
product: Conscious Activations
module: api
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CURRENT
build_authority: false
controlling_frs:
  - FR-APP-020 (admit a Brief-led interview — Entry Point A)
  - FR-APP-021 (admit an imported interview — Entry Point B)
  - FR-APP-022 (transcript alignment and phrase packing)
  - FR-APP-023 (shot map and keyframe indexing)
controlling_stories:
  - ST-APP-02.01 (Brief-led interview reaches Canonical Interview Source Package)
  - ST-APP-03.01 (upload an existing interview)
upstream_dependencies:
  - CA_PROJECT_SNAPSHOT_V2.md (authority — CURRENT)
  - CA_APP_FR_EPIC_SPEC_PLAN.md (authority — CURRENT)
  - TS-APP-API-001.md (quality_state: WRITTEN_PENDING_AUDIT — DRAFT_DEPENDENCY_NOT_ACCEPTED; this spec depends only on its `api/dependencies.py::get_interview` factory, `api/config.py::AppConfig`/`load_config`, and `api/errors.py::ErrorResponse` interfaces, not on any claim that the gateway is production-ready)
downstream_consumers:
  - TS-APP-API-004 (Campaign CRUD API — consumes `package_id` as `source_package_id` on Campaign Order creation)
  - TS-APP-UI-002 (Campaign List and Creation UI — CampaignNew.tsx import tab calls these endpoints)
  - TS-APP-COMPOSER-001 (Interview Composer Service Integration — will populate the `/brief-led` planning-lineage fields programmatically once built; until then, callers supply them directly)
output_path: api/routers/interviews.py (and supporting files listed in section 7)
wave: 1
---

# TS-APP-API-003 — Interview Admission API

## 1. Files and Authorities Read

| File | SHA-256 (short) | Status | Fact extracted |
|---|---|---|---|
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/source_package.py` | `8e83d673` | READ — CURRENT IMPLEMENTATION | `SourcePackageService.admit()` requires the exact key set `{workspace_id, project_id, admission_mode, source_kind, media_assets, source_authority, planning_lineage}`; `package_id` is a content-derived `semantic_id`, not caller-supplied |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/domain.py` | `abbd7511` | READ — CURRENT IMPLEMENTATION | `validate_planning_lineage()` enforces `ABSENT_NOT_CREATED` for `IMPORTED` and a hash-matched `PRESENT_VERIFIED` (with `INT_ARMED_PLAN_HASH_MISMATCH` on mismatch) for `BRIEF_LED`; `make_media_asset()` computes `asset_id` from content |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/transcript.py` | `1f0dad14` | READ — CURRENT IMPLEMENTATION | `TranscriptService.align()` requires fully pre-computed word-level timestamps and speaker labels — it validates and stores, it does not perform speech-to-text or forced alignment |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/visual.py` | `2ffba733` | READ — CURRENT IMPLEMENTATION | `VisualIndexService.compile()` requires pre-computed shots/keyframes; an empty `shots` list makes it default to one shot spanning the full `duration_ms` with no keyframes — it does not perform shot-boundary detection |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/media.py` | `4fcd9575` | READ — CURRENT IMPLEMENTATION | `MediaInspector.inspect()` reads real bytes, computes SHA-256, and shells out to `ffprobe`; on ffprobe failure it returns `probe_status: UNAVAILABLE_OR_UNSUPPORTED` and `duration_ms: 0` rather than raising |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/repository.py` | `7259d89d` | READ — CURRENT IMPLEMENTATION | `store_object()` is content-addressed idempotency (identical payload short-circuits to `created: False` even under a fresh `idempotency_key`); `get_object()` raises `NotFoundError` for unknown IDs |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/canonical.py` | `61a1f92c` | READ — CURRENT IMPLEMENTATION | `require_portable_uri()` only accepts `workspace://`, `source://`, `artifact://`, `memory://` prefixes — a raw filesystem path is rejected |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/errors.py` | `b2cfcdce` | READ — CURRENT IMPLEMENTATION | `ValidationError` (`INT_VALIDATION_FAILED`), `ConflictError` (`INT_CONFLICT`), `NotFoundError` (`INT_NOT_FOUND`), `StateError` (`INT_STATE_INVALID`) are the exception types the API must translate |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/application.py` | `25bd47f5` | READ — CURRENT IMPLEMENTATION | `InterviewExpressionApplication` exposes `.source_packages`, `.transcripts`, `.visual`, `.media`, `.repository` as plain attributes — matches the object `TS-APP-API-001` already instantiates as `app.state.interview` |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/bootstrap.py` | `90d5ba9b` | READ — CURRENT IMPLEMENTATION | Module-level `status(database_path)` calls `.repository.health()`, **not** an `.status()` method on the application object |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/adapters.py` | `02a1eb97` | READ — CURRENT IMPLEMENTATION | No ASR, forced-alignment, or shot-detection adapter exists anywhere in this package — only handoff-shape builders to Pipeline/AIR/Studio |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/cli.py` | `e2b3c63c` | READ — CURRENT IMPLEMENTATION | CLI subcommands are only `bootstrap`, `health`, `status`, `demo`, `export-schemas` — there is no import/admission command anywhere today |
| `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/demo.py` | `b8e21665` | READ — CURRENT IMPLEMENTATION | Canonical reference call order: `admit` → `transcripts.align` → `transcripts.pack_phrases` → `bind_component` (alignment, phrases) → `visual.compile` → `bind_component` (visual index) |
| `tests/phase4/_support.py` | `ea9c4e21` | READ — CURRENT IMPLEMENTATION | `imported_app()` fixture shows the exact `IMPORTED` admission command shape used by the acceptance suite |
| `tests/phase4/test_ts_int_001_source_package.py` | `da679d2e` | READ — CURRENT IMPLEMENTATION | `test_valid_brief_led_admission_preserves_exact_plan_refs` shows the exact `BRIEF_LED` planning-lineage shape, including `planned_object_digests` |
| `packages/ca_contracts/src/ca_contracts/canonical.py` | `1cfcb99f` | READ — CURRENT IMPLEMENTATION | `bytes_sha256`, `canonical_sha256`, `utc_now_rfc3339` signatures confirmed |
| `TS-APP-API-001.md` | n/a | READ — WRITTEN_PENDING_AUDIT (draft dependency) | Defines `Depends(get_interview)`, `api/config.py::AppConfig(ca_data_root, ca_media_root, ca_delegation_root)`, and `ErrorResponse{error_code, message, service, timestamp}` — this spec reuses all three verbatim |

**Source gap notice 1 — no ASR / forced-alignment provider.** `FR-APP-022` describes the system "assigning word-level timestamps," but no code in this repo produces word-level timing from raw audio/video. `TranscriptService.align()` only validates and stores timing that is already computed. This spec does not add an ASR provider (that is a distinct, larger gap not listed anywhere in `CA_PROJECT_SNAPSHOT_V2.md` Section 6 — it should be raised to Program Control as a new gap). This spec instead defines two admissible transcript input shapes for the caller to supply (Section 5), one of which (`SRT`) derives approximate word timing deterministically and labels it `INFERRED`, never `OBSERVED`.

**Source gap notice 2 — no shot-boundary/keyframe-detection provider.** Same situation for `FR-APP-023`: `VisualIndexService.compile()` only validates pre-computed shots/keyframes. This spec relies on the domain's own documented default (empty `shots` → one full-duration shot, no keyframes) rather than inventing a detection algorithm.

**Source gap notice 3 — `TS-APP-API-001` health-router assumption does not match `bootstrap.py`.** `TS-APP-API-001` Section 5 assumes every service application object exposes `.status()`; `conscious_activations_interview_expression` has no such method — only the module-level `bootstrap.status()` helper, which calls `.repository.health()`. This does not block writing this spec (this spec does not touch the health router), but it must be corrected during `TS-APP-API-001`'s audit. Flagged here per `DRAFT_DEPENDENCY_NOT_ACCEPTED` handling.

---

## 2. Problem, User Outcome, Solution, and Scope

### Problem without this spec
There is no way to get a real interview into Conscious Activations. The CLI has no admission command. `interview_expression`'s services are fully validated and tested against synthetic fixtures only (`tests/phase4/_support.py`), but nothing has ever driven them with a real uploaded `.mp4` and a real transcript. Both Entry Points from `CA_PROJECT_SNAPSHOT_V2.md` Section 2 (Engineered Interview and Imported Interview) dead-end at "Canonical Interview Source Package" with no HTTP door to walk through. Gate B (`CA_APP_FR_EPIC_SPEC_PLAN.md` Part 7 — "A real `.mp4` + transcript can be imported end to end") cannot pass.

### User outcome
An operator (today: a developer exercising the API directly; later: the `CampaignNew.tsx` import tab from `TS-APP-UI-002`) can `POST` a real video file and a real transcript file to `/api/interviews/import` and receive back a `package_id` referencing a Canonical Interview Source Package with its transcript alignment, packed phrase transcript, and visual structure index already bound. The same operator can `POST` to `/api/interviews/brief-led` when a Brief already exists (from `TS-APP-COMPOSER-001`, once built) and get the same result while preserving the planned/observed distinction. Either way, a `GET /api/interviews/{package_id}/status` call shows exactly what has been bound and what has not.

### Solution
`api/routers/interviews.py` orchestrates four existing `InterviewExpressionApplication` services — `source_packages`, `transcripts`, `visual`, `media` — behind three HTTP endpoints, plus two new API-local helper modules (`api/services/media_store.py`, `api/services/transcript_ingest.py`) that do only HTTP-layer plumbing (saving an upload, parsing a transcript file into the shape the domain already requires). No existing Python package is modified.

### In scope
- `POST /api/interviews/import` — Entry Point B (`FR-APP-021`)
- `POST /api/interviews/brief-led` — Entry Point A (`FR-APP-020`)
- `GET /api/interviews/{package_id}/status` — `FR-APP-022` / `FR-APP-023` progress and component-binding view
- `api/services/media_store.py` — save an uploaded file under `CA_MEDIA_ROOT` and build a portable `logical_uri`
- `api/services/transcript_ingest.py` — parse `PRE_ALIGNED_JSON` (pass-through) and `SRT` (deterministic even-split, labeled `INFERRED`) into the `words`/`speaker_segments` shape `TranscriptService.align()` requires
- `api/schemas/interviews.py` — Pydantic request/response models
- Registering `interviews.router` in `api/main.py` (the single line `TS-APP-API-001` left commented for this purpose)

### Out of scope
- Expression Moment discovery and approval (`FR-APP-024`) — a separate future spec; this spec never binds `expression_moments` or `reaction_receipts`, so `publish()` (which requires both) is never called and packages admitted here remain `derivative_eligible: false`
- An ASR / forced-alignment provider (Source gap notice 1) — plain, untimed transcript text is rejected, not auto-aligned
- A real shot-boundary/keyframe-detection provider (Source gap notice 2) — every package gets the domain's single-shot default unless the caller supplies real shot data
- Interview Composer integration (`FR-APP-010`–`FR-APP-012`, `TS-APP-COMPOSER-001`) — the `/brief-led` endpoint accepts planning-lineage refs as opaque caller-supplied input; it does not generate a Brief
- Authentication/authorization, workspace multi-tenancy enforcement beyond the `workspace_id` field already present in the domain command
- Campaign creation (`TS-APP-API-004`), WebSocket status (`TS-APP-API-005`), React UI (`TS-APP-UI-002`)
- Any modification to `services/interview/` domain code

---

## 3. Governing Decisions and Constraints

**Product sovereignty.** `conscious_activations_interview_expression` owns Canonical Interview Source Package identity, lifecycle, and component-binding rules. The router calls the existing services exactly as written; it never constructs an `ie_objects` row itself and never bypasses `admit()`/`bind_component()`/`align()`/`compile()`.

**No fabricated planning history (central doctrine).** For `admission_mode: IMPORTED`, `planning_lineage` is always exactly `{"state": "ABSENT_NOT_CREATED"}` — the router does not accept or synthesize any Brief-shaped data on this path, matching `CA_PROJECT_SNAPSHOT_V2.md`'s Entry Point B contract ("No fabricated Brief history"). For `admission_mode: BRIEF_LED`, the caller must supply `brief_ref`, `planned_aip_ref`, `iac_ref`, `arm_receipt_ref`, and `planned_object_digests` exactly as `validate_planning_lineage()` requires; the router performs zero massaging of these values.

**Epistemic honesty in derived transcript timing.** This is a hard rule, not a style preference: word-level `epistemic_state` must truthfully describe how the timing was produced.
- `PRE_ALIGNED_JSON` input is passed through unchanged — the caller's declared `epistemic_state` per word (typically `OBSERVED`, from an external ASR run) is preserved verbatim. The router performs no inference on this path.
- `SRT` input has only cue-level timing that is real (captured), but word-level timing within a cue is computed by an even split across the cue's token count. Every word produced this way is forced to `epistemic_state: "INFERRED"`, never `"OBSERVED"`, regardless of what the SRT author intended. This mirrors the same doctrine that keeps the visual index `technical_only: true` and `creates_expression_moments: false` — mechanical derivation must never be dressed up as direct observation.

**Visual index stays technical-only.** No path in this spec ever proposes Expression Moments, tags, or Anchor Hits. The default single-shot, zero-keyframe index this spec produces for real footage is a legitimate, honest placeholder for "no shot-detection provider wired yet" — it is not a claim that the footage has no visually interesting boundaries.

**Media asset identity is content-derived, not caller-supplied.** `make_media_asset()` computes `asset_id` from the file's own bytes, `logical_uri`, and `media_type`. The API never accepts an `asset_id` from the caller and never invents one.

**Resumability over rollback.** `store_object()` is content-addressed: re-submitting an identical `admit()` command (same workspace/project/media/authority/lineage) returns the same `package_id` and `created: false`, even under a different `idempotency_key`. The multi-step admission pipeline (`admit` → `align` → `pack_phrases` → three `bind_component` calls → `visual.compile` → `bind_component`) is therefore safely retryable end-to-end: a partial failure after `admit()` succeeded leaves a real, inspectable, resumable package rather than requiring compensating deletes.

**Claim ceiling.** `INTERVIEW_ADMISSION_API_DEVELOPMENT_EVIDENCE`. This spec does not claim: ASR accuracy, shot-detection accuracy, production readiness, or that a package admitted through it is ready for campaign production (it is not — `derivative_eligible` stays `false` until `FR-APP-024` and `publish()` are exposed by a future spec).

**Forbidden.** Do not modify `services/interview/`. Do not accept a `BRIEF_LED` admission without the full, exact planning-lineage ref set. Do not fabricate multi-speaker diarization on the `SRT` path — it requires one caller-declared `speaker_id` and applies it to every word; overlapping SRT cues (which would imply more than one speaker) are rejected, not guessed at. Do not let `visual.compile()` run against `duration_ms: 0` (an unprobable file) — reject before calling it.

**Draft-dependency caveat.** If `TS-APP-API-001`'s audit changes the signature of `get_interview()`, the shape of `ErrorResponse`, or the `AppConfig` field names, Stage 1 of Section 7 below must be revised to match before this spec's routes can be wired into `main.py`.

---

## 4. Current Brownfield Architecture

| Component | Path | Actual behaviour | Disposition | Reason |
|---|---|---|---|---|
| `SourcePackageService.admit` | `source_package.py` | Validates command shape, computes content-derived `package_id`, stores `ADMITTED` package with all component slots `PENDING_REQUIRED_COMPONENT` | REUSE | Called exactly as-is by the router |
| `SourcePackageService.bind_component` | `source_package.py` | Versions the package, moves one named slot to `BOUND`, records history | REUSE | Called three times per admission (transcript alignment, phrase pack, visual index) |
| `TranscriptService.align` / `.pack_phrases` | `transcript.py` | Validates fully pre-timed words + segments; packs them into speaker-bounded phrases | REUSE | Called with words/segments produced by the new `transcript_ingest.py` helper |
| `VisualIndexService.compile` | `visual.py` | Validates pre-computed shots/keyframes; defaults to one full-duration shot when `shots=[]` | REUSE | Called with `shots=[]`, `keyframe_candidates=[]` unless the caller supplies real data |
| `MediaInspector.inspect` | `media.py` | Reads real file bytes, computes SHA-256, shells to `ffprobe` for duration/streams | REUSE | Called against the path the new `media_store.py` helper just wrote |
| `InterviewRepository.get_object` | `repository.py` | Fetches the current revision of any stored object by ID; raises `NotFoundError` | REUSE | Backs `GET /api/interviews/{package_id}/status` |
| `cli.py` | `cli.py` | No import/admission subcommand exists | AS-IS, NOT MODIFIED | Confirms this HTTP endpoint is the first real ingestion path in the whole repo |
| `bootstrap.status()` | `bootstrap.py` | Module-level health helper, distinct from an application `.status()` method | AS-IS, NOT MODIFIED | Not used by this spec; flagged for `TS-APP-API-001`'s audit (Source gap notice 3) |
| `api/main.py` (from `TS-APP-API-001`) | `api/main.py` | Has a commented placeholder line `# app.include_router(interviews.router, prefix="/api/interviews", tags=["interviews"])` | ADAPT | Uncomment and point at this spec's router |
| `api/config.py`, `api/dependencies.py`, `api/errors.py` (from `TS-APP-API-001`) | `api/*.py` | `AppConfig.ca_media_root`, `get_interview()`, `ErrorResponse` | REUSE | Imported by the new router and services unchanged |

---

## 5. Proposed Architecture and Workflows

### New components and responsibilities

```
api/services/media_store.py
  save_upload(upload, media_root, workspace_id, project_id) -> (local_path, logical_uri)
    - sanitizes the filename
    - writes to {CA_MEDIA_ROOT}/interviews/{workspace_id}/{project_id}/{safe_name}
    - builds logical_uri = "workspace://{workspace_id}/{project_id}/{safe_name}"
      (satisfies require_portable_uri's allowed prefixes)

api/services/transcript_ingest.py
  load_pre_aligned_transcript(raw_bytes) -> (words, speaker_segments)
    - pure pass-through JSON parse + top-level shape check
    - zero inference; caller's epistemic_state values are untouched
  parse_srt_transcript(raw_bytes, speaker_id) -> (words, speaker_segments)
    - parses SRT cues (index, start_ms, end_ms, text)
    - rejects overlapping cues (would imply undeclared multi-speaker content)
    - splits each cue's text into words, evenly distributes timestamps within
      the cue span, forces epistemic_state="INFERRED" on every word
    - one speaker_segment per cue, all using the single caller-declared speaker_id

api/routers/interviews.py
  POST /import        -> Entry Point B pipeline (admission_mode=IMPORTED)
  POST /brief-led      -> Entry Point A pipeline (admission_mode=BRIEF_LED)
  GET  /{id}/status    -> read-only projection of the stored package
```

### `POST /api/interviews/import` workflow (Entry Point B)

```
1. save_upload(video)                         -> local_path, logical_uri
2. interview.media.inspect(local_path, ...)   -> media_asset (real sha256, real ffprobe technical)
     if technical.probe_status != "PROBED"    -> 422 MEDIA_PROBE_FAILED (stop, no writes yet)
3. transcript_ingest(transcript_format, ...)  -> words, speaker_segments, policy_id
     unsupported/untimed format               -> 422 UNSUPPORTED_TRANSCRIPT_FORMAT (stop, no writes yet)
4. source_packages.admit({..., admission_mode: "IMPORTED",
     planning_lineage: {"state": "ABSENT_NOT_CREATED"}})   -> package (ADMITTED)
5. transcripts.align(package_ref, words, speaker_segments) -> alignment
6. transcripts.pack_phrases(alignment_ref, policy)         -> phrase_pack
7. bind_component(package, "transcript_alignment", alignment_ref)
8. bind_component(package, "packed_phrase_transcript", phrase_ref)
9. visual.compile(package_ref, duration_ms, shots=[], keyframe_candidates=[]) -> visual_index
10. bind_component(package, "visual_structure_index", visual_ref)
11. repository.get_object(package_id)                      -> final projection returned to caller
```

Steps 4–11 each carry their own `idempotency_key` derived from one caller-supplied (or generated) key, so a retried `POST` after a step-9 crash re-runs steps 4–8 as no-op replays (identical content, `created: false`) and resumes cleanly from step 9.

### `POST /api/interviews/brief-led` workflow (Entry Point A)

Identical to the above except:
- `admission_mode: "BRIEF_LED"`
- `planning_lineage` is the caller-supplied `{state: "PRESENT_VERIFIED", brief_ref, planned_aip_ref, iac_ref, arm_receipt_ref, planned_object_digests}` object, passed to `validate_planning_lineage()` untouched. A digest mismatch surfaces as the domain's own `INT_ARMED_PLAN_HASH_MISMATCH` `ValidationError`, mapped to HTTP 422.

### `GET /api/interviews/{package_id}/status`

Read-only. Calls `interview.repository.get_object(package_id)` (raises `NotFoundError` → 404) and projects the stored payload's `lifecycle_state`, `admission_mode`, `source_kind`, `planning_lineage`, `derivative_eligible`, media asset summaries, and each of the seven component slots (`state`, and either `ref` or `reason`). No new domain calls, no side effects.

### Idempotency

An optional `Idempotency-Key` request header seeds every step's key (`f"{key}:admit"`, `f"{key}:align"`, …). If absent, the router derives one from `workspace_id`, `project_id`, and the uploaded filename. This is a safety net on top of — not a replacement for — the domain's own content-addressed `store_object()` dedup described in Section 3.

### Synchronous execution

Everything in this spec executes synchronously within the request/response cycle. `interview_expression` has no background job queue; `ffprobe` on a single interview-length file and pure-Python validation/storage calls are fast enough for a direct HTTP response. Asynchronous, long-running execution belongs to `cmf_pipeline` (`FR-APP-051`, `TS-APP-API-005`) once a Campaign Order is created — that is a different module and a different spec.

---

## 6. Data Models, Contracts, Schemas, and APIs

### `api/schemas/interviews.py`

```python
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel

class RefModel(BaseModel):
    object_id: str
    version: str
    sha256: str

class MediaAssetSummary(BaseModel):
    asset_id: str
    sha256: str
    bytes: int
    media_type: str

class ComponentSlotSummary(BaseModel):
    state: Literal["PENDING_REQUIRED_COMPONENT", "BOUND", "NOT_APPLICABLE", "INVALIDATED"]
    ref: RefModel | None = None
    reason: str | None = None

class ImportInterviewResponse(BaseModel):
    package_id: str
    revision: int
    lifecycle_state: str
    admission_mode: Literal["IMPORTED", "BRIEF_LED"]
    derivative_eligible: bool
    planning_lineage: dict
    transcript_alignment_ref: RefModel
    packed_phrase_transcript_ref: RefModel
    visual_structure_index_ref: RefModel
    word_count: int
    phrase_count: int
    shot_count: int
    keyframe_count: int
    idempotent_replay: bool

class InterviewStatusResponse(BaseModel):
    package_id: str
    revision: int
    workspace_id: str
    project_id: str
    admission_mode: Literal["IMPORTED", "BRIEF_LED"]
    source_kind: Literal["INTERVIEW_EXPRESSION", "NON_INTERVIEW"]
    lifecycle_state: str
    derivative_eligible: bool
    planning_lineage: dict
    components: dict[str, ComponentSlotSummary]
    media_assets: list[MediaAssetSummary]
```

### Endpoints defined in this spec

| Method | Path | Request | Response | Error codes |
|---|---|---|---|---|
| `POST` | `/api/interviews/import` | multipart: `video`, `transcript` files + form fields below | `ImportInterviewResponse` (201) | `VALIDATION_FAILED`, `MEDIA_PROBE_FAILED`, `UNSUPPORTED_TRANSCRIPT_FORMAT`, `CONFLICT` |
| `POST` | `/api/interviews/brief-led` | multipart: `video`, `transcript` files + form fields below + `planning_lineage_json` | `ImportInterviewResponse` (201) | `VALIDATION_FAILED`, `MEDIA_PROBE_FAILED`, `UNSUPPORTED_TRANSCRIPT_FORMAT`, `CONFLICT` |
| `GET` | `/api/interviews/{package_id}/status` | — | `InterviewStatusResponse` (200) | `NOT_FOUND` |

Shared form fields for both `POST` endpoints: `workspace_id`, `project_id`, `operator_id`, `authority_scope`, `assertion_id`, `transcript_format` (`PRE_ALIGNED_JSON` | `SRT`), `speaker_id` (required when `transcript_format=SRT`), `visual_profile_id` (optional, default `single-shot-import-v1`). `brief-led` additionally requires `planning_lineage_json` (a JSON-encoded string of the planning-lineage object).

Positive example — `POST /api/interviews/import` response:
```json
{
  "package_id": "ie:source-package:7c1a9f0b2e3d4c5f6a7b8c9d0e1f2a3b",
  "revision": 4,
  "lifecycle_state": "COMPONENTS_IN_PROGRESS",
  "admission_mode": "IMPORTED",
  "derivative_eligible": false,
  "planning_lineage": { "state": "ABSENT_NOT_CREATED" },
  "transcript_alignment_ref": { "object_id": "ie:transcript-alignment:...", "version": "1.0.0", "sha256": "..." },
  "packed_phrase_transcript_ref": { "object_id": "ie:phrase-pack:...", "version": "1.0.0", "sha256": "..." },
  "visual_structure_index_ref": { "object_id": "ie:visual-index:...", "version": "1.0.0", "sha256": "..." },
  "word_count": 812,
  "phrase_count": 96,
  "shot_count": 1,
  "keyframe_count": 0,
  "idempotent_replay": false
}
```

Negative example — `POST /api/interviews/brief-led` with mismatched digests:
```json
{
  "error_code": "VALIDATION_FAILED",
  "message": "INT_ARMED_PLAN_HASH_MISMATCH",
  "service": null,
  "timestamp": "2026-07-26T10:00:00Z"
}
```

Negative example — `GET /api/interviews/{unknown}/status`:
```json
{
  "error_code": "NOT_FOUND",
  "message": "object not found: ie:source-package:00000000000000000000000000000000",
  "service": null,
  "timestamp": "2026-07-26T10:00:00Z"
}
```

---

## 7. Implementation Stages and Exact Target Paths

All paths are relative to the repository root after the `CA_APP_FR_EPIC_SPEC_PLAN.md` Part 5 restructure and after `TS-APP-API-001` lands.

### Stage 1 — Schemas

**`api/schemas/__init__.py`** — empty

**`api/schemas/interviews.py`** — exactly the models in Section 6.

### Stage 2 — Media storage helper

**`api/services/__init__.py`** — empty

**`api/services/media_store.py`**
```python
from __future__ import annotations
import re
import shutil
from pathlib import Path
from fastapi import UploadFile

_UNSAFE = re.compile(r"[^A-Za-z0-9_.-]+")

def _sanitize(filename: str) -> str:
    name = Path(filename).name
    cleaned = _UNSAFE.sub("_", name)
    return cleaned or "upload.bin"

def save_upload(upload: UploadFile, *, media_root: Path, workspace_id: str, project_id: str) -> tuple[Path, str]:
    safe_name = _sanitize(upload.filename or "upload.bin")
    dest_dir = media_root / "interviews" / workspace_id / project_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / safe_name
    with dest_path.open("wb") as out:
        shutil.copyfileobj(upload.file, out)
    logical_uri = f"workspace://{workspace_id}/{project_id}/{safe_name}"
    return dest_path, logical_uri
```

### Stage 3 — Transcript ingestion helper

**`api/services/transcript_ingest.py`**
```python
from __future__ import annotations
import json
import re
from typing import Any

class TranscriptFormatError(RuntimeError):
    pass

def load_pre_aligned_transcript(raw: bytes) -> tuple[list[dict], list[dict]]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise TranscriptFormatError(f"pre-aligned transcript is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict) or set(payload) != {"words", "speaker_segments"}:
        raise TranscriptFormatError(
            "pre-aligned transcript must be an object with exactly 'words' and 'speaker_segments'"
        )
    return payload["words"], payload["speaker_segments"]

_SRT_CUE_RE = re.compile(
    r"\d+\s*\n"
    r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*\n"
    r"((?:.+\n?)+?)(?=\n\d+\s*\n|\Z)",
    re.MULTILINE,
)

def _ts_to_ms(h: str, m: str, s: str, ms: str) -> int:
    return ((int(h) * 3600 + int(m) * 60 + int(s)) * 1000) + int(ms)

def _parse_cues(text: str) -> list[dict[str, Any]]:
    cues = []
    for match in _SRT_CUE_RE.finditer(text.strip() + "\n\n"):
        start_ms = _ts_to_ms(*match.group(1, 2, 3, 4))
        end_ms = _ts_to_ms(*match.group(5, 6, 7, 8))
        content = " ".join(line.strip() for line in match.group(9).strip().splitlines() if line.strip())
        if content:
            cues.append({"start_ms": start_ms, "end_ms": end_ms, "text": content})
    cues.sort(key=lambda c: c["start_ms"])
    for prior, cue in zip(cues, cues[1:]):
        if cue["start_ms"] < prior["end_ms"]:
            raise TranscriptFormatError(
                "overlapping SRT cues imply undeclared multi-speaker content; "
                "not supported by single-speaker even-split ingestion"
            )
    return cues

def parse_srt_transcript(raw: bytes, *, speaker_id: str) -> tuple[list[dict], list[dict]]:
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise TranscriptFormatError(f"SRT file is not valid UTF-8: {exc}") from exc
    cues = _parse_cues(text)
    if not cues:
        raise TranscriptFormatError("SRT file contains no parseable cues")
    words: list[dict] = []
    segments: list[dict] = []
    index = 0
    for cue_i, cue in enumerate(cues):
        tokens = cue["text"].split()
        span = cue["end_ms"] - cue["start_ms"]
        per_word = span / len(tokens)
        cursor = cue["start_ms"]
        for pos, token in enumerate(tokens):
            is_last = pos == len(tokens) - 1
            end = cue["end_ms"] if is_last else cue["start_ms"] + round(per_word * (pos + 1))
            end = max(end, cursor + 1)
            words.append({
                "word_id": f"srt-w-{index:05d}",
                "index": index,
                "text": token,
                "start_ms": cursor,
                "end_ms": end,
                "speaker_id": speaker_id,
                "speaker_state": "RESOLVED",
                "epistemic_state": "INFERRED",
                "tag_refs": [],
                "event_refs": [],
            })
            cursor = end
            index += 1
        segments.append({
            "segment_id": f"srt-seg-{cue_i:04d}",
            "start_ms": cue["start_ms"],
            "end_ms": cue["end_ms"],
            "speaker_id": speaker_id,
            "speaker_state": "RESOLVED",
        })
    return words, segments
```

### Stage 4 — Router

**`api/routers/interviews.py`**
```python
from __future__ import annotations
import json
from typing import Literal
from fastapi import APIRouter, Depends, File, Form, Header, HTTPException, UploadFile

from ca_contracts import utc_now_rfc3339
from conscious_activations_interview_expression.application import InterviewExpressionApplication
from conscious_activations_interview_expression.errors import (
    ConflictError, InterviewExpressionError, NotFoundError, StateError, ValidationError,
)

from api.config import load_config
from api.dependencies import get_interview
from api.errors import ErrorResponse
from api.schemas.interviews import ComponentSlotSummary, ImportInterviewResponse, InterviewStatusResponse
from api.services.media_store import save_upload
from api.services.transcript_ingest import (
    TranscriptFormatError, load_pre_aligned_transcript, parse_srt_transcript,
)

router = APIRouter()

DEFAULT_PHRASE_POLICY = {"policy_id": "phrase-pack-import-v1", "max_words": 12, "max_gap_ms": 800, "break_on_terminal_punctuation": True}
DEFAULT_VISUAL_PROFILE = "single-shot-import-v1"

_DOMAIN_ERROR_MAP = {
    ValidationError: (422, "VALIDATION_FAILED"),
    ConflictError: (409, "CONFLICT"),
    NotFoundError: (404, "NOT_FOUND"),
    StateError: (409, "STATE_INVALID"),
}

def _http_error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail=ErrorResponse(error_code=code, message=message, timestamp=utc_now_rfc3339()).model_dump(),
    )

def _domain_error_to_http(exc: InterviewExpressionError) -> HTTPException:
    status_code, code = _DOMAIN_ERROR_MAP.get(type(exc), (500, "INTERNAL_ERROR"))
    return _http_error(status_code, code, str(exc))

def _inspect_media(interview: InterviewExpressionApplication, video: UploadFile, *, workspace_id: str, project_id: str, media_root) -> dict:
    dest_path, logical_uri = save_upload(video, media_root=media_root, workspace_id=workspace_id, project_id=project_id)
    media_asset = interview.media.inspect(dest_path, logical_uri=logical_uri, media_type=video.content_type or "video/mp4")
    if media_asset["technical"].get("probe_status") != "PROBED" or media_asset["technical"].get("duration_ms", 0) < 1:
        raise _http_error(422, "MEDIA_PROBE_FAILED", "uploaded file could not be probed for duration/streams (ffprobe unavailable or file is corrupt)")
    return media_asset

def _ingest_transcript(transcript: UploadFile, *, transcript_format: str, speaker_id: str | None) -> tuple[list[dict], list[dict], str]:
    raw = transcript.file.read()
    if transcript_format == "PRE_ALIGNED_JSON":
        words, segments = load_pre_aligned_transcript(raw)
        return words, segments, "external-pre-aligned-v1"
    if transcript_format == "SRT":
        if not speaker_id:
            raise _http_error(422, "VALIDATION_FAILED", "speaker_id is required when transcript_format=SRT")
        words, segments = parse_srt_transcript(raw, speaker_id=speaker_id)
        return words, segments, "srt-even-split-v1"
    raise _http_error(422, "UNSUPPORTED_TRANSCRIPT_FORMAT", f"transcript_format '{transcript_format}' is not supported; use PRE_ALIGNED_JSON or SRT")

def _run_admission_pipeline(interview: InterviewExpressionApplication, *, command: dict, words: list[dict], segments: list[dict], policy_id: str, visual_profile_id: str, key: str) -> dict:
    admitted = interview.source_packages.admit(command, idempotency_key=f"{key}:admit")
    package_ref = interview.source_packages.ref(admitted)

    aligned = interview.transcripts.align(source_package_ref=package_ref, words=words, speaker_segments=segments, policy_id=policy_id, idempotency_key=f"{key}:align")
    alignment_ref = interview.source_packages.ref(aligned)
    packed = interview.transcripts.pack_phrases(alignment_ref, policy=DEFAULT_PHRASE_POLICY, idempotency_key=f"{key}:pack")
    phrase_ref = interview.source_packages.ref(packed)
    interview.source_packages.bind_component(package_ref["object_id"], "transcript_alignment", alignment_ref, idempotency_key=f"{key}:bind-alignment")
    interview.source_packages.bind_component(package_ref["object_id"], "packed_phrase_transcript", phrase_ref, idempotency_key=f"{key}:bind-phrases")

    duration_ms = command["media_assets"][0]["technical"]["duration_ms"]
    visual = interview.visual.compile(source_package_ref=package_ref, duration_ms=duration_ms, shots=[], keyframe_candidates=[], profile_id=visual_profile_id, idempotency_key=f"{key}:visual")
    visual_ref = interview.source_packages.ref(visual)
    interview.source_packages.bind_component(package_ref["object_id"], "visual_structure_index", visual_ref, idempotency_key=f"{key}:bind-visual")

    final = interview.repository.get_object(package_ref["object_id"])
    return {
        "package": final,
        "alignment_ref": alignment_ref,
        "phrase_pack_ref": phrase_ref,
        "visual_index_ref": visual_ref,
        "word_count": len(aligned["object"]["payload"]["words"]),
        "phrase_count": len(packed["object"]["payload"]["phrases"]),
        "shot_count": len(visual["object"]["payload"]["shots"]),
        "keyframe_count": len(visual["object"]["payload"]["keyframes"]),
        "idempotent_replay": bool(admitted.get("idempotent_replay", False)),
    }

def _to_response(result: dict) -> ImportInterviewResponse:
    payload = result["package"]["payload"]
    return ImportInterviewResponse(
        package_id=payload["package_id"], revision=result["package"]["revision"],
        lifecycle_state=payload["lifecycle_state"], admission_mode=payload["admission_mode"],
        derivative_eligible=payload["derivative_eligible"], planning_lineage=payload["planning_lineage"],
        transcript_alignment_ref=result["alignment_ref"], packed_phrase_transcript_ref=result["phrase_pack_ref"],
        visual_structure_index_ref=result["visual_index_ref"], word_count=result["word_count"],
        phrase_count=result["phrase_count"], shot_count=result["shot_count"], keyframe_count=result["keyframe_count"],
        idempotent_replay=result["idempotent_replay"],
    )

@router.post("/import", status_code=201, response_model=ImportInterviewResponse)
async def import_interview(
    video: UploadFile = File(...), transcript: UploadFile = File(...),
    workspace_id: str = Form(...), project_id: str = Form(...), operator_id: str = Form(...),
    authority_scope: str = Form(...), assertion_id: str = Form(...),
    transcript_format: Literal["PRE_ALIGNED_JSON", "SRT"] = Form(...),
    speaker_id: str | None = Form(None), visual_profile_id: str = Form(DEFAULT_VISUAL_PROFILE),
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
    interview: InterviewExpressionApplication = Depends(get_interview),
):
    config = load_config()
    key = idempotency_key or f"import:{workspace_id}:{project_id}:{video.filename}"
    try:
        media_asset = _inspect_media(interview, video, workspace_id=workspace_id, project_id=project_id, media_root=config.ca_media_root)
        words, segments, policy_id = _ingest_transcript(transcript, transcript_format=transcript_format, speaker_id=speaker_id)
        command = {
            "workspace_id": workspace_id, "project_id": project_id, "admission_mode": "IMPORTED",
            "source_kind": "INTERVIEW_EXPRESSION", "media_assets": [media_asset],
            "source_authority": {"operator_id": operator_id, "authority_scope": authority_scope, "assertion_id": assertion_id},
            "planning_lineage": {"state": "ABSENT_NOT_CREATED"},
        }
        result = _run_admission_pipeline(interview, command=command, words=words, segments=segments, policy_id=policy_id, visual_profile_id=visual_profile_id, key=key)
    except InterviewExpressionError as exc:
        raise _domain_error_to_http(exc) from exc
    except TranscriptFormatError as exc:
        raise _http_error(422, "UNSUPPORTED_TRANSCRIPT_FORMAT", str(exc)) from exc
    return _to_response(result)

@router.post("/brief-led", status_code=201, response_model=ImportInterviewResponse)
async def brief_led_interview(
    video: UploadFile = File(...), transcript: UploadFile = File(...),
    workspace_id: str = Form(...), project_id: str = Form(...), operator_id: str = Form(...),
    authority_scope: str = Form(...), assertion_id: str = Form(...),
    transcript_format: Literal["PRE_ALIGNED_JSON", "SRT"] = Form(...),
    speaker_id: str | None = Form(None), visual_profile_id: str = Form(DEFAULT_VISUAL_PROFILE),
    planning_lineage_json: str = Form(...),
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
    interview: InterviewExpressionApplication = Depends(get_interview),
):
    try:
        planning_lineage = json.loads(planning_lineage_json)
    except json.JSONDecodeError as exc:
        raise _http_error(422, "VALIDATION_FAILED", f"planning_lineage_json is not valid JSON: {exc}") from exc
    config = load_config()
    key = idempotency_key or f"brief-led:{workspace_id}:{project_id}:{video.filename}"
    try:
        media_asset = _inspect_media(interview, video, workspace_id=workspace_id, project_id=project_id, media_root=config.ca_media_root)
        words, segments, policy_id = _ingest_transcript(transcript, transcript_format=transcript_format, speaker_id=speaker_id)
        command = {
            "workspace_id": workspace_id, "project_id": project_id, "admission_mode": "BRIEF_LED",
            "source_kind": "INTERVIEW_EXPRESSION", "media_assets": [media_asset],
            "source_authority": {"operator_id": operator_id, "authority_scope": authority_scope, "assertion_id": assertion_id},
            "planning_lineage": planning_lineage,
        }
        result = _run_admission_pipeline(interview, command=command, words=words, segments=segments, policy_id=policy_id, visual_profile_id=visual_profile_id, key=key)
    except InterviewExpressionError as exc:
        raise _domain_error_to_http(exc) from exc
    except TranscriptFormatError as exc:
        raise _http_error(422, "UNSUPPORTED_TRANSCRIPT_FORMAT", str(exc)) from exc
    return _to_response(result)

@router.get("/{package_id}/status", response_model=InterviewStatusResponse)
def get_interview_status(package_id: str, interview: InterviewExpressionApplication = Depends(get_interview)):
    try:
        stored = interview.repository.get_object(package_id)
    except NotFoundError as exc:
        raise _http_error(404, "NOT_FOUND", str(exc)) from exc
    payload = stored["payload"]
    components = {}
    for name, slot in payload["components"].items():
        if slot["state"] == "BOUND":
            components[name] = ComponentSlotSummary(state=slot["state"], ref=slot["ref"])
        else:
            components[name] = ComponentSlotSummary(state=slot["state"], reason=slot.get("reason"))
    return InterviewStatusResponse(
        package_id=payload["package_id"], revision=stored["revision"],
        workspace_id=payload["workspace_id"], project_id=payload["project_id"],
        admission_mode=payload["admission_mode"], source_kind=payload["source_kind"],
        lifecycle_state=payload["lifecycle_state"], derivative_eligible=payload["derivative_eligible"],
        planning_lineage=payload["planning_lineage"], components=components,
        media_assets=[{"asset_id": m["asset_id"], "sha256": m["sha256"], "bytes": m["bytes"], "media_type": m["media_type"]} for m in payload["media_assets"]],
    )
```

### Stage 5 — Wire into the gateway

**`api/main.py`** (edit — one import, one `include_router` line, replacing the placeholder comment from `TS-APP-API-001`):
```python
from api.routers import health, interviews
...
app.include_router(health.router, prefix="/api")
app.include_router(interviews.router, prefix="/api/interviews", tags=["interviews"])
```

No changes to `infra/docker/docker-compose.yml` or `dockerfile.api` — both already establish the shared `ca-media` volume and `CA_MEDIA_ROOT` env var this spec's `media_store.py` depends on.

---

## 8. Failure, Migration, Rollback, Recovery, and Observability

### Typed failures

| Failure | Cause | Behaviour | Recovery |
|---|---|---|---|
| `MEDIA_PROBE_FAILED` | `ffprobe` missing, upload is not a real media file, or file is corrupt | 422 returned before any repository write occurs | Verify `ffmpeg`/`ffprobe` is installed in the container (already required by `TS-APP-API-001`'s `dockerfile.api`); re-upload a valid file |
| `UNSUPPORTED_TRANSCRIPT_FORMAT` | Caller sends plain untimed text, or an unrecognized `transcript_format` value | 422 returned before any repository write occurs | Supply `PRE_ALIGNED_JSON` (from an external ASR run) or `SRT`; plain text without timing has no supported path until an ASR provider is wired (Source gap notice 1) |
| Overlapping SRT cues | SRT implies more than one concurrent speaker | 422 `UNSUPPORTED_TRANSCRIPT_FORMAT` before any repository write occurs | Re-export a single-speaker SRT, or supply `PRE_ALIGNED_JSON` with real diarization |
| `INT_ARMED_PLAN_HASH_MISMATCH` (domain `ValidationError`) | `/brief-led` planning-lineage digests don't match the referenced ref hashes | 422 `VALIDATION_FAILED`; no package created (fails inside `admit()`, before any component work) | Caller must supply correct `planned_object_digests`; once `TS-APP-COMPOSER-001` exists this is computed automatically instead of hand-supplied |
| Partial pipeline failure (e.g. crash between phrase-pack bind and visual compile) | Process restart, DB lock timeout, etc. | Package exists in `COMPONENTS_IN_PROGRESS` with some slots `BOUND` and some `PENDING_REQUIRED_COMPONENT`; no destructive state | Re-`POST` the identical request — content-addressed `admit()`/`align()`/`pack_phrases()` calls replay as no-ops and the pipeline resumes from the first unbound slot |
| `CONFLICT` (domain `ConflictError`) | Same `Idempotency-Key` reused with a genuinely different request body, or `expected_revision` race | 409 | Use a fresh `Idempotency-Key` for a genuinely different request, or re-`GET` status and retry with current revision |
| `STORAGE_WRITE_FAILED` (unhandled `OSError` from `media_store.save_upload`) | `CA_MEDIA_ROOT` volume unwritable or out of disk space | 500 `INTERNAL_ERROR` | Check volume mount and available disk space; no package or component state was created |

### Migration
This spec adds `api/routers/interviews.py`, `api/schemas/interviews.py`, `api/services/media_store.py`, `api/services/transcript_ingest.py`, and edits two lines of `api/main.py`. No database migration — `interview_expression`'s own `.initialize()` (already called at gateway startup by `TS-APP-API-001`) already applies its SQLite migration.

### Rollback
None required. The domain's append-only, content-addressed object store means there is nothing to compensate for; a bad admission simply sits at whatever component state it reached and can be resumed or ignored.

### Observability
- Each of the pipeline's seven steps (admit, align, pack, bind×2, visual compile, bind) is logged at `INFO` with `package_id` and elapsed milliseconds, consistent with `TS-APP-API-001`'s uvicorn access-log convention.
- `MEDIA_PROBE_FAILED` and `UNSUPPORTED_TRANSCRIPT_FORMAT` are logged at `WARNING` (caller error, not a system fault).
- `STORAGE_WRITE_FAILED` and any unmapped exception are logged at `ERROR` with the full traceback.

---

## 9. Acceptance Criteria

**AC-001 — Real interview imported end to end (Gate B)**
Given a real `.mp4` file and a well-formed `SRT` transcript,
When `POST /api/interviews/import` is called with `transcript_format=SRT` and a `speaker_id`,
Then the response is HTTP 201 with `admission_mode: "IMPORTED"`, `lifecycle_state: "COMPONENTS_IN_PROGRESS"`, non-null `transcript_alignment_ref`, `packed_phrase_transcript_ref`, and `visual_structure_index_ref`.
Failure example: response omits one of the three refs, or returns 500.
Evidence: response body JSON.
Test layer: integration — `tests/api/test_interviews_import.py::test_real_mp4_and_srt_import_succeeds`.

**AC-002 — Imported admission never fabricates planning history**
Given any successful `/import` call,
When the stored package is inspected,
Then `planning_lineage == {"state": "ABSENT_NOT_CREATED"}` exactly, with no other keys present.
Failure example: `planning_lineage` contains a `brief_ref` or any other key.
Evidence: `GET /api/interviews/{id}/status` response body.
Test layer: integration — `tests/api/test_interviews_import.py::test_imported_admission_preserves_absent_lineage`.

**AC-003 — Brief-led admission with correct planning lineage succeeds**
Given a video, transcript, and a `planning_lineage_json` whose `planned_object_digests` match the SHA-256 of each referenced ref,
When `POST /api/interviews/brief-led` is called,
Then the response is HTTP 201 with `admission_mode: "BRIEF_LED"` and `planning_lineage.state == "PRESENT_VERIFIED"`.
Failure example: package is created with `admission_mode: "IMPORTED"` instead.
Evidence: response body JSON.
Test layer: integration — `tests/api/test_interviews_brief_led.py::test_valid_brief_led_admission_succeeds`.

**AC-004 — Brief-led admission rejects a digest mismatch**
Given a `planning_lineage_json` whose `planned_object_digests.brief` does not match `brief_ref.sha256`,
When `POST /api/interviews/brief-led` is called,
Then the response is HTTP 422 with `error_code: "VALIDATION_FAILED"` and `message` containing `"INT_ARMED_PLAN_HASH_MISMATCH"`, and no package exists for the attempted content.
Failure example: a package is created despite the mismatch.
Evidence: response status/body; absence of a matching object in the repository.
Test layer: integration — `tests/api/test_interviews_brief_led.py::test_digest_mismatch_rejected`.

**AC-005 — SRT-derived words are never marked OBSERVED**
Given an `SRT` transcript ingested via `/import`,
When the resulting `transcript_alignment` object's `words` are inspected,
Then every word has `epistemic_state: "INFERRED"`.
Failure example: any word shows `epistemic_state: "OBSERVED"`.
Evidence: direct repository read of the stored `transcript_alignment` payload in the test.
Test layer: integration — `tests/api/test_interviews_import.py::test_srt_words_are_inferred_not_observed`.

**AC-006 — Pre-aligned JSON preserves caller-declared epistemic state verbatim**
Given a `PRE_ALIGNED_JSON` transcript where every word is declared `epistemic_state: "OBSERVED"`,
When `/import` ingests it,
Then the stored `transcript_alignment.words` show `epistemic_state: "OBSERVED"` unchanged.
Failure example: the API overwrites the declared value.
Evidence: stored payload comparison.
Test layer: integration — `tests/api/test_interviews_import.py::test_pre_aligned_json_epistemic_state_passthrough`.

**AC-007 — Untimed plain text transcript is rejected**
Given a plain `.txt` transcript with no timing information and `transcript_format=SRT` attempted against it (or an unsupported `transcript_format` value),
When `/import` is called,
Then the response is HTTP 422 with `error_code: "UNSUPPORTED_TRANSCRIPT_FORMAT"`, and no package is created.
Failure example: a package is created with fabricated timestamps.
Evidence: response status/body; repository has no new object.
Test layer: integration — `tests/api/test_interviews_import.py::test_untimed_transcript_rejected`.

**AC-008 — Corrupt media upload fails cleanly before any write**
Given an uploaded file that is not valid media (e.g. a zero-byte file),
When `/import` is called,
Then the response is HTTP 422 with `error_code: "MEDIA_PROBE_FAILED"`, and no `canonical_interview_source_package` object exists for the attempted content.
Failure example: `admit()` is called anyway and a broken package is created.
Evidence: response status/body; `repository.list_objects("canonical_interview_source_package")` count unchanged.
Test layer: integration — `tests/api/test_interviews_import.py::test_corrupt_media_rejected_before_admit`.

**AC-009 — Status on an unknown package returns 404**
Given no package exists with a given ID,
When `GET /api/interviews/{id}/status` is called,
Then the response is HTTP 404 with `error_code: "NOT_FOUND"`.
Failure example: HTTP 500 or an empty 200.
Evidence: response status/body.
Test layer: integration — `tests/api/test_interviews_status.py::test_unknown_package_returns_404`.

**AC-010 — Status reflects real component binding**
Given a package admitted via `/import`,
When `GET /api/interviews/{id}/status` is called,
Then `components.transcript_alignment.state == "BOUND"`, `components.packed_phrase_transcript.state == "BOUND"`, `components.visual_structure_index.state == "BOUND"`, and `components.expression_moments.state == "PENDING_REQUIRED_COMPONENT"`.
Failure example: `expression_moments` shows `BOUND` (this spec never binds it).
Evidence: response body JSON.
Test layer: integration — `tests/api/test_interviews_status.py::test_status_reflects_bound_components`.

**AC-011 — Identical retry is idempotent, not duplicative**
Given a successful `/import` call,
When the exact same multipart request is sent again (same files, same form fields, any `Idempotency-Key`),
Then the response is HTTP 201 with the same `package_id` and `idempotent_replay: true`, and the repository contains exactly one `canonical_interview_source_package` object for that content.
Failure example: a second, distinct `package_id` is created.
Evidence: response body across both calls; repository object count.
Test layer: integration — `tests/api/test_interviews_import.py::test_identical_retry_is_idempotent`.

**AC-012 — Visual index defaults to one full-duration shot with no keyframes**
Given `/import` is called without any caller-supplied shot/keyframe data,
When the resulting `visual_structure_index` is inspected,
Then `shots` has exactly one entry spanning `0` to the probed `duration_ms`, `keyframes` is empty, `technical_only: true`, and `creates_expression_moments: false`.
Failure example: fabricated shot boundaries or keyframes appear without a real detection provider behind them.
Evidence: stored `source_visual_structure_index` payload.
Test layer: integration — `tests/api/test_interviews_import.py::test_default_visual_index_is_single_shot`.

**AC-013 — No modification to existing service packages**
Given the Phase 9 test suite at `tests/` was passing before this spec,
When this spec is fully implemented and `python -m pytest tests/ -q` is run,
Then all pre-existing tests continue to pass.
Failure example: any previously-passing test now fails.
Evidence: pytest output — 0 new failures.
Test layer: regression — run full existing suite.

---

## 10. Testing and Completion Evidence

### Test files to create

**`tests/api/fixtures/`**
- `synthetic_interview.mp4` — a short, real, ffprobe-readable clip generated deterministically in CI via `ffmpeg -f lavfi -i testsrc -f lavfi -i sine -t 6 ...` (real bytes, real `ffprobe` output — not a declared/synthetic technical dict)
- `sample_transcript.srt` — a small, non-overlapping, single-speaker SRT fixture
- `sample_pre_aligned.json` — a `{"words": [...], "speaker_segments": [...]}` fixture matching `TranscriptService.align()`'s exact contract
- `corrupt.mp4` — a zero-byte file for AC-008
- `untimed.txt` — plain text with no timing for AC-007

**`tests/api/test_interviews_import.py`**
- `test_real_mp4_and_srt_import_succeeds` — AC-001
- `test_imported_admission_preserves_absent_lineage` — AC-002
- `test_srt_words_are_inferred_not_observed` — AC-005
- `test_pre_aligned_json_epistemic_state_passthrough` — AC-006
- `test_untimed_transcript_rejected` — AC-007
- `test_corrupt_media_rejected_before_admit` — AC-008
- `test_identical_retry_is_idempotent` — AC-011
- `test_default_visual_index_is_single_shot` — AC-012

**`tests/api/test_interviews_brief_led.py`**
- `test_valid_brief_led_admission_succeeds` — AC-003
- `test_digest_mismatch_rejected` — AC-004

**`tests/api/test_interviews_status.py`**
- `test_unknown_package_returns_404` — AC-009
- `test_status_reflects_bound_components` — AC-010

### Test tooling
Multipart upload pattern with FastAPI's `TestClient`:
```python
from fastapi.testclient import TestClient
from api.main import app

def test_real_mp4_and_srt_import_succeeds(fixtures_dir):
    with TestClient(app) as client:
        with open(fixtures_dir / "synthetic_interview.mp4", "rb") as video, \
             open(fixtures_dir / "sample_transcript.srt", "rb") as transcript:
            response = client.post(
                "/api/interviews/import",
                files={"video": ("interview.mp4", video, "video/mp4"), "transcript": ("t.srt", transcript, "text/plain")},
                data={
                    "workspace_id": "ws-1", "project_id": "prj-1", "operator_id": "op-1",
                    "authority_scope": "DEVELOPMENT_TEST", "assertion_id": "assert-1",
                    "transcript_format": "SRT", "speaker_id": "guest",
                },
            )
        assert response.status_code == 201
        body = response.json()
        assert body["admission_mode"] == "IMPORTED"
        assert body["planning_lineage"] == {"state": "ABSENT_NOT_CREATED"}
```

### Pre-existing regression
Run before and after implementing this spec:
```bash
python -m pytest tests/ -q --tb=short
```
Zero new failures is a hard gate (AC-013).

### Build Receipt claim ceiling
`INTERVIEW_ADMISSION_API_DEVELOPMENT_EVIDENCE`

This spec does not claim:
- ASR or forced-alignment accuracy (Source gap notice 1 remains open)
- shot-boundary or keyframe-detection accuracy (Source gap notice 2 remains open)
- that an admitted package is production- or campaign-ready — `derivative_eligible` remains `false` until Expression Moment discovery/approval (`FR-APP-024`) and `publish()` are exposed by a future spec
- authentication, authorization, or multi-tenant isolation
- certified or production-authorized operation

---
spec_end: true
next_spec: TS-APP-API-002 (Harness Library API) or TS-APP-API-004 (Campaign CRUD API), per Wave sequencing in CA_APP_FR_EPIC_SPEC_PLAN.md Part 4
open_question_for_next_spec_author: TS-APP-API-004 (Campaign CRUD) must decide whether Campaign Order creation requires derivative_eligible=true (which nothing in Wave 1 can produce, since that requires FR-APP-024 + publish()) or whether it may select COMPONENTS_IN_PROGRESS packages directly. This spec deliberately leaves that decision to TS-APP-API-004's author rather than guessing at it.
---
