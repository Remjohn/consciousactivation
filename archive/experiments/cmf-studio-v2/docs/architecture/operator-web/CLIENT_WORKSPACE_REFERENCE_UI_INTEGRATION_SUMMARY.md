# Client Workspace Reference UI Integration Summary

Branch: `feat/client-workspace-reference-ui`

## Existing UI Screens Inspected

- `operator-web/src/App.jsx`
  - Existing `GuestWorkspace` view under nav id `guests`.
  - Extended as the operator-first Client Workspace + Reference Library surface.
- `operator-web/src/components/supervisual/SuperVisualReferenceBoardPanel.jsx`
  - SuperVisual-specific reference panel; not reused as a general reference library.
- `operator-web/src/data.js`
  - Existing guest/asset fixtures.
- `operator-web/src/api/operatorRuntime.js`
  - Existing command/fallback API pattern.
- `operator-web/src/api/videoTimeline.js`
  - Existing backend-with-fixture-fallback API pattern.

No duplicate client workspace or reference screen was created.

## Backend Routes Added

Route factory added in `src/ccp_studio/api/v1/client_workspace_reference.py`:

- `POST /api/v1/client-workspaces`
- `GET /api/v1/client-workspaces`
- `GET /api/v1/client-workspaces/{client_workspace_id}`
- `POST /api/v1/client-workspaces/{client_workspace_id}/brand-context-versions`
- `POST /api/v1/client-workspaces/{client_workspace_id}/references/register`
- `GET /api/v1/client-workspaces/{client_workspace_id}/references`
- `PATCH /api/v1/client-workspaces/{client_workspace_id}/references/{artifact_ref_id}`

The repo does not currently expose a central FastAPI app bootstrap, so the route follows the existing module-level router and route-factory pattern.

## Backend Services Added

- `ClientWorkspaceReferenceService`
  - Creates client workspaces through `ClientWorkspaceService`.
  - Creates lightweight Brand Context Version read models.
  - Registers references through `ArtifactStoreService`.
  - Updates tags, rights status, approval state, and notes.
  - Lists references and counts by rights/approval state.
  - Uses in-memory persistence consistent with current V1 scaffolds.

## Frontend Files Modified

- `operator-web/src/App.jsx`
  - Existing `GuestWorkspace` view now includes the Client Workspace + Reference Library panel.
- `operator-web/src/styles.css`
  - Added responsive layout styles for the operator workspace/reference panel.

## Frontend Files Added

- `operator-web/src/api/clientWorkspaceReferences.js`
- `operator-web/src/components/workspace/ClientWorkspaceReferencePanel.jsx`
- `operator-web/src/fixtures/clientWorkspaceReferences.fixture.js`

## Fixture Fallback Status

Preserved and extended.

- Backend available: API client returns backend read models.
- Backend offline/missing: API client returns deterministic fixture workspace/reference state.
- Existing operator-web fixtures were not removed.

## Tests Run

Baseline before changes:

- `PYTHONPATH=src python -m compileall -q src`
- `PYTHONPATH=src python -m pytest -q tests/cmf_studio`
- Result: `904 passed, 12 skipped`

Targeted backend:

- `PYTHONPATH=src python -m compileall -q src`
- `PYTHONPATH=src python -m pytest -q tests/cmf_studio/test_client_workspace_reference_ui_backend_v1.py`
- Result: `14 passed, 1 skipped`

Full backend:

- `PYTHONPATH=src python -m pytest -q tests/cmf_studio`
- Result: `918 passed, 13 skipped`

Frontend:

- `npm --prefix operator-web run build -- --outDir ../.tmp/operator-web-build-check --emptyOutDir`
- Result: Vite build passed. The Windows npm wrapper emitted a non-fatal `Test-Path : Acces refuse` warning before running Vite.

No frontend test/lint scripts exist in `operator-web/package.json`.

## Confirmations

- Project Workspace + Artifact Store V1 is used.
- References create `ArtifactRef`-backed records.
- Rights status is explicit.
- Approval state is explicit.
- Client workspace creation requires `client_id`, `client_slug`, `brand_id`, and `brand_context_version_id`.
- `client_slug` path safety is enforced by the Project Workspace contract.
- Reference path traversal is rejected.
- Materialized references require `sha256`.
- No providers were called.
- No generation was triggered.
- No existing client files were moved or deleted.
- No binary upload endpoint was added.

## Known Limitations

- Binary upload is deferred because no general safe upload convention was found.
- Persistence is in-memory for this V1 wiring.
- The frontend uses fixture fallback when the backend is offline.
- No provider calls.
- No generation trigger.
- No avatar/library batch flow.
- Operator-first UI only.

## Next Recommended Step

Provider sample approval UI, Template Atlas UI wiring, or Avatar 64-State Library Builder UI/backend wiring.

