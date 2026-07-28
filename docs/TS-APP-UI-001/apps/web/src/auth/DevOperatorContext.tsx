import { createContext, useContext, type ReactNode } from "react";

// NOT AUTHENTICATION. TS-APP-API-001 has no auth routes yet (see its own
// "Out of scope"). This exists so every future component has one place to read
// "who is the operator" from, instead of inventing its own placeholder.
interface DevOperatorActor {
  readonly actor_id: string;
  readonly actor_type: "human";
  readonly product_id: string;
  readonly workflow_role: "operator";
}

const DEV_OPERATOR: DevOperatorActor = {
  actor_id: "dev-operator-local",
  actor_type: "human",
  product_id: "conscious-activations-web",
  workflow_role: "operator",
};

const DevOperatorContext = createContext<DevOperatorActor>(DEV_OPERATOR);

export function DevOperatorProvider({ children }: { children: ReactNode }) {
  return (
    <DevOperatorContext.Provider value={DEV_OPERATOR}>
      {children}
    </DevOperatorContext.Provider>
  );
}

// Standard Context+hook co-location; useOperator has to live beside the
// context it reads, which trips fast-refresh's "only export components" rule.
// eslint-disable-next-line react-refresh/only-export-components
export function useOperator(): DevOperatorActor {
  return useContext(DevOperatorContext);
}

export type { DevOperatorActor };
