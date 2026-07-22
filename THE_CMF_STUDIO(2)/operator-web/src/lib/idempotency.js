export function makeIdempotencyKey(action, targetId = "global") {
  const random =
    typeof crypto !== "undefined" && crypto.randomUUID
      ? crypto.randomUUID()
      : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  return `${action}:${targetId}:${random}`;
}

export function getActorId() {
  return import.meta.env.VITE_SUPERVISUAL_ACTOR_ID || "operator_local";
}

export function withCommandMeta(payload = {}, action = "supervisual.action", targetId = "global") {
  return {
    actor_id: payload.actor_id || getActorId(),
    idempotency_key: payload.idempotency_key || makeIdempotencyKey(action, targetId),
    ...payload,
  };
}
