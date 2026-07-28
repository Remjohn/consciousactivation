import { useHarnesses } from "../../hooks/useHarnesses";
import type { HarnessSummary } from "../../api/types";

interface HarnessPickerProps {
  onSelect: (harness: HarnessSummary) => void;
  selectedId?: string;
}

export function HarnessPicker({ onSelect, selectedId }: HarnessPickerProps) {
  const { data: harnesses, isLoading, isError } = useHarnesses();

  if (isLoading) {
    return <div className="text-ink-muted text-sm" data-testid="harness-picker-loading">Loading harnesses...</div>;
  }

  if (isError) {
    return <div className="text-state-blocked text-sm" data-testid="harness-picker-error">Failed to load harnesses.</div>;
  }

  return (
    <div className="grid grid-cols-3 gap-4" data-testid="harness-picker">
      {(harnesses ?? []).map((h) => {
        // Best-effort client-side check: format_profile_id subrule omitted —
        // API-002 has no format_profile_ids field, so the server's authoritative
        // FORMAT02_DEFERRED backstop is the only protection for format-profile-gated cases.
        const deferred = h.category_id === "2d_character_animation" || h.mode === "generic";
        const isSelected = h.definition_id === selectedId;

        return (
          <button
            key={h.definition_id}
            type="button"
            disabled={deferred}
            onClick={() => onSelect(h)}
            className={`rounded-[var(--radius-card)] border p-4 text-left transition-colors ${
              deferred
                ? "cursor-not-allowed opacity-40 border-border-subtle"
                : isSelected
                ? "border-gold bg-gold/10"
                : "border-border-subtle bg-surface hover:border-border-accent"
            }`}
            data-testid={`harness-card-${h.definition_id}`}
          >
            <div className="text-ink-primary text-sm font-semibold">{h.category_name ?? h.category_id ?? "Generic"}</div>
            <div className="mt-1 text-ink-muted text-xs">v{h.manifest_version}</div>
            <div className="mt-1 text-ink-muted text-xs">mode: {h.mode}</div>
            {deferred && (
              <span className="mt-2 inline-block text-state-blocked text-xs font-medium" data-testid={`harness-deferred-${h.definition_id}`}>
                Deferred
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}
