---
type: modular-prd
module: PRD-08
title: Conscious Primitives — Registry, Coalition, and Orchestration
author: John (Product Manager)
date: 2026-05-06
status: Source of Truth
version: 6.0
dependencies:
  - docs/prd/prd.md (Foundation PRD — FR-GA, CA-0, CA-2)
  - docs/prd/modules/PRD_INDEX.md
  - docs/prd/modules/PRD_01_CCP_Platform_Strategy.md
source_documents:
  - lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md
  - lab/CCP APRIL Updates/05_Core_Experience/Primitive_Conscious_Orchestration_Architecture.md
  - lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md
  - lab/CCP APRIL Updates/05_Core_Experience/Primitive_Family_Classification_CCP_CMF.md
  - lab/CCP APRIL Updates/05_Core_Experience/Primitive_Packets_and_Registry_Spec.md
  - lab/CCP APRIL Updates/05_Core_Experience/Meaning_Primitive_Registry_Spec.md
  - lab/CCP APRIL Updates/05_Core_Experience/Experience_Primitive_Registry_Spec.md
  - lab/CCP APRIL Updates/05_Core_Experience/Primitive_Crosswalk_Map.md
  - lab/CCP APRIL Updates/05_Core_Experience/Conscious_Reactions_Experience_Primitive_Orchestration_Architecture.md
  - lab/CCP update/CCP_Architecture_V5.0.docx.md
  - lab/CCP update/CCP_Evolution_Architecture_Report_V2.docx.md
  - lab/CCP update/CCP_Script_Generation_Skill_Type_Guide_v1.0.docx.md
  - lab/Public Speeaking Coaching/Primitive Biology Architecture.md
active_primitives:
  meaning_plane: [STR, PRS, HUM, CON, PSY, VOC, VSG, ACT, REF, BUS]
  experience_plane: [TRG, FRC, FBK, PRG, SAF, PER, SOC, TRB]
capability_areas: [CA-0, CA-2, FR-APR-08, FR-GA]
---

# PRD-08: Conscious Primitives — Registry, Coalition, and Orchestration

**Version:** 6.0 | **Status:** Source of Truth | **Date:** 2026-05-06

---

## 1. The Architectural Claim

CCP content becomes non-generic not through better prompts but through better internal perception. The platform needs a richer language for deciding what to notice, what to amplify, what to withhold, and how to shape resonance at the moment of execution.

Primitives are that language. They are not decorative labels, prompt tips, or content categories. They are **conscious faculties** — stable transformation operators that can be activated, measured, combined, suppressed, and validated in context. A primitive like "Irony Inversion" does not describe a writing trick. It describes a repeatable perceptual operation: detect where stated position and lived behavior diverge, invert the expectation, and produce recognition through surprise.

This module defines how primitives are structured, how they form coalitions, how they survive candidate selection, and how they govern content generation across all CCP execution environments. Every content pipeline — CCF scripts, CMF visuals, CBCS coaching notes, Conscious Reactions scoring, V2WS webinar slides — draws from this registry as its meaning and experience intelligence layer.

---

## 2. The Meaning/Experience Plane Separation

### 2.1 Why Two Planes

All CCP intelligence operates across two distinct architectural planes. This separation prevents the most common failure mode in coaching platforms: conflating *what to teach* with *how to deliver it*.

**Meaning Plane (Plane A)** governs the coaching ontology — cognitive truth, moral truth, transformation operators, narrative structure, persuasion mechanics, humor theory, psychological diagnostics, voice craft. It answers: *What does the coach mean? What truth is present? What transformation is possible? What makes this expression distinctive rather than generic?*

**Experience Plane (Plane B)** governs the delivery layer — trigger design, friction management, feedback loops, progression systems, safety signals, personalization, social dynamics, tribal identity. It answers: *How does the user encounter the meaning? What emotional and behavioral journey do they follow? Why do they come back tomorrow?*

A primitive like "Superobjective" (meaning: the character's deepest want driving every action) is not the same as "Variable Reward Schedule" (experience: unpredictable positive feedback to sustain engagement). They operate on different inputs, produce different outputs, and are validated by different standards. The registries, schemas, and validation pipelines are therefore separate.

### 2.2 The 18-Family Classification

| Plane | Code | Family Name | Count | Primary Environment |
|---|---|---|---|---|
| Meaning | **STR** | Narrative Structure | 27 | CCF, CMF |
| Meaning | **PRS** | Persuasion | 35 | CCF, V2WS |
| Meaning | **HUM** | Humor & Distortion | 12 | Conscious Reactions, CCF |
| Meaning | **CON** | Contrast & Juxtaposition | 8 | CCF, CMF |
| Meaning | **PSY** | Psychological Diagnostics | 12 | CBCS, Law28 |
| Meaning | **VOC** | Voice & Audio Intimacy | 12 | Voice Notes, CMF Sonic |
| Meaning | **VSG** | Visual & Sonic Guidance | 12 | CMF, CVE |
| Meaning | **ACT** | Performance & Delivery | 10 | Law28, Conscious Reactions |
| Meaning | **REF** | Referral & Trust-Transfer | 9 | CPSC, Silent Referral |
| Meaning | **BUS** | Design & Business | 14 | Dashboard, V2WS |
| Experience | **TRG** | Trigger & Hook Design | — | All surfaces |
| Experience | **FRC** | Friction & Flow Management | — | Telegram UX |
| Experience | **FBK** | Feedback & Scoring | — | Law28, Conscious Reactions |
| Experience | **PRG** | Progression & Mastery | — | Challenge System |
| Experience | **SAF** | Safety & Trust Signals | — | CBCS, Onboarding |
| Experience | **PER** | Personalization & Adaptation | — | Voice DNA, Context Premise |
| Experience | **SOC** | Social & Community Dynamics | — | Conscious Reactions, Co-Creation |
| Experience | **TRB** | Tribal Identity & Belonging | — | CPSC, Silent Referral |

### 2.3 The Crosswalk Layer

Some primitives straddle both planes. The Crosswalk Map handles these: it identifies which meaning primitives have experience-plane implications and vice versa, ensuring that orchestration respects both dimensions without creating false duplication. For example, "Audience-of-One Intimacy" (VOC meaning) has direct implications for "Personalization & Adaptation" (PER experience). The crosswalk ensures both are activated together when the context demands it.

---

## 3. The Primitive Registry Schema

### 3.1 Meaning Primitive Schema (v2.0)

Every meaning primitive is codified as a YAML artifact following this schema:

```yaml
primitive_id: "PRM-{FAMILY}-{NNN}"
primitive_name: "Human-readable name"
family: "{FAMILY_CODE}"
version: "2.0"
source_literature:
  book_title: "Source book"
  author: "Author name"
  audit_file: "Path to audit"
definition: "Dense 2-3 sentence mechanistic definition"
mechanistic_analysis: "How and why this primitive works"
coaching_application: "How a CCP coach deploys this in practice"
coalition_partners:
  synergistic: ["PRM-XXX-NNN"]
  antagonistic: ["PRM-XXX-NNN"]
geometry:
  intensity: 0.0-1.0
  complexity: 0.0-1.0
  emotional_valence: -1.0 to 1.0
  # ... family-specific float dimensions
workflow_integration:
  primary_environment: "CCF | CMF | CBCS | V2WS | Reactions"
  trigger_conditions: "When to activate"
  anti_patterns: "When NOT to use"
evidence_fidelity:
  audit_source: "Verified audit reference"
  book_reference: "Direct page/chapter reference"
  dual_source_validated: true
```

### 3.2 Basis Definitions: The Math Before the Primitive

Basis should be defined before full primitive formalization. Without basis we do not know what independence, magnitude, or valid range means. There are two layers of basis.

**Universal Effect Basis.** The shared human-state space that all primitives project into. These are the universal constants of the system because they describe the core directions of psychological effect across surfaces:

| Axis | What It Measures |
|---|---|
| Attention | Did the output change what the person notices? |
| Trust | Did the output increase or decrease felt safety? |
| Belonging | Did the output create felt connection to a group or person? |
| Surprise | Did the output violate expectation meaningfully? |
| Tension | Did the output create live pressure that demands resolution? |
| Clarity | Did the output make understanding easier or harder? |
| Emotional Intensity | How strongly did the output move feeling? |
| Memorability | Will this output be recalled unprompted? |
| Agency | Did the output increase felt power over next action? |
| Action Readiness | Is the person closer to doing something specific? |
| Ethical Risk | Could this output cause harm, manipulation, or coercion? |

**Family-Local Basis.** Each primitive family gets its own vector space with family-specific dimensions:

- **Visual (VSG):** density, contrast, focal priority, scan path, negative space
- **Sonic (VOC):** silence, layer density, dynamic range, motif recurrence, auditory POV
- **Narrative (STR):** gap strength, escalation force, turn force, closure quality, peak intensity
- **Conversational (PSY):** intimacy load, reflection depth, challenge force, containment, reciprocity
- **Humor (HUM):** absurdity magnitude, target precision, recovery speed, shared reference density
- **Persuasion (PRS):** credibility weight, urgency pressure, emotional leverage, logical coherence

Primitives then become operators defined inside local spaces that also project into the Universal Effect space. This lets us preserve detail without forcing every primitive into one giant flat vector model.

SDA adds a deeper distinction that should remain explicit:

- `Invariant Gravity` is a property of the existential invariant itself and belongs to the semantic ontology, not the primitive registry
- `Invariant Activation Intensity` is a runtime measure of how strongly a specific artifact activates that invariant
- `Invariant Resonance Multiplier` is a runtime measure of how much the active invariant amplifies emotional charge, personal relevance, symbolic density, and memory persistence when combined with the current coalition, edge product, geometry, and surface

These three concepts must not be collapsed into one generic "importance" field. They measure different things and belong to different architectural layers.

### 3.3 Experience Primitive Schema

Experience primitives follow a parallel schema but with behavioral field signatures:

```yaml
primitive_id: "EXP-{FAMILY}-{NNN}"
primitive_name: "Human-readable name"
family: "{FAMILY_CODE}"
behavioral_trigger:
  trigger_type: "time | action | state | social | absence"
  context_conditions: "When this trigger should fire"
  minimum_ability_threshold: "What the user must be able to do"
  motivation_requirement: "What emotional state enables this"
friction_design:
  entry_friction: 0.0-1.0   # lower = easier to start
  exit_friction: 0.0-1.0    # higher = harder to leave
  cognitive_load: 0.0-1.0   # working memory demand
reward_architecture:
  reward_type: "fixed | variable | social | achievement"
  reward_schedule: "immediate | delayed | intermittent"
  investment_ratio: "effort-in vs value-out"
safety_signals:
  failure_tolerance: 0.0-1.0  # how safe failure feels
  recovery_path: "How the system helps after failure"
  dignity_preservation: "How the system avoids shame"
progression_gate:
  prerequisite: "What must be completed first"
  biometric_threshold: "Score required to advance"
```

### 3.4 The Dual-Source Requirement

No primitive may be codified without **two verified sources**: the audit file (which synthesizes the book into CCP-actionable intelligence) and the direct book reference. This eliminates synthetic hallucination at the registry level. If a primitive cannot cite two real sources, it does not enter the registry. This is the anti-slop gate for the intelligence layer itself.

### 3.5 Upstream Intelligence Dependencies

Primitives do not operate in a vacuum.

The registry is not the first layer of intelligence in CCP. It is a transformation layer that depends on several retained upstream structures:

- **Client Intelligence Layer**
- **Cultural Memory Map**
- **Coach Story Archive**
- **Context Performance Registry**
- **Context Reasoning**
- **Semantic Affinity Guard**
- **Audience Maturity routing**

These are not themselves primitives. They are context substrates and routing constraints that determine which primitives should activate, which should be suppressed, and what kind of coalition is actually admissible.

If PRD-08 ignores those substrates, the primitive layer becomes abstract and overconfident.

### 3.6 Relationship to the Semantic Discernment Architecture

The Semantic Discernment Architecture (`SDA`) introduces a deeper semantic layer that must remain structurally distinct from the primitive registries.

The key rule is:

**primitives are not the deepest ontology.**

Primitives remain:

- transformation operators
- perception labs
- candidate generators
- coalition participants

SDA contributes the semantic structures that primitives operate over and the validator structures that later evaluate directional integrity.

This means SDA artifacts are **not** new primitive families.
They are a sibling intelligence stack with different roles and therefore different schemas, governance rules, and runtime behaviors.

The minimum SDA taxonomy relevant to PRD-08 is:

- **Canonical ontology**
  - `Existential Invariants`
  - `Representation Geometries`
- **Canonical structural grammar**
  - `Archetypal Geometries`
  - `Species Composition Grammar`
- **Runtime-derived semantic forms**
  - `Content Species`
  - `Edge Products`
- **Runtime semantic dynamics**
  - `Recursive Patterns`
  - `Emergent Contextual Invariants`
  - `Feedback Loops`
- **Validation policies**
  - `Directional Integrity Policies`
  - `Semantic Discernment Evaluation Policies`
- **Adversarial evaluation assets**
  - `Hard Negative Corpus`
  - `Mutation Stress Suites`
- **Execution packets**
  - `InvariantFieldPacket`
  - `ArchetypalGeometryPacket`
  - `RepresentationGeometryPacket`
  - `SpeciesHypothesisPacket`
  - `DirectionalIntegrityReport`
  - `HardNegativeEvaluationReport`

The practical division of labor is:

- if the artifact defines a **transformation operator**, it belongs to the Primitive Registry
- if the artifact defines a **deep semantic field**, **structural topology**, **directional encoding**, or **adversarial semantic validator**, it belongs to SDA
- if the artifact measures **how much force an invariant is carrying in the current composition**, it belongs to SDA runtime evaluation rather than primitive codification

The resulting stack is:

`context substrate -> SDA field -> primitive candidate field -> coalition -> archetype container -> SDA validation -> destination packet`

Under the biological orchestration model, primitives occupy the **force layer** of the organism.

That means:

- `SDA`, Voice DNA, and Negative Space define the deeper truth substrate
- primitives apply force over the currently active field
- `SFL` and downstream composition logic determine how that force is felt
- variation logic later determines whether the result remains alive, asymmetric, and memorable

So primitives are not the whole organism.
They are the muscular system inside it.

This clarifies five important non-negotiables:

1. `Existential Invariants` are not meaning primitives.
2. `Archetypal Geometries` are not content archetypes.
3. `Hard Negatives` are not prose descriptions of bad content; they are contrastive evaluation assets.
4. `Recursive Patterns`, `Emergent Contextual Invariants`, and `Feedback Loops` are runtime semantic-dynamics objects, not codified primitive families.
5. Primitive activation may consult SDA artifacts, but primitive codification must not absorb them into the registry as if they were interchangeable units.

One practical implication is especially important for future evaluation:

- `Invariant Gravity` should be stored on canonical SDA ontology objects
- `Invariant Activation Intensity` should be emitted in runtime packets such as `InvariantFieldPacket`
- `Invariant Resonance Multiplier` should be emitted in runtime reports such as `DirectionalIntegrityReport` or species-level evaluation outputs

This preserves the difference between what an invariant is, how present it is, and how much force it is amplifying.

For interpretive reference only, theology-to-architecture worked examples are maintained in:

`lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` Appendix A

---

## 4. Primitives Are Not Edges

### 4.1 The Core Ontological Correction

The most important architectural correction in the April–May rewrite is this: **primitives are not edges.** This distinction governs the entire orchestration pipeline.

Primitives are:
- encoded meaning spaces
- transformation operators
- perception labs
- candidate generators

Edges are emergent products that arise when primitive outputs interact with real CRAL evidence and authenticated coach response. The correct hierarchy is:

```
CRAL evidence → primitive spaces → candidate survival → coalition signature → edge product → CCF routing
```

When SDA is active, the fuller hierarchy becomes:

```
CRAL evidence → invariant field → primitive spaces → candidate survival → coalition signature → edge product → archetype container → directional integrity validation → CCF routing
```

If we mistake edges for primitives, we get false coalitions and weak measurement. The difference is between basis, composition, and emergence.

### 4.2 The Two Edge Phases

The system explicitly distinguishes two edge moments:

**Phase A: Pre-Trigger Broad Signal.** Before the coach inbox. Its job is to find the strongest broad pressure in the current research field that can provoke authentic coach reaction. This signal must be charged enough to provoke response, timely enough to matter now, and broad enough not to over-steer the coach. A pressure cue, not a conclusion.

**Phase B: Post-Trigger Coalition Formation.** After the coach responds and the material passes authenticity gating. Its job is to detect stronger primitive activations inside the coach's authentic language, generate candidate transforms, form a coalition signature, and route the coalition into CCF execution.

The governing law: **the first edge should be broad enough to elicit truth; the second edge should be sharp enough to organize execution.**

---

## 5. Coalition Formation Theory

### 5.1 What a Coalition Is

A primitive coalition is a sparse set of active primitive sub-agents whose weighted vector directions create a task-specific pattern of controlled variation. Coalitions are not random mixes — they are structured combinations chosen because they produce a specific behavioral style with precision.

Examples:
- A Discovery-mode CCF hook: `Shared_Experience + Irony_Inversion + Throughline`
- A Processing-mode Telegram coaching note: `Matching_Principle + Looping_for_Understanding + Emotional_Containment`
- A CMF breakthrough short: `What_Is_What_Could_Be + STAR_Moment + Auditory_POV + Sonic_Attention_Architecture`

### 5.2 Coalition Vector Geometry

The coalition vector is the compressed geometry of the active set. It tells us not only which faculties were present, but how they were weighted, aligned, or counterbalanced. This makes receipts reusable because we can compare task outcomes in terms of coalition structure rather than prose explanations.

Controlled variation emerges from three design rules:
1. **Sparse activation** — large registry, small active set (4–10 primitives per task from 150+ available)
2. **Weighted direction** — each active primitive carries a weight that governs its contribution
3. **Admissible range constraints** — defined float boundaries prevent overexpression or underexpression

This prevents both centroid blandness and chaotic overexpression.

### 5.3 The Anti-Centroid Law

Generic AI flattens human emotion toward the centroid — the safest, most polite average. CCP defends the edge. At every handoff point (research → provocation, coach response → blueprint, primitive → coalition, coalition → content), the Anti-Centroid Law requires active measurement of charge preservation. If charge has been diluted during a handoff, the system must flag the loss and attempt repair before proceeding. This is operationalized through Pydantic validation boundaries and coalition fatality detection.

### 5.4 Candidate Generation and Survival

Each primitive space generates multiple candidates from the same evidence field. An `Irony_Inversion` lab may propose 3–7 possible inversions. A `What_Is_What_Could_Be` lab may propose 3–7 contrast trajectories. The system should not commit at primitive detection time — it should commit after candidate survival scoring.

Each candidate is scored on: evidence fidelity, emotional charge, recognizability, tribal density, surprise potential, and compositional independence. Only candidates scoring above the survival threshold enter the coalition formation stage. Failed candidates are logged for pattern analysis but do not enter execution.

### 5.5 Coalition Formation as a Deterministic Selection Problem

Coalition formation must not be treated as a poetic act of taste alone. It is a deterministic selection problem operating over a probabilistic candidate field. The candidate field is wide, messy, and uncertain. The coalition decision is narrow, typed, and accountable. This is the point where CCP stops behaving like a clever writing assistant and starts behaving like a compiler.

The compiler logic works in four passes:

1. **Eligibility pass.** A primitive cannot enter coalition consideration unless its candidate survived evidence fidelity, charge, and routeability checks.
2. **Compatibility pass.** The surviving candidates are checked for synergy, antagonism, redundancy, and family saturation. Two individually strong primitives may still fail as a pair if they cancel each other or overconcentrate one dimension of force.
3. **Weighting pass.** The coalition is not only a set; it is a geometry. Each primitive is assigned a weight that reflects its required contribution to the final execution style. This weighting must be explicit enough to appear in receipts and later benchmarking.
4. **Routeability pass.** A coalition is not valid merely because it is internally elegant. It must cash out into a real CCF, CMF, CBCS, or VÂ²WS pathway. If the coalition has no viable execution route, it is not a usable coalition.

This means coalition formation is the exact point where the platform enforces anti-slop rigor. The registry may contain 150+ codified primitives, but runtime should still behave according to the law of **large registry, small active set**. Most outputs should be governed by four to ten meaning primitives and a similarly constrained experience set. Too many active primitives does not create richness. It creates ambiguity, redundancy, and hidden centroid regression.

### 5.6 The Orchestration Dichotomy: Deterministic vs Probabilistic Layers

One of the most important clarifications in the Era 3 architecture is that primitive orchestration operates across two different kinds of logic.

The **probabilistic layer** is where the system explores, proposes, projects, and detects. This includes latent signal detection in research, candidate generation inside primitive spaces, fuzzy similarity retrieval through vector memory, LLM reasoning during preliminary expression planning, and draft-level surfacing of near-miss patterns. This layer is allowed to be wide because its job is exploration. It searches for live possibilities, not final truth.

The **deterministic layer** is where the system constrains, validates, compiles, and records. This includes schema validation, admissible ranges, eligibility thresholds, coalition acceptance or rejection, routing law enforcement, receipt generation, and benchmark logging. This layer is intentionally strict because its job is execution integrity. A probabilistic candidate may whisper possibility. A deterministic gate decides whether the platform is allowed to act on it.

If we collapse everything into probabilistic language, the platform drifts into aesthetically plausible but unstable behavior. If we collapse everything into deterministic rigidity too early, the platform loses discovery power and becomes blind to latent pressure. The orchestration dichotomy therefore resolves as:

`probabilistic exploration -> deterministic selection -> probabilistic realization -> deterministic validation`

This sequence is the right balance between living intelligence and engineering discipline.

### 5.7 Anti-Centroid Enforcement Inside Primitive Logic

The Anti-Centroid Law is not a slogan about avoiding generic content. It is an operational rule enforced at the primitive level. Every primitive coalition must preserve the pressure that made the material worth generating in the first place.

Centroid drift usually appears through five failures:

- **soft averaging** â€” the output sounds broadly acceptable but emotionally dull
- **over-explanation** â€” recognition arrives late or never arrives
- **redundant layering** â€” multiple primitives add no new force
- **safety inflation** â€” the system self-softens into politeness
- **route flattening** â€” a live coalition becomes generic when projected to format

To prevent these, the system needs explicit anti-centroid checks:

- contrast preservation check
- recognition latency check
- weight collapse check
- redundancy check
- pressure leakage check

These checks matter even more in coaching than in ordinary media because the coach's voice is supposed to grow sharper, not safer in the bland sense. The platform must support dignity and ethical precision without muting conviction.

### 5.8 Coalition Templates and Runtime Freedom

The registry should eventually support recurring coalition templates. These templates are not frozen prompts; they are reusable geometries that have proven themselves across repeated outputs.

Examples include:

- `Shared_Experience + Throughline + Irony_Inversion` for recognition hooks
- `What_Is_What_Could_Be + Stakes_as_Personal_Why + Decision_Change_Arc` for pressure reframes
- `Matching_Principle + Looping_for_Understanding + Emotional_Containment` for relational reflections
- `Big_Idea_Formulation + Superobjective + Writing_for_the_Ear` for authority briefings

Templates improve runtime efficiency because they reduce search cost. But they cannot become rigid defaults. The runtime still needs freedom to reject a familiar coalition if the evidence field does not support it. Templates are memory aids, not replacement truth. Memory can suggest a proven pattern probabilistically, but the current evidence field still decides deterministically whether that pattern is admissible.

---

## 6. The Biology of the System

### 6.1 Biological Hierarchy

The strongest model for this architecture is a layered organism, not a flat cell or generic agent metaphor.

The earlier shorthand that treated the Primitive Registry as the whole genome is no longer sufficient. The registry is a critical encoded capability layer, but it is not the entirety of CCP truth. The fuller hierarchy is:

| Biological Layer | CCP Component | Function |
|---|---|---|
| **DNA / Truth** | Voice DNA, Negative Space, SDA ontology, primitive canon, stable constitutional policies | Defines what the organism is and what it must never become |
| **RNA / Transcription** | Context Premise, Trigger Match, invariant packets, geometry packets, primitive candidate packets, SFL packets, variation-ready packets | Decides which capacities are expressed in this moment |
| **Muscular / Force** | Primitive coalitions, edge products, activation steering | Applies transformation pressure to the semantic field |
| **Nervous / Delivery** | Runtime DSPy orchestration, SFL, rhythmic structure, strategic ambiguity, repetition with variation | Turns chosen force into felt transmission |
| **Variation / Phenotypic shaping** | asymmetry, resonance curves, salience distribution, paradox retention | Keeps the output alive instead of sterile |
| **Immune System** | validators, Pydantic, directional integrity, hard negatives, perceptual failure checks | Rejects malformed, generic, or corrupt output |
| **Selection Pressure** | real outcomes, receipts, benchmark memory, runtime traces | Determines what should be reinforced over time |

At runtime, primitives are best understood as **muscular faculties** or **force sub-agents**. They do not decide the whole organism. They operate after deep truth determination and before perceptual delivery. A full agent (`Telegram_Coach`, `CCF_Writer`, `CMF_Composer`) is the larger organism coordinating truth packets, primitive force, DSPy-backed delivery planning, tools, validators, and skills to complete a goal.

### 6.2 Vector States and Measurable Operations

A primitive is not just a vector — it is a sub-agent with a vector state. The sub-agent is the living faculty. The vector is the measurable representation of its state.

Key vector operations:
- `activate(p)` — instantiate a primitive sub-agent
- `suppress(p)` — keep it dormant
- `amplify(p, w)` — increase contribution
- `blend(p1, p2)` — produce combined expression
- `sequence(p1 → p2 → p3)` — define ordering
- `project(p, surface)` — translate into text, voice, visual, or sonic behavior
- `contrast(p1, p2)` — make opposing effects visible
- `normalize(C)` — prevent coalition overload
- `sparsify(C)` — keep only highest-value active set
- `gate(p by context)` — restrict activation based on mood, role, or risk

Edge cases are formalized: a zero vector represents silence, negative space, deliberate non-intervention, or withheld explanation. Extremely large magnitude signals melodrama, clutter, or coercive persuasion. Opposing vectors create tension or cancellation. Near-identical vectors reveal primitive duplication.

### 6.3 Voice as the Hardest Proof Case

The voice layer makes the biology especially concrete. In text, sloppy primitives can still look persuasive. In voice, primitive failure is much more obvious. A coaching note that is too dense, too flat, too performative, or too generic immediately loses trust. That is why voice is now the hardest proof case for this architecture.

If the primitive system can govern premium voice-note rendering — segment-level timing, emotional restraint, human-first sonic composition — then the rest of the platform becomes easier to formalize. This means primitive architecture no longer stops at plan generation. It must now survive contact with measurable audio output. The voice layer requires four production contracts:

1. **Render Profiles** — mapping coalition signatures to segment-level prosody targets (pacing, pitch variance, pause architecture)
2. **Expressive Memory Banks** — storing the coach's characteristic emotional movements for authenticity comparison
3. **Score Packets** — conviction density, hedge frequency, pitch stability, silence quality per segment
4. **Evaluation Packets** — post-render alignment vs similarity scoring against the Voice DNA Growth Model

### 6.4 JIT Activation Law

A good coach does not carry every mental model actively at once. They recruit the right faculty at the right moment. CCP should work the same way. The activation law is: **large registry, small active set.** One agent may have access to 150+ primitive types but activate only 4-10 for a given task. Runtime context acts epigenetically, deciding which encoded capacities are allowed to express in the current moment without changing the deeper DNA layer itself.

This law now also implies an execution rule:

- JIT activation is not prose improvisation
- JIT activation should prefer typed packets, executable skill contracts, and DSPy-backed routing where mechanics repeat
- a live runtime can assemble different active primitive sets on demand without collapsing into one giant monolithic prompt

---

## 7. The Matrix of Edging

### 7.1 Edging as Tension Selection

Edging is not a gimmick. It is the architecture of controlled tension selection. Its job is to help CCP find the strongest broad pressure worth bringing to the coach, get truth-rich reaction, transform authentic material into measurable primitive coalitions, and route the resulting force into real CCF and CMF workflows.

The current doctrine separates concerns cleanly: **Matrix of Edging selects the meaningful human pressure; experience primitives decide how that pressure should be timed, framed, softened, intensified, or replayed.**

### 7.2 Why Research Must Come First

Research is where the first edge pressure is found. The pre-trigger sequence should be:

```
CRAL / research field → broad primary signal extraction → provocation design → coach reaction
```

Not: research → wait for coach → then start thinking about edges. Generic research produces generic prompts. Generic prompts produce weak voice notes. Weak voice notes poison the whole downstream chain — scripts, visuals, sonic design, everything.

---

## 8. Orchestration Contracts

### 8.1 Skills as Organ-Level Procedures

`SKILL.md` files are not just guidance documents. They are orchestration contracts that tell an agent how to recruit, sequence, constrain, and validate primitive sub-agents in order to finish a task.

The newer CCP rule is that a mature skill should split into three layers:

1. **Skill / strategy layer**
   - what the skill is for
   - what quality law it enforces
2. **Schema layer**
   - typed inputs
   - typed outputs
   - admissible states
   - validation boundaries
3. **Executable layer**
   - DSPy module
   - Python or TypeScript tool
   - structured internal prompt program

A strong skill therefore specifies: task goal, eligible primitive families, candidate coalition patterns, activation thresholds, disallowed combinations, tool usage rules, validator obligations, receipt format, fatality conditions, and the exact schema/tool boundary where drift should be reduced through code rather than prose alone.

### 8.2 Workflow Integration Map

| Workflow Stage | Primary Families | Coalition Pattern |
|---|---|---|
| CRAL Research | STR, PRS, CON | Broad signal detection — sparse, wide-net |
| Trigger-First Provocation | CON, HUM, PSY | Pressure cue — charged, broad, not over-steered |
| Coach Response Analysis | PSY, ACT, VOC | Authenticity gating — LIWC, conviction density |
| Blueprint Distillation | STR, PRS, CON, HUM | Coalition formation — weighted, surviving candidates only |
| CCF Script Generation | STR, PRS, ACT, BUS | Full coalition execution — projected to text |
| CMF Visual Pipeline | VSG, CON, STR | Projected to visual coordinates — Skia/SAM3 |
| CMF Sonic Phase | VOC, VSG | Projected to sonic behavior — prosody, silence, motif |
| CBCS Coaching Notes | PSY, VOC, ACT | Projected to voice — one emotional job per note |
| Conscious Reactions Scoring | HUM, ACT, PRS | Projected to performance benchmark — delivery metrics |
| V2WS Webinar Slides | PRS, BUS, STR | Projected to teaching-while-selling — CTA architecture |

### 8.3 YAML Codification Protocol

The workflow map should also be read alongside the archetype layer.

Primitives do not replace archetype containers. They animate them.
An archetype defines the structural container and cognitive job. Primitives define the active transformation operators inside that container. Adapters then alter execution based on mood state, maturity, semantic affinity, and voice constraints.

The runtime relationship is:

`context substrate -> primitive candidate field -> coalition -> archetype container -> JIT contract -> destination packet`

With the newer doctrine in place, that relationship should now be read more precisely as:

`truth substrate -> primitive candidate field -> coalition -> edge product -> delivery stack -> variation stack -> validation -> destination packet`

where:

- the **truth substrate** includes Voice DNA, Negative Space, and SDA
- the **delivery stack** includes SFL and composition depth profiles
- the **variation stack** includes asymmetry, resonance, salience distribution, and paradox retention

This preserves the correct primitive placement: after deep truth determination, before perceptual delivery and render realization.

This prevents two opposite mistakes:

- reducing archetypes to mere content categories
- reducing primitives to vague creative adjectives

Every primitive entering the registry must follow the codification protocol:

1. **Read the audit file** — extract the mechanistic truth, not a summary
2. **Read the source book reference** — verify against the original material
3. **Write the definition** — dense, 2–3 sentences, no filler, no metaphor-only language
4. **Calibrate geometry floats** — each float must have a written rationale, no round numbers without justification
5. **Map coalition partners** — identify synergistic and antagonistic primitives
6. **Map workflow integration** — which environments use this primitive and when
7. **Validate dual-source** — both audit and book reference must be cited and verified

If any step fails, the primitive does not enter the registry. It is logged as a candidate for future codification with the failure reason recorded.

### 8.4 Self-Translation and the Invisible Pipeline

Per the Invisible App Doctrine (PRD-01 §6), the entire primitive orchestration pipeline is invisible to the coach. The coach records a voice note inside Telegram. Behind that simple action, the system activates the relevant primitive coalition, scores the delivery against biometric benchmarks, extracts content assets through the CMF pipeline, and refines the coach's Voice DNA — all without the coach ever seeing a primitive name, a coalition vector, or a workflow stage. The sophistication exists to serve the simplicity. Primitives make the coaching sessions better and the content more distinctive, but the coach experiences only the results: sharper feedback, more resonant content, more memorable outputs.

This is the Self-Translation Principle at the primitive level: the intelligence layer self-translates coaching sessions into two kinds of invisible value — content assets (shorts, carousels, benchmark scorecards) and Brand DNA refinement (Voice DNA Core/Style/Growth enrichment, CRAL evidence field expansion, coalition history strengthening).

---

## 9. Validation and Quality Gates

### 9.1 Pydantic Schema Enforcement

All coalition signatures are validated against Pydantic models before entering execution. If an LLM hallucinates an unsupported primitive candidate, Pydantic throws a schema error and the system reverts to a safe fallback. This is the blood-brain barrier of the intelligence layer — only molecules matching the biological schema pass.

### 9.2 Coalition Fatality Detection

A coalition is declared fatal (and logged for analysis) when:
- Charge preservation drops below 70% at any handoff
- A primitive is activated outside its admissible range
- Two antagonistic primitives are blended without explicit contrast intention
- The coalition vector magnitude exceeds the overexpression threshold
- Evidence fidelity scoring falls below the dual-source minimum

### 9.3 Receipt Architecture

Every coalition execution produces a structured receipt stored in the coach's PostgreSQL tenant schema:

```yaml
receipt:
  coalition_signature: ["PRM-STR-008", "PRM-PRS-006", "PRM-HUM-003"]
  primitive_weights: {"PRM-STR-008": 0.45, "PRM-PRS-006": 0.35, "PRM-HUM-003": 0.20}
  candidate_survival_scores: {"PRM-STR-008": 0.91, "PRM-PRS-006": 0.87, "PRM-HUM-003": 0.82}
  handoff_charge_measurements:
    research_to_provocation: 0.88
    response_to_blueprint: 0.79
    blueprint_to_content: 0.75
  output_quality: 0.81
  fatality_flags: []
  environment: "CCF"
  timestamp: "2026-05-06T15:30:00Z"
```

Receipts become the training data for future coalition refinement. Over time, the system learns which coalition patterns produce the highest charge preservation for each coach, which primitive combinations create the most memorable content, and which activation weights best match the coach's evolved Voice DNA. This is the selection pressure layer of the biological model — what actually worked in production shapes what gets activated next.

### 9.4 Attention Steering and Activation Steering

This architecture aligns naturally with how transformers already work. Attention is already selective. Steering is already possible. What has been missing is a stronger internal grammar for what should be selected and why.

Activation steering operates at the level of representation. If we know that contradiction, tension, or expectation violation rely on certain internal patterns, we can amplify those directions without bloating the prompt. Prompting then becomes more optimized because prompts no longer have to carry all meaning directly. They work as RNA-level local instructions informed by deeper steering. A compact expression plan can say: prioritize contradiction detection, hold back explanation until after recognition, amplify belonging cues early, reserve peak intensity for the final third. This is much more elegant than dumping theory into the prompt window.

The long-term technical stack should therefore distinguish three control layers: steering and sparse attention for latent selection, DSPy expression planning for typed orchestration, and prompt execution for surface realization. For voice rendering, a fourth layer — render-time score compilation and post-render evaluation — ensures the primitive system survives contact with measurable audio output.

This should now be understood as part of a larger organism distinction:

- runtime primitive force application
- runtime delivery and variation
- and a separate optimization layer where DSPy, activation steering, supervised finetuning, and reinforcement updates improve the system over time

Those optimization methods do not replace the primitive layer.
They refine how the primitive layer is selected, expressed, and evaluated.

---

## 10. Risk Mitigation

### 10.1 Primary Risks in the Primitive Layer

The primitive module carries unusually high architectural leverage. If it is wrong, every downstream surface becomes more sophisticated in the wrong direction. The risks are therefore deeper than ordinary feature bugs.

| Risk | Why It Matters | Mitigation |
|---|---|---|
| Ontology drift | Primitive meanings slowly mutate across agents, prompts, and teams | Keep YAML registry canonical, versioned, and validator-gated; never let vector memory define ontology |
| Coalition ornamentalism | Coalitions sound impressive but do not improve outputs | Require receipt logging, routeability checks, and post-output benchmark comparison |
| Anti-centroid theater | The system claims to defend edge but still flattens outputs at projection time | Enforce contrast preservation, weight collapse, and recognition-latency validators at each major handoff |
| Plane confusion | Meaning and experience primitives get flattened into one mixed registry | Maintain separate schemas, separate registries, and explicit crosswalk IDs |
| Primitive over-activation | Too many primitives fire at once, creating incoherent output | Enforce sparsity rules, family saturation caps, and normalization before execution |
| Coach misalignment | Coalition force sharpens in a way that no longer fits the coach's evolving voice | Route all high-stakes outputs through Voice DNA Core/Style/Growth alignment gates |
| Quality illusion | A premium-looking output hides weak primitive logic underneath | Use receipts and measurable validator outcomes, not visual polish alone, as pass conditions |

### 10.2 Deterministic Guardrails

The deterministic layer is the main mitigation against primitive failure. It should be treated as a hard envelope, not a soft suggestion. The envelope includes:

- Pydantic schema validation for registry objects and receipts
- typed coalition plans
- explicit admissible ranges for family-local geometry
- required dual-source validation for codified primitives
- anti-centroid checks at research, blueprint, and output projection stages
- fail-closed behavior when coalition integrity cannot be confirmed

Fail-closed is important. If the coalition cannot be validated, the system should reduce ambition and choose a lower-risk, narrower route rather than hallucinating sophistication.

### 10.3 Human Review Boundaries

Although the primitive system is designed to become highly reliable, some review surfaces should remain strategically human-supervised in early deployment:

- adding brand-new primitives to the canonical registry
- changing geometry ranges for high-leverage primitives
- accepting new coalition templates as reusable defaults
- adjusting fatality thresholds
- adjudicating disputes between coach alignment and benchmark performance

The point is not to slow the system down forever. The point is to protect the layer that defines truth for the rest of the platform.

### 10.4 Invisible App Compatibility

Per the Invisible App Doctrine, all of this complexity must remain backstage. Coaches should never experience primitive administration. They should experience:

- sharper prompts
- better reactions
- stronger content
- more human voice notes
- more coherent feedback
- more meaningful challenge progress

That means the risk mitigation strategy must protect simplicity at the surface. The backstage can be mathematically rich. The front-stage must remain legible and over-delivered. Primitive sophistication that leaks into the coach-facing UI as jargon is a product failure.

### 10.5 Final Mitigation Law

The primitive system should be treated as CCP's internal constitution.

If a feature, prompt, or pipeline wants to bypass primitive logic for speed, the platform should assume quality debt is being created. Temporary shortcuts may be tolerated for experimentation, but the production system must route back through the registry, coalition, validation, and receipt architecture. That is how the platform avoids becoming another pile of clever prompts with no durable intelligence spine.

---

*This document is one of 9 modular PRD modules. Consult `PRD_INDEX.md` for the complete module registry, cross-reference tables, and agent loading protocol.*


---

## ERA 3 BROWNFIELD ANALYSIS (Functional Requirements)

# Functional Requirements: PRD-08 Conscious Primitives

This document details the functional requirements for the **PRD-08 Conscious Primitives** module, applying the Era 3 (Core-24) Brownfield structural analysis to execute the Registry, Coalition, and Orchestration layer.

---

## 1. Needs to be Built (New Features & Updates)

### 1.1 The Meaning/Experience Plane Separation
*   **WHAT feature needs to be built OR Updated:** Split platform intelligence into two distinct planes: Meaning Plane (What to teach, e.g., Narrative, Persuasion, Diagnostics) and Experience Plane (How to deliver it, e.g., Triggers, Friction, Safety).
*   **WHICH Primitives are actively engaging:** All 18 Primitive Families across both planes.
*   **WHY it needs to be built OR Updated:** Conflating *what* is said with *how* it is delivered creates confused, incoherent coaching notes. A "Superobjective" (Meaning) is fundamentally different from a "Variable Reward Schedule" (Experience) and they require different validation rules.
*   **SO WHAT (the benefit of this in the CCP ecosystem):** Allows distinct agents to manage content logic vs delivery logic without contaminating each other, creating a modular, perfectly scaled intelligence engine.
*   **WHAT does not need to be built:** The foundational YAML parsing architecture and primitive validation logic.
*   **WHY it's already perfect how it is (PROOF):** Completely spec'd in `FR-APR-08_Primitive_Matrix_Engine_Tech_Spec.md`.

### 1.2 The Dual-Source Requirement (Anti-Slop Gate)
*   **WHAT feature needs to be built OR Updated:** Enforce a strict requirement that no primitive enters the registry without two verified sources: an internal audit file AND a direct book reference.
*   **WHICH Primitives are actively engaging:** All Meaning Primitives.
*   **WHY it needs to be built OR Updated:** Without this, the system relies on LLM hallucination and generic "internet marketing sludge." True authority cannot be simulated.
*   **SO WHAT (the benefit of this in the CCP ecosystem):** Guarantees that every piece of advice, frame, or coaching tactic the platform generates is rooted in verified, high-level human expertise.
*   **WHAT does not need to be built:** The primitive codification templates and GitHub action schema validators.
*   **WHY it's already perfect how it is (PROOF):** Exists natively inside the Primitive Validation Pipelines (`FR-APR-08`).

### 1.3 Coalition Formation & Receipt Architecture
*   **WHAT feature needs to be built OR Updated:** The system must orchestrate "Coalition Signatures" (sparse sets of 4-10 weighted primitives) for tasks and log their precise weights into a PostgreSQL "Receipt" for every generation event.
*   **WHICH Primitives are actively engaging:** FBK (Feedback & Scoring rituals).
*   **WHY it needs to be built OR Updated:** To prevent "Anti-Centroid Drift," where AI outputs slowly revert to the safest, most boring average. Receipts allow the platform to mathematically track why a generated output succeeded or failed over time.
*   **SO WHAT (the benefit of this in the CCP ecosystem):** Transforms CCP from a "prompt-and-pray" wrapper into a deterministic compiler that measures its own intelligence and effectiveness.
*   **WHAT does not need to be built:** The PostgreSQL receipt schemas and deterministic agent handoff logic.
*   **WHY it's already perfect how it is (PROOF):** Spec'd deeply in `FR-APR-08` and the `FR33_Automated_Webinar_Gen_Engine_Tech_Spec.md` orchestration architectures.

---

## 2. Inventory of Specs for CURRENT RELEVANT CCP FEATURES

The following technical specifications map to the foundational capabilities that act as the irreducible core of PRD-08. **These do NOT need to be built from scratch**; they are already architected, perfect as they are, and ready for deployment.

### Primitive Registry & Matrix Engine
*   `FR-APR-08_Primitive_Matrix_Engine_Tech_Spec.md`

### Orchestration & Compiler Logic
*   `FR33_Automated_Webinar_Gen_Engine_Tech_Spec.md`
*   `FR_VID-11_CCF_CMF_Content_Pipeline_Tech_Spec.md`

---

## 3. MARKED AS OBSOLETE (For System Removal)

The Era 3 analysis fundamentally shifts CCP from a "clever AI writing assistant" to a Deterministic Compiler. "Primitives are not prompt tips or adjectives." 

This forms the Master Deletion Inventory for Conscious Primitives:

*   **[OBSOLETE] Unstructured Prompt Engineering:** The legacy strategy of injecting massive, unstructured "creative guidelines" or raw book text into an LLM context window is completely deprecated. All platform intelligence must be passed as typed, validated YAML primitives. Any code relying on giant prose blocks for styling is obsolete.
*   **[OBSOLETE] Synthetic Generative Hallucination:** Any content pipeline that relies purely on an LLM's latent "guessing" without explicitly pulling a `PRM-XXX-NNN` primitive and verifying its Dual-Source integrity is obsolete and must be heavily modified or removed to protect the Anti-Slop Mandate.
