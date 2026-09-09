"""
Acceptance and integration tests for CA-M005 — Format and Archetype Matchmaking Gate.

Coverage:
- deterministic PASS decisions with exact narrative/hypothesis binding
- disallowed archetype/format coalition rejection
- declared aspect-ratio rejection
- missing required format capability rejection
- fail-closed pipeline admission
- operator-selection integration: invalid combinations create no production artifacts
- downstream compilation gate: legacy selections without CA-M005 receipts are rejected
- downstream compilation gate: tampered CA-M005 receipts are rejected
"""

from __future__ import annotations

import hashlib
import json

import pytest

from cae_interview_intelligence.composition_compatibility import (
    KNOWN_FORMATS,
    CompositionCompatibilityEvaluator,
)
from cae_interview_intelligence.hypothesis_adapter import SemanticRef
from cae_interview_intelligence.question_resolver import CompositionCompatibility
from cae_runtime.editorial_discovery_program import (
    EditorialDiscoveryProgramCoordinator,
    UnapprovedExecutionError,
)
from cae_runtime.editorial_discovery_store import (
    ContentCandidateRecord,
    EditorialDecisionReceiptRecord,
    EditorialDiscoveryStore,
    EvidenceSegmentRecord,
)
from cae_candidate_intelligence.domain import CandidateType, NarrativeCompleteness
from cmf_pipeline.candidates.service import CandidateSearchService
from cmf_pipeline.domain.errors import PipelineValidationError
from ca_runtime.program_state_runtime import AuthorityLane


def sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_candidate(workspace_id: str = "ws-ca-m005", candidate_id: str = "CND-CA-M005") -> ContentCandidateRecord:
    text = "I signed the exception after the inspection failed and documented the exact discrepancy."
    segment_id = f"SEG-{candidate_id}"
    segment_hash = sha(text)
    return ContentCandidateRecord(
        workspace_id=workspace_id,
        candidate_id=candidate_id,
        candidate_type=CandidateType.STORY_CANDIDATE.value,
        title="The inspection exception",
        hook_statement="A documented inspection failure changed the decision.",
        narrative_completeness=NarrativeCompleteness.COMPLETE.value,
        story_arc="THE_WITNESS",
        tension_ref="AET-CA-M005",
        invariant_ref="FR-ARCH-001",
        archetypal_container="ARCH-CRUCIBLE",
        evidence_links=[
            {
                "segment_id": segment_id,
                "annotation_id": "ANN-CA-M005",
                "speaker": "guest",
                "start_time_ms": 0,
                "end_time_ms": 900,
                "verbatim_text": text,
                "text_sha256": segment_hash,
            }
        ],
        cmf_score_bps={"composite_score_bps": 9000},
    )


def seed_candidate(store: EditorialDiscoveryStore, workspace_id: str = "ws-ca-m005") -> ContentCandidateRecord:
    candidate = build_candidate(workspace_id=workspace_id)
    link = candidate.evidence_links[0]
    store.insert_evidence_segment(
        EvidenceSegmentRecord(
            workspace_id=workspace_id,
            segment_id=link["segment_id"],
            session_id="SES-CA-M005",
            speaker="guest",
            start_time_ms=0,
            end_time_ms=900,
            verbatim_text=link["verbatim_text"],
            boundary_type="CLAUSE",
            text_sha256=link["text_sha256"],
            context_dependency={},
            is_authenticated=True,
        )
    )
    store.insert_content_candidate(candidate)
    return candidate


def test_ca_m005_feasible_binding_is_deterministic_and_verified() -> None:
    narrative_ref = SemanticRef(
        object_id="narrative:inspection-exception",
        version="2.1.0",
        sha256=sha("narrative:inspection-exception:v2.1.0"),
        object_type="narrative_revision",
    )
    hypothesis_ref = SemanticRef(
        object_id="hypothesis:inspection-failure",
        version="4.0.0",
        sha256=sha("hypothesis:inspection-failure:v4.0.0"),
        object_type="activation_hypothesis",
    )

    first = CompositionCompatibilityEvaluator.evaluate_preproduction_admission(
        target_archetype="ARCH-CRUCIBLE",
        target_format="FMT-01-STORY",
        target_narrative_role="ROLE-PROTAGONIST-CRUCIBLE",
        narrative_ref=narrative_ref,
        hypothesis_ref=hypothesis_ref,
    )
    second = CompositionCompatibilityEvaluator.evaluate_preproduction_admission(
        target_archetype="ARCH-CRUCIBLE",
        target_format="FMT-01-STORY",
        target_narrative_role="ROLE-PROTAGONIST-CRUCIBLE",
        narrative_ref=narrative_ref,
        hypothesis_ref=hypothesis_ref,
    )

    assert first.gate_status == "PASS"
    assert first.incompatible_reasons == []
    assert first.decision_sha256
    assert CompositionCompatibilityEvaluator.verify_admission_result(first)
    assert first.decision_sha256 == second.decision_sha256
    assert first.narrative_ref == narrative_ref
    assert first.hypothesis_ref == hypothesis_ref
    assert first.format_profile_ref is not None
    assert first.archetype_profile_ref is not None
    assert first.format_profile_ref.sha256 == second.format_profile_ref.sha256


def test_ca_m005_blocks_disallowed_archetype_format_pair() -> None:
    result = CompositionCompatibilityEvaluator.evaluate_preproduction_admission(
        target_archetype="ARCH-CRUCIBLE",
        target_format="FMT-02-REACTION",
        target_narrative_role="ROLE-PROTAGONIST-CRUCIBLE",
    )

    assert result.gate_status == "BLOCK"
    assert any("not supported by delivery format" in reason for reason in result.incompatible_reasons)
    assert result.decision_sha256
    assert CompositionCompatibilityEvaluator.verify_admission_result(result)


def test_ca_m005_blocks_declared_aspect_ratio_mismatch() -> None:
    result = CompositionCompatibilityEvaluator.evaluate_preproduction_admission(
        target_archetype="ARCH-WITNESS",
        target_format="FMT-02-REACTION",
        target_narrative_role="ROLE-OBSERVER-WITNESS",
        target_aspect_ratio="1:1",
    )

    assert result.gate_status == "BLOCK"
    assert result.target_aspect_ratio == "1:1"
    assert any("Aspect ratio '1:1' is not supported" in reason for reason in result.incompatible_reasons)


def test_ca_m005_blocks_missing_required_format_capability() -> None:
    required = KNOWN_FORMATS["FMT-03-BREAKDOWN"].required_capabilities
    result = CompositionCompatibilityEvaluator.evaluate_preproduction_admission(
        target_archetype="ARCH-INVESTIGATIVE",
        target_format="FMT-03-BREAKDOWN",
        target_narrative_role="ROLE-TECHNICAL-ANALYST",
        provided_format_capabilities=required[:-1],
    )

    assert result.gate_status == "BLOCK"
    assert result.missing_format_capabilities == [required[-1]]
    assert any("Required format capabilities are missing" in reason for reason in result.incompatible_reasons)


def test_ca_m005_pipeline_admission_is_fail_closed() -> None:
    with pytest.raises(PipelineValidationError, match="PreProduction admission blocked"):
        CandidateSearchService.enforce_preproduction_gate(
            {
                "gate_status": "BLOCK",
                "decision_sha256": sha("bad-gate"),
                "incompatible_reasons": ["unsupported archetype/format coalition"],
            },
            candidate_id="CND-FAIL-CLOSED",
        )

    with pytest.raises(PipelineValidationError, match="PreProduction admission blocked"):
        CandidateSearchService.enforce_preproduction_gate(
            {
                "gate_status": "PASS",
                "decision_sha256": None,
                "incompatible_reasons": [],
            },
            candidate_id="CND-NO-DIGEST",
        )


def test_ca_m005_invalid_selection_creates_no_storyboard_or_select_receipt() -> None:
    store = EditorialDiscoveryStore()
    try:
        candidate = seed_candidate(store)
        coordinator = EditorialDiscoveryProgramCoordinator(editorial_store=store)

        with pytest.raises(PipelineValidationError, match="PreProduction admission blocked"):
            coordinator.operator_select_candidate(
                lane=AuthorityLane.COMMANDER,
                workspace_id=candidate.workspace_id,
                operator_id="operator-ca-m005",
                candidate_id=candidate.candidate_id,
                priority_rank=1,
                rationale="The proposed format is not compatible with the archetype.",
                target_format="FMT-02-REACTION",
                target_archetype="ARCH-CRUCIBLE",
                target_aspect_ratio="1:1",
                format_capabilities=KNOWN_FORMATS["FMT-02-REACTION"].required_capabilities,
            )

        assert store.list_editorial_storyboards(candidate.workspace_id) == []
        assert store.list_decision_receipts(candidate.workspace_id, candidate.candidate_id) == []
        persisted = store.get_content_candidate(candidate.workspace_id, candidate.candidate_id)
        assert persisted is not None
        assert persisted.production_status == "DRAFT_CANDIDATE"
    finally:
        store._conn.close()


def test_ca_m005_downstream_rejects_selection_without_gate_receipt() -> None:
    store = EditorialDiscoveryStore()
    try:
        candidate = seed_candidate(store)
        receipt = EditorialDecisionReceiptRecord(
            workspace_id=candidate.workspace_id,
            receipt_id="REC-LEGACY-CA-M005",
            operator_id="legacy-operator",
            candidate_id=candidate.candidate_id,
            action_type="SELECT",
            rationale="Legacy selection predating the gate.",
            metadata_payload={"storyboard_id": "STB-LEGACY", "priority_rank": 1},
            receipt_sha256=sha("legacy-receipt"),
        )
        store.insert_decision_receipt(receipt)
        store.update_candidate_status(
            candidate.workspace_id,
            candidate.candidate_id,
            "SELECTED_FOR_PRODUCTION",
            operator_decision_ref=receipt.receipt_id,
        )

        coordinator = EditorialDiscoveryProgramCoordinator(editorial_store=store)
        with pytest.raises(UnapprovedExecutionError, match="missing CA-M005 format/archetype admission receipt"):
            coordinator.verify_downstream_production_eligibility(
                lane=AuthorityLane.COMMANDER,
                workspace_id=candidate.workspace_id,
                candidate_id=candidate.candidate_id,
            )
    finally:
        store._conn.close()


def test_ca_m005_tampered_gate_receipt_is_rejected_downstream() -> None:
    store = EditorialDiscoveryStore()
    try:
        candidate = seed_candidate(store)
        coordinator = EditorialDiscoveryProgramCoordinator(editorial_store=store)
        storyboard = coordinator.operator_select_candidate(
            lane=AuthorityLane.COMMANDER,
            workspace_id=candidate.workspace_id,
            operator_id="operator-ca-m005",
            candidate_id=candidate.candidate_id,
            priority_rank=1,
            rationale="The proposed format matches the intended archetype.",
        )

        receipt = store.list_decision_receipts(candidate.workspace_id, candidate.candidate_id)[-1]
        tampered = dict(receipt.metadata_payload)
        gate = dict(tampered["format_gate"])
        gate["decision_sha256"] = sha("tampered-gate")
        tampered["format_gate"] = gate
        store._conn.execute(
            "UPDATE cae_editorial_receipts SET metadata_payload = ? WHERE receipt_id = ?",
            (json.dumps(tampered), receipt.receipt_id),
        )
        store._conn.commit()

        assert storyboard.notes is not None
        assert "CA-M005 PASS:" in storyboard.notes
        with pytest.raises(UnapprovedExecutionError, match="CA-M005 admission receipt failed verification"):
            coordinator.verify_downstream_production_eligibility(
                lane=AuthorityLane.COMMANDER,
                workspace_id=candidate.workspace_id,
                candidate_id=candidate.candidate_id,
            )
    finally:
        store._conn.close()
