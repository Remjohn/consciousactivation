// TS-APP-UI-003 - CampaignHeader component
// Shows lifecycle badge, autonomy badge, and studio binding info

import { LifecycleBadge } from "../campaign-list/LifecycleBadge";
import { Badge } from "../ui/Badge";
import { LIFECYCLE_STATUS_TOKEN } from "../../lib/nodeState";
import type { ControlTowerProjection } from "../../api/campaigns";

interface CampaignHeaderProps {
  tower: ControlTowerProjection;
  campaignId: string;
}

export function CampaignHeader({ tower, campaignId }: CampaignHeaderProps) {
  const lifecycleState = tower.campaign?.lifecycle_state ?? "DRAFT";
  const autonomyMode = tower.campaign?.autonomy_mode ?? "AUTOPILOT";
  const surfaceTitle = tower.studio_binding?.primary_surface
    ? getStudioSurfaceTitle(tower.studio_binding.primary_surface)
    : "Unknown Studio";

  return (
    <div className="control-tower-card">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="font-mono text-sm text-ca-text-secondary">
            campaign:{campaignId.slice(0, 8)}
          </span>
          <LifecycleBadge state={lifecycleState} />
          <Badge tone="muted">{autonomyMode}</Badge>
        </div>
        <div className="text-sm text-ca-text-secondary">
          {surfaceTitle}
        </div>
      </div>
    </div>
  );
}

// Helper to get studio surface title (simplified - in production would import from studio)
function getStudioSurfaceTitle(surfaceId: string): string {
  const surfaceTitles: Record<string, string> = {
    "video-production": "Video Production",
    "social-media": "Social Media",
    "email-marketing": "Email Marketing",
  };
  return surfaceTitles[surfaceId] ?? surfaceId;
}
