export function SuperVisualProviderJobsPanel({ displayPayload = {}, lineage = {} }) {
  const blueprints = displayPayload.provider_blueprints || [];
  const jobs = displayPayload.provider_jobs || displayPayload.provider_job_receipts || [];
  const lineageBlueprints = lineage.provider_job_blueprint_ids || [];
  const lineageReceipts = lineage.provider_job_receipt_ids || [];

  return (
    <section className="sv-card">
      <div className="sv-panel-header">
        <div>
          <p className="sv-eyebrow">Materialization</p>
          <h3>Provider Jobs</h3>
        </div>
        <span>{jobs.length || lineageReceipts.length} receipts</span>
      </div>

      <div className="sv-mini-grid">
        <div>
          <strong>Blueprints</strong>
          {(blueprints.length ? blueprints : lineageBlueprints).length ? (
            <ul>
              {(blueprints.length ? blueprints : lineageBlueprints).map((item, index) => (
                <li key={item.provider_job_blueprint_id || item || index}>
                  {item.provider_job_blueprint_id || item}
                </li>
              ))}
            </ul>
          ) : (
            <p className="sv-muted">None yet.</p>
          )}
        </div>
        <div>
          <strong>Receipts</strong>
          {(jobs.length ? jobs : lineageReceipts).length ? (
            <ul>
              {(jobs.length ? jobs : lineageReceipts).map((item, index) => (
                <li key={item.provider_job_receipt_id || item || index}>
                  {item.provider_job_receipt_id || item}
                </li>
              ))}
            </ul>
          ) : (
            <p className="sv-muted">None yet.</p>
          )}
        </div>
      </div>
    </section>
  );
}
