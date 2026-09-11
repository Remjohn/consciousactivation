"""CA-M029 no-unanchored-invention composition gate.

The gate is deliberately structural and fail-closed.  It does not ask a model to
judge whether a sentence is grounded.  Each substantive sentence must either:

* carry one or more immutable references to admitted evidence whose exact bytes,
  revision/digest, admission state, and verbatim quote are independently verified;
  the verified quote must occur verbatim in the sentence; or
* be explicitly classified as an authorised connective transformation selected by
  an allow-listed program policy.

Any other sentence is rejected (or removed when the caller explicitly selects the
``PURGE`` action).  A soft coverage score cannot compensate for one unsupported
sentence: the predicate is evaluated independently for every sentence.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum
import hashlib
import re
from typing import Any, Callable, Iterable, Mapping, Protocol, Sequence

from ca_contracts import canonical_sha256

CA_M029 = "CA-M029"
FR_029 = "FR-029"
INVARIANT_ID = "INV-NO-INVENT-001"
POLICY_VERSION = "CA-M029-NO-UNANCHORED-INVENTION-V1"

# Upstream interview/runtime implementations use VALIDATED for admitted verbatim
# evidence objects, while the generic evidence-admission boundary uses ADMITTED.
ADMITTED_EVIDENCE_STATES = frozenset({"ADMITTED", "VALIDATED", "VERIFIED", "APPROVED"})
VERBATIM_PASS_STATES = frozenset({"PASS", "VERIFIED", "ADMITTED", "VALIDATED"})

_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])(?:[\"')\]]+)?(?:\s+|$)")
_WHITESPACE = re.compile(r"\s+")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class NoUnanchoredInventionError(RuntimeError):
    """Base error for the CA-M029 composition grounding boundary."""

    code = "CA_M029_NO_UNANCHORED_INVENTION"

    def __init__(self, message: str, *, sentence_index: int | None = None, context: Mapping[str, Any] | None = None):
        super().__init__(message)
        self.sentence_index = sentence_index
        self.context = dict(context or {})


class EvidenceResolutionError(NoUnanchoredInventionError):
    """Evidence reference cannot be resolved through the authoritative boundary."""

    code = "CA_M029_EVIDENCE_RESOLUTION_FAILED"


class EvidenceRevisionMismatchError(NoUnanchoredInventionError):
    """The submitted evidence reference does not identify the resolved immutable revision."""

    code = "CA_M029_EVIDENCE_REVISION_MISMATCH"


class EvidenceAdmissionError(NoUnanchoredInventionError):
    """The resolved evidence is not in an admitted/verified state."""

    code = "CA_M029_EVIDENCE_NOT_ADMITTED"


class VerbatimMismatchError(NoUnanchoredInventionError):
    """The supplied/recorded quote cannot be proven to be the exact source bytes."""

    code = "CA_M029_VERBATIM_MISMATCH"


class ConnectiveTransformationError(NoUnanchoredInventionError):
    """A connective sentence lacks an explicit, authorised transformation policy."""

    code = "CA_M029_CONNECTIVE_TRANSFORMATION_NOT_AUTHORISED"


class UnanchoredClaimError(NoUnanchoredInventionError):
    """A substantive sentence has no independently verified grounding."""

    code = "CA_M029_UNANCHORED_CLAIM"


class EvidenceResolver(Protocol):
    """Minimal resolver protocol for canonical content-addressed evidence."""

    def get_object_by_sha(self, object_id: str, sha256: str) -> Mapping[str, Any]:
        ...


class GroundingClass(str, Enum):
    EVIDENCE_BACKED = "EVIDENCE_BACKED"
    CONNECTIVE = "CONNECTIVE"


class EnforcementAction(str, Enum):
    BLOCK = "BLOCK"
    PURGE = "PURGE"
    FLAG = "FLAG"


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    """Immutable content-addressed reference to an admitted evidence object."""

    object_id: str
    version: str
    sha256: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "EvidenceRef":
        if not isinstance(value, Mapping):
            raise EvidenceResolutionError("evidence reference must be a mapping")
        missing = [key for key in ("object_id", "version", "sha256") if not value.get(key)]
        if missing:
            raise EvidenceResolutionError(
                "evidence reference is incomplete",
                context={"missing_fields": missing},
            )
        object_id = str(value["object_id"])
        version = str(value["version"])
        sha256 = str(value["sha256"]).lower()
        if not _SHA256_RE.fullmatch(sha256):
            raise EvidenceResolutionError("evidence reference sha256 must be a 64-character hex digest")
        return cls(object_id=object_id, version=version, sha256=sha256)

    def to_dict(self) -> dict[str, str]:
        return {"object_id": self.object_id, "version": self.version, "sha256": self.sha256}


@dataclass(frozen=True, slots=True)
class VerbatimAnchor:
    """Sentence-level grounding declaration using one exact source quote."""

    evidence_ref: EvidenceRef
    verbatim_quote: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "VerbatimAnchor":
        if not isinstance(value, Mapping):
            raise EvidenceResolutionError("verbatim anchor must be a mapping")
        quote = value.get("verbatim_quote", value.get("quote_text", value.get("quote")))
        if not isinstance(quote, str) or not quote:
            raise EvidenceResolutionError("verbatim anchor requires a non-empty verbatim_quote")
        ref_value = value.get("evidence_ref", value.get("ref"))
        if not isinstance(ref_value, Mapping):
            raise EvidenceResolutionError("verbatim anchor requires evidence_ref")
        return cls(EvidenceRef.from_mapping(ref_value), quote)

    def to_dict(self) -> dict[str, Any]:
        return {"evidence_ref": self.evidence_ref.to_dict(), "verbatim_quote": self.verbatim_quote}


@dataclass(frozen=True, slots=True)
class SentenceClaim:
    """A machine-auditable sentence-level composition unit."""

    sentence: str
    grounding: GroundingClass | str = GroundingClass.EVIDENCE_BACKED
    evidence_refs: tuple[EvidenceRef, ...] = ()
    verbatim_anchors: tuple[VerbatimAnchor, ...] = ()
    connective_operation: str | None = None
    claim_id: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        text = _clean_sentence(self.sentence)
        if not text:
            raise ValueError("sentence must be non-empty")
        object.__setattr__(self, "sentence", text)
        try:
            object.__setattr__(self, "grounding", GroundingClass(self.grounding))
        except ValueError as exc:
            raise ValueError(f"unsupported grounding class: {self.grounding!r}") from exc
        refs = tuple(self.evidence_refs)
        anchors = tuple(self.verbatim_anchors)
        object.__setattr__(self, "evidence_refs", refs)
        object.__setattr__(self, "verbatim_anchors", anchors)
        object.__setattr__(self, "metadata", dict(self.metadata))

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SentenceClaim":
        if not isinstance(value, Mapping):
            raise ValueError("sentence claim must be a mapping")
        sentence = value.get("sentence", value.get("text", value.get("content")))
        if not isinstance(sentence, str) or not sentence.strip():
            raise ValueError("sentence claim requires a non-empty sentence")
        raw_refs = value.get("evidence_refs", value.get("evidence_references", ()))
        if isinstance(raw_refs, Mapping):
            raw_refs = (raw_refs,)
        refs = tuple(EvidenceRef.from_mapping(item) for item in (raw_refs or ()))
        raw_anchors = value.get("verbatim_anchors", value.get("anchors", ()))
        if isinstance(raw_anchors, Mapping):
            raw_anchors = (raw_anchors,)
        anchors = tuple(VerbatimAnchor.from_mapping(item) for item in (raw_anchors or ()))
        # Accept the convenient top-level quote + ref representation as well.
        if not anchors and value.get("verbatim_quote") and refs:
            anchors = tuple(VerbatimAnchor(ref, str(value["verbatim_quote"])) for ref in refs)
        return cls(
            sentence=sentence,
            grounding=value.get("grounding", value.get("classification", GroundingClass.EVIDENCE_BACKED.value)),
            evidence_refs=refs,
            verbatim_anchors=anchors,
            connective_operation=value.get("connective_operation", value.get("transformation")),
            claim_id=value.get("claim_id", value.get("id")),
            metadata=value.get("metadata", {}),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "sentence": self.sentence,
            "grounding": self.grounding.value,
            "evidence_refs": [ref.to_dict() for ref in self.evidence_refs],
            "verbatim_anchors": [anchor.to_dict() for anchor in self.verbatim_anchors],
            "connective_operation": self.connective_operation,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class ConnectivePolicy:
    """Explicit program policy for connective transformations."""

    allowed_operations: frozenset[str]
    policy_id: str
    version: str

    @classmethod
    def strict_allowlist(
        cls,
        operations: Iterable[str],
        *,
        policy_id: str = "program-connective-policy",
        version: str = "1.0.0",
    ) -> "ConnectivePolicy":
        normalized = frozenset(_normalize_operation(item) for item in operations if str(item).strip())
        return cls(allowed_operations=normalized, policy_id=policy_id, version=version)

    def allows(self, operation: str | None) -> bool:
        return _normalize_operation(operation or "") in self.allowed_operations


@dataclass(frozen=True, slots=True)
class EvidenceVerification:
    """Proof produced after independently resolving and checking one evidence ref."""

    evidence_ref: EvidenceRef
    object_id: str
    object_version: str
    object_sha256: str
    evidence_state: str
    quote_text: str
    quote_sha256: str
    evidence_class: str | None
    source_lineage: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_ref": self.evidence_ref.to_dict(),
            "object_id": self.object_id,
            "object_version": self.object_version,
            "object_sha256": self.object_sha256,
            "evidence_state": self.evidence_state,
            "quote_text": self.quote_text,
            "quote_sha256": self.quote_sha256,
            "evidence_class": self.evidence_class,
            "source_lineage": dict(self.source_lineage),
        }


@dataclass(frozen=True, slots=True)
class SentenceAudit:
    """Audit result for one composition sentence."""

    sentence_index: int
    claim: SentenceClaim
    admitted: bool
    reasons: tuple[str, ...] = ()
    evidence_verifications: tuple[EvidenceVerification, ...] = ()
    action: EnforcementAction = EnforcementAction.BLOCK

    @property
    def flagged(self) -> bool:
        return not self.admitted

    def to_dict(self) -> dict[str, Any]:
        return {
            "sentence_index": self.sentence_index,
            "claim": self.claim.to_dict(),
            "admitted": self.admitted,
            "flagged": self.flagged,
            "reasons": list(self.reasons),
            "evidence_verifications": [item.to_dict() for item in self.evidence_verifications],
            "action": self.action.value,
        }


@dataclass(frozen=True, slots=True)
class CompositionAuditReport:
    """Hard-gate result for an entire composition artifact."""

    mandate_id: str
    invariant_id: str
    policy_version: str
    admitted: bool
    sentences: tuple[SentenceAudit, ...]
    admitted_sentences: tuple[str, ...]
    rejected_sentences: tuple[str, ...]
    purged_sentences: tuple[str, ...]
    validation_digest: str

    @property
    def flagged(self) -> bool:
        return any(item.flagged for item in self.sentences)

    def to_dict(self) -> dict[str, Any]:
        return {
            "mandate_id": self.mandate_id,
            "invariant_id": self.invariant_id,
            "policy_version": self.policy_version,
            "admitted": self.admitted,
            "flagged": self.flagged,
            "sentences": [item.to_dict() for item in self.sentences],
            "admitted_sentences": list(self.admitted_sentences),
            "rejected_sentences": list(self.rejected_sentences),
            "purged_sentences": list(self.purged_sentences),
            "validation_digest": self.validation_digest,
        }


@dataclass(frozen=True, slots=True)
class CompositionAdmission:
    """Release-safe compiled text plus the complete sentence-level audit."""

    text: str
    audit: CompositionAuditReport

    @property
    def admitted(self) -> bool:
        return self.audit.admitted

    def to_dict(self) -> dict[str, Any]:
        return {"text": self.text, "audit": self.audit.to_dict()}


def extract_sentences(text: str) -> tuple[str, ...]:
    """Split candidate prose conservatively into non-empty sentence units."""

    if not isinstance(text, str):
        raise TypeError("text must be a string")
    normalized = _WHITESPACE.sub(" ", text).strip()
    if not normalized:
        return ()
    chunks: list[str] = []
    start = 0
    for match in _SENTENCE_BOUNDARY.finditer(normalized):
        end = match.end()
        sentence = _clean_sentence(normalized[start:end])
        if sentence:
            chunks.append(sentence)
        start = end
    tail = _clean_sentence(normalized[start:])
    if tail:
        chunks.append(tail)
    return tuple(chunks)


def _clean_sentence(value: str) -> str:
    return _WHITESPACE.sub(" ", str(value).strip())


def _normalize_operation(value: str) -> str:
    return str(value).strip().upper().replace("-", "_").replace(" ", "_")


def _quote_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _unwrap_evidence_object(result: Any) -> Mapping[str, Any]:
    if isinstance(result, Mapping) and isinstance(result.get("object"), Mapping):
        return result["object"]
    if isinstance(result, Mapping):
        return result
    raise EvidenceResolutionError("authoritative evidence resolver returned a non-mapping object")


def _resolve_evidence(resolver: EvidenceResolver | Mapping[Any, Any] | Callable[..., Any], ref: EvidenceRef) -> Mapping[str, Any]:
    try:
        if hasattr(resolver, "get_object_by_sha"):
            resolved = resolver.get_object_by_sha(ref.object_id, ref.sha256)  # type: ignore[attr-defined]
        elif callable(resolver):
            try:
                resolved = resolver(ref.to_dict())
            except TypeError:
                resolved = resolver(ref.object_id, ref.sha256)
        elif isinstance(resolver, Mapping):
            resolved = resolver.get((ref.object_id, ref.sha256))
            if resolved is None:
                resolved = resolver.get(ref.object_id)
            if resolved is None:
                resolved = resolver.get(ref.to_dict())
        else:
            resolved = None
    except Exception as exc:
        raise EvidenceResolutionError(
            f"evidence reference {ref.object_id}@{ref.sha256} could not be resolved",
            context={"evidence_ref": ref.to_dict()},
        ) from exc
    if resolved is None:
        raise EvidenceResolutionError(
            f"evidence reference {ref.object_id}@{ref.sha256} could not be resolved",
            context={"evidence_ref": ref.to_dict()},
        )
    return _unwrap_evidence_object(resolved)


def verify_evidence_reference(
    evidence_ref: EvidenceRef | Mapping[str, Any],
    evidence_resolver: EvidenceResolver | Mapping[Any, Any] | Callable[..., Any],
) -> EvidenceVerification:
    """Resolve one evidence ref through the canonical store and prove its identity."""

    ref = evidence_ref if isinstance(evidence_ref, EvidenceRef) else EvidenceRef.from_mapping(evidence_ref)
    obj = _resolve_evidence(evidence_resolver, ref)
    object_id = str(obj.get("object_id", obj.get("evidence_id", "")))
    object_version = str(obj.get("version", obj.get("revision_id", obj.get("revision", ""))))
    object_sha256 = str(obj.get("sha256", obj.get("canonical_sha256", ""))).lower()
    if object_id != ref.object_id or object_version != ref.version or object_sha256 != ref.sha256:
        raise EvidenceRevisionMismatchError(
            "resolved evidence revision/digest does not match submitted evidence reference",
            context={"expected": ref.to_dict(), "resolved": {"object_id": object_id, "version": object_version, "sha256": object_sha256}},
        )

    payload = obj.get("payload")
    payload_map = payload if isinstance(payload, Mapping) else obj
    # The InterviewRepository hashes the payload bytes.  When a payload is exposed,
    # independently recompute that digest; this blocks forged wrapper metadata.
    if isinstance(payload, Mapping):
        computed_object_sha256 = canonical_sha256(dict(payload))
        if computed_object_sha256 != object_sha256:
            raise EvidenceRevisionMismatchError(
                "resolved evidence payload digest does not match its content-addressed object sha256",
                context={"expected_sha256": object_sha256, "computed_sha256": computed_object_sha256},
            )

    state = str(obj.get("lifecycle_state", payload_map.get("lifecycle_state", ""))).upper()
    admission = payload_map.get("admission_receipt", {})
    admission_status = str(
        payload_map.get("admission_state", admission.get("validation_status", payload_map.get("validation", {}).get("status", "")))
    ).upper()
    effective_state = state or admission_status
    if state not in {"ADMITTED", "VERIFIED", "APPROVED"} and not (
        state in {"VALIDATED", ""} and admission_status in VERBATIM_PASS_STATES
    ):
        raise EvidenceAdmissionError(
            "evidence object is not admitted/verified for downstream composition",
            context={"evidence_ref": ref.to_dict(), "lifecycle_state": state, "admission_state": admission_status},
        )

    quote = payload_map.get("quote_text", payload_map.get("verbatim_text", payload_map.get("verbatim_quote")))
    if not isinstance(quote, str) or not quote:
        raise VerbatimMismatchError(
            "admitted evidence does not contain a non-empty exact verbatim quote",
            context={"evidence_ref": ref.to_dict()},
        )
    supplied_quote_sha = str(payload_map.get("quote_sha256", payload_map.get("text_sha256", ""))).lower()
    actual_quote_sha = _quote_sha256(quote)
    if supplied_quote_sha != actual_quote_sha or not _SHA256_RE.fullmatch(actual_quote_sha):
        raise VerbatimMismatchError(
            "admitted evidence verbatim quote hash does not match its exact quote bytes",
            context={"evidence_ref": ref.to_dict(), "expected_quote_sha256": supplied_quote_sha, "actual_quote_sha256": actual_quote_sha},
        )

    validation = payload_map.get("validation", {})
    if isinstance(validation, Mapping) and validation.get("exact_character_slice") is False:
        raise VerbatimMismatchError(
            "evidence validation does not prove an exact verbatim source slice",
            context={"evidence_ref": ref.to_dict()},
        )

    source_lineage: dict[str, Any] = {}
    for key in ("source_package_ref", "transcript_ref", "source_span", "source_media_ref"):
        if key in payload_map:
            source_lineage[key] = payload_map[key]

    evidence_class = payload_map.get("evidence_class") or payload_map.get("evidence_type")
    return EvidenceVerification(
        evidence_ref=ref,
        object_id=object_id,
        object_version=object_version,
        object_sha256=object_sha256,
        evidence_state=effective_state,
        quote_text=quote,
        quote_sha256=actual_quote_sha,
        evidence_class=str(evidence_class) if evidence_class is not None else None,
        source_lineage=source_lineage,
    )


def _coerce_claims(candidate: str | Sequence[str] | Sequence[SentenceClaim | Mapping[str, Any]]) -> tuple[SentenceClaim, ...]:
    if isinstance(candidate, str):
        return tuple(SentenceClaim(sentence=item) for item in extract_sentences(candidate))
    claims: list[SentenceClaim] = []
    for item in candidate:
        if isinstance(item, SentenceClaim):
            claims.append(item)
        elif isinstance(item, Mapping):
            claims.append(SentenceClaim.from_mapping(item))
        elif isinstance(item, str):
            # Explicitly supplied strings remain substantive and therefore ungrounded
            # unless the caller adds an evidence-backed SentenceClaim object.
            claims.extend(SentenceClaim(sentence=sentence) for sentence in extract_sentences(item))
        else:
            raise TypeError(f"unsupported sentence claim type: {type(item)!r}")
    return tuple(claims)


def audit_sentences(
    claims: str | Sequence[str] | Sequence[SentenceClaim | Mapping[str, Any]],
    evidence_resolver: EvidenceResolver | Mapping[Any, Any] | Callable[..., Any],
    *,
    connective_policy: ConnectivePolicy | None = None,
    action: EnforcementAction | str = EnforcementAction.BLOCK,
) -> CompositionAuditReport:
    """Audit every sentence and return a hard-gate report.

    ``BLOCK`` is the default.  ``FLAG`` returns a failed report without changing
    content.  ``PURGE`` returns a report whose downstream text can safely omit all
    rejected sentences.  In every mode the original sentence-level findings remain
    available for audit.
    """

    enforcement = EnforcementAction(action)
    normalized_claims = _coerce_claims(claims)
    audits: list[SentenceAudit] = []
    for index, claim in enumerate(normalized_claims):
        try:
            audit = _audit_claim(
                index,
                claim,
                evidence_resolver,
                connective_policy=connective_policy,
                action=enforcement,
            )
        except NoUnanchoredInventionError as exc:
            audit = SentenceAudit(
                sentence_index=index,
                claim=claim,
                admitted=False,
                reasons=(getattr(exc, "code", exc.__class__.__name__), str(exc)),
                evidence_verifications=(),
                action=enforcement,
            )
        audits.append(audit)

    admitted_sentences = tuple(item.claim.sentence for item in audits if item.admitted)
    rejected_sentences = tuple(item.claim.sentence for item in audits if not item.admitted)
    purged_sentences = rejected_sentences if enforcement == EnforcementAction.PURGE else ()
    admitted = all(item.admitted for item in audits)
    # Only contract-governed primitives enter the validation digest.  Free-form
    # model metadata is intentionally excluded because it is descriptive rather
    # than an authority input and may contain unsupported JSON scalars such as floats.
    digest_basis = {
        "mandate_id": CA_M029,
        "invariant_id": INVARIANT_ID,
        "policy_version": POLICY_VERSION,
        "sentences": [
            {
                "sentence_index": item.sentence_index,
                "sentence": item.claim.sentence,
                "grounding": item.claim.grounding.value,
                "admitted": item.admitted,
                "reasons": list(item.reasons),
                "evidence_refs": [ref.to_dict() for ref in item.claim.evidence_refs],
                "verbatim_quotes": [verification.quote_text for verification in item.evidence_verifications],
            }
            for item in audits
        ],
    }
    return CompositionAuditReport(
        mandate_id=CA_M029,
        invariant_id=INVARIANT_ID,
        policy_version=POLICY_VERSION,
        admitted=admitted,
        sentences=tuple(audits),
        admitted_sentences=admitted_sentences,
        rejected_sentences=rejected_sentences,
        purged_sentences=purged_sentences,
        validation_digest=canonical_sha256(digest_basis),
    )


def _audit_claim(
    index: int,
    claim: SentenceClaim,
    evidence_resolver: EvidenceResolver | Mapping[Any, Any] | Callable[..., Any],
    *,
    connective_policy: ConnectivePolicy | None,
    action: EnforcementAction,
) -> SentenceAudit:
    if claim.grounding == GroundingClass.CONNECTIVE:
        if connective_policy is None or not connective_policy.allows(claim.connective_operation):
            raise ConnectiveTransformationError(
                "connective sentence is not covered by the versioned program connective policy",
                sentence_index=index,
                context={
                    "operation": claim.connective_operation,
                    "policy_id": connective_policy.policy_id if connective_policy else None,
                    "policy_version": connective_policy.version if connective_policy else None,
                },
            )
        return SentenceAudit(index, claim, True, ("AUTHORIZED_CONNECTIVE_TRANSFORMATION",), (), action)

    if not claim.evidence_refs and not claim.verbatim_anchors:
        raise UnanchoredClaimError(
            "substantive sentence has no admitted evidence reference or verbatim anchor",
            sentence_index=index,
            context={"sentence": claim.sentence},
        )

    verified: list[EvidenceVerification] = []
    if claim.evidence_refs:
        for ref in claim.evidence_refs:
            verified.append(verify_evidence_reference(ref, evidence_resolver))

    # Every explicit anchor is independently resolved.  It is not enough to set an
    # arbitrary 'anchored=true' bit or to point the whole paragraph at one ref.
    if claim.verbatim_anchors:
        for anchor in claim.verbatim_anchors:
            verification = verify_evidence_reference(anchor.evidence_ref, evidence_resolver)
            if verification.quote_text != anchor.verbatim_quote:
                raise VerbatimMismatchError(
                    "submitted verbatim anchor does not match the admitted evidence quote",
                    sentence_index=index,
                    context={
                        "evidence_ref": anchor.evidence_ref.to_dict(),
                        "expected_quote": verification.quote_text,
                        "submitted_quote": anchor.verbatim_quote,
                    },
                )
            if not _contains_verbatim(claim.sentence, verification.quote_text):
                raise UnanchoredClaimError(
                    "sentence introduces substantive wording outside the supplied exact verbatim anchor; classify as an authorised connective or provide a direct quote",
                    sentence_index=index,
                    context={
                        "evidence_ref": verification.evidence_ref.to_dict(),
                        "verbatim_quote": verification.quote_text,
                    },
                )
            if verification not in verified:
                verified.append(verification)
    else:
        # Evidence refs without explicit verbatim anchors are intentionally not
        # sufficient.  This prevents a whole paragraph/scene from borrowing one
        # evidence ID while silently adding unrelated facts.
        raise UnanchoredClaimError(
            "substantive sentence has evidence references but no sentence-level exact verbatim anchor",
            sentence_index=index,
            context={"evidence_refs": [ref.to_dict() for ref in claim.evidence_refs]},
        )

    # At least one independent source has been verified and its exact quote occurs in
    # the sentence.  Multiple anchors are allowed and remain independently auditable.
    if not verified:
        raise UnanchoredClaimError("sentence did not produce any verified evidence anchors", sentence_index=index)
    return SentenceAudit(
        sentence_index=index,
        claim=claim,
        admitted=True,
        reasons=("VERBATIM_ANCHOR_VERIFIED",),
        evidence_verifications=tuple(verified),
        action=action,
    )


def _contains_verbatim(sentence: str, quote: str) -> bool:
    # Quotes are compared literally after whitespace normalization only.  We do not
    # use semantic similarity, fuzzy matching, stemming, or model-generated rationale.
    return _clean_sentence(quote) in _clean_sentence(sentence)


def require_admitted_composition(
    claims: str | Sequence[str] | Sequence[SentenceClaim | Mapping[str, Any]],
    evidence_resolver: EvidenceResolver | Mapping[Any, Any] | Callable[..., Any],
    *,
    connective_policy: ConnectivePolicy | None = None,
) -> CompositionAdmission:
    """Compile only an admitted composition; raise on the first unanchored sentence."""

    audit = audit_sentences(
        claims,
        evidence_resolver,
        connective_policy=connective_policy,
        action=EnforcementAction.BLOCK,
    )
    if not audit.admitted:
        failed = next(item for item in audit.sentences if not item.admitted)
        reason = failed.reasons[1] if len(failed.reasons) > 1 else "composition failed grounding verification"
        raise NoUnanchoredInventionError(
            reason,
            sentence_index=failed.sentence_index,
            context=failed.to_dict(),
        )
    return CompositionAdmission(text=" ".join(audit.admitted_sentences), audit=audit)


def purge_unanchored_sentences(
    claims: str | Sequence[str] | Sequence[SentenceClaim | Mapping[str, Any]],
    evidence_resolver: EvidenceResolver | Mapping[Any, Any] | Callable[..., Any],
    *,
    connective_policy: ConnectivePolicy | None = None,
) -> CompositionAdmission:
    """Return only sentences that pass M029, while preserving the full purge audit."""

    audit = audit_sentences(
        claims,
        evidence_resolver,
        connective_policy=connective_policy,
        action=EnforcementAction.PURGE,
    )
    return CompositionAdmission(text=" ".join(audit.admitted_sentences), audit=audit)


def flag_unanchored_sentences(
    claims: str | Sequence[str] | Sequence[SentenceClaim | Mapping[str, Any]],
    evidence_resolver: EvidenceResolver | Mapping[Any, Any] | Callable[..., Any],
    *,
    connective_policy: ConnectivePolicy | None = None,
) -> CompositionAuditReport:
    """Run the same hard predicate while retaining all candidate content for review."""

    return audit_sentences(
        claims,
        evidence_resolver,
        connective_policy=connective_policy,
        action=EnforcementAction.FLAG,
    )


def evidence_reference_from_object(result: Mapping[str, Any]) -> EvidenceRef:
    """Extract the canonical object reference returned by a repository operation."""

    obj = result["object"] if isinstance(result.get("object"), Mapping) else result
    return EvidenceRef.from_mapping(
        {
            "object_id": obj.get("object_id", obj.get("evidence_id")),
            "version": obj.get("version", obj.get("revision_id", obj.get("revision"))),
            "sha256": obj.get("sha256", obj.get("canonical_sha256")),
        }
    )


__all__ = [
    "ADMITTED_EVIDENCE_STATES",
    "CA_M029",
    "FR_029",
    "INVARIANT_ID",
    "POLICY_VERSION",
    "CompositionAdmission",
    "CompositionAuditReport",
    "ConnectivePolicy",
    "ConnectiveTransformationError",
    "EnforcementAction",
    "EvidenceAdmissionError",
    "EvidenceRef",
    "EvidenceResolutionError",
    "EvidenceRevisionMismatchError",
    "EvidenceVerification",
    "GroundingClass",
    "NoUnanchoredInventionError",
    "SentenceAudit",
    "SentenceClaim",
    "UnanchoredClaimError",
    "VerbatimAnchor",
    "VerbatimMismatchError",
    "audit_sentences",
    "evidence_reference_from_object",
    "extract_sentences",
    "flag_unanchored_sentences",
    "purge_unanchored_sentences",
    "require_admitted_composition",
    "verify_evidence_reference",
]
