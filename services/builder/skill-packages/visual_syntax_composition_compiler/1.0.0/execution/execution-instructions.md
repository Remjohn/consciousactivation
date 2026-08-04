# Execution Instructions — Visual Syntax Composition Compiler

## Runtime Execution Flow

### Step 1: Input Validation

Validate every field of the input payload against `contracts/input.schema.json`.
Reject immediately if:
- `category_id` is not `carousels` or `supervisuals`
- `wrong_reading_locks` is empty
- `slide_evidence` is empty
- Any `observed_primitives` entry uses a primitive type not in the canonical
  taxonomy
- `activative_input_refs` is missing required lineage refs

### Step 2: Grammar Family Resolution

Map the `category_id` to its grammar family:
- `carousels` resolves to `CAROUSEL_SWIPE_PROGRESSION`
- `supervisuals` resolves to `SUPERVISUAL_STATIC_HIERARCHY`

Verify that the `grammar_family` field in the input matches the resolved value.

### Step 3: Slide Role Sequence Assembly

For each entry in `slide_evidence`, ordered by `slide_index`:
1. Validate `slide_role` against the grammar family's permitted roles
2. For `SUPERVISUAL_STATIC_HIERARCHY`, enforce that there is exactly one slide
   with role `single_frame`
3. For `CAROUSEL_SWIPE_PROGRESSION`, enforce that the first slide is `cover` and
   the last slide is one of the closing roles

### Step 4: Zone Configuration Resolution

For each slide role, resolve the zone configuration:
1. Look up the role's standard zone set from SKILL.md's Slide Roles table
2. For each zone, verify that the `observed_primitives` from specimen analysis
   map to the zone's `accepts` list
3. If a primitive does not match any zone's `accepts` list, classify it into the
   nearest valid zone and document the mapping in the `why` field

### Step 5: Attribute Range Computation

For each primitive instance:
1. Use the `observed_height_pct`, `observed_width_pct`, `observed_y_anchor_pct`,
   and `observed_font_size_px` from specimen evidence
2. Compute ranges by adding tolerance margins:
   - Height/width: observed value with a range of plus or minus 5 percentage points,
     clamped to the zone's height range
   - Font size: observed value with a range of plus or minus 4 pixels
   - Y-anchor: observed value with a range of plus or minus 3 percentage points
3. Set `overlap_allowed` from `overlap_observed` in specimen evidence
4. Set `anchor_mode` from `cross_slide_stable` in specimen evidence:
   - `true` means `cross_slide_locked`
   - `false` means `per_slide_variable`
   - Single-frame supervisuals always use `static`

### Step 6: Wrong-Reading Lock Translation

For each wrong-reading lock string:
1. Parse the constraint type from the lock's language
2. Map it to one or more `spatial_constraints` entries:
   - Locks about overlay positioning become `z_index_order` constraints
   - Locks about element presence become `presence_required` constraints
   - Locks about pairing (wrong/right, claim/repeated) become `pairing_required`
   - Locks about attribution become `anchor_lock` on badge primitives
   - Locks about legibility become `contrast_ratio` constraints
   - Locks about content separation (no mixing categories) become `content_separation`
3. Every lock must map to at least one constraint. If a lock is purely semantic
   (not expressible as a spatial constraint), map it as `presence_required` with
   the lock text in the `rule` field

### Step 7: Cross-Slide Anchor Verification

For carousel formats only:
1. Collect all primitives with `anchor_mode: cross_slide_locked`
2. For each anchored primitive, verify that its attribute ranges are identical
   across all slides it appears in
3. Record each anchor in the `cross_slide_anchors` output array
4. Flag any inconsistency as a validation failure

### Step 8: Deduplication Hash

Compute a content-addressed hash over:
- The grammar family
- The ordered slide role sequence
- All zone configurations (type, layout mode, height ranges)
- All primitive selections (type, semantic role, attribute ranges)
- All cross-slide anchor declarations

Two harnesses that produce identical hashes share the same visual syntax
specification. Emit the spec once, reference by hash.

### Step 9: Output Assembly and Validation

Assemble the `VisualSyntaxCompositionSpec` output object and validate against
`contracts/output.schema.json`. Verify that all `lineage` refs pass through
unchanged from input.
