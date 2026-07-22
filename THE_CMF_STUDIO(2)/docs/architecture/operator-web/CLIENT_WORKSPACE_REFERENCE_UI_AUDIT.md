# Client Workspace Reference UI Audit

Branch: `feat/client-workspace-reference-ui`

## Existing Client / Workspace Screens Found

- `operator-web/src/App.jsx`
  - Existing route/view id: `guests`
  - Nav label: `Guests`
  - Topbar label: `Brand Workspace`
  - Existing component: `GuestWorkspace`
  - Existing purpose: internal operator management of guest/brand workspace fields, consent state, Voice DNA, Emotional DNA, safety checklist, and guest asset ledger.

No separate client workspace product surface was found. The existing `GuestWorkspace` surface is the correct extension point.

## Existing Reference / Upload Screens Found

- `operator-web/src/components/supervisual/SuperVisualReferenceBoardPanel.jsx`
  - SuperVisual-specific reference board panel.
  - Not a general client workspace/reference library.
- `operator-web/src/App.jsx`
  - Shows `Guest Asset Ledger` from fixture data.
  - No backend-backed reference registration form existed before this prompt.

## Existing Frontend Routes

- `guests` -> `GuestWorkspace` in `operator-web/src/App.jsx`
- No duplicate `/workspace`, `/client-workspace`, or `/reference-library` route was found in operator-web.

## Existing API Clients

- `operator-web/src/api/operatorRuntime.js`
  - Posts operator UI commands to `/api/v1/operator-ui/...`
  - Falls back to an offline command ledger.
- `operator-web/src/api/videoTimeline.js`
  - Uses backend endpoints when available and fixture fallback when unavailable.
- `operator-web/src/api/supervisualRuntime.js`
  - SuperVisual runtime API client.

No general client workspace/reference API client was found.

## Existing Fixture Files

- `operator-web/src/data.js`
  - Contains guest, content asset, format, pipeline, and eval fixture data.
- `operator-web/src/fixtures/videoTimelineWorkbench.fixture.js`
  - Video Timeline Workbench fixture fallback.

No general client workspace/reference fixture file was found.

## Existing Forms / Fields

`GuestWorkspace` already has:

- display name
- handle
- Voice DNA
- Emotional DNA
- guest safety indicators
- guest asset ledger

Missing before this prompt:

- `client_id`
- `client_slug`
- `brand_id`
- `brand_context_version_id`
- brand context version creation
- reference registration
- rights status
- approval state
- source refs
- ArtifactRef-backed read model visibility

## Existing Approval / Rights UI

- Existing asset cards show content asset state (`Review`, `Blocked`, `Draft`, `Approved`).
- No explicit reference rights status UI existed.
- No explicit reference approval state UI existed.

## Missing UI Pieces

- Create Client Workspace form.
- Brand Context Version form.
- Register Reference metadata form.
- Reference list with rights status, approval state, tags, and source refs.
- Counts by rights status and approval state.
- Fixture fallback for reference library state.

## Duplicate-Risk Areas

- Do not add a second client workspace screen while `GuestWorkspace` exists.
- Do not repurpose SuperVisual reference board as the general reference library.
- Do not remove existing fixture data; use it as offline fallback.

## Recommended Approach

Extend the existing `GuestWorkspace` screen with a contained client workspace/reference panel. Keep it operator-first and backend-backed when available, with deterministic fixture fallback when offline.

