---
spec_id: TS-APP-API-005
title: Pipeline Status WebSocket
document_class: TECH_SPEC
product: Conscious Activations
module: api
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CURRENT
build_authority: false
controlling_frs:
  - FR-APP-051 (pipeline execution and progress reporting — "Status is reported in real time")
controlling_stories:
  - ST-APP-07.02 (watch Pipeline status in real time — WebSocket + GET polling fallback)
upstream_dependencies:
  - CA_PROJECT_SNAPSHOT_V2.md (authority — CURRENT)
  - CA_APP_FR_EPIC_SPEC_PLAN.md (authority — CURRENT)
  - TS-APP-API-001.md (quality_state: WRITTEN_PENDING_AUDIT — DRAFT_DEPENDENCY_NOT_ACCEPTED; this spec depends only on its `api/dependencies.py::get_pipeline` factory, `api/config.py::AppConfig`/`load_config`, and `api/errors.py::ErrorResponse` interfaces, not on any claim that the gateway is production-ready)
  - TS-APP-API-002.md (flagged this spec as **BLOCKED** on "Source Gap 4" — Builder/Pipeline schema mismatch; see Section 3, "Relationship to Gap 4")
  - TS-APP-API-004.md — **DOES NOT EXIST YET.** Campaign CRUD has not been written or built. This spec cannot assume any campaign persistence, campaign_id shape, or campaign→run linkage beyond what it defines itself in Section 3 ("Campaign→run resolution contract"). See Source Gap Notice below.
downstream_consumers:
  - TS-APP-API-004 (Campaign CRUD API — MUST write the `campaign_produces_run` edge this spec reads; see Section 3)
  - TS-APP-API-006 (Control Tower and Supervision API — supplies workflow topology/nodes+edges that this spec's stream deliberately excludes; RunGraph.tsx merges the two client-side)
  - TS-APP-UI-003 (Control Tower UI — RunGraph.tsx is the direct consumer of this WebSocket)
output_path: api/websockets/pipeline_status.py (and supporting files listed in section 7)
wave: 2
---

# TS-APP-API-005 — Pipeline Status WebSocket

## 1. Files and Authorities Read

| File | SHA-256 (short) | Status | Fact extracted |
|---|---|---|---|
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/application/run_service.py` | `44917906` | READ — CURRENT IMPLEMENTATION | `WorkflowRunService` is a synchronous, SQLite-backed state machine with **no pub/sub, no callback registry, no event bus**. Every transition (`dispatch_node`, `start_node`, `complete_node`, `fail_node`, `pause_run`, `resume_run`, `cancel_run`, `checkpoint`) writes a row to `pipeline_run_events` inside the same transaction as the state mutation, then returns. `status(run_id)` reconstructs a full run+node snapshot from `pipeline_runs`/`pipeline_node_states` (two indexed reads, O(nodes)). `replay(run_id)` returns the entire ordered, hash-verified event stream from sequence 1 (O(events)). Neither method accepts a "since sequence N" cursor. |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/application/scheduler.py` | `d6f3340b` | READ — CURRENT IMPLEMENTATION | `DeterministicScheduler.ready_nodes()`/`safe_parallel_batch()` compute what's dispatchable next; they do not dispatch anything themselves. Confirms there is no autonomous loop anywhere in this file. |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/application/jit_context.py` | `566342e5` | READ — CURRENT IMPLEMENTATION | `JITContextCompiler.compile()` produces a `jit_capsule` embedded in the `NodeDispatched` event payload; it carries `context_refs`, `allowed_actions`, `tool_ids`, etc. — not secret-bearing, but verbose and node-implementation-specific. Justifies excluding the full capsule body from the live diff stream (Section 3). |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/domain/models.py` | `df06da0d` | READ — CURRENT IMPLEMENTATION | `validate_runtime_workflow()` confirms the workflow's `nodes`/`edges`/`topological_order` are validated and stored as one JSON blob in `pipeline_workflows.definition_json`, addressed only by `workflow_id` — not by `run_id`, and not exposed through any public method on `WorkflowRunService` (only an underscore-prefixed `_workflow()` helper reads it). |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/infrastructure/repository.py` | `7307fbee` | READ — CURRENT IMPLEMENTATION | `PipelineRepository._connect()` opens SQLite with `journal_mode=WAL`, `synchronous=FULL`, one connection per call, always closed via `closing()`. WAL mode makes concurrent reads safe alongside a writer. `descendants(roots, relation_types)` does a generic forward graph traversal over `pipeline_edges`; `add_edge(source_id, target_id, relation_type, evidence=None)` writes an edge with **no foreign-key constraint** tying `source_id`/`target_id` to any other table — both are free-form `TEXT`. This is the mechanism this spec relies on for campaign→run resolution (Section 3). |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/domain/enums.py` | `584a03fb` | READ — CURRENT IMPLEMENTATION | `NodeState` = `BLOCKED, READY, DISPATCHED, RUNNING, SUCCEEDED, FAILED, CANCELLED, INVALIDATED, QUARANTINED`. `RunState` = `CREATED, RUNNING, PAUSED, CANCEL_REQUESTED, CANCELLED, COMPLETED, FAILED, INVALIDATED`. Terminal run states for this spec's purposes: `COMPLETED, FAILED, CANCELLED, INVALIDATED`. |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/domain/errors.py` | `abb1b94a` | READ — CURRENT IMPLEMENTATION | `PipelineNotFound`, `PipelineConflict`, `PipelineLifecycleError`, `PipelineValidationError` are the exception types this spec's router must translate to HTTP/WS error codes. |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/batch/service.py` | `d1553853` | READ — CURRENT IMPLEMENTATION | `ContentBatchService.compile_batch()` takes a `campaign_id` and produces a `batch_id` (content batch) containing `derivative_job` objects. **It never calls `WorkflowRunService.create_run()` and never persists any link from `campaign_id` to a `run_id`.** Confirms the campaign→run gap described in Section 3 is real, not a documentation oversight. |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/application.py` | `a32b6cea` | READ — CURRENT IMPLEMENTATION | `PipelineApplication` exposes `.runs` (`WorkflowRunService`), `.repository` (`PipelineRepository`, the same instance `.runs` was constructed with), and `.batches` (`ContentBatchService`) as plain public attributes — matches the `app.state.pipeline` object `TS-APP-API-001` already instantiates. Hash matches the hash already cited for this file in `TS-APP-API-001.md` — file unchanged since that spec was written. |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/cli.py` | `8008b055` | READ — CURRENT IMPLEMENTATION | Subcommands are exactly `health, init-db, bootstrap, status, load-development-candidates, demo, phase6-demo, export-schemas, replay-run, inspect-run`. **There is no `worker` subcommand and no automatic node dispatcher anywhere in this package.** See Source Gap Notice below. |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/demo.py` | `82811a41` | READ — CURRENT IMPLEMENTATION | `run_demo()` is the only place in the codebase that drives a run end-to-end: `create_run` → loop over `topological_order` calling `ready_nodes → dispatch_node → start_node → complete_node` → `checkpoint` → `replay`. This is the reference pattern this spec's test fixtures use to simulate a worker (Section 10). |
| `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/migrations/0001_pipeline_core.sql` | `544864de` | READ — CURRENT IMPLEMENTATION | Confirms `pipeline_edges` has no FK constraints (free-form `TEXT` source/target); confirms `pipeline_run_events` primary key is `(run_id, sequence)`; confirms neither `pipeline_runs` nor `pipeline_node_states` rows are returned with timestamps by `_run_state()` even though the columns exist — `status()`'s node dicts carry no `updated_at_utc`. |
| `CA_PROJECT_SNAPSHOT_V2.md` | — | READ — CURRENT AUTHORITY | Section 7 (target structure) names `api/routers/pipeline_status.py`; Section 8 (quickest path) instead shows a `worker` docker-compose service running `python -m cmf_pipeline worker --poll-interval 5`. Per the CLI fact above, that command does not exist today. Section 9 states "reports status back via WebSocket" as the last step of Harness execution. |
| `CA_APP_FR_EPIC_SPEC_PLAN.md` | — | READ — CURRENT AUTHORITY | Part 4 defines this spec exactly: `Scope: api/websockets/pipeline_status.py`; `Output: ws://api/campaigns/:id/status — streams node state transitions`; `Depends on: TS-APP-API-004`. Part 3 (ST-APP-07.02) adds the GET polling-fallback requirement and the "within 2 seconds" acceptance bound. |
| `TS-APP-API-002.md` | — | READ — CURRENT (WRITTEN_PENDING_AUDIT) | Frontmatter explicitly lists this spec as **"currently BLOCKED, see Source Gap 4"** and states: *"TS-APP-API-005 cannot report meaningful workflow node status for it [a Builder-exported Harness] until this gap is closed by a dedicated spec."* Addressed in Section 3. |

**Source gap notice (blocking risk, not fixed here — read before implementing):**

**Gap A — No automatic node dispatcher/worker exists.** `CA_PROJECT_SNAPSHOT_V2.md`'s docker-compose sketch shows a `worker` service running `python -m cmf_pipeline worker --poll-interval 5`, but `cli.py` has no `worker` subcommand and no code anywhere in `cmf_pipeline` autonomously walks `scheduler.ready_nodes()` and calls `dispatch_node → start_node → complete_node` in a loop. Today, node transitions happen only when something — currently only `demo.py`, `phase9_demo.py`, and tests — calls those `WorkflowRunService` methods directly. **This spec streams whatever transitions occur; it does not create a worker.** A dedicated Worker/Dispatcher spec (not yet queued — recommend `TS-APP-API-007` or folding into a Wave 2 addendum) must exist before "operator watches a real campaign execute live" is true end to end. This spec's acceptance criteria are scoped accordingly (Section 9): they prove the streaming mechanism against manually-driven transitions, not against an autonomous worker that doesn't exist yet.

**Gap B — Campaign→run linkage does not exist.** Confirmed by both `batch/service.py` (no `create_run` call, no persisted link) and by `TS-APP-API-004.md` simply not existing. This spec defines the exact contract it needs (a `pipeline_edges` row with `relation_type="campaign_produces_run"`, written by whoever creates a run for a campaign) and reads it via the pre-existing generic `PipelineRepository.descendants()` — see Section 3. It does **not** invent campaign storage, and it does **not** modify `cmf_pipeline` to add campaign awareness. TS-APP-API-004's author must write that edge when `create_run()` is called for a campaign, or the `campaign_id`-keyed endpoints in this spec will correctly and legibly 404.

**Relationship to Gap 4 (from TS-APP-API-002):** Gap 4 is about whether a Harness built through the Builder API can be **ingested and executed** by the Pipeline at all (schema mismatch between `PortableAtomicHarnessDefinition` and `AtomicHarnessDefinitionIntake`). This spec does not ingest, compile, or execute workflows — it only reads `pipeline_runs`/`pipeline_node_states`/`pipeline_run_events` for whatever `run_id` already exists, regardless of how that run's workflow was registered (Harness-derived, `demo.py`-derived, or hand-constructed in a test fixture). **The streaming mechanism in this spec works today, independent of Gap 4.** What Gap 4 actually blocks is Gate G (a real Harness producing a real run) — not this spec's transport layer. This spec does not claim Gate G; see the claim ceiling in Section 3.

---

## 2. Problem, User Outcome, Solution, and Scope

### Problem without this spec
Nothing in the system reports live progress anywhere. An operator (or a developer testing the Pipeline) has exactly one way to see a run's state today: run `cmf-pipeline inspect-run <run_id> --json` from a shell with access to the SQLite file. The React `RunGraph.tsx` component described in `CA_APP_FR_EPIC_SPEC_PLAN.md` has no endpoint to call. `WorkflowRunService` itself has no notion of "notify me when something changes" — it is a pure request/response state machine.

### User outcome
A developer or, once `TS-APP-UI-003` exists, an operator opens a page showing a campaign's production run and sees each node move from `BLOCKED` → `READY` → `DISPATCHED` → `RUNNING` → `SUCCEEDED` (or `FAILED`) within about a second of the transition actually happening, without reloading the page. If their browser or network can't hold a WebSocket open, the same information is available by polling a plain `GET` endpoint. When the run finishes, the connection closes itself with a clear reason instead of dangling.

### Solution
Because `WorkflowRunService` has no push mechanism, this spec builds a **poll-and-diff bridge** entirely inside the new `api/` layer:
- A background loop (one per open WebSocket connection) calls the existing, unmodified `WorkflowRunService.status(run_id)` on an interval, off the event loop thread.
- It diffs the new snapshot against the last one it sent and pushes only what changed.
- A `GET` endpoint on the identical resource path exposes a single snapshot for clients that poll manually.
- A third endpoint exposes the full historical event log (via the existing `replay()`) for anyone who wants the whole story, not just the current state.
- Because no `campaign_id → run_id` linkage exists yet anywhere in the codebase, every endpoint is offered in two forms: keyed directly by `run_id` (works today, fully testable, no upstream dependency) and keyed by `campaign_id` (a thin resolver on top, which depends on `TS-APP-API-004` writing one specific graph edge — see Section 3).

### In scope
- `api/schemas/pipeline_status.py` — response/message models
- `api/services/campaign_run_lookup.py` — the `campaign_id → run_id` resolver and its two typed failure modes
- `api/websockets/pipeline_status.py` — the poll-and-diff bridge, the WebSocket routes, and the REST fallback/history routes (all one resource, so one module)
- One additive field on `api/config.py::AppConfig` (`ws_poll_interval_ms`)
- One additive WebSocket-flavored dependency factory in `api/dependencies.py` (`get_pipeline_ws`)
- Two-line edit to `api/main.py` to register the new router
- Test fixtures that manually drive a run through `WorkflowRunService` (following the `demo.py` reference pattern) to exercise the stream, since no real worker exists to drive one for us

### Out of scope
- **A node dispatcher/worker** that autonomously executes ready nodes (Gap A) — a separate, not-yet-queued spec
- **Campaign creation and the `campaign_produces_run` edge write** — that belongs to `TS-APP-API-004`, which does not exist yet; this spec only reads the edge and defines its exact shape
- **Workflow topology** (the `nodes`/`edges`/`topological_order` graph shape) in the live stream — `WorkflowRunService` exposes no public accessor for it by `run_id`, and adding one would mean modifying `cmf_pipeline`, which this spec deliberately avoids (see Section 3, "Why topology is not in this stream"). Topology is `TS-APP-API-006`'s (Control Tower) responsibility; `RunGraph.tsx` merges topology (fetched once) with this spec's live node states (streamed continuously), keyed by `node_id`, on the client
- **Multi-run campaigns** — if a `campaign_id` resolves to more than one `run_id`, this spec returns a typed 409 rather than guessing which one to show (Section 3)
- **Authentication/authorization on the socket** — matches `TS-APP-API-001`'s explicit deferral of auth for the whole gateway
- **A shared broadcast hub** for many simultaneous viewers of the same run — each connection polls independently; documented as a scaling note, not a defect, for this development-stage spec
- **Any modification to `cmf_pipeline`, `cmf_activative_intelligence`, `cmf_vae`, or any other existing service package** — this spec is additive `api/` code only, with zero exceptions
- Reconciling Gap 4 (Builder/Pipeline schema mismatch) — orthogonal to this spec, as established above

---

## 3. Governing Decisions and Constraints

**This is a poll-and-diff bridge, not real push.** `WorkflowRunService` has no event bus. Faithfully representing that, this spec polls `status(run_id)` on an interval and diffs; it does not pretend to subscribe to anything. Default interval is `750ms` (`WS_POLL_INTERVAL_MS` env var, `api/config.py`). Worst-case detection latency is bounded by one poll interval plus one query round-trip (single-digit milliseconds against a local WAL-mode SQLite file with two `run_id`-indexed lookups) — comfortably inside FR-APP-051's ~2-second target even at the default interval, with headroom to raise the interval later if polling load becomes a concern.

**`WorkflowRunService` is synchronous and blocking.** Every call opens and closes a raw `sqlite3` connection. It must never be called directly from an `async def` route or the WS loop's coroutine — every call goes through `fastapi.concurrency.run_in_threadpool`. This is the same discipline `TS-APP-API-001` established for the (also synchronous) `.status()` calls in the health router, applied consistently here.

**No modification to `cmf_pipeline`.** The one new capability this spec needs from the domain — resolving a `campaign_id` to a `run_id` — is achieved entirely with the pre-existing, generic `PipelineRepository.add_edge()` / `.descendants()` graph API, which already has no foreign-key constraints tying edge endpoints to any particular object type. No new method, column, or table is added to any existing service package.

**Campaign→run resolution contract (the one thing TS-APP-API-004 must honor).** When `TS-APP-API-004` creates a pipeline run in service of a Campaign Order, it must call:
```python
pipeline.repository.add_edge(
    campaign_id,           # source_id — the Campaign Order's identifier
    run_id,                # target_id — the WorkflowRunService.create_run() result's run_id
    "campaign_produces_run",
)
```
This spec resolves `campaign_id → run_id` via `pipeline.repository.descendants([campaign_id], relation_types={"campaign_produces_run"})`. Until `TS-APP-API-004` exists and writes this edge, every `campaign_id`-keyed endpoint in this spec returns a well-formed `404 CAMPAIGN_HAS_NO_RUN` — a correct, legible answer, not a crash. The `run_id`-keyed endpoints have no such dependency and are fully exercisable today.

**Multi-run campaigns are refused, not guessed.** `descendants()` returns a set; if it ever contains more than one `run_id` for a `campaign_id` (a future multi-route campaign firing several Harness executions), this spec returns `409 CAMPAIGN_HAS_MULTIPLE_RUNS` rather than picking one — there is no "most recent" ordering available without reaching into `pipeline_runs` internals that no public method exposes. Resolving this is left to whichever future spec introduces real multi-run campaigns.

**Why topology is not in this stream.** `WorkflowRunService.status()` returns only `run_id, workflow_id, state, revision, cancel_requested, current_checkpoint_id, nodes[]` — where each node is `node_id, state, attempt_count, dispatch_ordinal, output_ref, failure`. It does not return the workflow's `nodes`/`edges`/`topological_order` graph shape; only an underscore-prefixed, package-internal `_workflow()` helper does, and reaching into it from the API layer would mean depending on a private contract or duplicating raw SQL against `pipeline_workflows.definition_json` from outside the domain package — both of which this spec's "no modification, no reaching around encapsulation" discipline rules out. Topology is fetched once (it does not change during a run) by `TS-APP-API-006`'s Control Tower endpoint; this spec streams only what actually changes.

**No per-node or per-run timestamp is available from `status()`.** The underlying SQLite columns (`updated_at_utc`) exist, but `_run_state()` does not return them, and this spec must not invent fields the domain doesn't produce. The poll-and-diff loop therefore detects a change by structural (deep) equality of each node's dict between ticks, not by comparing a clock. Every message this spec sends carries its own `retrieved_at_utc` — a timestamp of when *this API layer* observed the value, generated the same way `TS-APP-API-001`'s `ErrorResponse`/`HealthResponse` already do (`ca_contracts.utc_now_rfc3339()`) — never presented as if it came from the domain.

**One poll loop per connection; no shared broadcast hub.** Two operators watching the same run each get their own independent poll loop and their own SQLite reads. This is the simplest correct answer at development scale and avoids introducing new shared server-side state. Documented here as a known scaling boundary, not deferred silently: a future spec should add a per-`run_id` broadcast hub if concurrent-viewer counts ever make N independent pollers a real cost.

**Terminal run states end the connection server-side.** Once a poll observes `run.state` in `{COMPLETED, FAILED, CANCELLED, INVALIDATED}`, the server sends one final `run_terminal` message and closes the socket with code `1000`. Clients do not need to detect "nothing more is coming" themselves.

**WebSocket close codes are explicit, not generic.** Per RFC 6455, application codes live in `4000–4999`. This spec uses `4404` (unknown `run_id`, or `campaign_id` with no linked run) and `4409` (`campaign_id` with more than one linked run) so a WS client can distinguish "this will never resolve" from "try again later" without parsing a close reason string.

**Claim ceiling:** `PIPELINE_STATUS_STREAM_DEVELOPMENT_EVIDENCE`. This spec does not claim: an autonomous worker exists (Gap A); campaign creation or campaign-run linkage exists (Gap B, owned by `TS-APP-API-004`); Harness execution readiness (Gap 4, owned by a future reconciliation spec); workflow topology is available through this endpoint; production-grade push infrastructure (this is polling, honestly represented as polling); or multi-viewer scalability beyond development-scale concurrent connections.

---

## 4. Current Brownfield Architecture

| Component | Path | Actual behaviour | Disposition | Reason |
|---|---|---|---|---|
| `WorkflowRunService` | `services/pipeline/src/cmf_pipeline/workflow/application/run_service.py` | Synchronous state machine; `status()` and `replay()` are the only public read paths | REUSE — unmodified | This spec calls both, off-thread, and nothing else |
| `PipelineRepository` | `services/pipeline/src/cmf_pipeline/workflow/infrastructure/repository.py` | Generic object/edge/event store over SQLite (WAL mode) | REUSE — unmodified | `descendants()`/`add_edge()` power campaign→run resolution; no new methods added |
| `pipeline_run_events` / `pipeline_node_states` / `pipeline_runs` tables | `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/migrations/0001_pipeline_core.sql` | Append-only event log + current-state tables | REUSE — read-only from this spec | No migration needed |
| `pipeline_edges` table | same migration | Generic, FK-free graph edge store, already used by `ContentBatchService`/`import_harness_package` for unrelated relation types | REUSE — this spec adds one new `relation_type` string convention (`campaign_produces_run`), no schema change | FK-free by design; safe to layer a new relation type on top without migration |
| `cli.py` `worker` command | `services/pipeline/src/cmf_pipeline/cli.py` | **Does not exist** — `CA_PROJECT_SNAPSHOT_V2.md`'s docker-compose sketch describes a command that was never implemented | FLAG — MISSING, NOT FIXED HERE | Gap A; a dedicated Worker/Dispatcher spec must build this before real campaigns produce live transitions |
| `demo.py` `run_demo()` | `services/pipeline/src/cmf_pipeline/demo.py` | Manually drives one run end-to-end via direct `WorkflowRunService` calls | REUSE — as a test-fixture reference pattern only, not imported by production code | Nothing else in the codebase demonstrates driving a run; this spec's tests follow the same call sequence |
| `api/config.py` | `api/config.py` (from `TS-APP-API-001`) | `AppConfig` dataclass with `ca_data_root`, `ca_media_root`, `ca_delegation_root`, `gateway_version` | ADAPT — add one field, `ws_poll_interval_ms: int = 750` | Additive; existing fields and callers unchanged |
| `api/dependencies.py` | `api/dependencies.py` (from `TS-APP-API-001`) | `get_pipeline(request: Request) -> PipelineApplication` reads `request.app.state.pipeline` | ADAPT — add `get_pipeline_ws(websocket: WebSocket) -> PipelineApplication` | FastAPI's HTTP `Request` and `WebSocket` are different types; existing `get_pipeline` is untouched |
| `api/main.py` | `api/main.py` (from `TS-APP-API-001`) | Registers `health.router`; comments mark where Wave 2 routers attach | ADAPT — uncomment/add one `include_router` line for this spec's router | Matches the exact pattern `TS-APP-API-003` used to wire in `interviews.router` |
| Studio `controlTower.ts`/`timeline.ts` | `services/studio/src/` | Correct TypeScript domain types for the full Control Tower projection, including topology | NOT CONSUMED HERE | Reserved for `TS-APP-API-006`; this spec's payload is deliberately narrower than what those types eventually need |

---

## 5. Proposed Architecture and Workflows

### Component overview

```
Browser (RunGraph.tsx)
   │  new WebSocket("ws://.../api/campaigns/{campaign_id}/status")
   │  or GET .../api/campaigns/{campaign_id}/status  (polling fallback)
   ▼
api/websockets/pipeline_status.py
   ├── resolve_campaign_run_id()  ──uses──▶  PipelineRepository.descendants()
   │                                          (reads the campaign_produces_run edge
   │                                           TS-APP-API-004 is responsible for writing)
   ├── _poll_loop(run_id)  ── every WS_POLL_INTERVAL_MS ──▶  run_in_threadpool(pipeline.runs.status, run_id)
   │        │
   │        └── diff against last snapshot ──▶ send only what changed
   │
   └── GET .../status            ──▶ run_in_threadpool(pipeline.runs.status, run_id)   (single snapshot)
       GET .../status/events     ──▶ run_in_threadpool(pipeline.runs.replay, run_id)   (full history)

Meanwhile, elsewhere (out of scope, does not exist yet):
   demo.py / a future worker  ──▶  pipeline.runs.dispatch_node/start_node/complete_node/fail_node
                                     (this is what actually produces the transitions being streamed)
```

### WebSocket connection lifecycle

`WS /api/runs/{run_id}/status` (works today) and `WS /api/campaigns/{campaign_id}/status` (thin resolver wrapper) share one implementation, `_stream(websocket, pipeline, run_id)`:

1. `await websocket.accept()`
2. Resolve `run_id` (already known for the `/runs/` path; resolved via `resolve_campaign_run_id()` for the `/campaigns/` path). On `PipelineNotFound` / `CampaignHasNoRun` → `await websocket.close(code=4404, reason=...)`, return. On `CampaignHasMultipleRuns` → `close(code=4409, ...)`, return.
3. Fetch the first snapshot via `run_in_threadpool(pipeline.runs.status, run_id)`. Send `{"type": "snapshot", "retrieved_at_utc": ..., "run": {...}}`.
4. If the query param `include_history=true` was supplied, fetch `run_in_threadpool(pipeline.runs.replay, run_id)` once and send `{"type": "history", "retrieved_at_utc": ..., "event_count": ..., "event_stream_sha256": ..., "events": [...]}`. Off by default — `replay()` hash-verifies the entire event stream every call, and most connections only need the current state, not the full history.
5. Loop: `await anyio.sleep(poll_interval_ms / 1000)`, fetch a new snapshot the same way, diff against the last snapshot sent (Section 6 for the diff algorithm), send zero or more `node_state_changed` / `run_state_changed` messages.
6. If the new snapshot's `run.state` is terminal, send one `run_terminal` message, then `await websocket.close(code=1000, reason="run reached terminal state")`, return.
7. On `WebSocketDisconnect` at any `await` point: stop the loop, return cleanly. No server-side state outlives the connection.

### REST fallback and history workflow

`GET /api/runs/{run_id}/status` and `GET /api/campaigns/{campaign_id}/status` return the identical shape sent in the WebSocket's initial `snapshot` message (minus the `type` envelope field), via one `run_in_threadpool` call. `GET /.../status/events` returns `replay()`'s output almost verbatim, wrapped in a typed response model. All three raise the same typed failures as the WS path, translated to ordinary HTTP status codes instead of WS close codes (Section 8).

### Diff algorithm

Given `previous` and `current`, both the dict shape `run_service.status()` returns:
- If `previous is None` (first tick after the initial snapshot): no diff messages — the initial `snapshot` already covered it.
- Build `previous_nodes = {n["node_id"]: n for n in previous["nodes"]}` and the same for `current`.
- For each `node_id` in `current_nodes`: if `current_nodes[node_id] != previous_nodes.get(node_id)` (whole-dict equality — no per-node timestamp exists to compare instead), emit `node_state_changed` for it.
- If any of `current["state"]`, `current["revision"]`, `current["cancel_requested"]`, `current["current_checkpoint_id"]` differ from `previous`'s, emit one `run_state_changed` carrying those four fields plus `run_id`/`workflow_id`.
- `revision` (from `_run_state()`) is a monotonically increasing integer that `WorkflowRunService` bumps on every mutation — a convenient, already-existing cheap short-circuit: if `current["revision"] == previous["revision"]`, skip the node diff entirely (nothing changed).

### Query parameters

| Parameter | Applies to | Meaning |
|---|---|---|
| `include_history` (bool, default `false`) | WS connect | Send a one-time `history` message (full `replay()` output) immediately after the initial snapshot |
| `poll_interval_ms` (int, optional) | WS connect | Per-connection override of the server default (`WS_POLL_INTERVAL_MS`); clamped to `[250, 5000]` server-side to prevent abuse in either direction |

---

## 6. Data Models, Contracts, Schemas, and APIs

### `api/schemas/pipeline_status.py`

```python
from __future__ import annotations
from typing import Any, Literal
from pydantic import BaseModel

class NodeStatus(BaseModel):
    node_id: str
    state: str                       # NodeState value: BLOCKED|READY|DISPATCHED|RUNNING|SUCCEEDED|FAILED|CANCELLED|INVALIDATED|QUARANTINED
    attempt_count: int
    dispatch_ordinal: int | None
    output_ref: dict[str, Any] | None
    failure: dict[str, Any] | None

class RunStatus(BaseModel):
    run_id: str
    workflow_id: str
    state: str                       # RunState value
    revision: int
    cancel_requested: bool
    current_checkpoint_id: str | None
    nodes: list[NodeStatus]

class RunStatusEnvelope(BaseModel):
    retrieved_at_utc: str             # this API layer's observation timestamp — not from the domain
    run: RunStatus

class RunEventItem(BaseModel):
    sequence: int
    event_type: str                   # e.g. RunCreated, RunStarted, NodeDispatched, NodeStarted,
                                       # NodeSucceeded, NodeFailed, LateResultQuarantined,
                                       # RunPaused, RunResumed, CancellationRequested,
                                       # RunCancelled, RunCompleted, RunFailed, CheckpointAccepted
    aggregate_id: str
    payload: dict[str, Any]
    event_sha256: str

class RunEventsResponse(BaseModel):
    run_id: str
    event_count: int
    event_stream_sha256: str
    events: list[RunEventItem]
    current_state: RunStatus
    historical_events_rewritten: bool

# --- WebSocket message envelope shapes (sent as plain JSON, documented here for the frontend) ---

class WSSnapshotMessage(BaseModel):
    type: Literal["snapshot"] = "snapshot"
    retrieved_at_utc: str
    run: RunStatus

class WSHistoryMessage(BaseModel):
    type: Literal["history"] = "history"
    retrieved_at_utc: str
    event_count: int
    event_stream_sha256: str
    events: list[RunEventItem]

class WSNodeStateChangedMessage(BaseModel):
    type: Literal["node_state_changed"] = "node_state_changed"
    retrieved_at_utc: str
    run_id: str
    node: NodeStatus

class WSRunStateChangedMessage(BaseModel):
    type: Literal["run_state_changed"] = "run_state_changed"
    retrieved_at_utc: str
    run_id: str
    workflow_id: str
    state: str
    revision: int
    cancel_requested: bool
    current_checkpoint_id: str | None

class WSRunTerminalMessage(BaseModel):
    type: Literal["run_terminal"] = "run_terminal"
    retrieved_at_utc: str
    run: RunStatus
```

### Endpoints defined in this spec

| Method | Path | Response | Error codes |
|---|---|---|---|
| `WS` | `/api/runs/{run_id}/status` | Message stream (`WSSnapshotMessage` → `WSHistoryMessage`? → `WSNodeStateChangedMessage`\* / `WSRunStateChangedMessage`\* → `WSRunTerminalMessage`) | close `4404` |
| `WS` | `/api/campaigns/{campaign_id}/status` | Same message stream, after resolving `run_id` | close `4404`, `4409` |
| `GET` | `/api/runs/{run_id}/status` | `RunStatusEnvelope` (200) | `NOT_FOUND` (404) |
| `GET` | `/api/runs/{run_id}/status/events` | `RunEventsResponse` (200) | `NOT_FOUND` (404) |
| `GET` | `/api/campaigns/{campaign_id}/status` | `RunStatusEnvelope` (200) | `CAMPAIGN_HAS_NO_RUN` (404), `CAMPAIGN_HAS_MULTIPLE_RUNS` (409) |
| `GET` | `/api/campaigns/{campaign_id}/status/events` | `RunEventsResponse` (200) | `CAMPAIGN_HAS_NO_RUN` (404), `CAMPAIGN_HAS_MULTIPLE_RUNS` (409) |

Positive example — `GET /api/runs/{run_id}/status`:
```json
{
  "retrieved_at_utc": "2026-07-26T09:00:00Z",
  "run": {
    "run_id": "run:8f2a...",
    "workflow_id": "workflow:9c1b...",
    "state": "RUNNING",
    "revision": 5,
    "cancel_requested": false,
    "current_checkpoint_id": "checkpoint:44de...",
    "nodes": [
      {"node_id": "node-1", "state": "SUCCEEDED", "attempt_count": 1, "dispatch_ordinal": 1, "output_ref": {"object_id": "output:node-1", "sha256": "..."}, "failure": null},
      {"node_id": "node-2", "state": "RUNNING", "attempt_count": 1, "dispatch_ordinal": 2, "output_ref": null, "failure": null},
      {"node_id": "node-3", "state": "BLOCKED", "attempt_count": 0, "dispatch_ordinal": null, "output_ref": null, "failure": null}
    ]
  }
}
```

WebSocket message example — a node completing between two poll ticks:
```json
{"type": "node_state_changed", "retrieved_at_utc": "2026-07-26T09:00:01Z", "run_id": "run:8f2a...", "node": {"node_id": "node-2", "state": "SUCCEEDED", "attempt_count": 1, "dispatch_ordinal": 2, "output_ref": {"object_id": "output:node-2", "sha256": "..."}, "failure": null}}
```
followed by, on the same tick, since `revision` also changed:
```json
{"type": "run_state_changed", "retrieved_at_utc": "2026-07-26T09:00:01Z", "run_id": "run:8f2a...", "workflow_id": "workflow:9c1b...", "state": "RUNNING", "revision": 6, "cancel_requested": false, "current_checkpoint_id": "checkpoint:44de..."}
```

Negative example — `GET /api/campaigns/{campaign_id}/status` with no linked run:
```json
{
  "error_code": "CAMPAIGN_HAS_NO_RUN",
  "message": "No pipeline run is linked to campaign 'campaign:demo-1'. TS-APP-API-004 must write a campaign_produces_run edge when it creates a run for this campaign.",
  "service": "pipeline",
  "timestamp": "2026-07-26T09:00:00Z"
}
```

---

## 7. Implementation Stages and Exact Target Paths

All paths are relative to the repository root after the restructure in `CA_APP_FR_EPIC_SPEC_PLAN.md` Part 5.

### Stage 1 — Schemas

**`api/schemas/__init__.py`** — empty (create if `TS-APP-API-003` did not already create it; idempotent either way)

**`api/schemas/pipeline_status.py`** — exactly the models in Section 6.

### Stage 2 — Campaign→run resolver

**`api/services/__init__.py`** — empty (create if not already present)

**`api/services/campaign_run_lookup.py`**
```python
from __future__ import annotations
from cmf_pipeline.workflow.infrastructure.repository import PipelineRepository

CAMPAIGN_RUN_RELATION_TYPE = "campaign_produces_run"

class CampaignHasNoRun(Exception):
    def __init__(self, campaign_id: str):
        self.campaign_id = campaign_id
        super().__init__(f"No pipeline run is linked to campaign {campaign_id!r}.")

class CampaignHasMultipleRuns(Exception):
    def __init__(self, campaign_id: str, run_ids: list[str]):
        self.campaign_id = campaign_id
        self.run_ids = run_ids
        super().__init__(f"Campaign {campaign_id!r} has {len(run_ids)} linked runs; expected exactly one.")

def resolve_campaign_run_id(repository: PipelineRepository, campaign_id: str) -> str:
    """Read-only lookup over the pre-existing generic edge store.

    Writing the campaign_produces_run edge is TS-APP-API-004's responsibility,
    performed when it calls WorkflowRunService.create_run() for a Campaign Order:

        repository.add_edge(campaign_id, run_id, CAMPAIGN_RUN_RELATION_TYPE)

    This function does not write anything.
    """
    run_ids = repository.descendants([campaign_id], relation_types={CAMPAIGN_RUN_RELATION_TYPE})
    if not run_ids:
        raise CampaignHasNoRun(campaign_id)
    if len(run_ids) > 1:
        raise CampaignHasMultipleRuns(campaign_id, run_ids)
    return run_ids[0]
```

### Stage 3 — Config and dependency additions

**`api/config.py`** (edit — add one field with a default; existing callers unaffected)
```python
@dataclass(frozen=True)
class AppConfig:
    ca_data_root: Path
    ca_media_root: Path
    ca_delegation_root: Path
    gateway_version: str = "0.1.0"
    ws_poll_interval_ms: int = 750          # NEW

def load_config() -> AppConfig:
    data_root = Path(os.environ.get("CA_DATA_ROOT", "/state"))
    return AppConfig(
        ca_data_root=data_root,
        ca_media_root=Path(os.environ.get("CA_MEDIA_ROOT", data_root / "media")),
        ca_delegation_root=Path(
            os.environ.get("CA_DELEGATION_ROOT",
            Path(__file__).parent.parent / "packages" / "ca_delegation_rc4")
        ),
        ws_poll_interval_ms=int(os.environ.get("WS_POLL_INTERVAL_MS", "750")),   # NEW
    )
```

**`api/dependencies.py`** (edit — add one function; `get_pipeline` untouched)
```python
from fastapi import WebSocket

def get_pipeline_ws(websocket: WebSocket) -> PipelineApplication:
    return websocket.app.state.pipeline
```

### Stage 4 — The poll-and-diff bridge and router

**`api/websockets/__init__.py`** — empty

**`api/websockets/pipeline_status.py`**
```python
from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends, Query, Request, WebSocket, WebSocketDisconnect
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
import anyio

from ca_contracts import utc_now_rfc3339
from cmf_pipeline.application import PipelineApplication
from cmf_pipeline.domain.errors import PipelineNotFound

from api.dependencies import get_pipeline, get_pipeline_ws
from api.errors import ErrorResponse
from api.schemas.pipeline_status import RunEventsResponse, RunStatusEnvelope
from api.services.campaign_run_lookup import (
    CampaignHasMultipleRuns,
    CampaignHasNoRun,
    resolve_campaign_run_id,
)

router = APIRouter()

TERMINAL_RUN_STATES = {"COMPLETED", "FAILED", "CANCELLED", "INVALIDATED"}
MIN_POLL_INTERVAL_MS = 250
MAX_POLL_INTERVAL_MS = 5000


async def _snapshot(pipeline: PipelineApplication, run_id: str) -> dict[str, Any]:
    return await run_in_threadpool(pipeline.runs.status, run_id)


async def _replay(pipeline: PipelineApplication, run_id: str) -> dict[str, Any]:
    return await run_in_threadpool(pipeline.runs.replay, run_id)


def _diff_messages(run_id: str, previous: dict[str, Any] | None, current: dict[str, Any]) -> list[dict[str, Any]]:
    if previous is None or current["revision"] == previous["revision"]:
        return []
    messages: list[dict[str, Any]] = []
    previous_nodes = {n["node_id"]: n for n in previous["nodes"]}
    for node in current["nodes"]:
        if previous_nodes.get(node["node_id"]) != node:
            messages.append({
                "type": "node_state_changed",
                "retrieved_at_utc": utc_now_rfc3339(),
                "run_id": run_id,
                "node": node,
            })
    run_fields = ("state", "revision", "cancel_requested", "current_checkpoint_id")
    if any(current[f] != previous[f] for f in run_fields):
        messages.append({
            "type": "run_state_changed",
            "retrieved_at_utc": utc_now_rfc3339(),
            "run_id": run_id,
            "workflow_id": current["workflow_id"],
            **{f: current[f] for f in run_fields},
        })
    return messages


async def _stream(websocket: WebSocket, pipeline: PipelineApplication, run_id: str) -> None:
    config = websocket.app.state.config
    poll_ms = int(websocket.query_params.get("poll_interval_ms", config.ws_poll_interval_ms))
    poll_ms = max(MIN_POLL_INTERVAL_MS, min(MAX_POLL_INTERVAL_MS, poll_ms))
    include_history = websocket.query_params.get("include_history", "false").lower() == "true"

    await websocket.accept()
    try:
        current = await _snapshot(pipeline, run_id)
    except PipelineNotFound:
        await websocket.close(code=4404, reason=f"run not found: {run_id}")
        return

    await websocket.send_json({"type": "snapshot", "retrieved_at_utc": utc_now_rfc3339(), "run": current})

    if include_history:
        history = await _replay(pipeline, run_id)
        await websocket.send_json({
            "type": "history",
            "retrieved_at_utc": utc_now_rfc3339(),
            "event_count": history["event_count"],
            "event_stream_sha256": history["event_stream_sha256"],
            "events": history["events"],
        })

    try:
        while True:
            if current["state"] in TERMINAL_RUN_STATES:
                await websocket.send_json({"type": "run_terminal", "retrieved_at_utc": utc_now_rfc3339(), "run": current})
                await websocket.close(code=1000, reason="run reached terminal state")
                return
            await anyio.sleep(poll_ms / 1000)
            new_snapshot = await _snapshot(pipeline, run_id)
            for message in _diff_messages(run_id, current, new_snapshot):
                await websocket.send_json(message)
            current = new_snapshot
    except WebSocketDisconnect:
        return


@router.websocket("/runs/{run_id}/status")
async def ws_run_status(websocket: WebSocket, run_id: str, pipeline: PipelineApplication = Depends(get_pipeline_ws)) -> None:
    await _stream(websocket, pipeline, run_id)


@router.websocket("/campaigns/{campaign_id}/status")
async def ws_campaign_status(websocket: WebSocket, campaign_id: str, pipeline: PipelineApplication = Depends(get_pipeline_ws)) -> None:
    await websocket.accept()
    try:
        run_id = await run_in_threadpool(resolve_campaign_run_id, pipeline.repository, campaign_id)
    except CampaignHasNoRun:
        await websocket.close(code=4404, reason=f"campaign has no linked run: {campaign_id}")
        return
    except CampaignHasMultipleRuns:
        await websocket.close(code=4409, reason=f"campaign has multiple linked runs: {campaign_id}")
        return
    # _stream() calls accept() again; FastAPI/Starlette accept() is idempotent-safe to call once —
    # restructure _stream() to take an "already accepted" flag rather than double-accept in the final implementation.
    await _stream(websocket, pipeline, run_id)


@router.get("/runs/{run_id}/status", response_model=RunStatusEnvelope)
async def get_run_status(run_id: str, request: Request, pipeline: PipelineApplication = Depends(get_pipeline)) -> JSONResponse:
    try:
        run = await _snapshot(pipeline, run_id)
    except PipelineNotFound as exc:
        return JSONResponse(status_code=404, content=ErrorResponse(error_code="NOT_FOUND", message=str(exc), service="pipeline", timestamp=utc_now_rfc3339()).model_dump())
    return JSONResponse(content=RunStatusEnvelope(retrieved_at_utc=utc_now_rfc3339(), run=run).model_dump())


@router.get("/runs/{run_id}/status/events", response_model=RunEventsResponse)
async def get_run_events(run_id: str, pipeline: PipelineApplication = Depends(get_pipeline)) -> JSONResponse:
    try:
        history = await _replay(pipeline, run_id)
    except PipelineNotFound as exc:
        return JSONResponse(status_code=404, content=ErrorResponse(error_code="NOT_FOUND", message=str(exc), service="pipeline", timestamp=utc_now_rfc3339()).model_dump())
    return JSONResponse(content=RunEventsResponse(**history).model_dump())


@router.get("/campaigns/{campaign_id}/status", response_model=RunStatusEnvelope)
async def get_campaign_status(campaign_id: str, pipeline: PipelineApplication = Depends(get_pipeline)) -> JSONResponse:
    try:
        run_id = await run_in_threadpool(resolve_campaign_run_id, pipeline.repository, campaign_id)
    except CampaignHasNoRun as exc:
        return JSONResponse(status_code=404, content=ErrorResponse(error_code="CAMPAIGN_HAS_NO_RUN", message=str(exc), service="pipeline", timestamp=utc_now_rfc3339()).model_dump())
    except CampaignHasMultipleRuns as exc:
        return JSONResponse(status_code=409, content=ErrorResponse(error_code="CAMPAIGN_HAS_MULTIPLE_RUNS", message=str(exc), service="pipeline", timestamp=utc_now_rfc3339()).model_dump())
    return await get_run_status(run_id, None, pipeline)  # type: ignore[arg-type]


@router.get("/campaigns/{campaign_id}/status/events", response_model=RunEventsResponse)
async def get_campaign_events(campaign_id: str, pipeline: PipelineApplication = Depends(get_pipeline)) -> JSONResponse:
    try:
        run_id = await run_in_threadpool(resolve_campaign_run_id, pipeline.repository, campaign_id)
    except CampaignHasNoRun as exc:
        return JSONResponse(status_code=404, content=ErrorResponse(error_code="CAMPAIGN_HAS_NO_RUN", message=str(exc), service="pipeline", timestamp=utc_now_rfc3339()).model_dump())
    except CampaignHasMultipleRuns as exc:
        return JSONResponse(status_code=409, content=ErrorResponse(error_code="CAMPAIGN_HAS_MULTIPLE_RUNS", message=str(exc), service="pipeline", timestamp=utc_now_rfc3339()).model_dump())
    return await get_run_events(run_id, pipeline)
```

**Implementation note carried into Stage 4, not silently fixed in the prose above:** `ws_campaign_status` calls `websocket.accept()` before delegating to `_stream()`, which also calls `accept()`. Starlette's `WebSocket.accept()` is safe to call once; calling it twice raises. The exact final code must refactor `_stream()` to accept an `already_accepted: bool` parameter (or split "accept + resolve" from "stream") so this path only accepts once. Flagged explicitly here rather than left as a silent bug in a code sample.

### Stage 5 — Wire into the gateway

**`api/main.py`** (edit — one import, one `include_router` line, following the exact pattern `TS-APP-API-003` used for `interviews.router`):
```python
from api.websockets import pipeline_status
...
app.include_router(pipeline_status.router, prefix="/api", tags=["pipeline-status"])
```

No changes to `infra/docker/docker-compose.yml` or `dockerfile.api` — WebSocket support ships with `uvicorn[standard]` (already pinned in `TS-APP-API-001`'s `dockerfile.api`), and no new volume or env var beyond `WS_POLL_INTERVAL_MS` (optional, defaults to `750`) is required.

---

## 8. Failure, Migration, Rollback, Recovery, and Observability

### Typed failures

| Failure | Cause | Behaviour | Recovery |
|---|---|---|---|
| `NOT_FOUND` / WS `4404` | `run_id` does not exist in `pipeline_runs` | REST: 404 `ErrorResponse`. WS: `close(4404, ...)` before any messages are sent | Verify the `run_id`; if it came from `demo.py`/tests, re-check the run was actually created |
| `CAMPAIGN_HAS_NO_RUN` / WS `4404` | `campaign_id` has no `campaign_produces_run` edge | REST: 404. WS: `close(4404, ...)` | Confirm `TS-APP-API-004` is implemented and actually wrote the edge when the run was created; until then this is the expected, correct answer |
| `CAMPAIGN_HAS_MULTIPLE_RUNS` / WS `4409` | More than one `run_id` is linked to `campaign_id` | REST: 409. WS: `close(4409, ...)` | Out of scope for this spec — a future multi-run-campaign spec must add a real "which run" selection; until then, only single-run campaigns are supported |
| Poll query raises mid-stream (e.g. transient `sqlite3.OperationalError` under lock contention) | WAL-mode SQLite is generally read-concurrent-safe, but a lock timeout is still theoretically possible under heavy write load | Logged at `WARNING` with `run_id`; the current tick is skipped, the loop continues at the next interval rather than closing the socket | Self-healing; if it repeats every tick, investigate write contention on the shared `pipeline.db` file |
| Client disconnects (`WebSocketDisconnect`) | Normal browser navigation, network drop, tab close | Loop exits cleanly; no server-side state to clean up (no shared registry, no per-run subscriber list) | None needed — reconnect starts a fresh, independent loop |
| Run never reaches a terminal state (Gap A — no worker exists) | Nothing is driving the run forward | Connection stays open indefinitely, sending nothing (no diffs, because nothing is changing) until the client disconnects | Expected today; resolved once a Worker/Dispatcher spec exists. Not a bug in this spec |

### Migration
This spec adds `api/schemas/pipeline_status.py`, `api/services/campaign_run_lookup.py`, `api/websockets/pipeline_status.py`, and edits three existing files (`api/config.py`, `api/dependencies.py`, `api/main.py`) purely additively. No database migration — no new table, no new column, no FK. The `campaign_produces_run` `relation_type` string is a convention layered onto the pre-existing, schema-free `pipeline_edges` table.

### Rollback
Remove the three additive lines from `api/config.py`/`api/dependencies.py`/`api/main.py` and delete the three new files. Nothing else in the system depends on this spec's existence yet (it is a leaf in the dependency graph until `TS-APP-UI-003` is built), so rollback carries no data-migration risk.

### Observability
- WS connect logged at `INFO`: `run_id` (or `campaign_id` + resolved `run_id`), `poll_interval_ms`, `include_history`.
- WS close logged at `INFO` with the close code and reason (`1000` normal/terminal, `4404`/`4409` resolution failure, or an unexpected code on disconnect).
- Each poll tick that produces at least one diff message logged at `DEBUG` with the count and types of messages sent (not the full payload, to keep logs readable).
- Skipped ticks (transient query failure) logged at `WARNING`, consistent with `TS-APP-API-001`'s convention of not crashing the process on a single service hiccup.
- `Gap A` (no worker) is not separately logged per-connection — it would just be log noise for every open connection on a system with no dispatcher yet. It is documented here and in Section 1 instead.

---

## 9. Acceptance Criteria

**AC-001 — WS streams a manually-driven node transition (Gate D groundwork)**
Given a workflow registered and a run created via `WorkflowRunService` directly (following the `demo.py` reference pattern — no worker exists to do this automatically, per Gap A),
When a WS client connects to `GET /api/runs/{run_id}/status` [sic: `ws://.../api/runs/{run_id}/status`] and the test then calls `pipeline.runs.dispatch_node(...)` → `start_node(...)` → `complete_node(...)` for one node from a separate thread,
Then the client receives an initial `snapshot`, followed within `2 × WS_POLL_INTERVAL_MS` (1.5s at the 750ms default) by a `node_state_changed` message reflecting `state: "SUCCEEDED"` for that node and a `run_state_changed` message reflecting the bumped `revision`.
Failure example: no `node_state_changed` message arrives within 5 seconds.
Evidence: captured WS message sequence in the test log.
Test layer: integration — `tests/api/test_pipeline_status_ws.py::test_node_transition_streams_within_poll_window`.

**AC-002 — GET polling-fallback matches WS snapshot shape**
Given the same run as AC-001,
When `GET /api/runs/{run_id}/status` is called,
Then the response is HTTP 200 with a `RunStatusEnvelope` whose `run` field is byte-for-byte structurally identical (ignoring the wrapper `retrieved_at_utc`) to the `run` field of the WS `snapshot` message captured at the same moment.
Failure example: GET and WS report different `state` for the same node at the same instant.
Evidence: response body compared against a WS-captured snapshot in the same test.
Test layer: integration — `tests/api/test_pipeline_status_ws.py::test_get_fallback_matches_ws_snapshot`.

**AC-003 — Historical event log is complete and hash-verified**
Given a run driven through three node completions,
When `GET /api/runs/{run_id}/status/events` is called,
Then the response's `event_count` equals the number of `_append_event` calls made (`RunCreated`, `RunStarted`, then `NodeDispatched`/`NodeStarted`/`NodeSucceeded` ×3, ...), and `event_stream_sha256` matches the value independently computed by calling `pipeline.runs.replay(run_id)` directly in the test.
Failure example: `event_count` omits an event, or the hash does not match a direct `replay()` call.
Evidence: response body compared against a direct `replay()` call in the same test.
Test layer: integration — `tests/api/test_pipeline_status_ws.py::test_events_endpoint_matches_replay`.

**AC-004 — Unknown run_id fails clearly on both protocols**
Given no run exists with `run_id = "run:does-not-exist"`,
When `GET /api/runs/run:does-not-exist/status` is called, then `NOT_FOUND` 404 is returned.
When a WS client connects to `/api/runs/run:does-not-exist/status`,
Then the connection is accepted and immediately closed with code `4404` before any message is sent.
Failure example: WS connection stays open and silently sends nothing forever instead of closing with `4404`.
Evidence: HTTP status code and WS close code/reason captured in the test.
Test layer: integration — `tests/api/test_pipeline_status_ws.py::test_unknown_run_id_404_and_ws_4404`.

**AC-005 — campaign_id resolves correctly when the edge exists**
Given a run created for `campaign_id = "campaign:demo-1"` and the test manually writes `pipeline.repository.add_edge("campaign:demo-1", run_id, "campaign_produces_run")` (simulating what `TS-APP-API-004` will do once it exists),
When `GET /api/campaigns/campaign:demo-1/status` is called,
Then the response is identical in shape and content to `GET /api/runs/{run_id}/status` for the resolved `run_id`.
Failure example: the campaign-keyed and run-keyed endpoints disagree.
Evidence: response bodies compared in the same test.
Test layer: integration — `tests/api/test_pipeline_status_ws.py::test_campaign_resolves_to_run`.

**AC-006 — campaign_id with no linked run returns a legible 404, not a crash**
Given `campaign_id = "campaign:never-started"` with no `campaign_produces_run` edge anywhere in the graph (the current real-world default, since `TS-APP-API-004` does not exist yet),
When `GET /api/campaigns/campaign:never-started/status` is called,
Then the response is HTTP 404 with `error_code: "CAMPAIGN_HAS_NO_RUN"`.
Failure example: HTTP 500, or a 404 with a generic message that doesn't name the missing edge.
Evidence: response body.
Test layer: integration — `tests/api/test_pipeline_status_ws.py::test_campaign_with_no_run_returns_typed_404`.

**AC-007 — campaign_id with two linked runs returns 409, not a guess**
Given `campaign_id = "campaign:multi"` with two `campaign_produces_run` edges (test manually writes both, simulating a not-yet-supported multi-route campaign),
When `GET /api/campaigns/campaign:multi/status` is called,
Then the response is HTTP 409 with `error_code: "CAMPAIGN_HAS_MULTIPLE_RUNS"`, and no `run` field is guessed or returned.
Failure example: the endpoint silently picks one of the two runs.
Evidence: response body.
Test layer: integration — `tests/api/test_pipeline_status_ws.py::test_campaign_with_multiple_runs_returns_409`.

**AC-008 — WS closes cleanly on terminal run state**
Given a run driven to completion (all nodes `SUCCEEDED`, which `_finalize_success_if_possible` already transitions to `RunState.COMPLETED` automatically inside `complete_node`),
When a WS client is connected and the final `complete_node` call lands,
Then the client receives a `run_terminal` message with `run.state == "COMPLETED"`, immediately followed by the server closing the connection with code `1000`.
Failure example: the socket stays open after the run completes, or closes without sending `run_terminal` first.
Evidence: captured WS message sequence and close code.
Test layer: integration — `tests/api/test_pipeline_status_ws.py::test_ws_closes_on_terminal_state`.

**AC-009 — No modification to existing service packages (regression)**
Given the Phase 9 test suite at `tests/` was passing before this spec,
When this spec is fully implemented and `python -m pytest tests/ -q` is run,
Then all pre-existing tests continue to pass, and `git diff` shows zero changes under any of `services/pipeline/`, `services/air/`, `services/vae/`, `services/interview/`, `services/builder/`, or `packages/`.
Failure example: any pre-existing test now fails, or any file under `services/*/src` was touched.
Evidence: pytest output (0 new failures) and a diff scoped to `services/*/src` and `packages/*/src` showing no changes.
Test layer: regression — run full existing suite plus a diff-scope check in CI.

---

## 10. Testing and Completion Evidence

### Test files to create

**`tests/api/__init__.py`** — empty (if not already created by an earlier spec)

**`tests/api/test_pipeline_status_ws.py`**
- `test_node_transition_streams_within_poll_window` — AC-001
- `test_get_fallback_matches_ws_snapshot` — AC-002
- `test_events_endpoint_matches_replay` — AC-003
- `test_unknown_run_id_404_and_ws_4404` — AC-004
- `test_campaign_resolves_to_run` — AC-005
- `test_campaign_with_no_run_returns_typed_404` — AC-006
- `test_campaign_with_multiple_runs_returns_409` — AC-007
- `test_ws_closes_on_terminal_state` — AC-008

**`tests/api/_pipeline_fixtures.py`** — shared fixture module
```python
"""
Builds a minimal, valid runtime workflow and drives it exactly the way
demo.py drives one — dispatch/start/complete per node — since no
automatic worker exists yet (Gap A) to do this for us.
"""
from cmf_pipeline.application import PipelineApplication

def make_two_node_run(pipeline: PipelineApplication, *, workflow_id_suffix: str) -> str:
    # Build a minimal valid runtime_workflow payload satisfying
    # validate_runtime_workflow()'s required-key set (two nodes, one edge,
    # NodeKind.DETERMINISTIC_MODULE, ProductBoundary.AHP, WorkflowRole.NOT_APPLICABLE),
    # register it via pipeline.runs.register_workflow(...), then
    # pipeline.runs.create_run(...) with binding_manifest_ref/context_refs
    # shaped per require_ref()'s {object_id, sha256, version} contract.
    # Returns the created run_id. (Full node/edge payload omitted here —
    # constructed inline in the test module using the same field names
    # validated in workflow/domain/models.py::validate_runtime_node/
    # validate_runtime_workflow, shown in Section 1's file-read notes.)
    ...

def drive_node_to_success(pipeline: PipelineApplication, run_id: str, node_id: str, ordinal: int) -> None:
    pipeline.runs.dispatch_node(
        run_id, node_id,
        context_refs=[], allowed_actions=["inspect"], forbidden_actions=[], tool_ids=["test-adapter"],
        idempotency_key=f"test-dispatch-{run_id}-{ordinal}",
    )
    pipeline.runs.start_node(run_id, node_id, idempotency_key=f"test-start-{run_id}-{ordinal}")
    pipeline.runs.complete_node(
        run_id, node_id,
        output_ref={"object_id": f"output:{node_id}", "sha256": "0" * 64, "version": "1.0.0"},
        validation_receipt_refs=[f"validation:{ordinal}"],
        idempotency_key=f"test-complete-{run_id}-{ordinal}",
    )
```

### Test tooling
```bash
pip install httpx pytest-anyio websockets --break-system-packages
```
FastAPI's `TestClient` (`starlette.testclient.TestClient`) supports WebSocket testing directly via `client.websocket_connect(path)` as a context manager — no separate `websockets` client library is strictly required for the test suite itself, but it's useful for a standalone manual-QA script against a running `docker compose` stack.

```python
from fastapi.testclient import TestClient
from api.main import app

def test_unknown_run_id_404_and_ws_4404():
    with TestClient(app) as client:
        response = client.get("/api/runs/run:does-not-exist/status")
        assert response.status_code == 404
        assert response.json()["error_code"] == "NOT_FOUND"

        with client.websocket_connect("/api/runs/run:does-not-exist/status") as ws:
            pass  # starlette's test websocket raises on unexpected close; assert code via ws.close reason in the real test
```

Because the poll loop runs on a real timer (`anyio.sleep`), AC-001/AC-002/AC-008 need the test to run the `dispatch_node`/`start_node`/`complete_node` sequence from a background thread (or via `anyio`'s test clock utilities) while the WS test client is concurrently reading messages — analogous to how `demo.py` drives a run synchronously, except here it must happen *while* a connection is open, not before.

### Pre-existing regression
```bash
python -m pytest tests/ -q --tb=short
git diff --stat -- services/ packages/
```
Zero new failures and an empty diff under `services/`/`packages/` are both hard gates (AC-009).

### Build Receipt claim ceiling
`PIPELINE_STATUS_STREAM_DEVELOPMENT_EVIDENCE`

This spec does not claim:
- an autonomous worker/dispatcher exists (Gap A — not built by this spec)
- `TS-APP-API-004` exists or that any real campaign has ever been created (Gap B — this spec only defines and reads the contract)
- Harness execution readiness for any real production category (Gap 4, from `TS-APP-API-002` — orthogonal, still open)
- workflow topology is retrievable through this endpoint (deferred to `TS-APP-API-006`)
- production-grade push infrastructure, authentication, or multi-viewer broadcast scalability

---
spec_end: true
next_spec: TS-APP-API-004 (Campaign CRUD API) — must be written next; it is the only spec that can close Gap B by actually writing the `campaign_produces_run` edge this spec depends on reading. TS-APP-API-006 (Control Tower and Supervision API) remains queued behind it.
prerequisite_for_next: none — this spec's `run_id`-keyed endpoints are already fully usable without TS-APP-API-004; TS-APP-API-004's author should read Section 3 ("Campaign→run resolution contract") before writing its `create_run()` call site.
recommended_new_spec: A Worker/Dispatcher spec (suggested id TS-APP-API-007) to close Gap A — nothing in the system today autonomously drives a registered workflow's nodes from BLOCKED to SUCCEEDED. Until it exists, this spec's live-execution acceptance criteria are demonstrated with manually-driven test fixtures, not a real running campaign.
