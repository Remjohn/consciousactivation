"""
test_temporal_state_and_provenance.py
-------------------------------------
Tests separation between persistent identity profiles and dynamic temporal states.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "relational-intelligence" / "src"))

from datetime import datetime, timezone
from cae_relational_intelligence.domain import (
    AudienceProfile,
    AudienceTemporalState,
)
from cae_relational_intelligence.verifier import RelationalStateVerifier


def test_audience_temporal_state_transitions():
    ws_id = "ws-client-99"
    audience = AudienceProfile(
        workspace_id=ws_id,
        persona_name="Early Career Founders",
    )

    # State 1: Anxious / Low Capacity (e.g. Q1 Market Downturn)
    t1 = datetime(2026, 8, 20, 10, 0, tzinfo=timezone.utc)
    state_1 = AudienceTemporalState(
        workspace_id=ws_id,
        audience_id=audience.audience_id,
        observed_at=t1,
        affective_state="Acute Anxiety",
        semantic_frame="Survival & Runway",
        media_motive="Validation & Reassurance",
        capacity_level="LOW",
        active_tensions=["Cash burn vs Team loyalty"],
        evidence_refs=["slack_community_poll_aug20"],
    )

    # State 2: Integrative / High Capacity (e.g. Post-Funding)
    t2 = datetime(2026, 8, 26, 14, 0, tzinfo=timezone.utc)
    state_2 = AudienceTemporalState(
        workspace_id=ws_id,
        audience_id=audience.audience_id,
        observed_at=t2,
        affective_state="Cautious Optimism",
        semantic_frame="Strategic Architecture",
        media_motive="Deep Mastery",
        capacity_level="HIGH",
        active_tensions=["Product excellence vs Scale speed"],
        evidence_refs=["customer_interview_aug26"],
    )

    assert state_1.state_id != state_2.state_id
    assert state_1.audience_id == state_2.audience_id == audience.audience_id
    assert state_1.capacity_level == "LOW"
    assert state_2.capacity_level == "HIGH"

    assert RelationalStateVerifier.verify_temporal_state_freshness(state_2.observed_at) is True
