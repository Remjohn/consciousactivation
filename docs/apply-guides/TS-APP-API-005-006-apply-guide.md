# Apply Guide — TS-APP-API-005 + TS-APP-API-006 (combined)

## Overview

This package contains two technical specifications implemented in one session:

- **TS-APP-API-005** (Pipeline Status WebSocket): WebSocket endpoint + REST GET fallback for streaming pipeline run node state transitions.
- **TS-APP-API-006** (Control Tower and Supervision API): Control Tower projection, revision compilation, ship decision, audit export, and exception resolution routes via a Studio TypeScript RPC bridge.

## Files Created

### TS-APP-API-005 (Pipeline Status WebSocket)

| File | Purpose |
|------|---------|
| `api/schemas/pipeline_status.py` | Pydantic models for WS messages, REST envelopes, node/run status |
| `api/services/campaign_run_lookup.py` | Campaign→run resolution via `pipeline_edges` table |
| `api/websockets/__init__.py` | Package init |
| `api/websockets/pipeline_status.py` | WS poll-and-diff bridge, REST fallback endpoints |
| `tests/api/_pipeline_fixtures.py` | `make_run()`, `drive_node_to_success()`, `get_topological_order()` helpers |
| `tests/api/test_pipeline_status_ws.py` | 9 acceptance tests (AC-001 through AC-009) |

### TS-APP-API-006 (Control Tower and Supervision API)

| File | Purpose |
|------|---------|
| `services/studio/src/rpc.ts` | RPC bridge entrypoint — 16 commands routed to Studio pure functions |
| `api/services/studio_bridge.py` | Python `StudioBridge` class — per-call Node subprocess |
| `api/services/campaign_projection.py` | Campaign persistence over `PipelineRepository` generic object store |
| `api/schemas/supervision.py` | All supervision Pydantic models (ControlTower, Timeline, Exception, Revision, Ship, Audit) |
| `api/routers/revisions.py` | `POST /revisions`, `POST /revisions/direct`, `POST /revisions/{program_id}/execute` |
| `api/routers/ship.py` | `POST /ship`, `GET /audit-export` |
| `tests/api/fixtures/studio_campaign_fixtures.py` | `make_running_campaign()`, `make_failed_node_run()` |
| `tests/api/test_control_tower.py` | 4 AC tests (AC-001 through AC-004) |
| `tests/api/test_timeline.py` | 2 AC tests (AC-005, AC-006) |
| `tests/api/test_revisions.py` | 5 AC tests (AC-007 through AC-011) |
| `tests/api/test_exceptions.py` | 2 AC tests (AC-012, AC-013) |
| `tests/api/test_ship.py` | 4 AC tests (AC-014 through AC-017) |

## Files Modified

| File | Change |
|------|--------|
| `api/config.py` | Added `ws_poll_interval_ms`, `ca_studio_rpc_entrypoint` config fields |
| `api/dependencies.py` | Added `get_pipeline_ws()`, `get_studio_bridge()` dependencies |
| `api/main.py` | Added Studio bridge construction in lifespan, registered pipeline_status, revisions, and ship routers |
| `api/routers/campaigns.py` | Added supervision routes: `GET /{campaign_id}/tower`, `GET /{campaign_id}/timeline`, `GET /{campaign_id}/exceptions`, `POST /{campaign_id}/exceptions/resolve`; fixed `exc.message` → `str(exc)` in error handler |
| `api/routers/revisions.py` | Fixed `exc.message` → `str(exc)` in error handlers |
| `api/routers/ship.py` | Fixed `exc.message` → `str(exc)` in error handlers |
| `infra/docker/dockerfile.api` | Added `nodejs npm` to apt-get, `services/studio` COPY, npm install+build step |
| `infra/docker/docker-compose.yml` | Added `CA_STUDIO_RPC_ENTRYPOINT` env var |
| `services/studio/package.json` | Added `"rpc": "node dist/rpc.js"` script |
| `services/studio/src/node-shims.d.ts` | Extended `Process` interface with `stdin`, `stdout`, `stderr` |
| `tests/api/test_control_tower.py` | Fixed 404 assertion to handle both top-level and `detail`-wrapped error codes |

## Pre-requisites

1. **Node.js ≥ 20.19** on `PATH`
2. **Studio TypeScript build** must be run:
   ```bash
   cd services/studio && npm install && npm run build
   ```
   This produces `services/studio/dist/rpc.js` (the RPC bridge entrypoint).

## Apply Steps

### 1. Copy all new files to the target repository

Use the file tree above. Ensure directory structure is preserved.

### 2. Apply modifications to existing files

Apply the diffs for:
- `api/config.py`, `api/dependencies.py`, `api/main.py` — infrastructure wiring
- `api/routers/campaigns.py`, `revisions.py`, `ship.py` — router changes
- `infra/docker/dockerfile.api`, `docker-compose.yml` — Docker changes
- `services/studio/package.json`, `node-shims.d.ts` — Studio changes
- `tests/api/test_control_tower.py` — test fix

### 3. Build the Studio bridge

```bash
cd services/studio
npm install
npm run build
```

### 4. Run tests

```bash
python -m pytest tests/api/ --tb=short
```

### 5. Verify all ACs pass

Expected: 56 passed (0 failed). The 3 pre-existing interview failures (`test_digest_mismatch_rejected`, `test_untimed_transcript_rejected`, `test_corrupt_media_rejected_before_admit`) are unrelated to this spec — they fail on the unmodified `main` branch with `KeyError: 'error_code'`.

## AC Coverage

### TS-APP-API-005
- AC-001: WS streams node transitions (poll window)
- AC-002: GET fallback matches WS snapshot
- AC-003: Events endpoint matches replay
- AC-004: Unknown run_id → 404 + WS 4404
- AC-005: Campaign resolves to run
- AC-006: Campaign with no run → 404 CAMPAIGN_HAS_NO_RUN
- AC-007: Campaign with multiple runs → 409 CAMPAIGN_HAS_MULTIPLE_RUNS
- AC-008: WS closes on terminal state with code 1000
- AC-009: No service/package files modified

### TS-APP-API-006
- AC-001: Control Tower returns projection with run nodes
- AC-002: Control Tower reflects failed node from pipeline
- AC-003: Unknown campaign → 404
- AC-004: Studio binding present in projection
- AC-005: Timeline returns projection
- AC-006: Unknown campaign → 404
- AC-007: Natural language revision compiles to program
- AC-008: Direct manipulation compiles to program
- AC-009: Execute revision acknowledges
- AC-010: Invalid revision body → 422
- AC-011: Invalid direct manipulation body → 422
- AC-012: List exceptions returns list
- AC-013: Resolve exception returns response
- AC-014: Ship request returns decision
- AC-015: Ship request without authority → DENIED
- AC-016: Audit export returns manifest
- AC-017: Unknown campaign → 404

## Key Design Decisions

### Poll-and-diff bridge (API-005)
Since `WorkflowRunService` has no pub/sub, the WebSocket polls `status(run_id)` on an interval and diffs against the last snapshot, sending only changed `node_state_changed`/`run_state_changed` messages.

### Studio RPC bridge (API-006)
Per-call Node subprocess (`node dist/rpc.js <command>`). JSON envelope: `{ok: true, result}` or `{ok: false, error: {code, message, context}}`. `StudioValidationError` → exit 0 (well-formed), unexpected crash → exit 1.

### Campaign persistence (API-006)
Uses `PipelineRepository.store_object()`/`get_object()` with content-addressed, revisioned object store. Object types: `studio_campaign_order`, `studio_campaign_state`. Marked as `ASSUMED_INTERFACE_PENDING_004` — TS-APP-API-004's author must adopt or reconcile.

### Pydantic `exclude_none=False` (API-006)
All bridge payloads destined for the Studio TypeScript side must pass `model_dump(mode="json")` with `exclude_none=False` to avoid `undefined`-shaped `None` values that `normalize()` in `canonical.ts` rejects.

### `canonicalSha256` (API-006)
Requires every object key sorted and every number a safe integer — no floats or `undefined` in Studio-signed objects.