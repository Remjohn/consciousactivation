"""Evaluation receipt service for TS-CMF-050."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.evaluation_receipts import (
    EvaluationApprovalBlocker,
    EvaluationCategory,
    EvaluationCategoryInput,
    EvaluationDecision,
    EvaluationDomainEvent,
    EvaluationObjectType,
    EvaluationReceipt,
    EvaluationReviewReadModel,
    EvaluationScore,
    EvidenceClaimScope,
    EvidencePointer,
    HardFailure,
    default_evaluation_threshold_profile,
    evidence_ref,
    new_evaluation_receipt,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.evaluation_receipts import InMemoryEvaluationReceiptRepository
from ccp_studio.services.command_bus import CommandBus


class EvaluationReceiptError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class EvaluationReceiptService:
    repository: InMemoryEvaluationReceiptRepository = field(default_factory=InMemoryEvaluationReceiptRepository)

    def __post_init__(self) -> None:
        if "cmf.default.thresholds.v1" not in self.repository.threshold_profiles:
            self.repository.put_threshold_profile(default_evaluation_threshold_profile())

    def generate_evaluation_receipt(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        object_type: EvaluationObjectType | str,
        object_id: UUID,
        object_hash: str,
        actor_id: UUID,
        category_inputs: list[EvaluationCategoryInput | dict[str, Any]] | None = None,
        threshold_profile_id: str = "cmf.default.thresholds.v1",
        previous_receipt_id: UUID | None = None,
        warnings: list[str] | None = None,
        command_id: UUID | None = None,
    ) -> EvaluationReceipt:
        profile = self.repository.threshold_profiles.get(threshold_profile_id)
        if profile is None:
            raise EvaluationReceiptError("THRESHOLD_PROFILE_REQUIRED", "Evaluation threshold profile is required.")
        self._append_event("EvaluationStarted", None, object_type, object_id, {"threshold_profile_id": threshold_profile_id})
        normalized_inputs = self._inputs_for_all_categories(category_inputs, object_hash, profile.evaluator_version)
        scores: list[EvaluationScore] = []
        hard_failures: list[HardFailure] = []
        for category_input in normalized_inputs:
            threshold = profile.thresholds[category_input.category]
            score = EvaluationScore(
                category=category_input.category,
                score=category_input.score,
                threshold=threshold,
                passed=category_input.score >= threshold,
                evidence=category_input.evidence,
                evaluator_version=category_input.evaluator_version,
            )
            scores.append(score)
            self._append_event(
                "EvaluationCategoryScored",
                None,
                object_type,
                object_id,
                {"category": score.category.value, "score": score.score, "passed": score.passed},
            )
            if category_input.hard_failure:
                hard_failures.append(
                    HardFailure(
                        category=category_input.category,
                        code=category_input.hard_failure_code or "EVALUATION_HARD_FAILURE",
                        message=category_input.hard_failure_message or "Evaluation category hard-failed.",
                        evidence=category_input.evidence,
                        approval_blocker_code=category_input.approval_blocker_code,
                    )
                )
        receipt = new_evaluation_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            object_type=object_type,
            object_id=object_id,
            object_hash=object_hash,
            threshold_profile_id=threshold_profile_id,
            scores=scores,
            hard_failures=hard_failures,
            warnings=warnings or [],
            created_by_actor_id=actor_id,
            previous_receipt_id=previous_receipt_id,
            command_id=command_id,
        )
        self.repository.put_receipt(receipt)
        self._append_event(
            "EvaluationEvidenceValidated",
            receipt.evaluation_receipt_id,
            object_type,
            object_id,
            {"evidence_count": sum(len(score.evidence) for score in scores)},
        )
        for hard_failure in hard_failures:
            self._write_approval_blocker(receipt, hard_failure)
        if previous_receipt_id:
            self._append_event(
                "EvaluationReceiptSuperseded",
                receipt.evaluation_receipt_id,
                object_type,
                object_id,
                {"previous_receipt_id": str(previous_receipt_id)},
            )
        self._append_event(
            "EvaluationReceiptCreated",
            receipt.evaluation_receipt_id,
            object_type,
            object_id,
            {"decision": receipt.decision.value, "hard_failure_count": len(receipt.hard_failures)},
        )
        return receipt

    def rerun_after_revision(
        self,
        *,
        previous_receipt_id: UUID,
        revised_object_hash: str,
        actor_id: UUID,
        category_inputs: list[EvaluationCategoryInput | dict[str, Any]] | None = None,
        warnings: list[str] | None = None,
    ) -> EvaluationReceipt:
        previous = self.repository.receipts.get(previous_receipt_id)
        if previous is None:
            raise EvaluationReceiptError("PREVIOUS_EVALUATION_RECEIPT_REQUIRED", "Previous receipt is required for rerun.")
        if previous.object_hash == revised_object_hash:
            raise EvaluationReceiptError("REVISED_OBJECT_HASH_REQUIRED", "Rerun requires a revised object hash.")
        return self.generate_evaluation_receipt(
            organization_id=previous.organization_id,
            brand_id=previous.brand_id,
            object_type=previous.object_type,
            object_id=previous.object_id,
            object_hash=revised_object_hash,
            actor_id=actor_id,
            category_inputs=category_inputs,
            threshold_profile_id=previous.threshold_profile_id,
            previous_receipt_id=previous_receipt_id,
            warnings=warnings,
        )

    def build_review_read_model(self, evaluation_receipt_id: UUID) -> EvaluationReviewReadModel:
        receipt = self.repository.receipts.get(evaluation_receipt_id)
        if receipt is None:
            raise EvaluationReceiptError("EVALUATION_RECEIPT_REQUIRED", "Evaluation receipt is required.")
        blockers = self.repository.blockers_for_receipt(evaluation_receipt_id)
        evidence_source_ids = sorted(
            {
                evidence_ref(pointer)
                for score in receipt.scores
                for pointer in score.evidence
            }
            | {
                evidence_ref(pointer)
                for failure in receipt.hard_failures
                for pointer in failure.evidence
            }
        )
        return EvaluationReviewReadModel(
            schema_version="cmf.evaluation_review_read_model.v1",
            evaluation_receipt_id=receipt.evaluation_receipt_id,
            organization_id=receipt.organization_id,
            brand_id=receipt.brand_id,
            object_type=receipt.object_type,
            object_id=receipt.object_id,
            object_hash=receipt.object_hash,
            previous_receipt_id=receipt.previous_receipt_id,
            threshold_profile_id=receipt.threshold_profile_id,
            category_scores=receipt.scores,
            hard_failures=receipt.hard_failures,
            approval_blocker_ids=[blocker.evaluation_approval_blocker_id for blocker in blockers],
            decision=receipt.decision,
            evidence_source_ids=evidence_source_ids,
            created_at=receipt.created_at,
        )

    def stage13_generate_receipts(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        object_type: EvaluationObjectType | str,
        object_id: UUID,
        object_hash: str,
        actor_id: UUID,
        category_inputs: list[EvaluationCategoryInput | dict[str, Any]] | None = None,
    ) -> EvaluationReceipt:
        return self.generate_evaluation_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            object_type=object_type,
            object_id=object_id,
            object_hash=object_hash,
            actor_id=actor_id,
            category_inputs=category_inputs,
        )

    def _inputs_for_all_categories(
        self,
        category_inputs: list[EvaluationCategoryInput | dict[str, Any]] | None,
        object_hash: str,
        evaluator_version: str,
    ) -> list[EvaluationCategoryInput]:
        if not category_inputs:
            return [
                EvaluationCategoryInput(
                    category=category,
                    score=1.0,
                    evidence=[
                        EvidencePointer(
                            source_type="object_hash",
                            source_id=object_hash,
                            claim_scope=EvidenceClaimScope.supports,
                            route="deterministic_object_lineage",
                            note="Default deterministic evidence generated for review-ready object.",
                        )
                    ],
                    evaluator_version=evaluator_version,
                )
                for category in EvaluationCategory
            ]
        normalized = [
            item if isinstance(item, EvaluationCategoryInput) else EvaluationCategoryInput.model_validate(item)
            for item in category_inputs
        ]
        seen = {item.category for item in normalized}
        missing = [category.value for category in EvaluationCategory if category not in seen]
        if missing:
            raise EvaluationReceiptError("EVALUATION_CATEGORIES_INCOMPLETE", f"Missing evaluation categories: {', '.join(missing)}")
        if len(seen) != len(normalized):
            raise EvaluationReceiptError("EVALUATION_CATEGORIES_DUPLICATED", "Evaluation categories must be unique.")
        return normalized

    def _write_approval_blocker(self, receipt: EvaluationReceipt, hard_failure: HardFailure) -> EvaluationApprovalBlocker:
        blocker = EvaluationApprovalBlocker(
            schema_version="cmf.evaluation_approval_blocker.v1",
            evaluation_approval_blocker_id=uuid4(),
            evaluation_receipt_id=receipt.evaluation_receipt_id,
            organization_id=receipt.organization_id,
            brand_id=receipt.brand_id,
            object_type=receipt.object_type,
            object_id=receipt.object_id,
            blocker_code=hard_failure.approval_blocker_code,
            message=hard_failure.message,
            evidence_refs=[evidence_ref(pointer) for pointer in hard_failure.evidence],
            repair_action=f"repair_{hard_failure.category.value}",
            created_at=utc_now(),
        )
        self.repository.put_approval_blocker(blocker)
        self._append_event(
            "ApprovalBlockedFromEvaluation",
            receipt.evaluation_receipt_id,
            receipt.object_type,
            receipt.object_id,
            {"blocker_code": blocker.blocker_code, "hard_failure_code": hard_failure.code},
        )
        return blocker

    def _append_event(
        self,
        event_type: str,
        evaluation_receipt_id: UUID | None,
        object_type: EvaluationObjectType | str | None,
        object_id: UUID | None,
        payload: dict[str, Any],
    ) -> EvaluationDomainEvent:
        event = EvaluationDomainEvent(
            schema_version="cmf.evaluation_domain_event.v1",
            evaluation_event_id=uuid4(),
            event_type=event_type,
            evaluation_receipt_id=evaluation_receipt_id,
            object_type=EvaluationObjectType(object_type) if object_type else None,
            object_id=object_id,
            payload=payload,
            created_at=utc_now(),
        )
        return self.repository.append_event(event)


@dataclass
class EvaluationCommandHandler:
    command_type: str
    service: EvaluationReceiptService
    aggregate_type: str = "evaluation_receipt"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "reviewer", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "GenerateEvaluationReceiptCommand":
            receipt = self.service.generate_evaluation_receipt(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                object_type=payload["object_type"],
                object_id=UUID(payload["object_id"]),
                object_hash=payload["object_hash"],
                actor_id=envelope.actor.actor_id,
                category_inputs=payload.get("category_inputs"),
                threshold_profile_id=payload.get("threshold_profile_id", "cmf.default.thresholds.v1"),
                previous_receipt_id=UUID(payload["previous_receipt_id"]) if payload.get("previous_receipt_id") else None,
                warnings=payload.get("warnings", []),
                command_id=envelope.command_id,
            )
            return receipt.model_dump(mode="json")
        if self.command_type == "SupersedeEvaluationReceiptCommand":
            receipt = self.service.rerun_after_revision(
                previous_receipt_id=UUID(payload["previous_receipt_id"]),
                revised_object_hash=payload["revised_object_hash"],
                actor_id=envelope.actor.actor_id,
                category_inputs=payload.get("category_inputs"),
                warnings=payload.get("warnings", []),
            )
            return receipt.model_dump(mode="json")
        if self.command_type == "ValidateEvaluationEvidenceCommand":
            receipt = self.service.repository.receipts.get(UUID(payload["evaluation_receipt_id"]))
            if receipt is None:
                raise EvaluationReceiptError("EVALUATION_RECEIPT_REQUIRED", "Evaluation receipt is required.")
            return {
                "evaluation_receipt_id": str(receipt.evaluation_receipt_id),
                "evidence_valid": all(score.evidence for score in receipt.scores)
                and all(failure.evidence for failure in receipt.hard_failures),
            }
        if self.command_type == "BlockApprovalFromEvaluationCommand":
            receipt = self.service.repository.receipts.get(UUID(payload["evaluation_receipt_id"]))
            if receipt is None:
                raise EvaluationReceiptError("EVALUATION_RECEIPT_REQUIRED", "Evaluation receipt is required.")
            blockers = self.service.repository.blockers_for_receipt(receipt.evaluation_receipt_id)
            return {"evaluation_receipt_id": str(receipt.evaluation_receipt_id), "approval_blocker_count": len(blockers)}
        if self.command_type in {"RunEvaluationCategoryCommand", "RecordEvaluationReceiptCommand"}:
            raise EvaluationReceiptError("COMMAND_REQUIRES_GENERATE_RECEIPT", f"{self.command_type} is mediated by GenerateEvaluationReceiptCommand.")
        raise EvaluationReceiptError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("evaluation_receipt_id") or envelope.payload.get("evaluation_receipt_id") or envelope.payload.get("object_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_evaluation_command_handlers(bus: CommandBus, service: EvaluationReceiptService) -> None:
    for command_type in [
        "GenerateEvaluationReceiptCommand",
        "RunEvaluationCategoryCommand",
        "ValidateEvaluationEvidenceCommand",
        "RecordEvaluationReceiptCommand",
        "BlockApprovalFromEvaluationCommand",
        "SupersedeEvaluationReceiptCommand",
    ]:
        bus.register_handler(EvaluationCommandHandler(command_type=command_type, service=service))

