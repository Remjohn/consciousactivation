# M0084 — SourceQualityProfile and Adaptive Transformation Rules

**Evidence class:** SCHEMA + EXECUTABLE + TEST
**Mandate:** M0084
**Scope:** `packages/`, `services/`, `docs/cae/specs/`, `tests`

## Decision

Extend the canonical `ca_runtime.storyboard_session` transformation path with a measured `SourceQualityProfile`. A profile is attached to an existing `VisualAssetReference`; it does not become a new asset authority.

Required measurements are resolution, frame rate (in deterministic milli-fps), crop history, compression loss, sharpness, prior degradation, and evidence references. The profile deterministically derives a quality level: `HIGH`, `MEDIUM`, `LOW`, or `DEGRADED`.

`TransformationIntent` remains semantic. `TransformationRecipe` remains its bounded execution projection. Quality-aware functions only constrain or clamp declared transform magnitude; they do not change intent or invent source meaning.

## Deterministic policy

The quality score uses fixed-point basis points and weighted measured inputs:

| Measurement | Weight | Deterministic interpretation |
|---|---:|---|
| Resolution | 30% | 2160p+ → 10000; 1080p+ → 8000; 720p+ → 5500; 480p+ → 3500; lower → 2000 |
| Crop retention | 15% | Higher retained source area scores higher |
| Compression loss | 20% | `10000 - compression_loss_bps` |
| Sharpness | 20% | Higher sharpness scores higher |
| Frame-rate quality | 10% | 30000 milli-fps+ → 10000; 24000+ → 8500; 20000+ → 6500; 15000+ → 4500; lower → 2500 |
| Prior degradation | 5% | `10000 - prior_degradation_bps` |

Quality bands are `HIGH >= 8000`, `MEDIUM >= 6500`, `LOW >= 4500`, otherwise `DEGRADED`.

Transformation limits are expressed in basis points:

| Quality | Max scale delta | Max reframe | Max motion amplitude | Color |
|---|---:|---:|---:|---|
| HIGH | 1200 | 1200 | 1200 | NONE / CONTROLLED / SUBTLE_LUT |
| MEDIUM | 800 | 800 | 700 | NONE / CONTROLLED |
| LOW | 400 | 400 | 300 | NONE / GRAYSCALE / CONTROLLED |
| DEGRADED | 150 | 200 | 0 | NONE / GRAYSCALE |

These limits are implementation policy for M0084, not claims about universal perceptual thresholds.

## Adaptive presentation

The profile recommends `STANDARD`, `SUBTLE_REFRAME`, and `SUBTLE_COLOR` for `HIGH`; `STANDARD`, `REDUCED_SCALE`, and `SELECTIVE_FRAMING` for `MEDIUM`; `REDUCED_SCALE`, `INSET`, `CONTEXTUAL`, and `GRAYSCALE` for `LOW`; and `CONTAINERIZED`, `INSET`, `CONTEXTUAL`, and `GRAYSCALE` for `DEGRADED`.

`adapt_transformation_recipe_for_source_quality()` is a pure clamp. It preserves `intent_id`, preserves input semantic constraints, records the source-quality profile ID/level and evidence references, and selects the first quality-safe presentation strategy. It does not silently rewrite canonical meaning.

## Integration guard

`StoryboardSessionStore._validate_revision_input()` validates any attached profile before accepting a recipe. A profile must refer to the same `asset_id` and its evidence references must remain inside the revision's evidence lineage. Legacy assets without a structured profile continue to validate through the existing contract so this additive change does not silently invalidate historic records.

## False-proof case

A 480p, pre-cropped, compressed speaker clip can look polished after a large zoom. M0084 must still reject the recipe because the transform magnifies source defects and violates the source-quality limit. The acceptable alternative is a smaller/inset/contextual treatment that keeps the evidence legible without making degradation the focal event.

## Non-goals

No new retrieval system, semantic authority, asset store, runtime adapter, database migration, UI surface, provider integration, or external repository extraction is introduced by this mandate.


