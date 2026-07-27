import { canonicalSha256 } from "../dist/index.js";

export const ref = (id, seed = id) => ({ object_id: id, version: "1.0.0", sha256: canonicalSha256({ seed }) });
export const actor = { actor_id: "operator:test", actor_type: "human", product_id: "conscious-activations-studio", workflow_role: "operator" };
export const authority = { authority_id: "authority:test", authority_version: "1.0.0", authority_sha256: canonicalSha256({ authority: "test" }), authority_state: "candidate_not_current" };
export const artifact = (id, kind = "test_artifact", uri = `artifacts/${id}.json`) => ({ artifact_id: id, artifact_kind: kind, bytes: 10, media_type: "application/json", sha256: canonicalSha256({ id }), uri });
