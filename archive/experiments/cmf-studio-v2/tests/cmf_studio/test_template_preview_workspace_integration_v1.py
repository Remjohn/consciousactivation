from ccp_studio.contracts.project_workspace_artifact_store import ArtifactCategory
from ccp_studio.contracts.template_preview_atlas import TemplateFormat, TemplateSamplePayload
from ccp_studio.services.artifact_manifest_service import ArtifactManifestService
from ccp_studio.services.artifact_store_service import ArtifactStoreService
from ccp_studio.services.client_workspace_service import ClientWorkspaceService
from ccp_studio.services.template_atlas_service import TemplateAtlasService


def test_template_preview_svg_registers_as_workspace_template_artifact(tmp_path):
    workspace = ClientWorkspaceService().create_workspace(
        client_id="client_1",
        client_slug="client-one",
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
    )
    ClientWorkspaceService().materialize_workspace(workspace, base_dir=tmp_path)

    atlas = TemplateAtlasService()
    slot_map = atlas.default_supervisual_slot_map()
    preview = atlas.compile_preview_from_payload(
        slot_map=slot_map,
        payload=TemplateSamplePayload(
            template_format=TemplateFormat.SUPERVISUAL,
            values={
                "source_truth": "The client needs recovery margins.",
                "hero_object": "paper planner",
                "power_phrase": "Build the margin.",
                "brand_mark": "CCP",
                "negative_space": "lower_third",
            },
        ),
    )

    artifact, version = ArtifactStoreService().register_text_artifact(
        workspace=workspace,
        category=ArtifactCategory.TEMPLATE,
        relative_path=f"{workspace.workspace_relative_path}/libraries/templates/{preview.template_id}.svg",
        text=preview.preview_svg,
        content_type="image/svg+xml",
    )
    manifest = ArtifactManifestService().compile_manifest(
        client_workspace_id=workspace.client_workspace_id,
        manifest_name="template_preview_manifest",
        artifact_refs=[artifact],
        version_refs=[version],
    )

    assert artifact.client_workspace_id == workspace.client_workspace_id
    assert artifact.category == ArtifactCategory.TEMPLATE
    assert artifact.sha256 == version.sha256
    assert manifest.artifact_refs[0].artifact_ref_id == artifact.artifact_ref_id

