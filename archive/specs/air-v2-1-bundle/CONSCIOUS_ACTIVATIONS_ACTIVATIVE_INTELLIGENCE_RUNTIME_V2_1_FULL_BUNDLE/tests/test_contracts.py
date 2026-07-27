from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reference_implementation"))

from activative_intelligence_v2.models import (  # noqa: E402
    ActivationHypothesisPortfolio,
    CampaignActivationProgram,
    CanonicalInterviewSourcePackage,
    ExpressionMoment,
    HumanResolutionEpisode,
    InterviewAssetContract,
    ObservedActivativeIntelligencePack,
    PlannedActivativeIntelligencePack,
    ReactionReceipt,
)


class ContractExampleTests(unittest.TestCase):
    def load(self, name: str) -> dict:
        return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))

    def test_planned_pack(self) -> None:
        PlannedActivativeIntelligencePack.model_validate(
            self.load("01_julie_planned_activative_intelligence_pack.json")
        )

    def test_interview_asset_contract(self) -> None:
        InterviewAssetContract.model_validate(
            self.load("02_julie_interview_asset_contract.json")
        )

    def test_reaction_receipt(self) -> None:
        ReactionReceipt.model_validate(self.load("03_julie_reaction_receipt.json"))

    def test_expression_moment(self) -> None:
        ExpressionMoment.model_validate(self.load("04_julie_expression_moment.json"))

    def test_source_packages(self) -> None:
        CanonicalInterviewSourcePackage.model_validate(
            self.load("05_julie_canonical_source_package.json")
        )
        CanonicalInterviewSourcePackage.model_validate(
            self.load("11_imported_source_dual_admission.json")
        )

    def test_observed_pack(self) -> None:
        ObservedActivativeIntelligencePack.model_validate(
            self.load("06_julie_observed_activative_intelligence_pack.json")
        )

    def test_portfolio(self) -> None:
        ActivationHypothesisPortfolio.model_validate(
            self.load("08_james_relationship_activation_portfolio.json")
        )

    def test_human_resolution(self) -> None:
        HumanResolutionEpisode.model_validate(
            self.load("09_human_resolution_phone_addiction_collapse.json")
        )

    def test_campaign(self) -> None:
        CampaignActivationProgram.model_validate(
            self.load("10_campaign_activation_program.json")
        )


if __name__ == "__main__":
    unittest.main()
