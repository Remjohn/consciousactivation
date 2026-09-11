import { useState } from "react";
import { useInterviewStatus } from "../../hooks/useInterviewStatus";
import type { InterviewStatusResponse } from "../../api/types";

const READY_STATES = new Set(["COMPONENTS_IN_PROGRESS", "PUBLISHED_DERIVATIVE_ELIGIBLE"]);

interface ExistingSourcePanelProps {
  onReady: (packageId: string) => void;
}

export function ExistingSourcePanel({ onReady }: ExistingSourcePanelProps) {
  const [packageId, setPackageId] = useState("");
  const [triggeredId, setTriggeredId] = useState<string | null>(null);
  const { data, error, refetch, isFetching } = useInterviewStatus(triggeredId ?? "", triggeredId !== null);

  const isReady = data ? READY_STATES.has(data.lifecycle_state) : false;

  async function handleCheck() {
    setTriggeredId(packageId);
    await refetch();
  }

  function handleContinue() {
    if (isReady && packageId) {
      onReady(packageId);
    }
  }

  return (
    <div className="rounded-[var(--radius-card)] border border-border-subtle bg-surface p-6">
      <h3 className="text-ink-primary text-lg font-semibold">Use Existing Source</h3>
      <p className="mt-1 text-ink-muted text-sm">Enter a source package ID to verify it is ready for a campaign.</p>

      <div className="mt-4 flex gap-2">
        <input
          type="text"
          value={packageId}
          onChange={(e) => setPackageId(e.target.value)}
          placeholder="Source package ID"
          className="flex-1 rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary placeholder:text-ink-faint focus:border-gold focus:outline-none"
          data-testid="existing-source-input"
        />
        <button
          type="button"
          onClick={handleCheck}
          disabled={!packageId || isFetching}
          className="rounded-full border border-gold px-4 py-2 text-sm font-medium text-gold hover:bg-gold/10 disabled:opacity-40"
          data-testid="check-status-btn"
        >
          {isFetching ? "Checking..." : "Check Status"}
        </button>
      </div>

      {error && (
        <div className="mt-3 rounded border border-state-blocked/50 bg-state-blocked/10 p-3 text-sm text-state-blocked" data-testid="source-error">
          {error.errorCode}: {error.message}
        </div>
      )}

      {data && !isReady && (
        <div className="mt-3 rounded border border-state-awaiting/50 bg-state-awaiting/10 p-3 text-sm text-state-awaiting" data-testid="source-warning">
          This source is at <strong>{data.lifecycle_state}</strong> — needs at least one bound component before a campaign can use it.
        </div>
      )}

      {data && isReady && (
        <div className="mt-3 rounded border border-state-ready/50 bg-state-ready/10 p-3 text-sm text-state-ready" data-testid="source-ready">
          Source is ready (state: {data.lifecycle_state}). Word count: {data.word_count ?? "?"}, phrase count: {data.phrase_count ?? "?"}.
        </div>
      )}

      <button
        type="button"
        onClick={handleContinue}
        disabled={!isReady}
        className="mt-4 rounded-full bg-gold px-5 py-2.5 font-semibold text-gold-on disabled:opacity-40"
        data-testid="existing-continue-btn"
      >
        Continue
      </button>
    </div>
  );
}
