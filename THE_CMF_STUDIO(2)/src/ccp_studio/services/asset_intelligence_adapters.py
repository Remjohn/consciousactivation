from __future__ import annotations

from typing import Any

from ccp_studio.contracts.asset_intelligence import (
    AssetKind,
    AssetOrigin,
    AssetRecord,
    AssetUseMode,
    CreativeIngredient,
    RightsProvenanceProfile,
    RightsTier,
    ReviewStatus,
    SourceRef,
)


def _get_value(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


class AssetIntelligenceAdapters:
    """Adapters from existing repo objects to canonical Asset Intelligence V1 objects.

    These adapters are intentionally tolerant of dicts or Pydantic/domain objects.
    """

    @staticmethod
    def adapt_micro_semiotic_anchor(
        anchor: Any,
        *,
        brand_id: str,
        brand_context_version_id: str,
    ) -> CreativeIngredient:
        anchor_id = str(_get_value(anchor, "anchor_id", _get_value(anchor, "id", "unknown_anchor")))
        display_name = str(_get_value(anchor, "display_name", _get_value(anchor, "name", "Micro-Semiotic Anchor")))
        description = str(_get_value(anchor, "description", _get_value(anchor, "semantic_need", "")))

        return CreativeIngredient(
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            ingredient_kind="micro_semiotic_anchor",
            display_name=display_name,
            source_asset_ids=[f"asset_from_anchor_{anchor_id}"],
            source_refs=[SourceRef(source_kind="creative_library.micro_semiotic_anchor", source_id=anchor_id, description=description)],
            semantic_need=description or "Micro-semiotic anchor from creative library.",
            use_modes=[AssetUseMode.REFERENCE_ONLY, AssetUseMode.COMPOSITION_REFERENCE_ONLY],
            status="candidate",
        )

    @staticmethod
    def adapt_visual_candidate(
        candidate: Any,
        *,
        brand_id: str,
        brand_context_version_id: str,
    ) -> tuple[AssetRecord, RightsProvenanceProfile]:
        candidate_id = str(_get_value(candidate, "candidate_id", _get_value(candidate, "id", "visual_candidate")))
        url = _get_value(candidate, "url", _get_value(candidate, "source_url", None))
        title = str(_get_value(candidate, "title", _get_value(candidate, "display_name", "Visual Research Candidate")))
        licensing = str(_get_value(candidate, "licensing", _get_value(candidate, "license_tier", "reference_only")))

        rights_tier = RightsTier.REFERENCE_ONLY
        if licensing in {"owned", "brand_provided", "guest_provided", "public_domain", "royalty_free"}:
            rights_tier = RightsTier(licensing)
        elif licensing == "unknown":
            rights_tier = RightsTier.UNKNOWN
        elif licensing in {"restricted", "blocked"}:
            rights_tier = RightsTier.BLOCKED if licensing == "blocked" else RightsTier.RESTRICTED

        asset = AssetRecord(
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            asset_kind=AssetKind.VISUAL_REFERENCE,
            asset_origin=AssetOrigin.VISUAL_RESEARCH_CANDIDATE,
            display_name=title,
            source_refs=[SourceRef(source_kind="visual_research.candidate", source_id=candidate_id, description=url)],
            description=str(_get_value(candidate, "description", "")) or None,
        )

        rights = RightsProvenanceProfile(
            asset_id=asset.asset_id,
            rights_tier=rights_tier,
            direct_use_allowed=rights_tier in {RightsTier.OWNED, RightsTier.BRAND_PROVIDED, RightsTier.GUEST_PROVIDED, RightsTier.PUBLIC_DOMAIN, RightsTier.ROYALTY_FREE},
            reference_use_allowed=True,
            style_reference_allowed=True,
            composition_reference_allowed=True,
            provider_input_allowed=rights_tier in {RightsTier.OWNED, RightsTier.BRAND_PROVIDED, RightsTier.GUEST_PROVIDED},
            commercial_use_allowed=rights_tier in {RightsTier.OWNED, RightsTier.BRAND_PROVIDED, RightsTier.GUEST_PROVIDED, RightsTier.PUBLIC_DOMAIN, RightsTier.ROYALTY_FREE},
            review_status=ReviewStatus.PROVENANCE_READY if rights_tier not in {RightsTier.UNKNOWN, RightsTier.RESTRICTED, RightsTier.BLOCKED, RightsTier.REFERENCE_ONLY} else ReviewStatus.NEEDS_OPERATOR_REVIEW,
            provenance_summary=f"Adapted from visual research candidate {candidate_id}.",
        )

        return asset, rights

    @staticmethod
    def adapt_provider_output(
        provider_receipt: Any,
        *,
        brand_id: str,
        brand_context_version_id: str,
    ) -> AssetRecord:
        receipt_id = str(_get_value(provider_receipt, "provider_job_receipt_id", _get_value(provider_receipt, "receipt_id", "provider_receipt")))
        display_name = str(_get_value(provider_receipt, "display_name", "Provider Generated Asset"))

        return AssetRecord(
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            asset_kind=AssetKind.PROVIDER_GENERATED_IMAGE,
            asset_origin=AssetOrigin.PROVIDER_GENERATED,
            display_name=display_name,
            source_refs=[SourceRef(source_kind="provider_job_receipt", source_id=receipt_id)],
            description="Generated output registered through Asset Intelligence provider-output adapter.",
        )
