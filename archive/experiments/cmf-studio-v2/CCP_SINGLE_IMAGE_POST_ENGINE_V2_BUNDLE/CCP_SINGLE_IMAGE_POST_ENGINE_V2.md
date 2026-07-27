# CCP Single Image Post Engine V2

## Document purpose

This document turns the V1 visual atlas into an **executable, registry-driven Single Image Post Engine** for CCP Studio and the Conscious Media Factory.

The engine does not accept loose prompts. It receives structured evidence and brand context, selects a canonical composition, compiles a deterministic scene specification, creates only the generative assets that are actually needed, renders the final post through Skia, evaluates it mechanically, and pauses for operator approval.

The governing chain is:

```text
Complete Expression Session
→ Expression Moment
→ Core Content Archetype
→ Asset Derivative
→ optional Meme / Reaction Mechanism
→ Single Image Composition Router
→ SingleImageSceneSpec
→ Provider Jobs
→ Skia Render
→ Evaluation Receipt
→ Operator Approval
→ Publishing Intent
```

The old model of “write a prompt and make an image” is prohibited.

---

## 1. What V2 adds

V2 operationalizes the 54-image Supervisuals corpus as:

- **28 canonical composition contracts**;
- exact archetype and derivative compatibility;
- normalized composition zones;
- a deterministic routing policy;
- a Skia component catalog;
- Ideogram 4 prompt contracts;
- family-specific evaluation profiles;
- Pydantic production contracts;
- reference examples and failure-repair logic.

The source doctrine distinguishes meaning structures from packaging structures and CMF render routes. That separation is preserved here: content archetypes define what the content means, asset derivatives define what kind of single-image artifact is required, and this registry defines how that artifact is physically composed.

---

## 2. Runtime ownership

### Python / Pydantic / DSPy / Pi
Owns:

- structured context ingestion;
- archetype and derivative selection;
- composition routing;
- provider job creation;
- doctrine and primitive enforcement;
- evaluation and repair planning;
- receipts and audit history.

### TypeScript / Skia renderer
Owns:

- final deterministic layout;
- exact typography;
- image placement and masks;
- cards, borders, shadows, panels, stat chips, poll frames;
- Rough Notation overlays;
- reproducible image export.

The TypeScript render contract is generated from the Python models. It does not own semantic logic.

---

## 3. Canonical engine input

The engine receives a `SingleImageEngineInput`, including:

- organization and brand IDs;
- immutable Brand Context Version;
- source Expression Session and Expression Moment;
- Interview Asset Contract when applicable;
- Core Content Archetype;
- Asset Derivative;
- Meme or Reaction mechanism when applicable;
- Voice and Visual DNA references;
- Primitive evaluation scores;
- active doctrines and Negative Space rules;
- platform and aspect ratio;
- verified quote and data payloads;
- approved asset IDs;
- candidate Micro-Semiotic Anchors.

A composition may not be selected until this object validates.

---

## 4. Composition Router

The router first applies hard constraints, then scores all compatible compositions.

### Hard constraints

1. Composition supports target aspect ratio.
2. Content shape is supported.
3. Text fits the registered budget.
4. Required source assets exist or can be generated safely.
5. Source fidelity requirements are satisfied.
6. Brand Visual Constitution permits the family.
7. Identity, legal, and Micro-Semiotic Anchor constraints pass.

### Weighted selection

```text
24% archetype fit
18% asset derivative fit
14% content shape fit
12% Visual DNA fit
 8% asset availability
 7% primitive fit
 6% platform fit
 5% Micro-Semiotic Anchor fit
 3% novelty without brand drift
 3% historical performance
```

The router returns three candidates from diverse families where possible. The operator may override, but the override reason is stored.

### Fatigue management

The engine tracks recent composition family usage by brand. Repetition is penalized unless the brand deliberately uses a recognizable recurring series shell.

---

## 5. Composition registry

The registry contains 28 contracts across eight families:

| Family | Canonical compositions |
|---|---:|
| Assertion / Commentary | 6 |
| Documentary / Social Card | 2 |
| Comparison / Poll | 7 |
| Cartoon Moral | 3 |
| Cartoon Framework | 4 |
| Conceptual Metaphor | 4 |
| Sports Collage | 2 |
| Promo / Live | 2 |

Each composition includes:

- compatible archetypes and derivatives;
- supported content shapes;
- exact normalized zones;
- text budget;
- provider mode;
- Micro-Semiotic Anchor slots;
- Rough Notation limits;
- evaluation profile.

The canonical data lives in `single_image_composition_registry_v2.json`.

---

## 6. Content-archetype routing

### Story and vulnerability

Best composition families:

- `MAIN_CHARACTER_EMOTIONAL_SCENE`
- `QUOTE_ON_CLOSEUP_COMMENTARY`
- `DIFFICULT_CONVERSATION_CARD`
- `CARTOON_MORAL_SCENE`

Used for Transformation Story, Witness Story, Backstory Reveal, Confessional Turn, and Pain-to-Relief content.

### Authority and challenger content

Best compositions:

- `BLUNT_IMPERATIVE_POSTER`
- `MINIMAL_BLACK_QUOTE_CARD`
- `CARTOON_CHARACTER_PORTRAIT_THESIS`
- `TWEET_STYLE_COMMENTARY_CARD`

Used for Challenger / Frame Breaker, Myth Debunk, Scam Exposure, Authority Proof Stack, and Industry Hypocrisy Exposure.

### Comparison and debate

Best compositions:

- `CONCEPTUAL_CONTRAST_POSTER_LIGHT`
- `CONCEPTUAL_CONTRAST_POSTER_DARK`
- `VS_SCORECARD`
- `THIS_OR_THAT_DEBATE_CARD`
- `ONE_SCENE_TWO_SCENARIOS`
- `CARTOON_DIPTYCH_CONTRAST`

### Polls and audience identification

Best compositions:

- `WOULD_YOU_RATHER_BASIC`
- `WOULD_YOU_RATHER_IDENTITY_LADDER`
- `COMPARISON_POLL_VERTICAL`
- `THIS_OR_THAT_DEBATE_CARD`

### Education and frameworks

Best compositions:

- `POWERFUL_DEMONSTRATION_SINGLE`
- `CARTOON_OBJECT_METAPHOR`
- `CARTOON_TRIPTYCH_PROGRESS`
- `CARTOON_QUAD_FRAMEWORK`
- `PROGRESSION_FRAMEWORK_POSTER`

### Reactions and social proof

Best compositions:

- `SOCIAL_SCREENSHOT_REACTION_CARD`
- `TWEET_STYLE_COMMENTARY_CARD`
- `QUOTE_ON_CLOSEUP_COMMENTARY`

---

## 7. Composition geometry

All zones use normalized coordinates from `0.0` to `1.0`. This permits one canonical layout to render at 1080×1080, 1080×1350, or 1080×1920 while retaining deterministic proportions.

A composition is a set of declared zones. Assets and text may only occupy registered zones unless an operator explicitly edits the scene specification.

Example:

```json
{
  "composition_id": "WOULD_YOU_RATHER_BASIC",
  "zones": [
    {"id":"headline","bounds":{"x":0.06,"y":0.035,"w":0.88,"h":0.11}},
    {"id":"left","bounds":{"x":0.055,"y":0.18,"w":0.415,"h":0.60}},
    {"id":"right","bounds":{"x":0.53,"y":0.18,"w":0.415,"h":0.60}}
  ]
}
```

No generative provider decides these coordinates.

---

## 8. Skia component system

The renderer is component-based. Important components include:

- `CanvasRoot`
- `TextureBackground`
- `ImageCover`
- `SubjectCutout`
- `HeroScenePlate`
- `HeadlineBlock`
- `QuoteBlock`
- `PaperStripLabel`
- `OptionFrame`
- `VsBadge`
- `ScorecardBullets`
- `PanelGrid`
- `ProgressionPath`
- `StatChip`
- `SocialPostShell`
- `EventMetadataStack`
- `MicroSemioticAnchorLayer`
- `RoughAnnotationLayer`
- `BrandSignature`

Every component receives typed props and no component is allowed to fetch brand context independently. All context is precompiled into `SingleImageSceneSpecV2`.

---

## 9. Text compiler

The copy compiler turns expression material into a hierarchy, not a paragraph.

### Allowed text roles

- headline;
- support line;
- quote;
- option label;
- panel caption;
- bullet feature;
- stat chip;
- metadata;
- CTA;
- attribution.

### Rules

1. The registered word budget is a hard limit.
2. The renderer uses deterministic line breaking.
3. The agent may propose emphasis spans but cannot choose arbitrary fonts.
4. Accent words must come from meaning, contrast, or Voice DNA—not decoration.
5. Quote and stat posts require verified source objects.
6. Auto-fit may reduce size only within the composition's configured range. Beyond that, the content must be rewritten or another composition selected.

---

## 10. Ideogram 4 responsibilities

Ideogram 4 is used as a **composition and metaphor provider**, not the final poster renderer.

### Ideogram may create

- conceptual metaphor plates;
- emotional scenes;
- cartoon moral scenes;
- object metaphors;
- matched comparison assets;
- panel illustrations;
- custom hero scenes.

### Ideogram may not create

- final copy;
- quotes;
- statistics;
- handles or social metadata;
- dates, times, CTAs, or logos;
- final panel borders or poll UI.

For comparison and framework compositions, generate the scenes separately so that Skia retains exact geometry and option parity.

The prompt contracts live in `single_image_ideogram_prompt_contracts_v2.json`.

---

## 11. Qwen-Image-Layered, SAM3, GPT Image and Flux

### Qwen-Image-Layered

Use when a generated flat scene contains objects that should be repositioned, recolored, or independently evaluated. It produces an initial RGBA layer stack. It is not required for quote cards, social cards, poll shells, sports collages, or flyers.

### SAM3

Use for exact subject and object masks, cutouts, and refinement of Qwen-generated layers. SAM3 is also the default route for approved client portraits and real-world objects.

### GPT Image

Use for character assets, object assets, approved style variants, and targeted generation/editing.

### Flux Edit

Use for identity-preserving character substitution, visual repair, hand repair, and local style harmonization.

### Final authority

Skia always reconstructs the final composition.

---

## 12. Rough Notation doctrine

Rough Notation is permitted only when it performs one of these jobs:

1. directs attention;
2. marks contrast;
3. rejects or corrects a claim;
4. groups related information;
5. proves a visual relationship;
6. points to an action.

Each composition has a maximum annotation count. The annotation seed is stored so the final result is reproducible.

---

## 13. Micro-Semiotic Anchoring

Each composition may expose one or more anchor slots. The engine selects only from the approved Brand Anchor Library.

The anchor must be:

- audience-native;
- subtle or secondary;
- legally approved;
- consistent with the scene;
- semantically useful or socially recognizable.

The engine scores recognition, subtlety, brand fit, distraction risk, stereotyping risk, and trademark risk.

---

## 14. Evaluation and repair

Every render passes through a global rubric and its family-specific profile.

### Global dimensions

- hook clarity;
- message legibility;
- composition hierarchy;
- archetype fit;
- derivative fit;
- brand consistency;
- primitive compliance;
- negative-space compliance;
- Micro-Semiotic Anchor quality;
- source fidelity;
- platform fit.

### Example repair loop

```text
render
→ eval detects binary clarity = 0.58
→ evaluator identifies unequal option scale
→ repair plan adjusts image crop and option label size
→ deterministic rerender
→ eval repeats
→ operator review
```

Generative repair is allowed only when the failed dimension concerns an asset. Typography, geometry, spacing, and hierarchy failures are repaired deterministically.

---

## 15. Approval workflow

```text
draft
→ routed
→ assets_pending
→ rendering
→ auto_evaluated
→ awaiting_operator_review
→ approved / needs_revision / rejected
→ publishing intent
→ published
```

The operator can:

- accept the chosen composition;
- select another router candidate;
- edit copy within budget;
- replace an asset;
- change a Micro-Semiotic Anchor;
- request a generative repair;
- approve final publishing.

The system records every override and revision.

---

## 16. Reproducibility

Every production record pins:

- Brand Context Version;
- registry bundle version;
- provider and model versions;
- prompt contract version;
- provider seeds;
- approved asset IDs and hashes;
- Qwen layer manifest hash;
- SAM mask hash;
- font manifest hash;
- Rough Notation seed;
- Skia renderer version;
- final output SHA-256.

This guarantees that the same approved inputs can be rendered again even if a brand later changes.

---

## 17. Required production services

### Python services

- Single Image Compiler;
- Composition Router;
- Provider Job Planner;
- Asset Resolver;
- Evaluation Engine;
- Approval and Audit Service.

### Worker routes

- Ideogram composition worker;
- GPT Image asset worker;
- Flux edit worker;
- Qwen layer decomposition worker;
- SAM3 cutout worker;
- Skia render worker;
- visual evaluation worker.

### UI routes

- candidate comparison view;
- scene spec editor;
- layer and cutout review;
- final mobile preview;
- approve / revise / reject;
- publishing preview.

---

## 18. Implementation gate

The Single Image Post Engine V2 is production-ready only when:

1. all 28 contracts validate;
2. every contract has at least one golden render;
3. router regression tests cover every archetype family;
4. text overflow tests pass for all supported ratios;
5. source fidelity tests block altered quotes and statistics;
6. brand snapshots and asset hashes appear in every receipt;
7. operator override and revision actions are auditable;
8. deterministic rerenders produce the same output hash under the same renderer environment;
9. visual evaluations correctly localize common failures;
10. publishing cannot occur without explicit approval.

---

## 19. Included artifacts

- `single_image_composition_registry_v2.json`
- `single_image_router_policy_v2.json`
- `single_image_skia_component_catalog_v2.json`
- `single_image_ideogram_prompt_contracts_v2.json`
- `single_image_eval_rubrics_v2.json`
- `single_image_provider_responsibilities_v2.json`
- `single_image_examples_v2.json`
- `single_image_composition_models_v2.py`
- `single_image_render_contracts_v2.ts`

---

## Final doctrine

The Single Image Post Engine does not ask an image model to design the content.

It compiles meaning into an approved composition grammar, lets generative systems create only the visual assets that cannot be rendered deterministically, and uses Skia to assemble the final brand-safe artifact.
