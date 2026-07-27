from __future__ import annotations

import hashlib
import json
import os
from typing import Protocol

from ccp_studio.contracts.provider_adapters import (
    ProviderAdapterConfig,
    ProviderAdapterHealth,
    ProviderCostEstimate,
    ProviderExecutionRequest,
    ProviderExecutionStatus,
    ProviderId,
    ProviderPollReceipt,
    ProviderPreflightReport,
    ProviderSubmissionReceipt,
    ProviderCapabilityId,
    ProviderOutputAsset,
    ProviderJobReceipt,
    ProviderErrorCode,
)


class ProviderAdapter(Protocol):
    provider_id: ProviderId
    capability_ids: list[ProviderCapabilityId]

    def validate(self, request: ProviderExecutionRequest) -> ProviderPreflightReport: ...
    def estimate(self, request: ProviderExecutionRequest) -> ProviderCostEstimate: ...
    def submit(self, request: ProviderExecutionRequest) -> ProviderSubmissionReceipt: ...
    def poll(self, request: ProviderExecutionRequest, submission: ProviderSubmissionReceipt) -> ProviderPollReceipt: ...
    def download_outputs(self, request: ProviderExecutionRequest, poll: ProviderPollReceipt) -> list[ProviderOutputAsset]: ...
    def normalize(self, request: ProviderExecutionRequest, submission: ProviderSubmissionReceipt, poll: ProviderPollReceipt, outputs: list[ProviderOutputAsset]) -> ProviderJobReceipt: ...
    def cancel(self, provider_request_id: str) -> bool: ...


class BaseProviderAdapter:
    provider_id: ProviderId
    capability_ids: list[ProviderCapabilityId] = []

    def __init__(self, config: ProviderAdapterConfig):
        self.config = config

    def validate(self, request: ProviderExecutionRequest) -> ProviderPreflightReport:
        missing: list[str] = []
        blockers: list[ProviderErrorCode] = []

        if request.provider_id != self.provider_id:
            missing.append("matching_provider_id")
            blockers.append(ProviderErrorCode.BAD_REQUEST)
        if request.provider_capability_id not in self.capability_ids:
            missing.append("supported_capability")
            blockers.append(ProviderErrorCode.BAD_REQUEST)
        if not self.config.enabled:
            missing.append("provider_enabled")
            blockers.append(ProviderErrorCode.PROVIDER_DISABLED)
        if self.config.credential_ref and not os.getenv(self.config.credential_ref.env_var_name):
            missing.append(self.config.credential_ref.env_var_name)
            blockers.append(ProviderErrorCode.MISSING_CREDENTIALS)
        if not request.idempotency_key:
            missing.append("idempotency_key")
            blockers.append(ProviderErrorCode.BAD_REQUEST)

        return ProviderPreflightReport(
            request_id=request.provider_execution_request_id,
            provider_id=self.provider_id,
            capability_id=request.provider_capability_id,
            pass_status=not missing,
            missing_requirements=missing,
            blocker_codes=blockers,
        )

    def estimate(self, request: ProviderExecutionRequest) -> ProviderCostEstimate:
        return ProviderCostEstimate(
            request_id=request.provider_execution_request_id,
            provider_id=self.provider_id,
            estimated_cost_usd=None,
            estimated_units=1,
            notes="V1 estimate placeholder; replace with provider cost registry.",
        )

    def _payload_hash(self, payload: dict) -> str:
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    def health(self) -> ProviderAdapterHealth:
        credential_present = True
        if self.config.credential_ref:
            credential_present = bool(os.getenv(self.config.credential_ref.env_var_name))
        return ProviderAdapterHealth(
            provider_id=self.provider_id,
            enabled=self.config.enabled,
            configured=bool(self.config.base_url or self.config.transport_mode.value in {"fake", "local"}),
            credential_present=credential_present,
        )

    def cancel(self, provider_request_id: str) -> bool:
        return False

    def normalize(self, request, submission, poll, outputs):
        return ProviderJobReceipt(
            request_id=request.provider_execution_request_id,
            provider_id=self.provider_id,
            provider_capability_id=request.provider_capability_id,
            provider_request_id=submission.provider_request_id,
            status=ProviderExecutionStatus.SUCCEEDED if outputs else ProviderExecutionStatus.FAILED,
            output_assets=outputs,
            submission_receipt_id=submission.provider_submission_receipt_id,
            poll_receipt_id=poll.provider_poll_receipt_id,
            route_production_spec_id=request.route_production_spec_id,
            provider_job_blueprint_id=request.provider_job_blueprint_id,
            primary_style_route_id=request.primary_style_route_id,
            frame_profile=request.frame_profile,
            composition_role=request.composition_role,
        )
