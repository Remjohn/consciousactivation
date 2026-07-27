# CCP / CMF V3 — Brand Genesis, Creative Control Tower & Micro-Semiotic Paper-Cut Pipeline

**Document Type:** Production Architecture + Creative Pipeline Specification  
**Project:** Conscious Coaching Platform / Conscious Media Factory / Conscious Rivers  
**Version:** V3.0 — Brand Genesis & Operator Control Tower Update  
**Status:** Implementation Draft  
**Primary Goal:** Define the production system for onboarding each brand/client, manufacturing reusable creative assets, managing editing sessions, rendering coherent media, and preserving narrative/visual memory across future interviews.

---

## 0. Executive Summary

The Conscious Media Factory (CMF) should now be treated as a **multi-brand creative operations app**, not merely as a renderer.

The app must support three connected loops:

```text
1. Brand Genesis Loop
   Client photos + brand data
   → reusable creative universe
   → approved Brand Context v1

2. Expression-to-Asset Loop
   Interview / Complete Expression Session
   → expression moments
   → archetype routes
   → asset package spec
   → Complete Editing Sessions

3. Control Tower Loop
   editing queue
   → render jobs
   → evaluation receipts
   → approval
   → scheduling / Publer publishing
   → brand memory update
```

The key architectural upgrade is that onboarding is no longer “client setup.” It is the manufacturing of a **versioned creative substrate** for each client.

For each brand, CMF should create and maintain:

- a Brand Workspace,
- a Brand Context Version,
- an Identity Pack,
- a 64-state Acting Library,
- a Paper-Cut Avatar Rig,
- a Facial Expression Library,
- a Prop/Object Library,
- a Motion Primitive Library,
- a Sound Effect Library,
- a Micro-Semiotic Anchor Library,
- a Composition Preference Library,
- a Publishing Profile,
- and a memory layer that improves after every interview and render.

The first client-facing product remains the **Guest Asset Pack** or **Monthly Asset Engine**, but the internal operator product becomes the **CMF Control Tower**: a PWA + private Telegram operator cockpit + batch rendering workers + Publer publishing adapter.

---

## 1. Strategic Source Alignment

This V3 document preserves and extends the existing CCP doctrine:

### From V5

CMF remains built around **orchestration over generation**. The Complete Editing Session remains the downstream test boundary for media production. Visuals are not decorative; they are the visible phenotype of the system’s identity, psychology, and narrative intelligence.

### From V9

The launch center of gravity is now **Interview-First Expression**. CCP begins with human activation, not Telegram-first software adoption. The core loop is:

```text
Activation → Articulation → Asset Creation → Narrative Memory → Product Expansion
```

### From V9.1

Every interview is a **Complete Expression Session**. Every content-intended question is an **Interview Asset Contract**. Every useful answer becomes one or more **Expression Moments**. Every asset route becomes a **Complete Editing Session**. Every rendered asset receives an **Evaluation Receipt**.

### New in V3

This update adds the missing brand-level creative substrate:

```text
Brand Genesis Session
→ Brand Context Version
→ Reusable Creative Libraries
→ Future Expression Sessions
→ Coherent CMF Outputs
```

---

## 2. Product Surfaces

CMF should expose three operational surfaces.

### 2.1 CMF PWA Control Tower

The PWA is the primary operating system.

It manages:

- brands,
- onboarding,
- photo uploads,
- consent,
- generated asset packs,
- approval grids,
- expression sessions,
- asset packages,
- editing sessions,
- render queues,
- evaluation receipts,
- publishing calendar,
- Publer integration,
- brand memory.

The PWA is where the operator makes deep decisions.

### 2.2 Private Telegram Operator Bot

Telegram is **not** the client-facing product in the first phase.

Telegram becomes your private operator cockpit.

It handles:

- render-ready notifications,
- batch-finished notifications,
- failed worker alerts,
- quick approve / reject / regenerate actions,
- Publer scheduling confirmation,
- links back into the PWA.

Telegram is for mobile operations, not deep editing.

### 2.3 Publer Publishing Adapter

Publer should be a publishing adapter, not the system of record.

CMF owns:

- approval state,
- brand context,
- source expression traceability,
- captions,
- render outputs,
- evaluation receipts,
- publishing intents.

Publer handles:

- media upload,
- social account connections,
- scheduling,
- publishing,
- status retrieval,
- analytics retrieval.

---

## 3. System Topology

```text
                     ┌──────────────────────────┐
                     │     CMF PWA Control UI    │
                     └────────────┬─────────────┘
                                  │
                     ┌────────────▼─────────────┐
                     │    API / App Backend      │
                     └────────────┬─────────────┘
                                  │
        ┌─────────────────────────┼───────────────────────────┐
        │                         │                           │
┌───────▼────────┐      ┌─────────▼──────────┐       ┌────────▼─────────┐
│ Brand Service  │      │ Expression Service │       │ Editing Service  │
└───────┬────────┘      └─────────┬──────────┘       └────────┬─────────┘
        │                         │                           │
        └───────────────┬─────────┴───────────────┬───────────┘
                        │                         │
              ┌─────────▼─────────┐     ┌─────────▼──────────┐
              │ Postgres / RLS    │     │ Object Storage      │
              └─────────┬─────────┘     └─────────┬──────────┘
                        │                         │
                  ┌─────▼─────┐             ┌─────▼─────┐
                  │ Job Queue │────────────▶│ Workers   │
                  └─────┬─────┘             └─────┬─────┘
                        │                         │
         ┌──────────────▼─────────────────────────▼──────────────┐
         │ Remotion / Motion Canvas / Manim / GPU Batch Workers   │
         └──────────────┬─────────────────────────┬──────────────┘
                        │                         │
                ┌───────▼────────┐       ┌────────▼───────────┐
                │ Review Outputs │       │ Evaluation Receipts │
                └───────┬────────┘       └────────┬───────────┘
                        │                         │
          ┌─────────────▼─────────────────────────▼────────────┐
          │ Approval Service + Publishing Intent Service        │
          └─────────────┬──────────────────────────────────────┘
                        │
              ┌─────────▼──────────┐
              │ Publer API Adapter │
              └─────────┬──────────┘
                        │
              ┌─────────▼──────────┐
              │ Social Platforms    │
              └────────────────────┘

Private Telegram Operator Bot plugs into:
API / Job Queue / Approval Service / Publishing Intent Service.
```

---

## 4. Core Data Objects

### 4.1 Brand Workspace

The central tenant-level object for each client or brand.

```json
{
  "brand_id": "brand_001",
  "brand_name": "Client Brand",
  "status": "active",
  "primary_language": "fr",
  "industry": "holistic_health",
  "active_brand_context_version_id": "bcv_001",
  "publishing_profile_id": "pubprof_001"
}
```

### 4.2 Brand Genesis Session

The onboarding production session that creates the brand’s reusable creative universe.

```json
{
  "brand_genesis_session_id": "bgs_001",
  "brand_id": "brand_001",
  "input_photos": [],
  "input_brand_notes": {},
  "consent_record": {},
  "generated_packs": [],
  "review_status": "in_progress",
  "output_brand_context_version_id": "bcv_001"
}
```

### 4.3 Brand Context Version

The frozen creative state used by future editing sessions.

```json
{
  "brand_context_version_id": "bcv_001",
  "brand_id": "brand_001",
  "identity_pack_id": "identity_pack_v1",
  "acting_library_version_id": "acting_64_v1",
  "papercut_avatar_rig_id": "rig_v1",
  "visual_constitution_id": "visual_editorial_papercut_v1",
  "micro_semiotic_anchor_library_id": "msa_lib_v1",
  "motion_library_id": "motion_v1",
  "sfx_library_id": "sfx_v1",
  "composition_preference_library_id": "comprefs_v1",
  "snapshot_hash": "sha256...",
  "locked": true
}
```

### 4.4 Complete Expression Session

The upstream human expression event.

```text
Interview / podcast / roundtable / guided solo recording
→ transcript
→ expression moments
→ asset package candidates
```

### 4.5 Complete Editing Session

The downstream media-rendering job.

```json
{
  "complete_editing_session_id": "ces_001",
  "brand_id": "brand_001",
  "brand_context_version_id": "bcv_001",
  "source_expression_session_id": "xes_001",
  "source_expression_moment_id": "em_003",
  "asset_type": "short_video",
  "core_archetype": "Myth Debunk",
  "asset_derivative": "Scene-to-Principle",
  "cmf_route": "Paper-Cut Explainer",
  "visual_style": "editorial_2_5d_papercut_reel",
  "status": "queued"
}
```

---

## 5. Brand Genesis Session: Full Onboarding Flow

### Stage 1 — Client Intake

Collect:

- client name,
- brand name,
- industry,
- audience,
- offer,
- platform targets,
- tone preferences,
- forbidden tone,
- visual style preferences,
- forbidden visual styles,
- content goals,
- examples they like,
- examples they dislike.

### Stage 2 — Likeness Consent

Before generating assets from a real person, store explicit consent.

Consent should cover:

- use of uploaded photos,
- creation of realistic synthetic images,
- creation of stylized paper-cut avatars,
- use of likeness in social media assets,
- use of likeness in memes or humorous contexts,
- whether exact face likeness is allowed,
- whether parody-style output is allowed,
- whether generated assets can be stored for future sessions.

### Stage 3 — Photo Upload

Recommended input:

```text
5–10 photos minimum:
- front-facing neutral
- smiling
- serious
- 3/4 left
- 3/4 right
- full body
- natural candid
- professional brand photo
- expressive / animated photo
- optional seated or casual pose

Optional but valuable:
- 30–60 second vertical video of the client speaking naturally
```

Photos provide identity. Video provides performance cues.

### Stage 4 — Source Photo Quality Check

Auto-check:

- face visibility,
- resolution,
- blur,
- lighting,
- angle diversity,
- occlusion,
- duplicates,
- expression diversity,
- full-body availability.

### Stage 5 — Identity Summary

The agent generates a visual identity summary.

```json
{
  "identity_summary_id": "ids_001",
  "brand_id": "brand_001",
  "stable_traits": [
    "hair shape",
    "face shape",
    "skin tone range",
    "signature clothing",
    "common expression"
  ],
  "do_not_change": [
    "do not make the client younger",
    "do not over-smooth skin",
    "do not change hairstyle",
    "do not alter body type"
  ],
  "approved_style_modes": [
    "realistic_reference",
    "photo_paper_cutout",
    "editorial_papercut_avatar"
  ]
}
```

This becomes part of visual Negative Space.

---

## 6. The 64-State Acting Library

The 64 assets are not random poses.

They are **emotional-performance primitives**.

### 6.1 Emotional Families

```text
1. confident
2. warm
3. reflective
4. serious
5. challenging
6. playful
7. urgent
8. celebratory
```

### 6.2 Gesture / Body-Language Families

```text
1. open-hands explaining
2. pointing / directing
3. inviting / open palms
4. grounded authority
5. thinking / hand-to-face
6. emphasis gesture
7. uncertainty / shrug
8. dynamic uplift
```

### 6.3 8 × 8 Matrix

| Emotion \ Gesture | Open Explain | Point / Direct | Invite | Authority | Think | Emphasis | Shrug / Tension | Dynamic Uplift |
|---|---|---|---|---|---|---|---|---|
| Confident | confident_open_explain | confident_point | confident_invite | confident_authority | confident_think | confident_emphasis | confident_shrug | confident_uplift |
| Warm | warm_open_explain | warm_point | warm_invite | warm_authority | warm_think | warm_emphasis | warm_shrug | warm_uplift |
| Reflective | reflective_open_explain | reflective_point | reflective_invite | reflective_authority | reflective_think | reflective_emphasis | reflective_shrug | reflective_uplift |
| Serious | serious_open_explain | serious_point | serious_invite | serious_authority | serious_think | serious_emphasis | serious_shrug | serious_uplift |
| Challenging | challenging_open_explain | challenging_point | challenging_invite | challenging_authority | challenging_think | challenging_emphasis | challenging_shrug | challenging_uplift |
| Playful | playful_open_explain | playful_point | playful_invite | playful_authority | playful_think | playful_emphasis | playful_shrug | playful_uplift |
| Urgent | urgent_open_explain | urgent_point | urgent_invite | urgent_authority | urgent_think | urgent_emphasis | urgent_shrug | urgent_uplift |
| Celebratory | celebratory_open_explain | celebratory_point | celebratory_invite | celebratory_authority | celebratory_think | celebratory_emphasis | celebratory_shrug | celebratory_uplift |

### 6.4 Acting Reference Metadata

```json
{
  "asset_id": "act_confident_open_explain_01",
  "brand_id": "brand_001",
  "asset_type": "realistic_acting_reference",
  "emotion_primary": "confident",
  "gesture_family": "open_hands_explaining",
  "body_language": "upright_open",
  "facial_expression": "confident_half_smile",
  "energy_level": "medium_high",
  "framing": "medium_shot",
  "orientation": "front_3_4",
  "layout_bias": "right_side_subject",
  "review_status": "awaiting_review"
}
```

### 6.5 Generation Strategy

Generate in batches of 8.

```text
Batch 1: confident family
Batch 2: warm family
Batch 3: reflective family
...
Batch 8: celebratory family
```

Each batch passes:

```text
generated
→ auto-QC
→ human review
→ approved / needs fix / rejected
→ locked into library
```

### 6.6 No-LoRA Phase 1 Rule

Do not train LoRAs immediately.

Use the 64 approved acting references as:

- body-language references,
- identity references,
- expression references,
- editing references,
- future Flux/GPT Image edit anchors.

Train a LoRA only if the approved-reference workflow fails at real production scale.

---

## 7. Paper-Cut Avatar System

After realistic acting references are approved, generate the **Paper-Cut Avatar Pack**.

This is a separate system from the realistic acting library.

### 7.1 Paper-Cut Avatar Use Cases

- animated explainers,
- myth-busting videos,
- carousels,
- reaction visuals,
- meme visuals,
- poll visuals,
- avatar-based social reels,
- object-led teaching videos.

### 7.2 Required Avatar Assets

#### Head / Facial Expressions

```text
neutral
warm smile
big smile
serious
focused
surprised
thinking
skeptical
concerned
playful
celebratory
```

#### Eye / Brow Layers

```text
neutral eyes
happy eyes
wide eyes
skeptical brow
concerned brow
closed blink
focused squint
```

#### Mouth Shapes

```text
closed
small open
wide open
smile open
oo
ee
m / b / p
frown
```

#### Body Layers

```text
torso
head
neck
left upper arm
left forearm
left hand
right upper arm
right forearm
right hand
left leg
right leg
feet
shadow
```

#### Gesture Variants

```text
pointing left
pointing right
open hands
hand on chin
arms crossed
one hand up
celebration arm
shrug
```

### 7.3 Rig Manifest

```json
{
  "rig_id": "client_001_papercut_rig_v1",
  "type": "2d_cutout_rig",
  "coordinate_system": "vertical_9_16",
  "layers": [
    {
      "layer_id": "torso",
      "file": "torso.png",
      "z_index": 10,
      "anchor": [0.5, 0.15],
      "parent": null
    },
    {
      "layer_id": "head",
      "file": "head_neutral.png",
      "z_index": 30,
      "anchor": [0.5, 0.85],
      "parent": "torso"
    },
    {
      "layer_id": "mouth",
      "file": "mouth_closed.png",
      "z_index": 40,
      "anchor": [0.5, 0.5],
      "parent": "head"
    }
  ],
  "bones": [
    {
      "bone_id": "neck",
      "parent": "torso",
      "child": "head",
      "rotation_limits": [-8, 8]
    },
    {
      "bone_id": "left_elbow",
      "parent": "left_upper_arm",
      "child": "left_forearm",
      "rotation_limits": [-60, 40]
    }
  ],
  "expressions": {
    "happy": {
      "eyes": "eyes_happy.png",
      "mouth": "mouth_smile_open.png"
    },
    "surprised": {
      "eyes": "eyes_wide.png",
      "mouth": "mouth_open_wide.png"
    }
  }
}
```

### 7.4 Rig Preview Tests

Before locking the avatar rig, preview:

- blink,
- nod,
- small head bob,
- open-hands explanation,
- pointing,
- shrug,
- expression swap,
- mouth flap,
- subtle stop-motion jitter.

---

## 8. Paper-Cut Prop / Object Library

Each brand needs a reusable paper object universe.

### 8.1 Core Object Types

```text
headline strips
subtitle strips
paper note cards
number badges
arrows
underlines
stars
bursts
plants
leaves
mountains
clouds
dots
squiggles
mascot poses
icons
stamps
checkmarks
X marks
```

### 8.2 Object Metadata

```json
{
  "asset_id": "paper_arrow_blue_03",
  "brand_id": "brand_001",
  "asset_type": "paper_prop",
  "semantic_type": "arrow",
  "color": "blue",
  "style": "hand_cut_felt",
  "motion_affordances": ["bounce", "wiggle", "point_pulse"],
  "review_status": "approved"
}
```

### 8.3 Object Pack Generation

Minimum recommended pack:

```text
10 headline strips
10 subtitle strips
20 arrows
20 stars / bursts
20 plants / leaves
10 mountains
20 dots / badges
10 squiggles
10 underline strokes
10 callout boxes
10 number circles
5 mascot variants
```

---

## 9. Micro-Semiotic Anchoring Doctrine

### 9.1 Definition

**Micro-Semiotic Anchoring** is the deliberate placement of small, culturally recognizable visual cues inside a composition to trigger audience identification, locality, humor, trust, or tribal recognition without making the cue the main subject.

In simple terms:

```text
Tiny objects that make the viewer feel:
“This was made for people like me.”
```

### 9.2 Why It Matters

A Micro-Semiotic Anchor can:

- localize the content,
- humanize the character,
- create comment triggers,
- prove audience understanding,
- make content feel native instead of generic,
- increase shareability,
- strengthen audience identification before the message is explained.

Example principle:

```text
Fitness content for French audience
→ character wears yellow-and-blue budget-supermarket-coded socks
→ audience recognizes the cultural cue
→ comments increase because the detail feels funny and specific
```

### 9.3 Naming Hierarchy

```text
Doctrine: Micro-Semiotic Anchoring
Library: Micro-Semiotic Anchor Library
Object: Micro-Semiotic Anchor
Evaluation: Micro-Semiotic Anchor Score
```

### 9.4 Anchor Categories

```text
ordinary_life_object
local_brand_cue
cultural_ritual
work_tool
health_object
family_object
status_marker
place_marker
digital_habit
tribal_joke
```

### 9.5 Anchor Schema

```json
{
  "anchor_id": "msa_001",
  "brand_id": "fitness_france_001",
  "anchor_name": "budget supermarket socks",
  "anchor_category": "ordinary_life_object",
  "cultural_context": "French budget fitness audience",
  "audience_signal": "everyday relatable fitness humor",
  "recognition_effect": [
    "relatability",
    "comment_trigger",
    "local familiarity",
    "humor"
  ],
  "visual_description": "yellow and blue budget-supermarket-coded sports socks, visible on the character's feet",
  "preferred_placement": ["feet", "small clothing detail"],
  "prominence_level": "subtle_but_visible",
  "risk_level": "medium",
  "legal_note": "avoid exact protected logo unless licensed; use coded colors or inspired design",
  "approved": true
}
```

### 9.6 Anchor Evaluation

```json
{
  "micro_semiotic_anchor_score": {
    "recognition": 0.91,
    "subtlety": 0.84,
    "brand_fit": 0.88,
    "comment_potential": 0.86,
    "distraction_risk": 0.12,
    "legal_risk": 0.21
  }
}
```

### 9.7 Production Rule

Every high-identification composition should include **1–3 approved Micro-Semiotic Anchors**.

Hard fail if the anchor:

- steals attention from the message,
- stereotypes the audience,
- creates unnecessary legal/trademark risk,
- contradicts the brand,
- feels forced,
- is too generic to be recognized.

---

## 10. Editorial 2.5D Paper-Cut Reel Animation

### 10.1 Style Name

The official style name should be:

```text
Editorial 2.5D Paper-Cut Reel Animation
```

### 10.2 Core Feeling

```text
credible + warm + handmade + premium + educational
```

### 10.3 Motion Principle

```text
Paper gently coming alive.
```

Not:

```text
cartoon stickers bouncing everywhere.
```

### 10.4 Core Techniques

| Technique | Role |
|---|---|
| 2.5D Layering | Essential for paper strips, portraits, props, and depth |
| Parallax Depth | Adds physicality without complex animation |
| Slow Push-In / Drift | Keeps reels alive while preserving calm authority |
| Restrained Typography Reveals | Makes education clear and synchronized |
| Hand-Drawn Reveal | Selective use for arrows, circles, underlines, X marks |
| Selective Floating | Use sparingly for leaves, steam, dots, mascot details |
| Atmospheric Texture | Paper grain, dust, soft light, subtle imperfection |
| Light Pulse / Shadow Pass | Use minimally; avoid mystical overuse |

### 10.5 Motion Constitution

```json
{
  "visual_style": "editorial_2_5d_papercut_reel",
  "motion_language": "paper_gently_coming_alive",
  "motion_intensity": "restrained",
  "max_simultaneous_moving_layers": 4,
  "base_camera_motion": "slow_push_in",
  "camera_scale_range": [1.0, 1.035],
  "global_jitter_px": [0.3, 1.2],
  "global_rotation_jitter_deg": [0.1, 0.8],
  "max_bouncy_events_per_10s": 2,
  "typography_must_sync_to_voice": true,
  "decorative_motion_intensity": "low"
}
```

### 10.6 The Four Animation Jobs

Every animation must serve one of four purposes:

```text
1. Direct attention
2. Reveal meaning
3. Add tactile realism
4. Mark an emotional beat
```

If it does none of these, remove it.

---

## 11. Layer Taxonomy for Paper-Cut Animation

### 11.1 Background Layer

```text
cream_paper_background
```

Motion:

```text
slow_push_in
micro_texture_drift
subtle_light_movement
```

### 11.2 Headline Strips

```text
pink_strip
blue_strip
green_strip
yellow_strip
```

Motion:

```text
slide_in
paper_bounce
tiny_rotation_settle
```

### 11.3 Text Layers

Text should be rendered by Remotion/SVG/HTML whenever possible.

Motion:

```text
word_pop
line_reveal
type_on
stamp_in
```

### 11.4 Portrait / Avatar Cutout

```text
client_photo_cutout
paper_avatar
real_life_subject_cutout
```

Motion:

```text
slow_drift
subtle_scale
small_head_bob
expression_swap
finger_point_micro_motion
```

### 11.5 Paper Notes / Fact Cards

Motion:

```text
drop_in
slide_in
pin_pop
micro_shake_on_debunk
```

### 11.6 Props

```text
herbs
tea_cup
books
stars
plants
mountains
arrows
dots
squiggles
```

Motion:

```text
parallax
selective_float
tiny_rotation_jitter
```

### 11.7 Hand-Drawn Annotations

```text
underline
circle
x_mark
arrow
checkmark
scribble
```

Motion:

```text
draw_on
stroke_reveal
marker_scribble_sfx
```

### 11.8 Mascot

The mascot is a secondary attention guide.

Allowed actions:

```text
point
wave
react
hold_sign
look_at_text
```

Forbidden actions:

```text
excessive bouncing
stealing focus from client
childish overreaction
```

---

## 12. Motion Recipes

Motion recipes are reusable executable animation patterns.

### 12.1 Myth Busted Recipe

For:

- myth debunk,
- scam exposure,
- belief correction.

```json
{
  "motion_recipe_id": "myth_busted_reel_v1",
  "duration_seconds": 28,
  "beats": [
    {
      "beat": "hook",
      "duration_seconds": 3,
      "actions": [
        "headline_strip_slide_in",
        "hero_portrait_soft_drift",
        "background_slow_push"
      ]
    },
    {
      "beat": "myth_statement",
      "duration_seconds": 5,
      "actions": [
        "paper_note_drop",
        "underline_draw",
        "arrow_draw_to_object"
      ]
    },
    {
      "beat": "debunk",
      "duration_seconds": 4,
      "actions": [
        "stamp_label_pop",
        "myth_note_micro_shake",
        "hand_drawn_x"
      ]
    },
    {
      "beat": "truth",
      "duration_seconds": 10,
      "actions": [
        "line_by_line_text_reveal",
        "foreground_parallax",
        "subtle_leaf_float"
      ]
    },
    {
      "beat": "cta",
      "duration_seconds": 6,
      "actions": [
        "cta_strip_slide_up",
        "mascot_wave",
        "camera_settle"
      ]
    }
  ]
}
```

### 12.2 Initial Recipe Library

Start with eight recipes:

```text
1. myth_busted_reel_v1
2. three_tips_reel_v1
3. stop_the_scroll_warning_v1
4. conceptual_contrast_v1
5. quote_to_question_v1
6. scene_to_principle_v1
7. poll_dilemma_v1
8. avatar_reaction_v1
```

---

## 13. Sound Effect Library

### 13.1 Default SFX Categories

```text
paper_pop
paper_slide
paper_rustle
paper_tap
tape_stick
scissors_snip
marker_scribble
marker_underline
felt_plop
soft_whoosh
tiny_ding
wooden_click
stamp_hit
camera_snap
blink_pop
arrow_boop
leaf_rustle
```

### 13.2 SFX Event Mapping

```text
paper strip slides in → paper_slide
headline lands → paper_tap
underline draws → marker_scribble
stamp appears → stamp_hit
star pops → tiny_ding
mascot waves → soft_boop
paper card drops → paper_pop
```

### 13.3 Sound Doctrine

```json
{
  "max_sfx_per_10s": 4,
  "voice_priority": true,
  "sfx_ducking_under_voice_db": -18,
  "avoid_cartoon_excess": true,
  "wellness_content_intensity": "low_to_medium"
}
```

---

## 14. Ideogram 4 Composition Stage

### 14.1 Role

Ideogram 4 should be treated as the **Composition Director**.

It is not the final identity renderer.

It defines:

- poster layout,
- visual hierarchy,
- subject placement,
- text area,
- paper-strip arrangement,
- prop density,
- visual metaphor,
- color balance,
- micro-semiotic anchor placement.

### 14.2 SceneSpec Input Example

```json
{
  "asset_type": "paper_cut_explainer",
  "format": "vertical_9_16",
  "headline": "MYTHS BUSTED",
  "subtitle": "Holistic health edition",
  "main_points": [
    "Natural = always safe?",
    "Detox tea fixes everything?",
    "Herbs work instantly?"
  ],
  "avatar": {
    "position": "lower_right",
    "gesture": "pointing_up",
    "emotion": "confident_warm"
  },
  "objects": [
    "pink headline strip",
    "green title strip",
    "paper note cards",
    "yellow starburst",
    "black mascot",
    "plants",
    "arrows"
  ],
  "micro_semiotic_anchors": [
    {
      "anchor_id": "msa_pharmacy_receipt_001",
      "placement": "small foreground prop",
      "prominence": "subtle_but_visible"
    }
  ],
  "visual_style": "editorial_2_5d_papercut_reel"
}
```

### 14.3 Fast Route

```text
Ideogram composition
→ use as flattened background plate
→ overlay approved avatar/text/props
→ animate lightly in Remotion
```

Use for early MVP or low-budget assets.

### 14.4 Proper Route

```text
Ideogram composition
→ extract layout plan
→ rebuild scene using approved brand layers
→ render final text in Remotion
→ animate avatar/props as separate layers
```

Use for reusable premium production.

### 14.5 Production Rule

Do not rely on AI-generated text baked into the final image when the asset needs editing, localization, or platform-specific caption variations.

Use Ideogram to design text layout.

Use Remotion/SVG/HTML to render final production text.

---

## 15. GPT Image 2 Asset Factory

### 15.1 Role

GPT Image 2 should be used as the onboarding asset factory.

It creates:

- realistic acting references,
- paper-cut avatar sheets,
- expression sheets,
- mouth-shape sheets,
- prop sheets,
- object packs,
- style explorations,
- repair edits,
- alternate expressions.

### 15.2 Recommended Uses

```text
Client photo references
→ realistic 64-state acting library

Approved identity summary
→ paper-cut avatar expression sheet

Visual constitution
→ prop/object pack

Rejected asset + fix instruction
→ corrected asset candidate
```

### 15.3 Transparent Background Rule

If GPT Image 2 does not return transparent assets in the required format, CMF should:

```text
image generation
→ segmentation / masking
→ transparent PNG/WebP
→ layer QC
→ approval
```

---

## 16. Flux / ComfyUI Editing Stage

### 16.1 Role

Flux / Flux Kontext / ComfyUI workflows are used for:

- identity replacement,
- face/likeness refinement,
- local image repair,
- paper texture harmonization,
- character integration into Ideogram compositions,
- cleanup before layer extraction.

### 16.2 Identity Rule

Identity conditioning models are fixed at container build time.

Approved reference images are fixed in object storage.

Runtime agents may select approved references, but may not alter identity conditioning.

### 16.3 Batch Worker Rule

Do not run GPU workers persistently.

Use batch execution:

```text
queue fills
→ worker starts
→ pulls brand context + assets
→ runs batch
→ uploads outputs
→ writes receipts
→ shuts down
```

---

## 17. Layer Extraction and Rigging

### 17.1 Layer Extraction Goal

Convert generated or approved compositions into editable layers:

```text
background_paper.png
headline_strip.png
note_card_01.png
avatar_body.png
avatar_head.png
avatar_mouth.png
arrow_01.png
plant_01.png
shadow_layer.png
text_layer.svg
```

### 17.2 Layer Manifest

```json
{
  "layer_id": "paper_arrow_01",
  "semantic_type": "arrow",
  "file_uri": "s3://.../paper_arrow_01.png",
  "alpha_quality_score": 0.94,
  "edge_quality_score": 0.9,
  "bbox": [144, 420, 300, 120],
  "anchor_point": [0.5, 0.5],
  "z_index": 14,
  "casts_shadow": true,
  "motion_affordances": ["bounce", "wiggle", "slide", "pulse"]
}
```

### 17.3 Tools

Use a hybrid approach:

- segmentation models for generic object cutouts,
- See-Through-like decomposition for character/object layer separation,
- Stretchy Studio or custom rigging for 2D paper avatars,
- manual review for hero assets,
- Flux/GPT Image fixes for bad edges or fused areas.

---

## 18. Renderer Routing

### 18.1 Default Renderer

Remotion is the default production compiler for:

- vertical videos,
- paper-cut explainers,
- subtitles,
- social packaging,
- carousels as motion videos,
- quick proof assets,
- Publer-ready outputs.

### 18.2 Motion Canvas

Use Motion Canvas for:

- procedural explainers,
- vector diagrams,
- voice-over synchronized teaching animations,
- framework animations.

### 18.3 Manim

Use Manim for:

- data stories,
- bar-chart races,
- timelines,
- abstract visual explanations,
- mathematical/procedural animations.

### 18.4 SCAIL-2 / Motion Transfer

Use only for:

- memes,
- dancing motions,
- reaction clips,
- recurring motion formats.

Do not use as the default cinematic engine.

### 18.5 Video Generation Models

Use video generation models for:

- cinematic metaphor scenes,
- complex camera movement,
- atmospheric brand films,
- non-editable cinematic assets.

Avoid for assets that require precise text, client approval, or reusable layer control.

---

## 19. Publishing Flow

### 19.1 PublishingIntent Object

```json
{
  "publishing_intent_id": "pi_001",
  "brand_id": "brand_001",
  "render_output_id": "render_001",
  "approval_state": "approved",
  "platforms": {
    "linkedin": {
      "caption": "Long professional version...",
      "scheduled_at": "2026-06-20T09:00:00+02:00"
    },
    "instagram": {
      "caption": "Shorter Reels version...",
      "scheduled_at": "2026-06-20T12:00:00+02:00"
    },
    "tiktok": {
      "caption": "Hook-first caption...",
      "scheduled_at": "2026-06-20T18:00:00+02:00"
    }
  },
  "publer_status": "not_submitted"
}
```

### 19.2 Publishing Sequence

```text
render approved
→ PublishingIntent created
→ operator confirms
→ media uploaded to Publer
→ post scheduled as draft or scheduled post
→ Publer job ID stored
→ status polled
→ performance data imported later
```

### 19.3 Safety Rule

No one-tap public publishing.

Telegram can request scheduling, but public publishing must require confirmation.

---

## 20. App Screens

### 20.1 Brand Dashboard

Shows:

- active asset packages,
- editing sessions,
- render status,
- approval queue,
- publishing calendar,
- active Brand Context Version,
- Publer connection status.

### 20.2 Brand Genesis Wizard

Screens:

1. client intake,
2. consent,
3. photo upload,
4. photo QC,
5. identity summary approval,
6. 64 acting asset generation,
7. approval / fix / reject grid,
8. paper-cut avatar generation,
9. rig preview,
10. prop library generation,
11. micro-semiotic anchor library,
12. motion/SFX library,
13. lock Brand Context v1.

### 20.3 Asset Review Grid

Approve, reject, or request fixes for:

- acting references,
- expressions,
- avatar layers,
- prop assets,
- micro-semiotic anchors,
- motion recipes,
- SFX mappings.

### 20.4 Expression Sessions

Shows:

- recording files,
- transcript,
- expression moments,
- anchor hits,
- archetype routes,
- asset package candidates.

### 20.5 Editing Board

Kanban:

```text
Planned
Queued
Rendering
Needs Review
Approved
Scheduled
Published
Failed
```

### 20.6 Render Review Page

Shows:

- video preview,
- source quote,
- transcript segment,
- archetype route,
- brand context snapshot,
- selected assets,
- evaluation receipt,
- regenerate controls,
- approval controls,
- publishing controls.

---

## 21. Object Storage Structure

```text
brands/
  brand_001/
    genesis_sessions/
      bgs_001/
    source/
      photos/
      videos/
    identity/
      face_anchors/
      full_body_refs/
    acting_library/
      v1/
        realistic/
        metadata.json
    papercut_avatar/
      v1/
        heads/
        eyes/
        mouths/
        torso/
        arms/
        hands/
        rig_manifest.json
    props/
      v1/
        arrows/
        stars/
        plants/
        mountains/
        text_strips/
        mascot/
    micro_semiotic_anchors/
      v1/
        objects/
        metadata.json
    motions/
      v1/
        motion_primitives.json
    sfx/
      v1/
        paper_pop/
        scribble/
        whoosh/
        metadata.json
    compositions/
      ideogram_refs/
      approved_layouts/
    expression_sessions/
      xes_001/
    editing_sessions/
      ces_001/
    renders/
      approved/
      rejected/
      published/
```

---

## 22. Asset Lifecycle

```text
draft
generated
auto_qc_passed
auto_qc_failed
awaiting_human_review
approved
needs_fix
rejected
deprecated
locked
```

Production can only use:

```text
approved + locked
```

---

## 23. Evaluation System

### 23.1 Onboarding Asset Evaluation

For 64 acting references:

- likeness,
- emotion clarity,
- gesture clarity,
- body-language clarity,
- hand quality,
- age consistency,
- outfit consistency,
- crop usability.

For paper-cut avatar:

- recognizable likeness,
- clean cutout edges,
- layer separation,
- mouth-shape usability,
- expression clarity,
- rig preview pass,
- paper texture consistency.

For Micro-Semiotic Anchors:

- recognition,
- subtlety,
- comment potential,
- brand fit,
- visual legibility,
- distraction risk,
- legal/trademark risk.

### 23.2 Render Evaluation

Each rendered asset should score:

- identity consistency,
- composition quality,
- style consistency,
- emotional accuracy,
- platform fit,
- negative space compliance,
- hook strength,
- shareability,
- routeability,
- motion restraint,
- micro-semiotic anchor effectiveness.

### 23.3 Hard Fail Conditions

Hard fail if:

- wrong identity,
- distorted face,
- unreadable text,
- broken hero-frame hands,
- style drift into generic AI art,
- anchor stereotypes the audience,
- motion becomes childish or distracting,
- source expression is misrepresented,
- caption violates brand Negative Space,
- publication target is wrong.

---

## 24. Future Interview Session Flow

Once Brand Context v1 is locked:

```text
Complete Expression Session
→ transcript
→ expression moments
→ archetype routing
→ asset package spec
→ Complete Editing Sessions
→ SceneSpec / Template JSON
→ asset retrieval from Brand Context
→ optional Ideogram composition
→ optional Flux/GPT Image edit
→ Remotion/Motion Canvas render
→ evaluation receipt
→ approval
→ Publer publishing intent
→ brand memory update
```

Example expression moment:

```text
“People think burnout means they are weak. But sometimes it means their nervous system has been loyal for too long.”
```

Routing:

```text
Core Archetype: Myth Debunk
Asset Derivative: Scene-to-Principle
CMF Route: Paper-Cut Explainer
Emotion: compassionate authority
Gesture: open-hands explaining
```

Asset selection:

```text
Avatar expression: serious_warm
Avatar motion: open_explain_loop
Props: myth-busted headline, notes, arrows
Micro-Semiotic Anchor: messy calendar / coffee cup / health receipt
SFX: paper_pop, marker_underline, soft_boop
Renderer: Remotion
```

---

## 25. Brand Memory Update

Every interview and render should update:

- guest/client profile,
- expression moment library,
- anchor library,
- depth anchor library,
- archetype survival memory,
- CMF route performance,
- reaction seed library,
- approved composition library,
- rejected visual patterns,
- micro-semiotic anchor performance,
- motion recipe performance,
- SFX preference memory,
- publishing performance.

This is what turns CMF from a batch editor into a learning creative system.

---

## 26. Implementation Roadmap

### Phase 1 — Control Tower MVP

Build:

- Brand Workspace,
- Brand Genesis Session,
- photo upload,
- consent,
- object storage,
- approval grid,
- asset lifecycle,
- Brand Context lock.

### Phase 2 — 64 Acting Library

Build:

- 8 × 8 acting taxonomy,
- GPT Image generation requests,
- batch generation,
- auto-QC,
- review/fix/reject loop,
- asset metadata.

### Phase 3 — Paper-Cut Avatar Rig

Build:

- expression sheets,
- mouth shapes,
- body layers,
- rig manifest,
- basic Remotion rig preview.

### Phase 4 — Paper-Cut Render Mode

Build:

- visual constitution,
- prop library,
- motion recipes,
- SFX mapping,
- Remotion template,
- one full myth-busting reel.

### Phase 5 — Expression Session Integration

Build:

- Complete Expression Session ingestion,
- transcript import,
- expression moment extraction,
- archetype routing,
- asset package spec,
- Complete Editing Session creation.

### Phase 6 — Operator Cockpit

Build:

- Telegram bot notifications,
- approve / reject / regenerate buttons,
- PWA deep links,
- batch status alerts.

### Phase 7 — Publer Publishing Adapter

Build:

- PublishingIntent,
- Publer media upload,
- schedule/draft creation,
- job status polling,
- post status sync.

### Phase 8 — GPU Batch / Premium Generative Layer

Build:

- ComfyUI/Flux batch workers,
- identity-conditioned editing,
- layer cleanup,
- premium composition reconstruction.

---

## 27. MVP Definition

The first working version should prove:

```text
Client uploads photos
→ system generates 64 acting references
→ operator approves/fixes/rejects
→ system creates paper-cut avatar rig
→ system creates object + anchor + SFX libraries
→ Brand Context v1 is locked
→ one interview moment becomes one paper-cut reel
→ output is reviewed and approved
→ PublishingIntent is created
```

Do not start by building the entire CCP organism.

Start by proving that one brand can be onboarded into a reusable creative universe and that one expression moment can be turned into a coherent, animated, brand-consistent asset.

---

## 28. Final Doctrine

CMF V3 is not a video generator.

It is a **brand-consistent creative operating system**.

Its foundation is:

```text
Brand Genesis Session
→ Brand Context Version
→ Reusable Creative Libraries
→ Expression Sessions
→ Complete Editing Sessions
→ Rendered Assets
→ Publishing
→ Memory Update
```

The most important new doctrine is:

> Onboarding is not setup. Onboarding is the manufacturing of the client’s reusable creative universe.

The second most important doctrine is:

> Micro-Semiotic Anchoring makes the audience feel recognized before the message is explained.

The third:

> Editorial 2.5D Paper-Cut Reel Animation should feel like paper gently coming alive, not like cartoon stickers bouncing everywhere.

The fourth:

> The backend should not invent the brand every time. It should retrieve, compose, animate, evaluate, and remember from the approved Brand Context.

This is how CCP becomes scalable without becoming generic.

---

# Appendix A — Minimal Database Tables

```text
organizations
users
brand_workspaces
brand_genesis_sessions
brand_context_versions
consent_records
source_media
identity_summaries
identity_packs
acting_references
papercut_avatar_rigs
avatar_layers
facial_expression_assets
mouth_shape_assets
paper_object_assets
micro_semiotic_anchors
motion_primitives
sfx_assets
composition_preferences
complete_expression_sessions
expression_moments
archetype_routes
asset_package_specs
complete_editing_sessions
scene_specs
composition_plans
layer_manifests
animation_plans
render_jobs
render_outputs
evaluation_receipts
approval_events
publishing_profiles
publishing_intents
publer_jobs
operator_notifications
brand_memory_events
```

---

# Appendix B — Core JSON Contract Chain

```text
BrandGenesisSession
→ BrandContextVersion
→ CompleteExpressionSession
→ ExpressionMoment
→ ArchetypeRoute
→ AssetPackageSpec
→ CompleteEditingSession
→ SceneSpec
→ CompositionPlan
→ LayerManifest
→ AnimationPlan
→ RenderJob
→ EvaluationReceipt
→ ApprovalEvent
→ PublishingIntent
→ BrandMemoryEvent
```

---

# Appendix C — Golden Test Case

## Input

A holistic health client uploads 8 photos and defines the audience as French women interested in grounded naturopathy.

## Genesis Outputs

- 64 acting references approved,
- paper-cut avatar rig approved,
- herb/tea/pharmacy object pack approved,
- Micro-Semiotic Anchors approved:
  - pharmacy green cross,
  - herbal tea box,
  - dosage spoon,
  - supplement receipt,
  - supermarket tea label,
- motion recipe approved:
  - myth_busted_reel_v1,
- SFX pack approved:
  - paper_pop,
  - marker_scribble,
  - stamp_hit,
  - tiny_ding.

## Expression Moment

```text
“Natural does not always mean safe. Herbs can help, but context, dosage, and guidance matter.”
```

## Route

```text
Core Archetype: Myth Debunk
Asset Derivative: Scene-to-Principle
CMF Route: Paper-Cut Explainer
Visual Style: Editorial 2.5D Paper-Cut Reel
Motion Recipe: myth_busted_reel_v1
```

## Expected Output

A vertical paper-cut reel with:

- “MYTHS BUSTED” headline,
- three myth cards,
- client avatar lower-right pointing upward,
- subtle pharmacy/tea micro-semiotic anchor,
- restrained typography reveal,
- paper pop + marker underline SFX,
- final CTA strip.

## Pass Criteria

- client likeness recognizable,
- text readable,
- motion restrained,
- paper tactility strong,
- micro-semiotic anchor visible but not central,
- message not distorted,
- asset ready for approval/publishing.

