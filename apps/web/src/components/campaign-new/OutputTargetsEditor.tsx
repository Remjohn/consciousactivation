import { useState } from "react";
import type { OutputTarget } from "../../api/types";

interface OutputTargetsEditorProps {
  targets: OutputTarget[];
  onChange: (targets: OutputTarget[]) => void;
}

export function OutputTargetsEditor({ targets, onChange }: OutputTargetsEditorProps) {
  const [outputType, setOutputType] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [profileId, setProfileId] = useState("");

  function addTarget() {
    if (!outputType) return;
    onChange([
      ...targets,
      { output_type: outputType, quantity, profile_id: profileId || undefined } as OutputTarget,
    ]);
    setOutputType("");
    setQuantity(1);
    setProfileId("");
  }

  function removeTarget(index: number) {
    onChange(targets.filter((_, i) => i !== index));
  }

  return (
    <div className="space-y-3" data-testid="output-targets-editor">
      {targets.length > 0 && (
        <ul className="space-y-2">
          {targets.map((t, i) => (
            <li key={i} className="flex items-center gap-2 rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary">
              <span className="flex-1">{t.output_type} × {t.quantity}{t.profile_id ? ` (${t.profile_id})` : ""}</span>
              <button
                type="button"
                onClick={() => removeTarget(i)}
                className="text-state-blocked hover:text-state-blocked/80"
                data-testid={`remove-target-${i}`}
              >
                ×
              </button>
            </li>
          ))}
        </ul>
      )}

      <div className="flex gap-2">
        <input
          type="text"
          value={outputType}
          onChange={(e) => setOutputType(e.target.value)}
          placeholder="Output type"
          className="flex-1 rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary placeholder:text-ink-faint"
          data-testid="output-type-input"
        />
        <input
          type="number"
          value={quantity}
          onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
          min={1}
          className="w-20 rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary"
          data-testid="output-quantity-input"
        />
        <input
          type="text"
          value={profileId}
          onChange={(e) => setProfileId(e.target.value)}
          placeholder="Profile ID"
          className="flex-1 rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary placeholder:text-ink-faint"
          data-testid="output-profile-input"
        />
        <button
          type="button"
          onClick={addTarget}
          disabled={!outputType}
          className="rounded-full border border-gold px-4 py-2 text-sm font-medium text-gold hover:bg-gold/10 disabled:opacity-40"
          data-testid="add-output-btn"
        >
          Add
        </button>
      </div>
    </div>
  );
}
