# SuperVisual Studio Backend UI Integration Summary

## Scope

Phase 2 connects `operator-web` SuperVisual Studio to the SuperVisual Runtime API. The backend runtime remains the source of truth:

```text
backend state -> UI snapshot -> operator command -> API call -> runtime event -> refreshed snapshot/events
```

The frontend does not call providers directly and does not call builder services directly.

## Files Added

```text
operator-web/.env.supervisual.example
operator-web/src/api/supervisualRuntime.js
operator-web/src/api/supervisualRuntime.test.js
operator-web/src/components/supervisual/
operator-web/src/hooks/useSuperVisualActions.js
operator-web/src/hooks/useSuperVisualEvents.js
operator-web/src/hooks/useSuperVisualProject.js
operator-web/src/hooks/useSuperVisualProjects.js
operator-web/src/hooks/useSuperVisualSnapshot.js
operator-web/src/lib/apiClient.js
operator-web/src/lib/idempotency.js
operator-web/src/lib/supervisualViewModel.js
operator-web/src/lib/supervisualViewModel.test.js
operator-web/src/screens/SuperVisualStudio.jsx
operator-web/src/styles/supervisual.css
operator-web/src/types/supervisualRuntime.js
```

## Files Modified

```text
src/ccp_studio/api/v1/supervisual_runtime.py
src/ccp_studio/contracts/supervisual_runtime.py
src/ccp_studio/services/supervisual_runtime_service.py
```

The backend changes are thin runtime route/DTO additions required by the UI. They do not wire paid providers, renderers, or builder services.

## API Endpoints Consumed

```text
POST /api/v1/supervisual/projects
GET  /api/v1/supervisual/projects
GET  /api/v1/supervisual/projects/{project_id}
PATCH /api/v1/supervisual/projects/{project_id}
POST /api/v1/supervisual/projects/{project_id}/variants
GET  /api/v1/supervisual/variants/{variant_id}
POST /api/v1/supervisual/variants/{variant_id}/clone
GET  /api/v1/supervisual/variants/{variant_id}/snapshot
GET  /api/v1/supervisual/variants/{variant_id}/events
POST /api/v1/supervisual/variants/{variant_id}/build-runs
GET  /api/v1/supervisual/build-runs/{build_run_id}
POST /api/v1/supervisual/build-runs/{build_run_id}/steps/{step_name}/run
POST /api/v1/supervisual/variants/{variant_id}/composition/hypotheses
POST /api/v1/supervisual/variants/{variant_id}/composition/lock
POST /api/v1/supervisual/variants/{variant_id}/provider-blueprints
POST /api/v1/supervisual/variants/{variant_id}/materialize
POST /api/v1/supervisual/variants/{variant_id}/render-contract
POST /api/v1/supervisual/variants/{variant_id}/render
POST /api/v1/supervisual/variants/{variant_id}/evaluate
POST /api/v1/supervisual/variants/{variant_id}/revisions
GET  /api/v1/supervisual/variants/{variant_id}/revisions
POST /api/v1/supervisual/variants/{variant_id}/approve
POST /api/v1/supervisual/variants/{variant_id}/export
```

## Verification

Frontend build:

```powershell
cd operator-web
npm run build
```

Result: passed. npm emits a local PowerShell `Test-Path` access warning before running Vite, but Vite completes successfully.

Frontend tests:

```text
Not run. operator-web/package.json has no test script and no Vitest dependency.
```

Reference Vitest-style tests were added for future adoption.

Backend verification:

```powershell
$env:PYTHONPATH="src"
python -m compileall -q src
python -m pytest -q tests/cmf_studio
```

Result during integration: `551 passed, 4 skipped`.

Manual backend/browser verification:

```text
Not fully run in this environment.
```

There is no canonical backend app entrypoint or router registry to launch with `uvicorn`. A direct FastAPI smoke app could not start because this local Python environment is missing FastAPI's `annotated_doc` dependency. The full backend suite still passes because FastAPI-specific tests are guarded/skipped when FastAPI cannot fully import.

## Behavior Notes

- `SuperVisualStudio.jsx` no longer imports fixture data or the older `api/supervisuals.js` project API.
- Runtime action availability is derived from backend `available_actions`.
- The UI normalizes backend runtime action names to client route actions without hard-coding availability.
- Every write call from the UI client attaches `actor_id` and `idempotency_key`.
- The create-project modal rejects 16:9 delivery frame profiles.
- Backend blockers, snapshots, events, and available actions are projected through the view model.
- Provider calls are not made from the frontend.

## Known Limitations

- The UI requires a running backend mounted with `create_supervisual_runtime_router(...)`.
- The repo still needs a canonical FastAPI app entrypoint or router registry for local browser-level verification.
- Frontend tests are reference files until a test runner is added to `operator-web`.
- Runtime actions advance the persistence/state-machine shell; richer builder, renderer, provider, and eval receipts should be wired in later phases.

## Next Recommended Work

Add a canonical backend app entrypoint that includes the SuperVisual runtime router, then run browser-level verification against `VITE_API_BASE_URL=http://localhost:8000`.
