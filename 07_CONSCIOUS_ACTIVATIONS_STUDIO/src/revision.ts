import { canonicalSha256, deterministicId, uniqueSorted } from "./canonical.js";
import type { ImmutableRef } from "./generated/contracts.js";
import type {
  ChangeOperation,
  ChangeOperationTemplate,
  ChangeRequestProgram,
  DirectManipulationDelta,
  OperatorRevisionRequest,
  SteeringRecipeBinding,
  ToolDescriptor,
} from "./domain.js";
import {
  StudioValidationError,
  validateChangeProgram,
  validateDirectDelta,
  validateOperatorRequest,
  validateToolRegistry,
} from "./validators.js";

export interface RevisionContext {
  readonly tools: ReadonlyArray<ToolDescriptor>;
  readonly steering_recipes: ReadonlyArray<SteeringRecipeBinding>;
  readonly allowed_node_ids: ReadonlyArray<string>;
  readonly target_layers_by_ref: Readonly<Record<string, string>>;
  readonly state_version: number;
  readonly default_validation_plan: ReadonlyArray<string>;
  readonly default_invariants: ReadonlyArray<string>;
  readonly wrong_reading_locks: ReadonlyArray<string>;
}

export const DEFAULT_STUDIO_TOOLS: ReadonlyArray<ToolDescriptor> = Object.freeze([
  { tool_id: "studio.adjust_bbox", tool_version: "1.0.0", owner_product: "conscious-activations-studio", allowed_target_layers: ["COMPOSITION", "TIMELINE_OVERLAY"], argument_keys: ["axis", "delta_micros", "mode"], reversible: true },
  { tool_id: "studio.resize_bbox", tool_version: "1.0.0", owner_product: "conscious-activations-studio", allowed_target_layers: ["COMPOSITION", "TIMELINE_OVERLAY"], argument_keys: ["scale_delta_micros", "anchor"], reversible: true },
  { tool_id: "studio.trim_segment", tool_version: "1.0.0", owner_product: "conscious-activations-studio", allowed_target_layers: ["VIDEO_EDIT_PROGRAM"], argument_keys: ["edge", "delta_ms", "preserve_word_boundary", "preserve_expression_tail"], reversible: true },
  { tool_id: "studio.reorder_item", tool_version: "1.0.0", owner_product: "conscious-activations-studio", allowed_target_layers: ["VIDEO_EDIT_PROGRAM", "CAROUSEL_SEQUENCE"], argument_keys: ["relation", "anchor_id"], reversible: true },
  { tool_id: "studio.edit_text", tool_version: "1.0.0", owner_product: "conscious-activations-studio", allowed_target_layers: ["COMPOSITION_COPY"], argument_keys: ["text", "transformation_class"], reversible: true },
  { tool_id: "studio.set_parameter", tool_version: "1.0.0", owner_product: "conscious-activations-studio", allowed_target_layers: ["COMPOSITION", "VIDEO_EDIT_PROGRAM", "TIMELINE_OVERLAY", "CAMPAIGN"], argument_keys: ["parameter", "value"], reversible: true },
  { tool_id: "studio.select_candidate", tool_version: "1.0.0", owner_product: "conscious-activations-studio", allowed_target_layers: ["CANDIDATE_PORTFOLIO"], argument_keys: ["candidate_id"], reversible: true },
  { tool_id: "studio.apply_steering_recipe", tool_version: "1.0.0", owner_product: "conscious-activations-studio", allowed_target_layers: ["COMPOSITION", "VIDEO_EDIT_PROGRAM", "TIMELINE_OVERLAY"], argument_keys: ["recipe_id", "operation_index", "payload"], reversible: true },
  { tool_id: "studio.request_semantic_revision", tool_version: "1.0.0", owner_product: "activative-intelligence-runtime", allowed_target_layers: ["AIR_REVISION_REQUEST"], argument_keys: ["request", "reason", "source_ref"], reversible: false },
]);

function targetLayer(request: OperatorRevisionRequest, context: RevisionContext): string {
  const first = request.target_refs[0];
  if (!first) throw new StudioValidationError("TARGET_REQUIRED", "revision request requires a target");
  return context.target_layers_by_ref[first.object_id] ?? "COMPOSITION";
}

function operationFromTemplate(template: ChangeOperationTemplate, request: OperatorRevisionRequest, targetLayerValue: string, index: number): ChangeOperation {
  const target = request.target_refs[0]!;
  return {
    operation_id: deterministicId("change-operation", { request_id: request.request_id, index, template, target }),
    target_ref: target,
    target_node_id: request.target_node_ids[0]!,
    target_layer: template.tool_id === "studio.request_semantic_revision" ? "AIR_REVISION_REQUEST" : targetLayerValue,
    tool_id: template.tool_id,
    tool_version: template.tool_version,
    arguments: template.arguments,
    preconditions: template.preconditions,
    expected_effect: template.expected_effect,
  };
}

function recipeMatch(request: OperatorRevisionRequest, context: RevisionContext, normalized: string): { recipe: SteeringRecipeBinding; operations: ReadonlyArray<ChangeOperation> } | null {
  for (const recipe of context.steering_recipes) {
    if (!recipe.trigger_phrases.some((phrase) => normalized.includes(phrase.toLocaleLowerCase("en-US")))) continue;
    const operations = recipe.operations.map((template, index) => operationFromTemplate({
      ...template,
      tool_id: "studio.apply_steering_recipe",
      tool_version: "1.0.0",
      arguments: {
        recipe_id: recipe.recipe_ref.object_id,
        operation_index: index,
        payload: JSON.stringify(template.arguments),
      },
    }, request, recipe.target_layer, index));
    return { recipe, operations };
  }
  return null;
}

function oneOperation(request: OperatorRevisionRequest, targetLayerValue: string, template: ChangeOperationTemplate): ReadonlyArray<ChangeOperation> {
  return [operationFromTemplate(template, request, targetLayerValue, 0)];
}

function compileKnownLanguage(request: OperatorRevisionRequest, context: RevisionContext): { operations: ReadonlyArray<ChangeOperation>; interpretation: string; confidence: number; escalation: string | null; invariants?: ReadonlyArray<string> } {
  const normalized = request.natural_language_request.trim().toLocaleLowerCase("en-US");
  const layer = targetLayer(request, context);
  const recipe = recipeMatch(request, context, normalized);
  if (recipe) {
    return {
      operations: recipe.operations,
      interpretation: `Apply Steering Recipe ${recipe.recipe.recipe_ref.object_id} to the selected ${recipe.recipe.target_layer} target.`,
      confidence: 960_000,
      escalation: null,
      invariants: recipe.recipe.preserved_properties,
    };
  }

  let match = normalized.match(/^(?:move|shift)\s+.+?\s+(left|right|up|down)\s+by\s+(\d+)\s*(%|px|pixels?)?$/i);
  if (match) {
    const direction = match[1]!;
    const amount = Number(match[2]!);
    const unit = match[3] ?? "%";
    const signed = direction === "left" || direction === "up" ? -amount : amount;
    return {
      operations: oneOperation(request, layer, {
        tool_id: "studio.adjust_bbox", tool_version: "1.0.0",
        arguments: { axis: direction === "left" || direction === "right" ? "x" : "y", delta_micros: unit.startsWith("p") && unit !== "%" ? signed : signed * 10_000, mode: unit.startsWith("p") && unit !== "%" ? "PIXELS" : "NORMALIZED_MICROS" },
        preconditions: ["target_bbox_exists", "collision_check_required"], expected_effect: `Move the selected target ${direction} by ${amount}${unit}.`,
      }),
      interpretation: `Move selected target ${direction} while preserving semantic meaning.`, confidence: 990_000, escalation: null,
    };
  }

  match = normalized.match(/^(?:lower|raise)\s+.+?\s+by\s+(\d+)\s*(%|px|pixels?)?$/i);
  if (match) {
    const direction = normalized.startsWith("lower") ? "down" : "up";
    const amount = Number(match[1]!);
    const unit = match[2] ?? "%";
    const signed = direction === "up" ? -amount : amount;
    return {
      operations: oneOperation(request, layer, {
        tool_id: "studio.adjust_bbox", tool_version: "1.0.0", arguments: { axis: "y", delta_micros: unit.startsWith("p") && unit !== "%" ? signed : signed * 10_000, mode: unit.startsWith("p") && unit !== "%" ? "PIXELS" : "NORMALIZED_MICROS" },
        preconditions: ["target_bbox_exists", "collision_check_required"], expected_effect: `${direction === "down" ? "Lower" : "Raise"} the selected target by ${amount}${unit}.`,
      }), interpretation: `${direction === "down" ? "Lower" : "Raise"} selected target without changing its content.`, confidence: 990_000, escalation: null,
    };
  }

  match = normalized.match(/^(shorten|extend)\s+.+?\s+by\s+(\d+)\s*(ms|milliseconds?)$/i);
  if (match) {
    const action = match[1]!;
    const amount = Number(match[2]!);
    const delta = action === "shorten" ? -amount : amount;
    return {
      operations: oneOperation(request, "VIDEO_EDIT_PROGRAM", {
        tool_id: "studio.trim_segment", tool_version: "1.0.0", arguments: { edge: "END", delta_ms: delta, preserve_word_boundary: true, preserve_expression_tail: true },
        preconditions: ["word_boundary_available", "expression_tail_preserved"], expected_effect: `${action} selected segment by ${amount}ms.`,
      }), interpretation: `${action} the selected source segment at a valid word boundary.`, confidence: 980_000, escalation: null,
    };
  }

  match = normalized.match(/^move\s+.+?\s+(before|after)\s+(.+)$/i);
  if (match) {
    return {
      operations: oneOperation(request, layer === "COMPOSITION" ? "CAROUSEL_SEQUENCE" : layer, {
        tool_id: "studio.reorder_item", tool_version: "1.0.0", arguments: { relation: match[1]!.toUpperCase(), anchor_id: match[2]!.trim() },
        preconditions: ["same_sequence", "source_lineage_preserved"], expected_effect: `Move selected item ${match[1]} ${match[2]}.`,
      }), interpretation: `Reorder the selected item while preserving its source and semantic references.`, confidence: 970_000, escalation: null,
    };
  }

  match = request.natural_language_request.match(/^(?:change|set)\s+(?:the\s+)?text(?:\s+of\s+.+?)?\s+to\s+["“](.+)["”]$/i);
  if (match) {
    return {
      operations: oneOperation(request, "COMPOSITION_COPY", {
        tool_id: "studio.edit_text", tool_version: "1.0.0", arguments: { text: match[1]!, transformation_class: "OPERATOR_AUTHORED_COPY_REVISION" },
        preconditions: ["source_fidelity_recheck", "voice_dna_recheck", "final_script_revision_required_if_semantic"], expected_effect: "Replace selected presentation copy and re-evaluate source fidelity.",
      }), interpretation: "Change selected presentation copy; route semantic changes through AIR when required.", confidence: 900_000, escalation: "AIR_REVIEW_IF_SEMANTIC_MEANING_CHANGES",
    };
  }

  match = normalized.match(/^select\s+(?:candidate\s+)?(.+)$/i);
  if (match) {
    return {
      operations: oneOperation(request, "CANDIDATE_PORTFOLIO", {
        tool_id: "studio.select_candidate", tool_version: "1.0.0", arguments: { candidate_id: match[1]!.trim() },
        preconditions: ["candidate_exists", "candidate_evaluation_available"], expected_effect: `Select candidate ${match[1]!.trim()}.`,
      }), interpretation: "Select the named evaluated candidate without changing its bytes.", confidence: 990_000, escalation: null,
    };
  }

  if (/primitive|archetype|identity dna|psychological role|matrix of edging|final script meaning/.test(normalized)) {
    return {
      operations: oneOperation(request, "AIR_REVISION_REQUEST", {
        tool_id: "studio.request_semantic_revision", tool_version: "1.0.0", arguments: { request: request.natural_language_request, reason: "UPSTREAM_SEMANTIC_AUTHORITY_REQUIRED", source_ref: request.current_state_ref.object_id },
        preconditions: ["air_authority_available", "source_lineage_preserved"], expected_effect: "Request a new AIR-owned semantic version; do not mutate current meaning in Studio.",
      }), interpretation: "Route semantic-authority change to AIR.", confidence: 995_000, escalation: null,
    };
  }

  return { operations: [], interpretation: "The request cannot be grounded to one exact authorized operation.", confidence: 0, escalation: "CLARIFY_TARGET_OPERATION_OR_SELECT_STEERING_RECIPE" };
}

function finishProgram(args: {
  readonly requestRef: ImmutableRef;
  readonly interpretation: string;
  readonly operations: ReadonlyArray<ChangeOperation>;
  readonly status: ChangeRequestProgram["compilation_status"];
  readonly sourceKind: ChangeRequestProgram["source_kind"];
  readonly stateVersion: number;
  readonly context: RevisionContext;
  readonly confidence: number;
  readonly escalation: string | null;
  readonly extraInvariants?: ReadonlyArray<string>;
}): ChangeRequestProgram {
  const body = {
    compilation_status: args.status,
    request_ref: args.requestRef,
    interpretation: args.interpretation,
    target_layer_or_nodes: uniqueSorted(args.operations.flatMap((operation) => [operation.target_layer, operation.target_node_id])),
    exact_operations: args.operations,
    declared_invariants: uniqueSorted([...
      args.context.default_invariants,
      ...args.context.wrong_reading_locks,
      ...(args.extraInvariants ?? []),
      "upstream_semantic_authority_preserved",
      "source_lineage_preserved",
    ]),
    required_transformations: uniqueSorted(args.operations.map((operation) => operation.expected_effect)),
    creative_degrees_of_freedom: args.status === "COMPILED" ? ["bounded_parameter_values_within_declared_operation"] : [],
    invalidated_downstream_nodes: [],
    validation_plan: args.context.default_validation_plan,
    preview_required: args.operations.some((operation) => operation.tool_id !== "studio.select_candidate"),
    confidence_micros: args.confidence,
    escalation: args.escalation,
    source_kind: args.sourceKind,
    expected_state_version: args.stateVersion,
  } as const;
  const programId = deterministicId("change-request-program", body);
  const programWithoutHash = { program_id: programId, ...body };
  return { ...programWithoutHash, program_sha256: canonicalSha256(programWithoutHash) };
}

export function compileNaturalLanguageRevision(request: OperatorRevisionRequest, context: RevisionContext): ChangeRequestProgram {
  validateOperatorRequest(request);
  if (request.expected_state_version !== context.state_version) {
    throw new StudioValidationError("STALE_STATE_VERSION", `expected ${request.expected_state_version}, current ${context.state_version}`);
  }
  validateToolRegistry(context.tools);
  const compiled = compileKnownLanguage(request, context);
  const requestRef: ImmutableRef = { object_id: request.request_id, version: "1.0.0", sha256: canonicalSha256(request) };
  const program = finishProgram({ requestRef, interpretation: compiled.interpretation, operations: compiled.operations, status: compiled.operations.length ? "COMPILED" : "NEEDS_CLARIFICATION", sourceKind: "NATURAL_LANGUAGE", stateVersion: request.expected_state_version, context, confidence: compiled.confidence, escalation: compiled.escalation, extraInvariants: compiled.invariants });
  if (program.compilation_status === "COMPILED") validateChangeProgram(program, context.tools, context.allowed_node_ids);
  return program;
}

export function compileDirectManipulation(delta: DirectManipulationDelta, context: RevisionContext): ChangeRequestProgram {
  validateDirectDelta(delta);
  if (delta.expected_state_version !== context.state_version) throw new StudioValidationError("STALE_STATE_VERSION", "direct manipulation targets a stale state");
  const layer = context.target_layers_by_ref[delta.target_ref.object_id] ?? "COMPOSITION";
  const mappings: Readonly<Record<DirectManipulationDelta["manipulation_type"], { tool_id: string; tool_version: string; layer: string; expected: string }>> = {
    MOVE_BBOX: { tool_id: "studio.adjust_bbox", tool_version: "1.0.0", layer, expected: "Move selected BBOX." },
    RESIZE_BBOX: { tool_id: "studio.resize_bbox", tool_version: "1.0.0", layer, expected: "Resize selected BBOX." },
    TRIM_SEGMENT: { tool_id: "studio.trim_segment", tool_version: "1.0.0", layer: "VIDEO_EDIT_PROGRAM", expected: "Trim selected source segment." },
    REORDER_ITEM: { tool_id: "studio.reorder_item", tool_version: "1.0.0", layer: layer === "COMPOSITION" ? "CAROUSEL_SEQUENCE" : layer, expected: "Reorder selected item." },
    EDIT_TEXT: { tool_id: "studio.edit_text", tool_version: "1.0.0", layer: "COMPOSITION_COPY", expected: "Edit selected presentation text." },
    SET_PARAMETER: { tool_id: "studio.set_parameter", tool_version: "1.0.0", layer, expected: "Set selected parameter." },
    SELECT_CANDIDATE: { tool_id: "studio.select_candidate", tool_version: "1.0.0", layer: "CANDIDATE_PORTFOLIO", expected: "Select evaluated candidate." },
  };
  const mapping = mappings[delta.manipulation_type];
  const operation: ChangeOperation = {
    operation_id: deterministicId("change-operation", { delta_id: delta.delta_id, arguments: delta.arguments }),
    target_ref: delta.target_ref,
    target_node_id: delta.target_node_id,
    target_layer: mapping.layer,
    tool_id: mapping.tool_id,
    tool_version: mapping.tool_version,
    arguments: delta.arguments,
    preconditions: ["current_projection_matches_expected_version", "authority_and_scope_valid"],
    expected_effect: mapping.expected,
  };
  const requestRef: ImmutableRef = { object_id: delta.delta_id, version: "1.0.0", sha256: canonicalSha256(delta) };
  const program = finishProgram({ requestRef, interpretation: `Direct manipulation ${delta.manipulation_type} compiled through the canonical change path.`, operations: [operation], status: "COMPILED", sourceKind: "DIRECT_MANIPULATION", stateVersion: delta.expected_state_version, context, confidence: 1_000_000, escalation: null });
  validateChangeProgram(program, context.tools, context.allowed_node_ids);
  return program;
}
