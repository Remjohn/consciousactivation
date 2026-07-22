export function SuperVisualCanvasPreview({ previewRef, status, displayPayload }) {
  const imageRef = previewRef || displayPayload?.preview_uri || displayPayload?.render?.preview_uri;

  return (
    <section className="sv-canvas-panel">
      <div className="sv-canvas-toolbar">
        <div>
          <p className="sv-eyebrow">Canvas Preview</p>
          <h2>{status?.replaceAll("_", " ") || "draft"}</h2>
        </div>
      </div>

      <div className="sv-canvas">
        {imageRef ? (
          <img src={imageRef} alt="SuperVisual preview" />
        ) : (
          <div className="sv-canvas-placeholder">
            <span>Backend preview will appear here</span>
            <small>Run composition, render, or load a snapshot with preview_ref.</small>
          </div>
        )}
      </div>
    </section>
  );
}
