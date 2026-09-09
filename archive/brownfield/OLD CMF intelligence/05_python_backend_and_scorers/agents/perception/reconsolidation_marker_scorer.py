"""
Reconsolidation Marker Scorer — Audience Extraction Module

Implements the neurobiology of content "hits": detects markers of
memory reconsolidation potential from audience text.

Key insight: prediction error is the gateway to memory reconsolidation.
Content that violates audience expectations creates a labilization
window where existing schemas can be updated. High prediction-error
sensitivity + high save/low share = audience primed for deep impact.

Architecture: Context Premise Engine → Sub-Profile 5
Research: Audience Reconsolidation and Content Impact,
          Nader et al. (2000), Lane et al. (2015),
          Audience Appraisal Profiling Framework

Pre-computation constraints:
    - No LLM calls. Marker-based heuristics.
    - Save/share ratio is a proxy — true measurement requires engagement data.
    - Neural coupling proxy uses narrative mirroring markers.

Negative Space:
    - This scorer does NOT measure actual memory reconsolidation.
    - It detects LINGUISTIC MARKERS of reconsolidation readiness.
    - High prediction error sensitivity does NOT mean the person is gullible.
      It means their existing schemas are in active revision.
"""

import re
from backend.core.audience_trigger_models import ReconsolidationMarkers

# ─── Prediction Error Markers ────────────────────────────────────────
# Evidence of expectation violation — the gateway to labilization.
# These markers indicate the person's existing schema is being challenged.

PREDICTION_ERROR_MARKERS = {
    # Surprise / dissonance
    "i never thought", "i never realized", "wait what",
    "that changes everything", "mind blown", "blew my mind",
    "i had no idea", "this is not what i expected",
    "i was wrong", "i've been wrong", "turns out",
    # Schema revision
    "i used to think", "but now i see", "now i understand",
    "everything i believed", "completely different",
    "paradigm shift", "eye opening", "eye-opening",
    "game changer", "game-changer", "aha moment",
    # Cognitive dissonance
    "wait", "hold on", "but that means", "how is that possible",
    "that can't be right", "contradicts", "conflicts with",
    "on the other hand", "i'm confused but",
}

# ─── Save-Intent Markers ────────────────────────────────────────────
# Language indicating deep processing and desire to retain.
# Save-intent = private, reflective engagement.

SAVE_INTENT_MARKERS = {
    "need to remember", "saving this", "bookmarking", "bookmark",
    "going to come back to", "write this down", "noting this",
    "this is important", "need to think about",
    "let me sit with this", "need to process",
    "screenshot", "saved", "pinned",
    "coming back to this", "reference", "keep this",
}

# ─── Share-Intent Markers ────────────────────────────────────────────
# Language indicating social broadcasting desire.
# Share-intent = public, status-signaling engagement.

SHARE_INTENT_MARKERS = {
    "everyone needs to see", "everyone should know",
    "tagging", "sending this to", "sharing this",
    "you need to see this", "check this out",
    "repost", "retweet", "forwarding",
    "so true", "preach", "say it louder",
    "finally someone says it", "this right here",
}

# ─── Neural Coupling / Narrative Mirroring Markers ───────────────────
# Evidence of speaker-listener coupling: the audience mirrors the
# creator's narrative structure, indicating deep encoding.

COUPLING_MARKERS = {
    # Narrative mirroring (audience adopts creator's framing)
    "exactly how i feel", "you put it into words",
    "this is my story", "are you me", "literally me",
    "i felt that", "same", "this hit different",
    "you described", "you captured", "you nailed",
    # Temporal alignment (audience syncs with narrative timeline)
    "i was just thinking about this", "perfect timing",
    "i needed to hear this", "right when i needed it",
}

# ─── Parasocial Engagement Markers ───────────────────────────────────
# One-directional relational investment with content creator.

PARASOCIAL_MARKERS = {
    # Direct address to creator
    "you always", "you never fail", "you're the only one",
    "i feel like you understand", "you get me",
    "i trust you", "you've helped me so much",
    # Relational investment
    "been following you", "loyal fan", "since day one",
    "never miss", "always watch", "always listen",
    "part of my routine", "can't start my day without",
}

MIN_WORD_COUNT = 10


def _tokenize(text: str) -> list[str]:
    return re.findall(r'\b[a-z\']+\b', text.lower())


def _count_markers(tokens: list[str], text_lower: str, markers: set) -> int:
    count = 0
    for marker in markers:
        if " " in marker:
            count += text_lower.count(marker)
        else:
            count += tokens.count(marker)
    return count


def score_reconsolidation_markers(text: str) -> ReconsolidationMarkers:
    """
    Scores text for memory reconsolidation readiness markers.

    Four dimensions:
    1. Prediction error sensitivity: expectation violation markers
    2. Save/share ratio: deep vs. surface engagement proxy
    3. Neural coupling proxy: narrative mirroring markers
    4. Parasocial engagement: one-directional relational investment

    Args:
        text: Raw audience text to analyze.

    Returns:
        ReconsolidationMarkers with all four dimensions.
    """
    tokens = _tokenize(text)
    text_lower = text.lower()
    word_count = len(tokens)

    if word_count < MIN_WORD_COUNT:
        return ReconsolidationMarkers()

    # Prediction Error Sensitivity
    pe_hits = _count_markers(tokens, text_lower, PREDICTION_ERROR_MARKERS)
    pe_score = min(1.0, pe_hits / max(word_count * 0.03, 1))

    # Save/Share Ratio
    save_hits = _count_markers(tokens, text_lower, SAVE_INTENT_MARKERS)
    share_hits = _count_markers(tokens, text_lower, SHARE_INTENT_MARKERS)
    if share_hits == 0 and save_hits == 0:
        save_share_ratio = 0.0
    elif share_hits == 0:
        save_share_ratio = min(10.0, float(save_hits))
    else:
        save_share_ratio = min(10.0, save_hits / share_hits)

    # Neural Coupling Proxy
    coupling_hits = _count_markers(tokens, text_lower, COUPLING_MARKERS)
    coupling_score = min(1.0, coupling_hits / max(word_count * 0.03, 1))

    # Parasocial Engagement
    parasocial_hits = _count_markers(tokens, text_lower, PARASOCIAL_MARKERS)
    parasocial_score = min(1.0, parasocial_hits / max(word_count * 0.03, 1))

    return ReconsolidationMarkers(
        prediction_error_sensitivity=round(pe_score, 3),
        save_share_ratio=round(save_share_ratio, 3),
        neural_coupling_proxy=round(coupling_score, 3),
        parasocial_engagement=round(parasocial_score, 3),
    )
