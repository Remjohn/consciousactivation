# CCP / CMF Carousel Composition Atlas V1

**Corpus:** `Remjohn/Carousel-compositions`  
**Inspected:** 118 slides across 16 folders  
**Purpose:** Convert the curated visual corpus into executable composition contracts for the Python/Pydantic/DSPy harness and the Skia/Remotion renderer.

## 1. Executive conclusion

The repository should not become a folder of templates. It should become a **composition grammar registry**. The corpus repeatedly proves that high-performing-looking carousels rely on a small set of compositional laws: one dominant focal point, explicit hierarchy, intentional negative space, controlled repetition, and meaningful variation between cover, interior, transition, and CTA slides.

The recommended system contains **44 canonical composition specifications** and **12 sequence grammars**. Ideogram 4 is used selectively for composition ideation and scene/metaphor plates; Skia is the final geometry and compositing authority; Rough Notation is a semantic annotation layer; Qwen-Image-Layered is invoked only when a generated plate benefits from editable RGBA decomposition; SAM3 handles exact masks and cutouts.

## 2. Corpus inventory

| Metric | Value |
|---|---:|
| Folders inspected | 16 |
| Slides inspected | 118 |
| 4:5 slides | 36 |
| 3:4 slides | 38 |
| 1:1 slides | 44 |
| Canonical composition specs | 44 |
| Sequence grammars | 12 |

The set is a curated preference corpus, not a controlled performance dataset. It is strong enough to define visual grammars; future ranking should incorporate saves, shares, completion rate, comments, follower count, and topic baselines.

## 3. Findings from every folder

### Carousel 1
Cinematic opener followed by radical typographic restraint: solid fields, manifesto rhythm, and one clean timeline. Its strength is pacing through contrast rather than visual novelty on every slide.

### Carousel 2
Three full-bleed quote images use culturally familiar, whimsical scenes. Copy is short and the image supplies most of the emotional argument.

### Carousel 3
A relationship/identity quote series combining cosmic scale, animal humor, and a labeled meme. The recurring law is one visual joke or emotional metaphor per slide.

### Carousel 4
Four affirmation slides with recognizable characters and animals. Large text is placed where the photograph already has silence; the image is never merely decorative.

### Carousel 5
An exception/rarity theme: black sheep, child attitude, cartoon calm, and dog romance. Strongest compositional device is the obvious visual metaphor that can be read before the text.

### Carousel 6
Privacy/self-protection series using high-recognition pop-culture imagery and short central statements. Repetition of type treatment creates the carousel identity.

### Carousel 7
Hope/confidence sequence using humorous situational photography. Two slides use explicit meme labeling while others rely on scene–copy incongruity.

### Carousel 8
The most complete high-density educational sequence: dramatic poster cover, clean white lesson shell, colored sectional hierarchy, symbolic cards, one chart slide, one action-plan grid, and a creator-led CTA.

### Carousel 9
A highly coherent editorial framework system. Paper texture, serif typography, orange highlight blocks, and line-based diagrams provide repeatable structure without template fatigue.

### Carousel 10
A brand case-study carousel rather than a topic carousel. It proves that profile, palette, formats, mockups, and character identity can be composed as one narrative system.

### Carousel 11
A 19-slide episodic narrative with fixed shell and variable scenes. The colored protagonist among gray secondary characters creates instant focus; bottom caption and progress dots establish series continuity.

### Carousel Grid Mood Date
Eight 2×2 mood grids. Repetition, simple category labels, and image abundance make this ideal for saveable lists and cultural identification.

### Carousel LISTICLE + JUXTAPOSITION
A meta-educational comparison system. The strongest recurring grammar is title above, paired examples below, and binary verdict at the bottom.

### Carousel LISTICLE TEMPLATE
A disciplined numbered listicle shell. The cover and CTA differ, while every interior lesson retains number, title, explanation, and mini comparison pair.

### Carousel Template 1
Contains two distinct grammars: a repeated 2×2 category collage, a native-post/article card, and a strong vertical “don’t say / say” split.

### Minimal Style CAROUSEL
A soft-gradient, text-led sequence using large negative space, occasional surreal body fragments, one dark pattern interrupt, and a restrained action close.

## 4. Cross-corpus composition laws

1. One slide, one dominant perceptual job. A slide can hook, explain, compare, prove, pause, or ask—but should not do all of them.
2. Covers and interiors must use different density rules. Covers win with singularity; interiors win with structured hierarchy.
3. Text is a spatial object. Its position is determined by the image’s silence, gaze direction, and visual flow—not by a fixed centered default.
4. Negative space is active composition. The strongest examples use emptiness to produce confidence, pacing, and legibility.
5. Repetition creates identity; controlled variation prevents fatigue. Carousel 11 is the clearest evidence of a fixed shell with variable scenes.
6. The visual must add meaning. The best photo quote slides rely on incongruity, cultural recognition, or metaphor—not stock decoration.
7. Binary comparison is exceptionally legible. Red/green verdicts, old/new cards, and split panels compress explanation into immediate judgment.
8. Micro-Semiotic Anchoring belongs inside the visual plan. Familiar objects, clothing, technologies, locations, or rituals make the audience feel recognized.
9. A carousel needs sequence composition, not merely slide composition. Density, color, and format should pulse across the sequence.
10. Final text should be deterministic. Even when Ideogram supplies layout inspiration, Skia/DOM must render production typography exactly.

## 5. The 44 canonical composition specifications

### H01 — Cinematic Full-Bleed Headline
A film still or emotionally loaded photograph fills the canvas while a dominant headline occupies the clearest negative-space band.

- **Family:** `hook_cover`
- **Roles:** cover_hook, provocation, story_open
- **Attention path:** image subject → headline → small kicker
- **Aspect ratios:** 4:5, 3:4
- **Headline budget:** 3–9 words; 1–3 lines
- **Body budget:** 0–8 words
- **Micro-semiotic slots:** wardrobe_detail, background_prop, environmental_sign
- **Ideogram 4:** `composition_reference_or_scene`
- **Qwen-Image-Layered:** `conditional`
- **SAM3:** `subject_cutout_optional`
- **Rough Notation:** underline, highlight
- **Zones:**
  - `visual` — image at `[0, 0, 1, 1]`
  - `headline` — text at `[0.07, 0.12, 0.86, 0.24]`
  - `kicker` — text at `[0.55, 0.34, 0.35, 0.06]`
- **Avoid:** headline over face; more than one dominant focal point; low-contrast copy

### H02 — Dramatic Poster Maximal
A high-drama poster composition with oversized stacked typography, a central or lower-third hero, and a constrained cinematic palette.

- **Family:** `hook_cover`
- **Roles:** cover_hook, campaign_open, case_study_open
- **Attention path:** oversized title → hero face → secondary atmospheric details
- **Aspect ratios:** 4:5, 3:4, 1:1
- **Headline budget:** 3–10 words; 2–5 lines
- **Body budget:** 0–5 words
- **Micro-semiotic slots:** costume_detail, symbolic_prop, local_brand_cue
- **Ideogram 4:** `primary_composition_provider`
- **Qwen-Image-Layered:** `recommended`
- **SAM3:** `hero_mask_refinement`
- **Rough Notation:** highlight
- **Zones:**
  - `title` — text at `[0.08, 0.07, 0.84, 0.36]`
  - `hero` — image at `[0.16, 0.3, 0.72, 0.7]`
  - `meta` — text at `[0.2, 0.93, 0.6, 0.04]`
- **Avoid:** small headline; three or more type families; decorative clutter competing with face

### H03 — Editorial Object Split Cover
A clean editorial cover: large headline block on one side and a single surprising object or cropped body fragment on the other.

- **Family:** `hook_cover`
- **Roles:** cover_hook, educational_open, concept_open
- **Attention path:** headline → object → author/meta
- **Aspect ratios:** 1:1, 4:5
- **Headline budget:** 4–12 words; 2–6 lines
- **Body budget:** 0–18 words
- **Micro-semiotic slots:** object_surface_detail, ordinary_life_object
- **Ideogram 4:** `asset_or_composition_reference`
- **Qwen-Image-Layered:** `conditional`
- **SAM3:** `object_mask_optional`
- **Rough Notation:** underline, highlight
- **Zones:**
  - `headline` — text at `[0.08, 0.18, 0.48, 0.46]`
  - `hero_object` — image at `[0.52, 0.1, 0.44, 0.78]`
  - `meta` — text at `[0.08, 0.78, 0.4, 0.12]`
- **Avoid:** multiple objects; centered headline with centered object; insufficient breathing room

### H04 — Portrait Split Cover
A personal-brand cover with a clear text column and a large cutout portrait occupying the opposite half.

- **Family:** `hook_cover`
- **Roles:** cover_hook, personal_brand_open, listicle_open
- **Attention path:** headline → face → action cue
- **Aspect ratios:** 1:1, 4:5
- **Headline budget:** 6–24 words; 3–9 lines
- **Body budget:** 0–14 words
- **Micro-semiotic slots:** clothing_detail, handheld_object, small_accessory
- **Ideogram 4:** `layout_reference_optional`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `required_for_portrait_cutout`
- **Rough Notation:** underline, circle, highlight
- **Zones:**
  - `headline` — text at `[0.08, 0.2, 0.48, 0.56]`
  - `portrait` — image at `[0.52, 0.08, 0.46, 0.9]`
  - `action` — icons_or_text at `[0.08, 0.8, 0.34, 0.1]`
- **Avoid:** portrait below 38% canvas width; copy crossing portrait face; weak eye-line

### H05 — Minimal Highlighted Type Cover
A typography-led cover on paper or neutral texture, using one highlighted phrase and one directional line or rule.

- **Family:** `hook_cover`
- **Roles:** cover_hook, framework_open, authority_open
- **Attention path:** highlighted phrase → remaining title → continuation line
- **Aspect ratios:** 3:4, 1:1, 4:5
- **Headline budget:** 4–14 words; 3–7 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** paper_note_fragment, tiny printed mark
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `not_needed`
- **Rough Notation:** highlight, underline, brackets
- **Zones:**
  - `title` — text at `[0.1, 0.16, 0.78, 0.58]`
  - `highlight` — shape at `[0.09, 0.32, 0.68, 0.12]`
  - `rule` — line at `[0.78, 0.48, 0.2, 0.03]`
- **Avoid:** more than one highlighted phrase; decorative photo added without semantic need; low type contrast

### H06 — Centered Product or Device Mockup Cover
A bold format title sits above a centered phone, poster, screen, or product mockup on a branded field.

- **Family:** `hook_cover`
- **Roles:** case_study_section, format_intro, product_open
- **Attention path:** format title → centered mockup → small brand mark
- **Aspect ratios:** 4:5, 1:1
- **Headline budget:** 2–7 words; 1–3 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** brand_badge, tiny UI cue
- **Ideogram 4:** `not_needed_for_layout`
- **Qwen-Image-Layered:** `conditional`
- **SAM3:** `mockup_mask_optional`
- **Rough Notation:** none
- **Zones:**
  - `title` — text at `[0.1, 0.08, 0.8, 0.2]`
  - `mockup` — image at `[0.18, 0.27, 0.64, 0.66]`
  - `brand_mark` — logo at `[0.44, 0.02, 0.12, 0.07]`
- **Avoid:** multiple competing mockups; title overlaps device; perspective inconsistency

### H07 — Portfolio Format Grid Cover
A section title introduces two to six output examples arranged as a clean portfolio grid.

- **Family:** `hook_cover`
- **Roles:** case_study_section, proof_open, format_overview
- **Attention path:** format title → example grid → individual thumbnails
- **Aspect ratios:** 4:5, 1:1
- **Headline budget:** 2–6 words; 1–2 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** thumbnail_micro_detail
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `not_needed`
- **Rough Notation:** box
- **Zones:**
  - `title` — text at `[0.1, 0.06, 0.8, 0.19]`
  - `grid` — image_grid at `[0.08, 0.28, 0.84, 0.62]`
  - `brand_mark` — logo at `[0.44, 0.01, 0.12, 0.06]`
- **Avoid:** more than six thumbnails; unequal thumbnail treatment; no primary example

### H08 — Moodboard Grid with Central Label
A 2×2 image grid creates instant abundance and mood while a short label spans the center seam.

- **Family:** `hook_cover`
- **Roles:** list_item, moodboard, category_card, visual_listicle
- **Attention path:** four-image scan → central label → comparative details
- **Aspect ratios:** 1:1, 4:5
- **Headline budget:** 1–5 words; 1–2 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** food_item, place_detail, ritual_object
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `individual_asset_crop_optional`
- **Rough Notation:** highlight
- **Zones:**
  - `grid` — image_grid at `[0, 0, 1, 1]`
  - `label` — text at `[0.12, 0.43, 0.76, 0.14]`
  - `badge` — avatar_or_icon at `[0.03, 0.82, 0.1, 0.1]`
- **Avoid:** different color temperatures without unifying grade; label longer than five words; busy center seam

### N01 — Solid Field Micro-Statement
One short sentence is centered on a single-color field, producing a pause, conclusion, or emotional reset.

- **Family:** `narrative_emotion`
- **Roles:** bridge, pause, conclusion, emotional_landing
- **Attention path:** empty field → sentence
- **Aspect ratios:** 4:5, 3:4, 1:1
- **Headline budget:** 3–11 words; 1–3 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** none_or_tiny_signature_mark
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `not_needed`
- **Rough Notation:** underline
- **Zones:**
  - `statement` — text at `[0.16, 0.38, 0.68, 0.24]`
- **Avoid:** body copy; more than one sentence; decorative image

### N02 — Manifesto Left Column
A vertically paced list or manifesto sits in the upper-left quadrant with abundant negative space.

- **Family:** `narrative_emotion`
- **Roles:** manifesto, pressure_build, rules, internal_monologue
- **Attention path:** top line → downward rhythm → open field
- **Aspect ratios:** 4:5, 1:1
- **Headline budget:** 18–70 words; 6–18 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** tiny icon_or_symbol_at_end
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `not_needed`
- **Rough Notation:** brackets, underline
- **Zones:**
  - `manifesto` — text at `[0.13, 0.18, 0.48, 0.65]`
- **Avoid:** center alignment; dense full-width block; inconsistent line rhythm

### N03 — Minimal Gradient Statement
A restrained statement floats on a soft gradient or neutral field; bold weight marks the semantic turn.

- **Family:** `narrative_emotion`
- **Roles:** statement, reflection, challenge, bridge
- **Attention path:** first clause → bold phrase → silence
- **Aspect ratios:** 1:1, 4:5
- **Headline budget:** 5–24 words; 2–7 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** none
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `not_needed`
- **Rough Notation:** underline, highlight
- **Zones:**
  - `statement` — text at `[0.12, 0.34, 0.76, 0.33]`
  - `signature` — text at `[0.12, 0.84, 0.32, 0.05]`
- **Avoid:** extra ornaments; more than two emphasis changes; small type

### N04 — Dark Inversion Punchline
A dark interstitial interrupts a light sequence, carrying one strong corrective or confrontational line.

- **Family:** `narrative_emotion`
- **Roles:** pattern_interrupt, warning, hard_truth, contrast_reset
- **Attention path:** black field → white statement → bold ending
- **Aspect ratios:** 1:1, 4:5
- **Headline budget:** 7–26 words; 2–7 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** none
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `not_needed`
- **Rough Notation:** underline
- **Zones:**
  - `statement` — text at `[0.12, 0.34, 0.76, 0.32]`
  - `signature` — text at `[0.12, 0.84, 0.32, 0.05]`
- **Avoid:** using more than once per short carousel; low-contrast gray text; multiple colors

### N05 — Cinematic Scene with Bottom Caption Shell
A coherent cinematic scene occupies the frame while a bottom gradient shell carries a large episodic caption.

- **Family:** `narrative_emotion`
- **Roles:** memory, story_beat, nostalgia_item, episodic_list
- **Attention path:** scene action → highlighted character → caption
- **Aspect ratios:** 3:4, 4:5
- **Headline budget:** 5–16 words; 2–4 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** era_specific_object, household_ritual, technology_artifact, clothing_cue
- **Ideogram 4:** `primary_scene_provider`
- **Qwen-Image-Layered:** `conditional`
- **SAM3:** `character_and_prop_mask_refinement`
- **Rough Notation:** none
- **Zones:**
  - `scene` — image at `[0, 0, 1, 1]`
  - `caption_scrim` — gradient at `[0, 0.66, 1, 0.34]`
  - `caption` — text at `[0.1, 0.77, 0.8, 0.18]`
  - `series_progress` — dots at `[0.35, 0.965, 0.3, 0.015]`
- **Avoid:** caption over important action; style drift across slides; inconsistent character scale

### N06 — Full-Bleed Photo Quote Overlay
A contextual photograph or meme image carries a bold quote in the strongest negative-space region.

- **Family:** `narrative_emotion`
- **Roles:** affirmation, insight, quote, identity_statement
- **Attention path:** context image → quote → kicker
- **Aspect ratios:** 4:5, 3:4, 1:1
- **Headline budget:** 3–13 words; 1–4 lines
- **Body budget:** 0–8 words
- **Micro-semiotic slots:** clothing_cue, brand_object, location_cue, ordinary_life_prop
- **Ideogram 4:** `asset_generation_optional`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `subject_mask_optional`
- **Rough Notation:** underline, highlight
- **Zones:**
  - `photo` — image at `[0, 0, 1, 1]`
  - `quote` — text at `[0.07, 0.24, 0.86, 0.31]`
  - `kicker` — text at `[0.4, 0.52, 0.5, 0.07]`
- **Avoid:** generic stock photo; text over busy area; more than one idea

### N07 — Meme Label Metaphor
An existing or generated scene becomes a compact metaphor by labeling two actors, objects, or forces.

- **Family:** `narrative_emotion`
- **Roles:** humor, relatable_conflict, micro_contradiction, reaction
- **Attention path:** scene gag → label A → label B
- **Aspect ratios:** 4:5, 1:1
- **Headline budget:** 2–8 words; 1–2 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** recognizable_clothing, platform_object, local_brand_cue
- **Ideogram 4:** `scene_or_asset_generation_optional`
- **Qwen-Image-Layered:** `conditional`
- **SAM3:** `object_mask_optional`
- **Rough Notation:** arrow, circle
- **Zones:**
  - `scene` — image at `[0, 0, 1, 1]`
  - `label_a` — text at `[0.18, 0.1, 0.3, 0.1]`
  - `label_b` — text at `[0.42, 0.42, 0.5, 0.12]`
- **Avoid:** three or more labels; explanation paragraph; gag requiring caption to understand

### N08 — Conceptual Metaphor in Negative Space
A sparse conceptual visual—hands, silhouette, lone object, unusual scale—carries the emotional or intellectual metaphor beside short copy.

- **Family:** `narrative_emotion`
- **Roles:** conceptual_bridge, reflection, question, metaphor
- **Attention path:** text → metaphor object → implied relationship
- **Aspect ratios:** 1:1, 4:5
- **Headline budget:** 6–28 words; 2–8 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** ordinary_object_with_symbolic_role
- **Ideogram 4:** `primary_visual_provider`
- **Qwen-Image-Layered:** `conditional`
- **SAM3:** `object_mask_refinement`
- **Rough Notation:** arrow, underline
- **Zones:**
  - `copy` — text at `[0.12, 0.3, 0.58, 0.36]`
  - `metaphor` — image at `[0.56, 0.02, 0.44, 0.96]`
- **Avoid:** literal illustration of the sentence; centered object with no relationship to text; visual clutter

### N09 — Social Post or Article Card
A screenshot-like editorial card mimics a native social post or short article with avatar, headline, body copy, and action icons.

- **Family:** `narrative_emotion`
- **Roles:** authority_post, excerpt, longform_summary, social_proof
- **Attention path:** identity header → headline → body → social actions
- **Aspect ratios:** 1:1, 4:5
- **Headline budget:** 6–16 words; 2–4 lines
- **Body budget:** 45–110 words
- **Micro-semiotic slots:** profile_photo, tiny platform_mark
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `not_needed`
- **Rough Notation:** highlight, underline
- **Zones:**
  - `identity` — avatar_header at `[0.06, 0.04, 0.7, 0.1]`
  - `headline` — text at `[0.06, 0.15, 0.88, 0.18]`
  - `body` — text at `[0.06, 0.34, 0.88, 0.48]`
  - `actions` — icons at `[0.06, 0.86, 0.88, 0.08]`
- **Avoid:** body below readable size; more than 110 words; fake UI controls that dominate content

### F01 — Two-Column Explainer with Hero Card
The slide divides into a structured text column and a large illustrative card or artifact column.

- **Family:** `framework_education`
- **Roles:** lesson, bias, principle, explanation
- **Attention path:** lesson title → examples → hero card
- **Aspect ratios:** 3:4, 4:5, 1:1
- **Headline budget:** 3–10 words; 1–3 lines
- **Body budget:** 25–80 words
- **Micro-semiotic slots:** symbolic_prop_inside_card
- **Ideogram 4:** `asset_generation_for_hero_card`
- **Qwen-Image-Layered:** `conditional`
- **SAM3:** `card_mask_optional`
- **Rough Notation:** highlight, crossed-off, circle
- **Zones:**
  - `title` — text at `[0.07, 0.06, 0.86, 0.18]`
  - `copy` — text at `[0.07, 0.24, 0.45, 0.6]`
  - `hero_card` — image at `[0.55, 0.25, 0.38, 0.58]`
  - `progress` — icons at `[0.36, 0.91, 0.28, 0.04]`
- **Avoid:** copy column wider than hero column without reason; more than seven bullets; weak title hierarchy

### F02 — Definition Spine with Branch List
A highlighted term and short definition connect to a vertical spine carrying six to eight branches.

- **Family:** `framework_education`
- **Roles:** framework_component, taxonomy, mechanism, definition
- **Attention path:** highlighted term → definition → branch scan
- **Aspect ratios:** 3:4, 1:1, 4:5
- **Headline budget:** 1–5 words; 1–3 lines
- **Body budget:** 35–95 words
- **Micro-semiotic slots:** tiny icon_at_branch, paper_texture_detail
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `not_needed`
- **Rough Notation:** highlight, brackets
- **Zones:**
  - `term` — text at `[0.08, 0.36, 0.3, 0.18]`
  - `definition` — text at `[0.08, 0.54, 0.3, 0.16]`
  - `spine` — diagram at `[0.42, 0.08, 0.52, 0.8]`
- **Avoid:** unrelated branch lengths; more than nine branches; tiny serif type

### F03 — Radial Framework Hub
A central hub or axis radiates to numbered framework components, making the system visible at a glance.

- **Family:** `framework_education`
- **Roles:** framework_overview, system_map, recap
- **Attention path:** center hub → numbered spokes → component labels
- **Aspect ratios:** 3:4, 1:1
- **Headline budget:** 0–4 words; 0–2 lines
- **Body budget:** 20–60 words
- **Micro-semiotic slots:** number_badge_style
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `not_needed`
- **Rough Notation:** highlight, circle
- **Zones:**
  - `hub` — diagram at `[0.05, 0.25, 0.48, 0.5]`
  - `components` — text at `[0.15, 0.15, 0.8, 0.7]`
- **Avoid:** more than seven spokes; unequal label hierarchy; unexplained center

### F04 — Timeline Curve and Opportunity Bracket
A horizontal time axis uses a curve, milestone, or event peak plus a bracketed consequence/opportunity period.

- **Family:** `framework_education`
- **Roles:** timeline, progress, before_after_over_time, experience_to_opportunity
- **Attention path:** axis → peak/milestone → bracket implication
- **Aspect ratios:** 4:5, 3:4, 1:1
- **Headline budget:** 0–6 words; 0–2 lines
- **Body budget:** 6–20 words
- **Micro-semiotic slots:** tiny milestone_icon
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `not_needed`
- **Rough Notation:** brackets, circle
- **Zones:**
  - `title` — text at `[0.18, 0.14, 0.3, 0.08]`
  - `timeline` — diagram at `[0.1, 0.28, 0.82, 0.38]`
  - `bracket` — diagram at `[0.45, 0.6, 0.42, 0.14]`
- **Avoid:** decorative graph with no meaning; too many dates; unlabeled peak

### F05 — Numbered Lesson with Before/After Mini-Panels
A consistent lesson shell contains a small sequence number, large title, concise explanation, and two comparison mini-panels.

- **Family:** `framework_education`
- **Roles:** listicle_item, design_lesson, mistake_fix, before_after
- **Attention path:** number → lesson title → explanation → comparison pair
- **Aspect ratios:** 1:1, 4:5
- **Headline budget:** 3–10 words; 1–3 lines
- **Body budget:** 10–34 words
- **Micro-semiotic slots:** tiny example_detail
- **Ideogram 4:** `not_needed_for_shell`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `mini_panel_cutout_optional`
- **Rough Notation:** underline, highlight, crossed-off
- **Zones:**
  - `number` — text at `[0.07, 0.04, 0.12, 0.07]`
  - `title` — text at `[0.07, 0.12, 0.8, 0.18]`
  - `explanation` — text at `[0.07, 0.3, 0.8, 0.12]`
  - `comparison` — two_panel at `[0.07, 0.5, 0.86, 0.36]`
- **Avoid:** different structure between lessons; explanation longer than three lines; mini-panels too small

### F06 — Examples and Test Stack with Hero Card
A teaching slide organizes colored subheads, examples, tests, and corrections in a narrow column beside a symbolic hero card.

- **Family:** `framework_education`
- **Roles:** examples, diagnostic, weak_strong, bias_lesson
- **Attention path:** topic title → subhead labels → examples → hero card
- **Aspect ratios:** 3:4, 4:5
- **Headline budget:** 3–11 words; 1–3 lines
- **Body budget:** 35–100 words
- **Micro-semiotic slots:** archetypal_symbol
- **Ideogram 4:** `hero_card_asset_provider`
- **Qwen-Image-Layered:** `conditional`
- **SAM3:** `card_mask_optional`
- **Rough Notation:** highlight, crossed-off, circle
- **Zones:**
  - `title` — text at `[0.07, 0.06, 0.86, 0.18]`
  - `example_stack` — text at `[0.07, 0.25, 0.47, 0.58]`
  - `hero_card` — image at `[0.56, 0.27, 0.37, 0.54]`
  - `progress` — icons at `[0.36, 0.9, 0.28, 0.04]`
- **Avoid:** uncolored section hierarchy; more than four subhead types; hero card smaller than examples

### F07 — Data Chart with Companion Card
A short formula or step list is paired with a compact chart and a symbolic card, turning evidence into a visual system.

- **Family:** `framework_education`
- **Roles:** data_story, formula, evidence, behavior_curve
- **Attention path:** formula → chart curve → symbolic card
- **Aspect ratios:** 3:4, 4:5, 1:1
- **Headline budget:** 3–10 words; 1–3 lines
- **Body budget:** 20–55 words
- **Micro-semiotic slots:** symbolic_card_detail
- **Ideogram 4:** `card_asset_provider`
- **Qwen-Image-Layered:** `conditional`
- **SAM3:** `not_needed`
- **Rough Notation:** circle, highlight
- **Zones:**
  - `title` — text at `[0.07, 0.06, 0.86, 0.18]`
  - `formula` — text at `[0.07, 0.25, 0.43, 0.28]`
  - `chart` — chart at `[0.07, 0.56, 0.43, 0.26]`
  - `hero_card` — image at `[0.56, 0.26, 0.37, 0.56]`
- **Avoid:** chart without labels; tiny chart; data unsupported by source

### F08 — Action Plan Card Grid
A compact grid maps days, stages, or actions to individual visual cards and labels.

- **Family:** `framework_education`
- **Roles:** action_plan, schedule, recap, multi_step_plan
- **Attention path:** action headline → grid scan → day/action labels
- **Aspect ratios:** 3:4, 4:5, 1:1
- **Headline budget:** 4–12 words; 2–4 lines
- **Body budget:** 14–45 words
- **Micro-semiotic slots:** day_specific_icon
- **Ideogram 4:** `asset_provider_for_cards`
- **Qwen-Image-Layered:** `conditional`
- **SAM3:** `not_needed`
- **Rough Notation:** box, circle
- **Zones:**
  - `title` — text at `[0.1, 0.04, 0.8, 0.17]`
  - `grid` — card_grid at `[0.08, 0.24, 0.84, 0.62]`
  - `progress` — icons at `[0.36, 0.92, 0.28, 0.04]`
- **Avoid:** more than eight cards; unequal card sizes without hierarchy; labels detached from cards

### F09 — Stacked Steps with Numbered Bands
A large count or number anchors the slide while horizontal colored bands reveal steps in sequence.

- **Family:** `framework_education`
- **Roles:** tips, steps, checklist, how_to
- **Attention path:** giant number → band 1 → band 2 → band 3 → guide character
- **Aspect ratios:** 4:5, 3:4, 1:1
- **Headline budget:** 2–8 words; 1–3 lines
- **Body budget:** 6–30 words
- **Micro-semiotic slots:** wardrobe_detail, tiny_mascot_prop
- **Ideogram 4:** `composition_reference_optional`
- **Qwen-Image-Layered:** `conditional`
- **SAM3:** `avatar_cutout_optional`
- **Rough Notation:** arrow, underline, circle
- **Zones:**
  - `count` — text at `[0.05, 0.05, 0.36, 0.32]`
  - `title` — text at `[0.38, 0.08, 0.54, 0.24]`
  - `steps` — stacked_bands at `[0.35, 0.38, 0.58, 0.42]`
  - `avatar` — image at `[0.03, 0.44, 0.32, 0.48]`
- **Avoid:** more than five steps; equal emphasis on count and every band; too many decorations

### F10 — Question with Evidence Object Row
A provocative question occupies the upper half while a quiet row of repeated objects visualizes accumulation, decay, or evidence.

- **Family:** `framework_education`
- **Roles:** question, evidence, quantity, reflection
- **Attention path:** question → bold phrase → evidence row
- **Aspect ratios:** 1:1, 4:5
- **Headline budget:** 8–28 words; 3–8 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** everyday_discarded_object, receipt, saved_item_symbol
- **Ideogram 4:** `asset_generation_optional`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `object_mask_optional`
- **Rough Notation:** underline, circle
- **Zones:**
  - `question` — text at `[0.12, 0.22, 0.76, 0.34]`
  - `evidence` — image_row at `[0.12, 0.65, 0.76, 0.22]`
- **Avoid:** evidence row too literal; more than one row; tiny objects without silhouette

### J01 — Bad vs Good Side-by-Side
Two equally sized examples are compared beneath a numbered lesson and marked with a red rejection and green approval.

- **Family:** `comparison_juxtaposition`
- **Roles:** before_after, mistake_fix, quality_comparison
- **Attention path:** lesson title → bad panel → good panel → verdict icons
- **Aspect ratios:** 1:1, 4:5
- **Headline budget:** 4–12 words; 1–3 lines
- **Body budget:** 0–20 words
- **Micro-semiotic slots:** micro_detail_inside_examples
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `optional_mask_for_examples`
- **Rough Notation:** crossed-off, box
- **Zones:**
  - `lesson` — text at `[0.06, 0.1, 0.88, 0.2]`
  - `bad` — image at `[0.06, 0.4, 0.42, 0.38]`
  - `good` — image at `[0.52, 0.4, 0.42, 0.38]`
  - `verdicts` — icons at `[0.18, 0.8, 0.64, 0.08]`
- **Avoid:** different panel sizes; no clear verdict; more than one comparison dimension

### J02 — Say / Don’t Say Split
The canvas is divided into opposing tinted halves with mirrored content and explicit verbal alternatives.

- **Family:** `comparison_juxtaposition`
- **Roles:** language_reframe, wrong_right, script_rewrite
- **Attention path:** left label → left examples → right label → right alternatives
- **Aspect ratios:** 1:1, 4:5
- **Headline budget:** 2–8 words; 1–2 lines
- **Body budget:** 20–70 words
- **Micro-semiotic slots:** background_scene_detail
- **Ideogram 4:** `background_asset_optional`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `not_needed`
- **Rough Notation:** crossed-off, underline
- **Zones:**
  - `left` — panel at `[0, 0, 0.5, 1]`
  - `right` — panel at `[0.5, 0, 0.5, 1]`
  - `left_label` — text at `[0.06, 0.08, 0.38, 0.12]`
  - `right_label` — text at `[0.56, 0.08, 0.38, 0.12]`
- **Avoid:** different copy lengths per side; weak tint contrast; center seam clutter

### J03 — Contextual Photo A/B Choice
Two photo-driven alternatives share the same message, demonstrating how context, gaze, or whitespace changes meaning.

- **Family:** `comparison_juxtaposition`
- **Roles:** choice, context_comparison, visual_flow
- **Attention path:** instruction → option A → option B → verdict
- **Aspect ratios:** 1:1, 4:5
- **Headline budget:** 4–14 words; 1–3 lines
- **Body budget:** 0–18 words
- **Micro-semiotic slots:** gaze_direction, clothing_detail, environment_prop
- **Ideogram 4:** `asset_generation_optional`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `subject_mask_optional`
- **Rough Notation:** arrow, circle
- **Zones:**
  - `instruction` — text at `[0.06, 0.1, 0.88, 0.18]`
  - `option_a` — image at `[0.06, 0.38, 0.42, 0.4]`
  - `option_b` — image at `[0.52, 0.38, 0.42, 0.4]`
  - `verdicts` — icons at `[0.18, 0.81, 0.64, 0.07]`
- **Avoid:** options with different crop ratios; text obscured by subject; ambiguous verdict

### J04 — Weak / Strong or Old / New Contrast Cards
Two cards show the same idea under different contrast, hierarchy, wording, or stylistic treatment.

- **Family:** `comparison_juxtaposition`
- **Roles:** weak_strong, old_new, contrast_effect, design_comparison
- **Attention path:** contrast label → card A → card B → principle
- **Aspect ratios:** 1:1, 3:4, 4:5
- **Headline budget:** 3–12 words; 1–3 lines
- **Body budget:** 0–18 words
- **Micro-semiotic slots:** tiny difference_cue
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `not_needed`
- **Rough Notation:** highlight, crossed-off
- **Zones:**
  - `title` — text at `[0.06, 0.08, 0.88, 0.18]`
  - `card_a` — image at `[0.08, 0.38, 0.4, 0.38]`
  - `card_b` — image at `[0.52, 0.38, 0.4, 0.38]`
  - `verdicts` — icons at `[0.18, 0.79, 0.64, 0.08]`
- **Avoid:** different underlying message; too many changed variables; no explanatory title

### J05 — Quad Collage Comparison
Four equal images provide variations of one category, object, event, or mood for rapid comparative scanning.

- **Family:** `comparison_juxtaposition`
- **Roles:** visual_examples, variation_set, category_comparison
- **Attention path:** upper-left → upper-right → lower-left → lower-right → label
- **Aspect ratios:** 1:1, 4:5
- **Headline budget:** 0–4 words; 0–2 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** object_variant, ritual_detail
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `individual_crop_optional`
- **Rough Notation:** box
- **Zones:**
  - `grid` — image_grid at `[0, 0, 1, 1]`
  - `label` — text at `[0.32, 0.44, 0.36, 0.12]`
- **Avoid:** one image dominating accidentally; inconsistent white balance; unrelated categories

### J06 — Dominant Exception Contrast
One subject is visually isolated by color, scale, or uniqueness among repeated or desaturated peers.

- **Family:** `comparison_juxtaposition`
- **Roles:** identity_contrast, exception, rare_vs_common, hero_selection
- **Attention path:** pattern field → exception subject → headline
- **Aspect ratios:** 4:5, 3:4, 1:1
- **Headline budget:** 3–11 words; 1–3 lines
- **Body budget:** 0–8 words
- **Micro-semiotic slots:** distinctive_clothing_or_object_on_hero
- **Ideogram 4:** `primary_composition_provider`
- **Qwen-Image-Layered:** `recommended`
- **SAM3:** `hero_and_crowd_masks`
- **Rough Notation:** circle, arrow
- **Zones:**
  - `pattern` — image at `[0, 0, 1, 1]`
  - `headline` — text at `[0.08, 0.28, 0.84, 0.22]`
- **Avoid:** exception too subtle; multiple exceptions; headline obscuring exception

### B01 — Social Profile Mockup
A branded social profile is displayed inside a device mockup beneath a clear format title.

- **Family:** `identity_brand`
- **Roles:** case_study, brand_system, profile_showcase
- **Attention path:** title → device → profile details
- **Aspect ratios:** 4:5, 1:1
- **Headline budget:** 2–5 words; 1–2 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** profile_avatar, highlight_icon
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `device_mask_optional`
- **Rough Notation:** circle
- **Zones:**
  - `title` — text at `[0.12, 0.08, 0.76, 0.18]`
  - `device` — image at `[0.18, 0.25, 0.64, 0.72]`
- **Avoid:** illegible UI; device too small; title competing with mockup

### B02 — Content Portfolio Grid
Two to six branded content outputs are shown as a coherent portfolio under a format heading.

- **Family:** `identity_brand`
- **Roles:** case_study, proof, content_system
- **Attention path:** format title → first thumbnail → second thumbnail → system coherence
- **Aspect ratios:** 4:5, 1:1
- **Headline budget:** 2–5 words; 1–2 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** consistent_brand_mark_in_thumbnails
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `not_needed`
- **Rough Notation:** box
- **Zones:**
  - `title` — text at `[0.12, 0.08, 0.76, 0.18]`
  - `portfolio` — image_grid at `[0.08, 0.28, 0.84, 0.63]`
- **Avoid:** mixed brands; unequal thumbnail resolution; too many examples

### B03 — Palette Swatches with Avatar
Large color swatches communicate the visual system while a character cutout overlaps them for identity and scale.

- **Family:** `identity_brand`
- **Roles:** brand_palette, visual_constitution, identity_showcase
- **Attention path:** title → swatches → avatar → color codes
- **Aspect ratios:** 4:5, 1:1
- **Headline budget:** 1–4 words; 1–2 lines
- **Body budget:** 0–8 words
- **Micro-semiotic slots:** costume_or_accessory_brand_cue
- **Ideogram 4:** `avatar_asset_provider_optional`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `avatar_cutout_required`
- **Rough Notation:** box
- **Zones:**
  - `title` — text at `[0.18, 0.08, 0.64, 0.15]`
  - `swatches` — swatch_grid at `[0.1, 0.25, 0.8, 0.6]`
  - `avatar` — image at `[0.3, 0.36, 0.42, 0.6]`
- **Avoid:** avatar hiding all swatches; unlabeled colors; more than six primary swatches

### B04 — Single Asset Mockup Stage
One finished content asset is centered and framed as a portfolio artifact against a quiet branded background.

- **Family:** `identity_brand`
- **Roles:** case_study, asset_showcase, proof
- **Attention path:** format title → single asset → fine details
- **Aspect ratios:** 4:5, 1:1
- **Headline budget:** 2–6 words; 1–2 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** tiny watermark_or_brand_stamp
- **Ideogram 4:** `asset_generation_optional`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `not_needed`
- **Rough Notation:** box
- **Zones:**
  - `title` — text at `[0.12, 0.08, 0.76, 0.18]`
  - `asset` — image at `[0.22, 0.28, 0.56, 0.62]`
- **Avoid:** small asset; decorative clutter; background stronger than artifact

### B05 — Character Brand Hero
A recognizable character or branded avatar anchors the composition with a bold identity-led title.

- **Family:** `identity_brand`
- **Roles:** brand_intro, persona_case_study, identity_hook
- **Attention path:** face → title → costume/brand cues
- **Aspect ratios:** 4:5, 3:4, 1:1
- **Headline budget:** 3–11 words; 2–5 lines
- **Body budget:** 0–5 words
- **Micro-semiotic slots:** costume, badge, wand_or_tool, hair_or_accessory
- **Ideogram 4:** `primary_character_composition_provider`
- **Qwen-Image-Layered:** `recommended`
- **SAM3:** `hero_cutout_refinement`
- **Rough Notation:** highlight
- **Zones:**
  - `hero` — image at `[0.12, 0.18, 0.76, 0.82]`
  - `title` — text at `[0.12, 0.54, 0.76, 0.3]`
- **Avoid:** generic character; missing identity prop; headline hiding face

### C01 — Portrait and Social Actions CTA
A large portrait sits beside a direct question or continuation prompt with social action icons below.

- **Family:** `cta_closing`
- **Roles:** cta, part_two_prompt, discussion_prompt
- **Attention path:** question → face → action icons
- **Aspect ratios:** 1:1, 4:5
- **Headline budget:** 5–18 words; 2–7 lines
- **Body budget:** 0–12 words
- **Micro-semiotic slots:** clothing_detail, small_profile_badge
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `portrait_cutout_required`
- **Rough Notation:** underline, arrow
- **Zones:**
  - `prompt` — text at `[0.07, 0.2, 0.45, 0.44]`
  - `portrait` — image at `[0.52, 0.08, 0.46, 0.9]`
  - `actions` — icons at `[0.07, 0.78, 0.36, 0.12]`
- **Avoid:** generic “follow for more” only; portrait too small; icons without prompt

### C02 — Keyword Comment CTA with Portrait
A highlighted keyword command sits above a portrait framed by a hand-drawn aura or circle.

- **Family:** `cta_closing`
- **Roles:** lead_magnet_cta, comment_keyword, resource_offer
- **Attention path:** setup → highlighted keyword → portrait → offer detail
- **Aspect ratios:** 3:4, 4:5, 1:1
- **Headline budget:** 2–8 words; 1–2 lines
- **Body budget:** 8–24 words
- **Micro-semiotic slots:** profile_accessory
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `portrait_cutout_required`
- **Rough Notation:** highlight, circle
- **Zones:**
  - `setup` — text at `[0.14, 0.05, 0.72, 0.1]`
  - `keyword` — text at `[0.1, 0.16, 0.8, 0.14]`
  - `portrait` — image at `[0.24, 0.32, 0.52, 0.63]`
  - `detail` — text at `[0.12, 0.28, 0.76, 0.08]`
- **Avoid:** multiple keywords; weak offer; portrait without eye contact

### C03 — Repost / Share Arrow CTA
A creator portrait, large directional/repost icon, and supporting cards create an explicit share action.

- **Family:** `cta_closing`
- **Roles:** share_cta, repost_cta, save_cta
- **Attention path:** share headline → face → arrow/repost symbol → proof card
- **Aspect ratios:** 3:4, 4:5
- **Headline budget:** 4–13 words; 2–4 lines
- **Body budget:** 0–8 words
- **Micro-semiotic slots:** held_card_detail, wardrobe_cue
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `conditional`
- **SAM3:** `portrait_cutout_required`
- **Rough Notation:** arrow, circle
- **Zones:**
  - `headline` — text at `[0.1, 0.04, 0.8, 0.19]`
  - `portrait` — image at `[0.02, 0.32, 0.58, 0.66]`
  - `symbol` — icon at `[0.5, 0.34, 0.34, 0.25]`
  - `proof_card` — image at `[0.58, 0.58, 0.25, 0.3]`
- **Avoid:** small action symbol; ambiguous action; too many supporting cards

### C04 — Character Pair Share CTA
Two recognizable characters or creator/character pairings support a large emotional share request.

- **Family:** `cta_closing`
- **Roles:** share_cta, community_invitation, case_study_close
- **Attention path:** share request → character pair → brand symbol
- **Aspect ratios:** 4:5, 1:1
- **Headline budget:** 5–18 words; 2–5 lines
- **Body budget:** 0–6 words
- **Micro-semiotic slots:** costume, shared_symbol, franchise_or_tribal_cue
- **Ideogram 4:** `character_composition_provider`
- **Qwen-Image-Layered:** `conditional`
- **SAM3:** `character_masks_required`
- **Rough Notation:** underline
- **Zones:**
  - `headline` — text at `[0.08, 0.08, 0.84, 0.3]`
  - `characters` — image at `[0.06, 0.32, 0.88, 0.65]`
- **Avoid:** characters at unrelated scales; copy over faces; weak relationship between pair

### C05 — Text-Only Final Challenge
A minimal final line creates urgency or a behavioral challenge with no visual distraction.

- **Family:** `cta_closing`
- **Roles:** final_challenge, behavioral_cta, closing_punchline
- **Attention path:** short statement → emphasized final word
- **Aspect ratios:** 1:1, 4:5, 3:4
- **Headline budget:** 3–12 words; 1–4 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** none
- **Ideogram 4:** `not_needed`
- **Qwen-Image-Layered:** `not_needed`
- **SAM3:** `not_needed`
- **Rough Notation:** underline, highlight
- **Zones:**
  - `statement` — text at `[0.12, 0.36, 0.76, 0.26]`
  - `signature` — text at `[0.12, 0.84, 0.32, 0.05]`
- **Avoid:** generic CTA; secondary paragraph; decorative image

### C06 — Scene-Based Brand Promise Close
The same cinematic series shell closes on a brand promise, transformation statement, or invitation rather than another list item.

- **Family:** `cta_closing`
- **Roles:** brand_promise, service_positioning, emotional_close
- **Attention path:** scene → creator action → brand promise
- **Aspect ratios:** 3:4, 4:5
- **Headline budget:** 6–18 words; 2–5 lines
- **Body budget:** 0–0 words
- **Micro-semiotic slots:** production_tool, memory_object, brand_signature
- **Ideogram 4:** `scene_provider_optional`
- **Qwen-Image-Layered:** `conditional`
- **SAM3:** `subject_mask_optional`
- **Rough Notation:** none
- **Zones:**
  - `scene` — image at `[0, 0, 1, 1]`
  - `scrim` — gradient at `[0, 0.64, 1, 0.36]`
  - `promise` — text at `[0.1, 0.76, 0.8, 0.19]`
- **Avoid:** abrupt style change; generic follow CTA; promise disconnected from series

## 6. Sequence grammars

### S01 — Minimal Motivation Arc
- **Length:** 5–7 slides
- **Beat chain:** H01 or H05 cover → N01/N03 premise → N02 pressure or rules → F04 mechanism/timeline → C05 landing
- **Source:** Carousel 1

### S02 — Photo Quote Micro-Series
- **Length:** 3–6 slides
- **Beat chain:** N06 hook → N06 reinforcement → N07 or N08 twist → C05 optional close
- **Source:** Carousels 2–7

### S03 — Psychology Listicle with Artifact Cards
- **Length:** 9–12 slides
- **Beat chain:** H02 cover → H03 premise → F06 lessons × N → F07 evidence lesson optional → F08 action plan → C03 share CTA
- **Source:** Carousel 8

### S04 — Framework Decomposition
- **Length:** 7–9 slides
- **Beat chain:** H05 cover → F03 framework overview → F02 component slides × N → C02 keyword CTA
- **Source:** Carousel 9

### S05 — Brand Case Study
- **Length:** 7–10 slides
- **Beat chain:** H02/B05 hook → B01 profile → B02 portfolio formats → B03 palette → B04 hero assets → C04 share close
- **Source:** Carousel 10

### S06 — Nostalgia Memory Roll
- **Length:** 8–20 slides
- **Beat chain:** N05 hook memory → N05 recurring memory beats × N → C06 brand promise
- **Source:** Carousel 11

### S07 — Moodboard List
- **Length:** 5–10 slides
- **Beat chain:** H08 category beats × N → C05 question or save CTA
- **Source:** Carousel Grid Mood Date

### S08 — Do/Don’t Educational Guide
- **Length:** 7–11 slides
- **Beat chain:** H04 cover → J01/J03/J04 lessons × N → C01 continuation CTA
- **Source:** Carousel LISTICLE + JUXTAPOSITION

### S09 — Numbered Design Lesson Listicle
- **Length:** 7–11 slides
- **Beat chain:** H03 cover → F05 numbered lesson × N → C01 part-two CTA
- **Source:** Carousel LISTICLE TEMPLATE

### S10 — Minimal Confrontation Arc
- **Length:** 7–10 slides
- **Beat chain:** H04 or H03 hook → N03 recognition → N04 hard truth → F10 evidence/question → N03 resolution → C05 action
- **Source:** Minimal Style CAROUSEL

### S11 — Visual Taxonomy / System Breakdown
- **Length:** 6–9 slides
- **Beat chain:** H05 cover → F03 overview → F02 definitions → F04 timeline optional → F08 action plan → C02 resource CTA
- **Source:** Cross-corpus synthesis

### S12 — Mixed-Media Personal Brand Explainer
- **Length:** 6–10 slides
- **Beat chain:** H04 personal hook → N08 metaphor → F01/F06 teaching → J03 contrast → F09 steps → C01/C03 CTA
- **Source:** CCP target paper-cut system

## 7. Carousel Builder Engine

```text
Brand Context Version + Expression Moment + Archetype + Asset Derivative
                         ↓
DSPy Carousel Narrative Compiler
                         ↓
CarouselNarrativeSpec + SlideIntent[]
                         ↓
Sequence Grammar Router
                         ↓
Composition Router against the 44-spec registry
                         ↓
Ideogram 4 only for high-entropy composition/scene tasks
                         ↓
GPT Image / Flux for assets, identity edits, and repair
                         ↓
Qwen-Image-Layered when a generated plate needs editable RGBA layers
                         ↓
SAM3 for exact subject/object masks and cutout refinement
                         ↓
Skia + DOM typography + Rough Notation production render
                         ↓
Slide Eval → Sequence Eval → Human Review → Export/Publish
```

### 7.1 Why the renderer should be hybrid

- **Skia:** paper textures, masks, shadows, image treatment, vector geometry, gradients, grain, collage edges, and deterministic raster output.
- **DOM/CSS typography:** exact line breaking, text measurement, accessibility, and editable copy.
- **Rough Notation:** underline, box, circle, highlight, strike-through, crossed-off, and brackets only when there is a semantic reason.
- **Remotion:** one-frame static exports and motion-carousel/video variants can consume the same render contract, preventing layout drift.

### 7.2 Ideogram 4 routing rule

Ideogram 4 is not called for every slide. Call it when the slide depends on spatial invention: cinematic poster, conceptual metaphor, recurring scene, unusual object crop, moodboard plate, or subject–typography interaction. Do not call it for branch diagrams, deterministic text slides, before/after shells, article cards, or exact data graphics.

### 7.3 Qwen-Image-Layered routing rule

Invoke it after a useful flat visual plate exists and only when independent movement, replacement, recoloring, or repair is valuable. Pure typography and deterministic diagram slides bypass it. Decomposed layers must still pass semantic naming, alpha-edge, occlusion, and z-order QC before entering the asset library.

### 7.4 Rough Notation doctrine

Every annotation must have a semantic reason: emphasis, contrast, rejection, connection, proof, or action. Default limit: two annotations per slide, four only for explicit instructional/step compositions. Decorative scribbles that do not change comprehension are prohibited.

## 8. Composition routing

The router should retrieve 3–5 candidates and score them rather than select by prompt intuition alone.

```text
composition_score =
  0.24 × semantic_role_fit
+ 0.18 × copy_budget_fit
+ 0.16 × asset_availability_fit
+ 0.12 × sequence_position_fit
+ 0.10 × brand_style_fit
+ 0.08 × micro_semiotic_anchor_fit
+ 0.07 × aspect_ratio_fit
+ 0.05 × sequence_diversity_gain
- repetition_penalty
- generation_cost_penalty
```

The diversity planner should block the same composition ID from appearing on adjacent slides unless the sequence grammar intentionally uses a fixed shell such as N05.

## 9. Evaluation gates

- Semantic-role clarity: can a reviewer state the slide’s job in one phrase?
- Hook singularity: cover contains one dominant promise or tension.
- Swipe momentum: each slide opens or advances a loop rather than merely repeating.
- Hierarchy: focal order is visible at thumbnail scale.
- Legibility: text remains readable on a 320 px-wide preview.
- Copy fit: text stays inside composition-specific budgets.
- Visual contribution: images add metaphor, proof, identity, contrast, or context.
- Brand coherence: Brand Context Version, palette, typography, texture, and identity assets are respected.
- Micro-Semiotic Anchor quality: recognizable, subtle, relevant, and non-distracting.
- Sequence rhythm: density and format vary deliberately across the set.
- Source fidelity: claims trace to expression moments, evidence, or approved brand knowledge.
- Editability: generated plates are decomposed only where the downstream value justifies it.

## 10. Files in this bundle

- `CCP_CAROUSEL_COMPOSITION_ATLAS_V1.md` — human-readable architecture and atlas.
- `carousel_composition_registry_v1.json` — 44 executable composition entries and 12 sequence grammars.
- `carousel_composition_models.py` — Pydantic contracts for the Python harness.
- `carousel_corpus_mapping_v1.csv` — every one of the 118 inspected slides mapped to a canonical spec.