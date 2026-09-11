"""Bounded, proposal-only Visual Chat over the canonical Visual Asset Studio projection.

M0088 classifies operator language into a closed action vocabulary and emits an
immutable proposal bound to the current canonical revision. It never writes
storyboard/VAE state, performs retrieval, or promotes a candidate.
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Mapping

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ca_contracts import canonical_sha256, utc_now_rfc3339


class VisualChatValidationError(ValueError):
    """Raised when a Visual Chat request is not a governed operator proposal."""


class VisualChatAction(str, Enum):
    EXPLAIN = "EXPLAIN"
    FIND_ALTERNATIVES = "FIND_ALTERNATIVES"
    REPLACE_SOURCE = "REPLACE_SOURCE"
    REGENERATE_TRANSFORMATION = "REGENERATE_TRANSFORMATION"
    REGENERATE_BBOX_PROMPT = "REGENERATE_BBOX_PROMPT"
    COMPOSITION_ALTERNATIVES = "COMPOSITION_ALTERNATIVES"
    REDUCE_INTENSITY = "REDUCE_INTENSITY"
    MOVE_EMPHASIS = "MOVE_EMPHASIS"
    PRESERVE_EVIDENCE = "PRESERVE_EVIDENCE"


class VisualChatProposalStatus(str, Enum):
    PROPOSED = "PROPOSED"
    NEEDS_CANDIDATES = "NEEDS_CANDIDATES"
    BLOCKED = "BLOCKED"


class VisualChatRequest(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    natural_language_request: str = Field(min_length=1, max_length=2000)
    target_ref: dict[str, str]
    target_node_id: str = Field(min_length=1)
    operator_actor: dict[str, str]
    expected_state_version: int = Field(ge=1)
    action: VisualChatAction | None = None
    candidate_refs: tuple[dict[str, str], ...] = ()
    canonical_revision_ref: dict[str, str] | None = None

    @model_validator(mode="after")
    def validate_request(self) -> "VisualChatRequest":
        if not self.natural_language_request.strip():
            raise ValueError("natural_language_request must contain text")
        actor = self.operator_actor
        if actor.get("actor_type") != "human" or actor.get("workflow_role") != "operator":
            raise ValueError("visual chat proposals require a human operator actor")
        for ref in (self.target_ref, *self.candidate_refs):
            if not {"object_id", "version", "sha256"} <= set(ref):
                raise ValueError("all visual chat refs require object_id, version and sha256")
        return self


class VisualChatOperation(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    operation_id: str
    operation_type: str
    expected_effect: str
    governed: bool = True


class VisualChatProposal(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    proposal_id: str
    proposal_version: str = "1.0.0"
    action: VisualChatAction
    status: VisualChatProposalStatus
    target_ref: dict[str, str]
    target_node_id: str
    canonical_revision_ref: dict[str, str]
    expected_state_version: int
    interpretation: str
    exact_operations: tuple[VisualChatOperation, ...]
    candidate_refs: tuple[dict[str, str], ...] = ()
    evidence_preserved: bool = True
    requires_operator_authorization: bool = True
    canonical_state_mutated: bool = False
    created_at: str
    proposal_sha256: str

    @model_validator(mode="after")
    def validate_immutable_proposal(self) -> "VisualChatProposal":
        core = self.model_dump(mode="json", exclude={"proposal_id", "proposal_sha256"})
        expected = canonical_sha256(core)
        if self.proposal_sha256 != expected:
            raise ValueError("proposal_sha256 does not match immutable proposal payload")
        if self.proposal_id != f"visual-chat:{expected}":
            raise ValueError("proposal_id must be content-addressed")
        if self.canonical_state_mutated:
            raise ValueError("Visual Chat cannot mutate canonical state")
        if self.action == VisualChatAction.PRESERVE_EVIDENCE and not self.evidence_preserved:
            raise ValueError("preserve-evidence proposals must preserve evidence")
        return self


_KEYWORDS: tuple[tuple[VisualChatAction, tuple[str, ...]], ...] = (
    (VisualChatAction.PRESERVE_EVIDENCE, ("preserve evidence", "keep the source", "do not change the source")),
    (VisualChatAction.REPLACE_SOURCE, ("replace source", "swap source", "different source")),
    (VisualChatAction.FIND_ALTERNATIVES, ("find alternatives", "alternative assets", "other options")),
    (VisualChatAction.REGENERATE_BBOX_PROMPT, ("bbox", "bounding box", "regenerate prompt")),
    (VisualChatAction.REGENERATE_TRANSFORMATION, ("regenerate transform", "regenerate transformation", "redo transform")),
    (VisualChatAction.COMPOSITION_ALTERNATIVES, ("composition alternatives", "alternate composition", "three compositions")),
    (VisualChatAction.REDUCE_INTENSITY, ("reduce intensity", "reduce visual intensity", "less intense", "subtle")),
    (VisualChatAction.MOVE_EMPHASIS, ("increase intensity", "more intense", "move emphasis", "emphasize")),
)


def classify_visual_chat_request(text: str) -> VisualChatAction:
    normalized = " ".join(text.casefold().split())
    for action, keywords in _KEYWORDS:
        if any(keyword in normalized for keyword in keywords):
            return action
    return VisualChatAction.EXPLAIN


def _operations(action: VisualChatAction, target_node_id: str) -> tuple[VisualChatOperation, ...]:
    specs: dict[VisualChatAction, tuple[tuple[str, str], ...]] = {
        VisualChatAction.EXPLAIN: (("inspect_canonical_layer", "explain the linked canonical layer and evidence"),),
        VisualChatAction.FIND_ALTERNATIVES: (("enumerate_governed_candidates", "present governed alternatives without promotion"),),
        VisualChatAction.REPLACE_SOURCE: (("propose_source_replacement", "replace the source only after candidate and operator approval"),),
        VisualChatAction.REGENERATE_TRANSFORMATION: (("regenerate_transformation_proposal", "recompute a bounded transformation proposal"),),
        VisualChatAction.REGENERATE_BBOX_PROMPT: (("regenerate_bbox_prompt", "produce a bounded BBOX prompt proposal"),),
        VisualChatAction.COMPOSITION_ALTERNATIVES: (
            ("composition_alternative_1", "propose a restrained composition alternative"),
            ("composition_alternative_2", "propose a balanced composition alternative"),
            ("composition_alternative_3", "propose a high-emphasis composition alternative"),
        ),
        VisualChatAction.REDUCE_INTENSITY: (("reduce_visual_intensity", "reduce visual salience while preserving evidence"),),
        VisualChatAction.MOVE_EMPHASIS: (("move_visual_emphasis", "move emphasis within governed evidence bounds"),),
        VisualChatAction.PRESERVE_EVIDENCE: (("preserve_source_evidence", "retain source lineage and semantic reading"),),
    }
    return tuple(
        VisualChatOperation(
            operation_id=f"visual-chat-op:{action.value.lower()}:{index + 1}",
            operation_type=op,
            expected_effect=effect,
        )
        for index, (op, effect) in enumerate(specs[action])
    )


def compile_visual_chat(
    request: VisualChatRequest,
    *,
    canonical_revision_ref: Mapping[str, str],
    current_state_version: int,
) -> VisualChatProposal:
    if request.expected_state_version != current_state_version:
        raise VisualChatValidationError("stale canonical state version")
    canonical = dict(canonical_revision_ref)
    if request.canonical_revision_ref is not None and dict(request.canonical_revision_ref) != canonical:
        raise VisualChatValidationError("canonical revision digest mismatch")
    action = request.action or classify_visual_chat_request(request.natural_language_request)
    candidates = tuple(dict(ref) for ref in request.candidate_refs)
    status = VisualChatProposalStatus.PROPOSED
    interpretation = f"Bounded {action.value.lower().replace('_', ' ')} proposal for canonical node {request.target_node_id}."
    if action == VisualChatAction.REPLACE_SOURCE and not candidates:
        status = VisualChatProposalStatus.NEEDS_CANDIDATES
        interpretation = "Source replacement is held until an eligible governed candidate portfolio is supplied."
    if action == VisualChatAction.PRESERVE_EVIDENCE:
        interpretation = "Preserve source lineage and semantic reading; no replacement or semantic rewrite is permitted."
    core = {
        "proposal_version": "1.0.0",
        "action": action,
        "status": status,
        "target_ref": dict(request.target_ref),
        "target_node_id": request.target_node_id,
        "canonical_revision_ref": canonical,
        "expected_state_version": current_state_version,
        "interpretation": interpretation,
        "exact_operations": [op.model_dump(mode="json") for op in _operations(action, request.target_node_id)],
        "candidate_refs": [dict(ref) for ref in candidates],
        "evidence_preserved": True,
        "requires_operator_authorization": True,
        "canonical_state_mutated": False,
        "created_at": utc_now_rfc3339(),
    }
    # Time is not part of replay identity; use a stable timestamp for identical inputs.
    core["created_at"] = "1970-01-01T00:00:00Z"
    digest = canonical_sha256(core)
    return VisualChatProposal(proposal_id=f"visual-chat:{digest}", proposal_sha256=digest, **core)


__all__ = [
    "VisualChatAction",
    "VisualChatOperation",
    "VisualChatProposal",
    "VisualChatProposalStatus",
    "VisualChatRequest",
    "VisualChatValidationError",
    "classify_visual_chat_request",
    "compile_visual_chat",
]
