from pathlib import Path

import pytest

from ccp_studio.contracts.project_workspace_artifact_store import (
    ArtifactCategory,
    ArtifactLineage,
    ArtifactManifest,
    ArtifactReceipt,
    ArtifactRef,
    ArtifactStorageState,
    ArtifactVersion,
    ClientWorkspace,
    LineageRelation,
    PassStatus,
    RunArtifactDirectory,
    WorkspacePathPolicy,
)
from ccp_studio.services.artifact_lineage_service import ArtifactLineageService
from ccp_studio.services.artifact_manifest_service import ArtifactManifestService
from ccp_studio.services.artifact_store_service import ArtifactStoreService
from ccp_studio.services.client_workspace_service import ClientWorkspaceService
from ccp_studio.services.run_artifact_directory_service import RunArtifactDirectoryService
from ccp_studio.services.workspace_path_service import WorkspacePathService


def test_client_workspace_rejects_unsafe_slug():
    with pytest.raises(Exception):
        ClientWorkspace(
            client_id="client_1",
            client_slug="../escape",
            brand_id="brand_1",
            brand_context_version_id="bcv_1",
        )


def test_client_workspace_requires_brand_context_version():
    with pytest.raises(Exception):
        ClientWorkspace(
            client_id="client_1",
            client_slug="client-one",
            brand_id="brand_1",
            brand_context_version_id="",
        )


def test_workspace_path_policy_rejects_absolute_root_without_permission():
    with pytest.raises(Exception):
        WorkspacePathPolicy(workspace_root="/tmp/client_workspaces")


def test_workspace_folder_map_matches_convention():
    workspace = ClientWorkspaceService().create_workspace(
        client_id="client_1",
        client_slug="client-one",
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
    )
    folder_map = WorkspacePathService().compile_workspace_folder_map(workspace)
    assert folder_map.root == "client_workspaces/client-one"
    assert folder_map.avatar_library == "client_workspaces/client-one/libraries/avatar"
    assert folder_map.real_life_cutouts_library == "client_workspaces/client-one/libraries/real_life_cutouts"
    assert folder_map.templates_library == "client_workspaces/client-one/libraries/templates"


def test_run_artifact_directory_matches_convention():
    workspace = ClientWorkspaceService().create_workspace(
        client_id="client_1",
        client_slug="client-one",
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
    )
    directory = RunArtifactDirectoryService().compile_run_directory(workspace, "run_001")
    assert directory.run_root == "client_workspaces/client-one/runs/run_001"
    assert directory.asset_ideogram_plates.endswith("/assets/ideogram_plates")
    assert directory.asset_flux_edits.endswith("/assets/flux_edits")
    assert directory.renders.endswith("/renders")
    assert directory.exports.endswith("/exports")


def test_run_artifact_directory_rejects_unsafe_run_id():
    with pytest.raises(Exception):
        RunArtifactDirectory(
            client_workspace_id="cw_1",
            client_slug="client-one",
            run_id="../run",
        )


def test_workspace_materialization_creates_directories(tmp_path):
    service = ClientWorkspaceService()
    workspace = service.create_workspace(
        client_id="client_1",
        client_slug="client-one",
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
    )
    receipt = service.materialize_workspace(workspace, base_dir=tmp_path)
    assert receipt.pass_status == PassStatus.PASS
    assert (tmp_path / "client_workspaces/client-one/brand").exists()
    assert (tmp_path / "client_workspaces/client-one/references").exists()


def test_run_directory_materialization_creates_required_subfolders(tmp_path):
    workspace = ClientWorkspaceService().create_workspace(
        client_id="client_1",
        client_slug="client-one",
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
    )
    service = RunArtifactDirectoryService()
    directory = service.compile_run_directory(workspace, "run_001")
    receipt = service.materialize_run_directory(directory, base_dir=tmp_path)
    assert receipt.pass_status == PassStatus.PASS
    assert (tmp_path / "client_workspaces/client-one/runs/run_001/assets/flux_edits").exists()
    assert (tmp_path / "client_workspaces/client-one/runs/run_001/timeline").exists()


def test_artifact_ref_rejects_path_traversal():
    with pytest.raises(Exception):
        ArtifactRef(
            artifact_id="artifact_1",
            client_workspace_id="cw_1",
            client_slug="client-one",
            category=ArtifactCategory.REFERENCE,
            relative_path="client_workspaces/client-one/../escape.png",
        )


def test_materialized_artifact_requires_sha256():
    with pytest.raises(Exception):
        ArtifactRef(
            artifact_id="artifact_1",
            client_workspace_id="cw_1",
            client_slug="client-one",
            category=ArtifactCategory.REFERENCE,
            relative_path="client_workspaces/client-one/references/ref.png",
            storage_state=ArtifactStorageState.MATERIALIZED,
        )


def test_artifact_version_requires_sha256():
    with pytest.raises(Exception):
        ArtifactVersion(
            artifact_ref_id="artifact_ref_1",
            version=1,
            sha256="",
            relative_path="client_workspaces/client-one/references/ref.png",
        )


def test_artifact_store_registers_text_artifact_with_hash():
    workspace = ClientWorkspaceService().create_workspace(
        client_id="client_1",
        client_slug="client-one",
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
    )
    artifact, version = ArtifactStoreService().register_text_artifact(
        workspace=workspace,
        category=ArtifactCategory.MANIFEST,
        relative_path="client_workspaces/client-one/brand/context.json",
        text='{"brand":"demo"}',
        content_type="application/json",
    )
    assert artifact.sha256
    assert version.sha256 == artifact.sha256
    assert artifact.storage_state == ArtifactStorageState.MATERIALIZED


def test_artifact_manifest_requires_artifact_refs():
    with pytest.raises(Exception):
        ArtifactManifest(
            client_workspace_id="cw_1",
            manifest_name="empty",
            artifact_refs=[],
        )


def test_artifact_manifest_rejects_mixed_workspaces():
    a1 = ArtifactRef(
        artifact_id="artifact_1",
        client_workspace_id="cw_1",
        client_slug="client-one",
        category=ArtifactCategory.REFERENCE,
        relative_path="client_workspaces/client-one/references/ref1.png",
    )
    a2 = ArtifactRef(
        artifact_id="artifact_2",
        client_workspace_id="cw_2",
        client_slug="client-two",
        category=ArtifactCategory.REFERENCE,
        relative_path="client_workspaces/client-two/references/ref2.png",
    )
    with pytest.raises(Exception):
        ArtifactManifest(
            client_workspace_id="cw_1",
            manifest_name="mixed",
            artifact_refs=[a1, a2],
        )


def test_artifact_manifest_service_compiles_run_manifest():
    workspace = ClientWorkspaceService().create_workspace(
        client_id="client_1",
        client_slug="client-one",
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
    )
    artifact, version = ArtifactStoreService().register_text_artifact(
        workspace=workspace,
        category=ArtifactCategory.TIMELINE,
        relative_path="client_workspaces/client-one/runs/run_001/timeline/timeline.json",
        text="{}",
        run_id="run_001",
        content_type="application/json",
    )
    manifest = ArtifactManifestService().compile_manifest(
        client_workspace_id=workspace.client_workspace_id,
        run_id="run_001",
        manifest_name="run_manifest",
        artifact_refs=[artifact],
        version_refs=[version],
    )
    assert manifest.run_id == "run_001"
    assert manifest.artifact_refs[0].artifact_ref_id == artifact.artifact_ref_id


def test_artifact_lineage_requires_source_and_derived():
    with pytest.raises(Exception):
        ArtifactLineage(
            source_artifact_ref_ids=[],
            derived_artifact_ref_id="artifact_2",
            relation=LineageRelation.DERIVED_FROM,
            operation="test",
        )


def test_artifact_lineage_rejects_self_derivation():
    with pytest.raises(Exception):
        ArtifactLineage(
            source_artifact_ref_ids=["artifact_1"],
            derived_artifact_ref_id="artifact_1",
            relation=LineageRelation.DERIVED_FROM,
            operation="test",
        )


def test_lineage_service_records_lineage_and_receipt():
    service = ArtifactLineageService()
    lineage = service.record_lineage(
        source_artifact_ref_ids=["artifact_1"],
        derived_artifact_ref_id="artifact_2",
        relation=LineageRelation.EDITED_FROM,
        operation="flux_reference_edit",
        tool_or_service="flux",
    )
    receipt = service.record_receipt(
        artifact_ref_id="artifact_2",
        receipt_type="lineage_check",
        pass_status=PassStatus.PASS,
        checks={"lineage": lineage.artifact_lineage_id},
    )
    assert lineage.relation == LineageRelation.EDITED_FROM
    assert receipt.pass_status == PassStatus.PASS


def test_artifact_receipt_cannot_pass_with_blockers():
    with pytest.raises(Exception):
        ArtifactReceipt(
            artifact_ref_id="artifact_1",
            receipt_type="hash_verification",
            pass_status=PassStatus.PASS,
            blockers=["missing_hash"],
        )


def test_register_run_output_uses_run_directory_path():
    workspace = ClientWorkspaceService().create_workspace(
        client_id="client_1",
        client_slug="client-one",
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
    )
    directory = RunArtifactDirectoryService().compile_run_directory(workspace, "run_001")
    artifact, version = ArtifactStoreService().register_run_output(
        workspace=workspace,
        run_directory=directory,
        category=ArtifactCategory.RENDER,
        filename="proxy_receipt.json",
        text="{}",
        subdir="receipts",
    )
    assert "/runs/run_001/receipts/proxy_receipt.json" in artifact.relative_path
    assert artifact.run_id == "run_001"
    assert version.sha256
