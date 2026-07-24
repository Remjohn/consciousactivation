import test from "node:test";
import assert from "node:assert/strict";
import { canonicalSha256, compileDirectManipulation, compileNaturalLanguageRevision, compileSelectiveRerun, DEFAULT_STUDIO_TOOLS, validateChangeProgram, withRerunProjection } from "../dist/index.js";
import { actor, ref } from "./support.mjs";

const graph = [
  { node_id: "node:source", dependency_ids: [], lifecycle_state: "SUCCEEDED" },
  { node_id: "node:render", dependency_ids: ["node:source"], lifecycle_state: "SUCCEEDED" },
  { node_id: "node:eval", dependency_ids: ["node:render"], lifecycle_state: "SUCCEEDED" },
  { node_id: "node:review", dependency_ids: ["node:eval"], lifecycle_state: "WAITING_HUMAN" },
];
const context = { tools: DEFAULT_STUDIO_TOOLS, steering_recipes: [], allowed_node_ids: graph.map((node) => node.node_id), target_layers_by_ref: { "element:title": "COMPOSITION" }, state_version: 2, default_validation_plan: ["geometry_check", "independent_eval"], default_invariants: ["source_fidelity"], wrong_reading_locks: ["do_not_flatten_identity"] };
const request = { request_id: "request:1", run_ref: ref("run:1"), target_refs: [ref("element:title")], target_node_ids: ["node:render"], category_id: "static", natural_language_request: "move title left by 5%", current_state_ref: ref("state:1"), evaluation_ref: ref("eval:1"), jit_capsule_ref: ref("jit:1"), permitted_tool_registry_ref: ref("tools:1"), operator_actor: actor, expected_state_version: 2 };

test("natural language and direct manipulation use the same typed operation path", () => {
  const natural = compileNaturalLanguageRevision(request, context);
  const direct = compileDirectManipulation({ delta_id: "delta:1", run_ref: request.run_ref, target_ref: request.target_refs[0], target_node_id: "node:render", manipulation_type: "MOVE_BBOX", arguments: { axis: "x", delta_micros: -50000, mode: "NORMALIZED_MICROS" }, current_state_ref: request.current_state_ref, operator_actor: actor, expected_state_version: 2 }, context);
  assert.equal(natural.exact_operations[0].tool_id, direct.exact_operations[0].tool_id);
  assert.deepEqual(natural.exact_operations[0].arguments, direct.exact_operations[0].arguments);
});

test("unknown request requires clarification instead of guessed editing", () => {
  const result = compileNaturalLanguageRevision({ ...request, request_id: "request:unknown", natural_language_request: "make it better somehow" }, context);
  assert.equal(result.compilation_status, "NEEDS_CLARIFICATION");
  assert.equal(result.exact_operations.length, 0);
});

test("semantic changes route to AIR instead of mutating meaning", () => {
  const result = compileNaturalLanguageRevision({ ...request, request_id: "request:semantic", natural_language_request: "change the Primitive coalition meaning" }, { ...context, target_layers_by_ref: { "element:title": "AIR_SEMANTIC_AUTHORITY" } });
  assert.equal(result.exact_operations[0].tool_id, "studio.request_semantic_revision");
  assert.equal(result.exact_operations[0].target_layer, "AIR_REVISION_REQUEST");
});

test("selective rerun invalidates only descendants", () => {
  const program = compileNaturalLanguageRevision(request, context);
  const rerun = compileSelectiveRerun({ run_ref: request.run_ref, program, graph, evaluation_node_ids: ["node:eval", "node:review"] });
  assert.deepEqual(rerun.invalidated_node_ids, ["node:eval", "node:render", "node:review"]);
  assert.deepEqual(rerun.preserved_node_ids, ["node:source"]);
  const updated = withRerunProjection(program, rerun);
  assert.deepEqual(updated.invalidated_downstream_nodes, rerun.invalidated_node_ids);
});

test("minimality rejects duplicate operations", () => {
  const program = compileNaturalLanguageRevision(request, context);
  const duplicated = { ...program, exact_operations: [program.exact_operations[0], program.exact_operations[0]], program_sha256: canonicalSha256({ duplicate: true }) };
  assert.throws(() => validateChangeProgram(duplicated, context.tools, context.allowed_node_ids), /duplicate operations/);
});
