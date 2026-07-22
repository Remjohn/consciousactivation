"""Routing repositories for TS-CMF-033."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.routing import (
    ArchetypeRoute,
    AssetRouteReceipt,
    RouteSelectionCandidate,
    UnsupportedFormatRejection,
)


@dataclass
class InMemoryRoutingRepository:
    route_selection_candidates: dict[UUID, RouteSelectionCandidate] = field(default_factory=dict)
    archetype_routes: dict[UUID, ArchetypeRoute] = field(default_factory=dict)
    unsupported_format_rejections: dict[UUID, UnsupportedFormatRejection] = field(default_factory=dict)
    receipts: dict[UUID, AssetRouteReceipt] = field(default_factory=dict)

    def put_route_selection_candidate(self, candidate: RouteSelectionCandidate) -> RouteSelectionCandidate:
        self.route_selection_candidates[candidate.route_selection_candidate_id] = candidate
        return candidate

    def put_route(self, route: ArchetypeRoute) -> ArchetypeRoute:
        self.archetype_routes[route.archetype_route_id] = route
        return route

    def put_unsupported_format_rejection(self, rejection: UnsupportedFormatRejection) -> UnsupportedFormatRejection:
        self.unsupported_format_rejections[rejection.unsupported_format_rejection_id] = rejection
        return rejection

    def put_receipt(self, receipt: AssetRouteReceipt) -> AssetRouteReceipt:
        self.receipts[receipt.asset_route_receipt_id] = receipt
        return receipt
