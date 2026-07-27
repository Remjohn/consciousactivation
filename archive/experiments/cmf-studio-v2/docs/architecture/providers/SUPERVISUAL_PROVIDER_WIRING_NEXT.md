# SuperVisual Provider Wiring Next

## Purpose

The real provider adapter layer is now available as an orchestration boundary, but `SuperVisualBuilderService` must not call OpenAI, Ideogram, BFL, Qwen, Segment Anything, or any provider adapter directly.

The next implementation should wire SuperVisual builds through:

```python
SuperVisualProviderMaterializationService.materialize_from_blueprint(...)
```

## Required Preconditions

Provider materialization can only happen after the upstream production gates have produced typed receipts:

1. `CompositionDecisionReceipt` exists and the composition is locked.
2. `StyleRouteEngineService` has compiled a provider job blueprint or blueprint-like contract.
3. Asset Intelligence has confirmed source, reference, and input assets.
4. Visual Preproduction and composition gates have resolved frame profile, composition role, and source grounding.
5. The provider request has `brand_context_version_id`.
6. The provider request has `operator_approval_ref` or `trusted_auto_approval_policy_id` for real or paid providers.
7. Default automated tests use `ProviderId.FAKE_IMAGE` with `allow_fake_without_approval=True`.

## Wiring Rule

`SuperVisualBuilderService` should pass blueprint fields into `SuperVisualProviderMaterializationService`, then persist the returned `ProviderJobReceipt` as an intermediate materialization receipt.

Provider output is not the final SuperVisual. Final composition, layer assembly, typography, Skia/renderer export, eval receipts, and approval/export receipts remain separate deterministic stages.

## Non-Goals

- Do not run live provider calls by default.
- Do not commit provider secrets.
- Do not let UI components call providers directly.
- Do not treat generated provider assets as approved assets until eval and operator gates pass.
- Do not bypass Asset Intelligence, Style Route, Visual Preproduction, or Composition gates.

## Manual Live Testing

Live testing is a later manual-only path and must require explicit environment configuration:

```text
OPENAI_API_KEY
IDEOGRAM_API_KEY
BFL_API_KEY
QWEN_API_KEY
QWEN_IMAGE_ENDPOINT
SEGMENT_ANYTHING_ENDPOINT
RUN_PROVIDER_LIVE_TESTS=1
```

Default CI and local verification must remain fake-provider only.
