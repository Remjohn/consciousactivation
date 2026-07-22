"""
FR-ERA3-27 — Perceptual Influence Policy Registry
=================================================
Stores and resolves validation policy bundles by surface and domain.
"""

from __future__ import annotations

from src.ccp.models.perceptual_influence_models import (
    PerceptualInfluenceDecision,
    PerceptualInfluenceDomain,
    PerceptualInfluencePolicyBundle,
    PerceptualInfluenceSurface,
)

# default policies by surface
POLICY_BUNDLES: dict[str, PerceptualInfluencePolicyBundle] = {
    "PI-POL-SEMANTIC_PLANNING": PerceptualInfluencePolicyBundle(
        policy_id="PI-POL-SEMANTIC_PLANNING",
        domain=PerceptualInfluenceDomain.CCF,
        surface_class=PerceptualInfluenceSurface.SEMANTIC_PLANNING,
        pass_thresholds={
            "COGNITIVE_IMPRINT": 0.40,
            "SYMBOLIC_DENSITY": 0.35,
            "HUMAN_CONGRUENCE": 0.45,
            "CONTRAST_CLARITY": 0.35,
            "MEMORABILITY_PRESSURE": 0.35,
        },
        risk_ceilings={
            "OVEREXPLANATION_RISK": 0.65,
            "SYNTHETIC_SMOOTHNESS": 0.60,
        },
        influence_alignment_required=True,
        false_depth_blocks=True,
        missing_sfl_behavior=PerceptualInfluenceDecision.REVIEW,
        missing_di_behavior=PerceptualInfluenceDecision.REVIEW,
        notes="Internal semantic planning - advisory mode fallbacks.",
    ),
    "PI-POL-RENDER_RELEASE": PerceptualInfluencePolicyBundle(
        policy_id="PI-POL-RENDER_RELEASE",
        domain=PerceptualInfluenceDomain.CMF,
        surface_class=PerceptualInfluenceSurface.RENDER_RELEASE,
        pass_thresholds={
            "COGNITIVE_IMPRINT": 0.55,
            "SYMBOLIC_DENSITY": 0.50,
            "HUMAN_CONGRUENCE": 0.60,
            "CONTRAST_CLARITY": 0.50,
            "MEMORABILITY_PRESSURE": 0.50,
        },
        risk_ceilings={
            "OVEREXPLANATION_RISK": 0.50,
            "SYNTHETIC_SMOOTHNESS": 0.45,
        },
        influence_alignment_required=True,
        false_depth_blocks=True,
        missing_sfl_behavior=PerceptualInfluenceDecision.DOWNGRADE,
        missing_di_behavior=PerceptualInfluenceDecision.DOWNGRADE,
        notes="Render release - strict enforcement.",
    ),
    "PI-POL-COMMERCIAL_TRUST_TRANSFER": PerceptualInfluencePolicyBundle(
        policy_id="PI-POL-COMMERCIAL_TRUST_TRANSFER",
        domain=PerceptualInfluenceDomain.COMMERCIAL,
        surface_class=PerceptualInfluenceSurface.COMMERCIAL_TRUST_TRANSFER,
        pass_thresholds={
            "COGNITIVE_IMPRINT": 0.65,
            "SYMBOLIC_DENSITY": 0.55,
            "HUMAN_CONGRUENCE": 0.70,
            "CONTRAST_CLARITY": 0.55,
            "MEMORABILITY_PRESSURE": 0.55,
        },
        risk_ceilings={
            "OVEREXPLANATION_RISK": 0.40,
            "SYNTHETIC_SMOOTHNESS": 0.35,
        },
        influence_alignment_required=True,
        false_depth_blocks=True,
        missing_sfl_behavior=PerceptualInfluenceDecision.DOWNGRADE,
        missing_di_behavior=PerceptualInfluenceDecision.DOWNGRADE,
        notes="Commercial trust transfer - maximum strictness.",
    ),
    "PI-POL-SOCIAL_SHARE": PerceptualInfluencePolicyBundle(
        policy_id="PI-POL-SOCIAL_SHARE",
        domain=PerceptualInfluenceDomain.REACTIONS,
        surface_class=PerceptualInfluenceSurface.SOCIAL_SHARE,
        pass_thresholds={
            "COGNITIVE_IMPRINT": 0.60,
            "SYMBOLIC_DENSITY": 0.50,
            "HUMAN_CONGRUENCE": 0.65,
            "CONTRAST_CLARITY": 0.50,
            "MEMORABILITY_PRESSURE": 0.60,
        },
        risk_ceilings={
            "OVEREXPLANATION_RISK": 0.45,
            "SYNTHETIC_SMOOTHNESS": 0.40,
        },
        influence_alignment_required=True,
        false_depth_blocks=True,
        missing_sfl_behavior=PerceptualInfluenceDecision.DOWNGRADE,
        missing_di_behavior=PerceptualInfluenceDecision.DOWNGRADE,
        notes="Social share - high engagement requirements.",
    ),
    "PI-POL-COACHING_INTERVENTION": PerceptualInfluencePolicyBundle(
        policy_id="PI-POL-COACHING_INTERVENTION",
        domain=PerceptualInfluenceDomain.CBCS,
        surface_class=PerceptualInfluenceSurface.COACHING_INTERVENTION,
        pass_thresholds={
            "COGNITIVE_IMPRINT": 0.50,
            "SYMBOLIC_DENSITY": 0.40,
            "HUMAN_CONGRUENCE": 0.70,
            "CONTRAST_CLARITY": 0.45,
            "MEMORABILITY_PRESSURE": 0.40,
        },
        risk_ceilings={
            "OVEREXPLANATION_RISK": 0.50,
            "SYNTHETIC_SMOOTHNESS": 0.40,
        },
        influence_alignment_required=True,
        false_depth_blocks=True,
        missing_sfl_behavior=PerceptualInfluenceDecision.REVIEW,
        missing_di_behavior=PerceptualInfluenceDecision.REVIEW,
        notes="Coaching intervention - human-centric overrides.",
    ),
    "PI-POL-INTERNAL_REVIEW": PerceptualInfluencePolicyBundle(
        policy_id="PI-POL-INTERNAL_REVIEW",
        domain=PerceptualInfluenceDomain.CCF,
        surface_class=PerceptualInfluenceSurface.INTERNAL_REVIEW,
        pass_thresholds={
            "COGNITIVE_IMPRINT": 0.30,
            "SYMBOLIC_DENSITY": 0.25,
            "HUMAN_CONGRUENCE": 0.35,
            "CONTRAST_CLARITY": 0.25,
            "MEMORABILITY_PRESSURE": 0.25,
        },
        risk_ceilings={
            "OVEREXPLANATION_RISK": 0.75,
            "SYNTHETIC_SMOOTHNESS": 0.70,
        },
        influence_alignment_required=False,
        false_depth_blocks=False,
        missing_sfl_behavior=PerceptualInfluenceDecision.REVIEW,
        missing_di_behavior=PerceptualInfluenceDecision.REVIEW,
        notes="Internal review - lowest constraints.",
    ),
}


class PerceptualInfluencePolicyRegistry:
    def resolve(self, domain: PerceptualInfluenceDomain, surface: PerceptualInfluenceSurface) -> PerceptualInfluencePolicyBundle | None:
        # Match surface class
        for bundle in POLICY_BUNDLES.values():
            if bundle.surface_class == surface:
                return bundle
        # Fallback to general lookup
        for bundle in POLICY_BUNDLES.values():
            if bundle.domain == domain and bundle.surface_class == surface:
                return bundle
        return None

    def resolve_by_id(self, policy_id: str) -> PerceptualInfluencePolicyBundle | None:
        return POLICY_BUNDLES.get(policy_id)
