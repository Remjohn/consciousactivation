# Program / Agent / Harness Package Convention

The filesystem is an authoring/composition surface. Canonical CAE state remains in CAE-authoritative
storage/registries.

## Program package

programs/<program-id>/
    program.md
    manifest.yaml
    harness/
    agents/
    operations/
    evals/
    references/

## Harness package

harness/
    manifest
    state-machine
    policies
    hooks
    checks
    recovery
    agents
    atomic/

## Agent package

agents/<agent-id>/
    CAE.md
    instructions.md
    skills/
    subagents/
    tools/
    connections/
    extensions/
    evals/

## Rules

- `CAE.md` carries local persistent governance/context constraints.
- `instructions.md` carries role/work behavior.
- `SKILL.md` carries a Canonical Skill procedure; it remains passive.
- Agent packages cannot redefine canonical CAE authority.
- Sub-agents are locally isolated specialists and inherit only explicitly composed capabilities.
- Skills compose flatly: a Skill may not invoke another Skill.
- Hooks enforce deterministic runtime guarantees; they do not become an alternate ontology.
- Program manifests are compositional metadata and may be compiled into runtime bindings.
- Canonical artifacts and state never live only on disk as Markdown.
- No package structure may create a parallel source of truth.
