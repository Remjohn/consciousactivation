"""Execution-only external distribution for sealed CAE releases.

CA-M031 / FR-DIST-001 establishes a narrow delivery boundary:

* a :class:`ReleaseManifest` is verified before any destination call;
* adapters receive immutable release bytes, never semantic source objects or paths;
* only explicitly allow-listed technical transforms are publishable;
* semantic equivalence is checked by an independent verifier over source/output bytes;
* retries reuse one deterministic idempotency key and follow exponential backoff;
* every terminal delivery attempt produces a signed, auditable receipt; and
* successful idempotent replays return the original receipt without a second publish.

The module deliberately contains no outcome attribution, campaign lookup, or release
mutation. It consumes the Q29 release boundary and returns a downstream delivery
record only.
"""

from __future__ import annotations

import hashlib
import hmac
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from time import sleep
from typing import Any, Callable, Mapping, Protocol, Sequence, runtime_checkable
from uuid import uuid4

from ca_contracts import canonical_json_bytes, canonical_sha256

from .release_manifest import ReleaseManifest, ReleaseManifestIntegrityError

SCHEMA_VERSION = "ca-distribution-receipt/v1"
RECEIPT_SIGNATURE_ALGORITHM = "HMAC-SHA256"
SHA256_HEX_LENGTH = 64


class DistributionDeliveryError(RuntimeError):
    """Base class for fail-closed distribution errors."""


class DistributionValidationError(DistributionDeliveryError, ValueError):
    """Raised for malformed or internally inconsistent delivery inputs."""


class DistributionIntegrityError(DistributionDeliveryError):
    """Raised when the sealed release or delivery package fails integrity checks."""


class DistributionAuthorizationError(DistributionDeliveryError):
    """Raised when a destination or transformation is not explicitly eligible."""


class DistributionIdempotencyConflictError(DistributionDeliveryError):
    """Raised when an idempotency key is reused for different delivery content."""


class UnsupportedSemanticTransformationError(DistributionAuthorizationError):
    """Raised when an adapter attempts an unapproved semantic transformation."""


class RetryableDeliveryError(DistributionDeliveryError):
    """Raised by adapters when a publish attempt is safely retryable."""


class DistributionPublishError(DistributionDeliveryError):
    """Raised for terminal publication failures."""


class DeliveryStatus(str, Enum):
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"


class TransformationClass(str, Enum):
    IDENTITY = "IDENTITY"
    CONTAINER = "CONTAINER"
    CODEC = "CODEC"


@dataclass(frozen=True, slots=True)
class DistributionDestination:
    """Immutable destination declaration consumed by an adapter."""

    destination_id: str
    destination_type: str
    endpoint: str
    allowed_transformations: frozenset[str] = frozenset({TransformationClass.IDENTITY.value})
    configuration: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.destination_id, "destination_id")
        _require_text(self.destination_type, "destination_type")
        _require_text(self.endpoint, "endpoint")
        allowed = frozenset(str(value).upper() for value in self.allowed_transformations)
        if not allowed:
            raise DistributionValidationError("allowed_transformations must not be empty")
        unknown = allowed.difference({item.value for item in TransformationClass})
        if unknown:
            raise DistributionValidationError(
                f"unsupported transformation classes in destination configuration: {sorted(unknown)}"
            )
        object.__setattr__(self, "allowed_transformations", allowed)
        if not isinstance(self.configuration, Mapping):
            raise DistributionValidationError("destination configuration must be a mapping")
        object.__setattr__(self, "configuration", dict(self.configuration))

    @property
    def configuration_digest(self) -> str:
        return canonical_sha256(
            {
                "destination_id": self.destination_id,
                "destination_type": self.destination_type,
                "endpoint": self.endpoint,
                "allowed_transformations": sorted(self.allowed_transformations),
                "configuration": dict(self.configuration),
            }
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "destination_id": self.destination_id,
            "destination_type": self.destination_type,
            "endpoint": self.endpoint,
            "allowed_transformations": sorted(self.allowed_transformations),
            "configuration_digest": self.configuration_digest,
        }


@dataclass(frozen=True, slots=True)
class SealedReleaseArtifact:
    """Read-only bytes for one manifest artifact; filesystem paths stay internal."""

    artifact_id: str
    logical_uri: str
    kind: str
    source_sha256: str
    source_bytes: bytes
    byte_length: int

    def __post_init__(self) -> None:
        _require_sha256(self.source_sha256, "source_sha256")
        if not isinstance(self.source_bytes, bytes):
            raise DistributionValidationError("source_bytes must be immutable bytes")
        if len(self.source_bytes) != self.byte_length:
            raise DistributionIntegrityError(
                f"artifact {self.logical_uri!r} length changed before delivery"
            )
        actual = hashlib.sha256(self.source_bytes).hexdigest()
        if not hmac.compare_digest(actual, self.source_sha256):
            raise DistributionIntegrityError(
                f"artifact {self.logical_uri!r} bytes do not match the sealed release digest"
            )


@dataclass(frozen=True, slots=True)
class SealedReleasePackage:
    """Adapter input containing only immutable release identity and artifact bytes."""

    release_id: str
    release_version: str
    release_manifest_sha256: str
    merkle_root_sha256: str
    artifacts: tuple[SealedReleaseArtifact, ...]

    def __post_init__(self) -> None:
        _require_text(self.release_id, "release_id")
        _require_text(self.release_version, "release_version")
        _require_sha256(self.release_manifest_sha256, "release_manifest_sha256")
        _require_sha256(self.merkle_root_sha256, "merkle_root_sha256")
        if not self.artifacts:
            raise DistributionValidationError("sealed release package must contain artifacts")
        artifact_ids = [artifact.artifact_id for artifact in self.artifacts]
        if len(artifact_ids) != len(set(artifact_ids)):
            raise DistributionValidationError("sealed release package contains duplicate artifact ids")
        object.__setattr__(self, "artifacts", tuple(self.artifacts))

    @property
    def artifact_map(self) -> Mapping[str, SealedReleaseArtifact]:
        return {artifact.artifact_id: artifact for artifact in self.artifacts}


@dataclass(frozen=True, slots=True)
class AdaptedArtifact:
    """Destination-specific bytes plus an independently checked semantic projection."""

    artifact_id: str
    delivered_bytes: bytes
    transformation_class: str
    semantic_source_bytes: bytes
    semantic_delivered_bytes: bytes

    def __post_init__(self) -> None:
        _require_text(self.artifact_id, "artifact_id")
        if not isinstance(self.delivered_bytes, bytes):
            raise DistributionValidationError("delivered_bytes must be immutable bytes")
        if not isinstance(self.semantic_source_bytes, bytes):
            raise DistributionValidationError("semantic_source_bytes must be immutable bytes")
        if not isinstance(self.semantic_delivered_bytes, bytes):
            raise DistributionValidationError("semantic_delivered_bytes must be immutable bytes")
        normalized = str(self.transformation_class).upper()
        object.__setattr__(self, "transformation_class", normalized)
        if normalized.startswith("SEMANTIC") or normalized not in {item.value for item in TransformationClass}:
            raise UnsupportedSemanticTransformationError(
                f"adapter returned unsupported transformation class: {self.transformation_class!r}"
            )


@dataclass(frozen=True, slots=True)
class PublishResponse:
    """Transport response from a destination adapter."""

    response_id: str
    accepted: bool
    retryable: bool = False
    remote_receipt: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.response_id, "response_id")
        if not isinstance(self.accepted, bool) or not isinstance(self.retryable, bool):
            raise DistributionValidationError("accepted and retryable must be booleans")
        if not isinstance(self.remote_receipt, Mapping):
            raise DistributionValidationError("remote_receipt must be a mapping")
        object.__setattr__(self, "remote_receipt", dict(self.remote_receipt))


@runtime_checkable
class DistributionAdapter(Protocol):
    """Narrow adapter contract: adapt immutable bytes, then publish by idempotency key."""

    adapter_id: str
    adapter_version: str

    def adapt(
        self,
        package: SealedReleasePackage,
        *,
        destination: DistributionDestination,
    ) -> Sequence[AdaptedArtifact]:
        """Apply destination transformations without mutating package inputs."""

    def publish(
        self,
        payload: Sequence[AdaptedArtifact],
        *,
        package: SealedReleasePackage,
        destination: DistributionDestination,
        idempotency_key: str,
    ) -> PublishResponse:
        """Publish adapted bytes using the supplied stable idempotency key."""


SemanticFingerprint = Callable[[str, bytes], bytes]
Clock = Callable[[], str]
Sleeper = Callable[[float], None]


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """Bounded exponential-backoff policy."""

    max_attempts: int = 3
    initial_delay_seconds: float = 1.0
    multiplier: float = 2.0
    max_delay_seconds: float = 30.0

    def __post_init__(self) -> None:
        if not isinstance(self.max_attempts, int) or self.max_attempts < 1:
            raise DistributionValidationError("max_attempts must be >= 1")
        if self.initial_delay_seconds < 0:
            raise DistributionValidationError("initial_delay_seconds must be >= 0")
        if self.multiplier < 1:
            raise DistributionValidationError("multiplier must be >= 1")
        if self.max_delay_seconds < 0:
            raise DistributionValidationError("max_delay_seconds must be >= 0")

    def delay_before_retry(self, attempt_number: int) -> float:
        if attempt_number < 1:
            raise DistributionValidationError("attempt_number must be >= 1")
        return min(
            self.max_delay_seconds,
            self.initial_delay_seconds * (self.multiplier ** (attempt_number - 1)),
        )


@dataclass(frozen=True, slots=True)
class DeliveryAttempt:
    attempt_number: int
    started_at: str
    completed_at: str
    status: str
    retryable: bool
    response_id: str | None = None
    error_type: str | None = None
    error_message: str | None = None
    backoff_millis: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "attempt_number": self.attempt_number,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "status": self.status,
            "retryable": self.retryable,
            "response_id": self.response_id,
            "error_type": self.error_type,
            "error_message": self.error_message,
            "backoff_millis": self.backoff_millis,
        }


@dataclass(frozen=True, slots=True)
class DeliveryArtifactReceipt:
    artifact_id: str
    logical_uri: str
    source_sha256: str
    delivered_sha256: str
    transformation_class: str
    semantic_source_sha256: str
    semantic_delivered_sha256: str

    def to_dict(self) -> dict[str, str]:
        return {
            "artifact_id": self.artifact_id,
            "logical_uri": self.logical_uri,
            "source_sha256": self.source_sha256,
            "delivered_sha256": self.delivered_sha256,
            "transformation_class": self.transformation_class,
            "semantic_source_sha256": self.semantic_source_sha256,
            "semantic_delivered_sha256": self.semantic_delivered_sha256,
        }


@dataclass(frozen=True, slots=True)
class DeliveryReceipt:
    """Signed terminal record for one delivery invocation."""

    receipt_id: str
    release_id: str
    release_version: str
    release_manifest_sha256: str
    merkle_root_sha256: str
    destination_id: str
    destination_type: str
    destination_endpoint: str
    destination_configuration_digest: str
    destination_allowed_transformations: tuple[str, ...]
    adapter_id: str
    adapter_version: str
    idempotency_key: str
    request_fingerprint: str
    delivery_status: DeliveryStatus
    attempts: tuple[DeliveryAttempt, ...]
    artifacts: tuple[DeliveryArtifactReceipt, ...]
    remote_response_ids: tuple[str, ...]
    remote_receipt: Mapping[str, Any]
    supersedes_receipt_id: str | None
    receipt_sha256: str
    signature_algorithm: str
    signature: str
    created_at: str

    def unsigned_payload(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "receipt_id": self.receipt_id,
            "release_id": self.release_id,
            "release_version": self.release_version,
            "release_manifest_sha256": self.release_manifest_sha256,
            "merkle_root_sha256": self.merkle_root_sha256,
            "destination": {
                "destination_id": self.destination_id,
                "destination_type": self.destination_type,
                "endpoint": self.destination_endpoint,
                "configuration_digest": self.destination_configuration_digest,
                "allowed_transformations": list(self.destination_allowed_transformations),
            },
            "adapter": {
                "adapter_id": self.adapter_id,
                "adapter_version": self.adapter_version,
            },
            "idempotency_key": self.idempotency_key,
            "request_fingerprint": self.request_fingerprint,
            "delivery_status": self.delivery_status.value,
            "attempts": [attempt.to_dict() for attempt in self.attempts],
            "artifacts": [artifact.to_dict() for artifact in self.artifacts],
            "remote_response_ids": list(self.remote_response_ids),
            "remote_receipt": dict(self.remote_receipt),
            "supersedes_receipt_id": self.supersedes_receipt_id,
            "created_at": self.created_at,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            **self.unsigned_payload(),
            "receipt_sha256": self.receipt_sha256,
            "signature_algorithm": self.signature_algorithm,
            "signature": self.signature,
        }

    def verify(self, signing_secret: bytes | str) -> None:
        secret = _normalize_secret(signing_secret, "receipt signing secret")
        expected_digest = canonical_sha256(self.unsigned_payload())
        if not hmac.compare_digest(expected_digest, self.receipt_sha256):
            raise DistributionIntegrityError("delivery receipt digest mismatch")
        expected_signature = hmac.new(
            secret,
            canonical_json_bytes({**self.unsigned_payload(), "receipt_sha256": expected_digest}),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(expected_signature, self.signature):
            raise DistributionIntegrityError("delivery receipt signature mismatch")


@dataclass(frozen=True, slots=True)
class DeliveryResult:
    receipt: DeliveryReceipt
    deduplicated: bool


class DeliveryLedger:
    """Thread-safe local receipt ledger with stable idempotency records.

    A deployment that needs durable persistence can mirror these immutable receipts
    into the existing runtime receipt store. The ledger itself never mutates a prior
    receipt and rejects a key collision whose request fingerprint differs.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._receipts_by_key: dict[str, list[DeliveryReceipt]] = {}

    def latest(self, idempotency_key: str) -> DeliveryReceipt | None:
        with self._lock:
            records = self._receipts_by_key.get(idempotency_key)
            return records[-1] if records else None

    def history(self, idempotency_key: str) -> tuple[DeliveryReceipt, ...]:
        with self._lock:
            return tuple(self._receipts_by_key.get(idempotency_key, ()))

    def assert_compatible(self, idempotency_key: str, request_fingerprint: str) -> None:
        with self._lock:
            records = self._receipts_by_key.get(idempotency_key, ())
            for receipt in records:
                if not hmac.compare_digest(receipt.request_fingerprint, request_fingerprint):
                    raise DistributionIdempotencyConflictError(
                        "idempotency key has already been used for a different delivery request"
                    )

    def append(self, receipt: DeliveryReceipt) -> None:
        with self._lock:
            self.assert_compatible(receipt.idempotency_key, receipt.request_fingerprint)
            self._receipts_by_key.setdefault(receipt.idempotency_key, []).append(receipt)


class ExternalDistributionClient:
    """Canonical execution-only delivery boundary."""

    def __init__(
        self,
        *,
        release_signing_secret: bytes | str,
        receipt_signing_secret: bytes | str,
        ledger: DeliveryLedger | None = None,
        retry_policy: RetryPolicy | None = None,
        sleeper: Sleeper = sleep,
        clock: Clock | None = None,
    ) -> None:
        self._release_signing_secret = _normalize_secret(release_signing_secret, "release signing secret")
        self._receipt_signing_secret = _normalize_secret(receipt_signing_secret, "receipt signing secret")
        self._ledger = ledger or DeliveryLedger()
        self._retry_policy = retry_policy or RetryPolicy()
        self._sleeper = sleeper
        self._clock = clock or _utc_now_rfc3339
        self._delivery_lock = threading.RLock()

    @property
    def ledger(self) -> DeliveryLedger:
        return self._ledger

    def deliver(
        self,
        manifest: ReleaseManifest,
        *,
        destination: DistributionDestination,
        adapter: DistributionAdapter,
        semantic_fingerprint: SemanticFingerprint,
        expected_artifact_paths: Mapping[str, str] | None = None,
    ) -> DeliveryResult:
        """Verify, adapt, publish, retry, sign, and record one sealed-release delivery."""

        self._validate_adapter_identity(adapter)
        self._verify_release(manifest, expected_artifact_paths=expected_artifact_paths)
        package = self._load_sealed_package(manifest, expected_artifact_paths=expected_artifact_paths)
        idempotency_key = self._make_idempotency_key(manifest, destination, adapter)
        request_fingerprint = self._make_request_fingerprint(manifest, destination, adapter)
        with self._delivery_lock:
            self._ledger.assert_compatible(idempotency_key, request_fingerprint)

            existing = self._ledger.latest(idempotency_key)
            if existing and existing.delivery_status is DeliveryStatus.DELIVERED:
                existing.verify(self._receipt_signing_secret)
                return DeliveryResult(receipt=existing, deduplicated=True)

            previous_receipt_id = existing.receipt_id if existing else None
            adapted = self._adapt_and_verify(
                package,
                destination=destination,
                adapter=adapter,
                semantic_fingerprint=semantic_fingerprint,
            )
            receipt = self._publish_with_retries(
                manifest,
                package,
                destination=destination,
                adapter=adapter,
                adapted=adapted,
                idempotency_key=idempotency_key,
                request_fingerprint=request_fingerprint,
                supersedes_receipt_id=previous_receipt_id,
            )
            self._ledger.append(receipt)
            receipt.verify(self._receipt_signing_secret)
            return DeliveryResult(receipt=receipt, deduplicated=False)

    def _verify_release(
        self,
        manifest: ReleaseManifest,
        *,
        expected_artifact_paths: Mapping[str, str] | None,
    ) -> None:
        try:
            manifest.verify(
                self._release_signing_secret,
                expected_artifact_paths=expected_artifact_paths,
            )
        except ReleaseManifestIntegrityError as exc:
            raise DistributionIntegrityError(
                f"release manifest verification failed; delivery blocked: {exc}"
            ) from exc

    def _load_sealed_package(
        self,
        manifest: ReleaseManifest,
        *,
        expected_artifact_paths: Mapping[str, str] | None,
    ) -> SealedReleasePackage:
        paths = expected_artifact_paths or {
            artifact.logical_uri: artifact.filesystem_path
            for artifact in manifest.artifacts
            if artifact.filesystem_path is not None
        }
        artifacts: list[SealedReleaseArtifact] = []
        for artifact in manifest.artifacts:
            path_value = paths.get(artifact.logical_uri)
            if path_value is None:
                raise DistributionIntegrityError(
                    f"no verified filesystem path for release artifact {artifact.logical_uri!r}"
                )
            try:
                with open(path_value, "rb") as handle:
                    source_bytes = handle.read()
            except OSError as exc:
                raise DistributionIntegrityError(
                    f"unable to read sealed release artifact {artifact.logical_uri!r}"
                ) from exc
            artifacts.append(
                SealedReleaseArtifact(
                    artifact_id=artifact.artifact_id,
                    logical_uri=artifact.logical_uri,
                    kind=artifact.kind,
                    source_sha256=artifact.sha256,
                    source_bytes=source_bytes,
                    byte_length=artifact.byte_length,
                )
            )
        return SealedReleasePackage(
            release_id=manifest.release_id,
            release_version=manifest.release_version,
            release_manifest_sha256=manifest.manifest_sha256,
            merkle_root_sha256=manifest.merkle_root_sha256,
            artifacts=tuple(artifacts),
        )

    def _adapt_and_verify(
        self,
        package: SealedReleasePackage,
        *,
        destination: DistributionDestination,
        adapter: DistributionAdapter,
        semantic_fingerprint: SemanticFingerprint,
    ) -> tuple[AdaptedArtifact, ...]:
        try:
            adapted = tuple(adapter.adapt(package, destination=destination))
        except UnsupportedSemanticTransformationError:
            raise
        except Exception as exc:
            raise DistributionDeliveryError(f"distribution adapter adaptation failed: {exc}") from exc

        expected_ids = set(package.artifact_map)
        actual_ids = [item.artifact_id for item in adapted]
        if len(actual_ids) != len(set(actual_ids)):
            raise DistributionIntegrityError("adapter returned duplicate artifact ids")
        if set(actual_ids) != expected_ids:
            raise DistributionIntegrityError(
                "adapter output does not cover exactly the sealed release artifact set"
            )

        for item in adapted:
            if item.transformation_class not in destination.allowed_transformations:
                raise UnsupportedSemanticTransformationError(
                    f"destination {destination.destination_id!r} does not allow transformation "
                    f"{item.transformation_class!r}"
                )
            source_artifact = package.artifact_map[item.artifact_id]
            if hashlib.sha256(source_artifact.source_bytes).hexdigest() != source_artifact.source_sha256:
                raise DistributionIntegrityError(
                    f"source bytes for artifact {item.artifact_id!r} no longer match the sealed manifest"
                )
            source_semantic_digest = hashlib.sha256(
                semantic_fingerprint(source_artifact.kind, source_artifact.source_bytes)
            ).hexdigest()
            adapted_semantic_digest = hashlib.sha256(
                semantic_fingerprint(source_artifact.kind, item.delivered_bytes)
            ).hexdigest()
            declared_source_digest = hashlib.sha256(item.semantic_source_bytes).hexdigest()
            declared_delivered_digest = hashlib.sha256(item.semantic_delivered_bytes).hexdigest()
            if not hmac.compare_digest(source_semantic_digest, declared_source_digest):
                raise DistributionIntegrityError(
                    f"adapter semantic source projection does not match canonical verifier for {item.artifact_id!r}"
                )
            if not hmac.compare_digest(adapted_semantic_digest, declared_delivered_digest):
                raise DistributionIntegrityError(
                    f"adapter semantic output projection does not match canonical verifier for {item.artifact_id!r}"
                )
            if not hmac.compare_digest(source_semantic_digest, adapted_semantic_digest):
                raise DistributionIntegrityError(
                    f"semantic payload changed for artifact {item.artifact_id!r}; distribution fails closed"
                )
        return adapted

    def _publish_with_retries(
        self,
        manifest: ReleaseManifest,
        package: SealedReleasePackage,
        *,
        destination: DistributionDestination,
        adapter: DistributionAdapter,
        adapted: Sequence[AdaptedArtifact],
        idempotency_key: str,
        request_fingerprint: str,
        supersedes_receipt_id: str | None,
    ) -> DeliveryReceipt:
        attempts: list[DeliveryAttempt] = []
        remote_response_ids: list[str] = []
        remote_receipt: Mapping[str, Any] = {}
        response_success = False
        receipt_error: Exception | None = None

        for attempt_number in range(1, self._retry_policy.max_attempts + 1):
            started_at = self._clock()
            backoff = 0.0
            try:
                response = adapter.publish(
                    tuple(adapted),
                    package=package,
                    destination=destination,
                    idempotency_key=idempotency_key,
                )
                remote_response_ids.append(response.response_id)
                remote_receipt = dict(response.remote_receipt)
                if not response.accepted:
                    error = DistributionPublishError(
                        f"destination rejected delivery for response {response.response_id!r}"
                    )
                    retryable = bool(response.retryable)
                    if retryable and attempt_number < self._retry_policy.max_attempts:
                        backoff = self._retry_policy.delay_before_retry(attempt_number)
                        attempts.append(
                            DeliveryAttempt(
                                attempt_number=attempt_number,
                                started_at=started_at,
                                completed_at=self._clock(),
                                status="RETRYING",
                                retryable=True,
                                response_id=response.response_id,
                                error_type=type(error).__name__,
                                error_message=str(error),
                                backoff_millis=_delay_to_millis(backoff),
                            )
                        )
                        self._sleeper(backoff)
                        continue
                    receipt_error = error
                    attempts.append(
                        DeliveryAttempt(
                            attempt_number=attempt_number,
                            started_at=started_at,
                            completed_at=self._clock(),
                            status="FAILED",
                            retryable=retryable,
                            response_id=response.response_id,
                            error_type=type(error).__name__,
                            error_message=str(error),
                        )
                    )
                    break

                attempts.append(
                    DeliveryAttempt(
                        attempt_number=attempt_number,
                        started_at=started_at,
                        completed_at=self._clock(),
                        status="DELIVERED",
                        retryable=False,
                        response_id=response.response_id,
                    )
                )
                response_success = True
                break
            except Exception as exc:
                retryable = isinstance(exc, (RetryableDeliveryError, TimeoutError, ConnectionError))
                if retryable and attempt_number < self._retry_policy.max_attempts:
                    backoff = self._retry_policy.delay_before_retry(attempt_number)
                    attempts.append(
                        DeliveryAttempt(
                            attempt_number=attempt_number,
                            started_at=started_at,
                            completed_at=self._clock(),
                            status="RETRYING",
                            retryable=True,
                            error_type=type(exc).__name__,
                            error_message=str(exc),
                            backoff_millis=_delay_to_millis(backoff),
                        )
                    )
                    self._sleeper(backoff)
                    continue
                receipt_error = exc
                attempts.append(
                    DeliveryAttempt(
                        attempt_number=attempt_number,
                        started_at=started_at,
                        completed_at=self._clock(),
                        status="FAILED",
                        retryable=retryable,
                        error_type=type(exc).__name__,
                        error_message=str(exc),
                    )
                )
                break

        artifact_receipts = tuple(
            DeliveryArtifactReceipt(
                artifact_id=item.artifact_id,
                logical_uri=package.artifact_map[item.artifact_id].logical_uri,
                source_sha256=package.artifact_map[item.artifact_id].source_sha256,
                delivered_sha256=hashlib.sha256(item.delivered_bytes).hexdigest(),
                transformation_class=item.transformation_class,
                semantic_source_sha256=hashlib.sha256(item.semantic_source_bytes).hexdigest(),
                semantic_delivered_sha256=hashlib.sha256(item.semantic_delivered_bytes).hexdigest(),
            )
            for item in adapted
        )
        receipt = self._build_receipt(
            manifest,
            destination=destination,
            adapter=adapter,
            idempotency_key=idempotency_key,
            request_fingerprint=request_fingerprint,
            status=DeliveryStatus.DELIVERED if response_success else DeliveryStatus.FAILED,
            attempts=tuple(attempts),
            artifacts=artifact_receipts,
            remote_response_ids=tuple(remote_response_ids),
            remote_receipt=remote_receipt,
            supersedes_receipt_id=supersedes_receipt_id,
        )
        if receipt_error is not None and not response_success:
            return receipt
        return receipt

    def _build_receipt(
        self,
        manifest: ReleaseManifest,
        *,
        destination: DistributionDestination,
        adapter: DistributionAdapter,
        idempotency_key: str,
        request_fingerprint: str,
        status: DeliveryStatus,
        attempts: tuple[DeliveryAttempt, ...],
        artifacts: tuple[DeliveryArtifactReceipt, ...],
        remote_response_ids: tuple[str, ...],
        remote_receipt: Mapping[str, Any],
        supersedes_receipt_id: str | None,
    ) -> DeliveryReceipt:
        receipt_id = f"dist_rcpt_{uuid4().hex}"
        created_at = self._clock()
        unsigned = {
            "schema_version": SCHEMA_VERSION,
            "receipt_id": receipt_id,
            "release_id": manifest.release_id,
            "release_version": manifest.release_version,
            "release_manifest_sha256": manifest.manifest_sha256,
            "merkle_root_sha256": manifest.merkle_root_sha256,
            "destination": {
                "destination_id": destination.destination_id,
                "destination_type": destination.destination_type,
                "endpoint": destination.endpoint,
                "allowed_transformations": sorted(destination.allowed_transformations),
                "configuration_digest": destination.configuration_digest,
            },
            "adapter": {
                "adapter_id": str(adapter.adapter_id),
                "adapter_version": str(adapter.adapter_version),
            },
            "idempotency_key": idempotency_key,
            "request_fingerprint": request_fingerprint,
            "delivery_status": status.value,
            "attempts": [attempt.to_dict() for attempt in attempts],
            "artifacts": [artifact.to_dict() for artifact in artifacts],
            "remote_response_ids": list(remote_response_ids),
            "remote_receipt": dict(remote_receipt),
            "supersedes_receipt_id": supersedes_receipt_id,
            "created_at": created_at,
        }
        digest = canonical_sha256(unsigned)
        signature = hmac.new(
            self._receipt_signing_secret,
            canonical_json_bytes({**unsigned, "receipt_sha256": digest}),
            hashlib.sha256,
        ).hexdigest()
        return DeliveryReceipt(
            receipt_id=receipt_id,
            release_id=manifest.release_id,
            release_version=manifest.release_version,
            release_manifest_sha256=manifest.manifest_sha256,
            merkle_root_sha256=manifest.merkle_root_sha256,
            destination_id=destination.destination_id,
            destination_type=destination.destination_type,
            destination_endpoint=destination.endpoint,
            destination_configuration_digest=destination.configuration_digest,
            destination_allowed_transformations=tuple(sorted(destination.allowed_transformations)),
            adapter_id=str(adapter.adapter_id),
            adapter_version=str(adapter.adapter_version),
            idempotency_key=idempotency_key,
            request_fingerprint=request_fingerprint,
            delivery_status=status,
            attempts=attempts,
            artifacts=artifacts,
            remote_response_ids=remote_response_ids,
            remote_receipt=dict(remote_receipt),
            supersedes_receipt_id=supersedes_receipt_id,
            receipt_sha256=digest,
            signature_algorithm=RECEIPT_SIGNATURE_ALGORITHM,
            signature=signature,
            created_at=created_at,
        )

    @staticmethod
    def _validate_adapter_identity(adapter: DistributionAdapter) -> None:
        _require_text(getattr(adapter, "adapter_id", None), "adapter.adapter_id")
        _require_text(getattr(adapter, "adapter_version", None), "adapter.adapter_version")
        if not isinstance(adapter, DistributionAdapter):
            raise DistributionValidationError("adapter does not satisfy the distribution adapter contract")

    @staticmethod
    def _make_idempotency_key(
        manifest: ReleaseManifest,
        destination: DistributionDestination,
        adapter: DistributionAdapter,
    ) -> str:
        return canonical_sha256(
            {
                "purpose": "ca-m031-distribution",
                "release_manifest_sha256": manifest.manifest_sha256,
                "destination_id": destination.destination_id,
                "destination_configuration_digest": destination.configuration_digest,
                "adapter_id": str(adapter.adapter_id),
                "adapter_version": str(adapter.adapter_version),
            }
        )

    @staticmethod
    def _make_request_fingerprint(
        manifest: ReleaseManifest,
        destination: DistributionDestination,
        adapter: DistributionAdapter,
    ) -> str:
        return canonical_sha256(
            {
                "release_id": manifest.release_id,
                "release_version": manifest.release_version,
                "release_manifest_sha256": manifest.manifest_sha256,
                "merkle_root_sha256": manifest.merkle_root_sha256,
                "destination": destination.to_dict(),
                "adapter_id": str(adapter.adapter_id),
                "adapter_version": str(adapter.adapter_version),
            }
        )


def _require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DistributionValidationError(f"{field} must be a non-empty string")
    return value


def _require_sha256(value: Any, field: str) -> str:
    value = _require_text(value, field).lower()
    if len(value) != SHA256_HEX_LENGTH or any(char not in "0123456789abcdef" for char in value):
        raise DistributionValidationError(f"{field} must be a lowercase SHA-256 hex digest")
    return value


def _normalize_secret(value: bytes | str, field: str) -> bytes:
    if isinstance(value, str):
        value = value.encode("utf-8")
    if not isinstance(value, bytes) or not value:
        raise DistributionValidationError(f"{field} must be non-empty bytes")
    return value


def _delay_to_millis(seconds: float) -> int:
    if seconds < 0:
        raise DistributionValidationError("backoff delay cannot be negative")
    return int(round(seconds * 1000))


def _utc_now_rfc3339() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
