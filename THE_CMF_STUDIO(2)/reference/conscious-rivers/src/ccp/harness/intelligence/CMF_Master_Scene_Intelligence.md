# CMF Master Scene Intelligence
## 12-Paper Research Synthesis for Scene Builder & Master Effects Library

**Version:** 1.0  
**Date:** 2026-03-23  
**Status:** Active — Governs all automated composition decisions  
**Depends on:** Conscious Movie Alchemy, 4 Laws of Layered Questions v2, CBAR v1.0  
**Feeds into:** FR-VID-03 (Scene Builder), FR-VID-06 (Effects Library), FR-VID-04 (Audio Engine), FR-VID-01 (Remotion Manifest Assembly), FR-VID-10 (CMF Editor), FR-VID-11 (Project Management / Pipeline Monitor)

---

## Operational Role In The Video Automation Pipeline

This document is not only research context. It is an execution-layer intelligence source for CMF's video automation pipeline.

Its operational role is:

1. Accept raw-video automation inputs such as source mp4 files, transcripts, and srt/caption artifacts after they have been normalized into project artifacts.
2. Provide the compositional intelligence used by Scene Builder and the Master Effects Library.
3. Contribute directly to the Remotion Manifest that becomes the editable project file in the CMF Editor.
4. Constrain regeneration and refinement decisions inside the editor and review pipeline.
5. Improve the final rendered output by making scene composition, effect selection, and timing decisions biologically and structurally valid.

In other words: the subsystem intelligence defined here does not stop at prompt writing. It flows forward into manifest assembly, editing, review, and final render.

## Structure Library Contract

CMF now distinguishes three executable intelligence layers:

1. `intelligence/containers/` for fixed arc-position contracts
2. `intelligence/components/` for interchangeable scene vehicles
3. `intelligence/subsystems/` for research-backed enforcement and scoring units

The canonical container-definition layer now lives in [CMF_Scene_Containers_Definitions.md](CMF_Scene_Containers_Definitions.md).

The canonical component-definition layer now lives in [CMF_Scene_Components_Definitions.md](CMF_Scene_Components_Definitions.md).

The first container library is:

- `intelligence/containers/HOOK/`
- `intelligence/containers/SETUP/`
- `intelligence/containers/CHALLENGE/`
- `intelligence/containers/TURNING_POINT/`
- `intelligence/containers/RESOLUTION/`
- `intelligence/containers/VISION/`

The first component library is:

- `intelligence/components/HOOK/`
- `intelligence/components/SETUP/`
- `intelligence/components/CHALLENGE/`
- `intelligence/components/JUXTAPOSITION/`
- `intelligence/components/TURNING_POINT/`
- `intelligence/components/RESOLUTION/`
- `intelligence/components/ENCOURAGING_CHANGE/`
- `intelligence/components/SYMBOLIC_ECHO/`
- `intelligence/components/FRAME_AND_CONTRAST/`
- `intelligence/components/THE_TEASE/`
- `intelligence/components/VOICE_OF_TRUTH/`
- `intelligence/components/ARCHETYPAL_MOMENT/`
- `intelligence/components/DEMONSTRATION/`
- `intelligence/components/THE_EVIDENCE/`
- `intelligence/components/THE_COMMUNITY/`
- `intelligence/components/THE_PAUSE/`
- `intelligence/components/THE_VIBE/`
- `intelligence/components/THE_VISION/`

## Subsystem Library Contract

The priority implementation path is to turn each creative subsystem into an executable package.

Each subsystem should be authored as:

```text
intelligence/subsystems/CS-{NNN}/
   SKILL.md
   intelligence.md
   config.json
   rules.yaml
```

Meaning:

- `SKILL.md` tells agents how to apply the subsystem in runtime decisions
- `intelligence.md` contains the deep explanation, thresholds, examples, anti-examples, and why
- `config.json` contains machine-readable parameters and scoring thresholds
- `rules.yaml` contains optional compatibility, priority, routing, or enforcement rules

This master document remains the canonical synthesis layer until the full subsystem library is built.

The canonical subsystem-definition layer now lives in [CMF_Creative_Subsystems_Definitions.md](CMF_Creative_Subsystems_Definitions.md). It should be treated as the source document for splitting research insights into package-level `SKILL.md`, `intelligence.md`, `config.json`, and `rules.yaml` assets.

The first packaged subsystem wave is now:

- `intelligence/subsystems/CS-001/`
- `intelligence/subsystems/CS-008/`
- `intelligence/subsystems/CS-024/`
- `intelligence/subsystems/CS-025/`
- `intelligence/subsystems/CS-027/`
- `intelligence/subsystems/CS-032/`

## Runtime Compilation Contract

The 4 Laws and CBAR sections below are not execution targets by themselves. They compile into runtime assets that Scene Builder and editor regeneration can load mechanically.

The concrete asset contract is:

1. `DEP-VID-032` - Layered Questions Runtime Asset
2. `DEP-VID-033` - CBAR Gate Pack
3. `DEP-VID-034` - Constraint Resolution Manifest

The first compiled targets are:

- `intelligence/frameworks/layered_questions_scene_builder.runtime.json`
- `intelligence/frameworks/layered_questions_editor_regeneration.runtime.json`
- `intelligence/gates/cbar_scene_builder_gate_pack.runtime.json`
- `intelligence/gates/cbar_editor_regeneration_gate_pack.runtime.json`

Meaning:

- Scene Builder does not read Part II and Part IV as passive prose; it loads target-specific runtime packs.
- Editor regeneration does not accept a vague patch into the canonical manifest; it must pass the editor-specific runtime packs first.
- Both paths must emit a `DEP-VID-034` Constraint Resolution Manifest before commit.
- Both paths must also emit a standard CMF receipt-chain file so semantic legitimacy and cryptographic proof-of-work stay linked.

---

## Part I: The 30 Insights — Research Mapped to Conscious Movie Alchemy

Each insight is distilled from one or more of the 12 research papers and anchored to a specific Conscious Movie Alchemy principle. The insight describes *what the research proves*, the principle explains *why it matters for us*, and the implementation note describes *what the agent must do*.

---

### ATTENTION & PERCEPTION (Insights 1–7)

**Insight 1 — The 400ms Imprint: First Contact Is Biological, Not Creative**  
*Source: LC4MP, Attention Capture*  
*Alchemy Principle: Prediction Error*

The human brain forms a cognitive imprint — positive or negative — within 400 milliseconds of mobile exposure. This is not a "first impression" in the social sense; it is a biological sorting decision. The orienting response fires *before* conscious evaluation begins. If the first frame triggers cognitive overload (visual clutter, no focal point), the viewer swipes before encoding even starts.

**Agent rule:** Frame 1 of every composition must contain exactly ONE high-contrast focal element positioned in the upper-central third of the 9:16 frame. CLS must be ≤2 for the first 400ms. No exceptions.

---

**Insight 2 — The 2-Second Recognition Window: Faces Explode Attention**  
*Source: Attention Capture, Eye Tracking*  
*Alchemy Principle: Truth Is Recognized, Not Taught*

Between 1.5 and 2.5 seconds of exposure, the brain enters a "recognition explosion" — the fusiform gyrus and amygdala fire simultaneously, identifying faces and attributing emotional states. A single face retains gaze 4x longer than any other element. The Medium Close-Up (MCU) is the ideal shot scale because it places both eyes and mouth within a single foveal glance, eliminating saccadic search cost.

**Agent rule:** Every VULNERABILITY and RECOGNITION scene must use MCU framing with a single face as the primary anchor. The face must be positioned 15–25% from the top of the frame.

---

**Insight 3 — Averted Gaze Transfers Attention: The Coach Directs, Not Competes**  
*Source: Attention Capture*  
*Alchemy Principle: Attention Is Felt, Not Just Given*

When a face on screen looks directly at the camera (mutual gaze), attention stays on the face. When the face averts its gaze toward a text overlay or graphic, 64.48% of viewer attention transfers to where the face is looking (vs 47.79% with mutual gaze). The face becomes a *pointer*, not a destination.

**Agent rule:** When C-Roll text or graphics must be absorbed, the A-Roll face must avert gaze toward the graphic's screen position. Mutual gaze is reserved for VULNERABILITY beats where the connection IS the message.

---

**Insight 4 — The Tyranny of Film: Structured Editing Controls the Brain**  
*Source: Neurocinematics, Eye Tracking*  
*Alchemy Principle: Meaning Emerges from Constraint*

Hitchcock achieved 65% Inter-Subject Correlation (ISC) — meaning 65% of every viewer's cortex was synchronized. An unstructured park clip achieved 5%. The difference is NOT content quality; it is *structural constraint*. Template-based sequencing with a dramatic arc (Intrigue → Vulnerability → Struggle → Empowerment) is not a creative limitation — it is the mechanism that literally synchronizes the audience's brains.

**Agent rule:** Every video must follow the 4-phase arc. Free-form assembly is architecturally prohibited. Structure IS the quality.

---

**Insight 5 — Center Bias on Mobile Is Absolute**  
*Source: Eye Tracking*  
*Alchemy Principle: Constraint Forces Depth*

On 9:16 mobile screens, orbital reserve forces vertical midline dominance. The primary focal zone is 15–40% from the top of the frame. The bottom 20% is a dead zone (platform UI). Critical signaling text belongs in the center-vertical 60%. Subtitles placed in the bottom 20% are fighting biology AND the platform.

**Agent rule:** Safe zones are hard constraints, not guidelines. Primary face: 15–25% from top. Captions: 30–60% from top. Nothing critical in bottom 20% or far-right 15%.

---

**Insight 6 — Edit Blindness: The Audience Doesn't See Your Cuts**  
*Source: Eye Tracking, Film Editing*  
*Alchemy Principle: Story Is the Vessel, Not the Decoration*

Tim Smith's ATCC proves that viewers are functionally blind to edits due to saccadic suppression and inattentional blindness. Match-on-action cuts preserve gaze position across shots. The audience doesn't notice the edit — they experience the *meaning*. This means cut quality is measured by gaze continuity, not visual smoothness.

**Agent rule:** All cuts must preserve the viewer's focal point position. If the focal element is at center-left before the cut, the incoming shot's focal element must also be at center-left. Gaze continuity > transition aesthetics.

---

**Insight 7 — Theta Synchronization: Cuts Are Cognitive Resets, Not Interruptions**  
*Source: Neurocinematics*  
*Alchemy Principle: Surprise Requires Understanding*

EEG research shows that each cut triggers theta-band synchronization (4–8 Hz) in the first 188ms — the brain's "articulation axis" that encodes the new visual and integrates it with the previous shot. Cuts don't interrupt attention; they *reset* it. In high-distraction mobile environments, frequent logically-consistent cuts are the primary tool for maintaining engagement.

**Agent rule:** Treat every cut as a cognitive reset opportunity. The new shot must provide a clear reason for the reset (new information, new angle, new element). Unmotivated cuts waste theta resets.

---

### EMOTION & MEMORY (Insights 8–15)

**Insight 8 — The Golden Zone: Excitation Transfer Peaks at 2–5 Seconds**  
*Source: Excitation Transfer*  
*Alchemy Principle: Vulnerability Precedes Connection*

Zillmann's 3 temporal phases: Phase 1 (0–2s) = body hot + mind aware of source (transfer blocked). Phase 2 (2–5s) = body still hot but mind has moved on = **"Golden Zone"** for misattribution. Phase 3 (10s+) = arousal fully decayed = "retention suicide." The CLS4→CLS1 jump maximizes transfer: hit them hard, then go quiet while they're still physiologically aroused but cognitively shifted.

**Agent rule:** After every high-intensity beat (CLS 4), the next beat must drop to CLS 1–2 within 2–5 seconds. Never follow a CLS 4 with another CLS 4 — it blocks transfer. The quiet moment after the storm is where the audience *feels*.

---

**Insight 9 — Emotional Contamination: Neutral B-Roll Becomes Whatever Surrounds It**  
*Source: Kuleshov Effect*  
*Alchemy Principle: Specificity Creates Universality*

Kuleshov proved that meaning emerges from juxtaposition, not from individual shots. A neutral face paired with a bowl of soup = hunger. Same face paired with a coffin = grief. More critically: emotionally charged A-Roll *contaminates* the perception of neutral B-Roll that follows. The B-Roll doesn't need to "be" emotional — it absorbs the emotion from context.

**Agent rule:** B-Roll selection is governed by the A-Roll emotional state that precedes it, not by the B-Roll's intrinsic qualities. "Appropriate" B-Roll is whatever is *neutral enough* to absorb the preceding emotion without contradiction.

---

**Insight 10 — Cross-Modal Kuleshov: Audio Primes Visual Meaning**  
*Source: Kuleshov Effect, Audio-Visual Congruence*  
*Alchemy Principle: Emotion Is the Amplifier of Meaning*

Happy music makes a neutral face look happy; sad music makes it look sad. The audio track functions as the affective primer for ALL visual content. L-cuts and J-cuts smooth cross-modal integration because they allow the auditory primer to establish the emotional register *before* the visual arrives.

**Agent rule:** Music selection precedes visual selection in the composition pipeline. The audio establishes the emotional field; the visual enters that field. J-cuts (audio leads video) are the default for emotional scene transitions.

---

**Insight 11 — The Peak-End Rule: Only 2 Moments Matter**  
*Source: Peak-End Rule*  
*Alchemy Principle: Value Is What Remains After You're Gone*

Kahneman's Peak-End Rule proves that the "remembering self" evaluates an experience by the average of its most intense moment (the Peak = TURNING POINT) and its final moment (the End = VISION). Duration is neglected. The middle scenes (SETUP, CHALLENGE, RESOLUTION) are functional scaffolding — they provide context but do not drive retrospective evaluation.

**Agent rule:** Allocate 2x VFX/C-Roll complexity budget to the TURNING POINT and VISION scenes. The SETUP and CHALLENGE scenes get standard treatment. The Peak and the End are where brand recall lives.

---

**Insight 12 — The Neuralyzer Effect: The End Must Touch the CTA**  
*Source: Peak-End Rule, LC4MP*  
*Alchemy Principle: Authority Comes from Being Right About What Matters*

TikTok acts as a "memory-wiping Neuralyzer" — prospective memory is significantly impaired by rapid context switching. The END of a video and the behavioral call-to-action (CTA) must be nearly simultaneous. If there's a 3-second gap between the emotional resolution and the CTA, the next video in the feed has already begun the memory wipe.

**Agent rule:** The VISION scene and the CTA must occupy the same 2–3 second window. No fade-to-black. No pause. The emotional high and the action prompt are fused.

---

**Insight 13 — Variable Reward Schedule: Unpredictability > Symmetry**  
*Source: Excitation Transfer, Film Editing*  
*Alchemy Principle: The Question Is Always More Engaging Than the Answer (Information Gap)*

Symmetrical pacing (same duration for every beat, same intensity pattern every video) creates predictability. Predictability = brain conservation mode = ignored. Variable reward scheduling — where the viewer cannot predict when the next emotional hit will arrive — keeps the dopaminergic system engaged throughout.

**Agent rule:** No two consecutive videos from the same campaign should use identical beat timing patterns. The 1/f (pink noise) timing model generates natural-feeling variation: shot durations follow a power-law distribution, not a uniform one.

---

**Insight 14 — Rule of Three Emotional Beats: Complexity Is Death**  
*Source: Kuleshov Effect*  
*Alchemy Principle: Meaning Emerges from Constraint*

Limit to 2–3 emotional beats per 60-second video. More than 3 transitions (Fear→Anger→Joy→Sadness→Hope) produces cognitive stalling. Binary emotions (Fear→Empowerment, Sadness→Joy) are the highest-engagement patterns. The Kuleshov sequence works because it constrains: one emotion contaminates, one emotion resolves.

**Agent rule:** Every video declares a PRIMARY and SECONDARY emotional vector at composition time. No third emotion is allowed. The arc moves from PRIMARY to SECONDARY and resolves. Simplicity is structural integrity.

---

**Insight 15 — 750ms Minimum for Narrative Inference**  
*Source: Kuleshov Effect*  
*Alchemy Principle: Demonstrated Competence Precedes Permission to Be Uncertain*

750 milliseconds is the absolute minimum shot duration for the brain to perform narrative inference — but ONLY if preceded by 2–4 seconds of contextual setup. Without context, the minimum rises to ~2 seconds. This means ultra-fast cuts are only valid AFTER the viewer has been oriented.

**Agent rule:** Shots under 1 second are permitted only after at least 2 seconds of stable context. The HOOK can use rapid cuts; the VULNERABILITY section cannot.

---

### COLOR, LIGHT & MOTION (Insights 16–22)

**Insight 16 — The PAD Model: Color Is Not Aesthetic — It's Dimensional**  
*Source: Color Psychology*  
*Alchemy Principle: Emotion Requires Accuracy*

Color operates on three measurable dimensions: Pleasure (P), Arousal (A), Dominance (D). Valdez & Mehrabian's regression: P = f(Brightness, Saturation), A = f(Saturation, Brightness), D = f(1/Brightness). Saturation and Brightness dominate over Hue. This means two greens with different brightness values evoke *completely different emotional profiles*. Color grading is not a filter selection — it's a PAD vector calibration.

**Agent rule:** Every scene's color grade must match its target PAD vector from the 10 archetype palette. The agent selects archetypes (Personal Low, Hopeful, Gritty Determination, Playful Pop, etc.) based on the emotional vector declared in the scene metadata.

---

**Insight 17 — Warm Color Temperature = Pleasure, Cool = Dominance**  
*Source: Color Psychology*  
*Alchemy Principle: Humans Respond to Accuracy, Not Perfection*

Warm temperatures (2700–4500K) increase Pleasure. Cool temperatures (6500–9000K) increase Dominance. Desaturation + low brightness = authority. On OLED displays (true black), Dominance perception is amplified because the contrast ratio exceeds LCD response curves.

**Agent rule:** VULNERABILITY scenes use warm temperatures (3200–4000K). EMPOWERMENT scenes use cool temperatures (5500–7000K). The temperature shift IS part of the emotional arc.

---

**Insight 18 — Maximize Presence/Arousal Ratio, Not Raw Energy**  
*Source: Camera Motion*  
*Alchemy Principle: Scarcity Is Psychological, Not Physical*

The 16-effect camera motion scoring table rates each motion on Arousal (1–10), Presence (1–10), and CLS (1–5). The insight: the most powerful effects are NOT the highest-arousal ones. The Breathing Effect (Arousal 3, Presence 9) and Z-Space Parallax Sandwich (Arousal 7, Presence 10) create the deepest viewer immersion. Raw energy (Whip Pan, Arousal 8, Presence 4) creates excitement but not *transportation*.

**Agent rule:** Motion effect selection optimizes for Presence/Arousal ratio, not Arousal magnitude. High-Presence/Low-Arousal effects are the default. High-Arousal effects are reserved for the TURNING POINT only.

---

**Insight 19 — Directional Semantics: Camera Movement Carries Meaning**  
*Source: Camera Motion*  
*Alchemy Principle: Novelty Without Relevance Is Noise*

Camera directions have hardwired emotional associations: Up = aspiration/power. Down = loss/submission. Left-to-Right = progress/forward motion. Right-to-Left = conflict/resistance. These are cross-cultural biological responses, not learned conventions. Using them randomly is not "creative freedom" — it's noise.

**Agent rule:** Camera motion direction is dictated by the scene's narrative function. EMPOWERMENT = upward + L-to-R. CHALLENGE = R-to-L or downward. VULNERABILITY = static or slow breathing. The motion direction IS semantic content.

---

**Insight 20 — The 0.6 Parallax Scaling Rule: Phone Screens Need Less**  
*Source: Camera Motion*  
*Alchemy Principle: Constraint Forces Depth*

Vection (the perceptual illusion of self-motion) is achievable on phone screens as small as 10 square degrees — 88% of participants experience it. But parallax depth must be scaled to 60% of desktop values for realism. Over-scaling produces the "video game effect" where parallax feels artificial.

**Agent rule:** All parallax effects use a 0.6 scaling coefficient for mobile-first delivery. Desktop renders can use 1.0. This is not a quality compromise — it's biological calibration.

---

**Insight 21 — The 7-Second Pan Rule: Slow Enough to Encode**  
*Source: Camera Motion*  
*Alchemy Principle: Attention Is Felt, Not Just Given*

Horizontal pans faster than 7 seconds for a full-frame traverse produce visible judder artifacts that break immersion. The pan speed must be calibrated to the display's pixel density and refresh rate. On mobile, this means pans must be notably slower than desktop equivalents.

**Agent rule:** No full-frame horizontal pan completes in less than 7 seconds. If a scene requires faster lateral movement, use a cut + new composition instead of a continuous pan.

---

**Insight 22 — AV Congruence: 20–40% Recall Boost from Alignment**  
*Source: Audio-Visual Congruence*  
*Alchemy Principle: Authenticity Is Non-Negotiable*

Audio-visual congruence produces a 20–40% boost in recall over incongruent pairing. The synchrony window is narrow: audio leads by 75ms (hits) to 131ms (speech), video leads by 188ms (hits) to 258ms (speech). The optimal range is –20ms to +100ms. Strategic incongruence (e.g., happy image + ominous tone for foreshadowing) increases memory salience but impairs comprehension — use only for the TURNING POINT.

**Agent rule:** Audio and visual events must be synchronized within the –20ms to +100ms window. The audio engineer and scene builder share a common timing grid. Incongruence is a deliberate choice reserved for TENSION beats, never a default.

---

### PACING, STRUCTURE & COGNITION (Insights 23–30)

**Insight 23 — The 1/f Pink Noise Pattern: Natural-Feeling Rhythm**  
*Source: Film Editing*  
*Alchemy Principle: Humans Crave Context, Not Content*

Hollywood films converged over 80 years toward a 1/f power spectral density for shot durations — the same pattern found in heartbeats, ocean waves, and music. 1/f is scale-invariant, meaning it applies equally to 60-second videos and 2-hour films. The Voss-McCartney or inverse-FFT algorithm generates these timing vectors. Uniform-duration cuts feel robotic; random-duration cuts feel chaotic; 1/f cuts feel *alive*.

**Agent rule:** Shot duration vectors are generated by the 1/f algorithm, not manually assigned. The algorithm receives the video duration and the target Average Shot Length (ASL 2.5–4.5s for mobile) as inputs and produces a timing grid that has both short-range bursts and long-range variation.

---

**Insight 24 — The Arousal-Pacing Inverse: Hot Content Needs Cold Editing**  
*Source: LC4MP*  
*Alchemy Principle: The Shadow (Complexity requires careful navigation)*

Cognitive overload occurs at a SLOWER pacing rate for arousing content than for calm content. If the content is high-stakes or emotionally intense (VULNERABILITY, TURNING POINT), the editing must slow down. If the content is informational or calm (SETUP), pacing can increase. This is counterintuitive — most editors speed up during emotional peaks. The research says the opposite.

**Agent rule:** CLS and pacing are inversely correlated with content arousal. High-arousal content (CLS 3–4) = longer shot durations (3–5s). Low-arousal content (CLS 1–2) = shorter shot durations (1.5–3s) are permissible. The agent must cross-reference content emotional intensity with structural pacing before committing.

---

**Insight 25 — The 3-Second Retention Cascade: Pass 3s → 65% Watch 10s**  
*Source: Film Editing, Attention Capture*  
*Alchemy Principle: Demonstrated Competence Precedes Permission*

Mobile viewer retention follows a cascade: survive 3 seconds → 65% probability of 10 seconds → 45% probability of 30 seconds. The 1.7-second average decision time means the HOOK must front-load its strongest signal. ASL must be shorter at the start and can lengthen as the viewer commits.

**Agent rule:** The HOOK phase (0–3s) targets ASL of 0.8–1.5s with CLS ≤ 2 (high cut rate, low information density per cut). After 3s, ASL expands to the 1/f-generated vector. The front-load is a one-time investment that buys permission for the rest of the video.

---

**Insight 26 — The One-Face Advantage: Reduce Identity-Tracking Load**  
*Source: LC4MP, Attention Capture*  
*Alchemy Principle: Specificity Creates Universality*

Configural face processing is expensive — every new face forces the brain to allocate encoding resources for individuation. Using a single recognizable face (the coach) across all roles reduces "identity tracking" load, frees resources for message comprehension, and increases perceived brand authenticity through processing fluency.

**Agent rule:** A-Roll defaults to a single primary face per video. Secondary faces are permitted only in B-Roll and only when serving a narrative function (not decoration). The coach IS the face; guest faces are exceptions requiring explicit justification.

---

**Insight 27 — Mayer's Temporal Contiguity: Sync or Lose**  
*Source: Mayer's Principles*  
*Alchemy Principle: Emotion + Insight = Cultural Longevity*

Temporal contiguity yields the highest effect size of all Mayer's 12 principles. The Temporal Binding Window is 160–250ms — visual elements must appear within this window of the corresponding audio event. Visual-leading asynchrony (image before sound) is tolerated better than audio-leading. A graphic that appears 300ms after the coach says the keyword has already *missed the binding window*.

**Agent rule:** C-Roll graphics align to the audio waveform's amplitude peak for the target keyword. The first frame of the graphic appears within –20ms to +160ms of the phonetic onset. This is a hard constraint, not a guideline.

---

**Insight 28 — The Rule of Three Visual Elements: Screen Capacity Is 3**  
*Source: Mayer's Principles*  
*Alchemy Principle: Meaning Emerges from Constraint*

Maximum simultaneous visual elements on a mobile screen: 3 (e.g., 1 coach face, 1 text callout, 1 icon). Four or more simultaneous elements trigger split-attention overload. This is the visual equivalent of the 2–3 emotional beat limit — the channel capacity is hardwired.

**Agent rule:** The compositor enforces a max-3 simultaneous elements gatekeeper. Additional elements must be sequenced across cuts, not stacked. The agent must count elements per frame and reject compositions that exceed 3.

---

**Insight 29 — ISC Predicts Virality: Neural Synchrony = Platform Success**  
*Source: Neurocinematics*  
*Alchemy Principle: Tribal Alignment*

ISC explains 40.4% of variance in Spotify streams. Movie trailers with high ISC predict box office revenue. Anti-smoking ads with high ISC predict actual behavioral change. ISC measures the *collective subconscious response* of a population. When brains synchronize, people share. Structured template-based editing drives ISC toward 65%; ad-hoc assembly sits at 5–18%.

**Agent rule:** ISC is the North Star metric for composition quality. Structure, focal consistency, emotional arc, and cut logic all contribute to ISC. The agent optimizes every decision for maximum audience synchronization, not maximum visual novelty.

---

**Insight 30 — Narrative Phases Map to Neural Networks: The Arc Is Brain Architecture**  
*Source: Neurocinematics, Peak-End Rule*  
*Alchemy Principle: Story Is the Vessel, Not the Decoration*

Each phase of the narrative arc activates different neural networks: Exposition → Default Mode Network. Inciting Incident → Ventral Attention Network. Rising Action → Amygdala + Frontal Lobes. Climax → Multi-network integration (peak ISC). Resolution → Hippocampus (memory encoding). The dramatic arc isn't a creative tradition — it's an instruction set for sequentially activating the brain's processing centers.

**Agent rule:** Scene type metadata (HOOK, SETUP, CHALLENGE, TURNING_POINT, RESOLUTION, VISION) directly determines which editing parameters are applied. Each phase has a distinct CLS target, ASL target, motion effect palette, and color temperature range. These are not suggestions — they are biologically derived specifications.

---

## Part II: The 4 Laws of Layered Questions Applied to Scene Composition

The 4 Laws were designed for coaching question generation. Applied to scene composition, they become the agent's internal reasoning engine for deciding *what to show, when, and why*.

This is one of the most important legitimacy frameworks in the pipeline. It should be treated as runtime composition logic for Scene Builder, Effects selection, manifest assembly, and editor regeneration review. A scene that does not pass the 4 Laws may be visually attractive and still be structurally false.

### Detection Mode → Composition Strategy

| Detection Mode | In Coaching | In Scene Composition |
|:---|:---|:---|
| **TENSION** | *"I never thought of it that way"* | **The HOOK and TURNING POINT.** Prediction Error via visual surprise, unexpected juxtaposition, pattern-breaking cuts. Deploy strategic incongruence, Kuleshov-sequence reversals, high-contrast color shifts. |
| **VULNERABILITY** | *"You're human like me"* | **The SETUP and CHALLENGE.** MCU on face, warm color temperature, Breathing Effect motion, slow pacing (ASL 4–5s), J-cuts for audio-led emotional entry. Quiet. Intimate. CLS 1–2. |
| **RECOGNITION** | *"That's exactly what I feel"* | **The RESOLUTION and VISION.** Specific visual details the audience recognizes — not generic stock. Cultural accuracy. Tight B-Roll of real objects, real environments.  Color archetype must match tribe aesthetic. |

### The Compression Protocol Applied to Composition Layers

| Layer | In Coaching | In Composition |
|:---|:---|:---|
| **Layer 0 (Raw)** | 12 single-mode questions | 12 raw scene parameters: color, motion, CLS, ASL, font, position, B-Roll type, music key, transition type, focal element, text density, audio sync offset |
| **Layer 1 (Compressed)** | 6 dual-mode questions | 6 composition decisions that merge parameters: "warm MCU with slow breathing = VULNERABILITY anchor" (merges color temp + shot scale + motion) |
| **Layer 2 (Ultra-Dense)** | 3 triple-mode questions | 3 scene-level directives that trigger cascading parameter sets: "TURNING POINT at CLS 4" auto-resolves to → cool color shift, fast cuts, upward camera motion, Z-parallax, audio climax, high-contrast text, peak VFX budget |

### The Density Test Applied to Composition

A properly composed scene simultaneously:
1. **Breaks a prediction** (TENSION) — the viewer didn't expect this visual shift
2. **Exposes a cost** (VULNERABILITY) — the composition shows something raw, not polished
3. **Articulates an unnamed feeling** (RECOGNITION) — the specific visual details make the audience think "that's MY life"

All 3 in one composition = maximum ISC. The agent's goal is Layer-2 density in every TURNING POINT and VISION scene.

### The Unpredictability Gate Applied to Composition

**Law 4 axiom:** Quality is inversely proportional to predictability.

Applied: If the agent's composition choice for Scene N is predictable from Scene N-1, it fails the gate. Specifically:
- If CHALLENGE used warm tones, TURNING POINT must NOT use warm tones
- If SETUP used slow pans, CHALLENGE must NOT use slow pans
- Each beat must violate at least one parameter expectation set by the previous beat

The 1/f algorithm handles timing unpredictability. The agent must also enforce **parameter unpredictability** across consecutive beats.

---

## Part III: Feature List Enrichment — Research-Backed Specifications

Each subsystem feature now has precise thresholds, algorithms, and scoring models derived from the 12 papers.

These specifications are not isolated feature notes. They are the data that should feed:

- Scene Builder decisions
- Master Effects selection
- Audio timing and congruence rules
- Remotion Manifest assembly
- CMF Editor refinement and regeneration

### Scene Builder Subsystem

| Feature | Research Basis | Precise Specification |
|:---|:---|:---|
| **Shot duration generator** | Film Editing (1/f) | Voss-McCartney algorithm; target ASL 2.5–4.5s; α ≈ 1.0 power spectral density |
| **CLS scoring engine** | LC4MP | 5-level scale; Vii (7 dimensions of visual information) per cut; CLS × Content Arousal interaction matrix |
| **Focal zone enforcer** | Eye Tracking | Primary face: 15–25% from top; Captions: 30–60%; Dead zone: bottom 20% |
| **Gaze continuity checker** | Eye Tracking, ATCC | Pre/post-cut focal element position delta ≤ 15% of frame width |
| **Emotion arc validator** | Peak-End Rule, Kuleshov | Max 2 emotional vectors per video; binary transitions only; Rule of Three ceiling |
| **Excitation transfer timer** | Excitation Transfer | CLS 4→CLS 1 transition within 2–5s; never CLS 4→CLS 4 |
| **Visual element counter** | Mayer's Principles | Max 3 simultaneous elements per frame |
| **Shot minimum enforcer** | Kuleshov Effect | 750ms minimum after ≥2s context; 2s minimum without context |
| **Front-load ASL compressor** | Attention Capture, Film Editing | HOOK phase ASL 0.8–1.5s; post-3s expands to 1/f vector |

### Effects Library Subsystem

| Feature | Research Basis | Precise Specification |
|:---|:---|:---|
| **PAD color vector mapper** | Color Psychology | 10 archetype PAD vectors; P = f(B,S), A = f(S,B), D = f(1/B) |
| **Color temperature controller** | Color Psychology | VULNERABILITY: 3200–4000K; EMPOWERMENT: 5500–7000K; CHALLENGE: 4500–5500K |
| **Motion effect scorer** | Camera Motion | 16-effect table (M-01–M-16); optimize Presence/Arousal ratio, not raw Arousal |
| **Directional semantic enforcer** | Camera Motion | Up = aspiration; Down = loss; L→R = progress; R→L = conflict |
| **Parallax scaler** | Camera Motion | 0.6 coefficient for mobile; 1.0 for desktop |
| **Pan speed limiter** | Camera Motion | Minimum 7s for full-frame horizontal traverse |
| **Breathing effect engine** | Camera Motion | M-12: Arousal 3, Presence 9; default for VULNERABILITY scenes |

### Audio Engine Subsystem

| Feature | Research Basis | Precise Specification |
|:---|:---|:---|
| **AV synchrony enforcer** | Audio-Visual Congruence | –20ms to +100ms window; audio-lead ≤ 75ms; visual-lead ≤ 188ms |
| **Temporal binding aligner** | Mayer's Principles | C-Roll first frame within –20ms to +160ms of keyword phonetic onset |
| **Music-emotion primer** | Kuleshov Effect, AV Congruence | Music key/mode set BEFORE visual selection; J-cut default for transitions |
| **BPM-to-cut mapper** | Film Editing | 60–80 BPM = 1 cut/4–6s; 90–110 = 1 cut/2–4s; 120–140+ = 1 cut/0.5–2s |
| **Strategic incongruence flag** | AV Congruence | Allowed only in TENSION beats; requires explicit agent justification |
| **Lyrics/verbal conflict detector** | Mayer's Principles | Instrumental-only during narration segments; lyrics only permitted during non-verbal B-Roll |

---

## Part IV: CBAR Gates for Editing Wisdom Constraints

Each gate contains 4-part CBAR questions (Tension → Failure Scenario → Resolution Demand → Downstream Proof) that the agent must resolve BEFORE generating each scene composition.

CBAR Gates are one of the most important enforcement mechanisms in the pipeline. They should not be treated as commentary. They should run as explicit pre-commit checks before:

1. scene composition decisions are accepted
2. effects or motion decisions are locked
3. audio-visual timing is committed into the manifest
4. editor-driven regeneration requests are written back into the canonical project file

---

### GATE SC-01: Color Grade vs. Arc Stage

**Runs before:** Color grading application  
**Constraint Network:** 4 questions

**Q1 — The CLS-Color Tension**

*Tension:* The scene is tagged as TURNING_POINT (target CLS 4, high arousal). The color archetype "Personal Low" (desaturated, low brightness, low arousal PAD vector) was selected because it matches the coach's brand palette.

*Failure Scenario:* If both are applied, the visual communicates "authority/authority" when the narrative demands "climax/intensity." The Peak-End Rule's "snapshot" for this video will be a muted, low-energy frame — destroying the 2x VFX budget investment in the TURNING POINT.

*Resolution Demand:* Which constraint takes precedence — brand palette consistency or arc-stage emotional accuracy? Name the Alchemy principle that governs, and declare what color archetype will actually be used.

*Downstream Proof:* State how the resolved color grade affects the PAD vector received by the Excitation Transfer Timer (does the resolved Arousal level support the CLS 4 target?).

**Q2 — The Temperature-Emotion Tension**

*Tension:* The scene is a VULNERABILITY beat. The color temperature must be warm (3200–4000K). However, the preceding CHALLENGE scene used 3800K, and the Unpredictability Gate (Law 4) prohibits consecutive scenes with similar temperature.

*Failure Scenario:* If the same 3800K is used, the audience perceives no visual shift between CHALLENGE and VULNERABILITY — the emotional transition is invisible. If temperature shifts to cool, it violates the VULNERABILITY warmth rule.

*Resolution Demand:* How does the agent resolve temperature continuity vs. unpredictability? What specific K value will be used, and how is it differentiated from the preceding scene?

*Downstream Proof:* State the delta in PAD-Pleasure between the CHALLENGE and VULNERABILITY scenes and confirm it exceeds the perceptual discrimination threshold.

**Q3 — The OLED Dominance Escalation**

*Tension:* The target device is OLED. True black amplifies Dominance perception. The VISION scene targets high Pleasure (warm, bright) for the "Like" trigger. But the black letterboxing on OLED will introduce unintended Dominance that flattens the Pleasure peak.

*Failure Scenario:* The VISION scene feels authoritative instead of uplifting. The Peak-End "End" snapshot codes as "instructional" rather than "empowering." Likes decrease.

*Resolution Demand:* How does the agent compensate for OLED-induced Dominance in Pleasure-target scenes? Name the specific color adjustment.

*Downstream Proof:* Confirm that the adjusted PAD vector still maps to the target archetype.

**Q4 — Cascade Lock**

Review Q1–Q3 resolutions. Confirm that the total color trajectory across all scenes forms a coherent emotional arc where: HOOK(neutral/high-contrast) → SETUP(warm/moderate) → CHALLENGE(cool-shift/tension) → TURNING_POINT(high-saturation/high-contrast) → RESOLUTION(warm-return) → VISION(bright/warm/premium). Flag any pair of adjacent scenes where the PAD-Pleasure delta is < 0.1 or > 0.8 (both indicate either imperceptible or jarring transitions).

---

### GATE SC-02: Motion Effect vs. Cognitive Load

**Runs before:** Camera motion application  
**Constraint Network:** 4 questions

**Q1 — The Presence vs. CLS Tension**

*Tension:* The Z-Space Parallax Sandwich (M-16) achieves the highest Presence score (10) but costs CLS 3. The scene is VULNERABILITY (target CLS 1–2). Applying M-16 would exceed the CLS budget for this scene type.

*Failure Scenario:* High Presence with excessive CLS forces the viewer into "processing mode" during a scene that should be "feeling mode." Storage (memory encoding) is compromised because encoding is consuming all available resources.

*Resolution Demand:* Which motion effect achieves the highest Presence within the CLS 1–2 budget? Name it, cite its Presence/Arousal/CLS scores, and state why it's the correct choice for VULNERABILITY.

*Downstream Proof:* Confirm that the selected motion effect's CLS + the scene's content arousal rating does not exceed the LC4MP overload threshold in the Interaction Matrix.

**Q2 — The Directional Semantic Tension**

*Tension:* The EMPOWERMENT scene requires upward camera motion (aspiration/power semantics). But the scene depicts a "pulling away" composition (the coach stepping back to reveal a broader context) which semantically requires a downward or zoom-out movement.

*Failure Scenario:* Upward motion with a pulling-away composition creates contradictory signals: the camera says "rising" while the frame says "receding." The viewer's mirror neuron system receives conflicting proprioceptive data, reducing Presence.

*Resolution Demand:* Which constraint governs — the directional semantic rule or the compositional logic? State the resolution and the compensating adjustment.

*Downstream Proof:* Confirm that the resolved motion direction aligns with the scene's position in the PAD-Dominance trajectory.

**Q3 — The Pan Speed vs. Duration Tension**

*Tension:* The scene requires a full-frame horizontal pan. The 7-second pan rule applies. But the scene's allocated duration from the 1/f generator is 4.2 seconds. The pan cannot complete within the scene duration without violating the 7-second rule.

*Failure Scenario:* If the pan runs at 4.2s, judder artifacts appear which break immersion. If the scene extends to 7s, the 1/f timing vector is violated and the rhythm feels unnatural.

*Resolution Demand:* How does the agent resolve this? Name the alternative composition strategy.

*Downstream Proof:* Confirm the chosen alternative preserves the scene's ISC contribution (does it maintain gaze continuity with the adjacent cuts?).

**Q4 — Cascade Lock**

Review Q1–Q3. Confirm that the motion trajectory across all scenes follows the pattern: HOOK(high-energy, quick) → SETUP(static/minimal) → CHALLENGE(lateral/conflict) → TURNING_POINT(peak Presence) → RESOLUTION(deceleration) → VISION(gentle upward/breathing). Flag any consecutive scenes that use the same motion effect.

---

### GATE SC-03: Audio Congruence vs. Visual Rhythm

**Runs before:** Audio-visual synchronization  
**Constraint Network:** 4 questions

**Q1 — The BPM-Cut Mismatch**

*Tension:* The selected music track runs at 128 BPM (mapping to 1 cut/0.5–2s). The current scene is VULNERABILITY (target ASL 4–5s). The beat sync demands cuts every 0.9s but the emotional register demands stability.

*Failure Scenario:* If cuts match the beat, VULNERABILITY feels like a montage — frenetic, not intimate. If cuts ignore the beat, the AV congruence drops below the 20-40% recall boost threshold.

*Resolution Demand:* Does the agent change the music, change the cut rhythm, or use a hybrid approach (beat-sync for micro-accents but phrase-sync for cuts)? State the chosen strategy and cite the beat-vs-phrase synchronization principle.

*Downstream Proof:* Confirm the resolved AV sync offset for each cut remains within the –20ms to +100ms window.

**Q2 — The J-Cut vs. Hard-Cut Tension**

*Tension:* J-cuts are the default for emotional transitions (audio primes the visual). But the transition from CHALLENGE to TURNING_POINT requires a "cognitive reset" (theta synchronization) which is maximized by a hard cut, not a J-cut. J-cuts smooth the transition; the TURNING_POINT requires a shock.

*Failure Scenario:* A J-cut into the TURNING_POINT dilutes the Prediction Error. The Peak-End "Peak" snapshot is weakened because the viewer's brain was pre-primed instead of surprised.

*Resolution Demand:* Which transition type governs at this specific arc position? Name the neuroscientific mechanism that determines priority.

*Downstream Proof:* Confirm that the chosen transition type preserves the CLS 4 target for the TURNING_POINT (hard cuts increase CLS by +1; J-cuts are CLS-neutral).

**Q3 — The Strategic Incongruence Validation**

*Tension:* The agent has flagged a TENSION beat for strategic AV incongruence (happy visual + ominous audio for foreshadowing). Strategic incongruence increases memory salience but impairs comprehension. The scene precedes the TURNING_POINT — will impaired comprehension undermine the Peak?

*Failure Scenario:* The viewer remembers the scene IS unusual but cannot reconstruct WHY. The Kuleshov contamination effect requires comprehension of both shots for meaning to emerge. Impaired comprehension breaks the contamination chain.

*Resolution Demand:* Is the strategic incongruence permitted at this arc position? State the conditions under which it IS and IS NOT appropriate.

*Downstream Proof:* If permitted, confirm that the TURNING_POINT scene provides sufficient context to retroactively resolve the incongruence (information gap closure).

**Q4 — Cascade Lock**

Review Q1–Q3. Confirm the audio trajectory: HOOK(high-energy, beat-sync) → SETUP(lower energy, phrase-sync) → CHALLENGE(building tension, beat-sync returns) → TURNING_POINT(hard cut + audio climax) → RESOLUTION(instrumental only, soft) → VISION(uplifting, warm, keyword-synced CTA). Flag any scene where music energy level contradicts the CLS target.

---

### GATE SC-04: Kuleshov Sequencing vs. Excitation Transfer Timing

**Runs before:** Final scene assembly  
**Constraint Network:** 4 questions

**Q1 — The Contamination Direction Tension**

*Tension:* Kuleshov contamination flows stimulus→reaction (unidirectional). The current sequence shows B-Roll (stimulus) → A-Roll reaction. But the Excitation Transfer model requires the HIGH-CLS shot first (A-Roll at CLS 4) followed by the LOW-CLS shot (B-Roll at CLS 1) for the Golden Zone transfer. These two constraints demand opposite sequencing.

*Failure Scenario:* If Kuleshov sequencing governs (B→A), the excitation transfer is blocked because the low-CLS shot comes first — there's no excess arousal to misattribute. If Excitation Transfer governs (A→B at CLS 4→1), the Kuleshov meaning-flow is reversed — the reaction precedes the stimulus, producing incoherent narrative.

*Resolution Demand:* How does the agent resolve this? Is there a composition structure that satisfies both constraints simultaneously?

*Downstream Proof:* Confirm that the resolved sequence produces both (a) correct Kuleshov meaning-flow AND (b) a valid excitation transfer window of 2–5 seconds between the high and low CLS shots.

**Q2 — The Emotional Density vs. Cognitive Stall**

*Tension:* The agent has composed a 3-beat emotional progression (Fear → Anger → Empowerment) for a 60s video. This violates the Rule of Three ceiling (max 2–3 beats) only at the upper boundary. However, the Arousal-Pacing Inverse rule requires slower pacing for the high-arousal Fear and Anger beats, which may not leave sufficient duration for the Empowerment resolution.

*Failure Scenario:* If all 3 beats are included and Fear/Anger are paced slowly enough for proper encoding, the Empowerment beat is compressed to under 5 seconds — too brief for the Peak-End "End" snapshot to register.

*Resolution Demand:* How many emotional beats can fit in this specific video duration while respecting the Arousal-Pacing Inverse? State whether a beat must be eliminated and which one.

*Downstream Proof:* Confirm that the remaining beats provide a minimum of 10 seconds for the VISION scene (the End snapshot).

**Q3 — The Front-Load vs. Build Tension**

*Tension:* The 3-Second Retention Cascade demands maximum signal compression in the HOOK (ASL 0.8–1.5s, CLS ≤ 2). The Excitation Transfer model demands a low-arousal SETUP after the HOOK to create the misattribution window. But if the HOOK is CLS 2 and the SETUP is CLS 1, the delta is too small to trigger meaningful transfer. The HOOK should be CLS 3–4 for transfer to work, but CLS 3–4 in the first 3 seconds risks cognitive overload → swipe.

*Failure Scenario:* Either the HOOK fails to retain (too complex) or the HOOK→SETUP transition fails to transfer (too similar in CLS).

*Resolution Demand:* What CLS value for the HOOK resolves both constraints? Is the answer CLS ≤ 2 with transfer sacrificed, CLS 3 with front-load risk, or a different structural approach?

*Downstream Proof:* State the expected 3-second retention probability and the expected excitation transfer magnitude for the chosen resolution.

**Q4 — Cascade Lock**

Review Q1–Q3. Confirm that the complete video sequence satisfies: (a) Kuleshov meaning-flow in every A-B-A transition, (b) Excitation transfer Golden Zones exist after every CLS 4 beat, (c) emotional beats ≤ 3, (d) VISION scene ≥ 10s, (e) HOOK retains ≥ 70% past 3s, (f) 1/f timing vector is intact. Produce the Constraint Resolution Manifest as structured JSON.

---

## Part V: Agent Decision Protocol — Putting It All Together

When the Scene Builder agent receives a composition request, it executes this sequence:

```
1. SATURATE: Load scene metadata (arc position, emotional vector, CLS target, duration from 1/f)
2. DETECT: Identify which Detection Mode dominates (TENSION / VULNERABILITY / RECOGNITION)
3. COMPRESS: Select the Layer-2 composition directive that matches the detection mode
   → This auto-resolves 12 raw parameters into one coherent instruction set
4. GATE CHECK: Run CBAR Gates SC-01 through SC-04 BEFORE generating the composition
   → Each gate identifies tensions between the layer-2 directive and specific constraints
   → The agent resolves each tension with a cited rule
   → The Cascade Lock confirms global consistency
5. COMPOSE: Generate the scene composition with all resolved parameters
6. VERIFY: Check the output against the Constraint Resolution Manifest
   → Gaze continuity ✓
   → PAD vector match ✓
   → CLS within budget ✓
   → AV sync within window ✓
   → Visual element count ≤ 3 ✓
   → Shot minimum enforced ✓
```

This is not a creative workflow — it is a constraint satisfaction engine with a creative interface. The agent cannot produce output without first resolving the tensions. The tensions are concrete, not abstract. The resolutions are deterministic for each input configuration. This is CBAR applied to visual composition.

---

## Appendix A: Quick Reference — The 30 Insights Numbered

| # | Insight Name | Source Paper(s) | Alchemy Principle |
|:--|:---|:---|:---|
| 1 | 400ms Imprint | LC4MP, Attention | Prediction Error |
| 2 | 2-Second Recognition Window | Attention, Eye Tracking | Truth Is Recognized |
| 3 | Averted Gaze Transfer | Attention | Attention Is Felt |
| 4 | Tyranny of Film (ISC) | Neurocinematics, Eye Tracking | Meaning from Constraint |
| 5 | Center Bias on Mobile | Eye Tracking | Constraint Forces Depth |
| 6 | Edit Blindness (ATCC) | Eye Tracking, Film Editing | Story Is the Vessel |
| 7 | Theta Sync on Cuts | Neurocinematics | Surprise Requires Understanding |
| 8 | Golden Zone (2–5s) | Excitation Transfer | Vulnerability Precedes Connection |
| 9 | Emotional Contamination | Kuleshov | Specificity Creates Universality |
| 10 | Cross-Modal Kuleshov | Kuleshov, AV Congruence | Emotion Amplifies Meaning |
| 11 | Peak-End Rule | Peak-End Rule | Value Remains After You're Gone |
| 12 | Neuralyzer Effect | Peak-End, LC4MP | Authority from Being Right |
| 13 | Variable Reward Schedule | Excitation Transfer, Film Editing | Information Gap |
| 14 | Rule of Three Beats | Kuleshov | Meaning from Constraint |
| 15 | 750ms Minimum Shot | Kuleshov | Competence Precedes Permission |
| 16 | PAD Color Model | Color Psychology | Emotion Requires Accuracy |
| 17 | Warm=Pleasure, Cool=Dominance | Color Psychology | Accuracy Not Perfection |
| 18 | Presence/Arousal Ratio | Camera Motion | Scarcity Is Psychological |
| 19 | Directional Semantics | Camera Motion | Novelty Without Relevance Is Noise |
| 20 | 0.6 Parallax Scaling | Camera Motion | Constraint Forces Depth |
| 21 | 7-Second Pan Rule | Camera Motion | Attention Is Felt |
| 22 | AV Congruence (20–40% boost) | AV Congruence | Authenticity Non-Negotiable |
| 23 | 1/f Pink Noise Timing | Film Editing | Humans Crave Context |
| 24 | Arousal-Pacing Inverse | LC4MP | The Shadow |
| 25 | 3-Second Retention Cascade | Film Editing, Attention | Competence Precedes Permission |
| 26 | One-Face Advantage | LC4MP, Attention | Specificity Creates Universality |
| 27 | Temporal Contiguity (TBW) | Mayer's Principles | Emotion + Insight = Longevity |
| 28 | Rule of Three Visual Elements | Mayer's Principles | Meaning from Constraint |
| 29 | ISC Predicts Virality | Neurocinematics | Tribal Alignment |
| 30 | Arc = Neural Architecture | Neurocinematics, Peak-End | Story Is the Vessel |

---

*This document is the intelligence foundation for all automated scene composition in the CMF pipeline. Every agent decision must trace to a numbered insight, an Alchemy principle, and a resolved CBAR gate. No composition is valid without this chain of evidence.*
