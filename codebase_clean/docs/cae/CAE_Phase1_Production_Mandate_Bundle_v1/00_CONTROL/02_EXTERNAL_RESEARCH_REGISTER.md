# External Research / Reference Register

These are reference inputs, not CAE authorities. CAE constitutions remain higher authority.

## Runtime / agent systems

1. Pi
   https://github.com/earendil-works/pi
   Required reads:
   - `packages/agent/docs/harness-v2.md`
   - `packages/agent/docs/harness-v2-state-machine.md`
   - runtime/hook/extension documentation relevant to implementation

2. eve
   https://github.com/vercel/eve
   Required reads:
   - `AGENTS.md`
   - `docs/README.md`
   - `docs/reference/project-layout.md`
   - `docs/subagents.mdx`
   - `docs/guides/hooks.md`
   - agent config/context-control docs relevant to package composition

## Knowledge systems

3. Open Knowledge Format
   https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf
   Required:
   - `okf/SPEC.md`

4. Cole Medin knowledge base example
   https://github.com/coleam00/cole-medin-knowledge-base
   Required:
   - `SCHEMA.md`
   - `index.md`
   - representative `concepts/`, `entities/`, `sources/`, and raw-source conventions

5. Karpathy LLM wiki reference
   https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
   Required: full gist where used by knowledge-base package design.

## Hook authoring

6. Hook creation Skill
   https://github.com/coleam00/skills/blob/main/.claude/skills/hooks-create/SKILL.md
   Required full read before authoring CAE hook conventions or hook-builder work.

## Context / memory alternatives

7. Redis Iris demo
   https://github.com/coleam00/redis-iris-agent

8. Redis Iris Context Engine
   https://redis.io/docs/latest/develop/ai/context-engine/

9. Redis Iris quickstart
   https://redis.io/tutorials/getting-started-with-redis-iris/

Redis is an evaluated option, not selected architecture. The implementation bundle must not
introduce Redis merely because the external demo exists.

## Stateful agent research

10. StateM
    https://arxiv.org/pdf/2608.15089
    Required:
    - full paper
    - especially the control surface, runtime/control-profile distinction, explicit state
      machine, hooks/checks/repair, recovery, and failure-driven harness optimization sections.

## Use rule

External references may provide patterns. They may not override CAE source truth,
constitutions, canonical object authority, operator decisions, or repository-specific
implementation constraints.
