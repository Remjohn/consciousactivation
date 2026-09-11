import { canonicalSha256, deterministicId } from "./canonical";
export function buildAuditExportManifest(input: any): any {
  const core = { ...input, export_id: deterministicId("audit-export", input) };
  return { ...core, export_sha256: canonicalSha256(core), replay_instructions: input.replay_instructions ?? ["Re-open the campaign from the canonical repository", "Recompute the Visual Asset Studio projection from persisted refs", "Verify operator feedback against immutable revision linkage"] };
}
