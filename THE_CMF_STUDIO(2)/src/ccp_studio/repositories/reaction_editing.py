"""Reaction editing template repositories."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.reaction_editing import (
    ReactionEditingTemplate,
    ReactionTemplateRoute,
    ReactionTemplateRouteReceipt,
)


@dataclass
class InMemoryReactionEditingRepository:
    templates: dict[str, ReactionEditingTemplate] = field(default_factory=dict)
    routes: dict[UUID, ReactionTemplateRoute] = field(default_factory=dict)
    receipts: dict[UUID, ReactionTemplateRouteReceipt] = field(default_factory=dict)

    def put_template(self, template: ReactionEditingTemplate) -> ReactionEditingTemplate:
        self.templates[template.template_code.value] = template
        return template

    def put_route(self, route: ReactionTemplateRoute) -> ReactionTemplateRoute:
        self.routes[route.reaction_template_route_id] = route
        return route

    def put_receipt(self, receipt: ReactionTemplateRouteReceipt) -> ReactionTemplateRouteReceipt:
        self.receipts[receipt.reaction_template_route_receipt_id] = receipt
        return receipt
