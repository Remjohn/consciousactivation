from __future__ import annotations
from ccp_studio.contracts.carousel_engine import CarouselSequenceEvaluationReceipt

class CarouselEvalService:
    def run_sequence_eval(self, *, carousel_variant_id: str, claim_support: float = .85, mobile_readability: float = .85, sequence_cohesion: float = .85, style_route_purity: float = .85):
        return CarouselSequenceEvaluationReceipt(
            carousel_variant_id=carousel_variant_id,
            claim_support=claim_support,
            mobile_readability=mobile_readability,
            sequence_cohesion=sequence_cohesion,
            style_route_purity=style_route_purity,
        )
