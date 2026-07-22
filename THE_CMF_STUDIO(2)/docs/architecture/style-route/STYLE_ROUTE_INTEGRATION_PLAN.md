# Style Route V1 Integration Plan

Visual Preproduction says what the visual needs. Asset Intelligence says what usable assets and references exist. Style Route decides which visual language can express it correctly. Provider Orchestration later executes the provider job blueprint.

SuperVisualBuilderService should eventually call:

```python
StyleRouteEngineService.select_style_route(...)
StyleRouteEngineService.compile_route_production_spec(...)
StyleRouteEngineService.compile_provider_job_blueprint(...)
```
