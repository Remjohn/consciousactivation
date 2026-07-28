import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../api/http";
import type { ApiError } from "../api/ApiError";
import type { HealthResponse } from "../api/types";

export function useHealth() {
  return useQuery<HealthResponse, ApiError>({
    queryKey: ["health"],
    queryFn: () => apiFetch<HealthResponse>("/api/health"),
    refetchInterval: 30_000,
  });
}
