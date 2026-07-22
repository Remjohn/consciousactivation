# SuperVisual Provider Materialization Flow

```text
SuperVisualBuilderService
↓
StyleRouteEngineService.compile_provider_job_blueprint
↓
SuperVisualProviderMaterializationService.materialize_from_blueprint
↓
ProviderOrchestrationService.run
↓
ProviderAdapter
↓
ProviderJobReceipt
↓
AssetIntelligenceService.materialize_variant later
↓
SkiaRenderContract
```

Provider materialization is not final rendering.
