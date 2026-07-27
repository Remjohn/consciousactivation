"""Visual asset research repositories for TS-CMF-049."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.visual_research import (
    AssetResearchManifest,
    AssetResearchReceipt,
    ImageResolutionMap,
    LicensingDecision,
    VisualCandidate,
    VisualCandidateScore,
    VisualResearchQuery,
)


@dataclass
class InMemoryVisualResearchRepository:
    queries: dict[UUID, VisualResearchQuery] = field(default_factory=dict)
    licensing_decisions: dict[UUID, LicensingDecision] = field(default_factory=dict)
    scores: dict[UUID, VisualCandidateScore] = field(default_factory=dict)
    candidates: dict[UUID, VisualCandidate] = field(default_factory=dict)
    manifests: dict[UUID, AssetResearchManifest] = field(default_factory=dict)
    image_resolution_maps: dict[UUID, ImageResolutionMap] = field(default_factory=dict)
    receipts: dict[UUID, AssetResearchReceipt] = field(default_factory=dict)

    def put_query(self, query: VisualResearchQuery) -> VisualResearchQuery:
        self.queries[query.visual_research_query_id] = query
        return query

    def put_licensing_decision(self, decision: LicensingDecision) -> LicensingDecision:
        self.licensing_decisions[decision.licensing_decision_id] = decision
        return decision

    def put_score(self, score: VisualCandidateScore) -> VisualCandidateScore:
        self.scores[score.score_id] = score
        return score

    def put_candidate(self, candidate: VisualCandidate) -> VisualCandidate:
        self.candidates[candidate.visual_candidate_id] = candidate
        return candidate

    def put_manifest(self, manifest: AssetResearchManifest) -> AssetResearchManifest:
        self.manifests[manifest.asset_research_manifest_id] = manifest
        return manifest

    def put_image_resolution_map(self, image_map: ImageResolutionMap) -> ImageResolutionMap:
        self.image_resolution_maps[image_map.image_resolution_map_id] = image_map
        return image_map

    def put_receipt(self, receipt: AssetResearchReceipt) -> AssetResearchReceipt:
        self.receipts[receipt.asset_research_receipt_id] = receipt
        return receipt

    def candidates_for_query(self, visual_research_query_id: UUID) -> list[VisualCandidate]:
        return [
            item for item in self.candidates.values() if item.visual_research_query_id == visual_research_query_id
        ]
