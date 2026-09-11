import { useState } from "react";
import { Link } from "@tanstack/react-router";
import { useCampaigns } from "../hooks/useCampaigns";
import { CampaignCard } from "../components/campaign-list/CampaignCard";
import { CampaignFilters } from "../components/campaign-list/CampaignFilters";
import { EmptyCampaignState } from "../components/campaign-list/EmptyCampaignState";
import type { CampaignLifecycleState } from "../api/types";

function ListSkeleton() {
  return (
    <div className="mt-6 space-y-4">
      {[1, 2, 3].map((i) => (
        <div
          key={i}
          className="rounded-[var(--radius-card)] border border-border-subtle bg-surface p-5 animate-pulse"
        >
          <div className="h-4 w-24 rounded bg-surface-raised" />
          <div className="mt-2 h-3 w-48 rounded bg-surface-raised" />
        </div>
      ))}
    </div>
  );
}

function ErrorBanner({ onRetry }: { onRetry: () => void }) {
  return (
    <div className="mt-4 flex items-center gap-3 rounded-[var(--radius-card)] border border-state-blocked/50 bg-surface p-4">
      <span className="text-state-blocked text-sm">Failed to load campaigns.</span>
      <button
        type="button"
        onClick={onRetry}
        className="rounded-full border border-state-blocked px-3 py-1 text-xs font-medium text-state-blocked hover:bg-state-blocked/10"
      >
        Retry
      </button>
    </div>
  );
}

export default function CampaignList() {
  const [lifecycleFilter, setLifecycleFilter] = useState<CampaignLifecycleState | undefined>();
  const { data: campaigns, isLoading, isError, refetch } = useCampaigns({
    lifecycle_state: lifecycleFilter,
  });

  return (
    <div className="min-h-screen bg-canvas p-8">
      <div className="flex items-center justify-between">
        <h1 className="text-ink-primary text-2xl font-bold">Campaigns</h1>
        <Link
          to="/campaigns/new"
          className="rounded-full bg-gold px-5 py-2.5 font-semibold text-gold-on"
        >
          + New Campaign
        </Link>
      </div>

      <div className="mt-6">
        <CampaignFilters value={lifecycleFilter} onChange={setLifecycleFilter} />
      </div>

      {isLoading && <ListSkeleton />}
      {isError && <ErrorBanner onRetry={() => refetch()} />}
      {campaigns && campaigns.length === 0 && !isLoading && <EmptyCampaignState />}
      {campaigns && campaigns.length > 0 && (
        <div className="mt-6 space-y-4">
          {campaigns.map((c) => (
            <CampaignCard key={c.campaign_id} campaign={c} />
          ))}
        </div>
      )}
    </div>
  );
}
