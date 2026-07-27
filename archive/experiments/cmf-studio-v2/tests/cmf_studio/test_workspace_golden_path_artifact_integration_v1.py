from pathlib import Path

from ccp_studio.contracts.project_workspace_artifact_store import ArtifactCategory
from ccp_studio.services.artifact_manifest_service import ArtifactManifestService
from ccp_studio.services.artifact_store_service import ArtifactStoreService
from ccp_studio.services.client_workspace_service import ClientWorkspaceService
from ccp_studio.services.format02_golden_path_orchestrator_service import Format02GoldenPathOrchestratorService
from ccp_studio.services.run_artifact_directory_service import RunArtifactDirectoryService


FIXTURES_DIR = Path(__file__).resolve().parents[2] / "fixtures" / "golden_path"


def test_golden_path_outputs_register_into_single_workspace_run_manifest(tmp_path):
    workspace = ClientWorkspaceService().create_workspace(
        client_id="client_health_demo",
        client_slug="health-myth-demo",
        brand_id="brand_health_demo",
        brand_context_version_id="bcv_health_demo_v1",
    )
    run = Format02GoldenPathOrchestratorService().run_fixture(
        fixtures_dir=FIXTURES_DIR,
        brand_id=workspace.brand_id,
        brand_context_version_id=workspace.brand_context_version_id,
    )
    directory_service = RunArtifactDirectoryService()
    run_directory = directory_service.compile_run_directory(workspace, run.golden_path_run_id)
    directory_service.materialize_run_directory(run_directory, base_dir=tmp_path)

    store = ArtifactStoreService()
    timeline_ref, timeline_version = store.register_run_output(
        workspace=workspace,
        run_directory=run_directory,
        category=ArtifactCategory.TIMELINE,
        filename="video_timeline_program.json",
        text=run.output.video_timeline_program_id,
        subdir="timeline",
    )
    proxy_receipt_ref, proxy_receipt_version = store.register_run_output(
        workspace=workspace,
        run_directory=run_directory,
        category=ArtifactCategory.RECEIPT,
        filename="proxy_render_receipt.json",
        text=run.output.proxy_render_receipt_id,
        subdir="receipts",
    )
    export_ref, export_version = store.register_run_output(
        workspace=workspace,
        run_directory=run_directory,
        category=ArtifactCategory.EXPORT,
        filename="export_pack.json",
        text=run.output.export_pack_id,
        subdir="exports",
    )

    manifest = ArtifactManifestService().compile_manifest(
        client_workspace_id=workspace.client_workspace_id,
        run_id=run.golden_path_run_id,
        manifest_name="format02_golden_path_run_manifest",
        artifact_refs=[timeline_ref, proxy_receipt_ref, export_ref],
        version_refs=[timeline_version, proxy_receipt_version, export_version],
    )

    assert all(ref.client_workspace_id == workspace.client_workspace_id for ref in manifest.artifact_refs)
    assert all(ref.run_id == run.golden_path_run_id for ref in manifest.artifact_refs)
    assert all(version.sha256 for version in manifest.version_refs)
    assert timeline_ref.relative_path.startswith(run_directory.run_root)
    assert export_ref.relative_path.endswith("/exports/export_pack.json")
