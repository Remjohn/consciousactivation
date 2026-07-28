import { createFileRoute } from "@tanstack/react-router";
import { useHarnesses } from "../../hooks/useHarnesses";
import { HarnessFilterBar } from "../../components/harness/HarnessFilterBar";
import { HarnessCard } from "../../components/harness/HarnessCard";
import { HarnessLibraryEmptyState } from "../../components/harness/HarnessLibraryEmptyState";
import { HarnessLibraryErrorState } from "../../components/harness/HarnessLibraryErrorState";
import { validateSearch } from "./-validateHarnessSearch";

export const Route = createFileRoute("/harnesses/")({
  validateSearch,
  component: HarnessLibraryPage,
});

function HarnessLibraryPage() {
  const search = Route.useSearch();
  const { data, isLoading, isError, error } = useHarnesses();

  if (isError) return <HarnessLibraryErrorState error={error} />;
  if (isLoading) return <div className="p-8 text-muted-foreground">Loading harnesses…</div>;
  if (data.length === 0) return <HarnessLibraryEmptyState />;

  const filtered = data.filter((h) => {
    if (search.category && h.category_id !== search.category) return false;
    if (search.mode && h.mode !== search.mode) return false;
    if (search.q) {
      const needle = search.q.toLowerCase();
      if (!h.task_id.toLowerCase().includes(needle) && !h.manifest_id.toLowerCase().includes(needle)) {
        return false;
      }
    }
    return true;
  });

  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold text-foreground">Harness Library</h1>
      <HarnessFilterBar />
      <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filtered.map((harness) => (
          <HarnessCard key={harness.definition_id} harness={harness} sourceCategory={search.sourceCategory} />
        ))}
      </div>
    </div>
  );
}
