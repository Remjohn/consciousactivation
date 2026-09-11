---
spec_id: TS-APP-API-006
title: Control Tower and Supervision API
document_class: TECH_SPEC
product: Conscious Activations
module: api
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CURRENT
build_authority: false
controlling_frs:
  - FR-APP-060 (Control Tower)
  - FR-APP-061 (Timeline projection)
  - FR-APP-062 (Natural language revision)
  - FR-APP-063 (Exception review and resolution)
  - FR-APP-064 (Ship gate)
controlling_stories:
  - ST-APP-08.01 (View Control Tower for a campaign)
  - ST-APP-08.02 through ST-APP-08.03 (timeline projection, exception review — named collectively as
    "ST-APP-08.01 through ST-APP-08.05" in CA_APP_FR_EPIC_SPEC_PLAN.md Part 4; only 08.01 and 08.04 have
    written acceptance text in Part 3, so this spec derives 08.02/08.03/08.05 directly from FR-APP-061,
    FR-APP-063, FR-APP-064 rather than from unwritten story text — flagged, not invented)
  - ST-APP-08.04 (Submit a natural language revision)
upstream_dependencies:
  - CA_PROJECT_SNAPSHOT_V2.md (authority — CURRENT)
  - CA_APP_FR_EPIC_SPEC_PLAN.md (authority — CURRENT)
  - TS-APP-API-001.md (quality_state: WRITTEN_PENDING_AUDIT — DRAFT_DEPENDENCY_NOT_ACCEPTED; this spec
    depends on its `api/config.py::AppConfig`/`load_config`, `api/dependencies.py::get_pipeline`, and
    `api/errors.py::ErrorResponse`, and additionally PATCHES its `api/main.py` lifespan and
    `infra/docker/dockerfile.api` output — see Section 7 Stage 0)
  - TS-APP-API-004.md — NOT YET WRITTEN. Per CA_APP_FR_EPIC_SPEC_PLAN.md Part 4, TS-APP-API-004 (Campaign
    CRUD API) is this spec's direct upstream dependency ("Depends on: TS-APP-API-004, TS-APP-API-005").
    It has not been authored. This spec is being written out of Wave sequence at the user's explicit
    request. Section 3 defines the minimal persistence contract this spec needs from Campaign creation
    and marks it ASSUMED_INTERFACE_PENDING_004 — binding on TS-APP-API-004's author, not a substitute for
    that spec.
  - TS-APP-API-005.md — NOT YET WRITTEN. This spec does not call anything from TS-APP-API-005 directly
    (WebSocket status push is a separate concern from supervision's pull-based projections), so its
    absence is not load-bearing here, but is recorded for completeness per the Wave 2 dependency list.
downstream_consumers:
  - TS-APP-UI-003 (Control Tower UI — CampaignDetail.tsx, ControlTower.tsx, Timeline.tsx,
    RevisionComposer.tsx, ExceptionQueue.tsx all call these endpoints directly)
  - Production readiness Gates E and F in CA_APP_FR_EPIC_SPEC_PLAN.md Part 7
    ("A natural language revision compiles and executes", "Ship gate produces signed audit export")
output_path: api/routers/campaigns.py (supervision routes), api/routers/revisions.py, api/routers/ship.py
  (and supporting files listed in Section 7)
wave: 2
---

# TS-APP-API-006 — Control Tower and Supervision API

## 1. Files and Authorities Read

| File | SHA-256 (short) | Status | Fact extracted |
|---|---|---|---|
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/domain.ts` | `4fa1b8a5` | READ — CURRENT IMPLEMENTATION | Canonical TypeScript shapes for every object this spec projects or accepts: `ControlTowerProjection`, `TimelineProjection`, `OperatorRevisionRequest`, `DirectManipulationDelta`, `ChangeRequestProgram`, `ExceptionReviewPackage`, `HumanResolutionEpisode`, `ShipRequest`/`ShipDecision`, `AuditExportManifest`, `CampaignOrder`/`CampaignState` |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/controlTower.ts` | `1b46231f` | READ — CURRENT IMPLEMENTATION | `buildControlTowerProjection(input: ControlTowerInput)` is a pure, deterministic function; computes `available_actions` from campaign/timeline/artifact/exception state; validates every ref via `validators.ts` |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/timeline.ts` | `2e64ba20` | READ — CURRENT IMPLEMENTATION | `projectVideoEditProgram(program: VideoEditProgramInput)` requires exactly one track with `role === "PRIMARY_A_ROLL_SPINE"`; converts ms→frame; per-item `editable_operations` depend on track role and element kind |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/revision.ts` | `903449ed` | READ — CURRENT IMPLEMENTATION | `compileNaturalLanguageRevision`/`compileDirectManipulation` are pure functions over a caller-supplied `RevisionContext` (tools, steering recipes, allowed node IDs, target-layer map, state version, invariants, wrong-reading locks); `DEFAULT_STUDIO_TOOLS` is the canonical 9-tool registry; unmatched natural-language input returns `NEEDS_CLARIFICATION` with `escalation: "CLARIFY_TARGET_OPERATION_OR_SELECT_STEERING_RECIPE"` |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/rerun.ts` | `da5604bf` | READ — CURRENT IMPLEMENTATION | `compileSelectiveRerun` requires `compilation_status === "COMPILED"`, walks the dependency graph forward from changed nodes to compute `invalidated_node_ids`/`preserved_node_ids`; `withRerunProjection` re-derives `program_sha256` after attaching the rerun's invalidation set |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/resolutions.ts` | `b6ac91e1` | READ — CURRENT IMPLEMENTATION | `createHumanResolutionEpisode` is pure; `HumanResolutionLedger` is a **Node `fs`-backed**, hash-chained, append-only JSONL ledger (`store.ts`) — every append re-verifies the entire prior chain; `ProgrammingMaterialIndex` is in-memory only, lost on process exit |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/ship.ts` | `cfc21642` | READ — CURRENT IMPLEMENTATION | `evaluateShipRequest` denies unless: campaign `lifecycle_state === "READY_TO_SHIP"`, `autonomy_mode !== "SHADOW"`, both authority/policy refs present, at least one artifact and one evaluation ref present, and `unresolved_exception_ids` is empty — all six checks accumulate independently into `denial_codes`, not short-circuit |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/auditExport.ts` | `add16276` | READ — CURRENT IMPLEMENTATION | `buildAuditExportManifest` is pure; `writeAuditExport` re-verifies `canonicalSha256` against `export_sha256` before writing — refuses to write a manifest whose hash doesn't reproduce |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/campaign.ts` | `6142cf1d` | READ — CURRENT IMPLEMENTATION | `transitionCampaign` enforces a fixed state machine (`allowedTransitions`) and refuses `SHADOW → SHIPPED`; `buildExceptionReviewPackage` defaults `allowed_decisions` to `["REQUEST_REVISION", "REJECT"]`; `shouldInterruptOperator` encodes the autonomy-mode interrupt policy |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/validators.ts` | `437b9aa8` | READ — CURRENT IMPLEMENTATION | `forbiddenStudioLayers` = `{AIR_SEMANTIC_AUTHORITY, PRIMITIVE_MEANING, PRIMITIVE_COALITION_MEANING, ARCHETYPE_COALITION_MEANING, IDENTITY_DNA_CANONICAL, OBSERVED_HUMAN_REACTION}` — Studio can never compile an operation against these; bounded-program cap is 4 operations |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/canonical.ts` | `8cb8ecb9` | READ — CURRENT IMPLEMENTATION | `canonicalSha256`/`deterministicId` require every object key sorted and every number a safe integer — no floats anywhere in a Studio-signed object; this spec's Python-side payload construction must not introduce a float or an `undefined`-shaped `None` into any object it hands to the bridge |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/store.ts` | `9b952936` | READ — CURRENT IMPLEMENTATION | `AppendOnlyJsonLedger` is generic; used unmodified by `HumanResolutionLedger` |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/surfaces.ts` | `1d9edb46` | READ — CURRENT IMPLEMENTATION | `routeHarnessToSurfaces` is pure and cheap to recompute; rejects Format 02 categories |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/generated/contracts.ts` | `a38d316c` | READ — CURRENT IMPLEMENTATION | `TypedFailure{code, evidence_refs, message, next_action, responsible_product, retry_class}` is the canonical failure shape referenced by Section 5 |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/src/index.ts` | `f82a04b3` | READ — CURRENT IMPLEMENTATION | Re-exports every module above; `main()` only implements `health`/`demo` CLI subcommands — **no HTTP server, no RPC entrypoint of any kind exists today** |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/package.json` | `fcc83abe` | READ — CURRENT IMPLEMENTATION | `"type": "module"`, `tsc` build to `dist/`, zero runtime `dependencies` — pure Node standard library only |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/tsconfig.json` | `2288a69d` | READ — CURRENT IMPLEMENTATION | `target: ES2022`, `module: ES2022`, `moduleResolution: Bundler`, `outDir: dist` — confirms `node dist/rpc.js` is the correct invocation shape once built |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/application.py` | `a32b6cea` | READ — CURRENT IMPLEMENTATION | `PipelineApplication.repository` is a public attribute (`PipelineRepository`); `.status()` exists (unlike `interview_expression`, per TS-APP-API-003's Source gap notice 3) |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/infrastructure/repository.py` | (read directly, not re-hashed — see note below) | READ — CURRENT IMPLEMENTATION | `PipelineRepository.store_object(object_type, payload, *, idempotency_key, object_id, expected_revision=None, ...)` is a generic, content-addressed, **optimistically-concurrent, revisioned** object store — `expected_revision` mismatches raise `PipelineConflict`; `get_object(object_id)` returns the current revision; `list_objects(object_type=...)` lists by type. This is the exact primitive Section 3 uses for Campaign persistence — no new storage technology needed |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/application/run_service.py` | `44917906` | READ — CURRENT IMPLEMENTATION | `WorkflowRunService.status(run_id)` returns `{run_id, workflow_id, state, revision, cancel_requested, current_checkpoint_id, nodes: [{node_id, state, attempt_count, dispatch_ordinal, output_ref, failure}]}`; `fail_node()` stores an arbitrary `failure` mapping (expected `TypedFailure`-shaped) on `NodeState.FAILED`; `QUARANTINED` means a late result arrived after cancellation — it is **not** a human-review state |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/domain/enums.py` | `584a03fb` | READ — CURRENT IMPLEMENTATION | `NodeState = {BLOCKED, READY, DISPATCHED, RUNNING, SUCCEEDED, FAILED, CANCELLED, INVALIDATED, QUARANTINED}` — no direct match to Studio's `RunNodeProjection.status` enum (which has `PENDING`/`WAITING_HUMAN` instead of `BLOCKED`/`DISPATCHED`/`QUARANTINED`); `NodeKind.HUMAN_GATE` exists as a node *type*, not a node *state* |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/repair.py` | `51312306` | READ — CURRENT IMPLEMENTATION | `BoundedRepairService.diagnose(failures)` maps a `TypedFailure.code` to `responsible_layer` via `LAYER_BY_CODE` (7 known codes; unknown codes fall through to `UNKNOWN_REQUIRES_TRIAGE`) and `repairable_by_pipeline: layer in {RUNTIME, PIPELINE_COMPOSITION}`; `ALLOWED_ACTIONS = {SHIFT_BBOX, REDUCE_FONT_SIZE, ADD_AUDIO_FADE, SHIFT_CUT_TO_WORD_BOUNDARY, RERENDER_RUNTIME, ESCALATE_OWNER}` |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/service.py` | `42c119c9` | READ — CURRENT IMPLEMENTATION | `EvaluationService.evaluate()` stores an `independent_evaluation_receipt` object with `verdict ∈ {PASS, FAIL, BLOCKED}`; producer/evaluator independence is enforced (`EVAL_EVALUATOR_NOT_INDEPENDENT`) |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/media/program.py` | `7d149c72` | READ — CURRENT IMPLEMENTATION | `VideoEditProgramService.projection(program_id)` returns `{program_ref: {object_id, version, sha256}, canvas, tracks, read_only: True}` — the exact shape `projectVideoEditProgram`'s `VideoEditProgramInput` needs, modulo field renaming (`elements` vs. the stored `elements` — same key) |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/batch/service.py` | `d1553853` | READ — CURRENT IMPLEMENTATION | `ContentBatchService.compile_batch()` produces a `source_backed_content_batch` (`batch_id`, `jobs[]`) — a **different object shape from Studio's `CampaignOrder`/`CampaignState`**, with no `autonomy_policy`, `lifecycle_state`, or `version` field anywhere. See Source gap notice 2 |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/domain/errors.py` | `abb1b94a` | READ — CURRENT IMPLEMENTATION | `PipelineNotFound`, `PipelineConflict`, `PipelineValidationError`, `PipelineLifecycleError` are the exception types this spec's routers translate to HTTP |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/domain/models.py` | (read, spot-checked) | READ — CURRENT IMPLEMENTATION | Runtime workflow node fields are `{node_id, capability_id, phase_order, purpose, actor_kind, role, product_boundary, input_contracts, output_contracts, side_effect_class, implementation}` — `implementation.owner_product` is the closest analog to `RunNodeProjection.owner_product`; there is no `dependency_ids` field on the node itself (dependencies live in the workflow's edge/phase-order structure, read via `PipelineApplication.graph`) |
| `TS-APP-API-001.md` | `7fe1b48f` | READ — WRITTEN_PENDING_AUDIT (draft dependency) | Confirms `get_pipeline`, `AppConfig`/`load_config`, `ErrorResponse`, and the exact `api/main.py` lifespan/Dockerfile text this spec patches in Stage 0 |
| `TS-APP-API-002.md` | `a61d6b93` | READ — WRITTEN_PENDING_AUDIT (draft dependency) | `HarnessDetail` has no `wrong_reading_locks` field — see Source gap notice 5; confirms the `RefModel`-per-schema-file convention this spec follows |
| `TS-APP-API-003.md` | `5d6471f6` | READ — WRITTEN_PENDING_AUDIT (draft dependency) | Confirms the `RefModel`, error-mapping-table, and `Files and Authorities Read`-with-gap-notices conventions this spec follows |
| `CA_PROJECT_SNAPSHOT_V2.md` | `b568220d` | READ — CURRENT AUTHORITY | Section 4 lists Studio as "TypeScript domain, no React yet" with **no Python package** — confirms this is not an oversight, it is the actual state of the repo |
| `CA_APP_FR_EPIC_SPEC_PLAN.md` | `8ea2646c` | READ — CURRENT AUTHORITY | Source of `controlling_frs`/`controlling_stories`/scope text above; Part 7 Gates E and F are this spec's production-readiness targets |

### Source gap notices (read carefully — these govern this spec's design)

**Source gap notice 1 — Studio has no runtime, only a CLI.** `FR-APP-062`, `FR-APP-063`, and `FR-APP-064` in `CA_APP_FR_EPIC_SPEC_PLAN.md` each cite "Python revision compiler in cmf_pipeline," "cmf_pipeline error handling," and "Python ship logic" as existing code. None of these exist. Every revision-compilation, ship-decision, exception-package, and human-resolution function lives **only** in `07_CONSCIOUS_ACTIVATIONS_STUDIO`, a Node.js/TypeScript package with zero Python bindings and zero HTTP surface — only a CLI with `health` and `demo` subcommands (`index.ts`). `cmf_pipeline` has no `revision.py`, `ship.py`, or `resolutions.py` anywhere. This is the single largest gap this spec closes: Section 3 and Section 7 Stage 1 add a JSON-in/JSON-out RPC entrypoint (`services/studio/src/rpc.ts`) to the Studio package itself, and a Python subprocess bridge (`api/services/studio_bridge.py`) that calls it. This is new code this spec introduces, not a wrap of something that already runs as a service.

**Source gap notice 2 — no persisted object satisfies Studio's `CampaignOrder`/`CampaignState` shape anywhere in the Python codebase.** `cmf_pipeline.batch.service.ContentBatchService.compile_batch()` is the only "campaign-adjacent" Python code, and it produces a `source_backed_content_batch` (`batch_id`, `jobs[]`) with no `lifecycle_state`, `autonomy_policy`, or `version` field — it cannot serve as the Control Tower's `campaign`/`order` input without translation, and no such translation exists. TS-APP-API-004 ("Campaign CRUD API") is the spec responsible for closing this gap, but it has not been written. Section 3 defines the minimal persistence contract (object types, object IDs, and the `PipelineRepository.store_object`/`get_object` convention) this spec needs in order to read and advance campaign state, using the exact same content-addressed, revisioned object store `cmf_pipeline` already uses everywhere else — no new storage technology. This convention is marked `ASSUMED_INTERFACE_PENDING_004`: TS-APP-API-004's author must adopt it (or explicitly migrate away from it with a reconciliation note) when that spec is written. This spec's own test suite creates its own fixture `CampaignOrder`/`CampaignState` objects directly against the convention, since no creation endpoint exists yet to do it through HTTP.

**Source gap notice 3 — the Dockerfile TS-APP-API-001 defines has no Node.js runtime.** `infra/docker/dockerfile.api` (TS-APP-API-001 Stage 4) is `FROM python:3.12-slim` and never installs Node, never copies `services/studio`, never runs `npm install`/`npm run build`. Once this spec exists, the API container cannot start without Node available and the Studio package built — the bridge subprocess would fail on every request. Section 7 Stage 0 patches this Dockerfile.

**Source gap notice 4 — `NodeState` (Python) and `RunNodeProjection.status` (Studio TypeScript) are not the same enum.** Python has `BLOCKED, READY, DISPATCHED, RUNNING, SUCCEEDED, FAILED, CANCELLED, INVALIDATED, QUARANTINED`. Studio has `PENDING, READY, RUNNING, WAITING_HUMAN, SUCCEEDED, FAILED, CANCELLED, INVALIDATED`. Section 5 defines an explicit, documented mapping table rather than assuming a 1:1 correspondence. `QUARANTINED` (late/uncomsumable result) is mapped to `FAILED` with a specific blocker code — it is not the "waiting for human" state (there is no Python state for that; `WAITING_HUMAN` is derived from `NodeKind.HUMAN_GATE` combined with a mapped-`READY`/`RUNNING` status, per Section 5).

**Source gap notice 5 — `wrong_reading_locks` has no confirmed source.** `RevisionContext.wrong_reading_locks` is a required input to `compileNaturalLanguageRevision`/`compileDirectManipulation`. `TS-APP-API-002.md`'s `HarnessDetail` schema has no `wrong_reading_locks` field (its `category_binding: dict` may contain one under `CategoryBinding.canonical_dict()`, but this spec did not read `category_binding.py` closely enough to confirm the key name, and doing so is out of scope for this spec's file-read budget). This spec defaults `wrong_reading_locks` to `[]` when not present in the harness detail payload's `category_binding` dict under a `wrong_reading_locks` key, and flags this as an open reconciliation item for whichever spec (TS-APP-API-002's audit, or a future revision) confirms the real key.

**Source gap notice 6 — `target_layers_by_ref` has no general derivation across every module.** This spec confirmed the `video_edit_program` object type (from `media/program.py`) maps to Studio's `VIDEO_EDIT_PROGRAM` target layer. It did **not** read `cmf_pipeline/composition/ir.py`, VAE's asset object types, or AIR's candidate-portfolio object types closely enough to assert their exact `object_type` strings with the same confidence. Section 6 defines `OBJECT_TYPE_TO_TARGET_LAYER` as a small, explicitly partial dict with one confirmed entry and documents the extension mechanism (add an entry; unmapped types default to `"COMPOSITION"`, matching `revision.ts`'s own fallback in `targetLayer()`) rather than inventing unread object-type strings for the other modules.

---

## 2. Problem, User Outcome, Solution, and Scope

### Problem without this spec

Once a Campaign Order exists and the Pipeline is executing it (Wave 2's other specs), an operator has no way to see what is happening, correct it, or ship it. The entire supervisory surface described in `CA_PROJECT_SNAPSHOT_V2.md` Section 2 ("Operator reviews in Control Tower... exception queue... natural language revision... Human Resolution Episodes... Ship gate") is fully modeled as pure, tested TypeScript in `07_CONSCIOUS_ACTIVATIONS_STUDIO`, but that code has never been run by anything other than its own CLI's `demo` command. There is no HTTP door into it, and — because it is Node.js, not Python — the FastAPI gateway cannot simply `import` it the way it imports `cmf_pipeline` or `interview_expression`. Gates E and F in `CA_APP_FR_EPIC_SPEC_PLAN.md` Part 7 ("a natural language revision compiles and executes," "ship gate produces signed audit export") cannot pass.

### User outcome

An operator (today: a developer exercising the API directly; later: `TS-APP-UI-003`'s Control Tower page) can `GET` a single JSON projection of everything about a running campaign, request a plain-language or direct-manipulation change and see it compiled into an exact, bounded, auditable operation before anything executes, confirm that operation and have it execute with a recorded `HumanResolutionEpisode`, see and resolve blocked jobs in an exception queue, and — once the campaign is ready — request a ship decision that is denied or authorized against six independent, named conditions and produces a signed audit-export manifest on success.

### Solution

Two new pieces of infrastructure, plus three routers built on top of them:

1. **`services/studio/src/rpc.ts`** (new file, added to the existing Node package) — a stdin/stdout JSON command dispatcher over the pure functions already in `controlTower.ts`, `timeline.ts`, `revision.ts`, `rerun.ts`, `resolutions.ts`, `ship.ts`, `auditExport.ts`, `surfaces.ts`, and `campaign.ts`. No business logic is added or changed; this file only routes a JSON envelope to an existing exported function and serializes the result.
2. **`api/services/studio_bridge.py`** (new) — spawns `node services/studio/dist/rpc.js <command>` per call, writes the JSON payload to stdin, parses the `{ok, result}` / `{ok: false, error}` envelope from stdout, and raises typed Python exceptions the routers translate to HTTP.
3. **`api/services/campaign_projection.py`** (new) — reads and advances `CampaignOrder`/`CampaignState` via `PipelineApplication.repository`, per the convention in Section 3 (Source gap notice 2).
4. **`api/routers/campaigns.py`** (supervision routes added to the router TS-APP-API-004 will also own), **`api/routers/revisions.py`**, **`api/routers/ship.py`** — the eight HTTP endpoints in Section 6.

### In scope

- `GET /api/campaigns/{campaign_id}/tower` — `FR-APP-060`
- `GET /api/campaigns/{campaign_id}/timeline` — `FR-APP-061`
- `POST /api/campaigns/{campaign_id}/revisions` — compile only — `FR-APP-062`
- `POST /api/campaigns/{campaign_id}/revisions/{program_id}/execute` — confirm and execute — `FR-APP-062`
- `GET /api/campaigns/{campaign_id}/exceptions` — `FR-APP-063`
- `POST /api/campaigns/{campaign_id}/exceptions/{package_id}/resolve` — `FR-APP-063`
- `POST /api/campaigns/{campaign_id}/ship` — `FR-APP-064`
- `GET /api/campaigns/{campaign_id}/audit-export` — `FR-APP-064` (retrieval half of the ship gate's audit trail)
- `services/studio/src/rpc.ts` — the RPC bridge entrypoint
- `api/services/studio_bridge.py`, `api/services/campaign_projection.py`
- `api/schemas/supervision.py`
- Stage 0 corrective patch to `infra/docker/dockerfile.api` and `api/main.py` (Node.js runtime, `studio_bridge` app-state wiring)

### Out of scope

- Campaign **creation** (`POST /api/campaigns`), listing, and the `ContentBatchService` reconciliation — `TS-APP-API-004`, not written yet. This spec only reads and advances an already-existing `CampaignOrder`/`CampaignState` pair (or, in its own tests, creates fixture ones directly against the Section 3 convention).
- WebSocket/SSE live status push — `TS-APP-API-005`, not written yet. All endpoints here are synchronous request/response.
- `ProgrammingMaterialIndex` retrieval (`resolutions.ts`'s in-memory query index) — it has no persistence and requires a long-lived process to be useful; out of scope until a future spec makes the bridge a persistent worker instead of a per-call subprocess (see Section 8).
- Direct-manipulation UI (drag BBOX, trim source span) — this spec exposes the `POST /revisions` endpoint's `direct_manipulation` request mode, which is sufficient for `TS-APP-UI-003` to wire a drag handler to later; the drag interaction itself is a React concern.
- Real repair execution — `POST /exceptions/{id}/resolve` with `decision: "REQUEST_REVISION"` on a pipeline-repairable exception calls `BoundedRepairService.plan()` (already real) but does **not** call `BoundedRepairService`'s execution path (there isn't one — `plan()` only stores a `bounded_repair_plan` object; nothing consumes it yet). This spec surfaces the plan; a future spec must wire its actual re-render/re-render.
- Wiring `ProgrammingMaterialIndex` or `HumanResolutionLedger` retrieval into any AIR/Pipeline retrieval path — the ledger is written for audit purposes only in this spec.

---

## 3. Governing Decisions and Constraints

**The Studio bridge is a per-call Node subprocess, not a persistent worker.** Every one of this spec's endpoints spawns `node services/studio/dist/rpc.js <command>`, writes one JSON object to stdin, and reads one JSON object from stdout. Cold-start Node overhead (tens of milliseconds) is acceptable because every caller of this API is a human reviewing one campaign at a time — this is not a hot path. A persistent worker pool (long-lived Node process, newline-delimited JSON protocol) is the obvious next optimization but is explicitly deferred (Section 8) rather than built speculatively here.

**Campaign persistence reuses `PipelineRepository.store_object`/`get_object` — no new storage technology.** `CampaignOrder` is stored once, immutably, as `object_type="studio_campaign_order"`, `object_id=f"studio-campaign-order:{campaign_id}"`. `CampaignState` is stored as `object_type="studio_campaign_state"`, `object_id=f"studio-campaign-state:{campaign_id}"`, and every lifecycle transition is a new `store_object()` call with `expected_revision` set to the current revision — `PipelineRepository`'s own optimistic-concurrency check (`PipelineConflict` on mismatch) does the same job as `CampaignState.version`/`expected_state_version` inside Studio's own validators, so the two layers of version-checking (Studio's pure-function check, the repository's storage-level check) are complementary, not redundant: Studio's check catches a stale client; the repository's check catches a stale *server-side* read between this spec's own read-then-write steps.

**Revision compile and execute are two separate HTTP calls.** `ST-APP-08.04`'s acceptance text requires "confirmation display of compiled `ChangeRequestProgram` before execution." `POST /revisions` only compiles and persists the program (`object_type="studio_change_request_program"`); nothing executes and no `HumanResolutionEpisode` is written. `POST /revisions/{program_id}/execute` re-fetches the persisted program by ID (never trusts a client-resubmitted program body — a compiled program is looked up, not re-parsed), re-validates its `expected_state_version` against the *current* campaign state (which may have moved since compile time), computes the selective rerun, writes the `HumanResolutionEpisode`, and advances `CampaignState`.

**Exceptions are `FAILED` run nodes, diagnosed through `BoundedRepairService.diagnose()`, projected through `buildExceptionReviewPackage()`.** There is no other "exception" concept anywhere in the Python codebase (Source gap notice 4). `GET /exceptions` walks `pipeline.runs.status(run_id)["nodes"]`, filters to `state == "FAILED"`, and for each failed node calls `BoundedRepairService.diagnose([node["failure"]])` to get `responsible_layer`/`repairable_by_pipeline`, then calls the Studio bridge's `build-exception-review-package` command to produce the typed `ExceptionReviewPackage`. `allowed_decisions` includes `"REQUEST_REVISION"` only when `repairable_by_pipeline` is true; otherwise only `"REJECT"` is offered (matching `buildExceptionReviewPackage`'s own default, narrowed).

**No float, no `undefined`, sorted keys — this spec's Python code must produce bridge payloads that satisfy Studio's own `canonical.ts` normalizer.** Every integer field (`budget_units`, `bytes`, `start_frame`, timestamps in ms) is passed as a Python `int`, never `float`. Every optional field the TypeScript interfaces declare as `T | null` is passed as JSON `null`, never omitted (`normalize()` in `canonical.ts` throws on `undefined`, and Python's `json.dumps` silently omits keys whose value is a sentinel unless the Pydantic model explicitly sets `exclude_none=False` — this spec's Pydantic `model_dump(mode="json")` calls always pass `exclude_none=False` for any payload destined for the bridge).

**Claim ceiling:** `CONTROL_TOWER_SUPERVISION_API_DEVELOPMENT_EVIDENCE`. This spec does not claim: that any repair plan it surfaces actually re-executes anything (Source gap notice / Out of scope above); that the Node bridge is production-latency-appropriate (Section 8); that `wrong_reading_locks` sourcing is correct (Source gap notice 5); or that this spec's `CampaignOrder`/`CampaignState` persistence convention is the one TS-APP-API-004 will ultimately adopt (Source gap notice 2) — it is this spec's best-effort, fully-functional placeholder, not an authority.

---

## 4. Current Brownfield Architecture

| Component | Path | Actual behaviour | Disposition | Reason |
|---|---|---|---|---|
| `buildControlTowerProjection`, `projectVideoEditProgram`, `compileNaturalLanguageRevision`, `compileDirectManipulation`, `compileSelectiveRerun`, `createHumanResolutionEpisode`, `evaluateShipRequest`, `buildAuditExportManifest`, `routeHarnessToSurfaces`, `buildExceptionReviewPackage`, `transitionCampaign` | `services/studio/src/*.ts` | Pure, tested, deterministic functions; zero HTTP surface | REUSE (via new RPC entrypoint) | Exactly the logic every endpoint in this spec needs; none of it is rewritten |
| `HumanResolutionLedger` | `services/studio/src/resolutions.ts` | File-backed, hash-chained JSONL ledger | REUSE (via RPC, new ledger path per campaign) | Already does exactly what an audit trail needs; not reimplemented in Python |
| `WorkflowRunService.status()` / `fail_node()` | `services/pipeline/src/cmf_pipeline/workflow/application/run_service.py` | Returns per-node state incl. stored `failure` | REUSE | Source of `RunNodeProjection` and `ExceptionReviewPackage` inputs (Section 5, 6) |
| `BoundedRepairService.diagnose()` / `.plan()` | `services/pipeline/src/cmf_pipeline/evaluation/repair.py` | Maps failure code → responsible layer; stores a repair plan object | REUSE (`diagnose` fully; `plan` surfaced, not executed) | Exact source of exception-package `responsible_product`/`recommended_next_actions` |
| `EvaluationService.evaluate()` | `services/pipeline/src/cmf_pipeline/evaluation/service.py` | Stores `independent_evaluation_receipt` with `verdict` | REUSE (read-only, via `list_objects`) | Source of `ControlTowerProjection.evaluations` and `ShipRequest.evaluation_refs` |
| `VideoEditProgramService.projection()` | `services/pipeline/src/cmf_pipeline/media/program.py` | Returns program ref + canvas + tracks, read-only | REUSE | Direct input to `project-video-edit-program` bridge call |
| `PipelineRepository.store_object`/`get_object`/`list_objects` | `services/pipeline/src/cmf_pipeline/workflow/infrastructure/repository.py` | Generic, content-addressed, revisioned object store with optimistic concurrency | REUSE (for Campaign, compiled-program, and exception-decision persistence — new object types, same mechanism) | Avoids inventing new storage; Section 3 |
| `ContentBatchService.compile_batch()` | `services/pipeline/src/cmf_pipeline/batch/service.py` | Produces `source_backed_content_batch`, structurally unrelated to `CampaignOrder`/`CampaignState` | **FLAG — NOT RECONCILED** | Source gap notice 2. Not called by this spec. Documented as the open question for TS-APP-API-004 |
| `services/studio/src/index.ts` `main()` | `services/studio/src/index.ts` | CLI with `health`/`demo` only | UNCHANGED | This spec adds a sibling entrypoint (`rpc.ts`), does not modify `index.ts`'s CLI |
| `infra/docker/dockerfile.api` (from TS-APP-API-001) | `infra/docker/dockerfile.api` | `FROM python:3.12-slim`, no Node.js, never copies `services/studio` | **DEFECT — PATCH IN THIS SPEC** | Source gap notice 3; corrected in §7 Stage 0 |
| `api/main.py` lifespan (from TS-APP-API-001) | `api/main.py` | Wires `pipeline`/`air`/`vae`/`interview`/`builder` into `app.state`; no `studio_bridge` | **PATCH IN THIS SPEC** | §7 Stage 0 |

---

## 5. Proposed Architecture and Workflows

### The RPC bridge protocol

```
Python (api/services/studio_bridge.py)                Node (services/studio/dist/rpc.js)
  subprocess.run(
    ["node", rpc_entrypoint, "<command>"],
    input=json.dumps(payload).encode(),
    capture_output=True,
  )
      stdin  --> JSON payload, one object, matching the command's expected shape
      stdout <-- {"ok": true, "result": <json>}                    exit 0
             <-- {"ok": false, "error": {"code","message","context"}}  exit 0
      stderr <-- stack trace, on an *unexpected* crash                exit 1 (StudioBridgeCrash)
```

`StudioValidationError` thrown inside the pure functions is always caught inside `rpc.ts` and returned as `{ok: false, error}` with **exit 0** — a validation failure is an ordinary, well-formed answer, not a process crash. Only a genuinely unexpected exception (a bug) exits 1 and is surfaced to the caller as `INTERNAL_ERROR`.

### Control Tower assembly — `GET /api/campaigns/{campaign_id}/tower`

```
1. load_campaign(pipeline, campaign_id) → {order, state}         [404 CAMPAIGN_NOT_FOUND if absent]
2. run_id = state["run_refs"][-1]["object_id"] if state["run_refs"] else None
3. run_status = pipeline.runs.status(run_id) if run_id else None
4. run_nodes = [map_node_projection(n, run_status) for n in run_status["nodes"]]   (Node-state mapping table below)
5. failed = [n for n in run_status["nodes"] if n["state"] == "FAILED"]
   exception_packages = [assemble_exception_package(n, order, state) for n in failed]
       (calls BoundedRepairService.diagnose, then bridge "build-exception-review-package")
6. evaluations = pipeline.repository.list_objects(object_type="independent_evaluation_receipt")
       filtered to those whose artifact_ref matches an artifact in state["artifact_refs"]
7. timeline = project_timeline(campaign_id) if a video_edit_program ref is bound to this campaign, else None
       (same logic as the standalone /timeline endpoint, Section 5 next)
8. studio_binding = bridge.call("route-harness-to-surfaces", {harness_ref: order["harness_ref"],
       category_id: order["category_id"], output_targets: order["output_targets"]})
       (recomputed every call — pure and cheap; not persisted, since TS-APP-API-004 does not exist to
       persist it yet)
9. knowledge = KnowledgeProjection assembled from pipeline.skills / pipeline.retrieval — see Section 6
       for the (partial, best-effort) field-by-field sourcing
10. projection = bridge.call("build-control-tower-projection", ControlTowerInput{...})
11. 200 OK, ControlTowerProjectionModel
```

### Node-state mapping table (Source gap notice 4)

| Python `NodeState` | Node `NodeKind` | → Studio `RunNodeProjection.status` | Notes |
|---|---|---|---|
| `BLOCKED` | any | `PENDING` | Not yet ready to dispatch |
| `READY` | `HUMAN_GATE` | `WAITING_HUMAN` | Ready, but the node itself is a human gate |
| `READY` | anything else | `READY` | |
| `DISPATCHED` | `HUMAN_GATE` | `WAITING_HUMAN` | JIT capsule prepared for a human actor |
| `DISPATCHED` | anything else | `RUNNING` | Closest analog — work has been handed off |
| `RUNNING` | any | `RUNNING` | |
| `SUCCEEDED` | any | `SUCCEEDED` | |
| `FAILED` | any | `FAILED` | Source of `ExceptionReviewPackage` (below) |
| `CANCELLED` | any | `CANCELLED` | |
| `INVALIDATED` | any | `INVALIDATED` | |
| `QUARANTINED` | any | `FAILED` | Blocker code `LATE_RESULT_QUARANTINED_NOT_CONSUMABLE` appended; **not** treated as a human-review exception — it is a scheduling artifact, not a content problem |

### Exception package assembly

```
node.failure  (TypedFailure-shaped: {code, message, evidence_refs, next_action,
               responsible_product, retry_class})
  → diagnosis = pipeline.repairs.diagnose([node.failure])["diagnoses"][0]
  → allowed_decisions = ["REQUEST_REVISION", "REJECT"] if diagnosis["repairable_by_pipeline"]
                         else ["REJECT"]
  → recommended_next_actions =
        [a for a in ALLOWED_ACTIONS_FOR_LAYER[diagnosis["responsible_layer"]]]
        (a small static map from responsible_layer → the subset of
         BoundedRepairService.ALLOWED_ACTIONS that layer can perform; RUNTIME and
         PIPELINE_COMPOSITION map to the five non-escalation actions, every other
         layer maps to just ["ESCALATE_OWNER"])
  → bridge.call("build-exception-review-package", {
        campaign_ref, exception_code: node.failure.code,
        responsible_product: diagnosis["responsible_layer"],
        summary: node.failure.message,
        evidence_refs: node.failure.evidence_refs,
        candidate_refs: [], allowed_decisions, recommended_next_actions,
    }) → ExceptionReviewPackage
```

### Timeline projection — `GET /api/campaigns/{campaign_id}/timeline`

```
1. load_campaign → order, state
2. program_ref = find the video_edit_program object bound to this campaign
       (via pipeline.repository — an edge from a run node's output_ref of object_type
        "video_edit_program" to this campaign's run; see Section 6 for the exact
        lookup this spec implements)
       none found → 404 TIMELINE_NOT_AVAILABLE (nothing has been compiled yet)
3. projection_payload = pipeline.video_programs.projection(program_ref.object_id)
       → {program_ref, canvas, tracks, read_only}
4. timeline = bridge.call("project-video-edit-program", {
       program_id: program_ref.object_id, program_sha256: program_ref.sha256,
       canvas: projection_payload["canvas"], tracks: projection_payload["tracks"],
   })
5. 200 OK, TimelineProjectionModel
```

### Revision compile — `POST /api/campaigns/{campaign_id}/revisions`

```
1. load_campaign → order, state    [404 if absent; 409 CAMPAIGN_NOT_RUNNING unless
   state.lifecycle_state in {RUNNING, AWAITING_REVIEW, BLOCKED_EXCEPTION}]
2. context = assemble_revision_context(pipeline, order, state)   (Section 6)
3. mode == "natural_language":
       program = bridge.call("compile-natural-language-revision", {
           request: {...OperatorRevisionRequest fields, expected_state_version: state["version"]},
           context,
       })
   mode == "direct_manipulation":
       program = bridge.call("compile-direct-manipulation", {delta: {...}, context})
4. pipeline.repository.store_object("studio_change_request_program", program,
       idempotency_key=f"revision-compile:{program['program_id']}",
       object_id=f"studio-change-request-program:{program['program_id']}")
5. 200 OK, ChangeRequestProgramModel  (compilation_status may be COMPILED, NEEDS_CLARIFICATION,
   or DENIED — all three are 200 responses; the *status field*, not the HTTP code, tells the
   caller what happened, matching AC-004/AC-005 in Section 9)
```

### Revision execute — `POST /api/campaigns/{campaign_id}/revisions/{program_id}/execute`

```
1. load_campaign → order, state
2. stored = pipeline.repository.get_object(f"studio-change-request-program:{program_id}")
       [404 REVISION_NOT_FOUND if absent]
   program = stored["payload"]
   [409 PROGRAM_NOT_COMPILED if program["compilation_status"] != "COMPILED"]
3. [409 STALE_STATE_VERSION if program["expected_state_version"] != state["version"] —
    the campaign moved since this program was compiled; caller must recompile]
4. graph = build_dependency_graph_nodes(pipeline, state)   (from pipeline.graph, Section 6)
5. rerun = bridge.call("compile-selective-rerun", {
       run_ref: state["run_refs"][-1], program, graph,
       evaluation_node_ids: [n["node_id"] for n in run_status["nodes"]
                              if n["node_id"] in graph_evaluation_node_ids],
   })
6. episode_result = bridge.call("create-human-resolution-episode", {
       episode: {..HumanResolutionInput fields.., accepted: True, resolution_kind:
           "revision_request" if program["source_kind"] == "NATURAL_LANGUAGE"
           else "manual_parameter_change" if ... else "manual_timeline_change",
           program},
       ledger_path: f"{CA_DATA_ROOT}/studio/resolutions/{campaign_id}.ndjson",
   })
7. new_state = bridge.call("transition-campaign", {
       state, next: "AWAITING_REVIEW" if <autonomy policy says interrupt> else "RUNNING",
       updates: {},
   })
   save_campaign_state(pipeline, campaign_id, new_state, idempotency_key=...)
8. 200 OK, {"campaign": new_state, "rerun": rerun, "episode": episode_result["episode"]}
```

*Actual node re-execution is out of scope (Section 2) — `rerun.rerun_node_ids` tells the caller which nodes the Pipeline's scheduler must re-dispatch; wiring that dispatch belongs to `TS-APP-API-005`/Wave 2's run-service integration, since `WorkflowRunService` already has `dispatch_node`/`start_node`/`complete_node` primitives this spec does not call.*

### Exception resolve — `POST /api/campaigns/{campaign_id}/exceptions/{package_id}/resolve`

```
1. load_campaign, locate the FAILED node whose exception package_id matches
       [404 EXCEPTION_NOT_FOUND]
2. decision in {"REQUEST_REVISION", "REJECT"}   [400 DECISION_NOT_ALLOWED if not in the
   package's allowed_decisions]
3. decision == "REQUEST_REVISION" (only reachable when repairable_by_pipeline):
       repair_plan = pipeline.repairs.plan(target_ref=node.output_ref or node ref,
           diagnosis=diagnosis, action=<first ALLOWED_ACTIONS_FOR_LAYER entry>,
           parameters={}, preserved_refs=[], attempt_number=1, maximum_attempts=3,
           idempotency_key=...)
       next_state = "RUNNING"  (repair plan stored; execution wiring is out of scope, Section 2)
   decision == "REJECT":
       repair_plan = None
       next_state = "BLOCKED_EXCEPTION"   (stays blocked; a human must intervene outside this API)
4. episode = bridge.call("create-human-resolution-episode", {episode: {...,
       resolution_kind: "escalation_resolution", accepted: decision == "REQUEST_REVISION", ...},
       ledger_path: ...})
5. new_state = bridge.call("transition-campaign", {state, next: next_state, updates:
       {exception_ids: [x for x in state["exception_ids"] if x != package_id]}})
   save_campaign_state(...)
6. 200 OK, {"campaign": new_state, "episode": episode["episode"], "repair_plan": repair_plan}
```

### Ship — `POST /api/campaigns/{campaign_id}/ship`

```
1. load_campaign → order, state   [409 unless state.lifecycle_state == "READY_TO_SHIP" —
   note evaluateShipRequest *also* checks this and would DENY rather than error, but this
   spec fails fast with 409 rather than paying for a bridge round trip on an obviously
   wrong-state request; AC-013 covers the case where lifecycle_state is READY_TO_SHIP but
   the request is still denied for one of the other five reasons]
2. decision = bridge.call("evaluate-ship-request", {
       request: {...ShipRequestInput fields, campaign_ref, autonomy_mode: state["autonomy_mode"],
           artifact_refs: state["artifact_refs"], evaluation_refs: state["evaluation_refs"],
           unresolved_exception_ids: state["exception_ids"]},
       campaign: state,
   })
3. decision.status == "DENIED" → 200 OK, ShipDecisionModel  (denial is a successful answer,
   not an HTTP error — mirrors TS-APP-API-002's eligibility-endpoint convention)
4. decision.status == "AUTHORIZED":
       new_state = bridge.call("transition-campaign", {state, next: "SHIPPED", updates: {}})
       save_campaign_state(...)
       manifest = bridge.call("write-audit-export", {
           manifest_input: {campaign_ref, source_refs: [order["source_ref"]],
               semantic_refs: [r for r in [order.get("harness_ref")] if r],
               run_refs: state["run_refs"], artifact_refs: state["artifact_refs"],
               evaluation_refs: state["evaluation_refs"], command_refs: [], receipt_refs: [],
               human_resolution_refs: <every episode ref recorded for this campaign,
                   read back from the ledger via a "list" pass — see Section 6>,
               ship_decision: decision,
               replay_instructions: ["Replay via `python -m cmf_pipeline replay --run <run_id>`"]},
           path: f"{CA_DATA_ROOT}/studio/audit-exports/{campaign_id}.json",
       })
       200 OK, ShipDecisionModel
```

### Audit export retrieval — `GET /api/campaigns/{campaign_id}/audit-export`

```
1. load_campaign  [404 if absent]
2. [404 AUDIT_EXPORT_NOT_AVAILABLE unless state.lifecycle_state == "SHIPPED"]
3. read f"{CA_DATA_ROOT}/studio/audit-exports/{campaign_id}.json" from disk, parse, return
4. 200 OK, AuditExportManifestModel
```

---

## 6. Data Models, Contracts, Schemas, and APIs

### `api/schemas/supervision.py`

```python
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel

class RefModel(BaseModel):
    object_id: str
    version: str
    sha256: str

class ArtifactRefModel(BaseModel):
    artifact_id: str
    artifact_kind: str
    bytes: int
    media_type: str
    sha256: str
    uri: str

class ActorRefModel(BaseModel):
    actor_id: str
    actor_type: Literal["deterministic_module", "model_program", "human"]
    product_id: str
    workflow_role: Literal["hunter", "analyst", "composer", "commander", "evaluator", "operator"]

# --- Control Tower ---

class RunNodeProjectionModel(BaseModel):
    node_id: str
    node_type: str
    title: str
    status: Literal["PENDING", "READY", "RUNNING", "WAITING_HUMAN", "SUCCEEDED", "FAILED", "CANCELLED", "INVALIDATED"]
    owner_product: str
    dependency_ids: list[str]
    artifact_refs: list[ArtifactRefModel]
    receipt_refs: list[RefModel]
    blocker_codes: list[str]

class ExceptionReviewPackageModel(BaseModel):
    package_id: str
    campaign_ref: RefModel
    exception_code: str
    responsible_product: str
    summary: str
    evidence_refs: list[RefModel]
    candidate_refs: list[RefModel]
    allowed_decisions: list[Literal["APPROVE", "REJECT", "REQUEST_REVISION", "SELECT_CANDIDATE", "SHIP"]]
    recommended_next_actions: list[str]

class TimelineItemModel(BaseModel):
    item_id: str
    track_id: str
    kind: str
    role: str
    start_frame: int
    end_frame: int
    source_start_ms: int | None
    source_end_ms: int | None
    source_ref: RefModel | None
    artifact_ref: ArtifactRefModel | None
    editable_operations: list[str]

class TimelineTrackModel(BaseModel):
    track_id: str
    track_type: str
    role: str
    z_index: int
    item_ids: list[str]

class TimelineProjectionModel(BaseModel):
    projection_id: str
    video_edit_program_ref: RefModel
    state: Literal["READ_ONLY_CANONICAL_PROGRAM_PROJECTION"]
    width: int
    height: int
    fps_numerator: int
    fps_denominator: int
    duration_frames: int
    tracks: list[TimelineTrackModel]
    items: list[TimelineItemModel]

class ControlTowerProjectionModel(BaseModel):
    projection_id: str
    campaign: dict          # CampaignState — passthrough; see Section 3 persistence note
    order: dict             # CampaignOrder — passthrough
    studio_binding: dict
    source_package_ref: RefModel
    observed_activative_pack_ref: RefModel | None
    semantic_production_package_ref: RefModel | None
    final_script_ref: RefModel | None
    activation_transfer_contract_ref: RefModel | None
    run_nodes: list[RunNodeProjectionModel]
    artifacts: list[ArtifactRefModel]
    evaluations: list[RefModel]
    knowledge: dict
    runtime_health: list[dict]
    timeline: TimelineProjectionModel | None
    exception_packages: list[ExceptionReviewPackageModel]
    available_actions: list[str]
    projection_sha256: str

# --- Revisions ---

class NaturalLanguageRevisionInput(BaseModel):
    mode: Literal["natural_language"]
    target_refs: list[RefModel]
    target_node_ids: list[str]
    category_id: str
    natural_language_request: str
    current_state_ref: RefModel
    evaluation_ref: RefModel | None = None

class DirectManipulationInput(BaseModel):
    mode: Literal["direct_manipulation"]
    target_ref: RefModel
    target_node_id: str
    manipulation_type: Literal["MOVE_BBOX", "RESIZE_BBOX", "TRIM_SEGMENT", "REORDER_ITEM", "EDIT_TEXT", "SET_PARAMETER", "SELECT_CANDIDATE"]
    arguments: dict[str, str | int | bool]
    current_state_ref: RefModel

class RevisionRequestInput(BaseModel):
    revision: NaturalLanguageRevisionInput | DirectManipulationInput
    operator_actor: ActorRefModel

class ChangeOperationModel(BaseModel):
    operation_id: str
    target_ref: RefModel
    target_node_id: str
    target_layer: str
    tool_id: str
    tool_version: str
    arguments: dict[str, str | int | bool]
    preconditions: list[str]
    expected_effect: str

class ChangeRequestProgramModel(BaseModel):
    program_id: str
    compilation_status: Literal["COMPILED", "NEEDS_CLARIFICATION", "DENIED"]
    request_ref: RefModel
    interpretation: str
    target_layer_or_nodes: list[str]
    exact_operations: list[ChangeOperationModel]
    declared_invariants: list[str]
    required_transformations: list[str]
    creative_degrees_of_freedom: list[str]
    invalidated_downstream_nodes: list[str]
    validation_plan: list[str]
    preview_required: bool
    confidence_micros: int
    escalation: str | None
    source_kind: Literal["NATURAL_LANGUAGE", "DIRECT_MANIPULATION"]
    expected_state_version: int
    program_sha256: str

class ExecuteRevisionResponse(BaseModel):
    campaign: dict
    rerun: dict
    episode: dict

# --- Exceptions ---

class ResolveExceptionInput(BaseModel):
    decision: Literal["REQUEST_REVISION", "REJECT"]
    operator_actor: ActorRefModel
    notes: str | None = None

class ResolveExceptionResponse(BaseModel):
    campaign: dict
    episode: dict
    repair_plan: dict | None

# --- Ship ---

class ShipRequestInput(BaseModel):
    ship_request_id: str
    target_channel: str
    publication_authority_ref: RefModel | None
    publication_policy_ref: RefModel | None
    operator_actor: ActorRefModel

class ShipDecisionModel(BaseModel):
    decision_id: str
    request_ref: RefModel
    status: Literal["AUTHORIZED", "DENIED"]
    denial_codes: list[str]
    authorized_artifact_refs: list[ArtifactRefModel]
    acknowledgement_required: bool
    decision_actor: ActorRefModel
    decision_sha256: str

class AuditExportManifestModel(BaseModel):
    export_id: str
    campaign_ref: RefModel
    source_refs: list[RefModel]
    semantic_refs: list[RefModel]
    run_refs: list[RefModel]
    artifact_refs: list[ArtifactRefModel]
    evaluation_refs: list[RefModel]
    command_refs: list[RefModel]
    receipt_refs: list[RefModel]
    human_resolution_refs: list[RefModel]
    ship_decision_ref: RefModel | None
    replay_instructions: list[str]
    export_sha256: str
```

Note: `campaign`/`order`/`studio_binding`/`knowledge`/`runtime_health` are left as untyped `dict` passthrough rather than fully-typed Pydantic models. This is a deliberate, narrow exception to this spec's otherwise-strict typing: `CampaignOrder`/`CampaignState`'s authoritative shape is Studio's `domain.ts` (Section 1), and duplicating all 20+ of their fields into a third schema copy (TypeScript → this spec's Pydantic → whatever TS-APP-API-004 eventually defines) creates exactly the kind of drift Source gap notice 2 already flags as unresolved. Passthrough keeps this spec from asserting a shape it does not own.

### `OBJECT_TYPE_TO_TARGET_LAYER` (Source gap notice 6)

```python
OBJECT_TYPE_TO_TARGET_LAYER: dict[str, str] = {
    "video_edit_program": "VIDEO_EDIT_PROGRAM",
    # Extend here as other modules' object types are confirmed by their owning specs.
    # Unmapped object types default to "COMPOSITION", matching revision.ts's own
    # targetLayer() fallback — this is intentional parity, not a placeholder bug.
}
```

### `ALLOWED_ACTIONS_FOR_LAYER` (exception recommended-actions mapping)

```python
from cmf_pipeline.evaluation.repair import ALLOWED_ACTIONS  # {'SHIFT_BBOX', 'REDUCE_FONT_SIZE',
                                                              #  'ADD_AUDIO_FADE', 'SHIFT_CUT_TO_WORD_BOUNDARY',
                                                              #  'RERENDER_RUNTIME', 'ESCALATE_OWNER'}

ALLOWED_ACTIONS_FOR_LAYER: dict[str, list[str]] = {
    "RUNTIME": sorted(ALLOWED_ACTIONS - {"ESCALATE_OWNER"}),
    "PIPELINE_COMPOSITION": sorted(ALLOWED_ACTIONS - {"ESCALATE_OWNER"}),
    # every other responsible_layer (INTERVIEW_EXPRESSION, ACTIVATIVE_INTELLIGENCE_RUNTIME,
    # VISUAL_ASSET_EDITOR, INDEPENDENT_EVALUATION, UNKNOWN_REQUIRES_TRIAGE) is not repairable
    # by the Pipeline; the default (see get()) is ["ESCALATE_OWNER"]
}
```

### Endpoints defined in this spec

| Method | Path | Response | Notes |
|---|---|---|---|
| `GET` | `/api/campaigns/{campaign_id}/tower` | `ControlTowerProjectionModel` (200) | |
| `GET` | `/api/campaigns/{campaign_id}/timeline` | `TimelineProjectionModel` (200) | 404 if no program bound yet |
| `POST` | `/api/campaigns/{campaign_id}/revisions` | `ChangeRequestProgramModel` (200) | Compile only; 200 even for `NEEDS_CLARIFICATION`/`DENIED` |
| `POST` | `/api/campaigns/{campaign_id}/revisions/{program_id}/execute` | `ExecuteRevisionResponse` (200) | |
| `GET` | `/api/campaigns/{campaign_id}/exceptions` | `list[ExceptionReviewPackageModel]` (200) | Empty list, not 404, when none |
| `POST` | `/api/campaigns/{campaign_id}/exceptions/{package_id}/resolve` | `ResolveExceptionResponse` (200) | |
| `POST` | `/api/campaigns/{campaign_id}/ship` | `ShipDecisionModel` (200) | 200 for both `AUTHORIZED` and `DENIED` |
| `GET` | `/api/campaigns/{campaign_id}/audit-export` | `AuditExportManifestModel` (200) | 404 until `SHIPPED` |

### Error code → HTTP status mapping used by these routers

| Error code | HTTP status | Notes |
|---|---|---|
| `CAMPAIGN_NOT_FOUND` | 404 | No `studio_campaign_state` object for this `campaign_id` |
| `CAMPAIGN_NOT_RUNNING` | 409 | Revision requested against a campaign not in `{RUNNING, AWAITING_REVIEW, BLOCKED_EXCEPTION}` |
| `TIMELINE_NOT_AVAILABLE` | 404 | No `video_edit_program` bound to this campaign yet |
| `REVISION_NOT_FOUND` | 404 | `program_id` not in the store |
| `PROGRAM_NOT_COMPILED` | 409 | Attempting to execute a `NEEDS_CLARIFICATION`/`DENIED` program |
| `STALE_STATE_VERSION` | 409 | Campaign advanced since this program was compiled — recompile |
| `EXCEPTION_NOT_FOUND` | 404 | `package_id` does not match any current `FAILED` node |
| `DECISION_NOT_ALLOWED` | 400 | `decision` not in the package's `allowed_decisions` |
| `SHIP_NOT_READY` | 409 | `lifecycle_state != READY_TO_SHIP` (fast-fail before the bridge call) |
| `AUDIT_EXPORT_NOT_AVAILABLE` | 404 | Campaign not yet `SHIPPED` |
| Any `StudioValidationError.code` surfaced from the bridge (e.g. `STALE_STATE_VERSION`, `TARGET_REQUIRED`, `TOOL_NOT_ALLOWED`, `NODE_SCOPE_DENIED`, `PROGRAM_NOT_MINIMAL`) | 422 | Passed through verbatim as `error_code`; these are Studio's own domain validation codes, not reclassified |
| `StudioBridgeCrash` (Node process exited non-zero) | 500 | `INTERNAL_ERROR` — a bug in the bridge or Studio package |
| `PipelineConflict` (from `save_campaign_state`) | 409 | Another writer advanced the campaign between this request's read and write |
| `PipelineNotFound` | 404 | Unmapped node/run/object lookups inside `cmf_pipeline` |

---

## 7. Implementation Stages and Exact Target Paths

All paths are relative to the repository root after the directory restructure in `CA_APP_FR_EPIC_SPEC_PLAN.md` Part 5.

### Stage 0 — Corrective patch to TS-APP-API-001 output (Source gap notice 3)

**`infra/docker/dockerfile.api`** — add Node.js and build the Studio package:

```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y ffmpeg curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY packages/ca_contracts packages/ca_contracts
COPY packages/ca_runtime packages/ca_runtime
COPY packages/ca_delegation_rc4 packages/ca_delegation_rc4
COPY packages/ca_release packages/ca_release
COPY services/builder services/builder
COPY services/air services/air
COPY services/pipeline services/pipeline
COPY services/interview services/interview
COPY services/vae services/vae
COPY services/studio services/studio

RUN pip install --no-cache-dir \
    packages/ca_contracts packages/ca_runtime packages/ca_delegation_rc4 packages/ca_release \
    services/builder services/air services/pipeline services/interview services/vae \
    fastapi==0.115.0 uvicorn[standard]==0.30.0 python-multipart==0.0.9 pydantic==2.7.0

RUN cd services/studio && npm install && npm run build

COPY api api
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**`infra/docker/docker-compose.yml`** — add `CA_STUDIO_RPC_ENTRYPOINT` (optional override; default computed relative to `api/`, matching the `CA_DELEGATION_ROOT` default pattern TS-APP-API-001 already established):

```yaml
services:
  api:
    environment:
      CA_DATA_ROOT: /state
      CA_MEDIA_ROOT: /media
      CA_DELEGATION_ROOT: /app/packages/ca_delegation_rc4
      CA_STUDIO_RPC_ENTRYPOINT: /app/services/studio/dist/rpc.js
```

**`api/config.py`** — add one field:

```python
@dataclass(frozen=True)
class AppConfig:
    ca_data_root: Path
    ca_media_root: Path
    ca_delegation_root: Path
    ca_studio_rpc_entrypoint: Path      # NEW
    gateway_version: str = "0.1.0"

def load_config() -> AppConfig:
    data_root = Path(os.environ.get("CA_DATA_ROOT", "/state"))
    return AppConfig(
        ca_data_root=data_root,
        ca_media_root=Path(os.environ.get("CA_MEDIA_ROOT", data_root / "media")),
        ca_delegation_root=Path(os.environ.get("CA_DELEGATION_ROOT",
            Path(__file__).parent.parent / "packages" / "ca_delegation_rc4")),
        ca_studio_rpc_entrypoint=Path(os.environ.get("CA_STUDIO_RPC_ENTRYPOINT",
            Path(__file__).parent.parent / "services" / "studio" / "dist" / "rpc.js")),
    )
```

**`api/dependencies.py`** — add one dependency:

```python
from api.services.studio_bridge import StudioBridge

def get_studio_bridge(request: Request) -> StudioBridge:
    return request.app.state.studio_bridge
```

**`api/main.py`** — lifespan patch (inserted after the existing `builder` block, before `yield`):

```python
    # Studio bridge
    from api.services.studio_bridge import StudioBridge
    app.state.studio_bridge = StudioBridge(rpc_entrypoint=config.ca_studio_rpc_entrypoint)
```

and router registration (replacing the commented-out lines TS-APP-API-001 left):

```python
from api.routers import campaigns, revisions, ship
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])
app.include_router(revisions.router, prefix="/api/campaigns", tags=["revisions"])
app.include_router(ship.router, prefix="/api/campaigns", tags=["ship"])
```

### Stage 1 — Studio RPC bridge entrypoint

**`services/studio/src/rpc.ts`** (new file):

```typescript
import { readFileSync } from "node:fs";
import { buildControlTowerProjection, type ControlTowerInput } from "./controlTower.js";
import { projectVideoEditProgram, type VideoEditProgramInput } from "./timeline.js";
import { compileNaturalLanguageRevision, compileDirectManipulation, DEFAULT_STUDIO_TOOLS, type RevisionContext } from "./revision.js";
import { compileSelectiveRerun } from "./rerun.js";
import { createHumanResolutionEpisode, HumanResolutionLedger, type HumanResolutionInput } from "./resolutions.js";
import { evaluateShipRequest } from "./ship.js";
import { buildAuditExportManifest, writeAuditExport, type AuditExportInput } from "./auditExport.js";
import { routeHarnessToSurfaces } from "./surfaces.js";
import { buildExceptionReviewPackage, transitionCampaign } from "./campaign.js";
import { StudioValidationError } from "./validators.js";
import type {
  OperatorRevisionRequest, DirectManipulationDelta, CampaignState, CampaignLifecycleState,
} from "./domain.js";

type Envelope = { ok: true; result: unknown } | { ok: false; error: { code: string; message: string; context: unknown } };

function readStdin(): any {
  return JSON.parse(readFileSync(0, "utf8"));
}

function handle(command: string, input: any): unknown {
  switch (command) {
    case "list-default-tools":
      return DEFAULT_STUDIO_TOOLS;
    case "route-harness-to-surfaces":
      return routeHarnessToSurfaces(input);
    case "project-video-edit-program":
      return projectVideoEditProgram(input as VideoEditProgramInput);
    case "build-control-tower-projection":
      return buildControlTowerProjection(input as ControlTowerInput);
    case "compile-natural-language-revision":
      return compileNaturalLanguageRevision(input.request as OperatorRevisionRequest, input.context as RevisionContext);
    case "compile-direct-manipulation":
      return compileDirectManipulation(input.delta as DirectManipulationDelta, input.context as RevisionContext);
    case "compile-selective-rerun":
      return compileSelectiveRerun(input);
    case "create-human-resolution-episode": {
      const episode = createHumanResolutionEpisode(input.episode as HumanResolutionInput);
      const ledger = new HumanResolutionLedger(input.ledger_path as string);
      ledger.append(episode);
      return { episode, ledger_sha256: ledger.ledgerSha256() };
    }
    case "list-human-resolution-episodes": {
      const ledger = new HumanResolutionLedger(input.ledger_path as string);
      return { episodes: ledger.all() };
    }
    case "evaluate-ship-request":
      return evaluateShipRequest(input.request, input.campaign as CampaignState);
    case "build-audit-export-manifest":
      return buildAuditExportManifest(input as AuditExportInput);
    case "write-audit-export": {
      const manifest = buildAuditExportManifest(input.manifest_input as AuditExportInput);
      writeAuditExport(input.path as string, manifest);
      return manifest;
    }
    case "build-exception-review-package":
      return buildExceptionReviewPackage(input);
    case "transition-campaign":
      return transitionCampaign(input.state as CampaignState, input.next as CampaignLifecycleState, input.updates ?? {});
    default:
      throw new StudioValidationError("UNKNOWN_RPC_COMMAND", `unknown command: ${command}`);
  }
}

function main(): number {
  const command = process.argv[2];
  if (!command) {
    process.stderr.write("usage: rpc.js <command> < input.json\n");
    return 2;
  }
  try {
    const input = readStdin();
    const result = handle(command, input);
    const envelope: Envelope = { ok: true, result };
    process.stdout.write(JSON.stringify(envelope));
    return 0;
  } catch (error) {
    if (error instanceof StudioValidationError) {
      const envelope: Envelope = { ok: false, error: { code: error.code, message: error.message, context: error.context } };
      process.stdout.write(JSON.stringify(envelope));
      return 0;
    }
    process.stderr.write(error instanceof Error ? (error.stack ?? error.message) : String(error));
    return 1;
  }
}

process.exitCode = main();
```

`package.json` gains one script: `"rpc": "node dist/rpc.js"` (for manual/local invocation; the API calls `node dist/rpc.js <command>` directly, not through `npm run`).

### Stage 2 — Python bridge and campaign persistence

**`api/services/studio_bridge.py`** (new):

```python
from __future__ import annotations
import json
import subprocess
from pathlib import Path
from typing import Any

class StudioBridgeError(RuntimeError):
    """A well-formed StudioValidationError returned from the Node bridge."""
    def __init__(self, code: str, message: str, context: dict[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.context = context or {}

class StudioBridgeCrash(RuntimeError):
    """The Node process exited non-zero: a bug in the bridge or Studio package."""

class StudioBridge:
    def __init__(self, rpc_entrypoint: Path, node_binary: str = "node"):
        self.rpc_entrypoint = rpc_entrypoint
        self.node_binary = node_binary

    def call(self, command: str, payload: Any, *, timeout_seconds: float = 10.0) -> Any:
        process = subprocess.run(
            [self.node_binary, str(self.rpc_entrypoint), command],
            input=json.dumps(payload).encode("utf-8"),
            capture_output=True,
            timeout=timeout_seconds,
        )
        if process.returncode != 0:
            raise StudioBridgeCrash(
                f"studio rpc '{command}' crashed (exit {process.returncode}): "
                f"{process.stderr.decode('utf-8', errors='replace')[:2000]}"
            )
        envelope = json.loads(process.stdout.decode("utf-8"))
        if not envelope.get("ok"):
            error = envelope["error"]
            raise StudioBridgeError(error["code"], error["message"], error.get("context"))
        return envelope["result"]
```

**`api/services/campaign_projection.py`** (new — Source gap notice 2 / `ASSUMED_INTERFACE_PENDING_004`):

```python
from __future__ import annotations
from typing import Any
from cmf_pipeline.application import PipelineApplication
from cmf_pipeline.domain.errors import PipelineNotFound, PipelineConflict

CAMPAIGN_ORDER_TYPE = "studio_campaign_order"
CAMPAIGN_STATE_TYPE = "studio_campaign_state"

class CampaignNotFound(RuntimeError):
    pass

class CampaignStateConflict(RuntimeError):
    pass

def order_object_id(campaign_id: str) -> str:
    return f"studio-campaign-order:{campaign_id}"

def state_object_id(campaign_id: str) -> str:
    return f"studio-campaign-state:{campaign_id}"

def load_campaign(pipeline: PipelineApplication, campaign_id: str) -> dict[str, Any]:
    try:
        order = pipeline.repository.get_object(order_object_id(campaign_id))
        state = pipeline.repository.get_object(state_object_id(campaign_id))
    except PipelineNotFound as exc:
        raise CampaignNotFound(campaign_id) from exc
    return {"order": order["payload"], "state": state["payload"]}

def save_campaign_state(
    pipeline: PipelineApplication,
    campaign_id: str,
    state: dict[str, Any],
    *,
    idempotency_key: str,
) -> dict[str, Any]:
    """`state` must already carry the *next* version (Studio's own transitionCampaign()
    increments `version` before this is ever called). Fails with CampaignStateConflict if
    another writer advanced the persisted state first."""
    try:
        current = pipeline.repository.get_object(state_object_id(campaign_id))
        expected_revision = current["revision"]
    except PipelineNotFound:
        expected_revision = 0
    if state["version"] != expected_revision + 1:
        raise CampaignStateConflict(f"expected version {expected_revision + 1}, got {state['version']}")
    try:
        result = pipeline.repository.store_object(
            CAMPAIGN_STATE_TYPE,
            state,
            idempotency_key=idempotency_key,
            object_id=state_object_id(campaign_id),
            expected_revision=expected_revision,
        )
    except PipelineConflict as exc:
        raise CampaignStateConflict(str(exc)) from exc
    return result["object"]["payload"]
```

### Stage 3 — Routers

**`api/routers/campaigns.py`** (supervision routes; `campaigns` prefix already reserved for TS-APP-API-004's CRUD routes — this spec only adds the sub-paths below, in a clearly separated section of the file with a comment marking the boundary):

```python
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_pipeline, get_studio_bridge
from api.services import campaign_projection as campaigns_store
from api.services.studio_bridge import StudioBridgeError, StudioBridgeCrash
from api.schemas.supervision import ControlTowerProjectionModel, TimelineProjectionModel, ExceptionReviewPackageModel

router = APIRouter()

# --- TS-APP-API-006 supervision routes (Control Tower and Supervision API) ---
# CRUD routes (POST /, GET /, GET /{id}) are TS-APP-API-004's responsibility and are not
# defined in this file by this spec.

NODE_STATUS_MAP = {
    ("BLOCKED", "*"): "PENDING",
    ("READY", "HUMAN_GATE"): "WAITING_HUMAN",
    ("READY", "*"): "READY",
    ("DISPATCHED", "HUMAN_GATE"): "WAITING_HUMAN",
    ("DISPATCHED", "*"): "RUNNING",
    ("RUNNING", "*"): "RUNNING",
    ("SUCCEEDED", "*"): "SUCCEEDED",
    ("FAILED", "*"): "FAILED",
    ("CANCELLED", "*"): "CANCELLED",
    ("INVALIDATED", "*"): "INVALIDATED",
    ("QUARANTINED", "*"): "FAILED",
}

def map_node_status(python_state: str, node_kind: str) -> str:
    return NODE_STATUS_MAP.get((python_state, node_kind)) or NODE_STATUS_MAP[(python_state, "*")]

@router.get("/{campaign_id}/tower", response_model=ControlTowerProjectionModel)
def get_control_tower(campaign_id: str, pipeline=Depends(get_pipeline), bridge=Depends(get_studio_bridge)):
    try:
        campaign = campaigns_store.load_campaign(pipeline, campaign_id)
    except campaigns_store.CampaignNotFound:
        raise HTTPException(404, detail={"error_code": "CAMPAIGN_NOT_FOUND", "message": campaign_id})
    # ... assemble run_nodes, exception_packages, evaluations, timeline, studio_binding,
    # knowledge, runtime_health per Section 5's "Control Tower assembly" flow, then:
    try:
        projection = bridge.call("build-control-tower-projection", { ... })
    except StudioBridgeError as exc:
        raise HTTPException(422, detail={"error_code": exc.code, "message": str(exc), "context": exc.context})
    except StudioBridgeCrash as exc:
        raise HTTPException(500, detail={"error_code": "INTERNAL_ERROR", "message": str(exc)})
    return projection

@router.get("/{campaign_id}/timeline", response_model=TimelineProjectionModel)
def get_timeline(campaign_id: str, pipeline=Depends(get_pipeline), bridge=Depends(get_studio_bridge)):
    ...  # Section 5 "Timeline projection" flow; 404 TIMELINE_NOT_AVAILABLE when unbound

@router.get("/{campaign_id}/exceptions", response_model=list[ExceptionReviewPackageModel])
def list_exceptions(campaign_id: str, pipeline=Depends(get_pipeline), bridge=Depends(get_studio_bridge)):
    ...  # Section 5 "Exception package assembly"; returns [] when no FAILED nodes
```

*(`api/routers/revisions.py` and `api/routers/ship.py` follow the same shape as `campaigns.py` above, one handler per flow in Section 5 — `POST /{campaign_id}/revisions`, `POST /{campaign_id}/revisions/{program_id}/execute`, `POST /{campaign_id}/exceptions/{package_id}/resolve` in `revisions.py`; `POST /{campaign_id}/ship` and `GET /{campaign_id}/audit-export` in `ship.py`. Each handler is a direct, mechanical translation of its Section 5 pseudocode into the `load_campaign` → assemble bridge payload → `bridge.call(...)` → `save_campaign_state(...)` → response-model shape; omitted here for length, not because the mapping is ambiguous.)*

### Stage 4 — Registration

Already shown in Stage 0's `api/main.py` patch (registers `campaigns.router`, `revisions.router`, `ship.router`, all under the `/api/campaigns` prefix, alongside the health router from TS-APP-API-001 and whatever TS-APP-API-002/003/004 have already registered).

---

## 8. Failure, Migration, Rollback, Recovery, and Observability

### Typed failures

| Failure | Surface | Response |
|---|---|---|
| Node binary not on `PATH` | `subprocess.run` raises `FileNotFoundError` | Caught in `StudioBridge.call`, re-raised as `StudioBridgeCrash` → 500 `INTERNAL_ERROR` (this is a deployment defect, not a caller error — see Stage 0) |
| `services/studio/dist/rpc.js` missing (build not run) | Node exits non-zero, `MODULE_NOT_FOUND` on stderr | Same as above |
| Bridge call exceeds `timeout_seconds` | `subprocess.TimeoutExpired` | Not caught by this spec's `StudioBridge.call` — propagates as an unhandled 500 from FastAPI's default handler; a future spec should add an explicit `STUDIO_BRIDGE_TIMEOUT` 504 mapping (flagged, not fixed here, since no endpoint in this spec has a legitimate reason to run past 10s — a timeout here is itself evidence of a bug) |
| `CampaignStateConflict` on save | Two supervision actions raced on the same campaign | 409 `CAMPAIGN_STATE_CONFLICT`; caller must re-`GET /tower` and retry |
| `HumanResolutionLedger` hash-chain verification fails (Source gap notice: file corrupted out-of-band) | `StudioValidationError("EPISODE_HASH_MISMATCH", ...)` inside the Node process | Surfaces as a normal `StudioBridgeError` → 422; the ledger file itself is never auto-repaired |

### Migration

None. No SQL schema changes — this spec's persistence rides entirely on `pipeline_objects`, a table `TS-APP-API-001`'s existing `pipeline.initialize()` already creates via `cmf_pipeline`'s own migration.

### Observability

`GET /api/health` (TS-APP-API-001) is not extended by this spec to report Node/Studio-bridge health — a future, small patch should add a `studio_bridge` entry to `VALID_SERVICES` that shells out to `node dist/rpc.js list-default-tools` with an empty payload and checks for a 9-item response, proving both "Node is on `PATH`" and "the package is built" in one call. Flagged, not implemented here, since `TS-APP-API-001`'s health router shape assumes every service exposes a Python `.status()` method, and `StudioBridge` is not one of the five services enumerated there — extending `VALID_SERVICES`'s meaning to include a non-Python bridge is a decision that belongs to whoever next touches the health router, not a silent side effect of this spec.

### Deferred: persistent Studio worker

Every bridge call in this spec pays full Node process startup cost. If profiling later shows this is unacceptable for the Control Tower's polling pattern (`TS-APP-UI-003` will likely poll `/tower` every few seconds while a campaign runs), the fix is a long-lived `node services/studio/dist/rpc-server.js` process with a newline-delimited JSON protocol over a Unix socket, managed by the FastAPI app's lifespan (start on `app` startup, stop on shutdown) instead of `subprocess.run` per call. `StudioBridge`'s public `call()` signature would not need to change for callers of this spec's routers — only its internal implementation. Not built here; the per-call subprocess is the correct amount of engineering for a first working version.

---

## 9. Acceptance Criteria

**AC-001 — Control Tower assembles for a healthy running campaign.**
Given a `studio_campaign_order`/`studio_campaign_state` pair exists with `lifecycle_state: RUNNING` and a bound run with two `SUCCEEDED` nodes and one `RUNNING` node,
When `GET /api/campaigns/{id}/tower` is called,
Then the response is 200 with `run_nodes` containing exactly three entries whose `status` values are `SUCCEEDED, SUCCEEDED, RUNNING`, and `available_actions` includes `INSPECT_SOURCE`.
Failure example: a node's mapped status does not match the table in Section 5.
Evidence: response body diffed against the fixture's expected `run_nodes`.
Test layer: integration — `TestClient` + real Node subprocess (built `dist/rpc.js`).

**AC-002 — Control Tower on an unknown campaign is 404.**
Given no `studio_campaign_state` object exists for `campaign_id`,
When `GET /api/campaigns/{id}/tower` is called,
Then 404 with `error_code: CAMPAIGN_NOT_FOUND`.

**AC-003 — Timeline projection requires exactly one `PRIMARY_A_ROLL_SPINE` track.**
Given a bound `video_edit_program` with two tracks, neither carrying `role: PRIMARY_A_ROLL_SPINE`,
When `GET /api/campaigns/{id}/timeline` is called,
Then the bridge call returns `{ok: false, error: {code: "PRIMARY_A_ROLL_SPINE_REQUIRED"}}` and the endpoint responds 422 with that `error_code`.
Test layer: integration.

**AC-004 — Natural-language revision compiles a recognized pattern.**
Given a campaign in `RUNNING` with `expected_state_version` equal to the current state's `version`, and a request text `"move the logo left by 10%"`,
When `POST /revisions` is called with `mode: "natural_language"`,
Then the response is 200 with `compilation_status: "COMPILED"`, exactly one `exact_operations` entry with `tool_id: "studio.adjust_bbox"`, and `preview_required: true`.

**AC-005 — Unrecognized natural-language revision returns `NEEDS_CLARIFICATION`, not an error.**
Given the same campaign and a request text `"make it pop more"`,
When `POST /revisions` is called,
Then the response is 200 (not 4xx) with `compilation_status: "NEEDS_CLARIFICATION"` and `escalation: "CLARIFY_TARGET_OPERATION_OR_SELECT_STEERING_RECIPE"`.
Failure example: the endpoint returns a non-200 status for a well-formed-but-unmatched request.

**AC-006 — Revision execute fails on a stale compiled program.**
Given a program was compiled against `expected_state_version: 3`, and the campaign's persisted state has since advanced to `version: 4` (e.g., via a prior exception resolution),
When `POST /revisions/{program_id}/execute` is called,
Then 409 with `error_code: STALE_STATE_VERSION`, and no `HumanResolutionEpisode` is appended to the ledger.
Evidence: ledger file line count unchanged before/after the call.

**AC-007 — Revision execute succeeds and records exactly one episode.**
Given a freshly compiled, non-stale, `COMPILED` program,
When `POST /revisions/{program_id}/execute` is called,
Then 200 with a `rerun.invalidated_node_ids` list, an `episode.accepted: true`, and the campaign's `studio_campaign_state` object advances by exactly one revision.
Test layer: integration — reads the campaign state object's `revision` field before and after via `pipeline.repository.get_object`.

**AC-008 — Exceptions list is empty (not 404) when there are no failed nodes.**
Given a campaign with all nodes `SUCCEEDED`,
When `GET /exceptions` is called,
Then 200 with `[]`.

**AC-009 — A `FAILED` node with a `PIPELINE_COMPOSITION`-layer failure offers `REQUEST_REVISION`.**
Given a `FAILED` node whose stored `failure.code` is `"BBOX_COLLISION"` (mapped to `PIPELINE_COMPOSITION`, `repairable_by_pipeline: true`),
When `GET /exceptions` is called,
Then the corresponding package's `allowed_decisions` is exactly `["REJECT", "REQUEST_REVISION"]` and `recommended_next_actions` excludes `"ESCALATE_OWNER"`.

**AC-010 — A `FAILED` node with an unmapped failure code offers only `REJECT`.**
Given a `FAILED` node whose stored `failure.code` is `"UNSEEN_CODE_XYZ"` (not in `LAYER_BY_CODE`, so `responsible_layer: UNKNOWN_REQUIRES_TRIAGE`),
When `GET /exceptions` is called,
Then `allowed_decisions` is exactly `["REJECT"]`.

**AC-011 — Resolving an exception with a disallowed decision is 400.**
Given the AC-010 package (only `REJECT` allowed),
When `POST /exceptions/{package_id}/resolve` is called with `decision: "REQUEST_REVISION"`,
Then 400 with `error_code: DECISION_NOT_ALLOWED`.

**AC-012 — Resolving with `REJECT` transitions the campaign to `BLOCKED_EXCEPTION` and clears the exception ID.**
Given a campaign in `RUNNING` with `exception_ids: [package_id]`,
When `POST /exceptions/{package_id}/resolve` is called with `decision: "REJECT"`,
Then 200, the returned `campaign.lifecycle_state` is `"BLOCKED_EXCEPTION"`, and `campaign.exception_ids` no longer contains `package_id`.

**AC-013 — Ship is denied on all applicable grounds simultaneously, not just the first.**
Given a campaign in `READY_TO_SHIP` with `autonomy_mode: "SHADOW"`, no artifacts, no evaluations, and one unresolved exception, and a ship request missing both authority and policy refs,
When `POST /ship` is called,
Then 200 with `status: "DENIED"` and `denial_codes` containing all of `SHADOW_PUBLICATION_FORBIDDEN, PUBLICATION_AUTHORITY_REQUIRED, PUBLICATION_POLICY_REQUIRED, ARTIFACT_REQUIRED, EVALUATION_EVIDENCE_REQUIRED, UNRESOLVED_EXCEPTION` — six codes, not one.
Failure example: only the first-encountered denial reason is returned.

**AC-014 — Ship outside `READY_TO_SHIP` fails fast without a bridge call.**
Given a campaign in `RUNNING`,
When `POST /ship` is called,
Then 409 with `error_code: SHIP_NOT_READY`, and (verified via a call-count assertion on a mocked `StudioBridge`) `evaluate-ship-request` is never invoked.

**AC-015 — A successful ship writes a self-verifying audit export.**
Given a campaign in `READY_TO_SHIP` with valid authority/policy refs, at least one artifact, at least one evaluation, and no unresolved exceptions,
When `POST /ship` is called,
Then 200 with `status: "AUTHORIZED"`, the campaign's `lifecycle_state` becomes `"SHIPPED"`, and `GET /audit-export` immediately afterward returns 200 with an `export_sha256` that recomputes correctly (the write path already refuses to write on a hash mismatch — this AC proves the file that lands on disk is the one later read back).

**AC-016 — Audit export is unavailable before shipping.**
Given a campaign in `READY_TO_SHIP` (not yet shipped),
When `GET /audit-export` is called,
Then 404 with `error_code: AUDIT_EXPORT_NOT_AVAILABLE`.

**AC-017 — A `SHADOW` campaign can never reach `SHIPPED`, even via direct `transition-campaign`.**
Given a campaign with `autonomy_mode: "SHADOW"` in `READY_TO_SHIP`,
When the ship flow's internal `transition-campaign` call targets `"SHIPPED"`,
Then the bridge raises `StudioValidationError("SHADOW_CANNOT_SHIP", ...)` — but note `evaluateShipRequest` itself already denies `SHADOW` requests via `SHADOW_PUBLICATION_FORBIDDEN` before the transition is ever attempted, so this AC specifically exercises that `transition-campaign` is defense-in-depth, not the only guard (test calls the bridge's `transition-campaign` command directly, bypassing the ship endpoint, to prove the lower-level guard also holds).

**AC-018 — Regression: pre-existing test suite still passes.**
Given the Phase 9 test suite plus TS-APP-API-001/002/003's test suites were passing before this spec,
When this spec is fully implemented and `python -m pytest tests/ -q` and `npm test` (in `services/studio`) are both run,
Then all pre-existing tests continue to pass, and `services/studio`'s existing `node --test tests/*.test.mjs` suite is unaffected by the addition of `rpc.ts` (a new file that imports existing exports; nothing it imports is modified).

---

## 10. Testing and Completion Evidence

### Test files to create

**`services/studio/tests/rpc.test.mjs`** (new — Node's built-in test runner, matching the existing `node --test tests/*.test.mjs` convention from `package.json`)
- `test_unknown_command_returns_validation_error_envelope`
- `test_build_control_tower_projection_roundtrip`
- `test_compile_natural_language_revision_needs_clarification`
- `test_create_human_resolution_episode_appends_to_ledger` — asserts the ledger file's line count and hash chain both advance by exactly one entry

**`tests/api/fixtures/studio_campaign_fixtures.py`**
- `make_running_campaign(pipeline, campaign_id)` — writes fixture `studio_campaign_order`/`studio_campaign_state` objects directly via `campaign_projection` (since no creation endpoint exists — Section 2, out of scope)
- `make_failed_node_run(pipeline, run_id, failure_code)` — drives `run_service.fail_node()` with a synthetic `TypedFailure`

**`tests/api/test_control_tower.py`** — AC-001, AC-002
**`tests/api/test_timeline.py`** — AC-003
**`tests/api/test_revisions.py`** — AC-004, AC-005, AC-006, AC-007
**`tests/api/test_exceptions.py`** — AC-008, AC-009, AC-010, AC-011, AC-012
**`tests/api/test_ship.py`** — AC-013, AC-014, AC-015, AC-016, AC-017

### Test tooling

Every Python integration test in this spec requires `services/studio` to be built first:
```bash
cd services/studio && npm install && npm run build
```
Test fixtures assert against the **real** `node dist/rpc.js` subprocess — no mock bridge is used for AC-001 through AC-017, since the entire point of this spec is proving the Python↔Node boundary actually works. A separate, smaller set of router-only unit tests (not enumerated above, left to the implementer) may mock `StudioBridge` to test error-mapping branches (e.g. AC-014's "never invoked" assertion) without paying subprocess cost on every CI run.

```python
from fastapi.testclient import TestClient
from api.main import app
from tests.api.fixtures.studio_campaign_fixtures import make_running_campaign

def test_control_tower_maps_node_statuses(pipeline_app):
    campaign_id = make_running_campaign(pipeline_app, "campaign-1")
    with TestClient(app) as client:
        response = client.get(f"/api/campaigns/{campaign_id}/tower")
    assert response.status_code == 200
    statuses = [n["status"] for n in response.json()["run_nodes"]]
    assert statuses == ["SUCCEEDED", "SUCCEEDED", "RUNNING"]
```

### Pre-existing regression

```bash
python -m pytest tests/ -q --tb=short
cd services/studio && npm test
```
Zero new failures in either suite is a hard gate (AC-018).

### Build Receipt claim ceiling

`CONTROL_TOWER_SUPERVISION_API_DEVELOPMENT_EVIDENCE`

This spec does not claim: production-grade Node/Python IPC latency (Section 8); that `BoundedRepairService.plan()` output is ever consumed by a re-execution path (Out of scope, Section 2); that the `studio_campaign_order`/`studio_campaign_state` persistence convention is final (`ASSUMED_INTERFACE_PENDING_004`, Source gap notice 2); that `wrong_reading_locks` sourcing is correct (Source gap notice 5); authentication, authorization, or multi-tenant isolation; or certified/production-authorized operation.

---
spec_end: true
next_spec: TS-APP-API-004 (Campaign CRUD API) — strongly recommended next, specifically to resolve
  Source gap notice 2 (this spec's `ASSUMED_INTERFACE_PENDING_004` persistence convention) before more
  specs build on it; alternatively TS-APP-API-005 (Pipeline Status WebSocket) per Wave 2 sequencing.
open_question_for_next_spec_author: TS-APP-API-004's author must decide whether to (a) adopt this spec's
  `studio_campaign_order`/`studio_campaign_state` object-type convention over `PipelineRepository` as
  Campaign persistence's permanent home, or (b) replace it with something else and migrate this spec's
  reads/writes (`api/services/campaign_projection.py`) to match. Silently diverging (e.g., building a new
  SQL table for campaigns while this spec keeps reading `pipeline_objects`) would leave two
  non-communicating sources of truth for the same `campaign_id` — that must not happen unreconciled.
  A second, smaller open question for whoever writes the harness-detail audit pass: confirm the real key
  name for wrong-reading locks inside `HarnessDetail.category_binding` (Source gap notice 5) and update
  this spec's `assemble_revision_context` sourcing accordingly.
---
