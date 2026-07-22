export function SuperVisualBlockersPanel({ blockers = [] }) {
  if (!blockers.length) {
    return (
      <div className="sv-blockers is-clear">
        <strong>No blockers</strong>
        <span>The backend has not reported blocking issues.</span>
      </div>
    );
  }

  return (
    <div className="sv-blockers">
      <strong>Runtime blockers</strong>
      {blockers.map((blocker) => (
        <div key={blocker.id} className={`sv-blocker is-${blocker.severity}`}>
          <span>{blocker.severity}</span>
          <p>{blocker.message}</p>
          {blocker.code ? <small>{blocker.code}</small> : null}
        </div>
      ))}
    </div>
  );
}
