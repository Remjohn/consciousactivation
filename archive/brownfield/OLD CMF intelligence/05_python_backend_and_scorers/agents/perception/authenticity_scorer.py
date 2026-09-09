"""
Authenticity Scorer — Audience Extraction Module

Implements the L-depth framework (Kozinets netnography) combined with
a LIWC-22 Authenticity proxy for classifying text disclosure depth.

L-depth framework:
    L1 (Performative) = polished, high self-monitoring, broadcast-mode
    L2 (Communal) = semi-private, in-group norms, moderate authenticity
    L3 (Authentic) = anonymous, raw, unpolished, low self-monitoring

The LIWC-22 Authenticity proxy uses open-source heuristics:
    - Self-reference density (I/me/my ratio)
    - Negative emotion word frequency
    - Cognitive complexity inverse (simpler = more authentic)
    - Narrative vs. formal style detection

Architecture: Context Premise Engine → Sub-Profile 6
Research: Verified L3 Data Through Digital Ethnography,
          Pennebaker LIWC-22 (2022), Mind After Midnight hypothesis

Pre-computation constraints:
    - No LLM calls. Pronoun ratios + heuristics.
    - Minimum 20 words for reliable scoring.
    - Temporal context (timestamp) is optional but increases accuracy.

Negative Space:
    - Authenticity ≠ truthfulness. It measures self-monitoring level.
    - Low authenticity does NOT mean lying. It means polished/filtered.
    - This scorer does NOT verify identity or detect bots.
"""

import re
from typing import Optional
from backend.core.audience_trigger_models import (
    AuthenticityScore,
    LDepth,
)

# ─── Self-Reference Pronouns ────────────────────────────────────────
FIRST_PERSON_SINGULAR = {"i", "me", "my", "mine", "myself", "i'm", "i've", "i'll", "i'd"}

# ─── Negative Emotion Words ─────────────────────────────────────────
NEGATIVE_EMOTION = {
    "angry", "sad", "depressed", "anxious", "scared", "afraid",
    "frustrated", "overwhelmed", "exhausted", "hopeless", "worthless",
    "miserable", "devastated", "heartbroken", "furious", "terrified",
    "helpless", "lonely", "ashamed", "guilty", "disgusted",
    "hate", "regret", "cry", "crying", "sobbing", "tears",
    "stress", "stressed", "struggling", "suffering", "hurt",
    "pain", "painful", "ache", "aching", "broken",
}

# ─── Formal / Polished Markers (LOW authenticity) ────────────────────
FORMAL_MARKERS = {
    "furthermore", "moreover", "consequently", "nevertheless",
    "notwithstanding", "hereby", "pursuant", "regarding",
    "in conclusion", "to summarize", "in summary",
    "it should be noted", "one might argue",
    "the aforementioned", "as previously stated",
    "please note", "kindly",
}

# ─── Informal / Spontaneous Markers (HIGH authenticity) ──────────────
INFORMAL_MARKERS = {
    "honestly", "tbh", "ngl", "lowkey", "highkey",
    "literally", "omg", "wtf", "lol", "lmao",
    "idk", "imo", "imho", "smh", "fml",
    "can't even", "i swear", "no joke",
    "real talk", "for real", "not gonna lie",
    "dead serious", "seriously though",
}

# ─── Cognitive Complexity Markers (HIGH complexity = LOW authenticity)
COMPLEX_SYNTAX = {
    "however", "although", "whereas", "notwithstanding",
    "insofar as", "with respect to", "in terms of",
    "on the other hand", "in contrast", "conversely",
    "predicated on", "contingent upon",
}

# ─── L-depth contextual markers ─────────────────────────────────────
L1_CONTEXT_MARKERS = {
    "#ad", "#sponsored", "link in bio", "check out my",
    "follow me", "subscribe", "like and share",
    "swipe up", "don't forget to",
}

L2_CONTEXT_MARKERS = {
    "this group", "our community", "fellow", "members",
    "between us", "in this space", "safe space",
    "off the record", "just between",
}

L3_CONTEXT_MARKERS = {
    "throwaway", "anonymous", "burner account",
    "can't tell anyone", "nobody knows",
    "at 2am", "at 3am", "can't sleep",
    "first time admitting", "never told anyone",
}

MIN_WORD_COUNT = 20


def _tokenize(text: str) -> list[str]:
    return re.findall(r'\b[a-z\']+\b', text.lower())


def _count_markers(tokens: list[str], text_lower: str, markers: set) -> int:
    count = 0
    for marker in markers:
        if " " in marker or marker.startswith("#"):
            count += text_lower.count(marker)
        else:
            count += tokens.count(marker)
    return count


def score_authenticity(
    text: str,
    timestamp_hour: Optional[int] = None,
    platform_type: Optional[str] = None,
) -> AuthenticityScore:
    """
    Scores text for disclosure authenticity using LIWC-22 proxy heuristics
    and L-depth classification.

    Args:
        text: Raw audience text to analyze.
        timestamp_hour: Hour of day (0-23) when text was created, if known.
        platform_type: Platform type ('anonymous', 'social', 'professional'), if known.

    Returns:
        AuthenticityScore with L-depth classification and proxy scores.
    """
    tokens = _tokenize(text)
    text_lower = text.lower()
    word_count = len(tokens)

    if word_count < MIN_WORD_COUNT:
        return AuthenticityScore()

    # ── Component 1: Self-Reference Density ──
    fp_count = _count_markers(tokens, text_lower, FIRST_PERSON_SINGULAR)
    self_ref_density = min(1.0, fp_count / max(word_count * 0.1, 1))

    # ── Component 2: Negative Emotion Frequency ──
    neg_count = _count_markers(tokens, text_lower, NEGATIVE_EMOTION)
    neg_emotion_density = min(1.0, neg_count / max(word_count * 0.05, 1))

    # ── Component 3: Cognitive Complexity Inverse ──
    formal_count = _count_markers(tokens, text_lower, FORMAL_MARKERS)
    complex_count = _count_markers(tokens, text_lower, COMPLEX_SYNTAX)
    informal_count = _count_markers(tokens, text_lower, INFORMAL_MARKERS)

    formality_ratio = (formal_count + complex_count) / max(informal_count + 1, 1)
    complexity_inverse = max(0.0, min(1.0, 1.0 - (formality_ratio * 0.2)))

    # ── Composite LIWC Authenticity Proxy ──
    # Higher self-reference + higher negative emotion + lower complexity = higher authenticity
    authenticity_proxy = (
        0.35 * self_ref_density +
        0.30 * neg_emotion_density +
        0.35 * complexity_inverse
    )

    # ── Circadian Weighting (Mind After Midnight) ──
    temporal_context = "unknown"
    if timestamp_hour is not None:
        if 0 <= timestamp_hour <= 5:
            temporal_context = "late_night"
            authenticity_proxy = min(1.0, authenticity_proxy * 1.3)  # 30% boost
        elif 6 <= timestamp_hour <= 10:
            temporal_context = "morning"
        elif 11 <= timestamp_hour <= 17:
            temporal_context = "peak_hours"
        else:
            temporal_context = "evening"

    # ── L-Depth Classification ──
    l1_hits = _count_markers(tokens, text_lower, L1_CONTEXT_MARKERS)
    l2_hits = _count_markers(tokens, text_lower, L2_CONTEXT_MARKERS)
    l3_hits = _count_markers(tokens, text_lower, L3_CONTEXT_MARKERS)

    # Platform-based priors
    if platform_type == "anonymous":
        l3_hits += 2
    elif platform_type == "professional":
        l1_hits += 2

    # Classify L-depth
    if l3_hits > l2_hits and l3_hits > l1_hits:
        l_depth = LDepth.L3_AUTHENTIC
    elif l2_hits > l1_hits:
        l_depth = LDepth.L2_COMMUNAL
    elif l1_hits > 0:
        l_depth = LDepth.L1_PERFORMATIVE
    else:
        # Fall back to authenticity proxy
        if authenticity_proxy >= 0.65:
            l_depth = LDepth.L3_AUTHENTIC
        elif authenticity_proxy >= 0.35:
            l_depth = LDepth.L2_COMMUNAL
        else:
            l_depth = LDepth.L1_PERFORMATIVE

    return AuthenticityScore(
        l_depth=l_depth,
        liwc_authenticity_proxy=round(authenticity_proxy, 3),
        self_reference_density=round(self_ref_density, 3),
        temporal_context=temporal_context,
    )
