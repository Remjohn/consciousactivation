import { useMutation } from "@tanstack/react-query";
import { createCampaign } from "../api/campaigns";
import type { CampaignCreateRequest, CampaignDetailResponse } from "../api/types";
import type { ApiError } from "../api/ApiError";

export function useCreateCampaign() {
  return useMutation<CampaignDetailResponse, ApiError, CampaignCreateRequest>({
    mutationFn: createCampaign,
  });
}
