---
tech_spec_id: "TS-CMF-085"
title: "64-State Acting and Avatar Performance Selector"
story_id: "7.15"
story_title: "Acting and Avatar Performance Selector"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "TS-CMF-080 functional decomposition"
pipeline_stage: "10"
entry_object: "ResolvedBrandGenesisSubstrate and CompositionBeatMap"
exit_object: "PerformanceStateSelectionManifest"
validation_contract: "emotion, gesture, expression state, layout bias, route fit"
required_receipt: "PerformanceStateSelectionReceipt"
runtime_target: "Python / Pydantic v2 / object storage / renderer prop compiler"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-085: 64-State Acting and Avatar Performance Selector

## 1. Purpose

Select the correct human acting reference or avatar state for each composition beat. The 64-state acting library is an emotional-performance primitive system, not a pose bucket.

## 2. Selection Inputs

- expression state;
- source emotion from Expression Moment;
- route purpose;
- beat semantic function;
- guest/interviewer role;
- required gesture family;
- layout zone;
- platform crop;
- available acting references or avatar states;
- consent and likeness rules.

## 3. Primary Contracts

```python
class PerformanceStateSelection(BaseModel):
    schema_version: Literal["cmf.performance_state_selection.v1"]
    selection_id: UUID
    beat_id: UUID
    actor_role: Literal["guest", "interviewer", "avatar", "narrator"]
    selected_reference_id: UUID
    emotion_primary: str
    gesture_family: str
    body_language: str
    facial_expression: str
    energy_level: str
    framing: str
    orientation: str
    layout_bias: str
    source_fit_rationale: str
    consent_ref: str
    blocker_codes: list[str]
```

## 4. Selection Rules

- The selected state must support the beat emotion and route purpose.
- A reflective story beat cannot use celebratory uplift unless explicitly justified.
- A teaching step should prefer open explain, point, or invite gestures.
- Challenger beats may use authority, emphasis, or pointing, but must not degrade into aggression.
- Reaction clips must preserve authentic human proof when real footage exists.
- Avatar states must not replace source truth when actual guest expression is required.

## 5. Commands and Receipts

| Type | Names |
|---|---|
| Commands | `SelectPerformanceStateCommand`, `ValidatePerformanceStateFitCommand`, `RecordPerformanceStateSelectionCommand` |
| Events | `PerformanceStateSelected`, `PerformanceStateSelectionBlocked` |
| Receipt | `PerformanceStateSelectionReceipt` |

## 6. Blockers

| Blocker | Trigger |
|---|---|
| `ACTING_REFERENCE_NOT_APPROVED` | Reference is not approved/locked. |
| `EMOTION_ROUTE_MISMATCH` | Selected state contradicts expression state. |
| `GESTURE_BEAT_MISMATCH` | Gesture does not support beat function. |
| `CONSENT_SCOPE_MISSING` | Likeness use is not permitted. |
| `AVATAR_REPLACES_REQUIRED_REAL_PROOF` | Avatar used where real human proof is required. |

## 7. Acceptance Criteria

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Each beat using human/avatar layer has performance selection. | Avatar appears with no state metadata. |
| AC2 | Selection includes emotion, gesture, body language, framing, and layout bias. | Only stores `pose_3.png`. |
| AC3 | Consent and likeness scope are checked. | Meme uses exact likeness without permission. |
| AC4 | Route mismatch blocks render. | Playful state used in grief story without rationale. |

## 8. Testing

- 64-state matrix coverage tests.
- Route/gesture fit tests.
- Consent blocker tests.
- Real footage vs avatar substitution tests.
- Renderer prop handoff tests.

