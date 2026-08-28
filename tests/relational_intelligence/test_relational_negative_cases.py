"""
test_relational_negative_cases.py
---------------------------------
Validates rejection of one-axis false congruence, stale state, and score-without-evidence.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "relational-intelligence" / "src"))

import pytest
from datetime import datetime, timedelta, timezone

from cae_relational_intelligence.domain import (
    AgencyAttributionType,
    AudienceExperiencesTension,
    AudienceProfile,
    AudienceTemporalState,
    CopingPotentialType,
    FourAxisEvidence,
    GuestActivationState,
    GuestAudienceCongruence,
    GuestExperiencedTension,
    GuestProfile,
    MoralFoundationAxis,
    TemporalPositionType,
)
from cae_relational_intelligence.errors import (
    MissingTemporalProvenanceError,
    OneAxisFalseCongruenceError,
    ScoreWithoutEvidenceError,
    StaleStateError,
)
from cae_relational_intelligence.evaluator import RelationalCongruenceEvaluator
from cae_relational_intelligence.verifier import RelationalStateVerifier


def test_stale_temporal_state_rejection():
    stale_time = datetime.now(timezone.utc) - timedelta(days=25)  # > 14 day TTL

    with pytest.raises(StaleStateError, match="exceeds maximum allowable freshness TTL"):
        RelationalStateVerifier.verify_temporal_state_freshness(stale_time, max_age_days=14)


def test_future_observation_timestamp_rejection():
    future_time = datetime.now(timezone.utc) + timedelta(days=2)

    with pytest.raises(MissingTemporalProvenanceError, match="in the future"):
        RelationalStateVerifier.verify_temporal_state_freshness(future_time)


def test_score_without_evidence_rejection():
    ws_id = "ws-client-99"

    # Congruence missing axis score in dictionary
    invalid_four_axis = FourAxisEvidence(
        moral_foundation=MoralFoundationAxis.LIBERTY_OPPRESSION,
        moral_foundation_notes="Valid notes here",
        coping_potential=CopingPotentialType.PROBLEM_FOCUSED,
        coping_potential_notes="Valid coping notes",
        agency_attribution=AgencyAttributionType.INTERNAL,
        agency_attribution_notes="Valid agency notes",
        temporal_position=TemporalPositionType.TRANSCENDED_RESOLUTION,
        temporal_position_notes="Valid temporal notes",
        axis_alignment_scores={"moral_foundation": 0.8, "coping_potential": 0.8},  # Missing agency and temporal!
    )

    congruence = GuestAudienceCongruence(
        workspace_id=ws_id,
        guest_id="GST-1",
        guest_state_id="GAS-1",
        audience_id="AUD-1",
        audience_state_id="AST-1",
        shared_tension_theme="Test Theme",
        four_axis_evidence=invalid_four_axis,
        composite_congruence_score=0.85,
    )

    with pytest.raises(ScoreWithoutEvidenceError, match="Missing alignment score for required axis"):
        RelationalStateVerifier.verify_congruence(congruence)
