import test from "node:test";
import assert from "node:assert/strict";
import { buildAuditExportManifest, canonicalSha256, evaluateShipRequest } from "../dist/index.js";
import { actor, artifact, ref } from "./support.mjs";

const campaign = { campaign_id: "campaign:1", order_ref: ref("order:1"), lifecycle_state: "READY_TO_SHIP", autonomy_mode: "REVIEW_BEFORE_SHIP", active_checkpoint_id: null, exception_ids: [], run_refs: [ref("run:1")], artifact_refs: [artifact("artifact:1")], evaluation_refs: [ref("eval:1")], version: 3 };
const baseRequest = { ship_request_id: "ship:1", campaign_ref: { object_id: campaign.campaign_id, version: "3", sha256: canonicalSha256(campaign) }, autonomy_mode: campaign.autonomy_mode, target_channel: "development-export", artifact_refs: campaign.artifact_refs, evaluation_refs: campaign.evaluation_refs, unresolved_exception_ids: [], operator_actor: actor, publication_authority_ref: ref("authority:publish"), publication_policy_ref: ref("policy:publish") };

test("ship requires explicit authority and evaluation evidence", () => {
  const allowed = evaluateShipRequest(baseRequest, campaign);
  assert.equal(allowed.status, "AUTHORIZED");
  const denied = evaluateShipRequest({ ...baseRequest, ship_request_id: "ship:2", publication_authority_ref: null }, campaign);
  assert.equal(denied.status, "DENIED");
  assert(denied.denial_codes.includes("PUBLICATION_AUTHORITY_REQUIRED"));
});

test("SHADOW never authorizes publication", () => {
  const denied = evaluateShipRequest({ ...baseRequest, ship_request_id: "ship:shadow", autonomy_mode: "SHADOW" }, { ...campaign, autonomy_mode: "SHADOW" });
  assert.equal(denied.status, "DENIED");
  assert(denied.denial_codes.includes("SHADOW_PUBLICATION_FORBIDDEN"));
});

test("audit export preserves source-to-ship references and deterministic hash", () => {
  const decision = evaluateShipRequest(baseRequest, campaign);
  const manifest = buildAuditExportManifest({ campaign_ref: baseRequest.campaign_ref, source_refs: [ref("source:1")], semantic_refs: [ref("semantic:1")], run_refs: [ref("run:1")], artifact_refs: campaign.artifact_refs, evaluation_refs: campaign.evaluation_refs, command_refs: [ref("command:1")], receipt_refs: [ref("receipt:1")], human_resolution_refs: [ref("resolution:1")], ship_decision: decision, replay_instructions: ["load source", "replay run"] });
  const withoutHash = { ...manifest }; delete withoutHash.export_sha256;
  assert.equal(canonicalSha256(withoutHash), manifest.export_sha256);
});
