# CAE PRD Update — Visual Asset Studio, Storyboard and Editorial Expression

**Document type:** Brownfield PRD update  
**Status:** Proposed / implementation-ready decomposition  
**Date:** 2026-09-10  
**Product:** Conscious Activations

# 1. PRD delta

This update adds a first-class operator production capability:

> **Evidence-First Visual Asset Studio:** a governed workspace in which the operator inspects source evidence, designs transformation intent, resolves compositions, validates visual expression, teaches the system through feedback, and compiles approved visual expressions to downstream runtimes.

The capability extends existing CAE objects rather than replacing them.

Existing canonical boundaries remain:

```text
EditorialStoryboard
        ↓
SemanticProgram
        ↓
CompositionIR
        ↓
VideoEditProgram / runtime artifact
```

The new layer adds an inspectable, editable production session around those objects.

# 2. Product goals

1. Make evidence-first visual editing faster than manual external editing.
2. Make Storyboard the active production design layer between Harness and runtime.
3. Make Transformation Intent explicit and quantifiable.
4. Allow operators to inspect, edit, replace and regenerate visual compositions.
5. Make source quality an automatic constraint on visual expression.
6. Integrate open visual intelligence, including SAM3 tracking, without moving semantic authority into the model.
7. Keep one Studio tab while allowing multiple isolated runtime processes.
8. Capture operator judgment as structured evaluation data.

# 3. Non-goals

- Do not build a generic Photoshop clone.
- Do not make AI image generation the default production path.
- Do not merge OpenChatCut, Jellyfish, Wind Comic, DramaClaw or other applications into CAE core.
- Do not create a universal media AST before concrete format contracts prove it necessary.
- Do not allow model output to mutate canonical evidence or source media.
- Do not allow runtime-specific projects to become CAE semantic authority.

# 4. Canonical user flow

```text
CAMPAIGN
  ↓
SOURCE EVIDENCE
  ↓
CONTENT / ACTIVATION CANDIDATE
  ↓
FORMAT STORYBOARD PROGRAM
  ↓
STORYBOARD SESSION
  ↓
TRANSFORMATION INTENT
  ↓
TRANSFORMATION RECIPE
  ↓
VISUAL ASSET STUDIO
  ↓
VALIDATION
  ↓
OPERATOR RESOLUTION
  ↓
EXPRESSION / COMPOSITION COMPILE
  ↓
RUNTIME
  ↓
QA
  ↓
RELEASE
```

# 5. Functional requirements

## FR-VAE-001 — Evidence-first source panel

The Visual Asset Studio MUST display, for every selected visual asset:

- source identity
- exact source range where temporal
- source timestamp where available
- source hash
- rights state
- source quality profile
- semantic role
- editorial role
- upstream evidence reference

The operator MUST be able to open the original source context without leaving the Studio.

## FR-VAE-002 — Asset replacement

The operator MUST be able to replace a visual asset with another eligible candidate without losing the semantic obligation or storyboard element identity.

The system MUST record:

- old asset
- new asset
- candidate set
- operator
- reason
- source lineage
- resulting revision

## FR-VAE-003 — Transformation Intent

Each editable visual element MUST support a typed `TransformationIntent`.

Minimum fields:

```yaml
intent:
source:
semantic_target:
mode:
emphasis:
motion:
constraints:
```

## FR-VAE-004 — Transformation Recipe

The system MUST resolve each Transformation Intent to a registered Recipe or fail closed.

An unknown transformation must not fall through to arbitrary model-generated editing.

## FR-VAE-005 — Editorial Expression Calculus

The runtime MUST expose bounded numeric parameters for:

- timing
- scale
- occupancy
- motion amplitude
- motion velocity
- salience
- density
- intervention frequency

The calculator MUST validate values against:

- source quality
- format profile
- harness
- scene archetype
- Design System
- wrong-reading locks

## FR-VAE-006 — Narrative Editing Grammar

Each format Storyboard Program MUST reference a grammar profile defining acceptable relationships between scene meaning and visual interventions.

Example:

```text
CONTRADICTION
→ WITHHOLD
→ REVEAL
→ EVIDENCE HOLD
→ RETURN
```

## FR-VAE-007 — Source quality governance

The system MUST derive a source-quality class before applying scale/reframe/motion operations.

Aggressive operations on low-quality or already-cropped sources SHOULD fail validation or force an alternate presentation strategy.

## FR-VAE-008 — Storyboard validation

Validation MUST run at the storyboard level before runtime compilation.

Checks should include:

- semantic role alignment
- source provenance
- evidence preservation
- source quality
- geometry
- safe areas
- legibility
- Design System
- visual grammar
- harness constraints
- wrong-reading locks
- transformation intensity
- continuity

## FR-VAE-009 — Visual Chat

Visual Chat MUST generate typed proposals rather than unrestricted mutation.

Allowed initial operations:

```text
propose_transform
regenerate_visual_prompt
propose_alternatives
replace_candidate
adjust_intensity
edit_layer
request_validation_explanation
```

## FR-VAE-010 — Operator visual feedback

The operator MUST be able to mark any composition or element:

```text
GOOD
NEEDS_EDIT
REJECT
```

with optional structured reason and note.

## FR-VAE-011 — Feedback lineage

Feedback MUST reference:

- storyboard revision
- element revision
- asset/source identity
- harness
- Design System version
- operator
- timestamp

Feedback MUST be append-only.

## FR-VAE-012 — SAM3 tracking session

CAE MUST support an operator-controlled tracking workflow that can:

1. choose a specific target speaker/subject;
2. seed a visual prompt;
3. run tracking;
4. review tracking;
5. revise or reject the track;
6. expose accepted track geometry to Storyboard and BBOX consumers.

## FR-VAE-013 — Runtime routing

The Studio MUST present all required engines behind one CAE origin/gateway.

The operator MUST NOT need to open separate browser tabs for OpenChatCut, presentation runtime, or visual runtime.

## FR-VAE-014 — Native editor access

For video, the operator MUST retain access to the actual OpenChatCut editing surface.

The CAE Storyboard is the planning/composition authority; OpenChatCut remains the native video editor/execution surface.

## FR-VAE-015 — SuperVisual compilation

A resolved SuperVisual storyboard element MUST compile into the existing BBOX/CompositionIR path.

The compiler MUST preserve:

- semantic role
- transformation intent
- source references
- geometry
- Design System identity/version
- wrong-reading locks
- operator revision lineage

# 6. Functional requirements — Asset Research and Surgical Integration

## FR-VAE-016 — Asset Research Session

The system MUST provide an operator-facing Asset Research Session for retrieval of evidence-grounded source media.

It MUST support:

- retrieval requests generated from semantic/storyboard needs;
- actual media preview;
- transcript/context preview;
- source timestamps/ranges;
- rights/provenance state;
- ranking/confidence;
- candidate next/previous or swipe interaction;
- explicit accept/reject;
- replace-current-asset;
- search-again;
- promotion into Storyboard/VAE.

## FR-VAE-017 — Candidate selection receipt

Every promoted candidate MUST persist:

```text
request_ref
candidate_set_ref
selected_candidate
rejected_candidates
operator_ref or auto-selection policy
source_ref
source_hash
source_range
rights_state
storyboard_element_ref
revision_ref
```

## FR-VAE-018 — Automatic candidate acceptance

The system MAY automatically accept a candidate only when a registered deterministic acceptance policy passes all required eligibility, confidence, rights, provenance and quality gates.

The automatic decision MUST be distinguishable from an operator decision.

## FR-VAE-019 — Swipe/rapid inspection mode

The candidate surface SHOULD support rapid candidate comparison, including keyboard navigation and/or swipe gestures, without opening a new browser surface.

The current candidate, source identity and selection state MUST remain synchronized with the canonical CAE state.

## FR-VAE-020 — Surgical external-component adoption

Every external repository component adopted into the Studio MUST be traceable to one or more CAE Functional Requirements.

The adoption record MUST include:

```text
repository
commit/tag
files/components inspected
license
dependencies
behavior adopted
CAE contract
known divergence
test evidence
final integration location
```

An external component MUST NOT introduce a competing semantic, state, provenance, Design System or release authority.

## FR-VAE-021 — Component-session workflow

Agents performing repository adoption MUST work in bounded sessions:

```text
PRD FR
 ↓
source mapping
 ↓
surgical implementation
 ↓
contract tests
 ↓
visual/interaction proof
 ↓
integration proposal
```

The final integration session MAY compose multiple already-proven component sessions, but it MUST NOT broaden scope without new Functional Requirements.

## FR-VAE-022 — Visual inspection feedback

Every Storyboard/VAE visual composition MUST support: `GOOD`, `NEEDS_EDIT`, `REJECT`, optional note, optional reason category, and immutable revision linkage.

## 7. Canonical domain model

```text
EditorialStoryboard
      ↓
StoryboardSession
      ↓
StoryboardRevision
      ├── Scene
      │    └── Shot
      │         └── Element
      │              ├── AssetReference
      │              ├── TransformationIntent
      │              ├── TransformationRecipe
      │              ├── MotionPlan
      │              └── Validation
      │
      └── OperatorVisualFeedback
```

This is a production-session layer; it is not permission to create a second meaning authority next to `EditorialStoryboard`.

# 8. Visual Asset Studio layout

Initial partner-ready layout:

```text
┌───────────────────────────────────────────────────────────────┐
│ STORYBOARD / CAMPAIGN                                         │
├───────────────┬─────────────────────────┬─────────────────────┤
│ SOURCE        │ COMPOSITION             │ INSPECTOR           │
│               │                         │                     │
│ evidence      │ visual canvas           │ semantic purpose    │
│ source frame  │ layers                  │ transformation      │
│ clip          │ keyframes               │ source quality      │
│ rights        │ annotations             │ BBOX                │
│ candidates    │                         │ validation          │
│               │                         │                     │
│ [replace]     │ [preview]               │ [edit]              │
├───────────────┴─────────────────────────┴─────────────────────┤
│ VISUAL CHAT                                                   │
│ "Make the evidence more prominent without making the edit    │
│  noticeable."                                                 │
├───────────────────────────────────────────────────────────────┤
│ [GOOD] [NEEDS EDIT] [REJECT] [REGENERATE] [COMPILE]         │
└───────────────────────────────────────────────────────────────┘
```

# 8. Harness relationship

Each format Storyboard Program is a projection of a Harness grammar.

The relationship is:

```text
Harness
  ↓
allowed expression grammar
  ↓
Storyboard Program
  ↓
scene-level Transformation Plans
  ↓
operator resolution
  ↓
runtime contract
```

Harnesses remain the bounded execution grammar; Storyboard is the operator-facing instantiation and refinement layer.

# 9. External repository integration contracts

### Wind Comic

Use as primary reference for:

- shot workshop
- storyboard editing
- sketch-lock
- style/consistency audit
- timeline UX
- round-trip revision
- shot regeneration

### Jellyfish

Use as primary reference for:

- WYSIWYG storyboard workspace
- shot preparation
- candidate confirmation
- reusable asset context
- production versions

### DramaClaw

Use as reference for:

- infinite canvas
- dual-track exploration vs committed production
- node history
- agent/canvas interaction
- future previz interaction

### ArcReel

Use as reference for:

- production-stage review
- user adjustment/regeneration
- timeline/canvas flow

### Seedance2

Use as reference for:

- shot grammar
- timing language
- camera grammar
- keyframe/prompt specification
- continuity vocabulary

### WaooWaoo

Use as reference for:

- assistant + canvas interaction
- reference material handling
- result refinement/versioning

### Toonflow

Use as reference for:

- structured shot vocabulary
- scene/shot metadata
- linked asset references

# 10. Acceptance tests for the first release

A first release is acceptable when an operator can:

1. open a real source-backed storyboard;
2. inspect a real image/screenshot/clip and its provenance;
3. select a scene transformation intent;
4. preview the resulting transformation;
5. change the source candidate;
6. edit the composition;
7. send a Visual Chat request;
8. receive a governed proposal;
9. mark the result GOOD / NEEDS_EDIT / REJECT;
10. compile the approved expression to SuperVisual or OpenChatCut;
11. inspect the resulting native/runtime output;
12. trace every change back to evidence and storyboard revision.

# 11. Delivery sequence

### Slice A — foundation

- storyboard session/revision objects
- TransformationIntent
- TransformationRecipe
- source quality profile
- validation contract

### Slice B — operator workspace

- visual canvas
- source panel
- inspector
- replacement UI
- feedback controls

### Slice C — deterministic expression

- BBOX integration
- motion/keyframes
- Pretext fitting
- Rough Notation primitives
- SuperVisual preview

### Slice D — intelligence

- Visual Chat
- candidate ranking
- SAM3 tracking session

### Slice E — runtime convergence

- OpenChatCut bridge
- presentation routing
- one-origin gateway
- partner-ready vertical slice

# 12. Completion definition

The capability is not complete when a visual can be generated.

It is complete when:

```text
SOURCE
→ MEANING
→ STORYBOARD
→ TRANSFORMATION
→ COMPOSITION
→ OPERATOR RESOLUTION
→ RUNTIME
→ QA
→ RELEASE
```

is executable, inspectable, deterministic where promised, and fully traceable.

## 9. External repository adoption and surgical cloning

External repositories are implementation references and, where appropriate, isolated component sources. They are not automatically adopted wholesale.

Each component adoption follows a surgical session anchored to a specific Functional Requirement:

```text
Functional Requirement
      ↓
Repository/source mapping
      ↓
License/dependency review
      ↓
Minimal component clone or behavioral reproduction
      ↓
CAE adapter/contract
      ↓
unit + integration + interaction proof
      ↓
retain upstream component OR rebuild natively
      ↓
final composition integration
```

Agents MUST keep the session narrow enough that the resulting change can be reviewed independently. The final puzzle-composition session consumes already-proven component sessions and integrates them into the canonical CAE Storyboard/VAE architecture.

The approach deliberately supports evolutionary replacement: an external component can prove a UX pattern today and be replaced later by a smaller CAE-native implementation without changing the canonical contract.

## 10. Asset Research candidate session

The Asset Research Session is a first-class part of the Visual Asset Studio. It operationalizes the PlayPhrase-like insight without creating a second retrieval authority.

The session must make candidate inspection faster than chat-only replacement:

```text
REQUEST
  ↓
CANDIDATE PORTFOLIO
  ↓
PLAYABLE PREVIEW + CONTEXT
  ↓
SWIPE / NEXT / PREVIOUS
  ↓
ACCEPT / REJECT / SEARCH AGAIN
  ↓
PROMOTE
  ↓
STORYBOARD / VAE
```

The underlying Asset Intelligence / AuthorityFirstRetrievalService remains authoritative for eligibility and retrieval. The session is the operator projection of that authority.

## 11. Final puzzle integration gate

The final integration is not the first time components are tested together. Each adopted component must first have:

- functional requirement mapping;
- source/license provenance;
- local contract tests;
- interaction or visual evidence where applicable;
- known divergence from upstream;
- clear CAE state/receipt behavior.

The final Storyboard/VAE integration then composes these proven capabilities into one Studio experience and proves one end-to-end partner-ready vertical slice.
