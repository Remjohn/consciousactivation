---
tech_spec_id: "TS-CMF-087"
title: "Micro-Semiotic Anchor Selection and Risk Gate"
story_id: "7.17"
story_title: "Micro-Semiotic Anchor Runtime"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "TS-CMF-080 functional decomposition"
pipeline_stage: "10"
entry_object: "ContextPremise, AudienceRealityBrief, BrandContextVersion, CompositionTemplateFamily"
exit_object: "MicroSemioticAnchorSelectionReceipt"
validation_contract: "recognition, subtlety, brand fit, comment potential, legal risk, stereotype risk"
required_receipt: "MicroSemioticAnchorSelectionReceipt"
runtime_target: "Python / Pydantic v2 / eval service / Operator review"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-087: Micro-Semiotic Anchor Selection and Risk Gate

## 1. Purpose

Select and validate small audience-recognition cues that make the viewer feel the content was made for people like them.

Micro-semiotic anchors are not decoration. They are audience recognition instruments that must remain subtle, lawful, non-stereotyping, and brand-aligned.

## 2. Selection Inputs

- Audience Reality Brief;
- Context Premise;
- target platform;
- brand audience;
- cultural context;
- content archetype;
- route feel contract;
- available approved anchor library;
- legal and trademark notes.

## 3. Primary Contract

```python
class MicroSemioticAnchorSelection(BaseModel):
    schema_version: Literal["cmf.micro_semiotic_anchor_selection.v1"]
    selection_id: UUID
    composition_runtime_binding_id: UUID
    selected_anchor_ids: list[UUID]
    no_anchor_rationale: str | None
    recognition_score: float
    subtlety_score: float
    brand_fit_score: float
    comment_potential_score: float
    distraction_risk_score: float
    legal_risk_score: float
    stereotype_risk_score: float
    placement_notes: list[str]
    blocker_codes: list[str]
```

## 4. Selection Rules

- High-identification compositions should include 1-3 approved anchors.
- An anchor must not become the main subject unless explicitly routed as the story object.
- Legal/trademark risk must be managed through inspired cues, not protected marks, unless licensed.
- The anchor must be specific enough to be recognized.
- The anchor must not stereotype or reduce the audience.

## 5. Commands and Receipts

| Type | Names |
|---|---|
| Commands | `SelectMicroSemioticAnchorsCommand`, `EvaluateMicroSemioticAnchorRiskCommand`, `RecordMicroSemioticAnchorSelectionCommand` |
| Events | `MicroSemioticAnchorsSelected`, `MicroSemioticAnchorSelectionBlocked` |
| Receipt | `MicroSemioticAnchorSelectionReceipt` |

## 6. Blockers

| Blocker | Trigger |
|---|---|
| `MICRO_ANCHOR_NOT_APPROVED` | Selected anchor is not approved. |
| `MICRO_ANCHOR_TOO_GENERIC` | Recognition score too low. |
| `MICRO_ANCHOR_TOO_DOMINANT` | Anchor steals attention. |
| `MICRO_ANCHOR_STEREOTYPE_RISK` | Anchor reduces or stereotypes audience. |
| `MICRO_ANCHOR_LEGAL_RISK` | Trademark/legal risk exceeds threshold. |
| `MICRO_ANCHOR_BRAND_MISMATCH` | Anchor contradicts brand context. |

## 7. Acceptance Criteria

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Anchor selection emits risk and fit scores. | Anchor added as prompt adjective only. |
| AC2 | High-identification templates require anchors or no-anchor rationale. | Paper-Cut audience piece has no local recognition cue or explanation. |
| AC3 | Stereotype/legal risks block approval. | Exact protected logo used without license. |
| AC4 | Placement is specified. | Anchor appears randomly in final frame. |

## 8. Testing

- Recognition/subtlety score tests.
- Legal risk negative fixtures.
- Stereotype risk fixtures.
- No-anchor rationale tests.
- Operator review card tests.

