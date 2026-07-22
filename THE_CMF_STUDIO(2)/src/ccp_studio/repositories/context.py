"""Context compilation repositories for TS-CMF-024."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.context import (
    AudienceDeepTriggerMap,
    AudienceRealityBrief,
    ContextArtifactKind,
    ContextCompilationReceipt,
    ContextPremise,
    GuestDossier,
    InterviewerResonanceContext,
)


@dataclass
class InMemoryContextRepository:
    guest_dossiers: dict[UUID, GuestDossier] = field(default_factory=dict)
    audience_reality_briefs: dict[UUID, AudienceRealityBrief] = field(default_factory=dict)
    trigger_maps: dict[UUID, AudienceDeepTriggerMap] = field(default_factory=dict)
    context_premises: dict[UUID, ContextPremise] = field(default_factory=dict)
    resonance_contexts: dict[UUID, InterviewerResonanceContext] = field(default_factory=dict)
    receipts: dict[UUID, ContextCompilationReceipt] = field(default_factory=dict)

    def put_guest_dossier(self, dossier: GuestDossier) -> GuestDossier:
        self.guest_dossiers[dossier.guest_dossier_id] = dossier
        return dossier

    def put_audience_reality_brief(self, brief: AudienceRealityBrief) -> AudienceRealityBrief:
        self.audience_reality_briefs[brief.audience_reality_brief_id] = brief
        return brief

    def put_trigger_map(self, trigger_map: AudienceDeepTriggerMap) -> AudienceDeepTriggerMap:
        self.trigger_maps[trigger_map.trigger_map_id] = trigger_map
        return trigger_map

    def put_context_premise(self, premise: ContextPremise) -> ContextPremise:
        self.context_premises[premise.context_premise_id] = premise
        return premise

    def put_resonance_context(self, context: InterviewerResonanceContext) -> InterviewerResonanceContext:
        self.resonance_contexts[context.resonance_context_id] = context
        return context

    def put_receipt(self, receipt: ContextCompilationReceipt) -> ContextCompilationReceipt:
        self.receipts[receipt.context_compilation_receipt_id] = receipt
        return receipt

    def get_artifact(self, kind: ContextArtifactKind, artifact_id: UUID):
        if kind == ContextArtifactKind.guest_dossier:
            return self.guest_dossiers.get(artifact_id)
        if kind == ContextArtifactKind.audience_reality_brief:
            return self.audience_reality_briefs.get(artifact_id)
        if kind == ContextArtifactKind.audience_deep_trigger_map:
            return self.trigger_maps.get(artifact_id)
        if kind == ContextArtifactKind.context_premise:
            return self.context_premises.get(artifact_id)
        if kind == ContextArtifactKind.interviewer_resonance_context:
            return self.resonance_contexts.get(artifact_id)
        return None

    def put_artifact(self, kind: ContextArtifactKind, artifact):
        if kind == ContextArtifactKind.guest_dossier:
            return self.put_guest_dossier(artifact)
        if kind == ContextArtifactKind.audience_reality_brief:
            return self.put_audience_reality_brief(artifact)
        if kind == ContextArtifactKind.audience_deep_trigger_map:
            return self.put_trigger_map(artifact)
        if kind == ContextArtifactKind.context_premise:
            return self.put_context_premise(artifact)
        if kind == ContextArtifactKind.interviewer_resonance_context:
            return self.put_resonance_context(artifact)
        raise ValueError(f"Unsupported context artifact kind: {kind}")
