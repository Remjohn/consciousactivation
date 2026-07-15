"""JSON Schema helpers and shared delegation contract definitions."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


PROTOCOL_VERSION = "1.0"
PACKAGE_VERSION = "1.1.0-rc.4"
VISUAL_ASSET_DEMAND_VERSION = "1.1"
COMPATIBILITY_PROFILE_VERSION = "1.0"
MESSAGE_VERSIONS = {"visual-asset-demand": VISUAL_ASSET_DEMAND_VERSION}
SCHEMA_BASE = "https://contracts.cmf.dev/delegation"
PRINCIPAL_TYPES = [
    "CONTENT_HARNESS",
    "DELEGATION_PROTOCOL",
    "VISUAL_ASSET_EDITOR",
    "CONTROL_TOWER",
]
STATES = [
    "DRAFT",
    "SUBMITTED",
    "REJECTED",
    "ACCEPTED",
    "IN_PROGRESS",
    "RESULT_READY",
    "RESULT_REJECTED",
    "COMPLETED",
    "AMENDMENT_REQUIRED",
    "SUPERSEDED",
    "COST_APPROVAL_REQUIRED",
    "CAPABILITY_GAP",
    "HUMAN_REVIEW_REQUIRED",
    "CANCELLATION_REQUESTED",
    "CANCELLED",
    "PARTIAL_RESULT_READY",
    "INVALIDATED",
    "REVOKED",
    "REPLACED",
]


def string(**kwargs: Any) -> dict[str, Any]:
    return {"type": "string", **kwargs}


def integer(**kwargs: Any) -> dict[str, Any]:
    return {"type": "integer", **kwargs}


def boolean() -> dict[str, Any]:
    return {"type": "boolean"}


def array(items: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
    return {"type": "array", "items": items, **kwargs}


def obj(
    properties: dict[str, Any],
    required: list[str] | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": properties,
        "required": required if required is not None else list(properties),
        **kwargs,
    }


def ref(name: str) -> dict[str, Any]:
    return {"$ref": f"#/$defs/{name}"}


def nullable(schema: dict[str, Any]) -> dict[str, Any]:
    return {"anyOf": [schema, {"type": "null"}]}


HASH = string(pattern=r"^sha256:[0-9a-f]{64}$")
IDENTIFIER = string(pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
VERSION = string(pattern=r"^[0-9]+\.[0-9]+$")
TIMESTAMP = string(format="date-time")
URI = string(format="uri")
JSON_POINTER = string(pattern=r"^(?:/(?:[^~/]|~0|~1)*)*$")


COMMON_DEFS: dict[str, Any] = {
    "PrincipalRef": obj(
        {
            "principal_id": IDENTIFIER,
            "principal_type": string(enum=PRINCIPAL_TYPES),
            "product_version": VERSION,
        }
    ),
    "DemandIdentityRef": obj(
        {
            "request_id": IDENTIFIER,
            "version": integer(minimum=1),
            "payload_hash": HASH,
            "canonical_ref": URI,
        }
    ),
    "ResourceIdentityRef": obj(
        {
            "resource_id": IDENTIFIER,
            "version": string(minLength=1, maxLength=64),
            "payload_hash": HASH,
            "canonical_ref": URI,
        }
    ),
    "ResultIdentityRef": obj(
        {
            "result_id": IDENTIFIER,
            "version": integer(minimum=1),
            "payload_hash": HASH,
            "canonical_ref": URI,
        }
    ),
    "ExecutionIdentityRef": obj(
        {
            "execution_id": IDENTIFIER,
            "demand": ref("DemandIdentityRef"),
            "plan_ref": ref("ResourceIdentityRef"),
        }
    ),
    "AuthorityClaim": obj(
        {
            "action": string(minLength=1, maxLength=96),
            "principal": ref("PrincipalRef"),
            "field_scopes": array(JSON_POINTER, minItems=1, uniqueItems=True),
        }
    ),
    "IntegrityProof": obj(
        {
            "algorithm": string(const="Ed25519"),
            "key_id": URI,
            "signer": ref("PrincipalRef"),
            "signature": string(pattern=r"^[A-Za-z0-9_-]{86}$"),
            "issued_at": TIMESTAMP,
            "expires_at": nullable(TIMESTAMP),
            "nonce": IDENTIFIER,
        }
    ),
    "FailureSummary": obj(
        {
            "code": string(pattern=r"^[A-Z][A-Z0-9_]{2,63}$"),
            "category": string(
                enum=[
                    "VALIDATION",
                    "AUTHORITY",
                    "COMPATIBILITY",
                    "BUDGET",
                    "EXECUTION",
                    "INTEGRITY",
                    "LIFECYCLE",
                    "CAPABILITY",
                    "HUMAN_REVIEW",
                    "SECURITY",
                ]
            ),
            "message": string(minLength=1, maxLength=1024),
            "retryable": boolean(),
            "field_paths": array(JSON_POINTER, uniqueItems=True),
        }
    ),
    "MoneyAmount": obj(
        {
            "currency": string(pattern=r"^[A-Z]{3}$"),
            "minor_units": integer(minimum=0),
        }
    ),
    "BoundingBoxBasisPoints": obj(
        {
            "x": integer(minimum=0, maximum=10000),
            "y": integer(minimum=0, maximum=10000),
            "width": integer(minimum=1, maximum=10000),
            "height": integer(minimum=1, maximum=10000),
        }
    ),
    "EvidenceFinding": obj(
        {
            "code": string(pattern=r"^[A-Z][A-Z0-9_]{2,63}$"),
            "verdict": string(enum=["PASS", "CONCERNS", "FAIL"]),
            "evidence_refs": array(ref("ResourceIdentityRef"), minItems=1),
            "note": nullable(string(maxLength=1024)),
        }
    ),
    "ChangeItem": obj(
        {
            "path": JSON_POINTER,
            "operation": string(enum=["ADD", "REMOVE", "REPLACE"]),
            "value_ref": nullable(ref("ResourceIdentityRef")),
            "reason": string(minLength=1, maxLength=1024),
        }
    ),
    "State": string(enum=STATES),
}


def message_schema(
    message_type: str,
    title: str,
    properties: dict[str, Any],
    required: list[str] | None = None,
) -> dict[str, Any]:
    message_version = MESSAGE_VERSIONS.get(message_type, PROTOCOL_VERSION)
    schema = obj(properties, required)
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"{SCHEMA_BASE}/{message_type}/{message_version}/schema.json",
        "title": title,
        "description": f"CMF delegation protocol {message_type} message.",
        "x-cmf-message-type": message_type,
        "x-cmf-message-version": message_version,
        **schema,
        "$defs": deepcopy(COMMON_DEFS),
    }


def hash_value(character: str) -> str:
    return "sha256:" + character * 64


def demand_ref(request_id: str = "req-format02-001", version: int = 1) -> dict[str, Any]:
    return {
        "request_id": request_id,
        "version": version,
        "payload_hash": hash_value("a"),
        "canonical_ref": f"cmf-contract://demands/{request_id}/{version}",
    }


def resource_ref(resource_id: str, version: str = "1.0") -> dict[str, Any]:
    return {
        "resource_id": resource_id,
        "version": version,
        "payload_hash": hash_value("b"),
        "canonical_ref": f"cmf-contract://resources/{resource_id}/{version}",
    }


def result_ref(result_id: str = "result-format02-001", version: int = 1) -> dict[str, Any]:
    return {
        "result_id": result_id,
        "version": version,
        "payload_hash": hash_value("c"),
        "canonical_ref": f"cmf-contract://results/{result_id}/{version}",
    }


def principal(principal_type: str) -> dict[str, Any]:
    ids = {
        "CONTENT_HARNESS": "content-harness",
        "DELEGATION_PROTOCOL": "delegation-protocol",
        "VISUAL_ASSET_EDITOR": "visual-asset-editor",
        "CONTROL_TOWER": "control-tower",
    }
    return {
        "principal_id": ids[principal_type],
        "principal_type": principal_type,
        "product_version": "1.0",
    }
