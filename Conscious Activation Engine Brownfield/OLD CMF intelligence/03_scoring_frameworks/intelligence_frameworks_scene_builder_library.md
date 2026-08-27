###  **intelligence/frameworks/scene\_builder\_library.yaml**

Purpose: The 18 visual recipes used by the Blueprint Architect to construct the video.

Source: The Conscious Scene Builder (V3)

YAML

\# \==============================================================================  
\# CONSCIOUS SCENE BUILDER LIBRARY (V3)  
\# Used by: Blueprint Architect, Virtual Director  
\# \==============================================================================

scenes:  
  \# \--- HOOK SCENES (0-5s) \---  
  HOOK-1-AB-2:  
    name: "The Talking Head Pattern Match"  
    type: "HOOK"  
    cls: 2  
    elements: \["A-Roll", "Coach B-Roll"\]  
    visual\_recipe: "Punchy A-Roll statement \+ Matching B-Roll visual."  
    effects: \["EFFECT-M-04", "EFFECT-A-05"\]

  HOOK-2-B-1:  
    name: "The Cinematic Foreshadow"  
    type: "HOOK"  
    cls: 1  
    elements: \["Cinematic B-Roll"\]  
    visual\_recipe: "Single, slow, mysterious B-Roll shot \+ Cryptic VO."  
    effects: \["EFFECT-T-01", "EFFECT-A-03"\]

  HOOK-3-BA-2:  
    name: "The J-Cut Intrigue"  
    type: "HOOK"  
    cls: 2  
    elements: \["Coach B-Roll", "A-Roll"\]  
    visual\_recipe: "B-Roll visual \+ A-Roll audio start (J-Cut) \-\> Cut to A-Roll."  
    effects: \["EFFECT-C-01", "EFFECT-A-02"\]

  HOOK-4-BA-2:  
    name: "The Found Clip Reframe"  
    type: "HOOK"  
    cls: 3  
    elements: \["Found Clip", "A-Roll"\]  
    visual\_recipe: "Iconic E-Roll clip \-\> Smash Cut \-\> Coach contradicts it."  
    effects: \["EFFECT-TR-01", "EFFECT-A-06"\]

  HOOK-5-AE-2:  
    name: "The A-Roll Setup & Found Clip Reveal"  
    type: "HOOK"  
    cls: 3  
    elements: \["A-Roll", "Found Clip"\]  
    visual\_recipe: "A-Roll setup \-\> L-Cut \-\> Found Clip punchline."  
    effects: \["L-Cut", "EFFECT-A-06"\]

  \# \--- SETUP SCENES (5-15s) \---  
  SETUP-1-B-1:  
    name: "The 'Personal Low' Visualization"  
    type: "SETUP"  
    cls: 2  
    elements: \["Cinematic B-Roll"\]  
    visual\_recipe: "Single artful shot depicting despair/stagnation."  
    effects: \["EFFECT-M-01", "EFFECT-C-01", "EFFECT-A-03"\]

  SETUP-2-B-Montage-3-4:  
    name: "The Authentic Memory Montage"  
    type: "SETUP"  
    cls: 3  
    elements: \["Coach B-Roll Montage"\]  
    visual\_recipe: "Montage of authentic struggle clips."  
    effects: \["EFFECT-TR-05", "EFFECT-C-03", "EFFECT-A-02"\]

  SETUP-3-B-1:  
    name: "The Prop-Driven Metaphor"  
    type: "SETUP"  
    cls: 2  
    elements: \["Coach B-Roll"\]  
    visual\_recipe: "Coach interacting with a symbolic object (e.g., Clock)."  
    effects: \["EFFECT-C-07", "Foley SFX"\]

  SETUP-4-AB-2:  
    name: "The L-Cut Vulnerability Drop"  
    type: "SETUP"  
    cls: 3  
    elements: \["A-Roll", "Coach B-Roll"\]  
    visual\_recipe: "Vulnerable A-Roll line \-\> Audio L-Cut \-\> Contemplative B-Roll."  
    effects: \["L-Cut", "EFFECT-M-06"\]

  \# \--- CHALLENGE SCENES (15-30s) \---  
  CHALLENGE-1-B-Montage-3-5:  
    name: "The Struggle Montage"  
    type: "CHALLENGE"  
    cls: 4  
    elements: \["B-Roll Montage"\]  
    visual\_recipe: "Accelerating montage of physical struggle."  
    effects: \["EFFECT-M-02", "EFFECT-M-03", "EFFECT-TR-02", "EFFECT-A-04"\]

  CHALLENGE-2-AC-2:  
    name: "The C-Roll 'Enemy' Collage"  
    type: "CHALLENGE"  
    cls: 4  
    elements: \["A-Roll", "C-Roll"\]  
    visual\_recipe: "A-Roll names enemy \-\> Aggressive C-Roll takedown."  
    effects: \["EFFECT-G-04", "EFFECT-A-05"\]

  CHALLENGE-3-B-Montage-4-6:  
    name: "The Found Clip Chaos Montage"  
    type: "CHALLENGE"  
    cls: 4  
    elements: \["Coach B-Roll", "Found Clips"\]  
    visual\_recipe: "Rapid intercut of personal stress and universal chaos."  
    effects: \["EFFECT-TR-04", "EFFECT-A-06", "SFX\_Glitch"\]

  CHALLENGE-4-B-1:  
    name: "The Prop-Driven Struggle"  
    type: "CHALLENGE"  
    cls: 1  
    elements: \["Coach B-Roll"\]  
    visual\_recipe: "Single shot of physical struggle with a prop."  
    effects: \["EFFECT-M-01", "Diegetic SFX"\]

  \# \--- JUXTAPOSITION SCENES \---  
  JUXTAPOSE-1-AB-2:  
    name: "The Found Clip Punchline"  
    type: "JUXTAPOSITION"  
    cls: 3  
    elements: \["A-Roll", "Found Clip"\]  
    visual\_recipe: "Serious A-Roll \-\> Hard Cut \-\> Ironic Found Clip."  
    effects: \["EFFECT-A-06", "SFX\_Record\_Scratch"\]

  JUXTAPOSE-2-B-1:  
    name: "The Stylized Mismatch"  
    type: "JUXTAPOSITION"  
    cls: 4  
    elements: \["B-Roll", "A-Roll VO"\]  
    visual\_recipe: "Calm VO over chaotic/speed-ramped visuals."  
    effects: \["EFFECT-M-02", "EFFECT-A-01"\]

  JUXTAPOSE-3-BB-2:  
    name: "The Coach B-Roll Match Cut"  
    type: "JUXTAPOSITION"  
    cls: 3  
    elements: \["Coach B-Roll", "Coach B-Roll"\]  
    visual\_recipe: "Match cut between two different states of the coach."  
    effects: \["EFFECT-TR-07", "EFFECT-C-04", "EFFECT-C-02"\]

  JUXTAPOSE-4-BB-2:  
    name: "The Then vs. Now"  
    type: "JUXTAPOSITION"  
    cls: 3  
    elements: \["Coach B-Roll", "Coach B-Roll"\]  
    visual\_recipe: "Past state \-\> Transition \-\> Present state."  
    effects: \["EFFECT-TR-03", "SFX\_Chime\_Bright"\]

  \# \--- TURNING POINT SCENES (30-40s) \---  
  TURNING\_POINT-1-B-1:  
    name: "The Reaction Shot Hold"  
    type: "TURNING\_POINT"  
    cls: 1  
    elements: \["B-Roll"\]  
    visual\_recipe: "Tight close-up on face, expression shifting. Silent."  
    effects: \["EFFECT-M-01", "Sonic Vacuum"\]

  TURNING\_POINT-2-B-1:  
    name: "The Prop-Driven Metaphor"  
    type: "TURNING\_POINT"  
    cls: 2  
    elements: \["Coach B-Roll"\]  
    visual\_recipe: "Symbolic action (e.g., Key turning, Candle lighting)."  
    effects: \["EFFECT-C-02", "Resonant SFX"\]

  TURNING\_POINT-3-BB-2:  
    name: "The Whip Pan Pivot"  
    type: "TURNING\_POINT"  
    cls: 3  
    elements: \["Coach B-Roll"\]  
    visual\_recipe: "Struggle shot \-\> Whip Pan \-\> Action shot."  
    effects: \["EFFECT-TR-03", "EFFECT-A-11"\]

  TURNING\_POINT-4-BA-2:  
    name: "The J-Cut 'Aha\!' Moment"  
    type: "TURNING\_POINT"  
    cls: 2  
    elements: \["Coach B-Roll", "A-Roll"\]  
    visual\_recipe: "Contemplative B-Roll \-\> J-Cut Audio of Realization."  
    effects: \["EFFECT-M-08", "EFFECT-A-02"\]

  \# \--- RESOLUTION SCENES (40-50s) \---  
  RESOLUTION-1-B-1:  
    name: "The Cinematic Release"  
    type: "RESOLUTION"  
    cls: 3  
    elements: \["Cinematic B-Roll"\]  
    visual\_recipe: "Slow-motion shot of peace/relief."  
    effects: \["Slow Motion", "EFFECT-C-02", "EFFECT-TR-02"\]

  RESOLUTION-2-C-1:  
    name: "The C-Roll Affirmation"  
    type: "RESOLUTION"  
    cls: 2  
    elements: \["C-Roll"\]  
    visual\_recipe: "Single powerful word/quote animating on screen."  
    effects: \["EFFECT-G-03", "EFFECT-TXT-09", "SFX\_Bell\_Chime"\]

  RESOLUTION-3-B-1:  
    name: "The Bookend B-Roll"  
    type: "RESOLUTION"  
    cls: 2  
    elements: \["Coach B-Roll"\]  
    visual\_recipe: "Re-use of 'Challenge' prop/shot but in resolved state."  
    effects: \["EFFECT-C-02"\]

  RESOLUTION-4-A-1:  
    name: "The A-Roll 'Sigh' Moment"  
    type: "RESOLUTION"  
    cls: 1  
    elements: \["A-Roll"\]  
    visual\_recipe: "Uncut shot of coach taking a breath/smiling."  
    effects: \["EFFECT-M-01", "SFX\_Human\_Breath\_Calm"\]

  \# \--- ENCOURAGING CHANGE SCENES \---  
  ENCOURAGE-1-A-1:  
    name: "The Direct-to-Camera A-Roll"  
    type: "ENCOURAGING\_CHANGE"  
    cls: 2  
    elements: \["A-Roll"\]  
    visual\_recipe: "Coach breaks 4th wall, delivers call to action."  
    effects: \["EFFECT-M-12", "EFFECT-A-01"\]

  ENCOURAGE-2-C-1:  
    name: "The C-Roll 'Blueprint'"  
    type: "ENCOURAGING\_CHANGE"  
    cls: 5  
    elements: \["C-Roll"\]  
    visual\_recipe: "Animated framework/diagram breakdown."  
    effects: \["EFFECT-G-02", "EFFECT-G-15"\]

  ENCOURAGE-3-B-Montage-3-4:  
    name: "The Social Proof Montage"  
    type: "ENCOURAGING\_CHANGE"  
    cls: 3  
    elements: \["B-Roll Montage"\]  
    visual\_recipe: "Montage of successful clients/community."  
    effects: \["EFFECT-TR-05", "EFFECT-C-04"\]

  ENCOURAGE-4-AC-2:  
    name: "The C-Roll Reflective Question"  
    type: "ENCOURAGING\_CHANGE"  
    cls: 2  
    elements: \["A-Roll", "C-Roll"\]  
    visual\_recipe: "A-Roll poses question \-\> Text appears on screen."  
    effects: \["EFFECT-TXT-10", "SFX\_Typewriter"\]

  \# \--- SYMBOLIC ECHO SCENES \---  
  ECHO-1-BB-2:  
    name: "The B-Roll Match Cut"  
    type: "SYMBOLIC\_ECHO"  
    cls: 3  
    elements: \["B-Roll", "B-Roll"\]  
    visual\_recipe: "Match cut of same object in 'Challenge' vs 'Resolution' states."  
    effects: \["EFFECT-TR-07", "EFFECT-C-01", "EFFECT-C-02"\]

  ECHO-2-C-1:  
    name: "The C-Roll Symbol Transformation"  
    type: "SYMBOLIC\_ECHO"  
    cls: 2  
    elements: \["C-Roll"\]  
    visual\_recipe: "Icon morphs into new symbol."  
    effects: \["EFFECT-G-11", "SFX\_Ascend"\]

  ECHO-3-A-1:  
    name: "The Audio Callback"  
    type: "SYMBOLIC\_ECHO"  
    cls: 1  
    elements: \["A-Roll"\]  
    visual\_recipe: "Visual: Confident A-Roll. Audio: Echo of past vulnerability."  
    effects: \["EFFECT-A-02"\]

  ECHO-4-B-1:  
    name: "The AI Environmental Shift"  
    type: "SYMBOLIC\_ECHO"  
    cls: 2  
    elements: \["AI Animated B-Roll"\]  
    visual\_recipe: "Same AI environment as start, but transformed (cleaner/brighter)."  
    effects: \["EFFECT-C-02", "EFFECT-A-08"\]

  \# \--- FRAME & CONTRAST SCENES \---  
  CONTRAST-1-C-1:  
    name: "The C-Roll Split-Screen"  
    type: "FRAME\_CONTRAST"  
    cls: 4  
    elements: \["C-Roll"\]  
    visual\_recipe: "Split screen comparing 'Their Way' vs 'Your Way'."  
    effects: \["EFFECT-G-08"\]

  CONTRAST-2-AB-Montage-3-5:  
    name: "The A-Roll Fast-Cut Debate"  
    type: "FRAME\_CONTRAST"  
    cls: 4  
    elements: \["A-Roll", "Found Clips"\]  
    visual\_recipe: "Ping-pong cuts between coach and opposing view clips."  
    effects: \["EFFECT-M-04", "EFFECT-A-11"\]

  CONTRAST-3-C-1:  
    name: "The C-Roll 'Guru' Takedown"  
    type: "FRAME\_CONTRAST"  
    cls: 4  
    elements: \["C-Roll"\]  
    visual\_recipe: "Collage visually dismissing bad advice."  
    effects: \["EFFECT-G-04", "EFFECT-A-05"\]

  CONTRAST-4-BC-2:  
    name: "The Layered Text C-Roll"  
    type: "FRAME\_CONTRAST"  
    cls: 2  
    elements: \["B-Roll", "C-Roll"\]  
    visual\_recipe: "Text misconception is physically covered by truth text."  
    effects: \["EFFECT-TXT-01", "EFFECT-TXT-03"\]

  \# \--- THE TEASE SCENES \---  
  TEASE-1-C-1:  
    name: "The Redacted C-Roll"  
    type: "THE\_TEASE"  
    cls: 3  
    elements: \["C-Roll"\]  
    visual\_recipe: "Typewriter text with key word redacted."  
    effects: \["EFFECT-G-09", "SFX\_Censor\_Beep"\]

  TEASE-2-B-1:  
    name: "The Incomplete B-Roll Action"  
    type: "THE\_TEASE"  
    cls: 1  
    elements: \["B-Roll"\]  
    visual\_recipe: "Action builds but cuts to black before completion."  
    effects: \["SFX\_Impact\_Sharp"\]

  TEASE-3-A-1:  
    name: "The Out-of-Context A-Roll"  
    type: "THE\_TEASE"  
    cls: 3  
    elements: \["A-Roll"\]  
    visual\_recipe: "Cold open of coach at peak emotion."  
    effects: \["EFFECT-M-03", "EFFECT-C-04"\]

  TEASE-4-B-Montage-4-6:  
    name: "The Glitchy Flash Montage"  
    type: "THE\_TEASE"  
    cls: 4  
    elements: \["Mixed Montage"\]  
    visual\_recipe: "Rapid fire fragmented clips."  
    effects: \["EFFECT-TR-04", "SFX\_Glitch"\]

  \# \--- VOICE OF TRUTH SCENES \---  
  TRUTH-1-C-1:  
    name: "The C-Roll Quote Card"  
    type: "VOICE\_OF\_TRUTH"  
    cls: 2  
    elements: \["C-Roll"\]  
    visual\_recipe: "Elegant quote animation."  
    effects: \["EFFECT-G-03", "EFFECT-TXT-09"\]

  TRUTH-2-B-1:  
    name: "The Archival Audio Overlay"  
    type: "VOICE\_OF\_TRUTH"  
    cls: 2  
    elements: \["B-Roll", "Found Clip Audio"\]  
    visual\_recipe: "Modern B-Roll with old speech audio."  
    effects: \["EFFECT-A-06", "EFFECT-C-04"\]

  TRUTH-3-C-1:  
    name: "The C-Roll Mentor Collage"  
    type: "VOICE\_OF\_TRUTH"  
    cls: 3  
    elements: \["C-Roll"\]  
    visual\_recipe: "Collage of mentor image and quote."  
    effects: \["EFFECT-G-10"\]

  TRUTH-4-AB-2:  
    name: "The A-Roll 'Narrator' Mode"  
    type: "VOICE\_OF\_TRUTH"  
    cls: 2  
    elements: \["A-Roll", "AI Animated B-Roll"\]  
    visual\_recipe: "Letterboxed A-Roll quoting a source \+ Epic B-Roll."  
    effects: \["Letterbox", "EFFECT-C-02"\]

  \# \--- ARCHETYPAL MOMENT SCENES \---  
  ARCHETYPE-1-C-1:  
    name: "The Archetypal Foreshadow"  
    type: "ARCHETYPAL\_MOMENT"  
    cls: 2  
    elements: \["C-Roll"\]  
    visual\_recipe: "Animated illustration of an archetype."  
    effects: \["EFFECT-M-08", "SFX\_Chime\_Deep"\]

  ARCHETYPE-2-B-1:  
    name: "The Mid-Story Metaphor"  
    type: "ARCHETYPAL\_MOMENT"  
    cls: 2  
    elements: \["B-Roll"\]  
    visual\_recipe: "Epic natural shot (e.g. storm) representing internal state."  
    effects: \["Slow Motion", "EFFECT-C-01"\]

  ARCHETYPE-3-C-1:  
    name: "The Breakthrough Symbol"  
    type: "ARCHETYPAL\_MOMENT"  
    cls: 2  
    elements: \["C-Roll"\]  
    visual\_recipe: "Symbol of problem morphs into symbol of solution."  
    effects: \["EFFECT-G-11", "SFX\_Ascend"\]

  ARCHETYPE-4-B-1:  
    name: "The Mythic Resolution"  
    type: "ARCHETYPAL\_MOMENT"  
    cls: 2  
    elements: \["B-Roll"\]  
    visual\_recipe: "Coach interacting with resolution archetype (e.g. sunrise)."  
    effects: \["EFFECT-C-02", "EFFECT-A-08"\]

  \# \--- DEMONSTRATION SCENES \---  
  DEMO-1-B-1:  
    name: "The Full-Screen Walkthrough"  
    type: "DEMONSTRATION"  
    cls: 2  
    elements: \["Screen Recording"\]  
    visual\_recipe: "Clean screen recording with highlights."  
    effects: \["EFFECT-G-16", "SFX\_Click"\]

  DEMO-2-BC-2:  
    name: "The 'Picture-in-Picture' Guide"  
    type: "DEMONSTRATION"  
    cls: 2  
    elements: \["Screen Recording", "A-Roll"\]  
    visual\_recipe: "Screen recording with coach in corner."  
    effects: \["Masking", "Drop Shadow"\]

  DEMO-3-C-1:  
    name: "The '3D Screen' Showcase"  
    type: "DEMONSTRATION"  
    cls: 4  
    elements: \["C-Roll"\]  
    visual\_recipe: "Screen recording rotates in 3D space."  
    effects: \["EFFECT-M-15", "EFFECT-A-11"\]

  DEMO-4-BC-2:  
    name: "The Highlighted Zoom"  
    type: "DEMONSTRATION"  
    cls: 3  
    elements: \["Screen Recording"\]  
    visual\_recipe: "Punch-in zoom followed by spotlight highlight."  
    effects: \["EFFECT-M-04", "EFFECT-C-07"\]

  \# \--- EVIDENCE SCENES \---  
  EVIDENCE-1-C-1:  
    name: "The Animated Chart Reveal"  
    type: "EVIDENCE"  
    cls: 4  
    elements: \["C-Roll"\]  
    visual\_recipe: "Animated bar chart building sequentially."  
    effects: \["EFFECT-G-14"\]

  EVIDENCE-2-C-1:  
    name: "The 'Kinetic Number' Pop"  
    type: "EVIDENCE"  
    cls: 2  
    elements: \["C-Roll"\]  
    visual\_recipe: "Large statistic pops on screen."  
    effects: \["EFFECT-TXT-14", "EFFECT-A-05"\]

  EVIDENCE-3-B-1:  
    name: "The 'Before & After' Proof"  
    type: "EVIDENCE"  
    cls: 3  
    elements: \["B-Roll", "B-Roll"\]  
    visual\_recipe: "Split screen or whip pan between before/after states."  
    effects: \["EFFECT-TR-03", "EFFECT-C-01", "EFFECT-C-02"\]

  EVIDENCE-4-C-1:  
    name: "The Data Point Highlight"  
    type: "EVIDENCE"  
    cls: 2  
    elements: \["C-Roll"\]  
    visual\_recipe: "Document image with highlighter animation."  
    effects: \["EFFECT-G-16"\]

  \# \--- COMMUNITY SCENES \---  
  COMMUNITY-1-C-1:  
    name: "The 'Tweet/Comment' Showcase"  
    type: "COMMUNITY"  
    cls: 3  
    elements: \["C-Roll"\]  
    visual\_recipe: "Social media comment pop-up."  
    effects: \["EFFECT-G-03", "EFFECT-A-11"\]

  COMMUNITY-2-B-Montage-3-5:  
    name: "The 'UGC' Montage"  
    type: "COMMUNITY"  
    cls: 4  
    elements: \["B-Roll Montage"\]  
    visual\_recipe: "Fast montage of user-generated content."  
    effects: \["EFFECT-TR-01", "EFFECT-C-05"\]

  COMMUNITY-3-C-1:  
    name: "The Video Testimonial Snippet"  
    type: "COMMUNITY"  
    cls: 1  
    elements: \["C-Roll"\]  
    visual\_recipe: "Client video frame with name/title text."  
    effects: \["EFFECT-TXT-01"\]

  COMMUNITY-4-C-1:  
    name: "The 'Avatar Wall' Grid"  
    type: "COMMUNITY"  
    cls: 3  
    elements: \["C-Roll"\]  
    visual\_recipe: "Grid of user avatars filling the screen."  
    effects: \["EFFECT-TXT-03", "SFX\_Pop"\]

  \# \--- PAUSE SCENES \---  
  PAUSE-1-B-1:  
    name: "The Meditative B-Roll"  
    type: "PAUSE"  
    cls: 1  
    elements: \["B-Roll"\]  
    visual\_recipe: "Beautiful slow-motion nature shot, no VO."  
    effects: \["Slow Motion", "EFFECT-C-02"\]

  PAUSE-2-C-1:  
    name: "The Fading Word"  
    type: "PAUSE"  
    cls: 1  
    elements: \["C-Roll"\]  
    visual\_recipe: "Single word fades in/out on black."  
    effects: \["EFFECT-TXT-01"\]

  PAUSE-3-B-1:  
    name: "The 'Empty Room' Metaphor"  
    type: "PAUSE"  
    cls: 1  
    elements: \["B-Roll"\]  
    visual\_recipe: "Static shot of empty space."  
    effects: \["EFFECT-M-08"\]

  PAUSE-4-A-1:  
    name: "The Lingering Look"  
    type: "PAUSE"  
    cls: 1  
    elements: \["A-Roll"\]  
    visual\_recipe: "Coach holds eye contact in silence."  
    effects: \["EFFECT-M-01"\]

  \# \--- VIBE SCENES \---  
  VIBE-1-B-Montage-4-6:  
    name: "The Rhythmic Abstraction"  
    type: "VIBE"  
    cls: 4  
    elements: \["B-Roll Montage"\]  
    visual\_recipe: "Rapid abstract clips cut to beat."  
    effects: \["EFFECT-TR-01", "EFFECT-D-02"\]

  VIBE-2-B-1:  
    name: "The Meditative Haze"  
    type: "VIBE"  
    cls: 2  
    elements: \["B-Roll"\]  
    visual\_recipe: "Slow, blurry, atmospheric shot."  
    effects: \["EFFECT-M-12", "EFFECT-L-01"\]

  VIBE-3-C-1:  
    name: "The 'Hero Pose' Still"  
    type: "VIBE"  
    cls: 3  
    elements: \["C-Roll"\]  
    visual\_recipe: "Parallax layered still of coach in power pose."  
    effects: \["EFFECT-M-16", "EFFECT-C-17"\]

  VIBE-4-B-1:  
    name: "The One-Color World"  
    type: "VIBE"  
    cls: 4  
    elements: \["B-Roll"\]  
    visual\_recipe: "Desaturated shot with one color isolated."  
    effects: \["EFFECT-C-06", "EFFECT-T-01"\]

  \# \--- VISION SCENES \---  
  VISION-1-B-Montage-3-4:  
    name: "The 'Dream State' Montage"  
    type: "VISION"  
    cls: 4  
    elements: \["B-Roll Montage"\]  
    visual\_recipe: "Idealized future clips with smooth transitions."  
    effects: \["EFFECT-M-02", "EFFECT-TR-05", "EFFECT-L-04"\]

  VISION-2-C-1:  
    name: "The Future Self 'Mirror'"  
    type: "VISION"  
    cls: 3  
    elements: \["C-Roll"\]  
    visual\_recipe: "Stylized portrait of successful future self."  
    effects: \["EFFECT-M-16", "EFFECT-C-12"\]

  VISION-3-C-1:  
    name: "The 'Promise' Text Reveal"  
    type: "VISION"  
    cls: 5  
    elements: \["C-Roll"\]  
    visual\_recipe: "Complex flowchart or path animating on."  
    effects: \["EFFECT-G-15", "EFFECT-C-10"\]

  VISION-4-B-1:  
    name: "The 'First Person POV' Experience"  
    type: "VISION"  
    cls: 4  
    elements: \["B-Roll"\]  
    visual\_recipe: "POV shot of living the dream."  
    effects: \["EFFECT-M-14", "EFFECT-L-04"\]

---

## Research-Backed Intelligence Overlay (2026)

The library above remains the canonical scene ID registry. The rules below upgrade scene selection from intuitive pattern matching into research-backed editorial intelligence grounded in LC4MP, Mayer's multimedia principles, neurocinematics, eye-tracking continuity research, peak-end theory, crossmodal congruence, color PAD mapping, camera-motion research, and Kuleshov-style contextual framing.

### Core Interpretation Rules

- `cls` remains the baseline structural load score for the template, not the final scene load.
- Final scene load must be computed from `base_cls + arousal_modifier + information_density_modifier + text_competition_modifier` and then clamped to `1-5`.
- High-arousal content lowers the pacing tolerance of the viewer. If the narrative beat is emotionally intense, prefer one lower structural complexity band than the raw template would normally allow.
- No scene should present more than `3` primary visual elements at the same time unless the scene type is explicitly `EVIDENCE`, `DEMONSTRATION`, or `FRAME_CONTRAST`.
- Non-redundant on-screen text is expensive. Use it only when the scene's job is explanation, proof, or contrast. In emotional or story-forward scenes, captions should signal, not restate everything.
- Audio-visual incongruence is a short-duration attention interrupt, not a default style. Use it briefly in hooks, teases, or pivot moments, then resolve back to congruence.
- Kuleshov logic is preferred whenever a neutral or semi-neutral reaction shot can inherit meaning from adjacent context.
- Turning-point and end-state scenes carry disproportionate memory weight and should receive the highest asset quality, strongest continuity control, and cleanest audio-visual alignment.

### Scene Metadata Contract

```yaml
scene_research_contract:
  base_cls: 1-5
  target_attention_mode:
    - orienting
    - guided_focus
    - schema_building
    - emotional_peak
    - reflective_release
  isc_priority:
    - low
    - medium
    - high
  memory_role:
    - hook_imprint
    - context_encoding
    - tension_storage
    - peak_snapshot
    - end_snapshot
    - transfer_prompt
  av_congruence_mode:
    - strict
    - relaxed
    - strategic_mismatch
  continuity_requirement:
    - invisible_cut
    - match_action
    - eyeline_match
    - kuleshov_bridge
    - intentional_disruption
  text_policy:
    - none
    - keyword_only
    - guided_labels
    - explanatory
  recommended_duration_seconds: min-max
  max_primary_visual_units: 1-3
  peak_end_weight:
    - low
    - medium
    - high
```

### Phase Intelligence Matrix

```yaml
scene_type_intelligence:
  HOOK:
    target_attention_mode: orienting
    isc_priority: high
    memory_role: hook_imprint
    av_congruence_mode: strict
    text_policy: keyword_only
    recommended_duration_seconds: 0.8-2.5
    max_primary_visual_units: 2
    rule: "Deliver a legible first impression inside the first 400ms with one face, one conflict image, or one dominant contradiction."

  SETUP:
    target_attention_mode: guided_focus
    isc_priority: medium
    memory_role: context_encoding
    av_congruence_mode: strict
    text_policy: none
    recommended_duration_seconds: 1.5-4.0
    max_primary_visual_units: 2
    rule: "Reduce extraneous load and establish one emotional frame, prop, place, or vulnerability signal."

  CHALLENGE:
    target_attention_mode: guided_focus
    isc_priority: high
    memory_role: tension_storage
    av_congruence_mode: strict
    text_policy: keyword_only
    recommended_duration_seconds: 1.0-3.0
    max_primary_visual_units: 3
    rule: "Escalate load through motion and cut frequency, but insert continuity anchors so tension stays intelligible."

  TURNING_POINT:
    target_attention_mode: emotional_peak
    isc_priority: high
    memory_role: peak_snapshot
    av_congruence_mode: strict
    text_policy: none
    recommended_duration_seconds: 1.2-3.5
    max_primary_visual_units: 2
    peak_end_weight: high
    rule: "This is the primary remembered moment. Use the cleanest face/action/emotion alignment and avoid decorative overload."

  RESOLUTION:
    target_attention_mode: reflective_release
    isc_priority: medium
    memory_role: end_snapshot
    av_congruence_mode: strict
    text_policy: keyword_only
    recommended_duration_seconds: 1.5-4.0
    max_primary_visual_units: 2
    peak_end_weight: high
    rule: "Decrease structural load so the viewer can consolidate the emotional shift."

  ENCOURAGING_CHANGE:
    target_attention_mode: schema_building
    isc_priority: medium
    memory_role: transfer_prompt
    av_congruence_mode: strict
    text_policy: guided_labels
    recommended_duration_seconds: 1.5-5.0
    max_primary_visual_units: 3
    rule: "Pair call-to-action clarity with low-to-moderate load so intention survives the post-video scroll."

  FRAME_CONTRAST:
    target_attention_mode: schema_building
    isc_priority: medium
    memory_role: context_encoding
    av_congruence_mode: relaxed
    text_policy: explanatory
    recommended_duration_seconds: 1.5-4.0
    max_primary_visual_units: 3
    rule: "Contrast is allowed to be denser, but only when labels and layout make the comparison instantly parsable."

  THE_TEASE:
    target_attention_mode: orienting
    isc_priority: high
    memory_role: hook_imprint
    av_congruence_mode: strategic_mismatch
    text_policy: keyword_only
    recommended_duration_seconds: 0.8-2.0
    max_primary_visual_units: 2
    rule: "Create a curiosity gap, not confusion. Mismatch must resolve within one downstream beat."

  EVIDENCE:
    target_attention_mode: schema_building
    isc_priority: medium
    memory_role: context_encoding
    av_congruence_mode: strict
    text_policy: explanatory
    recommended_duration_seconds: 1.5-4.5
    max_primary_visual_units: 3
    rule: "Use signaling, spatial contiguity, and temporal contiguity. Never let charts compete with dense captions and aggressive motion."

  PAUSE:
    target_attention_mode: reflective_release
    isc_priority: low
    memory_role: end_snapshot
    av_congruence_mode: strict
    text_policy: none
    recommended_duration_seconds: 0.8-2.5
    max_primary_visual_units: 1
    rule: "Insert after CLS 4-5 bursts to protect storage and retrieval."

  VISION:
    target_attention_mode: emotional_peak
    isc_priority: high
    memory_role: end_snapshot
    av_congruence_mode: strict
    text_policy: guided_labels
    recommended_duration_seconds: 1.5-4.0
    max_primary_visual_units: 2
    peak_end_weight: high
    rule: "End-state imagery should feel fluent, aspirational, and crossmodally aligned so the final memory remains coherent."
```

### Research Rules For Scene Selection

```yaml
scene_selection_rules:
  lc4mp:
    - "Treat cuts, major text changes, and sound hits as resource calls on the encoding system."
    - "When arousal is high, reduce simultaneous novelty."
    - "If a template already contains rapid cuts, avoid adding non-redundant text unless the beat is proof-oriented."

  mayer_ctml:
    - "Prefer keyword callouts over full transcript text."
    - "Use signaling for evidence and demonstration scenes."
    - "Keep narration and the visual referent temporally aligned inside the same beat."
    - "Do not add decorative b-roll that does not serve the current line of meaning."

  neurocinematics:
    - "Use faces, biological motion, and clear action vectors as ISC anchors."
    - "Reserve the highest synchrony scenes for HOOK, TURNING_POINT, and VISION."
    - "Fast-cut sequences require a stable attentional magnet in-frame."

  eye_tracking_continuity:
    - "Preserve gaze landing zones across cuts."
    - "For talking-head scenes, keep eyes in the upper-central region of the vertical frame."
    - "If captions are required, place them below the speaker's eyes and above platform UI."

  peak_end:
    - "Allocate the best footage and cleanest design to TURNING_POINT and VISION/RESOLUTION."
    - "Middle scenes can stay simpler if they make the peak and the end more legible."

  kuleshov:
    - "Sequence reaction-context-reaction or context-reaction chains when emotion can be inferred rather than stated."
    - "Neutral b-roll is acceptable if the surrounding context carries strong emotional valence."

  audiovisual_congruence:
    - "Mood, motion rhythm, and color temperature should agree by default."
    - "If using mismatch, treat it as a brief expectancy violation followed by fast semantic resolution."
```

### Scene Family Overrides

```yaml
scene_family_overrides:
  A_ROLL_HEAVY:
    preferred_shot_scale: medium_close_up
    reason: "Optimizes eye-mouth reading, social presence, and emotional legibility."

  MONTAGE_HEAVY:
    requirement: "Every 2-3 shots must preserve one continuity anchor: motion vector, palette, prop, or sound bed."

  FOUND_CLIP_JUXTAPOSITION:
    requirement: "Use universal archetypes and strong valence transfer. Do not rely on niche cultural references when global legibility matters."

  SCREEN_RECORDING_DEMO:
    requirement: "Use signaling over spectacle. Motion exists to guide gaze, not to decorate the interface."

  SYMBOLIC_ECHO:
    requirement: "Reuse a prior motif, prop, environment, or gesture so the viewer experiences retrieval, not just novelty."
```

### Assembly Guidance

- A run of `CLS 4-5` scenes must be followed by either a `CLS 1-2` pause, resolution, or clarifying beat.
- `HOOK`, `TURNING_POINT`, and `VISION` scenes should be treated as premium memory anchors during asset ranking.
- Use `FRAME_CONTRAST`, `EVIDENCE`, and `DEMONSTRATION` scenes for explicit cognition. Use `SETUP`, `TURNING_POINT`, `RESOLUTION`, and `SYMBOLIC_ECHO` for affective cognition.
- Prefer one dominant scene job per beat: orient, explain, escalate, peak, release, or transfer. Scenes that try to do all of them at once usually become cognitively noisy.

