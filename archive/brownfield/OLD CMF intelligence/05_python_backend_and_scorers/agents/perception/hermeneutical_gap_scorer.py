"""
Hermeneutical Gap Scorer — Audience Extraction Module

Implements tri-modal testimonial smothering detection for identifying
unarticulated experience — moments where someone is trying to describe
something they don't yet have words for.

Three independent detection channels:
    1. Discourse Truncation: syntactic evidence of self-censorship
    2. Affective Parabola: emotional escalation → abrupt flattening
    3. Metaphor Novelty: non-conventional figurative language

High composite score = the individual is experiencing something they
cannot name. This is the HIGHEST-VALUE signal for content that provides
new interpretive frameworks (naming the unnamed).

Architecture: Context Premise Engine → Sub-Profile 4
Research: Detecting Hermeneutical Injustice Computationally,
          Fricker (2007), Dotson (2011), Lakoff & Johnson (1980)

Pre-computation constraints:
    - No LLM calls. Regex + token heuristics.
    - Affective parabola requires ≥3 sentences for trajectory detection.
    - Metaphor novelty is approximated via semantic anomaly heuristics.

Negative Space:
    - This scorer does NOT detect lying or deception.
    - Truncation ≠ shyness. It indicates structural inability to articulate.
    - High gap score does NOT mean the person is confused. It means
      their experience outstrips available conceptual resources.
"""

import re
from backend.core.audience_trigger_models import HermeneuticalGapProfile

# ─── Discourse Truncation Markers ────────────────────────────────────
# Syntactic truncation: evidence of self-censorship at the point of
# deepest disclosure. Phatic tokens signal communicative struggle.

TRUNCATION_MARKERS = {
    # Trailing markers (end-of-thought abandonment)
    "...", "i don't know", "it's hard to explain", "you know what i mean",
    "i can't really", "it's like", "sort of", "kind of",
    "you know", "anyway", "whatever", "i guess",
    "hard to put into words", "i don't have the words",
    "i can't describe", "words fail",
    # Phatic tokens (filled pauses indicating processing strain)
    "um", "uh", "like", "just", "basically",
    # Hedging (epistemic retreat)
    "maybe", "perhaps", "i think", "i suppose", "probably",
    "might be", "could be", "not sure", "i feel like",
}

# ─── Affective Escalation Markers ────────────────────────────────────
# Used to detect the "parabola": emotional intensity that rises
# and then abruptly flattens (self-censorship at peak disclosure).

POSITIVE_AFFECT = {
    "love", "amazing", "incredible", "beautiful", "wonderful",
    "happy", "grateful", "blessed", "thankful", "excited",
    "proud", "confident", "strong", "powerful", "free",
}

NEGATIVE_AFFECT = {
    "hate", "terrible", "horrible", "awful", "devastating",
    "angry", "furious", "heartbroken", "crushed", "destroyed",
    "miserable", "hopeless", "worthless", "disgusted", "enraged",
    "broken", "shattered", "traumatized", "violated",
}

FLATTENING_MARKERS = {
    "but anyway", "but yeah", "but whatever", "so yeah",
    "i don't know", "it's fine", "it doesn't matter",
    "never mind", "forget it", "it's not that big a deal",
    "i'm fine", "it's okay", "water under the bridge",
}

# ─── Metaphor Novelty Markers ────────────────────────────────────────
# Non-conventional figurative language that signals attempts to
# articulate experiences for which no standard vocabulary exists.
# These are structural patterns, not specific metaphors.

SIMILE_PATTERNS = [
    r'\blike\s+(?:a|an|the)\s+\w+',  # "like a _____"
    r'\bas\s+\w+\s+as\s+\w+',        # "as _____ as _____"
    r'\bfelt\s+like\s+\w+',           # "felt like _____"
]

NOVEL_FIGURATIVE_MARKERS = {
    "it's as if", "almost like", "not quite", "somewhere between",
    "a mix of", "part of me", "the other part",
    "it's this thing where", "imagine if",
    "picture this", "think of it as",
}

# ─── Weights for composite score ─────────────────────────────────────
TRUNCATION_WEIGHT = 0.40
PARABOLA_WEIGHT = 0.30
NOVELTY_WEIGHT = 0.30

MIN_WORD_COUNT = 15


def _tokenize(text: str) -> list[str]:
    return re.findall(r'\b[a-z\']+\b', text.lower())


def _count_markers(tokens: list[str], text_lower: str, markers: set) -> int:
    count = 0
    for marker in markers:
        if " " in marker:
            count += text_lower.count(marker)
        elif marker == "...":
            count += text_lower.count("...")
        else:
            count += tokens.count(marker)
    return count


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences using common delimiters."""
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]


def _score_affective_parabola(text: str) -> float:
    """
    Detects the emotional parabola pattern:
    escalation → peak → abrupt flattening.

    Returns 0-1 score indicating strength of the parabola pattern.
    """
    sentences = _split_sentences(text)
    if len(sentences) < 3:
        return 0.0

    text_lower = text.lower()
    tokens_full = _tokenize(text)

    # Check for emotional escalation
    has_negative_affect = _count_markers(tokens_full, text_lower, NEGATIVE_AFFECT) > 0
    has_positive_affect = _count_markers(tokens_full, text_lower, POSITIVE_AFFECT) > 0
    has_flattening = _count_markers(tokens_full, text_lower, FLATTENING_MARKERS) > 0

    # The parabola: high emotion followed by flattening
    if (has_negative_affect or has_positive_affect) and has_flattening:
        # Stronger signal if intense emotion precedes the flattening
        emotion_count = (
            _count_markers(tokens_full, text_lower, NEGATIVE_AFFECT) +
            _count_markers(tokens_full, text_lower, POSITIVE_AFFECT)
        )
        flattening_count = _count_markers(tokens_full, text_lower, FLATTENING_MARKERS)
        return min(1.0, (emotion_count + flattening_count) / max(len(sentences), 1))

    return 0.0


def _score_metaphor_novelty(text: str) -> float:
    """
    Detects non-conventional figurative language.

    Uses simile pattern matching + novel figurative markers as proxies
    for metaphor novelty. In production, this would upgrade to
    semantic anomaly detection via sentence-transformers.
    """
    text_lower = text.lower()
    tokens = _tokenize(text)
    word_count = max(len(tokens), 1)

    # Count simile patterns
    simile_count = 0
    for pattern in SIMILE_PATTERNS:
        simile_count += len(re.findall(pattern, text_lower))

    # Count novel figurative markers
    novel_count = _count_markers(tokens, text_lower, NOVEL_FIGURATIVE_MARKERS)

    total = simile_count + novel_count
    return min(1.0, total / max(word_count * 0.03, 1))


def score_hermeneutical_gap(text: str) -> HermeneuticalGapProfile:
    """
    Scores text for hermeneutical gap — evidence of unarticulated experience.

    Three independent channels are scored and combined with fixed weights:
    - Discourse truncation (40%): syntactic self-censorship
    - Affective parabola (30%): emotional escalation → abrupt flattening
    - Metaphor novelty (30%): non-conventional figurative language

    Args:
        text: Raw audience text to analyze.

    Returns:
        HermeneuticalGapProfile with component and composite scores.
    """
    tokens = _tokenize(text)
    text_lower = text.lower()
    word_count = len(tokens)

    if word_count < MIN_WORD_COUNT:
        return HermeneuticalGapProfile()

    # Channel 1: Discourse truncation
    trunc_hits = _count_markers(tokens, text_lower, TRUNCATION_MARKERS)
    truncation_score = min(1.0, trunc_hits / max(word_count * 0.05, 1))

    # Channel 2: Affective parabola
    parabola_score = _score_affective_parabola(text)

    # Channel 3: Metaphor novelty
    novelty_score = _score_metaphor_novelty(text)

    # Composite
    composite = (
        TRUNCATION_WEIGHT * truncation_score +
        PARABOLA_WEIGHT * parabola_score +
        NOVELTY_WEIGHT * novelty_score
    )

    return HermeneuticalGapProfile(
        discourse_truncation_score=round(truncation_score, 3),
        affective_parabola_score=round(parabola_score, 3),
        metaphor_novelty_score=round(novelty_score, 3),
        composite_gap_score=round(composite, 3),
    )
