"""
Causal admission enforcement for INV-CAUSAL-001.

Runtime admission boundary that prevents downstream execution when required
upstream ancestors are missing, out-of-order, stale, mismatched, or invalid.

A downstream program/node must not run because a UI says it is ready, because
a caller supplies a display-name placeholder, or because a missing ancestor
was synthesized.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Mapping, Sequence

from ...domain.enums import NodeState
from ...domain.errors import PipelineLifecycleError, PipelineValidationError



class CausalAdmissionDecision(StrEnum):
    ADMITTED = "ADMITTED"
    BLOCKED = "BLOCKED"


class CausalBlockReason(StrEnum):
    MISSING_ANCESTOR = "MISSING_ANCESTOR"
    WRONG_ORDER = "WRONG_ORDER"
    STALE_OR_MISMATCHED_IDENTITY = "STALE_OR_MISMATCHED_IDENTITY"
    INVALID_PREREQUISITE_STATE = "INVALID_PREREQUISITE_STATE"
    SYNTHESIZED_PLACEHOLDER = "SYNTHESIZED_PLACEHOLDER"
    BYPASS_ATTEMPT = "BYPASS_ATTEMPT"
    NO_BINDING = "NO_BINDING"


@dataclass(frozen=True)
class RequiredAncestor:
    """Declaration of a required upstream ancestor for causal admission."""

    ancestor_id: str
    required_state: str = NodeState.SUCCEEDED.value
    identity_digest: str | None = None  # expected content digest when known
    revision: str | None = None
    allow_placeholder: bool = False


@dataclass(frozen=True)
class AncestorBinding:
    """Authoritative binding of an admitted ancestor object.

    Identity is bound to the admitted object (digest/revision), not a display name.
    """

    ancestor_id: str
    identity: str  # stable semantic identity (not display name)
    content_digest: str
    revision: str
    state: str
    admitted_at_utc: str | None = None
    is_placeholder: bool = False
    provenance: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CausalBlock:
    reason: CausalBlockReason
    ancestor_id: str | None
    message: str
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CausalAdmissionResult:
    decision: CausalAdmissionDecision
    node_id: str
    blocks: tuple[CausalBlock, ...] = ()
    admitted_ancestors: tuple[str, ...] = ()

    @property
    def is_admitted(self) -> bool:
        return self.decision == CausalAdmissionDecision.ADMITTED

    def to_runtime_fact(self) -> dict[str, Any]:
        """Projection suitable for UI / operator surface (runtime truth, not invented)."""
        return {
            "node_id": self.node_id,
            "decision": self.decision.value,
            "admitted": self.is_admitted,
            "blocks": [
                {
                    "reason": b.reason.value,
                    "ancestor_id": b.ancestor_id,
                    "message": b.message,
                    "details": dict(b.details),
                }
                for b in self.blocks
            ],
            "admitted_ancestors": list(self.admitted_ancestors),
        }


class CausalAdmissionError(PipelineLifecycleError):
    """Raised when causal admission fails at the runtime boundary."""

    def __init__(self, result: CausalAdmissionResult):
        self.result = result
        messages = "; ".join(b.message for b in result.blocks) or "causal admission denied"
        super().__init__(f"causal admission blocked for node {result.node_id}: {messages}")


class CausalAdmissionService:
    """
    Enforces INV-CAUSAL-001 at the runtime admission boundary.

    Checks:
    - required ancestors present and in required state
    - topological / phase order respected
    - ancestor identity digests match expected (no stale/mismatched)
    - no synthesized placeholders accepted as real ancestors
    - no force-run / bypass of admission
    """

    def __init__(
        self,
        *,
        allow_force: bool = False,
    ):
        # Force-run must never bypass causal admission (prohibition).
        if allow_force:
            raise PipelineValidationError(
                "force-run / allow_force is prohibited at the causal admission boundary"
            )
        self._allow_force = False

    def evaluate(
        self,
        node_id: str,
        *,
        required_ancestors: Sequence[RequiredAncestor],
        bindings: Mapping[str, AncestorBinding],
        node_states: Mapping[str, str],
        topological_order: Sequence[str] | None = None,
        phase_order: int | None = None,
        ancestor_phase_orders: Mapping[str, int] | None = None,
        force: bool = False,
    ) -> CausalAdmissionResult:
        """
        Evaluate causal admission for a node.

        Returns a structured result. Callers that must fail-closed should
        call require_admitted() or raise on BLOCKED.
        """
        if force:
            return CausalAdmissionResult(
                decision=CausalAdmissionDecision.BLOCKED,
                node_id=node_id,
                blocks=(
                    CausalBlock(
                        reason=CausalBlockReason.BYPASS_ATTEMPT,
                        ancestor_id=None,
                        message="force-run / bypass of causal admission is prohibited",
                        details={"force": True},
                    ),
                ),
            )

        blocks: list[CausalBlock] = []
        admitted: list[str] = []

        # Phase / topological order check (wrong order)
        if topological_order is not None and node_id in topological_order:
            pos = {nid: i for i, nid in enumerate(topological_order)}
            node_pos = pos[node_id]
            for req in required_ancestors:
                if req.ancestor_id in pos and pos[req.ancestor_id] >= node_pos:
                    blocks.append(
                        CausalBlock(
                            reason=CausalBlockReason.WRONG_ORDER,
                            ancestor_id=req.ancestor_id,
                            message=(
                                f"ancestor {req.ancestor_id} appears at or after "
                                f"node {node_id} in topological order"
                            ),
                            details={
                                "node_position": node_pos,
                                "ancestor_position": pos[req.ancestor_id],
                            },
                        )
                    )

        if phase_order is not None and ancestor_phase_orders:
            for req in required_ancestors:
                a_phase = ancestor_phase_orders.get(req.ancestor_id)
                if a_phase is not None and a_phase >= phase_order:
                    blocks.append(
                        CausalBlock(
                            reason=CausalBlockReason.WRONG_ORDER,
                            ancestor_id=req.ancestor_id,
                            message=(
                                f"ancestor {req.ancestor_id} phase_order={a_phase} "
                                f"is not strictly before node phase_order={phase_order}"
                            ),
                            details={
                                "node_phase_order": phase_order,
                                "ancestor_phase_order": a_phase,
                            },
                        )
                    )

        for req in required_ancestors:
            binding = bindings.get(req.ancestor_id)

            if binding is None:
                # Check if state exists but no binding (missing authoritative identity)
                state = node_states.get(req.ancestor_id)
                if state is None:
                    blocks.append(
                        CausalBlock(
                            reason=CausalBlockReason.MISSING_ANCESTOR,
                            ancestor_id=req.ancestor_id,
                            message=f"required ancestor {req.ancestor_id} is missing",
                            details={},
                        )
                    )
                else:
                    blocks.append(
                        CausalBlock(
                            reason=CausalBlockReason.NO_BINDING,
                            ancestor_id=req.ancestor_id,
                            message=(
                                f"ancestor {req.ancestor_id} has state={state} but no "
                                "authoritative identity binding (digest/revision)"
                            ),
                            details={"state": state},
                        )
                    )
                continue

            # Reject synthesized placeholders
            if binding.is_placeholder and not req.allow_placeholder:
                blocks.append(
                    CausalBlock(
                        reason=CausalBlockReason.SYNTHESIZED_PLACEHOLDER,
                        ancestor_id=req.ancestor_id,
                        message=(
                            f"ancestor {req.ancestor_id} is a synthesized placeholder; "
                            "placeholders cannot satisfy causal admission"
                        ),
                        details={
                            "identity": binding.identity,
                            "is_placeholder": True,
                        },
                    )
                )
                continue

            # State must match required
            if binding.state != req.required_state:
                blocks.append(
                    CausalBlock(
                        reason=CausalBlockReason.INVALID_PREREQUISITE_STATE,
                        ancestor_id=req.ancestor_id,
                        message=(
                            f"ancestor {req.ancestor_id} state={binding.state} "
                            f"does not satisfy required_state={req.required_state}"
                        ),
                        details={
                            "actual_state": binding.state,
                            "required_state": req.required_state,
                        },
                    )
                )
                continue

            # Also cross-check live node_states if provided
            live_state = node_states.get(req.ancestor_id)
            if live_state is not None and live_state != binding.state:
                blocks.append(
                    CausalBlock(
                        reason=CausalBlockReason.INVALID_PREREQUISITE_STATE,
                        ancestor_id=req.ancestor_id,
                        message=(
                            f"ancestor {req.ancestor_id} binding state={binding.state} "
                            f"mismatches live node state={live_state}"
                        ),
                        details={
                            "binding_state": binding.state,
                            "live_state": live_state,
                        },
                    )
                )
                continue

            # Digest / identity integrity
            if req.identity_digest is not None:
                if binding.content_digest != req.identity_digest:
                    blocks.append(
                        CausalBlock(
                            reason=CausalBlockReason.STALE_OR_MISMATCHED_IDENTITY,
                            ancestor_id=req.ancestor_id,
                            message=(
                                f"ancestor {req.ancestor_id} content_digest mismatch "
                                f"(expected={req.identity_digest}, actual={binding.content_digest})"
                            ),
                            details={
                                "expected_digest": req.identity_digest,
                                "actual_digest": binding.content_digest,
                                "identity": binding.identity,
                            },
                        )
                    )
                    continue

            if req.revision is not None and binding.revision != req.revision:
                blocks.append(
                    CausalBlock(
                        reason=CausalBlockReason.STALE_OR_MISMATCHED_IDENTITY,
                        ancestor_id=req.ancestor_id,
                        message=(
                            f"ancestor {req.ancestor_id} revision mismatch "
                            f"(expected={req.revision}, actual={binding.revision})"
                        ),
                        details={
                            "expected_revision": req.revision,
                            "actual_revision": binding.revision,
                        },
                    )
                )
                continue

            # Reject empty / display-name-like identities (heuristic for synthesized)
            if not binding.identity or binding.identity.strip() == "":
                blocks.append(
                    CausalBlock(
                        reason=CausalBlockReason.STALE_OR_MISMATCHED_IDENTITY,
                        ancestor_id=req.ancestor_id,
                        message=f"ancestor {req.ancestor_id} has empty identity",
                        details={},
                    )
                )
                continue

            admitted.append(req.ancestor_id)

        if blocks:
            return CausalAdmissionResult(
                decision=CausalAdmissionDecision.BLOCKED,
                node_id=node_id,
                blocks=tuple(blocks),
                admitted_ancestors=tuple(admitted),
            )

        return CausalAdmissionResult(
            decision=CausalAdmissionDecision.ADMITTED,
            node_id=node_id,
            blocks=(),
            admitted_ancestors=tuple(admitted),
        )

    def require_admitted(
        self,
        node_id: str,
        *,
        required_ancestors: Sequence[RequiredAncestor],
        bindings: Mapping[str, AncestorBinding],
        node_states: Mapping[str, str],
        topological_order: Sequence[str] | None = None,
        phase_order: int | None = None,
        ancestor_phase_orders: Mapping[str, int] | None = None,
        force: bool = False,
    ) -> CausalAdmissionResult:
        """Evaluate and raise CausalAdmissionError if not admitted."""
        result = self.evaluate(
            node_id,
            required_ancestors=required_ancestors,
            bindings=bindings,
            node_states=node_states,
            topological_order=topological_order,
            phase_order=phase_order,
            ancestor_phase_orders=ancestor_phase_orders,
            force=force,
        )
        if not result.is_admitted:
            raise CausalAdmissionError(result)
        return result

    def required_ancestors_from_workflow_edges(
        self,
        workflow: Mapping[str, Any],
        node_id: str,
    ) -> list[RequiredAncestor]:
        """
        Derive required ancestors from workflow edges targeting node_id.

        Uses existing dependency declarations rather than inventing a second graph.
        """
        required: list[RequiredAncestor] = []
        for edge in workflow.get("edges", []):
            if edge.get("target_node_id") == node_id:
                source = edge.get("source_node_id")
                if source:
                    required.append(
                        RequiredAncestor(
                            ancestor_id=source,
                            required_state=NodeState.SUCCEEDED.value,
                        )
                    )
        return required

    def bindings_from_node_states_and_artifacts(
        self,
        node_states: Mapping[str, str],
        artifact_bindings: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> dict[str, AncestorBinding]:
        """
        Build AncestorBinding map from live states + optional artifact identity records.

        artifact_bindings[node_id] expected keys:
          identity, content_digest, revision, is_placeholder (optional), admitted_at_utc (optional)
        """
        artifact_bindings = artifact_bindings or {}
        result: dict[str, AncestorBinding] = {}
        for nid, state in node_states.items():
            art = artifact_bindings.get(nid, {})
            identity = art.get("identity") or art.get("semantic_identity")
            digest = art.get("content_digest") or art.get("digest")
            revision = art.get("revision") or art.get("version") or "0"
            if identity is None or digest is None:
                # No authoritative binding — omit so evaluate treats as NO_BINDING / MISSING
                continue
            result[nid] = AncestorBinding(
                ancestor_id=nid,
                identity=str(identity),
                content_digest=str(digest),
                revision=str(revision),
                state=state,
                admitted_at_utc=art.get("admitted_at_utc"),
                is_placeholder=bool(art.get("is_placeholder", False)),
                provenance=dict(art.get("provenance") or {}),
            )
        return result
