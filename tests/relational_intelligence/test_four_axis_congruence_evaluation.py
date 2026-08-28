"""
test_four_axis_congruence_evaluation.py
---------------------------------------
Tests 4-axis multi-dimensional congruence evaluation between Audience and Guest.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "relational-intelligence" / "src"))

from datetime import datetime, timezone
from cae_relational_intelligence.domain import (
    AgencyAttributionType,
    AudienceExperiencesTension,
    AudienceProfile,
    AudienceTemporalState,
    CopingPotentialType,
    GuestActivationState,
    GuestExperiencedTension,
    GuestProfile,
    MoralFoundationAxis,
    TemporalPositionType,
)
from cae_relational_intelligence.evaluator import RelationalCongruenceEvaluator
from cae_relational_intelligence.verifier import RelationalStateVerifier


def test_four_axis_successful_congruence():
    ws_id = "ws-client-99"
    now = datetime.now(timezone.utc)

    audience = AudienceProfile(workspace_id=ws_id, persona_name="Tech Leaders")
    aud_state = AudienceTemporalState(
        workspace_id=ws_id,
        audience_id=audience.audience_id,
        observed_at=now,
        affective_state="Overwhelmed",
        semantic_frame="Exhaustion",
        media_motive="Actionable Clarity",
    )
    aud_tension = AudienceExperiencesTension(
        workspace_id=ws_id,
        audience_id=audience.audience_id,
        tension_label="Burnout vs High Output",
        moral_foundation=MoralFoundationAxis.CARE_HARM,
        current_coping=CopingPotentialType.HELPLESSNESS,
        urgency_score=0.88,
        evidence_citation="Discord survey Q3-2026",
    )

    guest = GuestProfile(workspace_id=ws_id, full_name="Dr. Elena Rostova")
    guest_state = GuestActivationState(
        workspace_id=ws_id,
        guest_id=guest.guest_id,
        observed_at=now,
        current_arousal=0.70,
    )
    guest_tension = GuestExperiencedTension(
        workspace_id=ws_id,
        guest_id=guest.guest_id,
        tension_label="Burnout vs High Output",
        moral_foundation=MoralFoundationAxis.CARE_HARM,
        coping_type=CopingPotentialType.PROBLEM_FOCUSED,
        lived_proof_citation="10 years running high-stress neuro-ICU",
        was_resolved=True,
    )

    congruence = RelationalCongruenceEvaluator.evaluate(
        audience_profile=audience,
        audience_state=aud_state,
        audience_tension=aud_tension,
        guest_profile=guest,
        guest_state=guest_state,
        guest_tension=guest_tension,
        shared_theme="Sustainable High-Performance Under Pressure",
        agency_attribution=AgencyAttributionType.INTERNAL,
        guest_temporal_pos=TemporalPositionType.TRANSCENDED_RESOLUTION,
    )

    assert congruence.workspace_id == ws_id
    assert congruence.composite_congruence_score >= 0.80
    assert congruence.four_axis_evidence.moral_foundation == MoralFoundationAxis.CARE_HARM
    assert congruence.four_axis_evidence.coping_potential == CopingPotentialType.PROBLEM_FOCUSED
    assert congruence.four_axis_evidence.temporal_position == TemporalPositionType.TRANSCENDED_RESOLUTION

    assert RelationalStateVerifier.verify_congruence(
        congruence,
        audience_state=aud_state,
        guest_state=guest_state,
    ) is True
