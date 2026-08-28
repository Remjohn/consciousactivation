"""
test_workspace_isolation_and_anti_merge.py
------------------------------------------
Tests workspace tenant containment and anti-identity merge protections.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "relational-intelligence" / "src"))

import pytest
from datetime import datetime, timezone

from cae_relational_intelligence.domain import (
    AudienceExperiencesTension,
    AudienceProfile,
    AudienceTemporalState,
    CopingPotentialType,
    GuestActivationState,
    GuestExperiencedTension,
    GuestProfile,
    MoralFoundationAxis,
)
from cae_relational_intelligence.errors import (
    IdentityMergeForbiddenError,
    TenantLeakageError,
)
from cae_relational_intelligence.evaluator import RelationalCongruenceEvaluator
from cae_relational_intelligence.verifier import RelationalStateVerifier


def test_cross_workspace_leakage_rejection():
    now = datetime.now(timezone.utc)

    # Audience in Workspace A
    aud = AudienceProfile(workspace_id="ws-tenant-alpha", persona_name="Founders A")
    aud_st = AudienceTemporalState(
        workspace_id="ws-tenant-alpha",
        audience_id=aud.audience_id,
        observed_at=now,
        affective_state="Anxious",
        semantic_frame="Runway and survival",
        media_motive="Validation and support",
    )
    aud_ten = AudienceExperiencesTension(
        workspace_id="ws-tenant-alpha",
        audience_id=aud.audience_id,
        tension_label="Runway Anxiety",
        moral_foundation=MoralFoundationAxis.LIBERTY_OPPRESSION,
        current_coping=CopingPotentialType.PROBLEM_FOCUSED,
        urgency_score=0.90,
        evidence_citation="Discord survey cohort Q3-2026",
    )

    # Guest in Workspace B
    gst = GuestProfile(workspace_id="ws-tenant-beta", full_name="Guest B")
    gst_st = GuestActivationState(
        workspace_id="ws-tenant-beta",
        guest_id=gst.guest_id,
        observed_at=now,
        current_arousal=0.50,
    )
    gst_ten = GuestExperiencedTension(
        workspace_id="ws-tenant-beta",
        guest_id=gst.guest_id,
        tension_label="Runway Anxiety",
        moral_foundation=MoralFoundationAxis.LIBERTY_OPPRESSION,
        coping_type=CopingPotentialType.PROBLEM_FOCUSED,
        lived_proof_citation="Bootstrapped SaaS to profitability in 2020",
    )

    # Cross-tenant evaluation must raise TenantLeakageError
    with pytest.raises(TenantLeakageError, match="Workspace mismatch"):
        RelationalCongruenceEvaluator.evaluate(
            audience_profile=aud,
            audience_state=aud_st,
            audience_tension=aud_ten,
            guest_profile=gst,
            guest_state=gst_st,
            guest_tension=gst_ten,
            shared_theme="Survival",
        )


def test_same_email_cross_workspace_identity_merge_rejection():
    # Two distinct guests in two different workspaces with identical email addresses
    shared_email = "expert@stanford.edu"

    guest_tenant_1 = GuestProfile(
        workspace_id="ws-tenant-1",
        full_name="Prof. Marcus",
        email=shared_email,
    )

    guest_tenant_2 = GuestProfile(
        workspace_id="ws-tenant-2",
        full_name="Prof. Marcus",
        email=shared_email,
    )

    # Verifier must reject automatic merge attempt
    with pytest.raises(IdentityMergeForbiddenError, match="Cross-workspace identity merge attempt rejected"):
        RelationalStateVerifier.assert_no_identity_merging(guest_tenant_1, guest_tenant_2)
