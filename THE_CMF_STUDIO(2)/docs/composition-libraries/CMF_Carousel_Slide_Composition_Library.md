# CMF Carousel Slide Composition Library

Status: active-draft  
Registry: `registries/composition/carousel_slide_composition_library.v1.json`  
Applies to: `CAR-LST`, `CAR-JUX`

## 1. Current Recognition State

CMF Studio currently recognizes carousels at the format level:

| Code | Meaning |
|---|---|
| `CAR-LST` | Listicle Carousel: numbered learning sequence, framework map, explanatory sequence. |
| `CAR-JUX` | Juxtaposition Carousel: before/after, contrast, timeline, mistake/fix, two-world comparison. |

Before this library, CMF did not have a queryable slide-level composition library. The system could say "make a carousel", but it did not yet define reusable slide atoms with a precise composition meaning.

## 2. Principle

A carousel is not a stack of pretty slides.

It is a sequence of meaning-bearing visual moves. Each slide must answer:

```text
What does this slide do to the audience's understanding?
What primitive triad makes that move legitimate?
What visual grammar makes that move visible?
What geometry rules make it renderable?
Where may this slide appear in the sequence?
```

## 3. Required Carousel Primitives

These primitives should be treated as the default carousel foundation:

| Primitive | Use |
|---|---|
| `PRM-BUS-003` Narrative Structural Backbone | Prevents the carousel from becoming a flat information dump. |
| `PRM-BUS-012` The Grid as Cognitive Relief | Preserves continuity, alignment, and production scalability. |
| `PRM-VSG-018` Sequence Over Single Image | Forces shot/slide variety across the sequence. |
| `PRM-VSG-001` Composition as Eye-Path Engineering | Gives each slide a deliberate scan path. |
| `PRM-PRS-032` The Explanation Engine | Makes complex ideas legible without diluting them. |
| `PRM-PRS-015` The What Is / What Could Be Contrast Engine | Gives transformation, juxtaposition, and tension their structure. |
| `PRM-VSG-024` Space as Psychological Relationship | Lets space carry emotional state instead of acting as decoration. |
| `PRM-PRS-025` The Rule of Three Message Architecture | Keeps frameworks and listicles cognitively retainable. |

Supporting primitives such as `PRM-HUM-032` and `PRM-HUM-034` are valid when the carousel intentionally includes a pattern break, humor turn, or punch-up pass.

## 4. Slide Atoms

The registry currently defines 12 slide atoms:

| Code | Meaning Job | Best Position |
|---|---|---|
| `CAR-SL-001-HOOK-PREMISE` | Name the edge, contradiction, promise, or question. | first |
| `CAR-SL-002-AUDIENCE-MIRROR` | Make the audience recognize themselves. | early/middle |
| `CAR-SL-003-STAKES-COST` | Show the cost of the current belief or habit. | early/middle |
| `CAR-SL-004-MYTH-BREAK` | Separate myth from truer frame. | early/middle |
| `CAR-SL-005-MECHANISM-REVEAL` | Reveal the hidden mechanism or causal model. | middle |
| `CAR-SL-006-THREE-PILLAR-MAP` | Compress teaching into three memorable buckets. | middle/late |
| `CAR-SL-007-JUXTAPOSITION` | Compare two worlds, choices, states, or identities. | middle/late |
| `CAR-SL-008-EVIDENCE-OBJECT` | Ground the claim in source-backed proof. | middle/late |
| `CAR-SL-009-CONCRETE-SCENE` | Turn abstraction into a real-life scene. | middle/late |
| `CAR-SL-010-PATTERN-BREAK` | Interrupt a pattern for surprise or memorability. | late |
| `CAR-SL-011-REFRAME-IDENTITY` | Name the new interpretation or identity shift. | late/penultimate |
| `CAR-SL-012-APPLICATION-CTA` | Convert the insight into one concrete next action. | last |

## 5. Query Model

Agents should query the registry by:

- `format_code`;
- `composition_meaning`;
- `allowed_position`;
- `archetype_route`;
- `primitive_id`;
- `visual_shot_type`;
- `layout_density`;
- `matrix_pressure`;
- `audience_state`;
- `source_expression_moment_id`;
- `brand_context_version_id`.

Example query:

```json
{
  "format_code": "CAR-JUX",
  "composition_meaning": "contrast current belief with better frame",
  "primitive_id": "PRM-PRS-015",
  "allowed_position": "middle"
}
```

Expected candidate:

```json
{
  "slide_atom_code": "CAR-SL-007-JUXTAPOSITION",
  "requires": ["two comparable states", "short mirrored labels", "contrast-safe geometry"]
}
```

## 6. Default Sequence Blueprints

### Five Slide Explanation Carousel

```text
1. Hook Premise Cover
2. Audience Mirror
3. Mechanism Reveal
4. Three-Pillar Map
5. Application CTA
```

Use when the source expression moment is primarily educational and the audience needs clarity.

### Six Slide Juxtaposition Carousel

```text
1. Hook Premise Cover
2. Stakes and Cost
3. Juxtaposition Split
4. Evidence Object
5. Reframe and Identity Shift
6. Application CTA
```

Use when the source expression moment contains contrast, before/after, myth/truth, or competing worldviews.

### Seven Slide Listicle With Turn

```text
1. Hook Premise Cover
2. Audience Mirror
3. Mechanism Reveal
4. Three-Pillar Map
5. Concrete Scene
6. Pattern Break
7. Application CTA
```

Use when the guest's voice supports a self-aware turn and the carousel should feel more social-native.

## 7. Production Rules

- Every slide atom must pass at least three primitive validations.
- Every carousel must preserve grid continuity through `PRM-BUS-012`.
- Every carousel must preserve visual variety through `PRM-VSG-018`.
- Every slide must have a `composition_meaning`; decorative slides are invalid.
- Every slide must emit a Geometrics layout plan before Skia render.
- A pattern break slide is only valid after earlier slides establish a pattern.
- A CTA slide may contain only one primary action.

## 8. What This Enables

The CMF agents can now ask:

```text
Which slide atom best serves this source moment, this primitive coalition, this route, and this audience state?
```

Instead of:

```text
Which Canva-like layout should we use?
```

That difference matters. The slide library becomes a reasoning layer, not a design scrapbook.
