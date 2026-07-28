/**
 * Browser-safe validation predicates mirroring services/studio/src/validators.ts rules.
 * These are pure functions with zero runtime dependency on Node-only modules
 * (see TS-APP-UI-002 §3 Source Gap Notice 3).
 */

export type ValidationCode =
  | "EMPTY_VALUE"
  | "INVALID_INTEGER"
  | "OUTPUT_TARGET_REQUIRED"
  | "FORMAT02_DEFERRED";

export interface FieldError {
  readonly code: ValidationCode;
  readonly message: string;
}

export function requireNonEmpty(value: string, label: string): FieldError | null {
  return value.trim() ? null : { code: "EMPTY_VALUE", message: `${label} must not be empty` };
}

export function requirePositiveInteger(value: number, label: string): FieldError | null {
  return Number.isSafeInteger(value) && value >= 1
    ? null
    : { code: "INVALID_INTEGER", message: `${label} must be a whole number of at least 1` };
}

export function requireAtLeastOneOutputTarget(count: number): FieldError | null {
  return count >= 1
    ? null
    : { code: "OUTPUT_TARGET_REQUIRED", message: "At least one output target is required" };
}

/**
 * Same rule as validators.ts::validateCampaignOrder — kept in exact sync by hand
 * until a shared package exists.
 * NOTE: The format_profile_id subrule is best-effort only — API-002 has no
 * format_profile_ids field on HarnessSummary, so the server's authoritative
 * FORMAT02_DEFERRED backstop is the only protection for format-profile-gated cases.
 */
export function isFormat02Deferred(categoryId: string, formatProfileId: string): boolean {
  return categoryId === "2d_character_animation" || formatProfileId.startsWith("format02_");
}
