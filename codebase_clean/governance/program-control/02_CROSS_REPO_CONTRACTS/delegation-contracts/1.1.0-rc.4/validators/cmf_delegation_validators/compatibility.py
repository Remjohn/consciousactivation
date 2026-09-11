"""Compatibility negotiation and deterministic legacy adaptation."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .canonical import canonical_hash


class CompatibilityError(ValueError):
    """Raised when peers or legacy data cannot be safely reconciled."""


CONSTITUTIONAL_DOMAINS = {
    "source_provenance",
    "activative_semantic_lineage",
    "activation_contract",
    "visual_semantic_pack",
    "visual_narrative_program",
    "feature_contracts",
    "somatic_route_request",
    "expression_moment_lineage",
    "wrong_reading_locks",
    "derivative_lock_inheritance",
}
SOURCE_KINDS = (
    "interview_expression",
    "public_comment",
    "direct_message_reply",
    "authored_source",
    "live_premise",
    "research_synthesis",
    "operator_supplied",
    "legacy_migrated",
)
PROHIBITED_ADAPTER_EFFECTS = {"DROP", "WEAKEN", "SYNTHESIZE", "FLATTEN", "REINTERPRET"}
REQUIRED_DERIVATIVE_LOCK_MODES = {"PRESERVE", "ENFORCE"}


def _domain_map(items: Any, *, field: str) -> dict[str, dict[str, Any]]:
    if not isinstance(items, list):
        raise CompatibilityError(f"{field} must be an explicit list")
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("domain"), str):
            raise CompatibilityError(f"{field} contains an invalid domain claim")
        domain = item["domain"]
        if domain in result:
            raise CompatibilityError(f"{field} contains duplicate domain {domain}")
        result[domain] = item
    return result


def _message_version_map(items: Any) -> dict[str, set[str]]:
    if not isinstance(items, list):
        raise CompatibilityError("message_versions must be an explicit list")
    result: dict[str, set[str]] = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("message_type"), str):
            raise CompatibilityError("message_versions contains an invalid claim")
        versions = set(item.get("accepted_versions", [])) | set(item.get("emitted_versions", []))
        if not versions and isinstance(item.get("version"), str):
            versions.add(item["version"])
        if not versions:
            raise CompatibilityError(f"No versions declared for {item['message_type']}")
        result.setdefault(item["message_type"], set()).update(versions)
    return result


def validate_adapter_claim(
    adapter_claim: dict[str, Any], protected_paths: list[str] | tuple[str, ...]
) -> None:
    if adapter_claim.get("lossless") is not True:
        raise CompatibilityError("LOSSY_ADAPTER: adapter does not make a lossless claim")
    protected = tuple(protected_paths)
    for effect in adapter_claim.get("effects", []):
        operation = effect.get("operation")
        path = effect.get("path", "")
        touches_protected = any(
            path == candidate or path.startswith(candidate + "/") for candidate in protected
        )
        if operation in PROHIBITED_ADAPTER_EFFECTS or touches_protected:
            raise CompatibilityError(
                f"LOSSY_ADAPTER: {operation or 'UNKNOWN'} at protected path {path or '<missing>'}"
            )


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
    requested_versions = _message_version_map(requester.get("message_versions"))
    provided_versions = _message_version_map(provider.get("message_versions"))
    negotiated_versions: dict[str, str] = {}
    for message_type, versions in requested_versions.items():
        common_versions = sorted(versions & provided_versions.get(message_type, set()), reverse=True)
        if not common_versions:
            raise CompatibilityError(f"No common message version for {message_type}")
        negotiated_versions[message_type] = common_versions[0]

    requirements = _domain_map(
        requester.get("required_semantic_domains"), field="required_semantic_domains"
    )
    capabilities = _domain_map(
        provider.get("semantic_capabilities"), field="semantic_capabilities"
    )
    missing_domains = sorted(CONSTITUTIONAL_DOMAINS - set(requirements))
    if missing_domains:
        raise CompatibilityError(
            f"Required constitutional domains are undeclared: {missing_domains}"
        )
    requested_capabilities = _domain_map(
        requester.get("semantic_capabilities"), field="semantic_capabilities"
    )
    selected_capabilities: list[dict[str, Any]] = []
    for domain, requirement in requirements.items():
        capability = capabilities.get(domain)
        if capability is None:
            raise CompatibilityError(
                f"SEMANTIC_ENFORCEMENT_UNSUPPORTED: no capability evidence for {domain}"
            )
        required_modes = set(requirement.get("required_modes", []))
        supported_modes = set(capability.get("support_modes", []))
        if not required_modes or not required_modes.issubset(supported_modes):
            missing_modes = sorted(required_modes - supported_modes)
            raise CompatibilityError(
                f"SEMANTIC_ENFORCEMENT_UNSUPPORTED: {domain} missing modes {missing_modes}"
            )
        if "EVALUATE" in required_modes and not capability.get("evaluator_profile_refs"):
            raise CompatibilityError(f"EVALUATOR_EVIDENCE_MISSING: {domain}")
        if not capability.get("evidence_refs"):
            raise CompatibilityError(f"CAPABILITY_EVIDENCE_MISSING: {domain}")
        requested_families = set(
            requested_capabilities.get(domain, {}).get("feature_contract_families", [])
        )
        provided_families = set(capability.get("feature_contract_families", []))
        if not requested_families.issubset(provided_families):
            raise CompatibilityError(
                f"FEATURE_CONTRACT_UNSUPPORTED: {sorted(requested_families - provided_families)}"
            )
        selected_capabilities.append(deepcopy(capability))

    requester_policy = requester.get("adapter_policy", {})
    provider_policy = provider.get("adapter_policy", {})
    if requester_policy.get("lossless_required") is not True:
        raise CompatibilityError("Requester must require lossless constitutional adapters")
    if provider_policy.get("lossless_required") is not True:
        raise CompatibilityError("LOSSY_ADAPTER: provider does not require losslessness")
    required_prohibitions = set(requester_policy.get("prohibited_effects", []))
    provider_prohibitions = set(provider_policy.get("prohibited_effects", []))
    if not PROHIBITED_ADAPTER_EFFECTS.issubset(required_prohibitions):
        raise CompatibilityError("Requester adapter policy omits constitutional prohibitions")
    if not required_prohibitions.issubset(provider_prohibitions):
        raise CompatibilityError("LOSSY_ADAPTER: provider policy weakens prohibited effects")
    protected_paths = [f"/{domain}" for domain in CONSTITUTIONAL_DOMAINS]
    protected_paths.append("/activative_semantic_lineage/reaction_receipt_refs")
    protected_paths.append("/activative_semantic_lineage/expression_moment_refs")
    for claim in provider.get("adapter_declarations", []):
        validate_adapter_claim(claim, protected_paths)
    requester_derivative = requester.get("derivative_asset_flows")
    provider_derivative = provider.get("derivative_asset_flows")
    if not isinstance(requester_derivative, dict):
        raise CompatibilityError(
            "DERIVATIVE_LOCK_ENFORCEMENT_UNSUPPORTED: requester declaration missing"
        )
    selected_derivative = deepcopy(requester_derivative)
    if requester_derivative.get("supported") is True:
        requester_modes = set(requester_derivative.get("lock_inheritance_modes", []))
        if not REQUIRED_DERIVATIVE_LOCK_MODES.issubset(requester_modes) or not requester_derivative.get(
            "evidence_refs"
        ):
            raise CompatibilityError(
                "DERIVATIVE_LOCK_ENFORCEMENT_UNSUPPORTED: requester claims parse without enforcement"
            )
        if not isinstance(provider_derivative, dict) or provider_derivative.get("supported") is not True:
            raise CompatibilityError(
                "DERIVATIVE_LOCK_ENFORCEMENT_UNSUPPORTED: provider does not support derivative flows"
            )
        provider_modes = set(provider_derivative.get("lock_inheritance_modes", []))
        if not REQUIRED_DERIVATIVE_LOCK_MODES.issubset(provider_modes) or not provider_derivative.get(
            "evidence_refs"
        ):
            raise CompatibilityError(
                "DERIVATIVE_LOCK_ENFORCEMENT_UNSUPPORTED: provider parses without enforcing inheritance"
            )
        selected_derivative = deepcopy(provider_derivative)
    return {
        "protocol_version": common_protocols[0],
        "message_versions": negotiated_versions,
        "features": sorted(required_features),
        "semantic_capabilities": selected_capabilities,
        "behavioral_enforcement": "PASS",
        "derivative_asset_flows": selected_derivative,
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


def validate_visual_asset_demand_adapter(
    source: dict[str, Any], target: dict[str, Any]
) -> dict[str, Any]:
    """Reject adapters that parse but do not preserve governed source provenance."""

    from .contracts import validate_payload

    try:
        validate_payload("visual-asset-demand", source)
        validate_payload("visual-asset-demand", target)
    except Exception as exc:
        raise CompatibilityError("TARGET_INVALID: adapter demand is not schema-valid") from exc
    protected_values = (
        ("source_provenance", source["source_provenance"], target["source_provenance"]),
        (
            "reaction_receipt_refs",
            source["activative_semantic_lineage"].get("reaction_receipt_refs"),
            target["activative_semantic_lineage"].get("reaction_receipt_refs"),
        ),
        (
            "expression_moment_refs",
            source["activative_semantic_lineage"].get("expression_moment_refs"),
            target["activative_semantic_lineage"].get("expression_moment_refs"),
        ),
    )
    for name, source_value, target_value in protected_values:
        if source_value != target_value:
            raise CompatibilityError(f"LOSSY_ADAPTER: protected provenance changed at {name}")
    return deepcopy(target)


def validate_derivative_lock_adapter(
    source: dict[str, Any], target: dict[str, Any]
) -> dict[str, Any]:
    """Reject any adapter that alters portable derivative-lock evidence."""

    from .contracts import validate_payload
    from .derivative_locks import validate_derivative_lock_inheritance

    try:
        validate_payload("derivative-lock-inheritance", source)
        validate_payload("derivative-lock-inheritance", target)
    except Exception as exc:
        raise CompatibilityError("TARGET_INVALID: derivative lock claim is not schema-valid") from exc
    protected = (
        "authoritative_parent_ref",
        "parent_contract_version",
        "governing_authoritative_demand_ref",
        "parent_lock_evidence",
        "derivative_ref",
        "derivative_wrong_reading_locks",
        "derivation_type",
        "derivative_semantics",
        "authoritative_lock_authorization",
    )
    for name in protected:
        if source.get(name) != target.get(name):
            raise CompatibilityError(
                f"LOSSY_ADAPTER: protected derivative lock evidence changed at {name}"
            )
    if not validate_derivative_lock_inheritance(target).get("valid"):
        raise CompatibilityError(
            "PARSE_WITHOUT_ENFORCEMENT: adapted derivative lock claim is not behaviorally valid"
        )
    return deepcopy(target)


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
            "preserved_semantic_paths": [
                "/submission_validation_receipt",
                "/admission_receipt",
            ],
            "behavioral_enforcement": "PASS",
            "source_validation": "PASS",
            "target_validation": "PASS",
            "equivalence": "PASS",
            "output_ref": deepcopy(owner_evidence["output_ref"]),
            "evidence_refs": [deepcopy(owner_evidence["evidence_ref"])],
            "lossless": True,
            "migrated_at": source["migrated_at"],
        },
    }


def migrate_visual_asset_demand_v1(
    source: dict[str, Any], owner_context: dict[str, Any]
) -> dict[str, Any]:
    required_aliases = {"activative_intent", "wrongness_locks", "composition"}
    if not required_aliases.issubset(source):
        raise CompatibilityError("MIGRATION_REQUIRED: legacy demand aliases are incomplete")
    if {
        "activative_function",
        "wrong_reading_locks",
        "composition_intent",
    } & set(source):
        raise CompatibilityError("AMBIGUOUS_SOURCE: canonical and legacy fields cannot be mixed")
    if not isinstance(source.get("wrongness_locks"), list) or not source["wrongness_locks"]:
        raise CompatibilityError("TARGET_INVALID: legacy wrong-reading locks must be non-empty")
    required_context = {
        "owner_principal_type",
        "semantic_context",
        "evidence_ref",
        "output_ref",
        "migrated_at",
    }
    if set(owner_context) != required_context:
        raise CompatibilityError("MIGRATION_REQUIRED: complete owner context is mandatory")
    if owner_context["owner_principal_type"] != "CONTENT_HARNESS":
        raise CompatibilityError("AUTHORITY_DENIED: only Content Harness may supply demand meaning")
    required_semantic_context = {
        "source_provenance",
        "activative_semantic_lineage",
        "activation_contract",
        "visual_semantic_pack",
        "visual_narrative_program",
        "feature_contracts",
        "somatic_route_request",
    }
    semantic_context = owner_context["semantic_context"]
    if not isinstance(semantic_context, dict) or set(semantic_context) != required_semantic_context:
        raise CompatibilityError("MIGRATION_REQUIRED: constitution-complete owner context is mandatory")

    target = {
        key: deepcopy(value)
        for key, value in source.items()
        if key not in required_aliases
    }
    source_hash = canonical_hash(source)
    target["version"] = source["version"] + 1
    target["supersedes"] = {
        "request_id": source["request_id"],
        "version": source["version"],
        "payload_hash": source_hash,
        "canonical_ref": f"cmf-contract://demands/{source['request_id']}/{source['version']}",
    }
    target.update(deepcopy(semantic_context))
    target["activative_function"] = {
        "function": source["activative_intent"]["function"],
        "intended_viewer_effect": source["activative_intent"]["expected_effect"],
        "sequence_position": source["activative_intent"]["sequence_position"],
    }
    target["wrong_reading_locks"] = deepcopy(source["wrongness_locks"])
    target["composition_intent"] = deepcopy(source["composition"])

    from .contracts import validate_payload

    try:
        validate_payload("visual-asset-demand", target)
    except Exception as exc:
        raise CompatibilityError("TARGET_INVALID: migrated demand does not match v1.1") from exc
    for field in required_semantic_context:
        if target[field] != semantic_context[field]:
            raise CompatibilityError(f"LOSSY_MIGRATION: owner context changed at {field}")
    if target["wrong_reading_locks"] != source["wrongness_locks"]:
        raise CompatibilityError("LOSSY_MIGRATION: wrong-reading locks changed")

    target_hash = canonical_hash(target)
    path_by_domain = {
        domain: f"/{domain}" for domain in CONSTITUTIONAL_DOMAINS
    }
    path_by_domain["expression_moment_lineage"] = (
        "/activative_semantic_lineage/expression_moment_refs"
    )
    receipt = {
        "migration_id": "migration-visual-asset-demand-v1-to-v1.1",
        "source_message_type": "visual-asset-demand",
        "source_version": "1.0",
        "target_version": "1.1",
        "source_payload_hash": source_hash,
        "target_artifacts": [
            {
                "message_type": "visual-asset-demand",
                "payload_hash": target_hash,
                "canonical_ref": (
                    f"cmf-contract://demands/{target['request_id']}/{target['version']}"
                ),
            }
        ],
        "ordered_transformations": [
            "pin_owner_context",
            "apply_owner_supplied_source_kind",
            "rename_activative_intent",
            "rename_wrongness_locks",
            "rename_composition",
            "create_immutable_successor",
        ],
        "authority_effect_analysis": [
            {
                "target_path": path_by_domain[domain],
                "value_owner": "CONTENT_HARNESS",
                "effect": "PRESERVED",
            }
            for domain in sorted(CONSTITUTIONAL_DOMAINS)
        ],
        "preserved_semantic_paths": sorted(set(path_by_domain.values())),
        "behavioral_enforcement": "PASS",
        "source_validation": "PASS",
        "target_validation": "PASS",
        "equivalence": "PASS",
        "output_ref": deepcopy(owner_context["output_ref"]),
        "evidence_refs": [deepcopy(owner_context["evidence_ref"])],
        "lossless": True,
        "migrated_at": owner_context["migrated_at"],
    }
    try:
        validate_payload("contract-migration", receipt)
    except Exception as exc:
        raise CompatibilityError("TARGET_INVALID: migration receipt is invalid") from exc
    return {"target": target, "receipt": receipt}


def migrate_pre_discriminator_visual_asset_demand(
    source: dict[str, Any], owner_classification: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Create an immutable V1.1 successor without ever guessing source kind."""

    source_hash = canonical_hash(source)
    classification_required = {
        "status": "SOURCE_KIND_CLASSIFICATION_REQUIRED",
        "source_payload_hash": source_hash,
        "source_kind_path": "/source_provenance/source_kind",
        "required_authority": "CONTENT_HARNESS",
        "permitted_source_kinds": list(SOURCE_KINDS),
        "resolution": "new_authoritative_contract_or_explicit_owner_classification",
    }
    if "source_provenance" in source:
        raise CompatibilityError("AMBIGUOUS_SOURCE: source provenance already exists")
    if owner_classification is None:
        return classification_required
    required_classification = {
        "owner_principal_type",
        "source_kind",
        "evidence_ref",
        "output_ref",
        "classified_at",
    }
    if set(owner_classification) != required_classification:
        return classification_required
    if owner_classification["owner_principal_type"] != "CONTENT_HARNESS":
        raise CompatibilityError("AUTHORITY_DENIED: only Content Harness may classify source kind")
    source_kind = owner_classification["source_kind"]
    if source_kind not in SOURCE_KINDS:
        raise CompatibilityError(f"SOURCE_KIND_INVALID: {source_kind!r}")

    lineage = source.get("activative_semantic_lineage")
    if not isinstance(lineage, dict):
        raise CompatibilityError("TARGET_INVALID: activative semantic lineage is missing")
    if source_kind == "interview_expression" and (
        not lineage.get("reaction_receipt_refs")
        or not lineage.get("expression_moment_refs")
    ):
        return {
            "status": "INTERVIEW_PROVENANCE_REQUIRED",
            "source_payload_hash": source_hash,
            "required_paths": [
                "/activative_semantic_lineage/reaction_receipt_refs",
                "/activative_semantic_lineage/expression_moment_refs",
            ],
            "resolution": "new_authoritative_contract_required",
        }

    target = deepcopy(source)
    target["version"] = source["version"] + 1
    target["supersedes"] = {
        "request_id": source["request_id"],
        "version": source["version"],
        "payload_hash": source_hash,
        "canonical_ref": f"cmf-contract://demands/{source['request_id']}/{source['version']}",
    }
    target["source_provenance"] = {"source_kind": source_kind}

    from .contracts import validate_payload

    try:
        validate_payload("visual-asset-demand", target)
    except Exception as exc:
        raise CompatibilityError("TARGET_INVALID: classified demand does not match v1.1") from exc
    for field, value in source.items():
        if field not in {"version", "supersedes"} and target[field] != value:
            raise CompatibilityError(f"LOSSY_MIGRATION: source value changed at {field}")

    receipt = {
        "migration_id": "migration-visual-asset-demand-v1.1-source-kind-classification",
        "source_message_type": "visual-asset-demand",
        "source_version": "1.1",
        "target_version": "1.1",
        "source_payload_hash": source_hash,
        "target_artifacts": [
            {
                "message_type": "visual-asset-demand",
                "payload_hash": canonical_hash(target),
                "canonical_ref": f"cmf-contract://demands/{target['request_id']}/{target['version']}",
            }
        ],
        "ordered_transformations": [
            "verify_content_harness_classification",
            "add_source_provenance_source_kind",
            "create_immutable_successor",
        ],
        "authority_effect_analysis": [
            {
                "target_path": "/source_provenance/source_kind",
                "value_owner": "CONTENT_HARNESS",
                "effect": "OWNER_CLASSIFIED",
            },
            {
                "target_path": "/activative_semantic_lineage/reaction_receipt_refs",
                "value_owner": "CONTENT_HARNESS",
                "effect": "PRESERVED",
            },
            {
                "target_path": "/activative_semantic_lineage/expression_moment_refs",
                "value_owner": "CONTENT_HARNESS",
                "effect": "PRESERVED",
            },
        ],
        "preserved_semantic_paths": [
            "/activative_semantic_lineage/reaction_receipt_refs",
            "/activative_semantic_lineage/expression_moment_refs",
            "/source_provenance/source_kind",
        ],
        "behavioral_enforcement": "PASS",
        "source_validation": "PASS",
        "target_validation": "PASS",
        "equivalence": "PASS",
        "output_ref": deepcopy(owner_classification["output_ref"]),
        "evidence_refs": [deepcopy(owner_classification["evidence_ref"])],
        "lossless": True,
        "migrated_at": owner_classification["classified_at"],
    }
    try:
        validate_payload("contract-migration", receipt)
    except Exception as exc:
        raise CompatibilityError("TARGET_INVALID: source-kind migration receipt is invalid") from exc
    return {"status": "MIGRATED", "target": target, "receipt": receipt}
