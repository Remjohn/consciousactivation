import { useQuery } from "@tanstack/react-query";
import { getInterviewStatus } from "../api/interviews";
import type { ApiError } from "../api/ApiError";
import type { InterviewStatusResponse } from "../api/types";

export function useInterviewStatus(packageId: string, enabled = true) {
  return useQuery<InterviewStatusResponse, ApiError>({
    queryKey: ["interviewStatus", packageId] as const,
    queryFn: () => getInterviewStatus(packageId),
    enabled: enabled && !!packageId,
  });
}
