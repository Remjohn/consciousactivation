from ccp_studio.contracts.local_render_worker import RenderJobType
from ccp_studio.contracts.project_workspace_artifact_store import ArtifactCategory
from ccp_studio.services.artifact_manifest_service import ArtifactManifestService
from ccp_studio.services.artifact_store_service import ArtifactStoreService
from ccp_studio.services.client_workspace_service import ClientWorkspaceService
from ccp_studio.services.local_render_worker_service import LocalRenderWorkerService
from ccp_studio.services.render_job_lease_service import RenderJobLeaseService
from ccp_studio.services.render_job_queue_service import RenderJobQueueService
from ccp_studio.services.render_job_result_service import RenderJobResultService
from ccp_studio.services.run_artifact_directory_service import RunArtifactDirectoryService


def _dump_json(model):
    return model.model_dump_json() if hasattr(model, "model_dump_json") else model.json()


def test_fake_render_worker_result_registers_as_workspace_render_artifact(tmp_path):
    workspace = ClientWorkspaceService().create_workspace(
        client_id="client_render_demo",
        client_slug="render-demo",
        brand_id="brand_render_demo",
        brand_context_version_id="bcv_render_demo_v1",
    )
    run_directory_service = RunArtifactDirectoryService()
    run_directory = run_directory_service.compile_run_directory(workspace, "run_render_001")
    run_directory_service.materialize_run_directory(run_directory, base_dir=tmp_path)

    job = RenderJobQueueService().create_job(
        job_type=RenderJobType.THUMBNAIL_RENDER,
        job_name="Thumbnail render",
    )
    worker = LocalRenderWorkerService().register_worker(
        worker_id="worker_artifact_demo",
        machine_id="machine_artifact_demo",
        display_name="Artifact Demo Worker",
    )
    lease = RenderJobLeaseService().lease_job(job=job, worker=worker)
    result = RenderJobResultService().complete_fake_result(job=job, worker=worker, lease=lease)

    artifact_ref, artifact_version = ArtifactStoreService().register_run_output(
        workspace=workspace,
        run_directory=run_directory,
        category=ArtifactCategory.RENDER,
        filename="thumbnail_render_result.json",
        text=_dump_json(result),
        subdir="renders",
    )
    manifest = ArtifactManifestService().compile_manifest(
        client_workspace_id=workspace.client_workspace_id,
        run_id=run_directory.run_id,
        manifest_name="local_render_worker_fake_result_manifest",
        artifact_refs=[artifact_ref],
        version_refs=[artifact_version],
    )

    assert artifact_ref.run_id == run_directory.run_id
    assert artifact_ref.relative_path.endswith("/renders/thumbnail_render_result.json")
    assert artifact_ref.category == ArtifactCategory.RENDER
    assert manifest.artifact_refs[0].client_workspace_id == workspace.client_workspace_id
