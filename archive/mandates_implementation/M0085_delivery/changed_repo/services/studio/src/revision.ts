import { canonicalSha256, deterministicId } from "./canonical";
import { StudioValidationError } from "./errors";
import { validateDirectDelta, validateOperatorRequest, validateToolRegistry } from "./validators";
import type { ChangeOperation, ChangeRequestProgram, DirectManipulationDelta, OperatorRevisionRequest, ToolDescriptor } from "./domain";

export const DEFAULT_STUDIO_TOOLS: ReadonlyArray<ToolDescriptor> = Object.freeze([
  { tool_id: "studio.adjust_bbox", tool_version: "1.0.0", owner_product: "conscious-activations-studio", allowed_target_layers: ["COMPOSITION", "TIMELINE_OVERLAY"], argument_keys: ["axis", "delta_micros", "mode"], reversible: true },
  { tool_id: "studio.resize_bbox", tool_version: "1.0.0", owner_product: "conscious-activations-studio", allowed_target_layers: ["COMPOSITION", "TIMELINE_OVERLAY"], argument_keys: ["scale_delta_micros", "anchor"], reversible: true },
  { tool_id: "studio.trim_segment", tool_version: "1.0.0", owner_product: "conscious-activations-studio", allowed_target_layers: ["VIDEO_EDIT_PROGRAM"], argument_keys: ["edge", "delta_ms", "preserve_word_boundary", "preserve_expression_tail"], reversible: true },
  { tool_id: "studio.set_parameter", tool_version: "1.0.0", owner_product: "conscious-activations-studio", allowed_target_layers: ["COMPOSITION", "VIDEO_EDIT_PROGRAM", "TIMELINE_OVERLAY", "CAMPAIGN"], argument_keys: ["parameter", "value"], reversible: true },
  { tool_id: "studio.select_candidate", tool_version: "1.0.0", owner_product: "conscious-activations-studio", allowed_target_layers: ["CANDIDATE_PORTFOLIO"], argument_keys: ["candidate_id"], reversible: true },
  { tool_id: "studio.request_semantic_revision", tool_version: "1.0.0", owner_product: "activative-intelligence-runtime", allowed_target_layers: ["AIR_REVISION_REQUEST"], argument_keys: ["request", "reason", "source_ref"], reversible: false },
]);

function compile(request: OperatorRevisionRequest, sourceKind: ChangeRequestProgram["source_kind"], op: ChangeOperation | null, status: ChangeRequestProgram["compilation_status"] = "COMPILED", interpretation = "Bounded operator visual revision") : ChangeRequestProgram {
  const core = { compilation_status: status, request_id: request.request_id, request_ref: request.current_state_ref, target_layer_or_nodes: request.target_node_ids, exact_operations: op ? [op] : [], declared_invariants: ["upstream_semantic_authority_preserved", "source_lineage_preserved", "no_ui_only_state"], required_transformations: ["validate_source_lineage", "validate_geometry"], creative_degrees_of_freedom: [], invalidated_downstream_nodes: [], validation_plan: ["source_lineage", "bounds", "state_version", "deterministic_replay"], preview_required: true, confidence_micros: status === "COMPILED" ? 1_000_000 : 0, escalation: status === "COMPILED" ? null : "operator_clarification_required", source_kind: sourceKind, expected_state_version: request.expected_state_version };
  const programId = deterministicId("revision-program", core);
  return { ...core, program_id: programId, interpretation, program_sha256: canonicalSha256({ ...core, program_id: programId }) } as ChangeRequestProgram;
}

function match(request: OperatorRevisionRequest): ChangeOperation | null {
  const text = request.natural_language_request.trim().toLocaleLowerCase("en-US");
  const ref = request.target_refs[0]!; const node = request.target_node_ids[0]!;
  const left = text.match(/(?:move|shift).*?(?:left)\s+by\s+(\d+(?:\.\d+)?)%/);
  if (left) return { operation_id: deterministicId("change-operation", { id: request.request_id, action: "left", amount: left[1] }), target_ref: ref, target_node_id: node, target_layer: "COMPOSITION", tool_id: "studio.adjust_bbox", tool_version: "1.0.0", arguments: { axis: "x", delta_micros: -Math.round(Number(left[1]) * 10000), mode: "relative" }, preconditions: ["state_version_matches", "source_lineage_present"], expected_effect: `move ${node} left by ${left[1]}%` };
  const right = text.match(/(?:move|shift).*?(?:right)\s+by\s+(\d+(?:\.\d+)?)%/);
  if (right) return { operation_id: deterministicId("change-operation", { id: request.request_id, action: "right", amount: right[1] }), target_ref: ref, target_node_id: node, target_layer: "COMPOSITION", tool_id: "studio.adjust_bbox", tool_version: "1.0.0", arguments: { axis: "x", delta_micros: Math.round(Number(right[1]) * 10000), mode: "relative" }, preconditions: ["state_version_matches", "source_lineage_present"], expected_effect: `move ${node} right by ${right[1]}%` };
  const trim = text.match(/(?:shorten|trim).*?(\d+)\s*ms/);
  if (trim) return { operation_id: deterministicId("change-operation", { id: request.request_id, action: "trim", amount: trim[1] }), target_ref: ref, target_node_id: node, target_layer: "VIDEO_EDIT_PROGRAM", tool_id: "studio.trim_segment", tool_version: "1.0.0", arguments: { edge: "end", delta_ms: -Number(trim[1]), preserve_word_boundary: true, preserve_expression_tail: true }, preconditions: ["state_version_matches", "timeline_item_editable"], expected_effect: `shorten ${node} by ${trim[1]} ms` };
  return null;
}

export function compileNaturalLanguageRevision(request: OperatorRevisionRequest, context: any): ChangeRequestProgram {
  validateOperatorRequest(request); validateToolRegistry(context.tools ?? DEFAULT_STUDIO_TOOLS);
  if (request.expected_state_version !== Number(context.state_version)) throw new StudioValidationError("STALE_STATE_VERSION", `expected state version ${request.expected_state_version}, current ${context.state_version}`);
  const operation = match(request);
  if (!operation) return compile(request, "NATURAL_LANGUAGE", null, "NEEDS_CLARIFICATION", "No deterministic visual editing grammar matched the request; operator clarification required");
  return compile(request, "NATURAL_LANGUAGE", operation);
}

export function compileDirectManipulation(delta: DirectManipulationDelta, context: any): ChangeRequestProgram {
  validateDirectDelta(delta);
  if (delta.expected_state_version !== Number(context.state_version)) throw new StudioValidationError("STALE_STATE_VERSION", `expected state version ${delta.expected_state_version}, current ${context.state_version}`);
  const toolMap = new Map(DEFAULT_STUDIO_TOOLS.map(t => [t.tool_id, t]));
  const toolByType: Record<string, string> = { MOVE_BBOX: "studio.adjust_bbox", RESIZE_BBOX: "studio.resize_bbox", TRIM_SEGMENT: "studio.trim_segment", EDIT_TEXT: "studio.set_parameter", SET_PARAMETER: "studio.set_parameter", SELECT_CANDIDATE: "studio.select_candidate" };
  const toolId = toolByType[delta.manipulation_type];
  if (!toolId || !toolMap.has(toolId)) throw new StudioValidationError("UNSUPPORTED_MANIPULATION", `unsupported manipulation ${delta.manipulation_type}`);
  const op: ChangeOperation = { operation_id: deterministicId("change-operation", delta), target_ref: delta.target_ref, target_node_id: delta.target_node_id, target_layer: "COMPOSITION", tool_id: toolId, tool_version: toolMap.get(toolId)!.tool_version, arguments: delta.arguments, preconditions: ["state_version_matches", "target_authorized"], expected_effect: `apply ${delta.manipulation_type} deterministically` };
  const request = { request_id: delta.delta_id, run_ref: delta.run_ref, target_refs: [delta.target_ref], target_node_ids: [delta.target_node_id], category_id: "visual_asset_studio", natural_language_request: `Direct ${delta.manipulation_type}`, current_state_ref: delta.current_state_ref, evaluation_ref: null, jit_capsule_ref: delta.current_state_ref, permitted_tool_registry_ref: delta.current_state_ref, operator_actor: delta.operator_actor, expected_state_version: delta.expected_state_version } as OperatorRevisionRequest;
  return compile(request, "DIRECT_MANIPULATION", op, "COMPILED", `Bounded native visual edit: ${delta.manipulation_type}`);
}
