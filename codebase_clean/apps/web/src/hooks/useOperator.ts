// TS-APP-UI-001 §5 lists src/hooks/useOperator.ts alongside src/auth/DevOperatorContext.tsx
// in scope. The hook itself is implemented in DevOperatorContext.tsx (Stage 6) since it
// needs to sit next to the context object it reads; this file re-exports it so other
// hooks (useHealth.ts, etc.) and this one share a single src/hooks/ import root.
export { useOperator } from "../auth/DevOperatorContext";
export type { DevOperatorActor } from "../auth/DevOperatorContext";
