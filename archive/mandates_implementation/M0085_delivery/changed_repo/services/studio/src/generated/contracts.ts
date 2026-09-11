// Generated from activative-production-spine JSON Schemas.
// Do not edit manually.

export interface ActorRef {
  readonly actor_id: string;
  readonly actor_type: "deterministic_module" | "model_program" | "human";
  readonly product_id: string;
  readonly workflow_role: "hunter" | "analyst" | "composer" | "commander" | "evaluator" | "operator";
}

export interface ArtifactRef {
  readonly artifact_id: string;
  readonly artifact_kind: string;
  readonly bytes: number;
  readonly media_type: string;
  readonly sha256: string;
  readonly uri: string;
}

export interface AuthorityRef {
  readonly authority_id: string;
  readonly authority_sha256: string;
  readonly authority_state: "current" | "candidate_not_current";
  readonly authority_version: string;
}

export interface CommandEnvelope {
  readonly actor: ActorRef;
  readonly authority: AuthorityRef;
  readonly command_id: string;
  readonly command_type: string;
  readonly correlation_id: string;
  readonly idempotency_key: string;
  readonly payload_schema: string;
  readonly payload_sha256: string;
  readonly payload_version: string;
  readonly submitted_at_utc: string;
}

export interface EventEnvelope {
  readonly actor: ActorRef;
  readonly aggregate_id: string;
  readonly aggregate_version: number;
  readonly authority: AuthorityRef;
  readonly causation_id: string;
  readonly correlation_id: string;
  readonly event_id: string;
  readonly event_type: string;
  readonly occurred_at_utc: string;
  readonly payload_schema: string;
  readonly payload_sha256: string;
  readonly payload_version: string;
}

export interface ExecutionStackFingerprint {
  readonly canonical_sha256: string;
  readonly contract_release_ref: ImmutableRef;
  readonly evaluator_ref: null | ImmutableRef;
  readonly fingerprint_id: string;
  readonly hardware_profile: string;
  readonly implementation_ref: ImmutableRef;
  readonly model_ref: null | ImmutableRef;
  readonly precision: string;
  readonly runtime_ref: ImmutableRef;
  readonly tool_refs: ReadonlyArray<ImmutableRef>;
}

export interface ImmutableRef {
  readonly object_id: string;
  readonly sha256: string;
  readonly version: string;
}

export interface ProductHandoffEnvelope {
  readonly authority: AuthorityRef;
  readonly consumer_product: string;
  readonly created_at_utc: string;
  readonly handoff_id: string;
  readonly object_ref: ImmutableRef;
  readonly object_schema: string;
  readonly object_schema_version: string;
  readonly producer_product: string;
  readonly source_lineage_refs: ReadonlyArray<ImmutableRef>;
  readonly wrong_reading_lock_refs: ReadonlyArray<ImmutableRef>;
}

export interface ProductStatusEnvelope {
  readonly authority: AuthorityRef;
  readonly certified: boolean;
  readonly development_authorized: boolean;
  readonly lifecycle_state: string;
  readonly product_id: string;
  readonly product_version: string;
  readonly production_authorized: boolean;
  readonly updated_at_utc: string;
}

export interface ReceiptEnvelope {
  readonly authority: AuthorityRef;
  readonly command_ref: ImmutableRef;
  readonly evaluator: null | ActorRef;
  readonly failure: null | TypedFailure;
  readonly outcome: "accepted" | "denied" | "cancelled" | "failed";
  readonly receipt_id: string;
  readonly receipt_sha256: string;
  readonly recorded_at_utc: string;
  readonly result_refs: ReadonlyArray<ImmutableRef>;
}

export interface SourceSpanRef {
  readonly end_ms: number;
  readonly source_ref: ImmutableRef;
  readonly speaker_id: string | null;
  readonly start_ms: number;
  readonly transcript_sha256: string | null;
}

export interface TypedFailure {
  readonly code: string;
  readonly evidence_refs: ReadonlyArray<ImmutableRef>;
  readonly message: string;
  readonly next_action: string;
  readonly responsible_product: string;
  readonly retry_class: "non_retryable" | "retryable_same_input" | "retryable_after_input" | "human_decision_required";
}

