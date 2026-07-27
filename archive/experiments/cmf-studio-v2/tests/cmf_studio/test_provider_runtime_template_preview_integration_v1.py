from ccp_studio.contracts.provider_runtime import PassStatus
from ccp_studio.services.provider_sample_approval_service import ProviderSampleApprovalService


def test_template_preview_sample_approval_alone_does_not_unlock_provider_batch():
    gate = ProviderSampleApprovalService().compile_gate(
        scene_sample_approved=False,
        face_plate_sample_approved=False,
        template_preview_sample_approved=True,
        approved_by="operator",
    )
    receipt = ProviderSampleApprovalService().compile_batch_policy_receipt(
        gate=gate,
        batch_requested=True,
    )

    assert gate.template_preview_sample_approved is True
    assert gate.batch_approved is False
    assert receipt.pass_status == PassStatus.FAIL
    assert "batch_requires_scene_face_plate_and_template_sample_approval" in receipt.blockers
