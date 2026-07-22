export function SuperVisualCompositionPanel({ displayPayload = {}, onLockComposition, canLock, active }) {
  const options =
    displayPayload.composition_options ||
    displayPayload.composition_hypotheses ||
    [];

  return (
    <section className="sv-card">
      <div className="sv-panel-header">
        <div>
          <p className="sv-eyebrow">Composition</p>
          <h3>Options</h3>
        </div>
        <span>{options.length} option{options.length === 1 ? "" : "s"}</span>
      </div>

      {options.length ? (
        <div className="sv-option-list">
          {options.map((option, index) => {
            const id = option.composition_hypothesis_id || option.id || `option_${index + 1}`;
            return (
              <div key={id} className="sv-option-card">
                <strong>{option.title || option.name || `Option ${index + 1}`}</strong>
                <p>{option.rationale || option.description || "Backend composition option."}</p>
                <button
                  className="sv-button sv-button-small"
                  disabled={!canLock || active}
                  onClick={() => onLockComposition?.({ composition_decision_receipt_id: id })}
                >
                  Lock
                </button>
              </div>
            );
          })}
        </div>
      ) : (
        <p className="sv-muted">No composition options in the current snapshot.</p>
      )}
    </section>
  );
}
