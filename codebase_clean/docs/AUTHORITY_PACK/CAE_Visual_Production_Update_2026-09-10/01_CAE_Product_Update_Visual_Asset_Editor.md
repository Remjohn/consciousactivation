# CAE Product Update — Evidence-First Visual Asset Studio

**Status:** Proposed product update  
**Date:** 2026-09-10  
**Product:** Conscious Activations  
**Primary capability:** Visual Asset Editor + Storyboard + Evidence-First Transformation

## 1. Product decision

Conscious Activations will add a first-class **Evidence-First Visual Asset Studio** as the operator production surface for visual transformation and composition.

This is not a generic image-generation product.

The product hierarchy is:

```text
Research
  ↓
Evidence
  ↓
Semantic / Activation Meaning
  ↓
Format Storyboard Program
  ↓
Narrative Editing Grammar
  ↓
Editorial Expression Calculus
  ↓
Transformation Intent
  ↓
Transformation Recipe
  ↓
Visual Asset Studio
  ↓
Expression / Composition
  ↓
Runtime
```

The central production principle is:

> **Transform reality into clearer meaning before recreating reality synthetically.**

## 2. Why this is the right extension of CAE

The current repository already contains the essential upstream doctrine:

- `EditorialStoryboard` is the operator-approved visual/narrative blueprint.
- `SemanticProgram` carries intent and perceptual profile.
- `CompositionIR` is renderer-agnostic realization structure.
- `AssetAnnotation` carries deep multimodal labels and rights for selected reusable media.
- `InsertRole` distinguishes functional media such as `PATTERN_INTERRUPT`, `CONTRAST`, `SEMANTIC_SIMILE` and `EMOTIONAL_AMPLIFICATION`.
- the VAE delegation boundary is already receipt-driven and source-lineage aware.

The missing product surface is the **operator-editable visual transformation workspace** that makes these objects practically usable.

The existing object register already defines the key boundary: `EditorialStoryboard` is the operator-approved blueprint; `CompositionIR` is the renderer-agnostic realization; a concrete `VideoEditProgram` is downstream execution syntax. This update preserves that distinction rather than replacing it.

## 3. The new visual production model

### Evidence-first priority

The preferred order is:

```text
RETRIEVE
    ↓
TRANSFORM
    ↓
COMPOSE
    ↓
GENERATE
```

Generation remains available for justified cases, but it is not the default expression strategy.

### Visual Asset Studio responsibilities

The Studio lets the operator:

- inspect source evidence
- inspect source quality
- preview candidate media
- replace an asset
- crop / reframe / mask / cut out
- highlight evidence
- annotate
- blur or protect information
- create controlled zoom/pan/sequence motion
- apply justified color treatment
- extract OCR/text or regions
- create layers from real source material
- edit BBOX composition
- edit transformation intent
- regenerate a visual proposal or prompt
- compare revisions
- approve or reject a composition

## 4. Storyboard becomes an active production object

Storyboard is not a disposable planning document.

It becomes the living expression plan between Harness and runtime.

```text
Harness
  ↓
Storyboard Session
  ↓
Operator inspection
  ↓
Transformation design
  ↓
Composition resolution
  ↓
Runtime compile
```

Each format gets a format-specific Storyboard Program:

```text
VideoStoryboardProgram
CarouselStoryboardProgram
SuperVisualStoryboardProgram
PresentationStoryboardProgram
```

All share the same governed transformation and feedback contracts.

## 5. Narrative Editing Grammar

CAE introduces **Narrative Editing Grammar** as the formal language connecting narrative meaning to visual expression.

Core grammar operators initially include:

```text
WITHHOLD
REVEAL
FOCUS
CONTRAST
PROVE
EXPLAIN
CONNECT
REORIENT
ESCALATE
INTERRUPT
RESOLVE
```

These are editorial relationships, not effects.

Example:

```text
Scene purpose = CONTRADICTION
        ↓
Grammar = WITHHOLD → REVEAL → HOLD → RETURN
```

## 6. Editorial Expression Calculus

CAE introduces **Editorial Expression Calculus** as the numeric layer that controls magnitude and timing.

Initial variables:

```text
pace
shot_duration
hold_duration
cut_interval
occupancy
scale
motion_amplitude
motion_velocity
visual_density
caption_density
salience
intervention_frequency
```

The calculus must account for:

- archetype
- scene purpose
- activation meaning
- viewer attention state
- source quality
- existing visual complexity
- recent visual repetition
- format constraints

The model may propose a value range; deterministic code validates and clamps the resulting expression.

## 7. Transformation Intent

Transformation is defined as a semantic projection into perceptible media change.

Canonical fields:

```text
intent
source
semantic_target
mode
emphasis
motion
constraints
```

Example:

```yaml
intent: REVEAL
source: evidence_asset_213
semantic_target: revenue_figure
mode: EXTRACT_REGION
emphasis: MODERATE
motion: REVEAL_FOCUS
```

## 8. Transformation Recipes

To keep execution small and deterministic, the system will use reusable Transformation Recipes.

Initial examples:

```text
DOCUMENT_ZOOM_v1
FOCUS_ON_QUOTE_v1
SCREENSHOT_CALLOUT_v1
SUBJECT_ISOLATION_v1
CONTRADICTION_SPLIT_v1
PROOF_SEQUENCE_v1
REVEAL_REGION_v1
PATTERN_DISRUPTION_v1
BEFORE_AFTER_v1
```

A Recipe contains:

- supported intents
- eligible source types
- allowed primitives
- emphasis range
- motion grammar
- keyframe strategy
- source-quality limits
- Design System constraints
- wrong-reading constraints

## 9. Source quality must influence expression

The Studio will derive a `SourceQualityProfile`.

The editing grammar may therefore select different expression strategies for:

```text
4K / clean source
1080p / clean source
720p / pre-cropped source
480p / degraded source
heavily compressed source
```

Example:

```text
High quality talking head
→ subtle 8–12% reframe
→ subtle LUT
→ minimal attention cost
→ acceptable
```

versus:

```text
480p pre-cropped speaker
→ aggressive zoom
→ quality becomes salient
→ rejected
```

Alternative:

```text
480p speaker
→ smaller reaction container
→ source evidence dominates
→ grayscale / controlled treatment
→ distraction reduced
```

The point is not to hide low quality with effects; it is to prevent quality defects from competing with meaning.

## 10. SAM3 Visual Intelligence

CAE will create a dedicated tracking layer rather than make OpenChatCut the owner of visual identity.

Operator workflow:

```text
select speaker
  ↓
select reference face / body
  ↓
SAM3 prompt
  ↓
tracking session
  ↓
track geometry
  ↓
Storyboard / BBOX
  ↓
OpenChatCut / SuperVisual
```

The operator can refine, split, restart, or reject tracks.

The result is governed visual evidence, not semantic truth.

## 11. Visual Chat

The Visual Studio will include a chat interface analogous to the OpenChatCut operating model.

Examples:

```text
“Make this composition quieter.”
“Keep the screenshot but emphasize the number.”
“Give me three alternatives using the same evidence.”
“Move the visual emphasis away from the speaker’s face.”
“Regenerate the BBOX composition.”
“Use the same visual grammar as Scene 4.”
```

Chat actions create proposals. The operator remains the final authority.

## 12. Operator teaching loop

Every storyboard element can receive:

```text
GOOD
NEEDS_EDIT
REJECT
```

Optionally:

```text
reason
category
region
before/after
revision
```

Feedback is stored as immutable evidence for evaluation and future ranking improvements.

## 13. Runtime topology

One browser tab exposes one CAE Studio.

Underneath, runtimes remain isolated processes.

```text
CAE Studio
   ↓
Gateway / Runtime Registry
   ├── CAE API
   ├── OpenChatCut
   ├── Slidev / reveal
   ├── SuperVisual runtime
   └── SAM3
```

No runtime becomes the source of CAE meaning.

## 14. Partner-facing result

The product should be able to demonstrate:

```text
real interview evidence
→ selected source frame
→ storyboard scene
→ transformation intent
→ actual composition
→ operator correction
→ final compiled SuperVisual or OpenChatCut edit
→ preserved lineage
```

This demonstrates the CAE method rather than an AI-generation demo.

## 10. Asset Research Session

Asset research is a first-class operator activity, not a hidden search endpoint.

The Studio will provide a PlayPhrase-like **Asset Research Session** for evidence-grounded media retrieval:

```text
need
 ↓
retrieval
 ↓
candidates
 ↓
preview
 ↓
swipe / compare
 ↓
accept / reject / replace
 ↓
promote to storyboard
```

Candidates should be visible as actual playable media whenever technically possible, with source interval, transcript/context, rights, confidence and provenance immediately available.

## 11. Surgical integration strategy

External repositories are used in controlled extraction sessions. A session begins from a CAE Functional Requirement, identifies the exact source files/components needed to satisfy it, proves licensing/dependencies, reproduces behavior behind a CAE adapter, tests it, and only then decides whether to retain the external component or rebuild the capability natively.

This avoids both extremes:

```text
DO NOT:
clone everything blindly

DO NOT:
rebuild every proven interaction from scratch

DO:
extract proven behavior surgically
→ validate locally
→ normalize to CAE contracts
→ compose into one Studio
```

## 12. Partner-facing product promise

The operator experience should feel like one CAE Studio even when multiple engines execute underneath it. The operator can research evidence, preview candidates, storyboard the scene, modify transformation, inspect the composition, give feedback, and hand the resolved expression to the native runtime without leaving the Studio.

## 13. Functional requirement summary

The Visual Asset Studio release is treated as an implementation surface with explicit functional requirements, not as an open-ended design exercise. The PRD defines the normative requirements; the Product Update summarizes the partner-facing capabilities.

Core release requirements:

```text
FR-VAE-001–015  existing evidence, transformation, validation, runtime and SuperVisual requirements
FR-VAE-016       Asset Research Session
FR-VAE-017       Candidate selection receipt
FR-VAE-018       deterministic automatic acceptance
FR-VAE-019       rapid swipe/keyboard candidate inspection
FR-VAE-020       surgical external-component adoption traceability
FR-VAE-021       bounded component-session workflow
FR-VAE-022       operator visual feedback
```

A component is not considered adopted merely because an agent can copy its code. It must satisfy a CAE Functional Requirement and pass CAE contract plus interaction/visual evidence.
