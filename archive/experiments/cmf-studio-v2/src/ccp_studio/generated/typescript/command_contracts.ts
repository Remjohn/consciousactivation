// Generated from CMF STUDIO Python/Pydantic command contracts.
// Read-only consumer artifact for PWA and Telegram clients.

export type ActorType =
  | "human"
  | "pi"
  | "dspy_program"
  | "provider_webhook"
  | "workflow"
  | "recovery_job";

export type CommandStatus =
  | "accepted"
  | "rejected"
  | "succeeded"
  | "failed"
  | "replayed"
  | "quarantined";

export interface ActorContext {
  actor_id: string;
  actor_type: ActorType;
  role_ids: string[];
  tool_name?: string | null;
  session_id?: string | null;
}

export interface CommandEnvelope {
  schema_version: "cmf.command.v1";
  command_id: string;
  command_type: string;
  organization_id: string;
  brand_id: string;
  actor: ActorContext;
  idempotency_key: string;
  correlation_id: string;
  payload: Record<string, unknown>;
  requested_at: string;
  source_surface: string;
}

export interface ValidationResult {
  passed: boolean;
  code: string;
  message: string;
  evidence: Record<string, unknown>;
}

export interface CommandResult {
  command_id: string;
  status: CommandStatus;
  result_payload: Record<string, unknown>;
  validation_results: ValidationResult[];
  domain_event_id?: string | null;
  audit_receipt_id?: string | null;
}

