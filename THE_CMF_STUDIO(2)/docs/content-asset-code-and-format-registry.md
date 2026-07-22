---
title: "CMF Studio Content Asset Code and Format Registry"
status: "draft-canonical"
created_at: "2026-06-22"
source_files:
  - "THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md"
  - "THE CMF STUDIO/docs/prd/modules/PRD_CMF_03_Workspace_Commercial_Consent_Source.md"
  - "THE CMF STUDIO/docs/prd/modules/PRD_CMF_06_Interview_Expression_Routing.md"
  - "THE CMF STUDIO/docs/ux/ux-design-specification.md"
---

# CMF Studio Content Asset Code and Format Registry

## 1. Purpose

Every content asset needs two identities:

- a canonical internal ID for storage, commands, events, receipts, and joins;
- an operator-facing content asset code that tells a human what the asset is.

The internal ID can be opaque. The content asset code must be readable in queues, review screens, Telegram payloads, file exports, Publer drafts, memory entries, and revision history.

## 2. Scope Hierarchy

The product hierarchy is:

```text
organization
-> brand_workspace
-> guest
-> expression_session
-> asset_package
-> content_asset
-> asset_version
```

Operators must never work from a loose global asset list. Every asset belongs to a brand workspace and guest context before it becomes reviewable, publishable, or eligible for memory.

## 3. Canonical Content Asset Code

Format:

```text
{BRD}-{GST}-{SES}-{PKG}-{FMT}-{SEQ}-V{VER}
```

Example:

```text
CEL-CLDNTA-S01-GAP-SV-CSC-001-V01
```

This means:

| Segment | Meaning | Example |
|---|---|---|
| `BRD` | Brand workspace code | `CEL` for Conscious Elite |
| `GST` | Guest/client code | `CLDNTA` for Claude Ntahuga |
| `SES` | Session code | `S01` |
| `PKG` | Package or production scope | `GAP` for Guest Asset Pack |
| `FMT` | Content format code | `SV-CSC` |
| `SEQ` | Sequence number inside package/session | `001` |
| `VER` | Asset version | `V01` |

The code is not the database primary key. The system must still store stable UUIDs or equivalent internal IDs. The readable code is generated from scoped records and remains unique within the organization.

## 4. Package Codes

| Code | Package |
|---|---|
| `GAP` | Trial Guest Asset Pack |
| `MAE` | Monthly Asset Engine |
| `CUS` | Custom internal production scope, not a customer-facing offer |

Customer-facing pricing remains only `$29/week` trial Guest Asset Pack and `$99/month` Monthly Asset Engine.

## 5. Content Format Families

| Family Code | Family | Description |
|---|---|---|
| `SV` | Short Video | Vertical or platform-specific short-form video derived from an approved Expression Moment |
| `CAR` | Carousel | Multi-slide visual sequence, including listicle, juxtaposition, explanatory, or story arc carousels |
| `VPL` | Visual Poll | Poll-style visual prompt, versus/choice post, or audience-response asset |
| `TWQ` | Tweet-Like Quote | Text-first quote post that resembles social quote/tweet formatting without becoming an unsupported platform clone |
| `MEM` | Meme | Meme visual routed through a valid Meme Mechanism and source-safe distortion constraints |
| `SPV` | Super Visual | High-impact standalone visual, conceptual contrast, symbolic image, or premium single-frame asset |
| `RCT` | Reaction Seed | Reaction prompt, reaction visual, or reusable social-native response seed |

Newsletters are not a valid CMF content format.

## 5.1 Reaction Editing Template Codes

Reaction editing templates are animated editing grammars used after an approved route and before SceneSpec compilation. They are especially important now that CMF films guest material live: the Interview Asset Contract can ask questions designed to produce the live-answer slots required by the template.

| Template Code | Template | Primary Legacy App Reference | Typical Output |
|---|---|---|---|
| `VRS-SPLIT` | Versus Split Screen | `apps/react-debate` | this-vs-that debate, Would You Rather, split-screen verdict |
| `TRK-TIER` | Tier List Ranking | `apps/react-tierlist` | Goal-style tier list, red flag ranking, authority tier board |
| `RNK-BLIND` | Blind Ranking | `apps/react-blind-rank` | suspense ranking with locked positions |
| `RNK-PROPOSAL` | Proposal Ranking Quiz | `apps/react-ranking-quiz` | wrong-order correction, reorder quiz, principle reveal |
| `ELM-BRACKET` | Elimination Bracket | `apps/react-elimination` | knockout comparison, survivor/winner reveal |
| `MIR-QUIZ` | Mirror Quiz | `apps/react-mirror-quiz` | which-one-are-you recognition quiz |
| `AUTH-LADDER` | Authority Ladder Quiz | `apps/react-authority-quiz` | expert test, level ladder, pass/fail gate |

These are not separate customer-facing packages. They are production template routes attached to valid content formats such as `SV-RRC`, `VPL-WYR`, `VPL-VRS`, `CAR-LST`, `MEM-REL`, and `RCT-SEED`.

## 6. Short Video Subformats

The trial Guest Asset Pack expects four short videos when source material supports them:

| Code | Short Video Format | Purpose |
|---|---|---|
| `SV-CSC` | Cinematic Story Commentary | A source-backed story or emotionally charged commentary clip |
| `SV-EDU` | Educational Explainer | A clear teaching or explanation clip grounded in the guest's expertise |
| `SV-FRB` | Challenger / Frame Breaker | A contradiction, myth break, stance shift, or edge-product clip |
| `SV-RRC` | Reaction / Recognition Clip | A recognition moment, social-native reaction, or resonant audience mirror |

These are asset derivatives, not arbitrary video categories. They must originate from approved Expression Moments and route receipts.

## 7. Non-Video Format Codes

| Code | Format | Example Template Family |
|---|---|---|
| `CAR-LST` | Listicle Carousel | numbered learning sequence |
| `CAR-JUX` | Juxtaposition Carousel | before/after, contrast, timeline, mistake/fix |
| `VPL-WYR` | Would-You-Rather Visual Poll | two-option contrast prompt |
| `VPL-VRS` | Versus Visual Poll | A vs B comparison |
| `TWQ-STD` | Standard Tweet-Like Quote | identity header plus quote body |
| `TWQ-IMG` | Image-Backed Tweet-Like Quote | quote over portrait or contextual image |
| `MEM-INC` | Incongruity Meme | humor from mismatch or contradiction |
| `MEM-REL` | Relatable Recognition Meme | audience recognition or shared pain |
| `SPV-CON` | Conceptual Contrast Super Visual | high-impact visual metaphor or binary contrast |
| `SPV-SYM` | Symbolic Super Visual | symbolic single-frame image tied to primitive or route |
| `SPV-PRM` | Premium Brand Super Visual | brand-forward, polished standalone visual |
| `RCT-SEED` | Reaction Seed | reusable reaction prompt or visual cue |

These codes should be seed records in the content-format registry and can grow only through product-approved registry changes.

## 7.1 Single Image Composition Engine Compatibility

Single-image outputs are routed by the Single Image Post Engine, not by the carousel sequence builder. The same archetype can still become a carousel, video, poll, meme, quote card, reaction seed, or SuperVisual, but `format_subtype_code` decides which output-family router is allowed to own the composition.

Runtime source:

```text
THE CMF STUDIO/registries/composition/single_image_composition_registry.v2.json
THE CMF STUDIO/registries/composition/single_image_router_policy.v2.json
THE CMF STUDIO/registries/composition/single_image_provider_responsibilities.v2.json
THE CMF STUDIO/registries/evals/composition/single_image_eval_rubrics.v2.json
```

| Content Format | Single Image Families | Canonical Composition Examples |
|---|---|---|
| `SPV-CON` | conceptual metaphor, comparison poll | `POWERFUL_DEMONSTRATION_SINGLE`, `CONCEPTUAL_CONTRAST_POSTER_LIGHT`, `CONCEPTUAL_CONTRAST_POSTER_DARK`, `ONE_SCENE_TWO_SCENARIOS` |
| `SPV-SYM` | conceptual metaphor, cartoon moral | `MAIN_CHARACTER_EMOTIONAL_SCENE`, `CARTOON_OBJECT_METAPHOR`, `PROBLEM_AMPLIFICATION_URGENCY`, `CARTOON_MORAL_SCENE` |
| `SPV-PRM` | assertion commentary, promo live, documentary social card | `QUOTE_ON_CLOSEUP_COMMENTARY`, `MINIMAL_BLACK_QUOTE_CARD`, `EXPERT_FLYER_MINIMAL`, `LIVE_SHOW_FLYER` |
| `VPL-WYR` | comparison poll | `WOULD_YOU_RATHER_BASIC`, `WOULD_YOU_RATHER_IDENTITY_LADDER`, `COMPARISON_POLL_VERTICAL` |
| `VPL-VRS` | comparison poll | `VS_SCORECARD`, `THIS_OR_THAT_DEBATE_CARD`, `CONCEPTUAL_CONTRAST_POSTER_DARK` |
| `TWQ-STD` | assertion commentary, documentary social card | `MINIMAL_BLACK_QUOTE_CARD`, `TWEET_STYLE_COMMENTARY_CARD` |
| `TWQ-IMG` | assertion commentary, documentary social card | `QUOTE_ON_CLOSEUP_COMMENTARY`, `TWEET_STYLE_COMMENTARY_CARD` |
| `MEM-INC` | cartoon moral, conceptual metaphor | `CARTOON_OBJECT_METAPHOR`, `CARTOON_MORAL_SCENE`, `DIFFICULT_CONVERSATION_CARD` |
| `MEM-REL` | documentary social card, cartoon moral, assertion commentary | `SOCIAL_SCREENSHOT_REACTION_CARD`, `DIFFICULT_CONVERSATION_CARD`, `CARTOON_CHARACTER_PORTRAIT_THESIS` |
| `RCT-SEED` | documentary social card, comparison poll, assertion commentary | `SOCIAL_SCREENSHOT_REACTION_CARD`, `THIS_OR_THAT_DEBATE_CARD`, `QUOTE_ON_CLOSEUP_COMMENTARY` |

Every single-image composition must carry at least three primitive obligations, source fidelity when using quotes/stats/screenshots, a Skia render receipt, and an evaluation receipt before operator approval. Ideogram 4 may propose metaphor or composition plates, Qwen may extract editable layers, SAM3 may own masks, and GPT Image 2 or Flux Edit may own asset generation or repair, but Skia owns the final deterministic layout and final text placement.

## 7.2 Format to Reaction Template Compatibility

| Content Format | Compatible Reaction Templates |
|---|---|
| `SV-RRC` | `VRS-SPLIT`, `TRK-TIER`, `RNK-BLIND`, `RNK-PROPOSAL`, `ELM-BRACKET`, `MIR-QUIZ`, `AUTH-LADDER` |
| `SV-EDU` | `TRK-TIER`, `RNK-PROPOSAL`, `AUTH-LADDER` |
| `CAR-LST` | `TRK-TIER`, `RNK-PROPOSAL` |
| `VPL-WYR` | `VRS-SPLIT`, `MIR-QUIZ` |
| `VPL-VRS` | `VRS-SPLIT`, `RNK-BLIND`, `ELM-BRACKET` |
| `MEM-REL` | `MIR-QUIZ` |
| `RCT-SEED` | All registered reaction templates when the seed is stored for future use |

## 8. UI Requirements

Every production queue and review surface must show:

- brand workspace;
- guest/client;
- session;
- content asset code;
- content format family and subtype;
- package scope;
- route receipt;
- source Expression Moment;
- current version;
- approval state;
- publish state.

The Control Tower must provide filters for:

- brand workspace;
- guest/client;
- session;
- package;
- content format family;
- approval state;
- blocker state;
- publishing state.

## 9. Receipt Requirements

Receipts must reference both internal IDs and readable codes:

- `content_asset_id`
- `content_asset_code`
- `brand_workspace_id`
- `brand_workspace_code`
- `guest_id`
- `guest_code`
- `expression_session_id`
- `asset_package_id`
- `format_family_code`
- `format_subtype_code`
- `asset_version`

This prevents screenshots, Telegram messages, exports, file names, Publer drafts, and memory events from becoming ambiguous.
