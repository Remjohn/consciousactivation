import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../api/http";
import type { ApiError } from "../api/ApiError";
import type { HarnessDetail } from "../api/types";

export function useHarnessDetail(definitionId: string) {
  return useQuery<HarnessDetail, ApiError>({
    queryKey: ["harnesses", definitionId],
    queryFn: () => apiFetch<HarnessDetail>(`/api/harnesses/${definitionId}`),
  });
}
