# GMG Skill Implementation Gap Analysis
## Why Style Interpretation Is Failing

**Date:** 2026-02-03
**Subject:** Diagnosis of GMG Skill Dilution from Constitution to Implementation
**Finding:** The SKILL.md files are **truncated summaries** of the source Motion Cookbook guides, losing critical style depth

---

## 1. The Core Problem

> *"The skills really have killed the aesthetic value and quality of each expert"*
> — User Observation

**Confirmed.** After comparing the source Motion Cookbook documents to the implemented SKILL.md files, I found that the skills have:

1. **Lost Visual Lineage References** — The source defines style DNA (Sin City, Nike Motion Posters, Kendrick Lamar videos); the skill has none
2. **Lost Compositional Depth** — The source defines Z-axis dominance, plane layering; the skill has flat word lists
3. **Lost Texture Token Specificity** — The source defines "Analog Truth" tokens per Expert; the skill has generic lists
4. **Lost the "Premium Literal" Philosophy** — The source mandates metaphor → literal translation; the skill skips this

---

## 2. Side-by-Side Comparison: Expert 02

### What the SOURCE GUIDE Says (Motion Cookbook)

**Visual Lineage:**
> "Sin City (High-Contrast Noir), Vogue 'Living Covers,' Nike Motion Posters, Kendrick Lamar Music Videos, The Apple iPod Silhouette Campaign (Updated for 2026), Punk Zine Culture, Gotham City Weather."

**Core Physics Engine:**
> "Elemental Tension: The Avatar provides the Presence; The Weather provides the Motion; The Text provides the Impact."

**Visual Architecture — The 2.5D Collage:**
| Plane | Content | Function |
|-------|---------|----------|
| Plane 0 | Deep Matte Black #050505 | "Active Negative Space" — absorbs light |
| Plane 1 | Typography | Kinetic Element — SINGLE WORD, massive, structural |
| Plane 2 | The Avatar | Rotoscope Cutout — high-fidelity, sharp edges |
| Plane 3 | The Elements | Rain, Fog, Snow — exist BETWEEN planes, bonding Avatar to Void |

**The Elemental Library:**
| Element | Emotion | Motion |
|---------|---------|--------|
| WIND | Chaos, Anxiety, Power | Hair blowing, clothes flapping, dust flying |
| RAIN | Sadness, Struggle, Cleansing | Vertical streaks, floor splashes, wet skin texture |
| FOG | Mystery, Internal Thoughts | Drifts slowly, obscuring feet or text |
| THUNDER | Realization, Trauma | Instant strobe lighting changes |
| SNOW/ASH | Coldness, Isolation, Aftermath | Floats gently, slow-motion feel |

**The "Text Slam" Velocity:**
> "The text should not fade in. It should SLAM, SLIDE, or GROW instantly."

**The "Looping" Mindset:**
> "The avatar's breathing/idle motion should be continuous. The Weather is a continuous cycle."

---

### What the SKILL.md Says (Implemented)

**Visual Lineage:** ❌ **MISSING ENTIRELY**

**Core Physics Engine:** 
> "The FIGURE is FROZEN — statue in storm"

*(Truncated — misses the "Elemental Tension" philosophy)*

**Visual Architecture:** ❌ **NO PLANE LAYERING SPECIFIED**

**The Elemental Library:** 
Only vocabulary words:
```
silhouette, figure, stance, posture, weather, wind, rain,
snow, drift, blur, shadow, noir, contrast, solitary, 
isolated, endure, weather-beaten, horizon, storm, mist
```

*(The SOURCE had emotion-to-element mapping; the SKILL is just a word list)*

**The "Text Slam" Velocity:** ❌ **MISSING**

**The "Looping" Mindset:** ❌ **MISSING**

---

## 3. What's Causing Generic Outputs

### Gap 1: No Style DNA

The SOURCE says: "Visual Lineage: Sin City, Nike Motion Posters, Kendrick Lamar"

The SKILL says: Nothing.

**Result:** AI has no reference for what the output should LOOK like. It defaults to generic stock.

### Gap 2: No Plane Composition

The SOURCE says: "Build in Z-space: Void → Typography → Avatar → Elements"

The SKILL says: Nothing about layering.

**Result:** AI renders flat compositions instead of 2.5D collages.

### Gap 3: Emotion → Element Mapping Lost

The SOURCE says:
- WIND = Chaos/Power
- RAIN = Sadness/Struggle
- FOG = Mystery

The SKILL says: "weather, wind, rain, snow" (just words)

**Result:** AI picks random weather instead of emotion-motivated weather.

### Gap 4: Motion Behavior Lost

The SOURCE says:
- "Text should SLAM, SLIDE, or GROW instantly"
- "Fades are banned. Fades imply uncertainty."
- "We use Snaps (0-frame cuts) or Fast Slides (Spring Easing)"

The SKILL says: "DRIFT, BLOW, SETTLE, FREEZE, ENDURE"

**Result:** Motion is soft and drifting instead of violent and urgent.

### Gap 5: First Frame Philosophy Lost

The SOURCE says:
- "KEEP THE POSE EXACTLY THE SAME"
- "KEEP THE WEATHER"
- "We animate the atmosphere, not the skeleton"

The SKILL says:
```
ACTION: Reset weather to calm
- DELETE: The word "{WORD}"
- RESET: Remove all weather particles
```

**CRITICAL ERROR:** The skill says to REMOVE weather, but the source says to KEEP weather. This directly causes bad first frames.

---

## 4. The Constitution's Guardrails Are Missing

### What the Constitution Mandates

| Law | Source Requirement | Skill Implementation |
|-----|-------------------|---------------------|
| **"No Scene" Law** | Never render rooms/offices/streets | ❌ Not enforced |
| **"One Body" Law** | Never render two people interacting | ⚠️ Mentioned but not enforced |
| **"No Floating" Law** | Objects must be anchored by weather/shadow/glass | ❌ Not in skill |
| **"Metaphor → Premium Literal"** | Growth = Staircase in Neon Vector | ❌ Not in skill |
| **"Z-Axis Dominance"** | Premium motion moves Forward/Backward | ❌ Not in skill |
| **"Snap vs Fade"** | Fades are banned | ❌ Not in skill |

---

## 5. Diagnosis: Why This Happened

### The Truncation Pattern

When the skills were created, they followed a pattern:
1. Read the source guide
2. Extract the vocabulary
3. Create a "reasoning chain" template
4. Output a simplified skill

The problem: **Steps 2-4 lost the PHILOSOPHY**.

The vocabulary is just words. Without:
- **Visual Lineage** (what does this LOOK like?)
- **Plane Composition** (how are elements layered?)
- **Motion Philosophy** (snaps vs fades)
- **Anchoring Rules** (why does this element exist?)

...the AI has no framework to make aesthetic decisions. It defaults to generic.

---

## 6. The First Frame Problem Explained

### What Should Happen (per Constitution)

```
LAST FRAME: Audrey in crouch, heavy rain, word "HEAVY" above
FIRST FRAME: Audrey in crouch, heavy rain, word DELETED
MOTION: Rain continues, word SLAMS in
```

**The pose and weather are CONSTANT. Only the text animates.**

### What the Skill Instructs

```
ACTION: Reset weather to calm
- DELETE: The word "{WORD}"
- RESET: Remove all weather particles (rain, snow, wind debris)
```

**The skill tells AI to REMOVE the weather!**

This creates a first frame that looks COMPLETELY DIFFERENT from the last frame. When I2V tries to animate between them, it has to:
1. Re-add all the weather
2. Re-pose the character (even though it shouldn't change)
3. Slam in the text

**Result:** The motion is chaotic, the character morphs, the weather appears from nothing. It looks BAD.

---

## 7. Proposed Fix: Skill Depth Restoration

### Option A: Embed Full Source Content

Load the entire Motion Cookbook guide into the skill, not just a summary.

**Pros:** Maximum fidelity
**Cons:** 2000+ word skills; context window issues

### Option B: Separate Sessions with Source Loading

The skill says "Load for full context" but then duplicates a summary anyway.

**Fix:** Remove the summary from the skill. MANDATE loading the source. Each expert runs in isolation WITH the full source loaded.

### Option C: Create Style Primers

Create a new artifact type: `GMG_02_STYLE_PRIMER.md`

This file contains:
- Visual Lineage (5 reference images)
- Emotion → Element mapping
- Motion behavior rules
- First Frame philosophy
- Plane composition rules

The Composer loads ONLY the primer, not the full cookbook.

---

## 8. Immediate Fix for First Frames

The First Frame instruction is WRONG in all GMG skills.

**Current (BROKEN):**
```
ACTION: Reset weather to calm
- RESET: Remove all weather particles
```

**Corrected:**
```
ACTION: Remove text only — PRESERVE ALL ELSE
- DELETE: The word "{WORD}"
- KEEP: All weather particles (rain, snow, wind debris)
- KEEP: Exact pose, exact lighting, exact atmosphere
- KEEP: Film grain, texture, camera angle
```

This single fix will dramatically improve first frame quality.

---

## 9. Recommendation

1. **Fix First Frame Instructions NOW** — This is causing "REALLY REALLY REALLY BAD" first frames
2. **Create Style Primers** — Restore the visual lineage and philosophy per Expert
3. **Run Each Expert in Separate Session** — Prevent context pollution
4. **Embed Motion Philosophy** — Snaps vs Fades, Z-Axis Dominance

---

**END OF DIAGNOSIS**
