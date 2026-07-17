import pytest

from cmf_builder.application.certification_claims import CertificationClaim, ClaimClass, ClaimError, derive_offline_implementation_claim


def claim(**overrides):
    values = {
        "claim_identity": "claim:1",
        "claim_class": ClaimClass.LIMITED_SCOPE,
        "subject_identity": "builder",
        "requested_scope": "offline",
        "supported_scope": "offline",
        "prohibited_scope": ("production", "certification"),
        "evidence_requirements": ("receipts",),
        "supplied_evidence": ("receipt:1",),
        "missing_evidence": (),
        "authority_requirement": "OD-AM-005",
        "maturity_requirement": "offline_implementation",
        "supplied_maturity": "offline_implementation",
        "production_requirement": False,
        "certification_requirement": False,
        "decision": "SUPPORTED",
        "limitations": ("not production",),
        "expiration": "supersession",
        "invalidation": "ACTIVE",
    }
    values.update(overrides)
    return CertificationClaim(**values)


def test_offline_implementation_claim_derives_coverage_without_closing_evidence_gates():
    receipts = {f"ST-{i:02d}": "IMPLEMENTED_DEVELOPMENT_PASS" for i in range(69)}
    result = derive_offline_implementation_claim(receipts, total_confirmed_stories=69, open_gates=("BD-007", "BD-008", "human_evidence"))

    assert result.supported_scope == "69/69"
    assert result.decision == "LIMITED_SUPPORTED"
    assert "BD-007" in result.missing_evidence
    assert "production_ready" in result.prohibited_scope


def test_claims_reject_unsupported_production_certification_and_missing_evidence():
    with pytest.raises(ClaimError) as production:
        claim(claim_class=ClaimClass.PRODUCTION_READY)
    assert production.value.code == "PRODUCTION_OR_CERTIFICATION_CLAIM_UNSUPPORTED"

    with pytest.raises(ClaimError) as missing:
        claim(missing_evidence=("BD-007",))
    assert missing.value.code == "MISSING_EVIDENCE_CANNOT_SUPPORT_CLAIM"

    with pytest.raises(ClaimError) as maturity:
        claim(maturity_requirement="certified")
    assert maturity.value.code == "LOWER_MATURITY_CANNOT_SUPPORT_HIGHER_CLAIM"

    with pytest.raises(ClaimError) as human:
        claim(supplied_evidence=("agent_human_authority",))
    assert human.value.code == "AGENT_PROPOSAL_NOT_HUMAN_AUTHORITY"

    with pytest.raises(ClaimError) as invalidated:
        claim(invalidation="INVALIDATED")
    assert invalidated.value.code == "INVALIDATED_EVIDENCE_CANNOT_SUPPORT_CLAIM"
