from ccp_studio.contracts.provider_runtime import ProviderOutputAssetRole
from ccp_studio.services.avatar_face_plate_approval_service import AvatarFacePlateApprovalService
from ccp_studio.services.flux_provider_runtime_service import FluxProviderRuntimeService
from ccp_studio.services.provider_job_service import ProviderJobService
from ccp_studio.services.provider_output_asset_service import ProviderOutputAssetService


def test_flux_face_plate_sample_fake_executes_from_avatar_face_plate_refs():
    face_set = AvatarFacePlateApprovalService().compile_approved_face_plate_set(
        avatar_id="coach_avatar_v1",
        approved_by="operator",
    )
    source_refs = ["avatar_identity_coach_v1"]
    reference_refs = [plate.asset_ref for plate in face_set.face_plates[:1]]
    _profile, job = FluxProviderRuntimeService().compile_face_plate_sample_job(
        {"edit_instruction": "paperize approved face plate reference"},
        source_refs,
        reference_refs,
    )
    output, receipt = ProviderJobService().fake_execute(job)
    asset = ProviderOutputAssetService().compile_asset_ref(
        output,
        receipt,
        ProviderOutputAssetRole.FACE_PLATE,
        source_refs,
    )

    assert receipt.fake_execution is True
    assert receipt.provider_calls_executed is False
    assert output.provider_calls_executed is False
    assert asset.asset_role == ProviderOutputAssetRole.FACE_PLATE
    assert asset.provider_job_receipt_id == receipt.provider_job_receipt_id
    assert asset.sha256 == output.output_sha256
