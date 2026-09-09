---
type: registry-spec
author: Codex synthesis for CCP
date: 2026-05-05
status: Source of Truth Draft
dependencies:
  - D:\Work\The Conscious Coaching Factory\lab\CCP APRIL Updates\Primitive_Packets_and_Registry_Spec.md
  - D:\Work\The Conscious Coaching Factory\lab\CCP APRIL Updates\Primitive_Conscious_Orchestration_Architecture.md
  - D:\Work\The Conscious Coaching Factory\lab\CCP APRIL Updates\Primitive_Family_Classification_CCP_CMF.md
---

# Meaning Primitive Registry Spec

## 1. Purpose

This document defines the registry rules for `meaning primitives`.

These are the primitives written for:

- research extraction
- prompt steering
- coalition formation
- routing
- validation
- fine-tuning preparation
- transformer-facing output control

This registry exists to help CCP answer:

- what signal is present?
- what meaning move should be activated?
- what coalition should guide generation?
- what output quality should be validated?

This is not the registry for UI flow, onboarding, trigger timing, score reveal behavior, or social loop implementation.

Those belong in:
[Experience_Primitive_Registry_Spec.md](</D:/Work/The Conscious Coaching Factory/lab/CCP APRIL Updates/Experience_Primitive_Registry_Spec.md>)

## 2. Implementation Target

Meaning primitives are built for model and content systems.

Their implementation targets are:

- prompt structures
- DSPy / typed planning layers
- primitive coalition planners
- routing validators
- steering logic
- receipts
- training / fine-tuning datasets
- benchmarking against content outputs

So when we write a meaning primitive, we should ask:

- can this be activated intentionally?
- can it be measured in output?
- can it be routed with others?
- can it eventually become transformer-facing structure?

## 3. Required Metadata

Every meaning primitive entry should store its audit scores explicitly so the registry stays skimmable.

```yaml
primitive_id: string
canonical_name: string
aliases: [string]
family: enum[
  psychological_diagnostics,
  connection,
  contrast,
  humor_distortion,
  performance_delivery,
  persuasion,
  narrative_structure,
  story_discovery,
  explanation_translation,
  visual_sonic_guidance
]

source_audits: [string]
source_mcda_scores:
  - audit: string
    primitive_name: string
    score_200: integer

summary: string
core_move: string
why_it_works: string

phase_fit:
  pre_trigger: float
  post_trigger: float
  generation: float
  revision: float
  delivery: float

surface_fit:
  text: float
  voice: float
  visual: float
  sonic: float
  webinar: float
  telegram: float

goal_bias:
  connection: float
  surprise: float
  tension: float
  clarity: float
  memorability: float
  persuasion: float

trigger_conditions: [string]
suppression_conditions: [string]
misuse_modes: [string]
synergizes_with: [string]
conflicts_with: [string]

notes: string
```

The most important scanning rule is simple:

- always show `source_mcda_scores`
- list representative examples in descending original audit `MCDA` order whenever possible

## 4. What Belongs Here

### Yes, include:

- humor structures
- narrative structures
- performance and delivery moves
- explanation patterns
- visual and sonic meaning controls
- psychological diagnostics
- persuasion architectures

### No, do not flatten here:

- zero-thought onboarding
- trigger timing nudges
- signature score reveal behavior
- social sharing defaults
- redemption UI state logic
- micro-feedback gestures

Those are real primitives, but they are not meaning primitives.

## 5. Shelf-to-Registry Emphasis

The audit shelves still matter even when the registry is meaning-first.

## 5.1 Humor and Comedy

Representative high-value meaning primitives:

- `Hyper-Specificity Anchoring` - `195`
- `The Mix` - `191`
- `Directed Emotional Stance` - `190`
- `Setup-Premise-Payoff` - `185`

Why they belong here:

- they sharpen output distinctiveness
- reduce genericity
- create pattern breaks in generated content

## 5.2 Acting and Performance

Representative primitives:

- `Superobjective` - `194`
- `Magic As If / Particularization` - `192`
- `Pinch and Ouch` - `190`
- `Backstory Architecture` - `189`

Why they belong here:

- they govern how generated content is emotionally grounded
- they help voice, rehearsal, performance steering, and believable delivery

## 5.3 Public Speaking and Presentations

Representative primitives:

- `Throughline as Structural Anchor` - `196`
- `Big Idea Formulation Protocol` - `192`
- `Connection Before Content` - `190`
- `Explanation Engine` - `182`

Why they belong here:

- these are direct content-quality and delivery-architecture primitives

## 5.4 Storytelling and Narrative Design

Representative primitives:

- `Perception and Behavioral Guidance as a Unified Stack` - `199`
- `Emotional Journey Mapping and Peak-End Memory` - `196`
- `Change Choreography` - `194`
- `DataPOV as the Narrative Spine` - `192`

Why they belong here:

- they govern information arc, emotional movement, sequencing, and memory

## 5.5 Psychology and Communication

Representative primitives:

- `Identification Builds the Bridge` - `196`
- `Matching Principle` - `192`
- `Looping for Understanding` - `192`
- `Deep Questions` - `190`

Why they belong here:

- these are upstream diagnosis and communication-architecture primitives

## 5.6 Design, Photography, and Sound

These shelves belong here when they influence meaning and perceptual direction, not when they only define interface behavior.

Representative primitives:

- `Composition is Eye-Path Engineering` - `198`
- `Workflow Creates Aesthetics` - `198`
- `Write for the Distracted Ear` - `197`
- `Visual Emphasis Must Be Intentional` - `196`
- `Hierarchy as Semantic Attention Routing` - `192`

Why they belong here:

- they help generated assets carry clearer meaning
- they improve attention control inside outputs
- they reduce anti-slop drift across visual and sonic layers

## 6. Implementation Rule

The meaning registry should optimize for:

- control
- steerability
- coalition compatibility
- validation readiness
- training usefulness

So when uncertain between registries, ask:

- is this primitive mainly changing what the output means?
- is it helping a model or planner choose, route, compress, reveal, or emphasize meaning?

If yes, it belongs here.

## 7. Relationship to the Packet Layer

This registry is the meaning-side companion to:

- `PrimarySignalPacket`
- `PrimitiveCandidatePacket`
- `CoalitionSignature`
- `EdgeProductPacket`
- `CCFRoutingRecommendation`

The packet layer handles runtime objects.
The meaning registry handles reusable meaning units and their metadata.

## 8. Final Position

The meaning registry should be read as:

- a scan surface for high-value content primitives
- a steering vocabulary for generation systems
- a routing vocabulary for coalition logic
- a validation vocabulary for future benchmark and fine-tuning work

If a primitive is not useful for steering, routing, validating, or training, it probably belongs somewhere else.
