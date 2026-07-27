import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { canonicalJson, canonicalSha256 } from "./canonical.js";
import { buildAuditExportManifest, writeAuditExport } from "./auditExport.js";
import { createCampaignOrder, defaultAutonomyPolicy, launchCampaign, transitionCampaign } from "./campaign.js";
import { buildControlTowerProjection } from "./controlTower.js";
import type { ArtifactRef, ImmutableRef } from "./generated/contracts.js";
import { renderControlTowerHtml } from "./html.js";
import { createHumanResolutionEpisode, HumanResolutionLedger, ProgrammingMaterialIndex } from "./resolutions.js";
import { compileNaturalLanguageRevision, DEFAULT_STUDIO_TOOLS } from "./revision.js";
import { compileSelectiveRerun, withRerunProjection } from "./rerun.js";
import { evaluateShipRequest } from "./ship.js";
import { routeHarnessToSurfaces } from "./surfaces.js";
import { projectVideoEditProgram } from "./timeline.js";
import type { DependencyGraphNode, OperatorRevisionRequest, RunNodeProjection, RuntimeHealthProjection, SteeringRecipeBinding } from "./domain.js";

function ref(id: string, seed = id): ImmutableRef {
  return { object_id: id, version: "1.0.0", sha256: canonicalSha256({ seed }) };
}

function artifact(id: string, kind: string, uri: string, bytes: number): ArtifactRef {
  return { artifact_id: id, artifact_kind: kind, uri, bytes, media_type: kind.includes("video") ? "video/mp4" : "image/png", sha256: canonicalSha256({ id, uri, bytes }) };
}

export function runPhase7Demo(outputDir: string): Readonly<Record<string, unknown>> {
  mkdirSync(outputDir, { recursive: true });
  const operator = { actor_id: "operator:emilio", actor_type: "human", product_id: "conscious-activations-studio", workflow_role: "operator" } as const;
  const authority = { authority_id: "ca-program-control-v2.1-candidate", authority_version: "2.1.0-candidate", authority_sha256: canonicalSha256({ authority: "v2.1" }), authority_state: "candidate_not_current" } as const;
  const sourceRef = ref("interview-source-package:demo");
  const harnessRef = ref("harness:format07-direct-coaching");
  const order = createCampaignOrder({
    workspace_id: "workspace:demo", project_id: "project:source-expression", source_kind: "CANONICAL_INTERVIEW_SOURCE_PACKAGE", source_ref: sourceRef,
    harness_ref: harnessRef, category_id: "short_form_edited_video", format_profile_id: "format07_direct_coaching_a_roll", objective: "Turn one source expression into a coordinated batch without losing its edge.",
    initial_seed: "The viewer can act before certainty arrives.", taste_direction: ["human-first", "clear negative space", "preserve the reaction tail"],
    output_targets: [
      { output_type: "SOURCE_LED_SHORT", quantity: 1, profile_id: "format07_direct_coaching_a_roll" },
      { output_type: "SUPERVISUAL", quantity: 1, profile_id: "supervisual_reference" },
      { output_type: "ANIMATION_SCENE_PACKAGE", quantity: 1, profile_id: "animation_scene_reference" },
    ],
    budget_units: 1000, deadline_utc: null, autonomy_policy: defaultAutonomyPolicy("REVIEW_BEFORE_SHIP"), operator_actor: operator, authority,
  });
  const binding = routeHarnessToSurfaces({ harness_ref: harnessRef, category_id: order.category_id, output_targets: order.output_targets });
  let campaign = launchCampaign(order);
  campaign = transitionCampaign(campaign, "RUNNING", { run_refs: [ref("pipeline-run:demo")] });
  const videoArtifact = artifact("artifact:source-led-short", "source_led_video", "artifacts/source-led-short.mp4", 227326);
  const supervisualArtifact = artifact("artifact:supervisual", "supervisual", "artifacts/supervisual.png", 3219);
  const animationArtifact = artifact("artifact:animation-scene", "animation_scene", "artifacts/animation-scene.mp4", 3764);
  const evaluationRefs = [ref("evaluation:video"), ref("evaluation:supervisual"), ref("evaluation:animation")];
  campaign = transitionCampaign(campaign, "READY_TO_SHIP", { artifact_refs: [videoArtifact, supervisualArtifact, animationArtifact], evaluation_refs: evaluationRefs });

  const videoProgram = {
    program_id: "video-edit-program:demo", program_sha256: canonicalSha256({ program: "demo" }),
    canvas: { width: 360, height: 640, fps_numerator: 30, fps_denominator: 1, duration_ms: 2200 },
    tracks: [
      { track_id: "track:a-roll", track_type: "VIDEO", role: "PRIMARY_A_ROLL_SPINE", z_index: 0, elements: [
        { element_id: "a-roll:0", kind: "SOURCE_SEGMENT", output_start_ms: 0, output_end_ms: 600, semantic_role: "SOURCE_EXPRESSION", sequence_role: "HOOK", source_registration_ref: ref("source-media-registration:demo"), source_start_ms: 200, source_end_ms: 800 },
        { element_id: "a-roll:1", kind: "SOURCE_SEGMENT", output_start_ms: 600, output_end_ms: 2200, semantic_role: "SOURCE_EXPRESSION", sequence_role: "CLAIM", source_registration_ref: ref("source-media-registration:demo"), source_start_ms: 1000, source_end_ms: 2600 },
      ]},
      { track_id: "track:overlay", track_type: "TEXT", role: "SUPPORTING_OVERLAY", z_index: 10, elements: [
        { element_id: "claim-card", kind: "TEXT", output_start_ms: 700, output_end_ms: 1900, semantic_role: "CLAIM_SUPPORT", sequence_role: "CLAIM" },
      ]},
    ],
  } as const;
  const timeline = projectVideoEditProgram(videoProgram);
  const graph: ReadonlyArray<DependencyGraphNode> = [
    { node_id: "node:source", dependency_ids: [], lifecycle_state: "SUCCEEDED" },
    { node_id: "node:semantic", dependency_ids: ["node:source"], lifecycle_state: "SUCCEEDED" },
    { node_id: "node:video-render", dependency_ids: ["node:semantic"], lifecycle_state: "SUCCEEDED" },
    { node_id: "node:supervisual-render", dependency_ids: ["node:semantic"], lifecycle_state: "SUCCEEDED" },
    { node_id: "node:animation-render", dependency_ids: ["node:semantic"], lifecycle_state: "SUCCEEDED" },
    { node_id: "node:video-eval", dependency_ids: ["node:video-render"], lifecycle_state: "SUCCEEDED" },
    { node_id: "node:static-eval", dependency_ids: ["node:supervisual-render"], lifecycle_state: "SUCCEEDED" },
    { node_id: "node:animation-eval", dependency_ids: ["node:animation-render"], lifecycle_state: "SUCCEEDED" },
    { node_id: "node:final-review", dependency_ids: ["node:video-eval", "node:static-eval", "node:animation-eval"], lifecycle_state: "WAITING_HUMAN" },
  ];
  const runNodes: ReadonlyArray<RunNodeProjection> = graph.map((node) => ({ node_id: node.node_id, node_type: node.node_id.split(":")[1]!, title: node.node_id.replace("node:", "").replace(/-/g, " "), status: node.lifecycle_state as RunNodeProjection["status"], owner_product: node.node_id.includes("semantic") ? "activative-intelligence-runtime" : "atomic-harness-pipeline", dependency_ids: node.dependency_ids, artifact_refs: node.node_id === "node:video-render" ? [videoArtifact] : node.node_id === "node:supervisual-render" ? [supervisualArtifact] : node.node_id === "node:animation-render" ? [animationArtifact] : [], receipt_refs: [], blocker_codes: [] }));
  const health: ReadonlyArray<RuntimeHealthProjection> = [
    { component_id: "ffmpeg-runtime", component_type: "RUNTIME", status: "HEALTHY", capability_ids: ["SOURCE_LED_VIDEO"], budget_units_used: 180, budget_units_limit: 400, evidence_refs: [ref("runtime-receipt:ffmpeg")] },
    { component_id: "skia-reference", component_type: "RUNTIME", status: "DEGRADED", capability_ids: ["STATIC_REFERENCE_RENDER"], budget_units_used: 50, budget_units_limit: 200, evidence_refs: [ref("runtime-receipt:skia-reference")] },
    { component_id: "independent-evaluator", component_type: "EVALUATOR", status: "NOT_CONFIGURED", capability_ids: [], budget_units_used: 0, budget_units_limit: 200, evidence_refs: [] },
  ];
  const initialProjection = buildControlTowerProjection({ campaign, order, studio_binding: binding, source_package_ref: sourceRef, observed_activative_pack_ref: ref("observed-activative-pack:demo"), semantic_production_package_ref: ref("semantic-production-package:demo"), final_script_ref: ref("final-script:demo"), activation_transfer_contract_ref: ref("activation-transfer:demo"), run_nodes: runNodes, artifacts: [videoArtifact, supervisualArtifact, animationArtifact], evaluations: evaluationRefs, knowledge: { skill_refs: [ref("skill:supervisual-composition")], steering_recipe_refs: [ref("steering-recipe:presence-boost-v1")], retrieval_receipt_refs: [ref("retrieval-receipt:demo")], programmed_model_claim_refs: [], exclusion_codes: ["FORMAT02_DEFERRED"] }, runtime_health: health, timeline, exception_packages: [] });

  const request: OperatorRevisionRequest = {
    request_id: "operator-revision:demo", run_ref: ref("pipeline-run:demo"), target_refs: [ref("composition-element:coach")], target_node_ids: ["node:supervisual-render"], category_id: order.category_id,
    natural_language_request: "Make the coach feel more present", current_state_ref: ref(initialProjection.projection_id, initialProjection.projection_sha256), evaluation_ref: ref("evaluation:supervisual"), jit_capsule_ref: ref("jit-capsule:revision"), permitted_tool_registry_ref: ref("tool-registry:studio-v1"), operator_actor: operator, expected_state_version: campaign.version,
  };
  const recipes: ReadonlyArray<SteeringRecipeBinding> = [{ recipe_ref: ref("steering-recipe:presence-boost-v1"), trigger_phrases: ["make the coach feel more present", "increase coach presence"], target_layer: "COMPOSITION", preserved_properties: ["source_fidelity", "identity_anchor", "negative_space_for_claim"], operations: [
    { tool_id: "studio.resize_bbox", tool_version: "1.0.0", arguments: { scale_delta_micros: 50000, anchor: "FACE_CENTER" }, preconditions: ["face_bbox_available", "negative_space_preserved"], expected_effect: "Increase coach scale by five percent." },
    { tool_id: "studio.set_parameter", tool_version: "1.0.0", arguments: { parameter: "background_salience_delta_micros", value: -40000 }, preconditions: ["background_layer_available"], expected_effect: "Reduce background competition without altering source identity." },
  ] }];
  const context = { tools: DEFAULT_STUDIO_TOOLS, steering_recipes: recipes, allowed_node_ids: graph.map((node) => node.node_id), target_layers_by_ref: { "composition-element:coach": "COMPOSITION" }, state_version: campaign.version, default_validation_plan: ["geometry_check", "negative_space_check", "source_fidelity_check", "independent_static_evaluation"], default_invariants: ["final_script_meaning_unchanged", "source_lineage_unchanged"], wrong_reading_locks: ["do_not_replace_source_expression", "do_not_flatten_identity"] } as const;
  const compiled = compileNaturalLanguageRevision(request, context);
  const rerun = compileSelectiveRerun({ run_ref: request.run_ref, program: compiled, graph, evaluation_node_ids: ["node:static-eval", "node:final-review"] });
  const program = withRerunProjection(compiled, rerun);
  const beforeRef = ref(initialProjection.projection_id, initialProjection.projection_sha256);
  const afterRef = ref("control-tower-projection:after-revision");
  const episode = createHumanResolutionEpisode({ workspace_id: order.workspace_id, project_id: order.project_id, campaign_id: campaign.campaign_id, run_ref: request.run_ref, harness_ref: harnessRef, category_id: order.category_id, format_profile_id: order.format_profile_id, resolution_kind: "revision_request", state_before_ref: beforeRef, state_after_ref: afterRef, artifact_before_refs: [supervisualArtifact], request_text: request.natural_language_request, program, selected_or_rejected_candidate_refs: [], exact_changes: program.exact_operations.map((operation) => ({ target_object: operation.target_ref.object_id, operation: operation.tool_id, before: "current_version", after: canonicalJson(operation.arguments) })), runtime_and_model_refs: [ref("runtime:studio-deterministic-compiler")], retrieved_context_ref: ref("retrieval-receipt:demo"), wrong_reading_locks: context.wrong_reading_locks, result_refs: [ref("artifact:supervisual-revised")], evaluation_refs: [ref("evaluation:supervisual-revised")], accepted: true, human_authority_actor: operator, scope: "run_local", recorded_at_utc: "2026-07-24T00:00:00Z" });
  const ledger = new HumanResolutionLedger(join(outputDir, "human-resolution-ledger.ndjson"));
  ledger.append(episode);
  const index = new ProgrammingMaterialIndex();
  const programmingMaterial = index.addEpisode(episode);
  const shipRequest = { ship_request_id: "ship-request:demo", campaign_ref: { object_id: campaign.campaign_id, version: String(campaign.version), sha256: canonicalSha256(campaign) }, autonomy_mode: campaign.autonomy_mode, target_channel: "development-export", artifact_refs: [videoArtifact, supervisualArtifact, animationArtifact], evaluation_refs: evaluationRefs, unresolved_exception_ids: [], operator_actor: operator, publication_authority_ref: ref("publication-authority:development"), publication_policy_ref: ref("publication-policy:review-before-ship") } as const;
  const shipDecision = evaluateShipRequest(shipRequest, campaign);
  const audit = buildAuditExportManifest({ campaign_ref: shipRequest.campaign_ref, source_refs: [sourceRef], semantic_refs: [ref("semantic-production-package:demo"), ref("final-script:demo"), ref("activation-transfer:demo")], run_refs: [request.run_ref], artifact_refs: shipRequest.artifact_refs, evaluation_refs: evaluationRefs, command_refs: [{ object_id: program.program_id, version: "1.0.0", sha256: program.program_sha256 }], receipt_refs: [ref("selective-rerun-receipt:demo")], human_resolution_refs: [{ object_id: episode.episode_id, version: "1.0.0", sha256: episode.episode_sha256 }], ship_decision: shipDecision, replay_instructions: ["load source package", "load approved semantic package", "load VideoEditProgram", "apply ChangeRequestProgram", "execute selective rerun", "re-evaluate changed descendants"] });

  writeFileSync(join(outputDir, "control-tower.json"), `${canonicalJson(initialProjection)}\n`, "utf8");
  writeFileSync(join(outputDir, "studio-control-tower.html"), renderControlTowerHtml(initialProjection), "utf8");
  writeFileSync(join(outputDir, "change-request-program.json"), `${canonicalJson(program)}\n`, "utf8");
  writeFileSync(join(outputDir, "selective-rerun-request.json"), `${canonicalJson(rerun)}\n`, "utf8");
  writeFileSync(join(outputDir, "human-resolution-episode.json"), `${canonicalJson(episode)}\n`, "utf8");
  writeFileSync(join(outputDir, "programming-material-record.json"), `${canonicalJson(programmingMaterial)}\n`, "utf8");
  writeFileSync(join(outputDir, "ship-decision.json"), `${canonicalJson(shipDecision)}\n`, "utf8");
  writeAuditExport(join(outputDir, "audit-export.json"), audit);
  return {
    campaign_id: campaign.campaign_id,
    projection_id: initialProjection.projection_id,
    change_request_program_id: program.program_id,
    invalidated_nodes: rerun.invalidated_node_ids,
    preserved_nodes: rerun.preserved_node_ids,
    human_resolution_episode_id: episode.episode_id,
    programming_material_record_id: programmingMaterial.record_id,
    ship_decision: shipDecision.status,
    audit_export_id: audit.export_id,
    output_files: ["control-tower.json", "studio-control-tower.html", "change-request-program.json", "selective-rerun-request.json", "human-resolution-episode.json", "human-resolution-ledger.ndjson", "programming-material-record.json", "ship-decision.json", "audit-export.json"],
    claim_ceiling: "PHASE_07_STUDIO_SUPERVISION_DEVELOPMENT_EVIDENCE",
  };
}
