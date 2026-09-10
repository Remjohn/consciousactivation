"""
composition_asset_pack.py
-------------------------
CAE-M0064 typed selection -> production binding boundary.

The pack is deliberately downstream of retrieval and upstream of composition/runtime
realization. It preserves the selected retrieval candidate snapshot, exact source
interval, rights/provenance evidence, explicit selection authority, and a
tamper-evident lineage DAG root.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

from pydantic import BaseModel, ConfigDict, Field, model_validator


MANDATE_ID = "CAE-M0064"
PACK_VERSION = "1.0.0"
BOUND_STATE = "BOUND"
INVALIDATED_STATE = "INVALIDATED"


class AssetBindingError(ValueError):
    """Base error for selection -> production binding validation."""


class AssetLineageValidationError(AssetBindingError):
    """Raised when an identity, interval, rights, provenance, or authority proof is invalid."""


class AssetBindingInvalidatedError(AssetBindingError):
    """Raised when a previously bound package no longer matches its governed inputs."""


def _canonicalize(payload: Any) -> Any:
    if isinstance(payload, BaseModel):
        return _canonicalize(payload.model_dump(mode="python"))
    if isinstance(payload, Mapping):
        return {str(key): _canonicalize(value) for key, value in payload.items()}
    if isinstance(payload, (list, tuple)):
        return [_canonicalize(value) for value in payload]
    return payload


def _canonical_sha256(payload: Any) -> str:
    encoded = json.dumps(
        _canonicalize(payload),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AssetLineageValidationError(f"{field} is required")
    return value.strip()


def _require_sha256(value: Any, field: str) -> str:
    text = _require_text(value, field).lower()
    if len(text) != 64 or any(ch not in "0123456789abcdef" for ch in text):
        raise AssetLineageValidationError(f"{field} must be a 64-character SHA-256 hex digest")
    return text


def _normalize_interval(candidate: Mapping[str, Any]) -> tuple[float, float, float]:
    try:
        start = float(candidate["start_time"])
        end = float(candidate["end_time"])
    except (KeyError, TypeError, ValueError) as exc:
        raise AssetLineageValidationError("candidate must carry start_time and end_time") from exc
    if start < 0 or end <= start:
        raise AssetLineageValidationError("candidate interval must satisfy 0 <= start_time < end_time")
    supplied_duration = float(candidate.get("duration", end - start))
    expected_duration = end - start
    if abs(supplied_duration - expected_duration) > 1e-9:
        raise AssetLineageValidationError("candidate duration does not equal end_time - start_time")
    return start, end, supplied_duration


def _rights_snapshot(candidate: Mapping[str, Any]) -> dict[str, Any]:
    raw = candidate.get("rights")
    if isinstance(raw, Mapping):
        rights = dict(raw)
        status = rights.get("status", candidate.get("rights_status"))
        if hasattr(status, "value"):
            status = status.value
        rights["status"] = _require_text(status, "rights.status")
        return rights
    status = candidate.get("rights_status")
    if hasattr(status, "value"):
        status = status.value
    return {"status": _require_text(status, "rights_status")}


def _provenance_snapshot(candidate: Mapping[str, Any]) -> dict[str, str]:
    raw = candidate.get("provenance", {})
    if not isinstance(raw, Mapping):
        raise AssetLineageValidationError("candidate provenance must be a mapping")
    provenance = {str(k): str(v) for k, v in raw.items()}
    # Retrieval M0063 exposes these fields both as candidate attributes and in provenance.
    provenance.setdefault("scene_id", _require_text(candidate.get("scene_id"), "scene_id"))
    provenance.setdefault("source_version", _require_text(candidate.get("source_version"), "source_version"))
    provenance.setdefault("source_sha256", _require_sha256(candidate.get("source_sha256"), "source_sha256"))
    candidate_id = candidate.get("candidate_id")
    if candidate_id is not None:
        provenance.setdefault("candidate_id", _require_text(candidate_id, "candidate_id"))
    return dict(sorted(provenance.items()))


def candidate_identity_snapshot(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Return the immutable source-of-truth fields required by M0064."""
    asset_id = _require_text(candidate.get("asset_id"), "asset_id")
    scene_id = _require_text(candidate.get("scene_id"), "scene_id")
    source_version = _require_text(candidate.get("source_version"), "source_version")
    source_sha256 = _require_sha256(candidate.get("source_sha256"), "source_sha256")
    workspace_id = _require_text(candidate.get("workspace_id"), "workspace_id")
    semantic_role = _require_text(candidate.get("semantic_role"), "semantic_role")
    insert_role = candidate.get("insert_role")
    if hasattr(insert_role, "value"):
        insert_role = insert_role.value
    insert_role = _require_text(insert_role, "insert_role")
    start_time, end_time, duration = _normalize_interval(candidate)
    rights = _rights_snapshot(candidate)
    provenance = _provenance_snapshot(candidate)
    snapshot = {
        "asset_id": asset_id,
        "scene_id": scene_id,
        "workspace_id": workspace_id,
        "source_version": source_version,
        "source_sha256": source_sha256,
        "start_time": start_time,
        "end_time": end_time,
        "duration": duration,
        "semantic_role": semantic_role,
        "insert_role": insert_role,
        "rights": rights,
        "provenance": provenance,
    }
    snapshot["candidate_snapshot_sha256"] = _canonical_sha256(snapshot)
    return snapshot


class ExplicitSelectionReceipt(BaseModel):
    """Operator/selection authority proof; binding never infers selection itself."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    receipt_id: str = Field(..., min_length=1)
    workspace_id: str = Field(..., min_length=1)
    candidate_id: str = Field(..., min_length=1)
    selected_asset_ids: tuple[str, ...] = Field(..., min_length=1)
    selected_scene_ids: tuple[str, ...] = Field(..., min_length=1)
    actor: str = Field(..., min_length=1)
    authority: str = Field(..., min_length=1)
    source_receipt_refs: tuple[str, ...] = ()
    receipt_sha256: str = Field(..., min_length=64, max_length=64)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @model_validator(mode="after")
    def validate_digest(self) -> "ExplicitSelectionReceipt":
        core = {
            "receipt_id": self.receipt_id,
            "workspace_id": self.workspace_id,
            "candidate_id": self.candidate_id,
            "selected_asset_ids": list(self.selected_asset_ids),
            "selected_scene_ids": list(self.selected_scene_ids),
            "actor": self.actor,
            "authority": self.authority,
            "source_receipt_refs": list(self.source_receipt_refs),
            "created_at": self.created_at,
        }
        expected = _canonical_sha256(core)
        if self.receipt_sha256 != expected:
            raise AssetLineageValidationError("selection receipt digest mismatch")
        return self


class CompositionAssetBinding(BaseModel):
    """One exact selected retrieval candidate projected into production semantics."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    demand_id: str = Field(..., min_length=1)
    scene_index: int = Field(..., ge=1)
    asset_id: str = Field(..., min_length=1)
    scene_id: str = Field(..., min_length=1)
    workspace_id: str = Field(..., min_length=1)
    source_version: str = Field(..., min_length=1)
    source_sha256: str = Field(..., min_length=64, max_length=64)
    start_time: float = Field(..., ge=0.0)
    end_time: float = Field(..., gt=0.0)
    duration: float = Field(..., gt=0.0)
    semantic_role: str = Field(..., min_length=3)
    insert_role: str = Field(..., min_length=3)
    rights: Mapping[str, Any]
    provenance: Mapping[str, str]
    candidate_snapshot_sha256: str = Field(..., min_length=64, max_length=64)
    retrieval_receipt_id: str = Field(..., min_length=1)
    selection_receipt_id: str = Field(..., min_length=1)
    binding_sha256: str = Field(..., min_length=64, max_length=64)

    @model_validator(mode="after")
    def validate_binding(self) -> "CompositionAssetBinding":
        if self.end_time <= self.start_time:
            raise AssetLineageValidationError("binding interval must be positive")
        if abs(self.duration - (self.end_time - self.start_time)) > 1e-9:
            raise AssetLineageValidationError("binding duration does not equal its interval")
        if self.rights.get("status") in (None, ""):
            raise AssetLineageValidationError("binding rights status is required")
        core = self.model_dump(exclude={"binding_sha256"})
        expected = _canonical_sha256(core)
        if self.binding_sha256 != expected:
            raise AssetLineageValidationError("binding digest mismatch")
        return self

    def to_asset_insert(self) -> dict[str, Any]:
        """Project the binding into the existing SemanticSceneSpec.asset_inserts shape."""
        return {
            "asset_id": self.asset_id,
            "asset_version": self.source_version,
            "asset_sha256": self.source_sha256,
            "scene_id": self.scene_id,
            "source_start_time": self.start_time,
            "source_end_time": self.end_time,
            "duration": self.duration,
            "semantic_role": self.semantic_role,
            "insert_role": self.insert_role,
            "rights": dict(self.rights),
            "provenance": dict(self.provenance),
            "demand_id": self.demand_id,
            "lineage_binding_sha256": self.binding_sha256,
        }


class CompositionAssetPack(BaseModel):
    """Tamper-evident collection of explicit asset bindings for one SemanticProgram."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    pack_id: str = Field(..., min_length=1)
    pack_version: str = PACK_VERSION
    mandate_id: str = MANDATE_ID
    state: str = BOUND_STATE
    workspace_id: str = Field(..., min_length=1)
    candidate_id: str = Field(..., min_length=1)
    program_ref: Mapping[str, str]
    selection_receipt: ExplicitSelectionReceipt
    bindings: tuple[CompositionAssetBinding, ...] = Field(..., min_length=1)
    lineage_leaves_sha256: tuple[str, ...] = Field(..., min_length=1)
    lineage_root_sha256: str = Field(..., min_length=64, max_length=64)
    pack_sha256: str = Field(..., min_length=64, max_length=64)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @model_validator(mode="after")
    def validate_pack(self) -> "CompositionAssetPack":
        if self.state not in {BOUND_STATE, INVALIDATED_STATE}:
            raise AssetLineageValidationError(f"unsupported pack state: {self.state}")
        if any(binding.workspace_id != self.workspace_id for binding in self.bindings):
            raise AssetLineageValidationError("all bindings must remain in the pack workspace")
        if any(binding.selection_receipt_id != self.selection_receipt.receipt_id for binding in self.bindings):
            raise AssetLineageValidationError("all bindings must cite the governing selection receipt")
        if set(self.selection_receipt.selected_asset_ids) != {b.asset_id for b in self.bindings}:
            raise AssetLineageValidationError("selection receipt asset set does not equal bound asset set")
        if set(self.selection_receipt.selected_scene_ids) != {b.scene_id for b in self.bindings}:
            raise AssetLineageValidationError("selection receipt scene set does not equal bound scene set")
        expected_root = _lineage_root(
            workspace_id=self.workspace_id,
            candidate_id=self.candidate_id,
            program_ref=self.program_ref,
            selection_receipt=self.selection_receipt,
            bindings=self.bindings,
        )
        if self.lineage_root_sha256 != expected_root:
            raise AssetLineageValidationError("lineage root digest mismatch")
        expected_pack = _canonical_sha256(self.model_dump(mode="python", exclude={"pack_sha256"}))
        if self.pack_sha256 != expected_pack:
            raise AssetLineageValidationError("pack digest mismatch")
        return self

    def to_semantic_asset_inserts(self) -> list[dict[str, Any]]:
        return [binding.to_asset_insert() for binding in self.bindings]

    def as_handoff_receipt(self) -> dict[str, Any]:
        return {
            "receipt_id": f"RCP-{self.pack_id}",
            "mandate_id": self.mandate_id,
            "pack_id": self.pack_id,
            "pack_version": self.pack_version,
            "workspace_id": self.workspace_id,
            "candidate_id": self.candidate_id,
            "program_ref": dict(self.program_ref),
            "selection_receipt_id": self.selection_receipt.receipt_id,
            "binding_ids": [b.asset_id for b in self.bindings],
            "lineage_leaves_sha256": list(self.lineage_leaves_sha256),
            "lineage_root_sha256": self.lineage_root_sha256,
            "pack_sha256": self.pack_sha256,
            "state": self.state,
            "created_at": self.created_at,
        }


def _lineage_root(
    *,
    workspace_id: str,
    candidate_id: str,
    program_ref: Mapping[str, str],
    selection_receipt: ExplicitSelectionReceipt,
    bindings: Sequence[CompositionAssetBinding],
) -> str:
    leaves = []
    for binding in sorted(bindings, key=lambda item: (item.scene_index, item.asset_id)):
        leaves.append(
            _canonical_sha256(
                {
                    "kind": "asset-binding",
                    "binding_sha256": binding.binding_sha256,
                    "candidate_snapshot_sha256": binding.candidate_snapshot_sha256,
                }
            )
        )
    receipt_leaf = _canonical_sha256(
        {"kind": "selection-receipt", "receipt_sha256": selection_receipt.receipt_sha256}
    )
    program_leaf = _canonical_sha256(
        {"kind": "program-ref", "program_ref": dict(program_ref)}
    )
    leaves.extend([receipt_leaf, program_leaf])
    return _canonical_sha256(
        {
            "kind": "cae-m0064-lineage-dag",
            "mandate_id": MANDATE_ID,
            "workspace_id": workspace_id,
            "candidate_id": candidate_id,
            "leaves": sorted(leaves),
        }
    )


def build_selection_receipt(payload: Mapping[str, Any]) -> ExplicitSelectionReceipt:
    """Normalize and cryptographically validate an explicit selection receipt."""
    receipt = ExplicitSelectionReceipt(**dict(payload))
    return receipt


def bind_selected_retrieval_candidates(
    *,
    program_ref: Mapping[str, str],
    selection_receipt: ExplicitSelectionReceipt | Mapping[str, Any],
    retrieval_candidates: Sequence[Mapping[str, Any]],
    retrieval_receipt_id: str,
    scene_index_by_scene_id: Mapping[str, int] | None = None,
) -> CompositionAssetPack:
    """
    Convert only explicitly selected retrieval candidates into production bindings.

    The selector is an input, never an implementation detail. Candidate order is
    normalized only for deterministic hashing; no candidate is added or substituted.
    """
    receipt = (
        selection_receipt
        if isinstance(selection_receipt, ExplicitSelectionReceipt)
        else ExplicitSelectionReceipt(**dict(selection_receipt))
    )
    normalized_program_ref = {
        "object_id": _require_text(program_ref.get("object_id"), "program_ref.object_id"),
        "version": _require_text(program_ref.get("version"), "program_ref.version"),
        "sha256": _require_sha256(program_ref.get("sha256"), "program_ref.sha256"),
    }
    workspace_id = _require_text(program_ref.get("workspace_id", receipt.workspace_id), "workspace_id")
    candidate_id = _require_text(program_ref.get("candidate_id", receipt.candidate_id), "candidate_id")
    if workspace_id != receipt.workspace_id or candidate_id != receipt.candidate_id:
        raise AssetLineageValidationError("program and selection receipt scope do not match")

    selected_asset_ids = set(receipt.selected_asset_ids)
    selected_scene_ids = set(receipt.selected_scene_ids)
    supplied = list(retrieval_candidates)
    if {str(c.get("asset_id")) for c in supplied} != selected_asset_ids:
        raise AssetLineageValidationError("retrieval candidate set does not exactly match explicit selection")
    bindings: list[CompositionAssetBinding] = []
    used_scene_ids: set[str] = set()
    for candidate in supplied:
        snapshot = candidate_identity_snapshot(candidate)
        asset_id = snapshot["asset_id"]
        scene_id = snapshot["scene_id"]
        if asset_id not in selected_asset_ids or scene_id not in selected_scene_ids:
            raise AssetLineageValidationError("candidate is not present in the explicit selection receipt")
        candidate_workspace = snapshot["workspace_id"]
        if candidate_workspace != workspace_id:
            raise AssetLineageValidationError("selected asset crosses workspace boundary")
        if candidate.get("candidate_id") not in (None, candidate_id):
            raise AssetLineageValidationError("selected asset candidate_id does not match the governing candidate")
        if scene_id in used_scene_ids:
            raise AssetLineageValidationError("a scene may only bind once in a composition asset pack")
        used_scene_ids.add(scene_id)
        scene_index = int((scene_index_by_scene_id or {}).get(scene_id, len(bindings) + 1))
        core = {
            "demand_id": f"ASSET-{candidate_id}-{scene_index:03d}",
            "scene_index": scene_index,
            "asset_id": snapshot["asset_id"],
            "scene_id": scene_id,
            "workspace_id": workspace_id,
            "source_version": snapshot["source_version"],
            "source_sha256": snapshot["source_sha256"],
            "start_time": snapshot["start_time"],
            "end_time": snapshot["end_time"],
            "duration": snapshot["duration"],
            "semantic_role": snapshot["semantic_role"],
            "insert_role": snapshot["insert_role"],
            "rights": snapshot["rights"],
            "provenance": snapshot["provenance"],
            "candidate_snapshot_sha256": snapshot["candidate_snapshot_sha256"],
            "retrieval_receipt_id": _require_text(retrieval_receipt_id, "retrieval_receipt_id"),
            "selection_receipt_id": receipt.receipt_id,
        }
        binding = CompositionAssetBinding(
            **core,
            binding_sha256=_canonical_sha256(core),
        )
        bindings.append(binding)

    bindings.sort(key=lambda item: (item.scene_index, item.asset_id))
    lineage_leaves = []
    for binding in bindings:
        lineage_leaves.append(
            _canonical_sha256(
                {
                    "kind": "asset-binding",
                    "binding_sha256": binding.binding_sha256,
                    "candidate_snapshot_sha256": binding.candidate_snapshot_sha256,
                }
            )
        )
    lineage_leaves.extend(
        [
            _canonical_sha256({"kind": "selection-receipt", "receipt_sha256": receipt.receipt_sha256}),
            _canonical_sha256({"kind": "program-ref", "program_ref": normalized_program_ref}),
        ]
    )
    lineage_root = _lineage_root(
        workspace_id=workspace_id,
        candidate_id=candidate_id,
        program_ref=normalized_program_ref,
        selection_receipt=receipt,
        bindings=bindings,
    )
    pack_payload = {
        "pack_id": f"CAP-{lineage_root[:20]}",
        "pack_version": PACK_VERSION,
        "mandate_id": MANDATE_ID,
        "state": BOUND_STATE,
        "workspace_id": workspace_id,
        "candidate_id": candidate_id,
        "program_ref": normalized_program_ref,
        "selection_receipt": receipt,
        "bindings": tuple(bindings),
        "lineage_leaves_sha256": tuple(sorted(lineage_leaves)),
        "lineage_root_sha256": lineage_root,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    return CompositionAssetPack(
        **pack_payload,
        pack_sha256=_canonical_sha256(pack_payload),
    )


def validate_composition_asset_pack(
    pack: CompositionAssetPack | Mapping[str, Any],
    *,
    current_retrieval_candidates: Sequence[Mapping[str, Any]] | None = None,
    current_selection_receipt: ExplicitSelectionReceipt | Mapping[str, Any] | None = None,
    current_program_ref: Mapping[str, str] | None = None,
) -> CompositionAssetPack:
    """
    Verify the persisted pack and, when supplied, the current governed inputs.

    A mismatch is an invalidation event, not a mutation. The original pack is returned
    only when every compared input remains byte-equivalent at the governed field level.
    """
    bound_pack = pack if isinstance(pack, CompositionAssetPack) else CompositionAssetPack(**dict(pack))
    if bound_pack.state == INVALIDATED_STATE:
        raise AssetBindingInvalidatedError("composition asset pack is already invalidated")

    if current_selection_receipt is not None:
        current = (
            current_selection_receipt
            if isinstance(current_selection_receipt, ExplicitSelectionReceipt)
            else ExplicitSelectionReceipt(**dict(current_selection_receipt))
        )
        if current.receipt_sha256 != bound_pack.selection_receipt.receipt_sha256:
            raise AssetBindingInvalidatedError("selection receipt changed after binding")

    if current_program_ref is not None:
        normalized_current_program_ref = {
            "object_id": _require_text(current_program_ref.get("object_id"), "program_ref.object_id"),
            "version": _require_text(current_program_ref.get("version"), "program_ref.version"),
            "sha256": _require_sha256(current_program_ref.get("sha256"), "program_ref.sha256"),
        }
        if normalized_current_program_ref != dict(bound_pack.program_ref):
            raise AssetBindingInvalidatedError("program reference changed after binding")

    if current_retrieval_candidates is not None:
        current_snapshots = {
            candidate_identity_snapshot(candidate)["asset_id"]: candidate_identity_snapshot(candidate)
            for candidate in current_retrieval_candidates
        }
        bound_snapshots = {binding.asset_id: binding for binding in bound_pack.bindings}
        if set(current_snapshots) != set(bound_snapshots):
            raise AssetBindingInvalidatedError("selected asset set changed after binding")
        for asset_id, binding in bound_snapshots.items():
            current_snapshot_hash = current_snapshots[asset_id]["candidate_snapshot_sha256"]
            if current_snapshot_hash != binding.candidate_snapshot_sha256:
                raise AssetBindingInvalidatedError(
                    f"bound asset '{asset_id}' changed identity, timestamp, rights, role, or provenance"
                )
    return bound_pack


def invalidate_composition_asset_pack(pack: CompositionAssetPack | Mapping[str, Any]) -> CompositionAssetPack:
    """Produce a new INVALIDATED version without rewriting the historical BOUND pack."""
    bound = pack if isinstance(pack, CompositionAssetPack) else CompositionAssetPack(**dict(pack))
    payload = bound.model_dump(exclude={"pack_sha256"})
    payload["state"] = INVALIDATED_STATE
    return CompositionAssetPack(
        **payload,
        pack_sha256=_canonical_sha256(payload),
    )


def apply_composition_asset_pack(
    program: Any,
    pack: CompositionAssetPack,
) -> tuple[Any, Any]:
    """
    Project a verified CompositionAssetPack into the existing SemanticProgram shape.

    No semantic fields are inferred or re-selected. Each bound asset is copied verbatim
    into its declared scene index, and a standard CompositionHandoffReceipt is emitted
    with the M0064 lineage root and binding digests in metadata.
    """
    bound = validate_composition_asset_pack(pack)
    if getattr(program, "workspace_id", None) != bound.workspace_id:
        raise AssetLineageValidationError("program workspace does not match asset pack")
    if getattr(program, "candidate_id", None) != bound.candidate_id:
        raise AssetLineageValidationError("program candidate does not match asset pack")
    program_ref = {
        "object_id": str(getattr(program, "program_id")),
        "version": str(getattr(program, "program_version", "1.0.0")),
    }
    if bound.program_ref.get("object_id") != program_ref["object_id"] or bound.program_ref.get("version") != program_ref["version"]:
        raise AssetLineageValidationError("asset pack program reference does not match SemanticProgram")
    computed_program_sha256 = _canonical_sha256(program.model_dump(mode="python"))
    if bound.program_ref.get("sha256") != computed_program_sha256:
        raise AssetLineageValidationError("asset pack program hash does not match the executable SemanticProgram")

    scenes_by_index = {int(scene.scene_index): scene for scene in program.scenes}
    scene_updates: dict[int, list[dict[str, Any]]] = {}
    for binding in bound.bindings:
        if binding.scene_index not in scenes_by_index:
            raise AssetLineageValidationError(
                f"bound asset scene_index {binding.scene_index} is absent from SemanticProgram"
            )
        scene_updates.setdefault(binding.scene_index, []).append(binding.to_asset_insert())

    updated_scenes = []
    for scene in program.scenes:
        additions = scene_updates.get(int(scene.scene_index), [])
        updated_scenes.append(
            scene.model_copy(update={"asset_inserts": [*scene.asset_inserts, *additions]})
        )

    updated_program = program.model_copy(update={"scenes": updated_scenes})
    from .domain import CompositionHandoffReceipt

    evidence_hashes = [str(scene.text_sha256) for scene in updated_program.scenes]
    receipt_core = {
        "program_id": updated_program.program_id,
        "candidate_id": updated_program.candidate_id,
        "storyboard_id": updated_program.storyboard_id,
        "evidence_sha256_list": evidence_hashes,
        "asset_id_list": [binding.asset_id for binding in bound.bindings],
        "lineage_root_sha256": bound.lineage_root_sha256,
        "binding_sha256": [binding.binding_sha256 for binding in bound.bindings],
        "selection_receipt_id": bound.selection_receipt.receipt_id,
    }
    receipt_sha256 = _canonical_sha256(receipt_core)
    handoff = CompositionHandoffReceipt(
        program_id=updated_program.program_id,
        candidate_id=updated_program.candidate_id,
        storyboard_id=updated_program.storyboard_id,
        evidence_sha256_list=evidence_hashes,
        asset_id_list=[binding.asset_id for binding in bound.bindings],
        wrong_reading_locks=list(updated_program.wrong_reading_locks),
        receipt_sha256=receipt_sha256,
        metadata={
            "mandate_id": MANDATE_ID,
            "pack_id": bound.pack_id,
            "pack_sha256": bound.pack_sha256,
            "lineage_root_sha256": bound.lineage_root_sha256,
            "binding_sha256": [binding.binding_sha256 for binding in bound.bindings],
            "selection_receipt_id": bound.selection_receipt.receipt_id,
            "retrieval_receipt_id": bound.bindings[0].retrieval_receipt_id,
        },
    )
    return updated_program, handoff
