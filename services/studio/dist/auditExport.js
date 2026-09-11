import { writeFileSync } from "node:fs";
import { canonicalJson, canonicalSha256, deterministicId, uniqueSorted } from "./canonical.js";
import { validateArtifactRef, validateImmutableRef } from "./validators.js";
function sortRefs(refs) {
    return [...refs].sort((a, b) => a.object_id.localeCompare(b.object_id) || a.version.localeCompare(b.version));
}
export function buildAuditExportManifest(input) {
    validateImmutableRef(input.campaign_ref, "campaign_ref");
    for (const ref of [...input.source_refs, ...input.semantic_refs, ...input.run_refs, ...input.evaluation_refs, ...input.command_refs, ...input.receipt_refs, ...input.human_resolution_refs])
        validateImmutableRef(ref);
    for (const artifact of input.artifact_refs)
        validateArtifactRef(artifact);
    const shipDecisionRef = input.ship_decision
        ? { object_id: input.ship_decision.decision_id, version: "1.0.0", sha256: input.ship_decision.decision_sha256 }
        : null;
    const body = {
        campaign_ref: input.campaign_ref,
        source_refs: sortRefs(input.source_refs),
        semantic_refs: sortRefs(input.semantic_refs),
        run_refs: sortRefs(input.run_refs),
        artifact_refs: [...input.artifact_refs].sort((a, b) => a.artifact_id.localeCompare(b.artifact_id)),
        evaluation_refs: sortRefs(input.evaluation_refs),
        command_refs: sortRefs(input.command_refs),
        receipt_refs: sortRefs(input.receipt_refs),
        human_resolution_refs: sortRefs(input.human_resolution_refs),
        ship_decision_ref: shipDecisionRef,
        replay_instructions: uniqueSorted(input.replay_instructions),
    };
    const exportId = deterministicId("audit-export", body);
    const withoutHash = { export_id: exportId, ...body };
    return { ...withoutHash, export_sha256: canonicalSha256(withoutHash) };
}
export function writeAuditExport(path, manifest) {
    const withoutHash = { ...manifest };
    delete withoutHash.export_sha256;
    if (canonicalSha256(withoutHash) !== manifest.export_sha256)
        throw new Error("audit export hash mismatch");
    writeFileSync(path, `${canonicalJson(manifest)}\n`, "utf8");
}
