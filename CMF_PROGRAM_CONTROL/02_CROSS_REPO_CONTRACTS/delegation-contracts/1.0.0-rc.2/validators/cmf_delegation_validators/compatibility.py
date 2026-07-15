"""Compatibility negotiation and deterministic legacy adaptation."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .canonical import canonical_hash


class CompatibilityError(ValueError):
    """Raised when peers or legacy data cannot be safely reconciled."""


def negotiate(requester: dict[str, Any], provider: dict[str, Any]) -> dict[str, Any]:
    common_protocols = sorted(
        set(requester.get("protocol_versions", [])) & set(provider.get("protocol_versions", [])),
        reverse=True,
    )
    required_features = set(requester.get("required_features", []))
    available_features = set(provider.get("required_features", []))
    common_algorithms = sorted(
        set(requester.get("signature_algorithms", []))
        & set(provider.get("signature_algorithms", []))
    )
    if not common_protocols:
        raise CompatibilityError("No common protocol version")
    if not required_features.issubset(available_features):
        missing = sorted(required_features - available_features)
        raise CompatibilityError(f"Missing required features: {missing}")
    if not common_algorithms:
        raise CompatibilityError("No common signature algorithm")
    return {
        "protocol_version": common_protocols[0],
        "features": sorted(required_features),
        "signature_algorithm": common_algorithms[0],
    }


def adapt_legacy_demand_ref(legacy: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    expected = {"request_id", "version", "payload_hash", "canonical_ref"}
    if set(context) != expected:
        raise CompatibilityError("Pinned demand identity context must contain exactly four fields")
    if legacy.get("demand_ref") != context["request_id"]:
        raise CompatibilityError("Legacy demand_ref does not match pinned request_id")
    if not isinstance(context["version"], int) or context["version"] < 1:
        raise CompatibilityError("Pinned demand identity version must be a positive integer")
    if not isinstance(context["payload_hash"], str) or not context["payload_hash"].startswith("sha256:"):
        raise CompatibilityError("Pinned demand identity requires a SHA-256 payload hash")
    return deepcopy(context)


def migrate_legacy_submission_receipt(
    source: dict[str, Any], owner_evidence: dict[str, Any]
) -> dict[str, Any]:
    required_source = {
        "legacy_schema",
        "legacy_receipt_id",
        "protocol_validation_payload",
        "vae_admission_payload",
        "migrated_at",
    }
    if set(source) != required_source or source["legacy_schema"] != "submission-receipt@0.1":
        raise CompatibilityError("Legacy submission receipt source is incomplete or unsupported")
    required_evidence = {
        "protocol_validation_producer",
        "vae_admission_producer",
        "evidence_ref",
        "output_ref",
    }
    if set(owner_evidence) != required_evidence:
        raise CompatibilityError("MIGRATION_REQUIRED: complete owner evidence is mandatory")
    if owner_evidence["protocol_validation_producer"] != "DELEGATION_PROTOCOL":
        raise CompatibilityError("Protocol validation fact has the wrong owner")
    if owner_evidence["vae_admission_producer"] != "VISUAL_ASSET_EDITOR":
        raise CompatibilityError("VAE admission fact has the wrong owner")
    validation_target = deepcopy(source["protocol_validation_payload"])
    admission_target = deepcopy(source["vae_admission_payload"])
    from .contracts import validate_payload

    try:
        validate_payload("submission-validation-receipt", validation_target)
        validate_payload("admission-receipt", admission_target)
    except Exception as exc:
        raise CompatibilityError("TARGET_INVALID: migrated owner fact does not match its schema") from exc
    return {
        "targets": {
            "submission_validation_receipt": validation_target,
            "admission_receipt": admission_target,
        },
        "receipt": {
            "migration_id": "migration-submission-receipt-split-1",
            "source_message_type": "submission-receipt",
            "source_version": "0.1",
            "target_version": "1.0",
            "source_payload_hash": canonical_hash(source),
            "target_artifacts": [
                {
                    "message_type": "submission-validation-receipt",
                    "payload_hash": canonical_hash(validation_target),
                    "canonical_ref": "cmf-contract://migrations/migration-submission-receipt-split-1/validation",
                },
                {
                    "message_type": "admission-receipt",
                    "payload_hash": canonical_hash(admission_target),
                    "canonical_ref": "cmf-contract://migrations/migration-submission-receipt-split-1/admission",
                },
            ],
            "ordered_transformations": ["extract_protocol_validation", "extract_vae_admission"],
            "authority_effect_analysis": [
                {
                    "target_path": "/submission_validation_receipt",
                    "value_owner": "DELEGATION_PROTOCOL",
                    "effect": "SPLIT_WITH_EVIDENCE",
                },
                {
                    "target_path": "/admission_receipt",
                    "value_owner": "VISUAL_ASSET_EDITOR",
                    "effect": "SPLIT_WITH_EVIDENCE",
                },
            ],
            "source_validation": "PASS",
            "target_validation": "PASS",
            "equivalence": "PASS",
            "output_ref": deepcopy(owner_evidence["output_ref"]),
            "evidence_refs": [deepcopy(owner_evidence["evidence_ref"])],
            "lossless": True,
            "migrated_at": source["migrated_at"],
        },
    }
