# CCP Capability Preflight + Provider Menu V1 Integration Bundle

This bundle adds the operational preflight layer that must run before real provider, generation, batch, or local render jobs.

## Purpose

Before any real provider/render run, the system should know:

```text
what is configured
what is missing
what is degraded
what is blocked
what the estimated cost is
whether a sample is required before batch
what setup steps are needed
which providers/runtimes/tools are available
```

## Why this matters

This protects high-cost production flows such as:

```text
64-image avatar library generation
Ideogram composition plate generation
Flux reference-based object edit
Remotion render
FFmpeg finishing
local render worker execution
```

## Apply after

Recommended:

```text
Format 02 Golden Path Orchestrator V1
Video Editing Engine V1
Avatar Performance Layer V1
Composition Intelligence Core + Format 02 Pack V1
Provider adapter foundations, if present
```

## Do not

```text
Do not call providers.
Do not call Remotion.
Do not call FFmpeg.
Do not run local render jobs.
Do not infer configured secrets.
Do not mark a provider available if required secrets are missing.
Do not allow full batch if sample_required=True and sample_approved=False.
```

## What this bundle adds

```text
CapabilityPreflightReport
ProviderAvailabilityReport
ProviderMenuSummary
RuntimeAvailabilityReport
ToolSupportEnvelope
SetupOffer
PipelineCapabilityStatus
MissingCapabilityBlocker

capability_preflight_service.py
provider_menu_service.py
runtime_availability_service.py
tool_support_registry_service.py
```

## Milestones

### Milestone 1 — Docs, registries, contracts

Copy/add:

```text
docs/architecture/capability-preflight/
registries/canonical/capability_preflight/
src/ccp_studio/contracts/capability_preflight.py
CAPABILITY_PREFLIGHT_PROVIDER_MENU_V1_BUNDLE_MANIFEST.json
CAPABILITY_PREFLIGHT_PROVIDER_MENU_V1_LOCAL_VERIFICATION.json
APPLY_CAPABILITY_PREFLIGHT_PROVIDER_MENU_V1_PATCH.md
```

Commit:

```bash
git add .
git commit -m "feat(capability): add preflight contracts and registries"
```

### Milestone 2 — Repository, services, skills

Copy/add:

```text
src/ccp_studio/repositories/capability_preflight.py
src/ccp_studio/services/capability_preflight_service.py
src/ccp_studio/services/provider_menu_service.py
src/ccp_studio/services/runtime_availability_service.py
src/ccp_studio/services/tool_support_registry_service.py
registries/canonical/skills/shared/capability_preflight/
```

Commit:

```bash
git add .
git commit -m "feat(capability): add provider menu and runtime preflight services"
```

### Milestone 3 — Tests

Copy/add:

```text
tests/cmf_studio/test_capability_preflight_provider_menu_v1.py
```

Run:

```bash
PYTHONPATH=src python -m compileall -q src
PYTHONPATH=src python -m pytest -q tests/cmf_studio
```

Commit:

```bash
git add .
git commit -m "test(capability): verify provider menu and preflight gates"
```

## V1 limitations

```text
deterministic config-based checks only
no real provider calls
no actual secret probing unless a caller supplies secret/config status
no shelling out to ffmpeg/remotion
no UI/API endpoints
no cost billing reconciliation
```
