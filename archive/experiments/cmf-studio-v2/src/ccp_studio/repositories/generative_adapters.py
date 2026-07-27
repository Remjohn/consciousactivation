"""Generative provider adapter repositories for TS-CMF-044."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.generative_adapters import (
    GenerativeAdapterReceipt,
    GenerativeProviderOutput,
    GenerativeProviderRequest,
)


@dataclass
class InMemoryGenerativeAdapterRepository:
    requests: dict[UUID, GenerativeProviderRequest] = field(default_factory=dict)
    outputs: dict[UUID, GenerativeProviderOutput] = field(default_factory=dict)
    receipts: dict[UUID, GenerativeAdapterReceipt] = field(default_factory=dict)
    idempotency_index: dict[tuple[UUID, UUID, str], UUID] = field(default_factory=dict)

    def put_request(self, request: GenerativeProviderRequest) -> GenerativeProviderRequest:
        self.requests[request.generative_provider_request_id] = request
        self.idempotency_index[(request.organization_id, request.brand_id, request.idempotency_key)] = request.generative_provider_request_id
        return request

    def put_output(self, output: GenerativeProviderOutput) -> GenerativeProviderOutput:
        self.outputs[output.provider_output_id] = output
        return output

    def put_receipt(self, receipt: GenerativeAdapterReceipt) -> GenerativeAdapterReceipt:
        self.receipts[receipt.generative_adapter_receipt_id] = receipt
        return receipt

    def request_for_idempotency(self, organization_id: UUID, brand_id: UUID, idempotency_key: str) -> GenerativeProviderRequest | None:
        request_id = self.idempotency_index.get((organization_id, brand_id, idempotency_key))
        return self.requests.get(request_id) if request_id else None
