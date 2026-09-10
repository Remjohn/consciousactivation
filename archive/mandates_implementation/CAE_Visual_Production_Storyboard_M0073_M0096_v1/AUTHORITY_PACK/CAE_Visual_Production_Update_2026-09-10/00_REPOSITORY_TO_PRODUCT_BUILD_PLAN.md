# CAE Visual Production — Repository-to-Product Build Plan

**Status:** Proposed implementation plan  
**Date:** 2026-09-10  
**Baseline:** Conscious Activations current codebase archive + current upstream repository inspection  
**Purpose:** Freeze exactly what CAE should take from each external repository and what CAE must build natively.

## 1. Product decision

CAE will not become a generic AI image/video generation application.

The visual production method is evidence-first:

```text
RESEARCH
  ↓
EVIDENCE / SOURCE MEDIA
  ↓
SEMANTIC / ACTIVATION MEANING
  ↓
FORMAT STORYBOARD PROGRAM
  ↓
NARRATIVE EDITING GRAMMAR
  ↓
EDITORIAL EXPRESSION CALCULUS
  ↓
TRANSFORMATION INTENT
  ↓
TRANSFORMATION RECIPE
  ↓
VISUAL ASSET EDITOR
  ↓
COMPOSITION / STORYBOARD RESOLUTION
  ↓
RUNTIME ADAPTER
  ↓
OPENCHATCUT / PRESENTATION / SUPERVISUAL RUNTIME
  ↓
OPERATOR REVIEW
  ↓
HUMAN RESOLUTION
  ↓
RELEASE
```

Generation is an optional production capability after retrieval, editing and composition have been considered.

## 2. External repository adoption matrix

| Repository | Take | Do not take | Adoption mode | CAE role |
|---|---|---|---|---|
| **Wind Comic** | storyboard/shot workshop, sketch-lock idea, timeline interaction, visual/style audit patterns, character/scene consistency, round-trip storyboard editing, regeneration UX | provider/model gateway, provider-specific generation assumptions | **Reference extraction first; surgical clone only where a discrete component is useful and license-compatible** | **Primary Storyboard production reference** |
| **Jellyfish** | WYSIWYG storyboard workspace, shot preparation, candidate confirmation, asset/reuse workflow, versioned production workspace | its AI-drama domain model as CAE truth | **Reference extraction first; isolate only if code reuse is justified/licensing-safe** | **Primary Storyboard workspace reference** |
| **DramaClaw** | infinite canvas, dual-track explore/commit model, node history, canvas-agent interaction, promotion workflow, future previz interaction patterns | Enterprise/ELv2 assumptions and its full drama ontology | **Reference only unless licensing/dependency boundary is explicitly approved** | **Exploration + visual-agent interaction reference** |
| **ArcReel** | stage-based production/review/regenerate interaction, timeline/canvas production review patterns | proprietary/provider assumptions and direct architecture merge | **Reference extraction; isolate any reusable component behind adapter** | **Production review reference** |
| **Seedance2 Storyboard Generator** | shot grammar, timing, camera language, continuity/keyframe prompt structure | treating prompts as CAE authority | **Reference extraction; rebuild grammar in CAE** | **Shot-language / MotionPlan reference** |
| **WaooWaoo** | assistant + canvas workflow, references, version/refinement UX | provider-specific generation path | **Reference extraction** | **Visual assistant interaction reference** |
| **Toonflow** | structured scene/shot schema vocabulary, asset references, animation-short-drama planning | application-specific pipeline | **Reference extraction; rebuild schema in CAE** | **Storyboard schema vocabulary reference** |
| **Open Carrusel** | native carousel editing/preview, drag/reorder, exact-size export, operator surface | canonical CAE carousel authority | **Optional runtime/plugin; do not make canonical** | **Optional carousel preview/editor runtime** |
| **Slidev** | presentation runtime and preview | making Slidev the semantic source of truth | **Presentation renderer** |
| **reveal.js** | interactive presentation runtime | separate semantic presentation system | **Presentation renderer/runtime** |
| **Rough Notation** | annotation primitive usable across visual formats | making it a separate content system | **Reusable visual primitive** |
| **chenglou/pretext** | text measurement/layout | confusing it with PreTeXtBook | **Text/layout primitive inside SuperVisual** |
| **Skia** | deterministic graphics substrate | cloning full Skia unless build requirements justify it | **Low-level graphics substrate** |
| **Meta SAM3** | segmentation/tracking capability, promptable video tracking, multi-object tracking | making SAM3 the editor or source of semantic identity | **Visual Intelligence / Tracking Engine** |
| **sam3.cpp** | interactive local tracking UX/reference if technically useful | replacing the canonical Meta implementation without evaluation | **Optional local inference/runtime reference** |
| **OpenChatCut** | native video editing/timeline/runtime/MCP surface | moving CAE authority into OpenChatCut | **Canonical video execution surface** |

## 3. What CAE must build natively

### A. Storyboard domain

Create a canonical `StoryboardSession` / `StoryboardRevision` domain above the external editors.

Minimum objects:

- `StoryboardSession`
- `StoryboardScene`
- `StoryboardShot`
- `StoryboardElement`
- `TransformationIntent`
- `TransformationRecipe`
- `MotionPlan`
- `VisualAssetReference`
- `OperatorVisualFeedback`
- `StoryboardValidationReport`
- `StoryboardCompileReceipt`

The existing `EditorialStoryboard` remains the governed operator-approved narrative object. The new session/revision layer is the editable production workspace around it; it must not create a competing authority.

### B. Format-specific Storyboard Programs

Create sibling programs that share the canonical storyboard objects but implement different format grammars:

```text
VideoStoryboardProgram
CarouselStoryboardProgram
SuperVisualStoryboardProgram
PresentationStoryboardProgram
```

They compile into the same class of governed expression objects while respecting format-specific constraints.

### C. Narrative Editing Grammar

Build a small executable vocabulary for how narrative meaning becomes perceptual expression:

```text
WITHHOLD
REVEAL
FOCUS
CONTRAST
PROVE
EXPLAIN
CONNECT
ESCALATE
INTERRUPT
RESOLVE
```

The grammar describes sequencing and relational patterns; it is not a list of effects.

### D. Editorial Expression Calculus

Build deterministic numeric parameters for:

```text
pace
shot duration
hold duration
cut interval
occupancy
scale
motion amplitude
motion velocity
visual density
caption density
contrast
salience
intervention frequency
```

The calculus translates grammar into bounded values.

### E. Evidence-first Transformation system

Build the canonical transformation model:

```text
TransformationIntent
  → TransformationRecipe
  → primitive operations
  → MotionPlan / Keyframes
```

Preferred source path:

```text
RETRIEVE → TRANSFORM → COMPOSE → GENERATE (only when justified)
```

### F. Source-quality-aware editing

Add a `SourceQualityProfile` to transformation decisions.

At minimum classify:

```text
HIGH
MEDIUM
LOW
DEGRADED
```

with measurable metadata such as resolution, crop history, compression, sharpness and frame rate.

The editor should automatically reduce aggressive zoom/reframe/motion when source quality would make the manipulation visible or distracting.

### G. Visual Asset Studio

Build an operator-facing workspace with:

```text
source evidence
candidate asset preview
composition canvas
layer inspector
transform controls
keyframe controls
validation
version history
Visual Chat
operator notes
GOOD / NEEDS_EDIT / REJECT
```

The workspace must edit the governed storyboard/VAE objects rather than maintain a parallel state model.

### H. Visual Chat

Provide chat operations for:

```text
explain why this visual exists
find alternatives
replace source
regenerate transformation proposal
regenerate BBOX prompt
create three composition alternatives
reduce visual intensity
move emphasis
preserve evidence while changing presentation
```

Chat creates typed proposals. CAE validators and operator authorization decide whether those proposals are applied.

### I. SAM3 Tracking Session

Build a first-class operator-controlled tracking object:

```text
TrackingSession
TrackingTarget
TrackingPrompt
TrackSegment
TrackRevision
```

Operator can select a specific speaker/subject and seed SAM3 with a face/box/point/mask. The resulting track produces governed geometry that downstream BBOX, Storyboard and OpenChatCut can consume.

### J. Operator feedback loop

Simple first release:

```text
GOOD
NEEDS_EDIT
REJECT
```

Optional structured reason:

```text
semantic
composition
hierarchy
framing
legibility
source_quality
attention
continuity
visual_grammar
```

Store as immutable feedback records attached to storyboard revisions and expressions.

### K. Runtime topology

One CAE Studio tab; multiple local/runtime processes underneath.

```text
CAE Studio
  ↓
Studio Gateway / Runtime Registry
  ├─ CAE API
  ├─ OpenChatCut
  ├─ Presentation runtime
  ├─ SuperVisual runtime
  └─ SAM3 service
```

The browser sees one product. Engines remain isolated processes.

## 4. Surgical adaptive cloning and integration protocol

External repository adoption will happen in staged, surgical sessions. The agent MUST NOT copy an entire repository into CAE merely because the product is architecturally relevant.

For each target component:

```text
FUNCTIONAL REQUIREMENTS
        ↓
REPOSITORY FILE / COMPONENT MAPPING
        ↓
LICENSE + DEPENDENCY CHECK
        ↓
SURGICAL CLONE / ADAPTATION SESSION
        ↓
LOCAL CAE CONTRACT TEST
        ↓
INTEGRATION BRANCH / WORKTREE
        ↓
COMPOSED FINAL PUZZLE
        ↓
CAE-NATIVE REBUILD / NORMALIZATION
        ↓
FINAL INTEGRATION + CERTIFICATION
```

A surgical cloning session should have one narrowly bounded objective, such as:

- reproduce a storyboard shot-inspection interaction;
- reproduce a candidate media picker/swipe workflow;
- reproduce a canvas/node history interaction;
- reproduce a shot/timeline inspector;
- reproduce a visual audit panel;
- reproduce a reference/keyframe interaction.

The session must leave behind:

```text
source repository + commit
source files/components used
license determination
CAE adaptation contract
behavioral tests
visual/interaction evidence
known differences
replacement/rebuild plan
```

The external implementation is never itself the CAE source of truth. The final CAE-native implementation must conform to CAE contracts, state, provenance, Design System, Storyboard, Harness, validation and receipt rules.

## 5. Asset Research and Candidate Preview is a first-class production session

The Media Intelligence / PlayPhrase-like capability is not merely a backend search service. It requires an operator-facing **Asset Research Session**.

Canonical flow:

```text
semantic need
   ↓
retrieval request
   ↓
eligible candidate portfolio
   ↓
actual media preview
   ↓
operator compare / swipe / inspect
   ↓
auto-accept OR manual selection
   ↓
selected asset binding
   ↓
storyboard / VAE
```

The session MUST support:

- actual playable media previews where available;
- exact source interval and transcript context;
- rights/provenance state;
- confidence/ranking;
- candidate accept/reject;
- swipe/next/previous candidate interaction;
- replace current asset;
- search again;
- promote candidate into Storyboard/VAE;
- append-only selection receipt.

This is the CAE version of the PlayPhrase insight: **fast retrieval + immediate human inspection + governed promotion**.

The candidate picker may live inside Storyboard or Visual Asset Studio, but it must preserve the underlying Asset Intelligence retrieval contracts and must not create a parallel retrieval authority.

## 4. Explicit non-goals

Do NOT:

- merge the external repositories into one universal editor
- let external runtimes define CAE semantic meaning
- create a universal media AST before the concrete contracts prove necessary
- make image generation the default VAE path
- duplicate Asset Intelligence retrieval architecture
- duplicate `EditorialStoryboard` authority
- let model output bypass validators or operator gates
- allow visual feedback to silently rewrite production rules

## 6. First partner-ready vertical slice

The fastest high-value demonstration is:

```text
authenticated interview evidence
        ↓
selected source image / screenshot / clip
        ↓
VideoStoryboardProgram or SuperVisualStoryboardProgram
        ↓
TransformationIntent = REVEAL / FOCUS / CONTRAST
        ↓
TransformationRecipe
        ↓
SAM3 speaker/subject track when needed
        ↓
BBOX composition
        ↓
Visual Asset Studio preview
        ↓
operator edits / GOOD / NEEDS_EDIT
        ↓
compile
        ↓
OpenChatCut native timeline or SuperVisual render
        ↓
release-ready artifact + receipt
```

This demonstrates CAE's actual differentiation: source-grounded research, semantic intent, controlled transformation, operator teaching, deterministic composition, and native production execution.

## 7. Source links

- Wind Comic: https://github.com/ChrisChen667788/wind-comic
- Jellyfish: https://github.com/Forget-C/Jellyfish
- DramaClaw: https://github.com/dramaclaw/dramaclaw
- ArcReel: https://github.com/ArcReel/ArcReel
- Seedance2 Storyboard Generator: https://github.com/liangdabiao/Seedance2-Storyboard-Generator
- WaooWaoo: https://github.com/waoAI/waoowaoo
- Toonflow: https://github.com/HBAI-Ltd/Toonflow-app
- Open Carrusel: https://github.com/Hainrixz/open-carrusel
- Slidev: https://github.com/slidevjs/slidev
- reveal.js: https://github.com/hakimel/reveal.js
- Rough Notation: https://github.com/rough-stuff/rough-notation
- Pretext: https://github.com/chenglou/pretext
- Skia: https://github.com/google/skia
- SAM3: https://github.com/facebookresearch/sam3
- sam3.cpp: https://github.com/PABannier/sam3.cpp
- OpenChatCut: https://github.com/0xsline/OpenChatCut
