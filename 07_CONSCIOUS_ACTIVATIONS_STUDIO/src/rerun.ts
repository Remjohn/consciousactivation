import { canonicalSha256, deterministicId, uniqueSorted } from "./canonical.js";
import type { ImmutableRef } from "./generated/contracts.js";
import type { ChangeRequestProgram, DependencyGraphNode, SelectiveRerunRequest } from "./domain.js";
import { StudioValidationError, validateDependencyGraph, validateImmutableRef } from "./validators.js";

function descendants(start: ReadonlyArray<string>, nodes: ReadonlyArray<DependencyGraphNode>): ReadonlyArray<string> {
  const reverse = new Map<string, string[]>();
  for (const node of nodes) {
    for (const dependency of node.dependency_ids) {
      const list = reverse.get(dependency) ?? [];
      list.push(node.node_id);
      reverse.set(dependency, list);
    }
  }
  const seen = new Set<string>(start);
  const queue = [...start].sort();
  while (queue.length) {
    const current = queue.shift()!;
    for (const child of [...(reverse.get(current) ?? [])].sort()) {
      if (seen.has(child)) continue;
      seen.add(child);
      queue.push(child);
    }
  }
  return [...seen].sort();
}

export function compileSelectiveRerun(args: {
  readonly run_ref: ImmutableRef;
  readonly program: ChangeRequestProgram;
  readonly graph: ReadonlyArray<DependencyGraphNode>;
  readonly evaluation_node_ids: ReadonlyArray<string>;
}): SelectiveRerunRequest {
  validateImmutableRef(args.run_ref, "run_ref");
  validateDependencyGraph(args.graph);
  if (args.program.compilation_status !== "COMPILED") throw new StudioValidationError("PROGRAM_NOT_EXECUTABLE", "selective rerun requires a compiled change program");
  const graphIds = new Set(args.graph.map((node) => node.node_id));
  const changed = uniqueSorted(args.program.exact_operations.map((operation) => operation.target_node_id));
  for (const nodeId of changed) if (!graphIds.has(nodeId)) throw new StudioValidationError("UNKNOWN_CHANGED_NODE", `change targets unknown node ${nodeId}`);
  const invalidated = descendants(changed, args.graph);
  const preserved = [...graphIds].filter((nodeId) => !invalidated.includes(nodeId)).sort();
  const validation = uniqueSorted(args.evaluation_node_ids.filter((nodeId) => invalidated.includes(nodeId)));
  const programRef: ImmutableRef = { object_id: args.program.program_id, version: "1.0.0", sha256: args.program.program_sha256 };
  const payload = {
    run_ref: args.run_ref,
    change_request_program_ref: programRef,
    changed_node_ids: changed,
    invalidated_node_ids: invalidated,
    rerun_node_ids: invalidated,
    preserved_node_ids: preserved,
    validation_node_ids: validation,
    reason: "Studio correction invalidates only the changed nodes and graph descendants.",
  };
  return { rerun_request_id: deterministicId("selective-rerun", payload), ...payload };
}

export function withRerunProjection(program: ChangeRequestProgram, rerun: SelectiveRerunRequest): ChangeRequestProgram {
  const updated = { ...program, invalidated_downstream_nodes: rerun.invalidated_node_ids };
  const withoutHash = { ...updated } as Record<string, unknown>;
  delete withoutHash.program_sha256;
  return { ...updated, program_sha256: canonicalSha256(withoutHash) };
}
