# Asset Intelligence Adapter Plan

Asset Intelligence V1 must extend existing systems instead of replacing them.

## CreativeLibraryAdapter

Maps existing creative-library objects into canonical assets and ingredients.

Examples:

```text
MicroSemioticAnchor → CreativeIngredient(kind=micro_semiotic_anchor)
MotionRecipe → AssetRecord(kind=motion_recipe)
SfxAsset → AssetRecord(kind=sfx_asset)
CompositionPreference → CreativeIngredient(kind=composition_reference)
```

## VisualResearchAdapter

Maps visual research candidates into canonical Asset Intelligence objects.

Examples:

```text
VisualCandidate → AssetRecord(kind=visual_reference)
LicensingDecision → RightsProvenanceProfile
VisualCandidateScore → AssetEvaluationReceipt
AssetResearchManifest → VisualReferenceBoard
```

## ExpressionIngredientAdapter

Maps interview/source-derived ingredients.

Examples:

```text
ExpressionIngredient → CreativeIngredient
Transcript span → AssetRecord(kind=transcript_span)
Proof quote → CreativeIngredient(kind=proof_object)
```

## ActingLibraryAdapter

Maps acting and avatar references.

Examples:

```text
ActingReference → AssetRecord(kind=acting_reference)
RigManifest → AssetRecord(kind=avatar_asset)
Pose → CreativeIngredient(kind=acting_reference)
```

## ProviderOutputAdapter

Maps provider outputs into versioned assets and variants.

Examples:

```text
ProviderJobReceipt + generated image → CreativeIngredientVariant
SAM mask → AssetVersion(kind=mask)
Qwen layered output → AssetVersion(kind=provider_generated_layer)
Skia render → AssetVersion(kind=render_output)
```
