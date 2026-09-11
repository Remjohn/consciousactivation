declare function require(name: string): any;
const crypto = require("crypto") as { createHash(algorithm: string): { update(input: string): any; digest(encoding: string): string } };

export function normalize<T>(value: T): T {
  if (value === undefined) throw new Error("canonical value cannot contain undefined");
  if (Array.isArray(value)) return value.map(normalize) as T;
  if (value !== null && typeof value === "object") {
    const record = value as Record<string, unknown>;
    const sorted: Record<string, unknown> = {};
    for (const key of Object.keys(record).sort()) sorted[key] = normalize(record[key]);
    return sorted as T;
  }
  return value;
}

export function canonicalJson(value: unknown): string {
  return JSON.stringify(normalize(value));
}

export function canonicalSha256(value: unknown): string {
  return crypto.createHash("sha256").update(canonicalJson(value)).digest("hex");
}

export function deterministicId(prefix: string, value: unknown): string {
  if (!/^[a-zA-Z0-9][a-zA-Z0-9._:-]*$/.test(prefix)) throw new Error(`invalid deterministic ID prefix: ${prefix}`);
  return `${prefix}:${canonicalSha256(value).slice(0, 24)}`;
}

export function uniqueSorted(values: ReadonlyArray<string>): string[] {
  return Array.from(new Set(values)).sort();
}
