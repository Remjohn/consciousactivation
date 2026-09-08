"""Subject Constitution lifecycle and exception handling for CA-M003.

The module deliberately keeps the authoritative lifecycle bounded to this aggregate:
- a signed constitution is immutable and cryptographically self-verifying;
- exceptions are append-only evidence and never mutate the baseline;
- amendments require an explicit operator authority decision and evidence;
- each accepted amendment creates a new signed revision with parent lineage and a
  tamper-evident amendment receipt.

No model output is treated as an authority grant. The caller must present the
operator authority scope and the signing secret used by the trusted runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
import hmac
import json
from threading import RLock
from types import MappingProxyType
from typing import Any, Mapping, Sequence
from uuid import uuid4


MANDATE_ID = "CA-M003"
INVARIANT_ID = "INV-SUB-001"
AMENDMENT_AUTHORITY_SCOPE = "SUBJECT_CONSTITUTION_AMEND"
_SIGNATURE_PREFIX = "hmac-sha256:"


class SubjectConstitutionError(RuntimeError):
    """Base class for fail-closed Subject Constitution lifecycle errors."""


class ConstitutionAlreadyExistsError(SubjectConstitutionError):
    """Raised when a baseline already exists for a subject."""


class ConstitutionNotFoundError(SubjectConstitutionError):
    """Raised when a requested subject constitution does not exist."""


class ConstitutionImmutableError(SubjectConstitutionError):
    """Raised when a caller attempts an in-place mutation of signed state."""


class InvalidSignatureError(SubjectConstitutionError):
    """Raised when signed constitution or receipt integrity cannot be verified."""


class InvalidAmendmentError(SubjectConstitutionError):
    """Raised when an amendment packet violates the lifecycle contract."""


class StaleParentRevisionError(SubjectConstitutionError):
    """Raised when an amendment is based on a revision other than current."""


class UnauthorizedOperatorError(SubjectConstitutionError):
    """Raised when the proposed amendment lacks operator authority."""


class AmendmentAlreadyResolvedError(SubjectConstitutionError):
    """Raised when a pending amendment is approved or rejected twice."""


class ConstitutionExceptionType(str, Enum):
    """Governed causes that may require human review."""

    VOICE_DRIFT = "VOICE_DRIFT"
    FORBIDDEN_BOUNDARY = "FORBIDDEN_BOUNDARY"
    OTHER_GOVERNED = "OTHER_GOVERNED"


class AmendmentStatus(str, Enum):
    """Lifecycle state of an amendment packet."""

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class _AuthorityDecision(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidAmendmentError(f"{field_name} must be a non-empty string")
    return value.strip()


def _normalise_timestamp(value: str, field_name: str) -> str:
    value = _require_text(value, field_name)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InvalidAmendmentError(f"{field_name} must be RFC3339/ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise InvalidAmendmentError(f"{field_name} must include an explicit timezone")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _freeze_json_value(value: Any, field_name: str) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        return MappingProxyType({
            _require_text(str(key), f"{field_name}.key"): _freeze_json_value(item, f"{field_name}.{key}")
            for key, item in value.items()
        })
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json_value(item, f"{field_name}[]") for item in value)
    raise InvalidAmendmentError(f"{field_name} must contain only JSON-compatible values")


def _thaw_json_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _thaw_json_value(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw_json_value(item) for item in value]
    return value


def _freeze_mapping(value: Mapping[str, Any], field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise InvalidAmendmentError(f"{field_name} must be a mapping")
    frozen_value = _freeze_json_value(value, field_name)
    if not isinstance(frozen_value, Mapping):
        raise InvalidAmendmentError(f"{field_name} must be a JSON object")
    return frozen_value


def _freeze_sequence(values: Sequence[str], field_name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise InvalidAmendmentError(f"{field_name} must be a sequence of strings")
    result = tuple(_require_text(item, f"{field_name}[]") for item in values)
    return result


def _canonical_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _payload_hash(payload: Mapping[str, Any]) -> str:
    return sha256(_canonical_json(_thaw_json_value(payload)).encode("utf-8")).hexdigest()


def _sign(payload: Mapping[str, Any], secret: str) -> str:
    secret = _require_text(secret, "signing_secret")
    digest = hmac.new(
        secret.encode("utf-8"),
        _canonical_json(_thaw_json_value(payload)).encode("utf-8"),
        sha256,
    ).hexdigest()
    return f"{_SIGNATURE_PREFIX}{digest}"


def _verify(payload: Mapping[str, Any], signature: str, secret: str) -> bool:
    expected = _sign(payload, secret)
    return hmac.compare_digest(expected, signature)


def _mint_signed_constitution(
    *,
    subject_id: str,
    revision: int,
    status: str,
    source_evidence_refs: Sequence[str],
    voice_characteristics: Mapping[str, Any],
    boundaries: Mapping[str, Any],
    validation_state: Mapping[str, Any],
    signed_by_operator_id: str,
    signed_at_utc: str,
    content_sha256: str,
    signing_secret: str,
    parent_revision: int | None = None,
    amendment_receipt_id: str | None = None,
) -> SubjectConstitution:
    """Sign first, then construct. Frozen+slots records cannot hold an empty signature."""

    signed_at = _normalise_timestamp(signed_at_utc, "signed_at_utc")
    unsigned = {
        "mandate_id": MANDATE_ID,
        "invariant_id": INVARIANT_ID,
        "subject_id": _require_text(subject_id, "subject_id"),
        "revision": revision,
        "status": _require_text(status, "status"),
        "source_evidence_refs": list(_freeze_sequence(source_evidence_refs, "source_evidence_refs")),
        "voice_characteristics": _thaw_json_value(
            _freeze_mapping(voice_characteristics, "voice_characteristics")
        ),
        "boundaries": _thaw_json_value(_freeze_mapping(boundaries, "boundaries")),
        "validation_state": _thaw_json_value(_freeze_mapping(validation_state, "validation_state")),
        "signed_by_operator_id": _require_text(signed_by_operator_id, "signed_by_operator_id"),
        "signed_at_utc": signed_at,
        "content_sha256": _require_text(content_sha256, "content_sha256"),
        "parent_revision": parent_revision,
        # amendment_receipt_id is attached after signing; omit from signed body.
    }
    signature = _sign(unsigned, signing_secret)
    return SubjectConstitution(
        subject_id=unsigned["subject_id"],
        revision=revision,
        status=unsigned["status"],
        source_evidence_refs=source_evidence_refs,
        voice_characteristics=voice_characteristics,
        boundaries=boundaries,
        validation_state=validation_state,
        signed_by_operator_id=unsigned["signed_by_operator_id"],
        signed_at_utc=signed_at,
        content_sha256=unsigned["content_sha256"],
        signature_sha256=signature,
        parent_revision=parent_revision,
        amendment_receipt_id=amendment_receipt_id,
    )


@dataclass(frozen=True, slots=True)
class SubjectConstitution:
    """Immutable, signed historical Subject Constitution revision."""

    subject_id: str
    revision: int
    status: str
    source_evidence_refs: tuple[str, ...]
    voice_characteristics: Mapping[str, Any]
    boundaries: Mapping[str, Any]
    validation_state: Mapping[str, Any]
    signed_by_operator_id: str
    signed_at_utc: str
    content_sha256: str
    signature_sha256: str
    parent_revision: int | None = None
    amendment_receipt_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "subject_id", _require_text(self.subject_id, "subject_id"))
        if not isinstance(self.revision, int) or self.revision < 1:
            raise InvalidAmendmentError("revision must be a positive integer")
        object.__setattr__(self, "status", _require_text(self.status, "status"))
        object.__setattr__(self, "source_evidence_refs", _freeze_sequence(self.source_evidence_refs, "source_evidence_refs"))
        object.__setattr__(self, "voice_characteristics", _freeze_mapping(self.voice_characteristics, "voice_characteristics"))
        object.__setattr__(self, "boundaries", _freeze_mapping(self.boundaries, "boundaries"))
        object.__setattr__(self, "validation_state", _freeze_mapping(self.validation_state, "validation_state"))
        object.__setattr__(self, "signed_by_operator_id", _require_text(self.signed_by_operator_id, "signed_by_operator_id"))
        object.__setattr__(self, "signed_at_utc", _normalise_timestamp(self.signed_at_utc, "signed_at_utc"))
        if self.parent_revision is not None and (
            not isinstance(self.parent_revision, int) or self.parent_revision < 1
        ):
            raise InvalidAmendmentError("parent_revision must be a positive integer or None")
        if self.revision == 1 and self.parent_revision is not None:
            raise InvalidAmendmentError("baseline revision cannot have a parent revision")
        if self.revision > 1 and self.parent_revision != self.revision - 1:
            raise InvalidAmendmentError("amended revision must point to the immediately previous revision")
        if self.amendment_receipt_id is not None:
            object.__setattr__(self, "amendment_receipt_id", _require_text(self.amendment_receipt_id, "amendment_receipt_id"))
        object.__setattr__(self, "content_sha256", _require_text(self.content_sha256, "content_sha256"))
        object.__setattr__(self, "signature_sha256", _require_text(self.signature_sha256, "signature_sha256"))

    def unsigned_payload(self) -> dict[str, Any]:
        return {
            "mandate_id": MANDATE_ID,
            "invariant_id": INVARIANT_ID,
            "subject_id": self.subject_id,
            "revision": self.revision,
            "status": self.status,
            "source_evidence_refs": list(self.source_evidence_refs),
            "voice_characteristics": dict(self.voice_characteristics),
            "boundaries": dict(self.boundaries),
            "validation_state": dict(self.validation_state),
            "signed_by_operator_id": self.signed_by_operator_id,
            "signed_at_utc": self.signed_at_utc,
            "content_sha256": self.content_sha256,
            "parent_revision": self.parent_revision,
            # amendment_receipt_id is post-sign linkage metadata; excluded from the signed body.
        }

    def verify(self, signing_secret: str) -> bool:
        payload = self.unsigned_payload()
        if _payload_hash(
            {
                "source_evidence_refs": list(self.source_evidence_refs),
                "voice_characteristics": dict(self.voice_characteristics),
                "boundaries": dict(self.boundaries),
                "validation_state": dict(self.validation_state),
            }
        ) != self.content_sha256:
            return False
        return _verify(payload, self.signature_sha256, signing_secret)

    def require_verified(self, signing_secret: str) -> None:
        if not self.verify(signing_secret):
            raise InvalidSignatureError(
                f"Subject Constitution {self.subject_id}@v{self.revision} failed signature/integrity verification"
            )


@dataclass(frozen=True, slots=True)
class SubjectConstitutionException:
    """Append-only exception that may trigger human review but cannot mutate baseline state."""

    exception_id: str
    subject_id: str
    exception_type: ConstitutionExceptionType
    description: str
    evidence_refs: tuple[str, ...]
    observed_at_utc: str
    detected_by: str
    review_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "exception_id", _require_text(self.exception_id, "exception_id"))
        object.__setattr__(self, "subject_id", _require_text(self.subject_id, "subject_id"))
        if not isinstance(self.exception_type, ConstitutionExceptionType):
            object.__setattr__(self, "exception_type", ConstitutionExceptionType(self.exception_type))
        object.__setattr__(self, "description", _require_text(self.description, "description"))
        object.__setattr__(self, "evidence_refs", _freeze_sequence(self.evidence_refs, "evidence_refs"))
        object.__setattr__(self, "observed_at_utc", _normalise_timestamp(self.observed_at_utc, "observed_at_utc"))
        object.__setattr__(self, "detected_by", _require_text(self.detected_by, "detected_by"))
        if not self.evidence_refs:
            raise InvalidAmendmentError("exception requires at least one evidence reference")
        if not isinstance(self.review_required, bool):
            raise InvalidAmendmentError("review_required must be boolean")


@dataclass(frozen=True, slots=True)
class SubjectConstitutionAmendmentPacket:
    """Proposed change; not authoritative until an operator approves it."""

    amendment_id: str
    subject_id: str
    parent_revision: int
    proposed_voice_characteristics: Mapping[str, Any] | None
    proposed_boundaries: Mapping[str, Any] | None
    proposed_validation_state: Mapping[str, Any] | None
    reason: str
    evidence_refs: tuple[str, ...]
    operator_id: str
    exception_id: str | None = None
    status: AmendmentStatus = AmendmentStatus.PENDING

    def __post_init__(self) -> None:
        object.__setattr__(self, "amendment_id", _require_text(self.amendment_id, "amendment_id"))
        object.__setattr__(self, "subject_id", _require_text(self.subject_id, "subject_id"))
        if not isinstance(self.parent_revision, int) or self.parent_revision < 1:
            raise InvalidAmendmentError("parent_revision must be a positive integer")
        if self.proposed_voice_characteristics is not None:
            object.__setattr__(self, "proposed_voice_characteristics", _freeze_mapping(self.proposed_voice_characteristics, "proposed_voice_characteristics"))
        if self.proposed_boundaries is not None:
            object.__setattr__(self, "proposed_boundaries", _freeze_mapping(self.proposed_boundaries, "proposed_boundaries"))
        if self.proposed_validation_state is not None:
            object.__setattr__(self, "proposed_validation_state", _freeze_mapping(self.proposed_validation_state, "proposed_validation_state"))
        object.__setattr__(self, "reason", _require_text(self.reason, "reason"))
        object.__setattr__(self, "evidence_refs", _freeze_sequence(self.evidence_refs, "evidence_refs"))
        if not self.evidence_refs:
            raise InvalidAmendmentError("amendment requires at least one evidence reference")
        object.__setattr__(self, "operator_id", _require_text(self.operator_id, "operator_id"))
        if self.exception_id is not None:
            object.__setattr__(self, "exception_id", _require_text(self.exception_id, "exception_id"))
        if not isinstance(self.status, AmendmentStatus):
            object.__setattr__(self, "status", AmendmentStatus(self.status))
        if all(value is None for value in (
            self.proposed_voice_characteristics,
            self.proposed_boundaries,
            self.proposed_validation_state,
        )):
            raise InvalidAmendmentError("amendment must propose at least one constitutional field change")

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "mandate_id": MANDATE_ID,
            "amendment_id": self.amendment_id,
            "subject_id": self.subject_id,
            "parent_revision": self.parent_revision,
            "proposed_voice_characteristics": dict(self.proposed_voice_characteristics) if self.proposed_voice_characteristics is not None else None,
            "proposed_boundaries": dict(self.proposed_boundaries) if self.proposed_boundaries is not None else None,
            "proposed_validation_state": dict(self.proposed_validation_state) if self.proposed_validation_state is not None else None,
            "reason": self.reason,
            "evidence_refs": list(self.evidence_refs),
            "operator_id": self.operator_id,
            "exception_id": self.exception_id,
            "status": self.status.value,
        }


@dataclass(frozen=True, slots=True)
class AmendmentReceipt:
    """Immutable, signed record proving why and by whom a revision was promoted."""

    receipt_id: str
    amendment_id: str
    subject_id: str
    parent_revision: int
    resulting_revision: int
    operator_id: str
    authority_scope: str
    decision: str
    reason: str
    evidence_refs: tuple[str, ...]
    exception_id: str | None
    parent_signature_sha256: str
    resulting_constitution_signature_sha256: str
    decided_at_utc: str
    receipt_sha256: str
    signature_sha256: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "receipt_id", _require_text(self.receipt_id, "receipt_id"))
        object.__setattr__(self, "amendment_id", _require_text(self.amendment_id, "amendment_id"))
        object.__setattr__(self, "subject_id", _require_text(self.subject_id, "subject_id"))
        if self.parent_revision < 1 or self.resulting_revision != self.parent_revision + 1:
            raise InvalidAmendmentError("receipt revision lineage is invalid")
        object.__setattr__(self, "operator_id", _require_text(self.operator_id, "operator_id"))
        object.__setattr__(self, "authority_scope", _require_text(self.authority_scope, "authority_scope"))
        if self.decision != _AuthorityDecision.APPROVED.value:
            raise InvalidAmendmentError("amendment receipts may only record an approved decision")
        object.__setattr__(self, "reason", _require_text(self.reason, "reason"))
        object.__setattr__(self, "evidence_refs", _freeze_sequence(self.evidence_refs, "evidence_refs"))
        if not self.evidence_refs:
            raise InvalidAmendmentError("amendment receipt requires evidence references")
        if self.exception_id is not None:
            object.__setattr__(self, "exception_id", _require_text(self.exception_id, "exception_id"))
        object.__setattr__(self, "parent_signature_sha256", _require_text(self.parent_signature_sha256, "parent_signature_sha256"))
        object.__setattr__(self, "resulting_constitution_signature_sha256", _require_text(self.resulting_constitution_signature_sha256, "resulting_constitution_signature_sha256"))
        object.__setattr__(self, "decided_at_utc", _normalise_timestamp(self.decided_at_utc, "decided_at_utc"))
        object.__setattr__(self, "receipt_sha256", _require_text(self.receipt_sha256, "receipt_sha256"))
        object.__setattr__(self, "signature_sha256", _require_text(self.signature_sha256, "signature_sha256"))

    def unsigned_payload(self) -> dict[str, Any]:
        return {
            "mandate_id": MANDATE_ID,
            "invariant_id": INVARIANT_ID,
            "receipt_id": self.receipt_id,
            "amendment_id": self.amendment_id,
            "subject_id": self.subject_id,
            "parent_revision": self.parent_revision,
            "resulting_revision": self.resulting_revision,
            "operator_id": self.operator_id,
            "authority_scope": self.authority_scope,
            "decision": self.decision,
            "reason": self.reason,
            "evidence_refs": list(self.evidence_refs),
            "exception_id": self.exception_id,
            "parent_signature_sha256": self.parent_signature_sha256,
            "resulting_constitution_signature_sha256": self.resulting_constitution_signature_sha256,
            "decided_at_utc": self.decided_at_utc,
        }

    def verify(self, signing_secret: str) -> bool:
        return (
            self.receipt_sha256 == _payload_hash(self.unsigned_payload())
            and _verify({**self.unsigned_payload(), "receipt_sha256": self.receipt_sha256}, self.signature_sha256, signing_secret)
        )

    def require_verified(self, signing_secret: str) -> None:
        if not self.verify(signing_secret):
            raise InvalidSignatureError(f"amendment receipt {self.receipt_id} failed integrity verification")


class SubjectConstitutionLifecycle:
    """Authoritative in-memory lifecycle for a subject's constitution history.

    The storage boundary is deliberately local to this mandate because the repository
    currently has no existing Subject Constitution persistence schema. Callers can
    project these immutable records to the existing persistence layer without changing
    their authority semantics.
    """

    def __init__(self, *, signing_secret: str):
        self._signing_secret = _require_text(signing_secret, "signing_secret")
        self._constitutions: dict[str, dict[int, SubjectConstitution]] = {}
        self._exceptions: dict[str, SubjectConstitutionException] = {}
        self._amendments: dict[str, SubjectConstitutionAmendmentPacket] = {}
        self._receipts: dict[str, AmendmentReceipt] = {}
        self._lock = RLock()

    def create_signed_baseline(
        self,
        *,
        subject_id: str,
        source_evidence_refs: Sequence[str],
        voice_characteristics: Mapping[str, Any],
        boundaries: Mapping[str, Any],
        validation_state: Mapping[str, Any],
        operator_id: str,
        signed_at_utc: str,
    ) -> SubjectConstitution:
        subject_id = _require_text(subject_id, "subject_id")
        operator_id = _require_text(operator_id, "operator_id")
        with self._lock:
            if subject_id in self._constitutions:
                raise ConstitutionAlreadyExistsError(f"signed baseline already exists for subject {subject_id}")
            source_refs = _freeze_sequence(source_evidence_refs, "source_evidence_refs")
            if not source_refs:
                raise InvalidAmendmentError("signed baseline requires source evidence")
            payload_for_content = {
                "source_evidence_refs": list(source_refs),
                "voice_characteristics": dict(_freeze_mapping(voice_characteristics, "voice_characteristics")),
                "boundaries": dict(_freeze_mapping(boundaries, "boundaries")),
                "validation_state": dict(_freeze_mapping(validation_state, "validation_state")),
            }
            content_sha256 = _payload_hash(payload_for_content)
            constitution = _mint_signed_constitution(
                subject_id=subject_id,
                revision=1,
                status="SIGNED",
                source_evidence_refs=source_refs,
                voice_characteristics=payload_for_content["voice_characteristics"],
                boundaries=payload_for_content["boundaries"],
                validation_state=payload_for_content["validation_state"],
                signed_by_operator_id=operator_id,
                signed_at_utc=signed_at_utc,
                content_sha256=content_sha256,
                signing_secret=self._signing_secret,
            )
            constitution.require_verified(self._signing_secret)
            self._constitutions[subject_id] = {1: constitution}
            return constitution

    def current(self, subject_id: str) -> SubjectConstitution:
        subject_id = _require_text(subject_id, "subject_id")
        with self._lock:
            revisions = self._constitutions.get(subject_id)
            if not revisions:
                raise ConstitutionNotFoundError(subject_id)
            current = revisions[max(revisions)]
            current.require_verified(self._signing_secret)
            return current

    def history(self, subject_id: str) -> tuple[SubjectConstitution, ...]:
        subject_id = _require_text(subject_id, "subject_id")
        with self._lock:
            revisions = self._constitutions.get(subject_id)
            if not revisions:
                raise ConstitutionNotFoundError(subject_id)
            ordered = tuple(revisions[revision] for revision in sorted(revisions))
            for constitution in ordered:
                constitution.require_verified(self._signing_secret)
            return ordered

    def record_exception(
        self,
        *,
        subject_id: str,
        exception_type: ConstitutionExceptionType,
        description: str,
        evidence_refs: Sequence[str],
        observed_at_utc: str,
        detected_by: str,
        exception_id: str | None = None,
    ) -> SubjectConstitutionException:
        subject_id = _require_text(subject_id, "subject_id")
        self.current(subject_id)
        exception = SubjectConstitutionException(
            exception_id=exception_id or str(uuid4()),
            subject_id=subject_id,
            exception_type=exception_type,
            description=description,
            evidence_refs=tuple(evidence_refs),
            observed_at_utc=observed_at_utc,
            detected_by=detected_by,
        )
        with self._lock:
            if exception.exception_id in self._exceptions:
                raise InvalidAmendmentError(f"exception {exception.exception_id} already exists")
            self._exceptions[exception.exception_id] = exception
        return exception

    def get_exception(self, exception_id: str) -> SubjectConstitutionException:
        with self._lock:
            try:
                return self._exceptions[exception_id]
            except KeyError as exc:
                raise ConstitutionNotFoundError(exception_id) from exc

    def submit_amendment(self, packet: SubjectConstitutionAmendmentPacket) -> SubjectConstitutionAmendmentPacket:
        current = self.current(packet.subject_id)
        if packet.parent_revision != current.revision:
            raise StaleParentRevisionError(
                f"amendment {packet.amendment_id} targets revision {packet.parent_revision}; current is {current.revision}"
            )
        if packet.exception_id is not None:
            exception = self.get_exception(packet.exception_id)
            if exception.subject_id != packet.subject_id:
                raise InvalidAmendmentError("exception does not belong to amendment subject")
        with self._lock:
            if packet.amendment_id in self._amendments:
                raise InvalidAmendmentError(f"amendment {packet.amendment_id} already exists")
            self._amendments[packet.amendment_id] = packet
        return packet

    def approve_amendment(
        self,
        *,
        amendment_id: str,
        operator_id: str,
        authority_scope: str,
        decided_at_utc: str,
        signing_secret: str | None = None,
    ) -> tuple[SubjectConstitution, AmendmentReceipt]:
        operator_id = _require_text(operator_id, "operator_id")
        authority_scope = _require_text(authority_scope, "authority_scope")
        if authority_scope != AMENDMENT_AUTHORITY_SCOPE:
            raise UnauthorizedOperatorError(
                f"required authority scope is {AMENDMENT_AUTHORITY_SCOPE}; received {authority_scope}"
            )
        secret = _require_text(signing_secret or self._signing_secret, "signing_secret")
        if not hmac.compare_digest(secret, self._signing_secret):
            raise UnauthorizedOperatorError("amendment approval must use the lifecycle signing secret")
        with self._lock:
            try:
                packet = self._amendments[amendment_id]
            except KeyError as exc:
                raise ConstitutionNotFoundError(amendment_id) from exc
            if packet.status is not AmendmentStatus.PENDING:
                raise AmendmentAlreadyResolvedError(f"amendment {amendment_id} is already {packet.status.value}")
            if packet.operator_id != operator_id:
                raise UnauthorizedOperatorError("approval operator does not match amendment packet operator")
            current = self.current(packet.subject_id)
            current.require_verified(secret)
            if packet.parent_revision != current.revision:
                raise StaleParentRevisionError(
                    f"amendment {packet.amendment_id} targets revision {packet.parent_revision}; current is {current.revision}"
                )

            next_voice = (
                dict(packet.proposed_voice_characteristics)
                if packet.proposed_voice_characteristics is not None
                else dict(current.voice_characteristics)
            )
            next_boundaries = (
                dict(packet.proposed_boundaries)
                if packet.proposed_boundaries is not None
                else dict(current.boundaries)
            )
            next_validation = (
                dict(packet.proposed_validation_state)
                if packet.proposed_validation_state is not None
                else dict(current.validation_state)
            )
            next_payload_for_content = {
                "source_evidence_refs": list(current.source_evidence_refs),
                "voice_characteristics": next_voice,
                "boundaries": next_boundaries,
                "validation_state": next_validation,
            }
            next_content_hash = _payload_hash(next_payload_for_content)
            next_revision = current.revision + 1
            next_constitution = _mint_signed_constitution(
                subject_id=current.subject_id,
                revision=next_revision,
                status="SIGNED",
                source_evidence_refs=current.source_evidence_refs,
                voice_characteristics=next_voice,
                boundaries=next_boundaries,
                validation_state=next_validation,
                signed_by_operator_id=operator_id,
                signed_at_utc=decided_at_utc,
                content_sha256=next_content_hash,
                signing_secret=secret,
                parent_revision=current.revision,
            )
            next_constitution.require_verified(secret)

            receipt_id = str(uuid4())
            receipt_payload = {
                "mandate_id": MANDATE_ID,
                "invariant_id": INVARIANT_ID,
                "receipt_id": receipt_id,
                "amendment_id": packet.amendment_id,
                "subject_id": packet.subject_id,
                "parent_revision": current.revision,
                "resulting_revision": next_revision,
                "operator_id": operator_id,
                "authority_scope": authority_scope,
                "decision": _AuthorityDecision.APPROVED.value,
                "reason": packet.reason,
                "evidence_refs": list(packet.evidence_refs),
                "exception_id": packet.exception_id,
                "parent_signature_sha256": current.signature_sha256,
                "resulting_constitution_signature_sha256": next_constitution.signature_sha256,
                "decided_at_utc": _normalise_timestamp(decided_at_utc, "decided_at_utc"),
            }
            receipt_hash = _payload_hash(receipt_payload)
            receipt_signature = _sign({**receipt_payload, "receipt_sha256": receipt_hash}, secret)
            receipt = AmendmentReceipt(
                receipt_id=receipt_id,
                amendment_id=packet.amendment_id,
                subject_id=packet.subject_id,
                parent_revision=current.revision,
                resulting_revision=next_revision,
                operator_id=operator_id,
                authority_scope=authority_scope,
                decision=_AuthorityDecision.APPROVED.value,
                reason=packet.reason,
                evidence_refs=packet.evidence_refs,
                exception_id=packet.exception_id,
                parent_signature_sha256=current.signature_sha256,
                resulting_constitution_signature_sha256=next_constitution.signature_sha256,
                decided_at_utc=decided_at_utc,
                receipt_sha256=receipt_hash,
                signature_sha256=receipt_signature,
            )
            receipt.require_verified(secret)

            next_constitution = SubjectConstitution(
                subject_id=next_constitution.subject_id,
                revision=next_constitution.revision,
                status=next_constitution.status,
                source_evidence_refs=next_constitution.source_evidence_refs,
                voice_characteristics=next_constitution.voice_characteristics,
                boundaries=next_constitution.boundaries,
                validation_state=next_constitution.validation_state,
                signed_by_operator_id=next_constitution.signed_by_operator_id,
                signed_at_utc=next_constitution.signed_at_utc,
                content_sha256=next_constitution.content_sha256,
                signature_sha256=next_constitution.signature_sha256,
                parent_revision=next_constitution.parent_revision,
                amendment_receipt_id=receipt.receipt_id,
            )
            next_constitution.require_verified(secret)
            # Replace only the pending packet's lifecycle record. Historical
            # constitutions and receipts remain append-only.
            self._amendments[packet.amendment_id] = SubjectConstitutionAmendmentPacket(
                amendment_id=packet.amendment_id,
                subject_id=packet.subject_id,
                parent_revision=packet.parent_revision,
                proposed_voice_characteristics=packet.proposed_voice_characteristics,
                proposed_boundaries=packet.proposed_boundaries,
                proposed_validation_state=packet.proposed_validation_state,
                reason=packet.reason,
                evidence_refs=packet.evidence_refs,
                operator_id=packet.operator_id,
                exception_id=packet.exception_id,
                status=AmendmentStatus.APPROVED,
            )
            self._constitutions[packet.subject_id][next_revision] = next_constitution
            self._receipts[receipt.receipt_id] = receipt
            return next_constitution, receipt

    def reject_amendment(self, *, amendment_id: str, operator_id: str) -> SubjectConstitutionAmendmentPacket:
        operator_id = _require_text(operator_id, "operator_id")
        with self._lock:
            try:
                packet = self._amendments[amendment_id]
            except KeyError as exc:
                raise ConstitutionNotFoundError(amendment_id) from exc
            if packet.status is not AmendmentStatus.PENDING:
                raise AmendmentAlreadyResolvedError(f"amendment {amendment_id} is already {packet.status.value}")
            if packet.operator_id != operator_id:
                raise UnauthorizedOperatorError("rejection operator does not match amendment packet operator")
            rejected = SubjectConstitutionAmendmentPacket(
                amendment_id=packet.amendment_id,
                subject_id=packet.subject_id,
                parent_revision=packet.parent_revision,
                proposed_voice_characteristics=packet.proposed_voice_characteristics,
                proposed_boundaries=packet.proposed_boundaries,
                proposed_validation_state=packet.proposed_validation_state,
                reason=packet.reason,
                evidence_refs=packet.evidence_refs,
                operator_id=packet.operator_id,
                exception_id=packet.exception_id,
                status=AmendmentStatus.REJECTED,
            )
            self._amendments[amendment_id] = rejected
            return rejected

    def amendment(self, amendment_id: str) -> SubjectConstitutionAmendmentPacket:
        with self._lock:
            try:
                return self._amendments[amendment_id]
            except KeyError as exc:
                raise ConstitutionNotFoundError(amendment_id) from exc

    def receipt(self, receipt_id: str) -> AmendmentReceipt:
        with self._lock:
            try:
                receipt = self._receipts[receipt_id]
            except KeyError as exc:
                raise ConstitutionNotFoundError(receipt_id) from exc
            receipt.require_verified(self._signing_secret)
            return receipt

    def receipts_for_subject(self, subject_id: str) -> tuple[AmendmentReceipt, ...]:
        subject_id = _require_text(subject_id, "subject_id")
        with self._lock:
            receipts = tuple(receipt for receipt in self._receipts.values() if receipt.subject_id == subject_id)
            for receipt in receipts:
                receipt.require_verified(self._signing_secret)
            return tuple(sorted(receipts, key=lambda item: item.resulting_revision))

    def assert_no_in_place_mutation(self, constitution: SubjectConstitution) -> None:
        """Explicit lifecycle guard for callers that try to hand back a mutated object."""
        current = self.current(constitution.subject_id)
        if constitution is current:
            constitution.require_verified(self._signing_secret)
            return
        if constitution.revision <= current.revision:
            constitution.require_verified(self._signing_secret)
        else:
            raise ConstitutionImmutableError("new revisions must be created through approve_amendment")


__all__ = [
    "AMENDMENT_AUTHORITY_SCOPE",
    "AmendmentAlreadyResolvedError",
    "AmendmentReceipt",
    "AmendmentStatus",
    "ConstitutionAlreadyExistsError",
    "ConstitutionExceptionType",
    "ConstitutionImmutableError",
    "ConstitutionNotFoundError",
    "InvalidAmendmentError",
    "InvalidSignatureError",
    "MANDATE_ID",
    "INVARIANT_ID",
    "StaleParentRevisionError",
    "SubjectConstitution",
    "SubjectConstitutionAmendmentPacket",
    "SubjectConstitutionError",
    "SubjectConstitutionException",
    "SubjectConstitutionLifecycle",
    "UnauthorizedOperatorError",
]
