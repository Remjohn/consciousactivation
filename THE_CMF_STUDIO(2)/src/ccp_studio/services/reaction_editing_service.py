"""Reaction editing template routing service."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.reaction_editing import (
    ReactionEditingTemplate,
    ReactionEditingTemplateCode,
    ReactionTemplateRoute,
    ReactionTemplateRouteReceipt,
    default_reaction_editing_templates,
    new_reaction_template_route_receipt,
    reaction_template_registry_version,
)
from ccp_studio.repositories.reaction_editing import InMemoryReactionEditingRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.routing_service import RoutingService


class ReactionEditingTemplateError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class ReactionEditingTemplateService:
    routing_service: RoutingService
    repository: InMemoryReactionEditingRepository = field(default_factory=InMemoryReactionEditingRepository)

    def __post_init__(self) -> None:
        if not self.repository.templates:
            for template in default_reaction_editing_templates():
                self.repository.put_template(template)

    def list_templates(self) -> list[ReactionEditingTemplate]:
        return [template for template in self.repository.templates.values() if template.active]

    def plan_template_route(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        asset_route_receipt_id: UUID,
        actor_id: UUID,
        requested_template_code: str | None = None,
        content_format_code: str | None = None,
    ) -> ReactionTemplateRouteReceipt:
        route_receipt = self.routing_service.repository.receipts.get(asset_route_receipt_id)
        if route_receipt is None:
            raise ReactionEditingTemplateError("ASSET_ROUTE_RECEIPT_REQUIRED", "Reaction template routing requires an AssetRouteReceipt.")
        if route_receipt.organization_id != organization_id or route_receipt.brand_id != brand_id:
            raise ReactionEditingTemplateError("BRAND_SCOPE_VIOLATION", "Route receipt is outside active brand scope.")
        if route_receipt.decision_code != "ASSET_ROUTE_ACCEPTED" or not route_receipt.accepted_route_ids:
            return self._blocked_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_moment_id=route_receipt.expression_moment_id,
                asset_route_receipt_id=asset_route_receipt_id,
                actor_id=actor_id,
                decision_code="REACTION_TEMPLATE_ROUTE_BLOCKED",
                summary="Only accepted source-backed route receipts can select reaction editing templates.",
            )
        moment = self.routing_service.expression_review_service.assert_can_route_expression_moment(route_receipt.expression_moment_id)
        if moment.brand_id != brand_id:
            raise ReactionEditingTemplateError("BRAND_SCOPE_VIOLATION", "Expression Moment is outside active brand scope.")
        template = self._select_template(
            requested_template_code=requested_template_code,
            content_format_code=content_format_code,
            requested_format=route_receipt.requested_format,
        )
        resolved_format_code = self._resolve_content_format_code(template, content_format_code)
        registry_version = reaction_template_registry_version(self.list_templates())
        route_id = uuid4()
        scene_patch = {
            "reaction_template_route_id": str(route_id),
            "reaction_template_code": template.template_code.value,
            "content_format_code": resolved_format_code,
            "renderer_route": template.motion_grammar.renderer_route,
            "composition_id": template.motion_grammar.composition_id,
            "scene_pattern": template.motion_grammar.scene_pattern,
            "live_clip_slots": [slot.model_dump(mode="json") for slot in template.live_clip_slots],
            "motion_grammar": template.motion_grammar.model_dump(mode="json"),
            "primitive_eval_obligations": template.primitive_eval_obligations,
        }
        source_support = [
            f"expression_moment:{moment.expression_moment_id}",
            f"asset_route_receipt:{asset_route_receipt_id}",
            *route_receipt.source_support_evidence,
        ]
        route = self.repository.put_route(
            ReactionTemplateRoute(
                reaction_template_route_id=route_id,
                organization_id=organization_id,
                brand_id=brand_id,
                expression_moment_id=moment.expression_moment_id,
                asset_route_receipt_id=asset_route_receipt_id,
                template_code=template.template_code,
                content_format_code=resolved_format_code,
                source_support_evidence=source_support,
                live_clip_slot_specs=template.live_clip_slots,
                scene_spec_requirement_patch=scene_patch,
                created_at=moment.created_at,
            )
        )
        return self.repository.put_receipt(
            new_reaction_template_route_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_moment_id=moment.expression_moment_id,
                asset_route_receipt_id=asset_route_receipt_id,
                reaction_template_route_id=route.reaction_template_route_id,
                template_code=template.template_code,
                content_format_code=resolved_format_code,
                registry_version=registry_version,
                decision_code="REACTION_TEMPLATE_ROUTE_ACCEPTED",
                source_support_evidence=source_support,
                live_clip_slot_keys=[slot.slot_key for slot in template.live_clip_slots],
                scene_spec_requirement_patch=scene_patch,
                evaluator_summary=(
                    "Approved live Expression Moment mapped to a governed reaction editing template. "
                    "The template supplies live-clip slot needs and renderer motion grammar."
                ),
                actor_id=actor_id,
            )
        )

    def _blocked_receipt(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_moment_id: UUID,
        asset_route_receipt_id: UUID,
        actor_id: UUID,
        decision_code: str,
        summary: str,
    ) -> ReactionTemplateRouteReceipt:
        return self.repository.put_receipt(
            new_reaction_template_route_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_moment_id=expression_moment_id,
                asset_route_receipt_id=asset_route_receipt_id,
                registry_version=reaction_template_registry_version(self.list_templates()),
                decision_code=decision_code,
                evaluator_summary=summary,
                actor_id=actor_id,
            )
        )

    def _select_template(
        self,
        *,
        requested_template_code: str | None,
        content_format_code: str | None,
        requested_format: str | None,
    ) -> ReactionEditingTemplate:
        active = self.list_templates()
        if requested_template_code:
            normalized_code = requested_template_code.upper().replace("_", "-").strip()
            for template in active:
                if template.template_code.value == normalized_code:
                    return template
            raise ReactionEditingTemplateError("REACTION_TEMPLATE_NOT_REGISTERED", "Requested reaction editing template is not active.")
        cues = " ".join(item for item in [content_format_code, requested_format] if item).lower().replace("_", " ").replace("-", " ")
        for template in active:
            if content_format_code and content_format_code in template.valid_content_format_codes:
                if any(alias in cues for alias in template.alias_terms) or not requested_format:
                    return template
            if any(alias in cues for alias in template.alias_terms):
                return template
        for template in active:
            if template.template_code == ReactionEditingTemplateCode.versus_split:
                return template
        raise ReactionEditingTemplateError("REACTION_TEMPLATE_REGISTRY_EMPTY", "No active reaction editing templates are registered.")

    @staticmethod
    def _resolve_content_format_code(template: ReactionEditingTemplate, content_format_code: str | None) -> str:
        if content_format_code:
            if content_format_code not in template.valid_content_format_codes:
                raise ReactionEditingTemplateError("CONTENT_FORMAT_TEMPLATE_MISMATCH", "Content format is not allowed for the selected reaction template.")
            return content_format_code
        return template.valid_content_format_codes[0]


@dataclass
class ReactionEditingTemplateCommandHandler:
    command_type: str
    service: ReactionEditingTemplateService
    aggregate_type: str = "reaction_template_route"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "PlanReactionTemplateRouteCommand":
            return self.service.plan_template_route(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                asset_route_receipt_id=UUID(payload["asset_route_receipt_id"]),
                actor_id=envelope.actor.actor_id,
                requested_template_code=payload.get("requested_template_code"),
                content_format_code=payload.get("content_format_code"),
            ).model_dump(mode="json")
        if self.command_type == "ListReactionEditingTemplatesCommand":
            return {"templates": [item.model_dump(mode="json") for item in self.service.list_templates()]}
        raise ReactionEditingTemplateError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("reaction_template_route_id") or payload.get("asset_route_receipt_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_reaction_editing_template_command_handlers(bus: CommandBus, service: ReactionEditingTemplateService) -> None:
    for command_type in ["PlanReactionTemplateRouteCommand", "ListReactionEditingTemplatesCommand"]:
        bus.register_handler(ReactionEditingTemplateCommandHandler(command_type=command_type, service=service))
