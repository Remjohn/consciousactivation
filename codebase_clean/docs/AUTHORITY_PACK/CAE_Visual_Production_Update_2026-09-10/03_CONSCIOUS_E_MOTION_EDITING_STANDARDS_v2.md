# Conscious E-Motion Editing Standards v2
## Narrative Editing Grammar + Editorial Expression Calculus

**Status:** Proposed constitutional update  
**Date:** 2026-09-10  
**Purpose:** Formalize evidence-first, meaning-first editing as a governed language and quantitative expression system.

# Amendment I — The First Principle

> **The best editing is the editing the viewer does not see.**

Editing exists to serve meaning, story, evidence, emotion and attention.

Editing MUST NOT be performed merely to demonstrate technical activity.

An edit may be substantial in implementation while remaining perceptually invisible. That is a success when it improves the intended experience without diverting attention toward itself.

The system must distinguish:

```text
EDITING THAT SERVES MEANING
```

from:

```text
EDITING THAT CALLS ATTENTION TO THE EDIT
```

The former is preferred.

# Amendment II — Meaning Before Mechanism

Every editorial intervention MUST have an upstream purpose.

The canonical hierarchy is:

```text
ACTIVATIVE MEANING
       ↓
NARRATIVE ARC
       ↓
SCENE PURPOSE
       ↓
EDITORIAL INTENT
       ↓
NARRATIVE EDITING GRAMMAR
       ↓
EDITORIAL EXPRESSION CALCULUS
       ↓
TRANSFORMATION INTENT
       ↓
TRANSFORMATION RECIPE
       ↓
PRIMITIVES / KEYFRAMES
       ↓
RUNTIME
```

No primitive is a sufficient reason for itself.

"Zoom" is not meaning.

"Transition" is not meaning.

"Animation" is not meaning.

The reason must exist above the operation.

# Amendment III — Narrative Editing Grammar

**Narrative Editing Grammar** is the controlled language through which narrative meaning becomes perceptual expression.

Initial grammar operators:

```text
WITHHOLD
REVEAL
FOCUS
CONTRAST
PROVE
EXPLAIN
CONNECT
COMPARE
REORIENT
ESCALATE
INTERRUPT
RESOLVE
```

Grammar describes relationships and sequences.

Example:

```text
SCENE PURPOSE = CONTRADICTION

WITHHOLD
  ↓
REVEAL EVIDENCE
  ↓
HOLD
  ↓
RETURN TO SPEAKER
```

The implementation might use a screenshot, a crop, a highlight and a slow zoom. Those are consequences of the grammar.

# Amendment IV — Editorial Expression Calculus

**Editorial Expression Calculus** is the quantitative layer that controls the magnitude, frequency, timing and perceptual cost of an editorial expression.

Initial variables:

```text
pace
shot_duration
hold_duration
cut_interval
occupancy
scale
position
motion_amplitude
motion_velocity
motion_acceleration
visual_density
caption_density
salience
intervention_frequency
contrast
color_temperature
```

The calculus MUST account for:

- scene purpose
- content archetype
- activation meaning
- source quality
- existing visual density
- attention state
- format constraints
- Design System constraints
- continuity

The model may propose values, but deterministic code MUST validate, constrain and clamp them.

# Amendment V — Transformation Is a Projection of Meaning

Transformation is the executable projection from editorial meaning to perceptible media change.

Canonical object:

```text
TransformationIntent
```

Minimum fields:

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

```text
Meaning: prove the public claim against the source document

Grammar:
WITHHOLD → REVEAL → HOLD

Transformation:
REVEAL

Mode:
EXTRACT_REGION + HIGHLIGHT

Motion:
subtle target zoom
```

# Amendment VI — Evidence Before Synthesis

When suitable real material exists, the system SHOULD prefer:

```text
RETRIEVE
→ TRANSFORM
→ COMPOSE
→ GENERATE
```

Generation is justified when:

- no appropriate source exists;
- a conceptual visual cannot reasonably be represented by source material;
- transformation cannot express the required meaning;
- a format contract explicitly permits synthetic creation.

Synthetic material MUST remain identifiable and must not overwrite source provenance.

# Amendment VII — Source Quality Is Part of Editorial Meaning

Source quality is not merely a render parameter.

It changes the appropriate expression strategy.

A high-quality 4K/1080p source may tolerate subtle:

- zoom
- reframe
- color treatment
- LUT
- movement

without those choices becoming perceptually salient.

A 720p/480p, heavily compressed or already-cropped source may require:

- smaller visual occupancy
- inset/reaction composition
- contextual placement
- reduced scale change
- grayscale
- reduced motion
- selective framing

The correct question is:

> **What expression preserves meaning without making source limitations the thing the viewer notices?**

# Amendment VIII — Source Role Governs Treatment

Different evidence/media roles have different editorial grammars.

### A-Roll

Protect:

```text
identity
facial readability
speech continuity
natural motion
emotional credibility
```

### B-Roll / E-Roll

May express:

```text
context
association
contrast
metaphor
world-building
proof
pattern interruption
```

### Screenshot / Document

Prioritize:

```text
legibility
source authenticity
context
target region
```

### Pattern Interrupt

May use stronger visual discontinuity when justified, but it MUST still serve the scene purpose.

# Amendment IX — Attention Budget

Every intervention consumes viewer attention.

CAE SHOULD therefore evaluate:

```text
MEANING GAIN
−
EDITORIAL SALIENCE COST
−
SOURCE QUALITY LOSS
```

The intended result is:

```text
semantic attention ↑
editorial distraction ↓
```

The numeric model is initially a decision law and benchmark target, not a claim of a universal psychological constant.

# Amendment X — Motion Must Be Justified

Motion SHOULD normally be:

```text
subtle
controlled
short
purposeful
```

Motion MAY become conspicuous when conspicuousness itself is the intended function:

```text
PATTERN_INTERRUPT
DISRUPTION
SHOCK
CLIMAX
REVEAL
```

But mechanical VFX activity is never sufficient justification.

# Amendment XI — Keyframes Express Intent

Keyframes are not merely coordinates.

They are the numeric expression of transformation meaning.

```text
TransformationIntent
  ↓
MotionPlan
  ↓
Keyframes
```

A model may suggest:

> "Subtly draw attention to the highlighted number."

Code determines the valid motion path under:

- geometry
- source quality
- format
- safe areas
- Design System
- emphasis level

# Amendment XII — Storyboard Is the Transformation Design Layer

The Storyboard Program is responsible for designing how the scene's meaning should become perceptible.

A Storyboard Scene SHOULD contain:

```text
scene purpose
story function
activation meaning
source evidence
source media
editing grammar
transformation intent
transformation recipe
expression calculus
visual hierarchy
motion
constraints
```

The Storyboard exists to plan the **final hit**: the actual perceptual moment that should land with the audience.

# Amendment XIII — Format-Specific Storyboard Programs

Different media formats require different expression grammars.

```text
VideoStoryboardProgram
CarouselStoryboardProgram
SuperVisualStoryboardProgram
PresentationStoryboardProgram
```

They share the same core principles but differ in:

```text
timing
viewport
page/slide progression
spatial density
motion availability
interaction model
export constraints
```

A carousel may use storyboard planning to design only one or two critical visual transformations on selected slides and later reuse those resolved visual components in the final carousel composition.

# Amendment XIV — Visual Asset Editor Is the Workbench

The Visual Asset Editor MUST expose:

```text
source
provenance
evidence
source quality
transformation intent
recipe
composition
keyframes
preview
validation
versions
```

The operator MUST be able to:

```text
replace
edit
compare
regenerate
annotate
approve
reject
```

The operator's visual correction is authoritative for the current production revision.

# Amendment XV — Operator Feedback Becomes Institutional Memory

The operator may mark:

```text
GOOD
NEEDS_EDIT
REJECT
```

with optional notes and categories.

Those records become governed evaluation data.

They SHOULD inform:

```text
recipe quality
candidate ranking
harness refinement
visual benchmarks
future proposals
```

They MUST NOT silently rewrite canonical standards.

# Amendment XVI — Vision Supports Editing; It Does Not Own Meaning

Visual intelligence systems such as SAM3 may produce:

```text
masks
tracks
regions
subject geometry
confidence
```

They do not determine:

```text
who the subject means
why the scene exists
what the narrative should say
what the audience should believe
```

For speaker tracking, the operator may explicitly select the target subject and seed the vision model. The accepted track becomes a governed geometric input to Storyboard/BBOX/runtime.

# Amendment XVII — Final Test

Before applying a transformation, the system and operator should be able to answer:

> **What meaning does this edit make more perceptible?**

If there is no defensible answer, the transformation SHOULD NOT be applied.

The governing editorial question is not:

> **Can we animate this?**

It is:

> **Does this help the viewer perceive the intended meaning?**

# Amendment XVIII — CAE E-Motion Equation

The working doctrine is:

```text
Semantic Meaning
       ↓
Narrative Editing Grammar
       ↓
Editorial Expression Calculus
       ↓
Transformation
       ↓
Composition
       ↓
Perception
```

The objective is not maximum editing.

The objective is:

```text
MAXIMUM MEANING
with
MINIMUM UNNECESSARY EDITORIAL ATTENTION
```

That is the distinguishing standard of Conscious E-Motion Editing.

# Amendment XIX — Asset Research Is Part of Editing

Editing begins before the edit operation. Selecting the right source is itself an editorial act.

For evidence-first production, candidate retrieval SHOULD therefore be treated as part of the editing grammar:

```text
SEMANTIC NEED
   ↓
SOURCE RETRIEVAL
   ↓
CANDIDATE INSPECTION
   ↓
SELECTION
   ↓
TRANSFORMATION
   ↓
COMPOSITION
```

The operator SHOULD be able to inspect actual candidate media immediately and rapidly compare alternatives without leaving the Studio.

Automatic candidate acceptance is permitted only when a deterministic acceptance policy establishes eligibility, provenance, rights, quality and sufficient semantic fit.

# Amendment XX — Transformation Intensity Is Contextual

Transformation magnitude MUST be interpreted relative to:

```text
source quality
source role
scene purpose
content archetype
activation meaning
story position
attention state
existing visual density
format constraints
Design System
```

A transformation that is appropriate for clean 4K A-roll may be inappropriate for an already-cropped 480p source. The system must adapt the expression rather than blindly applying the same recipe.

# Amendment XXI — Composition Is a Teaching Surface

Storyboard and Visual Asset Studio are controlled environments in which operators may teach the system what successful expression looks like.

Operator judgments SHOULD be captured at the level of:

```text
source choice
transformation intent
composition
framing
visual hierarchy
attention
legibility
continuity
```

A judgment is useful when it explains not merely that an expression was bad, but **what perceptual objective it failed to achieve**.

# Amendment XXII — The Final Hit

The purpose of Storyboard is not to create a pretty preliminary image.

It is to design the final perceptual hit that will survive compilation into the target runtime.

A Storyboard element is complete when the system and operator can explain:

```text
what should be perceived
why it should be perceived
when it should be perceived
what evidence supports it
what transformation communicates it
how much transformation is justified
when the intervention should disappear
```
