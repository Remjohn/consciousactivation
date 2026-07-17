from __future__ import annotations

import hashlib

from cmf_builder.evaluation.maturity_promotion import (
    BranchStatus,
    CaseEvidence,
    CaseLayer,
    EvaluationIdentity,
    MaturityCommand,
    MaturityStatus,
    PortfolioBranch,
    PortfolioManifest,
    PromotionAction,
    PromotionAuthority,
    ProtectedEvidenceReceipt,
    promote_development_maturity,
)


ACTOR = "evaluation-governance-human"
NOW = "2026-07-17T12:00:00Z"


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def evaluation_identity(seed: str = "subject") -> EvaluationIdentity:
    return EvaluationIdentity(
        subject_id=f"repository-development-fixture-{seed}",
        subject_version="1.0.0",
        subject_sha256=digest(f"{seed}:subject"),
        source_ir_sha256=digest(f"{seed}:source-ir"),
        skill_package_sha256=digest(f"{seed}:skill-package"),
        adaptation_sha256=digest(f"{seed}:adaptation"),
        recipe_sha256=digest(f"{seed}:recipe"),
        jit_capsule_sha256=digest(f"{seed}:jit-capsule"),
        compiler_sha256=digest(f"{seed}:compiler"),
        model_policy_sha256=digest(f"{seed}:model-policy"),
        dataset_sha256=digest(f"{seed}:dataset"),
        rubric_sha256=digest(f"{seed}:rubric"),
        scoring_sha256=digest(f"{seed}:scoring"),
        evaluator_sha256=digest(f"{seed}:evaluator"),
        regression_policy_sha256=digest(f"{seed}:regression-policy"),
    )


def case_evidence() -> tuple[CaseEvidence, ...]:
    return (
        CaseEvidence(
            case_id="public-case",
            case_layer=CaseLayer.PUBLIC,
            evidence_role="public_development_control",
            expected_behavior_authority_sha256=digest("public-authority"),
            scoring_rule_sha256=digest("public-scoring"),
            source_provenance_sha256=digest("public-provenance"),
            custody_class="public",
        ),
        CaseEvidence(
            case_id="development-case",
            case_layer=CaseLayer.DEVELOPMENT,
            evidence_role="repository_owned_development_case",
            expected_behavior_authority_sha256=digest("development-authority"),
            scoring_rule_sha256=digest("development-scoring"),
            source_provenance_sha256=digest("development-provenance"),
            custody_class="development",
        ),
        CaseEvidence(
            case_id="protected-case-reference",
            case_layer=CaseLayer.PROTECTED,
            evidence_role="protected_case_contract_fixture",
            expected_behavior_authority_sha256=digest("protected-authority"),
            scoring_rule_sha256=digest("protected-scoring"),
            source_provenance_sha256=digest("protected-provenance"),
            custody_class="protected_custody_reference_only",
            custody_authority_sha256=digest("custody-authority"),
            case_assignment_receipt_sha256=digest("assignment-receipt"),
            evaluator_isolation_receipt_sha256=digest("evaluator-isolation"),
            protected_label_reference_sha256=digest("protected-label-reference"),
        ),
    )


def portfolio() -> PortfolioManifest:
    return PortfolioManifest(
        manifest_version="portfolio-v1",
        primary_reference=PortfolioBranch(
            branch_id="primary-reference",
            branch_role="primary_reference",
            status=BranchStatus.EVALUATED,
            artifact_sha256=digest("primary-artifact"),
            status_justification="primary repository fixture evaluated",
        ),
        contrasting_transfer_harnesses=(
            PortfolioBranch(
                branch_id="transfer-reference",
                branch_role="contrasting_transfer_harness",
                status=BranchStatus.NOT_EVALUATED,
                artifact_sha256=None,
                status_justification="transfer branch remains outside OD-AM-001 evidence closure",
            ),
        ),
        vae_target=PortfolioBranch(
            branch_id="vae-target",
            branch_role="vae_target",
            status=BranchStatus.NOT_EVALUATED,
            artifact_sha256=None,
            status_justification="VAE compatibility remains external",
        ),
        delegation_target=PortfolioBranch(
            branch_id="delegation-target",
            branch_role="delegation_target",
            status=BranchStatus.NOT_EVALUATED,
            artifact_sha256=None,
            status_justification="Delegation runtime remains external",
        ),
    )


def protected_evidence(
    identity: EvaluationIdentity | None = None,
    *,
    hard_gates_passed: bool = True,
    failures: tuple[str, ...] = (),
) -> ProtectedEvidenceReceipt:
    return ProtectedEvidenceReceipt(
        evaluation_identity=identity or evaluation_identity(),
        cases=case_evidence(),
        portfolio=portfolio(),
        fresh_context_receipt_sha256=digest("fresh-context-receipt"),
        repetition_statistics_receipt_sha256=digest("repetition-statistics"),
        hard_gate_receipt_sha256=digest("hard-gate-receipt"),
        artifact_identity_receipt_sha256=digest("artifact-identity-receipt"),
        no_guidance_control_receipt_sha256=digest("no-guidance-control"),
        scoring_summary_sha256=digest("scoring-summary"),
        threshold_policy_sha256=digest("threshold-policy"),
        required_repetitions=3,
        hard_gates_passed=hard_gates_passed,
        aggregate_score_basis_points=8200,
        non_compensable_failures=failures,
    )


def authority(resource_id: str, action: PromotionAction = PromotionAction.PROMOTE) -> PromotionAuthority:
    return PromotionAuthority(
        actor_id=ACTOR,
        action=action,
        resource_id=resource_id,
        authority_sha256=digest(f"{action.value}:authority"),
        expires_at_utc="2030-01-01T00:00:00Z",
    )


def command(
    resource_id: str,
    *,
    action: PromotionAction = PromotionAction.PROMOTE,
    status: MaturityStatus = MaturityStatus.DEVELOPMENT_VALIDATED,
    command_id: str = "command-001",
    replacement: str | None = None,
) -> MaturityCommand:
    return MaturityCommand(
        command_id=command_id,
        actor_id=ACTOR,
        action=action,
        resource_id=resource_id,
        requested_status=status,
        issued_at_utc=NOW,
        reason_sha256=digest(f"{command_id}:reason"),
        replacement_receipt_sha256=replacement,
    )


def test_exact_evaluated_version_receives_development_maturity_receipt() -> None:
    candidate = evaluation_identity()
    evidence = protected_evidence(candidate)
    receipt = promote_development_maturity(
        candidate=candidate,
        evidence=evidence,
        command=command(candidate.identity),
        authority=authority(candidate.identity),
    )

    payload = receipt.as_dict()
    assert payload["maturity_status"] == "development_validated"
    assert payload["maximum_maturity"] == "development_validated"
    assert payload["evidence_gate_closed"] is False
    assert payload["real_protected_evidence_closed"] is False
    assert payload["production_ready"] is False
    assert payload["certified"] is False
    assert payload["evaluation_identity"] == candidate.identity
    assert payload["protected_evidence_receipt_sha256"] == evidence.receipt_identity
    assert payload["portfolio_manifest_sha256"] == evidence.portfolio.manifest_identity


def test_layered_case_and_portfolio_identities_are_visible() -> None:
    evidence = protected_evidence()
    payload = evidence.as_dict()

    assert {case["case_layer"] for case in payload["cases"]} == {
        "public",
        "development",
        "protected",
    }
    assert payload["portfolio"]["primary_reference"]["status"] == "evaluated"
    assert payload["portfolio"]["vae_target"]["status"] == "not_evaluated"
    assert payload["portfolio"]["delegation_target"]["status"] == "not_evaluated"
    assert payload["real_protected_evidence_closed"] is False
