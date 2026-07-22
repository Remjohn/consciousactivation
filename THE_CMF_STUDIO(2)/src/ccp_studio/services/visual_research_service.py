"""SVRE/Aurore visual asset research service for TS-CMF-049."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.scene_spec import RenderContract
from ccp_studio.contracts.visual_research import (
    AssetResearchManifest,
    AssetResearchReceipt,
    CandidateUseMode,
    ImageResolutionMap,
    LicenseTier,
    LicensingDecision,
    VisualCandidate,
    VisualCandidateScore,
    VisualResearchQuery,
    new_asset_research_receipt,
    visual_research_hash,
)
from ccp_studio.repositories.visual_research import InMemoryVisualResearchRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.provider_operations_service import ProviderOperationsService
from ccp_studio.services.scene_spec_compiler import SceneSpecCompiler


LEGACY_ADAPTER_ROUTE = "svre_aurore_contract_adapter.v1"
BLOCKED_LEGACY_EXECUTION_ROUTES = {
    "svre_legacy_executor",
    "aurore_v2_live_executor",
    "legacy_asset_hunt_runtime",
    "runninghub",
}


class VisualResearchError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class VisualResearchService:
    provider_operations: ProviderOperationsService
    scene_spec_compiler: SceneSpecCompiler | None = None
    repository: InMemoryVisualResearchRepository = field(default_factory=InMemoryVisualResearchRepository)

    def __post_init__(self) -> None:
        if not self.provider_operations.repository.capabilities:
            self.provider_operations.seed_current_cmf_capabilities()

    def create_visual_research_query(
        self,
        *,
        scene_spec_id: UUID,
        asset_roll_role: str,
        emotional_state: str,
        symbolic_role: str,
        contradiction_value: str | None,
        brand_alignment_constraints: list[str],
        source_constraints: list[str],
        licensing_requirements: list[str],
        query_terms: list[str],
        actor_id: UUID,
        known_person_name: str | None = None,
        command_id: UUID | None = None,
    ) -> VisualResearchQuery:
        if self.scene_spec_compiler is not None and scene_spec_id not in self.scene_spec_compiler.repository.scene_specs:
            raise VisualResearchError("SCENE_SPEC_REQUIRED", "SceneSpec is required for visual research.")
        query = VisualResearchQuery(
            schema_version="cmf.visual_research_query.v1",
            visual_research_query_id=uuid4(),
            scene_spec_id=scene_spec_id,
            asset_roll_role=asset_roll_role,
            emotional_state=emotional_state,
            symbolic_role=symbolic_role,
            contradiction_value=contradiction_value,
            brand_alignment_constraints=brand_alignment_constraints,
            source_constraints=source_constraints,
            licensing_requirements=licensing_requirements,
            query_terms=query_terms,
            known_person_name=known_person_name,
            legacy_adapter_route=LEGACY_ADAPTER_ROUTE,
            created_at=utc_now(),
        )
        return self.repository.put_query(query)

    def record_licensing_decision(
        self,
        *,
        visual_research_query_id: UUID,
        source_url_or_ref: str,
        license_tier: LicenseTier | str,
        provenance_summary: str,
        actor_id: UUID,
        direct_use_requested: bool = True,
        attribution_required: bool = False,
        evidence_refs: list[str] | None = None,
        command_id: UUID | None = None,
    ) -> LicensingDecision:
        self._query(visual_research_query_id)
        tier = LicenseTier(license_tier)
        provenance_ready = bool(provenance_summary.strip()) and bool(evidence_refs)
        direct_use_allowed = provenance_ready and tier in {
            LicenseTier.owned,
            LicenseTier.public_domain,
            LicenseTier.royalty_free,
        }
        composition_reference_allowed = provenance_ready and tier != LicenseTier.restricted
        blockers: list[str] = []
        if not provenance_ready:
            blockers.append("ASSET_PROVENANCE_REQUIRED")
        if direct_use_requested and not direct_use_allowed:
            blockers.append("DIRECT_USE_LICENSE_NOT_AVAILABLE")
        if tier == LicenseTier.restricted:
            blockers.append("ASSET_LICENSE_RESTRICTED")
        decision_code = (
            "LICENSE_DIRECT_USE_ALLOWED"
            if direct_use_allowed
            else "LICENSE_REFERENCE_ONLY"
            if composition_reference_allowed
            else "LICENSE_BLOCKED"
        )
        decision = LicensingDecision(
            schema_version="cmf.licensing_decision.v1",
            licensing_decision_id=uuid4(),
            visual_research_query_id=visual_research_query_id,
            source_url_or_ref=source_url_or_ref,
            license_tier=tier,
            direct_use_allowed=direct_use_allowed,
            composition_reference_allowed=composition_reference_allowed,
            attribution_required=attribution_required,
            provenance_ready=provenance_ready,
            decision_code=decision_code,
            blocker_codes=blockers,
            evidence_refs=evidence_refs or [],
            decided_at=utc_now(),
        )
        return self.repository.put_licensing_decision(decision)

    def score_visual_candidate(
        self,
        *,
        visual_research_query_id: UUID,
        source_url_or_ref: str,
        candidate_uri: str | None,
        provenance_summary: str,
        licensing_decision_id: UUID,
        provider_route: str,
        score_fields: dict[str, float],
        actor_id: UUID,
        superseded_legacy_logic_refs: list[str] | None = None,
        command_id: UUID | None = None,
    ) -> VisualCandidate:
        query = self._query(visual_research_query_id)
        license_decision = self._license(licensing_decision_id)
        if license_decision.visual_research_query_id != visual_research_query_id:
            raise VisualResearchError("LICENSE_QUERY_MISMATCH", "License decision must belong to the query.")
        self._validate_current_provider_route(provider_route)
        score = self._score(query, score_fields)
        use_mode = self._use_mode(license_decision, score, query)
        stored_score = self.repository.put_score(score)
        candidate = VisualCandidate(
            schema_version="cmf.visual_candidate.v1",
            visual_candidate_id=uuid4(),
            visual_research_query_id=visual_research_query_id,
            source_url_or_ref=source_url_or_ref,
            candidate_uri=candidate_uri,
            provenance_summary=provenance_summary,
            use_mode=use_mode,
            license_decision_id=license_decision.licensing_decision_id,
            score_id=stored_score.score_id,
            provider_route=provider_route,
            superseded_legacy_logic_refs=superseded_legacy_logic_refs
            or ["svre:t-score", "aurore:source-win-rate", "cmf-manual:asset-hunt"],
            created_at=utc_now(),
        )
        return self.repository.put_candidate(candidate)

    def run_asset_research(
        self,
        *,
        visual_research_query_id: UUID,
        candidates: list[dict[str, Any]],
        actor_id: UUID,
        downstream_render_route: str,
        command_id: UUID | None = None,
    ) -> AssetResearchReceipt:
        for item in candidates:
            license_decision = self.record_licensing_decision(
                visual_research_query_id=visual_research_query_id,
                source_url_or_ref=item["source_url_or_ref"],
                license_tier=item["license_tier"],
                provenance_summary=item.get("provenance_summary", ""),
                direct_use_requested=bool(item.get("direct_use_requested", True)),
                attribution_required=bool(item.get("attribution_required", False)),
                evidence_refs=item.get("evidence_refs", []),
                actor_id=actor_id,
                command_id=command_id,
            )
            self.score_visual_candidate(
                visual_research_query_id=visual_research_query_id,
                source_url_or_ref=item["source_url_or_ref"],
                candidate_uri=item.get("candidate_uri"),
                provenance_summary=item.get("provenance_summary", ""),
                licensing_decision_id=license_decision.licensing_decision_id,
                provider_route=item["provider_route"],
                score_fields=item["score_fields"],
                superseded_legacy_logic_refs=item.get("superseded_legacy_logic_refs"),
                actor_id=actor_id,
                command_id=command_id,
            )
        manifest, image_map, receipt = self.write_asset_research_manifest(
            visual_research_query_id=visual_research_query_id,
            actor_id=actor_id,
            downstream_render_route=downstream_render_route,
            command_id=command_id,
        )
        return receipt

    def select_visual_candidate(
        self,
        *,
        visual_candidate_id: UUID,
        actor_id: UUID,
    ) -> VisualCandidate:
        candidate = self._candidate(visual_candidate_id)
        if candidate.use_mode == CandidateUseMode.blocked:
            raise VisualResearchError("VISUAL_CANDIDATE_BLOCKED", "Blocked candidates cannot be selected.")
        selected = candidate.model_copy(update={"selected": True})
        return self.repository.put_candidate(selected)

    def write_asset_research_manifest(
        self,
        *,
        visual_research_query_id: UUID,
        actor_id: UUID,
        downstream_render_route: str,
        selected_candidate_id: UUID | None = None,
        command_id: UUID | None = None,
    ) -> tuple[AssetResearchManifest, ImageResolutionMap, AssetResearchReceipt]:
        query = self._query(visual_research_query_id)
        candidates = self.repository.candidates_for_query(visual_research_query_id)
        if not candidates:
            raise VisualResearchError("VISUAL_CANDIDATE_REQUIRED", "At least one visual candidate is required.")
        selected = self._selected_candidate(candidates, selected_candidate_id)
        selected = self.select_visual_candidate(visual_candidate_id=selected.visual_candidate_id, actor_id=actor_id)
        scores = [self.repository.scores[item.score_id] for item in candidates]
        licenses = [self.repository.licensing_decisions[item.license_decision_id] for item in candidates]
        rejected = self._rejected_reasons(candidates, selected)
        alternatives = [
            item.visual_candidate_id
            for item in candidates
            if item.visual_candidate_id != selected.visual_candidate_id and item.use_mode != CandidateUseMode.blocked
        ]
        manifest_hash = visual_research_hash(
            {
                "query": query.model_dump(mode="json"),
                "selected": selected.model_dump(mode="json"),
                "alternatives": [str(item) for item in alternatives],
                "rejected": rejected,
                "route": downstream_render_route,
            }
        )
        manifest = self.repository.put_manifest(
            AssetResearchManifest(
                schema_version="cmf.asset_research_manifest.v1",
                asset_research_manifest_id=uuid4(),
                visual_research_query_id=query.visual_research_query_id,
                scene_spec_id=query.scene_spec_id,
                asset_roll_role=query.asset_roll_role,
                selected_candidate_id=selected.visual_candidate_id,
                alternative_candidate_ids=alternatives,
                rejected_candidate_reasons=rejected,
                selected_use_mode=selected.use_mode,
                downstream_render_route=downstream_render_route,
                scoring_receipt_refs=[item.score_id for item in scores],
                license_decision_refs=[item.licensing_decision_id for item in licenses],
                manifest_hash=manifest_hash,
                written_at=utc_now(),
            )
        )
        image_map = self.repository.put_image_resolution_map(self._image_map(manifest, selected, downstream_render_route))
        self._attach_to_render_contract(manifest, image_map)
        receipt = self.repository.put_receipt(
            new_asset_research_receipt(
                query=query,
                candidates=candidates,
                scores=scores,
                licenses=licenses,
                manifest=manifest,
                image_map=image_map,
                actor_id=actor_id,
                decision_code="ASSET_RESEARCH_MANIFEST_WRITTEN",
                evidence_refs=[
                    manifest.manifest_hash,
                    image_map.map_hash,
                    selected.source_url_or_ref,
                    selected.provider_route,
                    query.legacy_adapter_route,
                ],
                command_id=command_id,
            )
        )
        return manifest, image_map, receipt

    def _score(self, query: VisualResearchQuery, fields: dict[str, float]) -> VisualCandidateScore:
        known = fields.get("known_person_validity")
        values = [
            float(fields["emotional_mode_match"]),
            float(fields["tribal_cultural_proximity"]),
            float(fields["symbolic_role_fit"]),
            float(fields["visual_congruence"]),
            float(fields["authenticity"]),
            float(fields["source_quality"]),
            float(fields["brand_alignment"]),
            float(fields.get("source_win_rate", 0.5)),
        ]
        if query.known_person_name:
            values.append(float(known if known is not None else 0.0))
        total = round(sum(values) / len(values), 4)
        return VisualCandidateScore(
            schema_version="cmf.visual_candidate_score.v1",
            score_id=uuid4(),
            visual_research_query_id=query.visual_research_query_id,
            emotional_mode_match=fields["emotional_mode_match"],
            tribal_cultural_proximity=fields["tribal_cultural_proximity"],
            symbolic_role_fit=fields["symbolic_role_fit"],
            visual_congruence=fields["visual_congruence"],
            authenticity=fields["authenticity"],
            source_quality=fields["source_quality"],
            brand_alignment=fields["brand_alignment"],
            known_person_validity=known,
            source_win_rate=fields.get("source_win_rate", 0.5),
            total_score=total,
            scoring_rationale=fields.get(
                "scoring_rationale",
                "Migrated SVRE/Aurore scoring: emotional, cultural, symbolic, authenticity, source, brand, and source win-rate fit.",
            ),
            created_at=utc_now(),
        )

    @staticmethod
    def _use_mode(
        license_decision: LicensingDecision,
        score: VisualCandidateScore,
        query: VisualResearchQuery,
    ) -> CandidateUseMode:
        if query.known_person_name and (score.known_person_validity or 0.0) < 0.75:
            return CandidateUseMode.blocked
        if license_decision.direct_use_allowed:
            return CandidateUseMode.direct_use
        if license_decision.composition_reference_allowed:
            return CandidateUseMode.composition_reference_only
        return CandidateUseMode.blocked

    def _selected_candidate(
        self,
        candidates: list[VisualCandidate],
        selected_candidate_id: UUID | None,
    ) -> VisualCandidate:
        if selected_candidate_id is not None:
            candidate = self._candidate(selected_candidate_id)
            if candidate.use_mode == CandidateUseMode.blocked:
                raise VisualResearchError("VISUAL_CANDIDATE_BLOCKED", "Blocked candidates cannot be selected.")
            return candidate
        selectable = [item for item in candidates if item.use_mode != CandidateUseMode.blocked]
        if not selectable:
            raise VisualResearchError("VISUAL_CANDIDATE_SELECTABLE_REQUIRED", "No candidate passed license/provenance/known-person gates.")
        return sorted(
            selectable,
            key=lambda item: (
                1 if item.use_mode == CandidateUseMode.direct_use else 0,
                self.repository.scores[item.score_id].total_score,
            ),
            reverse=True,
        )[0]

    def _rejected_reasons(self, candidates: list[VisualCandidate], selected: VisualCandidate) -> dict[str, str]:
        reasons: dict[str, str] = {}
        for candidate in candidates:
            if candidate.visual_candidate_id == selected.visual_candidate_id:
                continue
            license_decision = self.repository.licensing_decisions[candidate.license_decision_id]
            if candidate.use_mode == CandidateUseMode.blocked:
                reasons[str(candidate.visual_candidate_id)] = ", ".join(license_decision.blocker_codes) or "known_person_or_license_gate_failed"
            else:
                reasons[str(candidate.visual_candidate_id)] = "lower_svre_aurore_score_or_less_direct_use_fit"
        return reasons

    def _image_map(
        self,
        manifest: AssetResearchManifest,
        selected: VisualCandidate,
        downstream_render_route: str,
    ) -> ImageResolutionMap:
        direct_uri = selected.candidate_uri if selected.use_mode == CandidateUseMode.direct_use else None
        reference_uri = selected.candidate_uri if selected.use_mode == CandidateUseMode.composition_reference_only else None
        steps = [
            "svre_aurore_scoring_migrated_to_contracts",
            "license_provenance_asset_roll_gate_passed",
            f"use_mode:{selected.use_mode.value}",
            f"downstream_render_route:{downstream_render_route}",
        ]
        map_hash = visual_research_hash(
            {
                "manifest": manifest.asset_research_manifest_id,
                "selected": selected.visual_candidate_id,
                "mode": selected.use_mode.value,
                "direct_uri": direct_uri,
                "reference_uri": reference_uri,
                "route": downstream_render_route,
            }
        )
        return ImageResolutionMap(
            schema_version="cmf.image_resolution_map.v1",
            image_resolution_map_id=uuid4(),
            asset_research_manifest_id=manifest.asset_research_manifest_id,
            selected_candidate_id=selected.visual_candidate_id,
            selected_use_mode=selected.use_mode,
            source_url_or_ref=selected.source_url_or_ref,
            direct_use_asset_uri=direct_uri,
            composition_reference_uri=reference_uri,
            downstream_render_route=downstream_render_route,
            provider_route=selected.provider_route,
            resolution_steps=steps,
            map_hash=map_hash,
            created_at=utc_now(),
        )

    def _attach_to_render_contract(self, manifest: AssetResearchManifest, image_map: ImageResolutionMap) -> None:
        if self.scene_spec_compiler is None:
            return
        try:
            contract = self.scene_spec_compiler.render_contract_for_scene(manifest.scene_spec_id)
        except Exception:
            return
        updated_props = {
            **contract.renderer_props,
            "asset_research_manifest_id": str(manifest.asset_research_manifest_id),
            "image_resolution_map_id": str(image_map.image_resolution_map_id),
            "selected_visual_candidate_id": str(manifest.selected_candidate_id),
            "selected_visual_candidate_use_mode": manifest.selected_use_mode.value,
        }
        updated = RenderContract(
            **contract.model_copy(update={"renderer_props": updated_props}).model_dump()
        )
        self.scene_spec_compiler.repository.put_render_contract(updated)

    def _validate_current_provider_route(self, provider_route: str) -> None:
        if provider_route in BLOCKED_LEGACY_EXECUTION_ROUTES:
            raise VisualResearchError("LEGACY_EXECUTION_ROUTE_BLOCKED", "SVRE/Aurore legacy execution services are migration sources only.")
        capability = self.provider_operations.repository.capabilities.get(provider_route)
        if capability is None or not capability.active:
            raise VisualResearchError("CURRENT_PROVIDER_ROUTE_REQUIRED", "Visual research must route through a current active CMF provider capability.")

    def _query(self, visual_research_query_id: UUID) -> VisualResearchQuery:
        query = self.repository.queries.get(visual_research_query_id)
        if query is None:
            raise VisualResearchError("VISUAL_RESEARCH_QUERY_REQUIRED", "VisualResearchQuery is required.")
        return query

    def _license(self, licensing_decision_id: UUID) -> LicensingDecision:
        decision = self.repository.licensing_decisions.get(licensing_decision_id)
        if decision is None:
            raise VisualResearchError("LICENSING_DECISION_REQUIRED", "LicensingDecision is required.")
        return decision

    def _candidate(self, visual_candidate_id: UUID) -> VisualCandidate:
        candidate = self.repository.candidates.get(visual_candidate_id)
        if candidate is None:
            raise VisualResearchError("VISUAL_CANDIDATE_REQUIRED", "VisualCandidate is required.")
        return candidate


@dataclass
class VisualResearchCommandHandler:
    command_type: str
    service: VisualResearchService
    aggregate_type: str = "visual_research"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "CreateVisualResearchQueryCommand":
            return self.service.create_visual_research_query(
                scene_spec_id=UUID(payload["scene_spec_id"]),
                asset_roll_role=payload["asset_roll_role"],
                emotional_state=payload["emotional_state"],
                symbolic_role=payload["symbolic_role"],
                contradiction_value=payload.get("contradiction_value"),
                brand_alignment_constraints=payload["brand_alignment_constraints"],
                source_constraints=payload["source_constraints"],
                licensing_requirements=payload["licensing_requirements"],
                query_terms=payload["query_terms"],
                known_person_name=payload.get("known_person_name"),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "RecordLicensingDecisionCommand":
            return self.service.record_licensing_decision(
                visual_research_query_id=UUID(payload["visual_research_query_id"]),
                source_url_or_ref=payload["source_url_or_ref"],
                license_tier=payload["license_tier"],
                provenance_summary=payload.get("provenance_summary", ""),
                direct_use_requested=bool(payload.get("direct_use_requested", True)),
                attribution_required=bool(payload.get("attribution_required", False)),
                evidence_refs=payload.get("evidence_refs", []),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "ScoreVisualCandidateCommand":
            return self.service.score_visual_candidate(
                visual_research_query_id=UUID(payload["visual_research_query_id"]),
                source_url_or_ref=payload["source_url_or_ref"],
                candidate_uri=payload.get("candidate_uri"),
                provenance_summary=payload.get("provenance_summary", ""),
                licensing_decision_id=UUID(payload["licensing_decision_id"]),
                provider_route=payload["provider_route"],
                score_fields=payload["score_fields"],
                superseded_legacy_logic_refs=payload.get("superseded_legacy_logic_refs"),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "RunAssetResearchCommand":
            return self.service.run_asset_research(
                visual_research_query_id=UUID(payload["visual_research_query_id"]),
                candidates=payload["candidates"],
                downstream_render_route=payload["downstream_render_route"],
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "SelectVisualCandidateCommand":
            return self.service.select_visual_candidate(
                visual_candidate_id=UUID(payload["visual_candidate_id"]),
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "WriteAssetResearchManifestCommand":
            _manifest, _image_map, receipt = self.service.write_asset_research_manifest(
                visual_research_query_id=UUID(payload["visual_research_query_id"]),
                selected_candidate_id=UUID(payload["selected_candidate_id"]) if payload.get("selected_candidate_id") else None,
                downstream_render_route=payload["downstream_render_route"],
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            )
            return receipt.model_dump(mode="json")
        raise VisualResearchError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("visual_research_query_id") or payload.get("visual_candidate_id") or payload.get("asset_research_manifest_id") or payload.get("scene_spec_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_visual_research_command_handlers(bus: CommandBus, service: VisualResearchService) -> None:
    for command_type in [
        "CreateVisualResearchQueryCommand",
        "RunAssetResearchCommand",
        "ScoreVisualCandidateCommand",
        "RecordLicensingDecisionCommand",
        "SelectVisualCandidateCommand",
        "WriteAssetResearchManifestCommand",
    ]:
        bus.register_handler(VisualResearchCommandHandler(command_type=command_type, service=service))
