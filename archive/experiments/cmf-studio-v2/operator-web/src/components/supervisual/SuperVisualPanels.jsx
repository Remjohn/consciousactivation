export function SuperVisualPanel({ kicker, title, children, action }) {
  return (
    <section className="sv-panel">
      <div className="sv-panel-header">
        <div>
          {kicker && <span className="eyebrow">{kicker}</span>}
          <h2>{title}</h2>
        </div>
        {action}
      </div>
      {children}
    </section>
  );
}

export function SuperVisualStatus({ label, tone = "neutral" }) {
  return <span className={`sv-status ${tone}`}>{label}</span>;
}

export function SuperVisualKV({ label, value }) {
  return (
    <div className="sv-kv">
      <span>{label}</span>
      <strong>{value || "Not set"}</strong>
    </div>
  );
}

export function SuperVisualReceiptList({ title, items, empty = "No receipts yet." }) {
  return (
    <div className="sv-receipt-block">
      <h3>{title}</h3>
      {items?.length ? (
        <div className="sv-receipt-list">
          {items.map((item) => (
            <article className="sv-receipt" key={item.receipt_ref || item.eval_receipt_id || item.composition_receipt_id || item.object_ref}>
              <strong>{item.provider_code || item.decision_code || item.object_ref || item.schema_version}</strong>
              <span>{item.output_ref || item.composition_id || item.decision || item.summary}</span>
              <small>{item.deterministic_seed || item.composition_hash || item.eval_receipt_hash || item.written_at}</small>
            </article>
          ))}
        </div>
      ) : (
        <p className="muted-copy">{empty}</p>
      )}
    </div>
  );
}

export function SuperVisualJson({ value }) {
  return <pre className="sv-json">{JSON.stringify(value || {}, null, 2)}</pre>;
}

export function SuperVisualGate({ label, score, blockers }) {
  const passed = Number(score) >= 0.84 && !blockers?.length;
  return (
    <div className={`sv-gate ${passed ? "passed" : "blocked"}`}>
      <div>
        <strong>{label}</strong>
        <span>{Math.round(Number(score || 0) * 100)}%</span>
      </div>
      <small>{passed ? "Gate passed" : blockers?.join(", ") || "Below threshold"}</small>
    </div>
  );
}
