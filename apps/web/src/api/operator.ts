/**
 * apps/web/src/api/operator.ts
 * 
 * Strongly typed client SDK for CAE Mandate M46:
 * Programs + Artifacts + Chat Operator Application.
 * 
 * Enforces:
 * - Anti-Stale Concurrency Headers (`If-Match-State-Version`, `If-Match-State-SHA256`)
 * - Lossless Artifact Lineage Graph fetching
 * - Authoritative Execution Trace Projections
 * - Chat Supervision Grammar Dispatching
 */

import { apiFetch } from "./http";

export interface ProgramSummary {
  program_id: string;
  version: string;
  status: string;
  purpose: string;
  lanes: string[];
  manifest_sha256: string;
  package_sha256: string;
  skills_count: number;
  operations_count: number;
}

export interface ProgramListResponse {
  programs: ProgramSummary[];
  total: number;
}

export interface ProgramExecutionSummary {
  aggregate_id: string;
  workspace_id: string;
  program_id: string;
  program_version: string;
  lifecycle: string;
  current_state: string;
  version: number;
  state_hash: string;
  last_receipt_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface ProgramExecutionListResponse {
  executions: ProgramExecutionSummary[];
  total: number;
}

export interface TransitionContract {
  from_state: string;
  to_state: string;
  required_lane: string;
  trigger_operation: string;
  preconditions: string[];
  side_effect_class: string;
}

export interface ProgramExecutionDetail {
  aggregate: ProgramExecutionSummary;
  state_data: Record<string, any>;
  allowable_transitions: string[];
  transition_contracts: Record<string, TransitionContract>;
  active_lane: string | null;
}

export interface LineageNode {
  node_id: string;
  node_type: string;
  label: string;
  sha256: string;
  lane: string;
  receipt_ref: string | null;
  timestamp: string;
  metadata: Record<string, any>;
}

export interface LineageEdge {
  edge_id: string;
  source_node_id: string;
  target_node_id: string;
  transformation_op: string;
  lane: string;
  receipt_ref: string | null;
  metadata: Record<string, any>;
}

export interface ArtifactLineageGraph {
  aggregate_id: string;
  artifact_id: string | null;
  is_lossless: boolean;
  verification_status: string;
  nodes: LineageNode[];
  edges: LineageEdge[];
  root_evidence_ids: string[];
  terminal_artifact_ids: string[];
  verification_digest: string;
}

export interface ExecutionTraceNode {
  step_index: number;
  transition_id: string;
  transition_name: string;
  trigger_operation: string;
  lane: string;
  actor_id: string;
  from_state: string;
  to_state: string;
  committed_version: number;
  receipt_id: string;
  timestamp: string;
  duration_ms: number | null;
  status: string;
  payload_summary: Record<string, any>;
}

export interface ExecutionTraceProjection {
  aggregate_id: string;
  workspace_id: string;
  program_id: string;
  program_version: string;
  lifecycle: string;
  current_state: string;
  version: number;
  state_hash: string;
  last_receipt_id: string | null;
  created_at: string;
  updated_at: string;
  allowable_transitions: string[];
  trace_nodes: ExecutionTraceNode[];
  blockers: string[];
}

export interface ChatCommandResult {
  command: string;
  action_type: string;
  lane: string;
  success: boolean;
  message: string;
  aggregate_id: string | null;
  state_version: number | null;
  state_hash: string | null;
  receipt_id: string | null;
  data: Record<string, any>;
  warnings: string[];
}

// ---------------------------------------------------------------------------
// API Client Functions
// ---------------------------------------------------------------------------

export async function fetchPrograms(status?: string): Promise<ProgramListResponse> {
  const query = status ? `?status=${encodeURIComponent(status)}` : "";
  return apiFetch<ProgramListResponse>(`/api/programs${query}`);
}

export async function fetchProgramDetails(programId: string): Promise<Record<string, any>> {
  return apiFetch<Record<string, any>>(`/api/programs/${encodeURIComponent(programId)}`);
}

export async function fetchExecutions(filters?: {
  workspace_id?: string;
  program_id?: string;
  lifecycle?: string;
  limit?: number;
  offset?: number;
}): Promise<ProgramExecutionListResponse> {
  const params = new URLSearchParams();
  if (filters?.workspace_id) params.set("workspace_id", filters.workspace_id);
  if (filters?.program_id) params.set("program_id", filters.program_id);
  if (filters?.lifecycle) params.set("lifecycle", filters.lifecycle);
  if (filters?.limit) params.set("limit", String(filters.limit));
  if (filters?.offset) params.set("offset", String(filters.offset));
  const qs = params.toString() ? `?${params.toString()}` : "";
  return apiFetch<ProgramExecutionListResponse>(`/api/programs/executions${qs}`);
}

export async function fetchExecutionDetail(aggregateId: string): Promise<ProgramExecutionDetail> {
  return apiFetch<ProgramExecutionDetail>(`/api/programs/executions/${encodeURIComponent(aggregateId)}`);
}

export async function runProgram(params: {
  program_id: string;
  workspace_id: string;
  actor_id?: string;
  initial_data?: Record<string, any>;
  context_claims?: string[];
}): Promise<ProgramExecutionSummary> {
  return apiFetch<ProgramExecutionSummary>("/api/programs/executions", {
    method: "POST",
    body: JSON.stringify(params),
  });
}

export async function pauseExecution(
  aggregateId: string,
  expectedVersion: number,
  expectedSha256: string,
  actorId: string = "operator"
): Promise<ProgramExecutionSummary> {
  return apiFetch<ProgramExecutionSummary>(`/api/programs/executions/${encodeURIComponent(aggregateId)}/pause`, {
    method: "POST",
    headers: {
      "If-Match-State-Version": String(expectedVersion),
      "If-Match-State-SHA256": expectedSha256,
    },
    body: JSON.stringify({
      actor_id: actorId,
      expected_version: expectedVersion,
      expected_state_sha256: expectedSha256,
    }),
  });
}

export async function resumeExecution(
  aggregateId: string,
  expectedVersion: number,
  expectedSha256: string,
  actorId: string = "operator"
): Promise<ProgramExecutionSummary> {
  return apiFetch<ProgramExecutionSummary>(`/api/programs/executions/${encodeURIComponent(aggregateId)}/resume`, {
    method: "POST",
    headers: {
      "If-Match-State-Version": String(expectedVersion),
      "If-Match-State-SHA256": expectedSha256,
    },
    body: JSON.stringify({
      actor_id: actorId,
      expected_version: expectedVersion,
      expected_state_sha256: expectedSha256,
    }),
  });
}

export async function approveExecutionGate(
  aggregateId: string,
  expectedVersion: number,
  expectedSha256: string,
  params?: {
    gate_id?: string;
    decision?: string;
    notes?: string;
    payload?: Record<string, any>;
    actor_id?: string;
  }
): Promise<ProgramExecutionSummary> {
  return apiFetch<ProgramExecutionSummary>(`/api/programs/executions/${encodeURIComponent(aggregateId)}/approve`, {
    method: "POST",
    headers: {
      "If-Match-State-Version": String(expectedVersion),
      "If-Match-State-SHA256": expectedSha256,
    },
    body: JSON.stringify({
      actor_id: params?.actor_id ?? "operator",
      gate_id: params?.gate_id ?? "HUMAN_GATE",
      decision: params?.decision ?? "APPROVE",
      notes: params?.notes,
      payload: params?.payload,
      expected_version: expectedVersion,
      expected_state_sha256: expectedSha256,
    }),
  });
}

export async function rejectExecutionGate(
  aggregateId: string,
  expectedVersion: number,
  expectedSha256: string,
  params: {
    rejection_reason: string;
    disposition_route?: string;
    feedback_notes?: string;
    gate_id?: string;
    actor_id?: string;
  }
): Promise<ProgramExecutionSummary> {
  return apiFetch<ProgramExecutionSummary>(`/api/programs/executions/${encodeURIComponent(aggregateId)}/reject`, {
    method: "POST",
    headers: {
      "If-Match-State-Version": String(expectedVersion),
      "If-Match-State-SHA256": expectedSha256,
    },
    body: JSON.stringify({
      actor_id: params.actor_id ?? "operator",
      gate_id: params.gate_id ?? "HUMAN_GATE",
      rejection_reason: params.rejection_reason,
      disposition_route: params.disposition_route ?? "RETURN_TO_HUNTER",
      feedback_notes: params.feedback_notes,
      expected_version: expectedVersion,
      expected_state_sha256: expectedSha256,
    }),
  });
}

export async function repairExecutionState(
  aggregateId: string,
  expectedVersion: number,
  expectedSha256: string,
  params: {
    repair_action: string;
    repair_payload: Record<string, any>;
    target_state?: string;
    actor_id?: string;
  }
): Promise<ProgramExecutionSummary> {
  return apiFetch<ProgramExecutionSummary>(`/api/programs/executions/${encodeURIComponent(aggregateId)}/repair`, {
    method: "POST",
    headers: {
      "If-Match-State-Version": String(expectedVersion),
      "If-Match-State-SHA256": expectedSha256,
    },
    body: JSON.stringify({
      actor_id: params.actor_id ?? "operator",
      repair_action: params.repair_action,
      repair_payload: params.repair_payload,
      target_state: params.target_state,
      expected_version: expectedVersion,
      expected_state_sha256: expectedSha256,
    }),
  });
}

export async function fetchLineageGraph(aggregateId: string, artifactId?: string): Promise<ArtifactLineageGraph> {
  const qs = artifactId ? `?artifact_id=${encodeURIComponent(artifactId)}` : "";
  return apiFetch<ArtifactLineageGraph>(`/api/programs/executions/${encodeURIComponent(aggregateId)}/lineage${qs}`);
}

export async function fetchExecutionTrace(aggregateId: string): Promise<ExecutionTraceProjection> {
  return apiFetch<ExecutionTraceProjection>(`/api/programs/executions/${encodeURIComponent(aggregateId)}/trace`);
}

export async function sendChatCommand(params: {
  command: string;
  workspace_id: string;
  current_aggregate_id?: string;
  expected_version?: number;
  expected_state_sha256?: string;
  actor_id?: string;
}): Promise<ChatCommandResult> {
  return apiFetch<ChatCommandResult>("/api/programs/operator/chat", {
    method: "POST",
    body: JSON.stringify(params),
  });
}
