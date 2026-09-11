import { Link } from "@tanstack/react-router";
import { LifecycleBadge } from "./LifecycleBadge";
import type { CampaignSummary } from "../../api/types";

export function CampaignCard({ campaign }: { campaign: CampaignSummary }) {
  return (
    <Link
      to="/campaigns/$campaignId"
      params={{ campaignId: campaign.campaign_id }}
      className="block rounded-[var(--radius-card)] border border-border-subtle bg-surface p-5 hover:border-border-accent transition-colors"
    >
      <div className="flex items-center justify-between">
        <LifecycleBadge state={campaign.lifecycle_state} />
        <span className="text-ink-muted text-sm">{campaign.category_id}</span>
      </div>
      <div className="mt-2 text-ink-muted text-xs tracking-wide uppercase">
        {campaign.autonomy_mode} &middot; {campaign.output_target_count} output
        {campaign.output_target_count === 1 ? "" : "s"} &middot; {campaign.budget_units} budget
      </div>
    </Link>
  );
}
