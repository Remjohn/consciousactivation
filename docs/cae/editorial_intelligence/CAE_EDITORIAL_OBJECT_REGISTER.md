# CAE Editorial Intelligence Object Register

**Document ID:** `CAE-REG-ED-001`  
**Governing Mandate:** `CAE-M00`  
**Status:** `CANONICAL SPECIFICATION`  
**Version:** `1.0.0`  
**Prepared:** 2026-08-28  

---

## 1. Overview & Purpose

This register formally establishes the 18 canonical objects governing the Editorial Intelligence lifecycle across the Conscious Activation Engine (CAE). It establishes the formal boundary separating **Program 1 (World $\rightarrow$ Interview Brief)** from **Program 2 (Interview $\rightarrow$ Production Assets)**.

No implementation package, service, or migration may introduce an editorial entity without adhering to the definitions, schemas, and lifecycle constraints declared herein.

---

## 2. Canonical Object Index

| # | Object Name | Primary Plane | Lifecycle Class | Write Authority (Mandate) | Nearest Neighbor / Anti-Collapse |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | `ResearchSignal` | World | Dynamic State | `CAE-M01` | $\ne$ `ContentOpportunity` (Signal $\ne$ Justified Intersection) |
| **02** | `AudienceState` | Relational | Dynamic State | `CAE-M02` | $\ne$ `GuestState` (Audience Wounds $\ne$ Guest Stance) |
| **03** | `GuestState` | Relational | Dynamic State | `CAE-M02` | $\ne$ `IdentityDNA` (Live Register $\ne$ Static Dossier) |
| **04** | `CollisionHypothesis` | Relational | Derived Artifact | `CAE-M03` | $\ne$ `ResearchSignal` (4-World Intersection $\ne$ Raw Trend) |
| **05** | `InterviewBrief` | Elicitation | Derived Artifact | `CAE-M04` | $\ne$ `InterviewResponse` (Elicitation Plan $\ne$ Human Evidence) |
| **06** | `InterviewResponse` | Evidence | Immutable Evidence | `CAE-M04` / Ingestion | $\ne$ `EvidenceSegment` (Raw Session Media $\ne$ Bounded Units) |
| **07** | `EvidenceSegment` | Evidence | Immutable Evidence | `CAE-M05` | $\ne$ `MediaAsset` (Transcript Span $\ne$ Storage Blob Handle) |
| **08** | `SemanticAnnotation` | Evidence | Derived Artifact | `CAE-M06` | $\ne$ `AssetAnnotation` (Broad Span Typing $\ne$ Deep Asset Label) |
| **09** | `ContentCandidate` | Editorial | Derived Artifact | `CAE-M07` | $\ne$ `EvidenceSegment` (Story Potential $\ne$ Raw Quote) |
| **10** | `CandidateCluster` | Editorial | Derived Artifact | `CAE-M08` | $\ne$ `ContentCandidate` (Semantic Family $\ne$ Single Option) |
| **11** | `EditorialStoryboard` | Editorial | Derived Artifact | `CAE-M09` | $\ne$ `SemanticProgram` (Operator Choice $\ne$ Realization Spec) |
| **12** | `MediaAsset` | Realization | Immutable Evidence | `CAE-M10` / Storage | $\ne$ `AssetAnnotation` (Byte Blob $\ne$ Semantic Metadata) |
| **13** | `AssetAnnotation` | Editorial | Derived Artifact | `CAE-M10` | $\ne$ `SemanticAnnotation` (Selected Asset $\ne$ Raw Segment) |
| **14** | `InsertRole` | Realization | Canonical Definition | `CAE-M10` | $\ne$ `VisualEffect` (Semantic Function $\ne$ Shader/Transition) |
| **15** | `SemanticProgram` | Realization | Derived Artifact | `CAE-M11` | $\ne$ `CompositionIR` (Editorial Intent $\ne$ Render Manifest) |
| **16** | `CompositionIR` | Realization | Execution Packet | `CAE-M11` | $\ne$ `VideoEditProgram` (Abstract Layout $\ne$ EDL Engine Syntax) |
| **17** | `VideoEditProgram` | Realization | Execution Packet | `CAE-M11` / CMF | $\ne$ `RemotionRender` (EDL/Code $\ne$ Rendered MP4) |
| **18** | `Outcome` | Outcome | Immutable Evidence | `CAE-M12` | $\ne$ `CandidateScore` (Observed Reality $\ne$ Predictive Guess) |

---

## 3. Object Specifications

### 01. `ResearchSignal`
* **Ontological Role:** Raw observed velocity, discourse, or cultural mutation in the external world.
* **Fields:**
  * `signal_id`: `str` (UUIDv7 / prefix `SIG-`)
  * `source`: `str` (`searxng` | `last30days` | `x_velocity` | `reddit_cluster` | `manual`)
  * `topic`: `str`
  * `entities`: `list[str]`
  * `raw_evidence`: `dict`
  * `velocity_score`: `float` ($0.0 \dots 1.0$)
  * `acceleration_score`: `float` ($0.0 \dots 1.0$)
  * `cross_source_divergence`: `float` ($0.0 \dots 1.0$)
  * `freshness_timestamp`: `datetime`
  * `provenance`: `dict`
* **Prohibition:** A `ResearchSignal` SHALL NOT contain guest activation hypotheses or audience tension assumptions.

---

### 02. `AudienceState`
* **Ontological Role:** The active psychological condition, subconscious tensions, schemas, and media motives of the target audience.
* **Fields:**
  * `audience_state_id`: `str` (UUIDv7 / prefix `AUD-`)
  * `context_premise_id`: `str` (Ref to CAE Context)
  * `active_tensions`: `list[str]` (Refs to `TNS-*`)
  * `existential_invariants`: `list[str]` (Refs to SDA Invariants)
  * `schema_assumptions`: `list[str]`
  * `affective_state`: `str`
  * `media_motive`: `str` (`validation` | `guidance` | `confrontation` | `escapism`)
* **Prohibition:** An `AudienceState` SHALL NOT store personal data of individual viewers; it represents cohort state.

---

### 03. `GuestState`
* **Ontological Role:** The lived authority, emotional DNA register, vulnerability boundaries, and trigger maps of the guest.
* **Fields:**
  * `guest_state_id`: `str` (UUIDv7 / prefix `GST-`)
  * `guest_id`: `str` (Ref to `CA-CAN-01B_GUEST`)
  * `emotional_dna_profile`: `dict` (Moral foundations, stance, edge, negative space)
  * `trigger_map_vectors`: `list[dict]` (EXP-TRG links, vulnerability vectors)
  * `lived_proof_milestones`: `list[str]`
  * `forbidden_territories`: `list[str]`
* **Prohibition:** A `GuestState` SHALL NOT be fabricated by an LLM without grounding in verified guest onboarding dossiers or prior transcripts.

---

### 04. `CollisionHypothesis`
* **Ontological Role:** A justified intersection among Audience Tension, Guest Authority, Oblique/Lateral World Lens, and Live World Signal.
* **Fields:**
  * `collision_id`: `str` (UUIDv7 / prefix `COL-`)
  * `audience_anchor_id`: `str` (Ref to `AudienceState`)
  * `guest_anchor_id`: `str` (Ref to `GuestState`)
  * `research_signal_id`: `str` (Ref to `ResearchSignal`)
  * `oblique_lens_passage_id`: `str` (Ref to Knowledge Portfolio book passage)
  * `collision_type`: `str` (`PREDICTION_VIOLATION` | `COSTLY_EXPOSURE` | `LATENT_ARTICULATION` | `PARADOX` | `SYSTEMS_MAPPING`)
  * `bridge_statement`: `str`
  * `activation_potential`: `float` ($0.0 \dots 1.0$)
  * `distribution_potential`: `float` ($0.0 \dots 1.0$)
  * `cliche_risk_score`: `float` ($0.0 \dots 1.0$)
  * `falsifiability_criteria`: `str`
* **Prohibition:** A `CollisionHypothesis` SHALL NOT become an `InterviewBrief` if its `cliche_risk_score` $> 0.70$ or if it lacks grounding in all 4 worlds.

---

### 05. `InterviewBrief`
* **Ontological Role:** The executable elicitation protocol instructing the interviewer/system on what evidence to extract from the human guest.
* **Fields:**
  * `brief_id`: `str` (UUIDv7 / prefix `BRF-`)
  * `collision_ref`: `str` (Ref to `CollisionHypothesis`)
  * `activation_objective`: `str`
  * `matrix_of_edging_seed`: `dict` (Target Expression, Resistance Vector)
  * `question_sequence`: `list[dict]` (Phase, Question, Provocation, Expected Evidence)
  * `forbidden_premature_closures`: `list[str]`
  * `evidence_requirements`: `list[str]`
* **Prohibition:** An `InterviewBrief` is a plan for extracting evidence; it SHALL NOT be treated as the evidence itself.

---

### 06. `InterviewResponse`
* **Ontological Role:** The raw, unmanipulated multimedia and transcript evidence recorded during an authentic interview session.
* **Fields:**
  * `response_id`: `str` (UUIDv7 / prefix `RSP-`)
  * `session_id`: `str` (Ref to `CA-CAN-02_INTERVIEW_SESSION`)
  * `brief_id`: `str` (Ref to `InterviewBrief`)
  * `raw_media_asset_id`: `str` (Ref to `MediaAsset`)
  * `raw_transcript_json`: `dict` (Word-level timestamps, speaker IDs, confidence)
  * `duration_seconds`: `float`
  * `authenticity_hash`: `str` (SHA-256 of raw bytes)
* **Prohibition:** An `InterviewResponse` is immutable; it SHALL NOT be edited, cleaned, or truncated in place.

---

### 07. `EvidenceSegment`
* **Ontological Role:** A rhetorically and semantically bounded contiguous slice of an interview transcript with exact time boundaries.
* **Fields:**
  * `segment_id`: `str` (UUIDv7 / prefix `SEG-`)
  * `response_id`: `str` (Ref to `InterviewResponse`)
  * `start_timestamp_ms`: `int`
  * `end_timestamp_ms`: `int`
  * `speaker_id`: `str`
  * `raw_text`: `str`
  * `semantic_boundary_type`: `str` (`THOUGHT_COMPLETION` | `RHETORICAL_SHIFT` | `ANECDOTE_BOUNDARY` | `REVELATION_MOMENT`)
  * `context_dependency_flag`: `bool`
* **Prohibition:** `EvidenceSegment` SHALL NOT receive expensive deep multimodal annotation at this stage (cheap segmentation only).

---

### 08. `SemanticAnnotation`
* **Ontological Role:** Preliminary semantic attribution and evidence typing applied to raw segments.
* **Fields:**
  * `annotation_id`: `str` (UUIDv7 / prefix `ANN-`)
  * `segment_id`: `str` (Ref to `EvidenceSegment`)
  * `evidence_class`: `str` (`QUOTE` | `BEAT` | `STORY` | `MECHANISM` | `CLAIM` | `CONTRADICTION` | `REVEAL`)
  * `invariant_refs`: `list[str]` (Refs to SDA Invariants)
  * `tension_ref`: `str` (Ref to `TNS-*`)
  * `emotional_register`: `str`
  * `guest_stance`: `str`
* **Prohibition:** A `SemanticAnnotation` does not grant publication or production authority.

---

### 09. `ContentCandidate`
* **Ontological Role:** A candidate story structure formed by combining evidence segments with narrative and rhetorical arcs.
* **Fields:**
  * `candidate_id`: `str` (UUIDv7 / prefix `CND-`)
  * `primary_segment_id`: `str` (Ref to `EvidenceSegment`)
  * `supporting_segment_ids`: `list[str]`
  * `story_arc_id`: `str` (`THE_WITNESS` | `BREAKTHROUGH` | `CONFRONTATION` | `SACRED_RETURN` | `CORE_TRANSFORMATION` | `TICKING_CLOCK` | etc.)
  * `archetype_id`: `str`
  * `hook_hypothesis`: `str`
  * `narrative_utility_score`: `float`
  * `activation_potential`: `float`
  * `distribution_potential`: `float`
  * `frame_alignment_score`: `float`
* **Prohibition:** A `ContentCandidate` SHALL NOT proceed to production without Operator Selection (`CAE-M09`).

---

### 10. `CandidateCluster`
* **Ontological Role:** A deduplicated cluster of content candidates sharing the same underlying tension or narrative mechanism.
* **Fields:**
  * `cluster_id`: `str` (UUIDv7 / prefix `CLS-`)
  * `latent_tension_ref`: `str`
  * `member_candidate_ids`: `list[str]`
  * `dominant_candidate_id`: `str`
  * `redundancy_score`: `float`
  * `cluster_summary`: `str`
* **Prohibition:** A cluster SHALL NOT drop unique variations until reviewed against audience sub-segments.

---

### 11. `EditorialStoryboard`
* **Ontological Role:** The operator-approved visual and narrative blueprint ready for production assembly.
* **Fields:**
  * `storyboard_id`: `str` (UUIDv7 / prefix `STB-`)
  * `selected_candidate_id`: `str` (Ref to `ContentCandidate`)
  * `operator_id`: `str` (Ref to `CA-CAN-01A_OPERATOR_ACCESS_GRANT`)
  * `narrative_structure`: `list[dict]` (Scene sequence: Hook $\rightarrow$ Tension $\rightarrow$ Turn $\rightarrow$ Mechanism $\rightarrow$ Resolution)
  * `planned_inserts`: `list[dict]` (Insert role, target duration, semantic simile criteria)
  * `operator_tuning_notes`: `str`
  * `approval_timestamp`: `datetime`
* **Prohibition:** An `EditorialStoryboard` cannot be created by automated inference without verified human operator signature.

---

### 12. `MediaAsset`
* **Ontological Role:** A verified immutable byte object (video, audio, image) stored with isolated storage coordinates and hash verification.
* **Fields:**
  * `media_asset_id`: `str` (UUIDv7 / prefix `AST-`)
  * `storage_uri`: `str`
  * `mime_type`: `str`
  * `byte_size`: `int`
  * `sha256_hash`: `str`
  * `duration_ms`: `int` (if temporal)
  * `provenance_type`: `str` (`RAW_INTERVIEW` | `REAL_WORLD_E_ROLL` | `ARCHIVAL_D_ROLL` | `PREVIOUS_INTERVIEW` | `SYNTHETIC_CANDIDATE`)
* **Prohibition:** Direct in-place mutation of a `MediaAsset` byte blob is constitutionally forbidden (`CA-CAN-01B`).

---

### 13. `AssetAnnotation`
* **Ontological Role:** Deep semantic and multimodal labeling applied strictly to operator-selected reusable assets.
* **Fields:**
  * `asset_annotation_id`: `str` (UUIDv7 / prefix `AAN-`)
  * `media_asset_id`: `str` (Ref to `MediaAsset`)
  * `exact_time_range`: `dict` (`start_ms`, `end_ms`)
  * `transcript_exact`: `str`
  * `editorial_roles`: `list[str]` (Refs to `InsertRole`)
  * `semantic_invariants`: `list[str]`
  * `emotional_valence`: `str`
  * `reuse_profile`: `dict` (Scores for `hook`, `story_beat`, `comedic_punctuation`, `training_sample`)
  * `license_and_rights`: `dict` (Usage constraints, attribution requirements)
* **Prohibition:** Full-length raw interviews SHALL NOT receive `AssetAnnotation` records (only selected slices).

---

### 14. `InsertRole`
* **Ontological Role:** Canonical functional classification of non-primary video/audio inserts (E-roll / D-roll).
* **Fields:**
  * `role_code`: `str` (`SEMANTIC_SIMILE` | `PATTERN_MATCH` | `PATTERN_INTERRUPT` | `COMEDIC_PUNCTUATION` | `FORESHADOWING` | `CONTRAST` | `CULTURAL_RECOGNITION` | `EMOTIONAL_AMPLIFICATION` | `WORLD_BUILDING`)
  * `category`: `str` (`E_ROLL_REALITY` | `D_ROLL_ILLUSTRATION`)
  * `max_recommended_duration_seconds`: `float` (Default: $6.0\text{s}$)
  * `description`: `str`
* **Prohibition:** An `InsertRole` is semantic intent; it SHALL NOT be hardcoded to a specific visual file.

---

### 15. `SemanticProgram`
* **Ontological Role:** The complete high-level semantic specification governing media rendering.
* **Fields:**
  * `program_id`: `str` (UUIDv7 / prefix `PRG-`)
  * `storyboard_id`: `str` (Ref to `EditorialStoryboard`)
  * `scene_sequence`: `list[dict]`
  * `primary_speech_assets`: `list[str]` (Refs to `AssetAnnotation`)
  * `insert_asset_manifest`: `list[dict]` (Asset Ref + `InsertRole`)
  * `sfl_perceptual_profile`: `dict` (Pacing, typography, audio density, camera grammar)
  * `target_duration_range`: `dict` (`min_seconds`, `max_seconds`)
* **Prohibition:** `SemanticProgram` SHALL NOT contain low-level FFmpeg parameters or canvas pixel coordinates.

---

### 16. `CompositionIR`
* **Ontological Role:** The intermediate representation specifying tracks, clips, overlays, transitions, and audio layers.
* **Fields:**
  * `composition_ir_id`: `str` (UUIDv7 / prefix `CIR-`)
  * `program_id`: `str` (Ref to `SemanticProgram`)
  * `timeline`: `dict` (Tracks: `video_a`, `video_b_insert`, `captions`, `audio_voice`, `audio_sfx`, `audio_bed`)
  * `clip_manifest`: `list[dict]` (Source URIs, cut-in, cut-out, timeline-start, timeline-end)
  * `caption_manifest`: `list[dict]` (Word-boundary tokens, style classes, highlight keys)
* **Prohibition:** `CompositionIR` must be renderer-agnostic (convertible to Remotion, HyperFrames, or FFmpeg EDL).

---

### 17. `VideoEditProgram`
* **Ontological Role:** The concrete execution syntax (Remotion project bundle, EDL, or FFmpeg filtergraph) ready for hardware execution.
* **Fields:**
  * `edit_program_id`: `str` (UUIDv7 / prefix `EDP-`)
  * `composition_ir_id`: `str` (Ref to `CompositionIR`)
  * `engine`: `str` (`REMOTION` | `HYPERFRAMES` | `FFMPEG_STANDALONE`)
  * `entrypoint_file`: `str`
  * `render_parameters`: `dict` (Resolution, FPS, Bitrate, Codec)
* **Prohibition:** A `VideoEditProgram` cannot be generated without an approved upstream `CompositionIR`.

---

### 18. `Outcome`
* **Ontological Role:** Verified distribution metrics and feedback observations capturing actual performance vs predictions.
* **Fields:**
  * `outcome_id`: `str` (UUIDv7 / prefix `OUT-`)
  * `edit_program_id`: `str` (Ref to `VideoEditProgram`)
  * `published_uri`: `str`
  * `metrics_snapshot`: `dict` (Retention at 3s, Retention at 50%, Completion rate, Shares, Comments, Activation conversions)
  * `predicted_vs_actual`: `dict`
  * `operator_retrospective`: `str`
  * `timestamp`: `datetime`
* **Prohibition:** Metrics alone SHALL NOT overwrite canonical schemas; they feed calibration models in `CAE-M12`.
