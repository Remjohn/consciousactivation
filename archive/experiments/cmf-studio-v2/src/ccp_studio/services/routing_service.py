"""Archetype and asset derivative routing service for TS-CMF-033."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.expression_review import ExpressionMoment
from ccp_studio.contracts.registry import RegistryEntry, RegistryFamily, RegistryStatus
from ccp_studio.contracts.routing import (
    AssetRouteReceipt,
    RouteDecision,
    RouteRegistryType,
    RouteSelectionCandidate,
    registry_bundle_version_for,
    new_archetype_route,
    new_asset_route_receipt,
    new_unsupported_format_rejection,
)
from ccp_studio.dspy_programs.route_selection import RouteSelectionProgram
from ccp_studio.repositories.routing import InMemoryRoutingRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.expression_review_service import ExpressionReviewService
from ccp_studio.services.registry_service import RegistryService


UNSUPPORTED_FORMAT_TERMS = {"newsletter", "newsletters", "email newsletter", "newsletter package"}


class RoutingServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class RoutingService:
    expression_review_service: ExpressionReviewService
    registry_service: RegistryService
    repository: InMemoryRoutingRepository = field(default_factory=InMemoryRoutingRepository)
    route_selection_program: RouteSelectionProgram = field(default_factory=RouteSelectionProgram)

    def route_expression_moment(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_moment_id: UUID,
        actor_id: UUID,
        requested_format: str | None = None,
    ) -> AssetRouteReceipt:
        moment = self.expression_review_service.assert_can_route_expression_moment(expression_moment_id)
        if moment.brand_id != brand_id:
            raise RoutingServiceError("BRAND_SCOPE_VIOLATION", "Expression Moment is outside active brand scope.")
        active_entries = self._active_entries_by_type()
        registry_refs = [f"registry_entry:{entry.registry_entry_id}" for entries in active_entries.values() for entry in entries]
        registry_bundle_version = registry_bundle_version_for(registry_refs)
        unsupported_reason = self._unsupported_format_reason(requested_format, active_entries)
        if unsupported_reason:
            return self._write_unsupported_format_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                moment=moment,
                actor_id=actor_id,
                requested_format=requested_format or "",
                reason=unsupported_reason,
                registry_bundle_version=registry_bundle_version,
                registry_refs=registry_refs,
            )
        self._require_route_registry_set(active_entries)
        route_candidate = self.route_selection_program.select(
            expression_moment=moment,
            registry_bundle_version=registry_bundle_version,
            active_entries_by_type=active_entries,
            requested_format=requested_format,
        )
        self.repository.put_route_selection_candidate(route_candidate)
        support_failure = self._source_support_failure(moment, route_candidate, active_entries)
        if support_failure:
            route = self.repository.put_route(
                new_archetype_route(
                    expression_moment_id=moment.expression_moment_id,
                    route_refs=route_candidate.route_refs,
                    source_support_evidence=route_candidate.source_support_evidence,
                    route_rationale=support_failure,
                    route_fit_score=min(route_candidate.route_fit_score, 0.42),
                    failure_alternatives=route_candidate.failure_alternatives,
                    decision=RouteDecision.rejected_source_unsupported,
                )
            )
            return self.repository.put_receipt(
                new_asset_route_receipt(
                    organization_id=organization_id,
                    brand_id=brand_id,
                    expression_moment_id=moment.expression_moment_id,
                    requested_format=requested_format,
                    rejected_route_ids=[route.archetype_route_id],
                    registry_bundle_version=registry_bundle_version,
                    registry_entry_refs=route_candidate.route_refs.all_refs(),
                    source_support_evidence=route_candidate.source_support_evidence,
                    route_rationale=support_failure,
                    route_fit_score=route.route_fit_score,
                    failure_alternatives=route.failure_alternatives,
                    evaluator_summary="Route rejected because source support was insufficient.",
                    decision_code="ROUTE_REJECTED_SOURCE_UNSUPPORTED",
                    package_planning_refs=[],
                    reviewer_actor_id=actor_id,
                )
            )
        route = self.repository.put_route(
            new_archetype_route(
                expression_moment_id=moment.expression_moment_id,
                route_refs=route_candidate.route_refs,
                source_support_evidence=route_candidate.source_support_evidence,
                route_rationale=route_candidate.route_rationale,
                route_fit_score=route_candidate.route_fit_score,
                failure_alternatives=route_candidate.failure_alternatives,
                decision=RouteDecision.accepted,
            )
        )
        return self.repository.put_receipt(
            new_asset_route_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_moment_id=moment.expression_moment_id,
                requested_format=requested_format,
                accepted_route_ids=[route.archetype_route_id],
                registry_bundle_version=registry_bundle_version,
                registry_entry_refs=route.route_refs.all_refs(),
                source_support_evidence=route.source_support_evidence,
                route_rationale=route.route_rationale,
                route_fit_score=route.route_fit_score,
                failure_alternatives=route.failure_alternatives,
                evaluator_summary="Route accepted through active migrated CMF registries.",
                decision_code="ASSET_ROUTE_ACCEPTED",
                package_planning_refs=[f"asset_package_spec_input:asset_route_receipt:{route.archetype_route_id}"],
                reviewer_actor_id=actor_id,
            )
        )

    def reject_unsupported_format(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_moment_id: UUID,
        actor_id: UUID,
        requested_format: str,
        reason: str | None = None,
    ) -> AssetRouteReceipt:
        moment = self.expression_review_service.assert_can_route_expression_moment(expression_moment_id)
        active_entries = self._active_entries_by_type()
        registry_refs = [f"registry_entry:{entry.registry_entry_id}" for entries in active_entries.values() for entry in entries]
        return self._write_unsupported_format_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            moment=moment,
            actor_id=actor_id,
            requested_format=requested_format,
            reason=reason or "Requested format is not an active CMF registry route.",
            registry_bundle_version=registry_bundle_version_for(registry_refs),
            registry_refs=registry_refs,
        )

    def reject_source_route(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_moment_id: UUID,
        actor_id: UUID,
        requested_format: str | None,
        reason: str,
    ) -> AssetRouteReceipt:
        moment = self.expression_review_service.assert_can_route_expression_moment(expression_moment_id)
        active_entries = self._active_entries_by_type()
        self._require_route_registry_set(active_entries)
        registry_refs = [f"registry_entry:{entry.registry_entry_id}" for entries in active_entries.values() for entry in entries]
        registry_bundle_version = registry_bundle_version_for(registry_refs)
        route_candidate = self.route_selection_program.select(
            expression_moment=moment,
            registry_bundle_version=registry_bundle_version,
            active_entries_by_type=active_entries,
            requested_format=requested_format,
        )
        route = self.repository.put_route(
            new_archetype_route(
                expression_moment_id=moment.expression_moment_id,
                route_refs=route_candidate.route_refs,
                source_support_evidence=route_candidate.source_support_evidence,
                route_rationale=reason,
                route_fit_score=0.25,
                failure_alternatives=route_candidate.failure_alternatives,
                decision=RouteDecision.rejected_source_unsupported,
            )
        )
        return self.repository.put_receipt(
            new_asset_route_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_moment_id=moment.expression_moment_id,
                requested_format=requested_format,
                rejected_route_ids=[route.archetype_route_id],
                registry_bundle_version=registry_bundle_version,
                registry_entry_refs=route.route_refs.all_refs(),
                source_support_evidence=route.source_support_evidence,
                route_rationale=reason,
                route_fit_score=route.route_fit_score,
                failure_alternatives=route.failure_alternatives,
                evaluator_summary="Route rejected by explicit source-support guard.",
                decision_code="ROUTE_REJECTED_SOURCE_UNSUPPORTED",
                reviewer_actor_id=actor_id,
            )
        )

    def latest_receipt_for_moment(self, expression_moment_id: UUID) -> AssetRouteReceipt | None:
        return next(
            (
                receipt
                for receipt in reversed(list(self.repository.receipts.values()))
                if receipt.expression_moment_id == expression_moment_id
            ),
            None,
        )

    def _write_unsupported_format_receipt(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        moment: ExpressionMoment,
        actor_id: UUID,
        requested_format: str,
        reason: str,
        registry_bundle_version: str,
        registry_refs: list[str],
    ) -> AssetRouteReceipt:
        rejection = self.repository.put_unsupported_format_rejection(
            new_unsupported_format_rejection(
                expression_moment_id=moment.expression_moment_id,
                requested_format=requested_format,
                reason=reason,
                evidence_refs=[f"expression_moment:{moment.expression_moment_id}", *registry_refs],
            )
        )
        return self.repository.put_receipt(
            new_asset_route_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_moment_id=moment.expression_moment_id,
                requested_format=requested_format,
                unsupported_format_rejection_ids=[rejection.unsupported_format_rejection_id],
                registry_bundle_version=registry_bundle_version,
                registry_entry_refs=registry_refs,
                source_support_evidence=[f"expression_moment:{moment.expression_moment_id}"],
                route_rationale=reason,
                route_fit_score=0.0,
                failure_alternatives=["choose an active CMF asset derivative", "route to review-only memory candidate"],
                evaluator_summary="Unsupported format rejected before package planning.",
                decision_code="ROUTE_REJECTED_UNSUPPORTED_FORMAT",
                package_planning_refs=[],
                reviewer_actor_id=actor_id,
            )
        )

    def _active_entries_by_type(self) -> dict[RouteRegistryType, list[RegistryEntry]]:
        entries_by_type: dict[RouteRegistryType, list[RegistryEntry]] = {item: [] for item in RouteRegistryType}
        for entry in self.registry_service.repository.registry_entries.values():
            if entry.status != RegistryStatus.active:
                continue
            route_type = self._route_type_for(entry)
            if route_type is not None:
                entries_by_type[route_type].append(entry)
        return entries_by_type

    @staticmethod
    def _route_type_for(entry: RegistryEntry) -> RouteRegistryType | None:
        raw = entry.payload.get("registry_type") or entry.payload.get("new_registry_type")
        if raw is None and entry.registry_family == RegistryFamily.archetype:
            raw = RouteRegistryType.core_content_archetype.value
        if raw is None and entry.registry_family == RegistryFamily.creative_subsystem:
            raw = RouteRegistryType.cmf_render_mode.value
        normalized = str(raw).lower().replace(" ", "_").replace("-", "_")
        aliases = {
            "core_content_archetype_schema": RouteRegistryType.core_content_archetype,
            "core_content_archetype": RouteRegistryType.core_content_archetype,
            "asset_derivative_schema": RouteRegistryType.asset_derivative,
            "asset_derivative": RouteRegistryType.asset_derivative,
            "meme_mechanism_schema": RouteRegistryType.meme_mechanism,
            "meme_mechanism": RouteRegistryType.meme_mechanism,
            "reaction_archetype_schema": RouteRegistryType.reaction_archetype,
            "reaction_archetype": RouteRegistryType.reaction_archetype,
            "cmf_render_mode_schema": RouteRegistryType.cmf_render_mode,
            "cmf_render_mode": RouteRegistryType.cmf_render_mode,
        }
        return aliases.get(normalized)

    @staticmethod
    def _require_route_registry_set(active_entries: dict[RouteRegistryType, list[RegistryEntry]]) -> None:
        missing = [
            item.value
            for item in [RouteRegistryType.core_content_archetype, RouteRegistryType.asset_derivative, RouteRegistryType.cmf_render_mode]
            if not active_entries.get(item)
        ]
        if missing:
            raise RoutingServiceError("ACTIVE_ROUTE_REGISTRY_REQUIRED", f"Missing active route registries: {', '.join(missing)}")

    @staticmethod
    def _unsupported_format_reason(
        requested_format: str | None,
        active_entries: dict[RouteRegistryType, list[RegistryEntry]],
    ) -> str | None:
        if requested_format is None:
            return None
        normalized = requested_format.lower().replace("_", " ").replace("-", " ").strip()
        if normalized in UNSUPPORTED_FORMAT_TERMS or "newsletter" in normalized:
            return "Newsletters are not CMF deliverables and cannot be routed."
        route_names: set[str] = set()
        for entry in [
            *active_entries.get(RouteRegistryType.asset_derivative, []),
            *active_entries.get(RouteRegistryType.cmf_render_mode, []),
        ]:
            names = [
                str(entry.payload.get("name", "")),
                str(entry.payload.get("format_key", "")),
                str(entry.payload.get("deliverable_format", "")),
                *[str(item) for item in entry.payload.get("aliases", [])],
            ]
            route_names.update(name.lower().replace("_", " ").replace("-", " ").strip() for name in names if name)
        if route_names and normalized not in route_names:
            return f"Requested format '{requested_format}' is not an active migrated CMF route."
        return None

    @staticmethod
    def _source_support_failure(
        moment: ExpressionMoment,
        route_candidate: RouteSelectionCandidate,
        active_entries: dict[RouteRegistryType, list[RegistryEntry]],
    ) -> str | None:
        if len(moment.source_quote.split()) < 5:
            return "Expression Moment quote is too thin to support a routed deliverable."
        quote_lower = moment.source_quote.lower()
        required_terms: list[str] = []
        for entries in active_entries.values():
            for entry in entries:
                required_terms.extend(str(item).lower() for item in entry.payload.get("required_source_terms", []))
        if required_terms and not any(term in quote_lower for term in required_terms):
            return "Expression Moment lacks the required source terms for the requested route."
        if not route_candidate.source_support_evidence:
            return "Route selection produced no source-support evidence."
        return None


@dataclass
class RoutingCommandHandler:
    command_type: str
    service: RoutingService
    aggregate_type: str = "archetype_route"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "reviewer"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type in {"RouteExpressionMomentCommand", "ApproveArchetypeRouteCommand"}:
            return self.service.route_expression_moment(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_moment_id=UUID(payload["expression_moment_id"]),
                requested_format=payload.get("requested_format"),
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "RejectUnsupportedFormatCommand":
            return self.service.reject_unsupported_format(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_moment_id=UUID(payload["expression_moment_id"]),
                requested_format=payload["requested_format"],
                reason=payload.get("reason"),
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "RejectUnsupportedSourceRouteCommand":
            return self.service.reject_source_route(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_moment_id=UUID(payload["expression_moment_id"]),
                requested_format=payload.get("requested_format"),
                reason=payload["reason"],
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "WriteAssetRouteReceiptCommand":
            receipt = self.service.latest_receipt_for_moment(UUID(payload["expression_moment_id"]))
            if receipt is None:
                raise RoutingServiceError("ASSET_ROUTE_RECEIPT_REQUIRED", "No route receipt exists for this moment.")
            return receipt.model_dump(mode="json")
        raise RoutingServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("expression_moment_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_routing_command_handlers(bus: CommandBus, service: RoutingService) -> None:
    for command_type in [
        "RouteExpressionMomentCommand",
        "RejectUnsupportedFormatCommand",
        "RejectUnsupportedSourceRouteCommand",
        "ApproveArchetypeRouteCommand",
        "WriteAssetRouteReceiptCommand",
    ]:
        bus.register_handler(RoutingCommandHandler(command_type=command_type, service=service))
