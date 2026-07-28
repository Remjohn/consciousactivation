import type { CategoryBindingDetail } from "../../api/types";

function Row({ label, value }: { readonly label: string; readonly value: string }) {
  return (
    <div className="mt-1 flex gap-2 text-sm">
      <dt className="w-56 shrink-0 text-muted-foreground">{label}</dt>
      <dd className="break-all text-foreground">{value}</dd>
    </div>
  );
}

export function GovernancePanel({ binding }: { readonly binding: CategoryBindingDetail }) {
  return (
    <section className="mt-6">
      <h2 className="font-semibold text-foreground">Governance record</h2>
      {binding.applicability === "NOT_APPLICABLE" ? (
        <p className="mt-2 text-sm text-muted-foreground">
          {binding.basis ?? "Harness is category-neutral (generic mode)."}
        </p>
      ) : (
        <dl className="mt-2">
          <Row label="Harness id" value={binding.harness_id} />
          <Row label="Harness version" value={binding.harness_version} />
          <Row label="Category" value={`${binding.category_name} (${binding.category_id})`} />
          <Row label="Category registry version" value={binding.category_registry_version} />
          <Row label="Category registry hash" value={binding.category_registry_hash} />
          <Row label="Constitutional authority ref" value={binding.constitutional_authority_ref} />
          <Row label="Runtime law" value={binding.runtime_law} />
          <Row label="Harness development law" value={binding.harness_development_law} />
          <Row label="Semantic lineage refs" value={binding.semantic_lineage_refs.join(", ") || "—"} />
          <Row label="Wrong-reading locks" value={binding.wrong_reading_locks.join(", ") || "—"} />
          <Row label="Certification state" value={binding.certification_state} />
          <Row label="Production ready" value={binding.production_ready ? "Yes" : "No"} />
          <Row label="Certified" value={binding.certified ? "Yes" : "No"} />
          <Row label="Binding hash" value={binding.binding_hash} />
        </dl>
      )}
    </section>
  );
}
