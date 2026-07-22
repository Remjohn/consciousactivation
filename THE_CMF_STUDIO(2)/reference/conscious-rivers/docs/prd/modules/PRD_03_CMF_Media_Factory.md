---
type: modular-prd
module: PRD-03
title: CMF Media Factory - Sovereign Visual, Sonic, and Assembly Engine
author: John (Product Manager)
date: 2026-05-06
status: Source of Truth
version: 6.0
dependencies:
  - docs/prd/prd.md (Foundation PRD - CA-10, FR-VIS, FR-VID)
  - docs/prd/CMF_Pipeline_Documentation.md
  - docs/prd/modules/PRD_INDEX.md
  - docs/prd/modules/PRD_01_CCP_Platform_Strategy.md
  - docs/prd/modules/PRD_02_CCF_Content_Factory.md
  - docs/prd/modules/PRD_08_Conscious_Primitives.md
source_documents:
  - docs/prd/CMF_Pipeline_Documentation.md
  - docs/prd/prd-update-visual-control-layer.md
  - lab/CCP APRIL Updates/04_Voice_Doctrines/CMF_Visual_Sonic_Orchestration_Brief.md
  - lab/CCP APRIL Updates/02_MCDA_Synthesis/CutClaw_CMF_Feature_Integration_MCDA.md
  - lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md
  - lab/CCP APRIL Updates/05_Core_Experience/Primitive_Conscious_Orchestration_Architecture.md
  - lab/CCP update/Sovereign_Visual_Research_Engine_TechSpec_V1.md
  - lab/CCP update/Trigger_First_Engine_Documentation.docx.md
  - Conscious Architect University/cau_master_curriculum_registry.md
active_primitives:
  meaning_plane: [STR, CON, VOC, VSG, ACT, BUS]
  experience_plane: [FRC, FBK, SAF, PER]
capability_areas: [CA-3, CA-10, FR-APR-03, FR-GA]
---

# PRD-03: CMF Media Factory - Sovereign Visual, Sonic, and Assembly Engine

**Version:** 6.0 | **Status:** Source of Truth | **Date:** 2026-05-06

---

## 1. Purpose and Architectural Claim

The Conscious Media Factory is the visual and sonic rendering arm of CCP. It does not decide what the coach means. It decides how that meaning becomes perceptible, cinematic, memorable, and emotionally legible across video, visuals, carousels, webinar assets, reaction clips, and brand proof objects.

CMF exists because content truth alone is not enough. A powerful idea can still die on screen through weak framing, generic pacing, bad sonic decisions, flat sequencing, or visuals that feel synthetic and socially unbelievable. CCP therefore needs a sovereign media system that can receive high-quality meaning packets from CCF and render them into premium outputs without collapsing into stock aesthetics or AI sludge.

The architectural claim of CMF is:

**CCF compiles the meaning. CMF renders the felt experience of that meaning.**

This distinction is critical. CMF is not just "video editing." It is the controlled translation of a validated coalition signature into:

- visual symbolism,
- narrative beat timing,
- sonic atmosphere,
- bodily presence,
- brand-consistent composition,
- and finished asset assemblies that feel intentional rather than auto-generated.

Like the rest of CCP, CMF remains invisible to the coach as an operating surface. The user does not enter a media workstation. They participate in Telegram coaching, reactions, recordings, webinars, and challenge loops. Behind that experience, CMF performs the heavy visual and sonic transformation work. The front-stage promise stays human: become more compelling, more memorable, more watchable, and more socially legible.

CMF must therefore satisfy six non-negotiable mandates:

1. **Preserve truth under translation.** The source meaning from CCF cannot be cosmetically beautified into falsehood.
2. **Render premium distinctiveness.** Outputs must look authored, branded, and socially credible.
3. **Exploit multimodal leverage.** Visuals, pacing, captions, music, and composition must reinforce one another instead of competing.
4. **Stay sovereign.** The pipeline must progressively replace black-box dependencies with controllable infrastructure.
5. **Support self-translation.** The coach's speaking, reaction, webinar, and field experiences should naturally produce media assets.
6. **Scale without public studio friction.** The coach should not need to become a video operator to benefit from the system.

CMF is therefore best understood as a **rendering constitution** for the platform. It governs how source truth becomes visible and audible at a premium standard.

---

## 2. Core Architecture and Runtime Model

### 2.1 The Three-Phase Media Pipeline

CMF operates as a three-phase engine:

```text
Phase 1: Narrative and media composition
-> Phase 2: Static asset generation and enrichment
-> Phase 3: Automated assembly, sync, captions, and rendering
```

This sequencing matters because CMF is not a one-shot generative video system. It separates concept, asset creation, and assembly so each stage can be validated independently.

### 2.2 The Media Factory Runtime Chain

A standard CMF runtime flow should look like this:

```text
CCF source artifacts
-> narrative arc and beat interpretation
-> visual / sonic / motion prompt composition
-> sovereign visual research and asset planning
-> deterministic control injection
-> static asset generation
-> music and dialogue alignment
-> manifest assembly
-> render orchestration
-> review and benchmark linkage
```

This architecture makes CMF a downstream-but-not-passive consumer of CCF. It depends on CCF for meaning, but it also adds its own rules for shot logic, visual contrast, music sync, framing precision, and surface-specific assembly.

### 2.3 The Seven Runtime Layers

| Layer | Name | Function | Dominant Plane |
|---|---|---|---|
| L1 | **Meaning Intake** | Receive source packets, script spines, and coalition logic from CCF. | Meaning |
| L2 | **Narrative Rendering Model** | Decide arc, beat cluster, and sequence logic for the media surface. | Meaning -> Visual bridge |
| L3 | **Prompt and Asset Composition** | Generate storyboard, GMG, CAC, caption, sonic, and visual research instructions. | Mixed |
| L4 | **Deterministic Control Layer** | Lock identity, pose, expression, framing, and first-frame composition. | Experience support |
| L5 | **Generation Layer** | Produce static image, motion, and sonic source assets. | Mixed |
| L6 | **Assembly Layer** | Build manifest, sync audio, apply captions, transitions, and render timing. | Experience-heavy |
| L7 | **Validation and Benchmarking** | Check fidelity, premium quality, portability, and outcome linkage. | Mixed |

This layered model allows the platform to improve specific sections without rewriting the whole factory. It also keeps CMF from becoming either a generic video editor or a pure generative art experiment.

### 2.4 What Counts as a CMF Output

CMF outputs are broader than short films. The media factory should be able to create:

| Output Family | Examples |
|---|---|
| **Cinematic Video Assets** | witness shorts, rally arcs, confession reels, reaction montages |
| **Structured Social Visuals** | quote visuals, rank cards, debate posters, comparison slides |
| **Carousel and Multi-Frame Packs** | teaching sequences, argument ladders, before/after emotional arcs |
| **Webinar Visual Assets** | first-frame covers, supporting scenes, branded inserts, visual metaphors |
| **Reaction-Derived Motion Assets** | score reveals, side-taking intros, team visuals, hot-topic bumpers |
| **Brand Memory Objects** | testimonials, celebration renders, church/community recognition visuals |

All of these surfaces should share the same rendering philosophy even if they use different pipelines.

### 2.5 Deterministic and Probabilistic Cooperation

CMF also follows the orchestration dichotomy:

- **Deterministic layer:** manifests, timing constraints, render states, control maps, crop rules, caption placement, validator thresholds, asset IDs, lifecycle states, and export governance.
- **Probabilistic layer:** visual prompt expansion, metaphor selection, sonic color, motion interpretation, ambient phrasing, image search reasoning, and aesthetic variation.

This separation is even more important in media than in text. Visual pipelines drift quickly without deterministic controls. At the same time, over-determinism kills emotional vitality. CMF must therefore behave like a constrained art engine, not an uncontrolled image roulette machine.

### 2.6 Media Operating Modes

CMF should support distinct operating modes without changing its constitutional logic:

| Mode | Typical Input | Typical Output |
|---|---|---|
| **Proof Mode** | testimonial, church/community win, breakthrough clip | trust-heavy proof media |
| **Reaction Mode** | Conscious Reactions or debate input | fast authority and polarity media |
| **Teaching Mode** | webinar fragment, explanation spine, coaching insight | instructional visual packs and recap clips |
| **Celebration Mode** | streak win, challenge completion, public recognition | scoreboards, winner visuals, testimony highlights |

These modes help the render commander choose the right balance of cinematic tension, social proof, text density, and polish level.

---

## 3. Data Contracts, Schemas, and Registry Dependencies

### 3.1 Core Input Contracts from CCF

CMF should never start from a blank brief. It must receive structured source truth from CCF, including:

- `CoalitionSignature`
- `EdgeProductPacket`
- `CCFRoutingRecommendation`
- `ContentArtifactManifest`
- `CoachResponseCapture` where relevant
- key evidence anchors and non-negotiable lines

These packets determine the allowed semantic surface. CMF may reinterpret them visually and sonically, but it cannot silently re-author the meaning.

### 3.2 CMF-Specific Packets

CMF needs its own machine-readable packet family:

| Packet | Role |
|---|---|
| **NarrativeRenderProfile** | arc type, emotional engine, pacing curve, cluster structure |
| **BeatClusterPacket** | shot groups, tension phases, symbolic load, visual concept anchors |
| **VisualCompositionBrief** | composition, body/gaze/expression controls, palette, lens, text overlay |
| **SonicRenderProfile** | BPM, stem directives, silence windows, emotional contour, cue map |
| **AssetResearchManifest** | source priorities, search queries, licensing class, composition reference rules |
| **RenderManifest** | timeline assembly instructions, transition math, caption timings, crop rules |
| **RenderEvaluationPacket** | validation outputs, quality scores, failure reasons, reuse recommendations |

These should be machine-readable and lineaged back to their originating content artifact. This gives agents and operators a clean audit trail from meaning to media.

### 3.3 Registry Dependencies

CMF draws heavily from both primitive planes:

- **Meaning primitives** for structure, contrast, performance, visual guidance, sonic intimacy, and persuasion-supporting composition.
- **Experience primitives** for first-frame stopping power, friction removal in recording, score reveal design, pacing of reveals, trust signals, and premium feel.

CMF should also consult the primitive crosswalk because many visual and sonic decisions sit directly on the boundary between meaning and experience. For example:

- a tension-focused contrast primitive may determine shot juxtaposition,
- an intimacy primitive may determine microphone and music spacing,
- a trust primitive may determine whether a scene should feel glossy or human-imperfect.

### 3.3A Relationship to the Semantic Discernment Architecture

CMF now explicitly inherits the Semantic Discernment Architecture (SDA) doctrine defined in:

- `lab/semantic_discernment_architecture_content_engine_v_1.md`
- `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`
- `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`
- `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md`

For CMF, the practical consequence is clear: rendering is not allowed to preserve only emotional intensity while mutating semantic direction. A render can become more cinematic, more compressed, or more symbolically charged, but it must continue to preserve:

- the active **Invariant Field** inherited from CCF,
- the intended **Archetypal Geometry**,
- the admissible **Representation Geometry**,
- and the downstream **Directional Integrity** of the source artifact.

This means CMF should interpret `Invariant Gravity` as a constraint on what symbolic exaggeration is permissible. If a source artifact is highly charged by belonging, sacrifice, authority, or transcendence, the render layer must not cheapen that gravity into stock symbolism, fake epicness, or manipulative prestige theater.

CMF therefore needs to preserve not only narrative arc, but also:

- symbolic density,
- representation drift limits,
- hard-negative distance from deceptive visual neighbors,
- and the long-loop trust effect of repeated aesthetic choices.

### 3.4 Canonical Metadata Requirements

Every CMF asset should expose:

- `asset_id`
- `originating_content_artifact_id`
- `coach_id`
- `render_profile_id`
- `arc_type`
- `beat_cluster_id`
- `control_assets_used`
- `source_urls_or_references`
- `license_class`
- `validator_status`
- `export_targets`
- `benchmark_link`

The media layer cannot be allowed to become a black box. If an image, clip, or render feels wrong, CCP must be able to inspect why it was created.

### 3.5 Asset Lifecycle States

Like CCF, CMF needs explicit lifecycle states:

| State | Meaning |
|---|---|
| **Planned** | render profile and asset plan exist |
| **Composed** | prompts and deterministic controls exist |
| **Generated** | source images, motion clips, or stems exist |
| **Assembled** | timeline manifest is complete |
| **Rendered** | output surface file exists |
| **Validated** | quality gates passed |
| **Benchmarked** | real performance or usage outcomes linked back |

This gives the platform a predictable way to resume, audit, or regenerate media objects without chaos.

### 3.6 Render Tier Contracts

CMF should explicitly support tiered outputs:

- **Preview tier:** fast, good-enough internal inspection
- **Review tier:** operator or coach-facing approval version
- **Final tier:** delivery or publication grade

The important rule is that these tiers are not different truths. They are different confidence and fidelity levels of the same asset lineage. This keeps regeneration and approval logic coherent.

---

## 4. The Architectural Correction CMF Enforces

CMF exists to correct several deep failures in how AI media pipelines are usually built.

### 4.1 Error One: Prompt-Only Visual Generation

Prompt-only pipelines produce fragile, inconsistent results. They treat "confident," "intimate," "authoritative," or "spiritual" as vague language that a model should guess at. CMF rejects this. Visual and sonic meaning must be progressively controlled through composition logic, deterministic aids, and validator feedback.

### 4.2 Error Two: Post-Production as Damage Control

Many systems accept poor raw recordings and try to fix them later with cropping, patching, and rescue edits. CMF prefers **source-level correctness**. This is why the Red Guide framing doctrine matters, why first-frame composition matters, and why capture constraints belong upstream. The best edit is often the one that was made unnecessary by better recording architecture.

### 4.3 Error Three: Media Detached from Meaning

Generic short-form video systems often create "cinematic feeling" without semantic fidelity. They know how to cut dramatically, but not what the emotional or philosophical truth actually is. CMF is downstream of CCF so that visuals and music inherit validated meaning packets rather than inventing a fake mood.

### 4.4 Error Four: Asset Hunting Without Semantic Intelligence

File-name search and generic stock browsing are too shallow. CMF must progress toward sovereign visual retrieval, emotional tagging, and timestamp-level asset intelligence so the system can search for symbolic usefulness, not just object labels.

### 4.5 Error Five: Media Studio Exposure

If the coach has to operate a complex editor to get value, CCP loses the invisible-app advantage. CMF must remain backstage. It should produce premium outputs without forcing the coach into an editing mindset.

### 4.6 Error Six: Beautiful but Untrustworthy AI

Purely synthetic visual polish can destroy trust if it feels too generic, too perfect, or too detached from reality. CMF must therefore balance authored polish with lived proof, real-world assets, intentional imperfections, and social credibility.

---

## 5. Deep Mechanism: Why the Media Factory Works

### 5.1 Arc-Governed Rendering

The strongest idea in the CMF pipeline is that media assembly is governed by narrative arc, not by generic montage logic. A Witness arc, a Rally arc, a Quiet Reflection arc, and a Confrontation arc should not share the same shot grammar, music tempo curve, or reveal pacing.

Arc routing matters because it determines:

- which quotes become spine-worthy,
- how cluster transitions should feel,
- whether tension should rise, pause, loop, or snap,
- what kind of visual metaphor is admissible,
- and what kind of score or silence treatment will preserve the emotional engine.

This makes CMF more than an editor. It makes it a **rendering interpreter of narrative geometry**.

### 5.2 Beat Clusters as Visual Translation Units

Beat clusters are the bridge between script meaning and media construction. They group pieces of meaning into coherent visual obligations:

- what moment is happening,
- what shift is being felt,
- what should be witnessed,
- what symbolic environment is needed,
- and how the viewer should move from one state to the next.

Without beat clusters, media systems either overcut randomly or overexplain visually. Beat clusters preserve story pressure while giving the visual layer a valid unit of translation.

### 5.3 PRIMAL, T-Code, and V-Code Logic

Storyboard and prompt composition become strong when they are based on repeatable interpretive frameworks. The PRIMAL analysis and T-Code / V-Code approach help turn fuzzy emotional content into precise visual and sonic obligations:

- psychological truth,
- relational force,
- identity signal,
- metaphor selection,
- atmosphere,
- liminality and state transition.

This is how the pipeline creates shots that feel related to the coach's meaning instead of simply looking expensive.

### 5.4 Sonic Composition as Narrative Force

Sound is not decoration in CMF. It is a timing and interpretation engine. The music layer must:

- shape anticipation,
- reinforce transitions,
- open and close silence intentionally,
- support rather than drown voice,
- and create emotional coherence between the visual and verbal layers.

The move toward sovereign music generation matters because third-party music APIs limit structural control. CMF wants stem-level mixing, beat extraction, and explicit ducking so the coach's spoken authority remains primary and the music becomes a multiplier rather than a blanket.

### 5.5 Deterministic Visual Control

The visual control layer exists because media pipelines fail when identity, pose, gaze, and expression are left to chance. ConsciousPose, ConsciousSmile, Identity LoRA, and First Frame Composer together create a deterministic scaffold inside the visual generative stack.

Their role is not to make visuals robotic. Their role is to protect:

- coach recognizability,
- intended body language,
- intended expression,
- scroll-stop first impression,
- and continuity across asset families.

In other words, deterministic control protects the premium brand layer from drifting into generic AI outputs.

### 5.6 Sovereign Visual Research and Retrieval

The Sovereign Visual Research Engine matters because the strongest media systems do not rely only on generation. They also know how to find and score the right composition references, documentary sources, known-person imagery, symbolic references, and future archive moments. CMF becomes more powerful as it learns to retrieve visuals by:

- emotional state,
- contradiction value,
- symbolic role,
- framing proximity,
- brand alignment,
- and cultural relevance.

This turns media production from ad hoc browsing into a searchable intelligence system.

### 5.7 Assembly as Cognitive Timing

The final render is not just file concatenation. It is cognitive timing. Cuts, captions, zooms, punch-ins, silence windows, and beat sync all determine whether a viewer feels:

- tension,
- recognition,
- authority,
- relief,
- inspiration,
- discomfort,
- or boredom.

Assembly is therefore one of the most psychologically important parts of CMF. It is where many otherwise decent assets either become potent or collapse.

---

## 6. Implementation Stack and Systems Biology

### 6.1 CMF as a Multimodal Organism

CMF can be read as a biological stack:

| Biological Analogy | CMF Component | Function |
|---|---|---|
| Eyes | SVRE and asset research engines | see the visual world and retrieve usable references |
| Ears | sonic engine and audio parser | detect beat, silence, and vocal priority |
| Skeleton | render manifest and timeline graph | hold the structure upright |
| Muscles | motion engines, zooms, transitions, caption emphasis | create visible movement |
| Skin | brand style, typography, palette, and surface polish | create the perceivable outer identity |
| Memory | vector libraries, beat archives, and render histories | preserve learned references |
| Immune system | quality gates and validator packets | reject distorted or generic outputs |

This helps clarify why CMF needs multiple subsystems. It is not one model call. It is a multimodal physiology.

### 6.2 Major Infrastructure Components

The implementation stack should include:

- sovereign search and visual research via SearXNG-based infrastructure,
- visual scoring and vector storage for archive assets,
- deterministic control assets and registries,
- ComfyUI or equivalent sovereign generation graph,
- music generation and beat parsing infrastructure,
- FFmpeg / Remotion assembly layer,
- caption generation and typographic control,
- render commander and lifecycle orchestrator,
- benchmark and evaluation store.

The goal is progressive sovereignty, not permanent dependence on black-box third parties.

### 6.3 Deterministic Control Layer

The control layer contains:

- **source framing constraints** from the Red Guide and capture UI,
- **First Frame Composer** for initial scroll-stop engineering,
- **ConsciousPose** for body language conditioning,
- **ConsciousSmile** for expression control,
- **Identity LoRA** for persistent coach face fidelity,
- **crop and punch-in safety windows** to prevent ugly reframing.

This layer should be treated as a first-class runtime concern, not a cosmetic add-on.

### 6.4 Audio and Sync Layer

The audio layer should perform:

- stem separation or generation where available,
- ducking around spoken sections,
- silence window detection,
- beat array extraction,
- transition snapping to downbeats where appropriate,
- emotional intensity curve mapping,
- caption-emphasis alignment.

This is one of the clearest areas where CutClaw-style cherry-picking makes sense. CMF should adopt beat-aware synchronization without adopting a generic editing brain.

### 6.5 Render Commander

The render commander should own:

- retries and regeneration logic,
- lifecycle state changes,
- asset dependency validation,
- preview/review/final tier production,
- exception routing,
- and review escalation when deterministic expectations fail.

CMF is too expensive and too consequential to run as a blind batch job. The commander keeps it operationally sane.

### 6.6 Licensing and Reference Governance

SVRE clarified an important rule: some sources are usable as direct media, some only as composition references. CMF must preserve this distinction. An asset plan should know whether a found image or clip is:

- directly usable,
- editorial only,
- stock but licensed,
- composition reference only,
- dead link fallback,
- internally generated,
- or archived coach-owned media.

This protects both compliance and future scalability.

### 6.7 Render Economics and Selective Intensity

Not every asset should consume the same generation budget. The factory should allocate rendering intensity according to strategic value:

- first frames, hero shorts, testimonials, and debate compilations deserve the highest precision,
- low-stakes support visuals can use lighter pipelines,
- archival recovery and internal review assets can use lower-cost paths.

This lets CMF preserve premium quality where it matters most without making the whole system financially brittle.

---

## 7. Workflow Integration Across the Platform

### 7.1 CCF -> CMF Handoff

CCF hands off the meaning packet; CMF interprets it into media. The handoff must be explicit about:

- required lines or phrases,
- non-negotiable emotional turns,
- evidence that must remain legible,
- intended surface families,
- unsafe distortions to avoid.

CMF may intensify, compress, contrast, or symbolize, but it should not secretly replace the content thesis.

### 7.2 Conscious Reactions Integration

Conscious Reactions should become one of CMF's richest input streams. A strong reaction event can produce:

- a fast-turn short,
- a side-taking team visual,
- a score reveal animation,
- a debate compilation,
- a long-form opinion montage,
- future topic wall assets,
- and identity-shaping archive material.

This makes CMF central to the virality and proof loop. It turns recorded reactions into premium public artifacts that make participation feel worthwhile.

### 7.3 CBCS Integration

CBCS does not only need talking-head clips. It also benefits from:

- progress visuals,
- testimonial packs,
- challenge celebration visuals,
- benchmark reveal animations,
- softer explanatory visuals for accountability and recovery moments.

CMF should therefore support both public-social assets and intimate-support assets, with different mood and polish levels where needed.

### 7.4 V2WS and Webinar Delivery

For webinars, CMF should help build:

- branded opener visuals,
- intermediate proof inserts,
- emotional metaphor stills,
- CTA intensification moments,
- recap slides or visual transitions,
- post-webinar recap clips.

This gives the webinar system a far stronger sensory layer than a plain deck.

### 7.5 OFAP and Field Proof

Offline field encounters should feed CMF as documentary truth. If a coach meets people, speaks publicly, gets challenged, or collects strong testimonial moments, CMF should be able to transform those into premium proof artifacts quickly. This is where real-world footage, trusted visual evidence, and social context matter most.

### 7.6 Churches and Community Programs

The church/community vertical especially benefits from CMF because recognition, testimonies, weekly winners, challenge completions, and community identity all become far stronger when rendered publicly with taste. CMF should be able to power:

- Sunday screen recognition visuals,
- testimony highlight reels,
- youth and kids challenge celebrations,
- social evangelisation assets,
- topic-based community reaction montages.

This is one of the clearest examples of media as trust architecture rather than just promotion.

### 7.7 Two-Touchpoint Discipline

Even though CMF is complex, it must remain invisible behind AFFiNE and Telegram. Its outputs should appear as:

- delivered content packs,
- embedded challenge assets,
- reaction clips,
- dashboard-ready proof objects,
- shareable social files.

No separate public-facing CMF editor or render studio should become a third touchpoint.

---

## 8. Self-Translation, Compounding, and Learning Memory

### 8.1 Media as Exhaust of Real Participation

CMF should fully inherit the self-translation principle. The coach should not have to choose between improving and producing. When they react, speak, teach, testify, debate, or practice, CMF should be able to convert those moments into assets.

This changes media production from a parallel job into a compounding byproduct of meaningful participation.

### 8.2 One Event, Many Media Derivatives

One source event can yield:

- one hero short,
- one quote visual,
- one comparison visual,
- one debate intro or reply card,
- one webinar insert,
- one testimonial cut,
- one long-form compilation candidate,
- one archive object for future retrieval.

This is not generic slicing. It is controlled translation across render families.

### 8.3 Archive Intelligence

CMF becomes stronger over time if it stores:

- footage and frame-level semantics,
- high-performing first-frame patterns,
- effective beat-sync choices,
- validated sonic patterns,
- successful crop and composition rules,
- reusable symbolic environments,
- community-recognition templates,
- failure cases and validator misses.

This allows the media system to develop taste memory rather than starting fresh every time.

### 8.4 Agent-Usable Media Metadata

Eventually, agents should be able to query CMF metadata the way they query primitive registries:

- which first-frame patterns work best for debate topics?
- which motion profile performs well for quiet reflection?
- which composition families suit a given coach's brand DNA?
- which sonic curves preserve authority in a church testimonial vs a coach callout?

This is how CMF stops being a one-way renderer and becomes a reusable visual intelligence substrate.

### 8.5 Premium Branding as Moat

The system should take seriously the insight that branding and taste are part of the moat. Too-minimal generic UI and too-generic AI visuals disappear into the feed. CMF should build and preserve a premium branded language that:

- remains consistent,
- feels authored,
- avoids the common AI tell,
- and still leaves room for coach-specific individuality.

This premium consistency compounds trust over time.

---

## 9. Validation, Benchmarks, and Quality Gates

### 9.1 Core Validation Questions

Every CMF output should answer yes to the following:

1. Does the media preserve the source meaning packet?
2. Does it feel premium without feeling fake?
3. Does the framing support the intended emotional engine?
4. Does the sonic layer reinforce rather than obscure the coach?
5. Is the first impression strong enough for the intended surface?
6. Is the asset socially credible and brand-aligned?

If any of these fail, the output is not ready.

### 9.2 Required Validators

| Validator | Purpose |
|---|---|
| **Meaning Fidelity Validator** | ensure the render did not betray the content thesis |
| **Identity Continuity Validator** | ensure the coach still feels like themselves |
| **Expression and Pose Validator** | compare generated output to deterministic control expectations |
| **First Frame Validator** | check hook composition, legibility, and crop safety |
| **Audio Sync Validator** | verify ducking, beat alignment, and dialogue priority |
| **Premium Surface Validator** | catch generic or low-trust aesthetics |
| **Routeability Validator** | ensure the asset fits the intended deployment context |

### 9.3 Benchmark Metrics

CMF should be judged on:

- same-session or same-day delivery rate where applicable,
- first-frame stop quality,
- render acceptance rate,
- regeneration rate,
- identity continuity score,
- caption legibility score,
- beat-sync accuracy,
- downstream performance and social proof creation,
- trust uplift and perceived quality,
- reuse rate of visual patterns and symbolic environments.

These are far more meaningful than just total renders produced.

### 9.4 Acceptance Thresholds

At minimum:

| Metric | Standard |
|---|---|
| Source lineage present | required |
| Meaning fidelity | high confidence |
| Deterministic control pass | no critical drift |
| Audio/dialogue clarity | required |
| First-frame safety | required |
| Premium surface quality | pass |
| Export class validity | required |

An asset that looks impressive but fails lineage or trust is not a win.

### 9.5 Benchmark Learning and Aesthetic Revision

CMF should continuously compare:

- intended arc vs perceived arc,
- chosen symbolic environment vs social response,
- soundtrack assumptions vs viewer feel,
- high-score visual controls vs actual memorability.

This matters because media quality is partly measurable and partly iterative. The platform should not only optimize for click response, but for alignment with the anti-slop and trust architecture. Some assets may perform loudly but damage long-term brand coherence. CMF should learn that difference.

### 9.6 Lower-Score Primitives Still Matter

As with the primitive registry more broadly, not every important media move will come from top-ranked primitives. Some lower-ranked visual or sonic primitives may matter as:

- accent moves,
- tension resets,
- recovery mechanisms,
- emotional punctuation,
- trust-preserving imperfections.

CMF should therefore benchmark them contextually rather than deleting them from consideration.

### 9.7 Revision Loop and Aesthetic Memory

After a render ships, CMF should ask a second-order question: not only "did this asset pass," but "what visual and sonic decisions actually made it work?" The answers should update aesthetic memory around:

- first-frame structures,
- expression presets,
- contrast pairings,
- soundtrack curves,
- caption rhythm,
- and brand-safe imperfection patterns.

This is how the media factory gradually becomes better at taste, not just faster at rendering.

---

## 10. Risk Mitigation

### 10.1 Generic Cinematic Slop Risk

**Risk:** Renders become visually competent but emotionally interchangeable.

**Mitigation:** preserve lineage to CCF meaning packets, enforce first-frame reasoning, require premium surface validation, and benchmark coach-recognition reactions rather than aesthetic smoothness alone.

### 10.2 Deterministic Overconstraint Risk

**Risk:** Strong control systems produce stiff, lifeless visuals.

**Mitigation:** keep deterministic assets as boundaries rather than total creative replacement. Allow aesthetic variation within controlled guardrails.

### 10.3 Source-Level Capture Failure Risk

**Risk:** Poor raw framing or weak recordings force expensive downstream rescue work.

**Mitigation:** invest in capture UI guides, enforce Red Guide framing, preserve source-level poka-yoke design, and treat bad capture as a system problem rather than an editor problem.

### 10.4 Sonic Overreach Risk

**Risk:** Music and sound design overwhelm the spoken message and cheapen authority.

**Mitigation:** prioritize voice clarity, use stem-level ducking, validate dialogue priority, and treat silence as a real compositional tool.

### 10.5 Licensing and Provenance Risk

**Risk:** Mixed-source media leads to unclear rights or unsafe reuse.

**Mitigation:** store asset class, reference class, source URL, and licensing state in all manifests and block ambiguous exports from automated promotion.

### 10.6 Hidden Complexity Risk

**Risk:** The backstage stack becomes so complex that it slows delivery and becomes hard to debug.

**Mitigation:** maintain explicit packet lineage, lifecycle states, commander visibility, and modular render stages. Complexity is acceptable only when inspectable.

### 10.7 Touchpoint Drift Risk

**Risk:** CMF complexity tempts the team into building a visible media dashboard.

**Mitigation:** preserve two-touchpoint discipline. AFFiNE and Telegram stay the user surfaces. CMF remains infrastructure.

### 10.8 Trust Erosion Through Excessive Artificiality

**Risk:** Highly polished AI renders weaken social proof by feeling unreal.

**Mitigation:** preserve documentary assets, intentional imperfections, archived real footage, and human believability as core quality dimensions.

---

*This document is one of 9 modular PRD modules. Consult PRD_INDEX.md for the complete module registry, cross-reference tables, and agent loading protocol.*


---

## ERA 3 BROWNFIELD ANALYSIS (Functional Requirements)

# Functional Requirements: PRD-03 CMF Media Factory

This document details the functional requirements for the **PRD-03 CMF Media Factory** module, applying the Era 3 (Core-24) Brownfield structural analysis.

---

## 1. Needs to be Built (New Features & Updates)

### 1.1 Arc-Governed Rendering & Three-Phase Pipeline
*   **WHAT feature needs to be built OR Updated:** CMF must transition from generic "montage" compilation to Arc-Governed Rendering. Media assembly must respect narrative geometry (e.g., Witness, Rally, Reflection) using Beat Clusters as visual translation units.
*   **WHICH Primitives are actively engaging:** STR (Narrative Structure), PER (Perception & Pacing), FRC (Friction & Flow Management).
*   **WHY it needs to be built OR Updated:** Generic short-form video systems create "cinematic feeling" without semantic fidelity. They overcut randomly, destroying the emotional engine of the source script.
*   **SO WHAT (the benefit of this in the CCP ecosystem):** Ensures that the final video feels authored, intentionally paced, and retains the coach's psychological authority. The media becomes an amplifier of meaning rather than a distraction.
*   **WHAT does not need to be built:** The fundamental video compilation architecture, manifest generation logic, and the Remotion assembly layer.
*   **WHY it's already perfect how it is (PROOF):** These complex systems are heavily spec'd and actively built across `FR-VID-01_Beat_Cluster_Remotion_Manifest_Tech_Spec.md`, `FR-VID-08_Remotion_Composition_Rendering_Tech_Spec.md`, and `FR-VID-09_Video_Pipeline_Commander_Tech_Spec.md`.

### 1.2 Deterministic Visual Control Layer
*   **WHAT feature needs to be built OR Updated:** Establish a deterministic scaffold inside the visual generative stack. This includes enforcing First Frame composition, ConsciousPose, ConsciousSmile, and Identity LoRAs before rendering.
*   **WHICH Primitives are actively engaging:** VIS (Visual Guidance), VOC (Voice & Audio Intimacy), SAF (Safety & Trust Signals).
*   **WHY it needs to be built OR Updated:** Prompt-only visual pipelines (guessing at "confident" or "intimate") produce fragile, generic, or hallucinated AI sludge. Relying purely on probabilistic generation destroys visual trust.
*   **SO WHAT (the benefit of this in the CCP ecosystem):** Protects coach recognizability, enforces intended body language, and ensures the crucial scroll-stop first impression never drifts into generic AI aesthetics. Preserves the premium brand moat.
*   **WHAT does not need to be built:** The control frameworks, expression adapters, and spatial composition engines.
*   **WHY it's already perfect how it is (PROOF):** These exist natively within the CA-10 Visual Control Layer: `FR-VIS-14_ConsciousSmile_Expression_Adapter_Tech_Spec.md`, `FR-VIS-15_ConsciousPose_Body_Language_Library_Tech_Spec.md`, `FR-VIS-16_First_Frame_Composer_Tech_Spec.md`, and `FR-VIS-17_Identity_LoRA_Training_Pipeline_Tech_Spec.md`.

### 1.3 Sovereign Visual Research Engine (SVRE)
*   **WHAT feature needs to be built OR Updated:** Implement SVRE to retrieve visual assets by emotional state, contradiction value, and symbolic role, formally deprecating the use of generic stock-hunting APIs (Serper/Tavily).
*   **WHICH Primitives are actively engaging:** REF (Referral & Trust-Transfer), CON (Contrast & Juxtaposition).
*   **WHY it needs to be built OR Updated:** File-name search and generic stock APIs return average, consensus imagery that feels immediately synthetic to the viewer.
*   **SO WHAT (the benefit of this in the CCP ecosystem):** Provides the CMF with culturally resonant, documentary-style truth that grounds the media in reality, enhancing believability.
*   **WHAT does not need to be built:** The Sovereign Visual Research architecture and the strict Image Type Validity Gates.
*   **WHY it's already perfect how it is (PROOF):** This intelligence is covered extensively in `Sovereign_Visual_Research_Engine_TechSpec_V1.md`, `FR-VIS-09_Image_Sourcing_Hierarchy_Tech_Spec.md`, and `FR-VIS-13_Image_Type_Validity_Gate_Tech_Spec.md`.

### 1.4 Sonic Composition Engine
*   **WHAT feature needs to be built OR Updated:** Implement stem-level audio ducking, beat array extraction, and silence window mapping to ensure the music strictly serves the coach's voice.
*   **WHICH Primitives are actively engaging:** VSG (Visual & Sonic Guidance), VOC (Voice & Audio Intimacy).
*   **WHY it needs to be built OR Updated:** Generic AI sound design often drowns out the spoken message, cheapening the coach's authority and distracting from the core insight.
*   **SO WHAT (the benefit of this in the CCP ecosystem):** Makes the music a force multiplier of the coach's authority, utilizing absolute silence as a compositional tool to maximize narrative impact.
*   **WHAT does not need to be built:** The core audio processing and stem separation engines.
*   **WHY it's already perfect how it is (PROOF):** Completely specified in `FR-VID-06_Audio_Engine_Tech_Spec.md`.

### 1.5 SDA-Aware Representation Geometry Preservation
*   **WHAT feature needs to be built OR Updated:** Extend CMF governance so render planning, beat-cluster design, visual control, and final validation explicitly preserve SDA-level `Representation Geometry`, `Invariant Field`, and `Directional Integrity`, referencing `lab/semantic_discernment_architecture_content_engine_v_1.md`, `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`, `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`, and `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md`.
*   **WHICH Primitives are actively engaging:** STR (Narrative Structure), VSG (Visual & Sonic Guidance), SAF (Safety & Trust Signals), PER (Perception & Pacing).
*   **WHY it needs to be built OR Updated:** A render can currently feel premium while still distorting semantic direction through wrong symbolism, false grandeur, coercive prestige cues, or flattened emotional geometry.
*   **SO WHAT (the benefit of this in the CCP ecosystem):** Protects long-term trust by ensuring the media layer amplifies the right meaning instead of merely amplifying attention. CMF becomes a meaning-preserving renderer, not a style machine.
*   **WHAT does not need to be built:** The underlying CMF assembly, control-layer, and SVRE infrastructure.
*   **WHY it's already perfect how it is (PROOF):** The rendering stack already exists; the missing work is SDA-aware governance over how that stack is allowed to interpret meaning.

---

## 2. Inventory of Specs for CURRENT RELEVANT CCP FEATURES

The following technical specifications map to the foundational capabilities (CA-10, CA-3) that act as the irreducible core of PRD-03. **These do NOT need to be built from scratch**; they are already architected, perfect as they are, and ready for deployment.

### Visual Control Layer (CA-10)
*   `FR-VIS-01_Visual_Composition_Brief_Tech_Spec.md`
*   `FR-VIS-03_PSSL_Prompt_Compilation_Tech_Spec.md`
*   `FR-VIS-04_Visual_Validation_Tech_Spec.md`
*   `FR-VIS-07_Format_Aspect_Ratio_Enforcement_Tech_Spec.md`
*   `FR-VIS-08_Style_Scoping_Tech_Spec.md`
*   `FR-VIS-14_ConsciousSmile_Expression_Adapter_Tech_Spec.md`
*   `FR-VIS-15_ConsciousPose_Body_Language_Library_Tech_Spec.md`
*   `FR-VIS-16_First_Frame_Composer_Tech_Spec.md`
*   `FR-VIS-17_Identity_LoRA_Training_Pipeline_Tech_Spec.md`
*   `FR-VIS-18_Spatial_Composition_Engine_Tech_Spec.md`

### Video Assembly & Manifest Logic
*   `FR-VID-01_Beat_Cluster_Remotion_Manifest_Tech_Spec.md`
*   `FR-VID-06_Audio_Engine_Tech_Spec.md`
*   `FR-VID-07_Caption_Typography_Engine_Tech_Spec.md`
*   `FR-VID-08_Remotion_Composition_Rendering_Tech_Spec.md`
*   `FR-VID-09_Video_Pipeline_Commander_Tech_Spec.md`

### Sovereign Visual Research Engine (SVRE)
*   `Sovereign_Visual_Research_Engine_TechSpec_V1.md`
*   `FR-VIS-09_Image_Sourcing_Hierarchy_Tech_Spec.md`
*   `FR-VIS-12_Known_Persons_Registry_Tech_Spec.md`
*   `FR-VIS-13_Image_Type_Validity_Gate_Tech_Spec.md`

---

## 3. MARKED AS OBSOLETE (For System Removal)

The following capabilities have been superseded by the Core-24 brownfield update and should be permanently removed from the active system architecture. This forms the Master Deletion Inventory for CMF:

*   **[OBSOLETE] Coach-Facing CMF Editor (FR-VID-10):** The Two-Touchpoint Discipline explicitly forbids a third touchpoint. The web-based React/Next.js Manifest Editor built for coaches is deprecated and must be removed.
    *   *Deletion Targets:* `cmf/apps/web/app/editor/`, `cmf/skills/cmf/video/editor/`, and `FR-VID-10_CMF_Editor_Tech_Spec.md`.
*   **[OBSOLETE] Prompt-Only Visual Generation:** Total reliance on probabilistic image generation without deterministic guards (ConsciousPose/Smile) is deprecated.
*   **[OBSOLETE] Third-Party API Visual Search (Serper/Tavily):** Deprecated in favor of the Sovereign Visual Research Engine (SearXNG).
    *   *Modification Targets:* Strip Serper logic from `multi_api_image_search.py`, `aurore_image_sourcing.py`, and related unit tests.
