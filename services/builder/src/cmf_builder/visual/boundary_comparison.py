"""Evidence-bound atomic-product comparison compiler for ST-02.04."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from typing import Sequence

from cmf_builder.application.authority import Action, AuthorityService

from cmf_builder.visual.atomicity_contracts import (
    AtomicityAuthorityRejected,
    AtomicityCommitRejected,
    AtomicityComparisonPacket,
    AtomicityComparisonReceipt,
    AtomicityComparisonResult,
    AtomicityStatus,
    AUTHORITY_CLAIM_POLICY_ID,
    AUTHORITY_CLAIM_POLICY_SHA256,
    AUTHORITY_CLAIM_POLICY_VERSION,
    AlternativesIncomplete,
    BoundaryCandidate,
    BoundaryEvidenceInvalid,
    BoundaryOptionKind,
    ComparisonDimension,
    EvidenceStatus,
    GrammarEvidenceReference,
    RecommendationDisposition,
    RiskDirection,
    RiskDomain,
    RiskSeverity,
    UnsupportedCertaintyRejected,
    validate_identifier_fields,
    validate_provisional_claim_text,
)
from cmf_builder.visual.grammar_contracts import (
    GrammarInductionResult,
)
from cmf_builder.visual.induction import InMemoryProvisionalGrammarWorkspace
from cmf_builder.visual.ontology import canonical_sha256, require_identifier


_ALL_OPTIONS = frozenset(BoundaryOptionKind)
_ALL_DIMENSIONS = frozenset(ComparisonDimension)
_ALL_RISK_DOMAINS = frozenset(RiskDomain)
def _nonempty_text(value: str, field: str) -> None:
    validate_provisional_claim_text(value, field)


def _validate_source(result: GrammarInductionResult) -> None:
    """Reuse ST-02.03's canonical commit validator without persisting state."""

    workspace = InMemoryProvisionalGrammarWorkspace()
    try:
        workspace.commit(
            result,
            actor_authority_ref=result.grammar.induction_authority_ref,
            expected_active_grammar_id=None,
        )
    except Exception as error:
        raise BoundaryEvidenceInvalid(
            "ST-02.03 grammar or induction receipt failed canonical validation"
        ) from error


def _validate_assessment(assessment, grammar) -> None:
    if not isinstance(assessment.dimension, ComparisonDimension):
        raise AlternativesIncomplete("comparison dimension is not typed")
    if not isinstance(assessment.evidence_status, EvidenceStatus):
        raise BoundaryEvidenceInvalid("dimension evidence status is not typed")
    _nonempty_text(assessment.finding, "dimension finding")
    graph_ids = set(assessment.source_graph_ids)
    motif_ids = set(assessment.motif_ids)
    hypothesis_ids = set(assessment.hypothesis_ids)
    if (
        len(graph_ids) != len(assessment.source_graph_ids)
        or len(motif_ids) != len(assessment.motif_ids)
        or len(hypothesis_ids) != len(assessment.hypothesis_ids)
    ):
        raise BoundaryEvidenceInvalid(
            "dimension evidence references must be unique rather than silently collapsed"
        )
    known_graphs = {item.graph_id: item for item in grammar.source_graphs}
    known_motifs = {item.motif_id: item for item in grammar.motifs}
    known_hypotheses = {item.hypothesis_id: item for item in grammar.hypotheses}
    if not graph_ids.issubset(known_graphs):
        raise BoundaryEvidenceInvalid("dimension references an unknown source graph")
    if not motif_ids.issubset(known_motifs):
        raise BoundaryEvidenceInvalid("dimension references an unknown grammar motif")
    if not hypothesis_ids.issubset(known_hypotheses):
        raise BoundaryEvidenceInvalid("dimension references an unknown hypothesis")
    if assessment.protected_boundary_claim or assessment.calibration_receipt_ref is not None:
        raise UnsupportedCertaintyRejected(
            "this offline branch has no independently verifiable protected-boundary calibration artifact"
        )
    if assessment.evidence_status is EvidenceStatus.UNAVAILABLE:
        if graph_ids or motif_ids or hypothesis_ids:
            raise BoundaryEvidenceInvalid(
                "unavailable evidence cannot carry hidden grammar evidence references"
            )
        return
    if assessment.evidence_status is EvidenceStatus.DETERMINISTIC_SYNTAX:
        if not graph_ids or not motif_ids or hypothesis_ids:
            raise BoundaryEvidenceInvalid(
                "deterministic syntax requires graph and motif evidence only"
            )
        expected_graphs = {
            graph_id for motif_id in motif_ids for graph_id in known_motifs[motif_id].source_graph_ids
        }
    else:
        if not graph_ids or motif_ids or not hypothesis_ids:
            raise BoundaryEvidenceInvalid(
                "provisional meaning requires graph and hypothesis evidence only"
            )
        expected_graphs = {
            graph_id
            for hypothesis_id in hypothesis_ids
            for graph_id in known_hypotheses[hypothesis_id].source_graph_ids
        }
    if graph_ids != expected_graphs:
        raise BoundaryEvidenceInvalid(
            "dimension cross-wires evidence objects and source-graph lineage"
        )


def _validate_risk(risk, grammar) -> None:
    if not isinstance(risk.domain, RiskDomain) or not isinstance(
        risk.direction, RiskDirection
    ) or not isinstance(risk.severity, RiskSeverity):
        raise BoundaryEvidenceInvalid("wrong-boundary risk is not fully typed")
    _nonempty_text(risk.consequence, "wrong-boundary consequence")
    if not risk.provisional:
        raise UnsupportedCertaintyRejected("wrong-boundary risk must remain provisional")
    graph_ids = set(risk.source_graph_ids)
    hypothesis_ids = set(risk.hypothesis_ids)
    if len(graph_ids) != len(risk.source_graph_ids) or len(hypothesis_ids) != len(
        risk.hypothesis_ids
    ):
        raise BoundaryEvidenceInvalid(
            "wrong-boundary evidence references must be unique"
        )
    known_hypotheses = {item.hypothesis_id: item for item in grammar.hypotheses}
    if not graph_ids or not hypothesis_ids or not hypothesis_ids.issubset(known_hypotheses):
        raise BoundaryEvidenceInvalid(
            "wrong-boundary risk requires known provisional hypothesis evidence"
        )
    expected_graphs = {
        graph_id
        for hypothesis_id in hypothesis_ids
        for graph_id in known_hypotheses[hypothesis_id].source_graph_ids
    }
    if graph_ids != expected_graphs:
        raise BoundaryEvidenceInvalid(
            "wrong-boundary risk cross-wires hypothesis and source-graph lineage"
        )


def _validate_candidate(candidate: BoundaryCandidate, grammar) -> None:
    validate_identifier_fields(candidate)
    if not isinstance(candidate.option_kind, BoundaryOptionKind):
        raise AlternativesIncomplete("boundary alternative kind is not typed")
    if not isinstance(candidate.status, AtomicityStatus):
        raise AlternativesIncomplete("atomicity status is not typed")
    if not isinstance(candidate.recommendation, RecommendationDisposition):
        raise AlternativesIncomplete("recommendation disposition is not typed")
    _nonempty_text(candidate.consequence, "candidate consequence")
    if not candidate.affected_specimen_ids or len(candidate.affected_specimen_ids) != len(
        set(candidate.affected_specimen_ids)
    ):
        raise AlternativesIncomplete("candidate must expose unique affected specimens")
    known_specimens = {item.specimen_id for item in grammar.source_graphs}
    if set(candidate.affected_specimen_ids) != known_specimens:
        raise BoundaryEvidenceInvalid(
            "candidate affected specimens do not exactly match source grammar evidence"
        )
    shared = set(candidate.shared_dimensions)
    differing = set(candidate.differing_dimensions)
    if len(shared) != len(candidate.shared_dimensions) or len(differing) != len(
        candidate.differing_dimensions
    ):
        raise AlternativesIncomplete(
            "shared and differing dimensions must not contain duplicate entries"
        )
    if shared & differing or shared | differing != _ALL_DIMENSIONS:
        raise AlternativesIncomplete(
            "shared and differing dimensions must be disjoint and cover all dimensions"
        )
    if not isinstance(candidate.configuration_sufficient, bool):
        raise AlternativesIncomplete("configuration sufficiency must be explicit")
    breaking = set(candidate.breaking_dimensions)
    if len(breaking) != len(candidate.breaking_dimensions) or not breaking.issubset(
        _ALL_DIMENSIONS
    ):
        raise AlternativesIncomplete("breaking dimensions must be typed")
    assessments = {item.dimension: item for item in candidate.dimensions}
    if len(assessments) != len(candidate.dimensions) or set(assessments) != _ALL_DIMENSIONS:
        raise AlternativesIncomplete(
            "each alternative must compare every required atomicity dimension exactly once"
        )
    for assessment in candidate.dimensions:
        _validate_assessment(assessment, grammar)
    missing_dimensions = {
        item.dimension
        for item in candidate.dimensions
        if item.evidence_status is EvidenceStatus.UNAVAILABLE
    }
    gaps = tuple(item.strip() for item in candidate.evidence_gaps if item.strip())
    if len(gaps) != len(candidate.evidence_gaps) or len(gaps) != len(set(gaps)):
        raise BoundaryEvidenceInvalid("evidence gaps must be explicit, nonblank and unique")
    evidence_state = (
        missing_dimensions,
        candidate.status is AtomicityStatus.INSUFFICIENT_EVIDENCE,
        candidate.recommendation is RecommendationDisposition.MORE_EVIDENCE,
        bool(gaps),
    )
    if any(evidence_state) and not all(evidence_state):
        raise BoundaryEvidenceInvalid(
            "unavailable evidence, insufficient status, more-evidence disposition and gaps must agree bidirectionally"
        )
    risks = {item.domain: item for item in candidate.risks}
    if len(risks) != len(candidate.risks) or set(risks) != _ALL_RISK_DOMAINS:
        raise AlternativesIncomplete(
            "each alternative must expose all five wrong-boundary risk domains"
        )
    for risk in candidate.risks:
        _validate_risk(risk, grammar)
    expected_direction = (
        RiskDirection.OVER_MERGE
        if candidate.option_kind in (BoundaryOptionKind.MERGE, BoundaryOptionKind.FAMILY)
        else RiskDirection.OVER_SPLIT
    )
    if any(risk.direction is not expected_direction for risk in candidate.risks):
        raise BoundaryEvidenceInvalid(
            "wrong-boundary risk direction does not match the candidate alternative"
        )


def _canonicalize_candidate(candidate: BoundaryCandidate) -> BoundaryCandidate:
    dimensions = tuple(
        sorted(
            (
                replace(
                    item,
                    source_graph_ids=tuple(sorted(item.source_graph_ids)),
                    motif_ids=tuple(sorted(item.motif_ids)),
                    hypothesis_ids=tuple(sorted(item.hypothesis_ids)),
                )
                for item in candidate.dimensions
            ),
            key=lambda item: item.dimension.value,
        )
    )
    risks = tuple(
        sorted(
            (
                replace(
                    item,
                    source_graph_ids=tuple(sorted(item.source_graph_ids)),
                    hypothesis_ids=tuple(sorted(item.hypothesis_ids)),
                )
                for item in candidate.risks
            ),
            key=lambda item: item.domain.value,
        )
    )
    return replace(
        candidate,
        affected_specimen_ids=tuple(sorted(candidate.affected_specimen_ids)),
        shared_dimensions=tuple(
            sorted(candidate.shared_dimensions, key=lambda item: item.value)
        ),
        differing_dimensions=tuple(
            sorted(candidate.differing_dimensions, key=lambda item: item.value)
        ),
        breaking_dimensions=tuple(
            sorted(candidate.breaking_dimensions, key=lambda item: item.value)
        ),
        evidence_gaps=tuple(sorted(candidate.evidence_gaps)),
        dimensions=dimensions,
        risks=risks,
    )


def _packet_core(packet: AtomicityComparisonPacket) -> dict[str, object]:
    payload = packet.as_dict()
    payload.pop("packet_id")
    payload.pop("version")
    payload.pop("artifact_sha256")
    return payload


def _receipt_core(receipt: AtomicityComparisonReceipt) -> dict[str, object]:
    payload = receipt.as_dict()
    payload.pop("receipt_id")
    return payload


def _expected_receipt_id(receipt: AtomicityComparisonReceipt) -> str:
    return f"ST-02.04:ComparisonReceipt:{canonical_sha256(_receipt_core(receipt))}"


def _validate_result(result: AtomicityComparisonResult) -> None:
    packet = result.packet
    receipt = result.receipt
    expected_hash = canonical_sha256(_packet_core(packet))
    if (
        packet.artifact_sha256 != expected_hash
        or packet.packet_id != f"ST-02.04:AtomicityComparison:{expected_hash}"
        or packet.version != f"0.0.0-development+{expected_hash[:16]}"
    ):
        raise AtomicityCommitRejected("comparison packet identity is not canonical")
    if (
        packet.knowledge_status != "PROVISIONAL_COMPARISON"
        or packet.decision_status != "UNRATIFIED"
        or packet.evidence_gate_status != "EVIDENCE_PENDING"
        or not packet.human_decision_required
        or packet.genesis_authorized
        or packet.production_ready
        or packet.certified
        or packet.claim_policy_id != AUTHORITY_CLAIM_POLICY_ID
        or packet.claim_policy_version != AUTHORITY_CLAIM_POLICY_VERSION
        or packet.claim_policy_sha256 != AUTHORITY_CLAIM_POLICY_SHA256
    ):
        raise AtomicityCommitRejected("comparison packet authority invariants are invalid")
    exact_receipt = (
        receipt.story_id == "ST-02.04"
        and receipt.development_mode == "OD_AM_001_OFFLINE_DEVELOPMENT"
        and receipt.event_name == "ST-02.04:ComparisonCompiled"
        and receipt.packet_id == packet.packet_id
        and receipt.packet_version == packet.version
        and receipt.packet_artifact_sha256 == packet.artifact_sha256
        and receipt.grammar_id == packet.grammar_evidence.grammar_id
        and receipt.grammar_artifact_sha256
        == packet.grammar_evidence.grammar_artifact_sha256
        and receipt.induction_receipt_sha256
        == packet.grammar_evidence.induction_receipt_sha256
        and receipt.comparison_authority_ref == packet.comparison_authority_ref
        and receipt.candidate_count == 4
        and receipt.dimension_count_per_candidate == 10
        and receipt.outcome == "OUTCOME_VERIFIED_PROVISIONAL"
        and receipt.failure_context == "NONE"
        and receipt.receipt_id == _expected_receipt_id(receipt)
    )
    if not exact_receipt:
        raise AtomicityCommitRejected(
            "comparison receipt is not exactly bound to the canonical packet"
        )


def _validate_result_against_source(
    result: AtomicityComparisonResult,
    grammar_result: GrammarInductionResult,
) -> None:
    _validate_source(grammar_result)
    packet = result.packet
    grammar = grammar_result.grammar
    evidence = packet.grammar_evidence
    expected_series_id = canonical_sha256(
        {
            "grammar_series_id": grammar.series_id,
            "category_id": grammar.category_id,
            "comparison_authority_ref": packet.comparison_authority_ref,
        }
    )
    if (
        packet.series_id != expected_series_id
        or packet.category_id != grammar.category_id
        or evidence.grammar_id != grammar.grammar_id
        or evidence.grammar_version != grammar.version
        or evidence.grammar_artifact_sha256 != grammar.artifact_sha256
        or evidence.induction_receipt_id != grammar_result.receipt.receipt_id
        or evidence.induction_receipt_sha256 != grammar_result.receipt.receipt_sha256
        or evidence.source_graph_ids
        != tuple(item.graph_id for item in grammar.source_graphs)
        or evidence.evidence_gate_status != "EVIDENCE_PENDING"
        or evidence.maturity != "PROVISIONAL"
    ):
        raise AtomicityCommitRejected(
            "comparison packet is not exactly bound to the validated ST-02.03 result"
        )
    if len(packet.candidates) != 4 or {
        item.option_kind for item in packet.candidates
    } != _ALL_OPTIONS:
        raise AtomicityCommitRejected(
            "comparison packet does not expose the complete alternative set"
        )
    if len({item.candidate_id for item in packet.candidates}) != 4:
        raise AtomicityCommitRejected(
            "comparison packet candidate identities are not unique"
        )
    if packet.candidates != tuple(
        sorted(packet.candidates, key=lambda item: item.option_kind.value)
    ):
        raise AtomicityCommitRejected(
            "comparison alternatives are not in canonical order"
        )
    for candidate in packet.candidates:
        try:
            _validate_candidate(candidate, grammar)
        except (AlternativesIncomplete, BoundaryEvidenceInvalid, UnsupportedCertaintyRejected) as error:
            raise AtomicityCommitRejected(
                "comparison packet failed semantic validation at commit"
            ) from error
        if candidate != _canonicalize_candidate(candidate):
            raise AtomicityCommitRejected(
                "comparison packet fields are not in canonical order"
            )
    if {risk.direction for item in packet.candidates for risk in item.risks} != set(
        RiskDirection
    ):
        raise AtomicityCommitRejected(
            "comparison packet does not distinguish over-merge and over-split risk"
        )


def compare_candidate_boundaries(
    *,
    run_id: str,
    grammar_result: GrammarInductionResult,
    candidates: Sequence[BoundaryCandidate],
    comparison_authority_ref: str,
) -> AtomicityComparisonResult:
    require_identifier(run_id, "comparison_run_id")
    require_identifier(comparison_authority_ref, "comparison_authority_ref")
    _validate_source(grammar_result)
    grammar = grammar_result.grammar
    supplied = tuple(candidates)
    if len(supplied) != 4 or {item.option_kind for item in supplied} != _ALL_OPTIONS:
        raise AlternativesIncomplete(
            "comparison must expose exactly merge, split, variant and family alternatives"
        )
    if len({item.candidate_id for item in supplied}) != len(supplied):
        raise AlternativesIncomplete("comparison candidate identities must be unique")
    for candidate in supplied:
        _validate_candidate(candidate, grammar)
    ordered = tuple(
        sorted(
            (_canonicalize_candidate(item) for item in supplied),
            key=lambda item: item.option_kind.value,
        )
    )
    if {risk.direction for item in ordered for risk in item.risks} != set(RiskDirection):
        raise AlternativesIncomplete(
            "comparison must distinguish both over-merge and over-split risk"
        )
    grammar_evidence = GrammarEvidenceReference(
        grammar_id=grammar.grammar_id,
        grammar_version=grammar.version,
        grammar_artifact_sha256=grammar.artifact_sha256,
        induction_receipt_id=grammar_result.receipt.receipt_id,
        induction_receipt_sha256=grammar_result.receipt.receipt_sha256,
        source_graph_ids=tuple(item.graph_id for item in grammar.source_graphs),
    )
    series_id = canonical_sha256(
        {
            "grammar_series_id": grammar.series_id,
            "category_id": grammar.category_id,
            "comparison_authority_ref": comparison_authority_ref,
        }
    )
    packet = AtomicityComparisonPacket(
        packet_id="PENDING_CANONICAL_BINDING",
        series_id=series_id,
        version="PENDING_CANONICAL_BINDING",
        category_id=grammar.category_id,
        grammar_evidence=grammar_evidence,
        candidates=ordered,
        comparison_authority_ref=comparison_authority_ref,
        artifact_sha256="PENDING_CANONICAL_BINDING",
    )
    artifact_sha256 = canonical_sha256(_packet_core(packet))
    packet = replace(
        packet,
        packet_id=f"ST-02.04:AtomicityComparison:{artifact_sha256}",
        version=f"0.0.0-development+{artifact_sha256[:16]}",
        artifact_sha256=artifact_sha256,
    )
    receipt = AtomicityComparisonReceipt(
        receipt_id="PENDING_CANONICAL_BINDING",
        run_id=run_id,
        packet_id=packet.packet_id,
        packet_version=packet.version,
        packet_artifact_sha256=packet.artifact_sha256,
        grammar_id=grammar.grammar_id,
        grammar_artifact_sha256=grammar.artifact_sha256,
        induction_receipt_sha256=grammar_result.receipt.receipt_sha256,
        comparison_authority_ref=comparison_authority_ref,
        candidate_count=len(ordered),
        dimension_count_per_candidate=len(ComparisonDimension),
    )
    receipt = replace(receipt, receipt_id=_expected_receipt_id(receipt))
    result = AtomicityComparisonResult(packet=packet, receipt=receipt)
    _validate_result(result)
    _validate_result_against_source(result, grammar_result)
    return result


class InMemoryAtomicityComparisonWorkspace:
    """Atomic, immutable workspace proving authority, replay and rollback."""

    def __init__(self, *, authority: AuthorityService) -> None:
        self._authority = authority
        self._packets: dict[str, AtomicityComparisonPacket] = {}
        self._results: dict[str, AtomicityComparisonResult] = {}
        self._active_by_series: dict[str, str] = {}

    def commit(
        self,
        result: AtomicityComparisonResult,
        *,
        grammar_result: GrammarInductionResult,
        actor_id: str,
        now: datetime,
        expected_active_packet_id: str | None,
        inject_failure: bool = False,
    ) -> AtomicityComparisonPacket:
        packet = result.packet
        actor = self._authority.authorize(
            actor_id=actor_id,
            action=Action.COMPARE_ATOMIC_BOUNDARIES,
            resource_id=packet.series_id,
            now=now,
        )
        if actor.actor_id != packet.comparison_authority_ref:
            raise AtomicityAuthorityRejected(
                "authorized actor does not match the packet comparison authority"
            )
        _validate_result(result)
        _validate_result_against_source(result, grammar_result)
        current = self._active_by_series.get(packet.series_id)
        if current == packet.packet_id:
            if self._results[packet.packet_id] != result:
                raise AtomicityCommitRejected(
                    "same packet identity was repeated with a different payload"
                )
            return self._packets[packet.packet_id]
        if current != expected_active_packet_id:
            raise AtomicityCommitRejected(
                "active comparison changed since the caller's governed expectation"
            )
        staged_packets = dict(self._packets)
        staged_results = dict(self._results)
        staged_active = dict(self._active_by_series)
        if packet.packet_id in staged_packets and staged_packets[packet.packet_id] != packet:
            raise AtomicityCommitRejected("immutable packet identity conflicts")
        if packet.packet_id in staged_results and staged_results[packet.packet_id] != result:
            raise AtomicityCommitRejected("immutable packet receipt binding conflicts")
        staged_packets[packet.packet_id] = packet
        staged_results[packet.packet_id] = result
        staged_active[packet.series_id] = packet.packet_id
        if inject_failure:
            raise AtomicityCommitRejected("injected failure before atomic comparison commit")
        self._packets = staged_packets
        self._results = staged_results
        self._active_by_series = staged_active
        return packet

    def rollback_to(
        self,
        *,
        series_id: str,
        packet_id: str,
        actor_id: str,
        now: datetime,
        expected_active_packet_id: str,
    ) -> AtomicityComparisonPacket:
        packet = self._packets.get(packet_id)
        if packet is None or packet.series_id != series_id:
            raise AtomicityCommitRejected(
                "rollback target is not an immutable packet in this series"
            )
        actor = self._authority.authorize(
            actor_id=actor_id,
            action=Action.COMPARE_ATOMIC_BOUNDARIES,
            resource_id=series_id,
            now=now,
        )
        if actor.actor_id != packet.comparison_authority_ref:
            raise AtomicityAuthorityRejected(
                "authorized actor does not match the packet comparison authority"
            )
        if self._active_by_series.get(series_id) != expected_active_packet_id:
            raise AtomicityCommitRejected(
                "active comparison changed since the rollback expectation"
            )
        staged = dict(self._active_by_series)
        staged[series_id] = packet_id
        self._active_by_series = staged
        return packet

    def active(self, series_id: str) -> AtomicityComparisonPacket | None:
        packet_id = self._active_by_series.get(series_id)
        return None if packet_id is None else self._packets[packet_id]

    def history(self, series_id: str) -> tuple[AtomicityComparisonPacket, ...]:
        return tuple(
            sorted(
                (item for item in self._packets.values() if item.series_id == series_id),
                key=lambda item: item.packet_id,
            )
        )
