"""Guest Asset Pack spec generation service for TS-CMF-034."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.asset_package import (
    TARGET_TRIAL_GUEST_PACK_COUNTS,
    AssetPackageItem,
    AssetPackageSpec,
    AssetPackageStatus,
    CompleteEditingSessionRequestCandidate,
    PackageGap,
    PackageItemStatus,
    PackageItemType,
    PackageSpecReceipt,
    ReactionSeed,
    new_asset_package_item,
    new_package_gap,
    new_package_spec_receipt,
)
from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.commercial import EntitlementStatus, PublicContentOffer
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.routing import AssetRouteReceipt
from ccp_studio.repositories.asset_package import InMemoryAssetPackageRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.commercial_policy_service import CommercialPolicyError, CommercialPolicyService
from ccp_studio.services.routing_service import RoutingService


ITEM_FORMAT_ALIASES: dict[PackageItemType, set[str]] = {
    PackageItemType.short_video: {"short video", "video", "paper cut explainer", "myth debunk", "conceptual contrast"},
    PackageItemType.carousel: {"carousel", "relief peak carousel"},
    PackageItemType.meme_visual: {"meme visual", "meme", "meme observation"},
    PackageItemType.poll_visual: {"poll visual", "poll"},
    PackageItemType.reaction_seed: {"reaction seed", "validation reaction", "solo reaction"},
}


class AssetPackageServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class AssetPackageService:
    routing_service: RoutingService
    commercial_policy_service: CommercialPolicyService
    repository: InMemoryAssetPackageRepository = field(default_factory=InMemoryAssetPackageRepository)

    def generate_trial_guest_asset_pack_spec(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_session_id: UUID,
        asset_route_receipt_ids: list[UUID],
        actor_id: UUID,
    ) -> AssetPackageSpec:
        entitlement = self.commercial_policy_service.repository.get_entitlement(organization_id, brand_id)
        if entitlement is None:
            raise AssetPackageServiceError("COMMERCIAL_ENTITLEMENT_REQUIRED", "Trial pack generation requires entitlement.")
        if entitlement.status != EntitlementStatus.active:
            raise AssetPackageServiceError("COMMERCIAL_ENTITLEMENT_NOT_ACTIVE", "Entitlement must be active.")
        if entitlement.public_offer != PublicContentOffer.trial_guest_asset_pack:
            raise AssetPackageServiceError("TRIAL_GUEST_PACK_ENTITLEMENT_REQUIRED", "Trial Guest Asset Pack entitlement is required.")
        price_label = self.commercial_policy_service.render_public_offer_copy(PublicContentOffer.trial_guest_asset_pack)
        self.commercial_policy_service.validate_public_copy(price_label)
        route_receipts = self._route_receipts(asset_route_receipt_ids)
        items: list[AssetPackageItem] = []
        gaps: list[PackageGap] = []
        available_receipts = list(route_receipts)
        for item_type, count in TARGET_TRIAL_GUEST_PACK_COUNTS.items():
            for _index in range(count):
                receipt = self._take_supported_receipt(available_receipts, item_type)
                if receipt is None:
                    gap = self.repository.put_gap(
                        new_package_gap(
                            target_item_type=item_type,
                            reason="Source material does not currently support this package item.",
                            missing_source_requirement=f"accepted route receipt for {item_type.value}",
                            route_attempt_receipt_ids=[item.asset_route_receipt_id for item in route_receipts if item.asset_route_receipt_id],
                        )
                    )
                    gaps.append(gap)
                    items.append(
                        new_asset_package_item(
                            item_type=item_type,
                            production_readiness=PackageItemStatus.source_gap,
                            evaluation_state="source_gap_recorded",
                            source_gap_id=gap.package_gap_id,
                        )
                    )
                    continue
                items.append(
                    new_asset_package_item(
                        item_type=item_type,
                        expression_moment_id=receipt.expression_moment_id,
                        asset_route_receipt_id=receipt.asset_route_receipt_id,
                        registry_refs=receipt.registry_entry_refs,
                        evaluation_state="route_receipt_passed_pending_render_eval",
                        production_readiness=PackageItemStatus.ready_for_editing_session,
                    )
                )
        package_spec_id = uuid4()
        reaction_seeds = [
            self.repository.put_reaction_seed(
                ReactionSeed(
                    schema_version="cmf.reaction_seed.v1",
                    reaction_seed_id=uuid4(),
                    asset_package_spec_id=package_spec_id,
                    package_item_id=item.package_item_id,
                    expression_moment_id=item.expression_moment_id,
                    seed_text="Reaction seed stored from approved routed expression moment.",
                    route_receipt_id=item.asset_route_receipt_id,
                )
            )
            for item in items
            if item.item_type == PackageItemType.reaction_seed
            and item.production_readiness == PackageItemStatus.ready_for_editing_session
            and item.expression_moment_id is not None
            and item.asset_route_receipt_id is not None
        ]
        readiness_status = "ready_for_approval" if not gaps else "source_gaps_recorded"
        ready_counts = self._item_counts(items, PackageItemStatus.ready_for_editing_session)
        gap_counts = self._gap_counts(gaps)
        receipt = self.repository.put_receipt(
            new_package_spec_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                asset_package_spec_id=package_spec_id,
                route_receipt_ids=asset_route_receipt_ids,
                ready_item_counts=ready_counts,
                gap_counts=gap_counts,
                offer_code=PublicContentOffer.trial_guest_asset_pack,
                customer_facing_price_label=price_label,
                readiness_status=readiness_status,
                reviewer_actor_id=actor_id,
            )
        )
        spec = AssetPackageSpec(
            schema_version="cmf.asset_package_spec.v1",
            asset_package_spec_id=package_spec_id,
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
            offer_code=PublicContentOffer.trial_guest_asset_pack,
            customer_facing_price_label=price_label,
            target_item_counts=TARGET_TRIAL_GUEST_PACK_COUNTS,
            items=items,
            gaps=gaps,
            reaction_seeds=reaction_seeds,
            package_spec_receipt_id=receipt.package_spec_receipt_id,
            status=AssetPackageStatus.draft,
            created_at=utc_now(),
        )
        return self.repository.put_spec(spec)

    def evaluate_package_source_sufficiency(
        self,
        *,
        asset_route_receipt_ids: list[UUID],
    ) -> dict[PackageItemType, int]:
        receipts = self._route_receipts(asset_route_receipt_ids)
        counts: Counter[PackageItemType] = Counter()
        available = list(receipts)
        for item_type, count in TARGET_TRIAL_GUEST_PACK_COUNTS.items():
            for _index in range(count):
                receipt = self._take_supported_receipt(available, item_type)
                if receipt is not None:
                    counts[item_type] += 1
        return dict(counts)

    def record_package_gap(
        self,
        *,
        target_item_type: PackageItemType,
        reason: str,
        missing_source_requirement: str,
        route_attempt_receipt_ids: list[UUID],
    ) -> PackageGap:
        return self.repository.put_gap(
            new_package_gap(
                target_item_type=target_item_type,
                reason=reason,
                missing_source_requirement=missing_source_requirement,
                route_attempt_receipt_ids=route_attempt_receipt_ids,
            )
        )

    def approve_asset_package_spec(
        self,
        *,
        asset_package_spec_id: UUID,
        actor_id: UUID,
    ) -> AssetPackageSpec:
        spec = self._spec(asset_package_spec_id)
        approved = spec.model_copy(update={"status": AssetPackageStatus.approved, "approved_at": utc_now()})
        return self.repository.put_spec(approved)

    def prepare_editing_session_requests(
        self,
        *,
        asset_package_spec_id: UUID,
        actor_id: UUID,
    ) -> list[CompleteEditingSessionRequestCandidate]:
        spec = self._spec(asset_package_spec_id)
        if spec.status != AssetPackageStatus.approved:
            raise AssetPackageServiceError("ASSET_PACKAGE_APPROVAL_REQUIRED", "Package must be approved before editing requests.")
        requests: list[CompleteEditingSessionRequestCandidate] = []
        updated_items: list[AssetPackageItem] = []
        for item in spec.items:
            if item.production_readiness != PackageItemStatus.ready_for_editing_session:
                updated_items.append(item)
                continue
            if item.expression_moment_id is None or item.asset_route_receipt_id is None:
                updated_items.append(item)
                continue
            receipt = self.routing_service.repository.receipts[item.asset_route_receipt_id]
            request = self.repository.put_editing_session_request(
                CompleteEditingSessionRequestCandidate(
                    schema_version="cmf.complete_editing_session_request_candidate.v1",
                    complete_editing_session_request_id=uuid4(),
                    asset_package_spec_id=spec.asset_package_spec_id,
                    package_item_id=item.package_item_id,
                    expression_moment_id=item.expression_moment_id,
                    asset_route_receipt_id=item.asset_route_receipt_id,
                    registry_refs=item.registry_refs,
                    brand_context_required=item.brand_context_required,
                    evaluation_state=item.evaluation_state,
                    route_state=receipt.decision_code,
                    source_lineage_refs=[
                        f"expression_moment:{item.expression_moment_id}",
                        f"asset_route_receipt:{item.asset_route_receipt_id}",
                        *receipt.source_support_evidence,
                    ],
                    created_at=utc_now(),
                )
            )
            requests.append(request)
            updated_items.append(item.model_copy(update={"complete_editing_session_request_id": request.complete_editing_session_request_id}))
        self.repository.put_spec(spec.model_copy(update={"items": updated_items}))
        return requests

    def _route_receipts(self, asset_route_receipt_ids: list[UUID]) -> list[AssetRouteReceipt]:
        receipts: list[AssetRouteReceipt] = []
        for receipt_id in asset_route_receipt_ids:
            receipt = self.routing_service.repository.receipts.get(receipt_id)
            if receipt is None:
                raise AssetPackageServiceError("ASSET_ROUTE_RECEIPT_REQUIRED", "Route receipt is required.")
            receipts.append(receipt)
        return receipts

    def _take_supported_receipt(
        self,
        receipts: list[AssetRouteReceipt],
        item_type: PackageItemType,
    ) -> AssetRouteReceipt | None:
        for index, receipt in enumerate(receipts):
            if self._receipt_supports_item(receipt, item_type):
                return receipts.pop(index)
        return None

    @staticmethod
    def _receipt_supports_item(receipt: AssetRouteReceipt, item_type: PackageItemType) -> bool:
        if receipt.decision_code != "ASSET_ROUTE_ACCEPTED":
            return False
        if not receipt.accepted_route_ids or not receipt.source_support_evidence or receipt.route_fit_score < 0.65:
            return False
        if receipt.requested_format is None:
            return True
        normalized = receipt.requested_format.lower().replace("_", " ").replace("-", " ").strip()
        return normalized in ITEM_FORMAT_ALIASES[item_type]

    @staticmethod
    def _item_counts(items: list[AssetPackageItem], status: PackageItemStatus) -> dict[PackageItemType, int]:
        counts: Counter[PackageItemType] = Counter(item.item_type for item in items if item.production_readiness == status)
        return {item_type: counts.get(item_type, 0) for item_type in TARGET_TRIAL_GUEST_PACK_COUNTS}

    @staticmethod
    def _gap_counts(gaps: list[PackageGap]) -> dict[PackageItemType, int]:
        counts: Counter[PackageItemType] = Counter(gap.target_item_type for gap in gaps)
        return {item_type: counts.get(item_type, 0) for item_type in TARGET_TRIAL_GUEST_PACK_COUNTS}

    def _spec(self, asset_package_spec_id: UUID) -> AssetPackageSpec:
        spec = self.repository.specs.get(asset_package_spec_id)
        if spec is None:
            raise AssetPackageServiceError("ASSET_PACKAGE_SPEC_REQUIRED", "AssetPackageSpec is required.")
        return spec


@dataclass
class AssetPackageCommandHandler:
    command_type: str
    service: AssetPackageService
    aggregate_type: str = "asset_package_spec"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "GenerateTrialGuestAssetPackSpecCommand":
            return self.service.generate_trial_guest_asset_pack_spec(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_session_id=UUID(payload["expression_session_id"]),
                asset_route_receipt_ids=[UUID(item) for item in payload["asset_route_receipt_ids"]],
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "EvaluatePackageSourceSufficiencyCommand":
            return {
                key.value: value
                for key, value in self.service.evaluate_package_source_sufficiency(
                    asset_route_receipt_ids=[UUID(item) for item in payload["asset_route_receipt_ids"]]
                ).items()
            }
        if self.command_type == "RecordPackageGapCommand":
            return self.service.record_package_gap(
                target_item_type=PackageItemType(payload["target_item_type"]),
                reason=payload["reason"],
                missing_source_requirement=payload["missing_source_requirement"],
                route_attempt_receipt_ids=[UUID(item) for item in payload.get("route_attempt_receipt_ids", [])],
            ).model_dump(mode="json")
        if self.command_type == "ApproveAssetPackageSpecCommand":
            return self.service.approve_asset_package_spec(
                asset_package_spec_id=UUID(payload["asset_package_spec_id"]),
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "PrepareEditingSessionRequestsCommand":
            return {
                "editing_session_requests": [
                    item.model_dump(mode="json")
                    for item in self.service.prepare_editing_session_requests(
                        asset_package_spec_id=UUID(payload["asset_package_spec_id"]),
                        actor_id=envelope.actor.actor_id,
                    )
                ]
            }
        raise AssetPackageServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("asset_package_spec_id") or payload.get("expression_session_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_asset_package_command_handlers(bus: CommandBus, service: AssetPackageService) -> None:
    for command_type in [
        "GenerateTrialGuestAssetPackSpecCommand",
        "EvaluatePackageSourceSufficiencyCommand",
        "RecordPackageGapCommand",
        "ApproveAssetPackageSpecCommand",
        "PrepareEditingSessionRequestsCommand",
    ]:
        bus.register_handler(AssetPackageCommandHandler(command_type=command_type, service=service))
