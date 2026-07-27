export class ApiError extends Error {
  constructor(message, { status, payload, url } = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.payload = payload;
    this.url = url;
  }
}

export function getApiBaseUrl() {
  return (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");
}

export async function apiFetch(path, options = {}) {
  const baseUrl = getApiBaseUrl();
  const url = `${baseUrl}${path}`;
  const headers = {
    Accept: "application/json",
    ...(options.body ? { "Content-Type": "application/json" } : {}),
    ...(options.headers || {}),
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json().catch(() => null)
    : await response.text().catch(() => "");

  if (!response.ok) {
    const message =
      payload?.detail ||
      payload?.message ||
      payload?.error ||
      `Request failed with ${response.status}`;
    throw new ApiError(message, { status: response.status, payload, url });
  }

  return payload;
}

export function normalizeApiError(error) {
  if (error instanceof ApiError) {
    return {
      message: error.message,
      status: error.status,
      payload: error.payload,
      url: error.url,
    };
  }
  return {
    message: error?.message || "Unknown error",
    status: null,
    payload: null,
    url: null,
  };
}
