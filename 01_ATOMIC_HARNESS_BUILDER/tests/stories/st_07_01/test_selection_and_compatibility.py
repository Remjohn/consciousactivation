from __future__ import annotations

from dataclasses import replace

import pytest

from cmf_builder.domain.compilation_targets import (
    EXTERNAL_VALIDATION_PENDING,
    TARGET_IDS,
    TargetSelectionRejected,
    select_compilation_target,
)
from test_three_target_registry import registry


@pytest.mark.parametrize("target_id", TARGET_IDS)
def test_exact_one_of_three_selection_preserves_target_identity(target_id: str) -> None:
    current = registry()
    result = select_compilation_target(
        run_id=f"select-{target_id}",
        registry=current,
        requested_target_ids=(target_id,),
        actor_id="target-code",
    )
    assert result.selection.target_id == target_id
    assert result.receipt.target_id == target_id
    assert result.receipt.registry_hash == current.registry_hash
    assert result.selection.production_ready is False
    assert result.selection.certified is False


@pytest.mark.parametrize(
    "requested",
    ((), ("atomic_content_harness", "visual_asset_editor"), ("universal_target",), ("2d_character_animation",)),
)
def test_zero_multiple_unknown_and_alias_selection_fail_closed(requested) -> None:
    with pytest.raises(TargetSelectionRejected):
        select_compilation_target(
            run_id="invalid-selection",
            registry=registry(),
            requested_target_ids=requested,
            actor_id="target-code",
        )


def test_external_target_selection_does_not_claim_external_compatibility() -> None:
    for target_id in ("visual_asset_editor", "content_asset_delegation_contract"):
        result = select_compilation_target(
            run_id=target_id,
            registry=registry(),
            requested_target_ids=(target_id,),
            actor_id="target-code",
        )
        assert result.selection.compatibility_state == EXTERNAL_VALIDATION_PENDING
        assert "compatible" not in result.receipt.outcome.lower()


def test_identical_selection_is_byte_stable() -> None:
    current = registry()
    first = select_compilation_target(
        run_id="stable", registry=current, requested_target_ids=(TARGET_IDS[0],), actor_id="target-code"
    )
    second = select_compilation_target(
        run_id="stable", registry=current, requested_target_ids=(TARGET_IDS[0],), actor_id="target-code"
    )
    assert first == second
    assert first.receipt.receipt_hash == second.receipt.receipt_hash


def test_selection_artifacts_reject_forged_links_and_false_compatibility() -> None:
    result = select_compilation_target(
        run_id="forgery",
        registry=registry(),
        requested_target_ids=("visual_asset_editor",),
        actor_id="target-code",
    )
    with pytest.raises(TargetSelectionRejected):
        replace(result.selection, compatibility_state="BUILDER_LOCAL_STRUCTURAL")
    with pytest.raises(TargetSelectionRejected):
        replace(result.selection, production_ready=True)
    with pytest.raises(TargetSelectionRejected):
        replace(result.receipt, profile_hash="sha256:" + "0" * 64)
    with pytest.raises(TargetSelectionRejected):
        replace(result, receipt=replace(result.receipt, run_id="different-run"))
