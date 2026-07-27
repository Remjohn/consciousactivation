---
tech_spec_id: "TS-CMF-082"
title: "Brand Genesis Substrate Resolver for Composition Runtime"
story_id: "7.12"
story_title: "Brand Genesis Substrate Resolver"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "TS-CMF-080 functional decomposition"
pipeline_stage: "10"
entry_object: "CompleteEditingSession and locked BrandContextVersion"
exit_object: "ResolvedBrandGenesisSubstrate"
validation_contract: "locked context, brand scope, required creative assets, receipt lineage"
required_receipt: "BrandGenesisSubstrateResolutionReceipt"
runtime_target: "Python / Pydantic v2 / repository services / object storage"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-082: Brand Genesis Substrate Resolver for Composition Runtime

## 1. Purpose

Implement the resolver that turns a locked Brand Context Version into the exact creative substrate available to a composition template.

The resolver is what prevents templates from inventing the brand. It must retrieve approved assets, verify hashes, enforce brand scope, and expose missing substrate as blockers.

## 2. Required Substrate

| Substrate | Required When |
|---|---|
| Identity pack | Always when a human likeness or brand identity is used. |
| 64-state acting library | Any human cutout, realistic reference, avatar state, or performance-driven composition. |
| Paper-Cut avatar rig | Paper-Cut or Animated Avatar route. |
| Visual constitution | Every composition. |
| Micro-semiotic anchor library | High-identification composition, Paper-Cut, polls, memes, and audience recognition assets. |
| Motion library | Any motion render or animated preview. |
| SFX library | Any video render with sound effects. |
| Composition preference library | Any composition template selection or Ideogram layout job. |
| Platform profile | Every render and review preview. |

## 3. Primary Contracts

```python
class ResolvedBrandGenesisSubstrate(BaseModel):
    schema_version: Literal["cmf.resolved_brand_genesis_substrate.v1"]
    brand_id: UUID
    brand_context_version_id: UUID
    brand_context_hash: str
    locked: bool
    identity_pack_ref: str
    acting_library_ref: str | None
    papercut_rig_ref: str | None
    visual_constitution_ref: str
    micro_semiotic_anchor_library_ref: str | None
    motion_library_ref: str | None
    sfx_library_ref: str | None
    composition_preference_library_ref: str | None
    platform_profile_ref: str
    selected_asset_hashes: dict[str, str]
    missing_required_substrate: list[str]
    blocker_codes: list[str]
```

## 4. Resolution Rules

- Brand Context must be locked.
- All selected assets must belong to the same brand.
- Historical renders must keep their original Brand Context Version.
- A newer Brand Context does not silently replace an older one.
- Provider-generated assets cannot enter runtime unless approved and attached to Brand Context.
- Composition templates may request substrate, but the resolver decides whether it is available and allowed.

## 5. Commands and Receipts

| Type | Names |
|---|---|
| Commands | `ResolveBrandGenesisSubstrateCommand`, `ValidateBrandSubstrateForRouteCommand`, `RecordBrandGenesisSubstrateResolutionCommand` |
| Events | `BrandGenesisSubstrateResolved`, `BrandGenesisSubstrateBlocked` |
| Receipt | `BrandGenesisSubstrateResolutionReceipt` |

## 6. Blockers

| Blocker | Trigger |
|---|---|
| `BRAND_CONTEXT_UNLOCKED` | Version is not locked. |
| `BRAND_CONTEXT_SCOPE_VIOLATION` | Asset belongs to another brand. |
| `IDENTITY_PACK_MISSING` | Likeness or brand identity is required but absent. |
| `ACTING_LIBRARY_MISSING` | Performance state required but no acting library is available. |
| `PAPERCUT_RIG_MISSING` | Paper-Cut route lacks approved rig. |
| `VISUAL_CONSTITUTION_MISSING` | Route lacks approved visual rules. |
| `PLATFORM_PROFILE_MISSING` | Render target lacks platform constraints. |

## 7. Acceptance Criteria

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Resolver emits a complete substrate object for a valid locked Brand Context. | Template directly reads object storage paths. |
| AC2 | Missing required substrate blocks runtime binding. | Paper-Cut render proceeds without rig. |
| AC3 | Cross-brand assets are blocked. | Guest A uses Guest B's anchor library. |
| AC4 | Hashes are included for selected assets. | Render cannot reconstruct asset versions. |

## 8. Testing

- Locked vs unlocked Brand Context tests.
- Route-specific substrate tests.
- Cross-brand scope tests.
- Historical version preservation tests.
- Object hash reconstruction tests.

