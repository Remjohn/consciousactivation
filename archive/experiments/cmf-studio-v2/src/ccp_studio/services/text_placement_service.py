from __future__ import annotations

from ccp_studio.contracts.composition_intelligence import TextPlacementPlan, TextRevealPolicy


class TextPlacementService:
    def compile_text_plan(
        self,
        *,
        headline_text: str,
        support_labels: list[str] | None = None,
        max_visible_words: int = 14,
        placement: str = "upper_card",
    ) -> TextPlacementPlan:
        return TextPlacementPlan(
            headline_text=headline_text,
            support_labels=support_labels or [],
            max_visible_words=max_visible_words,
            placement=placement,
        )

    def compile_reveal_policy(self, refs: list[str]) -> TextRevealPolicy:
        return TextRevealPolicy(reveal_order=refs)
