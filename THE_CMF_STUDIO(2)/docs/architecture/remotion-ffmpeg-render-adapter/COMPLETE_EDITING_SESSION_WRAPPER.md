# Complete Editing Session Wrapper

The render adapter preserves the upstream PRD object spine:

```text
research_snapshot_refs
asset_manifest_refs
scene_spec_refs
composition_job_refs
provider_job_receipt_refs
evaluation_receipt_refs
```

The renderer must not flatten the source state into an untraceable blob.
