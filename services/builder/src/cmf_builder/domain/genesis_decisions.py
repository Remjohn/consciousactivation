from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from hashlib import sha256
import json
from typing import Mapping

from cmf_builder.domain.atomicity import DraftHarnessModel
from cmf_builder.domain.genesis_questions import (
    DecisionGraph,
    GenesisQuestionPackage,
)


GENESIS_DECISION_VERSION = "1.0.0"


class GenesisDecisionError(Exception):
    code = "GenesisDecisionError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class GenesisDecisionInvalid(GenesisDecisionError):
    code = "GenesisDecisionInvalid"


class CascadeStatus(str, Enum):
    OPEN = "OPEN"
    PARTIALLY_RATIFIED = "PARTIALLY_RATIFIED"
    CASCADE_LOCKED = "CASCADE_LOCKED"


@dataclass(frozen=True, slots=True)
class HumanAnswer:
    answer_id: str
    answer_hash: str
    version: str
    run_id: str
    package_ref: str
    package_hash: str
    decision_node_id: str
    raw_answer: str
    human_id: str
    answered_at: datetime

    @classmethod
    def create(cls, **values: object) -> "HumanAnswer":
        payload = {"version": GENESIS_DECISION_VERSION, **values}
        _require_text(payload, "raw_answer", "human_id", "run_id", "package_ref", "package_hash", "decision_node_id")
        digest = sha256(_canonical_json(payload)).hexdigest()
        return cls(answer_id=f"human-answer_{digest}", answer_hash=f"sha256:{digest}", **payload)

    def canonical_dict(self) -> dict[str, object]:
        return {"answer_hash": self.answer_hash, "answer_id": self.answer_id, **self._payload()}

    def _payload(self) -> dict[str, object]:
        return {
            "answered_at": self.answered_at.isoformat(), "decision_node_id": self.decision_node_id,
            "human_id": self.human_id, "package_hash": self.package_hash,
            "package_ref": self.package_ref, "raw_answer": self.raw_answer,
            "run_id": self.run_id, "version": self.version,
        }


@dataclass(frozen=True, slots=True)
class FinalDecision:
    final_decision_id: str
    final_decision_hash: str
    version: str
    run_id: str
    answer_ref: str
    answer_hash: str
    decision_node_id: str
    selected_option: str
    rationale: str
    human_id: str
    decided_at: datetime
    provisional_draft_ref: str | None

    @classmethod
    def create(cls, *, answer: HumanAnswer, selected_option: str, rationale: str, provisional_draft_ref: str | None = None) -> "FinalDecision":
        payload = {
            "answer_hash": answer.answer_hash, "answer_ref": answer.answer_id,
            "decided_at": answer.answered_at.isoformat(), "decision_node_id": answer.decision_node_id,
            "human_id": answer.human_id, "provisional_draft_ref": provisional_draft_ref,
            "rationale": rationale, "run_id": answer.run_id,
            "selected_option": selected_option, "version": GENESIS_DECISION_VERSION,
        }
        _require_text(payload, "selected_option", "rationale")
        digest = sha256(_canonical_json(payload)).hexdigest()
        return cls(
            final_decision_id=f"final-decision_{digest}", final_decision_hash=f"sha256:{digest}",
            version=GENESIS_DECISION_VERSION, run_id=answer.run_id,
            answer_ref=answer.answer_id, answer_hash=answer.answer_hash,
            decision_node_id=answer.decision_node_id, selected_option=selected_option,
            rationale=rationale, human_id=answer.human_id, decided_at=answer.answered_at,
            provisional_draft_ref=provisional_draft_ref,
        )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "answer_hash": self.answer_hash, "answer_ref": self.answer_ref,
            "decided_at": self.decided_at.isoformat(), "decision_node_id": self.decision_node_id,
            "final_decision_hash": self.final_decision_hash, "final_decision_id": self.final_decision_id,
            "human_id": self.human_id, "provisional_draft_ref": self.provisional_draft_ref,
            "rationale": self.rationale, "run_id": self.run_id,
            "selected_option": self.selected_option, "version": self.version,
        }


@dataclass(frozen=True, slots=True)
class HarnessIRDecisionAmendment:
    amendment_id: str
    amendment_hash: str
    version: str
    run_id: str
    model_ref: str
    model_hash: str
    graph_ref: str
    graph_hash: str
    package_ref: str
    answer_ref: str
    final_decision_ref: str
    affected_ir_paths: tuple[str, ...]
    selected_value: str
    previous_authority: str
    new_authority: str
    invalidation_edges: tuple[str, ...]
    authority_identity: str

    @classmethod
    def compile(cls, *, model: DraftHarnessModel, graph: DecisionGraph, package: GenesisQuestionPackage, answer: HumanAnswer, decision: FinalDecision) -> "HarnessIRDecisionAmendment":
        node = graph.selected_node().definition
        node.validate(model=model)
        if (
            package.graph_ref != graph.graph_id or package.package_id != answer.package_ref
            or answer.answer_id != decision.answer_ref or answer.answer_hash != decision.answer_hash
            or node.decision_id != answer.decision_node_id or node.decision_id != decision.decision_node_id
            or decision.selected_option not in node.options or answer.human_id != decision.human_id
        ):
            raise GenesisDecisionInvalid("Answer, decision, selected node and governed options must agree.")
        payload = {
            "affected_ir_paths": list(node.affected_ir_paths), "answer_ref": answer.answer_id,
            "authority_identity": decision.human_id, "final_decision_ref": decision.final_decision_id,
            "graph_hash": graph.graph_hash, "graph_ref": graph.graph_id,
            "invalidation_edges": list(node.invalidation_edges), "model_hash": model.model_hash,
            "model_ref": model.model_id, "new_authority": "HUMAN_RATIFIED",
            "package_ref": package.package_id, "previous_authority": "UNRATIFIED",
            "run_id": graph.run_id, "selected_value": decision.selected_option,
            "version": GENESIS_DECISION_VERSION,
        }
        digest = sha256(_canonical_json(payload)).hexdigest()
        return cls(
            amendment_id=f"harness-ir-decision-amendment_{digest}", amendment_hash=f"sha256:{digest}",
            version=GENESIS_DECISION_VERSION, run_id=graph.run_id,
            model_ref=model.model_id, model_hash=model.model_hash,
            graph_ref=graph.graph_id, graph_hash=graph.graph_hash,
            package_ref=package.package_id, answer_ref=answer.answer_id,
            final_decision_ref=decision.final_decision_id,
            affected_ir_paths=node.affected_ir_paths, selected_value=decision.selected_option,
            previous_authority="UNRATIFIED", new_authority="HUMAN_RATIFIED",
            invalidation_edges=node.invalidation_edges, authority_identity=decision.human_id,
        )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "affected_ir_paths": list(self.affected_ir_paths), "amendment_hash": self.amendment_hash,
            "amendment_id": self.amendment_id, "answer_ref": self.answer_ref,
            "authority_identity": self.authority_identity, "final_decision_ref": self.final_decision_ref,
            "graph_hash": self.graph_hash, "graph_ref": self.graph_ref,
            "invalidation_edges": list(self.invalidation_edges), "model_hash": self.model_hash,
            "model_ref": self.model_ref, "new_authority": self.new_authority,
            "package_ref": self.package_ref, "previous_authority": self.previous_authority,
            "run_id": self.run_id, "selected_value": self.selected_value, "version": self.version,
        }


@dataclass(frozen=True, slots=True)
class GenesisDecisionMemory:
    memory_id: str
    memory_hash: str
    version: str
    run_id: str
    graph_ref: str
    graph_hash: str
    package_ref: str
    resolved_decision_ids: tuple[str, ...]
    ready_decision_ids: tuple[str, ...]
    locked_decision_ids: tuple[str, ...]
    answer_refs: tuple[str, ...]
    final_decision_refs: tuple[str, ...]
    amendment_refs: tuple[str, ...]
    cascade_status: CascadeStatus
    authority_identity: str

    @classmethod
    def compile(cls, *, graph: DecisionGraph, package: GenesisQuestionPackage, answer: HumanAnswer, decision: FinalDecision, amendment: HarnessIRDecisionAmendment, prior_memory: "GenesisDecisionMemory | None" = None) -> "GenesisDecisionMemory":
        resolved = set(prior_memory.resolved_decision_ids if prior_memory else ())
        if decision.decision_node_id in resolved:
            raise GenesisDecisionInvalid("A resolved decision cannot be approved again.")
        resolved.add(decision.decision_node_id)
        all_ids = {node.definition.decision_id for node in graph.nodes}
        ready = tuple(sorted(
            node.definition.decision_id for node in graph.nodes
            if node.definition.decision_id not in resolved and set(node.definition.dependencies) <= resolved
        ))
        locked = tuple(sorted(all_ids - resolved - set(ready)))
        status = CascadeStatus.CASCADE_LOCKED if resolved == all_ids else CascadeStatus.PARTIALLY_RATIFIED
        answers = tuple(sorted((*(prior_memory.answer_refs if prior_memory else ()), answer.answer_id)))
        decisions = tuple(sorted((*(prior_memory.final_decision_refs if prior_memory else ()), decision.final_decision_id)))
        amendments = tuple(sorted((*(prior_memory.amendment_refs if prior_memory else ()), amendment.amendment_id)))
        payload = {
            "amendment_refs": list(amendments), "answer_refs": list(answers),
            "authority_identity": decision.human_id, "cascade_status": status.value,
            "final_decision_refs": list(decisions), "graph_hash": graph.graph_hash,
            "graph_ref": graph.graph_id, "locked_decision_ids": list(locked),
            "package_ref": package.package_id, "ready_decision_ids": list(ready),
            "resolved_decision_ids": sorted(resolved), "run_id": graph.run_id,
            "version": GENESIS_DECISION_VERSION,
        }
        digest = sha256(_canonical_json(payload)).hexdigest()
        return cls(
            memory_id=f"genesis-decision-memory_{digest}", memory_hash=f"sha256:{digest}",
            version=GENESIS_DECISION_VERSION, run_id=graph.run_id,
            graph_ref=graph.graph_id, graph_hash=graph.graph_hash, package_ref=package.package_id,
            resolved_decision_ids=tuple(sorted(resolved)), ready_decision_ids=ready,
            locked_decision_ids=locked, answer_refs=answers,
            final_decision_refs=decisions, amendment_refs=amendments,
            cascade_status=status, authority_identity=decision.human_id,
        )

    def canonical_bytes(self) -> bytes:
        return _canonical_json({
            "amendment_refs": list(self.amendment_refs), "answer_refs": list(self.answer_refs),
            "authority_identity": self.authority_identity, "cascade_status": self.cascade_status.value,
            "final_decision_refs": list(self.final_decision_refs), "graph_hash": self.graph_hash,
            "graph_ref": self.graph_ref, "locked_decision_ids": list(self.locked_decision_ids),
            "memory_hash": self.memory_hash, "memory_id": self.memory_id,
            "package_ref": self.package_ref, "ready_decision_ids": list(self.ready_decision_ids),
            "resolved_decision_ids": list(self.resolved_decision_ids), "run_id": self.run_id,
            "version": self.version,
        })


@dataclass(frozen=True, slots=True)
class GenesisDecisionReceipt:
    receipt_id: str
    receipt_hash: str
    command_id: str
    run_id: str
    answer_id: str
    answer_hash: str
    final_decision_id: str
    final_decision_hash: str
    amendment_id: str
    amendment_hash: str
    memory_id: str
    memory_hash: str
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    outcome: str = "PASS"

    @classmethod
    def create(cls, **values: object) -> "GenesisDecisionReceipt":
        digest = sha256(_canonical_json(values)).hexdigest()
        return cls(**values, receipt_hash=f"sha256:{digest}")


@dataclass(frozen=True, slots=True)
class GenesisDecisionInvalidation:
    invalidation_id: str
    invalidation_hash: str
    command_id: str
    run_id: str
    memory_id: str
    memory_hash: str
    affected_amendment_ids: tuple[str, ...]
    affected_descendant_decision_ids: tuple[str, ...]
    reason: str
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    new_version_required: bool = True

    @classmethod
    def create(cls, **values: object) -> "GenesisDecisionInvalidation":
        payload = {**values, "new_version_required": True}
        digest = sha256(_canonical_json(payload)).hexdigest()
        return cls(**payload, invalidation_hash=f"sha256:{digest}")


def _require_text(values: Mapping[str, object], *keys: str) -> None:
    if any(not isinstance(values.get(key), str) or not str(values[key]).strip() for key in keys):
        raise GenesisDecisionInvalid("Required human decision content is absent.")


def _json_value(value: object) -> object:
    if isinstance(value, Enum): return value.value
    if isinstance(value, datetime): return value.isoformat()
    if isinstance(value, tuple): return [_json_value(item) for item in value]
    if isinstance(value, Mapping): return {str(key): _json_value(item) for key, item in value.items()}
    return value


def _canonical_json(value: object) -> bytes:
    return json.dumps(_json_value(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
