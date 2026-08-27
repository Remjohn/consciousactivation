"""
Coping Trajectory Scorer — Audience Extraction Module

Implements Lazarus & Folkman's Transactional Model of Stress and Coping
with computational markers for phase detection.

The SEARCH_PHASE is the highest-value detection target: it represents
peak receptivity to coaching intervention — the moment when a person
transitions from passive coping to actively seeking solutions.

Architecture: Context Premise Engine → Sub-Profile 3
Research: Coping Trajectory Staging Framework,
          Lazarus & Folkman (1984), Carver & Scheier (1994)

Detection Methods:
    1. Temporal language shift: past→present/future tense ratio
    2. Agency attribution delta: internal vs. external attribution
    3. Help-seeking behaviour markers: question patterns, advice-seeking

Pre-computation constraints:
    - No LLM calls. Regex + marker heuristics.
    - Single-text analysis (temporal trends require the aggregator).
    - Minimum 15 words for reliable scoring.

Negative Space:
    - This scorer does NOT detect clinical depression or anxiety.
    - This scorer does NOT assign diagnostic labels.
    - Phase assignment from a single text is tentative; confidence
      increases with temporal aggregation across multiple texts.
"""

import re
from backend.core.audience_trigger_models import (
    CopingTrajectoryPosition,
    CopingPhase,
)

# ─── Temporal Language Markers ───────────────────────────────────────

PAST_TENSE_MARKERS = {
    "was", "were", "had", "did", "used to", "back then",
    "last year", "years ago", "before", "previously",
    "i was", "we were", "it was", "they were",
    "couldn't", "wouldn't", "didn't", "hadn't",
}

PRESENT_TENSE_MARKERS = {
    "am", "is", "are", "right now", "currently", "today",
    "these days", "lately", "at the moment", "i'm",
    "i am", "we are", "it is", "i feel",
}

FUTURE_TENSE_MARKERS = {
    "will", "going to", "plan to", "intend to", "want to",
    "hope to", "looking forward", "next year", "someday",
    "one day", "eventually", "soon", "tomorrow", "gonna",
    "i'll", "we'll", "it'll", "shall",
}

# ─── Agency Attribution Markers ──────────────────────────────────────

INTERNAL_AGENCY = {
    "i decided", "i chose", "i realized", "my choice", "my decision",
    "i took", "i made", "i started", "i stopped", "i changed",
    "i'm going to", "i can", "i will", "it's up to me",
    "i built", "i created", "i learned", "i figured out",
    "my fault", "my responsibility", "i own",
}

EXTERNAL_AGENCY = {
    "it happened", "they made me", "i had no choice",
    "forced to", "couldn't help it", "nothing i can do",
    "out of my control", "it's not my fault", "he made", "she made",
    "the system", "they won't let", "life just", "fate",
    "unlucky", "no option", "stuck", "trapped", "powerless",
}

# ─── Search Phase / Help-Seeking Markers ─────────────────────────────

SEARCH_PHASE_MARKERS = {
    "has anyone", "does anyone", "can someone", "how do you",
    "what should i", "any advice", "any tips", "looking for",
    "seeking", "searching for", "trying to find", "where can i",
    "recommend", "suggestion", "help me", "need help",
    "first time", "new to this", "beginner", "just started",
    "considering", "thinking about", "exploring", "researching",
    "should i", "is it worth", "what's the best",
}

# ─── Pre-contemplation / Passive Markers ─────────────────────────────

PASSIVE_COPING_MARKERS = {
    "whatever", "don't care", "doesn't matter", "who cares",
    "nothing works", "what's the point", "given up", "resigned",
    "it is what it is", "can't change", "always been this way",
    "too late", "no use", "why bother", "same old",
}

# ─── Active Coping / Action Markers ──────────────────────────────────

ACTIVE_COPING_MARKERS = {
    "i've been doing", "i started", "so far", "progress",
    "working on", "getting better", "improving", "making changes",
    "step by step", "one day at a time", "small wins",
    "accountability", "tracking", "measuring", "routine",
    "committed to", "dedicated to", "practicing",
}

MIN_WORD_COUNT = 15


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


def score_coping_trajectory(text: str) -> CopingTrajectoryPosition:
    """
    Scores text for coping trajectory phase position.

    Analyzes temporal language orientation, agency attribution patterns,
    and help-seeking behaviour to determine coping phase.

    Args:
        text: Raw audience text to analyze.

    Returns:
        CopingTrajectoryPosition with phase and confidence.
    """
    tokens = _tokenize(text)
    text_lower = text.lower()
    word_count = len(tokens)

    if word_count < MIN_WORD_COUNT:
        return CopingTrajectoryPosition()

    # ── Temporal Language Shift ──
    past_count = _count_markers(tokens, text_lower, PAST_TENSE_MARKERS)
    present_count = _count_markers(tokens, text_lower, PRESENT_TENSE_MARKERS)
    future_count = _count_markers(tokens, text_lower, FUTURE_TENSE_MARKERS)

    total_temporal = past_count + present_count + future_count
    if total_temporal > 0:
        # -1 = fully past, +1 = fully future
        temporal_shift = ((present_count + future_count) - past_count) / total_temporal
    else:
        temporal_shift = 0.0

    # ── Agency Attribution Delta ──
    internal_count = _count_markers(tokens, text_lower, INTERNAL_AGENCY)
    external_count = _count_markers(tokens, text_lower, EXTERNAL_AGENCY)

    total_agency = internal_count + external_count
    if total_agency > 0:
        agency_delta = (internal_count - external_count) / total_agency
    else:
        agency_delta = 0.0

    # ── Phase Detection ──
    search_hits = _count_markers(tokens, text_lower, SEARCH_PHASE_MARKERS)
    passive_hits = _count_markers(tokens, text_lower, PASSIVE_COPING_MARKERS)
    active_hits = _count_markers(tokens, text_lower, ACTIVE_COPING_MARKERS)

    # Scoring: which phase has the strongest signal?
    phase_scores = {
        CopingPhase.PRE_CONTEMPLATION: passive_hits * 1.5,  # Weighted higher — harder to detect
        CopingPhase.SEARCH_PHASE: search_hits * 2.0,  # Weighted highest — most valuable
        CopingPhase.ACTIVE_COPING: active_hits * 1.0,
        CopingPhase.MAINTENANCE: 0.0,  # Cannot detect from single text
    }

    # Additional: if temporal_shift is positive AND agency_delta is rising,
    # boost search phase score (search phase = shift from past to future + seeking)
    if temporal_shift > 0.0 and agency_delta > -0.3:
        phase_scores[CopingPhase.SEARCH_PHASE] += search_hits * 0.5

    best_phase = max(phase_scores, key=phase_scores.get)
    max_score = phase_scores[best_phase]

    # Compute search phase confidence
    total_phase_signal = sum(phase_scores.values())
    if total_phase_signal > 0 and best_phase == CopingPhase.SEARCH_PHASE:
        search_confidence = min(1.0, phase_scores[CopingPhase.SEARCH_PHASE] / total_phase_signal)
    elif search_hits > 0:
        search_confidence = min(1.0, search_hits / max(total_phase_signal, 1))
    else:
        search_confidence = 0.0

    # Default to PRE_CONTEMPLATION if no signal at all
    if max_score == 0:
        best_phase = CopingPhase.PRE_CONTEMPLATION

    return CopingTrajectoryPosition(
        phase=best_phase,
        temporal_language_shift=round(temporal_shift, 3),
        agency_attribution_delta=round(agency_delta, 3),
        search_phase_confidence=round(search_confidence, 3),
    )
