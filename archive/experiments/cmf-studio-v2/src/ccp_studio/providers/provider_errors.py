from __future__ import annotations

from ccp_studio.contracts.provider_adapters import (
    ProviderErrorCode,
    ProviderErrorReceipt,
    ProviderId,
    RetryDecision,
)


def normalize_provider_error(
    *,
    provider_id: ProviderId,
    message: str,
    request_id: str | None = None,
    provider_request_id: str | None = None,
    status_code: int | None = None,
    provider_error_code: str | None = None,
    raw_error_redacted: dict | None = None,
) -> ProviderErrorReceipt:
    normalized = ProviderErrorCode.UNKNOWN
    retryable = False
    user_correctable = False
    safe_to_retry = False
    retry_decision = RetryDecision.DO_NOT_RETRY

    text = f"{provider_error_code or ''} {message}".lower()
    if status_code == 401 or "auth" in text:
        normalized = ProviderErrorCode.AUTH_FAILED
        user_correctable = True
    elif status_code == 429 or "rate" in text:
        normalized = ProviderErrorCode.RATE_LIMITED
        retryable = safe_to_retry = True
        retry_decision = RetryDecision.RETRY
    elif status_code and 500 <= status_code <= 599:
        normalized = ProviderErrorCode.SERVER_ERROR
        retryable = safe_to_retry = True
        retry_decision = RetryDecision.RETRY
    elif "timeout" in text:
        normalized = ProviderErrorCode.TIMEOUT
        retryable = safe_to_retry = True
        retry_decision = RetryDecision.RETRY
    elif "moderation" in text or "safety" in text:
        normalized = ProviderErrorCode.MODERATION_BLOCKED
        user_correctable = True
        retry_decision = RetryDecision.REPAIR_THEN_RETRY
    elif status_code == 400 or "bad request" in text:
        normalized = ProviderErrorCode.BAD_REQUEST
        user_correctable = True
        retry_decision = RetryDecision.REPAIR_THEN_RETRY

    return ProviderErrorReceipt(
        provider_id=provider_id,
        provider_request_id=provider_request_id,
        provider_status_code=status_code,
        provider_error_code=provider_error_code,
        normalized_error_code=normalized,
        retry_decision=retry_decision,
        retryable=retryable,
        user_correctable=user_correctable,
        safe_to_retry=safe_to_retry,
        message=message,
        request_id=request_id,
        raw_error_redacted=raw_error_redacted or {},
    )
