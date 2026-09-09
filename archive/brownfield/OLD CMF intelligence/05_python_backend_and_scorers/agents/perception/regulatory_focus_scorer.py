"""
Regulatory Focus Scorer — Audience Extraction Module

Implements Higgins' Regulatory Focus Theory (RFT) linguistic marker
detection. Scans text for promotion (eagerness) vs. prevention (vigilance)
markers to determine the audience's dominant motivational orientation.

Architecture: Context Premise Engine → Sub-Profile 1
Research: Higgins (1997), ACL Anthology "Prevention or Promotion?" (2023)

Pre-computation constraints:
    - No LLM calls. Marker-based heuristics only.
    - Minimum 20 words required for reliable scoring.
    - Threshold delta of 0.15 required before assigning dominant orientation.

Negative Space:
    - This scorer does NOT replace DHDs as a user-facing label.
    - This scorer does NOT assess chronic regulatory disposition (that requires RFQ).
    - This scorer ONLY detects situational regulatory focus from text.
"""

import re
from backend.core.audience_trigger_models import (
    RegulatoryFocusProfile,
    RegulatoryOrientation,
)

# ─── Promotion (Eagerness) Markers ───────────────────────────────────
# Source: ACL Anthology (2023), Higgins (1997), LIWC Hope/Achievement dims
PROMOTION_MARKERS = {
    # Core vocabulary
    "hope", "wish", "aspire", "dream", "imagine", "envision",
    "win", "success", "gain", "reward", "achieve", "accomplish",
    "grow", "growth", "advance", "progress", "opportunity", "potential",
    "build", "create", "innovate", "transform", "elevate", "expand",
    "ideal", "aspiration", "ambition",
    # Emotional valence (cheerfulness family)
    "excited", "thrilled", "passionate", "inspired", "motivated",
    "proud", "joyful", "optimistic", "eager", "enthusiastic",
    # Abstract / interpretive action verbs (promotion-linked)
    "helps", "enables", "empowers", "encourages", "fosters",
    "cultivates", "nurtures", "unlocks", "unleashes",
    # Future-oriented / maximal goal language
    "could be", "what if", "one day", "vision", "breakthrough",
    "next level", "level up", "upgrade", "soar",
}

# ─── Prevention (Vigilance) Markers ──────────────────────────────────
# Source: ACL Anthology (2023), Higgins (1997), LIWC Safety/Obligation dims
PREVENTION_MARKERS = {
    # Core vocabulary
    "careful", "cautious", "avoid", "prevent", "protect", "secure",
    "safe", "safety", "guard", "shield", "defend", "preserve",
    "duty", "obligation", "responsible", "responsibility", "must",
    "should", "ought", "need to", "have to", "supposed to",
    "mistake", "error", "loss", "risk", "threat", "danger",
    # Emotional valence (quiescence/agitation family)
    "worried", "anxious", "nervous", "concerned", "fearful",
    "relieved", "calm", "stable", "steady", "secure",
    "guilty", "ashamed",
    # Concrete / descriptive action verbs (prevention-linked)
    "check", "verify", "monitor", "inspect", "audit",
    "maintain", "sustain", "ensure", "comply", "adhere",
    # Past-oriented / minimal goal language
    "don't lose", "can't afford", "never again", "hold on to",
    "keep what", "not fall behind",
}

# ─── Scoring threshold ───────────────────────────────────────────────
ORIENTATION_DELTA_THRESHOLD = 0.15
MIN_WORD_COUNT = 20


def _tokenize(text: str) -> list[str]:
    """Simple whitespace + punctuation tokenizer."""
    return re.findall(r'\b[a-z\']+\b', text.lower())


def _count_marker_hits(tokens: list[str], text_lower: str, markers: set) -> int:
    """
    Count marker occurrences. Supports both single-word and multi-word markers.
    Single-word markers are matched against tokens.
    Multi-word markers are matched against the full lowered text.
    """
    count = 0
    for marker in markers:
        if " " in marker:
            # Multi-word marker: count occurrences in full text
            count += text_lower.count(marker)
        else:
            # Single-word marker: count in token list
            count += tokens.count(marker)
    return count


def score_regulatory_focus(text: str) -> RegulatoryFocusProfile:
    """
    Scores a text for Regulatory Focus orientation.

    Computes promotion (eagerness) and prevention (vigilance) scores
    as normalized marker densities. Assigns dominant orientation
    only when the differential exceeds 0.15.

    Args:
        text: Raw audience text to analyze.

    Returns:
        RegulatoryFocusProfile with scores and orientation.
    """
    tokens = _tokenize(text)
    word_count = len(tokens)

    if word_count < MIN_WORD_COUNT:
        return RegulatoryFocusProfile(
            eagerness_score=0.0,
            vigilance_score=0.0,
            dominant_orientation=RegulatoryOrientation.DUAL_DOMINANT,
            linguistic_evidence=["insufficient_text"],
        )

    text_lower = text.lower()

    # Count hits
    promo_hits = _count_marker_hits(tokens, text_lower, PROMOTION_MARKERS)
    prev_hits = _count_marker_hits(tokens, text_lower, PREVENTION_MARKERS)

    total_hits = promo_hits + prev_hits

    if total_hits == 0:
        return RegulatoryFocusProfile(
            eagerness_score=0.0,
            vigilance_score=0.0,
            dominant_orientation=RegulatoryOrientation.DUAL_DOMINANT,
            linguistic_evidence=["no_markers_detected"],
        )

    # Normalize to 0-1 range
    # Use density-based normalization: hits per 100 words, capped at 1.0
    eagerness = min(1.0, (promo_hits / word_count) * 10)
    vigilance = min(1.0, (prev_hits / word_count) * 10)

    # Determine dominant orientation
    delta = abs(eagerness - vigilance)
    if delta < ORIENTATION_DELTA_THRESHOLD:
        orientation = RegulatoryOrientation.DUAL_DOMINANT
    elif eagerness > vigilance:
        orientation = RegulatoryOrientation.PROMOTION
    else:
        orientation = RegulatoryOrientation.PREVENTION

    # Collect evidence (top matched markers)
    evidence = []
    for marker in PROMOTION_MARKERS:
        if " " in marker:
            if marker in text_lower:
                evidence.append(f"[PROMO] {marker}")
        else:
            if marker in tokens:
                evidence.append(f"[PROMO] {marker}")
    for marker in PREVENTION_MARKERS:
        if " " in marker:
            if marker in text_lower:
                evidence.append(f"[PREV] {marker}")
        else:
            if marker in tokens:
                evidence.append(f"[PREV] {marker}")

    return RegulatoryFocusProfile(
        eagerness_score=round(eagerness, 3),
        vigilance_score=round(vigilance, 3),
        dominant_orientation=orientation,
        linguistic_evidence=evidence[:10],  # Cap at 10 evidence items
    )
