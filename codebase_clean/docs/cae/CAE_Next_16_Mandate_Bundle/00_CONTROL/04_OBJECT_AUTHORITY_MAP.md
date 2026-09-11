# Object / Authority Map for M49–M64

| Object / component | Existing CAE evidence | Wave action |
|---|---|---|
| Agent | `AgentMemberSpec`, `SubagentSpec`, `CompiledAgentPackage` | M49–M50 formalize canonical registry/package |
| CAE.md context | `context_capsule.py`, existing Program `CAE.md` | M51 formalizes ancestry resolution |
| JITContextCapsule | existing runtime object | M52 reuses it; does not replace it |
| AgentInvocation | no proven first-class canonical invocation boundary | M52 establishes it |
| Program | Program manifests + operator runtime | M53 binds Agents to phases |
| Skill | existing Skill loader/registry and passive Skills | preserve |
| Workflow | `RuntimeWorkflowCompiler`, scheduler, run service | M57–M60 formalize/control it |
| Step Contract | runtime node/input/output contracts | M60 consolidates into explicit step contract |
| State | existing CAE State/transition model | preserve |
| Hook | existing hook runtime | preserve |
| Receipt | existing CAE receipt/evidence | extend for invocation/gates as needed |
| Agent Session | session/delegation fields exist in runtime | M56 promotes independently addressable session concept |
| Visualizer | current CAE Studio/operator surfaces + trace data | M63 converges observable read model |

## Constitution rule

Runtime classes are not automatically constitutional objects. Each mandate must distinguish an object that owns canonical meaning from an implementation class that realizes an existing object.
