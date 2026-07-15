"""Canonical message catalog for the CMF delegation protocol baseline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .common import (
    HASH,
    IDENTIFIER,
    JSON_POINTER,
    PACKAGE_VERSION,
    PRINCIPAL_TYPES,
    PROTOCOL_VERSION,
    STATES,
    TIMESTAMP,
    URI,
    VERSION,
    array,
    boolean,
    demand_ref,
    hash_value,
    integer,
    message_schema,
    nullable,
    obj,
    principal,
    ref,
    resource_ref,
    result_ref,
    string,
)


@dataclass(frozen=True)
class ContractDefinition:
    message_type: str
    title: str
    producer: str
    consumers: tuple[str, ...]
    idempotency: str
    lifecycle_effects: tuple[str, ...]
    schema: dict[str, Any]
    example: dict[str, Any]


def contract(
    message_type: str,
    title: str,
    producer: str,
    consumers: list[str],
    idempotency: str,
    lifecycle_effects: list[str],
    properties: dict[str, Any],
    example: dict[str, Any],
    schema_keywords: dict[str, Any] | None = None,
) -> ContractDefinition:
    schema = message_schema(message_type, title, properties)
    if schema_keywords:
        schema.update(schema_keywords)
    return ContractDefinition(
        message_type=message_type,
        title=title,
        producer=producer,
        consumers=tuple(consumers),
        idempotency=idempotency,
        lifecycle_effects=tuple(lifecycle_effects),
        schema=schema,
        example=example,
    )


T0 = "2026-07-14T10:00:00Z"
DEMAND = demand_ref()
DEMAND_2 = demand_ref("req-format02-002")
DEMAND_3 = demand_ref("req-format02-003")
PLAN = resource_ref("plan-format02-001")
BUDGET = resource_ref("budget-format02-001")
EVIDENCE = resource_ref("evidence-format02-001")
RESULT = result_ref()
FAILURE = {
    "code": "CONSTRAINT_CONFLICT",
    "category": "VALIDATION",
    "message": "Reserved title region intersects the required subject region.",
    "retryable": False,
    "field_paths": ["/composition/reserved_regions"],
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

DERIVATION_TYPES = (
    "DETERMINISTIC_CROP",
    "DETERMINISTIC_RESIZE",
    "DETERMINISTIC_FORMAT_CONVERSION",
    "DETERMINISTIC_COMPOSITE",
    "SEMANTIC_TRANSFORMATION",
    "TRANSFORMATIVE_RECOMPOSITION",
)

DERIVATIVE_SEMANTICS = (
    "NON_SEMANTIC",
    "SEMANTIC_TRANSFORMATIVE",
)


CONSTITUTIONAL_DOMAINS = (
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
)


def semantic_capability(domain: str) -> dict[str, Any]:
    modes = ["PRESERVE", "ENFORCE"]
    evaluator_profile_refs: list[dict[str, Any]] = []
    if domain in {
        "activation_contract",
        "visual_semantic_pack",
        "visual_narrative_program",
        "feature_contracts",
        "somatic_route_request",
        "expression_moment_lineage",
        "wrong_reading_locks",
        "derivative_lock_inheritance",
    }:
        modes.append("EVALUATE")
        evaluator_profile_refs.append(resource_ref(f"evaluator-{domain.replace('_', '-')}"))
    return {
        "domain": domain,
        "support_modes": modes,
        "evaluator_profile_refs": evaluator_profile_refs,
        "feature_contract_families": (
            ["gaze", "expression", "negative_space"] if domain == "feature_contracts" else []
        ),
        "evidence_refs": [resource_ref(f"capability-evidence-{domain.replace('_', '-')}")],
    }


def wrong_reading_lock_evidence() -> dict[str, Any]:
    return obj(
        {
            "lock_id": IDENTIFIER,
            "statement": string(minLength=1, maxLength=512),
            "meaning_hash": HASH,
            "scope_paths": array(JSON_POINTER, minItems=1, uniqueItems=True),
            "enforcement_level": integer(minimum=1, maximum=100),
        }
    )


CATALOG: tuple[ContractDefinition, ...] = (
    contract(
        "delegation-envelope",
        "Delegation Envelope",
        "ANY_PRINCIPAL",
        PRINCIPAL_TYPES,
        "CONDITIONAL",
        [],
        {
            "protocol_version": VERSION,
            "message_type": string(pattern=r"^[a-z][a-z0-9-]{2,63}$"),
            "message_version": VERSION,
            "message_id": IDENTIFIER,
            "correlation_id": IDENTIFIER,
            "causation_id": nullable(IDENTIFIER),
            "sender": ref("PrincipalRef"),
            "recipient": ref("PrincipalRef"),
            "authority": ref("AuthorityClaim"),
            "occurred_at": TIMESTAMP,
            "idempotency_key": nullable(IDENTIFIER),
            "payload_hash": HASH,
            "payload_ref": URI,
            "integrity": ref("IntegrityProof"),
        },
        {
            "protocol_version": PROTOCOL_VERSION,
            "message_type": "visual-asset-demand",
            "message_version": "1.1",
            "message_id": "msg-format02-001",
            "correlation_id": "corr-format02-001",
            "causation_id": None,
            "sender": principal("CONTENT_HARNESS"),
            "recipient": principal("DELEGATION_PROTOCOL"),
            "authority": {
                "action": "submit_visual_asset_demand",
                "principal": principal("CONTENT_HARNESS"),
                "field_scopes": [""],
            },
            "occurred_at": T0,
            "idempotency_key": "idem-format02-001",
            "payload_hash": hash_value("a"),
            "payload_ref": "cmf-contract://messages/visual-asset-demand/msg-format02-001",
            "integrity": {
                "algorithm": "Ed25519",
                "key_id": "cmf-key://content-harness/release-1",
                "signer": principal("CONTENT_HARNESS"),
                "signature": "A" * 86,
                "issued_at": T0,
                "expires_at": None,
                "nonce": "nonce-format02-001",
            },
        },
    ),
    contract(
        "visual-asset-demand",
        "Visual Asset Demand",
        "CONTENT_HARNESS",
        ["DELEGATION_PROTOCOL", "VISUAL_ASSET_EDITOR", "CONTROL_TOWER"],
        "REQUIRED",
        ["demand_recorded"],
        {
            "request_id": IDENTIFIER,
            "version": integer(minimum=1),
            "supersedes": nullable(ref("DemandIdentityRef")),
            "content_harness_ref": ref("ResourceIdentityRef"),
            "category_profile": ref("ResourceIdentityRef"),
            "format_profile": ref("ResourceIdentityRef"),
            "asset_classification": obj(
                {
                    "family": string(minLength=1, maxLength=64),
                    "subtype": string(minLength=1, maxLength=64),
                    "harness_role": string(minLength=1, maxLength=96),
                    "visual_syntax_role": string(minLength=1, maxLength=96),
                }
            ),
            "source_provenance": obj(
                {
                    "source_kind": string(enum=list(SOURCE_KINDS)),
                }
            ),
            "activative_semantic_lineage": obj(
                {
                    "activative_intelligence_pack_ref": ref("ResourceIdentityRef"),
                    "identity_dna_ref": ref("ResourceIdentityRef"),
                    "context_premise_ref": ref("ResourceIdentityRef"),
                    "resonance_map_ref": ref("ResourceIdentityRef"),
                    "matrix_edge_product_ref": ref("ResourceIdentityRef"),
                    "activative_call_refs": array(ref("ResourceIdentityRef"), minItems=1),
                    "reaction_receipt_refs": array(
                        ref("ResourceIdentityRef"), minItems=1, uniqueItems=True
                    ),
                    "expression_moment_refs": array(
                        ref("ResourceIdentityRef"), minItems=1, uniqueItems=True
                    ),
                    "source_evidence_refs": array(ref("ResourceIdentityRef"), minItems=1),
                },
                required=[
                    "activative_intelligence_pack_ref",
                    "identity_dna_ref",
                    "context_premise_ref",
                    "resonance_map_ref",
                    "matrix_edge_product_ref",
                    "activative_call_refs",
                    "source_evidence_refs",
                ],
            ),
            "activation_contract": obj(
                {
                    "edge_pressure": string(minLength=1, maxLength=512),
                    "activation_directions": array(
                        string(minLength=1, maxLength=128), minItems=1, uniqueItems=True
                    ),
                    "viewer_roles": array(
                        string(minLength=1, maxLength=128), minItems=1, uniqueItems=True
                    ),
                    "stance": string(minLength=1, maxLength=512),
                    "identity_urges": array(
                        string(minLength=1, maxLength=128), minItems=1, uniqueItems=True
                    ),
                    "intended_reaction": string(minLength=1, maxLength=1024),
                    "participation_design": string(minLength=1, maxLength=1024),
                    "micro_commitment": string(minLength=1, maxLength=1024),
                }
            ),
            "semantic_intent": obj(
                {
                    "subject": string(minLength=1, maxLength=1024),
                    "recognition_target": string(minLength=1, maxLength=1024),
                    "viewer_start_state": string(minLength=1, maxLength=512),
                    "viewer_end_state": string(minLength=1, maxLength=512),
                    "evidence_refs": array(ref("ResourceIdentityRef"), minItems=1),
                }
            ),
            "visual_semantic_pack": obj(
                {
                    "recognition_intent": string(minLength=1, maxLength=1024),
                    "recognition_carrier": string(minLength=1, maxLength=1024),
                    "audience_visual_world_refs": array(
                        ref("ResourceIdentityRef"), minItems=1
                    ),
                    "visual_dog_whistles": array(string(minLength=1, maxLength=256)),
                    "real_life_reference_classes": array(
                        string(minLength=1, maxLength=256)
                    ),
                    "emotional_load_carrier": string(minLength=1, maxLength=512),
                    "semiotic_mcda_receipt_ref": ref("ResourceIdentityRef"),
                }
            ),
            "visual_narrative_program": obj(
                {
                    "pattern_match": string(minLength=1, maxLength=1024),
                    "pattern_interrupt": string(minLength=1, maxLength=1024),
                    "attention_state_sequence": array(
                        string(minLength=1, maxLength=128), minItems=1
                    ),
                    "viewer_role_progression": array(
                        string(minLength=1, maxLength=128), minItems=1
                    ),
                    "prediction_gap": string(minLength=1, maxLength=1024),
                    "payoff": string(minLength=1, maxLength=1024),
                    "affinity_field": string(minLength=1, maxLength=1024),
                    "anticipation_residue": string(minLength=1, maxLength=1024),
                }
            ),
            "feature_contracts": array(
                obj(
                    {
                        "feature": string(minLength=1, maxLength=128),
                        "contract_ref": ref("ResourceIdentityRef"),
                        "required_for_meaning": boolean(),
                    }
                ),
                minItems=1,
            ),
            "somatic_route_request": obj(
                {
                    "t_codes": array(
                        string(minLength=1, maxLength=128), minItems=1, uniqueItems=True
                    ),
                    "v_codes": array(
                        string(minLength=1, maxLength=128), minItems=1, uniqueItems=True
                    ),
                    "intended_body_effect": string(minLength=1, maxLength=1024),
                }
            ),
            "activative_function": obj(
                {
                    "function": string(minLength=1, maxLength=256),
                    "intended_viewer_effect": string(minLength=1, maxLength=512),
                    "sequence_position": integer(minimum=0),
                }
            ),
            "wrong_reading_locks": array(
                string(minLength=1, maxLength=512), minItems=1, uniqueItems=True
            ),
            "composition_intent": obj(
                {
                    "canvas_width_px": integer(minimum=1, maximum=32768),
                    "canvas_height_px": integer(minimum=1, maximum=32768),
                    "intended_region": ref("BoundingBoxBasisPoints"),
                    "tolerance_basis_points": integer(minimum=0, maximum=2500),
                    "layer_role": string(minLength=1, maxLength=96),
                    "visual_weight": string(enum=["PRIMARY", "SECONDARY", "SUPPORTING"]),
                    "reserved_regions": array(ref("BoundingBoxBasisPoints")),
                    "gaze_direction": string(enum=["LEFT", "RIGHT", "CENTER", "NONE"]),
                }
            ),
            "identity_continuity": obj(
                {
                    "character_ref": nullable(ref("ResourceIdentityRef")),
                    "environment_ref": nullable(ref("ResourceIdentityRef")),
                }
            ),
            "reference_evidence": array(ref("ResourceIdentityRef"), minItems=1),
            "delivery": obj(
                {
                    "width_px": integer(minimum=1, maximum=32768),
                    "height_px": integer(minimum=1, maximum=32768),
                    "media_type": string(enum=["image/png", "image/jpeg", "image/webp"]),
                    "candidate_count": integer(minimum=1, maximum=16),
                }
            ),
            "evaluation_policy": obj(
                {
                    "profile_ref": ref("ResourceIdentityRef"),
                    "maximum_rounds": integer(minimum=1, maximum=20),
                    "hard_gate_codes": array(string(pattern=r"^[A-Z][A-Z0-9_]{2,63}$"), uniqueItems=True),
                }
            ),
            "execution_policy": obj(
                {
                    "budget_authorization_ref": ref("ResourceIdentityRef"),
                    "priority": string(enum=["LOW", "NORMAL", "HIGH", "CRITICAL"]),
                }
            ),
            "notes": nullable(string(maxLength=2048)),
        },
        {
            "request_id": DEMAND["request_id"],
            "version": 1,
            "supersedes": None,
            "content_harness_ref": resource_ref("content-harness-run-format02"),
            "category_profile": resource_ref("category-profile-portrait"),
            "format_profile": resource_ref("format02-reference-profile"),
            "asset_classification": {
                "family": "EDITORIAL_IMAGE",
                "subtype": "SUBJECT_PORTRAIT",
                "harness_role": "recognition_anchor",
                "visual_syntax_role": "primary_subject",
            },
            "source_provenance": {
                "source_kind": "interview_expression",
            },
            "activative_semantic_lineage": {
                "activative_intelligence_pack_ref": resource_ref("aip-format02-scene-004", "2.0"),
                "identity_dna_ref": resource_ref("coach-identity-dna-001", "4.0"),
                "context_premise_ref": resource_ref("context-premise-leadership-effort", "3.0"),
                "resonance_map_ref": resource_ref("resonance-coach-audience-011", "2.0"),
                "matrix_edge_product_ref": resource_ref("matrix-edge-effort-vs-design-003"),
                "activative_call_refs": [resource_ref("activative-call-format02-004")],
                "reaction_receipt_refs": [resource_ref("reaction-receipt-format02-004")],
                "expression_moment_refs": [resource_ref("expression-moment-format02-004")],
                "source_evidence_refs": [EVIDENCE],
            },
            "activation_contract": {
                "edge_pressure": "effort_without_system_design",
                "activation_directions": ["mirror", "contradiction"],
                "viewer_roles": ["skeptical_listener", "witness"],
                "stance": "design_and_leverage_over_blind_effort",
                "identity_urges": ["be_seen", "restore_dignity"],
                "intended_reaction": "Recognize defensive skepticism before explanation.",
                "participation_design": "Compare effort with the system producing the result.",
                "micro_commitment": "Admit that more effort is not always the missing intervention.",
            },
            "semantic_intent": {
                "subject": "A calm facilitator facing the content area.",
                "recognition_target": "The facilitator remains identifiable across the sequence.",
                "viewer_start_state": "Unoriented",
                "viewer_end_state": "Ready to follow the lesson",
                "evidence_refs": [EVIDENCE],
            },
            "visual_semantic_pack": {
                "recognition_intent": "That is my defensive reaction before I accept a better frame.",
                "recognition_carrier": "Restrained three-quarter skepticism with gaze toward the comparison field.",
                "audience_visual_world_refs": [resource_ref("visual-world-coaching-minimal-theatre")],
                "visual_dog_whistles": ["restrained_coach_reaction", "open_explanation_space"],
                "real_life_reference_classes": ["human_listening_reaction"],
                "emotional_load_carrier": "eyes_and_brow_tension",
                "semiotic_mcda_receipt_ref": resource_ref("semiotic-mcda-format02-004"),
            },
            "visual_narrative_program": {
                "pattern_match": "Familiar listening pose in a coaching explanation.",
                "pattern_interrupt": "Skeptical micro-expression appears before the explanatory text.",
                "attention_state_sequence": ["stimulation", "captivation", "prediction", "payoff", "affinity"],
                "viewer_role_progression": ["observer", "self-recognizer", "learner"],
                "prediction_gap": "Why is the listener resisting an apparently helpful explanation?",
                "payoff": "The reaction reveals effort is being defended because system design threatens identity.",
                "affinity_field": "Restrained human uncertainty rather than mockery.",
                "anticipation_residue": "The viewer waits for effort versus design to resolve.",
            },
            "feature_contracts": [
                {
                    "feature": "gaze",
                    "contract_ref": resource_ref("feature-gaze-format02-004"),
                    "required_for_meaning": True,
                },
                {
                    "feature": "expression",
                    "contract_ref": resource_ref("feature-expression-format02-004"),
                    "required_for_meaning": True,
                },
                {
                    "feature": "negative_space",
                    "contract_ref": resource_ref("feature-negative-space-format02-004"),
                    "required_for_meaning": True,
                },
            ],
            "somatic_route_request": {
                "t_codes": ["held_stillness", "breath"],
                "v_codes": ["tactile_proximity"],
                "intended_body_effect": "Quiet recognition rather than comic exaggeration.",
            },
            "activative_function": {
                "function": "orient_attention",
                "intended_viewer_effect": "Direct attention toward the reserved title region.",
                "sequence_position": 0,
            },
            "wrong_reading_locks": [
                "Do not place the subject inside the title-safe region.",
                "Do not read the expression as contempt or mockery.",
                "Do not imply that effort is worthless.",
            ],
            "composition_intent": {
                "canvas_width_px": 1080,
                "canvas_height_px": 1920,
                "intended_region": {"x": 500, "y": 2500, "width": 4400, "height": 6000},
                "tolerance_basis_points": 300,
                "layer_role": "foreground_subject",
                "visual_weight": "PRIMARY",
                "reserved_regions": [{"x": 5200, "y": 800, "width": 4000, "height": 2500}],
                "gaze_direction": "RIGHT",
            },
            "identity_continuity": {
                "character_ref": resource_ref("character-facilitator-01"),
                "environment_ref": None,
            },
            "reference_evidence": [EVIDENCE],
            "delivery": {
                "width_px": 1080,
                "height_px": 1920,
                "media_type": "image/png",
                "candidate_count": 1,
            },
            "evaluation_policy": {
                "profile_ref": resource_ref("evaluation-profile-format02"),
                "maximum_rounds": 3,
                "hard_gate_codes": ["TITLE_REGION_CLEAR", "IDENTITY_CONTINUITY"],
            },
            "execution_policy": {"budget_authorization_ref": BUDGET, "priority": "NORMAL"},
            "notes": None,
        },
        schema_keywords={
            "allOf": [
                {
                    "if": {
                        "properties": {
                            "source_provenance": {
                                "properties": {
                                    "source_kind": {"const": "interview_expression"}
                                },
                                "required": ["source_kind"],
                            }
                        },
                        "required": ["source_provenance"],
                    },
                    "then": {
                        "properties": {
                            "activative_semantic_lineage": {
                                "required": [
                                    "reaction_receipt_refs",
                                    "expression_moment_refs",
                                ]
                            }
                        },
                        "required": ["activative_semantic_lineage"],
                    },
                }
            ]
        },
    ),
    contract(
        "visual-asset-submission",
        "Visual Asset Submission",
        "CONTENT_HARNESS",
        ["DELEGATION_PROTOCOL", "CONTROL_TOWER"],
        "REQUIRED",
        ["submission_received"],
        {
            "submission_id": IDENTIFIER,
            "demand": ref("DemandIdentityRef"),
            "submitted_at": TIMESTAMP,
            "requested_priority": string(enum=["LOW", "NORMAL", "HIGH", "CRITICAL"]),
            "callback_resources": array(ref("ResourceIdentityRef"), minItems=1),
            "idempotency_key": IDENTIFIER,
        },
        {
            "submission_id": "submission-format02-001",
            "demand": DEMAND,
            "submitted_at": T0,
            "requested_priority": "NORMAL",
            "callback_resources": [resource_ref("callback-status-format02")],
            "idempotency_key": "idem-submission-format02-001",
        },
    ),
    contract(
        "submission-validation-receipt",
        "Submission Validation Receipt",
        "DELEGATION_PROTOCOL",
        ["CONTENT_HARNESS", "VISUAL_ASSET_EDITOR", "CONTROL_TOWER"],
        "REQUIRED",
        ["submission_validation_accepted", "submission_validation_rejected"],
        {
            "receipt_id": IDENTIFIER,
            "submission_id": IDENTIFIER,
            "demand": ref("DemandIdentityRef"),
            "status": string(enum=["ACCEPTED", "REJECTED"]),
            "validated_at": TIMESTAMP,
            "findings": array(ref("EvidenceFinding"), minItems=1),
            "rejection": nullable(ref("FailureSummary")),
            "negotiated_profile": nullable(ref("ResourceIdentityRef")),
        },
        {
            "receipt_id": "validation-receipt-format02-001",
            "submission_id": "submission-format02-001",
            "demand": DEMAND,
            "status": "ACCEPTED",
            "validated_at": T0,
            "findings": [
                {
                    "code": "SCHEMA_VALID",
                    "verdict": "PASS",
                    "evidence_refs": [EVIDENCE],
                    "note": None,
                }
            ],
            "rejection": None,
            "negotiated_profile": resource_ref("compatibility-profile-1-0"),
        },
    ),
    contract(
        "admission-receipt",
        "Visual Asset Editor Admission Receipt",
        "VISUAL_ASSET_EDITOR",
        ["DELEGATION_PROTOCOL", "CONTENT_HARNESS", "CONTROL_TOWER"],
        "REQUIRED",
        ["admission_accepted", "admission_rejected"],
        {
            "receipt_id": IDENTIFIER,
            "submission_receipt_id": IDENTIFIER,
            "execution": nullable(ref("ExecutionIdentityRef")),
            "demand": ref("DemandIdentityRef"),
            "status": string(enum=["ACCEPTED", "REJECTED"]),
            "admitted_at": TIMESTAMP,
            "status_resource": nullable(ref("ResourceIdentityRef")),
            "rejection": nullable(ref("FailureSummary")),
        },
        {
            "receipt_id": "admission-receipt-format02-001",
            "submission_receipt_id": "validation-receipt-format02-001",
            "execution": {"execution_id": "execution-format02-001", "demand": DEMAND, "plan_ref": PLAN},
            "demand": DEMAND,
            "status": "ACCEPTED",
            "admitted_at": T0,
            "status_resource": resource_ref("execution-status-format02-001"),
            "rejection": None,
        },
    ),
    contract(
        "visual-asset-event",
        "Visual Asset Lifecycle Event",
        "VISUAL_ASSET_EDITOR",
        ["DELEGATION_PROTOCOL", "CONTENT_HARNESS", "CONTROL_TOWER"],
        "REQUIRED",
        [
            "execution_started",
            "execution_blocked",
            "execution_resumed",
            "execution_failed",
        ],
        {
            "event_id": IDENTIFIER,
            "execution": ref("ExecutionIdentityRef"),
            "event_type": string(enum=["STARTED", "PROGRESS", "REVALIDATION_STARTED"]),
            "projected_state": string(enum=STATES),
            "occurred_at": TIMESTAMP,
            "progress_basis_points": integer(minimum=0, maximum=10000),
            "reason": nullable(ref("FailureSummary")),
            "evidence_refs": array(ref("ResourceIdentityRef")),
        },
        {
            "event_id": "event-format02-started",
            "execution": {"execution_id": "execution-format02-001", "demand": DEMAND, "plan_ref": PLAN},
            "event_type": "STARTED",
            "projected_state": "IN_PROGRESS",
            "occurred_at": T0,
            "progress_basis_points": 500,
            "reason": None,
            "evidence_refs": [EVIDENCE],
        },
    ),
    contract(
        "delegation-set",
        "Delegation Set",
        "CONTENT_HARNESS",
        ["DELEGATION_PROTOCOL", "VISUAL_ASSET_EDITOR", "CONTROL_TOWER"],
        "REQUIRED",
        ["delegation_set_recorded"],
        {
            "set_id": IDENTIFIER,
            "version": integer(minimum=1),
            "member_demands": array(ref("DemandIdentityRef"), minItems=1, uniqueItems=True),
            "dependency_edges": array(
                obj(
                    {
                        "predecessor": ref("DemandIdentityRef"),
                        "successor": ref("DemandIdentityRef"),
                        "kind": string(enum=["REQUIRES", "ORDER_BEFORE", "SHARES_IDENTITY"]),
                    }
                ),
                uniqueItems=True,
            ),
            "completion_policy": string(enum=["ALL", "MINIMUM_COUNT", "NAMED_MEMBERS"]),
            "minimum_completed": integer(minimum=1),
            "failure_policy": string(enum=["FAIL_FAST", "CONTINUE_INDEPENDENT", "PAUSE_DEPENDENTS"]),
        },
        {
            "set_id": "set-format02-001",
            "version": 1,
            "member_demands": [DEMAND, DEMAND_2, DEMAND_3],
            "dependency_edges": [
                {"predecessor": DEMAND, "successor": DEMAND_2, "kind": "SHARES_IDENTITY"},
                {"predecessor": DEMAND_2, "successor": DEMAND_3, "kind": "ORDER_BEFORE"},
            ],
            "completion_policy": "ALL",
            "minimum_completed": 3,
            "failure_policy": "PAUSE_DEPENDENTS",
        },
    ),
    contract(
        "budget-authorization",
        "Budget Authorization",
        "CONTENT_HARNESS",
        ["DELEGATION_PROTOCOL", "VISUAL_ASSET_EDITOR", "CONTROL_TOWER"],
        "REQUIRED",
        ["budget_authorized"],
        {
            "authorization_id": IDENTIFIER,
            "scope": string(enum=["DEMAND", "DELEGATION_SET"]),
            "demand": nullable(ref("DemandIdentityRef")),
            "delegation_set_ref": nullable(ref("ResourceIdentityRef")),
            "maximum_cost": ref("MoneyAmount"),
            "maximum_attempts": integer(minimum=1, maximum=100),
            "maximum_duration_seconds": integer(minimum=1),
            "valid_from": TIMESTAMP,
            "valid_until": TIMESTAMP,
        },
        {
            "authorization_id": "budget-format02-001",
            "scope": "DEMAND",
            "demand": DEMAND,
            "delegation_set_ref": None,
            "maximum_cost": {"currency": "EUR", "minor_units": 2500},
            "maximum_attempts": 3,
            "maximum_duration_seconds": 3600,
            "valid_from": T0,
            "valid_until": "2026-07-14T11:00:00Z",
        },
    ),
    contract(
        "budget-escalation-request",
        "Budget Escalation Request",
        "VISUAL_ASSET_EDITOR",
        ["DELEGATION_PROTOCOL", "CONTENT_HARNESS", "CONTROL_TOWER"],
        "REQUIRED",
        ["budget_escalation_requested"],
        {
            "request_id": IDENTIFIER,
            "execution": ref("ExecutionIdentityRef"),
            "current_authorization_ref": ref("ResourceIdentityRef"),
            "requested_additional_cost": ref("MoneyAmount"),
            "requested_additional_attempts": integer(minimum=0, maximum=100),
            "reason": string(minLength=1, maxLength=1024),
            "evidence_refs": array(ref("ResourceIdentityRef"), minItems=1),
        },
        {
            "request_id": "budget-escalation-format02-001",
            "execution": {"execution_id": "execution-format02-001", "demand": DEMAND, "plan_ref": PLAN},
            "current_authorization_ref": BUDGET,
            "requested_additional_cost": {"currency": "EUR", "minor_units": 1000},
            "requested_additional_attempts": 1,
            "reason": "One additional generation round is required.",
            "evidence_refs": [EVIDENCE],
        },
    ),
    contract(
        "budget-escalation-response",
        "Budget Escalation Response",
        "CONTENT_HARNESS",
        ["DELEGATION_PROTOCOL", "VISUAL_ASSET_EDITOR", "CONTROL_TOWER"],
        "REQUIRED",
        ["budget_escalation_approved", "budget_escalation_denied"],
        {
            "response_id": IDENTIFIER,
            "escalation_request_id": IDENTIFIER,
            "decision": string(enum=["APPROVED", "DENIED"]),
            "replacement_authorization_ref": nullable(ref("ResourceIdentityRef")),
            "reason": string(minLength=1, maxLength=1024),
            "decided_at": TIMESTAMP,
        },
        {
            "response_id": "budget-response-format02-001",
            "escalation_request_id": "budget-escalation-format02-001",
            "decision": "APPROVED",
            "replacement_authorization_ref": resource_ref("budget-format02-002"),
            "reason": "Additional round is within campaign limits.",
            "decided_at": T0,
        },
    ),
    contract(
        "cancellation-request",
        "Cancellation Request",
        "CONTENT_HARNESS",
        ["DELEGATION_PROTOCOL", "VISUAL_ASSET_EDITOR", "CONTROL_TOWER"],
        "REQUIRED",
        ["cancellation_requested"],
        {
            "request_id": IDENTIFIER,
            "demand": ref("DemandIdentityRef"),
            "execution_id": nullable(IDENTIFIER),
            "mode": string(enum=["BEST_EFFORT", "IMMEDIATE_IF_NOT_STARTED"]),
            "reason": string(minLength=1, maxLength=1024),
            "requested_at": TIMESTAMP,
        },
        {
            "request_id": "cancel-format02-001",
            "demand": DEMAND,
            "execution_id": "execution-format02-001",
            "mode": "BEST_EFFORT",
            "reason": "The lesson sequence was withdrawn.",
            "requested_at": T0,
        },
    ),
    contract(
        "cancellation-receipt",
        "Cancellation Receipt",
        "VISUAL_ASSET_EDITOR",
        ["DELEGATION_PROTOCOL", "CONTENT_HARNESS", "CONTROL_TOWER"],
        "REQUIRED",
        ["cancellation_accepted", "cancellation_rejected", "cancellation_completed"],
        {
            "receipt_id": IDENTIFIER,
            "cancellation_request_id": IDENTIFIER,
            "demand": ref("DemandIdentityRef"),
            "status": string(enum=["ACCEPTED", "REJECTED", "COMPLETED"]),
            "effective_at": nullable(TIMESTAMP),
            "reason": nullable(ref("FailureSummary")),
            "partial_artifact_refs": array(ref("ResourceIdentityRef")),
        },
        {
            "receipt_id": "cancel-receipt-format02-001",
            "cancellation_request_id": "cancel-format02-001",
            "demand": DEMAND,
            "status": "COMPLETED",
            "effective_at": T0,
            "reason": None,
            "partial_artifact_refs": [],
        },
    ),
    contract(
        "constraint-conflict",
        "Constraint Conflict",
        "VISUAL_ASSET_EDITOR",
        ["DELEGATION_PROTOCOL", "CONTENT_HARNESS", "CONTROL_TOWER"],
        "REQUIRED",
        ["constraint_conflict_reported"],
        {
            "conflict_id": IDENTIFIER,
            "execution": ref("ExecutionIdentityRef"),
            "conflicting_paths": array(JSON_POINTER, minItems=2, uniqueItems=True),
            "summary": ref("FailureSummary"),
            "evidence_refs": array(ref("ResourceIdentityRef"), minItems=1),
            "suggested_resolution": nullable(string(maxLength=1024)),
        },
        {
            "conflict_id": "conflict-format02-001",
            "execution": {"execution_id": "execution-format02-001", "demand": DEMAND, "plan_ref": PLAN},
            "conflicting_paths": ["/composition/intended_region", "/composition/reserved_regions"],
            "summary": FAILURE,
            "evidence_refs": [EVIDENCE],
            "suggested_resolution": "Move the intended region left by 300 basis points.",
        },
    ),
    contract(
        "amendment-proposal",
        "Amendment Proposal",
        "VISUAL_ASSET_EDITOR",
        ["DELEGATION_PROTOCOL", "VISUAL_ASSET_EDITOR", "CONTROL_TOWER"],
        "REQUIRED",
        ["amendment_proposed"],
        {
            "proposal_id": IDENTIFIER,
            "demand": ref("DemandIdentityRef"),
            "execution": ref("ExecutionIdentityRef"),
            "trigger_conflict_id": nullable(IDENTIFIER),
            "options": array(
                obj(
                    {
                        "option_id": IDENTIFIER,
                        "changes": array(ref("ChangeItem"), minItems=1),
                        "authority_class": string(
                            enum=[
                                "INTERNAL_PRODUCTION",
                                "EXECUTION_POLICY",
                                "COMPOSITION",
                                "SEMANTIC_ACTIVATIVE",
                                "CONSTITUTIONAL",
                            ]
                        ),
                        "rationale": string(minLength=1, maxLength=1024),
                        "predicted_impact_ref": ref("ResourceIdentityRef"),
                        "evidence_refs": array(ref("ResourceIdentityRef"), minItems=1),
                    }
                ),
                minItems=1,
            ),
            "expires_at": TIMESTAMP,
            "proposed_at": TIMESTAMP,
        },
        {
            "proposal_id": "amendment-format02-001",
            "demand": DEMAND,
            "execution": {"execution_id": "execution-format02-001", "demand": DEMAND, "plan_ref": PLAN},
            "trigger_conflict_id": "conflict-format02-001",
            "options": [{
                "option_id": "option-format02-001",
                "changes": [
                {
                    "path": "/composition/intended_region",
                    "operation": "REPLACE",
                    "value_ref": resource_ref("patch-format02-amendment-001"),
                    "reason": "Resolve the reported title-region conflict.",
                }
                ],
                "authority_class": "COMPOSITION",
                "rationale": "Move the intended region without changing production strategy.",
                "predicted_impact_ref": resource_ref("impact-format02-amendment-001"),
                "evidence_refs": [EVIDENCE],
            }],
            "expires_at": "2026-07-14T11:00:00Z",
            "proposed_at": T0,
        },
    ),
    contract(
        "amendment-response",
        "Amendment Response",
        "CONTENT_HARNESS",
        ["DELEGATION_PROTOCOL", "CONTENT_HARNESS", "CONTROL_TOWER"],
        "REQUIRED",
        ["amendment_accepted", "amendment_rejected"],
        {
            "response_id": IDENTIFIER,
            "proposal_id": IDENTIFIER,
            "selected_option_id": nullable(IDENTIFIER),
            "decision": string(enum=["ACCEPTED", "REJECTED", "ALTERNATIVE_REQUESTED"]),
            "authorized_successor_demand": nullable(ref("DemandIdentityRef")),
            "decision_principal": ref("PrincipalRef"),
            "reason": nullable(ref("FailureSummary")),
            "decided_at": TIMESTAMP,
        },
        {
            "response_id": "amendment-response-format02-001",
            "proposal_id": "amendment-format02-001",
            "selected_option_id": "option-format02-001",
            "decision": "ACCEPTED",
            "authorized_successor_demand": demand_ref(version=2),
            "decision_principal": principal("CONTENT_HARNESS"),
            "reason": None,
            "decided_at": T0,
        },
    ),
    contract(
        "demand-supersession",
        "Demand Supersession",
        "CONTENT_HARNESS",
        ["DELEGATION_PROTOCOL", "VISUAL_ASSET_EDITOR", "CONTROL_TOWER"],
        "REQUIRED",
        ["demand_superseded"],
        {
            "supersession_id": IDENTIFIER,
            "superseded_demand": ref("DemandIdentityRef"),
            "replacement_demand": ref("DemandIdentityRef"),
            "invalidation_scope": array(JSON_POINTER, minItems=1, uniqueItems=True),
            "reason": string(minLength=1, maxLength=1024),
            "effective_at": TIMESTAMP,
        },
        {
            "supersession_id": "supersession-format02-001",
            "superseded_demand": DEMAND,
            "replacement_demand": demand_ref(version=2),
            "invalidation_scope": ["/composition"],
            "reason": "A new composition version replaces the prior demand.",
            "effective_at": T0,
        },
    ),
    contract(
        "selective-invalidation-receipt",
        "Selective Invalidation Receipt",
        "VISUAL_ASSET_EDITOR",
        ["CONTENT_HARNESS", "VISUAL_ASSET_EDITOR", "CONTROL_TOWER"],
        "REQUIRED",
        ["selective_invalidation_recorded"],
        {
            "receipt_id": IDENTIFIER,
            "supersession_id": IDENTIFIER,
            "invalidated_paths": array(JSON_POINTER, minItems=1, uniqueItems=True),
            "preserved_evidence_refs": array(ref("ResourceIdentityRef")),
            "invalidated_evidence_refs": array(ref("ResourceIdentityRef")),
            "recorded_at": TIMESTAMP,
        },
        {
            "receipt_id": "invalidation-receipt-format02-001",
            "supersession_id": "supersession-format02-001",
            "invalidated_paths": ["/composition"],
            "preserved_evidence_refs": [resource_ref("identity-evidence-format02")],
            "invalidated_evidence_refs": [EVIDENCE],
            "recorded_at": T0,
        },
    ),
    contract(
        "asset-result-contract",
        "Visual Asset Result Contract",
        "VISUAL_ASSET_EDITOR",
        ["DELEGATION_PROTOCOL", "CONTENT_HARNESS", "CONTROL_TOWER"],
        "REQUIRED",
        ["result_declared"],
        {
            "result_id": IDENTIFIER,
            "version": integer(minimum=1),
            "execution": ref("ExecutionIdentityRef"),
            "demand": ref("DemandIdentityRef"),
            "artifact_ref": ref("ResourceIdentityRef"),
            "artifact_media_type": string(enum=["image/png", "image/jpeg", "image/webp"]),
            "artifact_width_px": integer(minimum=1, maximum=32768),
            "artifact_height_px": integer(minimum=1, maximum=32768),
            "completion_status": string(enum=["COMPLETE", "PARTIAL"]),
            "unresolved_roles": array(string(minLength=1, maxLength=96), uniqueItems=True),
            "provenance_refs": array(ref("ResourceIdentityRef"), minItems=1),
            "evaluation_findings": array(ref("EvidenceFinding"), minItems=1),
            "cost_consumed": ref("MoneyAmount"),
            "attempts_consumed": integer(minimum=1),
            "declared_at": TIMESTAMP,
        },
        {
            "result_id": RESULT["result_id"],
            "version": 1,
            "execution": {"execution_id": "execution-format02-001", "demand": DEMAND, "plan_ref": PLAN},
            "demand": DEMAND,
            "artifact_ref": resource_ref("artifact-format02-001"),
            "artifact_media_type": "image/png",
            "artifact_width_px": 1080,
            "artifact_height_px": 1920,
            "completion_status": "COMPLETE",
            "unresolved_roles": [],
            "provenance_refs": [resource_ref("provenance-format02-001")],
            "evaluation_findings": [
                {
                    "code": "FORMAT02_CONFORMANT",
                    "verdict": "PASS",
                    "evidence_refs": [EVIDENCE],
                    "note": None,
                }
            ],
            "cost_consumed": {"currency": "EUR", "minor_units": 1800},
            "attempts_consumed": 2,
            "declared_at": T0,
        },
    ),
    contract(
        "result-acknowledgement",
        "Result Acknowledgement",
        "CONTENT_HARNESS",
        ["DELEGATION_PROTOCOL", "VISUAL_ASSET_EDITOR", "CONTROL_TOWER"],
        "REQUIRED",
        ["result_accepted", "result_rejected", "result_accepted_with_concerns"],
        {
            "acknowledgement_id": IDENTIFIER,
            "result": ref("ResultIdentityRef"),
            "demand": ref("DemandIdentityRef"),
            "decision": string(enum=["ACCEPTED", "ACCEPTED_WITH_CONCERNS", "REJECTED"]),
            "consumption_authorized": boolean(),
            "findings": array(ref("EvidenceFinding"), minItems=1),
            "acknowledged_at": TIMESTAMP,
        },
        {
            "acknowledgement_id": "ack-format02-001",
            "result": RESULT,
            "demand": DEMAND,
            "decision": "ACCEPTED",
            "consumption_authorized": True,
            "findings": [
                {
                    "code": "HARNESS_ACCEPTED",
                    "verdict": "PASS",
                    "evidence_refs": [EVIDENCE],
                    "note": None,
                }
            ],
            "acknowledged_at": T0,
        },
    ),
    contract(
        "invalidation-notice",
        "Result Invalidation Notice",
        "CONTENT_HARNESS",
        ["DELEGATION_PROTOCOL", "VISUAL_ASSET_EDITOR", "CONTROL_TOWER"],
        "REQUIRED",
        ["result_invalidated"],
        {
            "notice_id": IDENTIFIER,
            "result": ref("ResultIdentityRef"),
            "demand": ref("DemandIdentityRef"),
            "scope": array(JSON_POINTER, minItems=1, uniqueItems=True),
            "reason": string(minLength=1, maxLength=1024),
            "replacement_expected": boolean(),
            "effective_at": TIMESTAMP,
        },
        {
            "notice_id": "invalidation-format02-001",
            "result": RESULT,
            "demand": DEMAND,
            "scope": ["/artifact_ref"],
            "reason": "The campaign title lock changed after completion.",
            "replacement_expected": True,
            "effective_at": T0,
        },
    ),
    contract(
        "revocation-notice",
        "Result Revocation Notice",
        "VISUAL_ASSET_EDITOR",
        ["DELEGATION_PROTOCOL", "VISUAL_ASSET_EDITOR", "CONTROL_TOWER"],
        "REQUIRED",
        ["result_revoked"],
        {
            "notice_id": IDENTIFIER,
            "result": ref("ResultIdentityRef"),
            "demand": ref("DemandIdentityRef"),
            "reason": string(minLength=1, maxLength=1024),
            "consumption_must_stop": boolean(),
            "effective_at": TIMESTAMP,
        },
        {
            "notice_id": "revocation-format02-001",
            "result": RESULT,
            "demand": DEMAND,
            "reason": "The source consent was withdrawn.",
            "consumption_must_stop": True,
            "effective_at": T0,
        },
    ),
    contract(
        "replacement-notice",
        "Result Replacement Notice",
        "VISUAL_ASSET_EDITOR",
        ["DELEGATION_PROTOCOL", "VISUAL_ASSET_EDITOR", "CONTROL_TOWER"],
        "REQUIRED",
        ["result_replaced"],
        {
            "notice_id": IDENTIFIER,
            "replaced_result": ref("ResultIdentityRef"),
            "replacement_result": ref("ResultIdentityRef"),
            "demand": ref("DemandIdentityRef"),
            "reason": string(minLength=1, maxLength=1024),
            "effective_at": TIMESTAMP,
        },
        {
            "notice_id": "replacement-format02-001",
            "replaced_result": RESULT,
            "replacement_result": result_ref("result-format02-002"),
            "demand": DEMAND,
            "reason": "A corrected crop replaces the prior artifact.",
            "effective_at": T0,
        },
    ),
    contract(
        "delegation-failure",
        "Delegation Failure",
        "ANY_PRINCIPAL",
        PRINCIPAL_TYPES,
        "REQUIRED",
        ["delegation_failed"],
        {
            "failure_id": IDENTIFIER,
            "demand": nullable(ref("DemandIdentityRef")),
            "execution_id": nullable(IDENTIFIER),
            "detecting_principal": ref("PrincipalRef"),
            "summary": ref("FailureSummary"),
            "evidence_refs": array(ref("ResourceIdentityRef")),
            "occurred_at": TIMESTAMP,
        },
        {
            "failure_id": "failure-format02-001",
            "demand": DEMAND,
            "execution_id": "execution-format02-001",
            "detecting_principal": principal("DELEGATION_PROTOCOL"),
            "summary": FAILURE,
            "evidence_refs": [EVIDENCE],
            "occurred_at": T0,
        },
    ),
    contract(
        "delegation-audit-receipt",
        "Delegation Audit Receipt",
        "DELEGATION_PROTOCOL",
        ["CONTENT_HARNESS", "VISUAL_ASSET_EDITOR", "CONTROL_TOWER"],
        "REQUIRED",
        ["audit_receipt_recorded"],
        {
            "receipt_id": IDENTIFIER,
            "message_id": IDENTIFIER,
            "correlation_id": IDENTIFIER,
            "payload_hash": HASH,
            "previous_receipt_hash": nullable(HASH),
            "effective_state": nullable(string(enum=STATES)),
            "authority_verdict": string(enum=["PASS", "FAIL"]),
            "schema_verdict": string(enum=["PASS", "FAIL"]),
            "recorded_at": TIMESTAMP,
        },
        {
            "receipt_id": "audit-format02-001",
            "message_id": "msg-format02-001",
            "correlation_id": "corr-format02-001",
            "payload_hash": hash_value("a"),
            "previous_receipt_hash": None,
            "effective_state": "DRAFT",
            "authority_verdict": "PASS",
            "schema_verdict": "PASS",
            "recorded_at": T0,
        },
    ),
    contract(
        "derivative-lock-inheritance",
        "Derivative Wrong-Reading-Lock Inheritance",
        "ANY_PRINCIPAL",
        PRINCIPAL_TYPES,
        "REQUIRED",
        [],
        {
            "inheritance_id": IDENTIFIER,
            "authoritative_parent_ref": ref("ResourceIdentityRef"),
            "parent_contract_version": VERSION,
            "governing_authoritative_demand_ref": ref("DemandIdentityRef"),
            "parent_lock_evidence": obj(
                {
                    "parent_wrong_reading_locks": nullable(
                        array(wrong_reading_lock_evidence(), minItems=1, uniqueItems=True)
                    ),
                    "parent_lock_set_ref": nullable(ref("ResourceIdentityRef")),
                    "parent_lock_set_hash": HASH,
                }
            ),
            "derivative_ref": ref("ResourceIdentityRef"),
            "derivative_wrong_reading_locks": array(
                wrong_reading_lock_evidence(), minItems=1, uniqueItems=True
            ),
            "derivation_type": string(enum=list(DERIVATION_TYPES)),
            "derivative_semantics": string(enum=list(DERIVATIVE_SEMANTICS)),
            "authoritative_lock_authorization": nullable(
                obj(
                    {
                        "authoritative_demand_ref": ref("DemandIdentityRef"),
                        "supersedes_demand_ref": nullable(ref("DemandIdentityRef")),
                        "applicable_wrong_reading_locks": array(
                            wrong_reading_lock_evidence(), minItems=1, uniqueItems=True
                        ),
                        "authorization_evidence_ref": ref("ResourceIdentityRef"),
                    }
                )
            ),
            "declared_at": TIMESTAMP,
        },
        {
            "inheritance_id": "inheritance-format02-001",
            "authoritative_parent_ref": resource_ref("parent-asset-format02-001"),
            "parent_contract_version": "1.0",
            "governing_authoritative_demand_ref": DEMAND,
            "parent_lock_evidence": {
                "parent_wrong_reading_locks": [
                    {
                        "lock_id": "lock-activative-meaning",
                        "statement": "Preserve the original activative meaning and do not depict coercion.",
                        "meaning_hash": "sha256:cd0efc2adbdc779195737f8e2a9eca5ee5cb04570ce26f897f6b1670a161eb94",
                        "scope_paths": ["/visual_semantic_pack"],
                        "enforcement_level": 50,
                    }
                ],
                "parent_lock_set_ref": resource_ref("parent-lock-set-format02-001"),
                "parent_lock_set_hash": "sha256:d686a859766ed5d7db31ab6583710dca952b9d9146b6666bd428f7a789199bf5",
            },
            "derivative_ref": resource_ref("derivative-asset-format02-001"),
            "derivative_wrong_reading_locks": [
                {
                    "lock_id": "lock-activative-meaning",
                    "statement": "Preserve the original activative meaning and do not depict coercion.",
                    "meaning_hash": "sha256:cd0efc2adbdc779195737f8e2a9eca5ee5cb04570ce26f897f6b1670a161eb94",
                    "scope_paths": ["/visual_semantic_pack"],
                    "enforcement_level": 50,
                }
            ],
            "derivation_type": "DETERMINISTIC_RESIZE",
            "derivative_semantics": "NON_SEMANTIC",
            "authoritative_lock_authorization": None,
            "declared_at": T0,
        },
    ),
    contract(
        "compatibility-manifest",
        "Compatibility Manifest",
        "ANY_PRINCIPAL",
        PRINCIPAL_TYPES,
        "PROHIBITED",
        ["compatibility_manifest_published"],
        {
            "manifest_id": IDENTIFIER,
            "package_version": string(pattern=r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$"),
            "protocol_versions": array(VERSION, minItems=1, uniqueItems=True),
            "message_versions": array(
                obj({"message_type": string(pattern=r"^[a-z][a-z0-9-]{2,63}$"), "version": VERSION}),
                minItems=1,
            ),
            "features": array(string(pattern=r"^[a-z][a-z0-9._-]{2,95}$"), minItems=1, uniqueItems=True),
            "required_semantic_domains": array(
                string(enum=list(CONSTITUTIONAL_DOMAINS)), minItems=len(CONSTITUTIONAL_DOMAINS), uniqueItems=True
            ),
            "semantic_capabilities": array(
                obj(
                    {
                        "domain": string(enum=list(CONSTITUTIONAL_DOMAINS)),
                        "support_modes": array(
                            string(enum=["PARSE", "PRESERVE", "ENFORCE", "EVALUATE"]),
                            minItems=1,
                            uniqueItems=True,
                        ),
                        "evaluator_profile_refs": array(ref("ResourceIdentityRef")),
                        "feature_contract_families": array(
                            string(minLength=1, maxLength=128), uniqueItems=True
                        ),
                        "evidence_refs": array(ref("ResourceIdentityRef"), minItems=1),
                    }
                ),
                minItems=len(CONSTITUTIONAL_DOMAINS),
            ),
            "adapter_policy": obj(
                {
                    "lossless_required": boolean(),
                    "prohibited_effects": array(
                        string(
                            enum=[
                                "DROP",
                                "WEAKEN",
                                "SYNTHESIZE",
                                "FLATTEN",
                                "REINTERPRET",
                            ]
                        ),
                        minItems=5,
                        uniqueItems=True,
                    ),
                }
            ),
            "derivative_asset_flows": obj(
                {
                    "supported": boolean(),
                    "lock_inheritance_modes": array(
                        string(enum=["PARSE", "PRESERVE", "ENFORCE"]),
                        minItems=1,
                        uniqueItems=True,
                    ),
                    "evidence_refs": array(ref("ResourceIdentityRef"), minItems=1),
                }
            ),
            "required_signature_algorithms": array(string(enum=["Ed25519"]), minItems=1),
            "status": string(enum=["RELEASE_CANDIDATE", "PUBLISHED", "DEPRECATED", "REVOKED"]),
            "published_at": TIMESTAMP,
        },
        {
            "manifest_id": f"cmf-delegation-contracts-{PACKAGE_VERSION.replace('.', '-').replace('rc.', 'rc-')}",
            "package_version": PACKAGE_VERSION,
            "protocol_versions": [PROTOCOL_VERSION],
            "message_versions": [{"message_type": "visual-asset-demand", "version": "1.1"}],
            "features": [
                "authority.registry",
                "behavioral.semantic-enforcement",
                "lifecycle.transitions",
                "format02.fixtures",
            ],
            "required_semantic_domains": list(CONSTITUTIONAL_DOMAINS),
            "semantic_capabilities": [
                semantic_capability(domain) for domain in CONSTITUTIONAL_DOMAINS
            ],
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
            "derivative_asset_flows": {
                "supported": True,
                "lock_inheritance_modes": ["PRESERVE", "ENFORCE"],
                "evidence_refs": [resource_ref("derivative-lock-inheritance-validator")],
            },
            "required_signature_algorithms": ["Ed25519"],
            "status": "RELEASE_CANDIDATE",
            "published_at": T0,
        },
    ),
    contract(
        "contract-migration",
        "Contract Migration Record",
        "DELEGATION_PROTOCOL",
        PRINCIPAL_TYPES,
        "REQUIRED",
        ["contract_migration_recorded"],
        {
            "migration_id": IDENTIFIER,
            "source_message_type": string(pattern=r"^[a-z][a-z0-9-]{2,63}$"),
            "source_version": VERSION,
            "target_version": VERSION,
            "source_payload_hash": HASH,
            "target_artifacts": array(
                obj(
                    {
                        "message_type": string(pattern=r"^[a-z][a-z0-9-]{2,63}$"),
                        "payload_hash": HASH,
                        "canonical_ref": URI,
                    }
                ),
                minItems=1,
            ),
            "ordered_transformations": array(IDENTIFIER, minItems=1),
            "authority_effect_analysis": array(
                obj(
                    {
                        "target_path": JSON_POINTER,
                        "value_owner": string(enum=PRINCIPAL_TYPES),
                        "effect": string(
                            enum=["PRESERVED", "SPLIT_WITH_EVIDENCE", "OWNER_CLASSIFIED"]
                        ),
                    }
                ),
                minItems=1,
            ),
            "preserved_semantic_paths": array(
                JSON_POINTER, minItems=1, uniqueItems=True
            ),
            "behavioral_enforcement": string(enum=["PASS", "FAIL"]),
            "source_validation": string(enum=["PASS", "FAIL"]),
            "target_validation": string(enum=["PASS", "FAIL"]),
            "equivalence": string(enum=["PASS", "FAIL"]),
            "output_ref": ref("ResourceIdentityRef"),
            "evidence_refs": array(ref("ResourceIdentityRef"), minItems=1),
            "lossless": boolean(),
            "migrated_at": TIMESTAMP,
        },
        {
            "migration_id": "migration-format02-001",
            "source_message_type": "submission-receipt",
            "source_version": "0.1",
            "target_version": PROTOCOL_VERSION,
            "source_payload_hash": hash_value("d"),
            "target_artifacts": [
                {
                    "message_type": "submission-validation-receipt",
                    "payload_hash": hash_value("e"),
                    "canonical_ref": "cmf-contract://migrations/migration-format02-001/validation",
                },
                {
                    "message_type": "admission-receipt",
                    "payload_hash": hash_value("f"),
                    "canonical_ref": "cmf-contract://migrations/migration-format02-001/admission",
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
            "output_ref": resource_ref("migration-output-format02-001"),
            "evidence_refs": [EVIDENCE],
            "lossless": True,
            "migrated_at": T0,
        },
    ),
)


MESSAGE_TYPES = tuple(item.message_type for item in CATALOG)

if len(MESSAGE_TYPES) != len(set(MESSAGE_TYPES)):
    raise RuntimeError("Duplicate message type in canonical catalog")
