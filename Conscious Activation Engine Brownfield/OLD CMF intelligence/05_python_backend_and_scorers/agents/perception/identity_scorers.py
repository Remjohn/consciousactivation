"""
Identity Scoring Sub-Agents — Layer 2 Computational Core

Four scoring functions that produce the component scores of the IdentityVector:
    1. score_narrative_identity()  → NarrativeIdentityScore  (Layer 2A)
    2. compute_self_discrepancy()  → SelfDiscrepancyProfile   (Layer 2B)
    3. score_sdt_needs()           → SDTNeedProfile           (Layer 2C)
    4. classify_cognitive_distortions() → CognitiveDistortionReport (Layer 2D)

These are NOT separate agents. They are modular scoring functions
called within Aria's extraction pipeline after entity extraction.

Architecture: identity_engine_architecture.md, Layer 2
CCF Bible Critique: Uses cognitive state instructions (Principle 1),
pre-computation constraints (Principle 3), no role assignments (Principle 7).
"""

import re
import logging
from typing import Optional
from pathlib import Path

import yaml

from backend.core.identity_models import (
    NarrativeIdentityScore,
    SelfDiscrepancyProfile,
    SDTNeedProfile,
    CognitiveDistortionReport,
    DetectedDistortion,
    CulturalFrame,
    DominantGapType,
    EmotionalSignature,
    DominantNeed,
    NeedTrajectory,
    CognitiveDistortionType,
    ConfidenceLevel,
)

logger = logging.getLogger(__name__)

# ─── Marker Library Loading ──────────────────────────────────────────

_MARKERS_DIR = Path(__file__).resolve().parent.parent.parent / "intelligence_library"


def _load_yaml(filename: str) -> dict:
    """Loads a YAML marker library from intelligence_library/."""
    path = _MARKERS_DIR / filename
    if not path.exists():
        logger.warning(f"Marker library not found: {path}")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


# Lazy-loaded marker dictionaries
_sdt_markers: dict | None = None
_cd_definitions: dict | None = None


def _get_sdt_markers() -> dict:
    global _sdt_markers
    if _sdt_markers is None:
        _sdt_markers = _load_yaml("sdt_markers.yaml")
    return _sdt_markers


def _get_cd_definitions() -> dict:
    global _cd_definitions
    if _cd_definitions is None:
        _cd_definitions = _load_yaml("cognitive_distortion_definitions.yaml")
    return _cd_definitions


# ─── 1. Narrative Identity Scorer (Layer 2A) ─────────────────────────

# Agency markers — Western/Individualist
_AGENCY_MARKERS_DIRECT = [
    "I decided", "I chose", "I took control", "I built", "I created",
    "I conquered", "I fought", "I overcame", "I achieved", "I made it",
    "I took charge", "I grabbed", "I dominated", "I won",
]

# Agency markers — Relational/Collectivist (per Cross-Cultural Identity paper)
_AGENCY_MARKERS_RELATIONAL = [
    "I accepted", "I fulfilled my role", "I honored", "I served",
    "I maintained", "we succeeded", "our family", "I upheld",
    "I carried", "I provided", "I endured", "I persevered",
]

_COMMUNION_MARKERS = [
    "we", "together", "connected", "shared", "community", "family",
    "belong", "support", "loved", "cared for", "trusted", "relationship",
    "bond", "close to", "my people", "our", "friendship",
]

_REDEMPTION_MARKERS = [
    "but then", "and that's when", "everything changed for the better",
    "I realized", "I finally understood", "it turned out",
    "the lesson was", "I grew from", "it made me stronger",
    "blessing in disguise", "silver lining", "it was worth it",
]

_CONTAMINATION_MARKERS = [
    "and then it all fell apart", "everything went wrong",
    "I lost everything", "it was ruined", "destroyed",
    "things got worse", "it went downhill", "the darkness came",
    "I spiraled", "fell apart", "broke down", "shattered",
]

_MEANING_MAKING_MARKERS = [
    "I understand now", "I learned that", "looking back",
    "I realize", "in hindsight", "the meaning of", "I see now",
    "it taught me", "I've come to see", "the pattern is",
    "I notice", "I'm starting to see", "what I understand now",
]


def score_narrative_identity(
    text: str,
    cultural_frame: CulturalFrame = CulturalFrame.DIRECT_INDIVIDUALIST,
) -> NarrativeIdentityScore:
    """
    Scores narrative identity dimensions from journal text.

    Cognitive state: Pattern recognition across narrative structures.
    You are identifying the building blocks of a life story being
    constructed in real-time — agency, communion, redemptive/contaminating
    sequences, and meaning-making operations.

    Cultural frame correction: Individualist users express agency through
    conquest language. Collectivist users express agency through
    role-fulfillment language. Without this correction, collectivist
    users receive systematically deflated agency scores.
    """
    text_lower = text.lower()
    word_count = len(text.split())
    evidence_quotes = []

    # Pre-computation constraint (CCF Bible, Principle 3):
    # If word count < 50, all scores get LOW confidence — insufficient signal.
    if word_count < 50:
        return NarrativeIdentityScore(confidence=ConfidenceLevel.LOW)

    # --- Agency scoring with cultural frame correction ---
    agency_markers = (
        _AGENCY_MARKERS_RELATIONAL
        if cultural_frame == CulturalFrame.RELATIONAL_COLLECTIVIST
        else _AGENCY_MARKERS_DIRECT
    )
    # Hybrid gets both marker sets
    if cultural_frame == CulturalFrame.HYBRID_DIASPORIC:
        agency_markers = _AGENCY_MARKERS_DIRECT + _AGENCY_MARKERS_RELATIONAL

    agency_hits = sum(1 for m in agency_markers if m.lower() in text_lower)
    agency_score = min(1.0, agency_hits / max(len(agency_markers) * 0.3, 1))

    # --- Communion scoring ---
    communion_hits = sum(1 for m in _COMMUNION_MARKERS if m.lower() in text_lower)
    communion_score = min(1.0, communion_hits / max(len(_COMMUNION_MARKERS) * 0.25, 1))

    # --- Redemption/Contamination arc ---
    redemption_hits = sum(1 for m in _REDEMPTION_MARKERS if m.lower() in text_lower)
    contam_hits = sum(1 for m in _CONTAMINATION_MARKERS if m.lower() in text_lower)
    total_arc = redemption_hits + contam_hits
    if total_arc > 0:
        redemption_arc = (redemption_hits - contam_hits) / total_arc
    else:
        redemption_arc = 0.0

    # --- Meaning-making ---
    meaning_hits = sum(1 for m in _MEANING_MAKING_MARKERS if m.lower() in text_lower)
    meaning_score = min(1.0, meaning_hits / max(len(_MEANING_MAKING_MARKERS) * 0.2, 1))

    # Collect evidence quotes for matched markers
    for markers_list in [agency_markers, _COMMUNION_MARKERS, _REDEMPTION_MARKERS, _CONTAMINATION_MARKERS]:
        for m in markers_list:
            if m.lower() in text_lower:
                # Extract sentence containing the marker
                for sentence in re.split(r'[.!?]+', text):
                    if m.lower() in sentence.lower():
                        evidence_quotes.append(sentence.strip()[:200])
                        break

    # Confidence based on total marker hits
    total_hits = agency_hits + communion_hits + redemption_hits + contam_hits + meaning_hits
    if total_hits >= 5:
        confidence = ConfidenceLevel.HIGH
    elif total_hits >= 2:
        confidence = ConfidenceLevel.MEDIUM
    else:
        confidence = ConfidenceLevel.LOW

    return NarrativeIdentityScore(
        agency=round(agency_score, 3),
        communion=round(communion_score, 3),
        redemption_arc=round(redemption_arc, 3),
        meaning_making=round(meaning_score, 3),
        cultural_frame=cultural_frame,
        confidence=confidence,
        evidence_quotes=evidence_quotes[:10],  # Cap at 10 quotes
    )


# ─── 2. Self-Discrepancy Calculator (Layer 2B) ──────────────────────

def compute_self_discrepancy(
    identity_entities: list[dict],
    dream_entities: list[dict],
    fear_entities: list[dict],
) -> SelfDiscrepancyProfile:
    """
    Computes self-discrepancy gaps between Actual, Ideal, and Feared selves.

    Cognitive state: Distance measurement between self-representations.
    You are computing how far apart three mental representations are:
    who the user IS (identity), who they WANT to be (dreams), and
    who they FEAR becoming (fears). The distances between these
    representations predict specific emotional outcomes (Higgins, 1987).

    Uses sentence-transformer embeddings for semantic distance.
    Falls back to lexical overlap when embeddings unavailable.
    """
    # Extract text from entities
    identity_texts = [e.get("name", "") for e in identity_entities if e.get("name")]
    dream_texts = [e.get("name", "") for e in dream_entities if e.get("name")]
    fear_texts = [e.get("name", "") for e in fear_entities if e.get("name")]

    # Need at least 1 identity entity to compute anything
    if not identity_texts:
        return SelfDiscrepancyProfile(confidence=ConfidenceLevel.LOW)

    # Try embedding-based distance, fall back to lexical overlap
    try:
        actual_ideal_gap, actual_ought_gap, feared_proximity = _compute_embedding_distances(
            identity_texts, dream_texts, fear_texts
        )
    except Exception as e:
        logger.warning(f"Embedding distance failed, using lexical fallback: {e}")
        actual_ideal_gap, actual_ought_gap, feared_proximity = _compute_lexical_distances(
            identity_texts, dream_texts, fear_texts
        )

    # Hope-Fear Balance (Paper 5: Possible Selves)
    # 0 = balanced (max motivation), -1 = all feared, +1 = all hoped
    hope_count = len(dream_texts)
    fear_count = len(fear_texts)
    total = hope_count + fear_count
    hope_fear_balance = (hope_count - fear_count) / total if total > 0 else 0.0

    # Determine dominant gap type and predicted emotional signature
    gaps = {
        DominantGapType.IDEAL: actual_ideal_gap,
        DominantGapType.FEARED: feared_proximity,
        DominantGapType.OUGHT: actual_ought_gap,
    }
    dominant = max(gaps, key=gaps.get)

    emotional_map = {
        DominantGapType.IDEAL: EmotionalSignature.DEJECTION,
        DominantGapType.OUGHT: EmotionalSignature.AGITATION,
        DominantGapType.FEARED: EmotionalSignature.ANXIETY,
    }

    # Confidence
    confidence = ConfidenceLevel.LOW
    if identity_texts and (dream_texts or fear_texts):
        confidence = ConfidenceLevel.MEDIUM
    if identity_texts and dream_texts and fear_texts:
        confidence = ConfidenceLevel.HIGH

    return SelfDiscrepancyProfile(
        actual_ideal_gap=round(actual_ideal_gap, 3),
        actual_ought_gap=round(actual_ought_gap, 3),
        feared_self_proximity=round(feared_proximity, 3),
        hope_fear_balance=round(hope_fear_balance, 3),
        dominant_gap_type=dominant,
        predicted_emotional_signature=emotional_map[dominant],
        confidence=confidence,
    )


def _compute_embedding_distances(
    identity: list[str], dreams: list[str], fears: list[str]
) -> tuple[float, float, float]:
    """
    Computes semantic distances using sentence-transformers.
    Returns (actual_ideal_gap, actual_ought_gap, feared_self_proximity).
    """
    from sentence_transformers import SentenceTransformer
    import numpy as np

    model = SentenceTransformer("all-MiniLM-L6-v2")

    identity_emb = model.encode(identity)
    identity_centroid = np.mean(identity_emb, axis=0)

    actual_ideal_gap = 0.5  # Default middle value
    if dreams:
        dream_emb = model.encode(dreams)
        dream_centroid = np.mean(dream_emb, axis=0)
        # Cosine distance (0 = identical, 1 = orthogonal)
        cos_sim = np.dot(identity_centroid, dream_centroid) / (
            np.linalg.norm(identity_centroid) * np.linalg.norm(dream_centroid) + 1e-8
        )
        actual_ideal_gap = max(0.0, min(1.0, 1.0 - cos_sim))

    feared_proximity = 0.0  # Default: far from feared self
    if fears:
        fear_emb = model.encode(fears)
        fear_centroid = np.mean(fear_emb, axis=0)
        # Similarity (higher = closer to feared self = worse)
        cos_sim = np.dot(identity_centroid, fear_centroid) / (
            np.linalg.norm(identity_centroid) * np.linalg.norm(fear_centroid) + 1e-8
        )
        feared_proximity = max(0.0, min(1.0, (cos_sim + 1) / 2))

    # Ought gap — approximated from dream gap + feared proximity
    # (True ought-self requires separate extraction not yet available)
    actual_ought_gap = min(1.0, (actual_ideal_gap + feared_proximity) / 2)

    return actual_ideal_gap, actual_ought_gap, feared_proximity


def _compute_lexical_distances(
    identity: list[str], dreams: list[str], fears: list[str]
) -> tuple[float, float, float]:
    """
    Fallback: lexical overlap-based distance when embeddings unavailable.
    """
    identity_words = set(" ".join(identity).lower().split())

    actual_ideal_gap = 0.5
    if dreams:
        dream_words = set(" ".join(dreams).lower().split())
        overlap = len(identity_words & dream_words)
        total = len(identity_words | dream_words) or 1
        actual_ideal_gap = 1.0 - (overlap / total)

    feared_proximity = 0.0
    if fears:
        fear_words = set(" ".join(fears).lower().split())
        overlap = len(identity_words & fear_words)
        total = len(identity_words | fear_words) or 1
        feared_proximity = overlap / total

    actual_ought_gap = min(1.0, (actual_ideal_gap + feared_proximity) / 2)
    return actual_ideal_gap, actual_ought_gap, feared_proximity


# ─── 3. SDT Need Profiler (Layer 2C) ────────────────────────────────

def score_sdt_needs(
    text: str,
    markers: Optional[dict] = None,
) -> SDTNeedProfile:
    """
    Scores Self-Determination Theory basic need satisfaction/frustration.

    Cognitive state: Need-signal detection across linguistic markers.
    You are scanning for evidence of three psychological needs being
    met or thwarted. The score for each need is the net balance of
    satisfaction markers minus frustration markers, normalized to 0-100.

    Pre-computation constraints (CCF Bible, Principle 3):
    - If word count < 50: all scores default to 50 (neutral), LOW confidence
    - Explicit markers score at 1.0 weight
    - Structural patterns score at 0.7 weight (detected keywords only for now)
    """
    text_lower = text.lower()
    word_count = len(text.split())

    if word_count < 50:
        return SDTNeedProfile(confidence=ConfidenceLevel.LOW)

    if markers is None:
        markers = _get_sdt_markers()

    results = {}
    all_evidence = {"autonomy": [], "competence": [], "relatedness": []}

    for need in ["autonomy", "competence", "relatedness"]:
        need_data = markers.get(need, {})
        sat_markers = need_data.get("satisfaction", {}).get("explicit", [])
        frust_markers = need_data.get("frustration", {}).get("explicit", [])

        # Count matches
        sat_hits = 0
        frust_hits = 0

        for marker in sat_markers:
            if marker.lower() in text_lower:
                sat_hits += 1
                # Find evidence
                for sentence in re.split(r'[.!?]+', text):
                    if marker.lower() in sentence.lower():
                        all_evidence[need].append(f"[SAT] {sentence.strip()[:150]}")
                        break

        for marker in frust_markers:
            if marker.lower() in text_lower:
                frust_hits += 1
                for sentence in re.split(r'[.!?]+', text):
                    if marker.lower() in sentence.lower():
                        all_evidence[need].append(f"[FRUST] {sentence.strip()[:150]}")
                        break

        # Score: satisfaction weighted at 1.0, frustration at 1.0
        # Normalize to 0-100 scale
        net = sat_hits - frust_hits
        # Map to 0-100: 0 hits = 50 (neutral), positive = above 50, negative = below 50
        score = max(0, min(100, 50 + (net * 10)))
        results[need] = score

    # Determine dominant need (most frustrated = lowest score)
    dominant = min(results, key=results.get)
    dominant_enum = DominantNeed(dominant.upper())

    # Confidence based on total marker hits
    total_evidence = sum(len(v) for v in all_evidence.values())
    if total_evidence >= 4:
        confidence = ConfidenceLevel.HIGH
    elif total_evidence >= 2:
        confidence = ConfidenceLevel.MEDIUM
    else:
        confidence = ConfidenceLevel.LOW

    return SDTNeedProfile(
        autonomy=results["autonomy"],
        competence=results["competence"],
        relatedness=results["relatedness"],
        autonomy_markers=all_evidence["autonomy"][:5],
        competence_markers=all_evidence["competence"][:5],
        relatedness_markers=all_evidence["relatedness"][:5],
        dominant_need=dominant_enum,
        need_trajectory=NeedTrajectory.UNKNOWN,  # Requires ≥3 entries — set by Chronos
        confidence=confidence,
    )


# ─── 4. Cognitive Distortion Classifier (Layer 2D) ──────────────────

def classify_cognitive_distortions(
    text: str,
    cd_definitions: Optional[dict] = None,
) -> CognitiveDistortionReport:
    """
    Classifies cognitive distortions in journal text using keyword heuristics.

    Cognitive state: Pattern matching against distortion taxonomy.
    You are scanning for thought patterns where the person's interpretation
    of events deviates from the evidence available. Each detected distortion
    must have: the exact quote, the distortion type, and which identity
    dimension it most affects.

    For LLM-based DoT classification, see classify_cognitive_distortions_llm().
    This function provides the fast, deterministic baseline.
    """
    text_lower = text.lower()
    word_count = len(text.split())

    if word_count < 30:
        return CognitiveDistortionReport()

    if cd_definitions is None:
        cd_definitions = _get_cd_definitions()

    distortion_defs = cd_definitions.get("distortions", {})
    detected = []

    for dist_key, dist_data in distortion_defs.items():
        keywords = dist_data.get("detection_heuristics", {}).get("keywords", [])
        dist_type_str = dist_data.get("type", "")
        identity_signal = dist_data.get("identity_signal", "")

        # Try to match CognitiveDistortionType enum
        try:
            dist_type = CognitiveDistortionType(dist_type_str)
        except ValueError:
            continue

        for keyword in keywords:
            if keyword.lower() in text_lower:
                # Find the sentence containing this keyword
                evidence = ""
                for sentence in re.split(r'[.!?]+', text):
                    if keyword.lower() in sentence.lower():
                        evidence = sentence.strip()[:200]
                        break

                # Avoid duplicate detections for same distortion type
                already_detected = any(d.type == dist_type for d in detected)
                if not already_detected:
                    detected.append(DetectedDistortion(
                        type=dist_type,
                        evidence_quote=evidence,
                        confidence=0.6,  # Keyword-only = medium confidence
                        identity_signal=identity_signal,
                        reasoning=f"Keyword '{keyword}' matched in journal entry",
                    ))
                break  # One keyword match per distortion type

    # Determine dominant distortion (most frequently detected type)
    dominant = None
    if detected:
        type_counts = {}
        for d in detected:
            type_counts[d.type] = type_counts.get(d.type, 0) + 1
        dominant = max(type_counts, key=type_counts.get)

    # Density: distortions per 100 words
    density = (len(detected) / word_count * 100) if word_count > 0 else 0.0

    return CognitiveDistortionReport(
        distortions=detected,
        dominant_distortion=dominant,
        distortion_density=round(density, 2),
    )


# ─── Composite: Build Full Identity Vector ──────────────────────────

def build_identity_vector(
    text: str,
    entities: list[dict],
    cultural_frame: CulturalFrame = CulturalFrame.DIRECT_INDIVIDUALIST,
    entry_id: str = "",
) -> "IdentityVector":
    """
    Orchestrates all 4 sub-agent scoring functions and composes
    the master IdentityVector.

    Called by Aria after entity extraction completes.
    """
    from backend.core.identity_models import IdentityVector

    word_count = len(text.split()) if text else 0

    # Separate entities by type
    identity_entities = [e for e in entities if e.get("relationship") == "HAS_IDENTITY"]
    dream_entities = [e for e in entities if e.get("relationship") == "CRAVES"]
    fear_entities = [e for e in entities if e.get("relationship") == "FEARS"]

    # Run all 4 sub-agents
    narrative = score_narrative_identity(text, cultural_frame)
    discrepancy = compute_self_discrepancy(identity_entities, dream_entities, fear_entities)
    sdt = score_sdt_needs(text)
    distortions = classify_cognitive_distortions(text)

    # Compute overall confidence (weighted average)
    confidence_map = {ConfidenceLevel.HIGH: 1.0, ConfidenceLevel.MEDIUM: 0.6, ConfidenceLevel.LOW: 0.2}
    sub_confidences = [
        confidence_map[narrative.confidence],
        confidence_map[discrepancy.confidence],
        confidence_map[sdt.confidence],
    ]
    overall_confidence = sum(sub_confidences) / len(sub_confidences)

    return IdentityVector(
        narrative=narrative,
        discrepancy=discrepancy,
        sdt=sdt,
        distortions=distortions,
        entry_id=entry_id,
        word_count=word_count,
        confidence=round(overall_confidence, 3),
    )
