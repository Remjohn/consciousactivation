import { createHash } from "node:crypto";

export type JsonPrimitive = string | number | boolean | null;
export type JsonValue = JsonPrimitive | ReadonlyArray<JsonValue> | { readonly [key: string]: JsonValue };

function normalize(value: unknown, path = "$"): JsonValue {
  if (value === null || typeof value === "string" || typeof value === "boolean") {
    return value;
  }
  if (typeof value === "number") {
    if (!Number.isSafeInteger(value)) {
      throw new TypeError(`${path}: canonical numbers must be safe integers`);
    }
    return value;
  }
  if (Array.isArray(value)) {
    return value.map((item, index) => normalize(item, `${path}[${index}]`));
  }
  if (typeof value === "object") {
    const object = value as Record<string, unknown>;
    const result: Record<string, JsonValue> = {};
    for (const key of Object.keys(object).sort()) {
      const item = object[key];
      if (item === undefined) {
        throw new TypeError(`${path}.${key}: undefined is not canonical`);
      }
      result[key] = normalize(item, `${path}.${key}`);
    }
    return result;
  }
  throw new TypeError(`${path}: unsupported canonical value ${typeof value}`);
}

export function canonicalJson(value: unknown): string {
  return JSON.stringify(normalize(value));
}

export function sha256Hex(value: string | Uint8Array): string {
  return createHash("sha256").update(value).digest("hex");
}

export function canonicalSha256(value: unknown): string {
  return sha256Hex(canonicalJson(value));
}

export function deterministicId(prefix: string, value: unknown): string {
  if (!/^[a-z0-9][a-z0-9._:-]*$/i.test(prefix)) {
    throw new TypeError(`invalid deterministic ID prefix: ${prefix}`);
  }
  return `${prefix}:${canonicalSha256(value).slice(0, 24)}`;
}

export function assertPortableUri(uri: string): void {
  if (!uri || uri.startsWith("/") || uri.includes("\\") || /^[A-Za-z]:\//.test(uri) || uri.includes("..")) {
    throw new TypeError(`non-portable URI: ${uri}`);
  }
}

export function assertSha256(value: string, label = "sha256"): void {
  if (!/^[0-9a-f]{64}$/.test(value)) {
    throw new TypeError(`${label} must be lowercase SHA-256`);
  }
}

export function uniqueSorted(values: ReadonlyArray<string>): ReadonlyArray<string> {
  return [...new Set(values)].sort();
}

export function tokenize(value: string): ReadonlyArray<string> {
  return uniqueSorted(
    value
      .toLocaleLowerCase("en-US")
      .normalize("NFKD")
      .replace(/[^a-z0-9:_-]+/g, " ")
      .trim()
      .split(/\s+/)
      .filter((token) => token.length >= 2),
  );
}
