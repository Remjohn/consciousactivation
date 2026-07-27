# SuperVisual Runtime API Spec V1

The router should be registered under:

```text
/api/v1/supervisual
```

## Project endpoints

```http
POST /api/v1/supervisual/projects
GET  /api/v1/supervisual/projects
GET  /api/v1/supervisual/projects/{project_id}
PATCH /api/v1/supervisual/projects/{project_id}
```

## Variant endpoints

```http
POST /api/v1/supervisual/projects/{project_id}/variants
GET  /api/v1/supervisual/projects/{project_id}/variants
GET  /api/v1/supervisual/variants/{variant_id}
POST /api/v1/supervisual/variants/{variant_id}/clone
```

## Build/run endpoints

```http
POST /api/v1/supervisual/variants/{variant_id}/build-runs
GET  /api/v1/supervisual/build-runs/{build_run_id}
POST /api/v1/supervisual/build-runs/{build_run_id}/steps/{step_name}/run
```

## Runtime state endpoints

```http
GET  /api/v1/supervisual/variants/{variant_id}/snapshot
GET  /api/v1/supervisual/variants/{variant_id}/events
POST /api/v1/supervisual/variants/{variant_id}/commands
```

## Composition/render/eval/approval/export endpoints

```http
POST /api/v1/supervisual/variants/{variant_id}/composition/lock
POST /api/v1/supervisual/variants/{variant_id}/provider-blueprints
POST /api/v1/supervisual/variants/{variant_id}/render
POST /api/v1/supervisual/variants/{variant_id}/evaluate
POST /api/v1/supervisual/variants/{variant_id}/approve
POST /api/v1/supervisual/variants/{variant_id}/export
```
