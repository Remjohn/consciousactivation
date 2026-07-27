from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.agent_factory import (  # noqa: E402
    AdapterExportTarget,
    AgentActivationState,
    AgentReadinessEval,
    AgentRoleSpec,
    DepartmentSpec,
    ExtensionSpec,
    HookSpec,
    LifecycleBoundary,
    PersonaRegistryEntry,
    PrimitiveObligation,
    SkillBinding,
    SkillBindingType,
    SubAgentInvocationRequest,
    SubAgentOutputEnvelope,
    SubAgentRoleSpec,
    ToolCapabilityKind,
    ToolCapabilitySpec,
    ToolInvocationRequest,
)
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.contracts.skills import (  # noqa: E402
    DSPyProgramSpec,
    JITSkillCompiler,
    SaturationContextBundle,
    SkillUseMode,
)
from ccp_studio.services.agent_factory_service import AgentFactoryError, AgentFactoryService  # noqa: E402
from ccp_studio.services.jit_skill_compiler_service import JITSkillCompilerError, JITSkillCompilerService  # noqa: E402


def _persona(code: str, display: str, scope: str) -> PersonaRegistryEntry:
    parts = code.split("-")
    return PersonaRegistryEntry(
        persona_registry_entry_id=uuid4(),
        entity_code=code,
        department_code=parts[0],
        service_code=parts[1],
        entity_type=parts[2],
        display_name=display,
        persona_name=display.split()[0],
        service_scope=scope,
        source_refs=["docs/cmf-studio-agent-factory-registry.md"],
        active=True,
    )


def _register_personas(service: AgentFactoryService) -> None:
    service.register_persona(_persona("RES-VISRSCH-AG", "Visual Research Agent", "researches visual evidence candidates"))
    service.register_persona(_persona("RES-EVDCRIT-SA", "Evidence Critic Sub-Agent", "scores source evidence alignment"))
    service.register_persona(_persona("REV-APPGATE-HK", "Approval Gate Hook", "checks approval lifecycle blockers"))
    service.register_persona(_persona("PUB-PUBLERX-EX", "Publer Extension", "mounts publishing integration tools"))
    service.register_persona(_persona("EXT-JITCOMP-JS", "JIT Compiler Skill", "compiles saturation bound extraction"))
    service.register_persona(_persona("OPS-CMDBUSX-SK", "Command Bus Skill", "submits governed command envelopes"))


def _agent_spec(code: str = "RES-VISRSCH-AG") -> AgentRoleSpec:
    return AgentRoleSpec(
        agent_role_spec_id=uuid4(),
        entity_code=code,
        department_key=code.split("-")[0],
        service_code=code.split("-")[1],
        display_name="Visual Research Agent",
        persona_name="Aurore",
        goal="Find source-grounded visual candidates for a guest-scoped production stage.",
        fit_rationale="The role is bounded to research artifacts, evidence, and candidate receipts.",
        pipeline_stage_refs=["research", "production"],
        active_object_types=["SourceArtifact", "VisualResearchCandidate"],
        entry_object_contracts=["SourceArtifact"],
        exit_object_contracts=["VisualResearchCandidateSet"],
        allowed_tool_refs=["visual_research.lookup", "command_bus.submit"],
        stable_skill_refs=["OPS-CMDBUSX-SK"],
        jit_skill_mode_refs=[SkillUseMode.source_expression_contrast],
        hook_refs=["REV-APPGATE-HK"],
        eval_refs=["eval.visual_research.source_alignment"],
        memory_access_policy_ref="current_guest_visual_memory",
        blocked_actions=["direct_repository_write", "bypass_command_bus"],
        required_receipt_types=["VisualResearchReceipt"],
        activation_state=AgentActivationState.draft,
    )


def _active_agent(service: AgentFactoryService) -> AgentRoleSpec:
    _register_personas(service)
    service.register_department(
        DepartmentSpec(
            department_key="RES",
            display_name="Research",
            pipeline_stage_refs=["research", "production"],
            owned_object_types=["SourceArtifact", "VisualResearchCandidate"],
            proof_obligations=["source evidence", "evaluation receipt"],
        )
    )
    spec = service.register_agent_role_spec(_agent_spec())
    readiness = service.run_agent_readiness_eval(
        AgentReadinessEval(
            agent_readiness_eval_id=uuid4(),
            entity_code=spec.entity_code,
            target_spec_ref=str(spec.agent_role_spec_id),
            primitive_obligations=[
                PrimitiveObligation(
                    primitive_family="FBK",
                    obligation="visual candidate must preserve source friction",
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
    return service.activate_agent_role_spec(spec.entity_code, readiness_eval_id=readiness.agent_readiness_eval_id)


def test_persona_registry_validates_exact_code_shape_service_signal_and_duplicates():
    service = AgentFactoryService()
    parts = service.validate_persona_code("RES-VISRSCH-AG")
    assert parts.department_code == "RES"
    assert parts.service_code == "VISRSCH"

    service.register_persona(_persona("RES-VISRSCH-AG", "Visual Research Agent", "researches visual evidence candidates"))

    with pytest.raises(AgentFactoryError) as duplicate:
        service.register_persona(_persona("RES-VISRSCH-AG", "Visual Research Agent", "researches visual evidence candidates"))
    assert duplicate.value.code == "PERSONA_CODE_DUPLICATE"

    with pytest.raises(AgentFactoryError) as invalid:
        service.validate_persona_code("RES-VIS-AG")
    assert invalid.value.code == "PERSONA_CODE_INVALID"

    with pytest.raises(AgentFactoryError) as vague:
        service.register_persona(_persona("RES-AUROREX-AG", "Aurore Agent", "generic prompt-only helper"))
    assert vague.value.code == "PERSONA_REGISTRY_REJECTED"


def test_agent_role_activation_requires_registered_persona_mutation_blocker_and_readiness_eval():
    service = AgentFactoryService()
    _register_personas(service)
    spec = service.register_agent_role_spec(_agent_spec())

    with pytest.raises(AgentFactoryError) as missing_readiness:
        service.activate_agent_role_spec(spec.entity_code, readiness_eval_id=uuid4())
    assert missing_readiness.value.code == "AGENT_READINESS_REQUIRED"

    readiness = service.run_agent_readiness_eval(
        AgentReadinessEval(
            agent_readiness_eval_id=uuid4(),
            entity_code=spec.entity_code,
            target_spec_ref=str(spec.agent_role_spec_id),
            primitive_obligations=[],
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
    assert readiness.status == "revision_required"

    accepted = service.run_agent_readiness_eval(
        readiness.model_copy(
            update={
                "agent_readiness_eval_id": uuid4(),
                "status": "accepted",
                "findings": [],
                "primitive_obligations": [
                    PrimitiveObligation(
                        primitive_family="SAF",
                        obligation="keep source evidence attached to visual choice",
                        evidence_ref="registries/primitives/SAF.md",
                    )
                ],
            }
        )
    )
    activated = service.activate_agent_role_spec(spec.entity_code, readiness_eval_id=accepted.agent_readiness_eval_id)
    assert activated.activation_state == AgentActivationState.active
    assert activated.readiness_eval_id == accepted.agent_readiness_eval_id


def test_sub_agent_delegation_is_parent_bounded_and_read_only_by_default():
    service = AgentFactoryService()
    parent = _active_agent(service)
    sub_agent = service.register_sub_agent_role_spec(
        SubAgentRoleSpec(
            sub_agent_role_spec_id=uuid4(),
            entity_code="RES-EVDCRIT-SA",
            parent_agent_refs=[parent.entity_code],
            invocation_conditions=["visual candidate needs source alignment critique"],
            input_model_ref="VisualResearchCandidateSet",
            output_model_ref="EvidenceCritique",
            allowed_context_fields=["source_artifact_refs", "candidate_refs"],
            allowed_tool_refs=["visual_research.lookup"],
            mutation_policy="read_only",
            required_evidence_refs=["source_artifact_refs"],
            blocked_actions=["direct_canonical_write"],
            receipt_type="SubAgentReceipt",
        )
    )

    with pytest.raises(AgentFactoryError) as mutation:
        service.invoke_sub_agent(
            SubAgentInvocationRequest(
                orchestration_run_id=uuid4(),
                stage_execution_plan_id=uuid4(),
                parent_agent_code=parent.entity_code,
                sub_agent_code=sub_agent.entity_code,
                requested_task="score evidence",
                input_payload={"candidate": "visual:001"},
                requested_tool_refs=["visual_research.lookup"],
                evidence_refs=["source:001"],
                attempts_state_mutation=True,
            ),
            SubAgentOutputEnvelope(
                sub_agent_code=sub_agent.entity_code,
                parent_agent_code=parent.entity_code,
                output_payload={"score": 0.91},
                evidence_refs=["source:001"],
                downstream_parent_decision="use as critique only",
            ),
        )
    assert mutation.value.code == "SUB_AGENT_MUTATION_FORBIDDEN"


def test_hooks_extensions_skills_tools_and_adapters_enforce_runtime_boundaries():
    service = AgentFactoryService()
    parent = _active_agent(service)

    with pytest.raises(AgentFactoryError) as creative_hook:
        service.register_hook_spec(
            HookSpec(
                hook_spec_id=uuid4(),
                entity_code="REV-APPGATE-HK",
                lifecycle_boundary=LifecycleBoundary.before_publishing,
                trigger_condition="publication requested",
                allowed_checks=["creative rewrite captions"],
                blocked_mutations=["approval_state"],
                emitted_receipt_type="HookExecutionReceipt",
                failure_behavior="block",
            )
        )
    assert creative_hook.value.code == "HOOK_CREATIVE_REASONING_BLOCKED"

    hook = service.register_hook_spec(
        HookSpec(
            hook_spec_id=uuid4(),
            entity_code="REV-APPGATE-HK",
            lifecycle_boundary=LifecycleBoundary.before_publishing,
            trigger_condition="publication requested",
            allowed_checks=["lineage_complete", "consent_compatible"],
            blocked_mutations=["approval_state"],
            emitted_receipt_type="HookExecutionReceipt",
            failure_behavior="block",
        )
    )
    hook_receipt = service.run_hook(entity_code=hook.entity_code, blocker_present=True)
    assert hook_receipt.decision_code == "blocked"

    extension = service.register_extension_spec(
        ExtensionSpec(
            extension_spec_id=uuid4(),
            entity_code="PUB-PUBLERX-EX",
            integration_scope="schedules approved publishing intents only",
            exposed_tool_refs=["publer.schedule"],
            credential_boundary_ref="vault:publer",
            canonical_state_authority="none",
            required_receipt_types=["PublishingJobReceipt"],
        )
    )
    assert service.mount_extension(extension.entity_code).decision_code == "mounted"

    binding = service.bind_skill(
        SkillBinding(
            skill_binding_id=uuid4(),
            skill_entity_code="EXT-JITCOMP-JS",
            binding_type=SkillBindingType.jit,
            agent_role_ref=parent.entity_code,
            allowed_stage_refs=["research"],
            allowed_use_modes=[SkillUseMode.interview_engineering, SkillUseMode.narrative_induction],
            jit_compiler_ref="jit.interview_brief.v1",
            required_invocation_record=True,
            output_schema_ref="InterviewBrief",
            evaluation_target_refs=["eval.interview_brief.source_specificity"],
        )
    )
    assert service.activate_skill_binding(binding.skill_binding_id).active is True

    with pytest.raises(AgentFactoryError) as unsafe_tool:
        service.register_tool_capability(
            ToolCapabilitySpec(
                tool_capability_spec_id=uuid4(),
                tool_key="unsafe.direct.write",
                kind=ToolCapabilityKind.command,
                department_code="RES",
                allowed_agent_refs=[parent.entity_code],
                allowed_stage_refs=["research"],
                input_model_ref="CommandEnvelope",
                output_model_ref="CommandReceipt",
                idempotency_required=True,
                required_receipt_type="CommandReceipt",
                mutation_boundary="none",
                failure_behavior="block",
            )
        )
    assert unsafe_tool.value.code == "TOOL_MUTATION_BOUNDARY_REQUIRED"

    tool = service.register_tool_capability(
        ToolCapabilitySpec(
            tool_capability_spec_id=uuid4(),
            tool_key="command_bus.submit",
            kind=ToolCapabilityKind.command,
            department_code="RES",
            allowed_agent_refs=[parent.entity_code],
            allowed_stage_refs=["research"],
            input_model_ref="CommandEnvelope",
            output_model_ref="CommandReceipt",
            idempotency_required=True,
            required_receipt_type="CommandReceipt",
            mutation_boundary="command_bus",
            failure_behavior="block",
        )
    )
    receipt = service.invoke_tool_capability(
        ToolInvocationRequest(
            tool_key=tool.tool_key,
            requesting_agent_code=parent.entity_code,
            stage_ref="research",
            input_payload={"command": "record_visual_candidate"},
            idempotency_key="tool:001",
            requested_mutation_boundary="command_bus",
        )
    )
    assert receipt.decision_code == "allowed"

    missing = service.invoke_tool_capability(
        ToolInvocationRequest(
            tool_key="invented.tool",
            requesting_agent_code=parent.entity_code,
            stage_ref="research",
            input_payload={},
            requested_mutation_boundary="none",
        )
    )
    assert missing.decision_code == "handoff"

    export_receipt = service.export_agent_adapter(entity_code=parent.entity_code, target=AdapterExportTarget.google_adk)
    export = service.repository.adapter_exports[export_receipt.adapter_export_id]
    drift_receipt = service.run_adapter_drift_check(
        adapter_export_id=export.adapter_export_id,
        current_files={export.generated_files[0].path: "hand edited adapter"},
    )
    assert drift_receipt.decision_code == "drift_detected"


def test_jit_compiler_supports_new_modes_and_blocks_scene_prompt_before_route_context():
    assert SkillUseMode.interview_engineering.value == "interview_engineering"
    assert SkillUseMode.narrative_induction.value == "narrative_induction"
    assert SkillUseMode.source_expression_contrast.value == "source_expression_contrast"
    assert SkillUseMode.scene_prompt_support_after_route.value == "scene_prompt_support_after_route"

    service = JITSkillCompilerService()
    spec = DSPyProgramSpec(
        schema_version="cmf.dspy_program_spec.v1",
        dspy_program_spec_id=uuid4(),
        program_key="jit.scene_prompt_support",
        input_model="SaturationContextBundle",
        output_model="ScenePromptSupport",
        version="2026.06.22",
        fixture_set_ids=[uuid4()],
        evaluation_target_ids=[uuid4()],
        eval_threshold=0.8,
    )
    service.register_program_spec(spec)
    compiler = JITSkillCompiler(
        schema_version="cmf.jit_skill_compiler.v1",
        skill_key="scene_prompt_support_jit",
        allowed_use_modes=[SkillUseMode.scene_prompt_support_after_route],
        dspy_program_spec_id=spec.dspy_program_spec_id,
        registry_snapshot_id=uuid4(),
        output_schema="ScenePromptSupport",
        compiler_fingerprint="jit-scene-post-route-v1",
        approved=True,
    )
    service.register_compiler(compiler)

    with pytest.raises(JITSkillCompilerError) as pre_route:
        service.invoke(
            skill_key="scene_prompt_support_jit",
            use_mode=SkillUseMode.scene_prompt_support_after_route,
            saturation_context=SaturationContextBundle(
                schema_version="cmf.saturation_context_bundle.v1",
                source_doc_refs=["source:deck"],
                transcript_segment_refs=["transcript:12-18"],
                prior_evaluation_receipt_ids=[uuid4()],
                failure_corpus_refs=["failure:generic-scene"],
            ),
            candidate_texts=["Source-specific scene prompt support after routing."],
            contrast_texts=["Generic visual prompt without route context."],
            evidence_refs=["route:missing"],
            confidence=0.9,
            eval_score=0.9,
        )
    assert pre_route.value.code == "SCENE_PROMPT_SUPPORT_PRE_ROUTE_BLOCKED"
