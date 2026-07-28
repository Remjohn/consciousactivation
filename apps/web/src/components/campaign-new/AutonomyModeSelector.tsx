import type { AutonomyMode } from "../../api/types";

interface AutonomyModeSelectorProps {
  value: AutonomyMode;
  onChange: (mode: AutonomyMode) => void;
}

const OPTIONS: { mode: AutonomyMode; label: string; description: string }[] = [
  { mode: "AUTOPILOT", label: "Autopilot", description: "Runs without interruption unless something breaks." },
  { mode: "REVIEW_BEFORE_SHIP", label: "Review Before Ship", description: "Runs freely, but pauses for your review at the final artifact." },
  { mode: "CHECKPOINTED", label: "Checkpointed", description: "Pauses at two fixed checkpoints: final script approval and final artifact review." },
  { mode: "SHADOW", label: "Shadow", description: "Runs silently for observation only — this campaign can never be shipped." },
];

export function AutonomyModeSelector({ value, onChange }: AutonomyModeSelectorProps) {
  return (
    <div className="space-y-3" data-testid="autonomy-mode-selector">
      {OPTIONS.map((opt) => (
        <button
          key={opt.mode}
          type="button"
          onClick={() => onChange(opt.mode)}
          className={`w-full rounded-[var(--radius-card)] border p-4 text-left transition-colors ${
            value === opt.mode
              ? "border-gold bg-gold/10"
              : "border-border-subtle hover:border-border-accent"
          }`}
          data-testid={`autonomy-option-${opt.mode}`}
        >
          <div className="text-ink-primary text-sm font-semibold">{opt.label}</div>
          <div className="mt-1 text-ink-muted text-xs">{opt.description}</div>
        </button>
      ))}
    </div>
  );
}
