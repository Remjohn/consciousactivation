"""
Moral Emotion Scorer — Audience Extraction Module

Implements the Convergence Matrix: reverse-engineers Moral Foundation
violations from moral emotion linguistic signatures.

Pipeline:
    Text → Moral Emotion Detection (indignation, compassion, contempt, disgust)
    → Appraisal Profile (Scherer CPM: relevance, goal_conduciveness,
       coping_potential, normative_significance)
    → Foundation Inversion (emotion → violated foundation)
    → Weighted MFT Vector {foundation: intensity}

Architecture: Context Premise Engine → Sub-Profile 2
Research: Haidt MFT (2012), Tangney moral emotions (2007),
          Scherer CPM (2001), LIWC psychological distancing (Pennebaker)

Pre-computation constraints:
    - No LLM calls. Two-stage marker-based heuristic.
    - Psychological distancing is the primary differentiating feature
      between closely related moral emotions (indignation vs. contempt).
    - Uses pronoun ratios and cognitive complexity as open-source LIWC proxies.

Negative Space:
    - This scorer does NOT perform sentiment analysis.
    - This scorer does NOT detect non-moral emotions (surprise, basic fear).
    - The output is NOT a boolean tag. It is a continuous weighted vector.
"""

import re
from backend.core.audience_trigger_models import MoralEmotionProfile

# ─── Moral Emotion Marker Dictionaries ───────────────────────────────

# INDIGNATION / RESENTMENT → Fairness/Cheating foundation
# Characterized by: high coping potential, high cognitive load,
# first-person immediacy, causal reasoning
INDIGNATION_MARKERS = {
    "unfair", "unjust", "inequality", "exploited", "cheated",
    "rigged", "unequal", "biased", "corrupt", "stolen",
    "deserve", "deserved", "entitled", "rights", "justice",
    "should have", "ought to", "not right", "wrong",
    "how dare", "unacceptable", "inexcusable", "outrageous",
    "because", "therefore", "consequently", "thus",
}

# COMPASSION / EMPATHIC DISTRESS → Care/Harm foundation
# Characterized by: vicarious goal obstruction, "we" pronouns,
# social process words, feeling-state vocabulary
COMPASSION_MARKERS = {
    "suffering", "pain", "hurt", "vulnerable", "innocent",
    "victim", "helpless", "defenseless", "neglected", "abandoned",
    "compassion", "empathy", "sympathy", "heartbreaking",
    "tragic", "devastating", "sorrowful", "pity",
    "we need to", "we should", "help them", "protect them",
    "care about", "concern for", "worried about",
}

# CONTEMPT / OUTRAGE → Loyalty/Authority foundation
# Characterized by: low coping potential, third-person distancing,
# social exclusion language, settled hierarchical judgments
CONTEMPT_MARKERS = {
    "traitor", "betrayed", "betrayal", "turncoat", "disloyal",
    "ungrateful", "pathetic", "worthless", "incompetent",
    "beneath", "laughable", "ridiculous", "embarrassing",
    "they don't deserve", "they should be", "those people",
    "sellout", "hypocrite", "coward", "weak",
    "disgraceful", "shameful", "unworthy", "sneer",
}

# DISGUST / REVULSION → Sanctity/Degradation foundation
# Characterized by: somatic vocabulary, extreme distancing,
# low cognitive processing, purity/contamination language
DISGUST_MARKERS = {
    "disgusting", "revolting", "repulsive", "vile", "sickening",
    "nauseating", "abhorrent", "filthy", "contaminated", "toxic",
    "polluted", "tainted", "degrading", "perverted", "unnatural",
    "depraved", "profane", "desecrated", "impure", "obscene",
    "gross", "stomach-turning", "putrid", "rotten",
}

# ─── Psychological Distancing Markers ────────────────────────────────

FIRST_PERSON_SINGULAR = {"i", "me", "my", "mine", "myself"}
FIRST_PERSON_PLURAL = {"we", "us", "our", "ours", "ourselves"}
THIRD_PERSON = {"they", "them", "their", "theirs", "those", "these people", "he", "she", "it"}
COGNITIVE_CAUSAL = {"because", "therefore", "since", "thus", "consequently", "hence", "so that", "due to"}
SOMATIC_WORDS = {"stomach", "sick", "nauseous", "vomit", "gag", "shudder", "cringe", "skin crawl", "flesh"}


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


def _compute_appraisal_profile(tokens: list[str], text_lower: str) -> dict[str, float]:
    """
    Approximates Scherer's 4 Stimulus Evaluation Checks using
    linguistic proxies.
    """
    word_count = max(len(tokens), 1)

    # Relevance: presence of any moral markers indicates relevance
    # Approximated by exclamation marks + intensity modifiers
    intensity_markers = {"very", "extremely", "absolutely", "completely", "totally", "utterly"}
    exclamation_count = text_lower.count("!")
    intensity_count = _count_markers(tokens, text_lower, intensity_markers)
    relevance = min(1.0, (exclamation_count + intensity_count) / max(word_count * 0.05, 1))

    # Goal conduciveness: negative = obstructive, approximated by negative emotion density
    neg_markers = {"not", "never", "no", "can't", "won't", "don't", "shouldn't", "isn't", "aren't"}
    neg_count = _count_markers(tokens, text_lower, neg_markers)
    goal_conduciveness = min(1.0, neg_count / max(word_count * 0.1, 1))

    # Coping potential: high first-person + causal words = high coping
    fp_count = _count_markers(tokens, text_lower, FIRST_PERSON_SINGULAR)
    causal_count = _count_markers(tokens, text_lower, COGNITIVE_CAUSAL)
    coping_potential = min(1.0, ((fp_count + causal_count) / max(word_count * 0.1, 1)))

    # Normative significance: presence of moral vocabulary
    norm_markers = {"should", "ought", "right", "wrong", "fair", "just", "moral", "ethical", "duty"}
    norm_count = _count_markers(tokens, text_lower, norm_markers)
    normative_significance = min(1.0, norm_count / max(word_count * 0.05, 1))

    return {
        "relevance": round(relevance, 3),
        "goal_conduciveness": round(goal_conduciveness, 3),
        "coping_potential": round(coping_potential, 3),
        "normative_significance": round(normative_significance, 3),
    }


def score_moral_emotion(text: str) -> MoralEmotionProfile:
    """
    Scores text for moral emotion signatures and reverse-engineers
    the violated Moral Foundation.

    Two-stage process:
    1. Detect moral emotion family via marker matching
    2. Weight foundation scores by intensity (marker density + modifiers)

    Args:
        text: Raw audience text to analyze.

    Returns:
        MoralEmotionProfile with weighted foundation vector.
    """
    tokens = _tokenize(text)
    text_lower = text.lower()
    word_count = len(tokens)

    if word_count < 10:
        return MoralEmotionProfile()

    # Stage 1: Detect moral emotion families
    indignation_hits = _count_markers(tokens, text_lower, INDIGNATION_MARKERS)
    compassion_hits = _count_markers(tokens, text_lower, COMPASSION_MARKERS)
    contempt_hits = _count_markers(tokens, text_lower, CONTEMPT_MARKERS)
    disgust_hits = _count_markers(tokens, text_lower, DISGUST_MARKERS)

    total_moral_hits = indignation_hits + compassion_hits + contempt_hits + disgust_hits

    if total_moral_hits == 0:
        return MoralEmotionProfile(
            appraisal_profile=_compute_appraisal_profile(tokens, text_lower)
        )

    # Stage 2: Compute foundation weights
    # Each emotion maps to its convergence matrix foundation
    raw_weights = {
        "care_harm": compassion_hits,
        "fairness_cheating": indignation_hits,
        "loyalty_betrayal": contempt_hits * 0.6,  # Contempt splits between loyalty and authority
        "authority_subversion": contempt_hits * 0.4,
        "sanctity_degradation": disgust_hits,
        "liberty_oppression": indignation_hits * 0.3,  # Liberty overlaps with fairness
    }

    # Normalize to sum ≈ 1.0
    total_weight = sum(raw_weights.values())
    if total_weight > 0:
        foundation_weights = {k: round(v / total_weight, 3) for k, v in raw_weights.items()}
    else:
        foundation_weights = {k: 0.0 for k in raw_weights}

    # Determine dominant emotion
    emotion_scores = {
        "indignation": indignation_hits,
        "compassion": compassion_hits,
        "contempt": contempt_hits,
        "disgust": disgust_hits,
    }
    dominant_emotion = max(emotion_scores, key=emotion_scores.get) if total_moral_hits > 0 else None

    # Compute appraisal profile
    appraisal = _compute_appraisal_profile(tokens, text_lower)

    return MoralEmotionProfile(
        foundation_weights=foundation_weights,
        dominant_emotion=dominant_emotion,
        appraisal_profile=appraisal,
    )
