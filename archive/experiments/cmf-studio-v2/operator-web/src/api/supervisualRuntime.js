import { apiFetch } from "../lib/apiClient";
import { withCommandMeta } from "../lib/idempotency";

const ROOT = "/api/v1/supervisual";

function jsonBody(payload) {
  return JSON.stringify(payload || {});
}

function defaultRef(prefix, targetId) {
  return `${prefix}:${targetId}`;
}

export function listSuperVisualProjects() {
  return apiFetch(`${ROOT}/projects`);
}

export function createSuperVisualProject(payload) {
  return apiFetch(`${ROOT}/projects`, {
    method: "POST",
    body: jsonBody(withCommandMeta(payload, "project.create", payload?.brand_id || "brand")),
  });
}

export function getSuperVisualProject(projectId) {
  return apiFetch(`${ROOT}/projects/${projectId}`);
}

export function updateSuperVisualProject(projectId, payload) {
  return apiFetch(`${ROOT}/projects/${projectId}`, {
    method: "PATCH",
    body: jsonBody(withCommandMeta(payload, "project.update", projectId)),
  });
}

export function createSuperVisualVariant(projectId, payload = {}) {
  return apiFetch(`${ROOT}/projects/${projectId}/variants`, {
    method: "POST",
    body: jsonBody(withCommandMeta(payload, "variant.create", projectId)),
  });
}

export function getSuperVisualVariant(variantId) {
  return apiFetch(`${ROOT}/variants/${variantId}`);
}

export function cloneSuperVisualVariant(variantId, payload = {}) {
  return apiFetch(`${ROOT}/variants/${variantId}/clone`, {
    method: "POST",
    body: jsonBody(withCommandMeta(payload, "variant.clone", variantId)),
  });
}

export function getSuperVisualSnapshot(variantId) {
  return apiFetch(`${ROOT}/variants/${variantId}/snapshot`);
}

export function getSuperVisualEvents(variantId) {
  return apiFetch(`${ROOT}/variants/${variantId}/events`);
}

export function startSuperVisualBuildRun(variantId, payload = {}) {
  return apiFetch(`${ROOT}/variants/${variantId}/build-runs`, {
    method: "POST",
    body: jsonBody(withCommandMeta(payload, "build.start", variantId)),
  });
}

export function getSuperVisualBuildRun(buildRunId) {
  return apiFetch(`${ROOT}/build-runs/${buildRunId}`);
}

export function runSuperVisualStep(buildRunId, stepName, payload = {}) {
  return apiFetch(`${ROOT}/build-runs/${buildRunId}/steps/${stepName}/run`, {
    method: "POST",
    body: jsonBody(withCommandMeta(payload, `step.${stepName}.run`, buildRunId)),
  });
}

export function createSuperVisualCompositionHypotheses(variantId, payload = {}) {
  return apiFetch(`${ROOT}/variants/${variantId}/composition/hypotheses`, {
    method: "POST",
    body: jsonBody(withCommandMeta(payload, "composition.hypotheses", variantId)),
  });
}

export function lockSuperVisualComposition(variantId, payload = {}) {
  const body = {
    ...payload,
    composition_decision_receipt_id:
      payload.composition_decision_receipt_id ||
      payload.composition_hypothesis_id ||
      defaultRef("composition_decision", variantId),
  };
  return apiFetch(`${ROOT}/variants/${variantId}/composition/lock`, {
    method: "POST",
    body: jsonBody(withCommandMeta(body, "composition.lock", variantId)),
  });
}

export function createSuperVisualProviderBlueprints(variantId, payload = {}) {
  const body = {
    ...payload,
    provider_job_blueprint_id:
      payload.provider_job_blueprint_id ||
      defaultRef("provider_blueprint", variantId),
  };
  return apiFetch(`${ROOT}/variants/${variantId}/provider-blueprints`, {
    method: "POST",
    body: jsonBody(withCommandMeta(body, "provider_blueprints.compile", variantId)),
  });
}

export function materializeSuperVisual(variantId, payload = {}) {
  const body = {
    ...payload,
    receipt_id: payload.receipt_id || payload.provider_job_receipt_id || defaultRef("provider_receipt", variantId),
  };
  return apiFetch(`${ROOT}/variants/${variantId}/materialize`, {
    method: "POST",
    body: jsonBody(withCommandMeta(body, "materialize.run", variantId)),
  });
}

export function createSuperVisualRenderContract(variantId, payload = {}) {
  const body = {
    ...payload,
    receipt_id: payload.receipt_id || payload.render_contract_id || defaultRef("render_contract", variantId),
  };
  return apiFetch(`${ROOT}/variants/${variantId}/render-contract`, {
    method: "POST",
    body: jsonBody(withCommandMeta(body, "render_contract.compile", variantId)),
  });
}

export function renderSuperVisualVariant(variantId, payload = {}) {
  const body = {
    ...payload,
    receipt_id: payload.receipt_id || payload.render_receipt_id || defaultRef("render_receipt", variantId),
  };
  return apiFetch(`${ROOT}/variants/${variantId}/render`, {
    method: "POST",
    body: jsonBody(withCommandMeta(body, "render.run", variantId)),
  });
}

export function evaluateSuperVisualVariant(variantId, payload = {}) {
  const body = {
    passed: true,
    ...payload,
    receipt_id: payload.receipt_id || payload.evaluation_receipt_id || defaultRef("eval_receipt", variantId),
  };
  return apiFetch(`${ROOT}/variants/${variantId}/evaluate`, {
    method: "POST",
    body: jsonBody(withCommandMeta(body, "eval.run", variantId)),
  });
}

export function submitSuperVisualRevision(variantId, payload = {}) {
  const body = {
    ...payload,
    revision_note:
      payload.revision_note ||
      payload.operator_feedback ||
      payload.feedback ||
      "Operator requested a SuperVisual revision.",
  };
  return apiFetch(`${ROOT}/variants/${variantId}/revisions`, {
    method: "POST",
    body: jsonBody(withCommandMeta(body, "revision.apply", variantId)),
  });
}

export function listSuperVisualRevisions(variantId) {
  return apiFetch(`${ROOT}/variants/${variantId}/revisions`);
}

export function approveSuperVisualVariant(variantId, payload = {}) {
  const body = {
    ...payload,
    approval_receipt_id: payload.approval_receipt_id || defaultRef("approval_receipt", variantId),
  };
  return apiFetch(`${ROOT}/variants/${variantId}/approve`, {
    method: "POST",
    body: jsonBody(withCommandMeta(body, "variant.approve", variantId)),
  });
}

export function exportSuperVisualVariant(variantId, payload = {}) {
  const body = {
    ...payload,
    export_pack_id: payload.export_pack_id || defaultRef("export_pack", variantId),
  };
  return apiFetch(`${ROOT}/variants/${variantId}/export`, {
    method: "POST",
    body: jsonBody(withCommandMeta(body, "variant.export", variantId)),
  });
}
