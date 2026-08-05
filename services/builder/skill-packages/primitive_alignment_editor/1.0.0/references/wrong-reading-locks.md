# Wrong-Reading Locks Governance — Primitive Alignment Editor

## Option B Partition Governance Rules

### Rule 1: Spatial Lock Isolation
Spatial layout locks (`wrong_reading_locks`) belong exclusively to
`visual_syntax_composition_compiler`. This Skill must never mutate, delete,
or rewrite spatial layout locks containing any of the following vocabulary:

**Primitive layout types:** `text_block`, `image_region`, `grid_cluster`,
`comparison_pair`, `badge`, `number_label`, `icon_row`, `caption_plate`,
`callout_arrow`, `flow_diagram`

**Container zones:** `header_zone`, `hero_zone`, `footer_zone`, `overlay_zone`,
`full_bleed`

**Spatial constraint types:** `z_index_order`, `non_overlap`, `anchor_lock`,
`contrast_ratio`, `presence_required`, `absence_required`, `pairing_required`,
`content_separation`

**Geometric vocabulary:** BBox coordinates, `height_pct`, `width_pct`,
`y_anchor`, `overlap_allowed`, `anchor_mode`, pixel measurements

### Rule 2: Meaning Lock Ownership
Meaning-plane locks (`wrong_reading_locks_meaning`) belong exclusively to this
Skill. Every lock in `wrong_reading_locks_meaning` must:
- Cite at least one primitive ID (`PRM-`/`EXP-`).
- Describe a psychological trap, archetypal misreading, or identity boundary
  violation.
- Contain zero proper nouns, character names, brand names, or specimen-specific
  content.
- Ground its constraint in the cited primitive's `core_move` language.

### Rule 3: Ambiguity Protocol
If a lock cannot be confidently classified as spatial or meaning-plane:
- Do NOT silently reclassify it into either field.
- Flag it in the alignment receipt's `ambiguous_locks_flagged` array.
- Set the receipt outcome to `PASS_WITH_REVIEW_REQUIRED`.
- A human reviewer will make the final classification decision.

This is the single easiest step for an implementing agent to get wrong. When in
doubt, flag — do not guess.

### Rule 4: No Noun Laundering
The alignment process must not retain specimen-specific proper nouns, character
names, episode titles, or brand references in meaning-plane locks. Replace all
specimen-specific content with generic references ("the reference specimen,"
"the subject," "the audience").

### Rule 5: Lineage Preservation
Immutable semantic lineage refs (`identity_dna_ref`, `source_premise_ref`,
`context_premise_ref`, `resonance_map_ref`, `matrix_of_edging_ref`,
`activative_intelligence_pack_ref`, `evaluation_contract_ref`) must pass
through byte-identical. Mutation of any lineage ref is an `OUT_OF_SCOPE_MUTATION`
error.
