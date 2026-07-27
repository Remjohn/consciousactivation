import { useState } from "react";
import { FRAME_PROFILE_OPTIONS, isInvalidDeliveryFrameProfile } from "../../types/supervisualRuntime";

export function SuperVisualCreateProjectModal({ open, onClose, onCreate, creating }) {
  const [form, setForm] = useState({
    title: "",
    brand_id: "",
    brand_context_version_id: "",
    source_context_refs: "",
    default_frame_profile: "1:1_SOFT_ROUNDED_EDITORIAL",
    target_platforms: "instagram",
  });
  const invalidFrame = isInvalidDeliveryFrameProfile(form.default_frame_profile);

  if (!open) return null;

  function update(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function submit(event) {
    event.preventDefault();
    if (invalidFrame) return;
    await onCreate?.({
      title: form.title || "Untitled SuperVisual",
      brand_id: form.brand_id,
      brand_context_version_id: form.brand_context_version_id,
      source_context_refs: form.source_context_refs
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean),
      default_frame_profile: form.default_frame_profile,
      target_platforms: form.target_platforms
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean),
    });
  }

  return (
    <div className="sv-modal-backdrop">
      <form className="sv-modal" onSubmit={submit}>
        <div className="sv-panel-header">
          <div>
            <p className="sv-eyebrow">New project</p>
            <h2>Create SuperVisual</h2>
          </div>
          <button type="button" className="sv-button sv-button-small" onClick={onClose}>
            Close
          </button>
        </div>

        <label>
          Title
          <input value={form.title} onChange={(event) => update("title", event.target.value)} />
        </label>
        <label>
          Brand ID
          <input required value={form.brand_id} onChange={(event) => update("brand_id", event.target.value)} />
        </label>
        <label>
          Brand Context Version ID
          <input required value={form.brand_context_version_id} onChange={(event) => update("brand_context_version_id", event.target.value)} />
        </label>
        <label>
          Source context refs comma-separated
          <input value={form.source_context_refs} onChange={(event) => update("source_context_refs", event.target.value)} />
        </label>
        <label>
          Delivery frame profile
          <select value={form.default_frame_profile} onChange={(event) => update("default_frame_profile", event.target.value)}>
            {FRAME_PROFILE_OPTIONS.map((option) => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </label>
        {invalidFrame ? <p className="sv-error">16:9 is source-only and cannot be used as delivery.</p> : null}
        <label>
          Target platforms comma-separated
          <input value={form.target_platforms} onChange={(event) => update("target_platforms", event.target.value)} />
        </label>

        <button className="sv-button sv-button-primary" disabled={creating || invalidFrame}>
          {creating ? "Creating…" : "Create project"}
        </button>
      </form>
    </div>
  );
}
