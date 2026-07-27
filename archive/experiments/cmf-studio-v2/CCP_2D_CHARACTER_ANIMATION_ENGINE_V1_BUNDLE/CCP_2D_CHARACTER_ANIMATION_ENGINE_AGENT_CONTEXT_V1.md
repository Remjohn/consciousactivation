# CCP 2D Character Animation Engine — Agent Start Here

## Purpose

This bundle is the canonical implementation context for a production-grade, JSON-driven 2D character animation engine inside CCP Studio / Conscious Media Factory.

The engine does **not** accept loose prompts as its primary input. It compiles a deterministic performance program from pinned, structured context:

- Brand Context Version;
- Interview Brief;
- Interview Asset Contract;
- Transcript Beat Map;
- Expression Moments;
- Voice DNA and Visual DNA;
- Primitive evaluations;
- Doctrines and Negative Space;
- Asset Package Specification;
- approved Character Identity Pack;
- approved 64-state Acting Library;
- approved Character Rig Version;
- scene template;
- format target.

The canonical runtime artifact is `TwoDCharacterProgram`. All renderers consume it. No provider is allowed to invent production behavior during final rendering.

## Binding architecture decisions

1. **Python is the semantic runtime.** Pydantic contracts, DSPy programs, Pi orchestration, evaluation, state machines, provider adapters, and receipts live in Python.
2. **TypeScript is a rendering consumer.** Motion Canvas, Remotion, and browser previews consume generated TypeScript types derived from Pydantic schemas.
3. **Character creation and performance compilation are separate lifecycles.** Character Genesis is occasional and approval-heavy; performance compilation happens per asset.
4. **Generative output must be promoted into an approved version before production.** No image model, decomposition model, or LLM runs inside the final deterministic render.
5. **Time is represented as integer ticks.** Floating-point seconds are never the source of truth.
6. **The operator is the final approval authority.** Automatic repair may propose or generate candidates, but publication requires an approved receipt.
7. **The character remains brand-owned and versioned.** Every output pins identity, art, layered asset, rig, performance library, materials, costume, props, and Micro-Semiotic Anchors.

## Recommended reading order

1. `01_MASTER_SPEC.md`
2. `02_PIPELINE_AND_PROVIDER_ROLES.md`
3. `03_RIGGING_AND_ASSET_CONTRACTS.md`
4. `04_PERFORMANCE_COMPILER.md`
5. `05_RENDERING_AND_REPRODUCIBILITY.md`
6. `06_EVALS_APPROVAL_AND_REPAIR.md`
7. `models/two_d_character_models.py`
8. `examples/example_two_d_character_program.json`

## Definition of done

The engine is production-ready only when it can:

- ingest an approved layered character package;
- compile a full `TwoDCharacterProgram` from structured interview context;
- render the same approved program reproducibly;
- preserve identity and materiality across scenes;
- synchronize mouth, gesture, gaze, props, subtitles, and audio to the canonical timebase;
- produce rig, blocking, and final previews;
- run automatic evaluations;
- accept typed operator repair commands;
- create an immutable final render receipt.

---

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

---

# Provider and Pipeline Responsibilities

## 1. Provider boundary rule

Every provider implements a narrow typed contract. No provider owns the full workflow.

```text
Python harness decides meaning and routing.
Providers execute bounded transformations.
The operator approves promoted assets.
Renderers consume frozen contracts.
```

## 2. See-Through provider

### Input

- approved rig-aware source illustration;
- character identity reference;
- target canonical part tags;
- desired output resolution;
- decomposition policy.

### Output

- layered PSD candidate;
- semantic masks;
- depth map;
- inferred drawing order;
- hidden-region inpainting;
- decomposition report;
- model/version receipt.

### Does not own

- final semantic approval;
- pivots;
- meshes;
- bones;
- animation;
- production release.

### Production caveat

Treat it as the default route only for supported illustration/anime-like characters. Real-photo or mixed-media personal-brand assets require alternate decomposition routing.

---

## 3. Qwen-Image-Layered provider

### Role

General-purpose semantic RGBA decomposition for flat generated scenes or mixed-media character art.

### Best uses

- photo-paper-cut character layers;
- props and costumes;
- complex generated poster scenes;
- recovery of reusable layers from composition plates.

### Output

- ordered RGBA layers;
- semantic grouping proposal;
- alpha-quality report.

### Follow-up

SAM3 refines precise masks; GPT Image/Flux repairs missing or contaminated regions.

---

## 4. SAM3 provider

### Role

Precise segmentation, alpha cleanup, object isolation, and tracking.

### Uses

- portrait cutout refinement;
- hand and prop isolation;
- layer-edge repair;
- background removal;
- mask generation for inpainting;
- tracked cutouts from source interview footage.

SAM3 is not a layered rig generator.

---

## 5. GPT Image / Flux provider

### Role

- rig-aware master-art generation;
- identity-preserving edits;
- hidden-region repair;
- costume and hand variants;
- paper texture harmonization;
- targeted correction after QC failure.

### Restriction

The provider output is always a candidate asset. It cannot be referenced by production programs until approved and versioned.

---

## 6. Stretchy Studio authoring adapter

### Role

- PSD import;
- hierarchy normalization;
- pivot editing;
- heuristic or DWPose-assisted rigging;
- mesh generation;
- limb weighting;
- shape-key authoring;
- direct vertex keyframes;
- audio-synced preview;
- runtime export.

### CCP integration

Create an importer/exporter that translates Stretchy project data into canonical Pydantic contracts.

The `.stretch` project remains an authoring artifact, not semantic source of truth.

---

## 7. Spine compiler/runtime provider

### Role

- bones;
- slots;
- skins;
- attachments;
- weighted meshes;
- animation tracks;
- deform timelines;
- clipping;
- IK constraints;
- layered playback.

### Important build rules

- pin editor/export/runtime versions;
- preserve local-space pivots;
- convert coordinate systems explicitly;
- bake unsupported warp deformations into deform timelines;
- review license requirements before distribution.

---

## 8. Motion Canvas choreography provider

### Input

Frozen `TwoDCharacterProgram` scene choreography section.

### Owns

- scene-level motion;
- camera movement;
- character placement;
- diagram timing;
- teaching object paths;
- procedural arrows and transitions.

### Does not own

- acting-state selection;
- transcript interpretation;
- brand doctrine;
- final approval.

---

## 9. Remotion compositor

### Input

- frozen program;
- character runtime bundle or RGBA plate;
- subtitles;
- scene assets;
- brand render profile.

### Owns

- final frame composition;
- deterministic typography;
- platform safe zones;
- scene sequencing;
- background and overlay layers;
- final render invocation.

### Randomness

All procedural jitter uses explicit seeds.

---

## 10. FFmpeg finishing provider

### Owns

- video/audio mux;
- codec and pixel format;
- loudness normalization;
- voice-priority music ducking;
- trim and padding;
- preview derivatives;
- final master verification.

### Does not own

- semantic timing;
- gestures;
- scene structure;
- subtitles;
- identity decisions.

---

# Rigging and Asset Contracts

## 1. PSD normalization

A valid production PSD must preserve full-canvas coordinates for every layer. Individual layers must not be destructively cropped unless the crop rectangle and canvas transform are recorded.

Each layer requires:

```json
{
  "layer_id": "forearm_L",
  "semantic_type": "forearm",
  "side": "left",
  "source_name": "left-arm-2",
  "draw_order": 42,
  "canvas_rect": [408, 612, 310, 492],
  "pivot_hint": [0.49, 0.11],
  "parent_hint": "upper_arm_L",
  "mask_ids": [],
  "material_id": "paper_skin_v1",
  "sha256": "..."
}
```

## 2. Layer graph

The layer graph stores:

- parent/child groups;
- sibling drawing order;
- semantic body part;
- source texture;
- masks;
- attachment role;
- material binding;
- visibility defaults;
- deformation margin.

Draw-order changes must be explicit timeline events.

## 3. Bone graph

Each bone stores:

- bone ID;
- parent ID;
- setup translation;
- setup rotation;
- scale and shear;
- pivot coordinates;
- rotation limits;
- bend preference;
- constraint memberships.

## 4. Mesh bundle

Large mesh data belongs in binary sidecars referenced by URI and hash.

For each mesh:

- rest vertices;
- UVs;
- triangle indices;
- bone indices;
- normalized weights;
- boundary contour;
- deformation safety bounds;
- associated attachment;
- material ID.

## 5. Masks and clipping

Masks must be explicit assets with stable IDs.

Use clipping for:

- irises inside eye whites;
- mouth interior;
- clothing overlap;
- hair behind face;
- props passing behind hands;
- paper edge reveal.

## 6. Shape-key bundle

Each shape key stores:

- target mesh;
- delta sidecar;
- legal range;
- compatible keys;
- exclusion group;
- approved extreme-frame previews.

## 7. Hand library

Recommended attachment variants:

```text
rest
open
point
pinch
fist
thumb_up
hold_card
hold_phone
hold_cup
hand_on_heart
thinking
```

Every variant must share wrist anchor, canvas, material, and lighting.

## 8. Mouth library

Recommended mouth attachments:

```text
REST
MBP
ETC
E
AI
O
U
FV
L
SMILE
FROWN
```

The engine may blend small shape-key changes on top of attachment swaps.

## 9. Gaze library

Semantic targets:

```text
camera
interviewer
memory_left
memory_right
teaching_object
quote_card
poll_A
poll_B
audience
down_reflective
```

Each gaze target defines iris position, optional head offset, blink policy, and return policy.

## 10. Costume and prop skins

Costumes and props are modular attachments, not duplicated rigs.

Examples:

```text
founder_black_tshirt
formal_green_blazer
paper_cut_blue_shirt
podcast_casual
fitness_outfit

tea_cup
paper_arrow
notebook
phone
microphone
sign_board
```

Micro-Semiotic Anchors are implemented as approved costume or prop variants.

## 11. Warp deformation export

If the target runtime lacks a native warp-deformer concept:

1. sample the source parameter range;
2. evaluate the deformed lattice;
3. apply the deformation to rest vertices;
4. calculate per-vertex deltas;
5. emit deform keyframes;
6. validate golden frames against the authoring preview.

## 12. Rig release gate

A CharacterRigVersion may be locked only after:

- semantic layer QC;
- hidden-region QC;
- pivot QC;
- mesh inversion test;
- extreme-pose test;
- hand/prop attachment test;
- face and eye clipping test;
- mouth library test;
- costume-switch test;
- deterministic export test;
- operator approval.

---

# Performance Compiler Specification

## 1. Purpose

The performance compiler translates meaning into bounded character behavior.

It does not invent content. It interprets structured interview context and chooses from approved performance resources.

## 2. DSPy program stages

Recommended modules:

```text
BeatMeaningAnalyzer
EmotionCurveCompiler
PrimitivePerformanceMapper
ActingStateRetriever
GesturePlanner
GazePlanner
FacialPosePlanner
VisemePlanner
PropAndAnchorPlanner
TransitionPlanner
PerformanceEvaluator
TwoDCharacterProgramAssembler
```

Every module emits typed Pydantic output.

## 3. Candidate retrieval

Acting states are retrieved by:

- communicative intent;
- primary and secondary emotion;
- body-language family;
- gesture family;
- energy;
- content format;
- primitive affinity;
- doctrine compatibility;
- recent-use penalty;
- transition compatibility.

Example scoring:

```text
0.25 communicative intent
0.20 emotion
0.15 gesture family
0.10 body language
0.10 primitive affinity
0.08 energy
0.05 scene compatibility
0.04 transition compatibility
0.03 recent-use diversity
```

Any doctrine hard fail removes the candidate regardless of score.

## 4. Beat-to-state mapping

Common beat mappings:

| Beat type | Preferred body language |
|---|---|
| memory scene | restrained, off-camera gaze, low gesture density |
| confession | closed-to-open posture, low amplitude |
| meaning reveal | stillness before one clear emphasis gesture |
| teaching | open torso, diagram-oriented gaze, measured hands |
| challenge | direct camera gaze, grounded point, limited aggression |
| invitation | warm open palms, camera gaze, relaxed shoulders |
| humor | timing hold, face-led reaction, minimal body excess |
| warning | stable posture, controlled seriousness |

## 5. Gesture planner

Each major gesture is represented as:

```json
{
  "gesture_id": "open_hand_emphasis_R",
  "semantic_target": "discipline",
  "prepare_start_tick": 317000,
  "stroke_tick": 342000,
  "hold_end_tick": 370000,
  "recover_end_tick": 405000,
  "amplitude": 0.58,
  "hand_pose": "open",
  "gaze_target": "camera"
}
```

## 6. Gaze planner

Gaze selection should account for:

- who is being addressed;
- whether the beat is remembered or taught;
- whether an object is on screen;
- eye-line consistency;
- emotional avoidance or openness;
- current head orientation.

## 7. Facial pose planner

Facial emotion must change less frequently than subtitles.

A facial state may span several transcript beats when they belong to one emotional unit.

## 8. Viseme planner

Pipeline:

```text
source audio
→ word alignment
→ phoneme alignment
→ phoneme-to-viseme mapping
→ confidence flags
→ smoothing and amplitude shaping
→ final viseme cues
```

Viseme cues cannot move beat boundaries or alter the source audio.

## 9. Prop and Micro-Semiotic Anchor planner

A prop is selected only when it:

- supports the spoken concept;
- is part of the approved library;
- does not distract from the face;
- fits brand context;
- passes legal and stereotype checks;
- has a valid attachment action.

## 10. Transition graph

The acting-state library should define allowed transitions and mix durations.

Example:

```json
{
  "from": "reflective_thinking",
  "to": "calm_open_explain",
  "allowed": true,
  "min_mix_ticks": 9600,
  "max_mix_ticks": 24000,
  "bridge_clip": "breath_and_raise_head"
}
```

## 11. Performance auto-evaluation

Before rendering, evaluate:

- gesture density;
- gesture/emphasis alignment;
- gaze semantics;
- facial state compatibility;
- primitive expression;
- doctrine compliance;
- transition legality;
- state repetition;
- prop relevance;
- performance energy versus Voice DNA.

Only a passing plan is assembled into `TwoDCharacterProgram`.

---

# Rendering and Reproducibility

## 1. Render modes

### Embedded runtime

Character runtime is evaluated directly inside the Remotion render.

Best for:

- simple scenes;
- lower storage overhead;
- exact character/subtitle synchronization;
- reusable character positioning.

### Precomposed RGBA plate

Motion Canvas or the character runtime renders transparent frames or ProRes 4444 before final composition.

Best for:

- complex choreography;
- debugging isolation;
- reusable character plates;
- scenes where the character engine and final compositor must be decoupled.

## 2. Motion Canvas contract

Motion Canvas consumes only:

- approved choreography cues;
- camera cues;
- scene-object cues;
- character placement;
- deterministic easing and seeds.

It cannot select acting states or change transcript meaning.

## 3. Remotion contract

Remotion receives:

- exact duration in frames;
- exact FPS and resolution;
- character render mode;
- scene template;
- subtitles;
- background plates;
- overlays;
- safe-zone profile;
- audio references;
- deterministic seeds.

## 4. FFmpeg finishing

Recommended production sequence:

```text
render video-only master
render or collect voice/music/SFX stems
normalize voice
apply music ducking
mix stems
mux audio and video
verify duration and stream metadata
create preview derivatives
hash all outputs
```

## 5. Canonical reproducibility receipt

Pin:

- program JSON hash;
- every asset hash;
- every sidecar hash;
- character runtime version;
- Motion Canvas version;
- Remotion version;
- FFmpeg build;
- fonts;
- renderer container digests;
- locale and timezone;
- FPS rational;
- audio sample rate;
- random seeds;
- color profile;
- codec settings;
- final command lines.

## 6. Golden tests

Maintain fixtures for:

- neutral rig frame;
- extreme arm bends;
- eye clipping;
- each mouth shape;
- costume switch;
- prop attach/detach;
- warp-deform export;
- paper-material rendering;
- acting-state transitions;
- one end-to-end reference asset.

CI should render selected frames and compare perceptual hashes and structured state snapshots.

## 7. Network isolation

The production renderer should run with no outbound network access. All files must already exist in content-addressed storage or the local render package.

---

# Evaluations, Approval, and Repair

## 1. Character Genesis gates

### Identity

- likeness;
- age consistency;
- skin tone;
- hair and silhouette;
- body proportion;
- approved stylization;
- no unwanted beautification.

### Decomposition

- semantic labels;
- hidden-region completeness;
- alpha quality;
- layer fusion;
- draw order;
- material continuity.

### Rig

- pivots;
- joint bending;
- mesh inversion;
- mask leakage;
- eye clipping;
- mouth deformation;
- costume and prop compatibility;
- runtime export parity.

## 2. Per-program gates

### Source alignment

- beat map pinned;
- source words preserved;
- timing confidence;
- no unapproved synthetic speech;
- exact audio duration.

### Performance

- emotional match;
- gesture timing;
- gaze logic;
- mouth sync;
- transition legality;
- motion restraint;
- performance diversity.

### Primitive and doctrine compliance

- target primitives expressed;
- prohibited primitives absent;
- Negative Space respected;
- trauma safety respected;
- Micro-Semiotic Anchors subtle;
- character does not make unsupported claims.

### Technical

- no missing textures;
- no alpha bleed;
- no frame drift;
- no audio clipping;
- correct output size;
- reproducibility receipt complete.

## 3. Preview hierarchy

### Rig Debug Preview

Display bones, pivots, meshes, masks, weights, draw order, and attachment IDs.

### Performance Blocking Preview

Display a neutral background plus:

- transcript;
- beat name;
- acting state;
- gesture markers;
- gaze target;
- primitive target;
- viseme label.

### Final Composition Preview

Full scene, subtitles, audio, SFX, and platform framing.

## 4. Typed repair commands

Supported command families:

```text
MOVE_PIVOT
REPAIR_MASK
REORDER_LAYER
REPLACE_ATTACHMENT
REPLACE_HAND_POSE
CHANGE_ACTING_STATE
REDUCE_GESTURE_AMPLITUDE
SHIFT_GESTURE_STROKE
CHANGE_GAZE_TARGET
REMAP_VISEME
CHANGE_COSTUME_SKIN
ATTACH_PROP
DETACH_PROP
REMOVE_MICRO_SEMIOTIC_ANCHOR
REDUCE_PAPER_JITTER
CHANGE_MIX_DURATION
```

Each command creates a new version or revision. Approved versions are immutable.

## 5. Operator approval lifecycle

```text
draft
→ compiled
→ automatic_eval_failed | blocking_preview_ready
→ revision_requested | final_preview_ready
→ approved_for_render
→ rendering
→ rendered
→ final_qc
→ approved_for_publish
→ archived
```

## 6. Receipt chain

Every final output records:

- context IDs;
- character version IDs;
- program hash;
- repair history;
- evaluation results;
- operator ID and approval timestamp;
- runtime versions;
- asset hashes;
- final output hashes.
