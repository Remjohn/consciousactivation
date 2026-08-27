intelligence/frameworks/scene\_builder\_library.yaml

\# CONSCIOUS SCENE BUILDER LIBRARY (V3)  
\# Used by: Blueprint Architect, Virtual Director

scenes:  
  \# \--- HOOK SCENES (0-5s) \---  
  HOOK-1-AB-2:  
    name: "The Talking Head Pattern Match"  
    type: "HOOK"  
    cls: 2 \# Cognitive Load Score (1-5)  
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
