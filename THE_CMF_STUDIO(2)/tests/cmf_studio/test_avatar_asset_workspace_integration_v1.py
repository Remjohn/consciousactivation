from ccp_studio.contracts.project_workspace_artifact_store import ArtifactCategory
from ccp_studio.services.artifact_manifest_service import ArtifactManifestService
from ccp_studio.services.artifact_store_service import ArtifactStoreService
from ccp_studio.services.avatar_face_plate_approval_service import AvatarFacePlateApprovalService
from ccp_studio.services.client_workspace_service import ClientWorkspaceService


def _dump_json(model):
    return model.model_dump_json() if hasattr(model, "model_dump_json") else model.json()


def test_avatar_face_plate_refs_register_in_workspace_manifest():
    workspace = ClientWorkspaceService().create_workspace(
        client_id="client_avatar_demo",
        client_slug="avatar-demo",
        brand_id="brand_avatar_demo",
        brand_context_version_id="bcv_avatar_demo_v1",
    )
    face_set = AvatarFacePlateApprovalService().compile_approved_face_plate_set(
        avatar_id="coach_avatar_v1",
        approved_by="operator",
    )

    store = ArtifactStoreService()
    artifact_refs = []
    version_refs = []
    for plate in face_set.face_plates:
        artifact_ref, artifact_version = store.register_text_artifact(
            workspace=workspace,
            category=ArtifactCategory.AVATAR,
            relative_path=f"{workspace.workspace_relative_path}/libraries/avatar/face/{plate.expression_name.value}.json",
            text=_dump_json(plate),
            content_type="application/json",
        )
        artifact_refs.append(artifact_ref)
        version_refs.append(artifact_version)

    manifest = ArtifactManifestService().compile_manifest(
        client_workspace_id=workspace.client_workspace_id,
        manifest_name="avatar_face_plate_library_manifest",
        artifact_refs=artifact_refs,
        version_refs=version_refs,
    )

    assert len(manifest.artifact_refs) == len(face_set.face_plates)
    assert all(ref.category == ArtifactCategory.AVATAR for ref in manifest.artifact_refs)
    assert all(ref.client_workspace_id == workspace.client_workspace_id for ref in manifest.artifact_refs)
    assert all(ref.relative_path.startswith("client_workspaces/avatar-demo/libraries/avatar/") for ref in manifest.artifact_refs)
