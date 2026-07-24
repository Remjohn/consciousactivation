import test from "node:test";
import assert from "node:assert/strict";
import { createCampaignOrder, defaultAutonomyPolicy, launchCampaign, routeHarnessToSurfaces, shouldInterruptOperator, transitionCampaign } from "../dist/index.js";
import { actor, authority, ref } from "./support.mjs";

function orderInput(mode = "REVIEW_BEFORE_SHIP") {
  return {
    workspace_id: "workspace:test", project_id: "project:test", source_kind: "CANONICAL_INTERVIEW_SOURCE_PACKAGE",
    source_ref: ref("source:test"), harness_ref: ref("harness:test"), category_id: "short_form_edited_video",
    format_profile_id: "format07_direct_coaching_a_roll", objective: "Preserve source expression", initial_seed: "A source-backed seed",
    taste_direction: ["identity-first"], output_targets: [
      { output_type: "SOURCE_LED_SHORT", quantity: 1, profile_id: "format07_direct_coaching_a_roll" },
      { output_type: "SUPERVISUAL", quantity: 1, profile_id: "supervisual_reference" },
    ],
    budget_units: 100, deadline_utc: null, autonomy_policy: defaultAutonomyPolicy(mode), operator_actor: actor, authority,
  };
}

test("campaign launch and autonomy transition are deterministic", () => {
  const order = createCampaignOrder(orderInput());
  assert.equal(order.order_id, createCampaignOrder(orderInput()).order_id);
  const campaign = launchCampaign(order);
  const running = transitionCampaign(campaign, "RUNNING");
  assert.equal(running.lifecycle_state, "RUNNING");
  assert.equal(shouldInterruptOperator(running, "final-artifact-review", false), true);
});

test("one shell routes output families to category-native surfaces", () => {
  const order = createCampaignOrder(orderInput());
  const binding = routeHarnessToSurfaces({ harness_ref: order.harness_ref, category_id: order.category_id, output_targets: order.output_targets });
  assert.equal(binding.primary_surface, "VIDEO_PRODUCTION_STUDIO");
  assert(binding.supporting_surfaces.includes("STATIC_COMPOSITION_STUDIO"));
  assert(binding.supporting_surfaces.includes("KNOWLEDGE_MODEL_STUDIO"));
});

test("Format 02 remains deferred", () => {
  const input = { ...orderInput(), category_id: "2d_character_animation", format_profile_id: "format02_minimal_coach_theatre" };
  assert.throws(() => createCampaignOrder(input), /Format 02 is deferred/);
});

test("SHADOW cannot ship", () => {
  const campaign = transitionCampaign(transitionCampaign(launchCampaign(createCampaignOrder(orderInput("SHADOW"))), "RUNNING"), "READY_TO_SHIP");
  assert.throws(() => transitionCampaign(campaign, "SHIPPED"), /SHADOW campaigns cannot/);
});
