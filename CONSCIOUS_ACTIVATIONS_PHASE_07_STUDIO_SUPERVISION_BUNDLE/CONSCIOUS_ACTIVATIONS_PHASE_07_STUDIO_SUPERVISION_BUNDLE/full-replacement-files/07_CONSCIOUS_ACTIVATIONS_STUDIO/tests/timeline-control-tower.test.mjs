import test from "node:test";
import assert from "node:assert/strict";
import { buildControlTowerProjection, canonicalSha256, createCampaignOrder, defaultAutonomyPolicy, launchCampaign, projectVideoEditProgram, routeHarnessToSurfaces } from "../dist/index.js";
import { actor, artifact, authority, ref } from "./support.mjs";

function fixture() {
  const order = createCampaignOrder({ workspace_id: "w", project_id: "p", source_kind: "CANONICAL_INTERVIEW_SOURCE_PACKAGE", source_ref: ref("source"), harness_ref: ref("harness"), category_id: "short_form_edited_video", format_profile_id: "format07_direct_coaching_a_roll", objective: "Objective", initial_seed: "Seed", taste_direction: ["edge"], output_targets: [{ output_type: "SOURCE_LED_SHORT", quantity: 1, profile_id: "format07_direct_coaching_a_roll" }], budget_units: 50, deadline_utc: null, autonomy_policy: defaultAutonomyPolicy("AUTOPILOT"), operator_actor: actor, authority });
  const campaign = launchCampaign(order);
  const timeline = projectVideoEditProgram({ program_id: "program:test", program_sha256: canonicalSha256({ p: 1 }), canvas: { width: 1080, height: 1920, fps_numerator: 30, fps_denominator: 1, duration_ms: 2000 }, tracks: [{ track_id: "track:a", track_type: "VIDEO", role: "PRIMARY_A_ROLL_SPINE", z_index: 0, elements: [{ element_id: "clip:1", kind: "SOURCE_SEGMENT", output_start_ms: 0, output_end_ms: 2000, semantic_role: "SOURCE_EXPRESSION", sequence_role: "CLAIM", source_registration_ref: ref("media:1"), source_start_ms: 100, source_end_ms: 2100 }] }] });
  const binding = routeHarnessToSurfaces({ harness_ref: order.harness_ref, category_id: order.category_id, output_targets: order.output_targets });
  const projection = buildControlTowerProjection({ campaign, order, studio_binding: binding, source_package_ref: order.source_ref, observed_activative_pack_ref: null, semantic_production_package_ref: null, final_script_ref: null, activation_transfer_contract_ref: null, run_nodes: [{ node_id: "node:source", node_type: "source", title: "source", status: "SUCCEEDED", owner_product: "interview-expression", dependency_ids: [], artifact_refs: [], receipt_refs: [], blocker_codes: [] }], artifacts: [artifact("artifact:1")], evaluations: [], knowledge: { skill_refs: [], steering_recipe_refs: [], retrieval_receipt_refs: [], programmed_model_claim_refs: [], exclusion_codes: [] }, runtime_health: [], timeline, exception_packages: [] });
  return { timeline, projection };
}

test("timeline is a read-only projection of VideoEditProgram", () => {
  const { timeline } = fixture();
  assert.equal(timeline.state, "READ_ONLY_CANONICAL_PROGRAM_PROJECTION");
  assert.equal(timeline.duration_frames, 60);
  assert.equal(timeline.items[0].start_frame, 0);
  assert.equal(timeline.items[0].end_frame, 60);
});

test("control tower projection is deterministic and exposes live actions", () => {
  const a = fixture().projection;
  const b = fixture().projection;
  assert.equal(a.projection_id, b.projection_id);
  assert.equal(a.projection_sha256, b.projection_sha256);
  assert(a.available_actions.includes("OPEN_TIMELINE"));
});

test("timeline rejects absence of source-led A-roll spine", () => {
  assert.throws(() => projectVideoEditProgram({ program_id: "program:bad", program_sha256: canonicalSha256({ bad: true }), canvas: { width: 10, height: 10, fps_numerator: 30, fps_denominator: 1, duration_ms: 10 }, tracks: [] }), /talking-head spine/);
});
