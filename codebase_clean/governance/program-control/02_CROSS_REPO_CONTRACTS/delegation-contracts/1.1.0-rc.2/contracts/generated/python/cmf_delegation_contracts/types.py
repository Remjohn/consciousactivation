"""Generated top-level TypedDict bindings. Do not edit manually."""

from typing import Any, Literal, TypedDict

SourceKind = Literal['interview_expression', 'public_comment', 'direct_message_reply', 'authored_source', 'live_premise', 'research_synthesis', 'operator_supplied', 'legacy_migrated']

class SourceProvenance(TypedDict):
    source_kind: SourceKind

class DelegationEnvelope(TypedDict):
    protocol_version: str
    message_type: str
    message_version: str
    message_id: str
    correlation_id: str
    causation_id: str | None
    sender: dict[str, Any]
    recipient: dict[str, Any]
    authority: dict[str, Any]
    occurred_at: str
    idempotency_key: str | None
    payload_hash: str
    payload_ref: str
    integrity: dict[str, Any]

class VisualAssetDemand(TypedDict):
    request_id: str
    version: int
    supersedes: dict[str, Any] | None
    content_harness_ref: dict[str, Any]
    category_profile: dict[str, Any]
    format_profile: dict[str, Any]
    asset_classification: dict[str, Any]
    source_provenance: SourceProvenance
    activative_semantic_lineage: dict[str, Any]
    activation_contract: dict[str, Any]
    semantic_intent: dict[str, Any]
    visual_semantic_pack: dict[str, Any]
    visual_narrative_program: dict[str, Any]
    feature_contracts: list[dict[str, Any]]
    somatic_route_request: dict[str, Any]
    activative_function: dict[str, Any]
    wrong_reading_locks: list[str]
    composition_intent: dict[str, Any]
    identity_continuity: dict[str, Any]
    reference_evidence: list[dict[str, Any]]
    delivery: dict[str, Any]
    evaluation_policy: dict[str, Any]
    execution_policy: dict[str, Any]
    notes: str | None

class VisualAssetSubmission(TypedDict):
    submission_id: str
    demand: dict[str, Any]
    submitted_at: str
    requested_priority: str
    callback_resources: list[dict[str, Any]]
    idempotency_key: str

class SubmissionValidationReceipt(TypedDict):
    receipt_id: str
    submission_id: str
    demand: dict[str, Any]
    status: str
    validated_at: str
    findings: list[dict[str, Any]]
    rejection: dict[str, Any] | None
    negotiated_profile: dict[str, Any] | None

class AdmissionReceipt(TypedDict):
    receipt_id: str
    submission_receipt_id: str
    execution: dict[str, Any] | None
    demand: dict[str, Any]
    status: str
    admitted_at: str
    status_resource: dict[str, Any] | None
    rejection: dict[str, Any] | None

class VisualAssetEvent(TypedDict):
    event_id: str
    execution: dict[str, Any]
    event_type: str
    projected_state: str
    occurred_at: str
    progress_basis_points: int
    reason: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]

class DelegationSet(TypedDict):
    set_id: str
    version: int
    member_demands: list[dict[str, Any]]
    dependency_edges: list[dict[str, Any]]
    completion_policy: str
    minimum_completed: int
    failure_policy: str

class BudgetAuthorization(TypedDict):
    authorization_id: str
    scope: str
    demand: dict[str, Any] | None
    delegation_set_ref: dict[str, Any] | None
    maximum_cost: dict[str, Any]
    maximum_attempts: int
    maximum_duration_seconds: int
    valid_from: str
    valid_until: str

class BudgetEscalationRequest(TypedDict):
    request_id: str
    execution: dict[str, Any]
    current_authorization_ref: dict[str, Any]
    requested_additional_cost: dict[str, Any]
    requested_additional_attempts: int
    reason: str
    evidence_refs: list[dict[str, Any]]

class BudgetEscalationResponse(TypedDict):
    response_id: str
    escalation_request_id: str
    decision: str
    replacement_authorization_ref: dict[str, Any] | None
    reason: str
    decided_at: str

class CancellationRequest(TypedDict):
    request_id: str
    demand: dict[str, Any]
    execution_id: str | None
    mode: str
    reason: str
    requested_at: str

class CancellationReceipt(TypedDict):
    receipt_id: str
    cancellation_request_id: str
    demand: dict[str, Any]
    status: str
    effective_at: str | None
    reason: dict[str, Any] | None
    partial_artifact_refs: list[dict[str, Any]]

class ConstraintConflict(TypedDict):
    conflict_id: str
    execution: dict[str, Any]
    conflicting_paths: list[str]
    summary: dict[str, Any]
    evidence_refs: list[dict[str, Any]]
    suggested_resolution: str | None

class AmendmentProposal(TypedDict):
    proposal_id: str
    demand: dict[str, Any]
    execution: dict[str, Any]
    trigger_conflict_id: str | None
    options: list[dict[str, Any]]
    expires_at: str
    proposed_at: str

class AmendmentResponse(TypedDict):
    response_id: str
    proposal_id: str
    selected_option_id: str | None
    decision: str
    authorized_successor_demand: dict[str, Any] | None
    decision_principal: dict[str, Any]
    reason: dict[str, Any] | None
    decided_at: str

class DemandSupersession(TypedDict):
    supersession_id: str
    superseded_demand: dict[str, Any]
    replacement_demand: dict[str, Any]
    invalidation_scope: list[str]
    reason: str
    effective_at: str

class SelectiveInvalidationReceipt(TypedDict):
    receipt_id: str
    supersession_id: str
    invalidated_paths: list[str]
    preserved_evidence_refs: list[dict[str, Any]]
    invalidated_evidence_refs: list[dict[str, Any]]
    recorded_at: str

class AssetResultContract(TypedDict):
    result_id: str
    version: int
    execution: dict[str, Any]
    demand: dict[str, Any]
    artifact_ref: dict[str, Any]
    artifact_media_type: str
    artifact_width_px: int
    artifact_height_px: int
    completion_status: str
    unresolved_roles: list[str]
    provenance_refs: list[dict[str, Any]]
    evaluation_findings: list[dict[str, Any]]
    cost_consumed: dict[str, Any]
    attempts_consumed: int
    declared_at: str

class ResultAcknowledgement(TypedDict):
    acknowledgement_id: str
    result: dict[str, Any]
    demand: dict[str, Any]
    decision: str
    consumption_authorized: bool
    findings: list[dict[str, Any]]
    acknowledged_at: str

class InvalidationNotice(TypedDict):
    notice_id: str
    result: dict[str, Any]
    demand: dict[str, Any]
    scope: list[str]
    reason: str
    replacement_expected: bool
    effective_at: str

class RevocationNotice(TypedDict):
    notice_id: str
    result: dict[str, Any]
    demand: dict[str, Any]
    reason: str
    consumption_must_stop: bool
    effective_at: str

class ReplacementNotice(TypedDict):
    notice_id: str
    replaced_result: dict[str, Any]
    replacement_result: dict[str, Any]
    demand: dict[str, Any]
    reason: str
    effective_at: str

class DelegationFailure(TypedDict):
    failure_id: str
    demand: dict[str, Any] | None
    execution_id: str | None
    detecting_principal: dict[str, Any]
    summary: dict[str, Any]
    evidence_refs: list[dict[str, Any]]
    occurred_at: str

class DelegationAuditReceipt(TypedDict):
    receipt_id: str
    message_id: str
    correlation_id: str
    payload_hash: str
    previous_receipt_hash: str | None
    effective_state: str | None
    authority_verdict: str
    schema_verdict: str
    recorded_at: str

class CompatibilityManifest(TypedDict):
    manifest_id: str
    package_version: str
    protocol_versions: list[str]
    message_versions: list[dict[str, Any]]
    features: list[str]
    required_semantic_domains: list[str]
    semantic_capabilities: list[dict[str, Any]]
    adapter_policy: dict[str, Any]
    required_signature_algorithms: list[str]
    status: str
    published_at: str

class ContractMigration(TypedDict):
    migration_id: str
    source_message_type: str
    source_version: str
    target_version: str
    source_payload_hash: str
    target_artifacts: list[dict[str, Any]]
    ordered_transformations: list[str]
    authority_effect_analysis: list[dict[str, Any]]
    preserved_semantic_paths: list[str]
    behavioral_enforcement: str
    source_validation: str
    target_validation: str
    equivalence: str
    output_ref: dict[str, Any]
    evidence_refs: list[dict[str, Any]]
    lossless: bool
    migrated_at: str

__all__ = ['DelegationEnvelope', 'VisualAssetDemand', 'VisualAssetSubmission', 'SubmissionValidationReceipt', 'AdmissionReceipt', 'VisualAssetEvent', 'DelegationSet', 'BudgetAuthorization', 'BudgetEscalationRequest', 'BudgetEscalationResponse', 'CancellationRequest', 'CancellationReceipt', 'ConstraintConflict', 'AmendmentProposal', 'AmendmentResponse', 'DemandSupersession', 'SelectiveInvalidationReceipt', 'AssetResultContract', 'ResultAcknowledgement', 'InvalidationNotice', 'RevocationNotice', 'ReplacementNotice', 'DelegationFailure', 'DelegationAuditReceipt', 'CompatibilityManifest', 'ContractMigration']
