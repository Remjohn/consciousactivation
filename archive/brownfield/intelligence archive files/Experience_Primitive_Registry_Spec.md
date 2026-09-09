---
type: registry-spec
author: Codex synthesis for CCP
date: 2026-05-05
status: Source of Truth Draft
dependencies:
  - D:\Work\The Conscious Coaching Factory\lab\CCP APRIL Updates\Conscious_Reactions_Source_of_Truth.md
  - D:\Work\The Conscious Coaching Factory\lab\CCP APRIL Updates\Conscious_Reactions_Experience_Primitive_Orchestration_Architecture.md
---

# Experience Primitive Registry Spec

## 1. Purpose

This document defines the registry rules for `experience primitives`.

These are the primitives written for product implementation.

Their job is to shape:

- trigger timing
- onboarding
- score reveals
- sharing loops
- comeback behavior
- retention
- conversion
- premium trust
- mini app flow

They are not primarily for steering model outputs.
They are primarily for steering user behavior and user state.

That means this registry is built for:

- tech specs
- UI / UX states
- Telegram flow design
- React component behavior
- notification rules
- scoring moments
- telemetry and experimentation

## 2. The Core Difference from Meaning Primitives

Meaning primitives ask:

- what should the content say?
- what structure should be activated?
- what truth or tension should be extracted?

Experience primitives ask:

- why should the coach enter right now?
- does this feel obvious and safe enough to try?
- does the score feel meaningful?
- does the share feel socially natural?
- does the user come back tomorrow?

So this registry must optimize for:

- adoption acceleration
- reduction of confusion
- reduction of hesitation
- emotional readiness
- social propagation
- continuity

## 3. Required Metadata

Every experience primitive entry should include its audit scores for fast scanning.

```yaml
experience_primitive_id: string
canonical_name: string
aliases: [string]

experience_family: enum[
  trigger_timing,
  friction_ability,
  trust_branding,
  feedback_scoring,
  progression_replay,
  social_referral,
  safe_failure_recovery,
  personalization_identity
]

mechanic_role: enum[
  loop,
  state,
  moment,
  accent,
  safeguard
]

moment_role: enum[
  notification,
  topic_brief,
  entry,
  record,
  score_reveal,
  share_prompt,
  comeback,
  challenge_transition,
  continuity,
  upgrade
]

source_audits: [string]
source_mcda_scores:
  - audit: string
    primitive_name: string
    score_200: integer

summary: string
core_move: string
why_it_works: string

experience_stage_fit:
  entry: float
  activation: float
  recording: float
  scoring: float
  social_spread: float
  recovery: float
  retention: float
  conversion: float

surface_fit:
  telegram_message: float
  mini_app: float
  score_card: float
  share_asset: float
  voice_prompt: float
  push_nudge: float

user_state_effects:
  confidence: float
  urgency: float
  clarity: float
  safety: float
  status: float
  belonging: float
  curiosity: float
  replay_desire: float

activation_conditions: [string]
suppression_conditions: [string]
misuse_modes: [string]
synergizes_with: [string]
conflicts_with: [string]

experience_metrics:
  entry_rate: float
  react_rate: float
  completion_rate: float
  share_rate: float
  comeback_rate: float
  day7_retention: float
  upgrade_signal: float

implementation_targets:
  frontend_components: [string]
  backend_rules: [string]
  telemetry_events: [string]
  experiments: [string]

notes: string
```

The key scanning rules are:

- always show `source_mcda_scores`
- list representative examples in descending original audit `MCDA` order whenever possible
- do not confuse low score with low importance if the primitive is a safeguard, accent, or moment-shaper

## 4. The Eight Registry Families

### 4.1 Trigger and Timing

Examples with source scores:

- `First Major Win-State Before Social Expansion` - `197`
- `Context-Aware System Triggers` - `170`
- `Contextual Timing Triggers` - `140`

### 4.2 Friction and Ability

Examples:

- `Evolved UI + Glowing Choice` - `191`
- `System 1 to System 2 Escalation` - `175`
- `The B=MAP Friction Audit` - `175`
- `Friction-Zero Ability` - `160`

### 4.3 Trust and Premium Branding

Examples:

- `Perception and Behavioral Guidance as a Unified Stack` - `199`
- `Design for Lived Use, Not Abstract Intent` - `194`
- `Placebo Onboarding` - `180`
- `Visceral Hooking` - `175`
- `The Trust Architecture` - `170`

### 4.4 Feedback and Scoring

Examples:

- `RIM Feedback Discipline` - `180`
- `Reflective Scoring` - `175`
- `The Signature Moment` - `170`
- `Bring the Data Forward` - `170`

### 4.5 Progression and Replay

Examples:

- `Hook Cycle Velocity` - `185`
- `Discover -> On-board -> Immerse -> Master -> Replay` - `178`
- `Go for an Epic Win` - `160`
- `Long Loops for Habit Formation` - `145`

### 4.6 Social Referral and Status

Examples:

- `Social Treasures + Group Quests` - `194`
- `Social Capital and Self-Esteem Economy` - `186`
- `Identity-Driven Social Proof` - `180`
- `Balanced Social Status Architecture` - `176`

### 4.7 Safe Failure and Recovery

Examples:

- `White Hat -> Black Hat -> White Hat Emotional Sequencing` - `196`
- `Possible-Win Scarcity` - `186`
- `Hypnosedation Reframing` - `185`
- `Practical Play / Safe Failure` - `168`
- `Behavioral Forgiveness` - `160`

### 4.8 Personalization and Identity

Examples:

- `Monitor Attachment + Alfred Personalization` - `193`
- `Adopt a Secret Identity` - `175`
- `Cumulative Investment` - `165`
- `Tailoring & Suggestion` - `165`

## 5. Cross-Shelf Contributions to the Experience Layer

The experience registry should not be built from `09_Experience_Engineering` alone.

Other shelves also matter because the coach does not experience only gamification.
They experience:

- humor
- performance
- story
- brand taste
- visual composition
- sonic texture
- psychological safety

### 5.1 Humor and Comedy

Representative carryovers:

- `Hyper-Specificity Anchoring` - `195`
- `The Mix` - `191`
- `Directed Emotional Stance` - `190`

Experience role:

- stronger, more human topic briefs
- anti-generic delivery feeling
- better social shareability
- better reaction energy

### 5.2 Acting and Performance

Representative carryovers:

- `Superobjective` - `194`
- `Magic As If / Particularization` - `192`
- `Pinch and Ouch` - `190`
- `Preparation / Pre-State Self-Stimulation` - `184`

Experience role:

- better voice-note preparation
- better guided delivery states
- stronger reaction confidence

### 5.3 Public Speaking and Presentations

Representative carryovers:

- `Throughline as Structural Anchor` - `196`
- `Big Idea Formulation Protocol` - `192`
- `Connection Before Content` - `190`
- `Explanation Engine` - `182`

Experience role:

- clearer topic rooms
- better brief sequencing
- better score explanation language

### 5.4 Storytelling and Narrative Design

Representative carryovers:

- `Perception and Behavioral Guidance as a Unified Stack` - `199`
- `Emotional Journey Mapping and Peak-End Memory` - `196`
- `Change Choreography` - `194`
- `DataPOV as the Narrative Spine` - `192`

Experience role:

- better onboarding arc
- better reaction-to-share journey
- better challenge continuation design

### 5.5 Psychology and Communication

Representative carryovers:

- `Identification Builds the Bridge` - `196`
- `Matching Principle` - `192`
- `Looping for Understanding` - `192`
- `Deep Questions` - `190`

Experience role:

- better agent replies
- better supervisor pairing behavior
- better recovery messages

### 5.6 Design and Business

Representative carryovers:

- `Perception and Behavioral Guidance as a Unified Stack` - `199`
- `Design for Lived Use, Not Abstract Intent` - `194`
- `FEPS Benefit Translation` - `194`
- `Hierarchy as Semantic Attention Routing` - `192`
- `Dignity Reduces Friction Better Than Force` - `189`

Experience role:

- better premium trust architecture
- clearer action prompts
- better conversion framing

### 5.7 Photography and Composition

Representative carryovers:

- `Composition is Eye-Path Engineering` - `198`
- `Intent Should Govern Style, Not the Reverse` - `196`
- `Visual Emphasis Must Be Intentional` - `196`
- `Order Must Be Imposed on Chaos` - `194`

Experience role:

- better score-card hierarchy
- better share-card salience
- better topic-brief composition

### 5.8 Sound Design

Representative carryovers:

- `Workflow Creates Aesthetics` - `198`
- `Write for the Distracted Ear` - `197`
- `Audience-of-One Intimacy` - `196`
- `Silence as a Positive Narrative Device` - `196`
- `Polyphony and Controlled Density` - `195`

Experience role:

- better sonic trust
- better reaction pacing
- better voice-note legibility

### 5.9 Experience Engineering

Experience-first anchors:

- `First Major Win-State Before Social Expansion` - `197`
- `White Hat -> Black Hat -> White Hat Emotional Sequencing` - `196`
- `Social Treasures + Group Quests` - `194`
- `Monitor Attachment + Alfred Personalization` - `193`

Meaning carryover:

- helps sequence content modes
- helps structure debate, jury, and replay loops

## 6. What Belongs Here

### Yes, include:

- onboarding mechanics
- score reveal behavior
- comeback and redemption logic
- share prompts
- replay triggers
- premium trust cues
- mini app friction reducers
- identity and continuity mechanics

### No, do not flatten here:

- content-only rhetorical structures
- hook formulas that do not alter product behavior
- explanation patterns that only influence script logic
- coalition-only meaning moves

Those belong in the meaning registry unless they clearly alter experience flow.

## 7. Implementation Rule

The experience registry should optimize for:

- adoption acceleration
- state change
- replay behavior
- conversion continuity
- social propagation
- trust preservation

So when uncertain between registries, ask:

- is this primitive mainly changing user behavior, state, or flow?
- does it belong in product specs, triggers, UI logic, telemetry, or experimentation?

If yes, it belongs here.

## 8. First Build Order

### Wave 1 - Adoption Baseline

- `First Major Win-State Before Social Expansion`
- `Design for Lived Use, Not Abstract Intent`
- `RIM Feedback Discipline`
- `Audience-of-One Intimacy`
- `Write for the Distracted Ear`

### Wave 2 - Spread and Continuity

- `Social Treasures + Group Quests`
- `Social Capital and Self-Esteem Economy`
- `Hook Cycle Velocity`
- `Possible-Win Scarcity`
- `Monitor Attachment + Alfred Personalization`

### Wave 3 - Premium Differentiation

- `Perception and Behavioral Guidance as a Unified Stack`
- `Composition is Eye-Path Engineering`
- `Polyphony and Controlled Density`
- `Silence as a Positive Narrative Device`
- `Reflective Scoring`

## 9. Final Position

The experience registry should be read as:

- the product-behavior companion to the meaning registry
- the technical-spec layer for adoption, trust, replay, and social spread
- the implementation vocabulary for making Conscious Reactions, CBCS, and challenge flows actually used

The product moat is not only that the system works.
It is that the user wants to come back, wants to keep going, and wants to bring others in without needing the product explained to them every time.
