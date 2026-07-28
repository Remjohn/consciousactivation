import { useMutation } from "@tanstack/react-query";
import { importInterview } from "../api/interviews";
import type { ImportInterviewInput, ImportInterviewResponse } from "../api/types";
import type { ApiError } from "../api/ApiError";

export function useImportInterview() {
  return useMutation<ImportInterviewResponse, ApiError, ImportInterviewInput>({
    mutationFn: importInterview,
  });
}
