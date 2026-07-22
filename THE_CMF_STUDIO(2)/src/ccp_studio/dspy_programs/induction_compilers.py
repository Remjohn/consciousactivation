"""DSPy-style CRAL, DNA, and induction rationale compilers for TS-CMF-028."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

from ccp_studio.contracts.context import (
    AudienceDeepTriggerMap,
    ContextPremise,
    GuestDossier,
    InterviewerResonanceContext,
    TriggerDepthMode,
)
from ccp_studio.contracts.induction import (
    CRALFinding,
    CRALMoment,
    EmotionalDNAProfile,
    InductionArtifactStatus,
    InductionRationale,
    RationaleMode,
    SupportedPsychologyClaim,
    VoiceDNAProfile,
    new_supported_claim,
)
from ccp_studio.contracts.matrix import EdgeProduct, MatrixOfEdgingBrief
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.pre_induction import PreInductionPlan, PreInductionQuestion
from ccp_studio.contracts.research import ResearchEvidence, SourceRole


UNSUPPORTED_CERTAINTY_TERMS = {
    "trauma",
    "diagnosis",
    "subconscious",
    "narcissist",
    "attachment wound",
    "pathology",
}


def _unique_ids(values: list[UUID]) -> list[UUID]:
    return list(dict.fromkeys(values))


def _evidence_by_id(evidence: list[ResearchEvidence], evidence_ids: list[UUID]) -> list[ResearchEvidence]:
    wanted = set(evidence_ids)
    return [item for item in evidence if item.evidence_id in wanted]


def _roles_for(evidence: list[ResearchEvidence], evidence_ids: list[UUID]) -> list[SourceRole]:
    return list(dict.fromkeys(item.source_role for item in _evidence_by_id(evidence, evidence_ids)))


def _confidence_for(evidence: list[ResearchEvidence], evidence_ids: list[UUID], default: float = 0.55) -> float:
    values = [item.confidence for item in _evidence_by_id(evidence, evidence_ids)]
    return min(values) if values else default


def _claim(
    *,
    statement: str,
    claim_type: str,
    evidence_ids: list[UUID],
    evidence: list[ResearchEvidence],
    mode: RationaleMode,
    limitation: str = "Use as interview preparation context, not asserted diagnosis or certainty.",
) -> SupportedPsychologyClaim:
    return new_supported_claim(
        statement=statement,
        claim_type=claim_type,
        evidence_ids=_unique_ids(evidence_ids),
        source_roles=_roles_for(evidence, evidence_ids),
        confidence=_confidence_for(evidence, evidence_ids),
        limitation=limitation,
        rationale_mode=mode,
    )


@dataclass(frozen=True)
class CRALResearchCompiler:
    compiler_version: str = "cral-research-compiler-v1"

    def predict(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        research_field_id: UUID,
        evidence: list[ResearchEvidence],
    ) -> list[CRALFinding]:
        now = utc_now()
        cral_evidence = [item for item in evidence if item.source_role == SourceRole.cral_signal] or evidence[:1]
        findings: list[CRALFinding] = []
        for index, moment in enumerate(CRALMoment):
            source = cral_evidence[index % len(cral_evidence)]
            findings.append(
                CRALFinding(
                    schema_version="cmf.cral_finding.v1",
                    cral_finding_id=uuid4(),
                    organization_id=organization_id,
                    brand_id=brand_id,
                    research_field_id=research_field_id,
                    moment=moment,
                    signal=f"{moment.value}: {source.claim}",
                    source_role=source.source_role,
                    evidence_ids=[source.evidence_id],
                    confidence=source.confidence,
                    contradiction_notes=source.contradiction_notes,
                    status=InductionArtifactStatus.compiled,
                    created_at=now,
                )
            )
        return findings


@dataclass(frozen=True)
class EmotionalDNAExtractor:
    compiler_version: str = "emotional-dna-extractor-v1"

    def predict(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        research_field_id: UUID,
        guest_id: UUID | None,
        dossier: GuestDossier,
        trigger_map: AudienceDeepTriggerMap,
        premise: ContextPremise,
        evidence: list[ResearchEvidence],
        include_profile: bool = True,
    ) -> EmotionalDNAProfile:
        now = utc_now()
        mode = RationaleMode.full_depth if include_profile and trigger_map.depth_mode == TriggerDepthMode.saturated else RationaleMode.partial
        identity_ids = _unique_ids([item for inference in dossier.identity_facts[:1] for item in inference.evidence_ids])
        territory_ids = _unique_ids([item for inference in dossier.emotional_territory[:1] for item in inference.evidence_ids])
        vector_ids = _unique_ids([item for inference in trigger_map.moral_emotional_vectors[:1] for item in inference.evidence_ids])
        gap_ids = _unique_ids([item for inference in trigger_map.hermeneutical_gaps[:1] for item in inference.evidence_ids])
        if not include_profile:
            return EmotionalDNAProfile(
                schema_version="cmf.emotional_dna_profile.v1",
                emotional_dna_profile_id=uuid4(),
                organization_id=organization_id,
                brand_id=brand_id,
                guest_id=guest_id,
                research_field_id=research_field_id,
                evidence_ids=[],
                limitation="Emotional DNA evidence is absent; rationale must remain partial.",
                status=InductionArtifactStatus.partial,
                created_at=now,
                updated_at=now,
            )
        evidence_ids = _unique_ids([*identity_ids, *territory_ids, *vector_ids, *gap_ids, *premise.evidence_ids])
        return EmotionalDNAProfile(
            schema_version="cmf.emotional_dna_profile.v1",
            emotional_dna_profile_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            guest_id=guest_id,
            research_field_id=research_field_id,
            belief_content=[
                _claim(
                    statement=(dossier.identity_facts[0].statement if dossier.identity_facts else premise.guest_implication),
                    claim_type="belief_content",
                    evidence_ids=identity_ids or premise.evidence_ids,
                    evidence=evidence,
                    mode=mode,
                )
            ],
            emotional_path=[
                _claim(
                    statement=(dossier.emotional_territory[0].statement if dossier.emotional_territory else premise.guest_implication),
                    claim_type="emotional_path",
                    evidence_ids=territory_ids or premise.evidence_ids,
                    evidence=evidence,
                    mode=mode,
                )
            ],
            suppression_markers=[
                _claim(
                    statement=(trigger_map.hermeneutical_gaps[0].statement if trigger_map.hermeneutical_gaps else premise.risk_if_wrong),
                    claim_type="suppression_marker",
                    evidence_ids=gap_ids or premise.evidence_ids,
                    evidence=evidence,
                    mode=mode,
                )
            ],
            escalation_triggers=[
                _claim(
                    statement=(trigger_map.moral_emotional_vectors[0].statement if trigger_map.moral_emotional_vectors else premise.audience_implication),
                    claim_type="escalation_trigger",
                    evidence_ids=vector_ids or premise.evidence_ids,
                    evidence=evidence,
                    mode=mode,
                )
            ],
            evidence_ids=evidence_ids,
            limitation=None if mode == RationaleMode.full_depth else "Depth is supported but incomplete.",
            status=InductionArtifactStatus.compiled if mode == RationaleMode.full_depth else InductionArtifactStatus.partial,
            created_at=now,
            updated_at=now,
        )


@dataclass(frozen=True)
class VoiceDNAProfileCompiler:
    compiler_version: str = "voice-dna-profile-compiler-v1"

    def predict(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        research_field_id: UUID,
        guest_id: UUID | None,
        dossier: GuestDossier,
        resonance: InterviewerResonanceContext | None,
        premise: ContextPremise,
        emotional_profile: EmotionalDNAProfile,
        evidence: list[ResearchEvidence],
        include_profile: bool = True,
    ) -> VoiceDNAProfile:
        now = utc_now()
        mode = RationaleMode.full_depth if include_profile and emotional_profile.evidence_ids else RationaleMode.partial
        language_ids = _unique_ids([item for inference in dossier.public_language[:1] for item in inference.evidence_ids])
        resonance_ids = resonance.evidence_ids if resonance else []
        if not include_profile:
            return VoiceDNAProfile(
                schema_version="cmf.voice_dna_profile.v1",
                voice_dna_profile_id=uuid4(),
                organization_id=organization_id,
                brand_id=brand_id,
                guest_id=guest_id,
                research_field_id=research_field_id,
                emotional_dna_profile_id=emotional_profile.emotional_dna_profile_id,
                evidence_ids=[],
                limitation="Voice DNA evidence is absent; do not imitate tone or infer full voice mechanics.",
                status=InductionArtifactStatus.partial,
                created_at=now,
                updated_at=now,
            )
        evidence_ids = _unique_ids([*language_ids, *resonance_ids, *emotional_profile.evidence_ids])
        avoid = resonance.questions_to_avoid[0] if resonance and resonance.questions_to_avoid else "Do not imitate surface tone."
        return VoiceDNAProfile(
            schema_version="cmf.voice_dna_profile.v1",
            voice_dna_profile_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            guest_id=guest_id,
            research_field_id=research_field_id,
            construction_mechanics=[
                _claim(
                    statement=(dossier.public_language[0].statement if dossier.public_language else "Start from lived source scenes before abstraction."),
                    claim_type="construction_mechanic",
                    evidence_ids=language_ids or premise.evidence_ids,
                    evidence=evidence,
                    mode=mode,
                )
            ],
            negative_space=[
                _claim(
                    statement=avoid,
                    claim_type="negative_space",
                    evidence_ids=resonance_ids or premise.evidence_ids,
                    evidence=evidence,
                    mode=mode,
                )
            ],
            normative_expression_targets=[
                _claim(
                    statement="Move from sourced contradiction into teachable language without copying generic expert tone.",
                    claim_type="normative_expression_target",
                    evidence_ids=evidence_ids or premise.evidence_ids,
                    evidence=evidence,
                    mode=mode,
                )
            ],
            emotional_dna_profile_id=emotional_profile.emotional_dna_profile_id,
            evidence_ids=evidence_ids,
            limitation=None if mode == RationaleMode.full_depth else "Voice construction is partially supported.",
            status=InductionArtifactStatus.compiled if mode == RationaleMode.full_depth else InductionArtifactStatus.partial,
            created_at=now,
            updated_at=now,
        )


@dataclass(frozen=True)
class UnsupportedPsychologyValidator:
    compiler_version: str = "supported-psychology-validator-v1"

    def evaluate_claims(self, claims: list[SupportedPsychologyClaim]) -> list[str]:
        blocked: list[str] = []
        for claim in claims:
            lowered = claim.statement.lower()
            if not claim.evidence_ids:
                blocked.append(f"PSYCHOLOGY_EVIDENCE_REQUIRED:{claim.claim_id}")
            if not claim.source_roles:
                blocked.append(f"PSYCHOLOGY_SOURCE_ROLE_REQUIRED:{claim.claim_id}")
            if not claim.limitation:
                blocked.append(f"PSYCHOLOGY_LIMITATION_REQUIRED:{claim.claim_id}")
            if any(term in lowered for term in UNSUPPORTED_CERTAINTY_TERMS) and claim.confidence >= 0.8:
                blocked.append(f"UNSUPPORTED_PSYCHOLOGICAL_CERTAINTY:{claim.claim_id}")
        return list(dict.fromkeys(blocked))


@dataclass(frozen=True)
class InductionRationaleCompiler:
    compiler_version: str = "induction-rationale-compiler-v1"

    def predict(
        self,
        *,
        plan: PreInductionPlan,
        matrix: MatrixOfEdgingBrief,
        premise: ContextPremise,
        trigger_map: AudienceDeepTriggerMap,
        cral_findings: list[CRALFinding],
        emotional_profile: EmotionalDNAProfile,
        voice_profile: VoiceDNAProfile,
        evidence: list[ResearchEvidence],
    ) -> list[InductionRationale]:
        rationales: list[InductionRationale] = []
        for question in plan.planned_questions:
            edge = self._edge_for_question(question, matrix)
            mode = self._mode(
                trigger_map=trigger_map,
                cral_findings=cral_findings,
                emotional_profile=emotional_profile,
                voice_profile=voice_profile,
            )
            support_limitations = self._limitations(
                mode=mode,
                trigger_map=trigger_map,
                emotional_profile=emotional_profile,
                voice_profile=voice_profile,
            )
            evidence_ids = _unique_ids(
                [
                    *question.evidence_ids,
                    *premise.evidence_ids,
                    *emotional_profile.evidence_ids,
                    *voice_profile.evidence_ids,
                    *[evidence_id for finding in cral_findings for evidence_id in finding.evidence_ids],
                ]
            )
            supported_claims = [
                _claim(
                    statement=premise.statement,
                    claim_type="context_premise",
                    evidence_ids=premise.evidence_ids,
                    evidence=evidence,
                    mode=mode,
                    limitation="Context Premise is a working hypothesis for interview preparation, not fact.",
                ),
                _claim(
                    statement=edge.anti_centroid_pressure if edge else question.authentic_curiosity,
                    claim_type="matrix_pressure",
                    evidence_ids=question.evidence_ids,
                    evidence=evidence,
                    mode=mode,
                ),
            ]
            if emotional_profile.belief_content:
                supported_claims.append(emotional_profile.belief_content[0])
            if voice_profile.construction_mechanics:
                supported_claims.append(voice_profile.construction_mechanics[0])
            target_states = edge.expected_expression_state if edge else ["vulnerability", "meaning"]
            outcomes = edge.route_implications if edge else ["source-backed expression moment", "routeable asset contract"]
            now = utc_now()
            rationales.append(
                InductionRationale(
                    schema_version="cmf.induction_rationale.v1",
                    rationale_id=uuid4(),
                    organization_id=plan.organization_id,
                    brand_id=plan.brand_id,
                    planned_move_id=question.question_id,
                    pre_induction_plan_id=plan.pre_induction_plan_id,
                    cral_finding_ids=[finding.cral_finding_id for finding in cral_findings],
                    context_premise_id=premise.context_premise_id,
                    trigger_map_id=trigger_map.trigger_map_id,
                    emotional_dna_profile_id=emotional_profile.emotional_dna_profile_id if emotional_profile.evidence_ids else None,
                    voice_dna_profile_id=voice_profile.voice_dna_profile_id if voice_profile.evidence_ids else None,
                    matrix_brief_id=matrix.matrix_brief_id,
                    matrix_edge_product_id=edge.edge_product_id if edge else question.matrix_edge_product_id,
                    target_expression_state=target_states,
                    intended_extraction_outcome=outcomes,
                    supported_claims=supported_claims,
                    evidence_ids=evidence_ids,
                    rationale_mode=mode,
                    support_limitations=support_limitations,
                    status=InductionArtifactStatus.compiled if mode == RationaleMode.full_depth else InductionArtifactStatus.partial,
                    created_at=now,
                    updated_at=now,
                )
            )
        return rationales

    @staticmethod
    def _edge_for_question(question: PreInductionQuestion, matrix: MatrixOfEdgingBrief) -> EdgeProduct | None:
        for edge in matrix.edge_products:
            if question.matrix_edge_product_id == edge.edge_product_id:
                return edge
        return matrix.edge_products[0] if matrix.edge_products else None

    @staticmethod
    def _mode(
        *,
        trigger_map: AudienceDeepTriggerMap,
        cral_findings: list[CRALFinding],
        emotional_profile: EmotionalDNAProfile,
        voice_profile: VoiceDNAProfile,
    ) -> RationaleMode:
        if not emotional_profile.evidence_ids and not voice_profile.evidence_ids:
            return RationaleMode.partial
        if trigger_map.depth_mode == TriggerDepthMode.shallow:
            return RationaleMode.shallow_supported
        if not cral_findings:
            return RationaleMode.partial
        if not emotional_profile.evidence_ids or not voice_profile.evidence_ids:
            return RationaleMode.partial
        return RationaleMode.full_depth

    @staticmethod
    def _limitations(
        *,
        mode: RationaleMode,
        trigger_map: AudienceDeepTriggerMap,
        emotional_profile: EmotionalDNAProfile,
        voice_profile: VoiceDNAProfile,
    ) -> list[str]:
        limitations: list[str] = []
        if trigger_map.depth_mode == TriggerDepthMode.shallow:
            limitations.append("Audience trigger map is shallow; do not claim full-depth audience psychology.")
        limitations.extend(trigger_map.gaps)
        if emotional_profile.limitation:
            limitations.append(emotional_profile.limitation)
        if voice_profile.limitation:
            limitations.append(voice_profile.limitation)
        if mode != RationaleMode.full_depth and not limitations:
            limitations.append("Rationale is supported but incomplete; block certainty language.")
        return list(dict.fromkeys(limitations))
