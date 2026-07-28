import type { CampaignCreateRequest, HarnessSummary } from "../../api/types";

interface LaunchReviewProps {
  request: CampaignCreateRequest;
  harness?: HarnessSummary;
  onLaunch: () => void;
  isPending: boolean;
  error: { error_code: string; message: string } | null;
}

export function LaunchReview({ request, harness, onLaunch, isPending, error }: LaunchReviewProps) {
  return (
    <div className="rounded-[var(--radius-card)] border border-border-subtle bg-surface p-6" data-testid="launch-review">
      <h3 className="text-ink-primary text-lg font-semibold">Launch Review</h3>

      <dl className="mt-4 space-y-2 text-sm">
        <div>
          <dt className="text-ink-muted">Source Package</dt>
          <dd className="text-ink-primary">{request.source_package_id}</dd>
        </div>
        <div>
          <dt className="text-ink-muted">Harness</dt>
          <dd className="text-ink-primary">{harness?.category_name ?? request.category_id}</dd>
        </div>
        <div>
          <dt className="text-ink-muted">Autonomy Mode</dt>
          <dd className="text-ink-primary">{request.autonomy_mode}</dd>
        </div>
        <div>
          <dt className="text-ink-muted">Output Targets</dt>
          <dd className="text-ink-primary">{request.output_targets.length} target(s)</dd>
        </div>
        <div>
          <dt className="text-ink-muted">Budget</dt>
          <dd className="text-ink-primary">{request.budget_units} units</dd>
        </div>
        <div>
          <dt className="text-ink-muted">Idempotency Key</dt>
          <dd className="text-ink-faint font-mono text-xs">{request.idempotency_key}</dd>
        </div>
      </dl>

      {error && (
        <div className="mt-3 rounded border border-state-blocked/50 bg-state-blocked/10 p-3 text-sm text-state-blocked" data-testid="launch-error">
          {error.error_code}: {error.message}
        </div>
      )}

      <button
        type="button"
        onClick={onLaunch}
        disabled={isPending}
        className="mt-6 w-full rounded-full bg-gold px-5 py-2.5 font-semibold text-gold-on disabled:opacity-40"
        data-testid="launch-campaign-btn"
      >
        {isPending ? "Launching..." : "Launch Campaign"}
      </button>
    </div>
  );
}
