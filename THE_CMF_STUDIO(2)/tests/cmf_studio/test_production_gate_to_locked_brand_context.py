from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.brand_context import (  # noqa: E402
    BrandContextAssetBundle,
    BrandContextStatus,
    BrandContextVersion,
)
from ccp_studio.contracts.brand_context_gate import (  # noqa: E402
    BrandContextGateStatus,
    SelectedBrandAssetRef,
    SupersededContextAction,
)
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.repositories.acting_library import InMemoryActingLibraryRepository  # noqa: E402
from ccp_studio.repositories.creative_library_items import InMemoryCreativeLibraryRepository  # noqa: E402
from ccp_studio.repositories.rig_manifests import InMemoryRigManifestRepository  # noqa: E402
from ccp_studio.services.brand_context_gate_service import BrandContextGateService, BrandContextGateServiceError  # noqa: E402
from ccp_studio.services.brand_context_service import BrandContextService  # noqa: E402
from ccp_studio.services.provider_request_builder import ProviderRequestBuilder  # noqa: E402
from ccp_studio.services.review_lineage_service import ReviewLineageService  # noqa: E402
from ccp_studio.services.scene_spec_compiler import SceneSpecCompiler  # noqa: E402
from ccp_studio.workflows.complete_editing_session import CompleteEditingSessionWorkflow  # noqa: E402


def _manual_context(status=BrandContextStatus.locked, brand_id=None, superseded_by=None):
    org_id = uuid4()
    brand_id = brand_id or uuid4()
    session_id = uuid4()
    actor_id = uuid4()
    bundle = BrandContextAssetBundle(
        schema_version="cmf.brand_context_asset_bundle.v1",
        acting_library_version_id=uuid4(),
        rig_manifest_id=uuid4(),
        micro_semiotic_anchor_ids=[uuid4()],
        motion_recipe_ids=[uuid4()],
        sfx_asset_ids=[uuid4()],
        composition_preference_ids=[uuid4()],
        platform_profile_ids=[uuid4()],
        creative_library_receipt_ids=[uuid4()],
        evaluation_receipt_ids=[uuid4()],
    )
    version = BrandContextVersion(
        schema_version="cmf.brand_context_version.v1",
        brand_context_version_id=uuid4(),
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        superseded_by_brand_context_version_id=superseded_by,
        status=status,
        version_hash=f"sha256-context-{status.value}-{uuid4()}",
        asset_bundle=bundle,
        clearance_certificate_id=uuid4() if status in {BrandContextStatus.locked, BrandContextStatus.superseded} else None,
        created_by_actor_id=actor_id,
        locked_by_actor_id=actor_id if status in {BrandContextStatus.locked, BrandContextStatus.superseded} else None,
        created_at=utc_now(),
        updated_at=utc_now(),
        locked_at=utc_now() if status in {BrandContextStatus.locked, BrandContextStatus.superseded} else None,
    )
    context_service = BrandContextService(
        InMemoryActingLibraryRepository(),
        InMemoryRigManifestRepository(),
        InMemoryCreativeLibraryRepository(),
    )
    context_service.repository.put_version(version)
    gate_service = BrandContextGateService(context_service)
    return gate_service, org_id, brand_id, actor_id, version


def _selected_refs(version):
    return [
        SelectedBrandAssetRef(
            schema_version="cmf.selected_brand_asset_ref.v1",
            asset_type="micro_semiotic_anchor",
            asset_id=version.asset_bundle.micro_semiotic_anchor_ids[0],
            asset_hash="sha256-anchor",
            brand_context_version_id=version.brand_context_version_id,
        ),
        SelectedBrandAssetRef(
            schema_version="cmf.selected_brand_asset_ref.v1",
            asset_type="motion_recipe",
            asset_id=version.asset_bundle.motion_recipe_ids[0],
            asset_hash="sha256-motion",
            brand_context_version_id=version.brand_context_version_id,
        ),
    ]


def test_complete_editing_session_gate_blocks_missing_or_unlocked_brand_context():
    gate, org_id, brand_id, _actor_id, draft = _manual_context(status=BrandContextStatus.draft)
    workflow = CompleteEditingSessionWorkflow(gate)

    missing = workflow.validate_brand_context(
        organization_id=org_id,
        brand_id=brand_id,
        brand_context_version_id=None,
    )
    unlocked = workflow.validate_brand_context(
        organization_id=org_id,
        brand_id=brand_id,
        brand_context_version_id=draft.brand_context_version_id,
    )

    assert missing.status == BrandContextGateStatus.blocked
    assert missing.decision_code == "BRAND_CONTEXT_REQUIRED"
    assert unlocked.status == BrandContextGateStatus.blocked
    assert unlocked.decision_code == "BRAND_CONTEXT_NOT_LOCKED"


def test_scene_spec_binding_requires_selected_assets_to_belong_to_locked_context():
    gate, org_id, brand_id, _actor_id, locked = _manual_context()
    compiler = SceneSpecCompiler(gate)
    scene_spec_id = uuid4()

    binding = compiler.bind_brand_context(
        organization_id=org_id,
        brand_id=brand_id,
        scene_spec_id=scene_spec_id,
        brand_context_version_id=locked.brand_context_version_id,
        selected_asset_refs=_selected_refs(locked),
    )

    assert binding.brand_context_version_hash == locked.version_hash
    assert len(binding.selected_asset_refs) == 2
    outside = SelectedBrandAssetRef(
        schema_version="cmf.selected_brand_asset_ref.v1",
        asset_type="micro_semiotic_anchor",
        asset_id=uuid4(),
        asset_hash="sha256-outside",
        brand_context_version_id=locked.brand_context_version_id,
    )
    with pytest.raises(BrandContextGateServiceError) as exc:
        compiler.bind_brand_context(
            organization_id=org_id,
            brand_id=brand_id,
            scene_spec_id=uuid4(),
            brand_context_version_id=locked.brand_context_version_id,
            selected_asset_refs=[outside],
        )
    assert exc.value.code == "BRAND_ASSET_NOT_IN_CONTEXT"


def test_superseded_context_revision_requires_preserve_or_fork_decision():
    gate, org_id, brand_id, actor_id, superseded = _manual_context(status=BrandContextStatus.superseded)
    replacement = superseded.model_copy(
        update={
            "brand_context_version_id": uuid4(),
            "status": BrandContextStatus.locked,
            "version_hash": "sha256-replacement-context",
            "parent_brand_context_version_id": superseded.brand_context_version_id,
        }
    )
    gate.brand_context_service.repository.put_version(replacement)

    first = gate.validate_production_context(
        organization_id=org_id,
        brand_id=brand_id,
        brand_context_version_id=superseded.brand_context_version_id,
    )
    decision = gate.record_superseded_context_decision(
        organization_id=org_id,
        brand_id=brand_id,
        superseded_brand_context_version_id=superseded.brand_context_version_id,
        action=SupersededContextAction.preserve_original,
        decided_by_actor_id=actor_id,
        rationale="old render revision must preserve original creative truth",
    )
    preserved = gate.validate_production_context(
        organization_id=org_id,
        brand_id=brand_id,
        brand_context_version_id=superseded.brand_context_version_id,
        superseded_decision_id=decision.superseded_context_decision_id,
    )
    fork_decision = gate.record_superseded_context_decision(
        organization_id=org_id,
        brand_id=brand_id,
        superseded_brand_context_version_id=superseded.brand_context_version_id,
        action=SupersededContextAction.fork_to_new_context,
        replacement_brand_context_version_id=replacement.brand_context_version_id,
        decided_by_actor_id=actor_id,
        rationale="future render should use new approved context",
    )
    forked = gate.validate_production_context(
        organization_id=org_id,
        brand_id=brand_id,
        brand_context_version_id=superseded.brand_context_version_id,
        superseded_decision_id=fork_decision.superseded_context_decision_id,
    )

    assert first.status == BrandContextGateStatus.decision_required
    assert first.decision_code == "BRAND_CONTEXT_DECISION_REQUIRED"
    assert preserved.status == BrandContextGateStatus.allowed
    assert preserved.decision_code == "BRAND_CONTEXT_ORIGINAL_PRESERVED"
    assert forked.status == BrandContextGateStatus.allowed
    assert forked.requested_brand_context_version_id == replacement.brand_context_version_id


def test_provider_receipt_includes_brand_context_version_hash_and_selected_asset_hashes():
    gate, org_id, brand_id, _actor_id, locked = _manual_context()
    compiler = SceneSpecCompiler(gate)
    provider_builder = ProviderRequestBuilder(gate)
    scene_spec_id = uuid4()
    compiler.bind_brand_context(
        organization_id=org_id,
        brand_id=brand_id,
        scene_spec_id=scene_spec_id,
        brand_context_version_id=locked.brand_context_version_id,
        selected_asset_refs=_selected_refs(locked),
    )

    receipt = provider_builder.bind_brand_context_receipt(
        provider_job_id=uuid4(),
        scene_spec_id=scene_spec_id,
    )

    assert receipt.brand_context_version_id == locked.brand_context_version_id
    assert receipt.brand_context_version_hash == locked.version_hash
    assert receipt.selected_asset_hashes == ["sha256-anchor", "sha256-motion"]
    with pytest.raises(BrandContextGateServiceError) as exc:
        provider_builder.bind_brand_context_receipt(provider_job_id=uuid4(), scene_spec_id=uuid4())
    assert exc.value.code == "PROVIDER_BRAND_CONTEXT_LINEAGE_REQUIRED"


def test_reviewer_can_inspect_locked_creative_universe_behind_render():
    gate, org_id, brand_id, _actor_id, locked = _manual_context()
    compiler = SceneSpecCompiler(gate)
    review = ReviewLineageService(gate)
    scene_spec_id = uuid4()
    compiler.bind_brand_context(
        organization_id=org_id,
        brand_id=brand_id,
        scene_spec_id=scene_spec_id,
        brand_context_version_id=locked.brand_context_version_id,
        selected_asset_refs=_selected_refs(locked),
    )

    view = review.view_brand_context_lineage(
        downstream_object_id=uuid4(),
        downstream_object_type="render_output",
        scene_spec_id=scene_spec_id,
    )

    assert view.brand_context_version_id == locked.brand_context_version_id
    assert view.brand_context_version_hash == locked.version_hash
    assert {ref.asset_type for ref in view.selected_asset_refs} == {"micro_semiotic_anchor", "motion_recipe"}


def test_cross_brand_context_fails_production_gate():
    gate, org_id, _brand_id, _actor_id, locked = _manual_context()

    result = gate.validate_production_context(
        organization_id=org_id,
        brand_id=uuid4(),
        brand_context_version_id=locked.brand_context_version_id,
    )

    assert result.status == BrandContextGateStatus.blocked
    assert result.decision_code == "BRAND_SCOPE_VIOLATION"
