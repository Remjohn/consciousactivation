# CAE Editorial Intelligence Contradiction Register

**Document ID:** `CAE-CON-ED-001`  
**Governing Mandate:** `CAE-M00`  
**Status:** `CANONICAL SPECIFICATION`  
**Version:** `1.0.0`  
**Prepared:** 2026-08-28  

---

## 1. Overview & Purpose

This register defines and defends the critical boundary separations across the CAE Editorial Intelligence architecture. In brownfield systems and LLM agent pipelines, there is a recurring tendency to collapse distinct concepts into generic shortcuts (e.g., treating search trends as content ideas, or treating entire raw transcripts as reusable assets). 

Such collapses cause architectural drift, reward hacking, and the loss of genuine editorial quality. This register establishes strict anti-collapsing rules.

---

## 2. Core Anti-Collapse Invariants

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   CORE ANTI-COLLAPSE INVARIANTS                                        │
├───────────────────────────────┬───────────────────────────────┬────────────────────────────────────────┤
│ Entity A                      │ Entity B                      │ Reason They Must Remain Distinct       │
├───────────────────────────────┼───────────────────────────────┼────────────────────────────────────────┤
│ ResearchSignal                │ ContentOpportunity            │ Signal = World Fact;                   │
│                               │                               │ Opportunity = Justified 4-World Cross  │
├───────────────────────────────┼───────────────────────────────┼────────────────────────────────────────┤
│ EvidenceSegment               │ MediaAsset                    │ Segment = Semantic/Text Boundary;      │
│                               │                               │ Asset = Isolated Physical Byte Blob    │
├───────────────────────────────┼───────────────────────────────┼────────────────────────────────────────┤
│ ContentCandidate              │ EditorialStoryboard           │ Candidate = Machine Narrative Option;  │
│                               │                               │ Storyboard = Operator-Approved Choice  │
├───────────────────────────────┼───────────────────────────────┼────────────────────────────────────────┤
│ SemanticAnnotation            │ AssetAnnotation               │ Semantic = Broad Cheap Span Typing;    │
│                               │                               │ Asset = Expensive Multimodal Label     │
├───────────────────────────────┼───────────────────────────────┼────────────────────────────────────────┤
│ SemanticProgram               │ CompositionIR                 │ Program = Intent & SFL Profile;        │
│                               │                               │ CompositionIR = Renderer-Agnostic Track│
└───────────────────────────────┴───────────────────────────────┴────────────────────────────────────────┘
```

---

## 3. Detailed Collision Analysis & Defenses

### Case 1: `ResearchSignal` $\ne$ `ContentOpportunity` (`CollisionHypothesis`)
* **The Failure Mode (Viral Scraper Fallacy):** An agent finds a trending topic on Reddit/X and immediately writes an interview prompt or video script.
* **Why It Fails:** A world trend is merely an environmental observation. Without grounding in the Guest's Emotional DNA and the Audience's subconscious invariant wounds, the resulting content is generic, inauthentic, and lacks authority.
* **The Boundary Defense:** A `ResearchSignal` cannot advance into an `InterviewBrief` without passing through `CAE-M03` (`CollisionHypothesis`), proving intersection with all 4 worlds (Guest, Audience, Oblique, Live).

---

### Case 2: `EvidenceSegment` $\ne$ `MediaAsset`
* **The Failure Mode (Media Storage Collapse):** Treating transcript text spans as storage asset IDs or vice-versa.
* **Why It Fails:** An `EvidenceSegment` is a logical, contextual unit of spoken thought with semantic boundaries (e.g., lines 14–22 of session 3). A `MediaAsset` is an immutable, content-addressed binary file (MP4/WAV) in S3. One `MediaAsset` may contain 400 `EvidenceSegments`.
* **The Boundary Defense:** `EvidenceSegment` references `InterviewResponse` and `MediaAsset` via foreign keys and millisecond offsets, but does not own raw storage bytes.

---

### Case 3: `ContentCandidate` $\ne$ `EditorialStoryboard`
* **The Failure Mode (Autonomous Slop Pipeline):** Allowing an automated candidate generator to directly trigger video rendering.
* **Why It Fails:** Machine scoring can easily reward-hack superficial keywords, fake profundity, or high-scoring phrases that have zero narrative cohesion or emotional truth.
* **The Boundary Defense:** `CAE-M09` establishes a non-negotiable **Operator Human Gate**. Only an `EditorialStoryboard` signed by an authenticated operator access grant can be compiled into a `SemanticProgram`.

---

### Case 4: `SemanticAnnotation` $\ne$ `AssetAnnotation`
* **The Failure Mode (Annotation Over-Spend):** Running expensive, multimodal, multi-model labeling and captioning on the entire 2-hour interview transcript.
* **Why It Fails:** Wasteful computation and token saturation. 90% of a raw interview will not be published as standalone short-form assets.
* **The Boundary Defense:**
  * `SemanticAnnotation` is cheap, high-recall categorization across all segments.
  * `AssetAnnotation` is deep, expensive, multimodal annotation applied strictly to the 10–40 assets selected by the Operator for reuse and dataset construction.

---

### Case 5: `SemanticProgram` $\ne$ `CompositionIR`
* **The Failure Mode (Coupled Renderer):** Putting FFmpeg command flags or Remotion component names directly inside the semantic editor.
* **Why It Fails:** Tight coupling breaks portability. When the rendering framework changes (e.g., from Remotion to HyperFrames or custom WebGL), the entire semantic engine must be rewritten.
* **The Boundary Defense:** `SemanticProgram` specifies *what* meaning, pacing, and assets to render (SFL profile). `CompositionIR` specifies *where* tracks, tokens, and cut points lie.

---

## 4. Enforcement & Static Audit

Any pull request, specification, or code change that violates these 5 boundary separations will be rejected by the static authority validator (`validate_editorial_authority.py`) with a structured `TAXONOMY_ERROR` or `AUTHORITY_ERROR`.
