import pytest
from ccp_studio.contracts.provider_runtime import (
    PassStatus, ProviderCapabilityProfile, ProviderCostEstimate, ProviderExecutionMode, ProviderJob,
    ProviderJobInput, ProviderJobKind, ProviderJobOutput, ProviderJobReceipt, ProviderJobStatus,
    ProviderName, ProviderOutputAssetRole, ProviderRetryPolicy, ProviderRole, ProviderSampleApprovalGate
)
from ccp_studio.services.flux_provider_runtime_service import FluxProviderRuntimeService
from ccp_studio.services.ideogram_provider_runtime_service import IdeogramProviderRuntimeService
from ccp_studio.services.provider_capability_profile_service import ProviderCapabilityProfileService
from ccp_studio.services.provider_cost_estimate_service import ProviderCostEstimateService
from ccp_studio.services.provider_decision_log_service import ProviderDecisionLogService
from ccp_studio.services.provider_job_service import ProviderJobService
from ccp_studio.services.provider_output_asset_service import ProviderOutputAssetService
from ccp_studio.services.provider_retry_policy_service import ProviderRetryPolicyService
from ccp_studio.services.provider_sample_approval_service import ProviderSampleApprovalService
from ccp_studio.services.provider_runtime_service import ProviderRuntimeService


def _decision(provider_name=ProviderName.IDEOGRAM, job_kind=ProviderJobKind.SCENE_SAMPLE):
    role = ProviderRole.COMPOSITION_PLATE_GENERATOR if provider_name == ProviderName.IDEOGRAM else ProviderRole.REFERENCE_BASED_OBJECT_EDITOR
    cost = ProviderCostEstimateService().estimate(provider_name, job_kind)
    return ProviderDecisionLogService().compile_decision(provider_name, role, job_kind, "reason", cost, "sample")


def test_provider_capability_available_requires_configured_and_tested():
    with pytest.raises(Exception):
        ProviderCapabilityProfile(provider_name=ProviderName.IDEOGRAM, provider_role=ProviderRole.COMPOSITION_PLATE_GENERATOR, capability_id="provider:image:ideogram", configured=True, tested=False, available=True, supported_job_kinds=[ProviderJobKind.SCENE_SAMPLE])


def test_ideogram_and_flux_roles_are_canonical():
    caps = ProviderCapabilityProfileService()
    assert caps.compile_ideogram_profile(True, True, True).provider_role == ProviderRole.COMPOSITION_PLATE_GENERATOR
    assert caps.compile_flux_profile(True, True, True).provider_role == ProviderRole.REFERENCE_BASED_OBJECT_EDITOR


def test_cost_estimate_validates_range():
    with pytest.raises(Exception):
        ProviderCostEstimate(provider_name=ProviderName.IDEOGRAM, job_kind=ProviderJobKind.SCENE_SAMPLE, min_usd=1, max_usd=.5)


def test_retry_policy_blocks_unlimited_attempts():
    with pytest.raises(Exception):
        ProviderRetryPolicy(max_attempts=999)
    assert ProviderRetryPolicyService().default_policy().can_attempt(1)


def test_sample_gate_requires_all_three_samples_for_batch():
    gate = ProviderSampleApprovalService().compile_gate(scene_sample_approved=True, face_plate_sample_approved=True, template_preview_sample_approved=False, approved_by="operator")
    assert not gate.batch_approved
    receipt = ProviderSampleApprovalService().compile_batch_policy_receipt(gate, batch_requested=True)
    assert receipt.pass_status == PassStatus.FAIL


def test_sample_gate_cannot_approve_with_blockers():
    with pytest.raises(Exception):
        ProviderSampleApprovalGate(scene_sample_approved=True, face_plate_sample_approved=True, template_preview_sample_approved=True, approved_by="operator", blockers=["bad sample"])


def test_provider_input_requires_source_refs_and_roles():
    with pytest.raises(Exception):
        ProviderJobInput(provider_name=ProviderName.IDEOGRAM, provider_role=ProviderRole.COMPOSITION_PLATE_GENERATOR, job_kind=ProviderJobKind.SCENE_SAMPLE, input_payload={"prompt": "x"}, source_refs=[])
    with pytest.raises(Exception):
        ProviderJobInput(provider_name=ProviderName.FLUX, provider_role=ProviderRole.COMPOSITION_PLATE_GENERATOR, job_kind=ProviderJobKind.FACE_PLATE_SAMPLE, input_payload={"prompt": "x"}, source_refs=["s"])


def test_provider_decision_log_requires_matching_cost_provider():
    cost = ProviderCostEstimateService().estimate(ProviderName.FLUX, ProviderJobKind.FACE_PLATE_SAMPLE)
    with pytest.raises(Exception):
        ProviderDecisionLogService().compile_decision(ProviderName.IDEOGRAM, ProviderRole.COMPOSITION_PLATE_GENERATOR, ProviderJobKind.SCENE_SAMPLE, "Use Ideogram", cost, "sample")


def test_provider_job_blocks_provider_calls_and_real_execution():
    job_service = ProviderJobService()
    provider_input = job_service.compile_input(ProviderName.IDEOGRAM, ProviderRole.COMPOSITION_PLATE_GENERATOR, ProviderJobKind.SCENE_SAMPLE, {"prompt": "scene"}, ["scene_1"])
    decision = _decision()
    with pytest.raises(Exception):
        ProviderJob(provider_name=ProviderName.IDEOGRAM, provider_role=ProviderRole.COMPOSITION_PLATE_GENERATOR, job_kind=ProviderJobKind.SCENE_SAMPLE, job_input=provider_input, capability_profile_id="cap", decision_log=decision, provider_calls_allowed=True)
    with pytest.raises(Exception):
        ProviderJob(provider_name=ProviderName.IDEOGRAM, provider_role=ProviderRole.COMPOSITION_PLATE_GENERATOR, job_kind=ProviderJobKind.SCENE_SAMPLE, job_input=provider_input, capability_profile_id="cap", decision_log=decision, execution_mode=ProviderExecutionMode.REAL_PROVIDER)


def test_batch_job_requires_three_sample_approvals():
    job_service = ProviderJobService()
    provider_input = job_service.compile_input(ProviderName.IDEOGRAM, ProviderRole.COMPOSITION_PLATE_GENERATOR, ProviderJobKind.COMPOSITION_PLATE_BATCH, {"batch": ["scene1"]}, ["scene_batch"])
    cost = ProviderCostEstimateService().estimate(ProviderName.IDEOGRAM, ProviderJobKind.COMPOSITION_PLATE_BATCH)
    decision = ProviderDecisionLogService().compile_decision(ProviderName.IDEOGRAM, ProviderRole.COMPOSITION_PLATE_GENERATOR, ProviderJobKind.COMPOSITION_PLATE_BATCH, "batch", cost, "batch")
    gate = ProviderSampleApprovalService().compile_gate(scene_sample_approved=True, face_plate_sample_approved=True, template_preview_sample_approved=False, approved_by="operator")
    with pytest.raises(Exception):
        job_service.compile_job(provider_input, "cap", decision, ProviderRetryPolicyService().default_policy(), gate, batch_requested=True)


def test_batch_job_compiles_after_three_sample_approvals():
    job_service = ProviderJobService()
    provider_input = job_service.compile_input(ProviderName.IDEOGRAM, ProviderRole.COMPOSITION_PLATE_GENERATOR, ProviderJobKind.COMPOSITION_PLATE_BATCH, {"batch": ["scene1"]}, ["scene_batch"])
    cost = ProviderCostEstimateService().estimate(ProviderName.IDEOGRAM, ProviderJobKind.COMPOSITION_PLATE_BATCH)
    decision = ProviderDecisionLogService().compile_decision(ProviderName.IDEOGRAM, ProviderRole.COMPOSITION_PLATE_GENERATOR, ProviderJobKind.COMPOSITION_PLATE_BATCH, "batch", cost, "batch")
    gate = ProviderSampleApprovalService().compile_gate(True, True, True, approved_by="operator")
    job = job_service.compile_job(provider_input, "cap", decision, ProviderRetryPolicyService().default_policy(), gate, batch_requested=True)
    assert job.batch_requested


def test_ideogram_scene_sample_fake_executes_and_emits_receipt():
    profile, job = IdeogramProviderRuntimeService().compile_scene_sample_job({"composition_prompt": "plate"}, ["composition_scene_1"])
    output, receipt = ProviderJobService().fake_execute(job)
    assert profile.provider_name == ProviderName.IDEOGRAM
    assert output.output_uri.startswith("fake://")
    assert receipt.pass_status == PassStatus.PASS
    assert not receipt.provider_calls_executed


def test_flux_face_plate_sample_fake_executes_and_emits_receipt():
    profile, job = FluxProviderRuntimeService().compile_face_plate_sample_job({"edit_instruction": "paperize face"}, ["avatar_identity"], ["face_ref"])
    output, receipt = ProviderJobService().fake_execute(job)
    assert profile.provider_name == ProviderName.FLUX
    assert output.output_sha256
    assert receipt.fake_execution


def test_provider_output_asset_ref_requires_receipt_and_sha():
    _, job = IdeogramProviderRuntimeService().compile_scene_sample_job({"composition_prompt": "plate"}, ["composition_scene_1"])
    out, rec = ProviderJobService().fake_execute(job)
    asset = ProviderOutputAssetService().compile_asset_ref(out, rec, ProviderOutputAssetRole.COMPOSITION_PLATE, ["composition_scene_1"])
    assert asset.provider_job_receipt_id == rec.provider_job_receipt_id
    assert asset.sha256 == out.output_sha256


def test_provider_job_output_blocks_real_provider_execution_flag():
    with pytest.raises(Exception):
        ProviderJobOutput(provider_job_id="job", provider_name=ProviderName.IDEOGRAM, job_kind=ProviderJobKind.SCENE_SAMPLE, output_uri="fake://x", output_sha256="hash", provider_calls_executed=True)


def test_provider_receipt_cannot_pass_with_blockers():
    cost = ProviderCostEstimateService().estimate(ProviderName.IDEOGRAM, ProviderJobKind.SCENE_SAMPLE)
    with pytest.raises(Exception):
        ProviderJobReceipt(provider_job_id="job", provider_name=ProviderName.IDEOGRAM, job_kind=ProviderJobKind.SCENE_SAMPLE, status=ProviderJobStatus.FAILED, pass_status=PassStatus.PASS, cost_estimate=cost, decision_log_id="decision", blockers=["failed"])


def test_provider_runtime_plan_non_batch_can_compile_with_partial_gate():
    _, job = IdeogramProviderRuntimeService().compile_scene_sample_job({"composition_prompt": "plate"}, ["composition_scene_1"])
    gate = ProviderSampleApprovalService().compile_gate(scene_sample_approved=True, face_plate_sample_approved=False, template_preview_sample_approved=True, approved_by="operator")
    plan = ProviderRuntimeService().compile_runtime_plan([job], gate)
    assert plan.provider_jobs[0].provider_job_id == job.provider_job_id


def test_sample_first_full_gate_allows_batch_policy_pass():
    gate = ProviderSampleApprovalService().compile_gate(True, True, True, approved_by="operator")
    receipt = ProviderSampleApprovalService().compile_batch_policy_receipt(gate, batch_requested=True)
    assert receipt.pass_status == PassStatus.PASS
