const API_BASE = import.meta.env.VITE_CMF_API_BASE_URL || "";

const scopeIds = {
  operatorUserId: "11111111-1111-4111-8111-111111111111",
  organizationId: "22222222-2222-4222-8222-222222222222",
  brandWorkspaceId: "33333333-3333-4333-8333-333333333333",
  activeObjectId: "44444444-4444-4444-8444-444444444444",
};

export async function testOperatorApi() {
  const startedAt = new Date().toISOString();
  try {
    const response = await fetch(`${API_BASE}/api/v1/operator-ui/content-formats`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const body = await response.json();
    return {
      state: "connected",
      checkedAt: startedAt,
      detail: `${body.format_families?.length || 0} format families loaded from CMF API`,
    };
  } catch (error) {
    return {
      state: "offline",
      checkedAt: startedAt,
      detail: error.message,
    };
  }
}

export async function submitOperatorUiCommand({
  commandType,
  commandPayload,
  activeGuest,
  sourceRoute,
  activeObjectType = "brand_workspace",
  activeObjectId = scopeIds.activeObjectId,
  contentAssetCode,
  blockers = [],
}) {
  const createdAt = new Date().toISOString();
  const createRequest = {
    requested_by_user_id: scopeIds.operatorUserId,
    requested_role_key: "operator",
    organization_id: scopeIds.organizationId,
    brand_workspace_id: scopeIds.brandWorkspaceId,
    guest_id: activeGuest?.uuid || null,
    active_object_type: activeObjectType,
    active_object_id: activeObjectId,
    command_type: commandType,
    command_payload: commandPayload,
    source_surface: "pwa",
    source_route: sourceRoute,
    expected_object_version: commandPayload?.expected_object_version || null,
  };

  try {
    const envelope = await postJson("/api/v1/operator-ui/commands", createRequest);
    const receipt = await postJson("/api/v1/operator-ui/commands/submit", {
      envelope,
      blockers,
      content_asset_code: contentAssetCode || commandPayload?.content_asset_code || null,
      object_version_current: true,
    });
    return normalizeBackendReceipt({ envelope, receipt, commandPayload, createdAt });
  } catch (error) {
    return buildOfflineReceipt({
      commandType,
      commandPayload,
      activeGuest,
      sourceRoute,
      activeObjectType,
      contentAssetCode,
      createdAt,
      backendError: error.message,
    });
  }
}

async function postJson(path, payload) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(`${path} failed with HTTP ${response.status}`);
  }
  return response.json();
}

function normalizeBackendReceipt({ envelope, receipt, commandPayload, createdAt }) {
  return {
    receipt_id: receipt.receipt_id,
    command_id: envelope.command_id,
    correlation_id: envelope.correlation_id,
    command_type: envelope.command_type,
    status: receipt.status,
    runtime_mode: "cmf-api",
    created_at: receipt.created_at || createdAt,
    source_surface: envelope.source_surface,
    source_route: envelope.source_route,
    active_object_type: envelope.active_object_type,
    content_asset_code: receipt.content_asset_code || commandPayload?.content_asset_code || null,
    payload: envelope.command_payload,
    validation_results: receipt.validation_results || [],
    backend_error: null,
  };
}

function buildOfflineReceipt({
  commandType,
  commandPayload,
  activeGuest,
  sourceRoute,
  activeObjectType,
  contentAssetCode,
  createdAt,
  backendError,
}) {
  const commandId = randomId("cmd");
  return {
    receipt_id: randomId("ui-local-receipt"),
    command_id: commandId,
    correlation_id: randomId("corr"),
    command_type: commandType,
    status: "accepted",
    runtime_mode: "offline-ui-ledger",
    created_at: createdAt,
    source_surface: "pwa",
    source_route: sourceRoute,
    active_object_type: activeObjectType,
    content_asset_code: contentAssetCode || commandPayload?.content_asset_code || null,
    payload: {
      ...commandPayload,
      brand_workspace_code: activeGuest?.workspace,
      guest_code: activeGuest?.code,
    },
    validation_results: [
      {
        code: "UI_COMMAND_CAPTURED",
        passed: true,
        message: "The operator action was captured as a command receipt in the local UI ledger.",
      },
      {
        code: "BACKEND_API_NOT_CONNECTED",
        passed: false,
        message: "The CMF API did not accept the command in this browser session.",
      },
    ],
    backend_error: backendError,
  };
}

export function randomId(prefix) {
  if (globalThis.crypto?.randomUUID) {
    return `${prefix}-${globalThis.crypto.randomUUID()}`;
  }
  return `${prefix}-${Date.now()}-${Math.round(Math.random() * 100000)}`;
}
