import { useMutation } from "@tanstack/react-query";
import { createResearchPackage } from "../api/interviewComposer";
import type { GuestResearchPackageResponse } from "../api/types";
import type { CreateResearchPackageInput } from "../api/interviewComposer";
import type { ApiError } from "../api/ApiError";

export function useCreateResearchPackage() {
  return useMutation<GuestResearchPackageResponse, ApiError, CreateResearchPackageInput>({
    mutationFn: createResearchPackage,
  });
}
