# CCP 2D Character Animation Engine — Master Specification

## 1. Product thesis

The 2D Character Animation Engine transforms approved personal-brand characters into reusable digital actors whose performances are compiled from interview-derived meaning.

The engine is not a generic avatar generator. It is a controlled character-performance subsystem inside an interview-first platform.

```text
Human expression
→ structured interview context
→ semantic performance intent
→ approved character system
→ deterministic animation program
→ rendered asset
→ evaluation and approval
```

The system must preserve four kinds of continuity:

1. **Identity continuity** — the character still represents the same person.
2. **Performance continuity** — emotion, gesture, gaze, energy, and timing match the source expression.
3. **Brand continuity** — visual DNA, materials, props, costume, doctrine, and Micro-Semiotic Anchoring remain coherent.
4. **Production continuity** — the same pinned program and runtime produce the same result.

---

## 2. Two-lifecycle model

### 2.1 Character Genesis

Character Genesis creates reusable, versioned character infrastructure:

```text
Identity references
→ rig-aware master art
→ decomposition
→ layered PSD normalization
→ rigging
→ mesh and constraints
→ face / mouth / hand / prop libraries
→ 64-state acting map
→ material and costume skins
→ validation
→ CharacterRigVersion lock
```

This lifecycle is generative and artistic, but heavily reviewed.

### 2.2 Performance Compilation

Performance Compilation runs for each derived video asset:

```text
Brand Context + Interview Contract + Transcript Beat Map
→ performance intent
→ acting-state retrieval
→ gesture / gaze / face / viseme plan
→ scene choreography
→ TwoDCharacterProgram
→ deterministic render
```

This lifecycle is schema-driven and reproducible.

---

## 3. Canonical immutable objects

### 3.1 CharacterIdentityPack

Contains:

- approved source images;
- approved physical identity description;
- non-negotiable likeness traits;
- age and body-proportion constraints;
- allowed stylizations;
- consent and usage scope;
- forbidden representations;
- reference hashes;
- approved 64-state acting reference library.

### 3.2 CharacterArtVersion

One approved rig-aware character design, including:

- master character art;
- expression sheet;
- eye-direction sheet;
- mouth-shape sheet;
- hand-gesture sheet;
- costume sheet;
- prop sheet;
- material definitions;
- source-generation provenance.

### 3.3 LayeredCharacterAssetVersion

Normalized layered assets:

- PSD;
- semantic layer graph;
- inpainted hidden regions;
- masks;
- depth estimate;
- drawing order;
- alpha-edge quality report;
- repair history.

### 3.4 CharacterRigVersion

Contains:

- setup pose;
- bones;
- pivots;
- slots;
- attachments;
- meshes;
- vertex weights;
- masks and clipping;
- shape keys;
- IK and transform constraints;
- attachment points;
- draw-order rules;
- material bindings;
- runtime export bundle.

### 3.5 PerformanceLibraryVersion

Contains reusable performance primitives:

- base idles;
- posture states;
- major gestures;
- facial poses;
- gaze policies;
- mouth/viseme mapping;
- hand attachment variants;
- prop actions;
- state transition graph;
- 64 semantic acting states;
- energy and amplitude profiles.

### 3.6 TwoDCharacterProgram

A per-asset immutable program describing:

- all pinned upstream context;
- exact character and runtime versions;
- canonical timebase;
- transcript alignment;
- performance tracks;
- Motion Canvas choreography;
- Remotion composition;
- FFmpeg finishing;
- evaluation thresholds;
- operator approval;
- final provenance.

---

## 4. Structured inputs

The performance compiler must receive explicit identifiers and typed summaries for:

### Brand context

- Voice DNA version;
- Visual DNA version;
- Negative Space constraints;
- doctrine bundle;
- identity pack;
- approved character versions;
- approved material profiles;
- approved costumes;
- approved props;
- Micro-Semiotic Anchor library;
- subtitle and typography profiles;
- motion-intensity preferences.

### Interview intelligence

- Interview Brief;
- Audience Reality Brief;
- Context Premises;
- Matrix of Edging brief;
- Interview Asset Contract;
- target archetype;
- target expression states;
- primitive targets;
- prohibited emotional treatments.

### Captured expression

- source audio/video hashes;
- transcript;
- word timings;
- phoneme timings;
- Transcript Beat Map;
- Expression Moments;
- pause map;
- emphasis-word map;
- emotional curve;
- source-fidelity requirements.

### Asset intent

- Asset Package Spec;
- content format;
- scene template;
- aspect ratio;
- duration constraints;
- platform safe zone;
- required props or diagrams;
- desired performance density;
- evaluation rubric.

---

## 5. Character design doctrine

### 5.1 Rig-aware design

The master character should be designed for animation rather than decomposed from an arbitrary final illustration.

Required qualities:

- arms visually separated from torso;
- shoulders and elbows readable;
- visible wrist transitions;
- head and neck overlap sufficient for rotation;
- neutral open eyes;
- neutral mouth;
- clothing layers designed with overlap regions;
- hands not fused to props;
- hair separated into front, side, and back masses;
- symmetrical canvas and stable root position;
- lighting and paper texture consistent across attachment variants.

### 5.2 PaperCut visual doctrine

PaperCut materiality should exhibit:

- tactile fiber texture;
- slight edge irregularity;
- shallow but visible layer thickness;
- restrained drop shadows;
- limited and meaningful deformation;
- stepped stop-motion variation;
- visible layer overlap;
- intentionally imperfect placement.

The character must never feel like smooth rubber or generic vector art.

### 5.3 Personal-brand likeness

The stylization may simplify, but must preserve:

- facial silhouette;
- skin tone;
- hairline and hair mass;
- eyebrow character;
- eye spacing;
- nose and mouth relationship;
- age signals;
- characteristic expression;
- body proportions approved for the brand.

---

## 6. Layer decomposition doctrine

The primary anime/illustration route is based on See-Through-style decomposition:

```text
single source illustration
→ semantic body parsing
→ transparent layer generation
→ depth estimation
→ hidden-region inpainting
→ inferred drawing order
→ layered PSD
```

The production pipeline must treat automatic output as a candidate, not an approved rig asset.

### Canonical layer tags

```text
back_hair
rear_accessory
rear_upper_arm_L / R
rear_forearm_L / R
rear_hand_L / R
rear_leg_L / R
torso
neck
head
ear_L / R
face_base
eye_white_L / R
iris_L / R
pupil_L / R
brow_L / R
nose
mouth_base
front_hair
front_upper_arm_L / R
front_forearm_L / R
front_hand_L / R
topwear
bottomwear
footwear
foreground_accessory
```

### Decomposition pass criteria

- semantically correct labels;
- left/right correctness;
- inpainted overlap behind occluders;
- no white halos;
- no fused body parts;
- no accidental duplicate edges;
- stable paper texture;
- valid drawing order;
- deformation margin around joints.

Realistic-photo or mixed-media characters should route through Qwen-Image-Layered, SAM3, and targeted GPT Image/Flux repair instead of assuming anime-oriented decomposition will generalize.

---

## 7. Rigging doctrine

### 7.1 Standard bone hierarchy

```text
root
└── body_root
    ├── pelvis
    ├── torso
    │   ├── chest
    │   │   ├── neck
    │   │   │   └── head
    │   │   ├── shoulder_L → upper_arm_L → forearm_L → hand_L
    │   │   └── shoulder_R → upper_arm_R → forearm_R → hand_R
    │   └── prop_anchor_chest
    ├── hip_L → thigh_L → shin_L → foot_L
    └── hip_R → thigh_R → shin_R → foot_R
```

### 7.2 Pivots

Pivots are approved rig data. Runtime inference is forbidden.

Each pivot stores:

- local normalized position;
- parent bone;
- preferred bend direction;
- rotation limits;
- mesh influence radius;
- overlap and mask policy.

### 7.3 Meshes

Use the simplest representation compatible with the required movement:

- rigid attachments for eyes, buttons, earrings, fixed hands, shoes, and props;
- weighted meshes for limbs;
- low-density warp meshes for torso and hair;
- moderate face mesh for head turns and expression blending;
- direct attachment swaps for dramatically different hand and mouth shapes.

### 7.4 Constraints

Use explicit constraints for:

- pointing to a diagram;
- holding signs or cards;
- hand-on-hip poses;
- feet planting;
- eye targeting;
- two-hand prop holding.

### 7.5 Shape keys

Shape keys store deltas from rest mesh and are composable where validated.

Required categories:

- brows;
- eyelids;
- eye smile;
- cheeks;
- mouth form;
- mouth open;
- sleeves at bend extremes;
- torso breathing;
- face yaw/pitch correction;
- paper fold and squash accents.

---

## 8. Performance architecture

### 8.1 Orthogonal track model

```text
Track 0: base body / idle
Track 1: major gesture
Track 2: head and gaze
Track 3: facial emotion
Track 4: mouth / visemes
Track 5: hands and prop events
Track 6: secondary motion / paper texture
Track 7: operator corrective override
```

Tracks must only affect properties they own unless an explicit override is declared.

### 8.2 Acting state model

The 64-state library is semantic:

```text
8 emotion families × 8 gesture/body-language families
```

Each state composes:

- base posture;
- gesture clip;
- facial pose;
- gaze policy;
- hand attachments;
- energy profile;
- allowed primitive affinities;
- forbidden doctrine contexts;
- transition policy.

### 8.3 Performance density

The compiler should prefer stillness.

Default limits:

- at most one major gesture per clause;
- no more than two major gesture peaks in five seconds unless format requires high energy;
- gaze shift only for semantic reason;
- emotional pose held across coherent beats;
- pause regions favor stillness and micro-breathing.

---

## 9. Canonical timebase

All production timing uses integer ticks.

```json
{
  "ticks_per_second": 48000,
  "audio_sample_rate": 48000,
  "fps_numerator": 30,
  "fps_denominator": 1
}
```

Words, phonemes, beat boundaries, pauses, gestures, transitions, subtitles, and sound effects reference ticks.

Frame conversion:

```text
frame = round(tick × fps_num / (ticks_per_second × fps_den))
```

This is the only valid conversion path.

---

## 10. Transcript-to-performance compiler

For each Transcript Beat:

1. read beat type and primitive targets;
2. read emotional curve and Voice DNA energy;
3. retrieve candidate acting states;
4. reject doctrine-incompatible states;
5. select base posture and face state;
6. select no more than one dominant gesture per clause;
7. align gesture stroke to emphasized word;
8. choose gaze target from semantic context;
9. create lip-sync cues;
10. attach props or Micro-Semiotic Anchors only when semantically justified;
11. generate transition cues;
12. evaluate the resulting performance plan;
13. freeze approved cues into `TwoDCharacterProgram`.

Gesture envelope defaults:

```text
Preparation: 120–300 ms before emphasis
Stroke: at emphasized word
Hold: 150–500 ms
Recovery: 250–700 ms
```

---

## 11. Runtime and composition

### Character runtime

A provider abstraction must support at least:

- Spine-compatible runtime bundle;
- native Stretchy-derived runtime or future custom WebGL runtime.

### Motion Canvas

Motion Canvas owns scene choreography:

- character path;
- camera path;
- diagram and prop movement;
- teaching object placement;
- procedural arrows and labels;
- scene-level timing.

### Remotion

Remotion owns final platform composition:

- aspect ratio;
- scene sequencing;
- subtitles;
- branded panels;
- backgrounds;
- overlays;
- safe zones;
- sound-event placement;
- final video render.

### FFmpeg

FFmpeg owns technical finishing:

- muxing;
- codec normalization;
- loudness normalization;
- ducking;
- derivative exports;
- final master checks.

---

## 12. Deterministic boundary

Generative systems may create candidates for:

- master character art;
- expression and gesture sheets;
- decomposition;
- inpainting;
- props and costumes;
- initial performance suggestions.

Before production they must become approved, hashed assets.

Final rendering must not call:

- LLMs;
- image models;
- decomposition models;
- external generation APIs;
- non-pinned package versions.

---

## 13. Evaluation and approval

The engine uses three preview layers:

1. Rig Debug Preview;
2. Performance Blocking Preview;
3. Final Composition Preview.

Each stage has typed evaluation results and typed repair commands.

Final publication requires:

- automatic gates passed;
- operator approval;
- frozen program hash;
- immutable render receipt.
