"""Route selection program stub for TS-CMF-033."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

from ccp_studio.contracts.expression_review import ExpressionMoment
from ccp_studio.contracts.registry import RegistryEntry
from ccp_studio.contracts.routing import (
    RegistryRouteRefs,
    RouteRegistryType,
    RouteSelectionCandidate,
)


@dataclass
class RouteSelectionProgram:
    def select(
        self,
        *,
        expression_moment: ExpressionMoment,
        registry_bundle_version: str,
        active_entries_by_type: dict[RouteRegistryType, list[RegistryEntry]],
        requested_format: str | None = None,
    ) -> RouteSelectionCandidate:
        core = active_entries_by_type[RouteRegistryType.core_content_archetype][0]
        asset = self._entry_for_format(
            active_entries_by_type.get(RouteRegistryType.asset_derivative, []),
            requested_format,
        )
        meme = self._optional_first(active_entries_by_type.get(RouteRegistryType.meme_mechanism, []))
        reaction = self._optional_first(active_entries_by_type.get(RouteRegistryType.reaction_archetype, []))
        render = active_entries_by_type[RouteRegistryType.cmf_render_mode][0]
        route_refs = RegistryRouteRefs(
            schema_version="cmf.registry_route_refs.v1",
            core_content_archetype_ref=self._ref(core),
            asset_derivative_ref=self._ref(asset) if asset else None,
            meme_mechanism_ref=self._ref(meme) if meme else None,
            reaction_archetype_ref=self._ref(reaction) if reaction else None,
            cmf_render_mode_ref=self._ref(render),
            registry_bundle_version=registry_bundle_version,
        )
        evidence = [
            f"expression_moment:{expression_moment.expression_moment_id}",
            *[f"source_range:{item.source_artifact_id}:{item.start_ms}-{item.end_ms}" for item in expression_moment.boundary.normalized_ranges()],
            *[f"registry_entry:{item}" for item in route_refs.all_refs()],
        ]
        route_fit_score = min(0.96, 0.74 + 0.03 * len(expression_moment.induction_context_ids) + 0.02 * len(route_refs.all_refs()))
        return RouteSelectionCandidate(
            schema_version="cmf.route_selection_candidate.v1",
            route_selection_candidate_id=uuid4(),
            expression_moment_id=expression_moment.expression_moment_id,
            requested_format=requested_format,
            route_refs=route_refs,
            source_support_evidence=evidence,
            route_rationale=(
                "Approved Expression Moment routed through active migrated registry entries "
                "with source ranges and review receipt lineage preserved."
            ),
            route_fit_score=route_fit_score,
            failure_alternatives=["narrower asset derivative", "review-only reaction seed", "source quote expansion required"],
        )

    @staticmethod
    def _entry_for_format(entries: list[RegistryEntry], requested_format: str | None) -> RegistryEntry | None:
        if not entries:
            return None
        if requested_format is None:
            return entries[0]
        normalized = requested_format.lower().replace("_", " ").replace("-", " ").strip()
        for entry in entries:
            names = [
                str(entry.payload.get("name", "")),
                str(entry.payload.get("format_key", "")),
                str(entry.payload.get("deliverable_format", "")),
                *[str(item) for item in entry.payload.get("aliases", [])],
            ]
            if normalized in {name.lower().replace("_", " ").replace("-", " ").strip() for name in names}:
                return entry
        return None

    @staticmethod
    def _optional_first(entries: list[RegistryEntry]) -> RegistryEntry | None:
        return entries[0] if entries else None

    @staticmethod
    def _ref(entry: RegistryEntry) -> str:
        return f"registry_entry:{entry.registry_entry_id}"
