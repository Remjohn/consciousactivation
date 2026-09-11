// TS-APP-UI-003 - useControlTower hook
// Polls GET /api/campaigns/{id}/tower, disables polling when WS is open (AC-006).

import { useQuery } from "@tanstack/react-query";
import { getControlTower } from "../api/campaigns";

/**
 * @param campaignId  the campaign whose tower projection to load
 * @param wsOpen      when true, the WebSocket is the freshness signal and the
 *                    REST poll is disabled (refetchInterval: false); when the WS
 *                    closes the caller flips this to false and 4s polling resumes.
 */
export function useControlTower(campaignId: string, wsOpen = false) {
  return useQuery({
    queryKey: ["campaign", campaignId, "tower"],
    queryFn: () => getControlTower(campaignId),
    refetchInterval: wsOpen ? false : 4000,
  });
}
