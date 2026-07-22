"""Matrix of Edging repositories for TS-CMF-025."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.matrix import MatrixOfEdgingBrief, MatrixReceipt


@dataclass
class InMemoryMatrixRepository:
    briefs: dict[UUID, MatrixOfEdgingBrief] = field(default_factory=dict)
    receipts: dict[UUID, MatrixReceipt] = field(default_factory=dict)

    def put_brief(self, brief: MatrixOfEdgingBrief) -> MatrixOfEdgingBrief:
        self.briefs[brief.matrix_brief_id] = brief
        return brief

    def put_receipt(self, receipt: MatrixReceipt) -> MatrixReceipt:
        self.receipts[receipt.matrix_receipt_id] = receipt
        return receipt

    def receipts_for_brief(self, matrix_brief_id: UUID) -> list[MatrixReceipt]:
        return [receipt for receipt in self.receipts.values() if receipt.matrix_brief_id == matrix_brief_id]
