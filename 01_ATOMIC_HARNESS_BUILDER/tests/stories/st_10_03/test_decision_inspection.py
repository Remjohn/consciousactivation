import pytest

from cmf_builder.application.decision_inspection import (
    DecisionInspectionError,
    DecisionInspectionResult,
    EvidenceKind,
    EvidenceReference,
    EvidenceState,
    SubjectType,
    SyntaxKind,
    SyntaxObservation,
    structured_explanation,
)


def evidence(eid, kind=EvidenceKind.DECISION_RECORD, state=EvidenceState.ACTIVE_SUPPORTING, **kwargs):
    return EvidenceReference(eid, kind, state, f"provenance:{eid}", f"lineage:{eid}", **kwargs)


def syntax(kind=SyntaxKind.CATEGORY_NATIVE_SYNTAX):
    return SyntaxObservation(f"syntax:{kind.value}", kind, "lineage:syntax", "compiled:syntax", "observed from canonical compiled evidence")


def result(**overrides):
    values = {
        "inspected_subject": "decision:category-native",
        "subject_type": SubjectType.DECISION,
        "governing_decision": "Bind category-native syntax to profile",
        "decision_status": "ACTIVE",
        "authority_owner": "authority:builder-rule",
        "evidence": (
            evidence("authority:1", EvidenceKind.AUTHORITY_RECORD),
            evidence("decision:1", EvidenceKind.DECISION_RECORD),
            evidence("grammar:1", EvidenceKind.PROVISIONAL_GRAMMAR),
        ),
        "syntax_observations": (syntax(SyntaxKind.SPATIAL_RELATIONSHIP), syntax(SyntaxKind.READING_ORDER)),
        "predecessor_decisions": ("decision:category-binding",),
        "superseding_decisions": (),
        "downstream_dependencies": ("workflow:1", "run-index:1"),
        "uncertainty": "development evidence only",
        "knowledge_status": "development_validated",
        "limitations": ("not certification",),
        "projection_freshness": "current:rev1",
    }
    values.update(overrides)
    return DecisionInspectionResult(**values)


def test_inspection_preserves_evidence_kinds_and_syntax_lineage():
    inspected = result()

    assert inspected.inspection_identity
    payload = inspected.as_dict()
    assert {item["kind"] for item in payload["evidence"]} >= {"AUTHORITY_RECORD", "DECISION_RECORD", "PROVISIONAL_GRAMMAR"}
    assert {item["syntax_kind"] for item in payload["syntax_observations"]} == {"reading_order", "spatial_relationship"}


def test_structured_explanation_includes_supporting_excluded_invalidated_redacted_and_missing_evidence():
    inspected = result(
        evidence=(
            evidence("authority:1", EvidenceKind.AUTHORITY_RECORD),
            evidence("support:1"),
            evidence("excluded:1", state=EvidenceState.EXCLUDED),
            evidence("invalidated:1", state=EvidenceState.INVALIDATED),
            evidence("redacted:1", state=EvidenceState.REDACTED, redaction_basis="governed redaction"),
            evidence("missing:1", state=EvidenceState.MISSING),
        )
    )

    explanation = structured_explanation(inspected)

    assert explanation["supporting_evidence"] == ["authority:1", "support:1"]
    assert explanation["excluded_evidence"] == ["excluded:1"]
    assert explanation["invalidated_evidence"] == ["invalidated:1"]
    assert explanation["redacted_evidence"] == ["redacted:1"]
    assert explanation["missing_evidence"] == ["missing:1"]
    assert explanation["inspection_is_authoritative_source"] is False


def test_conflicting_evidence_must_be_visible_in_limitations():
    with pytest.raises(DecisionInspectionError) as exc:
        result(evidence=(evidence("authority:1", EvidenceKind.AUTHORITY_RECORD), evidence("conflict:1", state=EvidenceState.ACTIVE_CONFLICTING)))
    assert exc.value.code == "CONFLICTING_EVIDENCE_MUST_BE_VISIBLE"

    inspected = result(
        evidence=(evidence("authority:1", EvidenceKind.AUTHORITY_RECORD), evidence("conflict:1", state=EvidenceState.ACTIVE_CONFLICTING)),
        limitations=("conflict recorded and unresolved",),
    )
    assert "conflict:1" in structured_explanation(inspected)["conflicting_evidence"]


def test_inspection_rejects_missing_authority_lineage_and_false_certification():
    with pytest.raises(DecisionInspectionError) as authority:
        result(evidence=(evidence("decision:1", EvidenceKind.DECISION_RECORD),))
    assert authority.value.code == "AUTHORITY_RECORD_REQUIRED"

    with pytest.raises(DecisionInspectionError) as missing:
        EvidenceReference("bad", EvidenceKind.RAW_SOURCE_REFERENCE, EvidenceState.ACTIVE_SUPPORTING, "", "lineage")
    assert missing.value.code == "MISSING_GOVERNED_FIELD"

    with pytest.raises(DecisionInspectionError) as certified:
        result(certified=True)
    assert certified.value.code == "FALSE_PRODUCTION_OR_CERTIFICATION_DISPLAY"


def test_not_applicable_and_redacted_evidence_require_explicit_basis():
    with pytest.raises(DecisionInspectionError) as redacted:
        evidence("redacted:bad", state=EvidenceState.REDACTED)
    assert redacted.value.code == "REDACTION_BASIS_REQUIRED"

    with pytest.raises(DecisionInspectionError) as na:
        evidence("na:bad", state=EvidenceState.NOT_APPLICABLE, limitation="not used")
    assert na.value.code == "NOT_APPLICABLE_BASIS_REQUIRED"
