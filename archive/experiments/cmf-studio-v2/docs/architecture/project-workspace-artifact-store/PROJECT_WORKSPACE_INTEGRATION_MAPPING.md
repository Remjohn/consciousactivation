# Project Workspace Integration Mapping

Project Workspace + Artifact Store V1 is the deterministic filesystem and reference backbone for generated outputs, source references, receipts, manifests, and lineage. This integration does not deeply wire enforcement into existing engines yet; it documents the safe call sites for follow-up work.

## 1. Client Onboarding

Recommended call sites:

```python
workspace = ClientWorkspaceService.create_workspace(...)
ClientWorkspaceService.materialize_workspace(workspace, base_dir=...)
```

The workspace materialization receipt should become the source of truth for whether the artifact store is configured and available.

## 2. Golden Path Run

Recommended call sites:

```python
run_directory = RunArtifactDirectoryService.compile_run_directory(workspace, run_id)
RunArtifactDirectoryService.materialize_run_directory(run_directory, base_dir=...)
ArtifactStoreService.register_run_output(...)
```

Golden path outputs should register timeline, proxy render receipt, final render receipt, approval packet, and export pack refs under one workspace/run manifest.

## 3. Capability Preflight

`artifact_store_configured` and `artifact_store_available` should come from workspace materialization status:

```python
CapabilityPreflightService.run_preflight(
    pipeline_id=PipelineId.FORMAT02_GOLDEN_PATH,
    artifact_store_configured=True,
    artifact_store_available=True,
)
```

Missing or unavailable artifact storage should block required pipelines that need durable output refs.

## 4. Provider Runtime

Recommended output locations:

- Ideogram outputs -> `assets/ideogram_plates/`
- Flux outputs -> `assets/flux_edits/`
- Provider receipts -> `receipts/`

Provider adapter storage should continue to hash saved bytes. Artifact Store should register refs, versions, lineage, and receipts after provider outputs are safely materialized.

## 5. Avatar 64-State Library

Recommended output locations:

- Avatar state images -> `libraries/avatar/` or `runs/<run_id>/assets/avatar/`
- Approval receipts -> `receipts/`
- Library manifest -> `libraries/avatar/`

The 64-state library builder should register every approved expression/pose state as an artifact ref with sha256 and lineage back to source plates.

## 6. Template Preview / Atlas

Recommended output locations:

- Template previews -> `libraries/templates/`
- Preview receipts -> `receipts/`

Template previews should be registered as non-final artifacts until operator approval promotes them.

## 7. Video Editing Engine

Recommended output locations:

- Timeline contracts -> `timeline/`
- Proxy renders -> `renders/`
- Final exports -> `exports/`
- Eval receipts -> `receipts/`

Video engine fake render receipts can be registered now as text artifacts. Real render workers should later register file-byte artifacts with sha256 and lineage from timeline contracts.

## 8. Source / Reference Ingestion

Recommended output locations:

- Uploaded references -> `references/`
- Source refs / rights receipts -> `receipts/`

Existing source artifact and source provenance services remain the authority for source truth. Artifact Store should point to materialized files and receipts without inventing source facts.

## Deferred Enforcement

- No existing engine is forced to use Artifact Store in this branch.
- No UI/API routes are added in this branch.
- No provider calls or render calls are added.
- Existing provider storage, source artifacts, and video export services are preserved.
