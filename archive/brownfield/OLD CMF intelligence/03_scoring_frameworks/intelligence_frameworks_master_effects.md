###  **intelligence/frameworks/master\_effects.yaml**

Purpose: The "Mechanical Room" codes for the Asset Taskmaster and Post-Super.

Source: The Master Effects Library 09-07

YAML

\# \==============================================================================  
\# MASTER EFFECTS LIBRARY (V4 \- CapCut Edition)  
\# Used by: Asset Taskmaster, Post-Super  
\# \==============================================================================

motion\_effects:  
  EFFECT-M-01: "The Slow Zoom Confession (Keyframed Scale)"  
  EFFECT-M-02: "The Speed Ramp Chaos (Speed Curve)"  
  EFFECT-M-03: "The Anxiety Camera Shake (Shake Effect)"  
  EFFECT-M-04: "The Emphasis Punch-In (Fast Zoom)"  
  EFFECT-M-05: "The Dolly Push (3D Zoom Pro)"  
  EFFECT-M-06: "The Rack Focus Shift (Blur \+ Mask)"  
  EFFECT-M-08: "The Vertical Drift (Position Keyframes)"  
  EFFECT-M-09: "The Rotational 'Dutch Angle' Roll"  
  EFFECT-M-10: "The Object-Tracked Pin"  
  EFFECT-M-11: "The Vertical Parallax"  
  EFFECT-M-12: "The 'Breathing' Effect (Pulsing Scale)"  
  EFFECT-M-13: "The 'Play Pendulum' Float"  
  EFFECT-M-14: "The 'Dynamic Handheld' Drift"  
  EFFECT-M-15: "The '3D Screen' Flip"  
  EFFECT-M-16: "The 'Immersive' Z-Space Sandwich"

color\_grades:  
  EFFECT-C-01: "The 'Personal Low' Grade (Cool/Desaturated)"  
  EFFECT-C-02: "The 'Hopeful' Grade (Warm/Golden)"  
  EFFECT-C-03: "The 'Nostalgic Memory' Grade (Faded/Warm)"  
  EFFECT-C-04: "The High-Contrast 'Modern' Grade"  
  EFFECT-C-05: "The 'Pro 4K' Polish"  
  EFFECT-C-06: "The 'Sin City' Color Isolate"  
  EFFECT-C-07: "The 'Spotlight' Focus Highlight"  
  EFFECT-C-09: "The 'Comedic' Grade"  
  EFFECT-C-10: "The 'Ethereal Spark' Grade"  
  EFFECT-C-12: "The 'Midas Touch' Golden Grade"  
  EFFECT-C-13: "The 'Romantic' Soft-Focus Grade"  
  EFFECT-C-14: "The 'Investigative' Grade"  
  EFFECT-C-15: "The 'Looming Shadow' Grade"  
  EFFECT-C-16: "The 'Playful Pop' Grade"  
  EFFECT-C-17: "The 'Gritty Determination' Grade"  
  EFFECT-C-18: "The 'Authentic & Raw' Grade"  
  EFFECT-C-19: "The 'Natural Daylight' Grade"  
  EFFECT-C-20: "The 'Fireside Chat' Grade"  
  EFFECT-C-21: "The 'Psychedelic Trip' Grade"  
  EFFECT-C-22: "The 'Graphic Novel' Grade"

texture\_overlays:  
  EFFECT-T-01: "The Cinematic Film Grain"  
  EFFECT-T-02: "The Dreamlike Lens Blur"  
  EFFECT-T-03: "The 'Living Doodle' Texture"  
  EFFECT-T-04: "The 'VHS Glitch' Texture"  
  EFFECT-T-05: "The 'Paper Collage' Texture"  
  EFFECT-T-06: "The 'Dust & Scratches' Overlay"  
  EFFECT-T-07: "The 'Ink Bleed' Overlay"  
  EFFECT-T-08: "The 'Blueprint Grid' Overlay"  
  EFFECT-T-09: "The 'Archival Film' Texture"

light\_effects:  
  EFFECT-L-01: "The Cinematic Light Leak"  
  EFFECT-L-03: "The 'Cathedral' Light Rays"  
  EFFECT-L-04: "The 'Aspirational' Bloom"

transitions:  
  EFFECT-TR-01: "The Glitch Transition"  
  EFFECT-TR-02: "The Cinematic Film Burn"  
  EFFECT-TR-03: "The Whip Pan"  
  EFFECT-TR-04: "The Data Corruption"  
  EFFECT-TR-05: "The Gentle Dissolve"  
  EFFECT-TR-06: "The Mask Reveal"  
  EFFECT-TR-07: "The 'Visual Continuity' Match-Cut"  
  EFFECT-TR-08: "The 'MKBHD' Side-Screen Swipe"  
  EFFECT-TR-09: "The 'Text-Behind' Depth Shift"  
  EFFECT-TR-10: "The 'Invisible' Hard Cut"  

## Research-Backed Effect Intelligence Overlay (2026)

The effect IDs above remain stable. The overlay below adds the psychological metadata needed for intelligent effect selection, validation, and sequencing.

### Effect Metadata Contract

```yaml
effect_research_contract:
  cls_impact: 1-5
  arousal: 1-10
  presence: 1-10
  pad_vector:
    pleasure: -1.0_to_1.0
    arousal: -1.0_to_1.0
    dominance: -1.0_to_1.0
  attention_role:
    - orient
    - signal
    - intensify
    - immerse
    - punctuate
    - resolve
  congruence_mode:
    - default_safe
    - conditional
    - mismatch_only
  sync_window_ms:
    discrete_event: min-max
  text_competition_risk:
    - low
    - medium
    - high
  best_for:
    - hook
    - setup
    - challenge
    - turning_point
    - resolution
    - vision
    - evidence
  avoid_when:
    - high_intrinsic_load
    - dense_text
    - low_frame_rate
    - emotional_peak_already_full
```

### Motion Effect Semantics

```yaml
motion_effect_intelligence:
  EFFECT-M-01:
    cls_impact: 1
    arousal: 3
    presence: 8
    attention_role: immerse
    congruence_mode: default_safe
    best_for: [setup, turning_point, resolution, pause]
    avoid_when: []
    note: "Slow zoom improves intimacy and focus without overloading encoding."

  EFFECT-M-02:
    cls_impact: 5
    arousal: 9
    presence: 2
    attention_role: intensify
    congruence_mode: conditional
    best_for: [challenge, tease, high-energy vision]
    avoid_when: [high_intrinsic_load, dense_text, low_frame_rate]
    note: "Use as a short spike, not as a sustained default."

  EFFECT-M-03:
    cls_impact: 4
    arousal: 9
    presence: 3
    attention_role: intensify
    congruence_mode: conditional
    best_for: [challenge, tease]
    avoid_when: [resolution, evidence, demonstration]
    note: "Shake induces sympathetic stress quickly and should be narratively justified."

  EFFECT-M-04:
    cls_impact: 2
    arousal: 6
    presence: 6
    attention_role: signal
    congruence_mode: default_safe
    sync_window_ms:
      discrete_event: -20-100
    best_for: [hook, evidence, demonstration, turning_point]
    avoid_when: []
    note: "Punch-ins work best as emphasis markers aligned to a word, beat, or reveal."

  EFFECT-M-05:
    cls_impact: 2
    arousal: 4
    presence: 9
    attention_role: immerse
    congruence_mode: default_safe
    best_for: [setup, turning_point, vision]
    avoid_when: []
    note: "Dolly push is high-presence and best reserved for significance or intimacy."

  EFFECT-M-06:
    cls_impact: 2
    arousal: 4
    presence: 5
    attention_role: signal
    congruence_mode: conditional
    best_for: [setup, turning_point]
    avoid_when: [dense_text]
    note: "Rack-focus style blur shifts should guide attention, not obscure the core referent."

  EFFECT-M-08:
    cls_impact: 2
    arousal: 3
    presence: 7
    attention_role: immerse
    congruence_mode: default_safe
    best_for: [pause, vibe, archetype]
    avoid_when: []
    note: "Vertical drift supports contemplative or aspirational states."

  EFFECT-M-09:
    cls_impact: 4
    arousal: 7
    presence: 3
    attention_role: intensify
    congruence_mode: conditional
    best_for: [contrast, challenge, destabilization]
    avoid_when: [pause, evidence]
    note: "Dutch-angle motion increases tension and should stay brief."

  EFFECT-M-10:
    cls_impact: 2
    arousal: 3
    presence: 6
    attention_role: signal
    congruence_mode: default_safe
    best_for: [demonstration, evidence]
    avoid_when: []
    note: "Tracked pins are effective when they reduce search, not when they add clutter."

  EFFECT-M-11:
    cls_impact: 2
    arousal: 4
    presence: 8
    attention_role: immerse
    congruence_mode: default_safe
    best_for: [vision, vibe, symbolic_echo]
    avoid_when: []
    note: "Parallax increases spatial presence if movement remains smooth and readable."

  EFFECT-M-12:
    cls_impact: 1
    arousal: 4
    presence: 9
    attention_role: immerse
    congruence_mode: default_safe
    best_for: [encouraging_change, vibe, resolution, pause]
    avoid_when: []
    note: "Human-like breathing motion adds life without imposing major cognitive cost."

  EFFECT-M-14:
    cls_impact: 3
    arousal: 7
    presence: 6
    attention_role: intensify
    congruence_mode: conditional
    best_for: [vision, challenge, kinetic hooks]
    avoid_when: [dense_text, explanation-heavy beats]
    note: "Dynamic handheld drift can feel vivid on mobile but loses clarity if stacked with text."

  EFFECT-M-15:
    cls_impact: 3
    arousal: 6
    presence: 4
    attention_role: punctuate
    congruence_mode: conditional
    best_for: [demonstration, reveal]
    avoid_when: [emotionally intimate beats]
    note: "3D flips are better for product/interface reveal than for emotional testimony."

  EFFECT-M-16:
    cls_impact: 3
    arousal: 3
    presence: 10
    attention_role: immerse
    congruence_mode: default_safe
    best_for: [vision, vibe, archetype]
    avoid_when: [low-quality source layers]
    note: "Z-space layering is the highest-presence motion option when depth cues are clean."
```

### Color Grade Semantics

```yaml
color_grade_intelligence:
  EFFECT-C-01:
    pad_vector: {pleasure: -0.65, arousal: -0.70, dominance: 0.30}
    attention_role: immerse
    congruence_mode: default_safe
    best_for: [setup, challenge, archetype]
    note: "Cool/desaturated grades lower pleasure and arousal to signal personal low, struggle, or melancholy."

  EFFECT-C-02:
    pad_vector: {pleasure: 0.80, arousal: 0.10, dominance: -0.45}
    attention_role: resolve
    congruence_mode: default_safe
    best_for: [resolution, symbolic_echo, vision]
    note: "Warm/golden grades support relief, safety, and hopeful consolidation."

  EFFECT-C-03:
    pad_vector: {pleasure: 0.65, arousal: -0.25, dominance: -0.15}
    attention_role: immerse
    congruence_mode: default_safe
    best_for: [setup, memory_montage, symbolic_echo]
    note: "Faded warmth supports nostalgia and autobiographical retrieval."

  EFFECT-C-04:
    pad_vector: {pleasure: 0.25, arousal: 0.55, dominance: 0.45}
    attention_role: intensify
    congruence_mode: default_safe
    best_for: [hook, truth, community, modern contrast]
    note: "High contrast sharpens attention and authority when the message is already simple."

  EFFECT-C-07:
    pad_vector: {pleasure: 0.20, arousal: 0.35, dominance: 0.30}
    attention_role: signal
    congruence_mode: default_safe
    best_for: [demonstration, evidence, prop-driven beats]
    note: "Spotlighting should reduce search cost and force focal clarity."

  EFFECT-C-12:
    pad_vector: {pleasure: 0.70, arousal: 0.35, dominance: 0.10}
    attention_role: resolve
    congruence_mode: default_safe
    best_for: [vision, aspiration]
    note: "Golden aspirational grades should pair with bright, high-register audio."

  EFFECT-C-17:
    pad_vector: {pleasure: -0.15, arousal: 0.35, dominance: 0.75}
    attention_role: intensify
    congruence_mode: default_safe
    best_for: [challenge, vibe, authority arcs]
    note: "Low-brightness, restrained color increases dominance and resolve."

  EFFECT-C-18:
    pad_vector: {pleasure: -0.05, arousal: 0.10, dominance: 0.40}
    attention_role: immerse
    congruence_mode: default_safe
    best_for: [testimonial, documentary, truth]
    note: "Raw grades help authenticity when polish would reduce trust."
```

### Transition And Audio Rules

```yaml
transition_and_audio_intelligence:
  transitions:
    EFFECT-TR-01:
      cls_impact: 4
      attention_role: punctuate
      congruence_mode: mismatch_only
      best_for: [hook, tease, glitch contrast]
      avoid_when: [resolution, reflective moments]

    EFFECT-TR-03:
      cls_impact: 3
      attention_role: intensify
      congruence_mode: conditional
      sync_window_ms:
        discrete_event: -20-100
      best_for: [turning_point, evidence pivot, challenge]

    EFFECT-TR-05:
      cls_impact: 1
      attention_role: resolve
      congruence_mode: default_safe
      best_for: [setup, resolution, vision]

    EFFECT-TR-07:
      cls_impact: 1
      attention_role: signal
      congruence_mode: default_safe
      best_for: [symbolic_echo, before_after, continuity-driven montage]
      note: "Best transition for eye-tracking continuity and Kuleshov legibility."

    EFFECT-TR-10:
      cls_impact: 1
      attention_role: signal
      congruence_mode: default_safe
      best_for: [high fluency dialogue and reaction-context edits]

  audio_effects:
    EFFECT-A-01:
      cls_impact: 1
      attention_role: resolve
      congruence_mode: default_safe
      best_for: [all spoken content]
      note: "Protect speech intelligibility before adding stylistic layers."

    EFFECT-A-02:
      cls_impact: 2
      attention_role: immerse
      congruence_mode: conditional
      best_for: [turning_point, reflective setup, symbolic_echo]
      note: "Use to signal interiority, not as generic polish."

    EFFECT-A-03:
      cls_impact: 2
      attention_role: intensify
      congruence_mode: default_safe
      best_for: [setup tension, foreshadowing]

    EFFECT-A-04:
      cls_impact: 3
      attention_role: intensify
      congruence_mode: conditional
      sync_window_ms:
        discrete_event: -20-100
      best_for: [challenge, turning_point]

    EFFECT-A-05:
      cls_impact: 2
      attention_role: punctuate
      congruence_mode: conditional
      sync_window_ms:
        discrete_event: -20-80
      best_for: [hook, evidence, contrast, kinetic punchline]

    EFFECT-A-06:
      cls_impact: 2
      attention_role: signal
      congruence_mode: default_safe
      best_for: [found_clip, archival, juxtaposition]
      note: "Lo-fi audio supports contextual reframing and authenticity coding."

    EFFECT-A-08:
      cls_impact: 1
      attention_role: immerse
      congruence_mode: default_safe
      best_for: [symbolic_echo, resolution, vision]

    EFFECT-A-11:
      cls_impact: 2
      attention_role: punctuate
      congruence_mode: conditional
      sync_window_ms:
        discrete_event: -20-100
      best_for: [punch-ins, wipes, chart reveals, contrast beats]
```

### Graphic And Text Heuristics

```yaml
graphic_and_text_rules:
  EFFECT-G-03:
    best_for: [truth, community, resolution]
    note: "Quote cards should present one idea cleanly, not become a second script."

  EFFECT-G-04:
    best_for: [challenge, contrast]
    note: "Aggressive collage works when the narrative job is takedown or enemy-framing."

  EFFECT-G-14:
    best_for: [evidence]
    note: "Sequential chart building follows signaling and temporal contiguity principles."

  EFFECT-G-16:
    best_for: [demonstration, evidence]
    note: "Highlighting is preferred over extra motion when guiding attention through interfaces or documents."

  EFFECT-TXT-09:
    text_competition_risk: low
    best_for: [truth, affirmation, resolution]

  EFFECT-TXT-10:
    text_competition_risk: medium
    best_for: [tease, reflective question]
    note: "Typewriter reveal creates anticipation; keep line length short."

  EFFECT-TXT-13:
    text_competition_risk: high
    best_for: [captioning only]
    note: "Captions must default to keyword emphasis and safe-zone placement in vertical video."

  EFFECT-TXT-14:
    text_competition_risk: medium
    best_for: [evidence, kinetic stat reveals]
```

### Selection Doctrine

- Choose effects by scene job first, then style.
- Protect speech and focal clarity before adding stimulation.
- Prefer congruent color, motion, and sound by default.
- When the beat is emotionally heavy, simplify the effect stack instead of escalating it.
- Use the highest-arousal effects as interrupts, not wallpaper.
- If a scene already contains dense text or complex proof, downgrade motion and transition intensity.
  EFFECT-TR-11: "The 'Fade to Black' Narrative Punctuation"

audio\_effects:  
  EFFECT-A-01: "The Standard Vocal Chain (Enhance Voice)"  
  EFFECT-A-02: "The 'Internal Thought' Reverb"  
  EFFECT-A-03: "The 'Tension' Drone"  
  EFFECT-A-04: "The Cinematic Riser"  
  EFFECT-A-05: "The Impact Hit"  
  EFFECT-A-06: "The 'Found Clip' Audio (Radio/Lo-Fi)"  
  EFFECT-A-07: "The 'Jesse' AI Narrator"  
  EFFECT-A-08: "The 'Environmental' Diegetic Layer"  
  EFFECT-A-09: "The 'AI Dialogue' Isolation"  
  EFFECT-A-10: "The 'Character' Voice Changer"  
  EFFECT-A-11: "The 'Kinetic' Whoosh Accent"  
  EFFECT-A-12: "The 'Audio Rip' Extractor"

graphic\_effects:  
  EFFECT-G-01: "The Desperation Collage"  
  EFFECT-G-02: "The Blueprint Reveal"  
  EFFECT-G-03: "The Kinetic Quote Card"  
  EFFECT-G-04: "The 'Takedown' Collage"  
  EFFECT-G-05: "The Animated Bar Chart"  
  EFFECT-G-06: "The 'Symbolic Echo' Reveal"  
  EFFECT-G-07: "The Isaac-Style Flowchart"  
  EFFECT-G-08: "The 'Juxtaposition' Split Collage"  
  EFFECT-G-09: "The 'Redacted Tease'"  
  EFFECT-G-10: "The 'Mentor Quote' Collage"  
  EFFECT-G-11: "The 'Transformation' Reveal"  
  EFFECT-G-12: "The Clean Icon List"  
  EFFECT-G-13: "The 'VOX' Animated Map Route"  
  EFFECT-G-14: "The 'Underscore' Animated Chart"  
  EFFECT-G-15: "The 'Isaac' Gradient Flowchart"  
  EFFECT-G-16: "The 'Digital Highlighter' Text Reveal"  
  EFFECT-G-17: "The 'Kinetic' Video-in-Text"  
  EFFECT-G-18: "The 'Segment' Progress Bar"

text\_effects:  
  EFFECT-TXT-01: "The Crisp Fade-In"  
  EFFECT-TXT-02: "The Gentle Drift & Fade"  
  EFFECT-TXT-03: "The Kinetic Pop"  
  EFFECT-TXT-04: "The 'Clarity' Scale Wipe"  
  EFFECT-TXT-05: "The Quick Color Flash"  
  EFFECT-TXT-06: "The Ghostly Echo"  
  EFFECT-TXT-07: "The Background Dim"  
  EFFECT-TXT-08: "The Subtle Rotational Settle"  
  EFFECT-TXT-09: "The Cinematic Glow"  
  EFFECT-TXT-10: "The Character Reveal (Typewriter)"  
  EFFECT-TXT-11: "The Tracking Expand"  
  EFFECT-TXT-12: "The Liquid Distortion"  
  EFFECT-TXT-13: "The 'Dynamic Auto-Caption' System"  
  EFFECT-TXT-14: "The 'Isaac-Style' Bounce Reveal"  
  EFFECT-TXT-15: "The 'Contained' Mask Reveal"

