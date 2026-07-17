"""Evidence-first provisional grammar induction for ST-02.03."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Sequence

from cmf_builder.visual.grammar_contracts import (
    AtomicGrammarCommitRejected,
    DEVELOPMENT_MODE,
    GrammarAuthorityRejected,
    GrammarInductionPolicy,
    GrammarInductionReceipt,
    GrammarInductionResult,
    GrammarMotif,
    GraphEvidenceInvalid,
    InsufficientGraphSupport,
    KnowledgePromotionRejected,
    GrammarMaturity,
    ProjectionMode,
    ProvisionalGrammar,
    ProvisionalMeaningHypothesis,
    RichObservationReference,
    SourceGraphReference,
    STORY_ID,
)
from cmf_builder.visual.graph_contracts import SubstrateGraph
from cmf_builder.visual.ontology import (
    KnowledgeStatus,
    ProvenanceReference,
    canonical_sha256,
    require_identifier,
)


def _graph_core(graph: SubstrateGraph) -> dict[str, object]:
    return {
        "graph_kind": graph.graph_kind.value,
        "substrate": graph.substrate.value,
        "specimen_id": graph.specimen_id,
        "specimen_artifact_sha256": graph.specimen_artifact_sha256,
        "plan_sha256": graph.plan_sha256,
        "nodes": [item.as_dict() for item in graph.nodes],
        "edges": [item.as_dict() for item in graph.edges],
    }


def _observation_core(observation) -> dict[str, object]:
    return {
        "specimen_id": observation.specimen_id,
        "component_id": observation.component_id,
        "category_id": observation.category_id,
        "ontology_term_id": observation.ontology_term_id,
        "geometry": observation.geometry.as_dict(),
        "observation_status": observation.observation_status.value,
        "governed_status": observation.governed_status.value,
        "knowledge_status": observation.knowledge_status.value,
        "source": observation.source.as_dict(),
        "provenance": [item.as_dict() for item in observation.provenance],
        "uncertainty": observation.uncertainty.as_dict(),
        "applicability": observation.applicability.as_dict(),
        "structural_fields": [list(item) for item in observation.structural_fields],
    }


def _edge_core(edge) -> dict[str, object]:
    return {
        "graph_kind": edge.graph_kind.value,
        "relation": edge.relation,
        "from_node_id": edge.from_node_id,
        "to_node_id": edge.to_node_id,
        "evidence_observation_ids": list(edge.evidence_observation_ids),
        "source": edge.source.as_dict(),
        "observation_status": edge.observation_status.value,
        "knowledge_status": edge.knowledge_status.value,
        "origin": edge.origin.value,
        "provenance": [item.as_dict() for item in edge.provenance],
        "uncertainty": edge.uncertainty.as_dict(),
        "applicability": edge.applicability.as_dict(),
    }


def _graph_source_content_sha256(graph: SubstrateGraph) -> str:
    content_hashes = {
        node.observation.source.content_sha256 for node in graph.nodes
    } | {edge.source.content_sha256 for edge in graph.edges}
    if len(content_hashes) != 1:
        raise GraphEvidenceInvalid(
            "a source graph must bind exactly one governed source content identity",
            graph_id=graph.graph_id,
        )
    return next(iter(content_hashes))


def _validate_graph(graph: SubstrateGraph, category_id: str) -> None:
    expected_hash = canonical_sha256(_graph_core(graph))
    if graph.artifact_sha256 != expected_hash or graph.graph_id != (
        f"ST-02.02:{graph.graph_kind.value}:{expected_hash}"
    ):
        raise GraphEvidenceInvalid(
            "source graph identity or artifact hash is invalid",
            graph_id=graph.graph_id,
        )
    node_ids = tuple(node.node_id for node in graph.nodes)
    if len(node_ids) != len(set(node_ids)):
        raise GraphEvidenceInvalid("source graph node identities must be unique")
    nodes = {node.node_id: node for node in graph.nodes}
    for node in graph.nodes:
        observation = node.observation
        if node.node_id != observation.observation_id or observation.observation_id != (
            canonical_sha256(_observation_core(observation))
        ):
            raise GraphEvidenceInvalid(
                "source graph node identity is not canonically bound to its observation"
            )
        if observation.specimen_id != graph.specimen_id:
            raise GraphEvidenceInvalid(
                "source graph observation is cross-wired to another specimen"
            )
        for variable in node.composition_variables:
            if variable.observation_id != observation.observation_id:
                raise GraphEvidenceInvalid(
                    "composition variable is cross-wired to another observation"
                )
            if not set(variable.provenance).issubset(observation.provenance):
                raise GraphEvidenceInvalid(
                    "composition variable provenance is detached from its observation"
                )
    if any(node.observation.category_id != category_id for node in graph.nodes):
        raise GraphEvidenceInvalid(
            "cross-category graph flattening is prohibited",
            graph_id=graph.graph_id,
        )
    edge_ids = tuple(edge.edge_id for edge in graph.edges)
    if len(edge_ids) != len(set(edge_ids)):
        raise GraphEvidenceInvalid("source graph edge identities must be unique")
    for edge in graph.edges:
        if edge.graph_kind is not graph.graph_kind:
            raise GraphEvidenceInvalid(
                "source edge graph kind does not match its containing graph"
            )
        if edge.from_node_id not in nodes or edge.to_node_id not in nodes:
            raise GraphEvidenceInvalid("source graph contains a dangling edge")
        if not set(edge.evidence_observation_ids).issubset(nodes):
            raise GraphEvidenceInvalid(
                "source graph edge evidence is not traceable to its rich observations"
            )
        if not {edge.from_node_id, edge.to_node_id}.issubset(
            edge.evidence_observation_ids
        ):
            raise GraphEvidenceInvalid(
                "source graph edge evidence must include both endpoint observations"
            )
        evidence_observations = tuple(
            nodes[observation_id].observation
            for observation_id in edge.evidence_observation_ids
        )
        if any(observation.source != edge.source for observation in evidence_observations):
            raise GraphEvidenceInvalid(
                "source graph edge is cross-wired to unrelated observation source content"
            )
        required_provenance = {
            reference
            for observation in evidence_observations
            for reference in observation.provenance
        }
        if not required_provenance.issubset(edge.provenance):
            raise GraphEvidenceInvalid(
                "source graph edge provenance is detached from its observations"
            )
        if edge.edge_id != canonical_sha256(_edge_core(edge)):
            raise GraphEvidenceInvalid(
                "source graph edge identity is not canonically bound to its payload"
            )
    _graph_source_content_sha256(graph)


def _source_graph_reference(graph: SubstrateGraph) -> SourceGraphReference:
    observations = tuple(
        RichObservationReference(
            observation_id=node.observation.observation_id,
            component_id=node.observation.component_id,
            ontology_term_id=node.observation.ontology_term_id,
            category_id=node.observation.category_id,
            source=node.observation.source,
            provenance=node.observation.provenance,
            uncertainty=node.observation.uncertainty,
            applicability=node.observation.applicability,
            observation_status=node.observation.observation_status.value,
            knowledge_status=node.observation.knowledge_status.value,
            geometry_sha256=node.observation.geometry.geometry_sha256,
        )
        for node in sorted(graph.nodes, key=lambda item: item.node_id)
    )
    return SourceGraphReference(
        graph_id=graph.graph_id,
        artifact_sha256=graph.artifact_sha256,
        graph_kind=graph.graph_kind,
        substrate=graph.substrate,
        specimen_id=graph.specimen_id,
        specimen_artifact_sha256=graph.specimen_artifact_sha256,
        source_content_sha256=_graph_source_content_sha256(graph),
        plan_sha256=graph.plan_sha256,
        observations=observations,
        edge_ids=tuple(sorted(edge.edge_id for edge in graph.edges)),
    )


@dataclass(slots=True)
class _MotifAccumulator:
    graph_ids: set[str]
    edge_ids: set[str]
    observation_ids: set[str]
    source_content_hashes: set[str]
    provenance: set[ProvenanceReference]


def _motifs(
    graphs: tuple[SubstrateGraph, ...], policy: GrammarInductionPolicy
) -> tuple[GrammarMotif, ...]:
    accumulators: dict[tuple[str, str, str, str, str], _MotifAccumulator] = {}
    for graph in graphs:
        nodes = {node.node_id: node.observation for node in graph.nodes}
        for edge in graph.edges:
            source = nodes[edge.from_node_id]
            target = nodes[edge.to_node_id]
            signature = (
                graph.substrate.value,
                graph.graph_kind.value,
                edge.relation,
                source.ontology_term_id,
                target.ontology_term_id,
            )
            accumulator = accumulators.setdefault(
                signature,
                _MotifAccumulator(set(), set(), set(), set(), set()),
            )
            accumulator.graph_ids.add(graph.graph_id)
            accumulator.edge_ids.add(edge.edge_id)
            accumulator.observation_ids.update(edge.evidence_observation_ids)
            accumulator.source_content_hashes.add(
                _graph_source_content_sha256(graph)
            )
            accumulator.provenance.update(edge.provenance)

    motifs: list[GrammarMotif] = []
    for signature, support in sorted(accumulators.items()):
        if len(support.source_content_hashes) < policy.minimum_distinct_specimen_support:
            continue
        substrate, graph_kind, relation, source_term, target_term = signature
        payload = {
            "substrate": substrate,
            "graph_kind": graph_kind,
            "relation": relation,
            "from_ontology_term_id": source_term,
            "to_ontology_term_id": target_term,
            "distinct_specimen_support": len(support.source_content_hashes),
            "source_graph_ids": sorted(support.graph_ids),
            "source_edge_ids": sorted(support.edge_ids),
            "source_observation_ids": sorted(support.observation_ids),
            "provenance": [
                item.as_dict()
                for item in sorted(
                    support.provenance,
                    key=lambda item: (
                        item.artifact_id,
                        item.relationship,
                        item.artifact_sha256,
                    ),
                )
            ],
            "knowledge_status": KnowledgeStatus.DETERMINISTIC_DERIVATION.value,
        }
        motifs.append(
            GrammarMotif(
                motif_id=canonical_sha256(payload),
                substrate=graphs[0].substrate.__class__(substrate),
                graph_kind=graphs[0].graph_kind.__class__(graph_kind),
                relation=relation,
                from_ontology_term_id=source_term,
                to_ontology_term_id=target_term,
                distinct_specimen_support=len(support.source_content_hashes),
                source_graph_ids=tuple(sorted(support.graph_ids)),
                source_edge_ids=tuple(sorted(support.edge_ids)),
                source_observation_ids=tuple(sorted(support.observation_ids)),
                provenance=tuple(
                    sorted(
                        support.provenance,
                        key=lambda item: (
                            item.artifact_id,
                            item.relationship,
                            item.artifact_sha256,
                        ),
                    )
                ),
            )
        )
    if not motifs:
        raise InsufficientGraphSupport(
            "no substrate-specific relation has the required distinct specimen support"
        )
    return tuple(motifs)


def _validate_hypotheses(
    hypotheses: Sequence[ProvisionalMeaningHypothesis],
    graphs: tuple[SubstrateGraph, ...],
    policy: GrammarInductionPolicy,
) -> tuple[ProvisionalMeaningHypothesis, ...]:
    graph_ids = {graph.graph_id for graph in graphs}
    graph_by_id = {graph.graph_id: graph for graph in graphs}
    edge_owners = {
        edge.edge_id: (graph.graph_id, edge)
        for graph in graphs
        for edge in graph.edges
    }
    observation_ids = {node.node_id for graph in graphs for node in graph.nodes}
    validated: list[ProvisionalMeaningHypothesis] = []
    for hypothesis in hypotheses:
        if hypothesis.hypothesis_id != canonical_sha256(
            hypothesis.identity_payload()
        ):
            raise KnowledgePromotionRejected(
                "hypothesis identity does not match its canonical governed payload"
            )
        if ProvisionalMeaningHypothesis.contains_unauthorized_claim(
            hypothesis.statement
        ):
            raise KnowledgePromotionRejected(
                "provisional hypothesis contains an unauthorized authority claim"
            )
        if hypothesis.proposer_authority_ref not in policy.allowed_hypothesis_proposers:
            raise GrammarAuthorityRejected(
                "hypothesis proposer is outside the governed authority set",
                proposer=hypothesis.proposer_authority_ref,
            )
        if hypothesis.knowledge_status is not KnowledgeStatus.HYPOTHESIS:
            raise KnowledgePromotionRejected(
                "meaning must remain a visibly provisional hypothesis"
            )
        if not set(hypothesis.source_graph_ids).issubset(graph_ids):
            raise GraphEvidenceInvalid("hypothesis references an unknown source graph")
        if not set(hypothesis.source_edge_ids).issubset(edge_owners):
            raise GraphEvidenceInvalid("hypothesis references an unknown source edge")
        if not set(hypothesis.source_observation_ids).issubset(observation_ids):
            raise GraphEvidenceInvalid(
                "hypothesis references an unknown rich source observation"
            )
        selected_graph_ids = set(hypothesis.source_graph_ids)
        selected_edges = tuple(
            edge_owners[edge_id] for edge_id in hypothesis.source_edge_ids
        )
        if {graph_id for graph_id, _ in selected_edges} != selected_graph_ids:
            raise GraphEvidenceInvalid(
                "hypothesis cross-wires source graph and edge lineage"
            )
        expected_observation_ids = {
            observation_id
            for _, edge in selected_edges
            for observation_id in edge.evidence_observation_ids
        }
        if set(hypothesis.source_observation_ids) != expected_observation_ids:
            raise GraphEvidenceInvalid(
                "hypothesis cross-wires edge and observation lineage"
            )
        for graph_id, edge in selected_edges:
            graph = graph_by_id[graph_id]
            graph_observations = {
                node.node_id: node.observation for node in graph.nodes
            }
            required_provenance = {
                reference
                for observation_id in edge.evidence_observation_ids
                for reference in graph_observations[observation_id].provenance
            }
            if not required_provenance.issubset(edge.provenance):
                raise GraphEvidenceInvalid(
                    "hypothesis source edge has detached provenance lineage"
                )
        validated.append(hypothesis)
    ids = tuple(item.hypothesis_id for item in validated)
    if len(ids) != len(set(ids)):
        raise KnowledgePromotionRejected("duplicate hypotheses are prohibited")
    return tuple(sorted(validated, key=lambda item: item.hypothesis_id))


def induce_provisional_grammar(
    *,
    run_id: str,
    graphs: Sequence[SubstrateGraph],
    policy: GrammarInductionPolicy,
    hypotheses: Sequence[ProvisionalMeaningHypothesis] = (),
) -> GrammarInductionResult:
    require_identifier(run_id, "grammar_induction_run_id")
    ordered_graphs = tuple(sorted(graphs, key=lambda item: item.graph_id))
    if not ordered_graphs:
        raise InsufficientGraphSupport("at least one graph is required")
    graph_ids = tuple(graph.graph_id for graph in ordered_graphs)
    if len(graph_ids) != len(set(graph_ids)):
        raise GraphEvidenceInvalid("source graph identities must be unique")
    for graph in ordered_graphs:
        _validate_graph(graph, policy.category_id)
    content_bindings: dict[str, tuple[str, str]] = {}
    artifact_bindings: dict[str, str] = {}
    for graph in ordered_graphs:
        content_sha256 = _graph_source_content_sha256(graph)
        specimen_binding = (graph.specimen_id, graph.specimen_artifact_sha256)
        previous_binding = content_bindings.setdefault(content_sha256, specimen_binding)
        if previous_binding != specimen_binding:
            raise GraphEvidenceInvalid(
                "the same governed source content cannot be relabelled as distinct specimen support"
            )
        previous_content = artifact_bindings.setdefault(
            graph.specimen_artifact_sha256, content_sha256
        )
        if previous_content != content_sha256:
            raise GraphEvidenceInvalid(
                "one predecessor specimen artifact cannot bind conflicting source content"
            )
    distinct_specimens = set(content_bindings)
    if len(distinct_specimens) < policy.minimum_distinct_specimen_support:
        raise InsufficientGraphSupport(
            "declared graph set lacks cross-specimen support"
        )

    motifs = _motifs(ordered_graphs, policy)
    validated_hypotheses = _validate_hypotheses(hypotheses, ordered_graphs, policy)
    source_graphs = tuple(_source_graph_reference(graph) for graph in ordered_graphs)
    series_id = canonical_sha256(
        {
            "policy_id": policy.policy_id,
            "category_id": policy.category_id,
            "projection_mode": policy.projection_mode.value,
        }
    )
    grammar_core = {
        "series_id": series_id,
        "category_id": policy.category_id,
        "policy_sha256": policy.policy_sha256,
        "source_graphs": [item.as_dict() for item in source_graphs],
        "motifs": [item.as_dict() for item in motifs],
        "hypotheses": [item.as_dict() for item in validated_hypotheses],
        "induction_authority_ref": policy.induction_authority_ref,
        "maturity": "PROVISIONAL",
        "projection_mode": policy.projection_mode.value,
        "evidence_gate_status": "EVIDENCE_PENDING",
        "production_ready": False,
        "certified": False,
    }
    artifact_sha256 = canonical_sha256(grammar_core)
    grammar = ProvisionalGrammar(
        grammar_id=f"ST-02.03:ProvisionalGrammar:{artifact_sha256}",
        series_id=series_id,
        version=f"0.0.0-development+{artifact_sha256[:16]}",
        category_id=policy.category_id,
        policy_sha256=policy.policy_sha256,
        source_graphs=source_graphs,
        motifs=motifs,
        hypotheses=validated_hypotheses,
        induction_authority_ref=policy.induction_authority_ref,
        artifact_sha256=artifact_sha256,
    )
    provenance = tuple(
        sorted(
            {
                reference
                for graph in ordered_graphs
                for node in graph.nodes
                for reference in node.observation.provenance
            },
            key=lambda item: (
                item.artifact_id,
                item.relationship,
                item.artifact_sha256,
            ),
        )
    )
    receipt = GrammarInductionReceipt(
        receipt_id="PENDING_CANONICAL_BINDING",
        run_id=run_id,
        grammar_id=grammar.grammar_id,
        grammar_version=grammar.version,
        grammar_artifact_sha256=artifact_sha256,
        policy_sha256=policy.policy_sha256,
        authority_identity=policy.induction_authority_ref,
        source_graph_count=len(source_graphs),
        motif_count=len(motifs),
        hypothesis_count=len(validated_hypotheses),
        provenance=provenance,
    )
    receipt = replace(
        receipt,
        receipt_id=_expected_receipt_id(receipt),
    )
    return GrammarInductionResult(grammar=grammar, receipt=receipt)


def _grammar_core_from_artifact(grammar: ProvisionalGrammar) -> dict[str, object]:
    return {
        "series_id": grammar.series_id,
        "category_id": grammar.category_id,
        "policy_sha256": grammar.policy_sha256,
        "source_graphs": [item.as_dict() for item in grammar.source_graphs],
        "motifs": [item.as_dict() for item in grammar.motifs],
        "hypotheses": [item.as_dict() for item in grammar.hypotheses],
        "induction_authority_ref": grammar.induction_authority_ref,
        "maturity": grammar.maturity.value,
        "projection_mode": grammar.projection_mode.value,
        "evidence_gate_status": grammar.evidence_gate_status,
        "production_ready": grammar.production_ready,
        "certified": grammar.certified,
    }


def _motif_core(motif: GrammarMotif) -> dict[str, object]:
    payload = motif.as_dict()
    payload.pop("motif_id")
    return payload


def _receipt_binding_core(receipt: GrammarInductionReceipt) -> dict[str, object]:
    payload = receipt.as_dict()
    payload.pop("receipt_id")
    return payload


def _expected_receipt_id(receipt: GrammarInductionReceipt) -> str:
    return f"ST-02.03:OfflineInduction:{canonical_sha256(_receipt_binding_core(receipt))}"


def _validate_commit_result(result: GrammarInductionResult) -> None:
    grammar = result.grammar
    receipt = result.receipt
    if (
        grammar.maturity is not GrammarMaturity.PROVISIONAL
        or grammar.projection_mode is not ProjectionMode.SUBSTRATE_SPECIFIC
        or grammar.evidence_gate_status != "EVIDENCE_PENDING"
        or grammar.production_ready
        or grammar.certified
    ):
        raise AtomicGrammarCommitRejected(
            "provisional grammar invariant flags are invalid"
        )
    expected_artifact_sha256 = canonical_sha256(_grammar_core_from_artifact(grammar))
    if grammar.artifact_sha256 != expected_artifact_sha256:
        raise AtomicGrammarCommitRejected(
            "grammar artifact hash does not match its canonical payload"
        )
    if grammar.grammar_id != f"ST-02.03:ProvisionalGrammar:{expected_artifact_sha256}":
        raise AtomicGrammarCommitRejected(
            "grammar identity does not match its canonical payload"
        )
    if grammar.version != f"0.0.0-development+{expected_artifact_sha256[:16]}":
        raise AtomicGrammarCommitRejected(
            "grammar version does not match its canonical payload"
        )
    source_graph_by_id = {item.graph_id: item for item in grammar.source_graphs}
    if len(source_graph_by_id) != len(grammar.source_graphs):
        raise AtomicGrammarCommitRejected(
            "grammar source graph identities must be unique"
        )
    for source_graph in grammar.source_graphs:
        observation_content_hashes = {
            observation.source.content_sha256
            for observation in source_graph.observations
        }
        if observation_content_hashes != {source_graph.source_content_sha256}:
            raise AtomicGrammarCommitRejected(
                "grammar source graph is not bound to one exact source content hash"
            )
    for motif in grammar.motifs:
        if motif.motif_id != canonical_sha256(_motif_core(motif)):
            raise AtomicGrammarCommitRejected(
                "grammar motif identity does not match its canonical payload"
            )
        if motif.knowledge_status is not KnowledgeStatus.DETERMINISTIC_DERIVATION:
            raise AtomicGrammarCommitRejected(
                "grammar motif knowledge status is not a deterministic derivation"
            )
        try:
            supporting_graphs = tuple(
                source_graph_by_id[graph_id] for graph_id in motif.source_graph_ids
            )
        except KeyError as error:
            raise AtomicGrammarCommitRejected(
                "grammar motif references an unknown source graph"
            ) from error
        if motif.distinct_specimen_support != len(
            {item.source_content_sha256 for item in supporting_graphs}
        ):
            raise AtomicGrammarCommitRejected(
                "grammar motif support count is not bound to distinct source content"
            )
        known_edges = {edge_id for item in supporting_graphs for edge_id in item.edge_ids}
        known_observations = {
            observation.observation_id
            for item in supporting_graphs
            for observation in item.observations
        }
        if not set(motif.source_edge_ids).issubset(known_edges) or not set(
            motif.source_observation_ids
        ).issubset(known_observations):
            raise AtomicGrammarCommitRejected(
                "grammar motif lineage is not bound to its source graphs"
            )
    for hypothesis in grammar.hypotheses:
        if (
            hypothesis.hypothesis_id != canonical_sha256(hypothesis.identity_payload())
            or hypothesis.knowledge_status is not KnowledgeStatus.HYPOTHESIS
            or hypothesis.maturity is not GrammarMaturity.PROVISIONAL
        ):
            raise AtomicGrammarCommitRejected(
                "grammar hypothesis identity or provisional invariants are invalid"
            )
    expected_provenance = tuple(
        sorted(
            {
                reference
                for source_graph in grammar.source_graphs
                for observation in source_graph.observations
                for reference in observation.provenance
            },
            key=lambda item: (
                item.artifact_id,
                item.relationship,
                item.artifact_sha256,
            ),
        )
    )
    receipt_matches = (
        receipt.story_id == STORY_ID
        and receipt.development_mode == DEVELOPMENT_MODE
        and receipt.event_name == "ST-02.03:OutcomeVerified"
        and receipt.grammar_id == grammar.grammar_id
        and receipt.grammar_version == grammar.version
        and receipt.grammar_artifact_sha256 == grammar.artifact_sha256
        and receipt.policy_sha256 == grammar.policy_sha256
        and receipt.authority_identity == grammar.induction_authority_ref
        and receipt.source_graph_count == len(grammar.source_graphs)
        and receipt.motif_count == len(grammar.motifs)
        and receipt.hypothesis_count == len(grammar.hypotheses)
        and receipt.provenance == expected_provenance
        and receipt.outcome == "OUTCOME_VERIFIED"
        and receipt.failure_context == "NONE"
        and receipt.receipt_id == _expected_receipt_id(receipt)
    )
    if not receipt_matches:
        raise AtomicGrammarCommitRejected(
            "grammar induction receipt is not exactly bound to the canonical grammar"
        )


class InMemoryProvisionalGrammarWorkspace:
    """Small atomic workspace used to prove authority, rollback, and immutability."""

    def __init__(self) -> None:
        self._artifacts: dict[str, ProvisionalGrammar] = {}
        self._results: dict[str, GrammarInductionResult] = {}
        self._active_by_series: dict[str, str] = {}

    def commit(
        self,
        result: GrammarInductionResult,
        *,
        actor_authority_ref: str,
        expected_active_grammar_id: str | None,
        inject_failure: bool = False,
    ) -> ProvisionalGrammar:
        grammar = result.grammar
        if actor_authority_ref != grammar.induction_authority_ref:
            raise GrammarAuthorityRejected(
                "only the declared induction authority may commit provisional grammar"
            )
        _validate_commit_result(result)
        current = self._active_by_series.get(grammar.series_id)
        if current == grammar.grammar_id:
            existing_result = self._results[grammar.grammar_id]
            if existing_result != result:
                raise AtomicGrammarCommitRejected(
                    "same grammar identity was repeated with a different result or receipt payload"
                )
            return existing_result.grammar
        if current != expected_active_grammar_id:
            raise AtomicGrammarCommitRejected(
                "active grammar changed since the caller's governed expectation"
            )
        staged_artifacts = dict(self._artifacts)
        staged_results = dict(self._results)
        staged_active = dict(self._active_by_series)
        existing = staged_artifacts.get(grammar.grammar_id)
        if existing is not None and existing != grammar:
            raise AtomicGrammarCommitRejected(
                "immutable grammar identity conflicts with existing bytes"
            )
        existing_result = staged_results.get(grammar.grammar_id)
        if existing_result is not None and existing_result != result:
            raise AtomicGrammarCommitRejected(
                "immutable grammar identity conflicts with an existing receipt binding"
            )
        staged_artifacts[grammar.grammar_id] = grammar
        staged_results[grammar.grammar_id] = result
        staged_active[grammar.series_id] = grammar.grammar_id
        if inject_failure:
            raise AtomicGrammarCommitRejected(
                "injected failure before atomic grammar commit"
            )
        self._artifacts = staged_artifacts
        self._results = staged_results
        self._active_by_series = staged_active
        return grammar

    def rollback_to(
        self,
        *,
        series_id: str,
        grammar_id: str,
        actor_authority_ref: str,
    ) -> ProvisionalGrammar:
        grammar = self._artifacts.get(grammar_id)
        if grammar is None or grammar.series_id != series_id:
            raise AtomicGrammarCommitRejected(
                "rollback target is not an immutable grammar in this series"
            )
        if actor_authority_ref != grammar.induction_authority_ref:
            raise GrammarAuthorityRejected(
                "only the declared induction authority may roll back grammar"
            )
        staged_active = dict(self._active_by_series)
        staged_active[series_id] = grammar_id
        self._active_by_series = staged_active
        return grammar

    def active(self, series_id: str) -> ProvisionalGrammar | None:
        grammar_id = self._active_by_series.get(series_id)
        return None if grammar_id is None else self._artifacts[grammar_id]

    def history(self, series_id: str) -> tuple[ProvisionalGrammar, ...]:
        return tuple(
            sorted(
                (
                    grammar
                    for grammar in self._artifacts.values()
                    if grammar.series_id == series_id
                ),
                key=lambda grammar: grammar.grammar_id,
            )
        )
