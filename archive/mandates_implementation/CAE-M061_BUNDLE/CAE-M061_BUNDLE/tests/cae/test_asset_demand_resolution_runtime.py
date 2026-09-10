
"""Runtime lifecycle tests for CAE-M061."""

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
MODULE_PATH = ROOT / "packages" / "ca_runtime" / "src" / "ca_runtime" / "asset_demand_resolution.py"
_SPEC = importlib.util.spec_from_file_location("ca_runtime_asset_demand_resolution", MODULE_PATH)
_MODULE = importlib.util.module_from_spec(_SPEC)
assert _SPEC and _SPEC.loader
sys.modules[_SPEC.name] = _MODULE
_SPEC.loader.exec_module(_MODULE)

AssetDemandLifecycleState = _MODULE.AssetDemandLifecycleState
AssetDemandStateError = _MODULE.AssetDemandStateError
validate_asset_demand_transition = _MODULE.validate_asset_demand_transition


def test_runtime_allows_governed_demand_to_resolution_path():
    emitted = validate_asset_demand_transition(
        actor="agent:production-program",
        source=AssetDemandLifecycleState.PROGRAM_NEEDS_ASSET,
        target=AssetDemandLifecycleState.DEMAND_EMITTED,
        receipt_ref="rcpt-001",
    )
    assert emitted.target == AssetDemandLifecycleState.DEMAND_EMITTED
    assert emitted.validator == "validate_asset_demand_transition"
    assert emitted.preconditions
    assert emitted.postconditions
    assert emitted.receipt_ref == "rcpt-001"
    assert emitted.error_route.startswith("REJECT_TRANSITION")
    assert emitted.recovery_route.startswith("RETAIN_SOURCE_STATE")
    assert "SEMANTIC_AUTHORITY_REMAINS_WITH_PROGRAM" in emitted.validation

    pending = validate_asset_demand_transition(
        actor="service:asset-intelligence",
        source=AssetDemandLifecycleState.DEMAND_EMITTED,
        target=AssetDemandLifecycleState.RESOLUTION_PENDING,
        receipt_ref="rcpt-002",
    )
    assert pending.target == AssetDemandLifecycleState.RESOLUTION_PENDING

    satisfied = validate_asset_demand_transition(
        actor="service:asset-intelligence",
        source=AssetDemandLifecycleState.RESOLUTION_PENDING,
        target=AssetDemandLifecycleState.SATISFIED,
        receipt_ref="rcpt-003",
    )
    assert satisfied.source == AssetDemandLifecycleState.RESOLUTION_PENDING


def test_runtime_does_not_allow_terminal_state_reopening_or_skipping_program_demand():
    with pytest.raises(AssetDemandStateError, match="Invalid asset demand transition"):
        validate_asset_demand_transition(
            actor="service:asset-intelligence",
            source=AssetDemandLifecycleState.PROGRAM_NEEDS_ASSET,
            target=AssetDemandLifecycleState.SATISFIED,
            receipt_ref="rcpt-bad",
        )

    with pytest.raises(AssetDemandStateError, match="Invalid asset demand transition"):
        validate_asset_demand_transition(
            actor="service:asset-intelligence",
            source=AssetDemandLifecycleState.SATISFIED,
            target=AssetDemandLifecycleState.DEMAND_EMITTED,
            receipt_ref="rcpt-bad",
        )
