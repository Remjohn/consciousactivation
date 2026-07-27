from ccp_studio.contracts.project_workspace_artifact_store import ArtifactCategory, LineageRelation
from ccp_studio.services.artifact_lineage_service import ArtifactLineageService
from ccp_studio.services.artifact_manifest_service import ArtifactManifestService
from ccp_studio.services.artifact_store_service import ArtifactStoreService
from ccp_studio.services.client_workspace_service import ClientWorkspaceService
from ccp_studio.services.run_artifact_directory_service import RunArtifactDirectoryService


def test_video_engine_fake_outputs_register_artifacts_and_render_lineage(tmp_path):
    workspace = ClientWorkspaceService().create_workspace(
        client_id="client_video_demo",
        client_slug="video-demo",
        brand_id="brand_video_demo",
        brand_context_version_id="bcv_video_demo_v1",
    )
    run_directory_service = RunArtifactDirectoryService()
    run_directory = run_directory_service.compile_run_directory(workspace, "run_video_001")
    run_directory_service.materialize_run_directory(run_directory, base_dir=tmp_path)

    store = ArtifactStoreService()
    timeline_ref, timeline_version = store.register_run_output(
        workspace=workspace,
        run_directory=run_directory,
        category=ArtifactCategory.TIMELINE,
        filename="timeline_contract.json",
        text='{"timeline_program_id":"timeline_1"}',
        subdir="timeline",
    )
    proxy_receipt_ref, proxy_receipt_version = store.register_run_output(
        workspace=workspace,
        run_directory=run_directory,
        category=ArtifactCategory.RECEIPT,
        filename="fake_proxy_render_receipt.json",
        text='{"proxy_render_receipt_id":"proxy_1","output_sha256":"sha256-proxy"}',
        subdir="receipts",
    )
    final_export_ref, final_export_version = store.register_run_output(
        workspace=workspace,
        run_directory=run_directory,
        category=ArtifactCategory.EXPORT,
        filename="final_export_pack.json",
        text='{"export_pack_id":"export_1","output_sha256":"sha256-final"}',
        subdir="exports",
    )

    manifest = ArtifactManifestService().compile_manifest(
        client_workspace_id=workspace.client_workspace_id,
        run_id=run_directory.run_id,
        manifest_name="video_fake_render_manifest",
        artifact_refs=[timeline_ref, proxy_receipt_ref, final_export_ref],
        version_refs=[timeline_version, proxy_receipt_version, final_export_version],
    )
    lineage = ArtifactLineageService().record_lineage(
        source_artifact_ref_ids=[timeline_ref.artifact_ref_id],
        derived_artifact_ref_id=final_export_ref.artifact_ref_id,
        relation=LineageRelation.RENDERED_FROM,
        operation="video_fake_final_render",
        tool_or_service="video_editing_engine_v1_fake",
        source_receipt_refs=[proxy_receipt_ref.artifact_ref_id],
    )

    assert len(manifest.artifact_refs) == 3
    assert all(ref.run_id == "run_video_001" for ref in manifest.artifact_refs)
    assert proxy_receipt_ref.relative_path.endswith("/receipts/fake_proxy_render_receipt.json")
    assert final_export_ref.relative_path.endswith("/exports/final_export_pack.json")
    assert lineage.relation == LineageRelation.RENDERED_FROM
    assert lineage.source_artifact_ref_ids == [timeline_ref.artifact_ref_id]
