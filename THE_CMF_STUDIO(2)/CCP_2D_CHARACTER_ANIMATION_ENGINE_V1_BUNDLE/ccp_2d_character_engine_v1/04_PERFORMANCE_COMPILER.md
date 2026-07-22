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
