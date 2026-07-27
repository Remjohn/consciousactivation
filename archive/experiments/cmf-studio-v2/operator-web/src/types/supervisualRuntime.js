export const SUPERVISUAL_STATUS_ORDER = [
  "draft",
  "context_ready",
  "preproduction_ready",
  "reference_board_ready",
  "composition_options_ready",
  "composition_locked",
  "materialization_planned",
  "assets_materialized",
  "render_ready",
  "rendered",
  "evaluated",
  "approval_ready",
  "approved",
  "exported",
];

export const SUPERVISUAL_ACTION_LABELS = {
  "build.start": "Start build",
  "context.run": "Run context",
  "preproduction.run": "Run preproduction",
  "reference_board.run": "Build reference board",
  "composition.hypotheses": "Generate compositions",
  "composition.lock": "Lock composition",
  "provider_blueprints.compile": "Compile provider blueprints",
  "materialize.run": "Materialize assets",
  "render_contract.compile": "Compile render",
  "render.run": "Render",
  "eval.run": "Evaluate",
  "revision.apply": "Request revision",
  "variant.approve": "Approve",
  "variant.export": "Export",
};

export const FRAME_PROFILE_OPTIONS = [
  "4:5_CAROUSEL_SLIDE",
  "4:5_FEED_POSTER",
  "1:1_SOFT_ROUNDED_EDITORIAL",
  "1:1_PROOF_CARD",
  "9:16_FULL_VERTICAL",
];

export function isInvalidDeliveryFrameProfile(frameProfile) {
  return String(frameProfile || "").startsWith("16:9");
}
