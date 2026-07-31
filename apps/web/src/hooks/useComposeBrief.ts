import { useMutation } from "@tanstack/react-query";
import { composeBrief } from "../api/interviewComposer";
import type { ActivativeInterviewBriefResponse } from "../api/types";
import type { ComposeBriefInput } from "../api/interviewComposer";
import type { ApiError } from "../api/ApiError";

export function useComposeBrief() {
  return useMutation<ActivativeInterviewBriefResponse, ApiError, ComposeBriefInput>({
    mutationFn: composeBrief,
  });
}
