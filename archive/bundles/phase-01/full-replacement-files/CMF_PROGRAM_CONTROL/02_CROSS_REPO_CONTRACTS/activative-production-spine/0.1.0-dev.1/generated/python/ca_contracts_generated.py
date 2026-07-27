# Generated from activative-production-spine JSON Schemas.
# Do not edit manually.
from __future__ import annotations

from typing import Literal, NotRequired, TypedDict

class ActorRef(TypedDict):
    actor_id: str
    actor_type: Literal['deterministic_module', 'model_program', 'human']
    product_id: str
    workflow_role: Literal['hunter', 'analyst', 'composer', 'commander', 'evaluator', 'operator']

class ArtifactRef(TypedDict):
    artifact_id: str
    artifact_kind: str
    bytes: int
    media_type: str
    sha256: str
    uri: str

class AuthorityRef(TypedDict):
    authority_id: str
    authority_sha256: str
    authority_state: Literal['current', 'candidate_not_current']
    authority_version: str

class CommandEnvelope(TypedDict):
    actor: ActorRef
    authority: AuthorityRef
    command_id: str
    command_type: str
    correlation_id: str
    idempotency_key: str
    payload_schema: str
    payload_sha256: str
    payload_version: str
    submitted_at_utc: str

class EventEnvelope(TypedDict):
    actor: ActorRef
    aggregate_id: str
    aggregate_version: int
    authority: AuthorityRef
    causation_id: str
    correlation_id: str
    event_id: str
    event_type: str
    occurred_at_utc: str
    payload_schema: str
    payload_sha256: str
    payload_version: str

class ExecutionStackFingerprint(TypedDict):
    canonical_sha256: str
    contract_release_ref: ImmutableRef
    evaluator_ref: None | ImmutableRef
    fingerprint_id: str
    hardware_profile: str
    implementation_ref: ImmutableRef
    model_ref: None | ImmutableRef
    precision: str
    runtime_ref: ImmutableRef
    tool_refs: tuple[ImmutableRef, ...]

class ImmutableRef(TypedDict):
    object_id: str
    sha256: str
    version: str

class ProductHandoffEnvelope(TypedDict):
    authority: AuthorityRef
    consumer_product: str
    created_at_utc: str
    handoff_id: str
    object_ref: ImmutableRef
    object_schema: str
    object_schema_version: str
    producer_product: str
    source_lineage_refs: tuple[ImmutableRef, ...]
    wrong_reading_lock_refs: tuple[ImmutableRef, ...]

class ProductStatusEnvelope(TypedDict):
    authority: AuthorityRef
    certified: bool
    development_authorized: bool
    lifecycle_state: str
    product_id: str
    product_version: str
    production_authorized: bool
    updated_at_utc: str

class ReceiptEnvelope(TypedDict):
    authority: AuthorityRef
    command_ref: ImmutableRef
    evaluator: None | ActorRef
    failure: None | TypedFailure
    outcome: Literal['accepted', 'denied', 'cancelled', 'failed']
    receipt_id: str
    receipt_sha256: str
    recorded_at_utc: str
    result_refs: tuple[ImmutableRef, ...]

class SourceSpanRef(TypedDict):
    end_ms: int
    source_ref: ImmutableRef
    speaker_id: str | None
    start_ms: int
    transcript_sha256: str | None

class TypedFailure(TypedDict):
    code: str
    evidence_refs: tuple[ImmutableRef, ...]
    message: str
    next_action: str
    responsible_product: str
    retry_class: Literal['non_retryable', 'retryable_same_input', 'retryable_after_input', 'human_decision_required']

