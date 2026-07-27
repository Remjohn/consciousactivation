# Provider Runtime Existing System Audit

Branch: `feat/provider-runtime-ideogram-flux-v1`

## Existing provider contract files found

- `src/ccp_studio/contracts/provider_jobs.py`
  - Existing provider request/job/response/receipt contract family.
  - Includes `ProviderJob`, `ProviderReceipt`, `ProviderCostPolicy`, and `ProviderRetryPolicy`.
- `src/ccp_studio/contracts/provider_adapters.py`
  - Existing provider adapter execution/request/receipt contract family.
  - Includes provider IDs, provider capabilities, provider execution requests, provider cost estimates, and adapter health.
- `src/ccp_studio/contracts/generative_adapters.py`
  - Existing generative provider adapter output contracts.
- `src/ccp_studio/contracts/composition.py`
  - Existing Ideogram composition plate lineage contracts.
- `src/ccp_studio/contracts/composition_intelligence.py`
  - Existing composition provider contract boundaries.
  - Requires Ideogram for composition plate provider in V1 and Flux for reference edit in V1.
- `src/ccp_studio/contracts/capability_preflight.py`
  - Existing provider/runtime capability preflight and provider menu contracts.

## Existing provider adapter files found

- `src/ccp_studio/api/v1/generative_provider_adapters.py`
- `src/ccp_studio/services/generative_provider_service.py`
- `src/ccp_studio/providers/ideogram.py`
- `src/ccp_studio/providers/`

These are existing provider/adapter surfaces and are not replaced by this integration.

## Existing provider job/receipt files found

- `src/ccp_studio/api/v1/provider_jobs.py`
- `src/ccp_studio/api/v1/provider_recovery.py`
- `src/ccp_studio/services/provider_operations_service.py`
- `src/ccp_studio/services/provider_recovery_service.py`
- `src/ccp_studio/workflows/provider_job_workflow.py`
- `tests/cmf_studio/test_provider_job_retry_resume_cancel_and_compensation.py`
- `tests/cmf_studio/test_generative_provider_adapters.py`

## Existing Ideogram references found

- `src/ccp_studio/providers/ideogram.py`
- `src/ccp_studio/api/v1/compositions.py`
- `src/ccp_studio/contracts/composition.py`
- `src/ccp_studio/contracts/composition_intelligence.py`
- `tests/cmf_studio/test_ideogram_4_compositionjob_lineage.py`
- `docs/ux/ux-design-specification.md`
- `registries/composition/single_image_ideogram_prompt_contracts.v2.json`
- `registries/composition/single_image_provider_responsibilities.v2.json`

## Existing Flux/BFL references found

- `src/ccp_studio/contracts/provider_adapters.py`
  - Existing `ProviderId.BFL_FLUX`.
- `src/ccp_studio/contracts/generative_adapters.py`
  - Existing `Flux2Klein9BParameters`.
- `src/ccp_studio/contracts/composition_intelligence.py`
  - Existing Flux reference edit provider boundary.
- `registries/composition/single_image_provider_responsibilities.v2.json`

## Existing cost/retry/sample approval systems found

- `src/ccp_studio/contracts/provider_jobs.py`
  - Existing provider cost and retry policy objects.
- `src/ccp_studio/contracts/provider_adapters.py`
  - Existing provider cost estimate and retry policy objects.
- `src/ccp_studio/contracts/capability_preflight.py`
  - Existing sample-first and cost estimate concepts.
- `tests/cmf_studio/test_capability_preflight_provider_batch_integration_v1.py`
  - Existing sample approval blocking coverage for provider scene batches.
- `tests/cmf_studio/test_avatar_asset_capability_preflight_integration_v1.py`
  - Existing sample approval preflight coverage for avatar batch generation.

## Existing operator-web provider UI files found

- `operator-web/src/components/supervisual/SuperVisualProviderJobsPanel.jsx`
- `operator-web/src/api/supervisualRuntime.js`
- `operator-web/src/components/supervisual/SuperVisualInspector.jsx`

These are read/inspection panels, not a provider runtime API for this bundle.

## Naming conflicts

The repo already has classes named `ProviderJob`, `ProviderRetryPolicy`, `ProviderCostEstimate`, `ProviderCapabilityProfile`, and `ProviderJobReceipt` in older provider contract modules. The bundle uses a new module, `src/ccp_studio/contracts/provider_runtime.py`, so the integration can be additive without overwriting those existing owners.

## Additive integration decision

This bundle can be applied additively as a governed fake-runtime layer for Ideogram/Flux job planning and fake execution. It must not replace:

- provider operations
- provider recovery
- existing provider adapters
- Ideogram composition lineage
- capability preflight

## Files requiring merge instead of copy

No target provider runtime files currently exist under the requested bundle paths. Existing provider systems are left untouched. The only merge requirement is conceptual: document that `provider_runtime.py` is a governed fake-runtime layer, not the existing provider adapter or provider operations implementation.
