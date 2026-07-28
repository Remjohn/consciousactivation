import { ApiError } from "./ApiError";
import type { ErrorResponse } from "./types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      ...init,
      headers: { "Content-Type": "application/json", ...init?.headers },
    });
  } catch {
    throw new ApiError("Network request failed — is the gateway running?", null, null);
  }

  if (!response.ok) {
    let body: ErrorResponse | null = null;
    try {
      body = (await response.json()) as ErrorResponse;
    } catch {
      // response body was not JSON — fall through with a generic message
    }
    throw new ApiError(
      body?.message ?? `Request failed with status ${response.status}`,
      response.status,
      body?.error_code ?? null,
      body?.service ?? null,
    );
  }

  return (await response.json()) as T;
}
