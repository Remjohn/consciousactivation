function slugFromGuest(activeGuest) {
  return String(activeGuest?.workspace || activeGuest?.id || "guest_workspace")
    .toLowerCase()
    .replace(/[^a-z0-9_-]+/g, "_")
    .replace(/^_+|_+$/g, "");
}

export function createClientWorkspaceReferenceFixture(activeGuest = {}) {
  const clientSlug = slugFromGuest(activeGuest);
  const clientWorkspaceId = `fixture_workspace_${clientSlug}`;
  const brandId = `brand_${clientSlug}`;
  const brandContextVersionId = `bcv_${clientSlug}_v1`;
  const workspace = {
    client_workspace_id: clientWorkspaceId,
    client_id: `client_${clientSlug}`,
    client_slug: clientSlug,
    brand_id: brandId,
    brand_context_version_id: brandContextVersionId,
    workspace_relative_path: `client_workspaces/${clientSlug}`,
    status: "active",
    display_name: activeGuest?.name || "Fixture Guest",
    notes: "Offline fixture workspace for operator review.",
    created_at: "2026-07-04T00:00:00+00:00",
    folder_map: {
      root: `client_workspaces/${clientSlug}`,
      brand: `client_workspaces/${clientSlug}/brand`,
      references: `client_workspaces/${clientSlug}/references`,
      libraries: `client_workspaces/${clientSlug}/libraries`,
      avatar_library: `client_workspaces/${clientSlug}/libraries/avatar`,
      real_life_cutouts_library: `client_workspaces/${clientSlug}/libraries/real_life_cutouts`,
      templates_library: `client_workspaces/${clientSlug}/libraries/templates`,
      runs: `client_workspaces/${clientSlug}/runs`,
    },
  };
  const reference = {
    artifact_ref_id: `fixture_reference_${clientSlug}_portrait`,
    artifact_id: "guest_portrait",
    client_workspace_id: clientWorkspaceId,
    client_slug: clientSlug,
    run_id: null,
    category: "reference",
    relative_path: `client_workspaces/${clientSlug}/references/guest-portrait.jpg`,
    uri: `workspace://${clientSlug}/client_workspaces/${clientSlug}/references/guest-portrait.jpg`,
    content_type: "image/jpeg",
    sha256: null,
    size_bytes: null,
    tags: ["portrait", "guest_asset_pack"],
    source_refs: ["fixture:guest_asset_pack"],
    rights_status: "client_provided",
    approval_state: "needs_review",
    notes: "Fixture reference. Register real assets through the backend when available.",
    storage_state: "registered",
    provider_calls_executed: false,
    generation_triggered: false,
    created_at: "2026-07-04T00:00:00+00:00",
  };
  return {
    workspace,
    brandContextVersion: {
      brand_context_version_id: brandContextVersionId,
      brand_id: brandId,
      client_workspace_id: clientWorkspaceId,
      context_label: "Guest Asset Pack intake",
      source_note: "Fixture brand context version.",
      created_at: "2026-07-04T00:00:00+00:00",
    },
    library: {
      client_workspace_id: clientWorkspaceId,
      references: [reference],
      counts_by_approval_state: { needs_review: 1 },
      counts_by_rights_status: { client_provided: 1 },
    },
  };
}

export function createFixtureWorkspace(payload = {}) {
  const fixture = createClientWorkspaceReferenceFixture({
    id: payload.client_slug,
    workspace: payload.client_slug,
    name: payload.display_name,
  });
  return {
    ...fixture.workspace,
    ...payload,
    client_workspace_id: `fixture_workspace_${payload.client_slug || fixture.workspace.client_slug}`,
    workspace_relative_path: `client_workspaces/${payload.client_slug || fixture.workspace.client_slug}`,
  };
}

export function createFixtureBrandContextVersion(clientWorkspaceId, payload = {}) {
  return {
    brand_context_version_id: payload.brand_context_version_id || `bcv_fixture_${Date.now()}`,
    brand_id: payload.brand_id || "brand_fixture",
    client_workspace_id: clientWorkspaceId,
    context_label: payload.context_label || "Fixture brand context",
    source_note: payload.source_note || "Backend unavailable; fixture context captured locally.",
    created_at: new Date().toISOString(),
  };
}

export function createFixtureReference(clientWorkspaceId, payload = {}) {
  const clientSlug = String(payload.client_slug || clientWorkspaceId || "fixture_workspace").replace(/^fixture_workspace_/, "");
  const filename = payload.filename || "registered-reference.jpg";
  return {
    artifact_ref_id: `fixture_reference_${Date.now()}`,
    artifact_id: filename.replace(/\.[^.]+$/, "").replace(/[^a-zA-Z0-9_-]+/g, "_"),
    client_workspace_id: clientWorkspaceId,
    client_slug: clientSlug,
    run_id: payload.run_id || null,
    category: payload.category || "reference",
    relative_path: payload.relative_path || `client_workspaces/${clientSlug}/references/${filename}`,
    uri: `workspace://${clientSlug}/client_workspaces/${clientSlug}/references/${filename}`,
    content_type: payload.content_type || "application/octet-stream",
    sha256: payload.sha256 || null,
    size_bytes: payload.size_bytes || null,
    tags: payload.tags || [],
    source_refs: payload.source_refs || [],
    rights_status: payload.rights_status || "unknown",
    approval_state: payload.approval_state || "pending",
    notes: payload.notes || "Fixture-only reference registration.",
    storage_state: payload.storage_state || "registered",
    provider_calls_executed: false,
    generation_triggered: false,
    created_at: new Date().toISOString(),
  };
}

export function countReferences(references = []) {
  return references.reduce(
    (counts, reference) => {
      counts.counts_by_approval_state[reference.approval_state] =
        (counts.counts_by_approval_state[reference.approval_state] || 0) + 1;
      counts.counts_by_rights_status[reference.rights_status] =
        (counts.counts_by_rights_status[reference.rights_status] || 0) + 1;
      return counts;
    },
    { counts_by_approval_state: {}, counts_by_rights_status: {} },
  );
}

