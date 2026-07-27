"""Evaluation workflow adapters for TS-CMF-050."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ccp_studio.contracts.evaluation_receipts import EvaluationObjectType, EvaluationReceipt
from ccp_studio.services.evaluation_receipt_service import EvaluationReceiptService


@dataclass
class EvaluationWorkflow:
    evaluation_service: EvaluationReceiptService

    def stage13_generate_receipts(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        object_type: EvaluationObjectType | str,
        object_id: UUID,
        object_hash: str,
        actor_id: UUID,
        category_inputs: list[dict[str, Any]] | None = None,
    ) -> EvaluationReceipt:
        return self.evaluation_service.stage13_generate_receipts(
            organization_id=organization_id,
            brand_id=brand_id,
            object_type=object_type,
            object_id=object_id,
            object_hash=object_hash,
            actor_id=actor_id,
            category_inputs=category_inputs,
        )

