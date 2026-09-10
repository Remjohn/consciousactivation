# Mandate ID & Title
CAE-M066 — Operator Control, Native Editing and Human Resolution Persistence

## Summary Table
| File changed | What changed | Invariant proven |
|---|---|---|
| `api/services/human_resolution.py` | Added native-edit compiler, bounded substitution/timing validation, canonical before/after diffing, CAS commit, immutable HumanResolutionEpisode storage, and idempotent replay. | `INV-HUMAN-RESOLUTION-001`: every accepted operator intervention has bounded validation, CAS protection, immutable evidence, and canonical state persistence. |
| `api/routers/revisions.py` | Wired native substitution/timing compile and execute endpoints to authoritative campaign state and the HumanResolutionEpisode commit service. | UI actions can no longer be accepted as UI-only changes; execute produces canonical state + episode or a stale/validation rejection. |
| `api/routers/campaigns.py` | Replaced the timeline placeholder with the canonical campaign timeline and exposed the native editable timeline/action in Control Tower. | Operator view reads authoritative state and can refresh/reopen from the persisted projection. |
| `api/schemas/supervision.py` | Added native manipulation types and nested argument support; allowed the native editable timeline state. | Asset-reference and timing payloads validate without widening unrelated action contracts. |
| `apps/web/src/components/control-tower/Timeline.tsx` | Turned the timeline into an operator-operable native edit surface with selection, bounded timing adjustment, asset substitution, preview, and explicit save. | Manual edits require explicit confirmation and route through the persisted native-edit path; no direct UI mutation is authoritative. |
| `apps/web/src/api/campaigns.ts` | Added native compile/execute API contracts and timeline item types. | Frontend uses the same canonical campaign/revision contract as the backend. |
| `apps/web/src/hooks/useRevision.ts` | Added `useNativeEdit` compile/execute mutation with campaign query invalidation after persistence. | Successful intervention invalidates/reloads authoritative campaign state instead of retaining stale UI state. |
| `apps/web/src/pages/CampaignDetail.tsx` | Passes the canonical campaign state version into the editing surface. | CAS expectation is sourced from current authoritative state shown to the operator. |
| `apps/web/src/lib/actionRegistry.ts` | Marked `DIRECT_MANIPULATION` implemented and routed it to the timeline surface. | The declared operator action is actually connected to the native editor. |
| `apps/web/src/components/control-tower/__tests__/Timeline.test.tsx` | Added coverage for editable rendering, selection, preview-without-auto-save, asset validation, and explicit confirmation. | UI behavior preserves the operator confirmation boundary and native-edit contract. |
| `apps/web/src/lib/__tests__/actionRegistry.test.ts` | Updated action-registry expectations for the now-implemented direct manipulation surface. | The operator action registry reflects the actual supported capability. |
| `tests/cae/test_m066_human_resolution.py` | Added self-contained integration-style tests for bounds, editability, diff evidence, canonical persistence, CAS conflict, immutable episode count, and idempotent replay. | Backend acceptance criteria are executable and the false-proof/UI-only countercase is covered by direct persisted-state assertions. |

## Files Added and Files Modified

### Files Added
- `api/services/human_resolution.py` — New bounded native-edit and human-resolution persistence service. It is intentionally scoped to M0066 and reuses the existing pipeline object store/CAS mechanism; no new database subsystem was introduced.
- `tests/cae/test_m066_human_resolution.py` — Self-contained M0066 regression/integration coverage.

### Files Modified
- `api/routers/revisions.py` — Native substitution/timing compilation and atomic execution path.
- `api/routers/campaigns.py` — Canonical timeline projection and Control Tower action exposure.
- `api/schemas/supervision.py` — Native manipulation/schema support, including nested source references.
- `apps/web/src/api/campaigns.ts` — Native timeline/edit API types and calls.
- `apps/web/src/hooks/useRevision.ts` — Native compile/execute React Query hook.
- `apps/web/src/pages/CampaignDetail.tsx` — Supplies current state version to the editor.
- `apps/web/src/lib/actionRegistry.ts` — Enables direct manipulation routing.
- `apps/web/src/lib/__tests__/actionRegistry.test.ts` — Registry regression coverage.
- `apps/web/src/components/control-tower/Timeline.tsx` — Operator-native edit UI.
- `apps/web/src/components/control-tower/__tests__/Timeline.test.tsx` — UI acceptance tests.

## Exact paste instructions and post-apply commands
1. From the repository root, copy each bundle path exactly as packaged, preserving directory structure. Overwrite the listed modified files and add the two new files.
2. No SQL migration is required. M0066 stores HumanResolutionEpisode objects in the existing `pipeline_objects` revision/CAS store and reuses the existing campaign-state object.
3. Install the repository's normal backend dependencies, then run:
   `pytest -q tests/cae/test_m066_human_resolution.py --disable-warnings`
4. Install the frontend dependencies from `apps/web/package.json`, then run:
   `cd apps/web && npm test -- --run src/components/control-tower/__tests__/Timeline.test.tsx src/lib/__tests__/actionRegistry.test.ts`
5. Run frontend type checking:
   `cd apps/web && npm run typecheck`
6. Start the application normally, open a campaign in Control Tower, select an editable timeline item, preview a bounded timing or asset substitution, and use the explicit `Confirm & Save` action. Refresh/reopen the campaign and verify the persisted timeline matches the saved change and the response contains the HumanResolutionEpisode receipt. A concurrent stale state-version request must return `409 STALE_STATE_VERSION`.
7. Do not promote the HumanResolutionEpisode into doctrine/authority or bypass the existing QA/release path; the persisted campaign state is marked `QA_REQUIRED` after the human revision.

## Test Command (exact pytest/test command to verify)
Backend M0066 verification:
`pytest -q tests/cae/test_m066_human_resolution.py --disable-warnings`

Frontend M0066 verification:
`cd apps/web && npm test -- --run src/components/control-tower/__tests__/Timeline.test.tsx src/lib/__tests__/actionRegistry.test.ts`

Frontend type verification:
`cd apps/web && npm run typecheck`

## Expected Test Results
- Backend automated tests in this bundle: **6; all 6 passing** in the supplied sandbox.
- Frontend automated tests added/updated: **6 assertions across 2 test files** (5 Timeline scenarios plus the direct-manipulation registry regression); these were not executable in the supplied sandbox because `apps/web/node_modules` was absent, the npm registry was unreachable, and the npm package cache did not contain the required `zod` artifact.
- Full repository pytest was also blocked in the supplied sandbox by missing optional runtime packages (`psycopg`, then the absent `cmf_builder` package in the uploaded brownfield tree). No dependency shims were included in this bundle.
- The uploaded repository contained no `.git` metadata, so no source commit SHA can be captured from the supplied archive. Apply this bundle in the target repository and record the resulting repository commit as the implementation commit.

## Operator Gate
**Decision required:** ACCEPT / ACCEPT WITH LIMITATIONS / REPAIR / BLOCK.

Recommended current disposition: **ACCEPT WITH LIMITATIONS** pending execution of the frontend tests/typecheck in a fully provisioned repository environment and operator visual validation of the Control Tower flow. The backend M0066 invariant proof is passing, and the frontend implementation is intentionally blocked from claiming runtime verification until its dependencies are available.

## Bundle Artifact Identity
Content manifest SHA-256: `d3f14a9e4104f02e32d22d0a62148e7c241bbb58d8ff340c9f587c70b99936b0`
