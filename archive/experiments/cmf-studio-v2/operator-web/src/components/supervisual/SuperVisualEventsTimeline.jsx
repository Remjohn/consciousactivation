export function SuperVisualEventsTimeline({ events = [], onRefresh, loading }) {
  return (
    <section className="sv-card sv-events-card">
      <div className="sv-panel-header">
        <div>
          <p className="sv-eyebrow">Runtime</p>
          <h3>Events</h3>
        </div>
        <button className="sv-button sv-button-small" onClick={onRefresh} disabled={loading}>
          Refresh
        </button>
      </div>

      {events.length ? (
        <div className="sv-events">
          {events.map((event, index) => (
            <div key={event.supervisual_event_id || event.id || index} className="sv-event">
              <strong>{event.event_type || event.type || "event"}</strong>
              <span>{event.created_at || ""}</span>
              {event.actor_id ? <small>{event.actor_id}</small> : null}
            </div>
          ))}
        </div>
      ) : (
        <p className="sv-muted">No events yet.</p>
      )}
    </section>
  );
}
