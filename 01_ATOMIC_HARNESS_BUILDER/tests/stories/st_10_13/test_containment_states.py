import pytest

from cmf_builder.application.containment_states import ContainmentError, ContainmentRecord, ContainmentState, export_containment


def test_containment_export_preserves_partial_redacted_failed_and_invalidated_states():
    partial = ContainmentRecord("a", ContainmentState.PARTIAL, ("id",), ("secret",), (), "NONE", "", (), ("request_authority",), True, ("receipt:a",), ("partial not complete",))
    redacted = ContainmentRecord("b", ContainmentState.REDACTED, ("id",), ("secret",), ("protected_value",), "NONE", "", (), ("request_unredacted_authority",), False, ("receipt:b",), ())
    failed = ContainmentRecord("c", ContainmentState.FAILED, ("id",), (), (), "SCHEMA_ERROR", "", (), ("retry",), True, ("receipt:c",), ())
    invalidated = ContainmentRecord("d", ContainmentState.INVALIDATED, ("id",), (), (), "NONE", "parent_invalidated", ("child:1",), ("view_history",), False, ("receipt:d",), ())

    exported = export_containment((invalidated, failed, redacted, partial))
    assert [item["subject_identity"] for item in exported["containment_records"]] == ["a", "b", "c", "d"]
    assert "containment_state_preserved" in exported["export_limitations"]


def test_containment_rejects_state_flattening_security_and_authority_errors():
    with pytest.raises(ContainmentError) as partial:
        ContainmentRecord("a", ContainmentState.PARTIAL, ("id",), (), (), "NONE", "", (), (), False, ("receipt",), ())
    assert partial.value.code == "PARTIAL_REQUIRES_UNAVAILABLE_FIELDS"

    with pytest.raises(ContainmentError) as redaction:
        ContainmentRecord("b", ContainmentState.REDACTED, ("id",), ("field",), (), "NONE", "", (), (), False, ("receipt",), ())
    assert redaction.value.code == "REDACTION_REASON_REQUIRED"

    with pytest.raises(ContainmentError) as authority:
        ContainmentRecord("c", ContainmentState.REDACTED, ("id",), ("field",), ("protected",), "MISSING_AUTHORITY", "", (), (), False, ("receipt",), ())
    assert authority.value.code == "MISSING_AUTHORITY_NOT_REDACTION"

    with pytest.raises(ContainmentError) as human_truth:
        ContainmentRecord("d", ContainmentState.REDACTED, ("id",), ("field",), ("protected",), "NONE", "", (), ("RECONSTRUCT_HUMAN_TRUTH",), False, ("receipt",), ())
    assert human_truth.value.code == "HUMAN_TRUTH_RECONSTRUCTION_PROHIBITED"
