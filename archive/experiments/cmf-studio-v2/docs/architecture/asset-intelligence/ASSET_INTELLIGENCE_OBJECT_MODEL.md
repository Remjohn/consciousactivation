# Asset Intelligence V1 Object Model

## Asset vs Creative Ingredient

An asset is a file, source object, reference, library item, generated output, mask, cutout, render, or media object.

A creative ingredient is the meaning-bearing production unit derived from one or more assets.

Example:

```text
Asset:
photo of a worn notebook on a kitchen table

Creative Ingredients:
- proof object
- memory object
- ordinary-life anchor
- CAC real-life reference
- paper-cut artifact candidate
```

## Object hierarchy

```text
AssetSource
↓
AssetRecord
↓
AssetVersion
↓
RightsProvenanceProfile
↓
AssetClassification
↓
AssetSemanticProfile
↓
CreativeIngredient
↓
CreativeIngredientVariant
↓
AssetEvaluationReceipt
↓
AssetUsageReceipt
↓
AssetPerformanceMemory
↓
AssetFatigueRecord / WinningAssetRecord
```

## Central object

`AssetRecord` is the canonical asset identity.

Required production fields:

```text
asset_id
brand_id
brand_context_version_id
asset_kind
asset_origin
asset_status
display_name
source_refs
rights_profile_id
current_version_id
classification_id
semantic_profile_id
primitive_binding_refs
style_route_affinities
frame_profile_affinities
composition_role_affinities
```

## Direct-use rule

`RightsProvenanceProfile` decides whether an asset can be:

```text
direct_use
reference_only
composition_reference_only
style_reference_only
provider_input_only
operator_review_required
blocked
```

Unknown-rights assets cannot be direct-use.
