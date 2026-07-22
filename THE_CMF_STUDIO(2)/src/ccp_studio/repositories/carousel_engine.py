from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class InMemoryCarouselEngineRepository:
    stores: dict[str, dict[str, Any]] = field(default_factory=lambda: {
        "projects": {}, "variants": {}, "source_packets": {}, "sequence_strategies": {},
        "viewer_sequences": {}, "slide_count_decisions": {}, "slide_role_plans": {},
        "claim_maps": {}, "copy_systems": {}, "slide_briefs": {}, "slide_copy_packets": {},
        "asset_requirement_plans": {}, "asset_allocation_plans": {}, "visual_systems": {},
        "style_route_policies": {}, "composition_hypotheses": {}, "composition_decisions": {},
        "sequence_audits": {}, "layer_plans": {}, "provider_blueprints": {}, "render_contracts": {},
        "render_receipts": {}, "eval_receipts": {}, "revision_receipts": {}, "variant_comparison_reports": {},
        "export_packs": {}, "approval_packets": {}
    })
    def upsert(self, store: str, key: str, value: Any) -> Any:
        self.stores[store][key] = value
        return value
    def get(self, store: str, key: str) -> Any:
        return self.stores[store][key]
