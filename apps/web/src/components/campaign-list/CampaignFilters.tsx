import type { CampaignLifecycleState } from "../../api/types";
import { LIFECYCLE_TOKENS } from "../../lib/statusTokens";

const STATES: CampaignLifecycleState[] = [
  "DRAFT",
  "LAUNCHED",
  "RUNNING",
  "AWAITING_REVIEW",
  "BLOCKED_EXCEPTION",
  "READY_TO_SHIP",
  "SHIPPED",
  "CANCELLED",
];

interface CampaignFiltersProps {
  value: CampaignLifecycleState | undefined;
  onChange: (value: CampaignLifecycleState | undefined) => void;
}

export function CampaignFilters({ value, onChange }: CampaignFiltersProps) {
  return (
    <div className="flex flex-wrap gap-2" data-testid="campaign-filters">
      <button
        type="button"
        onClick={() => onChange(undefined)}
        className={`rounded-full border px-3 py-1 text-xs font-medium tracking-wide uppercase transition-colors ${
          value === undefined
            ? "border-gold text-gold"
            : "border-border-subtle text-ink-muted hover:border-border-accent"
        }`}
      >
        All
      </button>
      {STATES.map((s) => {
        const token = LIFECYCLE_TOKENS[s];
        const isActive = value === s;
        return (
          <button
            key={s}
            type="button"
            onClick={() => onChange(isActive ? undefined : s)}
            className={`rounded-full border px-3 py-1 text-xs font-medium tracking-wide uppercase transition-colors ${
              isActive
                ? `border-${token.color} text-${token.color}`
                : "border-border-subtle text-ink-muted hover:border-border-accent"
            }`}
          >
            {s.replace(/_/g, " ")}
          </button>
        );
      })}
    </div>
  );
}
