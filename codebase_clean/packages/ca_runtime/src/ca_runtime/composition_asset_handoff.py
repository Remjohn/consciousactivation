"""
composition_asset_handoff.py
----------------------------
CAE-M0064 runtime-side verification and projection of a CompositionAssetPack.

This module intentionally has no semantic selection capability. It verifies the
production-bound payload, preserves exact identity/timing/rights/provenance, and emits
a provider-neutral runtime input envelope whose lineage root is the handoff proof.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence

from pydantic import BaseModel, ConfigDict, Field



class RuntimeAssetInput(BaseModel):
    """Executable provider-neutral input for an already selected production asset."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    asset_id: str = Field(..., min_length=1)
    asset_version: str = Field(..., min_length=1)
    asset_sha256: str = Field(..., min_length=64, max_length=64)
    scene_id: str = Field(..., min_length=1)
    source_start_time: float = Field(..., ge=0.0)
    source_end_time: float = Field(..., gt=0.0)
    semantic_role: str = Field(..., min_length=3)
    insert_role: str = Field(..., min_length=3)
    rights: dict[str, object]
    provenance: dict[str, str]
    demand_id: str = Field(..., min_length=1)
    binding_sha256: str = Field(..., min_length=64, max_length=64)
    lineage_root_sha256: str = Field(..., min_length=64, max_length=64)


class RuntimeAssetHandoff(BaseModel):
    """Tamper-evident collection of runtime inputs derived from one bound pack."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    mandate_id: str = "CAE-M0064"
    pack_id: str
    pack_sha256: str = Field(..., min_length=64, max_length=64)
    lineage_root_sha256: str = Field(..., min_length=64, max_length=64)
    inputs: tuple[RuntimeAssetInput, ...] = Field(..., min_length=1)
    handoff_sha256: str = Field(..., min_length=64, max_length=64)

    @classmethod
    def from_pack(cls, pack: Any) -> "RuntimeAssetHandoff":
        _validate_bound_pack(pack)
        inputs = tuple(
            RuntimeAssetInput(
                asset_id=b.asset_id,
                asset_version=b.source_version,
                asset_sha256=b.source_sha256,
                scene_id=b.scene_id,
                source_start_time=b.start_time,
                source_end_time=b.end_time,
                semantic_role=b.semantic_role,
                insert_role=b.insert_role,
                rights=dict(b.rights),
                provenance=dict(b.provenance),
                demand_id=b.demand_id,
                binding_sha256=b.binding_sha256,
                lineage_root_sha256=_pack_value(pack, "lineage_root_sha256"),
            )
            for b in pack.bindings
        )
        core = {
            "mandate_id": "CAE-M0064",
            "pack_id": pack.pack_id,
            "pack_sha256": pack.pack_sha256,
            "lineage_root_sha256": pack.lineage_root_sha256,
            "inputs": [item.model_dump(mode="json") for item in inputs],
        }
        return cls(**core, handoff_sha256=_sha256(core))

    def to_semantic_asset_inserts(self) -> list[dict[str, Any]]:
        return [
            {
                "asset_id": item.asset_id,
                "asset_version": item.asset_version,
                "asset_sha256": item.asset_sha256,
                "scene_id": item.scene_id,
                "source_start_time": item.source_start_time,
                "source_end_time": item.source_end_time,
                "semantic_role": item.semantic_role,
                "insert_role": item.insert_role,
                "rights": dict(item.rights),
                "provenance": dict(item.provenance),
                "demand_id": item.demand_id,
                "lineage_binding_sha256": item.binding_sha256,
                "lineage_root_sha256": item.lineage_root_sha256,
            }
            for item in self.inputs
        ]


# Resolve postponed Pydantic annotations explicitly for vendored/dynamic module loading.
RuntimeAssetInput.model_rebuild()
RuntimeAssetHandoff.model_rebuild()


class RuntimeAssetLineageError(ValueError):
    """Raised when an executable runtime input fails lineage validation."""


def _sha256(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str).encode("utf-8")
    ).hexdigest()


def verify_runtime_asset_handoff(handoff: RuntimeAssetHandoff) -> bool:
    """Verify the handoff hash and all input lineage roots before execution."""
    core = {
        "mandate_id": handoff.mandate_id,
        "pack_id": handoff.pack_id,
        "pack_sha256": handoff.pack_sha256,
        "lineage_root_sha256": handoff.lineage_root_sha256,
        "inputs": [item.model_dump(mode="json") for item in handoff.inputs],
    }
    if _sha256(core) != handoff.handoff_sha256:
        raise RuntimeAssetLineageError("runtime handoff digest mismatch")
    for item in handoff.inputs:
        if item.lineage_root_sha256 != handoff.lineage_root_sha256:
            raise RuntimeAssetLineageError("runtime input lineage root mismatch")
    return True


def _pack_value(pack: Any, field: str) -> Any:
    if isinstance(pack, Mapping):
        return pack[field]
    return getattr(pack, field)


def _validate_bound_pack(pack: Any) -> None:
    state = _pack_value(pack, "state")
    if state != "BOUND":
        raise RuntimeAssetLineageError(f"composition asset pack is not executable: state={state}")
    bindings = _pack_value(pack, "bindings")
    if not bindings:
        raise RuntimeAssetLineageError("composition asset pack has no bindings")
    expected_root = _pack_value(pack, "lineage_root_sha256")
    for binding in bindings:
        actual_root = _pack_value(binding, "lineage_root_sha256") if hasattr(binding, "lineage_root_sha256") or isinstance(binding, Mapping) and "lineage_root_sha256" in binding else expected_root
        if actual_root != expected_root:
            raise RuntimeAssetLineageError("runtime binding lineage root mismatch")


def resolve_runtime_asset_inputs(
    pack: Any,
    *,
    current_retrieval_candidates: Sequence[Mapping[str, Any]] | None = None,
) -> RuntimeAssetHandoff:
    """Validate a bound pack against current governed inputs and make runtime inputs."""
    _validate_bound_pack(pack)
    if current_retrieval_candidates is not None:
        # The production-package validator owns candidate identity semantics. Runtime
        # deliberately accepts only the already-validated bound pack and does not reselect.
        expected_assets = {str(_pack_value(item, "asset_id")) for item in _pack_value(pack, "bindings")}
        current_assets = {str(item.get("asset_id")) for item in current_retrieval_candidates}
        if expected_assets != current_assets:
            raise RuntimeAssetLineageError("current retrieval candidate set differs from bound runtime inputs")
    handoff = RuntimeAssetHandoff.from_pack(pack)
    verify_runtime_asset_handoff(handoff)
    return handoff
