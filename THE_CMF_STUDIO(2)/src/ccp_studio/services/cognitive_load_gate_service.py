from __future__ import annotations

from ccp_studio.contracts.composition_intelligence import CognitiveLoadBudget, CognitiveLoadReport, PassStatus


class CognitiveLoadGateService:
    def evaluate(
        self,
        budget: CognitiveLoadBudget,
        *,
        visible_words: int,
        headline_words: int,
        support_labels: int,
        audience_proxies: int,
        hero_real_life_objects: int,
        support_real_life_objects: int,
        diagram_nodes: int,
        simultaneous_motion_events: int,
        negative_space_ratio: float,
    ) -> CognitiveLoadReport:
        blockers = []
        if visible_words > budget.max_visible_words:
            blockers.append("visible_words_exceed_budget")
        if headline_words > budget.max_headline_words:
            blockers.append("headline_words_exceed_budget")
        if support_labels > budget.max_support_labels:
            blockers.append("support_labels_exceed_budget")
        if audience_proxies > budget.max_audience_proxies:
            blockers.append("audience_proxy_count_exceeds_budget")
        if hero_real_life_objects > budget.max_hero_real_life_objects:
            blockers.append("hero_real_life_object_count_exceeds_budget")
        if support_real_life_objects > budget.max_support_real_life_objects:
            blockers.append("support_real_life_object_count_exceeds_budget")
        if diagram_nodes > budget.max_diagram_nodes:
            blockers.append("diagram_node_count_exceeds_budget")
        if simultaneous_motion_events > budget.max_simultaneous_motion_events:
            blockers.append("motion_event_count_exceeds_budget")
        if negative_space_ratio < budget.minimum_negative_space_ratio:
            blockers.append("negative_space_below_minimum")
        return CognitiveLoadReport(
            budget_id=budget.cognitive_load_budget_id,
            visible_words=visible_words,
            headline_words=headline_words,
            support_labels=support_labels,
            audience_proxies=audience_proxies,
            hero_real_life_objects=hero_real_life_objects,
            support_real_life_objects=support_real_life_objects,
            diagram_nodes=diagram_nodes,
            simultaneous_motion_events=simultaneous_motion_events,
            negative_space_ratio=negative_space_ratio,
            pass_status=PassStatus.FAIL if blockers else PassStatus.PASS,
            blockers=blockers,
        )
