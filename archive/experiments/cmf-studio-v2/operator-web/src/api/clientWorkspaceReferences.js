import { apiFetch } from "../lib/apiClient.js";
import {
  countReferences,
  createClientWorkspaceReferenceFixture,
  createFixtureBrandContextVersion,
  createFixtureReference,
  createFixtureWorkspace,
} from "../fixtures/clientWorkspaceReferences.fixture.js";

export const CLIENT_WORKSPACE_FIXTURE_MODE =
  import.meta.env.VITE_CMF_CLIENT_WORKSPACE_FIXTURE_MODE === "true";

function withSourceMode(payload, sourceMode) {
  return {
    ...payload,
    source_mode: sourceMode,
  };
}

export function createInitialClientWorkspaceState(activeGuest) {
  const fixture = createClientWorkspaceReferenceFixture(activeGuest);
  return {
    ...fixture,
    sourceMode: "fixture",
  };
}

export async function createClientWorkspace(payload) {
  if (CLIENT_WORKSPACE_FIXTURE_MODE) {
    return withSourceMode(createFixtureWorkspace(payload), "fixture");
  }
  try {
    return withSourceMode(
      await apiFetch("/api/v1/client-workspaces", {
        method: "POST",
        body: JSON.stringify(payload),
      }),
      "backend",
    );
  } catch {
    return withSourceMode(createFixtureWorkspace(payload), "fixture");
  }
}

export async function listClientWorkspaces() {
  if (CLIENT_WORKSPACE_FIXTURE_MODE) {
    return [];
  }
  try {
    return await apiFetch("/api/v1/client-workspaces");
  } catch {
    return [];
  }
}

export async function getClientWorkspace(clientWorkspaceId) {
  if (CLIENT_WORKSPACE_FIXTURE_MODE) {
    return null;
  }
  try {
    return withSourceMode(await apiFetch(`/api/v1/client-workspaces/${clientWorkspaceId}`), "backend");
  } catch {
    return null;
  }
}

export async function createBrandContextVersion(clientWorkspaceId, payload) {
  if (CLIENT_WORKSPACE_FIXTURE_MODE) {
    return withSourceMode(createFixtureBrandContextVersion(clientWorkspaceId, payload), "fixture");
  }
  try {
    return withSourceMode(
      await apiFetch(`/api/v1/client-workspaces/${clientWorkspaceId}/brand-context-versions`, {
        method: "POST",
        body: JSON.stringify({ ...payload, client_workspace_id: clientWorkspaceId }),
      }),
      "backend",
    );
  } catch {
    return withSourceMode(createFixtureBrandContextVersion(clientWorkspaceId, payload), "fixture");
  }
}

export async function registerReference(clientWorkspaceId, payload) {
  if (CLIENT_WORKSPACE_FIXTURE_MODE) {
    return withSourceMode(createFixtureReference(clientWorkspaceId, payload), "fixture");
  }
  try {
    return withSourceMode(
      await apiFetch(`/api/v1/client-workspaces/${clientWorkspaceId}/references/register`, {
        method: "POST",
        body: JSON.stringify({ ...payload, client_workspace_id: clientWorkspaceId }),
      }),
      "backend",
    );
  } catch {
    return withSourceMode(createFixtureReference(clientWorkspaceId, payload), "fixture");
  }
}

export async function listReferences(clientWorkspaceId, fallbackReferences = []) {
  if (CLIENT_WORKSPACE_FIXTURE_MODE) {
    const counts = countReferences(fallbackReferences);
    return withSourceMode(
      {
        client_workspace_id: clientWorkspaceId,
        references: fallbackReferences,
        ...counts,
      },
      "fixture",
    );
  }
  try {
    return withSourceMode(await apiFetch(`/api/v1/client-workspaces/${clientWorkspaceId}/references`), "backend");
  } catch {
    const counts = countReferences(fallbackReferences);
    return withSourceMode(
      {
        client_workspace_id: clientWorkspaceId,
        references: fallbackReferences,
        ...counts,
      },
      "fixture",
    );
  }
}

export async function updateReference(clientWorkspaceId, artifactRefId, payload, currentReference) {
  if (CLIENT_WORKSPACE_FIXTURE_MODE) {
    return withSourceMode({ ...currentReference, ...payload }, "fixture");
  }
  try {
    return withSourceMode(
      await apiFetch(`/api/v1/client-workspaces/${clientWorkspaceId}/references/${artifactRefId}`, {
        method: "PATCH",
        body: JSON.stringify(payload),
      }),
      "backend",
    );
  } catch {
    return withSourceMode({ ...currentReference, ...payload }, "fixture");
  }
}

