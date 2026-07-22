from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.context import ContextArtifactKind  # noqa: E402
from ccp_studio.contracts.matrix import MatrixBriefStatus, MatrixPass  # noqa: E402
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.contracts.research import EvidenceCitation, SourceRole, TemporalSensitivity  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.context_compilation_service import ContextCompilationService  # noqa: E402
from ccp_studio.services.matrix_service import MatrixService, MatrixServiceError, register_matrix_command_handlers  # noqa: E402
from ccp_studio.services.research_service import ResearchService  # noqa: E402
from ccp_studio.workflows.interview_preparation import InterviewPreparationWorkflow  # noqa: E402


def _citation(title="Matrix source", source_hash="sha256-matrix"):
    return EvidenceCitation(
        schema_version="cmf.evidence_citation.v1",
        citation_id=uuid4(),
        uri="https://example.com/matrix-source",
        title=title,
        retrieved_at=utc_now(),
        quoted_span_ref="p2",
        source_hash=source_hash,
    )


def _approved_context():
    research = ResearchService()
    organization_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    guest_id = uuid4()
    field = research.create_field(
        organization_id=organization_id,
        brand_id=brand_id,
        guest_id=guest_id,
        objective="Find the first Matrix edge for camera resistance.",
        source_scope=["primary source", "audience comments", "CRAL notes"],
        created_by_actor_id=actor_id,
    )
    evidence = [
        research.attach_evidence(
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=field.research_field_id,
            claim="The guest frames camera resistance as exposure risk, not laziness.",
            source_role=SourceRole.primary_source,
            citations=[_citation("Guest source", "sha256-guest")],
            confidence=0.91,
            temporal_sensitivity=TemporalSensitivity.low,
            provenance_summary="Primary source.",
            contradiction_notes=["public laziness frame vs private exposure risk"],
            primitive_family_hints=["vulnerable-specificity"],
            created_by_actor_id=actor_id,
        ),
        research.attach_evidence(
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=field.research_field_id,
            claim="Audience comments ask for practical recording language before mindset claims.",
            source_role=SourceRole.audience_signal,
            citations=[_citation("Audience source", "sha256-audience")],
            confidence=0.86,
            temporal_sensitivity=TemporalSensitivity.medium,
            freshness_due_at=utc_now().replace(year=utc_now().year + 1),
            provenance_summary="Audience source.",
            contradiction_notes=["practical demand vs abstract expert phrasing"],
            primitive_family_hints=["what-is-what-could-be"],
            created_by_actor_id=actor_id,
        ),
        research.attach_evidence(
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=field.research_field_id,
            claim="CRAL identifies competence versus visibility as the broad pressure.",
            source_role=SourceRole.cral_signal,
            citations=[_citation("CRAL source", "sha256-cral")],
            confidence=0.87,
            temporal_sensitivity=TemporalSensitivity.low,
            provenance_summary="CRAL source.",
            contradiction_notes=["competence in delivery vs visibility avoidance"],
            primitive_family_hints=["edge-pressure"],
            created_by_actor_id=actor_id,
        ),
    ]
    for item in evidence:
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
    context_service = ContextCompilationService(research_service=research)
    receipt = context_service.compile_context_artifacts(
        organization_id=organization_id,
        brand_id=brand_id,
        research_field_id=field.research_field_id,
        evidence_ids=[item.evidence_id for item in evidence],
        operator_id=actor_id,
        audience_scope="Expression-latent founders",
        compiler_actor_id=actor_id,
        guest_id=guest_id,
    )
    for kind in [
        ContextArtifactKind.guest_dossier,
        ContextArtifactKind.audience_reality_brief,
        ContextArtifactKind.audience_deep_trigger_map,
        ContextArtifactKind.context_premise,
    ]:
        context_service.approve_context_artifact(
            organization_id=organization_id,
            brand_id=brand_id,
            artifact_kind=kind,
            artifact_id=receipt.output_ids[kind],
            reviewer_actor_id=actor_id,
        )
    return context_service, organization_id, brand_id, actor_id, receipt


def _matrix(service, org_id, brand_id, actor_id, context_receipt, **overrides):
    values = {
        "organization_id": org_id,
        "brand_id": brand_id,
        "guest_dossier_id": context_receipt.output_ids[ContextArtifactKind.guest_dossier],
        "audience_reality_brief_id": context_receipt.output_ids[ContextArtifactKind.audience_reality_brief],
        "context_premise_id": context_receipt.output_ids[ContextArtifactKind.context_premise],
        "trigger_map_id": context_receipt.output_ids[ContextArtifactKind.audience_deep_trigger_map],
        "compiled_by_actor_id": actor_id,
    }
    values.update(overrides)
    return service.compile_matrix_brief(**values)


def test_matrix_compiler_emits_all_eight_pass_outputs_and_receipt():
    context_service, org_id, brand_id, actor_id, context_receipt = _approved_context()
    service = MatrixService(context_service=context_service)

    brief = _matrix(service, org_id, brand_id, actor_id, context_receipt)

    assert {item.pass_name for item in brief.pass_outputs} == set(MatrixPass)
    assert brief.broad_primary_signals
    assert brief.tension_sites
    assert brief.primitive_candidates
    assert brief.coalition_signatures
    assert brief.edge_products
    assert next(iter(service.repository.receipts.values())).decision_code == "MATRIX_BRIEF_COMPILED"


def test_unsupported_tension_site_is_speculative_and_cannot_anchor_question():
    context_service, org_id, brand_id, actor_id, context_receipt = _approved_context()
    service = MatrixService(context_service=context_service)

    brief = _matrix(
        service,
        org_id,
        brand_id,
        actor_id,
        context_receipt,
        speculative_tension_statement="The guest secretly resents their audience.",
    )
    speculative = [site for site in brief.tension_sites if site.speculative][0]

    assert speculative.evidence_ids == []
    assert speculative.can_anchor_question is False


def test_likely_failure_points_show_anti_centroid_guidance():
    context_service, org_id, brand_id, actor_id, context_receipt = _approved_context()
    service = MatrixService(context_service=context_service)

    brief = _matrix(service, org_id, brand_id, actor_id, context_receipt)

    assert any("framework before the guest lands" in item.statement for item in brief.likely_failure_points)
    assert any("Start with the contradiction" in item.avoidance_guidance for item in brief.likely_failure_points)


def test_primitive_candidates_remain_traceable_to_coalitions_edges_and_downstream_packet():
    context_service, org_id, brand_id, actor_id, context_receipt = _approved_context()
    service = MatrixService(context_service=context_service)
    brief = _matrix(service, org_id, brand_id, actor_id, context_receipt)
    service.evaluate_matrix_collision(
        organization_id=org_id,
        brand_id=brand_id,
        matrix_brief_id=brief.matrix_brief_id,
        evaluator_actor_id=actor_id,
    )
    approved = service.approve_matrix_brief(
        organization_id=org_id,
        brand_id=brand_id,
        matrix_brief_id=brief.matrix_brief_id,
        reviewer_actor_id=actor_id,
    )

    packet = service.prepare_downstream_matrix_inputs(
        organization_id=org_id,
        brand_id=brand_id,
        matrix_brief_id=approved.matrix_brief_id,
    )

    assert set(packet.primitive_candidate_ids) == {item.primitive_candidate_id for item in brief.primitive_candidates}
    assert packet.coalition_signature_ids == [brief.coalition_signatures[0].coalition_signature_id]
    assert packet.edge_product_ids == [brief.edge_products[0].edge_product_id]


def test_generic_matrix_output_fails_rscs_specificity_and_must_be_regenerated():
    context_service, org_id, brand_id, actor_id, context_receipt = _approved_context()
    service = MatrixService(context_service=context_service)
    brief = _matrix(service, org_id, brand_id, actor_id, context_receipt, force_generic=True)

    receipt = service.evaluate_matrix_collision(
        organization_id=org_id,
        brand_id=brand_id,
        matrix_brief_id=brief.matrix_brief_id,
        evaluator_actor_id=actor_id,
    )

    assert receipt.decision_code == "MATRIX_EVALUATION_FAILED"
    assert "RSCS_SPECIFICITY_FAILED" in receipt.failure_points
    assert service.repository.briefs[brief.matrix_brief_id].status == MatrixBriefStatus.evaluation_failed


def test_unresolved_primitive_registry_ref_blocks_matrix_approval():
    context_service, org_id, brand_id, actor_id, context_receipt = _approved_context()
    service = MatrixService(context_service=context_service)
    brief = _matrix(
        service,
        org_id,
        brand_id,
        actor_id,
        context_receipt,
        primitive_refs=["unresolved:LegacyPrimitive", "PSY:Vulnerable Specificity"],
    )
    service.evaluate_matrix_collision(
        organization_id=org_id,
        brand_id=brand_id,
        matrix_brief_id=brief.matrix_brief_id,
        evaluator_actor_id=actor_id,
    )

    with pytest.raises(MatrixServiceError) as exc:
        service.approve_matrix_brief(
            organization_id=org_id,
            brand_id=brand_id,
            matrix_brief_id=brief.matrix_brief_id,
            reviewer_actor_id=actor_id,
        )

    assert exc.value.code == "PRIMITIVE_REGISTRY_VALIDATION_REQUIRED"


def test_workflow_stage3_4_compiles_matrix_from_approved_context():
    context_service, org_id, brand_id, actor_id, context_receipt = _approved_context()
    workflow = InterviewPreparationWorkflow(context_service.research_service, context_service=context_service)

    brief = workflow.stage3_4_compile_matrix(
        organization_id=org_id,
        brand_id=brand_id,
        guest_dossier_id=context_receipt.output_ids[ContextArtifactKind.guest_dossier],
        audience_reality_brief_id=context_receipt.output_ids[ContextArtifactKind.audience_reality_brief],
        context_premise_id=context_receipt.output_ids[ContextArtifactKind.context_premise],
        trigger_map_id=context_receipt.output_ids[ContextArtifactKind.audience_deep_trigger_map],
        actor_id=actor_id,
    )

    assert brief.status == MatrixBriefStatus.draft
    assert brief.pass_outputs[0].pass_name == MatrixPass.research


def test_matrix_command_bus_emits_compiled_brief_event():
    context_service, org_id, brand_id, actor_id, context_receipt = _approved_context()
    service = MatrixService(context_service=context_service)
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_matrix_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["operator"])
    envelope = new_command_envelope(
        command_type="CompileMatrixOfEdgingBriefCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "guest_dossier_id": str(context_receipt.output_ids[ContextArtifactKind.guest_dossier]),
            "audience_reality_brief_id": str(context_receipt.output_ids[ContextArtifactKind.audience_reality_brief]),
            "context_premise_id": str(context_receipt.output_ids[ContextArtifactKind.context_premise]),
            "trigger_map_id": str(context_receipt.output_ids[ContextArtifactKind.audience_deep_trigger_map]),
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["schema_version"] == "cmf.matrix_of_edging_brief.v1"
    assert bus.event_outbox.events[-1].event_type == "CompileMatrixOfEdgingBriefCommand.succeeded"
