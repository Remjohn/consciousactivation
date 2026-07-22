# SuperVisual Runtime UI Handoff

Phase 2 should connect SuperVisual Studio UI to backend endpoints.

The UI should render from:

```text
SuperVisualProjectDetailResponse
SuperVisualSnapshot
SuperVisualEvent[]
```

The UI should not mutate raw state directly.

Operator actions must become typed `SuperVisualCommand` records.

Fixture data should be replaced with:

```text
GET /api/v1/supervisual/projects
GET /api/v1/supervisual/projects/{project_id}
GET /api/v1/supervisual/variants/{variant_id}/snapshot
POST /api/v1/supervisual/variants/{variant_id}/build-runs
POST /api/v1/supervisual/build-runs/{build_run_id}/steps/{step_name}/run
POST /api/v1/supervisual/variants/{variant_id}/commands
POST /api/v1/supervisual/variants/{variant_id}/approve
```
