import { SUPERVISUAL_ACTION_LABELS, SUPERVISUAL_STATUS_ORDER } from "../types/supervisualRuntime";

export const SUPERVISUAL_RUNTIME_ACTION_MAP = {
  start_build_run: "build.start",
  run_context_hydrate: "context_hydrate",
  lock_composition: "composition.lock",
  compile_provider_blueprints: "provider_blueprints.compile",
  compile_render_contract: "render_contract.compile",
  render: "render.run",
  evaluate: "eval.run",
  approve: "variant.approve",
  apply_revision: "revision.apply",
  export: "variant.export",
};

export function normalizeRuntimeAction(action) {
  return SUPERVISUAL_RUNTIME_ACTION_MAP[action] || action;
}

export function buildStatusRail(status) {
  const currentIndex = SUPERVISUAL_STATUS_ORDER.indexOf(status);
  return SUPERVISUAL_STATUS_ORDER.map((item, index) => ({
    id: item,
    label: item.replaceAll("_", " "),
    state:
      currentIndex === -1
        ? "pending"
        : index < currentIndex
          ? "complete"
          : index === currentIndex
            ? "active"
            : "pending",
  }));
}

export function normalizeBlockers(blockers = []) {
  return blockers.map((blocker, index) => ({
    id: blocker.blocker_id || blocker.id || `blocker_${index}`,
    severity: blocker.severity || "blocking",
    message: blocker.message || blocker.reason || String(blocker),
    code: blocker.code || blocker.blocker_code || null,
  }));
}

export function normalizeEvents(events = []) {
  return [...events].sort((a, b) => {
    const left = new Date(a.created_at || 0).getTime();
    const right = new Date(b.created_at || 0).getTime();
    return right - left;
  });
}

export function actionLabel(action) {
  const normalized = normalizeRuntimeAction(action);
  return SUPERVISUAL_ACTION_LABELS[normalized] || String(normalized).replaceAll("_", " ").replaceAll(".", " ");
}

export function buildSuperVisualViewModel({ projectDetail, snapshot, events }) {
  const project = projectDetail?.project || projectDetail || null;
  const currentVariant =
    projectDetail?.current_variant ||
    projectDetail?.variant ||
    projectDetail?.currentVariant ||
    null;
  const latestSnapshot = snapshot || projectDetail?.latest_snapshot || null;
  const status =
    latestSnapshot?.status ||
    currentVariant?.status ||
    project?.status ||
    "draft";

  const displayPayload = latestSnapshot?.display_payload || {};
  const blockers = normalizeBlockers(
    latestSnapshot?.blockers ||
      projectDetail?.blockers ||
      []
  );
  const rawAvailableActions =
    latestSnapshot?.available_actions ||
    projectDetail?.available_actions ||
    [];
  const availableActions = rawAvailableActions.map(normalizeRuntimeAction);

  return {
    project,
    currentVariant,
    latestSnapshot,
    projectTitle: project?.title || "Untitled SuperVisual",
    variantLabel: currentVariant?.variant_label || currentVariant?.label || "Working variant",
    status,
    currentStep: latestSnapshot?.step || status,
    statusRail: buildStatusRail(status),
    previewRef: latestSnapshot?.preview_ref || displayPayload.preview_ref || null,
    displayPayload,
    blockers,
    rawAvailableActions,
    availableActions,
    actions: availableActions.map((action) => ({
      id: action,
      label: actionLabel(action),
    })),
    events: normalizeEvents(events || projectDetail?.events || []),
    lineage: currentVariant?.lineage || projectDetail?.lineage || {},
    canApprove: availableActions.includes("variant.approve") || status === "approval_ready",
    canExport: availableActions.includes("variant.export") || status === "approved",
    canRunStep: availableActions.some((action) => action.includes(".run") || action.includes("step")),
  };
}
