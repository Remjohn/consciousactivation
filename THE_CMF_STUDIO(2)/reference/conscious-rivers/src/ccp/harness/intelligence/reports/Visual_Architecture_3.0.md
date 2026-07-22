# Visual Architecture 3.0: The Schema-First System

**Date:** January 30, 2026
**Version:** 3.0 (Comprehensive Redesign)
**Context:** System Thinking Analysis of Storyboard, CAC, and GMG Pipelines
**Methodology:** First Principles, System Thinking, SWOT Analysis
**Word Count:** ~2400 Words

---

## 1. Introduction: The Missing Layer

The Visual Pipeline Audit revealed three systemic failures:
1.  **Storyboard:** Signal Entropy (Architect → Photographer → Poet dilutes specificity).
2.  **CAC:** Metaphorical Drift (Surrealism over Subjective Reality).
3.  **GMG:** Context Pollution (6 Experts in 1 file = Average Output).

The root cause is the same across all three: **We are prompting without research.**

If the Script pipeline uses SPR (Sparse Priming Representation) to compress meaning *before* writing, the Visual pipeline needs a **Visual Schema**—a researched, specific, context-bound definition of reality *before* prompting.

This document defines:
1.  **What a Visual Schema is** and how to build it.
2.  **How each pipeline (Storyboard, CAC, GMG) uses the Schema.**
3.  **SWOT Analysis** for each proposed architecture.

---

## 2. First Principle: Recognition Before Creation

### 2.1 The Core Truth

> **"Surprise requires understanding."** —Conscious Movie Alchemy

A visual cannot "surprise" if the viewer doesn't recognize the context. The brain must first say "I know this" before it can say "Wait, that's different."

*   **Recognition Failure:** "A glowing ribcage cathedral." → The brain does not recognize this. It processes it as "CGI." No emotion.
*   **Recognition Success:** "A woman sitting at a kitchen table at 3 AM, the microwave light the only source of illumination." → Everyone has been in a kitchen at 3 AM. The brain recognizes this instantly. Emotion is possible.

### 2.2 The 12 Elements of Visual Familiarity

What makes a visual instantly recognizable? These elements are grounded in visual psychology and human perception—not arbitrary categories.

#### Category A: Human Experience (The Universal)

| # | Element | Definition | CMF Application |
|---|---|---|---|
| 1 | **Universal Human Experiences** | Everyday moments: eating, sleeping, greeting loved ones. | Root CAC scenes in *daily rituals*, not abstract voids. |
| 2 | **Recognizable Emotions** | Genuine smiles, tears, body language. Transcends culture. | The foundation of **Reaction Shots**. Face = Emotion = Recognition. |
| 3 | **Familiar Faces & Body Types** | Evolutionary programming to recognize human forms. | Always include the **Brand Avatar** in frame—partial body counts. |
| 4 | **"Decisive Moment" Timing** | Capturing action at its peak. Feels authentic. | T2I prompts must specify *when* in the gesture we are (mid-wince, not post-wince). |

#### Category B: Environmental Context (The Setting)

| # | Element | Definition | CMF Application |
|---|---|---|---|
| 5 | **Contextual Clues** | Objects that signal settings: classroom desk, hospital bed, kitchen counter. | Extract from transcript—*specific* objects the subject mentions. |
| 6 | **Relatable Daily Life (Human-Scale Spaces)** | Crowded kitchens, cozy bedrooms, familiar streets. | CAC must use **real locations** from transcript, not fantasy voids. |
| 7 | **The "Liminal" or Dreamlike State** | Empty hallways, abandoned spaces feel hauntingly familiar (subconscious memory). | Use for *Dissociation* distortion—the uncanny valley of space. |
| 8 | **Cultural Icons & Symbols** | Eiffel Tower, stop signs, brand logos. | Use culturally-specific symbols from the subject's context (African wax print, French café). |

#### Category C: Visual Grammar (The Technique)

| # | Element | Definition | CMF Application |
|---|---|---|---|
| 9 | **Archetypal Compositions** | Horizons dividing sky/land, centered faces, symmetry. | GMG should use archetypal geometry. Storyboard uses T-Codes/V-Codes. |
| 10 | **Natural Framing** | Doors, windows, trees framing the subject. | Photographer layer should always consider *what frames the subject*. |
| 11 | **Strong Focal Point** | Clear "hero" subject via focus, contrast, or size. | Ban cluttered compositions. One subject, one action. |
| 12 | **Clear Context/Lighting** | Good lighting that makes objects appear as expected. | Light Anchor must be *named* (Golden Hour, Tungsten Interior) not "beautiful light." |

#### Category D: Aesthetic Memory (The Feeling)

| # | Element | Definition | CMF Application |
|---|---|---|---|
| 13 | **Common Color Palettes** | Sunset oranges, ocean blues, forest greens. Hardwired from nature. | GMG Experts should have *nature-derived* palettes, not arbitrary hex codes. |
| 14 | **Nostalgic Aesthetics** | Vintage filters, film grain, retro grading. | CAC can use era-specific aesthetics if relevant to subject's story. |
| 15 | **Light Quality** | Golden hour, harsh midday, blue hour. Emotionally recognized. | Mandatory in every prompt: *What time of day is it?* |
| 16 | **Recurring Visual Tropes** | Graduation cap toss, jumping group photo. Visual shorthand. | Use intentionally or *subvert* intentionally—never by accident. |

**The Rule:** A prompt must leverage **at least 4 of these 16 elements** to guarantee recognition. If the prompt relies on *invented* imagery (Ribcage Cathedrals) instead of *familiar* imagery (Kitchen at 3 AM), it fails.

---

## 3. The Visual Schema: The Pre-Prompting Research Phase

### 3.1 What is a Visual Schema?

A Visual Schema is a **JSON artifact** generated *before* any Composer runs. It is the "Visual SPR"—a compressed, researched definition of the project's specific reality, mapped to the **16 Elements of Visual Familiarity**.

```json
{
  "project_id": "05_50-12 Fitou",
  
  "category_a_human_experience": {
    "universal_experiences": [
      "Working through physical pain",
      "The ritual of arriving at work before dawn"
    ],
    "recognizable_emotions": {
      "primary": "Chronic pain masked by stoicism",
      "secondary": "Pride in craftsmanship",
      "micro_expressions": ["Jaw clench", "Nostril flare", "Eye squeeze"]
    },
    "brand_avatar": {
      "physical_dna": "50-year-old West African male, shaved head, rectangular black-framed glasses",
      "costume": "Mustard/green wax print shirt, work boots"
    },
    "decisive_moments": [
      "The moment his hand presses into his side",
      "The moment he straightens up after aligning bricks",
      "The moment he removes his glasses to wipe sweat"
    ]
  },
  
  "category_b_environmental_context": {
    "contextual_clues": [
      "Construction site with exposed rebar",
      "Stacked bricks in perfect alignment",
      "Cement mixer in background"
    ],
    "human_scale_spaces": [
      "Outdoor construction site (vast, open)",
      "His home interior (implied, intimate)"
    ],
    "liminal_spaces": [
      "Empty construction site at dawn (before workers arrive)",
      "Scaffolding corridor"
    ],
    "cultural_symbols": [
      "West African wax print fabric",
      "French construction site signage"
    ]
  },
  
  "category_c_visual_grammar": {
    "archetypal_compositions": [
      "Man against vast open sky",
      "Hands framing meticulous work"
    ],
    "natural_framing": [
      "Through scaffolding poles",
      "Doorframe of unfinished building"
    ],
    "focal_point_rule": "One man. One action. One emotion.",
    "lighting_contexts": {
      "outdoor_work": "Harsh midday sun, no shade, sharp shadows",
      "indoor_rest": "Warm tungsten, soft shadows"
    }
  },
  
  "category_d_aesthetic_memory": {
    "color_palette": {
      "dominant": "Ochre (dust), Grey (cement), Green (wax print)",
      "accent": "Rust (rebar), Blue (sky)"
    },
    "nostalgic_aesthetic": "Documentary realism, handheld texture",
    "light_quality": {
      "pain_scenes": "Harsh, overexposed, bleaching",
      "order_scenes": "Golden hour, warm, symmetrical shadows"
    },
    "visual_tropes_to_use": [
      "The solitary worker against the machine",
      "Hands at work (macro)"
    ],
    "visual_tropes_to_avoid": [
      "The inspirational sunrise",
      "The triumphant fist pump"
    ]
  },
  
  "subjective_distortions": {
    "pain": {
      "distortion_type": "Isolation",
      "visual_effect": "Shallow depth of field—only he is sharp. Coworkers blur.",
      "texture_emphasis": "Cement dust cracking along skin tension lines"
    },
    "order": {
      "distortion_type": "Symmetry",
      "visual_effect": "Perfect grid alignment. All lines parallel. Calm.",
      "texture_emphasis": "Smooth brick surfaces, clean edges"
    },
    "fatigue": {
      "distortion_type": "Weight",
      "visual_effect": "Low angle, everything looms above him",
      "texture_emphasis": "Sweat mixing with dust on forearms"
    }
  }
}
```

### 3.2 How to Build the Visual Schema

**Source:** The `transcript_clean.md`, `strategy_brief.json`, and `Brand Avatar.md`.

**Process (New Agent: Visual Researcher):**

#### Step 1: Extract Category A (Human Experience)
1.  **Universal Experiences:** What daily rituals does the subject mention? (Eating, working, sleeping, etc.)
2.  **Recognizable Emotions:** What is the SPR? Map to micro-expressions.
3.  **Brand Avatar:** Copy physical DNA verbatim. No paraphrasing.
4.  **Decisive Moments:** Identify 3-5 peak action moments from the script.

#### Step 2: Extract Category B (Environmental Context)
1.  **Contextual Clues:** List all specific objects mentioned in transcript.
2.  **Human-Scale Spaces:** Where does the action take place? Be specific.
3.  **Liminal Spaces:** Are there transition moments? (Dawn, dusk, empty rooms.)
4.  **Cultural Symbols:** What culturally-specific elements are present?

#### Step 3: Define Category C (Visual Grammar)
1.  **Archetypal Compositions:** What classic visual arrangements fit this story?
2.  **Natural Framing:** What physical elements in the space can frame shots?
3.  **Focal Point Rule:** Always one subject, one action, one emotion.
4.  **Lighting Contexts:** Define light for each emotional state.

#### Step 4: Define Category D (Aesthetic Memory)
1.  **Color Palette:** Extract dominant colors from location + costume.
2.  **Nostalgic Aesthetic:** What era/style does this story evoke?
3.  **Light Quality:** Map light quality to emotional beats.
4.  **Visual Tropes:** List tropes to USE and tropes to AVOID.

#### Step 5: Define Subjective Distortions
For each primary emotion in the SPR, define:
*   **Distortion Type:** (Isolation, Symmetry, Weight, Fragmentation, etc.)
*   **Visual Effect:** How does the camera/composition change?
*   **Texture Emphasis:** What physical detail becomes hyper-visible?

---

## 4. Pipeline 1: Storyboard (The Reaction Shot)

### 4.1 System Thinking: The Relay Race Problem

**Current Flow:** Architect → Photographer → Poet → Final Prompt.
**The Entropy:** Each handoff loses 20% of specificity. By the final prompt, the "Micro-Wince" has become "Sad Face."

**The Fix:** The Architect *consumes* the Visual Schema directly. The Schema provides the 6 cues. The Architect's job is to *select* which cues are relevant for this scene, not to invent new ones.

### 4.2 First Principles: The Reaction Shot Formula

A Reaction Shot is not a picture of a face. It is a picture of **a thought colliding with reality**.

**The 6 Ingredients (Prioritized):**

1.  **The Trigger (Context):** What just happened? (From Schema: `object_anchors`, `location_anchors`).
2.  **The Body (Physiology):** What does the body *involuntarily* do? (From Schema: `body_anchors`).
3.  **The Environment (Atmosphere):** What grounds the scene in reality? (From Schema: `texture_anchors`, `light_anchors`).
4.  **The Camera (Point of View):** How intimate is our gaze? (Defined by T-Codes/V-Codes).
5.  **The Imperfection (Entropy):** What is slightly "wrong" that signals reality? (A smudge, a flyaway hair, asymmetry).
6.  **The Implication (Sound):** What sound is implied that the viewer "hears"? (From Schema: `sound_anchors`).

**The Rule:** Ingredients 1-3 must be present. Ingredients 4-6 elevate the shot from "Good" to "Great."

### 4.3 SWOT Analysis: Proposed Storyboard Architecture

| **Strengths** | **Weaknesses** |
| :--- | :--- |
| Architect's "Primal Protocol" is already strong. | Photographer/Poet layers can still dilute. |
| T-Codes/V-Codes provide established constraint. | Over-reliance on "Prose Poetry" risks losing keywords. |

| **Opportunities** | **Threats** |
| :--- | :--- |
| Visual Schema injection ensures Architect has specific cues. | Model bias towards "beauty" over "truth." |
| "Reaction Priority" rule forces face/body focus. | Poetic language is habit—hard to break. |

---

### 5.1 System Thinking: What CAC Actually Is

**The Vision:** CAC = **Vogue Living Covers.** Editorial photography. Magazine-quality compositions.

**The Goal:**
*   A stunning portrait that captures **the feeling**.
*   Plays with music only (no voiceover) for 2-5 seconds.
*   The viewer is immersed in the emotion through **composition, posture, and gaze**—not through CGI or fantasy.

**Current Flow:** Script Quote → Archetype Selection (El Shaddai) → Surreal Prompt.
**The Drift:** The 24 Archetypes ("Ribcage Cathedral," "Body as Container of Light") produce CGI spectacles, not editorial photography.

**The Fix:** Remove Archetypes. Keep the **El Shaddai 6-Section Structure** but replace "The Metaphor" with **"The Composition."**

### 5.2 What to Keep from Current CAC (Good Bones)

| Element | Why It Works |
|---|---|
| **VAE Decoder Protocol** | Forces reasoning before prompting. Semantic Check grounds the emotional truth. |
| **6-Section Prompt Structure** | Anchor → Contact → [Section 3] → Atmosphere → Imperfection → Lens. This is solid. |
| **Motion Spec Rule** | "Only ONE element moves, subject frozen." This IS the Vogue Living aesthetic. |
| **Sensory Stacking** | Touch + Temperature + Sight = Immersion. |
| **Mundane Anchor** | Dust motes, fallen leaves, imperfections = Reality. |
| **Anti-Cliché Gate** | Subverts stock AI art. |
| **Lens/Camera Specs** | Kodak Portra, focal length, aperture = Editorial quality. |

### 5.3 What to Remove (The Problem)

| Element | Why It Fails |
|---|---|
| **24 Archetypes** | "Ribcage Cathedral," "Lightning Veins" = CGI Spectacle, not Editorial Photography. |
| **Section 3: "The Metaphor" (The Impossible Environment)** | This invites surrealism. Replace with composition. |
| **System Message** | "Bridges the real and the surreal" → Should be: "Captures feeling through editorial composition." |

### 5.4 The New 6-Section Structure (Revised)

| Section | Word Count | Content |
|---------|------------|---------|
| 1. **The Anchor** | 20-30 | Character Physical DNA + Costume (verbatim from Brand Avatar) |
| 2. **The Contact** | 20-30 | What the subject is physically touching (grounds the body) |
| 3. **The Composition** | 40-60 | **Editorial framing:** Subject placement, negative space, natural framing, symmetry/asymmetry. |
| 4. **The Atmosphere** | 40-60 | Lighting, air quality, temperature (sensory stacking) |
| 5. **The Imperfection** | 30-40 | Micro-details: dust, scratches, wear, moisture |
| 6. **The Lens** | 30-40 | Camera specs: focal length, aperture, film stock |

**The Key Change:** Section 3 is no longer "The Impossible Environment." It is now **"The Composition"**—how the frame is constructed like an editorial photograph.

### 5.5 The Composition Rules (New Section 3)

To achieve Vogue Living quality, Section 3 must answer:

1.  **Subject Placement:** Where is the subject in the frame? (Rule of thirds? Centered? Off-center?)
2.  **Negative Space:** What occupies the frame without competing with the subject? (Open sea, garden in soft focus, falling rain, snow, wide sky, blurred cityscape.) Negative space doesn't mean "empty" — it means "breathing room."
3.  **Natural Framing (Optional):** If the environment has edges that draw the eye (doorframes, windows, branches, arches), use them. This creates intimacy—"we're glimpsing a private moment." Skip this if the emotion is openness/freedom—let the subject own the whole frame.
4.  **Posture & Gaze:** What does the body tell us? Eyes closed? Looking away? Looking at camera?
5.  **Environment:** A REAL location from the Visual Schema, curated for beauty.
6.  **One Action:** What single gesture captures the feeling?

### 5.6 Motion Spec Rule (Refined)

This is the secret weapon. It's what makes CAC feel cinematic, not static.

**The Core Aesthetic:** A living photograph. The subject is *almost* still, but life continues around and within them.

| Category | What Moves | What Stays Still |
|---|---|---|
| **Body (95% Frozen)** | Subtle: Eyes can blink. Head can tilt slightly. Tears can shed. Nostrils can flare. A single swallow. | Limbs, torso, hands stay locked. Mouth never opens. |
| **Environment (Alive)** | Wind moves fabric/hair. Rain falls. Dust swirls. Smoke curls. Light shifts. Leaves drift. | The architecture, furniture, ground stay fixed. |
| **Focal Emotion** | ONE emotional micro-movement that deepens the feeling. | Everything else serves as contrast. |

**Allowed Facial Micro-Motions:**
*   Eye blink (slow, deliberate)
*   Tear tracking down cheek
*   Head turn (< 10 degrees)
*   Nostril flare
*   Swallow (Adam's apple)
*   Eye focus shift (looking from one point to another)

**Forbidden:**
*   Mouth opening (breaks the silence)
*   Speaking/singing
*   Full body gestures
*   Walking/moving through space

**Environmental Motion Examples:**
*   Wind: Fabric/clothes rustle, hair drifts, leaves swirl
*   Rain: Drops streak the frame, puddles ripple
*   Snow: Flakes fall slowly, accumulate on shoulders
*   Dust: Motes float in light shafts
*   Smoke/Steam: Curls from coffee, breath in cold air
*   Light: Golden hour glow pulses, shadows lengthen

| Parameter | Value |
| **BODY_STRENGTH** | 0.15-0.25 (Very subtle—almost still) |
| **ENVIRONMENT_STRENGTH** | 0.35-0.50 (More visible movement) |
| **DURATION** | 3-5 seconds |

**The Effect:** The stillness of the body + the life of the environment creates a **"Frozen in Time"** feeling. The viewer feels like they've caught a private moment. The subject is processing something—the world continues, but they are suspended in feeling.

### 5.7 Advanced Elements: Maximizing Relatability

These additional elements elevate a CAC from "good photograph" to "moment that lives in memory."

#### 5.7.1 The Breath

Every emotion has a breath pattern. Specify which part of the breath cycle the subject is in:

| Emotion | Breath State | Visual Cue |
|---|---|---|
| **Grief** | Breath held mid-exhale | Chest slightly deflated, shoulders down |
| **Anticipation** | Breath held mid-inhale | Chest expanded, shoulders lifted |
| **Relief** | Post-exhale, emptied | Shoulders dropped, chest neutral, soft |
| **Tension** | Shallow, held | No visible breath movement, throat tight |
| **Processing** | Between breaths | That suspended moment before the next inhale |

#### 5.7.2 The Temporal Question

Is this the moment **BEFORE** or **AFTER** the event? This changes everything.

| Temporal State | Emotional Register | Example (Fitou) |
|---|---|---|
| **Before** | Anticipation, dread, hope | "He is about to press his hand to his side—the pain hasn't hit yet." |
| **During** | Intensity, peak emotion | "His hand is pressing—he is in it." |
| **After** | Processing, aftermath, echo | "His hand has just released—he is feeling the relief spread." |

**The Rule:** CAC almost never captures "During." It captures **Before** (anticipation) or **After** (processing). The peak moment is for Storyboard/A-Roll.

#### 5.7.3 The Silence Rule

The visual must feel like it has NO sound. This reinforces the closed-mouth rule and shapes the entire composition.

**Ask:** "If I muted this image, what would it feel like?"

*   If the answer is "Busy, chaotic, loud" → Wrong composition.
*   If the answer is "Still, weighted, private" → Correct.

**Silence Indicators:**
*   Closed mouth
*   Soft environmental elements (snow, not rain)
*   Distant sounds implied (the traffic is far away)
*   The subject is INSIDE the moment, not reacting to it

#### 5.7.4 Color Temperature as Emotional Code

Map the emotional beat to a color temperature:

| Emotion | Color Temperature | Visual Treatment |
|---|---|---|
| **Grief, Loss** | Cool (blue hour, tungsten shadows) | Desaturated, blue undertones |
| **Warmth, Belonging** | Warm (golden hour, candlelight) | Saturated ambers, skin glows |
| **Numbness, Dissociation** | Neutral (overcast, flat) | Low contrast, no shadows |
| **Tension, Anger** | Hot (harsh midday, tungsten orange) | High contrast, hard shadows |
| **Hope, Possibility** | Mixed (dawn, sun breaking through) | Cool background, warm face |

#### 5.7.5 The "One Imperfect Thing" Focus

Section 5 (Imperfection) already covers this, but emphasize: the imperfection should be **emotionally resonant**, not random.

| Imperfection | What It Communicates |
|---|---|
| Tear track (dried) | Recent crying, now composed |
| Smudged glasses | Too distracted to notice |
| Untucked shirt corner | Sudden exit, or not caring |
| Chapped lips | Neglect of self |
| A single grey hair | Time passing, weight of years |

**The Rule:** The imperfection should tell a micro-story. It's evidence of what the subject has been through.

#### 5.7.6 The Depth Rule (Foreground/Subject/Background)

Editorial photography uses depth to guide the eye and create atmosphere.

| Layer | Content | Focus |
|---|---|---|
| **Foreground** | Environmental element (out of focus): grass, railing, glass | Soft blur (f/1.8-2.8) |
| **Subject** | The person | Sharp focus |
| **Background** | Context (their world) | Soft blur, shapes recognizable |

**The Rule:** All three layers should be present. The foreground "peeks" into frame, creating intimacy—like we're watching from behind something.

### 5.7 Example: Fitou (Revised CAC Prompt)

**Before (El Shaddai / Surreal):**
> "Lightning veins pulse through his flesh. His torso is a glass vessel containing crimson smoke."

**After (Vogue Living / Editorial):**
> **1. THE ANCHOR:** Fitou, 50-year-old West African male, shaved head, rectangular black-framed glasses, deep umber skin catching the harsh light. Costume: Mustard/green wax print shirt, sleeves rolled to elbows, forearms dusty with dried cement.
>
> **2. THE CONTACT:** His right hand presses flat against a stack of perfectly aligned bricks. His left hand rests on his side, fingers digging into the fabric at his waist.
>
> **3. THE COMPOSITION:** Fitou is off-center, occupying the left third of the frame. Behind him, the construction site at golden hour—scaffolding rises like cathedral arches against the amber sky. The scaffolding poles create natural framing, leading lines pointing toward him. Negative space dominates the right two-thirds: open sky, distant cranes in silhouette. His posture is upright but tense—shoulders slightly raised, jaw set. He looks directly at the camera. Eye contact is uncomfortable. Challenging.
>
> **4. THE ATMOSPHERE:** Golden hour light rakes across the site, casting long shadows. The air is thick with dust, visible in the shafts of light. Temperature implied: hot, dry, the end of a long day.
>
> **5. THE IMPERFECTION:** Cement dust cracks along the creases in his forearms. A thin line of sweat traces the crease beside his nose. His glasses have a faint smudge on the left lens.
>
> **6. THE LENS:** Shot on Kodak Portra 400. 50mm lens, f/2.8. Shallow focus on his face/hands, scaffolding soft behind. Vertical 9:16. Low camera angle—he towers over us.
>
> **MOTION SPEC:** SUBJECT: The dust motes floating in the shafts of light. FROZEN: Fitou, the bricks, the scaffolding. STRENGTH: 0.35.

### 5.8 SWOT Analysis: Proposed CAC Architecture

| **Strengths** | **Weaknesses** |
| :--- | :--- |
| Editorial quality = Magazine-cover aesthetic. | Requires understanding of photographic composition. |
| Preserves proven structure (6-Section, Motion Spec). | May feel "less fantastical" to those expecting surrealism. |
| Grounded in Visual Schema = Specific to each project. | Composition rules need clear examples per emotional beat. |

| **Opportunities** | **Threats** |
| :--- | :--- |
| Vogue Living aesthetic is premium, recognizable, shareable. | AI may default to "pretty" over "meaningful" without emotional guidance. |
| Music-only moments become powerful visual punctuation. | Edge cases: How to handle abstract emotions that resist literal composition. |

---

## 6. Pipeline 3: GMG (The Expert Specialist)

### 6.1 System Thinking: The Context Pollution Problem

**Current Flow:** Script Quote → Expert Selection (1-6) → Prompt (all 6 experts in one file).
**The Pollution:** The LLM reads all 6 expert descriptions, so "Expert 06 (Pure Geometry)" subconsciously borrows from "Expert 02 (Noir Silhouette)."

**The Fix:** **Isolate each Expert into a separate SKILL file and a separate session.** When "Expert 06" runs, they know nothing about Experts 01-05. They have never heard of "Gold" or "Shadows."

### 6.2 First Principles: Creativity Within Constraint

You noted that GMG prompts produce "the same exact visual." This is because the constraints are too broad (*Noir Triad*) without being specific enough (*Physics Rules*).

**The Rule:** Each Expert needs:
1.  **A Banned List:** Things they CANNOT use.
2.  **A Vocabulary:** 10-15 words they MUST use.
3.  **A Physics Rule:** How does their world behave?

**Example: Expert 06 (The Logician)**
*   **Banned:** Gold, Shadow, Gradient, Organic Curves, Texture.
*   **Vocabulary:** Axiom, Proof, Circle, Tangent, Theorem, Line, Point, Radius, Angle, Symmetry.
*   **Physics:** Frictionless. Zero Gravity. Infinite Precision. Objects are *defined* not *rendered*.

**Example: Expert 03 (The Sculptor)**
*   **Banned:** White Background, Sharp Edges, Text, 2D Flat.
*   **Vocabulary:** Viscous, Melt, Pour, Fracture, Drip, Surface Tension, Refraction, Weight.
*   **Physics:** Gravity is slow. Everything has mass. Materials obey fluid dynamics.

### 6.3 SWOT Analysis: Proposed GMG Architecture

| **Strengths** | **Weaknesses** |
| :--- | :--- |
| Context Purity eliminates "Average" output. | Requires 6 separate SKILL files (more maintenance). |
| Banned Lists force radical specificity. | May require 6 separate agent sessions (workflow change). |

| **Opportunities** | **Threats** |
| :--- | :--- |
| Each Expert can develop a deep, unique aesthetic. | Risk of repetition if Vocabulary is too narrow. |
| "Creativity within Constraint" produces premium art. | Routing logic (which Expert for which scene?) needs clarity. |

---

## 7. Implementation: The Schema-First Workflow

### 7.1 New Phase: Visual Research

**Before any visual prompt is written:**
1.  **Visual Researcher Agent** reads transcript + Brand Avatar.
2.  **Outputs:** `Visual_Schema.json` (containing the 6 Recognition Cues + Subjective Distortions).
3.  **Schema is passed to:** Storyboard Architect, CAC Composer, GMG Composer.

### 7.2 Session Isolation

*   **Storyboard:** Runs in its own session with the Schema.
*   **CAC:** Runs in its own session with the Schema.
*   **GMG (Expert N):** Runs in its own session with the Schema + ONLY the Expert N SKILL file.

### 7.3 Quality Gate: The Recognition Test

Before any prompt is approved:
> **"Can a human verify this prompt by looking at their own life?"**

*   If the prompt contains a "Ribcage Cathedral" → Fail.
*   If the prompt contains "A kitchen table at 3 AM with a cold cup of coffee" → Pass.

---

## 8. Conclusion: Context is King

The Visual Pipeline Audit identified the "what is broken." This document provides the "how to fix it."

**The Core Shifts:**
1.  **From Invention to Excavation:** Prompts draw from researched cues (Visual Schema), not hallucinated metaphors.
2.  **From Generalism to Specialism:** GMG Experts are isolated, each with their own world.
3.  **From Poetry to Evidence:** Storyboard prioritizes renderable facts over literary beauty.

**The Metric:**
A visual succeeds when the viewer's brain fires a Mirror Neuron Spike. That happens when the brain *recognizes* the context and *simulates* the emotion.

> **Recognition → Simulation → Feeling → Memory.**

This is the path to visuals that are not just "Cool" but "True."

**Status:** Ready for Implementation. Requires:
1.  Visual Researcher Agent (to build Schema).
2.  6 Isolated GMG Expert SKILL files.
3.  Updated CAC Composer (Subjective Distortions, not Archetypes).
4.  Updated Storyboard Architect (Schema injection, Reaction Priority).
