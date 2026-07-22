import { SuperVisualBlockersPanel } from "./SuperVisualBlockersPanel";
import { SuperVisualEvalPanel } from "./SuperVisualEvalPanel";
import { SuperVisualProviderJobsPanel } from "./SuperVisualProviderJobsPanel";
import { SuperVisualReferenceBoardPanel } from "./SuperVisualReferenceBoardPanel";

export function SuperVisualInspector({ viewModel, onRefresh }) {
  return (
    <aside className="sv-inspector">
      <section className="sv-card">
        <div className="sv-panel-header">
          <div>
            <p className="sv-eyebrow">Inspector</p>
            <h3>{viewModel.variantLabel}</h3>
          </div>
          <button className="sv-button sv-button-small" onClick={onRefresh}>
            Refresh
          </button>
        </div>

        <dl className="sv-definition-list">
          <dt>Status</dt>
          <dd>{viewModel.status}</dd>
          <dt>Step</dt>
          <dd>{viewModel.currentStep}</dd>
          <dt>Project</dt>
          <dd>{viewModel.project?.supervisual_project_id || "—"}</dd>
          <dt>Variant</dt>
          <dd>{viewModel.currentVariant?.supervisual_variant_id || "—"}</dd>
        </dl>
      </section>

      <SuperVisualBlockersPanel blockers={viewModel.blockers} />
      <SuperVisualReferenceBoardPanel displayPayload={viewModel.displayPayload} lineage={viewModel.lineage} />
      <SuperVisualProviderJobsPanel displayPayload={viewModel.displayPayload} lineage={viewModel.lineage} />
      <SuperVisualEvalPanel displayPayload={viewModel.displayPayload} lineage={viewModel.lineage} />
    </aside>
  );
}
