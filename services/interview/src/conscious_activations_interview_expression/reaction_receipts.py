"""
CA-M020 — Reaction Receipts as First-Class Evidence.

A Reaction Receipt is a content-addressed evidence token.  It may only be
minted when the reaction is bound to an exact CA-M021 sovereign-media
coordinate and to the exact admitted source-package revision that owns that
media asset.

The proof is intentionally composed only from canonical, persisted inputs:

    source package ref + media coordinates + actor + actor timestamp
    + reaction payload + optional supporting observation refs

Changing any of those fields changes the proof and the content address.  A
verifier can therefore reject a stale/edited token without trusting a caller's
"linked" flag.  The repository's immutable-by-reference object revisions are
used as the persistence boundary; the verifier always resolves the exact
source-package and receipt digests carried by the token.

This module does not implement a private-key signature scheme.  The
cryptographic claim here is tamper-evident, content-addressed integrity and
source dissociation prevention using SHA-256 over canonical CA data.  It does
not establish actor authenticity by itself; actor identity remains an
application-level assertion in the current development runtime.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from typing import Any

from ca_contracts import canonical_sha256

from .anchor_coordinates import require_exact_anchor_coordinates, validate_coordinates_within_source
from .canonical import exact_keys, immutable_ref, require_ref, require_sha, require_string, semantic_id
from .errors import ValidationError
from .repository import InterviewRepository


CA_M020 = "CA-M020"
FR_020 = "FR-020"
REACTION_RECEIPT_SCHEMA_VERSION = "1.0.0"
REACTION_RECEIPT_OBJECT_TYPE = "reaction_receipt"
REACTION_RECEIPT_ID_PREFIX = "ie:reaction-receipt"
HASH_ALGORITHM = "SHA-256"


_RECEIPT_PROOF_FIELDS = frozenset(
    {
        "algorithm",
        "coordinate_binding_sha256",
        "receipt_binding_sha256",
        "source_package_sha256",
        "source_media_sha256",
    }
)


def _require_utc_timestamp(value: Any, name: str) -> str:
    text = require_string(value, name)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError(
            f"{name} must be an RFC-3339 timestamp"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise ValidationError(f"{name} must include a UTC offset")
    # Normalize only the representation stored in the token.  This makes the
    # exact actor timestamp part of the content-addressed proof.
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _contract_safe(value: Any) -> Any:
    """Map values into the ca_contracts canonical subset (no floats)."""

    if isinstance(value, float):
        return format(value, ".15g")
    if isinstance(value, Mapping):
        return {str(key): _contract_safe(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_contract_safe(item) for item in value]
    return value


def _normalize_observation_refs(value: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    refs = [require_ref(item, f"observation_refs[{i}]") for i, item in enumerate(value)]
    ids = [item["object_id"] for item in refs]
    if len(ids) != len(set(ids)):
        raise ValidationError("observation_refs must not contain duplicates")
    return sorted(refs, key=lambda item: item["object_id"])


def _normalize_media_coordinates(
    value: Mapping[str, Any],
    *,
    source_package_payload: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate exact CA-M021 coordinates and bind them to the package asset."""

    # Stored receipts re-enter this helper with the fingerprint already bound.
    if not isinstance(value, Mapping):
        raise ValidationError(
            "media_coordinates must be a mapping",
            context={"classification": "FR_020_COORDINATES_REQUIRED"},
        )
    raw_coordinates = dict(value)
    raw_coordinates.pop("stream_metadata_fingerprint", None)
    coordinates = require_exact_anchor_coordinates(raw_coordinates, "media_coordinates")

    assets = source_package_payload.get("media_assets")
    if not isinstance(assets, list) or not assets:
        raise ValidationError(
            "source package contains no sovereign media assets",
            context={"classification": "FR_020_SOURCE_MEDIA_MISSING"},
        )

    asset = next(
        (
            item
            for item in assets
            if isinstance(item, Mapping)
            and item.get("asset_id") == coordinates["media_asset_id"]
            and item.get("sha256") == coordinates["media_sha256"]
        ),
        None,
    )
    if asset is None:
        raise ValidationError(
            "reaction media coordinates are not bound to a media asset in the admitted source package",
            context={"classification": "FR_020_MEDIA_DISSOCIATED"},
        )

    validate_coordinates_within_source(coordinates, asset, "media_coordinates")

    # CA-M021 validates the temporal envelope.  Also prove that byte offsets
    # cannot point past the admitted sovereign asset length.
    byte_count = asset.get("bytes")
    if isinstance(byte_count, int) and byte_count > 0:
        if coordinates["byte_offset_end"] > byte_count:
            raise ValidationError(
                "reaction media byte span exceeds the admitted sovereign media asset",
                context={"classification": "FR_020_BYTE_SPAN_OUT_OF_BOUNDS"},
            )

    technical = asset.get("technical")
    if not isinstance(technical, Mapping):
        technical = {}

    # If stream timing metadata exists, retain its exact source timebase as a
    # proof input.  We never infer a replacement timebase here.
    stream_fingerprint: dict[str, Any] | str = "NOT_DECLARED"
    streams = technical.get("streams")
    if isinstance(streams, list) and streams:
        stream_fingerprint = [
            {
                "index": item.get("index"),
                "codec_type": item.get("codec_type"),
                "time_base": item.get("time_base"),
            }
            for item in streams
            if isinstance(item, Mapping)
        ]

    return {
        **coordinates,
        "stream_metadata_fingerprint": stream_fingerprint,
    }


def _coordinate_binding_sha256(
    *,
    source_package_ref: Mapping[str, str],
    media_coordinates: Mapping[str, Any],
) -> str:
    binding = {
        "source_package_ref": dict(source_package_ref),
        "media_coordinates": dict(media_coordinates),
        "mandate_id": CA_M020,
        "invariant_id": FR_020,
    }
    return canonical_sha256(binding)


def _proof_sha256(
    *,
    receipt_binding: Mapping[str, Any],
    coordinate_binding_sha256: str,
    source_package_sha256: str,
    source_media_sha256: str,
) -> str:
    return canonical_sha256(
        {
            "algorithm": HASH_ALGORITHM,
            "coordinate_binding_sha256": coordinate_binding_sha256,
            "receipt_binding": dict(receipt_binding),
            "source_package_sha256": source_package_sha256,
            "source_media_sha256": source_media_sha256,
        }
    )


class ReactionReceiptEvidenceService:
    """Authoritative admission and verification boundary for CA-M020 receipts."""

    OBJECT_TYPE = REACTION_RECEIPT_OBJECT_TYPE
    MANDATE_ID = CA_M020
    INVARIANT_ID = FR_020
    SCHEMA_VERSION = REACTION_RECEIPT_SCHEMA_VERSION

    def __init__(self, repository: InterviewRepository):
        self.repository = repository

    def admit(
        self,
        *,
        source_package_ref: Mapping[str, Any],
        actor_id: str,
        actor_timestamp_utc: str,
        reaction_kind: str,
        reaction: Mapping[str, Any],
        media_coordinates: Mapping[str, Any],
        observation_refs: Sequence[Mapping[str, Any]] = (),
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Mint and persist one first-class, media-bound Reaction Receipt."""

        source_ref = require_ref(source_package_ref, "source_package_ref")
        actor = require_string(actor_id, "actor_id")
        actor_timestamp = _require_utc_timestamp(actor_timestamp_utc, "actor_timestamp_utc")
        kind = require_string(reaction_kind, "reaction_kind")
        if not isinstance(reaction, Mapping):
            raise ValidationError("reaction must be an object")
        reaction_payload = _contract_safe(dict(reaction))
        observations = _normalize_observation_refs(observation_refs)

        # Resolve the exact admitted source-package revision.  This is a hard
        # provenance boundary; no caller-supplied package/media boolean is
        # trusted as proof of linkage.
        try:
            source_package = self.repository.get_object_by_sha(
                source_ref["object_id"], source_ref["sha256"]
            )
        except Exception as exc:
            raise ValidationError(
                "source_package_ref is stale or missing",
                context={"classification": "FR_020_SOURCE_REF_INVALID"},
            ) from exc

        if source_package["object_type"] != "canonical_interview_source_package":
            raise ValidationError(
                "source_package_ref does not resolve to a canonical interview source package",
                context={"classification": "FR_020_SOURCE_OBJECT_TYPE_INVALID"},
            )
        if source_package["version"] != source_ref["version"]:
            raise ValidationError(
                "source package version does not match source_package_ref",
                context={"classification": "FR_020_SOURCE_VERSION_MISMATCH"},
            )

        coordinates = _normalize_media_coordinates(
            media_coordinates,
            source_package_payload=source_package["payload"],
        )

        if not observations:
            observation_state = "DIRECT_CAPTURE"
        else:
            observation_state = "SUPPORTED_BY_OBSERVATIONS"

        # The actor timestamp is deliberately an explicit required input; a
        # verifier can distinguish when the reaction was observed from when it
        # was sealed into the repository.
        core = {
            "source_package_ref": dict(source_ref),
            "source_package_sha256": source_ref["sha256"],
            "source_media_sha256": coordinates["media_sha256"],
            "media_coordinates": coordinates,
            "actor_id": actor,
            "actor_timestamp_utc": actor_timestamp,
            "reaction_kind": kind,
            "reaction": reaction_payload,
            "observation_refs": observations,
            "observation_state": observation_state,
            "mandate_id": CA_M020,
            "invariant_id": FR_020,
            "schema_version": REACTION_RECEIPT_SCHEMA_VERSION,
        }
        object_id = semantic_id(REACTION_RECEIPT_ID_PREFIX, core)
        receipt_binding = {
            "reaction_receipt_id": object_id,
            "source_package_ref": dict(source_ref),
            "source_media_sha256": coordinates["media_sha256"],
            "media_coordinates": coordinates,
            "actor_id": actor,
            "actor_timestamp_utc": actor_timestamp,
            "reaction_kind": kind,
            "reaction": reaction_payload,
            "observation_refs": observations,
            "observation_state": observation_state,
            "mandate_id": CA_M020,
            "invariant_id": FR_020,
            "schema_version": REACTION_RECEIPT_SCHEMA_VERSION,
        }
        coordinate_binding_sha256 = _coordinate_binding_sha256(
            source_package_ref=source_ref,
            media_coordinates=coordinates,
        )
        proof_sha256 = _proof_sha256(
            receipt_binding=receipt_binding,
            coordinate_binding_sha256=coordinate_binding_sha256,
            source_package_sha256=source_ref["sha256"],
            source_media_sha256=coordinates["media_sha256"],
        )
        payload = {
            **core,
            "reaction_receipt_id": object_id,
            "version": REACTION_RECEIPT_SCHEMA_VERSION,
            "evidence_class": "FIRST_CLASS_REACTION_RECEIPT",
            "lifecycle_state": "VERIFIED",
            "proof": {
                "algorithm": HASH_ALGORITHM,
                "coordinate_binding_sha256": coordinate_binding_sha256,
                "receipt_binding_sha256": canonical_sha256(receipt_binding),
                "source_package_sha256": source_ref["sha256"],
                "source_media_sha256": coordinates["media_sha256"],
                "proof_sha256": proof_sha256,
            },
            "validation": {
                "status": "PASS",
                "media_coordinate_verified": True,
                "source_package_verified": True,
                "source_media_digest_bound": True,
                "actor_timestamp_present": True,
                "cryptographic_proof_verified": True,
                "first_class_evidence": True,
                "mandate_id": CA_M020,
                "invariant_id": FR_020,
            },
        }

        result = self.repository.store_object(
            REACTION_RECEIPT_OBJECT_TYPE,
            payload,
            object_id=object_id,
            idempotency_key=idempotency_key,
            lifecycle_state="VERIFIED",
        )
        self.repository.add_edge(
            source_ref["object_id"],
            object_id,
            "source_of_reaction_receipt",
        )
        for observation in observations:
            self.repository.add_edge(
                observation["object_id"],
                object_id,
                "supports_reaction_receipt",
            )

        result["receipt"] = {
            "command": "admit_reaction_receipt",
            "mandate_id": CA_M020,
            "invariant_id": FR_020,
            "object_ref": immutable_ref(
                object_id,
                payload,
                version=REACTION_RECEIPT_SCHEMA_VERSION,
            ),
            "evidence_class": "FIRST_CLASS_REACTION_RECEIPT",
            "actor_id": actor,
            "actor_timestamp_utc": actor_timestamp,
            "source_package_ref": dict(source_ref),
            "source_media_sha256": coordinates["media_sha256"],
            "media_coordinates": coordinates,
            "proof_sha256": proof_sha256,
            "validation_status": "PASS",
        }
        return result

    # ``create_receipt`` is a compatibility alias for callers that use the
    # existing interview-expression reaction vocabulary.
    create_receipt = admit

    def verify(self, receipt_ref: Mapping[str, Any]) -> dict[str, Any]:
        """Re-resolve and cryptographically verify a persisted receipt."""

        ref = require_ref(receipt_ref, "reaction_receipt_ref")
        stored = self.repository.get_object_by_sha(ref["object_id"], ref["sha256"])
        if stored["object_type"] != REACTION_RECEIPT_OBJECT_TYPE:
            raise ValidationError(
                "receipt ref does not resolve to reaction_receipt",
                context={"classification": "FR_020_RECEIPT_TYPE_INVALID"},
            )
        payload = stored["payload"]
        if payload.get("version") != REACTION_RECEIPT_SCHEMA_VERSION:
            raise ValidationError("reaction receipt schema version mismatch")
        if payload.get("reaction_receipt_id") != ref["object_id"]:
            raise ValidationError("reaction receipt object identity mismatch")
        if stored["sha256"] != ref["sha256"]:
            raise ValidationError("reaction receipt digest mismatch")

        source_ref = require_ref(payload.get("source_package_ref"), "source_package_ref")
        source_package = self.repository.get_object_by_sha(
            source_ref["object_id"], source_ref["sha256"]
        )
        if source_package["version"] != source_ref["version"]:
            raise ValidationError("receipt source package version mismatch")

        coordinates = _normalize_media_coordinates(
            payload.get("media_coordinates"),
            source_package_payload=source_package["payload"],
        )
        if coordinates != payload.get("media_coordinates"):
            raise ValidationError(
                "stored reaction media coordinates are not canonical",
                context={"classification": "FR_020_COORDINATE_MUTATION"},
            )

        actor = require_string(payload.get("actor_id"), "actor_id")
        actor_timestamp = _require_utc_timestamp(
            payload.get("actor_timestamp_utc"), "actor_timestamp_utc"
        )
        kind = require_string(payload.get("reaction_kind"), "reaction_kind")
        reaction = payload.get("reaction")
        if not isinstance(reaction, Mapping):
            raise ValidationError("stored reaction payload is invalid")
        observations = _normalize_observation_refs(payload.get("observation_refs", []))
        observation_state = require_string(
            payload.get("observation_state"), "observation_state"
        )

        core = {
            "source_package_ref": dict(source_ref),
            "source_package_sha256": source_ref["sha256"],
            "source_media_sha256": coordinates["media_sha256"],
            "media_coordinates": coordinates,
            "actor_id": actor,
            "actor_timestamp_utc": actor_timestamp,
            "reaction_kind": kind,
            "reaction": dict(reaction),
            "observation_refs": observations,
            "observation_state": observation_state,
            "mandate_id": CA_M020,
            "invariant_id": FR_020,
            "schema_version": REACTION_RECEIPT_SCHEMA_VERSION,
        }
        expected_object_id = semantic_id(REACTION_RECEIPT_ID_PREFIX, core)
        if expected_object_id != payload["reaction_receipt_id"]:
            raise ValidationError(
                "reaction receipt content address does not match its persisted content",
                context={"classification": "FR_020_CONTENT_ADDRESS_INVALID"},
            )

        receipt_binding = {
            "reaction_receipt_id": expected_object_id,
            "source_package_ref": dict(source_ref),
            "source_media_sha256": coordinates["media_sha256"],
            "media_coordinates": coordinates,
            "actor_id": actor,
            "actor_timestamp_utc": actor_timestamp,
            "reaction_kind": kind,
            "reaction": dict(reaction),
            "observation_refs": observations,
            "observation_state": observation_state,
            "mandate_id": CA_M020,
            "invariant_id": FR_020,
            "schema_version": REACTION_RECEIPT_SCHEMA_VERSION,
        }
        expected_coordinate_binding = _coordinate_binding_sha256(
            source_package_ref=source_ref,
            media_coordinates=coordinates,
        )
        expected_receipt_binding = canonical_sha256(receipt_binding)
        expected_proof = _proof_sha256(
            receipt_binding=receipt_binding,
            coordinate_binding_sha256=expected_coordinate_binding,
            source_package_sha256=source_ref["sha256"],
            source_media_sha256=coordinates["media_sha256"],
        )

        proof = payload.get("proof")
        if not isinstance(proof, Mapping) or set(proof) != _RECEIPT_PROOF_FIELDS | {"proof_sha256"}:
            raise ValidationError(
                "reaction receipt proof shape is invalid",
                context={"classification": "FR_020_PROOF_SHAPE_INVALID"},
            )
        if proof.get("algorithm") != HASH_ALGORITHM:
            raise ValidationError("reaction receipt proof algorithm mismatch")
        if proof.get("coordinate_binding_sha256") != expected_coordinate_binding:
            raise ValidationError(
                "reaction receipt coordinate proof mismatch",
                context={"classification": "FR_020_COORDINATE_PROOF_INVALID"},
            )
        if proof.get("receipt_binding_sha256") != expected_receipt_binding:
            raise ValidationError(
                "reaction receipt binding proof mismatch",
                context={"classification": "FR_020_RECEIPT_PROOF_INVALID"},
            )
        if proof.get("source_package_sha256") != source_ref["sha256"]:
            raise ValidationError("reaction receipt source package proof mismatch")
        if proof.get("source_media_sha256") != coordinates["media_sha256"]:
            raise ValidationError("reaction receipt source media proof mismatch")
        if proof.get("proof_sha256") != expected_proof:
            raise ValidationError(
                "reaction receipt cryptographic proof mismatch",
                context={"classification": "FR_020_PROOF_INVALID"},
            )

        return {
            "status": "VERIFIED",
            "mandate_id": CA_M020,
            "invariant_id": FR_020,
            "evidence_class": "FIRST_CLASS_REACTION_RECEIPT",
            "reaction_receipt_ref": dict(ref),
            "source_package_ref": dict(source_ref),
            "source_media_sha256": coordinates["media_sha256"],
            "media_coordinates": coordinates,
            "actor_id": actor,
            "actor_timestamp_utc": actor_timestamp,
            "proof_sha256": expected_proof,
            "cryptographic_proof_verified": True,
            "first_class_evidence": True,
        }


# Clear public aliases for codebases that prefer the shorter service name.
ReactionReceiptService = ReactionReceiptEvidenceService


def verify_reaction_receipt(
    repository: InterviewRepository,
    receipt_ref: Mapping[str, Any],
) -> dict[str, Any]:
    """Functional verification helper for integration boundaries/tests."""

    return ReactionReceiptEvidenceService(repository).verify(receipt_ref)
