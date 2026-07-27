import { assertPortableUri, assertSha256 } from "./canonical.js";
import type { ActorRef, ArtifactRef, ImmutableRef } from "./generated/contracts.js";
import type { CampaignOrder, ChangeRequestProgram, DependencyGraphNode, DirectManipulationDelta, OperatorRevisionRequest, ToolDescriptor } from "./domain.js";

export class StudioValidationError extends Error {
  readonly code: string;
  readonly context: Readonly<Record<string, string | number | boolean>>;

  constructor(code: string, message: string, context: Readonly<Record<string, string | number | boolean>> = {}) {
    super(message);
    this.name = "StudioValidationError";
    this.code = code;
    this.context = context;
  }
}

export function requireNonEmpty(value: string, label: string): void {
  if (!value.trim()) throw new StudioValidationError("EMPTY_VALUE", `${label} must not be empty`, { label });
}

export function requireSafeInteger(value: number, label: string, minimum = 0): void {
  if (!Number.isSafeInteger(value) || value < minimum) {
    throw new StudioValidationError("INVALID_INTEGER", `${label} must be a safe integer >= ${minimum}`, { label, value });
  }
}

export function validateImmutableRef(ref: ImmutableRef, label = "ref"): void {
  requireNonEmpty(ref.object_id, `${label}.object_id`);
  requireNonEmpty(ref.version, `${label}.version`);
  assertSha256(ref.sha256, `${label}.sha256`);
}

export function validateArtifactRef(ref: ArtifactRef): void {
  requireNonEmpty(ref.artifact_id, "artifact_id");
  requireNonEmpty(ref.artifact_kind, "artifact_kind");
  requireNonEmpty(ref.media_type, "media_type");
  requireSafeInteger(ref.bytes, "bytes", 1);
  assertSha256(ref.sha256);
  assertPortableUri(ref.uri);
}

export function validateActor(actor: ActorRef): void {
  requireNonEmpty(actor.actor_id, "actor_id");
  requireNonEmpty(actor.product_id, "product_id");
}

export function validateCampaignOrder(order: CampaignOrder): void {
  requireNonEmpty(order.workspace_id, "workspace_id");
  requireNonEmpty(order.project_id, "project_id");
  validateImmutableRef(order.source_ref, "source_ref");
  validateImmutableRef(order.harness_ref, "harness_ref");
  requireNonEmpty(order.category_id, "category_id");
  requireNonEmpty(order.objective, "objective");
  requireNonEmpty(order.initial_seed, "initial_seed");
  requireSafeInteger(order.budget_units, "budget_units", 1);
  if (order.output_targets.length === 0) throw new StudioValidationError("OUTPUT_TARGET_REQUIRED", "at least one output target is required");
  for (const target of order.output_targets) requireSafeInteger(target.quantity, "output_target.quantity", 1);
  if (order.category_id === "2d_character_animation" || order.format_profile_id.startsWith("format02_")) {
    throw new StudioValidationError("FORMAT02_DEFERRED", "Format 02 is deferred pending a current validated Atomic Harness");
  }
  validateActor(order.operator_actor);
}

export function validateToolRegistry(tools: ReadonlyArray<ToolDescriptor>): Map<string, ToolDescriptor> {
  const registry = new Map<string, ToolDescriptor>();
  for (const tool of tools) {
    requireNonEmpty(tool.tool_id, "tool_id");
    requireNonEmpty(tool.tool_version, "tool_version");
    if (registry.has(tool.tool_id)) throw new StudioValidationError("DUPLICATE_TOOL", `duplicate tool ${tool.tool_id}`);
    registry.set(tool.tool_id, tool);
  }
  return registry;
}

export function validateOperatorRequest(request: OperatorRevisionRequest): void {
  validateImmutableRef(request.run_ref, "run_ref");
  validateImmutableRef(request.current_state_ref, "current_state_ref");
  validateImmutableRef(request.jit_capsule_ref, "jit_capsule_ref");
  validateImmutableRef(request.permitted_tool_registry_ref, "permitted_tool_registry_ref");
  validateActor(request.operator_actor);
  requireNonEmpty(request.natural_language_request, "natural_language_request");
  requireSafeInteger(request.expected_state_version, "expected_state_version", 1);
  if (request.target_refs.length === 0 || request.target_node_ids.length === 0) {
    throw new StudioValidationError("TARGET_REQUIRED", "revision request requires target refs and target nodes");
  }
}

export function validateDirectDelta(delta: DirectManipulationDelta): void {
  validateImmutableRef(delta.run_ref, "run_ref");
  validateImmutableRef(delta.target_ref, "target_ref");
  validateImmutableRef(delta.current_state_ref, "current_state_ref");
  validateActor(delta.operator_actor);
  requireNonEmpty(delta.target_node_id, "target_node_id");
  requireSafeInteger(delta.expected_state_version, "expected_state_version", 1);
}

export function validateDependencyGraph(nodes: ReadonlyArray<DependencyGraphNode>): void {
  const ids = new Set(nodes.map((node) => node.node_id));
  if (ids.size !== nodes.length) throw new StudioValidationError("DUPLICATE_GRAPH_NODE", "dependency graph node IDs must be unique");
  for (const node of nodes) {
    for (const dependency of node.dependency_ids) {
      if (!ids.has(dependency)) throw new StudioValidationError("UNKNOWN_GRAPH_DEPENDENCY", `${node.node_id} depends on unknown ${dependency}`);
    }
  }
}

const forbiddenStudioLayers = new Set([
  "AIR_SEMANTIC_AUTHORITY",
  "PRIMITIVE_MEANING",
  "PRIMITIVE_COALITION_MEANING",
  "ARCHETYPE_COALITION_MEANING",
  "IDENTITY_DNA_CANONICAL",
  "OBSERVED_HUMAN_REACTION",
]);

export function validateChangeProgram(program: ChangeRequestProgram, tools: ReadonlyArray<ToolDescriptor>, allowedNodeIds: ReadonlyArray<string>): void {
  if (program.compilation_status !== "COMPILED") throw new StudioValidationError("PROGRAM_NOT_COMPILED", "only compiled programs may execute");
  requireSafeInteger(program.expected_state_version, "expected_state_version", 1);
  requireSafeInteger(program.confidence_micros, "confidence_micros", 0);
  if (program.confidence_micros > 1_000_000) throw new StudioValidationError("CONFIDENCE_RANGE", "confidence_micros must be <= 1,000,000");
  if (program.exact_operations.length === 0) throw new StudioValidationError("OPERATION_REQUIRED", "compiled program requires an operation");
  if (program.exact_operations.length > 4) throw new StudioValidationError("PROGRAM_NOT_MINIMAL", "bounded Phase 7 programs may contain at most four operations");
  const registry = validateToolRegistry(tools);
  const allowed = new Set(allowedNodeIds);
  const signatures = new Set<string>();
  for (const operation of program.exact_operations) {
    if (forbiddenStudioLayers.has(operation.target_layer)) {
      throw new StudioValidationError("SEMANTIC_AUTHORITY_VIOLATION", `Studio cannot mutate ${operation.target_layer}`);
    }
    const tool = registry.get(operation.tool_id);
    if (!tool || tool.tool_version !== operation.tool_version) throw new StudioValidationError("TOOL_NOT_ALLOWED", `tool ${operation.tool_id}@${operation.tool_version} is not allowed`);
    if (!tool.allowed_target_layers.includes(operation.target_layer)) throw new StudioValidationError("TOOL_LAYER_DENIED", `tool ${tool.tool_id} cannot target ${operation.target_layer}`);
    if (!allowed.has(operation.target_node_id)) throw new StudioValidationError("NODE_SCOPE_DENIED", `target node ${operation.target_node_id} is outside scope`);
    const keys = Object.keys(operation.arguments).sort();
    for (const key of keys) if (!tool.argument_keys.includes(key)) throw new StudioValidationError("ARGUMENT_DENIED", `argument ${key} is not accepted by ${tool.tool_id}`);
    const signature = `${operation.tool_id}|${operation.target_ref.object_id}|${JSON.stringify(operation.arguments)}`;
    if (signatures.has(signature)) throw new StudioValidationError("DUPLICATE_OPERATION", "duplicate operations violate minimality");
    signatures.add(signature);
  }
}
