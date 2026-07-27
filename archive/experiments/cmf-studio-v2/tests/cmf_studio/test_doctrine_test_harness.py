from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope
from ccp_studio.contracts.doctrine_tests import (
    DoctrineInvariant,
    DoctrineNegativeFixture,
    DoctrinePrimitiveTestObligation,
    DoctrineTestDecision,
    new_doctrine_test_target,
)
from ccp_studio.services.command_bus import create_in_memory_command_bus
from ccp_studio.services.doctrine_test_harness import (
    DoctrineTestHarnessService,
    register_doctrine_test_harness_command_handlers,
)


def _invariant() -> DoctrineInvariant:
    return DoctrineInvariant(
        schema_version="cmf.doctrine_invariant.v1",
        invariant_id="INV-CMF-COMPOSITION-JSON",
        name="Ideogram 4 composition JSON must be traceable",
        statement="Reaction and visual outputs must be derived from explicit composition JSON.",
        source_doctrine_refs=[
            "THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md",
            "THE CMF STUDIO/CCP V9.1 - Expression Capture & Archetype Routing Update.md",
        ],
        applies_to_target_types=["reaction_clip_template"],
        required_evidence_types=["composition_json", "primitive_registry"],
        hard_failure_code="COMPOSITION_JSON_LINEAGE_MISSING",
        approval_blocker_code="BLOCK_COMPOSITION_JSON_LINEAGE_MISSING",
    )


def _primitive_obligation() -> DoctrinePrimitiveTestObligation:
    return DoctrinePrimitiveTestObligation(
        schema_version="cmf.doctrine_primitive_test_obligation.v1",
        primitive_ref="PRM-STR-001",
        primitive_family="STR",
        doctrine_binding="Signal must distill into a scene-shaping structure before output generation.",
        required_evidence_types=["primitive_registry", "signal_distillation"],
        hard_failure_code="STRUCTURE_PRIMITIVE_EVIDENCE_MISSING",
        approval_blocker_code="BLOCK_STRUCTURE_PRIMITIVE_EVIDENCE_MISSING",
    )


def _negative_fixture() -> DoctrineNegativeFixture:
    return DoctrineNegativeFixture(
        schema_version="cmf.doctrine_negative_fixture.v1",
        fixture_id="NEG-GENERIC-TOPIC-FIRST-QUESTION",
        forbidden_shortcut="topic-first interview question",
        description="Interview briefs cannot collapse into generic biographical or topic-first prompts.",
        required_absent_terms=["tell me about your background", "what is your story"],
        required_evidence_types=["negative_fixture_review"],
        hard_failure_code="GENERIC_INTERVIEW_SHORTCUT_DETECTED",
        approval_blocker_code="BLOCK_GENERIC_INTERVIEW_SHORTCUT_DETECTED",
    )


def test_missing_doctrine_invariant_evidence_blocks_approval():
    service = DoctrineTestHarnessService()
    target = new_doctrine_test_target(
        target_type="reaction_clip_template",
        target_id=uuid4(),
        pipeline_stage="composition_template_approval",
    )

    receipt = service.run_suite(
        organization_id=uuid4(),
        brand_id=uuid4(),
        target=target,
        actor_id=uuid4(),
        invariants=[_invariant()],
        evidence_by_key={"composition_json": ["composition_json:RCT-VS-SPLIT:v1"]},
    )

    assert receipt.decision == DoctrineTestDecision.blocked
    assert receipt.hard_failures == ["COMPOSITION_JSON_LINEAGE_MISSING"]
    assert receipt.approval_blocker_codes == ["BLOCK_COMPOSITION_JSON_LINEAGE_MISSING"]
    assert receipt.invariant_results[0].missing_evidence_types == ["primitive_registry"]


def test_complete_doctrine_primitive_and_negative_fixture_evidence_passes():
    service = DoctrineTestHarnessService()
    target = new_doctrine_test_target(
        target_type="reaction_clip_template",
        target_id=uuid4(),
        pipeline_stage="composition_template_approval",
        lineage_refs=["composition_json:RCT-VS-SPLIT:v1"],
    )

    receipt = service.run_suite(
        organization_id=uuid4(),
        brand_id=uuid4(),
        target=target,
        actor_id=uuid4(),
        invariants=[_invariant()],
        primitive_obligations=[_primitive_obligation()],
        negative_fixtures=[_negative_fixture()],
        evidence_by_key={
            "primitive_registry": ["primitive_registry:PRM-STR-001"],
            "signal_distillation": ["signal_distillation:approved"],
            "negative_fixture_review": ["negative_fixture_review:operator-approved"],
        },
        observed_text="How did that contradiction first become visible in your body and decisions?",
    )

    assert receipt.decision == DoctrineTestDecision.passed
    assert not receipt.hard_failures
    assert receipt.invariant_results[0].passed
    assert receipt.primitive_results[0].passed
    assert receipt.negative_fixture_results[0].passed
    assert receipt.receipt_hash and receipt.receipt_hash != "pending"


def test_negative_fixture_blocks_generic_interview_shortcut():
    service = DoctrineTestHarnessService()
    target = new_doctrine_test_target(
        target_type="interview_brief",
        target_id=uuid4(),
        pipeline_stage="conscious_interview_brief",
    )

    receipt = service.run_suite(
        organization_id=uuid4(),
        brand_id=uuid4(),
        target=target,
        actor_id=uuid4(),
        negative_fixtures=[_negative_fixture()],
        evidence_by_key={"negative_fixture_review": ["negative_fixture_review:pending"]},
        observed_text="Tell me about your background and what made you start.",
    )

    assert receipt.decision == DoctrineTestDecision.blocked
    assert receipt.negative_fixture_results[0].triggered_terms == ["tell me about your background"]
    assert "GENERIC_INTERVIEW_SHORTCUT_DETECTED" in receipt.hard_failures


def test_spec_audit_mode_blocks_specs_without_doctrine_harness_binding(tmp_path):
    spec_path = tmp_path / "TS-CMF-999-shallow.md"
    spec_path.write_text(
        "# TS-CMF-999\n\n## Files Read\n- product brief\n\n## Testing Strategy\n- unit tests\n",
        encoding="utf-8",
    )
    service = DoctrineTestHarnessService()

    receipt = service.audit_spec_file(
        organization_id=uuid4(),
        brand_id=uuid4(),
        spec_path=str(spec_path),
        actor_id=uuid4(),
        spec_id="TS-CMF-999",
    )

    assert receipt.decision == DoctrineTestDecision.blocked
    assert "SPEC_DOCTRINE_TEST_HARNESS_BINDING_MISSING" in receipt.hard_failures
    assert "SPEC_LEGACY_INVENTORY_MISSING" in receipt.hard_failures
    assert "SPEC_PIPELINE_STAGE_TRACE_MISSING" in receipt.hard_failures


def test_command_bus_runs_doctrine_test_suite_and_records_event():
    org_id = uuid4()
    brand_id = uuid4()
    actor = ActorContext(
        actor_id=uuid4(),
        actor_type=ActorType.human,
        role_ids=["owner"],
    )
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    service = DoctrineTestHarnessService()
    register_doctrine_test_harness_command_handlers(bus, service)
    target = new_doctrine_test_target(
        target_type="reaction_clip_template",
        target_id=uuid4(),
        pipeline_stage="composition_template_approval",
        lineage_refs=["composition_json:RCT-VS-SPLIT:v1"],
    )
    envelope = new_command_envelope(
        command_type="RunDoctrineTestSuiteCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "target": target.model_dump(mode="json"),
            "invariants": [_invariant().model_dump(mode="json")],
            "evidence_by_key": {
                "primitive_registry": ["primitive_registry:PRM-STR-001"],
            },
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["decision"] == DoctrineTestDecision.passed.value
    assert bus.event_outbox.events[-1].event_type == "RunDoctrineTestSuiteCommand.succeeded"
    assert len(service.repository.receipts) == 1
