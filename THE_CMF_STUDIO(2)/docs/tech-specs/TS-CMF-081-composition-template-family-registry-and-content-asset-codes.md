---
tech_spec_id: "TS-CMF-081"
title: "Composition Template Family Registry and Content Asset Codes"
story_id: "7.11"
story_title: "Composition Template Family Registry"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "TS-CMF-080 functional decomposition"
pipeline_stage: "8 / 9 / 10"
entry_object: "AssetPackageSpec and FourVideoFormatPlan"
exit_object: "CompositionTemplateFamilyRegistry and ContentAssetCodeReservation"
validation_contract: "template code uniqueness, guest/brand scope, slot coverage, route compatibility"
required_receipt: "CompositionTemplateFamilyRegistryReceipt"
runtime_target: "Python / Pydantic v2 / JSON Schema / registry loader"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-081: Composition Template Family Registry and Content Asset Codes

## 1. Purpose

Define the registry that makes every composition template addressable, scoped, versioned, and tied to a content asset code. This prevents visual templates from becoming loose PNGs or generic filenames.

TS-CMF-080 says compositions must be runtime-bound. This spec defines the registry layer that decides which template families exist and which content asset code each output receives.

## 2. Source Doctrine

| Source | Requirement |
|---|---|
| CCP V9.1 | Four Guest Asset Pack video slots plus carousels, memes, polls, and reaction seeds. |
| Brand Genesis V3 | Composition preference library belongs to locked Brand Context. |
| TS-CMF-073 | Composition JSON is canonical. |
| TS-CMF-078 | Four short-video slots are `SV-CSC`, `SV-EDU`, `SV-FRB`, and `SV-RRC`. |
| TS-CMF-080 | Templates must bind source lineage, brand substrate, timing, renderer, eval, and approval. |

## 3. Registry Scope

The registry covers:

- 24 initial video composition template codes:
  - `SV-CSC-CIN-001` through `SV-CSC-CIN-006`;
  - `SV-EDU-PAP-001` through `SV-EDU-PAP-006`;
  - `SV-FRB-CHL-001` through `SV-FRB-CHL-006`;
  - `SV-RRC-RCT-001` through `SV-RRC-RCT-006`;
- future carousel, meme, poll, and super visual template families;
- content asset codes for every guest/brand output;
- compatibility rules between slot, archetype, derivative, CMF route, renderer, and platform.

## 4. Primary Contracts

```python
class CompositionTemplateFamily(BaseModel):
    schema_version: Literal["cmf.composition_template_family.v1"]
    family_code: str
    slot_code: str
    cmf_routes: list[str]
    allowed_archetypes: list[str]
    allowed_asset_derivatives: list[str]
    default_renderer_targets: list[str]
    required_brand_substrate: list[str]
    required_runtime_specs: list[str]
    status: Literal["draft", "active", "deprecated", "blocked"]


class ContentAssetCodeReservation(BaseModel):
    schema_version: Literal["cmf.content_asset_code_reservation.v1"]
    content_asset_code: str
    organization_id: UUID
    brand_id: UUID
    guest_id: UUID | None
    asset_package_spec_id: UUID
    composition_template_family_code: str
    expression_moment_id: UUID
    asset_type: str
    slot_code: str | None
    platform_targets: list[str]
    reserved_at: datetime
```

## 5. Required Code Semantics

Content asset codes must make the asset traceable without exposing private content:

```text
CMF-{brand_slug}-{guest_slug}-{pack_cycle}-{asset_type}-{slot_or_family}-{sequence}
```

Examples:

- `CMF-CE-CLAUDE-2026M06-SV-CSC-001`
- `CMF-CE-CLAUDE-2026M06-SV-EDU-002`
- `CMF-CE-CLAUDE-2026M06-POLL-TENSION-001`

Rules:

- no two assets in the same brand workspace can share a code;
- codes must survive renderer retries and revisions;
- a revision appends a revision suffix, not a new identity;
- codes must appear in Operator UI, receipts, exports, and publishing intent.

## 6. Commands and Receipts

| Type | Names |
|---|---|
| Commands | `RegisterCompositionTemplateFamilyCommand`, `ReserveContentAssetCodeCommand`, `DeprecateTemplateFamilyCommand`, `ValidateTemplateFamilyCompatibilityCommand` |
| Events | `CompositionTemplateFamilyRegistered`, `ContentAssetCodeReserved`, `TemplateFamilyDeprecated`, `TemplateFamilyCompatibilityValidated` |
| Receipt | `CompositionTemplateFamilyRegistryReceipt`, `ContentAssetCodeReservationReceipt` |

## 7. Blockers

| Blocker | Trigger |
|---|---|
| `TEMPLATE_FAMILY_CODE_DUPLICATE` | Family code already exists. |
| `CONTENT_ASSET_CODE_DUPLICATE` | Reserved code conflicts within brand workspace. |
| `SLOT_ROUTE_INCOMPATIBLE` | Template family does not support requested CMF route. |
| `OUTPUT_FORMAT_NOT_ALLOWED` | Template attempts unsupported format such as newsletter. |
| `BRAND_SCOPE_MISSING` | Asset code is not bound to brand workspace. |

## 8. Acceptance Criteria

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | All 24 starting video template families are registered. | A board exists but no family code exists. |
| AC2 | Every asset receives a unique content asset code. | Operator sees only `final_video_2.mp4`. |
| AC3 | Template family compatibility blocks wrong route usage. | Paper-Cut family used for Cinematic Story without explicit route. |
| AC4 | Unsupported output formats are rejected. | Newsletter asset code is accepted as Guest Asset Pack output. |

## 9. Testing

- Registry uniqueness tests.
- Compatibility matrix tests for all four video slots.
- Content asset code collision tests.
- Negative test for unsupported newsletter output.
- Read model test proving code appears in Operator UI and receipts.

