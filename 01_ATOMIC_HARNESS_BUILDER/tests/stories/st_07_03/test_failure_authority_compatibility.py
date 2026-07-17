from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
import json

import pytest

from cmf_builder.domain.external_handoff_contracts import (
    DELEGATION_TARGET,
    HandoffContractRejected,
    SourceProvenance,
    SourceProvenanceRejected,
    compile_external_handoff,
    validate_local_contract,
    HandoffAuthorityRejected,
)
from test_external_handoff_contracts import handoff_input, ref


def test_ambiguous_unknown_and_unreceipted_legacy_sources_fail_closed() -> None:
    with pytest.raises(SourceProvenanceRejected, match="Ambiguous"):
        compile_external_handoff(
            replace(
                handoff_input(),
                source=SourceProvenance("Operator-authored source", ref("source_provenance")),
            )
        )
    with pytest.raises(SourceProvenanceRejected, match="Unknown"):
        compile_external_handoff(
            replace(handoff_input(), source=SourceProvenance("guessed-source", ref("source_provenance")))
        )
    with pytest.raises(SourceProvenanceRejected, match="migration receipt"):
        compile_external_handoff(
            replace(handoff_input(), source=SourceProvenance("Legacy migration", ref("source_provenance")))
        )


def test_exact_rc4_pin_and_nonproduction_boundary_are_enforced() -> None:
    with pytest.raises(HandoffContractRejected, match="exact RC4"):
        compile_external_handoff(
            replace(handoff_input(DELEGATION_TARGET), local_contract_pin="1.1.0-rc.3")
        )
    with pytest.raises(HandoffContractRejected, match="readiness or certification"):
        compile_external_handoff(replace(handoff_input(), production_ready=True))


def test_local_validation_receipt_preserves_external_pending_limitations() -> None:
    request = compile_external_handoff(handoff_input(DELEGATION_TARGET))
    receipt = validate_local_contract(request)
    assert receipt.authority == "BUILDER_LOCAL_CONTRACT_VALIDATION_ONLY"
    assert receipt.external_compatibility == "EXTERNAL_VALIDATION_PENDING"
    assert set(receipt.limitations) == {
        "NO_EXTERNAL_ACCEPTANCE",
        "NO_RUNTIME_VALIDATION",
        "NO_CERTIFICATION",
        "STRUCTURAL_FIXTURE_NOT_PARENT_MEANING_OR_REAL_PROFILE_EVIDENCE",
        "INTERVIEW_PROVENANCE_NOT_APPLICABLE",
    }
    with pytest.raises(HandoffContractRejected):
        replace(receipt, mapping_identity="lossy-generic-mapping")
    with pytest.raises(HandoffContractRejected):
        replace(receipt, output_hash="sha256:" + "0" * 64)
    with pytest.raises(HandoffContractRejected):
        replace(receipt, limitations=("NO_CERTIFICATION",))
    with pytest.raises(HandoffContractRejected):
        replace(receipt, receipt_id="ST-07.03:LocalValidation:forged")


def test_local_contract_does_not_copy_or_claim_external_schema_ownership() -> None:
    request = compile_external_handoff(handoff_input(DELEGATION_TARGET))
    payload = request.canonical_bytes.decode("utf-8")
    assert "shared_schema_owner" not in payload
    assert "external_acceptance" not in payload
    assert "production_ready\":true" not in payload
    assert "certified\":true" not in payload


def test_acknowledgement_and_result_links_reject_false_external_state() -> None:
    from cmf_builder.application.external_handoff_commands import (
        ExternalHandoffCommandResult,
        LocalHandoffAcknowledgement,
        LocalExternalResultEnvelope,
        LocalVisualAssetDemandTestDouble,
    )

    request = compile_external_handoff(handoff_input())
    ack = LocalVisualAssetDemandTestDouble().acknowledge(request)
    validation = validate_local_contract(request)
    boundary = LocalExternalResultEnvelope(
        request_identity=request.request_hash,
        target_identity=request.target_id,
        status="LOCAL_ACKNOWLEDGED",
        result_hash=validation.output_hash,
        error_code=None,
        reconciliation_required=False,
    )
    ExternalHandoffCommandResult(request, ack, validation, boundary)
    with pytest.raises(HandoffAuthorityRejected):
        replace(ack, external_acceptance=True)
    with pytest.raises(HandoffContractRejected):
        replace(ack, acknowledged_payload_hash="sha256:" + "0" * 64)
    with pytest.raises(HandoffContractRejected):
        ExternalHandoffCommandResult(
            request,
            ack,
            validation,
            replace(boundary, result_hash="sha256:" + "0" * 64),
        )
    altered_values = ack.identity_dict()
    altered_values["authority_identity"] = "another-authority"
    altered_ack = LocalHandoffAcknowledgement(
        acknowledgement_id=(
            "ST-07.03:LocalAck:"
            + sha256(
                (json.dumps(altered_values, sort_keys=True, separators=(",", ":")) + "\n").encode()
            ).hexdigest()
        ),
        **altered_values,
    )
    with pytest.raises(HandoffAuthorityRejected, match="Acknowledgement authority"):
        ExternalHandoffCommandResult(
            request,
            altered_ack,
            validation,
            boundary,
        )
