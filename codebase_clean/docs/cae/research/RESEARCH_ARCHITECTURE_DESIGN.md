# Research Architecture Design — Guest-Emotional-DNA-Conditioned Content Opportunity Engine

**Document ID:** `CAE-RSRCH-DESIGN-001`
**Author:** ZCode independent review lane (not a governed execution agent)
**Status:** `DESIGN_DRAFT — AWAITING_OPERATOR_REVIEW` (this is a design proposal, NOT an accepted spec, NOT an executed mandate, NOT a ratified record)
**Date:** `2026-08-27`
**Feeds:** future `SPEC-RSRCH-001` and its Track B implementation mandate
**Priority order honored:** upstream intelligence → object constitutions → operator review → then extension of the research layer

---

## 0. Why this document exists

The CAE already has the interview intelligence to take Guest Context + Research and produce a Brief (SPEC-GST-UI-001 → SPEC-BRF-001). What is missing — and what this document addresses — is the **research acquisition layer** itself: how we *generate* the research that feeds the interview brief, rather than only ingesting operator-supplied URLs and documents.

The operator's requirement, stated verbatim:

> "we need to research content ideas that will trigger the reaction of our guest according to their emotional DNA profile but also CONTENT IDEAS that have high chances to go viral as well"

The four referenced sources are:
- `mvanhorn/last30days-skill` — cross-source research aggregation methodology
- `searxng/searxng` — metasearch retrieval infrastructure
- `Remjohn/ccf` (early 2025 Conscious Content Engine) — viral frameworks, archetypes, voice DNA
- `Remjohn/CCP/lab` — emotional DNA, trigger map, research methodology, eval scoring

This document reads those sources against the **existing CAE ontology** (SDA/SFL/primitives/constitutions/typed domain in `services/air/src/cmf_activative_intelligence/domain.py`) and designs the integration so it **extends** the ontology rather than importing a parallel doctrine.
---

## 1. The one load-bearing distinction: ResearchSignal ≠ ContentOpportunity

This is the core architectural commitment, and everything else follows from it.

- **ResearchSignal** = something happening in the world. A query is rising in velocity. A moral controversy is forming. A niche is fragmenting. It exists independent of any guest.
- **ContentOpportunity** = the *justified intersection* of a world signal with (a) a specific guest's emotional DNA, (b) the audience's current state, (c) the live premise being engineered, (d) semantic geometry, and (e) distribution potential.

Most trend tools stop at "this is trending." The CAE does not. A trend becomes a ContentOpportunity only when it can be shown to *activate this guest* and *carry distribution weight*. The raw signal is necessary but never sufficient.

This maps directly to the CCP insight from the SearXNG viral-engine research: cross-engine **divergence** (pre-consensus state) is the alpha signal, and to the CAE governance principle that no object is promoted without evidence lineage.

---

## 2. What each external source actually contributes

### 2.1 SearXNG — the retrieval infrastructure layer

SearXNG is not a trend source; it is a **privacy-preserving metasearch engine** that aggregates results across Google/Bing/DuckDuckGo/etc. Its value to CAE is as the *neutral retrieval backbone* — it exposes raw SERPs across engines, which lets us measure **cross-engine consensus vs divergence** without a single-vendor bias.

The CCP lab's `lab/Viral Trend Engine with SEARXNG.md` defines the 14 signal parameters we should adopt as the ResearchSignal feature space:

| Group | Signals |
|---|---|
| Query-level | velocity, acceleration (2nd derivative — early detection), novelty score, mutation rate |
| Cross-engine (SearXNG advantage) | engine agreement, engine divergence, result-rank volatility |
| Freshness/velocity | publication timestamp density, new-domain emergence, content-volume spike |
| Content structure | entity extraction density, headline pattern clustering |
| Engagement proxies | SERP feature presence, click-entropy proxy |

**The alpha insight to keep:** high engine divergence + high query mutation + low click entropy = "pre-consensus trend." That is precisely the state where a content opportunity can be captured before it commoditizes. This is the *distribution-potential* half of the score.

### 2.2 last30days-skill — the cross-source aggregation adapter

`last30days-skill` is a multi-source research skill that searches Reddit, X, YouTube, Hacker News, Polymarket, and the web, then clusters and synthesizes results with engagement weighting. Its methodology gives us the **ResearchAdapter** pattern: fan out to N heterogeneous sources, normalize into a common signal shape, then cluster.

What we take from it is **not** its specific tooling (which is agent-scoped), but the architectural pattern:
1. multi-source fan-out (social + news + prediction market + forum),
2. per-source normalization,
3. engagement-weighted ranking,
4. cluster → narrative synthesis.

This supplies the *breadth* of the epistemic surface, distinct from SearXNG's *retrieval depth*.

### 2.3 CCF (early 2025) — the viral framework heritage

`Remjohn/ccf` `Strategy and Frameworks/` holds 18 documents including "The 22 Enhanced Viral Frameworks," "Content Archetypes Emotional Triggers," "The Semiotics of Virality," "The Memetic Viral Engineering," and "TTT DNA for CCF Voice Engineering." Its README plus Stage 1–3 soul-infused generators reveal the early architectural intent: stream-of-consciousness → prompt adapter → voice-authentic script.

What survives into the new ontology:
- **Viral Trinity (Surprise + Emotion + Specificity)** — the original viral scoring axiom from the OLD CMF archive, already cross-mapped to the new SemanticAssessment (see §6).
- **22 framework ↔ archetype ↔ persuasive-angle ↔ TTT-palette mapping** (`CCP/lab/framework_archetype_mapping.yalm.md`) — the distribution grammar: a given content idea belongs to a framework whose archetype and voice-gravity palette determine its viral ceilings and floor.
- **TTT voice DNA** — maps to CAE `voice_dna` / `BRAND_VOICE`.

### 2.4 CCP lab — the emotional DNA + trigger + research-method heritage

This is the decisive source because it is where "emotional DNA" and "trigger prediction" are actually defined, and it cleanly maps onto CAE's existing typed domain.

Key directories/files read:
- `emotional DNA/` — "Emotional DNA: Market Validation Framework" (neuroaesthetics: mPFC/self-referential reward circuit), "Emotional Granularity and Affective Signatures," "Cognitive Appraisal Theory."
- `Trigger Map Flow/` — "Moral Foundations Theory for Trigger Prediction" (Haidt; predictive over reactive trigger identification), "Evocative Question Design for AI" (semantic construction vs episodic retrieval — the "mask" of defended beliefs).
- `CRAL/` — netnography, precision journalism, sensemaking theory, information foraging, mood congruence: the *reproducible research-method* layer.
- `Novelty distribution/`, `Memetic Engine/`, `Identity Engine Research/`, `Voice DNA/`, `Memory/`, `Inference-Time Compute/`.
- `phase0_eval_card_scoring_model_v_1.md` — the 6+1 eval surface: Humanity, Presence, Trust, Memorability, Resonance, Signal, plus `AI Slop Risk`.

**The single most important CCP insight for this design** (from the Emotional DNA market validation + Trigger Map):

> Semantic construction (prefrontal, defended, socially-desirable "what do you think?") ≠ episodic retrieval (hippocampal/amygdala, lived, raw "what happened?"). A content idea *triggers* only when it reaches the episodic register, not the semantic one.

This is why "researching topics the guest cares about" is insufficient. The research layer must surface **signals that map to the guest's lived-trigger structure** (moral foundations, identity threat, self-referential reward), not merely their stated topical interests.

---

## 3. The CAE ontology already has the slots — no new doctrine required

This is the key finding that makes the integration tractable. The typed domain in `services/air/src/cmf_activative_intelligence/domain.py` already validates the exact objects this research layer must produce and consume:

| Concept (external) | CAE object / field (already in domain.py) |
|---|---|
| Emotional DNA profile | `identity_dna` object + `identity_dna_candidate_observation` with `proposed_dimension` enum: `identity_role`, `stance`, `edge`, `emotional_range`, `visual_world`, `negative_space`, `lived_proof` |
| Trigger prediction (Moral Foundations) | `experience_plane` primitives `EXP-TRG-*` (PRIMITIVE_INVENTORY.csv); `matrix_of_edging`; `planned_questions` with `psychological_role` + `activation_direction` |
| Voice/emotion calibration | `voice_dna` with `emotional_distance`; `visual_dna` |
| Guest context binding | `context` object requiring `identity_dna_ref`, `audience_context_ref`, `live_premise`, `matrix_of_edging_ref`, `evidence_refs` |
| Provenance / legal grounding | `EVIDENCE_SOURCE` context class + `FR-CAE-TEN-009_EVIDENCE_SOURCE_PROVENANCE` |
| Captioning for future dataset | `CAPTION_TRACK` context class (already in `interview_composer.py:45-51`) |
| Misuse/over-reach guard | `misuse_risk` object with `trigger_condition`, `misuse_mode`, `probable_wrong_reading`, `severity`, `prevention_gate` |
| Active context class taxonomy | `IDENTITY_DNA`, `CONTEXT_PREMISE`, `RESONANCE_REFERENCE`, `BRAND_VOICE`, `EVIDENCE_SOURCE`, `INTERVIEW_RECORDING`, `CAPTION_TRACK` (already in both `interview_composer.py` and `schemas`)

**Conclusion:** the emotional DNA profile and trigger architecture already have canonical homes. The research layer only needs to **emit** ResearchSignals and **resolve** them into ContentOpportunities that carry typed refs back to these objects. There is no fifth parallel identity system to invent.

---

## 4. The proposed pipology: three research modes, one resolver

Consistent with the "world-first, guest-DNA-conditioned, audience-congruence" three-mode framing already discussed, the research engine has three acquisition modes feeding a single resolver:

### Mode A — World-first (SearXNG + last30days adapter)
Cold acquisition of emergent signals with no guest input. Pure ResearchSignal production: query velocity/acceleration, cross-engine divergence, freshness spikes, headline clustering. Output: raw `ResearchSignal` candidates with distribution evidence.

### Mode B — Guest-DNA-conditioned (the operator's explicit priority)
The world signal space is *filtered and re-ranked by the guest's* `identity_dna` dimensions + `EXP-TRG-*` trigger primitives + moral-foundations axes. The question is no longer "what is trending" but **"which of the trending signals maps onto this guest's lived trigger structure?"** This is where SemanticAssessment must be conditioned on episodic-retrieval (not semantic-construction) framing — per CCP's Trigger Map + Evocative Question design.

### Mode C — Audience-congruence
Signals scored against `audience_context_ref` for whether the audience is at a receptive state (per CCP's Mood Management / Uses-and-Gratifications / Regulatory Focus research in `Novelty distribution/`).

All three modes converge on the **Resolver**, which is the only component permitted to emit a `ContentOpportunity`.

---

## 5. The dual scoring model

Every ContentOpportunity is scored on three multiplied axes (no one axis may compensate for another — consistent with the "non-compensable hard gates" principle from the OLD CMF):

```
ContentOpportunityScore =
  ActivationPotential    × DistributionPotential    × EvidenceConfidence
```

- **ActivationPotential** (0–1): does this signal reach the guest's *lived* trigger register? Derived from the intersection of the signal's entities/frames with the guest's `identity_dna` dimensions, `EXP-TRG-*` triggers, and moral-foundations mapping. Low if the signal only *sounds* relevant (semantic construction) but does not reach an episodic trigger.
- **DistributionPotential** (0–1): the viral half. SearXNG pre-consensus signals (velocity, divergence, novelty) cross-referenced with CCF's 22-framework/archetype/TTT mapping and the phase0 `Signal` + `Memorability` + `Resonance` clusters. `AI Slop Risk` is a *negative* gate (not a subtractive score — a hard ceiling if it exceeds threshold).
- **EvidenceConfidence** (0–1): provenance quality per `FR-CAE-TEN-009`. Number of independent sources, cross-engine agreement, source authority, contradiction account. Directly the anti-fabrication axis — an opportunity borrowed from a single unverifiable source scores near-zero here.

**Hard gates (non-compensable):**
1. No `ContentOpportunity` may cite a guest trigger it cannot trace to an `identity_dna` dimension or an `EXP-TRG-*` primitive.
2. No `ContentOpportunity` may proceed with EvidenceConfidence below a floor (unproven world signal is not publishable research).
3. `AI Slop Risk` above threshold → the opportunity is quarantined, not downgraded.

---

## 6. CMF Heritage crosswalk (RETAIN / ADAPT / SUBSUME)

This connects to the prior OLD CMF integration analysis. The old CMF scoring/clustering is not competition — it is the distribution/viral application layer that the new ontology's Evaluator was missing:

| OLD CMF heritage | New CAE disposition | Action |
|---|---|---|
| 13 Story Arcs | canonical registry of `CMF-ARC-*` under the SFL/primitive layer | **RETAIN** (as governed registry, not free text) |
| Viral Trinity (Surprise+Emotion+Specificity) | folded into `SemanticAssessment` evaluation profile | **SUBSUME** (keeps the triad, gains typed home) |
| Perception scorers (authenticity, coping, moral emotion, reconsolidation) | deterministic `ANALYST` evaluator nodes | **ADAPT** (deterministic scorers become governed evaluator nodes) |
| `beat_cluster.json` EDL | `HarnessRun` output schema | **ADAPT** (beat cluster = run artifact, not loose JSON) |
| CCF 22 viral frameworks / archetypes / TTT | DistributionPotential feature dictionary + `voice_dna` | **ADAPT** (framework mapping as governed reference data) |
| phase0 6+1 eval card surface | `evaluation_profile` fields | **SUBSUME** (Humanity/Presence/Trust/Memorability/Resonance/Signal/AI-Slop) |

Nothing is wholesale deprecated. The integration is a *re-homing* of proven scoring grammar into governed, versioned, receipted objects.

---

## 7. Slotting into the existing 4-node topology

The canonical workflow is already HUNTER → COMPOSER → ANALYST → COMMANDER (per `services/pipeline/src/cmf_pipeline/demo.py` and the corrected topology decision). The research engine maps as:

- **HUNTER** = SearXNG + last30days adapter fan-out. Inspects the *world* (Mode A). Emits `ResearchSignal` candidates. Does not interpret; only extracts structured signals.
- **CONDITIONER** (new, but expressed through existing `CONTEXT_PREMISE` + `identity_dna_ref`) = Mode B + C. Filters/re-ranks signals against guest DNA + audience. This is NOT a new agent; it is the existing `context` object's live-premise binding, applied at research time.
- **COMPOSER** = the Resolver. Assembles the justified `ContentOpportunity` with its dual-score and typed refs.
- **ANALYST** = read-only evaluator. Runs the deterministic perception/eval scorers (adapted CMF scorers + phase0 clusters) and emits the `SemanticAssessment` / `evaluation_profile` with evidence links. Read-only; never mutates.
- **COMMANDER** = operator review gate. The opportunity is presented to the operator, who decides whether it proceeds to Brief generation (SPEC-BRF-001).

This is the same 4-node topology with the research acquisition prepended, not a replacement.

---

## 8. Canonical object contracts (proposed — to be finalized in SPEC-RSRCH-001)

```text
ResearchSignal
  signal_id, observed_at, source_refs[] (EVIDENCE_SOURCE)
  signal_kind (query_velocity | freshness_spike | engine_divergence | entity_emergence | moral_controversy | ...)
  feature_vector (the 14 SearXNG params, normalized)
  raw_evidence_refs[] (FR-CAE-TEN-009 provenance)

ContentOpportunity
  opportunity_id, research_signal_ref
  guest_ref (identity_dna_ref), audience_context_ref
  live_premise, trigger_refs[] (EXP-TRG-*), moral_foundation_axes[]
  activation_potential, distribution_potential, evidence_confidence
  ai_slop_risk, hard_gate_violations[]
  framework_ref (CCF archetype), voice_dna_ref
  evaluation_profile_ref, semantic_assessment_ref
  receipt_sha256 (immutable, per CA-UPTL-01 reasoning receipt pattern)
```

Both objects are typed, versioned, receipted, and tenant-scoped. The `ContentOpportunity` is the bridge object between the research layer and the existing `POST /api/interviews/compose/brief/generate` flow (SPEC-BRF-001): a generated brief must be able to cite the `ContentOpportunity` it was derived from.

---

## 9. Recommended mandate sequence (for operator review — NOT yet authorized)

This design does **not** authorize any implementation. It proposes the following order, consistent with the operator's "upstream first, constitutions second, then read and decide" protocol:

1. **`CA-CMFI-01`** — Old-Intelligence Canonical Import: register 13 arcs, viral rubrics, scorer suite, and EDL schema as governed canonical registries. (Precondition for DistributionPotential having canonical reference data.)
2. **`SPEC-RSRCH-001`** — ResearchSignal → ContentOpportunity spec: finalizes §8 contracts, the dual-score, the hard gates, and the endpoint surface. This document is its design seed.
3. **`CA-RSRCH-01`** — SearXNG retrieval adapter + last30days fan-out (Mode A) verification: proves real retrieval against a seeded SearXNG instance, with live-probe evidence.
4. **`CA-RSRCH-02`** — Guest-DNA-conditioned resolver (Modes A→B→C) + dual scoring + ANALYST eval integration.
5. **`CA-BRF-UI-01`** — Brief UI (Track B #3), which then consumes `ContentOpportunity` refs when generating briefs.

Step 4 is the one that delivers the operator's exact sentence: research ideas that *both* trigger the guest per emotional DNA *and* carry viral potential.

---

## 10. Open decisions requiring the operator (do not proceed past design)

1. **SearXNG deployment scope**: self-hosted instance (full control, `searxng/searxng`) vs a managed metasearch endpoint. Affects retrieval credentials and rate limits — an infrastructure decision the operator must make.
2. **Research-autonomy ceiling**: how far the Resolver may rank/recommend before an operator gate is mandatory. (This document assumes COMMANDER gates every ContentOpportunity; the operator may relax this for Mode C only later.)
3. **The 14 SearXNG features** are adopted *as a proposal*; the operator may trim the feature space before SPEC-RSRCH-001 freezes it.
4. **CMF heritage import cadence**: whether CA-CMFI-01 imports all 13 arcs at once or only the arcs with live scorer coverage.

None of these are resolvable from the codebase; they are authority/provisioning decisions.