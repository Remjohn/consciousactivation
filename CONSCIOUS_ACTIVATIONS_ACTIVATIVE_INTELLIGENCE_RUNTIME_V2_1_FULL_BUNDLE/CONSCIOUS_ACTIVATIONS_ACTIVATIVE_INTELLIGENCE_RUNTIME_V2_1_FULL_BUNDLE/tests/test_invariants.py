from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys
import unittest

from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reference_implementation"))

from activative_intelligence_v2.lifecycle import (  # noqa: E402
    InvalidLifecycleTransition,
    require_transition,
)
from activative_intelligence_v2.models import (  # noqa: E402
    ActivationDirection,
    ActivationDomain,
    ActivationEvaluationReceipt,
    AdmissionMode,
    CampaignActivationProgram,
    CampaignAssetPlan,
    CanonicalInterviewSourcePackage,
    EpistemicState,
    ExpressionMoment,
    ExpressionMomentState,
    ImmutableRef,
    LifecycleState,
)


def ref(name: str) -> ImmutableRef:
    import hashlib
    return ImmutableRef(
        object_id=name,
        version="1.0.0",
        sha256=hashlib.sha256(name.encode()).hexdigest(),
    )


class InvariantTests(unittest.TestCase):
    def test_invalid_lifecycle_transition_rejected(self) -> None:
        with self.assertRaises(InvalidLifecycleTransition):
            require_transition(LifecycleState.PLANNED, LifecycleState.PUBLISHED)

    def test_valid_lifecycle_transition(self) -> None:
        require_transition(LifecycleState.PLANNED, LifecycleState.ARMED)

    def test_imported_source_requires_absent_planning_declaration(self) -> None:
        with self.assertRaises(ValidationError):
            CanonicalInterviewSourcePackage(
                source_package_id="x",
                version="1",
                admission_mode=AdmissionMode.IMPORTED_SOURCE,
                original_media_refs=(ref("media"),),
                transcript_ref=ref("transcript"),
                speaker_map_ref=ref("speaker"),
                phrase_pack_ref=ref("phrases"),
                absent_planning_declaration=False,
                operator_source_authority_ref=ref("operator-source-authority"),
                provenance_refs=(ref("provenance"),),
            )

    def test_approved_moment_requires_approval_ref(self) -> None:
        with self.assertRaises(ValidationError):
            ExpressionMoment(
                moment_id="m",
                source_package_ref=ref("source"),
                source_span_ref=ref("span"),
                speaker_id="speaker",
                start_ms=0,
                end_ms=1,
                quote_or_summary="q",
                context_window="c",
                qualities=("complete",),
                role_potential=("witness",),
                eligible_routes=("reel",),
                state=ExpressionMomentState.APPROVED,
                epistemic_state=EpistemicState.OBSERVED,
            )

    def test_campaign_diversity_is_noncompensable(self) -> None:
        assets = (
            CampaignAssetPlan(
                asset_id="a1",
                derivative_program_ref=ref("p1"),
                sequence_index=0,
                primary_role="judge",
                primary_direction=ActivationDirection.TARGET,
                edge="e1",
                format_harness="carousel",
            ),
            CampaignAssetPlan(
                asset_id="a2",
                derivative_program_ref=ref("p2"),
                sequence_index=1,
                primary_role="judge",
                primary_direction=ActivationDirection.TARGET,
                edge="e2",
                format_harness="reel",
            ),
        )
        with self.assertRaises(ValidationError):
            CampaignActivationProgram(
                campaign_id="c",
                source_package_ref=ref("source"),
                audience_segments=("aud",),
                assets=assets,
                role_diversity_minimum=2,
                direction_diversity_minimum=2,
                repeated_structure_limit=1,
                fatigue_budget=0.5,
                evaluation_contract_ref=ref("eval"),
            )

    def test_failed_gate_cannot_pass(self) -> None:
        with self.assertRaises(ValidationError):
            ActivationEvaluationReceipt(
                receipt_id="r",
                evaluated_ref=ref("obj"),
                domain=ActivationDomain.AUDIENCE,
                gate_results={"source_lineage": False},
                dimension_scores={"role_clarity": 0.9},
                verdict="pass",
                evidence_refs=(ref("evidence"),),
                created_at=datetime.now(timezone.utc),
            )


if __name__ == "__main__":
    unittest.main()
