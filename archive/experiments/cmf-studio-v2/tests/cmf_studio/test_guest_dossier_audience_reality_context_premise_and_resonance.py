from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.context import ContextArtifactKind, ContextOutputStatus, TriggerDepthMode  # noqa: E402
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.contracts.research import EvidenceCitation, SourceRole, TemporalSensitivity  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.context_compilation_service import (  # noqa: E402
    ContextCompilationService,
    ContextCompilationServiceError,
    register_context_compilation_command_handlers,
)
from ccp_studio.services.research_service import ResearchService  # noqa: E402
from ccp_studio.workflows.interview_preparation import InterviewPreparationWorkflow  # noqa: E402


def _citation(title="Source", source_hash="sha256-context"):
    return EvidenceCitation(
        schema_version="cmf.evidence_citation.v1",
        citation_id=uuid4(),
        uri="https://example.com/context-source",
        title=title,
        retrieved_at=utc_now(),
        quoted_span_ref="p1",
        source_hash=source_hash,
    )


def _research_context():
    research = ResearchService()
    organization_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    guest_id = uuid4()
    field = research.create_field(
        organization_id=organization_id,
        brand_id=brand_id,
        guest_id=guest_id,
        objective="Prepare an interview about recording resistance and exposure risk.",
        source_scope=["primary source", "audience comments", "CRAL notes"],
        created_by_actor_id=actor_id,
    )
    primary = research.attach_evidence(
        organization_id=organization_id,
        brand_id=brand_id,
        research_field_id=field.research_field_id,
        claim="The guest explains camera resistance as exposure risk, not laziness.",
        source_role=SourceRole.primary_source,
        citations=[_citation("Guest interview", "sha256-guest")],
        confidence=0.9,
        temporal_sensitivity=TemporalSensitivity.low,
        provenance_summary="Cited guest interview with source hash.",
        contradiction_notes=["public laziness frame vs lived exposure risk"],
        primitive_family_hints=["exposure", "trust"],
        created_by_actor_id=actor_id,
    )
    audience = research.attach_evidence(
        organization_id=organization_id,
        brand_id=brand_id,
        research_field_id=field.research_field_id,
        claim="Audience comments show founders want practical language before mindset framing.",
        source_role=SourceRole.audience_signal,
        citations=[_citation("Audience comment cluster", "sha256-audience")],
        confidence=0.84,
        temporal_sensitivity=TemporalSensitivity.medium,
        freshness_due_at=utc_now().replace(year=utc_now().year + 1),
        provenance_summary="Audience signal cluster with temporal review.",
        contradiction_notes=["desire for practical language vs abstract expert phrasing"],
        primitive_family_hints=["language", "practicality"],
        created_by_actor_id=actor_id,
    )
    cral = research.attach_evidence(
        organization_id=organization_id,
        brand_id=brand_id,
        research_field_id=field.research_field_id,
        claim="CRAL signal identifies the first edge pressure between competence and visibility.",
        source_role=SourceRole.cral_signal,
        citations=[_citation("CRAL note", "sha256-cral")],
        confidence=0.86,
        temporal_sensitivity=TemporalSensitivity.low,
        provenance_summary="CRAL note preserved as source discipline.",
        contradiction_notes=["competence in work vs avoidance in visibility"],
        primitive_family_hints=["edge-pressure"],
        created_by_actor_id=actor_id,
    )
    for item in [primary, audience, cral]:
        research.validate_evidence_provenance(
            organization_id=organization_id,
            brand_id=brand_id,
            evidence_id=item.evidence_id,
            validator_actor_id=actor_id,
        )
        research.approve_evidence(
            organization_id=organization_id,
            brand_id=brand_id,
            evidence_id=item.evidence_id,
            validator_actor_id=actor_id,
        )
    return research, organization_id, brand_id, actor_id, guest_id, field, [primary, audience, cral]


def _compile(service, organization_id, brand_id, actor_id, guest_id, field, evidence):
    return service.compile_context_artifacts(
        organization_id=organization_id,
        brand_id=brand_id,
        research_field_id=field.research_field_id,
        evidence_ids=[item.evidence_id for item in evidence],
        operator_id=actor_id,
        audience_scope="Expression-latent founders who resist recording.",
        compiler_actor_id=actor_id,
        guest_id=guest_id,
        guest_profile_hints=["The guest teaches from lived exposure rather than abstract theory."],
        operator_notes=["The exposure-risk contradiction feels emotionally true."],
    )


def test_compilers_produce_typed_artifacts_with_source_references_confidence_and_receipt():
    research, org_id, brand_id, actor_id, guest_id, field, evidence = _research_context()
    service = ContextCompilationService(research_service=research)

    receipt = _compile(service, org_id, brand_id, actor_id, guest_id, field, evidence)
    dossier = service.repository.guest_dossiers[receipt.output_ids[ContextArtifactKind.guest_dossier]]
    audience = service.repository.audience_reality_briefs[receipt.output_ids[ContextArtifactKind.audience_reality_brief]]
    premise = service.repository.context_premises[receipt.output_ids[ContextArtifactKind.context_premise]]

    assert dossier.identity_facts[0].evidence_ids == [evidence[0].evidence_id]
    assert dossier.identity_facts[0].confidence == 0.9
    assert audience.current_anxieties[0].evidence_ids
    assert premise.stored_as_fact is False
    assert premise.evidence_ids
    assert receipt.source_hashes
    assert "context premise stored as temporary working hypothesis" in receipt.evaluator_results


def test_context_premise_connects_guest_truth_to_audience_reality_and_trigger_depth():
    research, org_id, brand_id, actor_id, guest_id, field, evidence = _research_context()
    service = ContextCompilationService(research_service=research)

    receipt = _compile(service, org_id, brand_id, actor_id, guest_id, field, evidence)
    premise = service.repository.context_premises[receipt.output_ids[ContextArtifactKind.context_premise]]
    trigger_map = service.repository.trigger_maps[receipt.output_ids[ContextArtifactKind.audience_deep_trigger_map]]

    assert "Guest truth" in premise.statement
    assert "Audience anxiety" in premise.statement
    assert premise.audience_conversation_refs
    assert premise.trigger_match_summary == "Audience language and guest truth meet through the trigger map before question design."
    assert any("audience comments" in item.lower() or "recurring audience" in item.lower() for item in premise.question_implications)
    assert trigger_map.depth_mode == TriggerDepthMode.saturated
    assert trigger_map.hermeneutical_gaps
    assert trigger_map.moral_emotional_vectors
    assert trigger_map.audience_guest_matches


def test_interviewer_resonance_context_includes_curiosity_bridges_avoid_list_and_opening_state():
    research, org_id, brand_id, actor_id, guest_id, field, evidence = _research_context()
    service = ContextCompilationService(research_service=research)

    receipt = _compile(service, org_id, brand_id, actor_id, guest_id, field, evidence)
    resonance = service.repository.resonance_contexts[
        receipt.output_ids[ContextArtifactKind.interviewer_resonance_context]
    ]

    assert resonance.authentic_curiosity == ["The exposure-risk contradiction feels emotionally true."]
    assert resonance.emotional_bridges
    assert any("unverified psychology" in item for item in resonance.questions_to_avoid)
    assert resonance.opening_state == "curious, grounded, source-led"
    assert resonance.evidence_ids


def test_unsupported_or_persona_collapsed_context_premise_is_flagged_for_revision():
    research, org_id, brand_id, actor_id, guest_id, field, evidence = _research_context()
    service = ContextCompilationService(research_service=research)

    receipt = service.compile_context_artifacts(
        organization_id=org_id,
        brand_id=brand_id,
        research_field_id=field.research_field_id,
        evidence_ids=[item.evidence_id for item in evidence],
        operator_id=actor_id,
        audience_scope="Expression-latent founders",
        compiler_actor_id=actor_id,
        guest_id=guest_id,
        premise_statement="Generic founder persona wants content pillars.",
    )
    premise = service.repository.context_premises[receipt.output_ids[ContextArtifactKind.context_premise]]

    assert premise.status == ContextOutputStatus.evidence_review_required
    assert "PERSONA_COLLAPSE_DETECTED" in premise.unsupported_inference_flags
    with pytest.raises(ContextCompilationServiceError) as exc:
        service.approve_context_artifact(
            organization_id=org_id,
            brand_id=brand_id,
            artifact_kind=ContextArtifactKind.context_premise,
            artifact_id=premise.context_premise_id,
            reviewer_actor_id=actor_id,
        )
    assert exc.value.code == "CONTEXT_INFERENCE_UNSUPPORTED"


def test_approved_context_artifact_ids_become_saturation_context_for_asset_contracts():
    research, org_id, brand_id, actor_id, guest_id, field, evidence = _research_context()
    service = ContextCompilationService(research_service=research)
    receipt = _compile(service, org_id, brand_id, actor_id, guest_id, field, evidence)

    dossier = service.approve_context_artifact(
        organization_id=org_id,
        brand_id=brand_id,
        artifact_kind=ContextArtifactKind.guest_dossier,
        artifact_id=receipt.output_ids[ContextArtifactKind.guest_dossier],
        reviewer_actor_id=actor_id,
    )
    audience = service.approve_context_artifact(
        organization_id=org_id,
        brand_id=brand_id,
        artifact_kind=ContextArtifactKind.audience_reality_brief,
        artifact_id=receipt.output_ids[ContextArtifactKind.audience_reality_brief],
        reviewer_actor_id=actor_id,
    )
    premise = service.approve_context_artifact(
        organization_id=org_id,
        brand_id=brand_id,
        artifact_kind=ContextArtifactKind.context_premise,
        artifact_id=receipt.output_ids[ContextArtifactKind.context_premise],
        reviewer_actor_id=actor_id,
    )

    packet = service.prepare_downstream_context_inputs(
        organization_id=org_id,
        brand_id=brand_id,
        guest_dossier_id=dossier.guest_dossier_id,
        audience_reality_brief_id=audience.audience_reality_brief_id,
        context_premise_id=premise.context_premise_id,
    )

    assert packet.guest_dossier_id == dossier.guest_dossier_id
    assert packet.audience_reality_brief_id == audience.audience_reality_brief_id
    assert packet.context_premise_id == premise.context_premise_id
    assert set(packet.evidence_ids).issuperset({evidence[0].evidence_id, evidence[1].evidence_id})
    assert packet.context_compilation_receipt_ids


def test_brand_scope_prevents_context_artifact_leakage():
    research, org_id, brand_id, actor_id, guest_id, field, evidence = _research_context()
    service = ContextCompilationService(research_service=research)
    receipt = _compile(service, org_id, brand_id, actor_id, guest_id, field, evidence)

    with pytest.raises(ContextCompilationServiceError) as exc:
        service.approve_context_artifact(
            organization_id=org_id,
            brand_id=uuid4(),
            artifact_kind=ContextArtifactKind.guest_dossier,
            artifact_id=receipt.output_ids[ContextArtifactKind.guest_dossier],
            reviewer_actor_id=actor_id,
        )

    assert exc.value.code == "BRAND_SCOPE_VIOLATION"


def test_workflow_stage3_compiles_context_after_research_snapshot():
    research, org_id, brand_id, actor_id, guest_id, field, evidence = _research_context()
    workflow = InterviewPreparationWorkflow(research)

    snapshot = workflow.stage3_collect_research_evidence(
        organization_id=org_id,
        brand_id=brand_id,
        research_field_id=field.research_field_id,
        evidence_ids=[item.evidence_id for item in evidence],
        actor_id=actor_id,
    )
    receipt = workflow.stage3_compile_context(
        organization_id=org_id,
        brand_id=brand_id,
        research_field_id=field.research_field_id,
        evidence_ids=snapshot.approved_evidence_ids,
        operator_id=actor_id,
        audience_scope="Expression-latent founders",
        actor_id=actor_id,
        guest_id=guest_id,
    )

    assert receipt.decision_code == "CONTEXT_ARTIFACTS_COMPILED"
    assert ContextArtifactKind.context_premise in receipt.output_ids


def test_context_compilation_command_bus_emits_receipt_and_domain_event():
    research, org_id, brand_id, actor_id, guest_id, field, evidence = _research_context()
    service = ContextCompilationService(research_service=research)
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_context_compilation_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["operator"])
    envelope = new_command_envelope(
        command_type="CompileContextPremiseCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "research_field_id": str(field.research_field_id),
            "evidence_ids": [str(item.evidence_id) for item in evidence],
            "operator_id": str(actor_id),
            "audience_scope": "Expression-latent founders",
            "guest_id": str(guest_id),
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["decision_code"] == "CONTEXT_ARTIFACTS_COMPILED"
    assert bus.event_outbox.events[-1].event_type == "CompileContextPremiseCommand.succeeded"
