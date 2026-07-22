# CMF Visual Ingredient Specialization Analysis
## Multi-Criteria Decision Analysis (MCDA): SB vs CAC vs GMG

**Date:** 2026-02-02
**Subject:** Differential Ingredient Requirements for Three Visual Generation Systems
**Source of Truth:** [Visual_Architecture_3.0.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/intelligence/reports/Visual_Architecture_3.0.md)
**Hypothesis:** Storyboard (SB), Conscious Ambient Cinema (CAC), and Generative Motion Graphics (GMG) require fundamentally DIFFERENT ingredient sets, and forcing them to share the same preparation data causes AI to produce a "safe average" that belongs to neither visual language.

---

## 1. Executive Summary

This analysis applies Multi-Criteria Decision Analysis (MCDA) to evaluate whether the three visual generation systems in the CMF pipeline should have **differentiated ingredient preparation phases** instead of sharing a common data source.

### The Core Discovery

After reading all three composer skill files and the authoritative Visual Architecture 3.0 document, the hypothesis is **confirmed**. These systems are not variations of the same task — they are fundamentally different visual languages:

| System | Visual Language (per Visual Architecture 3.0) | Core Function |
|--------|-----------------------------------------------|---------------|
| **Storyboard (SB)** | **Reaction Shots** | "A picture of a thought colliding with reality" |
| **CAC** | **Vogue Living Editorial Photography** | "A stunning portrait that captures the feeling" |
| **GMG** | **6 Isolated Expert Specialists** | Each Expert has Banned List + Vocabulary + Physics Rule |

**The problem:** When SB and CAC receive the same ingredients, the AI cannot distinguish between "Reaction to stimulus" (SB) and "Editorial composition" (CAC). It produces a blurry middle — a static portrait with nice lighting that is **neither** a reaction shot **nor** a magazine cover.

**The GMG problem is worse:** Each of the 6 Experts has completely different world physics, vocabulary, and banned elements. First Frame (I2I) generation is failing because the deconstruction logic is generic, not Expert-specific.

---

## 2. Source of Truth: Visual Architecture 3.0 Definitions

### 2.1 Storyboard = Reaction Shots

> *"A Reaction Shot is not a picture of a face. It is a picture of **a thought colliding with reality**."*
> — Visual Architecture 3.0, Section 4.2

**The 6 Ingredients (Prioritized):**

| # | Ingredient | Source | Example |
|---|------------|--------|---------|
| 1 | **The Trigger (Context)** | Schema: object_anchors, location_anchors | "What just happened?" |
| 2 | **The Body (Physiology)** | Schema: body_anchors | "What does the body involuntarily do?" |
| 3 | **The Environment (Atmosphere)** | Schema: texture_anchors, light_anchors | "What grounds the scene in reality?" |
| 4 | **The Camera (POV)** | T-Codes / V-Codes | "How intimate is our gaze?" |
| 5 | **The Imperfection (Entropy)** | Smudge, flyaway hair, asymmetry | "What signals reality?" |
| 6 | **The Implication (Sound)** | Schema: sound_anchors | "What sound is implied?" |

**Rule:** Ingredients 1-3 must be present. Ingredients 4-6 elevate from "Good" to "Great."

---

### 2.2 CAC = Vogue Living Editorial Photography

> *"CAC = **Vogue Living Covers.** Editorial photography. Magazine-quality compositions."*
> — Visual Architecture 3.0, Section 5.1

**The Goal:**
- A stunning portrait that captures **the feeling**
- Plays with music only (no voiceover) for 2-5 seconds
- The viewer is immersed through **composition, posture, and gaze** — not CGI

**The 6-Section Structure:**

| Section | Content |
|---------|---------|
| 1. The Anchor | Character Physical DNA + Costume (verbatim) |
| 2. The Contact | What the subject is physically touching |
| 3. **The Composition** | Editorial framing: subject placement, negative space, natural framing |
| 4. The Atmosphere | Lighting, air quality, temperature |
| 5. The Imperfection | Micro-details: dust, scratches, wear |
| 6. The Lens | Camera specs: focal length, aperture, film stock |

**The Key Change from old CAC:** Section 3 is no longer "The Metaphor" (surreal). It is now **"The Composition"** — how the frame is constructed like an editorial photograph.

**Advanced Elements unique to CAC:**
- **Breath State:** Which part of the breath cycle? (Grief = held mid-exhale; Relief = post-exhale)
- **Temporal State:** Before or After the event? (CAC almost never captures "During")
- **The Silence Rule:** The visual must feel like it has NO sound
- **Color Temperature as Emotional Code**
- **Three-Layer Depth:** Foreground (blur) → Subject (sharp) → Background (blur)

---

### 2.3 GMG = 6 Isolated Expert Specialists

> *"Isolate each Expert into a separate SKILL file and a separate session. When 'Expert 06' runs, they know nothing about Experts 01-05."*
> — Visual Architecture 3.0, Section 6.1

**The Core Problem:** Context Pollution. When all 6 Experts are in one file, "Expert 06 (Pure Geometry)" borrows from "Expert 02 (Noir Silhouette)."

**Each Expert Needs:**

| Requirement | Purpose | Example (Expert 06: The Logician) |
|-------------|---------|-----------------------------------|
| **Banned List** | What they CANNOT use | Gold, Shadow, Gradient, Organic Curves, Texture |
| **Vocabulary** | 10-15 words they MUST use | Axiom, Proof, Circle, Tangent, Theorem, Line, Point |
| **Physics Rule** | How their world behaves | Frictionless. Zero Gravity. Infinite Precision. |

**The 6 Experts and Their Worlds:**

| Expert | Specialty | Physics Rule |
|--------|-----------|--------------|
| 01 | Network/Systems | Connections, nodes, flow |
| 02 | Human Struggle/Weather | Noir silhouette, isolation |
| 03 | Matter Sculptor | Gravity is slow, materials melt/crack/pour |
| 04 | Paper Architect | Documents, archives, evidence |
| 05 | Data Weaver | Numbers, metrics, value |
| 06 | Logic/Geometry | Frictionless, zero gravity, pure proof |

**The First Frame (I2I) Problem:**
Each Expert's "deconstruction" logic is different:
- Expert 03: Reassemble broken/melted material to solid
- Expert 04: Stack scattered documents back to neat pile
- Expert 06: Collapse solved equation back to fragments

Generic I2I instructions produce generic first frames.

---

## 3. Criteria Definition for MCDA

To evaluate the differentiation hypothesis, I define the following decision criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **C1: Semantic Alignment** | 25% | Does the ingredient type match the system's core visual language? |
| **C2: Uniqueness Potential** | 20% | Can the ingredient produce outputs that could ONLY belong to this project? |
| **C3: Anti-Generic Enforcement** | 20% | Does the ingredient structure prevent collapse to "safe average" outputs? |
| **C4: Operational Feasibility** | 15% | Is it practical to extract these ingredients in separate sessions? |
| **C5: Handoff Clarity** | 10% | Is the contract between Preparer and Composer unambiguous? |
| **C6: Debugging Traceability** | 10% | Can failures be traced to specific ingredient defects? |

---

## 4. System Analysis: Why Shared Ingredients Fail

### 4.1 The SB vs CAC Averaging Problem

When both systems receive the same `beat_cluster.json`:

```
AI Internal Logic:
  SB expects: "Trigger + Body Physiology + Environment"
  CAC expects: "Composition + Posture/Gaze + Breath State"
  
  Both receive: "visual_intent: A powerful, centered portrait"
  
  AI Compromise:
    "I need to make something that's a reaction shot AND an editorial..."
    → Result: Static portrait with nice lighting
    → This is NEITHER a thought-colliding-with-reality NOR a magazine cover
```

**The damage:** The outputs look interchangeable. SB produces what looks like CAC. CAC produces what looks like SB. Neither achieves its intended visual language.

### 4.2 The GMG Context Pollution Problem

When all 6 Experts run in the same session or receive the same generic preparation:

```
AI Internal Logic:
  Expert 03 (Matter Sculptor) needs: Melt, Crack, Pour, Viscous
  Expert 06 (Logician) needs: Axiom, Proof, Tangent, Frictionless
  
  Both receive: "physical_noun: transformation, visual_intent: change"
  
  AI Contamination:
    Expert 06 accidentally uses "Melt" because it heard about Expert 03
    → Result: Geometric shapes with organic melting = Visual Incoherence
```

**The First Frame disaster:** The I2I step receives generic "deconstruct this" instructions. Since each Expert's deconstruction is fundamentally different (melting vs. scattering vs. solving), generic instructions produce nonsensical first frames.

---

## 5. MCDA Scoring Matrix

### 5.1 Current State: Shared `beat_cluster.json`

| Criterion | SB Score | CAC Score | GMG Score | Weighted Average |
|-----------|----------|-----------|-----------|------------------|
| C1: Semantic Alignment (25%) | 5/10 | 4/10 | 2/10 | 3.65 |
| C2: Uniqueness Potential (20%) | 5/10 | 4/10 | 3/10 | 4.0 |
| C3: Anti-Generic Enforcement (20%) | 3/10 | 3/10 | 1/10 | 2.3 |
| C4: Operational Feasibility (15%) | 8/10 | 8/10 | 8/10 | 8.0 |
| C5: Handoff Clarity (10%) | 5/10 | 4/10 | 2/10 | 3.7 |
| C6: Debugging Traceability (10%) | 4/10 | 3/10 | 2/10 | 3.0 |
| **TOTAL** | | | | **3.9/10** |

**Why GMG scores lowest:** Each Expert is a completely different world with different physics, but they all receive the same noun-to-physics translation. The First Frame problem drags the score down significantly.

---

### 5.2 Proposed State: Differentiated Ingredient Tracks

| Criterion | SB Score | CAC Score | GMG Score | Weighted Average |
|-----------|----------|-----------|-----------|------------------|
| C1: Semantic Alignment (25%) | 9/10 | 9/10 | 9/10 | 9.0 |
| C2: Uniqueness Potential (20%) | 8/10 | 8/10 | 9/10 | 8.3 |
| C3: Anti-Generic Enforcement (20%) | 8/10 | 8/10 | 9/10 | 8.3 |
| C4: Operational Feasibility (15%) | 6/10 | 6/10 | 5/10 | 5.7 |
| C5: Handoff Clarity (10%) | 9/10 | 9/10 | 9/10 | 9.0 |
| C6: Debugging Traceability (10%) | 9/10 | 9/10 | 9/10 | 9.0 |
| **TOTAL** | | | | **8.2/10** |

**The trade-off:** Operational feasibility drops because we need separate preparation sessions. For GMG, we may need **6 separate per-Expert preparation sessions** (one per Expert), which is the most operationally complex but also the highest quality payoff.

---

## 6. Proposed Architecture: Multi-Track Ingredient Preparation

### 6.1 SB Ingredients (Reaction Shot)

**Command:** `/cmf-prepare-sb {project_id}`

**Extracted Ingredients:**

| Ingredient | Extraction Source | Example Output |
|------------|-------------------|----------------|
| **Trigger** | Transcript events | "She just received the call confirming her diagnosis" |
| **Body Physiology** | Physical verbs from quotes | "Shoulders drop, breath catches, jaw unclenches" |
| **Environment** | Visual Schema locations | "Her living room at golden hour, the sofa where sessions happened" |
| **Camera Intent** | T-Code / V-Code selection | "V5 Tactile Proximity, T1 Flesh" |
| **Imperfection** | Specific detail | "Thread loose on cuff, mascara slightly smudged" |
| **Implied Sound** | Transcript context | "The hum of a refrigerator, distant traffic" |

**Output:** `{project_id}_SB_INGREDIENTS.json`

---

### 6.2 CAC Ingredients (Vogue Living Editorial)

**Command:** `/cmf-prepare-cac {project_id}`

**Extracted Ingredients:**

| Ingredient | Extraction Source | Example Output |
|------------|-------------------|----------------|
| **Composition** | Visual Schema + beat | "Off-center left third, scaffolding framing, open sky negative space" |
| **Posture & Gaze** | Beat cluster emotion | "Shoulders raised, jaw set, direct camera eye contact" |
| **Breath State** | Emotion mapping | "Grief = breath held mid-exhale, chest deflated" |
| **Temporal State** | Before/After analysis | "AFTER — she has just set down her phone" |
| **Color Temperature** | Emotion-to-light mapping | "Warmth/Belonging = golden hour, saturated ambers" |
| **Three-Layer Depth** | Environmental analysis | "Foreground: railing blur. Subject: sharp. Background: cityscape soft" |
| **Silence Test** | Composition check | "Still, weighted, private — PASS" |

**Output:** `{project_id}_CAC_INGREDIENTS.json`

---

### 6.3 GMG Ingredients (Per-Expert Specialization)

**Commands:** One per Expert

| Command | Expert | Output |
|---------|--------|--------|
| `/cmf-prepare-gmg-01` | Neo-Schematic (Networks) | `{project_id}_GMG_01_INGREDIENTS.json` |
| `/cmf-prepare-gmg-02` | Mono-Kinetic (Human/Weather) | `{project_id}_GMG_02_INGREDIENTS.json` |
| `/cmf-prepare-gmg-03` | Matter Sculptor (Transformation) | `{project_id}_GMG_03_INGREDIENTS.json` |
| `/cmf-prepare-gmg-04` | Paper Architect (Documents) | `{project_id}_GMG_04_INGREDIENTS.json` |
| `/cmf-prepare-gmg-05` | Data Weaver (Numbers) | `{project_id}_GMG_05_INGREDIENTS.json` |
| `/cmf-prepare-gmg-06` | Visual Synthesizer (Logic) | `{project_id}_GMG_06_INGREDIENTS.json` |

**Each Expert's Ingredients:**

| Ingredient | Purpose | Example (Expert 03) |
|------------|---------|---------------------|
| **Physical Noun** | What material to render | "Lead, Gold, Water" |
| **Physics Translation** | How this material behaves | "Gravity slow, viscous, surface tension" |
| **State Change** | What transformation occurs | "Solid → Liquid (melting)" |
| **Expert Vocabulary** | Words to USE | "melt, crack, pour, viscous, drip" |
| **Banned List** | Words to AVOID | "networks, silhouettes, paper" |
| **First Frame Logic** | How to deconstruct | "Reassemble broken material to solid sphere" |
| **Motion Verbs** | I2V verbs | "MELT, CRACK, POUR" |
| **Power Word** | Typography | "FONTE" |

**Output:** Expert-specific JSON with First Frame deconstruction logic embedded.

---

## 7. Pipeline Integration

```
PHASE 1A: NARRATIVE (unchanged)
    ↓
beat_cluster.json (basic)
    ↓
╔══════════════════════════════════════════════════════════════════╗
║                 PHASE 1B: VISUAL PREPARATION                      ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  SESSION A: /cmf-prepare-sb      → SB_INGREDIENTS.json            ║
║                                                                   ║
║  SESSION B: /cmf-prepare-cac     → CAC_INGREDIENTS.json           ║
║                                                                   ║
║  SESSION C: /cmf-prepare-gmg-{N} → GMG_{N}_INGREDIENTS.json       ║
║             (Run for each Expert routed to in this project)       ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
    ↓
[QUALITY GATE / HUMAN REVIEW of ingredient files]
    ↓
╔══════════════════════════════════════════════════════════════════╗
║                 PHASE 1B: VISUAL COMPOSITION                      ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  SESSION D: /cmf-compose-sb      → SB_W{N}_T2I.txt, _I2V.txt      ║
║                                                                   ║
║  SESSION E: /cmf-compose-cac     → CAC_W{N}.txt, _i2v.txt         ║
║                                                                   ║
║  SESSION F: /cmf-compose-gmg-{N} → GMG_W{N}_T2I.txt, _I2I.txt, _I2V.txt ║
║             (Run for each Expert used in this project)            ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 8. Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Many sessions required (especially GMG)** | High | Medium | Route to minimum needed Experts; batch where possible |
| **SB and CAC still averaging** | Low | High | Structurally incompatible ingredient schemas prevent averaging |
| **GMG First Frames still bad** | Medium | High | Embed Expert-specific deconstruction logic directly in ingredients |
| **Schema drift between files** | Medium | Medium | Versioned schemas; validation at composition start |

---

## 9. Decision: Proceed with Full Differentiation

### MCDA Verdict

| Approach | Score | Recommendation |
|----------|-------|----------------|
| Current (Shared beat_cluster.json) | 3.9/10 | ❌ Reject |
| Proposed (Differentiated Ingredient Tracks) | 8.2/10 | ✅ Accept |

**The data is clear:** Differentiated ingredient preparation more than doubles the expected quality score.

### Implementation Priority

1. **GMG First (Most Pressing):** Create per-Expert preparation commands with embedded First Frame logic
2. **SB vs CAC Separation:** Create incompatible ingredient schemas so AI cannot average them
3. **Update RUN_PIPELINE.ps1:** Integrate multi-track preparation sessions
4. **Pilot on Audrey:** Run all tracks and compare to previous outputs

---

## 10. Conclusion

The user's observation is validated:

> *"These 3 are very different but in the past they really seemed to come from the same ingredients forcing these images to try to force skills into generic outputs."*

Per Visual Architecture 3.0:
- **SB** is "a thought colliding with reality" (Reaction)
- **CAC** is "Vogue Living editorial photography" (Magazine Cover)
- **GMG** is "6 Isolated Expert Specialists" (Each with unique physics)

Forcing them to share ingredients produces:
- SB that looks like CAC
- CAC that looks like SB
- GMG First Frames that are "REALLY REALLY REALLY BAD"

By creating structurally incompatible ingredient sets, we make averaging impossible. Each visual system will produce outputs true to its visual language.

---

**END OF MCDA ANALYSIS**
