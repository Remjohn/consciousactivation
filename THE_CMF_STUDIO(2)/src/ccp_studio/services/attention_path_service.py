from __future__ import annotations

from ccp_studio.contracts.composition_intelligence import AttentionPathPlan, AttentionPathStep, CompositionRole


class AttentionPathService:
    def compile_default_format02_path(
        self,
        *,
        headline_ref: str,
        avatar_ref: str | None = None,
        object_ref: str | None = None,
        proxy_ref: str | None = None,
    ) -> AttentionPathPlan:
        steps = [AttentionPathStep(order=1, target_role=CompositionRole.TEXT_ANCHOR, target_ref=headline_ref, reason="headline anchors the concept")]
        order = 2
        if object_ref:
            steps.append(AttentionPathStep(order=order, target_role=CompositionRole.HERO_OBJECT, target_ref=object_ref, reason="object makes concept tangible"))
            order += 1
        if avatar_ref:
            steps.append(AttentionPathStep(order=order, target_role=CompositionRole.AVATAR, target_ref=avatar_ref, reason="avatar guides attention"))
            order += 1
        if proxy_ref:
            steps.append(AttentionPathStep(order=order, target_role=CompositionRole.AUDIENCE_PROXY, target_ref=proxy_ref, reason="proxy mirrors viewer state"))
        return AttentionPathPlan(steps=steps)
