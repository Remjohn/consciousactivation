---
name: visual_syntax_composition_compiler
version: 1.0.0
authority_lane: Composer
maturity: development_uncertified
---

# Visual Syntax Composition Compiler

Compile one governed visual syntax specification from a harness definition's
category binding, wrong-reading locks, and slide-role evidence into a normalized
set of composition primitives with attribute ranges, container layout rules, and
cross-element anchor continuity constraints. The output is a structural
specification the CompositionIR layer consumes at campaign time to produce
per-element BBox, z-index, and text-measurement geometry — this Skill does not
render pixels.

## Canonical Primitive Taxonomy

Every visual element in every category resolves to exactly one of these primitive
types. A primitive is a reusable ingredient — like salt, it appears across many
formats. What varies per harness is the attribute ranges and composition rules,
never the primitive type definitions themselves.

### Primitive Types

| Primitive Type       | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `text_block`         | Any text element: headline, caption, refrain, question, label, subtitle.    |
| `image_region`       | Any image element: photo, illustration, collage panel, UGC portrait.        |
| `grid_cluster`       | Multi-image arrangement within a single container zone.                     |
| `comparison_pair`    | Side-by-side wrong/right, before/after, or do-not/do pairing.              |
| `badge`              | Creator avatar, brand mark, dot anchor, or fixed authorship element.        |
| `number_label`       | Sequential numbering element: 01, #1, Step 1, Bias #3.                     |
| `icon_row`           | Engagement or action icon set: comment, heart, save, share.                 |
| `caption_plate`      | Solid-color background plate behind text for contrast and readability.       |
| `callout_arrow`      | Annotation connector linking a symbol or garment to its referent label.      |
| `flow_diagram`       | Explanatory model or relationship visualization (non-statistical).          |

### Primitive Attributes (Universal)

Every primitive instance carries these attributes, whose legal values are
constrained per harness by attribute ranges:

- `height_pct`: percentage of parent container height `[min, max]`
- `width_pct`: percentage of parent container width `[min, max]`
- `font_size_px`: text size in pixels `[min, max]` (text primitives only)
- `font_weight`: one of `{thin, light, regular, medium, bold, black}`
- `alignment`: one of `{left, center, right}`
- `color_constraint`: palette reference or contrast-ratio minimum
- `z_index_range`: layer ordering range `[min, max]`
- `padding_px`: internal spacing `[min, max]`
- `overlap_allowed`: boolean — whether this element may collide with siblings
- `anchor_mode`: one of `{static, cross_slide_locked, per_slide_variable}`

## Container Zones

Primitives compose inside container zones. A container is a rectangular region of
the canvas that arranges its children according to a layout mode.

### Zone Types

| Zone Type       | Layout Mode        | Typical Children                                    |
|-----------------|--------------------|-----------------------------------------------------|
| `header_zone`   | `vertical_stack`   | `text_block`, `number_label`, `badge`               |
| `hero_zone`     | `overlay` or `grid`| `image_region`, `grid_cluster`, `comparison_pair`, `text_block` |
| `footer_zone`   | `horizontal_row`   | `badge`, `text_block`, `icon_row`, `number_label`   |
| `overlay_zone`  | `absolute`         | `caption_plate` + `text_block` layered over `hero_zone` |
| `full_bleed`    | `fill`             | `image_region` spanning the entire canvas            |

### Zone Attributes

- `height_pct`: percentage of canvas `[min, max]`
- `width_pct`: percentage of canvas (usually `[100, 100]`)
- `y_anchor`: vertical start position as percentage `[min, max]`
- `required`: boolean — must this zone be present for the format to be valid
- `accepts`: list of primitive types this zone can host
- `max_children`: integer — maximum number of child primitives

## Slide Roles

For multi-slide formats (carousels), each slide in the sequence carries a
structural role that determines its zone configuration:

| Slide Role             | Zone Configuration                                         |
|------------------------|------------------------------------------------------------|
| `cover`                | `full_bleed` + `overlay_zone{text_block[headline]}`        |
| `numbered_item`        | `header_zone{number_label}` + `hero_zone` + `footer_zone`  |
| `comparison_beat`      | `hero_zone{comparison_pair}` + `footer_zone`               |
| `refrain_beat`         | `hero_zone{text_block[claim]}` only, no imagery            |
| `photo_beat`           | `full_bleed{image_region}` + `overlay_zone{caption_plate}` |
| `grid_collage`         | `header_zone{text_block}` + `hero_zone{grid_cluster}`      |
| `closing_question`     | `hero_zone{text_block[question]}` only, no imagery          |
| `closing_cta`          | `hero_zone{text_block}` + `footer_zone{icon_row, badge}`   |
| `closing_comparison`   | `hero_zone{comparison_pair}` + `footer_zone{badge}`        |
| `testimonial`          | `hero_zone{caption_plate + text_block}` + `footer_zone`    |

For single-frame formats (supervisuals), the entire canvas is one slide with
role `single_frame`.

## Grammar Families

This Skill resolves two grammar families. Both share the same primitive taxonomy
and container model. They differ only in temporal and reading-order dimensions:

### CAROUSEL_SWIPE_PROGRESSION

- **Spatial:** `slide_role_layout`, `cross_slide_anchor_continuity`
- **Temporal:** `NOT_APPLICABLE` — static slides have no frame-time motion
- **Reading Order:** `swipe_progression`, `final_commitment_slide`
- **Character Performance:** `NOT_APPLICABLE`
- **Conversational Turn:** `NOT_APPLICABLE`

### SUPERVISUAL_STATIC_HIERARCHY

- **Spatial:** `frame_hierarchy`, `subject_caption_separation`
- **Temporal:** `NOT_APPLICABLE` — single frame has no temporal grammar
- **Reading Order:** `recognition_to_pressure_to_activative_call`
- **Character Performance:** `NOT_APPLICABLE`
- **Conversational Turn:** `NOT_APPLICABLE`

### Shared with SHORT_FORM_EDITED_VIDEO_TIMELINE

The following spatial grammar rules are shared across all visual categories and
must use the same primitive definitions (no duplication):

- Subject-caption separation (text overlays must not obscure primary visual subject)
- Z-index collision rules (BBox intersection detection with overlap_allowed flags)
- Anchor continuity (elements that persist across transitions: brand badge in
  carousels = lower-third bug in video = fixed attribution in supervisuals)
- Contrast-ratio enforcement (text over imagery must meet minimum legibility)
- Safe-zone margins (no critical content in platform-cropped edge regions)

## Active Procedure

1. **Resolve Grammar Family.** Read `category_id` from the harness definition.
   Map to `CAROUSEL_SWIPE_PROGRESSION` or `SUPERVISUAL_STATIC_HIERARCHY`. If the
   category is not `carousels` or `supervisuals`, this Skill does not apply —
   return `NOT_APPLICABLE` with the category as the reason.

2. **Extract Slide Roles.** From the harness evidence (specimen analysis and
   activative_input), identify the ordered set of slide roles present. For
   supervisuals this is always `[single_frame]`. For carousels, derive the
   sequence from the harness's structural description (e.g., cover + N numbered
   items + closing CTA).

3. **Resolve Zone Configuration Per Slide Role.** For each slide role, look up
   the zone configuration from the Slide Roles table. Validate that each zone's
   `accepts` list is satisfied by the primitives the harness evidence implies.

4. **Select Primitive Ingredients.** For each zone, select the specific primitive
   types from the Canonical Primitive Taxonomy. Do not invent new primitive types.
   If a visual element in the specimen does not map to an existing primitive,
   classify it as the nearest primitive type and document the mapping in the
   `why` field.

5. **Constrain Attribute Ranges.** For each selected primitive instance, derive
   attribute ranges from the specimen evidence:
   - Measure relative proportions (height/width as percentage of canvas)
   - Identify font-size bounds from specimen text scaling
   - Determine z-index ordering from specimen layer relationships
   - Set `overlap_allowed` based on whether the specimen shows intentional overlay
   - Set `anchor_mode` based on whether the element persists across slides

6. **Enforce Wrong-Reading Locks as Spatial Constraints.** Translate each
   wrong-reading lock from the harness into a testable spatial or typographic
   constraint. Examples:
   - "Do not let metadata migrate off the solid plate" → `caption_plate.z_index`
     must be less than `text_block.z_index`, both inside `overlay_zone`
   - "Creator badge must remain legible on every slide" → `badge.anchor_mode`
     must be `cross_slide_locked`
   - "Don't/Do pair must not flatten to single frame" → `comparison_pair` must
     occupy its own `hero_zone`, never merged with a sibling comparison

7. **Validate Cross-Slide Anchor Continuity.** For carousel formats, identify all
   primitives with `anchor_mode: cross_slide_locked` and verify:
   - Same `height_pct`, `width_pct`, and `y_anchor` ranges across all slides
   - Same `z_index_range` across all slides
   - Position variance is zero or within a declared tolerance

8. **Deduplicate.** If two harnesses produce identical zone configurations,
   identical primitive selections, and identical attribute ranges, they share the
   same visual syntax specification. Do not emit a duplicate. Record the shared
   specification once and reference it by content hash.

9. **Emit Composition Specification.** Output the normalized specification as a
   typed `VisualSyntaxCompositionSpec` containing:
   - Grammar family
   - Slide role sequence
   - Per-slide zone configurations
   - Per-zone primitive selections with attribute ranges
   - Cross-slide anchor continuity declarations
   - Wrong-reading lock spatial constraint mappings
   - Deduplication hash

10. **Validate Output.** Validate the result against `contracts/output.schema.json`.

## Completion Criteria

- All slide roles are resolved to valid zone configurations.
- Every primitive instance maps to exactly one canonical primitive type.
- Every attribute range has non-zero width (min less than or equal to max).
- Every wrong-reading lock maps to at least one spatial or typographic constraint.
- Cross-slide anchors are consistent across all slides they span.
- No primitive type is invented outside the Canonical Primitive Taxonomy.
- No attribute range exceeds the normalized canvas bounds (0 to 1,000,000).
- Deduplication hash is computed and identical specifications are merged.
- Identity DNA, source premise, and semantic lineage refs are unchanged and
  reference-only.

## What This Skill Does Not Do

- Does not render pixels or produce final slide media.
- Does not generate copy, headlines, or caption text.
- Does not select photographs, illustrations, or UGC images.
- Does not determine which real-world case study, dish, or topic fills the format.
- Does not produce CompositionIR elements directly — it produces the structural
  specification that a downstream CompositionIR compiler consumes.
- Does not modify wrong-reading locks — it only translates them into spatial
  constraints.

Load branch-specific detail only from the package references named by the
immutable manifest.
