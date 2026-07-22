import { useState } from "react";

export function SuperVisualCommandBar({ onSubmitRevision, disabled }) {
  const [feedback, setFeedback] = useState("");

  async function submit(event) {
    event.preventDefault();
    const trimmed = feedback.trim();
    if (!trimmed) return;
    await onSubmitRevision?.(trimmed);
    setFeedback("");
  }

  return (
    <form className="sv-command-bar" onSubmit={submit}>
      <textarea
        value={feedback}
        disabled={disabled}
        onChange={(event) => setFeedback(event.target.value)}
        placeholder="Ask for a typed revision: make it more editorial, replace proof object, increase negative space…"
      />
      <button className="sv-button" disabled={disabled || !feedback.trim()}>
        Submit revision
      </button>
    </form>
  );
}
