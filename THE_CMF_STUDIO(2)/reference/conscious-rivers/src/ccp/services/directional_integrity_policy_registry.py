"""Directional Integrity Policy Registry — DEP-SDA-021.
Stores compiled validation policy bundles by surface/domain with mandatory thresholds from §7.3."""
from __future__ import annotations
from src.ccp.models.directional_integrity_models import (
    DirectionalIntegrityDimension as Dim, DirectionalIntegrityDomain as Dom,
    DirectionalIntegrityPolicyBundle, DirectionalIntegrityPolicyRule,
    DirectionalIntegritySurfaceClass as Surf,
)

def _r(rid, dim, warn, block, surf, dom, desc):
    return DirectionalIntegrityPolicyRule(rule_id=rid, dimension=dim, warning_threshold=warn, block_threshold=block, applies_to_surface=surf, applies_to_domain=dom, description=desc)

FORBIDDEN_DRIFTS = ["prestige theater", "coercive urgency", "humiliation-as-motivation", "synthetic belonging capture", "mystical authority inflation"]

POLICY_BUNDLES: dict[str, DirectionalIntegrityPolicyBundle] = {
    "DI-POL-CCF-001": DirectionalIntegrityPolicyBundle(policy_id="DI-POL-CCF-001", domain=Dom.CCF, surface_class=Surf.SEMANTIC_PLANNING, version="1.0", rules=[
        _r("CCF-INV", Dim.INVARIANT_PRESERVATION, 0.70, 0.60, Surf.SEMANTIC_PLANNING, Dom.CCF, "Invariant preservation for internal planning"),
        _r("CCF-REP", Dim.REPRESENTATION_DRIFT, 0.30, 0.45, Surf.SEMANTIC_PLANNING, Dom.CCF, "Representation drift for internal planning"),
        _r("CCF-HN", Dim.HARD_NEGATIVE_ADJACENCY, 0.25, 0.40, Surf.SEMANTIC_PLANNING, Dom.CCF, "Hard negative adjacency for internal planning"),
        _r("CCF-TRJ", Dim.TRAJECTORY_RISK, 0.30, 0.45, Surf.SEMANTIC_PLANNING, Dom.CCF, "Trajectory risk for internal planning"),
    ]),
    "DI-POL-CMF-001": DirectionalIntegrityPolicyBundle(policy_id="DI-POL-CMF-001", domain=Dom.CMF, surface_class=Surf.RENDER_RELEASE, version="1.0", rules=[
        _r("CMF-INV", Dim.INVARIANT_PRESERVATION, 0.75, 0.65, Surf.RENDER_RELEASE, Dom.CMF, "Invariant preservation for render release"),
        _r("CMF-REP", Dim.REPRESENTATION_DRIFT, 0.25, 0.40, Surf.RENDER_RELEASE, Dom.CMF, "Representation drift for render release"),
        _r("CMF-HN", Dim.HARD_NEGATIVE_ADJACENCY, 0.22, 0.38, Surf.RENDER_RELEASE, Dom.CMF, "Hard negative adjacency for render release"),
        _r("CMF-TRJ", Dim.TRAJECTORY_RISK, 0.28, 0.42, Surf.RENDER_RELEASE, Dom.CMF, "Trajectory risk for render release"),
    ]),
    "DI-POL-CBCS-001": DirectionalIntegrityPolicyBundle(policy_id="DI-POL-CBCS-001", domain=Dom.CBCS, surface_class=Surf.COACHING_INTERVENTION, version="1.0", rules=[
        _r("CBCS-INV", Dim.INVARIANT_PRESERVATION, 0.80, 0.70, Surf.COACHING_INTERVENTION, Dom.CBCS, "Invariant preservation for coaching"),
        _r("CBCS-REP", Dim.REPRESENTATION_DRIFT, 0.20, 0.35, Surf.COACHING_INTERVENTION, Dom.CBCS, "Representation drift for coaching"),
        _r("CBCS-HN", Dim.HARD_NEGATIVE_ADJACENCY, 0.20, 0.35, Surf.COACHING_INTERVENTION, Dom.CBCS, "Hard negative adjacency for coaching"),
        _r("CBCS-TRJ", Dim.TRAJECTORY_RISK, 0.25, 0.40, Surf.COACHING_INTERVENTION, Dom.CBCS, "Trajectory risk for coaching"),
    ]),
    "DI-POL-REACTIONS-001": DirectionalIntegrityPolicyBundle(policy_id="DI-POL-REACTIONS-001", domain=Dom.REACTIONS, surface_class=Surf.SOCIAL_REACTION, version="1.0", rules=[
        _r("RCT-INV", Dim.INVARIANT_PRESERVATION, 0.78, 0.68, Surf.SOCIAL_REACTION, Dom.REACTIONS, "Invariant preservation for social reactions"),
        _r("RCT-REP", Dim.REPRESENTATION_DRIFT, 0.25, 0.40, Surf.SOCIAL_REACTION, Dom.REACTIONS, "Representation drift for social reactions"),
        _r("RCT-HN", Dim.HARD_NEGATIVE_ADJACENCY, 0.24, 0.40, Surf.SOCIAL_REACTION, Dom.REACTIONS, "Hard negative adjacency for social reactions"),
        _r("RCT-TRJ", Dim.TRAJECTORY_RISK, 0.28, 0.45, Surf.SOCIAL_REACTION, Dom.REACTIONS, "Trajectory risk for social reactions"),
    ]),
    "DI-POL-WEBINAR-001": DirectionalIntegrityPolicyBundle(policy_id="DI-POL-WEBINAR-001", domain=Dom.WEBINAR, surface_class=Surf.LONG_FORM_AUTHORITY, version="1.0", rules=[
        _r("WEB-INV", Dim.INVARIANT_PRESERVATION, 0.82, 0.72, Surf.LONG_FORM_AUTHORITY, Dom.WEBINAR, "Invariant preservation for long-form authority"),
        _r("WEB-REP", Dim.REPRESENTATION_DRIFT, 0.22, 0.38, Surf.LONG_FORM_AUTHORITY, Dom.WEBINAR, "Representation drift for long-form authority"),
        _r("WEB-HN", Dim.HARD_NEGATIVE_ADJACENCY, 0.20, 0.35, Surf.LONG_FORM_AUTHORITY, Dom.WEBINAR, "Hard negative adjacency for long-form authority"),
        _r("WEB-TRJ", Dim.TRAJECTORY_RISK, 0.25, 0.40, Surf.LONG_FORM_AUTHORITY, Dom.WEBINAR, "Trajectory risk for long-form authority"),
    ]),
    "DI-POL-COMMERCIAL-001": DirectionalIntegrityPolicyBundle(policy_id="DI-POL-COMMERCIAL-001", domain=Dom.COMMERCIAL, surface_class=Surf.COMMERCIAL_TRUST_TRANSFER, version="1.0", rules=[
        _r("COM-INV", Dim.INVARIANT_PRESERVATION, 0.85, 0.75, Surf.COMMERCIAL_TRUST_TRANSFER, Dom.COMMERCIAL, "Invariant preservation for commercial trust"),
        _r("COM-REP", Dim.REPRESENTATION_DRIFT, 0.15, 0.30, Surf.COMMERCIAL_TRUST_TRANSFER, Dom.COMMERCIAL, "Representation drift for commercial trust"),
        _r("COM-HN", Dim.HARD_NEGATIVE_ADJACENCY, 0.15, 0.30, Surf.COMMERCIAL_TRUST_TRANSFER, Dom.COMMERCIAL, "Hard negative adjacency for commercial trust"),
        _r("COM-TRJ", Dim.TRAJECTORY_RISK, 0.20, 0.35, Surf.COMMERCIAL_TRUST_TRANSFER, Dom.COMMERCIAL, "Trajectory risk for commercial trust"),
    ]),
}

class DirectionalIntegrityPolicyRegistry:
    def resolve(self, domain: Dom, surface: Surf) -> DirectionalIntegrityPolicyBundle | None:
        for bundle in POLICY_BUNDLES.values():
            if bundle.domain == domain and bundle.surface_class == surface:
                return bundle
        return None
    def resolve_by_id(self, policy_id: str) -> DirectionalIntegrityPolicyBundle | None:
        return POLICY_BUNDLES.get(policy_id)
