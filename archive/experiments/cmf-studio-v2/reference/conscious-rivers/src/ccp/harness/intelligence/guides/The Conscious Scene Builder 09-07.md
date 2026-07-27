### **The Conscious Scene Builder (V4 — Natron + CMF 2.0 Edition)**

This document is the definitive blueprint for constructing scene montages within the CMF production system. Each template is designed to be built as a polished scene within **Natron** before being assembled by MoviePy into your final `Sonic Arc Timeline`. 

> **🔄 System Change (V4):** This edition replaces all CapCut-specific instructions with Natron Python scripts from the `natron_effects_library/`. Effects are applied programmatically during Stage 5 (Natron Fabrication) via headless rendering on Runpod.

---

**Introduction: The Director's Playbook**

This document is the definitive blueprint for the 18 core scene types that form the backbone of the CONSCIOUS MOVIE FACTORY. Each template is a pre-designed, emotionally-tuned montage recipe, and this guide provides its creative and technical specifications.

**The Dual-Role C-Roll Philosophy**

C-Rolls serve two distinct and opposite functions. Your choice of C-Roll directly impacts the pacing and digestibility of your video.

* **Maximalist C-Rolls (The Story Machines):** Complex, multi-layered compositions with a high Cognitive Load. Their purpose is to add **Depth** and explain complex ideas.
* **Minimalist C-Rolls (The Pacing Punctuators):** Simple, often text-based graphics on a clean background. Their purpose is to create a **Pause** and bring **Clarity** to a single point.

**Introducing the Cognitive Load Score (CLS)**

Every effect, and therefore every scene, demands a certain amount of attention from the viewer. We quantify this with the **Cognitive Load Score (CLS)**.

* 🟢 **CLS 1 (Rest Point):** Simple, clean, effortless to digest.
* 🟡 **CLS 2 (Simple Information):** A single, clear idea or clean visual element.
* 🟠 **CLS 3 (Moderate Complexity):** A multi-layered thought or standard C-Roll composition.
* 🔴 **CLS 4 (High Complexity):** A dense, visually active scene demanding significant attention.
* 🟣 **CLS 5 (Peak Complexity):** A "showstopper" moment demanding the viewer's full focus.

---

## **Natron Effect Implementation Reference**

All effects are now implemented in `natron_effects_library/`. Use this mapping:

| Effect Code | Natron Implementation | Module |
|-------------|----------------------|--------|
| **EFFECT-M-01** | Slow Zoom Confession | `motion_effects.py` |
| **EFFECT-M-02** | Speed Ramp Chaos | `motion_effects.py` |
| **EFFECT-M-03** | Anxiety Camera Shake | `motion_effects.py` |
| **EFFECT-M-04** | Emphasis Punch-In | `motion_effects.py` |
| **EFFECT-M-08** | Vertical Drift | `motion_effects.py` |
| **EFFECT-M-09** | Dutch Angle Roll | `motion_effects.py` |
| **EFFECT-M-12** | Breathing Effect | `motion_effects.py` |
| **EFFECT-M-13** | Play Pendulum Float | `motion_effects.py` |
| **EFFECT-M-14** | Dynamic Handheld Drift | `motion_effects.py` |
| **EFFECT-C-01** | Personal Low Grade | `color_effects.py` |
| **EFFECT-C-02** | Hopeful Grade | `color_effects.py` |
| **EFFECT-C-03** | Nostalgic Memory Grade | `color_effects.py` |
| **EFFECT-C-04** | High-Contrast Modern | `color_effects.py` |
| **EFFECT-C-12** | Midas Touch Golden | `color_effects.py` |
| **EFFECT-C-15** | Looming Shadow | `color_effects.py` |
| **EFFECT-T-01** | Cinematic Film Grain | `color_effects.py` |
| **EFFECT-T-02** | Dreamlike Lens Blur | `color_effects.py` |
| **EFFECT-L-04** | Aspirational Bloom | `color_effects.py` |
| **EFFECT-TR-01** | Glitch Transition | `transition_effects.py` |
| **EFFECT-TR-03** | Whip Pan | `transition_effects.py` |
| **EFFECT-TR-05** | Gentle Dissolve | `transition_effects.py` |
| **EFFECT-TR-11** | Fade to Black | `transition_effects.py` |

**Audio Effects (Handled by MoviePy, not Natron):**
- EFFECT-A-01 through EFFECT-A-11 are applied during Stage 6 (MoviePy Assembly)

---

### **🎥 Scene 1: HOOK**

* **Emotional Function:** Shock / Intrigue / Curiosity
* **Story Function:** Establish tone, POV, or identity
* **Pacing & Rhythm:** Fast / Jarring / Pattern Interrupt
* **C-Roll:** ❌ Not used

**🔹 Template 1.1 — The Talking Head Pattern Match**

* **Code:** `HOOK-1-AB-2 🟠🟡`
* **Visual Recipe:** (2 clips: A-roll + [Coach B-Roll]) Start with a medium-close A-roll making a bold statement. Cut to a [Coach B-Roll] clip that reinforces the idea.
* **Story/Emotion:** Activates an immediate "that's me" feeling by mirroring the audience's identity or struggle.
* **Pacing & Rhythm:** A very fast, staccato rhythm. A quick A-roll phrase (1-2s) is immediately punctuated by an equally short B-roll beat (1s).
* **Natron VFX:** Apply **EFFECT-M-04** (Emphasis Punch-In) to the A-Roll.
* **Audio (MoviePy):** The cut to B-roll is accented with **EFFECT-A-05** (Impact Hit SFX).

**🔹 Template 1.2 — The Cinematic Foreshadow**

* **Code:** `HOOK-2-B-1 🟢🟢`
* **Visual Recipe:** (1 clip: B-roll + A-roll VO) Use an [AI Animated B-Roll] or [Cinematic Stock B-Roll] shot with A-roll voiceover delivering a cryptic phrase.
* **Story/Emotion:** Creates intrigue and establishes a cinematic, story-driven tone.
* **Pacing & Rhythm:** A deliberately slow, held shot that creates suspense.
* **Natron VFX:** Apply **EFFECT-T-01** (Cinematic Film Grain) for texture.
* **Audio (MoviePy):** Use **EFFECT-A-03** (Tension Drone) which swells in volume under the VO.

**🔹 Template 1.3 — The J-Cut Intrigue**

* **Code:** `HOOK-3-BA-2 🟡🟡`
* **Visual Recipe:** (2 clips: [Coach B-Roll] → A-roll) Start with authentic [Coach B-Roll]. Layer in J-cut audio. Cut to A-roll as they finish.
* **Story/Emotion:** Creates powerful curiosity by forcing the viewer to lean in.
* **Natron VFX:** Apply **EFFECT-C-01** (Personal Low Grade) over the B-Roll.
* **Audio (MoviePy):** Use **EFFECT-A-02** (Internal Thought Reverb) on the J-Cut audio.

**🔹 Template 1.4 — The Found Clip Reframe**

* **Code:** `HOOK-4-BA-2 🟠`
* **Visual Recipe:** (2 clips: [Found Clip] + A-roll) Open with a 1–2 second [Found Clip] (E-Roll). Smash cut to the coach's A-roll contradicting that clip.
* **Story/Emotion:** Uses borrowed cultural authority, then creates tension by subverting expectation.
* **Natron VFX:** Use **EFFECT-TR-01** (Glitch Transition) between clips.
* **Audio (MoviePy):** Use original E-Roll audio (EFFECT-A-06), cut with SFX_Record_Scratch.

**🔹 Template 1.5 — The A-Roll Setup & Found Clip Reveal**

* **Code:** `HOOK-5-AE-2 🟠`
* **Visual Recipe:** (2 clips: A-roll → [Found Clip] with L-Cut) Coach's A-Roll poses question, voice continues over Found Clip.
* **Story/Emotion:** Positions coach as masterful presenter with **Anticipation** followed by **Surprise**.
* **Natron VFX:** No effects needed—relies on L-Cut technique.
* **Audio (MoviePy):** Apply **EFFECT-A-06** (Found Clip Audio processing).

---

### **🎥 Scene 2: SETUP**

* **Emotional Function:** Vulnerability / Empathy / Context
* **Story Function:** Establish the emotional stakes and character's "Personal Low"
* **Pacing & Rhythm:** Deliberately slowing down to create connection
* **C-Roll:** ❌ Not used

**🔹 Template 2.1 — The "Personal Low" Visualization**

* **Code:** `SETUP-1-B-1 🟢🟡🟢`
* **Visual Recipe:** (1 clip: B-roll + A-roll VO) Single, artful [AI Animated B-Roll] depicting despair.
* **Story/Emotion:** Visualizes internal state of overwhelm, building deep empathy.
* **Natron VFX:** Apply **EFFECT-M-01** (Slow Zoom) + **EFFECT-C-01** (Personal Low Grade).
* **Audio (MoviePy):** Use **EFFECT-A-03** (Tension Drone) mixed with diegetic SFX.

**🔹 Template 2.2 — The Authentic Memory Montage**

* **Code:** `SETUP-2-B-Montage-3-4 🟡🟠🟢`
* **Visual Recipe:** (3-4 clips: [Coach B-Roll] Montage + A-roll VO) Montage of authentic coach B-Roll.
* **Story/Emotion:** Puts audience inside a real-life memory, making struggle feel authentic.
* **Natron VFX:** Apply **EFFECT-C-03** (Nostalgic Memory Grade) + **EFFECT-TR-05** (Gentle Dissolve) between clips.
* **Audio (MoviePy):** Use **EFFECT-A-02** (Internal Thought Reverb) on the VO.

**🔹 Template 2.3 — The Prop-Driven Metaphor**

* **Code:** `SETUP-3-B-1 🟡`
* **Visual Recipe:** (1 clip: [Coach B-Roll]) Clean shot of coach with prop representing the "Setup."
* **Story/Emotion:** Uses physical object to make abstract concept tangible.
* **Natron VFX:** Use masking to isolate prop (requires matte pipeline—see Gap 3).
* **Audio (MoviePy):** Crisp, clean Foley SFX for the prop action.

**🔹 Template 2.4 — The L-Cut Vulnerability Drop**

* **Code:** `SETUP-4-AB-2 🟠`
* **Visual Recipe:** (2 clips: A-roll → [Coach B-Roll]) Coach delivers vulnerable line, audio carries over B-Roll of quiet reflection.
* **Story/Emotion:** Connects shocking vulnerability with contemplative visual.
* **Natron VFX:** Apply **EFFECT-M-06** (Rack Focus-simulated via blur keyframes) to B-roll if depth permits.

---

### **🎥 Scene 3: CHALLENGE**

* **Emotional Function:** Rising Tension / Conflict / Stakes
* **Story Function:** Introduce the core obstacle or internal struggle
* **Pacing & Rhythm:** Accelerating / Staccato / Crescendo
* **C-Roll:** ✅ Used

**🔹 Template 3.1 — The Struggle Montage**

* **Code:** `CHALLENGE-1-B-Montage-3-5 🔴🟠🟠🟠`
* **Visual Recipe:** (3-5 clips: B-roll Montage + A-roll VO) Montage showing character battling metaphor for struggle.
* **Story/Emotion:** Visualizes internal struggle cinematically, raising stakes.
* **Natron VFX:** Apply **EFFECT-M-02** (Speed Ramp) + **EFFECT-M-03** (Anxiety Camera Shake) + **EFFECT-TR-01** (Glitch Transition).
* **Audio (MoviePy):** Tense music bed + **EFFECT-A-04** (Cinematic Riser).

**🔹 Template 3.2 — The C-Roll "Enemy" Collage**

* **Code:** `CHALLENGE-2-AC-2 🔴🟢`
* **Visual Recipe:** (2 clips: A-roll → C-roll) Coach names the "enemy," cuts to dynamic C-roll.
* **Story/Emotion:** Personifies abstract challenge, giving audience clear "enemy" to root against.
* **Natron VFX:** C-Roll requires compositing in Natron with text animations and glitch effects.
* **Audio (MoviePy):** Deep drone + "smash" or "error buzzer" SFX.

**🔹 Template 3.3 — The Found Clip Chaos Montage**

* **Code:** `CHALLENGE-3-B-Montage-4-6 🔴🟡`
* **Visual Recipe:** (4-6 clips: Mixed Montage + A-roll VO) Rapid intercut of [Coach B-Roll] and [Found Clips] of chaos.
* **Story/Emotion:** Creates powerful sense of shared experience and validation.
* **Natron VFX:** Use **EFFECT-TR-01** (Glitch Transition) between cuts.
* **Audio (MoviePy):** Layered cacophony with EFFECT-A-06 + EFFECT-A-09.

**🔹 Template 3.4 — The Prop-Driven Struggle**

* **Code:** `CHALLENGE-4-B-1 🟢`
* **Visual Recipe:** (1 clip: [Coach B-Roll]) Single shot of coach demonstrating challenge with prop.
* **Story/Emotion:** Makes challenge tangible and easy to understand.
* **Natron VFX:** Apply **EFFECT-M-01** (Slow Zoom) to heighten tension.
* **Audio (MoviePy):** Raw diegetic sound of prop, amplified.

---

### **🎥 Scene 4: JUXTAPOSITION**

* **Emotional Function:** Rhythm Break / Ironic Release / Shock
* **Story Function:** Make a point through unexpected contrast
* **Pacing & Rhythm:** Abrupt Shift / The "Beat Drop"
* **C-Roll:** ❌ Not used

**🔹 Template 4.1 — The Found Clip Punchline**

* **Code:** `JUXTAPOSE-1-AB-2`
* **Visual Recipe:** (2 clips: A-roll → [Found Clip]) Coach makes serious statement. Hard cut to [Found Clip] that ironically undercuts it.
* **Story/Emotion:** Creates ironic release (humor or shock) that breaks tension.
* **Natron VFX:** None required—power is in the edit.
* **Audio (MoviePy):** Original E-Roll audio + SFX_Record_Scratch.

**🔹 Template 4.2 — The Stylized Mismatch**

* **Code:** `JUXTAPOSE-2-B-1 🔴`
* **Visual Recipe:** (1 clip: B-roll + A-roll VO) Calm VO over B-roll depicting intense action.
* **Story/Emotion:** Creates unsettling or comedic dissonance.
* **Natron VFX:** Apply **EFFECT-M-02** (Speed Ramp) to B-roll.
* **Audio (MoviePy):** Keep VO pristine (EFFECT-A-01), mute B-roll audio.

**🔹 Template 4.3 — The Coach B-Roll Match Cut**

* **Code:** `JUXTAPOSE-3-BB-2 🟡🟡🟢`
* **Visual Recipe:** (2 clips: [Coach B-Roll] → [Coach B-Roll]) Match cut between two shots with similar composition.
* **Story/Emotion:** Creates powerful non-verbal metaphor about different "selves."
* **Natron VFX:** Apply **EFFECT-C-04** to first clip, **EFFECT-C-02** to second.
* **Audio (MoviePy):** None specified.

**🔹 Template 4.4 — The Then vs. Now**

* **Code:** `JUXTAPOSE-4-BB-2 🟠`
* **Visual Recipe:** (2 clips: [Coach B-Roll] past → [Coach B-Roll] present) A-roll VO describes change.
* **Story/Emotion:** Clear, authentic, undeniable proof of transformation.
* **Natron VFX:** Use **EFFECT-TR-03** (Whip Pan) or **EFFECT-TR-05** (Dissolve).
* **Audio (MoviePy):** Subtle SFX_Sparkle on "Now" shot.

---

### **🎥 Scene 5: TURNING POINT**

* **Emotional Function:** The Pivot / Realization / Release
* **Story Function:** A new belief is formed; the story's direction changes
* **Pacing & Rhythm:** The Decisive Pause / The Still Point
* **C-Roll:** ❌ Not used

**🔹 Template 5.1 — The Reaction Shot Hold**

* **Code:** `TURNING_POINT-1-B-1 🟢`
* **Visual Recipe:** (1 clip: B-roll) Tight close-up of character's face as expression changes. Hold 3-4 seconds.
* **Story/Emotion:** An "earned slow moment" witnessing internal change in real-time.
* **Natron VFX:** Apply **EFFECT-M-01** (Slow Zoom) to enhance focus.
* **Audio (MoviePy):** All music/drones cut to **complete silence**.

**🔹 Template 5.2 — The Prop-Driven Metaphor**

* **Code:** `TURNING_POINT-2-B-1 🟡`
* **Visual Recipe:** (1 clip: [Coach B-Roll] + A-roll VO) Single symbolic B-roll shot (Key Turning, Lit Candle).
* **Story/Emotion:** Translates internal "aha!" into clear visual metaphor.
* **Natron VFX:** Apply **EFFECT-C-02** (Hopeful Grade) for warm glow.
* **Audio (MoviePy):** Clean SFX matching prop (SFX_Key_Turn, etc.).

**🔹 Template 5.3 — The Whip Pan Pivot**

* **Code:** `TURNING_POINT-3-BB-2 🟠🟢`
* **Visual Recipe:** (2 clips: [Coach B-Roll] → [Coach B-Roll]) On VO realization, whip pan to new scene.
* **Story/Emotion:** Physically represents the "pivot" with renewed energy.
* **Natron VFX:** Apply **EFFECT-TR-03** (Whip Pan).
* **Audio (MoviePy):** **EFFECT-A-11** (Kinetic Whoosh Accent).

**🔹 Template 5.4 — The J-Cut "Aha!" Moment**

* **Code:** `TURNING_POINT-4-BA-2 🟢🟢`
* **Visual Recipe:** (2 clips: [Coach B-Roll] → A-roll) Hold on contemplative B-roll. J-cut A-roll audio.
* **Story/Emotion:** Separates internal thought from external reality.
* **Natron VFX:** Apply **EFFECT-M-08** (Vertical Drift) for gentle ascension feeling.
* **Audio (MoviePy):** **EFFECT-A-02** (Internal Thought Reverb).

---

### **🎥 Scene 6: RESOLUTION**

* **Emotional Function:** Emotional Resonance / Calm / Relief
* **Story Function:** Show the result of change; the "earned" slow moment
* **Pacing & Rhythm:** Deliberately Slow / "Breathing Room" / Decelerating
* **C-Roll:** ✅ Used

**🔹 Template 6.1 — The Cinematic Release**

* **Code:** `RESOLUTION-1-B-1 🟡🟠`
* **Visual Recipe:** (1 clip: B-roll + A-roll VO) Beautiful shot showing character in state of peace.
* **Story/Emotion:** Allows audience to savor victory and absorb emotional payoff.
* **Natron VFX:** Apply **EFFECT-C-02** (Hopeful Grade). Set speed to 50-60%.
* **Audio (MoviePy):** Peaceful, ambient music bed.

**🔹 Template 6.2 — The C-Roll Affirmation**

* **Code:** `RESOLUTION-2-C-1 🟡🟡`
* **Visual Recipe:** (1 clip: C-roll) Powerful word displayed ("Worthy," "Free").
* **Story/Emotion:** Crystallizes internal resolution into memorable affirmation.
* **Natron VFX:** Text animation with **EFFECT-L-04** (Bloom) for glow.
* **Audio (MoviePy):** Single resonant SFX_Bell_Chime.

**🔹 Template 6.3 — The Bookend B-Roll**

* **Code:** `RESOLUTION-3-B-1 🟡`
* **Visual Recipe:** (1 clip: [Coach B-Roll]) Re-use B-roll from "Challenge" scene in resolved context.
* **Story/Emotion:** Deeply satisfying closure contrasting "before" and "after."
* **Natron VFX:** Apply **EFFECT-C-02** (Hopeful Grade).
* **Audio (MoviePy):** Soft, resolving musical cue from Sonic Arc.

**🔹 Template 6.4 — The A-Roll "Sigh" Moment**

* **Code:** `RESOLUTION-4-A-1 🟢`
* **Visual Recipe:** (1 clip: A-roll) Uncut shot of coach taking deep breath with genuine smile.
* **Story/Emotion:** Most authentic resolution—non-verbal expression of relief.
* **Natron VFX:** Apply **EFFECT-M-01** (Slow Zoom) for intimacy.
* **Audio (MoviePy):** Amplified SFX_Human_Breath_Calm.

---

### **🎥 Scene 7: ENCOURAGING CHANGE**

* **Emotional Function:** Empowerment / Inspiration / Call-to-Action
* **Story Function:** Transfer the story's lesson to the viewer
* **Pacing & Rhythm:** Re-accelerating / Upbeat / Motivational
* **C-Roll:** ✅ Used

**🔹 Template 7.1 — The Direct-to-Camera A-Roll**

* **Code:** `ENCOURAGE-1-A-1 🟢🟢`
* **Visual Recipe:** (1 clip: A-roll) Coach breaks fourth wall, looking into camera.
* **Story/Emotion:** Powerful personal connection, transforming story into direct advice.
* **Natron VFX:** Apply **EFFECT-M-12** (Breathing Effect) for subconscious human feel.
* **Audio (MoviePy):** **EFFECT-A-01** (Standard Vocal Chain) + inspirational music.

**🔹 Template 7.2 — The C-Roll "Blueprint"**

* **Code:** `ENCOURAGE-2-C-1 🔴🟣`
* **Visual Recipe:** (1 clip: C-roll + A-roll VO) Composition breaking down concept with animated text/icons.
* **Story/Emotion:** Makes abstract concept practical and empowering.
* **Natron VFX:** Complex C-Roll built in Natron with text animations.
* **Audio (MoviePy):** Upbeat with percussive SFX timed to animations.

**🔹 Template 7.3 — The Social Proof Montage**

* **Code:** `ENCOURAGE-3-B-Montage-3-4 🟢🟡`
* **Visual Recipe:** (3-4 clips: Mixed B-roll Montage + A-roll VO) Different people successfully applying new belief.
* **Story/Emotion:** Shows universality of message, providing social proof.
* **Natron VFX:** Use **EFFECT-TR-05** (Dissolve) + **EFFECT-C-04** (High-Contrast Grade).
* **Audio (MoviePy):** Inspiring music track.

**🔹 Template 7.4 — The C-Roll Reflective Question**

* **Code:** `ENCOURAGE-4-AC-2 🟡`
* **Visual Recipe:** (2 clips: A-roll → C-roll) Coach poses final question, animated as C-Roll.
* **Story/Emotion:** Shifts focus to viewer's life as call to action.
* **Natron VFX:** Text animation (typewriter style).
* **Audio (MoviePy):** SFX_Typewriter sound.

---

### **🎥 Scene 8: SYMBOLIC ECHO**

* **Emotional Function:** Narrative Cohesion / Deeper Meaning / "Aha!" Moment
* **Story Function:** Re-contextualize an earlier element to show change
* **Pacing & Rhythm:** Mirrored / Rhythmic "Click" / Deliberate
* **C-Roll:** ✅ Used

**🔹 Template 8.1 — The B-Roll Match Cut**

* **Code:** `ECHO-1-BB-2 🟡🟡🟢`
* **Visual Recipe:** (2 clips: B-roll → B-roll + A-roll VO) Hard cut from object in "Challenge" state to "Resolution" state.
* **Story/Emotion:** Deeply satisfying "click" as viewer recognizes change.
* **Natron VFX:** Apply **EFFECT-C-01** to first clip, **EFFECT-C-02** to second.
* **Audio (MoviePy):** Resonant SFX_Chime_Deep bridges the cut.

**🔹 Template 8.2 — The C-Roll Symbol Transformation**

* **Code:** `ECHO-2-C-1 🟡`
* **Visual Recipe:** (1 clip: C-roll) Icon/symbol animates to morph into new, positive symbol.
* **Story/Emotion:** Visually represents core transformation in single elegant graphic.
* **Natron VFX:** Transformation animation via masked wipe/dissolve.
* **Audio (MoviePy):** Magical SFX_Ascend matching visual.

**🔹 Template 8.3 — The Audio Callback**

* **Code:** `ECHO-3-A-1 🟢`
* **Visual Recipe:** (1 clip: A-roll with audio layer) Confident A-roll with faint callback to vulnerable "Setup" audio.
* **Story/Emotion:** Contrasts past self with present using only audio.
* **Natron VFX:** None—audio-based effect.
* **Audio (MoviePy):** Callback with **EFFECT-A-02** mixed at -15 to -20dB.

**🔹 Template 8.4 — The AI Environmental Shift**

* **Code:** `ECHO-4-B-1 🟢🟢`
* **Visual Recipe:** (1 clip: [AI Animated B-Roll]) Re-use environment shot, now bright/clean.
* **Story/Emotion:** Shows change so profound it altered the environment.
* **Natron VFX:** Apply **EFFECT-C-02** (Hopeful Grade).
* **Audio (MoviePy):** Shift from EFFECT-A-03 to EFFECT-A-08 (Environmental Diegetic).

---

### **🎥 Scene 9: FRAME & CONTRAST**

* **Emotional Function:** Intellectual Tension / Perspective Shift
* **Story Function:** Expand context by showing layered or opposing views
* **Pacing & Rhythm:** Call & Response / Debate / Rhythmic Back-and-Forth
* **C-Roll:** ✅ Used

**🔹 Template 9.1 — The C-Roll Split-Screen**

* **Code:** `CONTRAST-1-C-1 🔴🟡🟡`
* **Visual Recipe:** (1 clip: C-roll with 2 video panels + A-roll VO) "Their way" vs. "your way."
* **Story/Emotion:** Creates intellectual tension forcing direct comparison.
* **Natron VFX:** Split-screen compositing in Natron with different grades per side.
* **Audio (MoviePy):** N/A.

**🔹 Template 9.2 — The A-Roll Fast-Cut Debate**

* **Code:** `CONTRAST-2-AB-Montage-3-5 🟠🟢🟡`
* **Visual Recipe:** (3-5 clips: A-roll/[Found Clip] intercut) Rapid cuts between coach and opposing clips.
* **Story/Emotion:** Creates dynamic debate feeling, positioning coach as authority.
* **Natron VFX:** Apply **EFFECT-M-04** (Punch-In) on A-roll cuts.
* **Audio (MoviePy):** **EFFECT-A-11** (Whoosh) + **EFFECT-A-06** on E-Roll.

**🔹 Template 9.3 — The C-Roll "Guru" Takedown**

* **Code:** `CONTRAST-3-C-1 🔴🟢`
* **Visual Recipe:** (1 clip: C-roll) Collage: coach cutout vs. generic "guru" cutout.
* **Story/Emotion:** Positions coach as clear, rational voice against industry noise.
* **Natron VFX:** Composited C-Roll with glitch text and animations.
* **Audio (MoviePy):** "Smash" or "error buzzer" SFX.

**🔹 Template 9.4 — The Layered Text C-Roll**

* **Code:** `CONTRAST-4-BC-2 🟢`
* **Visual Recipe:** (2 clips: B-roll + C-roll layer) Misconception text appears, then truth text covers it.
* **Story/Emotion:** Visually clean way to demonstrate paradigm shift.
* **Natron VFX:** Text layering with opacity animation.
* **Audio (MoviePy):** SFX_Swoosh on Text 2 appear.

---

### **🎥 Scene 10: THE TEASE**

* **Emotional Function:** Disruptive Mystery / Shock / Curiosity
* **Story Function:** Intentionally withhold context to build tension
* **Pacing & Rhythm:** Fragmented / Disorienting / Abrupt
* **C-Roll:** ✅ Used

**🔹 Template 10.1 — The Redacted C-Roll**

* **Code:** `TEASE-1-C-1 🟠`
* **Visual Recipe:** (1 clip: C-roll) Sentence typed out with key word covered by black bar.
* **Story/Emotion:** Creates intense curiosity and "Wait, what?" feeling.
* **Natron VFX:** Text animation with mask reveal.
* **Audio (MoviePy):** "Censor beep" SFX.

**🔹 Template 10.2 — The Incomplete B-Roll Action**

* **Code:** `TEASE-2-B-1`
* **Visual Recipe:** (1 clip: B-roll) Shot builds to key moment, cuts to black before completion.
* **Story/Emotion:** Pure tension play leveraging brain's desire for resolution.
* **Natron VFX:** None—editorial cut.
* **Audio (MoviePy):** Cut to silence or SFX_Impact_Sharp.

**🔹 Template 10.3 — The Out-of-Context A-Roll**

* **Code:** `TEASE-3-A-1 🟠🟡`
* **Visual Recipe:** (1 clip: A-roll) Start cold with coach at peak emotion, zero setup.
* **Story/Emotion:** Disorients viewer, creates desperate need for context.
* **Natron VFX:** Apply **EFFECT-M-03** (Camera Shake) + **EFFECT-C-04** (High-Contrast).
* **Audio (MoviePy):** Slightly increased volume.

**🔹 Template 10.4 — The Glitchy Flash Montage**

* **Code:** `TEASE-4-B-Montage-4-6 🔴🟠`
* **Visual Recipe:** (4-6 clips: Mixed Montage) 1-2 second montage of tiny, fragmented clips.
* **Story/Emotion:** Corrupted memory, premonition, brain piecing information.
* **Natron VFX:** Use **EFFECT-TR-01** (Glitch Transition) between clips.
* **Audio (MoviePy):** Chaotic SFX_Glitch + SFX_Riser_Short.

---

### **🎥 Scene 11: VOICE OF TRUTH**

* **Emotional Function:** External Anchor / Validation / Release
* **Story Function:** Use universal truth to validate character's journey
* **Pacing & Rhythm:** Steady / Authoritative / Clear
* **C-Roll:** ✅ Used

**🔹 Template 11.1 — The C-Roll Quote Card**

* **Code:** `TRUTH-1-C-1 🟡🟡`
* **Visual Recipe:** (1 clip: C-roll) Impactful quote over blurred atmospheric background.
* **Story/Emotion:** Lends credibility by connecting to timeless truth.
* **Natron VFX:** Text with **EFFECT-L-04** (Bloom) for premium feel.
* **Audio (MoviePy):** Soft SFX_Ambient_Swell.

**🔹 Template 11.2 — The Archival Audio Overlay**

* **Code:** `TRUTH-2-B-1 🟡🟡`
* **Visual Recipe:** (1 clip: B-roll + [Found Clip] Audio) Old grainy audio over modern cinematic B-roll.
* **Story/Emotion:** Creates sense of legacy and historical weight.
* **Natron VFX:** Apply **EFFECT-C-04** (High-Contrast Modern).
* **Audio (MoviePy):** **EFFECT-A-06** (Radio/Lo-Fi effect).

**🔹 Template 11.3 — The C-Roll Mentor Collage**

* **Code:** `TRUTH-3-C-1 🟠`
* **Visual Recipe:** (1 clip: C-roll + A-roll VO) Cutout image of "mentor" figure being quoted.
* **Story/Emotion:** Creates visual link between coach and inspiration source.
* **Natron VFX:** Composited C-Roll with text and cutout.
* **Audio (MoviePy):** Soft SFX_Page_Turn.

**🔹 Template 11.4 — The A-Roll "Narrator" Mode**

* **Code:** `TRUTH-4-AB-2 🟡`
* **Visual Recipe:** (2 clips: A-roll + [AI Animated B-Roll]) Coach quotes source with epic B-roll.
* **Story/Emotion:** Elevates coach from character to wise narrator.
* **Natron VFX:** Letterbox effect + **EFFECT-C-02** (Hopeful Grade) on B-roll.
* **Audio (MoviePy):** Epic orchestral music bed.

---

### **🎥 Scene 12: THE ARCHETYPAL MOMENT**

* **Emotional Function:** Universal Resonance / Subconscious Connection / Awe
* **Story Function:** Connect personal story to universal human theme
* **Pacing & Rhythm:** Deliberate / Reverent / Often slow-motion
* **C-Roll:** ✅ Used

**🔹 Template 12.1 — The Archetypal Foreshadow**

* **Code:** `ARCHETYPE-1-C-1 🟢🟡`
* **Visual Recipe:** (1 clip: C-roll + A-roll VO) Powerful animated archetype from [AI Illustrated B-Roll].
* **Story/Emotion:** Primes subconscious with universal theme, making struggle mythic.
* **Natron VFX:** Apply **EFFECT-M-08** (Vertical Drift) + **EFFECT-M-13** (Pendulum Float).
* **Audio (MoviePy):** Deep SFX_Chime_Deep or SFX_Ambient_Hum.

**🔹 Template 12.2 — The Mid-Story Metaphor**

* **Code:** `ARCHETYPE-2-B-1 🟡`
* **Visual Recipe:** (1 clip: B-roll) Cut from personal struggle to natural archetype (lone tree in storm).
* **Story/Emotion:** Externalizes internal conflict, amplifying emotional stakes.
* **Natron VFX:** Apply **EFFECT-C-01** (Personal Low Grade).
* **Audio (MoviePy):** Tense score + environmental SFX (SFX_Storm, SFX_Wind_Howl).

**🔹 Template 12.3 — The Breakthrough Symbol**

* **Code:** `ARCHETYPE-3-C-1 🟡`
* **Visual Recipe:** (1 clip: C-roll + A-roll VO) Symbol of problem transforms into symbol of solution.
* **Story/Emotion:** Deeply satisfying symbolic representation of breakthrough.
* **Natron VFX:** Transformation animation (masked dissolve).
* **Audio (MoviePy):** SFX_Ascend or SFX_Shatter.

**🔹 Template 12.4 — The Mythic Resolution**

* **Code:** `ARCHETYPE-4-B-1 🟡🟢`
* **Visual Recipe:** (1 clip: B-roll + A-roll VO) Cinematic B-roll of resolution archetype (walking into sunrise).
* **Story/Emotion:** Concludes story on mythic level, suggesting permanent shift.
* **Natron VFX:** Apply **EFFECT-C-02** (Hopeful Grade).
* **Audio (MoviePy):** **EFFECT-A-08** (Environmental Diegetic) with peaceful sounds.

---

### **🎥 Scene 13: THE DEMONSTRATION**

* **Emotional Function:** Clarity / Empowerment / Education
* **Story Function:** Clearly show process, teach skill, demonstrate tool
* **Pacing & Rhythm:** Clear / Methodical / Step-by-Step
* **C-Roll:** ✅ Used

**🔹 Template 13.1 — The Full-Screen Walkthrough**

* **Code:** `DEMO-1-B-1 🟡`
* **Visual Recipe:** (1 clip: Screen Recording + A-roll VO) Standard full-screen recording of process.
* **Story/Emotion:** Empowers viewer with clear, actionable instructions.
* **Natron VFX:** Text overlays highlighting buttons/menus.
* **Audio (MoviePy):** Pop-up SFX (SFX_Click, SFX_Pop).

**🔹 Template 13.2 — The "Picture-in-Picture" Guide**

* **Code:** `DEMO-2-BC-2 🟡`
* **Visual Recipe:** (2 clips: Screen Recording + A-Roll) Screen recording with coach's face in corner.
* **Story/Emotion:** Adds human connection to technical demonstration.
* **Natron VFX:** Masked circle/rectangle overlay of A-roll.
* **Audio (MoviePy):** N/A.

**🔹 Template 13.3 — The "3D Screen" Showcase**

* **Code:** `DEMO-3-C-1 🔴🟠`
* **Visual Recipe:** (1 clip: C-Roll from Screen Recording) Screen recording transformed into 3D object.
* **Story/Emotion:** Makes standard screen recording feel dynamic and premium.
* **Natron VFX:** Apply **EFFECT-M-15** (3D Screen Flip)—requires PyPlug.
* **Audio (MoviePy):** Whoosh SFX synced to flip.

**🔹 Template 13.4 — The Highlighted Zoom**

* **Code:** `DEMO-4-BC-2 🟠🟡`
* **Visual Recipe:** (Screen Recording + C-Roll) Dynamic punch-in to specific area.
* **Story/Emotion:** Creates emphasis by guiding viewer's eye precisely.
* **Natron VFX:** Apply **EFFECT-M-04** (Punch-In) + highlight graphic.
* **Audio (MoviePy):** N/A.

---

### **🎥 Scene 14: THE EVIDENCE**

* **Emotional Function:** Credibility / Authority / Trust
* **Story Function:** Build logical case with data, statistics, or proof
* **Pacing & Rhythm:** Factual / Deliberate / Punchy
* **C-Roll:** ✅ Used

**🔹 Template 14.1 — The Animated Chart Reveal**

* **Code:** `EVIDENCE-1-C-1 🔴`
* **Visual Recipe:** (1 clip: C-Roll) Animated bar chart building on screen.
* **Story/Emotion:** Makes data digestible, turning numbers into visual story.
* **Natron VFX:** Chart animation with wipe reveals.
* **Audio (MoviePy):** Sequential build SFX.

**🔹 Template 14.2 — The "Kinetic Number" Pop**

* **Code:** `EVIDENCE-2-C-1 🟡`
* **Visual Recipe:** (1 clip: C-Roll) Single powerful statistic ("93%") dominating screen.
* **Story/Emotion:** Creates impact, makes data point monumental.
* **Natron VFX:** Text with bounce/pop animation.
* **Audio (MoviePy):** **EFFECT-A-05** (Impact Hit).

**🔹 Template 14.3 — The "Before & After" Proof**

* **Code:** `EVIDENCE-3-B-1 🟠`
* **Visual Recipe:** (1-2 clips: B-Roll/Image) Split-screen or sequential before/after reveal.
* **Story/Emotion:** Most direct way to prove transformation.
* **Natron VFX:** Split-screen comp or **EFFECT-TR-03** (Whip Pan) for reveal.
* **Audio (MoviePy):** N/A.

**🔹 Template 14.4 — The Data Point Highlight**

* **Code:** `EVIDENCE-4-C-1 🟡`
* **Visual Recipe:** (1 clip: C-Roll using image) Screenshot with specific data highlighted.
* **Story/Emotion:** Builds credibility by citing source, guiding to key info.
* **Natron VFX:** Animated highlight bar over text.
* **Audio (MoviePy):** N/A.

---

### **🎥 Scene 15: THE COMMUNITY**

* **Emotional Function:** Belonging / Social Proof / Connection
* **Story Function:** Show viewer is part of larger movement
* **Pacing & Rhythm:** Upbeat / Rhythmic / Collective
* **C-Roll:** ✅ Used

**🔹 Template 15.1 — The "Tweet/Comment" Showcase**

* **Code:** `COMMUNITY-1-C-1 🟠`
* **Visual Recipe:** (1 clip: C-Roll) Composition mimicking social media UI with real testimonial.
* **Story/Emotion:** Lends authenticity using real people's words.
* **Natron VFX:** UI mockup with fade/slide animation.
* **Audio (MoviePy):** N/A.

**🔹 Template 15.2 — The "UGC" Montage**

* **Code:** `COMMUNITY-2-B-Montage-3-5 🟢🟠`
* **Visual Recipe:** (3-5 clips: B-Roll) Fast montage of client video clips.
* **Story/Emotion:** Creates feeling of thriving, active community.
* **Natron VFX:** Use **EFFECT-TR-01** (Glitch) or **EFFECT-TR-05** (Dissolve) + **EFFECT-C-04**.
* **Audio (MoviePy):** Upbeat music cut to beat.

**🔹 Template 15.3 — The Video Testimonial Snippet**

* **Code:** `COMMUNITY-3-C-1 🟢`
* **Visual Recipe:** (1 clip: C-Roll using B-Roll) Client testimonial framed with name/title graphic.
* **Story/Emotion:** Combines authenticity with professional presentation.
* **Natron VFX:** Text overlay with fade-in.
* **Audio (MoviePy):** N/A.

**🔹 Template 15.4 — The "Avatar Wall" Grid**

* **Code:** `COMMUNITY-4-C-1 🟠`
* **Visual Recipe:** (1 clip: C-Roll) Grid of profile pictures animating onto screen.
* **Story/Emotion:** Powerful visual metaphor for large community.
* **Natron VFX:** Staggered pop-up animation of multiple layers.
* **Audio (MoviePy):** N/A.

---

### **🎥 Scene 16: THE PAUSE**

* **Emotional Function:** Reflection / Contemplation / Emphasis
* **Story Function:** Slow pace, create breathing room, let message sink in
* **Pacing & Rhythm:** Still / Slow / Deliberate Silence
* **C-Roll:** ✅ Used

**🔹 Template 16.1 — The Meditative B-Roll**

* **Code:** `PAUSE-1-B-1 🟡`
* **Visual Recipe:** (1 clip: B-Roll) Single slow-motion B-roll (nature, gentle motion), no VO.
* **Story/Emotion:** Gives viewer moment to breathe and process.
* **Natron VFX:** Set speed to 50% + **EFFECT-C-02** (Hopeful Grade).
* **Audio (MoviePy):** Music from Sonic Arc only.

**🔹 Template 16.2 — The Fading Word**

* **Code:** `PAUSE-2-C-1 🟢`
* **Visual Recipe:** (1 clip: C-Roll) Single word ("Breathe," "Listen") on black screen.
* **Story/Emotion:** Forces focus on single concept.
* **Natron VFX:** Slow fade-in/fade-out text animation.
* **Audio (MoviePy):** N/A.

**🔹 Template 16.3 — The "Empty Room" Metaphor**

* **Code:** `PAUSE-3-B-1 🟢`
* **Visual Recipe:** (1 clip: B-Roll) Lingering shot of empty space (chair, office, stage).
* **Story/Emotion:** Creates contemplation, anticipation, or aftermath feeling.
* **Natron VFX:** Apply **EFFECT-M-08** (Vertical Drift) for subtle motion.
* **Audio (MoviePy):** N/A.

**🔹 Template 16.4 — The Lingering Look**

* **Code:** `PAUSE-4-A-1 🟢`
* **Visual Recipe:** (1 clip: A-Roll) Extended A-Roll with 2-3 seconds of silence after speaking.
* **Story/Emotion:** Powerful, intimate, sometimes uncomfortable direct connection.
* **Natron VFX:** Apply **EFFECT-M-01** (Slow Zoom) during silence.
* **Audio (MoviePy):** Complete silence.

---

### **🎥 Scene 17: THE VIBE**

* **Emotional Function:** Abstract Mood / Textural Immersion / Rhythmic Energy
* **Story Function:** Create "vibe" enhancing sonic arc without narrative info
* **Pacing & Rhythm:** Extremely fast and percussive, OR hypnotic and slow
* **C-Roll:** ✅ Used (Exclusively)

**🔹 Template 17.1 — The Rhythmic Abstraction**

* **Code:** `VIBE-1-B-Montage-4-6 🔴`
* **Visual Recipe:** (4-6 clips: Abstract B-Roll Montage) Rapid-fire montage cut to percussive music.
* **Story/Emotion:** Visceral, high-energy feeling—visual drum solo.
* **Natron VFX:** Use **EFFECT-TR-01** (Glitch) between cuts. Apply distortion effects.
* **Audio (MoviePy):** Beat-synced to driving percussion.

**🔹 Template 17.2 — The Meditative Haze**

* **Code:** `VIBE-2-B-1 🟡`
* **Visual Recipe:** (1 clip: B-Roll) Single slow-motion atmospheric shot, no VO.
* **Story/Emotion:** Visual pause evoking Longing, Nostalgia, or Peace.
* **Natron VFX:** Apply **EFFECT-M-12** (Breathing) + **EFFECT-T-02** (Lens Blur).
* **Audio (MoviePy):** Music carries emotion.

**🔹 Template 17.3 — The "Hero Pose" Still**

* **Code:** `VIBE-3-C-1 🟠`
* **Visual Recipe:** (1 C-Roll Composition) Stylized coach still as "living portrait."
* **Story/Emotion:** Visual power-up—transforms coach into archetype.
* **Natron VFX:** Apply **EFFECT-M-16** (Z-Space Sandwich—requires matte) + **EFFECT-L-04** (Bloom).
* **Audio (MoviePy):** N/A.

**🔹 Template 17.4 — The One-Color World**

* **Code:** `VIBE-4-B-1 🔴`
* **Visual Recipe:** (1 clip: B-Roll) Desaturated except for one symbolic color.
* **Story/Emotion:** Focus on single symbolic idea (Romance, Longing, Curiosity).
* **Natron VFX:** Color isolation effect + **EFFECT-T-01** (Film Grain).
* **Audio (MoviePy):** N/A.

---

### **🎥 Scene 18: THE VISION**

* **Emotional Function:** Aspiration / Longing / Hopeful Anticipation
* **Story Function:** Paint vivid picture of future state, goal, or "Promised Land"
* **Pacing & Rhythm:** Dreamlike, flowing, cinematic
* **C-Roll:** ✅ Used

**🔹 Template 18.1 — The "Dream State" Montage**

* **Code:** `VISION-1-B-Montage-3-4 🔴`
* **Visual Recipe:** (3-4 clips: [Cinematic Stock B-Roll] Montage) Idealized "after" state clips.
* **Story/Emotion:** Creates powerful Longing and Inspiration—the "Promised Land."
* **Natron VFX:** Apply **EFFECT-M-02** (Speed Ramp) + **EFFECT-TR-05** (Dissolve) + **EFFECT-L-04** (Bloom).
* **Audio (MoviePy):** Aspirational music.

**🔹 Template 18.2 — The Future Self "Mirror"**

* **Code:** `VISION-2-C-1 🟠`
* **Visual Recipe:** (1 C-Roll Composition) PNG cutout of confident coach as aspirational "future self."
* **Story/Emotion:** Visual manifestation of viewer's goal—immense Inspiration.
* **Natron VFX:** Apply **EFFECT-M-16** (Z-Space—requires matte) + **EFFECT-C-12** (Midas Touch Golden).
* **Audio (MoviePy):** N/A.

**🔹 Template 18.3 — The "Promise" Text Reveal**

* **Code:** `VISION-3-C-1 🟣`
* **Visual Recipe:** (1 C-Roll "Showstopper") Complex composition mapping steps to future.
* **Story/Emotion:** Turns abstract promise into concrete plan—Empowerment.
* **Natron VFX:** Complex text animation with **EFFECT-L-04** (Bloom).
* **Audio (MoviePy):** Sequential reveal SFX.

**🔹 Template 18.4 — The "First Person POV" Experience**

* **Code:** `VISION-4-B-1 🔴`
* **Visual Recipe:** (1 clip: B-Roll) First-person POV of desired outcome.
* **Story/Emotion:** Most immersive—places viewer inside the dream.
* **Natron VFX:** Apply **EFFECT-M-14** (Handheld Drift) + **EFFECT-L-04** (Bloom) + **EFFECT-T-02** (Lens Blur).
* **Audio (MoviePy):** N/A.

---

## **Implementation Notes for Stage 5**

### Blueprint Integration

When generating the Blueprint JSON, each scene should reference:

```json
{
  "scene_id": "SC_03",
  "scene_type": "SETUP",
  "template": "SETUP-1-B-1",
  "effects": [
    {"code": "EFFECT-M-01", "params": {"start_scale": 1.0, "end_scale": 1.1}},
    {"code": "EFFECT-C-01"}
  ],
  "audio_effects": ["EFFECT-A-03"]
}
```

### Effect Chaining

Effects are applied in sequence:
1. Motion effects first (Transform)
2. Color/Grade effects second (ColorCorrect)
3. Transitions last (Dissolve/Merge)

### Audio Effects Separation

All EFFECT-A-## codes are handled by MoviePy during Stage 6, not Natron:
- EFFECT-A-01: Standard Vocal Chain
- EFFECT-A-02: Internal Thought Reverb
- EFFECT-A-03: Tension Drone
- EFFECT-A-04: Cinematic Riser
- EFFECT-A-05: Impact Hit
- EFFECT-A-06: Found Clip Audio
- EFFECT-A-07: Audio Fade
- EFFECT-A-08: Environmental Diegetic
- EFFECT-A-09: Distorted Reality
- EFFECT-A-10: Tape Degradation
- EFFECT-A-11: Kinetic Whoosh

---

**CMF Conscious Scene Builder V4 — Natron + CMF 2.0 Edition**
*Conscious Movie Factory December 2024*
