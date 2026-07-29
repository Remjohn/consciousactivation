// TS-APP-UI-003 - useControlTower hook
// Polls GET /api/campaigns/{id}/tower, disables polling when WS is open

import { useQuery, useQueryClient } from "@tanstack/react-query";
import { getControlTower } from "../api/campaigns";
import type { ControlTowerProjection } from "../api/campaigns";

export function useControlTower(campaignId: string, wsOpen: boolean = false) {
  const queryClient = useQueryClient();

  return useQuery({
    queryKey: ["campaign", campaignId, "tower"],
    queryFn: () => getControlTower(campaignId) as Promise<ControlTowerProjection>,
    refetchInterval: wsOpen ? false : 4000, // Disable polling when WS is open
    onError: (error: Error) => {
      console.error("[useControlTower] Failed to fetch tower:", error);
    },
  });
}

// Helper to invalidate tower data
export function useInvalidateControlTower(campaignId: string) {
  const queryClient = useQueryClient();

  return () => {
    queryClient.invalidateQueries({ queryKey: ["campaign", campaignId, "tower"] });
  };
}
