---
tech_spec_id: "TS-CMF-118"
title: "Content Sequence Program Compiler and Composition Handoff"
story_id: "12.5"
story_title: "Content Sequence Program Compiler"
epic_id: 12
epic_title: "Conscious Sequencing and Expression Acquisition"
status: "ready-for-development"
created_at: "2026-06-25"
source_story: "CCP Conscious Sequencing and Expression Acquisition Engine V1 bundle"
pipeline_stage: "9 / 10 / 11"
entry_object: "Frozen ExpressionIngredientInventory, sequence hypotheses, route target, format target, Brand Context, doctrine bundle, primitive receipts"
exit_object: "ContentSequenceProgram, SequenceCompositionHandoff, sequence preview read model, frozen program receipt"
validation_contract: "ingredient binding, loop closure, viewer-state progression, format adapter compatibility, source grounding, primitive coalition, composition function handoff"
required_receipt: "ContentSequenceProgramFreezeReceipt"
runtime_target: "Python / Pydantic v2 / DSPy compiler / composition engines / Remotion / Motion Canvas / Skia / PWA review"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-118: Content Sequence Program Compiler and Composition Handoff

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory CMF/ERA3 spec protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Phase 4 CBAR mandates for composition/render meaning gates. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Phase 5 CBAR mandates for verifiable artifacts. |
| `THE CMF STUDIO/docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md` | Phase 4 adversarial audit trail. |
| `THE CMF STUDIO/docs/architecture/cbar_audits/CBAR_Audit_Phase5_Growth.md` | Phase 5 adversarial audit trail. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_12_Conscious_Sequencing_Expression_Acquisition.md` | Product owner for FR-CMF-12.05. |
| `THE CMF STUDIO/CCP_CONSCIOUS_SEQUENCING_AND_EXPRESSION_ACQUISITION_ENGINE_V1_BUNDLE/ccp_conscious_sequence_engine_v1/01_MASTER_SPEC.md` | Content Sequence Program, sequence patterns, format adapters, composition functions. |
| `.../02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Program state machine and invariants. |
| `.../03_RUNTIME_WORKFLOWS.md` | Sequence compilation and composition handoff workflow. |
| `.../04_REGISTRIES_AND_FORMAT_ADAPTERS.md` | Format adapter principle. |
| `.../05_EVALUATION_GOVERNANCE_AND_LEARNING.md` | Sequence gates and ethical hard gates. |
| `.../models/sequence_engine_models.py` | `SequenceLoop`, `ViewerJourney`, `SequenceBeat`, `ContentSequenceProgram`. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-078-four-video-format-runtime-and-doctrine-crosswalk.md` | Four canonical video format binding. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-080-composition-template-runtime-transcript-timing-and-brand-genesis-binding.md` | Composition runtime, transcript timing, brand genesis binding. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-096-carousel-slide-composition-library-and-sequence-builder.md` | Carousel sequence dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md` | Single-image/SuperVisual dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-112-two-d-character-scene-program-and-performance-compiler.md` | 2D character program dependency. |

## 2. Overview

This spec compiles approved expression ingredients into viewer-state `ContentSequenceProgram` objects and hands them to the correct composition engines. The program is a semantic/timing contract. It says which approved ingredients appear in which beat, what loop each beat opens or closes, what primitive coalition it serves, what viewer-state transition it performs, and which format adapter and composition functions should realize it.

The composition layer may make a sequence temporal or spatial, but it cannot change the semantic beat order, invent missing human expression, remove promised payoff, or bypass primitive/doctrine gates without creating a new program version.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-118-001 | `SequenceLoop` | Opens, closes, or explicitly defers a viewer-state question. |
| DEP-CMF-118-002 | `ViewerJourney` | Defines entry state, exit state, central question, promised payoff, future value key. |
| DEP-CMF-118-003 | `SequenceBeat` | Ordered beat bound to approved ingredient IDs and primitive coalition. |
| DEP-CMF-118-004 | `ContentSequenceProgram` | Frozen semantic program for one asset or sequence scope. |
| DEP-CMF-118-005 | `SequenceCompositionHandoff` | Hash-backed handoff to the correct composition engine. |
| DEP-CMF-118-006 | `ContentSequenceProgramFreezeReceipt` | Receipt proving source, loop, doctrine, adapter, and approval gates. |

### Existing Backend Integration

| Python Owner | Database Table(s) | API Route(s) | Migration / Backfill Behavior |
|---|---|---|---|
| `src/ccp_studio/services/content_sequence_program_compiler.py` | `content_sequence_programs`, `content_sequence_beats`, `sequence_loops` | `POST /api/cmf/sequence-programs/compile`, `POST /api/cmf/sequence-programs/{id}/freeze` | New tables keyed by inventory and format target. |
| `src/ccp_studio/services/sequence_composition_handoff_service.py` | `sequence_composition_handoffs` | `POST /api/cmf/sequence-programs/{id}/handoff` | New handoff table; downstream engines consume immutable handoff hash. |
| `src/ccp_studio/services/scene_spec_compiler.py` | `scene_specs`, `complete_editing_sessions` | existing composition routes | Consumes only frozen sequence handoffs. |
| `src/ccp_studio/services/evaluation_receipt_service.py` | `receipt_chain`, `evaluation_receipts`, `approval_blockers` | shared receipt writer | Writes program freeze receipt and adapter blockers. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-TRS-004` | Phase4-M02 | Sequence and composition handoff must preserve cinematic meaning and reject flat visual grammar. |
| `EXP-PRG-001` | Phase4-M03 | Adapter routing to downstream engines must resolve inline and deterministically. |
| `EXP-FBK-001` | Phase4-M05 | Loop, source, and adapter failures must return exact beat and ingredient repair action. |
| `EXP-TRS-003` | Phase4-M06 | Audio/caption/voice handoff cannot use generic sonic fallbacks when dynamic voice is involved. |
| `EXP-SOC-001` | Phase5-M01 | Frozen programs and handoffs are verifiable artifacts with hashes. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M02: Cinematic Meaning Rule | Phase 4 Story 2.1 | `EXP-TRS-004` | Program freeze blocks source-distorting sequence beats and flat/corporate adapter mappings. |
| Phase4-M03: Inline Routing SLA | Phase 4 Story 3.1 | `EXP-PRG-001` | Format adapter and composition target resolve during compile/freeze, not after rendering. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Rejections name exact beat, loop, ingredient, and adapter mapping failure. |
| Phase4-M06: Sonic Prestige Rule | Phase 4 Story 6.1 | `EXP-TRS-003` | Handoff flags voice/audio obligations for downstream premium audio handling. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Frozen sequence program and handoff write receipt-chain rows. |

### Receipt Chain Guard

| Receipt | Table | Action | Idempotency Key | Required Hashes |
|---|---|---|---|---|
| `ContentSequenceProgramFreezeReceipt` | `receipt_chain` | `content_sequence_program.frozen` | `sequence_program_id + version + program_sha256` | program hash, inventory hash, adapter hash, primitive receipt hashes |

### Sequence Pattern Examples

| Pattern | Typical Use |
|---|---|
| `QUESTION_CLUE_REFRAME_PAYOFF` | Opens audience curiosity, reveals clues, reframes, then pays off. |
| `SCENE_COST_MEANING` | Story/commentary sequence from lived scene to cost to meaning. |
| `MYTH_MECHANISM_REPLACEMENT` | Educational/PaperCut or carousel teaching sequence. |
| `CLAIM_PROOF_APPLICATION` | Authority or proof-led sequence. |
| `CHOICE_PREDICTION_REVEAL` | Poll, ranking, or this-vs-that reaction sequence. |
| `QUOTE_REACTION_INTERPRETATION_INVITATION` | Living Commentary Reaction or Conscious Reactions sequence. |

### Composition Function Handoff

| Composition Function | Downstream Runtime |
|---|---|
| `unexpected_closeup` | Video editing / Remotion. |
| `memory_object_insert` | Cinematic Story Commentary. |
| `paper_note_sequence` | PaperCut / Motion Canvas / 2D character runtime. |
| `contrast_panel` | Carousel, SuperVisual, reaction UI, or explainer panel. |
| `framework_reveal` | Educational / Explainer. |
| `reaction_pause` | Living Commentary Reaction. |
| `poll_choice_state` | Conscious Reactions Editing. |
| `tier_list` | Reaction template / quiz template. |
| `signature_end_card` | Package continuity and final CTA. |

### Downstream Compatibility Matrix

| `composition_engine_target` | Downstream Spec / Object | Required Handoff Fields |
|---|---|---|
| `video_edit_program` | `TS-CMF-106` reserved Video Edit Program compiler and `TS-CMF-080` composition runtime | Beat map refs, transcript timing refs, format target, locked ingredients, composition functions. |
| `carousel_builder` | `TS-CMF-096`, `TS-CMF-097`, `TS-CMF-098` / `CarouselSpec` | Slide sequence positions, slide atom hints, approved ingredients, primitive receipts. |
| `single_image_supervisual` | `TS-CMF-099` through `TS-CMF-105` / Single Image or SuperVisual spec | Single-frame composition family, headline/payoff, visual asset refs, primitive triad receipts. |
| `two_d_character_program` | `TS-CMF-110` through `TS-CMF-113` / `TwoDCharacterProgram` | Teaching beats, character action cues, performance states, transcript concept refs. |
| `reaction_template_runtime` | `TS-CMF-071` through `TS-CMF-075` / reaction template JSON | Reaction UI state, poll/ranking/tier-list states, lower-frame human reaction refs. |

### Format Adapter Principle

The sequence pattern is semantic. The adapter makes it temporal or spatial:

| Format | Adapter Responsibility |
|---|---|
| Cinematic Story Commentary | Full-screen guest closeups, memory-object inserts, atmospheric plates, emotional subtitles, slow push-ins, quote overlays. |
| Educational / Explainer | PaperCut or 2D avatar panels, diagrams, arrows, timeline strips, rough annotations, teaching labels. |
| Living Commentary Reaction | Upper-body guest/interviewer cutouts, reaction closeups, quote cards, emotional pause emphasis, eye-line matching. |
| Conscious Reactions Editing | Upper-frame reaction UI, polls, rankings, tier lists, debate cards, comments, meme cues, lower-frame human reaction. |
| Carousel | Slide atoms and composition atlas routing. |
| Single Image / SuperVisual | One-frame composition families, primitive triads, Skia final render. |

### Gate Thresholds

| Gate ID | Threshold | Hard Fail | Consequence |
|---|---:|---|---|
| `ingredient_binding_valid` | 1.00 | Yes | Program cannot compile. |
| `beat_order_unique_sorted` | 1.00 | Yes | Program rejected. |
| `loop_closure_valid` | 1.00 | Yes | Program cannot freeze. |
| `source_grounding` | 1.00 | Yes | Program cannot hand off to composition. |
| `format_adapter_compatibility` | 1.00 | Yes | Program cannot target format. |
| `primitive_coalition_coverage` | 0.90 | Yes | Composition-bearing beat blocked. |
| `doctrine_alignment` | 0.95 | Yes | Program cannot freeze. |
| `viewer_state_progression` | 0.85 | No | Operator review required. |

### Gate Verdict Semantics

| Verdict | Rule | Receipt Behavior |
|---|---|---|
| `PASS` | Beat order, loops, source, doctrine, adapter, and primitive gates pass. | Write freeze receipt and allow handoff. |
| `PROVISIONAL` | Viewer-state progression or format fit is below target but not hard-failed. | Require operator review; no render handoff yet. |
| `FAIL` | Repairable loop, source, adapter, or primitive failure. | Write blocker with exact beat and repair command. |
| `BLOCKED` | Unapproved ingredient, synthetic guest claim, or missing required payoff. | Stop program freeze. |

## 4. Implementation Plan

1. Add `src/ccp_studio/services/content_sequence_program_compiler.py`.
2. Add DSPy program `ContentSequenceProgramCompiler`.
3. Load frozen inventory, route target, format target, active registries, Brand Context, doctrine, and primitive receipts.
4. Rank planned hypotheses against actual ingredient quality and discover stronger unplanned hypotheses.
5. Select pattern and bind approved ingredient IDs to ordered beats.
6. Validate sequence loops and closure policies.
7. Attach primitive coalitions, affinity contract, future value contract, and doctrine constraints.
8. Run format adapter compatibility and composition function mapping.
9. Produce sequence preview read model for operator review.
10. Freeze approved program and emit composition handoff to specific engines.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class SequenceCompositionHandoff(BaseModel):
    schema_version: Literal["cmf.sequence_composition_handoff.v1"]
    handoff_id: str
    sequence_program_id: str
    sequence_program_sha256: str
    format_target: str
    composition_engine_target: Literal[
        "video_edit_program",
        "carousel_builder",
        "single_image_supervisual",
        "two_d_character_program",
        "reaction_template_runtime",
    ]
    composition_functions: list[str]
    beat_to_composition_map: list[dict]
    locked_ingredient_ids: list[str]
    transcript_timing_refs: list[str]
    brand_context_version_id: str
    doctrine_bundle_id: str
    primitive_receipt_refs: list[str]
    handoff_sha256: str


class ContentSequenceProgramFreezeReceipt(BaseModel):
    schema_version: Literal["cmf.content_sequence_program_freeze_receipt.v1"]
    receipt_id: str
    sequence_program_id: str
    version: int
    ingredient_inventory_id: str
    format_target: str
    sequence_pattern_id: str
    loop_closure_passed: bool
    source_grounding_passed: bool
    format_adapter_passed: bool
    doctrine_alignment_score: float = Field(ge=0, le=1)
    blocker_codes: list[str] = Field(default_factory=list)
    operator_status: Literal["approved", "needs_revision", "rejected"]
```

The canonical `ContentSequenceProgram` must retain bundle fields for `viewer_journey`, `loops`, `beats`, `affinity_contract`, `future_value_contract`, `doctrine_constraints`, `evaluation_requirement_ids`, and `program_sha256`.

## 6. Workflow

```text
load_frozen_inventory
-> rank_sequence_hypotheses
-> discover_unplanned_high_value_sequences
-> select_sequence_pattern
-> bind_ingredients_to_beats
-> validate_loops
-> attach_primitive_coalitions
-> select_format_adapter
-> map_composition_functions
-> operator_review
-> freeze_content_sequence_program
-> handoff_to_composition_engine
```

State machine:

```text
draft
-> source_validated
-> doctrine_validated
-> format_adapted
-> operator_review
-> approved
-> frozen
-> rendered
-> evaluated
-> published
```

## 7. API, Service, and Event Contracts

| Contract | Shape |
|---|---|
| `POST /api/cmf/sequence-programs/compile` | Compiles from inventory, route, and format target. |
| `POST /api/cmf/sequence-programs/{id}/validate` | Runs loop, source, doctrine, and adapter gates. |
| `POST /api/cmf/sequence-programs/{id}/review` | Operator revision/approval commands. |
| `POST /api/cmf/sequence-programs/{id}/freeze` | Freezes program and emits receipt. |
| `POST /api/cmf/sequence-programs/{id}/handoff` | Emits `SequenceCompositionHandoff`. |
| `GET /api/cmf/sequence-programs/{id}/preview` | Returns sequence preview read model. |

Events:

```text
ContentSequenceProgramCompiled
SequenceLoopValidated
SequenceProgramApprovalBlocked
ContentSequenceProgramFrozen
SequenceCompositionHandoffEmitted
```

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | Mandate / Test Evidence |
|---|---|---|---|
| AC1 | Content sequence compilation requires a frozen inventory. | A program compiles from unreviewed transcript fragments and bypasses inventory freeze. | Phase5-M01, `EXP-SOC-001`; inventory dependency test. |
| AC2 | Every human-expression beat references approved ingredient IDs. | A beat contains a generated quote that does not map to an approved ingredient. | Phase4-M02, `EXP-TRS-004`; source-grounding test. |
| AC3 | Beat order is unique, sorted, and immutable after freeze. | Composition moves payoff before clue without creating a new program version. | Phase4-M05, `EXP-FBK-001`; versioning test. |
| AC4 | Required loops must close unless explicitly marked `discussion_open` or `series_deferred`. | A title promises an answer but no beat closes the loop. | Phase4-M02, `EXP-TRS-004`; loop closure test. |
| AC5 | Format adapters cannot remove promised payoff or required source grounding. | Carousel adapter drops the proof beat because there is no slide space. | Phase4-M05, `EXP-FBK-001`; adapter compatibility test. |
| AC6 | Composition handoff includes program hash, locked ingredients, primitive receipts, transcript timing refs, doctrine refs, and target object mapping. | Handoff says `video_edit_program` but lacks beat-to-composition map or target spec owner. | Phase5-M01, `EXP-SOC-001`; handoff schema test. |

## 9. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Program validation tests | Beat order, loop closure, and missing ingredient failures. |
| Adapter tests | Each canonical format maps supported functions and blocks incompatible patterns. |
| Source-grounding tests | Synthetic or unapproved ingredient IDs block handoff. |
| Primitive tests | Beat-level primitive coalition coverage is enforced. |
| Revision tests | Reordering beat semantics creates new version. |
| Handoff tests | Composition handoff contains all hashes and refs needed by downstream engines. |

## 10. Doctrine-Driven Test Harness Binding

The harness must evaluate:

```text
perceptual_entry
relevant_open_question
active_prediction
truthful_payoff
human_affinity
expected_future_value
ethical_earned_attention
composition_handoff_integrity
```

Hard failures block freeze or composition handoff.

## Spec Audit Receipt

| Check | Status |
|---|---|
| Turns approved ingredients into semantic sequence programs | Pass |
| Keeps composition engines downstream of frozen sequence programs | Pass |
| Supports four video formats, carousel, and single-image/SuperVisual adapters | Pass |
| Blocks false open loops and fabricated guest meaning | Pass |
| Requires primitive/doctrine receipts before handoff | Pass |
