---
type: modular-prd
module: PRD-02
title: CCF Content Factory - Trigger-First Research-to-Content Compiler
author: John (Product Manager)
date: 2026-05-06
status: Source of Truth
version: 6.0
dependencies:
  - docs/prd/prd.md (Foundation PRD - FR-GA, CA-2, CA-3, CA-4)
  - docs/prd/modules/PRD_INDEX.md
  - docs/prd/modules/PRD_01_CCP_Platform_Strategy.md
  - docs/prd/modules/PRD_08_Conscious_Primitives.md
source_documents:
  - lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md
  - lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md
  - lab/CCP APRIL Updates/05_Core_Experience/Primitive_Conscious_Orchestration_Architecture.md
  - lab/CCP APRIL Updates/05_Core_Experience/Primitive_Family_Classification_CCP_CMF.md
  - lab/CCP update/CCP_Architecture_V5.0.docx.md
  - lab/CCP update/CCP_Evolution_Architecture_Report_V2.docx.md
  - lab/CCP update/CRAL_Documentation_V1.docx.md
  - lab/CCP update/Sovereign_CRAL_Research_Engine_TechSpec_V1.md
  - lab/CCP update/SearXNG_Custom_Scaffolding_Engine.md
  - lab/CCP update/JIT_Skill_Compiler_Architecture.docx.md
  - lab/CCP update/CCP_Script_Generation_Skill_Type_Guide_v1.0.docx.md
  - lab/CCP update/Mood_State_Architecture_Documentation.docx.md
  - lab/CCP update/Trigger_First_Engine_Documentation.docx.md
  - Conscious Architect University/cau_master_curriculum_registry.md
active_primitives:
  meaning_plane: [STR, PRS, CON, PSY, VOC, VSG, ACT, REF, BUS]
  experience_plane: [TRG, FRC, FBK, PER]
capability_areas: [CA-2, CA-3, CA-4, FR-APR-02, FR-GA]
---

# PRD-02: CCF Content Factory - Trigger-First Research-to-Content Compiler

**Version:** 6.0 | **Status:** Source of Truth | **Date:** 2026-05-06

---

## 1. Purpose and Architectural Claim

The Conscious Content Factory is the system that turns lived expression into usable communication assets without forcing the coach to become a content operator. It is not a writing assistant, not a batch content dashboard, and not a topic ideation sandbox. It is an **invisible trigger-first compiler** that sits behind the two CCP touchpoints - AFFiNE and Telegram - and converts research pressure, authentic response, primitive orchestration, and routing logic into precise content source material.

CCF exists because most content systems start too late and too shallow. They begin with topic selection, format choice, and output drafting. That approach optimizes for speed to text, but it destroys the very qualities CCP is trying to protect: real conviction, pressure-tested specificity, lived proof, recognizable rhythm, and emotionally legible judgment. CCF reverses the sequence. It starts upstream, with the right pressure, the right evidence, the right trigger, and the right coach reaction. Only then does it authorize content generation.

Its mandate is fourfold:

1. **Find the pressure field.** Research what is timely, undeniable, culturally alive, and relevant to the coach's worldview.
2. **Cause authentic expression.** Surface a real reaction from the coach through a well-chosen prompt, topic, or contextual event.
3. **Compile meaning.** Transform the raw expression into structured primitive coalitions and routeable content logic.
4. **Emit controlled outputs.** Produce source artifacts that downstream systems can render into shorts, carousels, scripts, decks, voice notes, reaction briefs, and social proof objects.

The key architectural claim is simple: **CCF does not write from nothing. It compiles from activated truth.** The difference is category-defining. Generic systems synthesize plausible language around a topic. CCF uses sovereign research, primitive orchestration, and authenticated reaction to produce material that would not exist without this coach, this moment, and this triggering context.

This module therefore defines the content factory as a compiler, not a creator in the consumer-tool sense. It is the source-of-truth content spine for the wider platform: CMF renders its scripts and shot logic, CBCS uses its distilled truth packets, Conscious Reactions uses its topic and counter-position briefs, V2WS uses its narrative structures and conversion arcs, and Law28 uses its speaking doctrine outputs as both learning material and transformation proof.

---

## 2. Core Architecture and Runtime Model

### 2.1 The Trigger-First Compilation Chain

The runtime architecture of CCF follows a strict causal order:

```text
SCRE / CRAL signal discovery
-> primary signal packet
-> edge selection / pressure framing
-> coach provocation
-> authenticated response capture
-> primitive candidate generation
-> coalition survival and weighting
-> subliminal function and depth selection
-> variation shaping
-> route recommendation
-> source artifact emission
-> downstream rendering and delivery
```

Every stage narrows ambiguity while preserving authenticity. The system should never skip directly from research to polished content. If there is no authentic response, there is no right to render.

The older shorthand for CCF was "research -> reaction -> coalition -> output." That remains directionally true, but it is now incomplete. CCF must explicitly carry the deeper runtime organism:

`truth -> transcription -> force -> delivery -> variation -> phenotype -> evaluation`

Inside CCF, that means:

- **truth**
  - Voice DNA
  - Negative Space
  - SDA pressures
  - constitutional policies
- **transcription**
  - signal packets
  - trigger packets
  - invariant / geometry packets
  - primitive candidate packets
- **force**
  - coalition formation
  - edge product determination
- **delivery**
  - SFL selection
  - composition depth selection
  - runtime DSPy skill orchestration
- **variation**
  - salience shaping
  - asymmetry
  - resonance / paradox retention
- **phenotype**
  - source artifact manifests
  - downstream render-ready outputs

### 2.2 The Seven Runtime Layers

| Layer | Name | Function | Primary Owner |
|---|---|---|---|
| L1 | **Signal Discovery** | Find timely, resonant, undeniable, and coach-relevant material. | SCRE / CRAL |
| L2 | **Pressure Selection** | Decide what tension or contradiction is worth activating. | Edging + Planner |
| L3 | **Coach Activation** | Elicit real reaction in voice, text, or conversational form. | Telegram / AFFiNE ingress |
| L4 | **Meaning Distillation** | Convert expression into primitive candidates, evidence links, and content vectors. | Primitive orchestrator |
| L5 | **Coalition Formation** | Choose sparse weighted combinations that can carry the idea. | Coalition engine |
| L6 | **Routing and Formatting** | Select the right content archetype, format family, and delivery role. | Compiler / routers |
| L7 | **Artifact Emission** | Produce structured output packets for CMF, V2WS, CBCS, and reactions. | Export governance |

This layered model matters because CCF is not one monolithic prompt. It is a series of rights and constraints. A downstream render only becomes legitimate if the upstream layers established enough epistemic and emotional pressure.

### 2.3 What CCF Actually Produces

CCF is not the final media renderer. It emits **content source artifacts** that downstream systems can transform. The core artifact classes are:

| Artifact Class | Purpose | Downstream Consumer |
|---|---|---|
| **Signal Brief** | Compresses the current event, contradiction, or cultural shift into a triggerable object. | Conscious Reactions, Telegram prompts |
| **Response Distillate** | Preserves the coach's raw position, emotional charge, evidence, and verbal anchors. | CBCS, Law28, archival memory |
| **Coalition Script Spine** | Encodes the winning primitive coalition, sequence logic, and tone geometry. | CMF, short-form writing, decks |
| **Format Blueprint** | Maps the same meaning into multiple render families without flattening the core. | Carousels, shorts, webinar slides, quote visuals |
| **Content Manifest** | Provides asset-level instructions, dependencies, and validation expectations. | CMF, V2WS, delivery agents |

CCF is therefore the **meaning compiler** for the platform. It decides the logic and source truth of what will be said. Other modules decide the cinematic treatment, interface delivery, or experiential framing.

### 2.4 Deterministic and Probabilistic Cooperation

CCF must respect the orchestration dichotomy defined in PRD-01 and PRD-08:

- **Deterministic layer:** packet schemas, routing constraints, anti-centroid laws, evidence links, guardrails, export rules, validator thresholds, delivery surfaces, dependency contracts.
- **Probabilistic layer:** research synthesis, provocation wording, coalition candidate generation, tone adjustments, metaphor variants, format translations, and higher-order narrative shaping.

This split is essential. Deterministic systems protect the architecture from drift. Probabilistic systems keep the outputs alive, human, and contextually sharp. CCF becomes powerful only when both are present. A purely deterministic content engine becomes rigid and dead. A purely probabilistic content engine becomes slop.

### 2.5 Compiler Operating Modes

CCF should support four operating modes, all using the same architecture but entering through different trigger conditions:

| Mode | Entry Condition | Typical Goal |
|---|---|---|
| **Reactive Mode** | news, cultural shift, or industry flashpoint | produce timely authority and reaction assets |
| **Reflective Mode** | coaching session, CBCS voice note, or breakthrough reflection | convert private insight into reusable truth objects |
| **Instructional Mode** | a coach needs to teach, explain, or clarify a known pattern | build structured educational assets without losing signature voice |
| **Conversion Mode** | webinar, offer, objection, or sales friction moment | compile persuasive and trust-preserving communication |

These modes do not replace the trigger-first chain. They simply change which validators, primitive families, and render priorities become dominant. This keeps the architecture unified while still allowing the factory to serve multiple business-critical communication jobs.

---

## 3. Data Contracts, Schemas, and Registry Dependencies

### 3.1 Core Packets

CCF depends on the packet architecture defined in the primitive registry work. At minimum, the content factory must be able to read and write the following canonical packets:

| Packet | Role in CCF |
|---|---|
| **PrimarySignalPacket** | Holds the raw research signal, evidence provenance, relevance tags, mood-state cues, and edge hypothesis. |
| **PrimitiveCandidatePacket** | Stores candidate transformation operators extracted from the reaction plus confidence and survivability metadata. |
| **CoalitionSignature** | Stores the sparse winning set of primitives, weights, sequence geometry, and tension structure. |
| **EdgeProductPacket** | Encodes the emergent behavioral and rhetorical effect produced by the coalition, not just the primitive list. |
| **CCFRoutingRecommendation** | Suggests which content families, format surfaces, and downstream systems should receive the coalition. |
| **CoalitionBenchmarkRecord** | Tracks how similar coalition geometries perform over time for validation, ranking, and future reuse. |

CCF also needs two module-specific packets:

1. **CoachResponseCapture**
   - raw transcript
   - timestamps
   - emotional markers
   - confidence markers
   - evidence references
   - language anchors worth preserving

2. **ContentArtifactManifest**
   - artifact type
   - downstream consumer
   - required invariants
   - format constraints
   - validator checklist
   - source packet lineage

CCF now also needs SDA-aware packets whenever the system is operating at high semantic precision:

3. **InvariantFieldPacket**
   - active existential invariants
   - invariant weights
   - invariant activation intensity
   - evidence anchors
   - pressure summary

4. **ArchetypalGeometryPacket**
   - active structural topology
   - authority flow
   - agency distribution
   - sacrifice / transformation pattern

5. **RepresentationGeometryPacket**
   - authority encoding
   - fear weighting
   - status distribution
   - identity framing
   - directional risks

6. **SpeciesHypothesisPacket**
   - derived semantic species guess
   - invariant lineage
   - geometry lineage
   - shadow drift notes

7. **DirectionalIntegrityReport**
   - semantic validator verdict
   - drift flags
   - preserved invariants
   - invariant resonance multiplier
   - mutation-test outcomes

8. **HardNegativeEvaluationReport**
   - contrastive evaluation verdicts
   - deceptive adjacency risk
   - failing divergence axes
   - escalation state

### 3.2 Registry Dependencies

CCF uses the primitive registries in a meaning-first way. Experience primitives may influence prompting and delivery framing, but the content factory is anchored primarily in the **meaning registry**. Its canonical dependencies are:

- Meaning primitive registry for transformation operators.
- Experience primitive registry for ingress and prompt shaping support.
- Crosswalk map for concepts that require both meaning and experience coordination.
- Family classification surfaces for workflow scanning.
- Coalition benchmark records for reuse and validator training.

The practical rule is:

- if a primitive changes *what is said*, it belongs to the meaning decision.
- if a primitive changes *how the coach is brought to say it* or *how the result is surfaced*, it belongs to experience support.

CCF also depends on retained V5 intelligence layers that should now be treated as active compiler inputs rather than historical context:

- **Client Intelligence Layer**
- **Cultural Memory Map**
- **Coach Story Archive**
- **Context Performance Registry**
- **Context Reasoning**
- **Semantic Affinity Guard**
- **Audience Maturity routing**

CCF should now also treat the Semantic Discernment Architecture (`SDA`) as part of the anti-genericity stack rather than an optional downstream review idea. The relevant SDA dependencies are:

- **Existential Invariant field detection**
- **Archetypal Geometry selection / validation**
- **Representation Geometry analysis**
- **Content Species hypothesis generation**
- **Directional Integrity validation**
- **Hard Negative evaluation**
- **Recursive Pattern detection**
- **Emergent Contextual Invariant inference**
- **Feedback Loop projection**

These layers are part of the anti-genericity stack. If CCF ignores them, it regresses toward plausible but replaceable content.

The formal scalar language is:

- `Invariant Gravity` belongs to canonical SDA ontology and describes how much human weight an invariant naturally carries
- `Invariant Activation Intensity` belongs to runtime inference and describes how strongly the current artifact is activating that invariant
- `Invariant Resonance Multiplier` belongs to runtime semantic evaluation and describes how much the active invariant amplifies emotional charge, personal relevance, symbolic density, and memory persistence in the current composition

CCF must not collapse these into one generic "strength" field. They serve different jobs in the compiler.

For interpretive reference only, theology-to-architecture worked examples are maintained in:

`lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` Appendix A

### 3.3 Canonical Metadata Requirements

Every CCF artifact must be traceable back to source truth. That means each content object needs:

- `coach_id`
- `session_or_event_id`
- `primary_signal_id`
- `response_capture_id`
- `coalition_signature_id`
- `routing_profile`
- `validator_status`
- `evidence_lineage`
- `downstream_consumers`
- `render_permissions`

This traceability is not optional. It is how CCP avoids hallucinated persuasion, flattened voice, and context loss. It also allows the platform to audit why a specific short, carousel, script, or webinar section exists.

### 3.4 Content Family Surfaces

CCF must emit source truth that can travel across the following families without semantic collapse:

| Family | Typical Forms | Core CCF Responsibility |
|---|---|---|
| **Reaction Content** | topic brief, hot take, dual reaction spine | preserve urgency and side-taking logic |
| **Teaching Content** | carousel text, thread logic, explainer spine | preserve structure and pedagogical sequence |
| **Authority Content** | ranked claims, quote visuals, argument fragments | preserve sharpness and social proof |
| **Narrative Content** | witness arc, backstory reveal, confessional turn | preserve emotional transitions |
| **Conversion Content** | webinar turns, offer pivots, objection reframes | preserve persuasion geometry |

The same coalition may route to multiple families, but each family must preserve the original charge rather than rephrasing it into corporate mush.

### 3.4A Archetype Containers and JIT Compilation

The family surfaces above are not the deepest structural layer. Under them sits the **content archetype** layer.

That distinction matters:

- format is how the output is rendered,
- family is what business job the output serves,
- archetype is the psychological and structural container in which the meaning is compiled.

CCF should therefore treat archetypes as first-class runtime containers. They are not "reel templates." They are the containers through which the JIT compiler builds scripts, proof order, emotional turns, and later media expectations.

The practical runtime sequence should be:

`signal -> coach reaction -> invariant field -> primitive coalition -> edge product -> archetypal geometry check -> archetype container -> directional integrity validation -> JIT script contract -> render blueprint`

not:

`topic -> choose a format -> ask a model to write something`

The next doctrinal refinement should be understood through the biological orchestration model:

- `SDA`, Voice DNA, and Negative Space behave like the **DNA / truth layer**
- runtime packets behave like the **RNA / transcription layer**
- primitive coalitions and edge products behave like the **force layer**
- `SFL` and composition-depth profiles behave like the **delivery layer**
- asymmetry, resonance, salience distribution, and paradox retention behave like the **variation layer**
- render and validation produce the final **phenotype and evaluation**

So the more precise emerging sequence is:

`signal -> coach reaction -> invariant field -> primitive coalition -> edge product -> archetypal geometry check -> archetype container -> subliminal function stack -> composition depth profile -> variation profile -> directional integrity validation -> perceptual influence validation -> JIT script contract -> render blueprint`

This does not replace the earlier sequence.
It clarifies the hidden layers inside it.

### 3.4B What an Archetype Contract Must Hold

Each archetype contract should expose at least:

- an **intent**: what cognitive job this archetype performs
- an **activation condition**: when it should be selected instead of another archetype
- **structural invariants**: what remains true across every valid compilation
- a **mood-state interaction matrix**: how Processing, Escape, Discovery, and Status states alter execution
- an **anti-draft profile**: what generic AI failure looks like for this archetype
- a **distillation funnel**: how the content should compress while preserving its core charge
- **archetype-specific quality gates**

When SDA is active, the contract should also remain legible to deeper semantic validation. That means the archetype contract should either expose or preserve lineage to:

- the active **Existential Invariant** field
- the active **Archetypal Geometry**
- the active **Representation Geometry**
- the current **Species Hypothesis**
- any **Emergent Contextual Invariants** currently acting as local constraints
- any active **Directional Integrity** rules that the output must not violate

This is how CCF avoids black-box generation while preserving runtime flexibility.

### 3.4C Archetypes Govern More Than Scripts

Archetypes also influence downstream media behavior.

Each archetype should imply:

- pacing expectations
- proof density
- emotional curve
- caption density
- likely shot rhythm
- visual hook pressure
- and typical anti-genericity risks in media rendering

That is why CCF cannot treat archetypes as a private writing concern only. They are one of the bridges into PRD-03 media rendering and PRD-04 surface experience.

### 3.4D Biological Placement of CCF

CCF should now be understood as the main `RNA -> force -> delivery` compiler in the CCP organism.

In practical terms:

- it does not own the deepest identity law; that belongs to Voice DNA, Negative Space, and SDA
- it does not own the final outcome loop; that belongs to validators, receipts, and real-world feedback
- it does own the translation of deep truth into contextually expressed instructions and then into routeable content artifacts

This is why CCF must preserve lineage through:

- the truth layer it is expressing
- the primitive force layer it activated
- the delivery stack it selected
- the variation profile it allowed

without collapsing all of those into one opaque “generated script” concept.

### 3.4E Retained Archetype Inventory

CCF should explicitly preserve a visible archetype inventory instead of treating the container layer as an invisible internal abstraction.

At the retained core, the older architecture already established seven major compiler families:

1. **Storytelling**
2. **Listicle**
3. **Case Study**
4. **Comparison**
5. **Myth and Scam**
6. **Tier List / Ranking**
7. **Core Formats / Educational Authority**

Those families should remain active in the PRD because they are the main containers through which JIT script contracts are compiled.

### 3.4F Canonical Script Archetypes

The script-side inventory should be treated as an explicit working set, not a hidden registry somewhere else.

At minimum, CCF should recognize and route into archetypes such as:

- **Achievement Story**
- **Transformation Story**
- **Witness Story**
- **Backstory Reveal**
- **Confessional Turn**
- **Case Study Breakdown**
- **Comparison Breakdown**
- **Before vs After Contrast**
- **Wrong Way / Right Way Contrast**
- **Myth Debunk**
- **Scam Exposure**
- **Fear / Anxiety Listicle**
- **Shocking Listicle**
- **Stepwise Teaching Listicle**
- **Mistakes Listicle**
- **Tier List Authority**
- **Ranked Take / Ranked Claims**
- **Core Educator / Explainer**
- **Challenger / Frame Breaker**
- **Authority Proof Stack**

These are not all identical in function.
Some are optimized for:

- tribal recognition
- proof credibility
- contrastive surprise
- educational clarity
- indignation
- confession
- or conversion pressure

That is exactly why they must be explicit in the source of truth.

### 3.4F Observational Humor and Distortion Archetypes

CCF should also explicitly preserve humor-led archetypes rather than treating humor as a flavor layer only.

Important humor and distortion surfaces include:

- **Observational Humor**
- **Meme Observation**
- **Tribal Absurdity**
- **Benign Violation Reframe**
- **Pain-to-Relief Contrast**
- **Status Satire**
- **Industry Hypocrisy Exposure**

Observational Humor deserves explicit mention because it already carries strong media constraints elsewhere in the stack:

- real-image preference
- stronger tribal recognition logic
- and high dependence on authentic lived noticing rather than generic joke-writing

### 3.4G Conscious Reactions Archetype Family

The newer architecture adds a second large archetype family born from `Conscious Reactions`.

These are not merely UI modes.
They are also content containers because they shape:

- what gets said
- how tension is structured
- what social proof is created
- and what sort of media object will be emitted later

The explicit `Conscious Reactions` family should include:

- **Solo Reaction**
- **Vote Then React**
- **Debate with Jury Mode**
- **Supervisor Pairing**
- **Redemption Round**
- **Reaction Duel**
- **Audience Mirror Quiz**
- **Blind Rank Reveal / Blind Rank Defense**
- **Alphabet Challenge**
- **Last One Standing**
- **Authority Quiz / Pressure Ladder**
- **Tierlist Authority**

These modes are part of the CCF compiler surface because each one creates a different raw-material geometry:

- a solo take
- a ranked argument
- a debate branch
- a social vote loop
- a comeback clip
- or a game-show style authority fragment

CCF must know which type of container produced the raw material if it wants to compile the right downstream scripts and media.

### 3.4H Archetype Selection Law

The archetype should not be picked because a user asked for a format.

It should be selected because the system has enough evidence about:

- the signal type
- the coach's authentic reaction
- the audience maturity
- the emotional job
- the semantic-affinity risk
- the desired business job
- and the likely downstream render surface

This is the law that keeps archetypes meaningful instead of decorative.

### 3.4I Compilation Archetype Container

CCF should also formalize a dedicated **Compilation** archetype container.

**Archetype ID:** `ARC-COMP`

**Purpose**

Assemble multiple scored source reactions, debate branches, or ranked takes into a single mid-form or long-form narrative object.

**Structural invariants**

- minimum `3` source reactions per compilation
- each source must preserve score and stance metadata
- the compilation must follow an arc:
  - setup
  - tension
  - resolution or deliberate open question
- intro and outro hooks should be planned before assembly

**Coalition family**

- `STR` for sequence
- `PRS` for contrast
- `VOC` for pacing
- `HUM` optionally for relief beats

**Routing rules**

- Debate Mode compilations should preserve side-taking tension
- Solo Mode compilations should show progressive depth or change
- Tier List compilations should use ranking as the narrative spine

**Render targets**

- YouTube long-form
- audio-only podcast-style cut
- carousel summary companion

This archetype exists because compilation is not just editing.
It is a distinct narrative assembly job with its own logic.

### 3.5 Manifest Discipline and Human Auditability

Every emitted artifact should be readable by both machines and humans. This means the manifest must include a short explanation section, not just metadata. A human operator reviewing a CCF output should quickly understand:

- why this signal was selected,
- what the coach actually reacted to,
- which primitives survived,
- what the intended effect is,
- which downstream assets are authorized,
- what must not be lost in translation.

This is especially important for future review, benchmark comparisons, and fine-tuning decisions. If a human cannot audit the causal chain quickly, the compiler has become too opaque to trust.

---

## 4. The Architectural Correction CCF Enforces

CCF exists to correct five historical errors in content systems.

### 4.1 Error One: Topic-First Drafting

Most systems start with "what should we post about?" CCF starts with "what is already alive, relevant, and pressure-bearing in the world and in this coach?" The difference is enormous. Topic-first systems reward plausibility. Trigger-first systems reward recognition.

### 4.2 Error Two: Studio Thinking

The content industry assumes that value comes from a visible studio environment: calendars, planners, boards, post lists, and campaign dashboards. CCP rejects this as the front-stage experience. CCF is backstage infrastructure. The coach should feel like they are improving their communication and participating in meaningful interactions, not operating a content factory manually.

This is why CCF lives behind Telegram and AFFiNE. AFFiNE stores knowledge, memory, and human-readable strategy objects. Telegram carries the living flow of prompts, reactions, feedback, and delivery. There is no third consumer-facing production console.

### 4.3 Error Three: Format Before Meaning

Choosing "short, carousel, webinar, meme" too early destroys the deeper signal. CCF first compiles a meaning object and only then decides the render profile. The format is downstream from coalition truth, not upstream from it.

With SDA added, "meaning object" must now be understood more precisely. It is not only:

- a primitive coalition
- a content family guess
- or an archetype label

It also includes:

- the active invariant field
- the edge product that emerged from the coalition
- the archetypal geometry organizing that force
- the representation geometry encoding that meaning direction
- the invariant activation intensity of the current field
- the invariant resonance multiplier produced by the current composition
- and the directional integrity constraints that must survive compression and translation

This is how the system avoids a subtler failure mode than format-first thinking: **structure-first but direction-blind compilation**. A piece may be structurally elegant while still distorting the deeper semantic trajectory. SDA exists to stop that drift before media rendering begins.

### 4.4 Error Four: Single-Pass Generation

One-shot generation is the enemy of quality. CCF is multi-pass by design:

1. discover the signal
2. activate the coach
3. extract the reaction
4. propose primitive candidates
5. validate the coalition
6. route the artifact
7. only then emit downstream instructions

This is slower than naive prompting, but it is the only way to preserve distinctiveness at scale.

### 4.5 Error Five: Generic Similarity

Many systems mistake "sounds like the coach" for "is aligned with the coach's best current truth." CCF rejects imitation as the highest standard. It should preserve the coach's recognizable identity while still improving clarity, sequencing, conviction, and usefulness. This is the content equivalent of the Voice DNA doctrine: alignment outranks static similarity.

---

## 5. Deep Mechanism: Why the Compiler Works

### 5.1 CRAL and Sovereign Signal Discovery

CCF begins with CRAL because content quality depends on upstream evidence quality. The research layer is not an optional enrichment step. It is the origin of specificity. CRAL's JIT moments - relevant, believable, undeniable, resonant, surprising, irrefutable, relatable - act as signal filters. The system is not just looking for facts. It is looking for evidence with activation potential.

The Sovereign CRAL Research Engine deepens this by routing queries through custom categories and a source cache rather than generic search. A coach in a leadership lane may need:

- cultural-now material to feel timely,
- behavioral science to feel grounded,
- narrative journalism to humanize a point,
- tribal vernacular to feel socially native,
- anomaly science to create surprise,
- precision journalism to anchor credibility.

The important principle is that research is **diagonal**, not linear. It crosses evidence types to find the sharpest possible trigger, not just the most obvious article.

### 5.2 The Broad Signal Before the Sharp Edge

Perceptual Primitives Architecture established a crucial law: broad signal precedes precise coaching logic. The coach should react first to something that feels culturally or personally alive. Only after the reaction is captured does the system tighten the semantic geometry.

This prevents two common failures:

- over-specifying the meaning before the coach has emotionally entered it;
- under-specifying the meaning after the reaction has been captured.

CCF therefore supports two edge phases:

1. **Pre-trigger broad signal:** enough pressure to awaken reaction.
2. **Post-trigger sharpened edge product:** enough coalition precision to generate differentiated assets.

### 5.3 Primitive Candidate Survival

Once a response is captured, CCF does not immediately decide on a final frame. It generates primitive candidates, then forces them into survival pressure. Candidates that do not explain the signal, fit the coach, and route cleanly across formats are discarded.

This stage is essential because authenticity is not enough by itself. A raw reaction can still be noisy, repetitive, or structurally weak. The primitive layer turns raw truth into transformation logic. It asks:

- What is the actual move here?
- Is this contrast, escalation, diagnosis, reversal, status claim, confession, frame break, moral indictment, or invitation?
- Which combination can hold across a short, a carousel, a deck, a voice note, and a debate prompt?

The winning output is not one primitive but a **coalition signature**.

### 5.4 Coalition Signatures and Edge Products

Primitives are not content categories. They are composable faculties. Coalition signatures matter because meaningful expression almost never arrives through a single move. A memorable artifact often requires:

- one structural primitive,
- one persuasion primitive,
- one psychological primitive,
- one delivery primitive,
- one trust-transfer or authority primitive.

The coalition signature records the weighted geometry of that combination. The edge product records the emergent result. This distinction matters because "what primitives were present" is not the same thing as "what effect did the composition produce." CCF must preserve both.

### 5.5 Mood-State Routing

Mood state architecture adds another crucial layer. Not every signal should become the same style of content. A coach in a processing state may need witness and clarification. A coach in a status state may need authority and contrast. A discovery state may reward frameworks and synthesized insight. An escape state may need humor, relief, or pattern interruption.

Mood-state routing therefore acts as a compiler bias. It does not override the content, but it changes which coalition families are favored and which render profiles are safest.

### 5.6 Anti-Centroid Enforcement

CCF must aggressively avoid centroid collapse. The anti-centroid law means:

- do not average conflicting positions into a polite compromise,
- do not replace real verbal anchors with smooth corporate prose,
- do not flatten conviction into neutrality for the sake of format portability,
- do not over-normalize the coach's idiosyncrasies if they are part of the memorability engine.

The compiler should preserve edge while cleaning chaos. If the output becomes broadly acceptable but no longer recognizable, CCF failed.

### 5.7 Retained V5 Intelligence Layers

The April rewrite changed the product center, but it did not invalidate several crucial V5 intelligence substrates. CCF should explicitly preserve them as active compiler law:

- **Client Intelligence Layer**
  distinguishes Tier 1 research-only understanding from Tier 2 transcript-informed understanding and Tier 3 full CBCS plus journal plus session understanding
- **Cultural Memory Map**
  gives the compiler access to the audience's formative texts, mythologies, enemy language, and aspirational vocabulary
- **Coach Story Archive**
  provides first-person and testimonial evidence that may outperform external research for certain moments
- **Context Performance Registry**
  records which context selections historically performed well for this coach-audience pair
- **Context Reasoning**
  decides whether story, culture, external research, or humor precedent should dominate before directives are compiled

These layers are not optional memory luxuries. They are part of the infrastructure that makes generic output structurally difficult.

---

## 6. Implementation Stack and Systems Biology

### 6.1 Runtime Components

CCF should now be read through the fuller organism model rather than a loose systems-biology analogy:

| Organism Layer | CCF Component | Function |
|---|---|---|
| **Truth / DNA** | Voice DNA, Negative Space, SDA doctrine, constitutional policies | Defines what this coach and this system are allowed to become |
| **Transcription / RNA** | SCRE / CRAL signals, Context Premise, Trigger Match, invariant and geometry packets, primitive candidates | Turns stable truth into situation-specific expression plans |
| **Force** | primitive coalition engine, edge product determination, activation steering | Applies transformation pressure to the semantic field |
| **Delivery** | runtime DSPy modules, SFL function stack, composition depth profiles, archetype container logic | Converts force into a felt, structured communication strategy |
| **Variation** | salience distribution, asymmetry shaping, resonance carry, paradox retention | Prevents dead regularity and preserves aliveness |
| **Phenotype** | source artifacts, manifests, render hints, export packets | What downstream systems can actually render and deliver |
| **Protection** | validators, anti-pattern laws, anti-centroid checks, directional integrity, hard negatives | Prevents corruption, genericity, and perceptual collapse |

This is not decorative. It is what keeps research, capture, coalition, delivery, variation, and validation from being flattened into one giant "content generation" blur.

### 6.2 Sovereign Search and Signal Routing

The sovereign search layer should use:

- custom SearXNG categories,
- domain weighting,
- freshness windows,
- caches for repeatable retrieval,
- category-specific query templates,
- provenance preservation.

Signals should enter CCF already tagged for likely use:

- reaction-worthy,
- teaching-worthy,
- authority-worthy,
- conversion-worthy,
- memory-worthy.

This pre-classification speeds later routing without deciding the final content shape prematurely.

### 6.3 JIT Skill Compilation

CCF should never behave like one universal prompt. It should assemble context-specific generation contracts from a registry of skills, adapters, and validators. The JIT Skill Compiler architecture is therefore a direct fit:

- choose relevant skill families,
- inject coach and audience context,
- inject coalition signature,
- inject render family expectations,
- compile a task-specific instruction contract.

This lets the same core engine emit different kinds of source artifacts without losing internal consistency.

The build process now needs to treat that contract as executable, not merely descriptive. The expected chain is:

`skill doctrine -> typed schema -> DSPy/tool execution unit -> validated runtime packet`

That means CCF should prefer:

- runtime DSPy modules for typed routing and packet-safe reasoning
- code-backed tools where the mechanics are repeatable
- structured internal prompt programs only where computation has not yet been hardened into tools

This is especially important because many CCP skills are created just in time. JIT creation does not mean prose-only improvisation. It means the runtime should assemble the right doctrine, schema, tool, and validator mix for the moment.

The missing bridge that must be explicit is:

- primitives define what transformation operators are active
- archetypes define what structural container can carry those operators
- adapters define how mood, maturity, affinity risk, and voice constraints modify the container
- the JIT contract defines what script sections, proof order, anti-draft fences, and typed execution path are compiled
- downstream systems then decide how that structured meaning becomes media

This is how CCF remains inspectable instead of magical.

### 6.3A Context Reasoning Before Compilation

Before a JIT directive is finalized, the planner should reason through questions like:

1. does the Coach Story Archive contain a better first-person proof object than external research for this moment?
2. which Cultural Memory Map layers are strongest for the audience and topic?
3. what does the Context Performance Registry suggest has worked in similar conditions?
4. is there semantic-affinity risk that requires payload masking or route mutation?
5. what audience-maturity depth is safe and useful for this build?

Only after those decisions should the contract finalize.

### 6.3B Script-to-Visual Bridge

CCF should emit more than prose logic.

Its JIT outputs should also provide structured downstream hints such as:

- proof-object priority
- emotional beat markers
- contrast moments
- visual hook obligations
- caption density expectations
- crop or scene pressure implications
- and archetype-level anti-genericity warnings

PRD-03 renders these implications, but PRD-02 is where they become explicit and auditable.

### 6.4 Event-Driven Operation

CCF should operate in event-driven fashion rather than static weekly planning. Its triggers include:

- new sovereign signal crosses relevance threshold,
- coach voice note reveals a high-charge fragment,
- a Conscious Reactions topic produces a strong debate branch,
- a webinar rehearsal surfaces a compelling objection sequence,
- OFAP field report reveals a strong live story,
- a testimonial capture reveals language worth reframing into authority content.

This is the production equivalent of self-translation. Real life feeds the factory continuously.

### 6.5 Export Governance

Downstream consumers must not guess what CCF meant. Each export therefore needs:

- invariant phrases or ideas that must survive,
- optional alternative phrasings,
- emotional arc expectations,
- evidence anchors,
- risk flags,
- allowed compression ranges,
- prohibited simplifications.

Export governance protects the coach's signature from accidental flattening during rendering.

### 6.6 Operator Review and Escalation Boundaries

CCF is designed to automate high-value content compilation, but some cases should escalate to review rather than flow through automatically. Review should be triggered when:

- evidence is emotionally loaded but legally or ethically sensitive,
- the coach's reaction contains unstable or contradictory position shifts,
- the coalition signature is unusually sparse or unusually overloaded,
- route recommendations disagree strongly across validators,
- the output is likely to become a major campaign anchor, keynote spine, or church/community message.

The review layer does not exist to rewrite everything manually. It exists to catch high-impact ambiguity. One of CCF's key design rules is that human review should intervene at the level of meaning and consequence, not at the level of cosmetic line editing.

### 6.7 Artifact Lifecycle States

Each CCF output should move through an explicit lifecycle so that agents and operators know how trustworthy it is:

| State | Meaning |
|---|---|
| **Captured** | source signal and response exist, but no coalition has been validated |
| **Distilled** | primitive candidates and first-pass meaning objects are available |
| **Compilable** | coalition survived and routing is plausible |
| **Validated** | required guards passed and export is safe |
| **Rendered** | a downstream module created a surface-specific artifact |
| **Benchmarked** | post-delivery outcome data has been linked back to the coalition |

This lifecycle allows the factory to function as a living operating system rather than a one-shot text emitter. It also makes future agent access far easier, because each artifact can be queried by maturity rather than only by file name.

---

## 7. Workflow Integration Across the Platform

### 7.1 Telegram and AFFiNE as the Only Front-Stage Surfaces

CCF must integrate with the platform's invisible-app doctrine. The coach experiences the content system through:

- **Telegram:** prompts, reactions, recordings, delivery, feedback, challenge continuity.
- **AFFiNE:** memory, artifacts, knowledge, relationship history, campaign logic, and operator visibility.

There is no separate third touchpoint that forces the coach into "content ops mode." CCF supports those surfaces invisibly.

### 7.2 Conscious Reactions Integration

Conscious Reactions is one of the strongest ingress routes into CCF. The flow is:

1. sovereign signal selected,
2. brief created,
3. coach reacts,
4. reaction scored and captured,
5. CCF distills the response,
6. coalition signature formed,
7. artifacts emitted for short-form, ranking, quote, and follow-up challenge content.

This means the product experience and the content engine mutually reinforce each other. The coach is not "making content" in the old sense. They are participating in a meaningful experience that naturally produces content-worthy truth.

### 7.3 CBCS Integration

CBCS uses CCF in a quieter way. Here the content engine supports:

- benchmark-based reflections,
- teaching follow-ups,
- voice-note reframes,
- testimonial triggers,
- challenge reminders with real context,
- progress summaries grounded in the user's own expression.

The important rule is that CBCS outputs should feel personal first, reusable second. CCF supports this by preserving the source lineage and allowing selective translation into public-facing content later.

### 7.4 V2WS and Webinar Delivery

In webinar mode, CCF should produce:

- thesis spines,
- tension turns,
- objection ladders,
- proof sequences,
- quote-ready reframes,
- CTA bridges aligned with coach voice.

V2WS then transforms those into slides and recording guidance. CCF is responsible for the persuasive architecture, not the visual deck polish itself.

### 7.5 OFAP and Field Intelligence

Offline field encounters should feed CCF directly. Conversations, objections, surprise questions, and live stories are all premium raw material. When captured well, OFAP produces some of the highest-trust source data in the system because it is grounded in real social contact rather than abstract brainstorming.

### 7.5A Cross-Niche Authority Debates

CCF should support a content mode where a coach's take is structurally contrasted against a professional from a different field, not merely another coach.

Useful pairings include:

- coach x lawyer
- coach x doctor
- coach x therapist
- coach x financial advisor

The point is not rivalry theater.
It is productive tension between adjacent but different authority frames.

Why this works better than coach-vs-coach in many cases:

- lower credibility damage
- stronger outsider curiosity for both audiences
- more natural contrast
- and easier discovery across audience boundaries

Expected content objects:

- split-screen debate clip
- strongest-moment standalone clips
- audience vote results
- follow-up reaction invitations

The guardrail is important:

the pairing should create useful tension without collapsing into hostility or caricature. The anti-centroid validator should ensure each side remains legible as themselves rather than drifting into generic debate speech.

### 7.6 CMF Integration

CMF should treat CCF artifacts as authoritative meaning packets. It may reinterpret visually and sonically, but it should not overwrite the coalition logic without explicit validator approval. This protects the meaning plane while allowing a stronger media plane.

### 7.7 Four-Surface Skill Ladder Integration

CCF must also support the platform's main communication surfaces as defined by the new skill ladder architecture:

- **Law28 Public Speaking:** source stories, reframes, and speaking drills derived from real pressure.
- **Webinar Sales Delivery:** persuasive sequence, proof objects, and objection geometry.
- **Networking Conversations Mastery:** short social scripts, field stories, and conversational confidence anchors.
- **Social Co-Creations Charisma / Conscious Reactions:** timely takes, response chains, rankings, and debate seeds.

The factory should not treat these as separate businesses. They are four expression surfaces drawing from the same underlying meaning compiler. This unification is strategically important because it means one strong source event can strengthen multiple growth channels at once.

---

## 8. Self-Translation, Compounding, and Learning Memory

### 8.1 The Self-Translation Principle

CCF must embody the self-translation principle from PRD-01: the coach's actual growth work should automatically produce reusable artifacts. Speaking practice, reactions, webinars, coaching notes, social conversations, and testimonials are not separate from content. They are the source of content when properly captured and compiled.

This radically changes the economics of content creation. Instead of forcing a separate creative labor block, the platform turns already-valuable human activity into strategic communication assets.

### 8.2 From Single Event to Asset Lattice

One high-quality reaction should be capable of producing:

- one short-form narrative spine,
- one quote visual idea,
- one carousel teaching sequence,
- one debate prompt or counter-position brief,
- one webinar proof fragment,
- one CBCS reinforcement note,
- one memory object for future retrieval.

This is not content multiplication by empty slicing. It is coalition-preserving translation across surfaces.

### 8.3 Benchmark Memory

CCF should maintain an ongoing record of:

- which signal types activate which coaches,
- which coalition signatures produce strong outcomes,
- which format translations preserve force best,
- which evidence styles cause the strongest recognition,
- which validator failures repeat.

This benchmark memory is how the factory becomes more sovereign over time. It is not just generating outputs. It is learning the geometry of what works without collapsing into generic optimization.

### 8.4 Agent-Usable Metadata

The next-level version of CCF depends on machine-readable metadata for primitives, coalitions, routing preferences, and validation history. Once this exists, agents across the platform can consult CCF not merely as a rendering backend, but as a strategic source of truth. This is how modules begin to cooperate intelligently rather than through ad hoc copying.

---

## 9. Validation, Benchmarks, and Quality Gates

### 9.1 Core Quality Questions

Every CCF artifact must answer yes to the following:

1. Did the artifact come from authenticated coach expression rather than synthetic invention?
2. Is the evidence lineage visible and plausible?
3. Does the coalition signature explain why the output feels distinctive?
4. Is the artifact routeable across intended downstream surfaces without semantic collapse?
5. Does the output preserve identity while still improving clarity and structure?

If any of these fail, the artifact should not ship.

### 9.2 Required Validators

| Validator | Purpose |
|---|---|
| **Evidence Fidelity Guard** | prevent unsupported claims, drift from source, or fabricated proof |
| **Anti-Centroid Validator** | prevent flattening into generic compromise language |
| **Coalition Coherence Validator** | ensure primitive weights and sequence actually make sense together |
| **Voice Alignment Validator** | ensure the result is aligned with core identity and current best self |
| **Routeability Validator** | ensure the artifact can survive format translation |
| **Mood-State Safety Guard** | ensure render style matches user state and context |

### 9.3 Benchmark Metrics

CCF should not be evaluated only by output volume. Its scorecard should prioritize:

- trigger-to-response rate,
- coalition survival quality,
- downstream acceptance rate,
- edit distance after validator pass,
- signature preservation score,
- format portability score,
- engagement and resonance quality after publication,
- reuse rate in future modules,
- testimonial-worthy outcomes generated from the same source event.

### 9.4 Acceptance Thresholds

Artifacts should meet the following minimum standards:

| Metric | Minimum Standard |
|---|---|
| Evidence lineage completeness | 100% |
| Authenticated source dependency | required |
| Coalition sparsity | no overloaded primitive stacks |
| Render portability | at least 2 intended surfaces without loss |
| Voice alignment | high confidence |
| Validator pass state | no critical failures |

If an artifact only works in one surface because it was overfit, the compiler has not done enough abstraction work.

### 9.5 Revision Loop and Benchmark Learning

Quality control in CCF is not finished when an artifact passes validation. The system must compare intent to outcome and feed that delta back into the benchmark memory. The review loop should ask:

- Did the published artifact create recognition, debate, relief, or action?
- Did the downstream renderer preserve the coalition or subtly betray it?
- Did the coach feel accurately represented?
- Did the asset travel well across social, teaching, and conversion contexts?
- Did a lower-ranked primitive unexpectedly contribute to memorability?

This is why low-score primitives from the audit library should not be discarded automatically. Some operate as accent primitives, recovery primitives, or situational amplifiers. Benchmark learning should therefore track not only which high-MCDA primitives win often, but which lower-ranked ones materially improve specific contexts.

### 9.6 Quality Control as Adoption Infrastructure

In CCP, quality control is not only a production concern. It is an adoption concern. The coach will keep using the ecosystem if what emerges from the factory feels unusually accurate, unusually fast, and unusually like them at their best. That means CCF quality gates are part of the product moat. A good content artifact does not merely perform externally. It deepens trust internally by making the coach feel understood.

---

## 10. Risk Mitigation

### 10.1 Generic Output Risk

**Risk:** The engine compiles safe, competent, but forgettable assets.

**Mitigation:** enforce anti-centroid validation, keep source verbal anchors visible, require coalition explanation, and track edit distance to detect normalization drift.

### 10.2 Research Noise Risk

**Risk:** Sovereign search retrieves too much low-signal material and weakens prompt quality.

**Mitigation:** rely on JIT moment scoring, provenance weighting, category-specific routing, cached winners, and planner-level evidence compression before coach exposure.

### 10.3 Over-Routing Risk

**Risk:** The same event gets over-expanded into too many derivative assets and loses force.

**Mitigation:** require a content manifest with priority surfaces, cap low-value derivative renders, and preserve the strongest artifact first before multiplying.

### 10.4 Experience Leakage Risk

**Risk:** CCF begins to absorb too much experience logic and becomes confused about its role.

**Mitigation:** keep the meaning/experience plane distinction hard. CCF owns meaning compilation. Product experience modules own the sensation of participation, scoring, sharing, and comeback behavior.

### 10.5 Identity Fossilization Risk

**Risk:** The system preserves the coach's past voice so rigidly that it suppresses growth.

**Mitigation:** use the voice alignment rule from PRD-01: alignment with evolving truth outranks static similarity. Allow growth deltas to influence compile choices when they feel integrated.

### 10.6 Determinism Failure Risk

**Risk:** The probabilistic layer becomes so dominant that outputs cannot be debugged or benchmarked.

**Mitigation:** keep packet lineage, deterministic schemas, validator states, and routing contracts explicit. Every artifact must be explainable after the fact.

### 10.7 Empty Scale Risk

**Risk:** The factory scales output volume before it scales truth quality.

**Mitigation:** make authenticated source capture a hard dependency. If real reaction quality drops, generation volume should slow rather than fill the gap with synthetic guesses.

### 10.8 Surface Fragmentation Risk

**Risk:** Different modules consume CCF outputs inconsistently and create multiple competing truths.

**Mitigation:** treat the content artifact manifest as the authoritative source object, require downstream lineage preservation, and audit any module that repeatedly rewrites source meaning.

---

*This document is one of 9 modular PRD modules. Consult PRD_INDEX.md for the complete module registry, cross-reference tables, and agent loading protocol.*


---

## ERA 3 BROWNFIELD ANALYSIS (Functional Requirements)

# Functional Requirements: PRD-02 CCF Content Factory

This document details the functional requirements for the **PRD-02 CCF Content Factory** module, applying the Era 3 (Core-24) Brownfield structural analysis.

---

## 1. Needs to be Built (New Features & Updates)

### 1.1 Trigger-First Execution Flow Enforcement
*   **WHAT feature needs to be built OR Updated:** Enforce the Trigger-First execution flow (signal → provocation → reaction → primitive distillation → compilation) across all content pipelines, physically preventing blank-page generative "prompting".
*   **WHICH Primitives are actively engaging:** STR (Narrative Structure), TRG (Trigger & Hook Design), FRC (Friction & Flow Management).
*   **WHY it needs to be built OR Updated:** Topic-first content generation bypasses authentic human emotion. Generative AI creating content from thin air produces generic, low-conviction "slop" that damages the coach's trust and authority.
*   **SO WHAT (the benefit of this in the CCP ecosystem):** Ensures all content is a genuine extraction of the coach's lived truth. Final assets become highly differentiated, carry real emotional weight, and serve as undeniable authority proof.
*   **WHAT does not need to be built:** The JIT Skill Compiler routines and Weekly Pipeline task automation logic.
*   **WHY it's already perfect how it is (PROOF):** These orchestration mechanisms are fully specified and capable of handling the flow, as detailed in `JIT_Skill_Compiler_Architecture.docx.md`, `FR24_Weekly_Pipeline_Tech_Spec.md`, and `FR11_Activation_Event_Seed_Construction_Tech_Spec.md`.

### 1.2 Archetype Container Routing
*   **WHAT feature needs to be built OR Updated:** Elevate Archetypes (e.g., Achievement Story, Myth Debunk, Observational Humor) into first-class runtime containers. The compiler must structure the meaning into these archetypes *before* any downstream media format (carousel, video) is selected.
*   **WHICH Primitives are actively engaging:** STR (Narrative Structure), PRS (Persuasion), HUM (Humor & Distortion), PSY (Psychological Diagnostics).
*   **WHY it needs to be built OR Updated:** Choosing a media format prematurely destroys the deeper psychological signal. Meaning and narrative structure must be locked in before deciding how it looks on screen.
*   **SO WHAT (the benefit of this in the CCP ecosystem):** Protects the psychological integrity of the coach's message. Whether the final output is a 60-second video or a text thread, the core persuasion geometry remains lethal and intact.
*   **WHAT does not need to be built:** The psychological routing engines and context premise extraction pipelines.
*   **WHY it's already perfect how it is (PROOF):** These foundational routing logics are heavily spec'd and built in `FR18_Psychological_Routing_Brief_Tech_Spec.md`, `FR13_Client_Context_Premise_Map_Tech_Spec.md`, and `FR29_Context_Premise_Extraction_Tech_Spec.md`.

### 1.3 Sovereign Search Integration (SearXNG / SCRE)
*   **WHAT feature needs to be built OR Updated:** Migrate the CRAL research subsystem away from third-party APIs (Serper/Tavily) to the self-hosted Sovereign CRAL Research Engine (SearXNG).
*   **WHICH Primitives are actively engaging:** REF (Referral & Trust-Transfer), SAF (Safety & Trust Signals).
*   **WHY it needs to be built OR Updated:** Generic search returns average, consensus material. Sovereign search allows diagonal queries across custom categories (e.g., anomaly science, tribal vernacular) without hitting API throttles.
*   **SO WHAT (the benefit of this in the CCP ecosystem):** Feeds the factory with high-activation, highly specific cultural pressure signals, ensuring the coach is always reacting to something timely, surprising, and undeniable.
*   **WHAT does not need to be built:** The CRAL Research Subsystem infrastructure itself.
*   **WHY it's already perfect how it is (PROOF):** The research engine architecture is comprehensively specified in `FR14_CRAL_Research_Subsystem_Tech_Spec.md` and `Sovereign_CRAL_Research_Engine_TechSpec_V1.md`.

### 1.4 Export Governance & Anti-Centroid Enforcement
*   **WHAT feature needs to be built OR Updated:** Enforce strict Pydantic validation boundaries on all artifact exports to detect and reject "centroid collapse" (the loss of emotional charge, edge, or idiosyncrasy).
*   **WHICH Primitives are actively engaging:** CON (Contrast & Juxtaposition), VOC (Voice & Audio Intimacy).
*   **WHY it needs to be built OR Updated:** LLMs naturally regress toward the mean, attempting to average conflicting or edgy positions into polite, corporate compromises during data handoffs.
*   **SO WHAT (the benefit of this in the CCP ecosystem):** Protects the coach's signature quirks and sharpest takes from being accidentally flattened, preserving their unique authority in the marketplace.
*   **WHAT does not need to be built:** The baseline validation gating systems and pipeline orchestration.
*   **WHY it's already perfect how it is (PROOF):** Validation rules are already structurally defined in `FR26_Validation_Gate_Tech_Spec.md`, `FR12_Failure_Prevention_Gates_Tech_Spec.md`, and `FR-CA11-08_Content_Machine_Pipeline_Tech_Spec.md`.

---

## 2. Inventory of Specs for CURRENT RELEVANT CCP FEATURES

The following technical specifications map to the foundational capabilities (CA-2, CA-3, CA-4) that act as the irreducible core of PRD-02. **These do NOT need to be built from scratch**; they are already architected, perfect as they are, and ready for deployment.

### Psychological Routing & Intelligence (CA-2)
*   `FR18_Psychological_Routing_Brief_Tech_Spec.md`
*   `FR19_Semantic_Affinity_Guard_Tech_Spec.md`
*   `FR20_Audience_Maturity_Lifecycle_Tech_Spec.md`
*   `FR21_Receipt_Chain_Guard_Tech_Spec.md`
*   `FR22_Anti_Draft_Intelligence_Tech_Spec.md`
*   `FR23_Skill_Fingerprint_ID_Tech_Spec.md`
*   `FR29_Context_Premise_Extraction_Tech_Spec.md`

### CRAL Research Intelligence (CA-3)
*   `FR14_CRAL_Research_Subsystem_Tech_Spec.md`
*   `FR15_Scheduled_Monitor_Agent_Tech_Spec.md`
*   `FR16_Human_Evidence_Bias_Gate_Tech_Spec.md`
*   `FR17_Research_Synthesis_Protocol_Tech_Spec.md`
*   `Sovereign_CRAL_Research_Engine_TechSpec_V1.md`

### Weekly Pipeline & Content Factory Core (CA-4 / CA-11)
*   `FR24_Weekly_Pipeline_Tech_Spec.md`
*   `FR25_Boredom_Ban_Tech_Spec.md`
*   `FR26_Validation_Gate_Tech_Spec.md`
*   `FR-CA11-08_Content_Machine_Pipeline_Tech_Spec.md`
*   `JIT_Skill_Compiler_Architecture.docx.md`

---

## 3. MARKED AS OBSOLETE (For System Removal)

The following capabilities have been superseded by the Core-24 brownfield update and should be permanently removed from the active system architecture:

*   **[OBSOLETE] "Prompt Engineering" Workstations / Manual Text Entry:** The coach interacts with provocations, never blank prompt inputs.
*   **[OBSOLETE] Generic Content Calendars (Topic-First):** Deprecated in favor of Trigger-First event-driven JIT generation.
*   **[OBSOLETE] Third-Party Search APIs (Serper/Tavily):** Deprecated in favor of the Sovereign SearXNG instance.
