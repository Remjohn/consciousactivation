"""
test_relational_domain_contracts.py
-----------------------------------
Tests serialization, invariants, and typing of relational intelligence domain entities.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "relational-intelligence" / "src"))

from cae_relational_intelligence.domain import (
    AudienceProfile,
    AudienceTemporalState,
    CopingPotentialType,
    GuestActivationState,
    GuestExperiencedTension,
    GuestProfile,
    MoralFoundationAxis,
)


def test_audience_and_guest_profile_instantiation():
    ws_id = "ws-client-99"

    audience = AudienceProfile(
        workspace_id=ws_id,
        persona_name="Anxious High-Performers",
        existential_invariants=["Self-worth tied to output", "Fear of plateauing"],
        core_wounds=["Imposter vulnerability", "Burnout exhaustion"],
    )

    assert audience.audience_id.startswith("AUD-")
    assert audience.workspace_id == ws_id

    guest = GuestProfile(
        workspace_id=ws_id,
        full_name="Dr. Aris Thorne",
        email="aris@thorne-research.org",
        lived_proof_milestones=["10 years neurobiology lab director", "Recovered from severe clinical burnout in 2021"],
    )

    assert guest.guest_id.startswith("GST-")
    assert guest.workspace_id == ws_id


def test_tensions_and_activation_states():
    ws_id = "ws-client-99"
    guest_id = "GST-1234"

    tension = GuestExperiencedTension(
        workspace_id=ws_id,
        guest_id=guest_id,
        tension_label="Burnout vs Ambition",
        moral_foundation=MoralFoundationAxis.CARE_HARM,
        coping_type=CopingPotentialType.PROBLEM_FOCUSED,
        lived_proof_citation="Chapter 4 in memoir and keynote speech at Oxford 2023",
        was_resolved=True,
    )

    assert tension.relation_id.startswith("REL-GET-")
    assert tension.was_resolved is True

    activation = GuestActivationState(
        workspace_id=ws_id,
        guest_id=guest_id,
        current_arousal=0.75,
        active_vulnerability_vectors=["Fear of repeating past breakdown"],
        defended_stances=["Intellectualizing workload limits"],
    )

    assert activation.state_id.startswith("GAS-")
    assert activation.current_arousal == 0.75
