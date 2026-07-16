from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Mapping

from cmf_builder.domain.atomicity import (
    AuthorityStatus,
    DraftHarnessModel,
    KnowledgeStatus,
    ModelStatus,
)
from cmf_builder.domain.evidence_saturation import SaturationEvaluation, SaturationOutcome


GENESIS_QUESTION_VERSION = "1.0.0"
ADVISORY_AUTHORITY_STATEMENT = "ADVISORY_NOT_HUMAN_RATIFICATION"


class GenesisQuestionError(Exception):
    code = "GenesisQuestionError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class DecisionDefinitionInvalid(GenesisQuestionError):
    code = "DecisionDefinitionInvalid"


class RecommendationInvalid(GenesisQuestionError):
    code = "RecommendationInvalid"


class QuestionPackageInvalid(GenesisQuestionError):
    code = "QuestionPackageInvalid"


class DecisionNodeStatus(str, Enum):
    LOCKED = "LOCKED"
    READY = "READY"
    SELECTED = "SELECTED"


@dataclass(frozen=True, slots=True)
class RecommendationAlternative:
    option_id: str
    tradeoffs: tuple[str, ...]
    downstream_consequences: tuple[str, ...]
    risks: tuple[str, ...]

    def validate(self, *, options: tuple[str, ...]) -> None:
        if (
            self.option_id not in options
            or not self.tradeoffs
            or not self.downstream_consequences
            or not self.risks
            or any(not value.strip() for value in (*self.tradeoffs, *self.downstream_consequences, *self.risks))
        ):
            raise RecommendationInvalid("Every viable alternative requires governed tradeoffs, consequences and risks.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "downstream_consequences": list(self.downstream_consequences),
            "option_id": self.option_id,
            "risks": list(self.risks),
            "tradeoffs": list(self.tradeoffs),
        }


@dataclass(frozen=True, slots=True)
class DecisionDefinition:
    decision_id: str
    version: str
    target_profile_applicability: tuple[str, ...]
    priority: int
    question: str
    rationale: str
    required_evidence: tuple[str, ...]
    dependencies: tuple[str, ...]
    options: tuple[str, ...]
    recommended_option: str
    recommendation_policy: str
    authority_owner: str
    affected_ir_paths: tuple[str, ...]
    invalidation_edges: tuple[str, ...]
    completion_rule: str
    definition_hash: str

    @classmethod
    def create(
        cls,
        *,
        decision_id: str,
        target_profile_applicability: tuple[str, ...],
        priority: int,
        question: str,
        rationale: str,
        required_evidence: tuple[str, ...],
        dependencies: tuple[str, ...],
        options: tuple[str, ...],
        recommended_option: str,
        recommendation_policy: str,
        authority_owner: str,
        affected_ir_paths: tuple[str, ...],
        invalidation_edges: tuple[str, ...],
        completion_rule: str,
        version: str = GENESIS_QUESTION_VERSION,
    ) -> "DecisionDefinition":
        payload = {
            "affected_ir_paths": sorted(affected_ir_paths),
            "authority_owner": authority_owner,
            "completion_rule": completion_rule,
            "decision_id": decision_id,
            "dependencies": sorted(dependencies),
            "invalidation_edges": sorted(invalidation_edges),
            "options": list(options),
            "priority": priority,
            "question": question,
            "rationale": rationale,
            "recommendation_policy": recommendation_policy,
            "recommended_option": recommended_option,
            "required_evidence": sorted(required_evidence),
            "target_profile_applicability": sorted(target_profile_applicability),
            "version": version,
        }
        value = cls(
            decision_id=decision_id,
            version=version,
            target_profile_applicability=tuple(sorted(target_profile_applicability)),
            priority=priority,
            question=question,
            rationale=rationale,
            required_evidence=tuple(sorted(required_evidence)),
            dependencies=tuple(sorted(dependencies)),
            options=options,
            recommended_option=recommended_option,
            recommendation_policy=recommendation_policy,
            authority_owner=authority_owner,
            affected_ir_paths=tuple(sorted(affected_ir_paths)),
            invalidation_edges=tuple(sorted(invalidation_edges)),
            completion_rule=completion_rule,
            definition_hash=f"sha256:{sha256(_canonical_json(payload)).hexdigest()}",
        )
        value.validate()
        return value

    def validate(self, *, model: DraftHarnessModel | None = None) -> None:
        texts = (
            self.decision_id,
            self.version,
            self.question,
            self.rationale,
            self.recommended_option,
            self.recommendation_policy,
            self.authority_owner,
            self.completion_rule,
        )
        if (
            any(not value.strip() for value in texts)
            or self.version != GENESIS_QUESTION_VERSION
            or self.priority < 0
            or not self.target_profile_applicability
            or not self.required_evidence
            or len(self.options) < 2
            or len(set(self.options)) != len(self.options)
            or self.recommended_option not in self.options
            or self.authority_owner != "HUMAN"
            or not self.affected_ir_paths
            or not self.invalidation_edges
            or any(not value.strip() for value in (*self.target_profile_applicability, *self.required_evidence, *self.dependencies, *self.options, *self.affected_ir_paths, *self.invalidation_edges))
        ):
            raise DecisionDefinitionInvalid("Decision definition is incomplete or violates human authority.")
        expected = sha256(_canonical_json(self._identity_payload())).hexdigest()
        if self.definition_hash != f"sha256:{expected}":
            raise DecisionDefinitionInvalid("Decision definition hash differs from canonical bytes.")
        if model is not None:
            fields = {field.name: field for field in model.fields}
            for path in self.affected_ir_paths:
                name = path.removeprefix("fields.")
                field = fields.get(name)
                if (
                    field is None
                    or field.authority_status is not AuthorityStatus.UNRATIFIED
                    or field.knowledge_status is not KnowledgeStatus.HYPOTHESIS
                    or field.disposition != "DECISION_REQUIRED"
                ):
                    raise DecisionDefinitionInvalid(
                        "HG-001 forbids a question from targeting absent or already-authoritative meaning.",
                        affected_ir_path=path,
                    )

    def _identity_payload(self) -> dict[str, object]:
        return {
            "affected_ir_paths": list(self.affected_ir_paths),
            "authority_owner": self.authority_owner,
            "completion_rule": self.completion_rule,
            "decision_id": self.decision_id,
            "dependencies": list(self.dependencies),
            "invalidation_edges": list(self.invalidation_edges),
            "options": list(self.options),
            "priority": self.priority,
            "question": self.question,
            "rationale": self.rationale,
            "recommendation_policy": self.recommendation_policy,
            "recommended_option": self.recommended_option,
            "required_evidence": list(self.required_evidence),
            "target_profile_applicability": list(self.target_profile_applicability),
            "version": self.version,
        }

    def canonical_dict(self) -> dict[str, object]:
        return {**self._identity_payload(), "definition_hash": self.definition_hash}


@dataclass(frozen=True, slots=True)
class DecisionNode:
    definition: DecisionDefinition
    status: DecisionNodeStatus
    missing_dependencies: tuple[str, ...]
    missing_evidence: tuple[str, ...]

    def canonical_dict(self) -> dict[str, object]:
        return {
            "definition": self.definition.canonical_dict(),
            "missing_dependencies": list(self.missing_dependencies),
            "missing_evidence": list(self.missing_evidence),
            "status": self.status.value,
        }


@dataclass(frozen=True, slots=True)
class DecisionGraph:
    graph_id: str
    graph_hash: str
    version: str
    run_id: str
    target_profile_id: str
    source_lock_ref: str
    boundary_ref: str
    ratification_ref: str
    model_ref: str
    model_hash: str
    saturation_ref: str
    saturation_hash: str
    nodes: tuple[DecisionNode, ...]
    selected_decision_id: str
    maximum_active_questions: int = 1

    @classmethod
    def compile(
        cls,
        *,
        run_id: str,
        target_profile_id: str,
        source_lock_ref: str,
        boundary_ref: str,
        ratification_ref: str,
        model: DraftHarnessModel,
        saturation: SaturationEvaluation,
        definitions: tuple[DecisionDefinition, ...],
        completed_decision_ids: tuple[str, ...] = (),
        available_evidence_refs: tuple[str, ...] = (),
    ) -> "DecisionGraph":
        if (
            model.status is not ModelStatus.UNRATIFIED_CONSTITUTIONAL_FIELDS
            or saturation.outcome not in {SaturationOutcome.PASS, SaturationOutcome.PASS_WITH_LIMITATIONS}
            or not definitions
            or len({item.decision_id for item in definitions}) != len(definitions)
        ):
            raise DecisionDefinitionInvalid("Genesis requires active saturation and one unratified Draft Harness Model.")
        completed = set(completed_decision_ids)
        evidence = set(available_evidence_refs)
        preliminary: list[DecisionNode] = []
        for definition in sorted(definitions, key=lambda item: (item.priority, item.decision_id)):
            definition.validate(model=model)
            if target_profile_id not in definition.target_profile_applicability and "*" not in definition.target_profile_applicability:
                continue
            missing_dependencies = tuple(sorted(set(definition.dependencies) - completed))
            missing_evidence = tuple(sorted(set(definition.required_evidence) - evidence))
            status = DecisionNodeStatus.READY if not missing_dependencies and not missing_evidence else DecisionNodeStatus.LOCKED
            preliminary.append(DecisionNode(definition, status, missing_dependencies, missing_evidence))
        ready = [item for item in preliminary if item.status is DecisionNodeStatus.READY]
        if not ready:
            raise DecisionDefinitionInvalid("No dependency-ready constitutional question is available.")
        selected_id = ready[0].definition.decision_id
        nodes = tuple(
            DecisionNode(item.definition, DecisionNodeStatus.SELECTED if item.definition.decision_id == selected_id else item.status, item.missing_dependencies, item.missing_evidence)
            for item in preliminary
        )
        base = {
            "boundary_ref": boundary_ref,
            "maximum_active_questions": 1,
            "model_hash": model.model_hash,
            "model_ref": model.model_id,
            "nodes": [item.canonical_dict() for item in nodes],
            "ratification_ref": ratification_ref,
            "run_id": run_id,
            "saturation_hash": saturation.evaluation_hash,
            "saturation_ref": saturation.evaluation_id,
            "selected_decision_id": selected_id,
            "source_lock_ref": source_lock_ref,
            "target_profile_id": target_profile_id,
            "version": GENESIS_QUESTION_VERSION,
        }
        digest = sha256(_canonical_json(base)).hexdigest()
        return cls(
            graph_id=f"decision-graph_{digest}", graph_hash=f"sha256:{digest}",
            version=GENESIS_QUESTION_VERSION, run_id=run_id,
            target_profile_id=target_profile_id, source_lock_ref=source_lock_ref,
            boundary_ref=boundary_ref, ratification_ref=ratification_ref,
            model_ref=model.model_id, model_hash=model.model_hash,
            saturation_ref=saturation.evaluation_id, saturation_hash=saturation.evaluation_hash,
            nodes=nodes, selected_decision_id=selected_id,
        )

    def selected_node(self) -> DecisionNode:
        selected = tuple(item for item in self.nodes if item.status is DecisionNodeStatus.SELECTED)
        if len(selected) != 1 or selected[0].definition.decision_id != self.selected_decision_id:
            raise DecisionDefinitionInvalid("A graph must contain exactly one selected question.")
        return selected[0]

    def canonical_dict(self) -> dict[str, object]:
        return {
            "boundary_ref": self.boundary_ref, "graph_hash": self.graph_hash,
            "graph_id": self.graph_id, "maximum_active_questions": self.maximum_active_questions,
            "model_hash": self.model_hash, "model_ref": self.model_ref,
            "nodes": [item.canonical_dict() for item in self.nodes],
            "ratification_ref": self.ratification_ref, "run_id": self.run_id,
            "saturation_hash": self.saturation_hash, "saturation_ref": self.saturation_ref,
            "selected_decision_id": self.selected_decision_id,
            "source_lock_ref": self.source_lock_ref, "target_profile_id": self.target_profile_id,
            "version": self.version,
        }


@dataclass(frozen=True, slots=True)
class EvidenceBackedRecommendation:
    recommendation_id: str
    recommendation_hash: str
    decision_id: str
    recommended_option: str
    facts: tuple[str, ...]
    inferences: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    alternatives: tuple[RecommendationAlternative, ...]
    authority_statement: str = ADVISORY_AUTHORITY_STATEMENT

    @classmethod
    def create(
        cls, *, definition: DecisionDefinition, facts: tuple[str, ...],
        inferences: tuple[str, ...], evidence_refs: tuple[str, ...],
        alternatives: tuple[RecommendationAlternative, ...],
    ) -> "EvidenceBackedRecommendation":
        base = {
            "alternatives": [item.canonical_dict() for item in alternatives],
            "authority_statement": ADVISORY_AUTHORITY_STATEMENT,
            "decision_id": definition.decision_id, "evidence_refs": sorted(evidence_refs),
            "facts": sorted(facts), "inferences": sorted(inferences),
            "recommended_option": definition.recommended_option,
        }
        digest = sha256(_canonical_json(base)).hexdigest()
        result = cls(
            recommendation_id=f"recommendation_{digest}", recommendation_hash=f"sha256:{digest}",
            decision_id=definition.decision_id, recommended_option=definition.recommended_option,
            facts=tuple(sorted(facts)), inferences=tuple(sorted(inferences)),
            evidence_refs=tuple(sorted(evidence_refs)), alternatives=alternatives,
        )
        result.validate(definition)
        return result

    def validate(self, definition: DecisionDefinition) -> None:
        if (
            self.decision_id != definition.decision_id
            or self.recommended_option != definition.recommended_option
            or not self.facts or not self.inferences or not self.evidence_refs
            or set(definition.required_evidence) - set(self.evidence_refs)
            or {item.option_id for item in self.alternatives} != set(definition.options)
            or self.authority_statement != ADVISORY_AUTHORITY_STATEMENT
        ):
            raise RecommendationInvalid("Recommendation evidence or advisory authority is incomplete.")
        for item in self.alternatives:
            item.validate(options=definition.options)
        base = self._identity_payload()
        digest = sha256(_canonical_json(base)).hexdigest()
        if self.recommendation_id != f"recommendation_{digest}" or self.recommendation_hash != f"sha256:{digest}":
            raise RecommendationInvalid("Recommendation identity differs from governed content.")

    def _identity_payload(self) -> dict[str, object]:
        return {
            "alternatives": [item.canonical_dict() for item in self.alternatives],
            "authority_statement": self.authority_statement,
            "decision_id": self.decision_id, "evidence_refs": list(self.evidence_refs),
            "facts": list(self.facts), "inferences": list(self.inferences),
            "recommended_option": self.recommended_option,
        }

    def canonical_dict(self) -> dict[str, object]:
        return {**self._identity_payload(), "recommendation_hash": self.recommendation_hash, "recommendation_id": self.recommendation_id}


@dataclass(frozen=True, slots=True)
class GenesisQuestionPackage:
    package_id: str
    package_hash: str
    version: str
    run_id: str
    graph_ref: str
    graph_hash: str
    selected_decision_id: str
    question: str
    recommendation: EvidenceBackedRecommendation
    locked_decision_ids: tuple[str, ...]
    authority_identity: str
    production_eligible: bool = False
    certified: bool = False

    @classmethod
    def compile(cls, *, graph: DecisionGraph, recommendation: EvidenceBackedRecommendation, authority_identity: str) -> "GenesisQuestionPackage":
        node = graph.selected_node()
        recommendation.validate(node.definition)
        if not authority_identity.strip():
            raise QuestionPackageInvalid("Question selection requires exact code authority.")
        base = {
            "authority_identity": authority_identity, "certified": False,
            "graph_hash": graph.graph_hash, "graph_ref": graph.graph_id,
            "locked_decision_ids": sorted(item.definition.decision_id for item in graph.nodes if item.status is DecisionNodeStatus.LOCKED),
            "production_eligible": False, "question": node.definition.question,
            "recommendation": recommendation.canonical_dict(), "run_id": graph.run_id,
            "selected_decision_id": graph.selected_decision_id, "version": GENESIS_QUESTION_VERSION,
        }
        digest = sha256(_canonical_json(base)).hexdigest()
        return cls(
            package_id=f"genesis-question_{digest}", package_hash=f"sha256:{digest}",
            version=GENESIS_QUESTION_VERSION, run_id=graph.run_id, graph_ref=graph.graph_id,
            graph_hash=graph.graph_hash, selected_decision_id=graph.selected_decision_id,
            question=node.definition.question, recommendation=recommendation,
            locked_decision_ids=tuple(base["locked_decision_ids"]), authority_identity=authority_identity,
        )

    def canonical_bytes(self) -> bytes:
        return _canonical_json({
            "authority_identity": self.authority_identity, "certified": self.certified,
            "graph_hash": self.graph_hash, "graph_ref": self.graph_ref,
            "locked_decision_ids": list(self.locked_decision_ids), "package_hash": self.package_hash,
            "package_id": self.package_id, "production_eligible": self.production_eligible,
            "question": self.question, "recommendation": self.recommendation.canonical_dict(),
            "run_id": self.run_id, "selected_decision_id": self.selected_decision_id,
            "version": self.version,
        })

    def validate(self, graph: DecisionGraph) -> None:
        selected = graph.selected_node().definition
        self.recommendation.validate(selected)
        if (
            self.run_id != graph.run_id or self.graph_ref != graph.graph_id
            or self.graph_hash != graph.graph_hash
            or self.selected_decision_id != graph.selected_decision_id
            or self.question != selected.question
            or self.locked_decision_ids != tuple(sorted(
                item.definition.decision_id for item in graph.nodes
                if item.status is DecisionNodeStatus.LOCKED
            ))
            or not self.authority_identity.strip()
            or self.production_eligible or self.certified
        ):
            raise QuestionPackageInvalid("Question package differs from its governed graph.")
        base = {
            "authority_identity": self.authority_identity, "certified": False,
            "graph_hash": self.graph_hash, "graph_ref": self.graph_ref,
            "locked_decision_ids": list(self.locked_decision_ids),
            "production_eligible": False, "question": self.question,
            "recommendation": self.recommendation.canonical_dict(), "run_id": self.run_id,
            "selected_decision_id": self.selected_decision_id, "version": self.version,
        }
        digest = sha256(_canonical_json(base)).hexdigest()
        if self.package_id != f"genesis-question_{digest}" or self.package_hash != f"sha256:{digest}":
            raise QuestionPackageInvalid("Question package identity differs from canonical bytes.")


@dataclass(frozen=True, slots=True)
class GenesisQuestionReceipt:
    receipt_id: str
    receipt_hash: str
    command_id: str
    run_id: str
    graph_id: str
    graph_hash: str
    package_id: str
    package_hash: str
    selected_decision_id: str
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    outcome: str = "PASS"

    @classmethod
    def create(cls, **values: object) -> "GenesisQuestionReceipt":
        payload = dict(values)
        digest = sha256(_canonical_json(payload)).hexdigest()
        return cls(**payload, receipt_hash=f"sha256:{digest}")

    def validate(self, graph: DecisionGraph, package: GenesisQuestionPackage) -> None:
        if (
            self.run_id != graph.run_id or self.graph_id != graph.graph_id
            or self.graph_hash != graph.graph_hash
            or self.package_id != package.package_id or self.package_hash != package.package_hash
            or self.selected_decision_id != graph.selected_decision_id
            or self.authority_identity != package.authority_identity
            or len(self.event_ids) != 1 or self.stream_version <= 0 or self.outcome != "PASS"
        ):
            raise QuestionPackageInvalid("Genesis receipt does not prove this graph and package.")
        payload = {
            "receipt_id": self.receipt_id, "command_id": self.command_id,
            "run_id": self.run_id, "graph_id": self.graph_id, "graph_hash": self.graph_hash,
            "package_id": self.package_id, "package_hash": self.package_hash,
            "selected_decision_id": self.selected_decision_id,
            "authority_identity": self.authority_identity,
            "event_ids": self.event_ids, "stream_version": self.stream_version,
            "outcome": self.outcome,
        }
        if self.receipt_hash != f"sha256:{sha256(_canonical_json(payload)).hexdigest()}":
            raise QuestionPackageInvalid("Genesis receipt hash differs from canonical bytes.")


@dataclass(frozen=True, slots=True)
class GenesisQuestionInvalidation:
    invalidation_id: str
    invalidation_hash: str
    command_id: str
    run_id: str
    package_id: str
    package_hash: str
    reason: str
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    new_version_required: bool = True

    @classmethod
    def create(cls, **values: object) -> "GenesisQuestionInvalidation":
        payload = {**values, "new_version_required": True}
        digest = sha256(_canonical_json(payload)).hexdigest()
        return cls(**payload, invalidation_hash=f"sha256:{digest}")

    def validate(self, package: GenesisQuestionPackage) -> None:
        if (
            self.run_id != package.run_id or self.package_id != package.package_id
            or self.package_hash != package.package_hash or not self.reason.strip()
            or self.authority_identity != package.authority_identity
            or len(self.event_ids) != 1 or self.stream_version <= 0
            or not self.new_version_required
        ):
            raise QuestionPackageInvalid("Invalidation does not target the active immutable question package.")
        payload = {
            "invalidation_id": self.invalidation_id, "command_id": self.command_id,
            "run_id": self.run_id, "package_id": self.package_id,
            "package_hash": self.package_hash, "reason": self.reason,
            "authority_identity": self.authority_identity, "event_ids": self.event_ids,
            "stream_version": self.stream_version, "new_version_required": True,
        }
        if self.invalidation_hash != f"sha256:{sha256(_canonical_json(payload)).hexdigest()}":
            raise QuestionPackageInvalid("Invalidation hash differs from canonical bytes.")


def _json_value(value: object) -> object:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    return value


def _canonical_json(value: object) -> bytes:
    return json.dumps(_json_value(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
