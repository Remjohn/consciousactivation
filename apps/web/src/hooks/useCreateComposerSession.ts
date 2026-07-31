import { useMutation } from "@tanstack/react-query";
import { createComposerSession } from "../api/interviewComposer";
import type { ComposerSessionResponse } from "../api/types";
import type { ComposeSessionInput } from "../api/interviewComposer";
import type { ApiError } from "../api/ApiError";

export function useCreateComposerSession() {
  return useMutation<ComposerSessionResponse, ApiError, ComposeSessionInput>({
    mutationFn: createComposerSession,
  });
}
