from ccp_studio.contracts.project_workspace_artifact_store import ArtifactCategory
from ccp_studio.contracts.provider_runtime import ProviderOutputAssetRole
from ccp_studio.services.artifact_manifest_service import ArtifactManifestService
from ccp_studio.services.artifact_store_service import ArtifactStoreService
from ccp_studio.services.client_workspace_service import ClientWorkspaceService
from ccp_studio.services.ideogram_provider_runtime_service import IdeogramProviderRuntimeService
from ccp_studio.services.provider_job_service import ProviderJobService
from ccp_studio.services.provider_output_asset_service import ProviderOutputAssetService
from ccp_studio.services.run_artifact_directory_service import RunArtifactDirectoryService


def test_fake_ideogram_output_asset_ref_can_register_workspace_artifact(tmp_path):
    workspace = ClientWorkspaceService().create_workspace(
        client_id="client_provider_demo",
        client_slug="provider-demo",
        brand_id="brand_provider_demo",
        brand_context_version_id="bcv_provider_demo_v1",
    )
    run_directory_service = RunArtifactDirectoryService()
    run_directory = run_directory_service.compile_run_directory(workspace, "run_provider_001")
    run_directory_service.materialize_run_directory(run_directory, base_dir=tmp_path)

    _profile, job = IdeogramProviderRuntimeService().compile_scene_sample_job(
        {"composition_prompt": "paper cut myth busting scene"},
        ["format02_scene_1"],
    )
    output, receipt = ProviderJobService().fake_execute(job)
    provider_asset = ProviderOutputAssetService().compile_asset_ref(
        output,
        receipt,
        ProviderOutputAssetRole.COMPOSITION_PLATE,
        ["format02_scene_1"],
    )

    artifact_ref, artifact_version = ArtifactStoreService().register_run_output(
        workspace=workspace,
        run_directory=run_directory,
        category=ArtifactCategory.IDEOGRAM_PLATE,
        filename="scene_sample_plate.json",
        text=provider_asset.model_dump_json() if hasattr(provider_asset, "model_dump_json") else provider_asset.json(),
        subdir="assets/ideogram_plates",
    )
    manifest = ArtifactManifestService().compile_manifest(
        client_workspace_id=workspace.client_workspace_id,
        run_id=run_directory.run_id,
        manifest_name="provider_runtime_fake_outputs",
        artifact_refs=[artifact_ref],
        version_refs=[artifact_version],
    )

    assert provider_asset.provider_job_receipt_id == receipt.provider_job_receipt_id
    assert provider_asset.sha256 == output.output_sha256
    assert provider_asset.source_refs == ["format02_scene_1"]
    assert artifact_ref.category == ArtifactCategory.IDEOGRAM_PLATE
    assert artifact_ref.sha256
    assert manifest.artifact_refs[0].client_workspace_id == workspace.client_workspace_id
    assert manifest.artifact_refs[0].run_id == "run_provider_001"
