import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { canonicalSha256, compileNaturalLanguageRevision, createHumanResolutionEpisode, DEFAULT_STUDIO_TOOLS, HumanResolutionLedger, ProgrammingMaterialIndex } from "../dist/index.js";
import { actor, artifact, ref } from "./support.mjs";

function episodeFixture(accepted = true) {
  const graphNodes = ["node:render"];
  const context = { tools: DEFAULT_STUDIO_TOOLS, steering_recipes: [], allowed_node_ids: graphNodes, target_layers_by_ref: { "element:title": "COMPOSITION" }, state_version: 1, default_validation_plan: ["eval"], default_invariants: ["source_fidelity"], wrong_reading_locks: ["lock:1"] };
  const request = { request_id: "request:episode", run_ref: ref("run:episode"), target_refs: [ref("element:title")], target_node_ids: ["node:render"], category_id: "static", natural_language_request: "move title left by 5%", current_state_ref: ref("state:before"), evaluation_ref: ref("eval:before"), jit_capsule_ref: ref("jit:episode"), permitted_tool_registry_ref: ref("tools:episode"), operator_actor: actor, expected_state_version: 1 };
  const program = compileNaturalLanguageRevision(request, context);
  return createHumanResolutionEpisode({ workspace_id: "w", project_id: "p", campaign_id: "c", run_ref: request.run_ref, harness_ref: ref("harness:1"), category_id: "static", format_profile_id: "supervisual", resolution_kind: "revision_request", state_before_ref: request.current_state_ref, state_after_ref: ref("state:after"), artifact_before_refs: [artifact("a:before")], request_text: request.natural_language_request, program, selected_or_rejected_candidate_refs: [], exact_changes: [{ target_object: "element:title", operation: "studio.adjust_bbox", before: "x=0.5", after: "x=0.45" }], runtime_and_model_refs: [ref("runtime:deterministic")], retrieved_context_ref: ref("context:1"), wrong_reading_locks: ["lock:1"], result_refs: [ref("a:after")], evaluation_refs: [ref("eval:after")], accepted, human_authority_actor: actor, scope: "run_local", recorded_at_utc: "2026-07-24T00:00:00Z" });
}

test("HumanResolution ledger is append-only, idempotent and hash chained", () => {
  const dir = mkdtempSync(join(tmpdir(), "ca-resolution-"));
  try {
    const ledger = new HumanResolutionLedger(join(dir, "ledger.ndjson"));
    const episode = episodeFixture();
    ledger.append(episode);
    ledger.append(episode);
    assert.equal(ledger.all().length, 1);
    assert.match(ledger.ledgerSha256(), /^[0-9a-f]{64}$/);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test("human resolutions become scoped retrieval and training candidates", () => {
  const episode = episodeFixture();
  const index = new ProgrammingMaterialIndex();
  const record = index.addEpisode(episode);
  assert.equal(record.dispositions.retrieval_memory, "AUTOMATIC");
  assert.equal(record.dispositions.programmed_model_training, "CANDIDATE");
  assert.equal(index.query("move title source fidelity").length, 1);
});

test("rejected resolution becomes a hard-negative candidate", () => {
  const episode = episodeFixture(false);
  assert.equal(episode.programming_material_dispositions.hard_negative, "CANDIDATE");
  const withoutHash = { ...episode }; delete withoutHash.episode_sha256;
  assert.equal(canonicalSha256(withoutHash), episode.episode_sha256);
});
