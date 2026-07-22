export function SuperVisualStatusRail({ items = [] }) {
  return (
    <div className="sv-status-rail">
      {items.map((item) => (
        <div key={item.id} className={`sv-status-item is-${item.state}`}>
          <span className="sv-status-dot" />
          <span>{item.label}</span>
        </div>
      ))}
    </div>
  );
}
