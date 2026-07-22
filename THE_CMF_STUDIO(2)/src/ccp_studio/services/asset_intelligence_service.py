from __future__ import annotations

import hashlib
from pathlib import Path
from statistics import mean
from typing import Iterable

from ccp_studio.contracts.asset_intelligence import (
    AssetCandidateMatch,
    AssetClassification,
    AssetClass,
    AssetEvaluationReceipt,
    AssetFatigueRecord,
    AssetKind,
    AssetOrigin,
    AssetPerformanceMemory,
    AssetRecord,
    AssetRetrievalQuery,
    AssetRole,
    AssetSemanticProfile,
    AssetStatus,
    AssetUsageReceipt,
    AssetUseMode,
    AssetVersion,
    CreativeIngredient,
    CreativeIngredientVariant,
    EvaluationScope,
    MissingIngredientGap,
    ProductionRole,
    RequestingComponent,
    ReviewStatus,
    RightsProvenanceProfile,
    RightsTier,
    SourceRef,
    VisualReferenceBoard,
    WinningAssetRecord,
)
from ccp_studio.repositories.asset_intelligence import InMemoryAssetIntelligenceRepository


class AssetIntelligenceService:
    """Canonical Asset Intelligence V1 service.

    V1 is intentionally deterministic and in-memory-testable. DSPy or provider
    calls should be added behind methods without changing the public contracts.
    """

    def __init__(self, repository: InMemoryAssetIntelligenceRepository | None = None):
        self.repository = repository or InMemoryAssetIntelligenceRepository()

    def ingest_asset(
        self,
        *,
        brand_id: str,
        brand_context_version_id: str | None,
        asset_kind: AssetKind,
        asset_origin: AssetOrigin,
        display_name: str,
        description: str | None = None,
        source_refs: list[SourceRef] | None = None,
        tags: list[str] | None = None,
    ) -> AssetRecord:
        asset = AssetRecord(
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            asset_kind=asset_kind,
            asset_origin=asset_origin,
            display_name=display_name,
            description=description,
            source_refs=source_refs or [],
            tags=tags or [],
            asset_status=AssetStatus.INGESTED,
        )
        return self.repository.upsert_asset(asset)

    def fingerprint_asset(
        self,
        asset_id: str,
        *,
        content_bytes: bytes | None = None,
        file_path: str | None = None,
        uri: str | None = None,
        mime_type: str | None = None,
        width: int | None = None,
        height: int | None = None,
        duration_seconds: float | None = None,
    ) -> AssetVersion:
        if content_bytes is None and file_path:
            content_bytes = Path(file_path).read_bytes()
        if content_bytes is None:
            content_bytes = f"{asset_id}:{uri or ''}".encode("utf-8")

        sha256 = hashlib.sha256(content_bytes).hexdigest()
        version = AssetVersion(
            asset_id=asset_id,
            sha256=sha256,
            uri=uri or file_path,
            mime_type=mime_type,
            width=width,
            height=height,
            duration_seconds=duration_seconds,
            byte_size=len(content_bytes),
        )
        self.repository.upsert_version(version)

        asset = self.repository.get_asset(asset_id)
        asset.current_version_id = version.asset_version_id
        asset.asset_status = AssetStatus.FINGERPRINTED
        self.repository.upsert_asset(asset)
        return version

    def attach_rights_profile(
        self,
        asset_id: str,
        *,
        rights_tier: RightsTier,
        direct_use_allowed: bool = False,
        reference_use_allowed: bool = True,
        composition_reference_allowed: bool = True,
        style_reference_allowed: bool = True,
        provider_input_allowed: bool = False,
        commercial_use_allowed: bool = False,
        review_status: ReviewStatus | None = None,
        provenance_summary: str | None = None,
        evidence_refs: list[str] | None = None,
    ) -> RightsProvenanceProfile:
        if review_status is None:
            review_status = (
                ReviewStatus.PROVENANCE_READY
                if rights_tier in {
                    RightsTier.OWNED,
                    RightsTier.BRAND_PROVIDED,
                    RightsTier.GUEST_PROVIDED,
                    RightsTier.PUBLIC_DOMAIN,
                    RightsTier.ROYALTY_FREE,
                }
                else ReviewStatus.NEEDS_OPERATOR_REVIEW
            )
            if rights_tier == RightsTier.BLOCKED:
                review_status = ReviewStatus.BLOCKED

        rights = RightsProvenanceProfile(
            asset_id=asset_id,
            rights_tier=rights_tier,
            direct_use_allowed=direct_use_allowed,
            reference_use_allowed=reference_use_allowed,
            composition_reference_allowed=composition_reference_allowed,
            style_reference_allowed=style_reference_allowed,
            provider_input_allowed=provider_input_allowed,
            commercial_use_allowed=commercial_use_allowed,
            review_status=review_status,
            provenance_summary=provenance_summary,
            evidence_refs=evidence_refs or [],
        )
        self.repository.upsert_rights_profile(rights)

        asset = self.repository.get_asset(asset_id)
        asset.rights_profile_id = rights.rights_profile_id
        if review_status == ReviewStatus.BLOCKED:
            asset.asset_status = AssetStatus.RIGHTS_BLOCKED
        elif rights_tier == RightsTier.REFERENCE_ONLY:
            asset.asset_status = AssetStatus.REFERENCE_ONLY
        else:
            asset.asset_status = AssetStatus.NEEDS_CLASSIFICATION
        self.repository.upsert_asset(asset)
        return rights

    def classify_asset(
        self,
        asset_id: str,
        *,
        asset_classes: list[AssetClass],
        asset_roles: list[AssetRole],
        production_roles: list[ProductionRole] | None = None,
        ingredient_kinds: list[str] | None = None,
        confidence: float = 0.75,
    ) -> AssetClassification:
        classification = AssetClassification(
            asset_id=asset_id,
            asset_classes=asset_classes,
            asset_roles=asset_roles,
            production_roles=production_roles or [],
            ingredient_kinds=ingredient_kinds or [],
            confidence=confidence,
        )
        self.repository.upsert_classification(classification)

        asset = self.repository.get_asset(asset_id)
        asset.classification_id = classification.classification_id
        asset.asset_status = AssetStatus.NEEDS_EVALUATION
        self.repository.upsert_asset(asset)
        return classification

    def compile_semantic_profile(
        self,
        asset_id: str,
        *,
        literal_description: str,
        recognizable_objects: list[str] | None = None,
        human_context: str | None = None,
        setting_context: str | None = None,
        emotional_signal: list[str] | None = None,
        familiarity_signal: str | None = None,
        proof_signal: str | None = None,
        memory_signal: str | None = None,
        primitive_affinities: list[str] | None = None,
        best_use_cases: list[str] | None = None,
        bad_use_cases: list[str] | None = None,
    ) -> AssetSemanticProfile:
        profile = AssetSemanticProfile(
            asset_id=asset_id,
            literal_description=literal_description,
            recognizable_objects=recognizable_objects or [],
            human_context=human_context,
            setting_context=setting_context,
            emotional_signal=emotional_signal or [],
            familiarity_signal=familiarity_signal,
            proof_signal=proof_signal,
            memory_signal=memory_signal,
            primitive_affinities=primitive_affinities or [],
            best_use_cases=best_use_cases or [],
            bad_use_cases=bad_use_cases or [],
        )
        self.repository.upsert_semantic_profile(profile)

        asset = self.repository.get_asset(asset_id)
        asset.semantic_profile_id = profile.semantic_profile_id
        asset.asset_status = AssetStatus.CANDIDATE
        self.repository.upsert_asset(asset)
        return profile

    def evaluate_intrinsic(
        self,
        asset_id: str,
        *,
        technical_quality: float = 0.75,
        source_quality: float = 0.75,
        provenance_quality: float = 0.75,
        recognition_clarity: float = 0.75,
        semantic_strength: float = 0.75,
        rationale: str | None = None,
    ) -> AssetEvaluationReceipt:
        receipt = AssetEvaluationReceipt(
            asset_id=asset_id,
            scope=EvaluationScope.INTRINSIC,
            technical_quality=technical_quality,
            source_quality=source_quality,
            provenance_quality=provenance_quality,
            recognition_clarity=recognition_clarity,
            semantic_strength=semantic_strength,
            pass_status="pass" if min(technical_quality, provenance_quality, recognition_clarity) >= 0.5 else "fail",
            rationale=rationale,
        )
        self.repository.upsert_evaluation(receipt)

        asset = self.repository.get_asset(asset_id)
        if receipt.pass_status == "pass" and asset.asset_status not in {AssetStatus.RIGHTS_BLOCKED, AssetStatus.BLOCKED}:
            asset.asset_status = AssetStatus.APPROVED
            self.repository.upsert_asset(asset)
        return receipt

    def evaluate_contextual(
        self,
        asset_id: str,
        *,
        requesting_component: RequestingComponent,
        context_ref: str | None = None,
        primitive_fit: float = 0.75,
        visual_schema_fit: float = 0.75,
        style_route_fit: float = 0.75,
        frame_profile_fit: float = 0.75,
        composition_role_fit: float = 0.75,
        source_truth_fit: float = 0.75,
        brand_context_fit: float = 0.75,
        audience_recognition_fit: float = 0.75,
        freshness_fit: float = 0.75,
        fatigue_risk: float = 0.0,
        rationale: str | None = None,
    ) -> AssetEvaluationReceipt:
        blockers: list[str] = []
        if source_truth_fit < 0.5:
            blockers.append("source_truth_fit_low")
        if primitive_fit < 0.5:
            blockers.append("primitive_fit_low")
        if fatigue_risk > 0.8:
            blockers.append("fatigue_risk_high")

        receipt = AssetEvaluationReceipt(
            asset_id=asset_id,
            scope=EvaluationScope.CONTEXTUAL,
            requesting_component=requesting_component,
            context_ref=context_ref,
            primitive_fit=primitive_fit,
            visual_schema_fit=visual_schema_fit,
            style_route_fit=style_route_fit,
            frame_profile_fit=frame_profile_fit,
            composition_role_fit=composition_role_fit,
            source_truth_fit=source_truth_fit,
            brand_context_fit=brand_context_fit,
            audience_recognition_fit=audience_recognition_fit,
            freshness_fit=freshness_fit,
            fatigue_risk=fatigue_risk,
            pass_status="fail" if blockers else "pass",
            blocker_codes=blockers,
            rationale=rationale,
        )
        return self.repository.upsert_evaluation(receipt)

    def create_creative_ingredient(
        self,
        asset_id: str,
        *,
        ingredient_kind: str,
        display_name: str,
        semantic_need: str | None = None,
        compatible_style_routes: list[str] | None = None,
        compatible_frame_profiles: list[str] | None = None,
        composition_role_affinities: list[str] | None = None,
        use_modes: list[AssetUseMode] | None = None,
    ) -> CreativeIngredient:
        asset = self.repository.get_asset(asset_id)
        ingredient = CreativeIngredient(
            brand_id=asset.brand_id,
            brand_context_version_id=asset.brand_context_version_id,
            ingredient_kind=ingredient_kind,
            display_name=display_name,
            source_asset_ids=[asset_id],
            source_refs=asset.source_refs,
            semantic_need=semantic_need,
            primitive_binding_refs=asset.primitive_binding_refs,
            compatible_style_routes=compatible_style_routes or asset.style_route_affinities,
            compatible_frame_profiles=compatible_frame_profiles or asset.frame_profile_affinities,
            composition_role_affinities=composition_role_affinities or asset.composition_role_affinities,
            use_modes=use_modes or [AssetUseMode.REFERENCE_ONLY],
        )
        return self.repository.upsert_ingredient(ingredient)

    def retrieve_candidates(self, query: AssetRetrievalQuery) -> list[AssetCandidateMatch]:
        candidates: list[AssetCandidateMatch] = []

        for asset in self.repository.list_assets():
            if asset.asset_id in query.avoid_asset_ids:
                continue
            if asset.brand_id != query.brand_id:
                continue
            if asset.brand_context_version_id and asset.brand_context_version_id != query.brand_context_version_id:
                continue
            if asset.asset_status in {AssetStatus.BLOCKED, AssetStatus.RIGHTS_BLOCKED, AssetStatus.ARCHIVED, AssetStatus.DEPRECATED}:
                continue
            if query.allowed_asset_kinds and asset.asset_kind not in query.allowed_asset_kinds:
                continue

            rights = self.repository.get_rights_profile_for_asset(asset)
            if rights is None:
                if query.required_use_mode == AssetUseMode.DIRECT_USE:
                    continue
                rights_status = ReviewStatus.PENDING
            else:
                if not rights.allows(query.required_use_mode):
                    continue
                rights_status = rights.review_status

            classification = (
                self.repository.classifications.get(asset.classification_id)
                if asset.classification_id
                else None
            )
            if query.desired_asset_roles:
                if not classification:
                    continue
                if not set(query.desired_asset_roles).intersection(set(classification.asset_roles)):
                    continue

            ingredients = self.repository.list_ingredients_for_asset(asset.asset_id)
            ingredient = ingredients[0] if ingredients else None

            asset_version_id = asset.current_version_id
            role_fit = 0.75
            if query.desired_asset_roles and classification:
                role_fit = 1.0 if set(query.desired_asset_roles).intersection(set(classification.asset_roles)) else 0.25

            style_fit = 0.85 if not query.style_route or query.style_route in asset.style_route_affinities else 0.55
            frame_fit = 0.85 if not query.frame_profile or query.frame_profile in asset.frame_profile_affinities else 0.55
            fatigue = self._latest_fatigue_score(asset.asset_id)
            total = max(0.0, min(1.0, (role_fit + style_fit + frame_fit + (1.0 - fatigue)) / 4.0))

            candidates.append(
                AssetCandidateMatch(
                    asset_id=asset.asset_id,
                    asset_version_id=asset_version_id,
                    creative_ingredient_id=ingredient.creative_ingredient_id if ingredient else None,
                    use_mode=query.required_use_mode,
                    rights_status=rights_status,
                    semantic_match_score=0.75,
                    primitive_fit_score=0.75,
                    visual_schema_fit_score=0.75,
                    style_route_fit_score=style_fit,
                    frame_profile_fit_score=frame_fit,
                    composition_role_fit_score=role_fit,
                    freshness_score=0.75,
                    fatigue_risk_score=fatigue,
                    total_score=total,
                    rationale="Candidate passed deterministic brand, rights, role, style, frame, and fatigue filters.",
                )
            )

        return sorted(candidates, key=lambda c: c.total_score, reverse=True)[: query.max_candidates]

    def build_reference_board(
        self,
        *,
        query: AssetRetrievalQuery,
        candidates: list[AssetCandidateMatch],
        required_roles: list[AssetRole] | None = None,
        semantic_need: str | None = None,
    ) -> VisualReferenceBoard:
        grouped: dict[str, list[str]] = {}
        for candidate in candidates:
            asset = self.repository.get_asset(candidate.asset_id)
            classification = (
                self.repository.classifications.get(asset.classification_id)
                if asset.classification_id
                else None
            )
            if classification and classification.asset_roles:
                for role in classification.asset_roles:
                    grouped.setdefault(role.value, []).append(asset.asset_id)
            else:
                grouped.setdefault("unclassified", []).append(asset.asset_id)

        missing: list[MissingIngredientGap] = []
        for role in required_roles or []:
            if role.value not in grouped:
                missing.append(
                    MissingIngredientGap(
                        required_role=role,
                        semantic_need=semantic_need or f"Missing required asset role: {role.value}",
                        recommendation="Ingest or retrieve a source-grounded candidate before composition lock.",
                    )
                )

        board = VisualReferenceBoard(
            brand_id=query.brand_id,
            brand_context_version_id=query.brand_context_version_id,
            requesting_component=query.requesting_component,
            query_id=query.retrieval_query_id,
            candidate_matches=candidates,
            grouped_asset_ids=grouped,
            missing_gaps=missing,
        )
        return self.repository.upsert_reference_board(board)

    def materialize_variant(
        self,
        *,
        creative_ingredient_id: str,
        asset_id: str,
        variant_asset_version_id: str,
        variant_kind: str,
        source_asset_version_id: str | None = None,
        provider_job_receipt_id: str | None = None,
        render_receipt_id: str | None = None,
        transformation_summary: str | None = None,
    ) -> CreativeIngredientVariant:
        variant = CreativeIngredientVariant(
            creative_ingredient_id=creative_ingredient_id,
            asset_id=asset_id,
            source_asset_version_id=source_asset_version_id,
            variant_asset_version_id=variant_asset_version_id,
            variant_kind=variant_kind,
            provider_job_receipt_id=provider_job_receipt_id,
            render_receipt_id=render_receipt_id,
            transformation_summary=transformation_summary,
        )
        return self.repository.upsert_variant(variant)

    def record_usage(
        self,
        *,
        asset_id: str,
        brand_id: str,
        brand_context_version_id: str,
        requesting_component: RequestingComponent,
        used_as: AssetUseMode,
        asset_version_id: str | None = None,
        creative_ingredient_id: str | None = None,
        output_ref: str | None = None,
        project_ref: str | None = None,
        scene_ref: str | None = None,
        beat_ref: str | None = None,
        timeline_range: tuple[float, float] | None = None,
        composition_role: str | None = None,
        style_route: str | None = None,
        frame_profile: str | None = None,
        primitive_coalition_contract_id: str | None = None,
    ) -> AssetUsageReceipt:
        receipt = AssetUsageReceipt(
            asset_id=asset_id,
            asset_version_id=asset_version_id,
            creative_ingredient_id=creative_ingredient_id,
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            requesting_component=requesting_component,
            output_ref=output_ref,
            project_ref=project_ref,
            scene_ref=scene_ref,
            beat_ref=beat_ref,
            timeline_range=timeline_range,
            composition_role=composition_role,
            style_route=style_route,
            frame_profile=frame_profile,
            primitive_coalition_contract_id=primitive_coalition_contract_id,
            used_as=used_as,
        )
        return self.repository.upsert_usage(receipt)

    def update_performance(
        self,
        *,
        asset_id: str,
        brand_id: str,
        performance_score: float,
        platform: str | None = None,
        output_ref: str | None = None,
        views: int | None = None,
        saves: int | None = None,
        shares: int | None = None,
        completion_rate: float | None = None,
        engagement_rate: float | None = None,
        qualitative_notes: str | None = None,
    ) -> AssetPerformanceMemory:
        memory = AssetPerformanceMemory(
            asset_id=asset_id,
            brand_id=brand_id,
            platform=platform,
            output_ref=output_ref,
            views=views,
            saves=saves,
            shares=shares,
            completion_rate=completion_rate,
            engagement_rate=engagement_rate,
            qualitative_notes=qualitative_notes,
            performance_score=performance_score,
        )
        return self.repository.upsert_performance(memory)

    def compute_fatigue(self, asset_id: str, *, recent_window_count: int = 5) -> AssetFatigueRecord:
        asset = self.repository.get_asset(asset_id)
        usage = self.repository.list_usage_for_asset(asset_id)
        usage_count = len(usage)
        recent_usage_count = min(usage_count, recent_window_count)
        fatigue_score = min(1.0, usage_count / 10.0)
        status = AssetStatus.FATIGUED if fatigue_score >= 0.7 else AssetStatus.ACTIVE

        fatigue = AssetFatigueRecord(
            asset_id=asset_id,
            brand_id=asset.brand_id,
            usage_count=usage_count,
            recent_usage_count=recent_usage_count,
            fatigue_score=fatigue_score,
            status_recommendation=status,
            rationale="Deterministic V1 fatigue score based on usage count.",
        )
        self.repository.upsert_fatigue(fatigue)

        if status == AssetStatus.FATIGUED:
            asset.asset_status = AssetStatus.FATIGUED
            self.repository.upsert_asset(asset)

        return fatigue

    def promote_winner(
        self,
        asset_id: str,
        *,
        promoted_by_actor_id: str | None = None,
        evidence_receipt_ids: list[str] | None = None,
        minimum_score: float = 0.65,
        approved: bool = True,
    ) -> WinningAssetRecord:
        asset = self.repository.get_asset(asset_id)
        performance = self.repository.list_performance_for_asset(asset_id)
        score = mean([p.performance_score for p in performance]) if performance else 0.0

        if score < minimum_score:
            raise ValueError("winner promotion requires performance evidence above threshold")

        winner = WinningAssetRecord(
            asset_id=asset_id,
            brand_id=asset.brand_id,
            promoted_by_actor_id=promoted_by_actor_id,
            evidence_receipt_ids=evidence_receipt_ids or [p.performance_memory_id for p in performance],
            performance_score=score,
            approved=approved,
            winning_pattern_summary="Promoted from Asset Intelligence V1 performance threshold.",
        )
        return self.repository.upsert_winner(winner)

    def block_asset(self, asset_id: str, reason: str | None = None) -> AssetRecord:
        asset = self.repository.get_asset(asset_id)
        asset.asset_status = AssetStatus.BLOCKED
        if reason:
            asset.tags.append(f"blocked_reason:{reason}")
        return self.repository.upsert_asset(asset)

    def deprecate_asset(self, asset_id: str, reason: str | None = None) -> AssetRecord:
        asset = self.repository.get_asset(asset_id)
        asset.asset_status = AssetStatus.DEPRECATED
        if reason:
            asset.tags.append(f"deprecated_reason:{reason}")
        return self.repository.upsert_asset(asset)

    def _latest_fatigue_score(self, asset_id: str) -> float:
        records = [
            record
            for record in self.repository.fatigue_records.values()
            if record.asset_id == asset_id
        ]
        if not records:
            return 0.0
        return sorted(records, key=lambda r: r.created_at)[-1].fatigue_score
