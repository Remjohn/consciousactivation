from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.agent_factory import (  # noqa: E402
    AgentActivationState,
    AgentReadinessEval,
    AgentRoleSpec,
    PersonaRegistryEntry,
    PrimitiveObligation,
)
from ccp_studio.contracts.operator_ui import ReviewEvidenceState, UiBlockerSummary, UiSurface  # noqa: E402
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.contracts.skills import SkillUseMode  # noqa: E402
from ccp_studio.services.agent_factory_service import AgentFactoryService  # noqa: E402
from ccp_studio.services.operator_ui_service import (  # noqa: E402
    ALLOWED_CUSTOMER_OFFERS,
    OperatorUiError,
    OperatorUiService,
)


def _blocker(code: str = "CONSENT_REQUIRED") -> UiBlockerSummary:
    return UiBlockerSummary(
        blocker_code=code,
        severity="hard",
        object_ref="content_asset:blocked",
        required_action="repair_in_pwa",
    )


def test_content_asset_codes_format_registry_and_pricing_are_operator_safe():
    service = OperatorUiService()

    code = service.render_asset_code(
        brand_workspace_code="CEL",
        guest_code="CLDNTA",
        session_code="S01",
        package_code="GAP",
        format_code="SV-CSC",
        sequence_number=1,
        version_number=1,
    )
    assert code.rendered_code == "CEL-CLDNTA-S01-GAP-SV-CSC-001-V01"

    registry = service.content_format_registry()
    valid_codes = {subformat.code for family in registry.format_families for subformat in family.subformats}
    assert {"SV-CSC", "SV-EDU", "SV-FRB", "SV-RRC", "CAR-JUX", "VPL-WYR", "TWQ-STD", "MEM-REL", "SPV-CON"}.issubset(valid_codes)
    assert registry.forbidden_formats == ["newsletter"]

    with pytest.raises(OperatorUiError) as newsletter:
        service.render_asset_code(
            brand_workspace_code="CEL",
            guest_code="CLDNTA",
            session_code="S01",
            package_code="GAP",
            format_code="newsletter",
            sequence_number=1,
            version_number=1,
        )
    assert newsletter.value.code == "CONTENT_FORMAT_FORBIDDEN"

    shell = service.build_shell_state(
        operator_user_id=uuid4(),
        active_role_key="operator",
        organization_id=uuid4(),
        organization_name="Conscious Elite",
        brand_workspace_id=uuid4(),
        brand_workspace_code="CEL",
        brand_workspace_display_name="Conscious Elite",
    )
    control_tower = service.build_control_tower_state(shell)
    assert control_tower.commercial_summary.allowed_customer_offers == ALLOWED_CUSTOMER_OFFERS
    assert "newsletter" in control_tower.commercial_summary.forbidden_offer_warnings[0]
    assert control_tower.monthly_entry_artifact == "interview_brief"
    assert control_tower.primary_monthly_command_type == "generate_monthly_interview_brief"
    assert control_tower.pipeline_stage_summaries[0]["stage_key"] == "monthly_interview_brief"
    assert control_tower.pipeline_stage_summaries[0]["primary"] is True
    assert control_tower.pipeline_stage_summaries[1]["stage_key"] == "existing_interview_ingestion"
    assert control_tower.pipeline_stage_summaries[1]["fallback"] is True
    assert "no new interview" in control_tower.pipeline_stage_summaries[1]["entry_rule"]


def test_ui_command_envelope_preserves_scope_contract_version_and_receipt_blockers():
    service = OperatorUiService()
    org_id = uuid4()
    brand_id = uuid4()
    guest_id = uuid4()
    asset_id = uuid4()

    envelope = service.create_command_envelope(
        requested_by_user_id=uuid4(),
        requested_role_key="reviewer",
        organization_id=org_id,
        brand_workspace_id=brand_id,
        guest_id=guest_id,
        active_object_type="content_asset",
        active_object_id=asset_id,
        command_type="approve_review_object",
        command_payload={"public_or_high_risk": False},
        source_surface=UiSurface.pwa,
        source_route="/review/content_asset",
        expected_object_version="asset:v1",
    )

    assert envelope.organization_id == org_id
    assert envelope.brand_workspace_id == brand_id
    assert envelope.guest_id == guest_id
    assert envelope.generated_contract_version.startswith("cmf-ui-contracts")

    receipt = service.submit_ui_command(
        envelope,
        blockers=[_blocker()],
        content_asset_code="CEL-CLDNTA-S01-GAP-SV-CSC-001-V01",
    )
    assert receipt.status == "rejected"
    assert receipt.blockers[0].blocker_code == "CONSENT_REQUIRED"


def test_telegram_quick_action_rejects_stale_or_complex_review_and_requires_pwa_deeplink():
    service = OperatorUiService()
    envelope = service.create_command_envelope(
        requested_by_user_id=uuid4(),
        requested_role_key="reviewer",
        organization_id=uuid4(),
        brand_workspace_id=uuid4(),
        guest_id=uuid4(),
        active_object_type="content_asset",
        active_object_id=uuid4(),
        command_type="approve_review_object",
        command_payload={"public_or_high_risk": True, "primitive_failures": True},
        source_surface=UiSurface.telegram,
        source_route="telegram:review",
        expected_object_version="asset:v1",
    )

    receipt = service.submit_ui_command(
        envelope,
        object_version_current=False,
        pwa_deep_link="/review/content_asset/123",
    )

    assert receipt.status == "rejected"
    assert any(blocker.blocker_code == "TELEGRAM_PWA_REVIEW_REQUIRED" for blocker in receipt.blockers)
    assert any(result.code == "STALE_OBJECT_VERSION" for result in receipt.validation_results)


def test_review_evidence_preserves_composition_json_and_disables_approval_on_hard_blockers():
    service = OperatorUiService()
    review = service.build_review_evidence_state(
        ReviewEvidenceState(
            review_object_id=uuid4(),
            review_object_type="render_output",
            content_asset_code="CEL-CLDNTA-S01-GAP-SPV-CON-001-V01",
            source_quote="The guest named the exact contradiction.",
            transcript_timestamp_range="00:12:10-00:13:42",
            source_artifact_refs=["transcript:12-18"],
            expression_moment_id=uuid4(),
            route_receipt_id=uuid4(),
            scene_spec_id=uuid4(),
            composition_job_id=uuid4(),
            composition_job_json={"layers": [{"role": "subject", "position": "left"}]},
            render_output_id=uuid4(),
            primitive_failures=[{"primitive": "FBK", "reason": "edge softened"}],
            consent_state={"status": "valid"},
            approval_blockers=[_blocker("PRIMITIVE_FAILURE_REVIEW_REQUIRED")],
        )
    )

    assert review.composition_job_json["layers"][0]["role"] == "subject"
    assert review.next_valid_review_commands[0].enabled is False
    assert review.next_valid_review_commands[0].disabled_reason == "hard blocker requires repair"


def test_agent_factory_ui_state_exposes_roles_readiness_and_jit_modes():
    agent_service = AgentFactoryService()
    agent_service.register_persona(
        PersonaRegistryEntry(
            persona_registry_entry_id=uuid4(),
            entity_code="RES-VISRSCH-AG",
            department_code="RES",
            service_code="VISRSCH",
            entity_type="AG",
            display_name="Visual Research Agent",
            persona_name="Aurore",
            service_scope="researches visual evidence candidates",
            source_refs=["docs/cmf-studio-agent-factory-registry.md"],
            active=True,
        )
    )
    spec = agent_service.register_agent_role_spec(
        AgentRoleSpec(
            agent_role_spec_id=uuid4(),
            entity_code="RES-VISRSCH-AG",
            department_key="RES",
            service_code="VISRSCH",
            display_name="Visual Research Agent",
            persona_name="Aurore",
            goal="Find source-grounded visual candidates.",
            fit_rationale="Bounded research agent with evidence and receipt obligations.",
            pipeline_stage_refs=["research"],
            active_object_types=["SourceArtifact"],
            entry_object_contracts=["SourceArtifact"],
            exit_object_contracts=["VisualResearchCandidateSet"],
            allowed_tool_refs=["visual_research.lookup"],
            jit_skill_mode_refs=[SkillUseMode.source_expression_contrast],
            eval_refs=["eval.visual_research.source_alignment"],
            memory_access_policy_ref="current_guest_visual_memory",
            blocked_actions=["direct_repository_write"],
            required_receipt_types=["VisualResearchReceipt"],
            activation_state=AgentActivationState.draft,
        )
    )
    readiness = agent_service.run_agent_readiness_eval(
        AgentReadinessEval(
            agent_readiness_eval_id=uuid4(),
            entity_code=spec.entity_code,
            target_spec_ref=str(spec.agent_role_spec_id),
            primitive_obligations=[
                PrimitiveObligation(
                    primitive_family="FBK",
                    obligation="preserve source contrast",
                    evidence_ref="registries/primitives/FBK.md",
                )
            ],
            tool_scope_passed=True,
            memory_policy_passed=True,
            eval_bindings_passed=True,
            receipt_obligations_passed=True,
            blocked_actions_passed=True,
            adapter_boundary_passed=True,
            status="accepted",
            findings=[],
            created_at=utc_now(),
        )
    )
    agent_service.activate_agent_role_spec(spec.entity_code, readiness_eval_id=readiness.agent_readiness_eval_id)

    ui_service = OperatorUiService(agent_factory_repository=agent_service.repository)
    state = ui_service.build_agent_factory_state(brand_workspace_id=uuid4())

    assert state.agents[0]["entity_code"] == "RES-VISRSCH-AG"
    assert state.readiness_findings[0]["status"] == "accepted"
    assert {"mode": "interview_engineering"} in state.jit_skill_modes
