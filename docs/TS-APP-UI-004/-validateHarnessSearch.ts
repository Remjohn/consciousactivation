import { CANONICAL_CATEGORIES } from "../../api/types";
import type { CanonicalCategoryId, HarnessLibrarySearch } from "../../api/types";

export function validateSearch(search: Record<string, unknown>): HarnessLibrarySearch {
  const categoryIds = new Set(CANONICAL_CATEGORIES.map((c) => c.id));
  return {
    category:
      typeof search.category === "string" && categoryIds.has(search.category as CanonicalCategoryId)
        ? (search.category as CanonicalCategoryId)
        : undefined,
    mode:
      search.mode === "generic" || search.mode === "activative" ? search.mode : undefined,
    q: typeof search.q === "string" && search.q.length > 0 ? search.q : undefined,
    sourceCategory: typeof search.sourceCategory === "string" ? search.sourceCategory : undefined,
  };
}
