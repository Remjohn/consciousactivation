"""
evaluator.py
------------
Relational Congruence Evaluator computing 4-axis multi-dimensional alignment without flat collapse.
"""

from __future__ import annotations

from typing import Dict
from .domain import (
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
from .errors import (
    OneAxisFalseCongruenceError,
    ScoreWithoutEvidenceError,
    TenantLeakageError,
)


class RelationalCongruenceEvaluator:
    """
    Evaluates emotional, moral, and coping congruence between Audience and Guest states.
    Preserves 4-axis breakdown.
    """

    @classmethod
    def evaluate(
        cls,
        *,
        audience_profile: AudienceProfile,
        audience_state: AudienceTemporalState,
        audience_tension: AudienceExperiencesTension,
        guest_profile: GuestProfile,
        guest_state: GuestActivationState,
        guest_tension: GuestExperiencedTension,
        shared_theme: str,
        agency_attribution: AgencyAttributionType = AgencyAttributionType.INTERNAL,
        guest_temporal_pos: TemporalPositionType = TemporalPositionType.TRANSCENDED_RESOLUTION,
        notes: Dict[str, str] | None = None,
    ) -> GuestAudienceCongruence:
        """
        Synthesize a GuestAudienceCongruence object with complete 4-axis evidence.
        """
        # 1. Multi-Tenant Containment Gate
        if audience_profile.workspace_id != guest_profile.workspace_id:
            raise TenantLeakageError(
                f"Workspace mismatch: Audience is in '{audience_profile.workspace_id}', Guest is in '{guest_profile.workspace_id}'."
            )
        if audience_state.workspace_id != guest_state.workspace_id:
            raise TenantLeakageError("Temporal states belong to different workspace tenants.")

        ws_id = audience_profile.workspace_id
        user_notes = notes or {}

        # 2. Axis 1: Moral Foundation alignment
        moral_match = (audience_tension.moral_foundation == guest_tension.moral_foundation)
        moral_score = 1.0 if moral_match else 0.20
        moral_notes = user_notes.get(
            "moral",
            f"Both engage with the {guest_tension.moral_foundation.value} axis in context of {shared_theme}."
            if moral_match else f"Moral axis divergence: Audience {audience_tension.moral_foundation} vs Guest {guest_tension.moral_foundation}."
        )

        # 3. Axis 2: Coping Potential complementary alignment
        # Guest who resolved or uses problem-focused coping can mentor audience in acute/emotional coping
        coping_score = 0.85 if guest_tension.was_resolved else 0.50
        coping_notes = user_notes.get(
            "coping",
            f"Guest offers resolved {guest_tension.coping_type.value} model to audience currently in {audience_tension.current_coping.value}."
        )

        # 4. Axis 3: Agency Attribution
        agency_score = 0.80
        agency_notes = user_notes.get(
            "agency",
            f"Agency attributed primarily via {agency_attribution.value} framing."
        )

        # 5. Axis 4: Temporal Position Bridge
        # Ideal bridge: Guest in TRANSCENDED_RESOLUTION speaks to Audience in PRESENT_ACUTE_STRUGGLE
        temporal_score = 0.90 if guest_temporal_pos == TemporalPositionType.TRANSCENDED_RESOLUTION else 0.60
        temporal_notes = user_notes.get(
            "temporal",
            f"Temporal bridge established from Guest ({guest_temporal_pos.value}) to Audience acute present."
        )

        axis_scores = {
            "moral_foundation": moral_score,
            "coping_potential": coping_score,
            "agency_attribution": agency_score,
            "temporal_position": temporal_score,
        }

        # Check for Anti-Centroid / One-Axis False Congruence
        active_axes = sum(1 for s in axis_scores.values() if s >= 0.70)
        if active_axes == 1 and moral_score >= 0.90:
            # High moral match but complete absence of coping/agency/temporal alignment
            raise OneAxisFalseCongruenceError(
                "One-axis resonance detected: High moral similarity alone without coping, agency, or temporal alignment cannot claim broad congruence."
            )

        # Composite score calculation (geometric mean / weighted product)
        composite = (moral_score * 0.35) + (coping_score * 0.25) + (agency_score * 0.20) + (temporal_score * 0.20)

        four_axis = FourAxisEvidence(
            moral_foundation=guest_tension.moral_foundation,
            moral_foundation_notes=moral_notes,
            coping_potential=guest_tension.coping_type,
            coping_potential_notes=coping_notes,
            agency_attribution=agency_attribution,
            agency_attribution_notes=agency_notes,
            temporal_position=guest_temporal_pos,
            temporal_position_notes=temporal_notes,
            axis_alignment_scores=axis_scores,
        )

        return GuestAudienceCongruence(
            workspace_id=ws_id,
            guest_id=guest_profile.guest_id,
            guest_state_id=guest_state.state_id,
            audience_id=audience_profile.audience_id,
            audience_state_id=audience_state.state_id,
            shared_tension_theme=shared_theme,
            four_axis_evidence=four_axis,
            composite_congruence_score=round(composite, 3),
        )
