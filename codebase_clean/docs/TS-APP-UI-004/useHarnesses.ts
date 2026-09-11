import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../api/http";
import type { ApiError } from "../api/ApiError";
import type { HarnessSummary } from "../api/types";

export function useHarnesses() {
  return useQuery<HarnessSummary[], ApiError>({
    queryKey: ["harnesses"],
    queryFn: () => apiFetch<HarnessSummary[]>("/api/harnesses"),
  });
}
