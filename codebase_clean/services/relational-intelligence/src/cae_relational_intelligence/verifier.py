"""
verifier.py
-----------
Gating and verification logic for Relational Intelligence (CAE-M02).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from .domain import (
    AudienceProfile,
    AudienceTemporalState,
    GuestActivationState,
    GuestAudienceCongruence,
    GuestProfile,
)
from .errors import (
    IdentityMergeForbiddenError,
    MissingTemporalProvenanceError,
    ScoreWithoutEvidenceError,
    StaleStateError,
    TenantLeakageError,
)


class RelationalStateVerifier:
    """Enforces constitutional invariants on Relational Intelligence states and congruences."""

    DEFAULT_TEMPORAL_STATE_MAX_AGE_DAYS = 14

    @classmethod
    def verify_temporal_state_freshness(
        cls,
        observed_at: datetime,
        *,
        max_age_days: int = DEFAULT_TEMPORAL_STATE_MAX_AGE_DAYS,
        current_time: Optional[datetime] = None,
    ) -> bool:
        """Enforces that dynamic temporal states do not exceed TTL without explicit refresh."""
        now = current_time or datetime.now(timezone.utc)
        if observed_at > now + timedelta(hours=1):
            raise MissingTemporalProvenanceError(f"Observation timestamp {observed_at} is in the future relative to {now}.")
            
        age = now - observed_at
        if age > timedelta(days=max_age_days):
            raise StaleStateError(f"Temporal state age ({age.days} days) exceeds maximum allowable freshness TTL of {max_age_days} days.")
        return True

    @classmethod
    def verify_congruence(
        cls,
        congruence: GuestAudienceCongruence,
        *,
        audience_state: Optional[AudienceTemporalState] = None,
        guest_state: Optional[GuestActivationState] = None,
        current_time: Optional[datetime] = None,
    ) -> bool:
        """Validates a GuestAudienceCongruence object against all constitutional constraints."""
        # 1. 4-Axis Evidence Verification
        ev = congruence.four_axis_evidence
        if not ev:
            raise ScoreWithoutEvidenceError("GuestAudienceCongruence has no 4-axis evidence attached.")

        for axis_name in ["moral_foundation", "coping_potential", "agency_attribution", "temporal_position"]:
            if axis_name not in ev.axis_alignment_scores:
                raise ScoreWithoutEvidenceError(f"Missing alignment score for required axis: {axis_name}")
            notes_field = f"{axis_name}_notes"
            notes_val = getattr(ev, notes_field, "")
            if not notes_val or len(notes_val.strip()) < 5:
                raise ScoreWithoutEvidenceError(f"Missing or insufficient evidence notes for axis: {axis_name}")

        # 2. Freshness check on attached states
        if audience_state:
            cls.verify_temporal_state_freshness(audience_state.observed_at, current_time=current_time)
            if audience_state.workspace_id != congruence.workspace_id:
                raise TenantLeakageError("Audience state workspace does not match congruence workspace.")

        if guest_state:
            cls.verify_temporal_state_freshness(guest_state.observed_at, current_time=current_time)
            if guest_state.workspace_id != congruence.workspace_id:
                raise TenantLeakageError("Guest state workspace does not match congruence workspace.")

        return True

    @classmethod
    def assert_no_identity_merging(
        cls,
        guest_a: GuestProfile,
        guest_b: GuestProfile,
    ) -> None:
        """
        Anti-Merge Guard: Forbids automatic identity merging across distinct guest records,
        especially when located in different workspaces, even if names or emails match.
        """
        if guest_a.guest_id != guest_b.guest_id:
            if guest_a.workspace_id != guest_b.workspace_id:
                # Same email across workspaces cannot be unified
                if guest_a.email and guest_b.email and guest_a.email.lower() == guest_b.email.lower():
                    raise IdentityMergeForbiddenError(
                        f"Cross-workspace identity merge attempt rejected: Guest '{guest_a.guest_id}' (WS: {guest_a.workspace_id}) "
                        f"and Guest '{guest_b.guest_id}' (WS: {guest_b.workspace_id}) share email '{guest_a.email}', but must remain distinct per CA-CAN-01B."
                    )
