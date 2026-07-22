import { useEffect, useMemo, useState } from "react";
import {
  createBrandContextVersion,
  createClientWorkspace,
  createInitialClientWorkspaceState,
  listReferences,
  registerReference,
  updateReference,
} from "../../api/clientWorkspaceReferences.js";

const rightsOptions = [
  "unknown",
  "owned",
  "licensed",
  "client_provided",
  "public_domain",
  "fair_use_review",
  "restricted",
  "rejected",
];

const approvalOptions = ["pending", "needs_review", "approved", "rejected", "quarantined"];

function splitTokens(value) {
  return String(value || "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function slugFromGuest(activeGuest) {
  return String(activeGuest?.workspace || activeGuest?.id || "guest_workspace")
    .toLowerCase()
    .replace(/[^a-z0-9_-]+/g, "_")
    .replace(/^_+|_+$/g, "");
}

function summarizeCounts(counts = {}) {
  const entries = Object.entries(counts);
  if (!entries.length) return "none";
  return entries.map(([key, value]) => `${key}: ${value}`).join(" / ");
}

export function ClientWorkspaceReferencePanel({ activeGuest }) {
  const initialState = useMemo(() => createInitialClientWorkspaceState(activeGuest), [activeGuest?.id]);
  const [workspace, setWorkspace] = useState(initialState.workspace);
  const [brandContextVersion, setBrandContextVersion] = useState(initialState.brandContextVersion);
  const [library, setLibrary] = useState(initialState.library);
  const [sourceMode, setSourceMode] = useState(initialState.sourceMode);
  const [message, setMessage] = useState("Fixture fallback is available if the backend is offline.");
  const [busy, setBusy] = useState(false);

  const [workspaceForm, setWorkspaceForm] = useState(() => ({
    client_id: `client_${slugFromGuest(activeGuest)}`,
    client_slug: slugFromGuest(activeGuest),
    brand_id: `brand_${slugFromGuest(activeGuest)}`,
    brand_context_version_id: `bcv_${slugFromGuest(activeGuest)}_v1`,
    display_name: activeGuest?.name || "",
    notes: "Operator-created workspace for Guest Asset Pack inputs.",
  }));
  const [brandForm, setBrandForm] = useState(() => ({
    brand_context_version_id: `bcv_${slugFromGuest(activeGuest)}_v2`,
    context_label: "Guest Asset Pack intake",
    source_note: "Brand context version registered by operator.",
  }));
  const [referenceForm, setReferenceForm] = useState(() => ({
    filename: "guest-reference.jpg",
    content_type: "image/jpeg",
    category: "reference",
    tags: "guest_asset_pack, source_truth",
    source_refs: "operator:intake",
    rights_status: "client_provided",
    approval_state: "pending",
    sha256: "",
    size_bytes: "",
    notes: "Registered metadata only; binary upload is deferred.",
  }));

  useEffect(() => {
    const next = createInitialClientWorkspaceState(activeGuest);
    const slug = slugFromGuest(activeGuest);
    setWorkspace(next.workspace);
    setBrandContextVersion(next.brandContextVersion);
    setLibrary(next.library);
    setSourceMode(next.sourceMode);
    setMessage("Fixture fallback is available if the backend is offline.");
    setWorkspaceForm({
      client_id: `client_${slug}`,
      client_slug: slug,
      brand_id: `brand_${slug}`,
      brand_context_version_id: `bcv_${slug}_v1`,
      display_name: activeGuest?.name || "",
      notes: "Operator-created workspace for Guest Asset Pack inputs.",
    });
    setBrandForm({
      brand_context_version_id: `bcv_${slug}_v2`,
      context_label: "Guest Asset Pack intake",
      source_note: "Brand context version registered by operator.",
    });
  }, [activeGuest?.id]);

  const readyForGeneration =
    library.references.some((reference) => reference.approval_state === "approved") &&
    library.references.every((reference) => !["restricted", "rejected"].includes(reference.rights_status));

  async function handleCreateWorkspace(event) {
    event.preventDefault();
    setBusy(true);
    const created = await createClientWorkspace(workspaceForm);
    setWorkspace(created);
    setSourceMode(created.source_mode || "backend");
    setMessage(`Workspace ${created.client_slug} registered from ${created.source_mode || "backend"}.`);
    setBusy(false);
  }

  async function handleCreateBrandContext(event) {
    event.preventDefault();
    setBusy(true);
    const created = await createBrandContextVersion(workspace.client_workspace_id, {
      ...brandForm,
      brand_id: workspace.brand_id,
    });
    setBrandContextVersion(created);
    setSourceMode(created.source_mode || sourceMode);
    setMessage(`Brand Context Version ${created.brand_context_version_id} captured.`);
    setBusy(false);
  }

  async function handleRegisterReference(event) {
    event.preventDefault();
    setBusy(true);
    const registered = await registerReference(workspace.client_workspace_id, {
      ...referenceForm,
      tags: splitTokens(referenceForm.tags),
      source_refs: splitTokens(referenceForm.source_refs),
      sha256: referenceForm.sha256 || null,
      size_bytes: referenceForm.size_bytes ? Number(referenceForm.size_bytes) : null,
    });
    const nextReferences = [registered, ...library.references.filter((item) => item.artifact_ref_id !== registered.artifact_ref_id)];
    const nextLibrary = await listReferences(workspace.client_workspace_id, nextReferences);
    setLibrary(nextLibrary);
    setSourceMode(registered.source_mode || nextLibrary.source_mode || sourceMode);
    setMessage(`Reference ${registered.filename || registered.artifact_id} registered as ArtifactRef metadata.`);
    setBusy(false);
  }

  async function handleReferencePatch(reference, patch) {
    setBusy(true);
    const updated = await updateReference(workspace.client_workspace_id, reference.artifact_ref_id, patch, reference);
    const nextReferences = library.references.map((item) =>
      item.artifact_ref_id === reference.artifact_ref_id ? updated : item,
    );
    const nextLibrary = await listReferences(workspace.client_workspace_id, nextReferences);
    setLibrary(nextLibrary);
    setSourceMode(updated.source_mode || nextLibrary.source_mode || sourceMode);
    setMessage(`Reference ${updated.artifact_id} metadata updated.`);
    setBusy(false);
  }

  return (
    <section className="panel span-2 workspace-reference-panel">
      <div className="panel-header">
        <div>
          <span className="eyebrow amber">Operator Workspace Inputs</span>
          <h2>Client Workspace + Reference Library</h2>
        </div>
        <span className={`status-pill ${sourceMode}`}>{sourceMode}</span>
      </div>

      <div className="workspace-reference-status">
        <div>
          <span>Workspace path</span>
          <strong>{workspace.workspace_relative_path}</strong>
        </div>
        <div>
          <span>Brand Context Version</span>
          <strong>{brandContextVersion.brand_context_version_id}</strong>
        </div>
        <div>
          <span>Ready for Generation</span>
          <strong>{readyForGeneration ? "yes" : "no"}</strong>
        </div>
      </div>

      <div className="workspace-reference-grid">
        <form className="workspace-reference-form" onSubmit={handleCreateWorkspace}>
          <h3>Create Client Workspace</h3>
          <label>
            Client ID
            <input value={workspaceForm.client_id} onChange={(event) => setWorkspaceForm((current) => ({ ...current, client_id: event.target.value }))} />
          </label>
          <label>
            Client Slug
            <input value={workspaceForm.client_slug} onChange={(event) => setWorkspaceForm((current) => ({ ...current, client_slug: event.target.value }))} />
          </label>
          <label>
            Brand ID
            <input value={workspaceForm.brand_id} onChange={(event) => setWorkspaceForm((current) => ({ ...current, brand_id: event.target.value }))} />
          </label>
          <label>
            Brand Context Version ID
            <input
              value={workspaceForm.brand_context_version_id}
              onChange={(event) => setWorkspaceForm((current) => ({ ...current, brand_context_version_id: event.target.value }))}
            />
          </label>
          <label>
            Display Name
            <input value={workspaceForm.display_name} onChange={(event) => setWorkspaceForm((current) => ({ ...current, display_name: event.target.value }))} />
          </label>
          <button className="primary-button" type="submit" disabled={busy}>
            Create Client Workspace
          </button>
        </form>

        <form className="workspace-reference-form" onSubmit={handleCreateBrandContext}>
          <h3>Brand Context Version</h3>
          <label>
            Brand Context Version ID
            <input
              value={brandForm.brand_context_version_id}
              onChange={(event) => setBrandForm((current) => ({ ...current, brand_context_version_id: event.target.value }))}
            />
          </label>
          <label>
            Context Label
            <input value={brandForm.context_label} onChange={(event) => setBrandForm((current) => ({ ...current, context_label: event.target.value }))} />
          </label>
          <label>
            Source Note
            <textarea value={brandForm.source_note} onChange={(event) => setBrandForm((current) => ({ ...current, source_note: event.target.value }))} />
          </label>
          <button className="ghost-button" type="submit" disabled={busy}>
            Save Brand Context Version
          </button>
          <div className="folder-map">
            {Object.entries(workspace.folder_map || {}).map(([label, path]) => (
              <div key={label}>
                <span>{label}</span>
                <strong>{path}</strong>
              </div>
            ))}
          </div>
        </form>

        <form className="workspace-reference-form register-reference-form" onSubmit={handleRegisterReference}>
          <h3>Register Reference</h3>
          <label>
            Filename
            <input value={referenceForm.filename} onChange={(event) => setReferenceForm((current) => ({ ...current, filename: event.target.value }))} />
          </label>
          <label>
            Content Type
            <input value={referenceForm.content_type} onChange={(event) => setReferenceForm((current) => ({ ...current, content_type: event.target.value }))} />
          </label>
          <label>
            Category
            <select value={referenceForm.category} onChange={(event) => setReferenceForm((current) => ({ ...current, category: event.target.value }))}>
              <option value="reference">reference</option>
              <option value="brand">brand</option>
              <option value="avatar">avatar</option>
              <option value="template">template</option>
              <option value="other">other</option>
            </select>
          </label>
          <label>
            Tags
            <input value={referenceForm.tags} onChange={(event) => setReferenceForm((current) => ({ ...current, tags: event.target.value }))} />
          </label>
          <label>
            Source Refs
            <input value={referenceForm.source_refs} onChange={(event) => setReferenceForm((current) => ({ ...current, source_refs: event.target.value }))} />
          </label>
          <label>
            Rights Status
            <select value={referenceForm.rights_status} onChange={(event) => setReferenceForm((current) => ({ ...current, rights_status: event.target.value }))}>
              {rightsOptions.map((option) => (
                <option value={option} key={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>
          <label>
            Approval State
            <select value={referenceForm.approval_state} onChange={(event) => setReferenceForm((current) => ({ ...current, approval_state: event.target.value }))}>
              {approvalOptions.map((option) => (
                <option value={option} key={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>
          <label>
            SHA256
            <input value={referenceForm.sha256} onChange={(event) => setReferenceForm((current) => ({ ...current, sha256: event.target.value }))} />
          </label>
          <label>
            Size Bytes
            <input value={referenceForm.size_bytes} onChange={(event) => setReferenceForm((current) => ({ ...current, size_bytes: event.target.value }))} />
          </label>
          <label className="span-two">
            Notes
            <textarea value={referenceForm.notes} onChange={(event) => setReferenceForm((current) => ({ ...current, notes: event.target.value }))} />
          </label>
          <button className="primary-button" type="submit" disabled={busy}>
            Register Reference
          </button>
        </form>
      </div>

      <div className="reference-library-header">
        <div>
          <span className="eyebrow">Reference Library</span>
          <h3>Rights: {summarizeCounts(library.counts_by_rights_status)}</h3>
        </div>
        <div>
          <span className="eyebrow">Approval</span>
          <h3>{summarizeCounts(library.counts_by_approval_state)}</h3>
        </div>
      </div>

      <div className="reference-card-grid">
        {library.references.map((reference) => (
          <article className="reference-card" key={reference.artifact_ref_id}>
            <div className="reference-thumb" aria-hidden="true">
              REF
            </div>
            <div className="reference-card-copy">
              <span>{reference.category}</span>
              <strong>{reference.artifact_id}</strong>
              <small>{reference.relative_path}</small>
              <div className="reference-chip-row">
                <span>{reference.rights_status}</span>
                <span>{reference.approval_state}</span>
                {reference.tags.map((tag) => (
                  <span key={tag}>{tag}</span>
                ))}
              </div>
              <div className="reference-edit-row">
                <select
                  value={reference.rights_status}
                  onChange={(event) => handleReferencePatch(reference, { rights_status: event.target.value })}
                >
                  {rightsOptions.map((option) => (
                    <option value={option} key={option}>
                      {option}
                    </option>
                  ))}
                </select>
                <select
                  value={reference.approval_state}
                  onChange={(event) => handleReferencePatch(reference, { approval_state: event.target.value })}
                >
                  {approvalOptions.map((option) => (
                    <option value={option} key={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </article>
        ))}
      </div>

      <p className="workspace-reference-message">{message}</p>
    </section>
  );
}

