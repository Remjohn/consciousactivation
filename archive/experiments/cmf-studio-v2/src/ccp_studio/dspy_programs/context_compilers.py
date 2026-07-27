"""DSPy-style context compiler boundaries for TS-CMF-024.

These classes keep the DSPy boundary explicit while remaining deterministic for
local tests. Real DSPy programs can later replace the prediction internals as
long as they return the same Pydantic contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

from ccp_studio.contracts.context import (
    AudienceDeepTriggerMap,
    AudienceRealityBrief,
    ContextCompilerInputPacket,
    ContextOutputStatus,
    ContextPremise,
    EvidenceBackedInference,
    GuestDossier,
    InterviewerResonanceContext,
    TriggerDepthMode,
    new_inference,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.research import ResearchEvidence, SourceRole


def _unique_ids(values: list[UUID]) -> list[UUID]:
    return list(dict.fromkeys(values))


def _from_evidence(evidence: ResearchEvidence, *, prefix: str | None = None) -> EvidenceBackedInference:
    statement = f"{prefix}: {evidence.claim}" if prefix else evidence.claim
    limitation = None
    if evidence.research_gap:
        limitation = "Research gap remains open."
    elif evidence.confidence < 0.7:
        limitation = "Use as tentative context, not asserted fact."
    return new_inference(
        statement=statement,
        evidence_ids=[evidence.evidence_id],
        confidence=evidence.confidence,
        limitation=limitation,
    )


def _by_role(evidence: list[ResearchEvidence], roles: set[SourceRole]) -> list[ResearchEvidence]:
    return [item for item in evidence if item.source_role in roles]


def _fallback(evidence: list[ResearchEvidence]) -> list[ResearchEvidence]:
    return evidence[:1]


@dataclass(frozen=True)
class GuestDossierCompiler:
    compiler_version: str = "guest-dossier-context-v1"

    def predict(self, packet: ContextCompilerInputPacket, evidence: list[ResearchEvidence]) -> GuestDossier:
        now = utc_now()
        primary = _by_role(evidence, {SourceRole.primary_source, SourceRole.public_context}) or _fallback(evidence)
        cral = _by_role(evidence, {SourceRole.cral_signal})
        audience = _by_role(evidence, {SourceRole.audience_signal})
        contradictions = [
            new_inference(
                statement=note,
                evidence_ids=[item.evidence_id],
                confidence=max(item.confidence - 0.05, 0),
                limitation="Contradiction note must be used as interview pressure, not settled fact.",
            )
            for item in evidence
            for note in item.contradiction_notes
        ]
        state_hints = [
            new_inference(
                statement=f"Likely expression state pressure: {hint}",
                evidence_ids=[item.evidence_id],
                confidence=item.confidence,
                limitation="State hint requires live operator confirmation.",
            )
            for item in evidence
            for hint in item.primitive_family_hints
        ]
        profile_hints = [
            new_inference(
                statement=hint,
                evidence_ids=[primary[0].evidence_id],
                confidence=primary[0].confidence,
                limitation="Guest profile hint must remain subordinate to source evidence.",
            )
            for hint in packet.guest_profile_hints
        ]
        return GuestDossier(
            schema_version="cmf.guest_dossier.v1",
            guest_dossier_id=uuid4(),
            organization_id=packet.organization_id,
            brand_id=packet.brand_id,
            guest_id=packet.guest_id,
            research_field_id=packet.research_field_id,
            identity_facts=[_from_evidence(item, prefix="Guest truth") for item in primary],
            biography_and_work=profile_hints or [_from_evidence(item, prefix="Biography/work") for item in primary],
            recurring_themes=[_from_evidence(item, prefix="Recurring theme") for item in primary + cral],
            strongest_scenes=[_from_evidence(item, prefix="Strong scene candidate") for item in primary],
            public_language=[_from_evidence(item, prefix="Public language") for item in primary],
            prior_interview_patterns=[_from_evidence(item, prefix="Prior pattern") for item in primary],
            contradictions=contradictions,
            emotional_territory=[_from_evidence(item, prefix="Emotional territory") for item in cral or primary],
            likely_expression_states=state_hints,
            risks_and_boundaries=contradictions[:],
            audience_overlap=[_from_evidence(item, prefix="Audience overlap") for item in audience],
            research_gaps=[item.claim for item in evidence if item.research_gap or item.confidence < 0.55],
            status=ContextOutputStatus.draft,
            created_at=now,
            updated_at=now,
        )


@dataclass(frozen=True)
class AudienceRealityBriefCompiler:
    compiler_version: str = "audience-reality-context-v1"

    def predict(self, packet: ContextCompilerInputPacket, evidence: list[ResearchEvidence]) -> AudienceRealityBrief:
        now = utc_now()
        audience = _by_role(evidence, {SourceRole.audience_signal, SourceRole.cral_signal}) or _fallback(evidence)
        contradiction_items = [item for item in evidence if item.contradiction_notes]
        temporal_relevance = "freshness_reviewed" if any(item.freshness_due_at for item in evidence) else "evergreen_or_reviewed"
        return AudienceRealityBrief(
            schema_version="cmf.audience_reality_brief.v1",
            audience_reality_brief_id=uuid4(),
            organization_id=packet.organization_id,
            brand_id=packet.brand_id,
            research_field_id=packet.research_field_id,
            audience_scope=packet.audience_scope,
            current_anxieties=[_from_evidence(item, prefix="Audience anxiety") for item in audience],
            recurring_comments=[_from_evidence(item, prefix="Recurring comment") for item in audience],
            social_debates=[_from_evidence(item, prefix="Social debate") for item in contradiction_items],
            search_questions=[_from_evidence(item, prefix="Search question") for item in audience],
            objections=[_from_evidence(item, prefix="Objection") for item in contradiction_items or audience],
            cultural_language=[_from_evidence(item, prefix="Cultural language") for item in audience],
            identity_tensions=[_from_evidence(item, prefix="Identity tension") for item in contradiction_items],
            ordinary_objects_and_rituals=[_from_evidence(item, prefix="Ordinary ritual") for item in audience],
            micro_semiotic_anchor_candidates=[_from_evidence(item, prefix="Micro-semiotic anchor") for item in audience],
            temporal_relevance=temporal_relevance,
            status=ContextOutputStatus.draft,
            created_at=now,
            updated_at=now,
        )


@dataclass(frozen=True)
class AudienceDeepTriggerMapCompiler:
    compiler_version: str = "audience-deep-trigger-map-v1"

    def predict(
        self,
        packet: ContextCompilerInputPacket,
        evidence: list[ResearchEvidence],
        dossier: GuestDossier,
        audience_brief: AudienceRealityBrief,
    ) -> AudienceDeepTriggerMap:
        now = utc_now()
        audience_ids = {item.evidence_id for item in _by_role(evidence, {SourceRole.audience_signal, SourceRole.cral_signal})}
        contradiction_items = [item for item in evidence if item.contradiction_notes]
        depth_mode = TriggerDepthMode.saturated if audience_ids and contradiction_items and dossier.identity_facts else TriggerDepthMode.shallow
        match_ids = _unique_ids(
            [
                *[inference.evidence_ids[0] for inference in dossier.identity_facts[:1]],
                *[inference.evidence_ids[0] for inference in audience_brief.current_anxieties[:1]],
            ]
        )
        match = new_inference(
            statement="Audience pressure should meet guest truth through a sourced contradiction, not a generic persona.",
            evidence_ids=match_ids or packet.approved_evidence_ids[:1],
            confidence=min([item.confidence for item in evidence] or [0.5]),
            limitation="This is a working trigger match for interview preparation only.",
        )
        return AudienceDeepTriggerMap(
            schema_version="cmf.audience_deep_trigger_map.v1",
            trigger_map_id=uuid4(),
            organization_id=packet.organization_id,
            brand_id=packet.brand_id,
            research_field_id=packet.research_field_id,
            depth_mode=depth_mode,
            hermeneutical_gaps=[
                _from_evidence(item, prefix="Hermeneutical gap") for item in contradiction_items or evidence[:1]
            ],
            moral_emotional_vectors=[
                _from_evidence(item, prefix="Moral-emotional vector") for item in contradiction_items or evidence[:1]
            ],
            coping_trajectory=audience_brief.current_anxieties[:1],
            audience_guest_matches=[match],
            audience_coach_matches=[match],
            regulatory_focus="prevention" if contradiction_items else None,
            confidence=min([item.confidence for item in evidence] or [0.5]),
            gaps=["Audience trigger depth is shallow."] if depth_mode == TriggerDepthMode.shallow else [],
            status=ContextOutputStatus.draft,
            created_at=now,
            updated_at=now,
        )


@dataclass(frozen=True)
class ContextPremiseCompiler:
    compiler_version: str = "context-premise-v1"

    def predict(
        self,
        packet: ContextCompilerInputPacket,
        evidence: list[ResearchEvidence],
        dossier: GuestDossier,
        audience_brief: AudienceRealityBrief,
        trigger_map: AudienceDeepTriggerMap,
        statement_override: str | None = None,
    ) -> ContextPremise:
        now = utc_now()
        guest_text = dossier.identity_facts[0].statement if dossier.identity_facts else "guest truth is under-evidenced"
        audience_text = audience_brief.current_anxieties[0].statement if audience_brief.current_anxieties else "audience reality is under-evidenced"
        statement = statement_override or (
            f"The interview should begin where {guest_text} collides with {audience_text}."
        )
        evidence_ids = _unique_ids(
            [
                *[item for inference in dossier.identity_facts[:1] for item in inference.evidence_ids],
                *[item for inference in audience_brief.current_anxieties[:1] for item in inference.evidence_ids],
                *[item for inference in trigger_map.audience_guest_matches[:1] for item in inference.evidence_ids],
            ]
        )
        flags = _context_premise_flags(
            statement=statement,
            evidence_ids=evidence_ids,
            trigger_map=trigger_map,
        )
        status = ContextOutputStatus.evidence_review_required if flags else ContextOutputStatus.draft
        confidence_values = [item.confidence for item in evidence if item.evidence_id in set(evidence_ids)]
        confidence = min(confidence_values) if confidence_values else 0.5
        return ContextPremise(
            schema_version="cmf.context_premise.v1",
            context_premise_id=uuid4(),
            organization_id=packet.organization_id,
            brand_id=packet.brand_id,
            research_field_id=packet.research_field_id,
            guest_dossier_id=dossier.guest_dossier_id,
            audience_reality_brief_id=audience_brief.audience_reality_brief_id,
            trigger_map_id=trigger_map.trigger_map_id,
            statement=statement,
            evidence_ids=evidence_ids or packet.approved_evidence_ids[:1],
            confidence=confidence,
            guest_implication="Start with the lived scene, pattern, or contradiction the guest can truthfully own.",
            audience_implication="Name the audience pressure as a question field rather than asserting hidden psychology.",
            question_implications=[
                "Begin with source-backed lived material before methodology.",
                "Use the trigger map to choose pressure, not extremity.",
                "Translate recurring audience comments into question pressure before selecting content routes.",
            ],
            audience_conversation_refs=[
                f"evidence:{item}"
                for inference in [
                    *audience_brief.recurring_comments[:2],
                    *audience_brief.objections[:2],
                    *audience_brief.search_questions[:2],
                    *audience_brief.social_debates[:2],
                ]
                for item in inference.evidence_ids
            ],
            trigger_match_summary="Audience language and guest truth meet through the trigger map before question design.",
            risk_if_wrong="The interviewer may steer the guest into a generic or unsupported frame.",
            unsupported_inference_flags=flags,
            status=status,
            created_at=now,
            updated_at=now,
        )


@dataclass(frozen=True)
class InterviewerResonanceCompiler:
    compiler_version: str = "interviewer-resonance-v1"

    def predict(self, packet: ContextCompilerInputPacket, evidence: list[ResearchEvidence]) -> InterviewerResonanceContext:
        now = utc_now()
        evidence_ids = [item.evidence_id for item in evidence[:3]]
        notes = [note for note in packet.operator_notes if note.strip()]
        return InterviewerResonanceContext(
            schema_version="cmf.interviewer_resonance_context.v1",
            resonance_context_id=uuid4(),
            organization_id=packet.organization_id,
            brand_id=packet.brand_id,
            research_field_id=packet.research_field_id,
            operator_id=packet.operator_id,
            authentic_curiosity=notes or ["Which sourced scene stayed alive after research?"],
            emotional_bridges=[
                "Share only a small reflection that is true for the Operator.",
                "Ask where the guest felt the contradiction before naming the method.",
            ],
            questions_to_avoid=[
                "Do not assert unverified psychology.",
                "Do not flatten the audience into a generic persona.",
            ],
            opening_state="curious, grounded, source-led",
            small_reflection_zones=notes[:2],
            refusal_to_fake=["Do not perform certainty the evidence does not support."],
            evidence_ids=evidence_ids or packet.approved_evidence_ids[:1],
            status=ContextOutputStatus.draft,
            created_at=now,
            updated_at=now,
        )


def _context_premise_flags(
    *,
    statement: str,
    evidence_ids: list[UUID],
    trigger_map: AudienceDeepTriggerMap,
) -> list[str]:
    flags: list[str] = []
    lowered = statement.lower()
    if not evidence_ids:
        flags.append("CONTEXT_PREMISE_EVIDENCE_REQUIRED")
    if "persona" in lowered or "generic" in lowered or "content pillar" in lowered:
        flags.append("PERSONA_COLLAPSE_DETECTED")
    if trigger_map.depth_mode == TriggerDepthMode.shallow:
        flags.append("TRIGGER_DEPTH_SHALLOW")
    if not trigger_map.hermeneutical_gaps or not trigger_map.moral_emotional_vectors or not trigger_map.audience_guest_matches:
        flags.append("AUDIENCE_TRIGGER_STRUCTURE_REQUIRED")
    return list(dict.fromkeys(flags))
