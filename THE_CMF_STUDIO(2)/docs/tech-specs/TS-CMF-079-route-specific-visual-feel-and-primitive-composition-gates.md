# TS-CMF-079: Route-Specific Visual Feel and Primitive Composition Gates

## 1. Purpose

This spec repairs a critical failure mode discovered during visual composition previsualization: all CMF video formats can collapse into the same generic "premium social" look if the system treats composition as an aesthetic wrapper instead of a doctrine-bound production route.

CMF STUDIO must not approve composition previews, composition JSON templates, renderer templates, or generated keyframes unless they preserve the distinct feeling, materiality, primitive obligations, and source intent of their assigned route.

The four short-video slots are not skins over one template. They are different delivery systems:

- `SV-CSC` makes the viewer feel the story.
- `SV-EDU` makes the viewer understand the idea.
- `SV-FRB` makes the viewer question the frame.
- `SV-RRC` makes the viewer trust, recognize, or participate.

## 2. Source Doctrine

This spec is grounded in:

- `CCP V9.1 - Expression Capture & Archetype Routing Update.md`: canonical Guest Asset Pack slots and route purposes.
- `Matrix of Edging.md`: Matrix selects pressure; experience primitives deliver pressure.
- `product-brief-CMF_STUDIO-2026-06-19.md`: Ideogram 4 composition role, ImageCritic visual gates, 64-state acting library, scene reproducibility.
- `CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md`: Brand Context, Paper-Cut Avatar Rig, Micro-Semiotic Anchors, Editorial 2.5D Paper-Cut style.
- `CCP_Creative_Pipeline_Architecture_V2.md`: composition before rendering, paper-cut / stop-motion style constitution, layer manifests, renderer routing, quality gates.
- `reference/cmf-drafts/prd-modules/PRD_12_CMF_Primitive_Eval_Review_Workbench.md`: primitive-aware evaluation and approval blockers.
- `registries/evals/composition/cmf_composition_primitive_triads.v1.json`: machine-loadable primitive triad registry and route-specific composition blockers.

## 3. Core Claim

Every composition preview must declare and pass a route-specific `VisualFeelContract` before it can become a `CompositionPlan`.

No composition object may advance with fewer than three validated primitive obligations.

The canonical machine-readable rule is `registries/evals/composition/cmf_composition_primitive_triads.v1.json`. This spec explains the product and implementation meaning of that registry; the registry is the enforcement source for route triads, primitive roles, thresholds, and blocker codes.

The `VisualFeelContract` is evaluated before:

- image generation,
- Ideogram 4 composition jobs,
- paper-cut scene assembly,
- reaction template binding,
- Remotion or Motion Canvas implementation,
- approval workbench display.

## 4. Required Contract

```json
{
  "visual_feel_contract_id": "vfc_...",
  "asset_slot": "SV-EDU",
  "cmf_route": "Paper-Cut Explainer",
  "visual_style_id": "visual.editorial_2_5d_papercut_reel.v1",
  "source_expression_moment_id": "em_...",
  "primitive_obligations": [
    {
      "primitive_id": "PRM-HUM-025",
      "primitive_name": "Analogy Bridge",
      "primitive_role": "meaning_transform",
      "evidence_ref": "matrix_of_edging:primitive_pass",
      "must_validate": ["metaphor_clarity", "source_fit"],
      "minimum_score": 0.85
    },
    {
      "primitive_id": "PRM-PRS-007",
      "primitive_name": "Teaching as Compassion",
      "primitive_role": "delivery_shape",
      "evidence_ref": "context_premise:audience_need",
      "must_validate": ["teaching_generosity", "cognitive_load"],
      "minimum_score": 0.85
    },
    {
      "primitive_id": "PRM-VSG-020",
      "primitive_name": "Perspective and Layering as Meaning",
      "primitive_role": "format_material",
      "evidence_ref": "brand_context:visual_constitution",
      "must_validate": ["paper_layer_depth", "torn_edges", "physical_shadows"],
      "minimum_score": 0.9
    }
  ],
  "minimum_validated_primitives": 3,
  "matrix_pressure": {
    "tension_selected": "Natural does not always mean safe",
    "edge_product": "support, not magic"
  },
  "feel_targets": [],
  "material_rules": [],
  "forbidden_style_drift": [],
  "composition_must_show": [],
  "motion_must_serve": [],
  "eval_bindings": [],
  "hard_fail_conditions": []
}
```

## 4.1 Minimum Three-Primitive Law

Every composition, prompt, JSON template, generated keyframe, renderer template, and approval preview must bind to at least three primitive validations.

The three required primitive roles are:

| Primitive role | Purpose | Required evidence |
|---|---|---|
| `meaning_transform` | Proves the composition is carrying the right tension, edge, analogy, contrast, story, or recognition pressure. | Matrix of Edging, Context Premise, source transcript, or Expression Moment evidence. |
| `delivery_shape` | Proves the composition delivers the selected pressure through the correct audience experience. | Experience primitive, persuasion primitive, voice/audio primitive, or interaction primitive. |
| `format_material` | Proves the composition uses the correct route-specific material and visual grammar. | Brand Context, visual constitution, render mode, composition JSON, or ImageCritic evidence. |

The gate fails if:

- fewer than three primitives are declared;
- a primitive is named without an exact primitive ID or approved family ref;
- a primitive has no evidence ref;
- a primitive has no validation dimensions;
- a primitive score is below its threshold;
- the three primitives all belong to the same role and fail to cover meaning, delivery, and material/format;
- one primitive is repeated under different names to inflate the count;
- the selected primitive conflicts with the route purpose.

### 4.1.1 Approved Primitive Reference Types

Primitive references may point to:

- exact registered primitive IDs, such as `PRM-PSY-001`, `PRM-PRS-007`, `PRM-VSG-020`, or `EXP-TRS-003`;
- registered Matrix primitive refs, such as `MATRIX.IRONY_INVERSION`, `MATRIX.ANALOGY_BRIDGE`, or `MATRIX.STAKES_AS_PERSONAL_WHY`, as pressure-selection support only;
- route triad entries in `registries/evals/composition/cmf_composition_primitive_triads.v1.json`.

Matrix refs help explain why a route was selected, but they do not satisfy the minimum three count by themselves. The minimum must be met by exact registered primitive IDs.

Fuzzy labels such as "make it premium", "feel cinematic", or "good social proof" do not count as primitive validations.

## 5. Four Route Feel Bibles

### 5.1 `SV-CSC`: Cinematic Story Commentary

**Purpose:** story, emotional identification, narrative authority.

**Allowed feeling:** documentary, intimate, atmospheric, witness-like, emotionally specific.

**Visual grammar:**

- authentic guest or filmed subject carries the emotional truth;
- darker cinematic background is allowed only when it supports memory, tension, or testimony;
- memory objects, location fragments, archival-like cards, or atmospheric B-roll should act as source-adjacent meaning carriers;
- typography should feel like a narrated truth, not a poll prompt;
- motion should be slow, restrained, emotionally paced.

**Primitive obligations:**

Minimum recommended triad:

| Role | Primitive ref | Why it fits |
|---|---|---|
| meaning_transform | `PRM-ACT-005` Backstory Architecture or `PRM-PRS-009` McKee Inciting Incident Engine | Keeps the clip anchored in personal stakes, disruption, backstory, and lived motivation. |
| delivery_shape | `PRM-PRS-002` Tension-and-Release Narrative Engine | Controls the emotional release arc instead of flattening the story into a quote. |
| format_material | `PRM-VSG-021` Punctum, Air, and Felt Truth or `PRM-VSG-016` Light and Color as Emotional Architecture | Makes the frame feel documentary, specific, and emotionally inhabited rather than generically dramatic. |

Optional supporting primitives:

- `PRM-PRS-015` What Is / What Could Be Contrast Engine where the story contains transformation;
- `PRM-PRS-023` Emotionally Competent Stimulus Design for first-frame emotional hook;
- `PRM-VOC-009` Sensory Scene Anchoring or `PRM-VOC-007` The Theatre of the Mind for atmospheric scene memory;
- `PRM-VOC-006` Start Strong, End Strong for opening and closing structure.

**Hard fails:**

- feels like a reaction/poll format;
- story moment is replaced by generic motivational drama;
- subject face or voice is not the emotional center;
- no visible tie to memory, witness, or transformation;
- typography screams when the moment requires silence.

### 5.2 `SV-EDU`: Educational / Paper-Cut / Animated Avatar Explainer

**Purpose:** teaching, clarity, framework extraction.

**Allowed feeling:** credible, warm, handmade, premium, educational.

**Official style for Paper-Cut route:**

```text
visual.editorial_2_5d_papercut_reel.v1
```

**Motion principle:**

```text
Paper gently coming alive.
```

**Visual grammar:**

- textured cream paper background;
- torn paper strips for headlines and fact cards;
- colored paper or felt shapes;
- visible paper grain and soft offset shadows;
- handmade typography, marker underlines, paper pins, small bursts;
- paper props and metaphor objects selected from the Brand Context;
- client photo cutout or paper avatar with clean cut edge;
- micro-semiotic anchors visible but not central;
- one clear teaching premise per scene.

**Composition examples:**

- myth strip + large paper note question + avatar lower-right;
- truth strip + 2-4 paper fact notes + object pack;
- metaphor sequence using paper objects and arrows;
- Scene-to-Principle with physical object -> principle card -> final CTA strip.

**Primitive obligations:**

Minimum recommended triad:

| Role | Primitive ref | Why it fits |
|---|---|---|
| meaning_transform | `PRM-HUM-025` Analogy Bridge or `PRM-PRS-015` What Is / What Could Be Contrast Engine | Converts abstract teaching into a physical metaphor, myth/truth split, or visible conceptual contrast. |
| delivery_shape | `PRM-PRS-007` Teaching as Compassion or `PRM-PRS-032` Explanation Engine | Ensures the frame clarifies for the audience instead of showing off expertise. |
| format_material | `PRM-VSG-020` Perspective and Layering as Meaning, `PRM-VSG-008` Character Coherence Beats Beauty, or `PRM-VSG-003` Intent Governs Style | Requires tactile paper layering, coherent cutout/avatar acting, and route-specific handmade materiality. |

Optional supporting primitives:

- `PRM-PRS-027` Multisensory Delivery Architecture for "see it, hear it, feel it";
- `PRM-PRS-025` Rule of Three Message Architecture for myth/truth/fix structures;
- `PRM-VSG-001` Composition as Eye-Path Engineering for headline -> object -> avatar scan path;
- `PRM-PRS-001` Strong Title as Idea Architecture for paper-strip headline discipline.

**Hard fails:**

- dark cinematic template used as default;
- glossy 3D, sterile SaaS vector, neon cyberpunk, or generic AI influencer realism;
- flat Canva-style clip art without tactile texture;
- paper objects do not look physically placed;
- too many decorative objects crowd the teaching premise;
- motion becomes childish, chaotic, or sticker-like;
- avatar is treated as a generic presenter rather than a rigged paper actor.

### 5.3 `SV-FRB`: Challenger / Frame Breaker

**Purpose:** authority, edge, belief correction.

**Allowed feeling:** charged, corrective, evidentiary, contrastive, sharp but controlled.

**Visual grammar:**

- a false belief must be visible as an object to break, cross out, expose, or compare;
- receipts, source panels, contradiction maps, or proof cards must carry authority;
- red/green, warning, or high-contrast systems are allowed if they serve belief correction;
- the guest can appear as commentator, witness, or authority figure;
- composition should be built around the frame shift, not around generic outrage.

**Primitive obligations:**

Minimum recommended triad:

| Role | Primitive ref | Why it fits |
|---|---|---|
| meaning_transform | `PRM-HUM-021` Irony Inversion or `PRM-PRS-015` What Is / What Could Be Contrast Engine | Exposes the contradiction between what the audience believes and what the guest/source reveals. |
| delivery_shape | `PRM-REF-009` Constructive Tension Control or `PRM-PSY-008` Attack Problem Not Person | Keeps the correction sharp, ethical, and structured instead of turning into identity attack. |
| format_material | `PRM-VSG-012` Frame as Active Meaning Device or `PRM-VSG-001` Composition as Eye-Path Engineering | Makes receipts, proof cards, split frames, or VS surfaces carry the argument instead of decorating it. |

Optional supporting primitives:

- `PRM-PRS-015` What Is / What Could Be Contrast Engine;
- `PRM-PRS-001` Strong Title as Idea Architecture;
- `PRM-PRS-002` Tension-and-Release Narrative Engine when the piece needs a stronger reveal arc.

**Hard fails:**

- outrage without evidence;
- same layout as a reaction poll;
- no visible false belief or no visible reframe;
- claim stronger than source transcript supports;
- proof cards are decorative instead of evidentiary.

### 5.4 `SV-RRC`: Reaction / Recognition Clip

**Purpose:** audience participation, social proof, comment generation.

**Allowed feeling:** human, participatory, recognizable, socially live, responsive.

**Visual grammar:**

- upper zone carries reaction interface: poll, prompt, tweet-like card, tier list, blind ranking, mirror quiz, bracket, comments, or quote card;
- lower zone carries real human proof: guest/interviewer upper-body cutouts or guest-only reaction;
- interaction must match the interview question and the guest's response;
- the frame should feel like a live social object, not a static poster;
- facial reaction, pause, recognition, disagreement, or tension must be visible.

**Primitive obligations:**

Minimum recommended triad:

| Role | Primitive ref | Why it fits |
|---|---|---|
| meaning_transform | `PRM-PSY-001` Matching Principle | Confirms the reaction mechanism matches the practical, emotional, or social identity layer. |
| delivery_shape | `PRM-REF-009` Constructive Tension Control | Lets the clip invite disagreement, recognition, or voting without becoming chaotic. |
| format_material | `PRM-VSG-015` Composition as Attention Routing or `PRM-VSG-024` Space as Psychological Relationship | Routes the eye between upper reaction UI and lower human proof while preserving the interview relationship. |

Optional supporting primitives:

- `PRM-BUS-014` Affordance as Invitation for poll, ranking, quiz, or comment response mechanics;
- `EXP-TRS-003` Reflective Social Proof for recognition/status share dynamics;
- `PRM-VOC-008` Voice as Identity Signature when subtitles and audio must preserve guest personality.

**Hard fails:**

- no human proof in the lower zone;
- reaction UI does not correspond to what the guest is saying;
- poll/ranking mechanic is arbitrary;
- format feels like Challenger when it should feel participatory;
- recognition is forced or generic.

## 6. Composition Preflight Gate

Before generating or approving a composition preview, the system must produce a `CompositionPreflightReceipt`.

```json
{
  "composition_preflight_receipt_id": "cpr_...",
  "composition_plan_id": "cp_...",
  "asset_slot": "SV-EDU",
  "route": "Paper-Cut Explainer",
  "visual_feel_contract_id": "vfc_...",
  "source_expression_moment_id": "em_...",
  "minimum_validated_primitives": 3,
  "primitive_validation_count": 3,
  "primitive_results": [
    {
      "primitive_id": "PRM-HUM-025",
      "role": "meaning_transform",
      "score": 0.91,
      "threshold": 0.85,
      "evidence_refs": ["matrix_of_edging:primitive_pass"],
      "decision": "pass"
    }
  ],
  "primitive_obligations_passed": true,
  "route_feel_passed": true,
  "style_drift_warnings": [],
  "hard_failures": [],
  "decision": "allow_preview_generation"
}
```

The gate blocks if:

- no source Expression Moment is bound;
- fewer than three primitive obligations are declared;
- fewer than three primitive obligations pass validation;
- primitive obligations do not cover meaning, delivery, and material/format roles;
- the route feel bible is missing;
- the prompt borrows another slot's visual grammar without explicit justification;
- the composition cannot explain how it delivers the Matrix-selected pressure;
- Paper-Cut route lacks paper materiality requirements;
- Reaction route lacks interaction and human proof requirements.

The gate emits:

```text
COMPOSITION_PRIMITIVE_MINIMUM_NOT_MET
```

when fewer than three primitives validate.

It emits:

```text
COMPOSITION_PRIMITIVE_ROLE_COVERAGE_MISSING
```

when three primitives exist but fail to cover the required role spread.

## 7. Prompt Compiler Requirements

The prompt compiler shall not use a generic prompt such as "premium vertical social video" across routes.

Every prompt must include:

- `asset_slot`;
- `cmf_route`;
- `visual_style_id`;
- `source_expression_summary`;
- `primitive_obligations`;
- `minimum_validated_primitives: 3`;
- `primitive_validation_dimensions`;
- `primitive_evidence_refs`;
- `matrix_pressure`;
- `composition_must_show`;
- `material_rules`;
- `negative_style_drift`;
- `text_space_requirements`;
- `layer_separation_requirements`;
- `expected_operator_review_questions`.

For Paper-Cut prompts, required language includes:

```text
textured cream paper, torn paper strips, handmade paper shadows,
visible paper grain, paper props, tactile collage, restrained motion,
paper gently coming alive
```

For Paper-Cut prompts, forbidden language includes:

```text
dark cinematic social template, glossy 3D, cyberpunk, SaaS vector,
generic influencer realism, neon gradient, sticker clutter
```

## 8. ImageCritic / Visual Eval Requirements

Every generated keyframe or preview must be evaluated for:

- route feel fidelity;
- at least three primitive activations;
- primitive role coverage;
- primitive evidence strength;
- style consistency;
- negative space compliance;
- source truth alignment;
- text hierarchy;
- layerability;
- materiality;
- micro-semiotic anchor subtlety;
- platform fit.

Additional Paper-Cut checks:

- paper texture visible;
- torn edges visible;
- soft offset shadows present;
- paper objects look physically placed;
- motion plan preserves materiality;
- avatar or cutout has clean edge;
- micro-semiotic anchors do not stereotype or dominate.

Additional Reaction checks:

- upper UI and lower human proof are both present;
- interaction mechanic matches source expression;
- guest/interviewer cutouts preserve authenticity;
- ranking/poll/quiz state is not arbitrary.

## 9. Approval Workbench Requirements

The Operator Composition Workbench shall show:

- selected source Expression Moment;
- route and asset slot;
- primitive obligations;
- primitive count and role coverage;
- primitive pass/fail cards;
- route feel contract;
- composition preview;
- ImageCritic results;
- hard-fail blockers;
- generated repair instruction;
- approve / repair / reject controls.

The workbench must expose a specific blocker for:

```text
VISUAL_FEEL_COLLAPSE
```

Definition:

```text
The artifact borrows the general visual skin of another route or generic social media instead of delivering the intended route-specific feel.
```

The workbench must also expose:

```text
COMPOSITION_PRIMITIVE_MINIMUM_NOT_MET
COMPOSITION_PRIMITIVE_ROLE_COVERAGE_MISSING
COMPOSITION_PRIMITIVE_EVIDENCE_MISSING
```

These blockers disable approval until repaired.

## 10. Test Fixtures

Required golden fixtures:

- Paper-Cut Myth Debunk: natural health / tea / herbs / myth-busted example with tactile paper.
- Reaction Recognition: upper poll or prompt + lower guest/interviewer cutouts.
- Challenger Frame Breaker: false belief + evidence receipt + reframe.
- Cinematic Story: source-backed memory object + emotional guest moment.

Required negative fixtures:

- Any composition with only one or two primitives declared.
- Any composition with three primitives declared but all three are generic delivery primitives with no meaning-transform or material/format primitive.
- Any composition that names primitives without exact primitive IDs or approved family refs.
- Paper-Cut rendered as dark cinematic thumbnail.
- Reaction rendered as static poster with no human proof.
- Challenger rendered as outrage without receipt.
- Cinematic Story rendered as generic motivation quote.
- Any four-slot board where all formats share the same palette, typography, background, and emotional tempo.

## 11. Acceptance Criteria

This spec is complete when:

- `VisualFeelContract` and `CompositionPreflightReceipt` contracts exist.
- `VisualFeelContract` requires `minimum_validated_primitives: 3`.
- Composition JSON generation requires a route feel contract.
- Composition JSON generation blocks if fewer than three primitive validations pass.
- The three primitive validations cover meaning, delivery, and format/material roles.
- Primitive validations use exact primitive IDs or approved primitive family refs.
- Image generation prompts are route-specific.
- Preview approval blocks `VISUAL_FEEL_COLLAPSE`.
- Preview approval blocks `COMPOSITION_PRIMITIVE_MINIMUM_NOT_MET`.
- Paper-Cut route uses `visual.editorial_2_5d_papercut_reel.v1`.
- The Paper-Cut route can reproduce the holistic-health myth-busting golden fixture structure:
  - myth/truth torn strips;
  - tactile cream paper;
  - client avatar or cutout;
  - micro-semiotic anchors;
  - restrained paper motion;
  - final CTA strip.
- The Reaction route preserves the upper UI / lower human proof composition for relevant clips.
- The Challenger route preserves proof-backed belief correction.
- The Cinematic route preserves narrative authority and emotional pacing.

## 12. Repair Directive

All previously generated composition boards that reused one generic dark/premium social feel across multiple routes must be marked as non-canonical draft exploration.

They may inform structural zoning only. They must not be used as:

- approved visual style references;
- golden fixtures;
- renderer templates;
- JSON template defaults;
- ImageCritic benchmark examples.

New boards must be regenerated only after `CompositionPreflightReceipt` passes for each format family.
