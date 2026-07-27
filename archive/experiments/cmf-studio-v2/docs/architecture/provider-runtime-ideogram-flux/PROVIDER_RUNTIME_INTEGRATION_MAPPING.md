# Provider Runtime Integration Mapping

Branch: `feat/provider-runtime-ideogram-flux-v1`

## Capability Preflight

Provider runtime should not start a real provider job until preflight confirms the required capability is configured, tested, and available.

- Ideogram maps to `provider:image:ideogram`.
- Flux maps to `provider:image:flux`.
- Batch jobs remain blocked until the sample-first gate passes.
- V1 fake execution does not read secrets and does not call providers.

Recommended call site:

```python
CapabilityPreflightService().run_preflight(
    pipeline_id=PipelineId.FORMAT02_PROVIDER_SCENE_BATCH,
    ideogram_configured=True,
    ideogram_available=True,
    flux_configured=True,
    flux_available=True,
    batch_requested=True,
    sample_approved=True,
)
```

## Project Workspace / Artifact Store

`ProviderOutputAssetRef` should later map to `ArtifactRef` once generated assets are materialized or registered.

Suggested storage:

- Ideogram outputs: `client_workspaces/<client_slug>/runs/<run_id>/assets/ideogram_plates/`
- Flux outputs: `client_workspaces/<client_slug>/runs/<run_id>/assets/flux_edits/`
- Provider receipts: `client_workspaces/<client_slug>/runs/<run_id>/receipts/`

V1 does not write binary image files. It can register deterministic fake output refs with `sha256` and `source_refs`.

## Template Preview / Atlas

`template_preview_sample` can use a `TemplatePreviewResult` as a sample input. Template preview sample approval is necessary before batch generation, but it is not sufficient alone.

Batch approval still requires:

1. scene sample approval
2. face plate sample approval
3. template preview sample approval

## Avatar Asset Production

`face_plate_sample` should produce or reference face plate sample outputs. Face plate sample approval is required before avatar/provider batch generation.

For V1:

- Flux face plate samples fake-execute only.
- Output asset refs can use `asset_role=face_plate`.
- No real Flux or BFL call occurs.

## Format 02 Composition

Ideogram `scene_sample` jobs should be generated from `CompositionSceneProgram` or `Format02SceneProgram` references.

The scene sample approval gate is required before scene batch generation. Provider runtime should carry source refs from the composition scene into `ProviderJobInput.source_refs` and `ProviderOutputAssetRef.source_refs`.

## Operator Review

The operator should eventually see:

- `ProviderDecisionLog`
- `ProviderCostEstimate`
- `ProviderSampleApprovalGate`
- `ProviderBatchPolicyReceipt`
- `ProviderJobReceipt`
- `ProviderOutputAssetRef`

No silent provider/model substitution should occur. Decision logs must show the provider role and alternatives considered.

## Real provider adapters later

V1 fake output should be replaced by real Ideogram/Flux calls only in a future provider adapter bundle or prompt.

The governance contracts must stay in front of real provider execution:

- capability preflight
- sample-first approval
- decision log
- cost estimate
- retry policy
- receipt and output asset ref

Real clients should not be added in this V1 integration.
