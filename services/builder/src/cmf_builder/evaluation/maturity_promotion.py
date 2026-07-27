"""Development-only maturity promotion contracts for ST-08.02.

The module implements the OD-AM-001 offline development mechanism for protected
evidence receipts and maturity receipts.  It does not close protected benchmark,
external evidence, production, or certification gates.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
import hashlib
import json
import re
import weakref
from typing import Any, Iterable


STORY_ID = "ST-08.02"
MINIMUM_REPETITIONS = 3
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_ISO_UTC = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
_PROHIBITED_CLAIMS = frozenset(
    {
        "stable",
        "shadow_ready",
        "production_ready",
        "certified",
        "production_certified",
        "external_target_compatible",
        "real_protected_benchmark_passed",
        "empirical_superiority",
        "transfer_generality_proven",
    }
)
_CONSTRUCTION_ANCHORS: dict[int, tuple[weakref.ReferenceType[Any], str]] = {}


class MaturityPromotionError(ValueError):
    """Typed fail-closed error with deterministic context."""

    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class CaseLayer(str, Enum):
    PUBLIC = "public"
    DEVELOPMENT = "development"
    PROTECTED = "protected"


class BranchStatus(str, Enum):
    EVALUATED = "evaluated"
    NOT_EVALUATED = "not_evaluated"


class MaturityStatus(str, Enum):
    DRAFT = "draft"
    EVALUATION_PENDING = "evaluation_pending"
    EXPERIMENTAL = "experimental"
    TESTED = "tested"
    DEVELOPMENT_VALIDATED = "development_validated"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"


class PromotionAction(str, Enum):
    PROMOTE = "promote_development_maturity"
    DEPRECATE = "deprecate_development_maturity"
    SUPERSEDE = "supersede_development_maturity"
    ROLLBACK = "rollback_development_maturity"
    INVALIDATE = "invalidate_development_maturity"


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _construction_payload(instance: Any) -> dict[str, Any]:
    payload_builder = getattr(instance, "_construction_payload", None)
    return payload_builder() if payload_builder is not None else instance.as_dict()


def _seal_constructed_identity(instance: Any) -> None:
    key = id(instance)

    def remove_anchor(reference: weakref.ReferenceType[Any], *, identity: int = key) -> None:
        current = _CONSTRUCTION_ANCHORS.get(identity)
        if current is not None and current[0] is reference:
            _CONSTRUCTION_ANCHORS.pop(identity, None)

    reference = weakref.ref(instance, remove_anchor)
    _CONSTRUCTION_ANCHORS[key] = (reference, canonical_sha256(_construction_payload(instance)))


def _require_unmutated(instance: Any, field_name: str) -> None:
    anchored = _CONSTRUCTION_ANCHORS.get(id(instance))
    if anchored is None or anchored[0]() is not instance:
        raise MaturityPromotionError(
            "UNANCHORED_GOVERNED_OBJECT",
            f"{field_name} lacks its module-private construction anchor",
            field=field_name,
        )
    try:
        current = canonical_sha256(_construction_payload(instance))
    except (AttributeError, TypeError, ValueError) as exc:
        raise MaturityPromotionError(
            "MUTATED_GOVERNED_OBJECT",
            f"{field_name} no longer has valid canonical semantics",
            field=field_name,
        ) from exc
    if current != anchored[1]:
        raise MaturityPromotionError(
            "MUTATED_GOVERNED_OBJECT",
            f"{field_name} changed after immutable construction",
            field=field_name,
        )


def _safe_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return {
            item.name: _safe_value(getattr(value, item.name, None))
            for item in fields(value)
            if item.init
        }
    if isinstance(value, dict):
        return {str(key): _safe_value(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_safe_value(item) for item in value]
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    return {"unsupported_type": type(value).__qualname__}


def _require_text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MaturityPromotionError("MISSING_GOVERNED_FIELD", f"{field} is required", field=field)
    _reject_claim_vocabulary(value, field)
    return value


def _require_sha256(value: str, field: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise MaturityPromotionError(
            "INVALID_IMMUTABLE_IDENTITY",
            f"{field} must be a lowercase SHA-256 digest",
            field=field,
        )
    return value


def _require_optional_sha256(value: str | None, field: str) -> None:
    if value is not None:
        _require_sha256(value, field)


def _require_enum(value: object, enum_type: type[Enum], field: str) -> None:
    if not isinstance(value, enum_type):
        raise MaturityPromotionError(
            "INVALID_GOVERNED_TYPE",
            f"{field} must be a {enum_type.__name__}",
            field=field,
        )


def _require_bool(value: object, field: str) -> None:
    if type(value) is not bool:
        raise MaturityPromotionError(
            "INVALID_GOVERNED_TYPE",
            f"{field} must be a boolean",
            field=field,
        )


def _require_utc(value: str, field: str) -> None:
    _require_text(value, field)
    if not _ISO_UTC.fullmatch(value):
        raise MaturityPromotionError(
            "INVALID_GOVERNED_TIME",
            f"{field} must be an explicit UTC timestamp ending in Z",
            field=field,
        )


def _reject_claim_vocabulary(value: str, field: str) -> None:
    normalized = re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")
    padded = f"_{normalized}_"
    matched = [token for token in _PROHIBITED_CLAIMS if f"_{token}_" in padded]
    if matched:
        raise MaturityPromotionError(
            "PROHIBITED_MATURITY_OR_CERTIFICATION_CLAIM",
            f"{field} contains a prohibited maturity or certification claim",
            field=field,
            matched=tuple(sorted(matched)),
        )


@dataclass(frozen=True, slots=True, weakref_slot=True)
class EvaluationIdentity:
    subject_id: str
    subject_version: str
    subject_sha256: str
    source_ir_sha256: str
    skill_package_sha256: str
    adaptation_sha256: str
    recipe_sha256: str
    jit_capsule_sha256: str
    compiler_sha256: str
    model_policy_sha256: str
    dataset_sha256: str
    rubric_sha256: str
    scoring_sha256: str
    evaluator_sha256: str
    regression_policy_sha256: str

    def __post_init__(self) -> None:
        _require_text(self.subject_id, "subject_id")
        _require_text(self.subject_version, "subject_version")
        for field_name in (
            "subject_sha256",
            "source_ir_sha256",
            "skill_package_sha256",
            "adaptation_sha256",
            "recipe_sha256",
            "jit_capsule_sha256",
            "compiler_sha256",
            "model_policy_sha256",
            "dataset_sha256",
            "rubric_sha256",
            "scoring_sha256",
            "evaluator_sha256",
            "regression_policy_sha256",
        ):
            _require_sha256(getattr(self, field_name), field_name)
        _seal_constructed_identity(self)

    @property
    def identity(self) -> str:
        _require_unmutated(self, "evaluation_identity")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "story_id": STORY_ID,
            "subject_id": self.subject_id,
            "subject_version": self.subject_version,
            "subject_sha256": self.subject_sha256,
            "source_ir_sha256": self.source_ir_sha256,
            "skill_package_sha256": self.skill_package_sha256,
            "adaptation_sha256": self.adaptation_sha256,
            "recipe_sha256": self.recipe_sha256,
            "jit_capsule_sha256": self.jit_capsule_sha256,
            "compiler_sha256": self.compiler_sha256,
            "model_policy_sha256": self.model_policy_sha256,
            "dataset_sha256": self.dataset_sha256,
            "rubric_sha256": self.rubric_sha256,
            "scoring_sha256": self.scoring_sha256,
            "evaluator_sha256": self.evaluator_sha256,
            "regression_policy_sha256": self.regression_policy_sha256,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "evaluation_identity")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class CaseEvidence:
    case_id: str
    case_layer: CaseLayer
    evidence_role: str
    expected_behavior_authority_sha256: str
    scoring_rule_sha256: str
    source_provenance_sha256: str
    custody_class: str
    custody_authority_sha256: str | None = None
    case_assignment_receipt_sha256: str | None = None
    evaluator_isolation_receipt_sha256: str | None = None
    protected_label_reference_sha256: str | None = None
    protected_label_bytes_in_receipt: bool = False
    generator_access_to_expected_behavior: bool = False
    synthetic_fixture_claimed_as_real_protected_evidence: bool = False

    def __post_init__(self) -> None:
        _require_text(self.case_id, "case_id")
        _require_enum(self.case_layer, CaseLayer, "case_layer")
        _require_text(self.evidence_role, "evidence_role")
        _require_text(self.custody_class, "custody_class")
        for field_name in (
            "expected_behavior_authority_sha256",
            "scoring_rule_sha256",
            "source_provenance_sha256",
        ):
            _require_sha256(getattr(self, field_name), field_name)
        for field_name in (
            "custody_authority_sha256",
            "case_assignment_receipt_sha256",
            "evaluator_isolation_receipt_sha256",
            "protected_label_reference_sha256",
        ):
            _require_optional_sha256(getattr(self, field_name), field_name)
        _require_bool(self.protected_label_bytes_in_receipt, "protected_label_bytes_in_receipt")
        _require_bool(self.generator_access_to_expected_behavior, "generator_access_to_expected_behavior")
        _require_bool(
            self.synthetic_fixture_claimed_as_real_protected_evidence,
            "synthetic_fixture_claimed_as_real_protected_evidence",
        )
        if self.protected_label_bytes_in_receipt:
            raise MaturityPromotionError(
                "PROTECTED_LABEL_LEAKAGE",
                "protected labels cannot be serialized into portable receipts",
            )
        if self.generator_access_to_expected_behavior:
            raise MaturityPromotionError(
                "PROTECTED_EXPECTED_BEHAVIOR_LEAKAGE",
                "generator context cannot include protected expected behavior",
            )
        if self.synthetic_fixture_claimed_as_real_protected_evidence:
            raise MaturityPromotionError(
                "SYNTHETIC_FIXTURE_FALSELY_CLAIMS_PROTECTED_EVIDENCE",
                "synthetic fixtures cannot close the real protected-evidence gate",
            )
        if self.case_layer is CaseLayer.PROTECTED:
            if self.custody_class != "protected_custody_reference_only":
                raise MaturityPromotionError(
                    "INVALID_PROTECTED_CUSTODY_CLASS",
                    "protected cases must use reference-only custody",
                )
            required = {
                "custody_authority_sha256": self.custody_authority_sha256,
                "case_assignment_receipt_sha256": self.case_assignment_receipt_sha256,
                "evaluator_isolation_receipt_sha256": self.evaluator_isolation_receipt_sha256,
                "protected_label_reference_sha256": self.protected_label_reference_sha256,
            }
            missing = tuple(name for name, value in required.items() if value is None)
            if missing:
                raise MaturityPromotionError(
                    "MISSING_PROTECTED_CUSTODY_EVIDENCE",
                    "protected cases require custody, assignment, label and evaluator isolation references",
                    missing=missing,
                )
        elif self.protected_label_reference_sha256 is not None:
            raise MaturityPromotionError(
                "PROTECTED_LABEL_ON_UNPROTECTED_CASE",
                "public and development cases cannot carry protected-label references",
            )
        _seal_constructed_identity(self)

    @property
    def case_identity(self) -> str:
        _require_unmutated(self, "case_evidence")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "case_layer": self.case_layer.value,
            "evidence_role": self.evidence_role,
            "expected_behavior_authority_sha256": self.expected_behavior_authority_sha256,
            "scoring_rule_sha256": self.scoring_rule_sha256,
            "source_provenance_sha256": self.source_provenance_sha256,
            "custody_class": self.custody_class,
            "custody_authority_sha256": self.custody_authority_sha256,
            "case_assignment_receipt_sha256": self.case_assignment_receipt_sha256,
            "evaluator_isolation_receipt_sha256": self.evaluator_isolation_receipt_sha256,
            "protected_label_reference_sha256": self.protected_label_reference_sha256,
            "protected_label_bytes_in_receipt": self.protected_label_bytes_in_receipt,
            "generator_access_to_expected_behavior": self.generator_access_to_expected_behavior,
            "synthetic_fixture_claimed_as_real_protected_evidence": (
                self.synthetic_fixture_claimed_as_real_protected_evidence
            ),
            "real_protected_evidence_closed": False,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "case_evidence")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class PortfolioBranch:
    branch_id: str
    branch_role: str
    status: BranchStatus
    artifact_sha256: str | None
    status_justification: str

    def __post_init__(self) -> None:
        _require_text(self.branch_id, "branch_id")
        _require_text(self.branch_role, "branch_role")
        _require_enum(self.status, BranchStatus, "status")
        _require_text(self.status_justification, "status_justification")
        _require_optional_sha256(self.artifact_sha256, "artifact_sha256")
        if self.status is BranchStatus.EVALUATED and self.artifact_sha256 is None:
            raise MaturityPromotionError(
                "MISSING_EVALUATED_BRANCH_ARTIFACT",
                "evaluated portfolio branches require an artifact identity",
            )
        if self.status is BranchStatus.NOT_EVALUATED and not self.status_justification:
            raise MaturityPromotionError(
                "MISSING_NOT_EVALUATED_JUSTIFICATION",
                "not-evaluated branches must remain explicit",
            )
        _seal_constructed_identity(self)

    @property
    def branch_identity(self) -> str:
        _require_unmutated(self, "portfolio_branch")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "branch_id": self.branch_id,
            "branch_role": self.branch_role,
            "status": self.status.value,
            "artifact_sha256": self.artifact_sha256,
            "status_justification": self.status_justification,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "portfolio_branch")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class PortfolioManifest:
    manifest_version: str
    primary_reference: PortfolioBranch
    contrasting_transfer_harnesses: tuple[PortfolioBranch, ...]
    vae_target: PortfolioBranch
    delegation_target: PortfolioBranch

    def __post_init__(self) -> None:
        _require_text(self.manifest_version, "manifest_version")
        if not isinstance(self.primary_reference, PortfolioBranch):
            raise MaturityPromotionError("INVALID_GOVERNED_TYPE", "primary_reference is required")
        if self.primary_reference.status is not BranchStatus.EVALUATED:
            raise MaturityPromotionError(
                "PRIMARY_REFERENCE_NOT_EVALUATED",
                "the primary reference branch must be explicitly evaluated",
            )
        if not isinstance(self.contrasting_transfer_harnesses, tuple) or not self.contrasting_transfer_harnesses:
            raise MaturityPromotionError(
                "MISSING_TRANSFER_BRANCH_DECLARATIONS",
                "contrasting transfer branches must be declared",
            )
        for index, branch in enumerate(
            (self.primary_reference, *self.contrasting_transfer_harnesses, self.vae_target, self.delegation_target)
        ):
            if not isinstance(branch, PortfolioBranch):
                raise MaturityPromotionError(
                    "INVALID_GOVERNED_TYPE",
                    "portfolio branches must be PortfolioBranch values",
                    index=index,
                )
            _require_unmutated(branch, f"portfolio_branch[{index}]")
        _seal_constructed_identity(self)

    @property
    def manifest_identity(self) -> str:
        _require_unmutated(self, "portfolio_manifest")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "manifest_version": self.manifest_version,
            "primary_reference": self.primary_reference.as_dict(),
            "contrasting_transfer_harnesses": [
                branch.as_dict() for branch in self.contrasting_transfer_harnesses
            ],
            "vae_target": self.vae_target.as_dict(),
            "delegation_target": self.delegation_target.as_dict(),
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "portfolio_manifest")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class ProtectedEvidenceReceipt:
    evaluation_identity: EvaluationIdentity
    cases: tuple[CaseEvidence, ...]
    portfolio: PortfolioManifest
    fresh_context_receipt_sha256: str
    repetition_statistics_receipt_sha256: str
    hard_gate_receipt_sha256: str
    artifact_identity_receipt_sha256: str
    no_guidance_control_receipt_sha256: str
    scoring_summary_sha256: str
    threshold_policy_sha256: str
    required_repetitions: int
    hard_gates_passed: bool
    aggregate_score_basis_points: int
    non_compensable_failures: tuple[str, ...] = ()
    real_protected_evidence_closed: bool = False
    production_ready: bool = False
    certified: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.evaluation_identity, EvaluationIdentity):
            raise MaturityPromotionError("INVALID_GOVERNED_TYPE", "evaluation_identity is required")
        if not isinstance(self.portfolio, PortfolioManifest):
            raise MaturityPromotionError("INVALID_GOVERNED_TYPE", "portfolio is required")
        _require_unmutated(self.evaluation_identity, "evaluation_identity")
        _require_unmutated(self.portfolio, "portfolio")
        for field_name in (
            "fresh_context_receipt_sha256",
            "repetition_statistics_receipt_sha256",
            "hard_gate_receipt_sha256",
            "artifact_identity_receipt_sha256",
            "no_guidance_control_receipt_sha256",
            "scoring_summary_sha256",
            "threshold_policy_sha256",
        ):
            _require_sha256(getattr(self, field_name), field_name)
        if isinstance(self.required_repetitions, bool) or not isinstance(self.required_repetitions, int):
            raise MaturityPromotionError("INVALID_REPETITION_COUNT", "required_repetitions must be an integer")
        if self.required_repetitions < MINIMUM_REPETITIONS:
            raise MaturityPromotionError(
                "INSUFFICIENT_REPETITIONS",
                "development maturity requires repeated fresh-context evidence",
            )
        _require_bool(self.hard_gates_passed, "hard_gates_passed")
        if isinstance(self.aggregate_score_basis_points, bool) or not isinstance(
            self.aggregate_score_basis_points, int
        ):
            raise MaturityPromotionError(
                "INVALID_SCORE",
                "aggregate_score_basis_points must be an integer",
            )
        if not (0 <= self.aggregate_score_basis_points <= 10_000):
            raise MaturityPromotionError("INVALID_SCORE", "aggregate score is out of range")
        if not isinstance(self.cases, tuple) or not self.cases:
            raise MaturityPromotionError("MISSING_CASE_EVIDENCE", "cases are required")
        layers = set()
        case_ids = set()
        for index, case in enumerate(self.cases):
            if not isinstance(case, CaseEvidence):
                raise MaturityPromotionError("INVALID_GOVERNED_TYPE", "cases must be CaseEvidence")
            _require_unmutated(case, f"case[{index}]")
            if case.case_id in case_ids:
                raise MaturityPromotionError("DUPLICATE_CASE_ID", "case identities must be unique")
            case_ids.add(case.case_id)
            layers.add(case.case_layer)
        if layers != set(CaseLayer):
            raise MaturityPromotionError(
                "INCOMPLETE_LAYERED_CASE_EVIDENCE",
                "public, development and protected case layers must remain distinct",
            )
        if not isinstance(self.non_compensable_failures, tuple):
            raise MaturityPromotionError(
                "INVALID_GOVERNED_TYPE",
                "non_compensable_failures must be an immutable tuple",
            )
        for failure in self.non_compensable_failures:
            _require_text(failure, "non_compensable_failure")
        for field_name in ("real_protected_evidence_closed", "production_ready", "certified"):
            _require_bool(getattr(self, field_name), field_name)
            if getattr(self, field_name):
                raise MaturityPromotionError(
                    "PROHIBITED_PRODUCTION_OR_EVIDENCE_CLAIM",
                    f"{field_name} must remain false in OD-AM-001",
                    field=field_name,
                )
        _seal_constructed_identity(self)

    @property
    def receipt_identity(self) -> str:
        _require_unmutated(self, "protected_evidence_receipt")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "story_id": STORY_ID,
            "evaluation_identity": self.evaluation_identity.as_dict(),
            "cases": [case.as_dict() for case in self.cases],
            "portfolio": self.portfolio.as_dict(),
            "fresh_context_receipt_sha256": self.fresh_context_receipt_sha256,
            "repetition_statistics_receipt_sha256": self.repetition_statistics_receipt_sha256,
            "hard_gate_receipt_sha256": self.hard_gate_receipt_sha256,
            "artifact_identity_receipt_sha256": self.artifact_identity_receipt_sha256,
            "no_guidance_control_receipt_sha256": self.no_guidance_control_receipt_sha256,
            "scoring_summary_sha256": self.scoring_summary_sha256,
            "threshold_policy_sha256": self.threshold_policy_sha256,
            "required_repetitions": self.required_repetitions,
            "hard_gates_passed": self.hard_gates_passed,
            "aggregate_score_basis_points": self.aggregate_score_basis_points,
            "non_compensable_failures": list(self.non_compensable_failures),
            "real_protected_evidence_closed": False,
            "production_ready": False,
            "certified": False,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "protected_evidence_receipt")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class PromotionAuthority:
    actor_id: str
    action: PromotionAction
    resource_id: str
    authority_sha256: str
    expires_at_utc: str

    def __post_init__(self) -> None:
        _require_text(self.actor_id, "actor_id")
        _require_enum(self.action, PromotionAction, "action")
        _require_sha256(self.resource_id, "resource_id")
        _require_sha256(self.authority_sha256, "authority_sha256")
        _require_utc(self.expires_at_utc, "expires_at_utc")
        _seal_constructed_identity(self)

    @property
    def authority_identity(self) -> str:
        _require_unmutated(self, "promotion_authority")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "actor_id": self.actor_id,
            "action": self.action.value,
            "resource_id": self.resource_id,
            "authority_sha256": self.authority_sha256,
            "expires_at_utc": self.expires_at_utc,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "promotion_authority")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class MaturityCommand:
    command_id: str
    actor_id: str
    action: PromotionAction
    resource_id: str
    requested_status: MaturityStatus
    issued_at_utc: str
    reason_sha256: str
    replacement_receipt_sha256: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.command_id, "command_id")
        _require_text(self.actor_id, "actor_id")
        _require_enum(self.action, PromotionAction, "action")
        _require_sha256(self.resource_id, "resource_id")
        _require_enum(self.requested_status, MaturityStatus, "requested_status")
        _require_utc(self.issued_at_utc, "issued_at_utc")
        _require_sha256(self.reason_sha256, "reason_sha256")
        _require_optional_sha256(self.replacement_receipt_sha256, "replacement_receipt_sha256")
        if self.requested_status in {MaturityStatus.DEPRECATED, MaturityStatus.SUPERSEDED}:
            if self.action not in {PromotionAction.DEPRECATE, PromotionAction.SUPERSEDE}:
                raise MaturityPromotionError(
                    "INVALID_MATURITY_ACTION",
                    "terminal status must match its transition action",
                )
        if self.action is PromotionAction.PROMOTE and self.requested_status not in {
            MaturityStatus.EVALUATION_PENDING,
            MaturityStatus.EXPERIMENTAL,
            MaturityStatus.TESTED,
            MaturityStatus.DEVELOPMENT_VALIDATED,
        }:
            raise MaturityPromotionError(
                "INVALID_MATURITY_ACTION",
                "promotion can only emit development progression statuses",
            )
        _seal_constructed_identity(self)

    @property
    def command_identity(self) -> str:
        _require_unmutated(self, "maturity_command")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "command_id": self.command_id,
            "actor_id": self.actor_id,
            "action": self.action.value,
            "resource_id": self.resource_id,
            "requested_status": self.requested_status.value,
            "issued_at_utc": self.issued_at_utc,
            "reason_sha256": self.reason_sha256,
            "replacement_receipt_sha256": self.replacement_receipt_sha256,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "maturity_command")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class DevelopmentMaturityReceipt:
    evaluation_identity: str
    protected_evidence_receipt_sha256: str
    portfolio_manifest_sha256: str
    command_identity: str
    authority_identity: str
    maturity_status: MaturityStatus
    prior_status: MaturityStatus
    outcome: str
    observations: tuple[str, ...]
    invalidates_descendants: tuple[str, ...] = ()
    evidence_gate_closed: bool = False
    real_protected_evidence_closed: bool = False
    production_ready: bool = False
    certified: bool = False

    def __post_init__(self) -> None:
        for field_name in (
            "evaluation_identity",
            "protected_evidence_receipt_sha256",
            "portfolio_manifest_sha256",
            "command_identity",
            "authority_identity",
        ):
            _require_sha256(getattr(self, field_name), field_name)
        _require_enum(self.maturity_status, MaturityStatus, "maturity_status")
        _require_enum(self.prior_status, MaturityStatus, "prior_status")
        _require_text(self.outcome, "outcome")
        if not isinstance(self.observations, tuple) or not self.observations:
            raise MaturityPromotionError("MISSING_OBSERVABILITY", "observations are required")
        for observation in self.observations:
            _require_text(observation, "observation")
        if not isinstance(self.invalidates_descendants, tuple):
            raise MaturityPromotionError(
                "INVALID_GOVERNED_TYPE",
                "invalidates_descendants must be an immutable tuple",
            )
        for digest in self.invalidates_descendants:
            _require_sha256(digest, "invalidates_descendants")
        for field_name in (
            "evidence_gate_closed",
            "real_protected_evidence_closed",
            "production_ready",
            "certified",
        ):
            _require_bool(getattr(self, field_name), field_name)
            if getattr(self, field_name):
                raise MaturityPromotionError(
                    "PROHIBITED_PRODUCTION_OR_EVIDENCE_CLAIM",
                    f"{field_name} must remain false in OD-AM-001",
                    field=field_name,
                )
        _seal_constructed_identity(self)

    @property
    def receipt_identity(self) -> str:
        _require_unmutated(self, "development_maturity_receipt")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "story_id": STORY_ID,
            "evaluation_identity": self.evaluation_identity,
            "protected_evidence_receipt_sha256": self.protected_evidence_receipt_sha256,
            "portfolio_manifest_sha256": self.portfolio_manifest_sha256,
            "command_identity": self.command_identity,
            "authority_identity": self.authority_identity,
            "maturity_status": self.maturity_status.value,
            "prior_status": self.prior_status.value,
            "outcome": self.outcome,
            "observations": list(self.observations),
            "invalidates_descendants": list(self.invalidates_descendants),
            "maximum_maturity": MaturityStatus.DEVELOPMENT_VALIDATED.value,
            "evidence_gate_closed": False,
            "real_protected_evidence_closed": False,
            "production_ready": False,
            "certified": False,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "development_maturity_receipt")
        return self._construction_payload()


def _validate_exact_authority(
    command: MaturityCommand, authority: PromotionAuthority, action: PromotionAction
) -> None:
    _require_unmutated(command, "maturity_command")
    _require_unmutated(authority, "promotion_authority")
    if command.action is not action or authority.action is not action:
        raise MaturityPromotionError("AUTHORITY_ACTION_MISMATCH", "action must match authority")
    if command.actor_id != authority.actor_id:
        raise MaturityPromotionError("AUTHORITY_ACTOR_MISMATCH", "actor must match authority")
    if command.resource_id != authority.resource_id:
        raise MaturityPromotionError("AUTHORITY_RESOURCE_MISMATCH", "resource must match authority")


def _require_promotable_evidence(
    candidate: EvaluationIdentity, evidence: ProtectedEvidenceReceipt
) -> None:
    _require_unmutated(candidate, "evaluation_identity")
    _require_unmutated(evidence, "protected_evidence_receipt")
    if evidence.evaluation_identity.identity != candidate.identity:
        raise MaturityPromotionError(
            "EVALUATED_ARTIFACT_IDENTITY_MISMATCH",
            "only the exact evaluated artifact version can be promoted",
        )
    if not evidence.hard_gates_passed:
        raise MaturityPromotionError(
            "HARD_GATE_FAILURE",
            "hard gates cannot be compensated by aggregate score",
        )
    if evidence.non_compensable_failures:
        raise MaturityPromotionError(
            "NON_COMPENSABLE_FAILURE",
            "non-compensable failures block maturity promotion",
            failures=evidence.non_compensable_failures,
        )


def promote_development_maturity(
    *,
    candidate: EvaluationIdentity,
    evidence: ProtectedEvidenceReceipt,
    command: MaturityCommand,
    authority: PromotionAuthority,
    prior_status: MaturityStatus = MaturityStatus.TESTED,
) -> DevelopmentMaturityReceipt:
    """Promote only the exact evaluated development fixture up to development_validated."""

    _require_enum(prior_status, MaturityStatus, "prior_status")
    _validate_exact_authority(command, authority, PromotionAction.PROMOTE)
    _require_promotable_evidence(candidate, evidence)
    if command.resource_id != candidate.identity:
        raise MaturityPromotionError(
            "COMMAND_RESOURCE_MISMATCH",
            "promotion command must target the evaluated identity",
        )
    return DevelopmentMaturityReceipt(
        evaluation_identity=candidate.identity,
        protected_evidence_receipt_sha256=evidence.receipt_identity,
        portfolio_manifest_sha256=evidence.portfolio.manifest_identity,
        command_identity=command.command_identity,
        authority_identity=authority.authority_identity,
        maturity_status=command.requested_status,
        prior_status=prior_status,
        outcome="DEVELOPMENT_MATURITY_PROMOTED_WITHOUT_EVIDENCE_CLOSURE",
        observations=(
            f"{STORY_ID}:ProtectedEvidenceReceiptValidated",
            f"{STORY_ID}:DevelopmentMaturityReceiptIssued",
        ),
    )


def validate_repeat_command(
    *,
    existing: DevelopmentMaturityReceipt,
    candidate: EvaluationIdentity,
    evidence: ProtectedEvidenceReceipt,
    command: MaturityCommand,
    authority: PromotionAuthority,
) -> DevelopmentMaturityReceipt:
    """Return the same receipt for identical commands and fail closed on conflicts."""

    replayed = promote_development_maturity(
        candidate=candidate, evidence=evidence, command=command, authority=authority
    )
    if existing.receipt_identity != replayed.receipt_identity:
        raise MaturityPromotionError(
            "CONFLICTING_REPEAT_COMMAND",
            "repeat command payload does not reproduce the existing receipt",
        )
    return existing


def invalidate_maturity_receipt(
    *,
    receipt: DevelopmentMaturityReceipt,
    changed_identities: Iterable[str],
    command: MaturityCommand,
    authority: PromotionAuthority,
) -> DevelopmentMaturityReceipt:
    changed = tuple(sorted(changed_identities))
    if not changed:
        raise MaturityPromotionError("MISSING_INVALIDATION_INPUT", "changed identities are required")
    for digest in changed:
        _require_sha256(digest, "changed_identity")
    _validate_exact_authority(command, authority, PromotionAction.INVALIDATE)
    if command.resource_id != receipt.receipt_identity:
        raise MaturityPromotionError(
            "COMMAND_RESOURCE_MISMATCH",
            "invalidation must target the active receipt identity",
        )
    return DevelopmentMaturityReceipt(
        evaluation_identity=receipt.evaluation_identity,
        protected_evidence_receipt_sha256=receipt.protected_evidence_receipt_sha256,
        portfolio_manifest_sha256=receipt.portfolio_manifest_sha256,
        command_identity=command.command_identity,
        authority_identity=authority.authority_identity,
        maturity_status=MaturityStatus.SUPERSEDED,
        prior_status=receipt.maturity_status,
        outcome="DEVELOPMENT_MATURITY_INVALIDATED_BY_CHANGED_INPUT",
        observations=(f"{STORY_ID}:DevelopmentMaturityInvalidated",),
        invalidates_descendants=changed,
    )


def transition_maturity_receipt(
    *,
    receipt: DevelopmentMaturityReceipt,
    command: MaturityCommand,
    authority: PromotionAuthority,
) -> DevelopmentMaturityReceipt:
    """Issue deterministic deprecation, supersession, or rollback transition receipts."""

    _require_unmutated(receipt, "development_maturity_receipt")
    if command.action not in {
        PromotionAction.DEPRECATE,
        PromotionAction.SUPERSEDE,
        PromotionAction.ROLLBACK,
    }:
        raise MaturityPromotionError("INVALID_MATURITY_ACTION", "transition action is required")
    _validate_exact_authority(command, authority, command.action)
    if command.resource_id != receipt.receipt_identity:
        raise MaturityPromotionError(
            "COMMAND_RESOURCE_MISMATCH",
            "transition command must target the active receipt identity",
        )
    if command.action is PromotionAction.SUPERSEDE and command.replacement_receipt_sha256 is None:
        raise MaturityPromotionError(
            "MISSING_REPLACEMENT_RECEIPT",
            "supersession requires a replacement receipt",
        )
    status = {
        PromotionAction.DEPRECATE: MaturityStatus.DEPRECATED,
        PromotionAction.SUPERSEDE: MaturityStatus.SUPERSEDED,
        PromotionAction.ROLLBACK: MaturityStatus.TESTED,
    }[command.action]
    return DevelopmentMaturityReceipt(
        evaluation_identity=receipt.evaluation_identity,
        protected_evidence_receipt_sha256=receipt.protected_evidence_receipt_sha256,
        portfolio_manifest_sha256=receipt.portfolio_manifest_sha256,
        command_identity=command.command_identity,
        authority_identity=authority.authority_identity,
        maturity_status=status,
        prior_status=receipt.maturity_status,
        outcome=f"DEVELOPMENT_MATURITY_{command.action.value.upper()}",
        observations=(f"{STORY_ID}:DevelopmentMaturityTransitioned",),
        invalidates_descendants=(
            (command.replacement_receipt_sha256,) if command.replacement_receipt_sha256 else ()
        ),
    )


def build_rejection_receipt(
    error: MaturityPromotionError,
    *,
    command: MaturityCommand | None,
    candidate: EvaluationIdentity | None,
    evidence: ProtectedEvidenceReceipt | None,
) -> dict[str, Any]:
    """Create deterministic rejection evidence without committing promotion state."""

    return {
        "story_id": STORY_ID,
        "outcome": "REJECTED_NO_MATURITY_RECEIPT",
        "failure_code": error.code,
        "failure_context": _safe_value(error.context),
        "command_identity": command.command_identity if command is not None else None,
        "candidate_identity": candidate.identity if candidate is not None else None,
        "evidence_receipt_identity": evidence.receipt_identity if evidence is not None else None,
        "rejection_identity": canonical_sha256(
            {
                "failure_code": error.code,
                "failure_context": _safe_value(error.context),
                "command": _safe_value(command) if command is not None else None,
                "candidate": _safe_value(candidate) if candidate is not None else None,
                "evidence": _safe_value(evidence) if evidence is not None else None,
            }
        ),
        "evidence_gate_closed": False,
        "production_ready": False,
        "certified": False,
    }
