import { StudioValidationError } from "./errors";
import type { ChangeRequestProgram, DirectManipulationDelta, OperatorRevisionRequest, ToolDescriptor } from "./domain";

export function validateToolRegistry(tools: ReadonlyArray<ToolDescriptor>): void {
  const ids = new Set<string>();
  for (const tool of tools) {
    if (ids.has(tool.tool_id)) throw new StudioValidationError("DUPLICATE_TOOL", `tool registry contains duplicate ${tool.tool_id}`);
    ids.add(tool.tool_id);
  }
}

export function validateOperatorRequest(request: OperatorRevisionRequest): void {
  if (!request.request_id.trim()) throw new StudioValidationError("EMPTY_VALUE", "request_id must not be empty");
  if (!request.natural_language_request.trim()) throw new StudioValidationError("EMPTY_VALUE", "natural_language_request must not be empty");
  if (request.expected_state_version < 1 || !Number.isInteger(request.expected_state_version)) throw new StudioValidationError("INVALID_INTEGER", "expected_state_version must be an integer >= 1");
  if (request.target_refs.length === 0 || request.target_node_ids.length === 0) throw new StudioValidationError("TARGET_REQUIRED", "revision request requires a target");
  if (request.operator_actor.actor_type !== "human" || request.operator_actor.workflow_role !== "operator") throw new StudioValidationError("OPERATOR_REQUIRED", "operator actor must be human/operator");
}

export function validateDirectDelta(delta: DirectManipulationDelta): void {
  if (!delta.delta_id.trim()) throw new StudioValidationError("EMPTY_VALUE", "delta_id must not be empty");
  if (delta.expected_state_version < 1 || !Number.isInteger(delta.expected_state_version)) throw new StudioValidationError("INVALID_INTEGER", "expected_state_version must be an integer >= 1");
  if (delta.operator_actor.actor_type !== "human" || delta.operator_actor.workflow_role !== "operator") throw new StudioValidationError("OPERATOR_REQUIRED", "operator actor must be human/operator");
}

export function validateChangeProgram(program: ChangeRequestProgram): void {
  if (!program.program_id || program.program_sha256.length !== 64) throw new StudioValidationError("INVALID_PROGRAM", "change request program must have a canonical SHA-256");
}
