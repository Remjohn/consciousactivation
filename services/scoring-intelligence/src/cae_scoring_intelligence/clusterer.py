"""
clusterer.py
------------
Semantic candidate clustering engine for portfolio coverage and redundancy analysis.
"""

from __future__ import annotations

from typing import Dict, List

from .domain import CandidateEvaluationProfile, ClusterGroup, EditorialBoard


class CandidateClusterEngine:
    """Partitions candidates into semantic clusters to analyze portfolio coverage and redundancy."""

    @classmethod
    def form_clusters(
        cls,
        *,
        workspace_id: str,
        evaluations: List[CandidateEvaluationProfile],
        theme_map: Dict[str, List[str]],  # theme -> list of candidate_ids
    ) -> EditorialBoard:
        """Groups candidate evaluation profiles into an EditorialBoard with cluster redundancy metrics."""
        clusters: List[ClusterGroup] = []

        for theme, cand_ids in theme_map.items():
            # Calculate redundancy index based on candidate density in cluster
            count = len(cand_ids)
            if count <= 1:
                redundancy = 0.0
            elif count == 2:
                redundancy = 0.35
            elif count == 3:
                redundancy = 0.65
            else:
                redundancy = min(0.95, 0.65 + 0.1 * (count - 3))

            cluster = ClusterGroup(
                theme=theme,
                candidate_ids=cand_ids,
                redundancy_index=round(redundancy, 2),
                coverage_domain=f"EDITORIAL_DOMAIN_{theme.upper().replace(' ', '_')}",
            )
            clusters.append(cluster)

        return EditorialBoard(
            workspace_id=workspace_id,
            evaluated_candidates=evaluations,
            clusters=clusters,
        )
