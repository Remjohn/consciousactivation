import { useQuery } from "@tanstack/react-query";
import { listCampaigns, type CampaignListFilters } from "../api/campaigns";
import type { ApiError } from "../api/ApiError";

export function useCampaigns(filters: CampaignListFilters) {
  return useQuery<ReturnType<typeof listCampaigns>, ApiError>({
    queryKey: ["campaigns", filters] as const,
    queryFn: () => listCampaigns(filters),
  });
}
