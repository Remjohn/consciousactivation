# Capability Preflight Existing System Audit

## Existing Provider Adapter Files Found

- `src/ccp_studio/contracts/provider_adapters.py`
- `src/ccp_studio/providers/base.py`
- `src/ccp_studio/providers/registry.py`
- `src/ccp_studio/providers/fake_image_adapter.py`
- `src/ccp_studio/providers/openai_image_adapter.py`
- `src/ccp_studio/providers/ideogram_adapter.py`
- `src/ccp_studio/providers/bfl_flux_adapter.py`
- `src/ccp_studio/providers/qwen_image_adapter.py`
- `src/ccp_studio/providers/segment_anything_adapter.py`
- `src/ccp_studio/services/provider_orchestration_service.py`
- `src/ccp_studio/services/supervisual_provider_materialization_service.py`
- `registries/canonical/providers/`

## Existing Provider Job / Receipt Files Found

- `src/ccp_studio/contracts/provider_jobs.py`
- `src/ccp_studio/repositories/provider_jobs.py`
- `src/ccp_studio/services/provider_operations_service.py`
- `src/ccp_studio/workflows/provider_job_workflow.py`
- `src/ccp_studio/contracts/style_route_runtime.py`
- `src/ccp_studio/services/style_route_engine_service.py`
- `registries/canonical/skills/shared/style_route/08_style_route.provider_blueprint.compile.skill.yaml`

## Existing Render / Runtime Files Found

- `src/ccp_studio/contracts/video_editing_engine.py`
- `src/ccp_studio/services/video_render_contract_service.py`
- `src/ccp_studio/services/video_editing_engine_service.py`
- `src/ccp_studio/services/deterministic_rendering_service.py`
- `src/ccp_studio/workflows/render_workflow.py`
- `registries/canonical/video_editing/`
- `registries/canonical/skills/engines/video/`
- `docs/architecture/video-editing-engine/`

## Existing Cost / Sample / Approval Files Found

- `docs/architecture/providers/PROVIDER_SECURITY_AND_COST_POLICY.md`
- `registries/canonical/providers/provider_cost_profiles.v1.json`
- `docs/tech-specs/TS-CMF-131-budget-cost-and-resource-governance.md`
- `docs/architecture/cmf_studio_build_workflow/build_receipts/TS-CMF-131-budget-cost-and-resource-governance-build.md`
- `src/ccp_studio/contracts/approval_gate.py`
- `src/ccp_studio/services/approval_gate_service.py`
- `tests/cmf_studio/test_approval_blockers.py`

## Existing Tool Registry Files Found

- `docs/tech-specs/TS-CMF-068-pi-harness-tool-registry.md`
- `docs/tech-specs/TS-CMF-123-capability-tool-registry-and-provider-menu.md`
- `docs/architecture/cmf_studio_build_workflow/build_receipts/TS-CMF-068-pi-harness-tool-registry-build.md`
- `docs/architecture/cmf_studio_build_workflow/build_receipts/TS-CMF-123-capability-tool-registry-and-provider-menu-build.md`
- `registries/cmf-assembler-schemas/dep_run_003_tool_registry.schema.json`
- `registries/cmf-assembler-schemas/dep_run_004_tool_policy.schema.json`

## Naming Conflicts

No existing `capability_preflight` contract, repository, service, registry namespace, or shared skill pack was present. Existing terms such as provider preflight, composition preflight, provider capability registry, render runtime lock, and cost governance exist as adjacent systems, not direct file conflicts.

## Additive Applicability

The bundle can be applied additively. It should sit above the existing provider adapters, provider job workflows, Video Editing Engine render contracts, Golden Path fake-render path, and approval/cost policy docs. It must not replace those systems or call them for real execution.

## Files Requiring Merge Instead Of Copy

None of the target implementation files existed. Package `__init__.py` files in the bundle were intentionally not copied because the repo already has package initialization files and current imports use direct module paths.
