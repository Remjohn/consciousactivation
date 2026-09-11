import { useState, useEffect, useRef } from "react";
import { useNavigate, useSearch } from "@tanstack/react-router";
import { CANONICAL_CATEGORIES } from "../../api/types";
import type { CanonicalCategoryId, HarnessMode, HarnessLibrarySearch } from "../../api/types";

// Sentinel used only inside this component's own <select> value — never written to the
// URL. "Category-neutral" harnesses are exactly the generic-mode ones (category_id is
// always null in generic mode per api/routers/harnesses.py's projection), so selecting
// it is expressed via the `mode` search param rather than an invalid category id, since
// HarnessLibrarySearch.category only accepts the five canonical ids (TS-APP-UI-004 §6).
const CATEGORY_NEUTRAL_VALUE = "__category_neutral__";

export function HarnessFilterBar() {
  const search = useSearch({ from: "/harnesses/" });
  const navigate = useNavigate({ from: "/harnesses/" });
  const [q, setQ] = useState(search.q ?? "");
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => setQ(search.q ?? ""), [search.q]);

  function updateSearch(patch: Partial<HarnessLibrarySearch>) {
    navigate({ search: (prev) => ({ ...prev, ...patch }) });
  }

  function handleCategoryChange(value: string) {
    if (value === "") updateSearch({ category: undefined });
    else if (value === CATEGORY_NEUTRAL_VALUE) updateSearch({ category: undefined, mode: "generic" });
    else updateSearch({ category: value as CanonicalCategoryId });
  }

  function handleModeChange(value: string) {
    updateSearch({ mode: value === "" ? undefined : (value as HarnessMode) });
  }

  function handleQChange(value: string) {
    setQ(value);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      updateSearch({ q: value.length > 0 ? value : undefined });
    }, 300);
  }

  const categoryValue = search.category ?? (search.mode === "generic" ? CATEGORY_NEUTRAL_VALUE : "");

  return (
    <div className="mt-4 flex flex-wrap items-center gap-2">
      <select
        aria-label="Filter by category"
        value={categoryValue}
        onChange={(event) => handleCategoryChange(event.target.value)}
        className="rounded-md border border-border bg-surface px-2 py-1 text-sm text-foreground"
      >
        <option value="">All categories</option>
        {CANONICAL_CATEGORIES.map((category) => (
          <option key={category.id} value={category.id}>
            {category.label}
          </option>
        ))}
        <option value={CATEGORY_NEUTRAL_VALUE}>Category-neutral</option>
      </select>

      <select
        aria-label="Filter by mode"
        value={search.mode ?? ""}
        onChange={(event) => handleModeChange(event.target.value)}
        className="rounded-md border border-border bg-surface px-2 py-1 text-sm text-foreground"
      >
        <option value="">All modes</option>
        <option value="generic">Generic</option>
        <option value="activative">Activative</option>
      </select>

      <input
        aria-label="Search by task or manifest id"
        type="text"
        value={q}
        onChange={(event) => handleQChange(event.target.value)}
        placeholder="Search task or manifest id…"
        className="rounded-md border border-border bg-surface px-2 py-1 text-sm text-foreground"
      />
    </div>
  );
}
