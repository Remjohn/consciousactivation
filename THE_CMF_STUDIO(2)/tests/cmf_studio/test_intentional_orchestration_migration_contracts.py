from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.legacy_orchestration import OrganismLayer, gate_ref, packet_ref
from ccp_studio.services.orchestration_intent_service import (
    OrchestrationIntentError,
    OrchestrationIntentService,
)


def _record(service=None, **overrides):
    service = service or OrchestrationIntentService()
    values = {
        "migration_ledger_entry_id": uuid4(),
        "product_purpose": "Preserve CRAL source discipline by turning research signals into interview-ready context before extraction.",
        "organism_layer": OrganismLayer.rna_contextual_transcription,
        "upstream_inputs": [
            packet_ref("ResearchSignalSet", "ccp_studio.contracts.research.ResearchSignalSet"),
            packet_ref("AudienceRealityBrief", "ccp_studio.contracts.context.AudienceRealityBrief"),
        ],
        "emitted_packets": [
            packet_ref("ContextPremise", "ccp_studio.contracts.context.ContextPremise"),
        ],
        "downstream_consumers": ["InterviewPreparationWorkflow", "JITSkillCompilerService"],
        "required_gates": [
            gate_ref("source_discipline_gate", "ccp_studio.gates.greenfield_gates.GreenfieldGateService"),
            gate_ref("anti_centroid_gate", "ccp_studio.services.jit_skill_compiler_service.JITSkillCompilerService"),
        ],
        "failure_modes": ["research vibe collapse", "unsupported audience assumption"],
        "proof_obligations": ["cite source document", "emit typed ContextPremise", "preserve downstream gate"],
        "source_document_refs": ["THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md#intentional-orchestration"],
        "typed_contract_or_registry_target": "ccp_studio.contracts.context.ContextPremise",
        "reviewer_actor_id": uuid4(),
    }
    values.update(overrides)
    return service.create_intent_record(**values)


def test_orchestration_module_record_includes_purpose_layer_packets_consumers_gates_failures_and_proof():
    service = OrchestrationIntentService()

    record = _record(service)
    receipt = next(iter(service.repository.receipts.values()))

    assert record.product_purpose.startswith("Preserve CRAL")
    assert record.organism_layer == OrganismLayer.rna_contextual_transcription
    assert record.upstream_inputs[0].packet_name == "ResearchSignalSet"
    assert record.emitted_packets[0].packet_name == "ContextPremise"
    assert "InterviewPreparationWorkflow" in record.downstream_consumers
    assert record.required_gates[0].gate_name == "source_discipline_gate"
    assert "research vibe collapse" in record.failure_modes
    assert "emit typed ContextPremise" in record.proof_obligations
    assert receipt.decision_code == "ORCHESTRATION_INTENT_CREATED"


def test_cral_context_emotional_voice_svre_scene_modules_require_source_doc_and_typed_target():
    service = OrchestrationIntentService()

    with pytest.raises(OrchestrationIntentError) as source_exc:
        _record(service, source_document_refs=[])
    with pytest.raises(OrchestrationIntentError) as target_exc:
        _record(service, typed_contract_or_registry_target="")

    assert source_exc.value.code == "SOURCE_DOCUMENT_REQUIRED"
    assert target_exc.value.code == "ORCHESTRATION_TYPED_TARGET_REQUIRED"


def test_style_advice_or_prompt_snippet_summary_blocks_activation():
    service = OrchestrationIntentService()

    with pytest.raises(OrchestrationIntentError) as exc:
        _record(service, product_purpose="Used for better storytelling vibe and prompt snippet reuse.")

    assert exc.value.code == "ORCHESTRATION_INTENT_FLATTENED"


def test_missing_proof_obligations_blocks_migration_activation():
    service = OrchestrationIntentService()

    with pytest.raises(OrchestrationIntentError) as exc:
        _record(service, proof_obligations=[])

    assert exc.value.code == "ORCHESTRATION_PROOF_REQUIRED"


def test_authority_overlap_is_resolved_into_organism_layers():
    service = OrchestrationIntentService()
    cral = _record(service)
    svre = _record(
        service,
        product_purpose="Preserve SVRE visual research order before scene container generation.",
        organism_layer=OrganismLayer.force,
        emitted_packets=[packet_ref("VisualResearchManifest", "ccp_studio.contracts.visual.VisualResearchManifest")],
        typed_contract_or_registry_target="ccp_studio.contracts.visual.VisualResearchManifest",
    )

    review = service.resolve_authority_overlap(
        intent_record_ids=[
            cral.legacy_orchestration_intent_record_id,
            svre.legacy_orchestration_intent_record_id,
        ],
        resolved_layer_assignments={
            str(cral.legacy_orchestration_intent_record_id): OrganismLayer.rna_contextual_transcription,
            str(svre.legacy_orchestration_intent_record_id): OrganismLayer.force,
        },
        reviewer_actor_id=uuid4(),
        decision="CRAL owns context transcription; SVRE owns visual force inputs.",
    )

    assert review.decision.startswith("CRAL owns")
    assert review.resolved_layer_assignments[str(svre.legacy_orchestration_intent_record_id)] == OrganismLayer.force


def test_downstream_story_or_spec_can_inherit_gates_from_approved_intent_record():
    service = OrchestrationIntentService()
    record = service.approve_intent_record(intent_record_id=_record(service).legacy_orchestration_intent_record_id)

    inherited = service.inherit_gates_for_downstream(
        intent_record_id=record.legacy_orchestration_intent_record_id,
        downstream_ref="docs/tech-specs/TS-CMF-028-cral-context-premise-emotional-dna-and-root-down-induction.md",
    )

    assert inherited.inherited_gate_names == ["source_discipline_gate", "anti_centroid_gate"]
    assert "preserve downstream gate" in inherited.proof_obligations


def test_downstream_spec_cannot_cite_orchestration_module_without_intent_record():
    service = OrchestrationIntentService()

    with pytest.raises(OrchestrationIntentError) as exc:
        service.validate_downstream_reference(intent_record_id=None)

    assert exc.value.code == "ORCHESTRATION_INTENT_RECORD_REQUIRED"
