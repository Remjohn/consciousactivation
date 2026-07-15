"""Generate the checked-in Stage 3 contract baseline from the canonical catalog."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "packages" / "contracts" / "src"
sys.path.insert(0, str(SRC.parent))

from src.catalog import CATALOG, CONSTITUTIONAL_DOMAINS, semantic_capability  # noqa: E402
from src.common import PACKAGE_VERSION, PRINCIPAL_TYPES, PROTOCOL_VERSION  # noqa: E402


TRANSITIONS = [
    ("DRAFT", "submission_validation_accepted", "SUBMITTED", "DELEGATION_PROTOCOL"),
    ("DRAFT", "submission_validation_rejected", "REJECTED", "DELEGATION_PROTOCOL"),
    ("SUBMITTED", "admission_accepted", "ACCEPTED", "VISUAL_ASSET_EDITOR"),
    ("SUBMITTED", "admission_rejected", "REJECTED", "VISUAL_ASSET_EDITOR"),
    ("SUBMITTED", "contract_rejected", "REJECTED", "DELEGATION_PROTOCOL"),
    ("ACCEPTED", "execution_started", "IN_PROGRESS", "VISUAL_ASSET_EDITOR"),
    ("ACCEPTED", "amendment_proposed", "AMENDMENT_REQUIRED", "VISUAL_ASSET_EDITOR"),
    ("IN_PROGRESS", "amendment_proposed", "AMENDMENT_REQUIRED", "VISUAL_ASSET_EDITOR"),
    ("ACCEPTED", "budget_escalation_requested", "COST_APPROVAL_REQUIRED", "VISUAL_ASSET_EDITOR"),
    ("IN_PROGRESS", "budget_escalation_requested", "COST_APPROVAL_REQUIRED", "VISUAL_ASSET_EDITOR"),
    ("COST_APPROVAL_REQUIRED", "budget_escalation_approved", "IN_PROGRESS", "CONTENT_HARNESS"),
    ("COST_APPROVAL_REQUIRED", "budget_escalation_denied", "CAPABILITY_GAP", "CONTENT_HARNESS"),
    ("ACCEPTED", "capability_gap_reported", "CAPABILITY_GAP", "VISUAL_ASSET_EDITOR"),
    ("IN_PROGRESS", "capability_gap_reported", "CAPABILITY_GAP", "VISUAL_ASSET_EDITOR"),
    ("ACCEPTED", "human_review_requested", "HUMAN_REVIEW_REQUIRED", "VISUAL_ASSET_EDITOR"),
    ("IN_PROGRESS", "human_review_requested", "HUMAN_REVIEW_REQUIRED", "VISUAL_ASSET_EDITOR"),
    ("IN_PROGRESS", "result_declared", "RESULT_READY", "VISUAL_ASSET_EDITOR"),
    ("IN_PROGRESS", "partial_result_declared", "PARTIAL_RESULT_READY", "VISUAL_ASSET_EDITOR"),
    ("RESULT_READY", "result_accepted", "COMPLETED", "CONTENT_HARNESS"),
    ("RESULT_READY", "result_accepted_with_concerns", "COMPLETED", "CONTENT_HARNESS"),
    ("RESULT_READY", "result_rejected", "RESULT_REJECTED", "CONTENT_HARNESS"),
    ("RESULT_REJECTED", "revalidation_started", "IN_PROGRESS", "VISUAL_ASSET_EDITOR"),
    ("PARTIAL_RESULT_READY", "partial_result_accepted", "COMPLETED", "CONTENT_HARNESS"),
    ("PARTIAL_RESULT_READY", "partial_result_rejected", "RESULT_REJECTED", "CONTENT_HARNESS"),
    ("PARTIAL_RESULT_READY", "partial_continuation_authorized", "IN_PROGRESS", "CONTENT_HARNESS"),
    ("SUBMITTED", "cancellation_requested", "CANCELLATION_REQUESTED", "CONTENT_HARNESS"),
    ("ACCEPTED", "cancellation_requested", "CANCELLATION_REQUESTED", "CONTENT_HARNESS"),
    ("IN_PROGRESS", "cancellation_requested", "CANCELLATION_REQUESTED", "CONTENT_HARNESS"),
    ("CANCELLATION_REQUESTED", "cancellation_receipted", "CANCELLED", "VISUAL_ASSET_EDITOR"),
    ("AMENDMENT_REQUIRED", "amendment_rejected_capability_gap", "CAPABILITY_GAP", "CONTENT_HARNESS"),
    ("AMENDMENT_REQUIRED", "amendment_rejected_cancelled", "CANCELLED", "CONTENT_HARNESS"),
    ("COMPLETED", "result_invalidated", "INVALIDATED", "CONTENT_HARNESS"),
    ("COMPLETED", "result_revoked", "REVOKED", "VISUAL_ASSET_EDITOR"),
    ("COMPLETED", "replacement_acknowledged", "REPLACED", "CONTENT_HARNESS"),
    ("INVALIDATED", "replacement_acknowledged", "REPLACED", "CONTENT_HARNESS"),
    ("REVOKED", "replacement_acknowledged", "REPLACED", "CONTENT_HARNESS"),
    ("SUBMITTED", "demand_superseded", "SUPERSEDED", "CONTENT_HARNESS"),
    ("ACCEPTED", "demand_superseded", "SUPERSEDED", "CONTENT_HARNESS"),
    ("IN_PROGRESS", "demand_superseded", "SUPERSEDED", "CONTENT_HARNESS"),
    ("AMENDMENT_REQUIRED", "demand_superseded", "SUPERSEDED", "CONTENT_HARNESS"),
    ("COST_APPROVAL_REQUIRED", "demand_superseded", "SUPERSEDED", "CONTENT_HARNESS"),
    ("RESULT_READY", "demand_superseded", "SUPERSEDED", "CONTENT_HARNESS"),
    ("RESULT_REJECTED", "demand_superseded", "SUPERSEDED", "CONTENT_HARNESS"),
    ("PARTIAL_RESULT_READY", "demand_superseded", "SUPERSEDED", "CONTENT_HARNESS"),
]


SCENARIOS = [
    {
        "scenario_id": "SCN-01",
        "title": "Successful single character asset",
        "messages": [
            ("visual-asset-demand", "CONTENT_HARNESS", "ACCEPTED"),
            ("visual-asset-submission", "CONTENT_HARNESS", "ACCEPTED"),
            ("submission-validation-receipt", "DELEGATION_PROTOCOL", "ACCEPTED"),
            ("admission-receipt", "VISUAL_ASSET_EDITOR", "ACCEPTED"),
            ("visual-asset-event", "VISUAL_ASSET_EDITOR", "ACCEPTED"),
            ("asset-result-contract", "VISUAL_ASSET_EDITOR", "ACCEPTED"),
            ("result-acknowledgement", "CONTENT_HARNESS", "ACCEPTED"),
        ],
        "transitions": [
            ("DRAFT", "submission_validation_accepted", "SUBMITTED", "DELEGATION_PROTOCOL"),
            ("SUBMITTED", "admission_accepted", "ACCEPTED", "VISUAL_ASSET_EDITOR"),
            ("ACCEPTED", "execution_started", "IN_PROGRESS", "VISUAL_ASSET_EDITOR"),
            ("IN_PROGRESS", "result_declared", "RESULT_READY", "VISUAL_ASSET_EDITOR"),
            ("RESULT_READY", "result_accepted", "COMPLETED", "CONTENT_HARNESS"),
        ],
        "initial_state": "DRAFT",
        "terminal_state": "COMPLETED",
        "effect_counts": {"vae_executions": 1, "accepted_results": 1, "acknowledgements": 1},
        "prohibited_effects": ["duplicate_execution", "unacknowledged_consumption", "owner_field_mutation"],
        "negative_variants": ["tampered_demand_hash", "missing_production_receipt", "stale_dependency_snapshot"],
        "race_variants": ["result_before_acknowledgement", "duplicate_submission_delivery"],
    },
    {
        "scenario_id": "SCN-02",
        "title": "Atomic multi-asset Delegation Set",
        "messages": [
            ("delegation-set", "CONTENT_HARNESS", "ACCEPTED"),
            ("visual-asset-demand", "CONTENT_HARNESS", "ACCEPTED"),
            ("visual-asset-submission", "CONTENT_HARNESS", "ACCEPTED"),
            ("submission-validation-receipt", "DELEGATION_PROTOCOL", "ACCEPTED"),
            ("admission-receipt", "VISUAL_ASSET_EDITOR", "ACCEPTED"),
            ("asset-result-contract", "VISUAL_ASSET_EDITOR", "ACCEPTED"),
            ("result-acknowledgement", "CONTENT_HARNESS", "ACCEPTED"),
        ],
        "transitions": [
            ("DRAFT", "submission_validation_accepted", "SUBMITTED", "DELEGATION_PROTOCOL"),
            ("SUBMITTED", "admission_accepted", "ACCEPTED", "VISUAL_ASSET_EDITOR"),
            ("ACCEPTED", "execution_started", "IN_PROGRESS", "VISUAL_ASSET_EDITOR"),
            ("IN_PROGRESS", "result_declared", "RESULT_READY", "VISUAL_ASSET_EDITOR"),
            ("RESULT_READY", "result_accepted", "COMPLETED", "CONTENT_HARNESS"),
        ],
        "initial_state": "DRAFT",
        "terminal_state": "COMPLETED",
        "effect_counts": {"member_correlations": 3, "vae_executions": 3, "set_releases": 1},
        "prohibited_effects": ["partial_atomic_release", "merged_member_lineage", "cross_member_acknowledgement"],
        "negative_variants": ["missing_required_member", "dependency_cycle", "member_hash_mismatch"],
        "race_variants": ["member_cancellation_during_completion", "member_supersession_before_set_release"],
    },
    {
        "scenario_id": "SCN-03",
        "title": "In-flight demand supersession",
        "messages": [
            ("demand-supersession", "CONTENT_HARNESS", "ACCEPTED"),
            ("selective-invalidation-receipt", "VISUAL_ASSET_EDITOR", "ACCEPTED"),
        ],
        "transitions": [
            ("IN_PROGRESS", "demand_superseded", "SUPERSEDED", "CONTENT_HARNESS"),
        ],
        "initial_state": "IN_PROGRESS",
        "terminal_state": "SUPERSEDED",
        "effect_counts": {"old_branch_terminations": 1, "new_successor_branches": 1, "stale_promotions": 0},
        "prohibited_effects": ["old_result_satisfies_new_demand", "history_deletion", "speculative_reuse"],
        "negative_variants": ["changed_path_diff_mismatch", "late_old_result", "reuse_without_evidence"],
        "race_variants": ["supersession_before_result_commit", "result_before_supersession_commit"],
    },
    {
        "scenario_id": "SCN-04",
        "title": "Budget escalation and approval",
        "messages": [
            ("budget-escalation-request", "VISUAL_ASSET_EDITOR", "ACCEPTED"),
            ("budget-escalation-response", "CONTENT_HARNESS", "ACCEPTED"),
        ],
        "transitions": [
            ("IN_PROGRESS", "budget_escalation_requested", "COST_APPROVAL_REQUIRED", "VISUAL_ASSET_EDITOR"),
            ("COST_APPROVAL_REQUIRED", "budget_escalation_approved", "IN_PROGRESS", "CONTENT_HARNESS"),
        ],
        "initial_state": "IN_PROGRESS",
        "terminal_state": "IN_PROGRESS",
        "effect_counts": {"budget_escalations": 1, "replacement_authorizations": 1, "hard_ceiling_breaches": 0},
        "prohibited_effects": ["work_beyond_hard_ceiling", "in_place_budget_patch", "vae_budget_approval"],
        "negative_variants": ["approval_without_new_authorization", "expired_budget", "denial_to_capability_gap"],
        "race_variants": ["budget_approval_before_cancellation", "cancellation_before_budget_approval"],
    },
    {
        "scenario_id": "SCN-05",
        "title": "Constraint conflict and amendment",
        "messages": [
            ("constraint-conflict", "VISUAL_ASSET_EDITOR", "ACCEPTED"),
            ("amendment-proposal", "VISUAL_ASSET_EDITOR", "ACCEPTED"),
            ("amendment-response", "CONTENT_HARNESS", "ACCEPTED"),
            ("visual-asset-demand", "CONTENT_HARNESS", "ACCEPTED"),
            ("demand-supersession", "CONTENT_HARNESS", "ACCEPTED"),
        ],
        "transitions": [
            ("IN_PROGRESS", "amendment_proposed", "AMENDMENT_REQUIRED", "VISUAL_ASSET_EDITOR"),
            ("AMENDMENT_REQUIRED", "demand_superseded", "SUPERSEDED", "CONTENT_HARNESS"),
        ],
        "initial_state": "IN_PROGRESS",
        "terminal_state": "SUPERSEDED",
        "effect_counts": {"non_binding_proposals": 1, "owner_decisions": 1, "successor_demands": 1},
        "prohibited_effects": ["vae_mutates_demand", "semantic_auto_approval", "old_demand_resume_after_acceptance"],
        "negative_variants": ["constitutional_auto_amendment", "expired_proposal", "option_without_evidence"],
        "race_variants": ["amendment_acceptance_before_supersession", "duplicate_supersession"],
    },
    {
        "scenario_id": "SCN-06",
        "title": "Safe cancellation",
        "messages": [
            ("cancellation-request", "CONTENT_HARNESS", "ACCEPTED"),
            ("cancellation-receipt", "VISUAL_ASSET_EDITOR", "ACCEPTED"),
        ],
        "transitions": [
            ("IN_PROGRESS", "cancellation_requested", "CANCELLATION_REQUESTED", "CONTENT_HARNESS"),
            ("CANCELLATION_REQUESTED", "cancellation_receipted", "CANCELLED", "VISUAL_ASSET_EDITOR"),
        ],
        "initial_state": "IN_PROGRESS",
        "terminal_state": "CANCELLED",
        "effect_counts": {"cancellation_requests": 1, "safe_checkpoint_receipts": 1, "late_promotions": 0},
        "prohibited_effects": ["new_work_after_cancellation", "late_output_consumption", "evidence_deletion"],
        "negative_variants": ["wrong_owner_cancellation", "missing_checkpoint", "consumption_authorized_receipt"],
        "race_variants": ["cancellation_before_result", "result_before_cancellation"],
    },
    {
        "scenario_id": "SCN-07",
        "title": "Result invalidation and replacement",
        "messages": [
            ("invalidation-notice", "CONTENT_HARNESS", "ACCEPTED"),
            ("replacement-notice", "VISUAL_ASSET_EDITOR", "ACCEPTED"),
            ("result-acknowledgement", "CONTENT_HARNESS", "ACCEPTED"),
        ],
        "transitions": [
            ("COMPLETED", "result_invalidated", "INVALIDATED", "CONTENT_HARNESS"),
            ("INVALIDATED", "replacement_acknowledged", "REPLACED", "CONTENT_HARNESS"),
        ],
        "initial_state": "COMPLETED",
        "terminal_state": "REPLACED",
        "effect_counts": {"invalidations": 1, "replacement_candidates": 1, "replacement_acknowledgements": 1},
        "prohibited_effects": ["history_overwrite", "unacknowledged_replacement_use", "silent_geometry_change"],
        "negative_variants": ["replacement_geometry_mismatch", "stale_acknowledgement", "missing_impact_evidence"],
        "race_variants": ["acknowledgement_before_revocation", "revocation_before_acknowledgement"],
    },
    {
        "scenario_id": "SCN-08",
        "title": "Authority violation rejection",
        "messages": [
            ("visual-asset-demand", "VISUAL_ASSET_EDITOR", "REJECTED"),
            ("delegation-audit-receipt", "DELEGATION_PROTOCOL", "ACCEPTED"),
        ],
        "transitions": [],
        "initial_state": "DRAFT",
        "terminal_state": "DRAFT",
        "effect_counts": {"authority_denials": 1, "vae_executions": 0, "state_changes": 0},
        "prohibited_effects": ["production_start", "demand_mutation", "denial_without_audit"],
        "negative_variants": ["vae_composition_mutation", "hidden_extension_authority", "forged_owner_principal"],
        "race_variants": ["denied_mutation_before_valid_submission", "valid_submission_before_denied_mutation"],
    },
    {
        "scenario_id": "SCN-09",
        "title": "Compatibility migration",
        "messages": [
            ("compatibility-manifest", "CONTENT_HARNESS", "ACCEPTED"),
            ("compatibility-manifest", "VISUAL_ASSET_EDITOR", "ACCEPTED"),
            ("contract-migration", "DELEGATION_PROTOCOL", "ACCEPTED"),
            ("visual-asset-submission", "CONTENT_HARNESS", "ACCEPTED"),
            ("submission-validation-receipt", "DELEGATION_PROTOCOL", "ACCEPTED"),
        ],
        "transitions": [
            ("DRAFT", "submission_validation_accepted", "SUBMITTED", "DELEGATION_PROTOCOL"),
        ],
        "initial_state": "DRAFT",
        "terminal_state": "SUBMITTED",
        "effect_counts": {"negotiated_profiles": 1, "migration_outputs": 2, "admissions_before_pin": 0},
        "prohibited_effects": ["silent_upgrade", "dropped_wrongness_lock", "migration_authority_transfer"],
        "negative_variants": ["lossy_wrongness_lock", "forged_manifest", "ambiguous_adapter_path"],
        "race_variants": ["new_release_during_pinned_correlation", "repeated_identical_migration"],
    },
    {
        "scenario_id": "SCN-10",
        "title": "Replay and out-of-order resilience",
        "messages": [
            ("visual-asset-submission", "CONTENT_HARNESS", "ACCEPTED"),
            ("visual-asset-submission", "CONTENT_HARNESS", "IDEMPOTENT_REPLAY"),
            ("visual-asset-event", "VISUAL_ASSET_EDITOR", "REJECTED_OUT_OF_ORDER"),
            ("delegation-audit-receipt", "DELEGATION_PROTOCOL", "ACCEPTED"),
        ],
        "transitions": [
            ("DRAFT", "submission_validation_accepted", "SUBMITTED", "DELEGATION_PROTOCOL"),
        ],
        "initial_state": "DRAFT",
        "terminal_state": "SUBMITTED",
        "effect_counts": {"submission_effects": 1, "duplicate_receipts_reused": 1, "hostile_replay_effects": 0},
        "prohibited_effects": ["duplicate_execution", "replay_acceptance", "progress_before_admission"],
        "negative_variants": ["nonce_reuse_changed_bytes", "message_id_collision", "expired_signature"],
        "race_variants": ["duplicate_concurrent_submission", "progress_before_admission"],
    },
]


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_json(path: Path, value: Any) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def file_hash(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_value_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def class_name(message_type: str) -> str:
    return "".join(part.capitalize() for part in re.split(r"[-_]", message_type))


def python_type(schema: dict[str, Any]) -> str:
    if "$ref" in schema:
        return "dict[str, Any]"
    if "anyOf" in schema:
        non_null = [item for item in schema["anyOf"] if item.get("type") != "null"]
        return f"{python_type(non_null[0])} | None"
    schema_type = schema.get("type")
    if schema_type == "string":
        return "str"
    if schema_type == "integer":
        return "int"
    if schema_type == "boolean":
        return "bool"
    if schema_type == "array":
        return f"list[{python_type(schema['items'])}]"
    if schema_type == "object":
        return "dict[str, Any]"
    return "Any"


def typescript_type(schema: dict[str, Any]) -> str:
    if "$ref" in schema:
        return "Record<string, unknown>"
    if "anyOf" in schema:
        non_null = [item for item in schema["anyOf"] if item.get("type") != "null"]
        return f"{typescript_type(non_null[0])} | null"
    schema_type = schema.get("type")
    if schema_type == "string":
        if "enum" in schema:
            return " | ".join(json.dumps(item) for item in schema["enum"])
        return "string"
    if schema_type == "integer":
        return "number"
    if schema_type == "boolean":
        return "boolean"
    if schema_type == "array":
        return f"Array<{typescript_type(schema['items'])}>"
    if schema_type == "object":
        return "Record<string, unknown>"
    return "unknown"


def _pointer_token(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _referenced_schema(node: dict[str, Any], root_schema: dict[str, Any]) -> dict[str, Any] | None:
    reference = node.get("$ref")
    if not reference or not reference.startswith("#/$defs/"):
        return None
    return root_schema["$defs"][reference.removeprefix("#/$defs/")]


def exact_owner_paths(schema: dict[str, Any], owner: str) -> dict[str, str]:
    paths: dict[str, str] = {}

    def walk(node: dict[str, Any], path: str, reference_stack: tuple[str, ...] = ()) -> None:
        node["x-cmf-value-owner"] = owner
        referenced = _referenced_schema(node, schema)
        if referenced is not None:
            reference = node["$ref"]
            if reference not in reference_stack:
                walk(referenced, path, (*reference_stack, reference))
            return
        for variant in node.get("anyOf", []):
            if variant.get("type") != "null":
                walk(variant, path, reference_stack)
        if node.get("type") == "object":
            for property_name, property_schema in node.get("properties", {}).items():
                property_path = f"{path}/{_pointer_token(property_name)}"
                paths[property_path] = owner
                walk(property_schema, property_path, reference_stack)
        if node.get("type") == "array":
            item_path = path + "/{index}"
            paths[item_path] = owner
            walk(node["items"], item_path, reference_stack)

    for property_name, property_schema in schema["properties"].items():
        property_path = f"/{_pointer_token(property_name)}"
        paths[property_path] = owner
        walk(property_schema, property_path)
    return dict(sorted(paths.items()))


def generate_types() -> None:
    py_lines = [
        '"""Generated top-level TypedDict bindings. Do not edit manually."""',
        "",
        "from typing import Any, TypedDict",
        "",
    ]
    ts_lines = ["// Generated top-level bindings. Do not edit manually.", ""]
    exports: list[str] = []
    for item in CATALOG:
        name = class_name(item.message_type)
        exports.append(name)
        py_lines.append(f"class {name}(TypedDict):")
        for prop, prop_schema in item.schema["properties"].items():
            py_lines.append(f"    {prop}: {python_type(prop_schema)}")
        py_lines.append("")
        ts_lines.append(f"export interface {name} " + "{")
        for prop, prop_schema in item.schema["properties"].items():
            ts_lines.append(f"  {prop}: {typescript_type(prop_schema)};")
        ts_lines.extend(["}", ""])
    py_lines.extend([f"__all__ = {exports!r}", ""])
    py_root = ROOT / "packages" / "contracts" / "generated" / "python" / "cmf_delegation_contracts"
    write_text(py_root / "types.py", "\n".join(py_lines))
    write_text(py_root / "__init__.py", "from .types import *  # noqa: F401,F403\n")
    write_text(ROOT / "packages" / "contracts" / "generated" / "typescript" / "index.ts", "\n".join(ts_lines))


def generate_contracts() -> None:
    contracts_root = ROOT / "packages" / "contracts"
    registry_items: list[dict[str, Any]] = []
    authority_items: list[dict[str, Any]] = []
    for item in CATALOG:
        allowed = PRINCIPAL_TYPES if item.producer == "ANY_PRINCIPAL" else [item.producer]
        schema = deepcopy(item.schema)
        value_owner = "SIGNING_PRINCIPAL" if item.producer == "ANY_PRINCIPAL" else item.producer
        value_owner_by_path = exact_owner_paths(schema, value_owner)
        schema["x-cmf-authority"] = {
            "allowed_producers": allowed,
            "path_kind": "JSON_POINTER_TEMPLATE",
            "value_owner_by_path": value_owner_by_path,
        }
        schema["x-cmf-consumers"] = list(item.consumers)
        schema["x-cmf-idempotency"] = item.idempotency
        schema["x-cmf-lifecycle-effects"] = list(item.lifecycle_effects)
        schema_path = contracts_root / "schemas" / f"{item.message_type}.schema.json"
        example_path = contracts_root / "examples" / f"{item.message_type}.example.json"
        write_json(schema_path, schema)
        write_json(example_path, item.example)
        if item.message_type in {
            "visual-asset-demand",
            "compatibility-manifest",
            "contract-migration",
        }:
            write_text(
                ROOT / "contracts" / "schemas" / f"{item.message_type}.schema.yaml",
                yaml.safe_dump(schema, sort_keys=False, allow_unicode=True),
            )
            write_text(
                ROOT / "contracts" / "examples" / f"{item.message_type}.example.yaml",
                yaml.safe_dump(item.example, sort_keys=False, allow_unicode=True),
            )
        registry_items.append(
            {
                "message_type": item.message_type,
                "message_version": schema["x-cmf-message-version"],
                "schema_id": schema["$id"],
                "schema_path": schema_path.relative_to(ROOT).as_posix(),
                "schema_hash": file_hash(schema_path),
                "example_path": example_path.relative_to(ROOT).as_posix(),
                "example_hash": file_hash(example_path),
                "allowed_producers": allowed,
                "consumers": list(item.consumers),
                "idempotency": item.idempotency,
                "lifecycle_effects": list(item.lifecycle_effects),
            }
        )
        authority_items.append(
            {
                "message_type": item.message_type,
                "allowed_producers": allowed,
                "path_kind": "JSON_POINTER_TEMPLATE",
                "value_owner_by_path": value_owner_by_path,
                "forbidden_paths": (
                    ["/authorization/downstream_consumption_authorized"]
                    if item.message_type == "asset-result-contract"
                    else []
                ),
            }
        )
    write_json(
        contracts_root / "registry.json",
        {
            "package": "cmf-delegation-contracts",
            "package_version": PACKAGE_VERSION,
            "protocol_version": PROTOCOL_VERSION,
            "status": "RELEASE_CANDIDATE",
            "messages": registry_items,
        },
    )
    write_json(
        contracts_root / "authority-registry.json",
        {
            "package_version": PACKAGE_VERSION,
            "policy": "A signing principal may set values only in messages it is allowed to produce.",
            "messages": authority_items,
        },
    )
    write_json(
        contracts_root / "lifecycle.json",
        {
            "package_version": PACKAGE_VERSION,
            "serialization_scope": "correlation_id",
            "terminal_states": [
                "REJECTED",
                "SUPERSEDED",
                "CANCELLED",
                "COMPLETED",
                "INVALIDATED",
                "REVOKED",
                "REPLACED",
            ],
            "transitions": [
                {
                    "from_state": source,
                    "trigger": trigger,
                    "to_state": target,
                    "principal_type": principal_type,
                }
                for source, trigger, target, principal_type in TRANSITIONS
            ],
        },
    )
    generate_types()


def generate_fixtures() -> None:
    fixtures_root = ROOT / "packages" / "fixtures"
    registry = json.loads(
        (ROOT / "packages" / "contracts" / "registry.json").read_text(encoding="utf-8")
    )
    registry_by_type = {item["message_type"]: item for item in registry["messages"]}
    constitutional_assertions_by_scenario = {
        "SCN-01": [
            "semantic_lineage_survives_happy_path",
            "reaction_and_expression_lineage_survive",
            "wrong_reading_locks_remain_non_empty",
        ],
        "SCN-02": [
            "member_demand_lineage_remains_independent",
            "set_coordination_does_not_flatten_semantics",
        ],
        "SCN-05": [
            "vae_proposal_cannot_mutate_protected_meaning",
            "successor_requires_content_harness_authority",
        ],
        "SCN-08": [
            "vae_semantic_mutation_is_authority_denied",
            "authority_denial_has_no_state_or_production_effect",
        ],
        "SCN-09": [
            "v1_to_v1_1_migration_is_lossless_and_traceable",
            "parse_only_or_missing_evaluator_support_is_incompatible",
        ],
        "SCN-10": [
            "aip_version_and_hash_survive_retry_and_replay",
            "reaction_and_expression_lineage_survive_retry_and_replay",
        ],
    }
    scenario_entries = []
    for scenario in SCENARIOS:
        scenario_slug = scenario["scenario_id"].lower()
        member_correlation_count = 3 if scenario["scenario_id"] == "SCN-02" else 1
        member_correlations = [
            f"{scenario_slug}-member-corr-{index:03d}"
            for index in range(1, member_correlation_count + 1)
        ]
        message_sequence = []
        audit_sequence = []
        outbox_deliveries = []
        previous_message_id = None
        committed_audit_sequence = 0
        for index, (message_type, principal_type, disposition) in enumerate(
            scenario["messages"], start=1
        ):
            is_idempotent_replay = disposition == "IDEMPOTENT_REPLAY"
            message_id = (
                message_sequence[-1]["message_id"]
                if is_idempotent_replay and message_sequence
                else f"{scenario_slug}-msg-{index:03d}"
            )
            causation_id = (
                message_sequence[-1]["causation_id"]
                if is_idempotent_replay and message_sequence
                else previous_message_id
            )
            if disposition != "IDEMPOTENT_REPLAY":
                committed_audit_sequence += 1
            effective_audit_sequence = committed_audit_sequence
            message_sequence.append(
                {
                    "sequence": index,
                    "message_id": message_id,
                    "correlation_id": member_correlations[0],
                    "causation_id": causation_id,
                    "message_type": message_type,
                    "principal_type": principal_type,
                    "expected_disposition": disposition,
                    "fixture_ref": f"packages/contracts/examples/{message_type}.example.json",
                    "fixture_hash": registry_by_type[message_type]["example_hash"],
                }
            )
            audit_sequence.append(
                {
                    "audit_sequence": effective_audit_sequence,
                    "message_id": message_id,
                    "message_type": message_type,
                    "disposition": disposition,
                    "receipt_mode": (
                        "REUSED"
                        if disposition == "IDEMPOTENT_REPLAY"
                        else "REJECTION"
                        if disposition.startswith("REJECTED")
                        else "ORIGINAL"
                    ),
                    "state_change_expected": bool(
                        registry_by_type[message_type]["lifecycle_effects"]
                        and disposition == "ACCEPTED"
                    ),
                }
            )
            if disposition != "IDEMPOTENT_REPLAY":
                outbox_deliveries.append(
                    {
                        "audit_sequence": effective_audit_sequence,
                        "message_id": message_id,
                        "delivery_kind": (
                            "REJECTION_RECEIPT"
                            if disposition.startswith("REJECTED")
                            else "ACCEPTED_FACT"
                        ),
                        "duplicate_domain_effect_allowed": False,
                    }
                )
            previous_message_id = message_id
        value = {
            "scenario_id": scenario["scenario_id"],
            "title": scenario["title"],
            "fixture_profile": "FORMAT02_REFERENCE",
            "member_correlations": member_correlations,
            "message_sequence": message_sequence,
            "lifecycle_sequence": [
                {
                    "sequence": index,
                    "from_state": transition[0],
                    "trigger": transition[1],
                    "to_state": transition[2],
                    "principal_type": transition[3],
                }
                for index, transition in enumerate(scenario["transitions"], start=1)
            ],
            "expected_initial_state": scenario["initial_state"],
            "expected_terminal_state": scenario["terminal_state"],
            "assertions": {
                "authority": [
                    {
                        "message_type": message_type,
                        "principal_type": principal_type,
                        "expected_disposition": disposition,
                    }
                    for message_type, principal_type, disposition in scenario["messages"]
                ],
                "identity": [
                    "exact_demand_identity_is_preserved",
                    "correlation_and_causation_are_deterministic",
                    "pinned_profile_does_not_silently_upgrade",
                ],
                "audit": {
                    "accepted_and_rejected_actions_receipted": True,
                    "receipt_chain_required": True,
                    "committed_sequence_is_ordering_authority": True,
                    "expected_sequence": audit_sequence,
                },
                "outbox": {
                    "accepted_effects_publish_after_atomic_commit": True,
                    "delivery_redrive_must_not_duplicate_domain_effect": True,
                    "expected_deliveries": outbox_deliveries,
                },
                "effect_counts": scenario["effect_counts"],
                "projection": [
                    {
                        "correlation_id": member_correlations[0],
                        "expected_state": scenario["terminal_state"],
                        "protocol_version": PROTOCOL_VERSION,
                        "source_audit_sequence": committed_audit_sequence,
                    },
                    {
                        "assertion": "denied_or_stale_effects_are_visible_without_becoming_authority"
                    },
                ],
                "prohibited_effects": scenario["prohibited_effects"],
                "negative_variants": scenario["negative_variants"],
                "race_variants": scenario["race_variants"],
            },
        }
        if scenario["scenario_id"] in constitutional_assertions_by_scenario:
            value["assertions"]["constitutional"] = (
                constitutional_assertions_by_scenario[scenario["scenario_id"]]
            )
        path = fixtures_root / "format02" / "scenarios" / f"{scenario['scenario_id']}.json"
        write_json(path, value)
        scenario_entries.append(
            {
                "scenario_id": scenario["scenario_id"],
                "path": path.relative_to(ROOT).as_posix(),
                "hash": file_hash(path),
            }
        )
    write_json(
        fixtures_root / "format02" / "manifest.json",
        {
            "profile": "FORMAT02_REFERENCE",
            "package_version": PACKAGE_VERSION,
            "scenario_count": len(scenario_entries),
            "scenarios": scenario_entries,
        },
    )
    write_json(
        fixtures_root / "conformance" / "legacy-demand-ref.input.json",
        {"demand_ref": "req-format02-001"},
    )
    write_json(
        fixtures_root / "conformance" / "legacy-demand-ref.context.json",
        {
            "request_id": "req-format02-001",
            "version": 1,
            "payload_hash": "sha256:" + "a" * 64,
            "canonical_ref": "cmf-contract://demands/req-format02-001/1",
        },
    )
    write_json(
        fixtures_root / "conformance" / "unknown-field.invalid.json",
        {"message_type": "visual-asset-submission", "additional_property": True},
    )


def generate_compatibility() -> None:
    compatibility_root = ROOT / "packages" / "compatibility"
    fixture_root = ROOT / "packages" / "fixtures" / "compatibility"
    examples = {item.message_type: deepcopy(item.example) for item in CATALOG}
    required_modes = {
        domain: (
            ["PRESERVE", "ENFORCE", "EVALUATE"]
            if domain
            in {
                "activation_contract",
                "visual_semantic_pack",
                "visual_narrative_program",
                "feature_contracts",
                "somatic_route_request",
                "expression_moment_lineage",
                "wrong_reading_locks",
            }
            else ["PRESERVE", "ENFORCE"]
        )
        for domain in CONSTITUTIONAL_DOMAINS
    }
    semantic_capabilities = [
        semantic_capability(domain) for domain in CONSTITUTIONAL_DOMAINS
    ]
    compatibility_manifest = {
        "package": "cmf-delegation-compatibility",
        "package_version": PACKAGE_VERSION,
        "status": "RELEASE_CANDIDATE",
        "protocol_versions": [PROTOCOL_VERSION],
        "message_versions": [
            {
                "message_type": "visual-asset-demand",
                "accepted_versions": ["1.1"],
                "emitted_versions": ["1.1"],
            }
        ],
        "required_features": [
            "authority.registry",
            "behavioral.semantic-enforcement",
            "closed.schemas",
            "format02.fixtures",
            "lifecycle.transitions",
            "rfc8785.safe-integer-profile",
        ],
        "required_semantic_domains": [
            {"domain": domain, "required_modes": required_modes[domain]}
            for domain in CONSTITUTIONAL_DOMAINS
        ],
        "semantic_capabilities": semantic_capabilities,
        "adapter_policy": {
            "lossless_required": True,
            "prohibited_effects": [
                "DROP",
                "WEAKEN",
                "SYNTHESIZE",
                "FLATTEN",
                "REINTERPRET",
            ],
        },
        "signature_algorithms": ["Ed25519"],
        "legacy_inputs": [
            "submission-receipt@0.1",
            "demand_ref:string@0.1",
            "visual-asset-demand@1.0",
        ],
    }
    write_json(
        compatibility_root / "manifest.json",
        compatibility_manifest,
    )
    write_json(
        compatibility_root / "adapters" / "legacy-demand-ref-to-demand-identity.json",
        {
            "adapter_id": "adapter-legacy-demand-ref-1",
            "source": "demand_ref:string@0.1",
            "target": "DemandIdentityRef@1.0",
            "classification": "LOSSLESS_WITH_PINNED_CONTEXT",
            "required_context": ["request_id", "version", "payload_hash", "canonical_ref"],
            "determinism": "The output is the exact pinned context after request_id equality validation.",
        },
    )
    write_json(
        compatibility_root / "migrations" / "submission-receipt-v0-to-v1.json",
        {
            "migration_id": "migration-submission-receipt-split-1",
            "source": "submission-receipt@0.1",
            "targets": ["submission-validation-receipt@1.0", "admission-receipt@1.0"],
            "classification": "EXPLICIT_MIGRATION_REQUIRED",
            "automatic": False,
            "required_evidence": [
                "original producer principal",
                "protocol validation decision",
                "editor admission decision",
            ],
            "reason": "The legacy object mixed protocol validation authority with editor admission authority.",
        },
    )
    write_json(
        compatibility_root / "migrations" / "visual-asset-demand-v1-to-v1.1.json",
        {
            "migration_id": "migration-visual-asset-demand-v1-to-v1.1",
            "source": "visual-asset-demand@1.0",
            "target": "visual-asset-demand@1.1",
            "classification": "EXPLICIT_OWNER_CONTEXT_MIGRATION_REQUIRED",
            "automatic": False,
            "lossless": True,
            "legacy_aliases": {
                "activative_intent": "activative_function",
                "wrongness_locks": "wrong_reading_locks",
                "composition": "composition_intent",
            },
            "owner_context_required_for": [
                "activative_semantic_lineage",
                "activation_contract",
                "visual_semantic_pack",
                "visual_narrative_program",
                "feature_contracts",
                "somatic_route_request",
            ],
            "prohibited_effects": compatibility_manifest["adapter_policy"]["prohibited_effects"],
            "traceability": "The target is a new immutable demand version whose supersedes identity pins the complete source payload.",
        },
    )
    direct_input = {
        "requester": compatibility_manifest,
        "provider": compatibility_manifest,
    }
    write_json(fixture_root / "direct" / "compatible.input.json", direct_input)
    write_json(
        fixture_root / "direct" / "compatible.expected.json",
        {
            "protocol_version": "1.0",
            "message_versions": {"visual-asset-demand": "1.1"},
            "features": compatibility_manifest["required_features"],
            "semantic_capabilities": semantic_capabilities,
            "behavioral_enforcement": "PASS",
            "signature_algorithm": "Ed25519",
        },
    )
    adapter_source = {"demand_ref": "req-format02-001"}
    adapter_context = {
        "request_id": "req-format02-001",
        "version": 1,
        "payload_hash": "sha256:" + "a" * 64,
        "canonical_ref": "cmf-contract://demands/req-format02-001/1",
    }
    write_json(fixture_root / "adapter" / "legacy-demand-ref.source.json", adapter_source)
    write_json(fixture_root / "adapter" / "legacy-demand-ref.context.json", adapter_context)
    write_json(fixture_root / "adapter" / "legacy-demand-ref.expected.json", adapter_context)
    write_json(
        fixture_root / "adapter" / "legacy-demand-ref.receipt.json",
        {
            "adapter_id": "adapter-legacy-demand-ref-1",
            "source_hash": canonical_value_hash(adapter_source),
            "context_hash": canonical_value_hash(adapter_context),
            "output_hash": canonical_value_hash(adapter_context),
            "field_preservation": "PASS",
            "lossless": True,
        },
    )
    write_json(
        fixture_root / "adapter" / "legacy-demand-ref.lossy.invalid.json",
        {
            "source": adapter_source,
            "context": {
                "request_id": "req-format02-001",
                "version": 1,
                "canonical_ref": "cmf-contract://demands/req-format02-001/1",
            },
            "expected_error": "PINNED_CONTEXT_INCOMPLETE",
        },
    )
    validation_target = examples["submission-validation-receipt"]
    admission_target = examples["admission-receipt"]
    migration_source = {
        "legacy_schema": "submission-receipt@0.1",
        "legacy_receipt_id": "legacy-submission-receipt-format02-001",
        "protocol_validation_payload": validation_target,
        "vae_admission_payload": admission_target,
        "migrated_at": "2026-07-14T10:00:00Z",
    }
    migration_evidence = {
        "protocol_validation_producer": "DELEGATION_PROTOCOL",
        "vae_admission_producer": "VISUAL_ASSET_EDITOR",
        "evidence_ref": {
            "resource_id": "migration-evidence-format02-001",
            "version": "1.0",
            "payload_hash": "sha256:" + "b" * 64,
            "canonical_ref": "cmf-contract://resources/migration-evidence-format02-001/1.0",
        },
        "output_ref": {
            "resource_id": "migration-output-format02-001",
            "version": "1.0",
            "payload_hash": "sha256:" + "b" * 64,
            "canonical_ref": "cmf-contract://resources/migration-output-format02-001/1.0",
        },
    }
    migration_receipt = {
        "migration_id": "migration-submission-receipt-split-1",
        "source_message_type": "submission-receipt",
        "source_version": "0.1",
        "target_version": "1.0",
        "source_payload_hash": canonical_value_hash(migration_source),
        "target_artifacts": [
            {
                "message_type": "submission-validation-receipt",
                "payload_hash": canonical_value_hash(validation_target),
                "canonical_ref": "cmf-contract://migrations/migration-submission-receipt-split-1/validation",
            },
            {
                "message_type": "admission-receipt",
                "payload_hash": canonical_value_hash(admission_target),
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
        "output_ref": migration_evidence["output_ref"],
        "evidence_refs": [migration_evidence["evidence_ref"]],
        "lossless": True,
        "migrated_at": migration_source["migrated_at"],
    }
    write_json(fixture_root / "migration" / "submission-receipt.source.json", migration_source)
    write_json(fixture_root / "migration" / "submission-receipt.owner-evidence.json", migration_evidence)
    write_json(
        fixture_root / "migration" / "submission-receipt.expected.json",
        {
            "targets": {
                "submission_validation_receipt": validation_target,
                "admission_receipt": admission_target,
            },
            "receipt": migration_receipt,
        },
    )
    write_json(
        fixture_root / "migration" / "submission-receipt.missing-owner.invalid.json",
        {
            "source": migration_source,
            "owner_evidence": {
                "protocol_validation_producer": "DELEGATION_PROTOCOL",
                "expected_error": "MIGRATION_REQUIRED",
            },
        },
    )
    lossy_source = deepcopy(migration_source)
    lossy_source["protocol_validation_payload"].pop("findings")
    write_json(
        fixture_root / "migration" / "submission-receipt.lossy.invalid.json",
        {"source": lossy_source, "owner_evidence": migration_evidence, "expected_error": "TARGET_INVALID"},
    )

    current_demand = examples["visual-asset-demand"]
    legacy_demand = {
        key: deepcopy(value)
        for key, value in current_demand.items()
        if key
        not in {
            "activative_semantic_lineage",
            "activation_contract",
            "visual_semantic_pack",
            "visual_narrative_program",
            "feature_contracts",
            "somatic_route_request",
            "activative_function",
            "wrong_reading_locks",
            "composition_intent",
        }
    }
    legacy_demand["activative_intent"] = {
        "function": current_demand["activative_function"]["function"],
        "expected_effect": current_demand["activative_function"]["intended_viewer_effect"],
        "sequence_position": current_demand["activative_function"]["sequence_position"],
    }
    legacy_demand["wrongness_locks"] = deepcopy(current_demand["wrong_reading_locks"])
    legacy_demand["composition"] = deepcopy(current_demand["composition_intent"])
    owner_context = {
        "owner_principal_type": "CONTENT_HARNESS",
        "semantic_context": {
            key: deepcopy(current_demand[key])
            for key in (
                "activative_semantic_lineage",
                "activation_contract",
                "visual_semantic_pack",
                "visual_narrative_program",
                "feature_contracts",
                "somatic_route_request",
            )
        },
        "evidence_ref": deepcopy(current_demand["reference_evidence"][0]),
        "output_ref": {
            "resource_id": "migration-output-visual-asset-demand-v1.1",
            "version": "1.0",
            "payload_hash": "sha256:" + "b" * 64,
            "canonical_ref": "cmf-contract://resources/migration-output-visual-asset-demand-v1.1/1.0",
        },
        "migrated_at": "2026-07-14T10:00:00Z",
    }
    source_hash = canonical_value_hash(legacy_demand)
    migrated_demand = {
        key: deepcopy(value)
        for key, value in legacy_demand.items()
        if key not in {"activative_intent", "wrongness_locks", "composition"}
    }
    migrated_demand["version"] = legacy_demand["version"] + 1
    migrated_demand["supersedes"] = {
        "request_id": legacy_demand["request_id"],
        "version": legacy_demand["version"],
        "payload_hash": source_hash,
        "canonical_ref": (
            f"cmf-contract://demands/{legacy_demand['request_id']}/{legacy_demand['version']}"
        ),
    }
    migrated_demand.update(deepcopy(owner_context["semantic_context"]))
    migrated_demand["activative_function"] = {
        "function": legacy_demand["activative_intent"]["function"],
        "intended_viewer_effect": legacy_demand["activative_intent"]["expected_effect"],
        "sequence_position": legacy_demand["activative_intent"]["sequence_position"],
    }
    migrated_demand["wrong_reading_locks"] = deepcopy(legacy_demand["wrongness_locks"])
    migrated_demand["composition_intent"] = deepcopy(legacy_demand["composition"])
    migrated_hash = canonical_value_hash(migrated_demand)
    migration_path_by_domain = {
        domain: f"/{domain}" for domain in CONSTITUTIONAL_DOMAINS
    }
    migration_path_by_domain["expression_moment_lineage"] = (
        "/activative_semantic_lineage/expression_moment_refs"
    )
    visual_demand_migration_receipt = {
        "migration_id": "migration-visual-asset-demand-v1-to-v1.1",
        "source_message_type": "visual-asset-demand",
        "source_version": "1.0",
        "target_version": "1.1",
        "source_payload_hash": source_hash,
        "target_artifacts": [
            {
                "message_type": "visual-asset-demand",
                "payload_hash": migrated_hash,
                "canonical_ref": (
                    f"cmf-contract://demands/{migrated_demand['request_id']}/{migrated_demand['version']}"
                ),
            }
        ],
        "ordered_transformations": [
            "pin_owner_context",
            "rename_activative_intent",
            "rename_wrongness_locks",
            "rename_composition",
            "create_immutable_successor",
        ],
        "authority_effect_analysis": [
            {
                "target_path": migration_path_by_domain[domain],
                "value_owner": "CONTENT_HARNESS",
                "effect": "PRESERVED",
            }
            for domain in sorted(CONSTITUTIONAL_DOMAINS)
        ],
        "preserved_semantic_paths": sorted(set(migration_path_by_domain.values())),
        "behavioral_enforcement": "PASS",
        "source_validation": "PASS",
        "target_validation": "PASS",
        "equivalence": "PASS",
        "output_ref": deepcopy(owner_context["output_ref"]),
        "evidence_refs": [deepcopy(owner_context["evidence_ref"])],
        "lossless": True,
        "migrated_at": owner_context["migrated_at"],
    }
    constitutional_root = fixture_root / "constitutional"
    write_json(
        constitutional_root / "aip-lineage.source.json",
        {"source": legacy_demand, "owner_context": owner_context},
    )
    write_json(
        constitutional_root / "aip-lineage.expected.json",
        {"target": migrated_demand, "receipt": visual_demand_migration_receipt},
    )
    write_json(
        constitutional_root / "expression-moment-drop.invalid.json",
        {
            "adapter_claim": {
                "adapter_id": "adapter-lossy-expression-moment",
                "source_version": "1.1",
                "target_version": "1.1",
                "lossless": False,
                "effects": [
                    {
                        "operation": "DROP",
                        "path": "/activative_semantic_lineage/expression_moment_refs",
                    }
                ],
            },
            "protected_paths": [
                "/activative_semantic_lineage/expression_moment_refs"
            ],
            "expected_error": "LOSSY_ADAPTER",
        },
    )
    wrong_reading_provider = deepcopy(compatibility_manifest)
    for capability in wrong_reading_provider["semantic_capabilities"]:
        if capability["domain"] == "wrong_reading_locks":
            capability["support_modes"] = ["PARSE"]
            capability["evaluator_profile_refs"] = []
    write_json(
        constitutional_root / "wrong-reading-unsupported.invalid.json",
        {
            "requester": compatibility_manifest,
            "provider": wrong_reading_provider,
            "expected_error": "SEMANTIC_ENFORCEMENT_UNSUPPORTED",
        },
    )
    evaluator_gap_provider = deepcopy(compatibility_manifest)
    for capability in evaluator_gap_provider["semantic_capabilities"]:
        if capability["domain"] == "visual_narrative_program":
            capability["support_modes"] = ["PRESERVE", "ENFORCE", "EVALUATE"]
            capability["evaluator_profile_refs"] = []
    write_json(
        constitutional_root / "evaluator-gap.invalid.json",
        {
            "requester": compatibility_manifest,
            "provider": evaluator_gap_provider,
            "expected_error": "EVALUATOR_EVIDENCE_MISSING",
        },
    )


def generate_release_manifest() -> None:
    included_roots = [
        ROOT / "packages" / "contracts",
        ROOT / "packages" / "fixtures",
        ROOT / "packages" / "compatibility",
        ROOT / "packages" / "validators",
        ROOT / "packages" / "protocol",
    ]
    manifest_path = ROOT / "packages" / "contracts" / "release-manifest.json"
    files = []
    for included_root in included_roots:
        for path in included_root.rglob("*"):
            if not path.is_file() or path == manifest_path:
                continue
            if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
                continue
            files.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "hash": file_hash(path),
                }
            )
    for path in (ROOT / "CONTRACT_CHANGELOG.md", ROOT / "COMPATIBILITY_MANIFEST.yaml"):
        files.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "hash": file_hash(path),
            }
        )
    write_json(
        manifest_path,
        {
            "package": "cmf-delegation-contract-baseline",
            "package_version": PACKAGE_VERSION,
            "protocol_version": PROTOCOL_VERSION,
            "status": "RELEASE_CANDIDATE",
            "signature_status": "UNSIGNED",
            "files": sorted(files, key=lambda item: item["path"]),
        },
    )


def main() -> None:
    generate_contracts()
    generate_fixtures()
    generate_compatibility()
    generate_release_manifest()
    print(f"Generated {len(CATALOG)} contracts and {len(SCENARIOS)} Format 02 scenarios.")


if __name__ == "__main__":
    main()
