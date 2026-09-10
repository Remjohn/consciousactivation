# Surgical Adaptive Cloning Prompt

Use this for external-repository extraction mandates.

```text
You are performing a surgical adaptive-cloning session for CAE mandate [MANDATE_ID].

Do not clone the target repository wholesale. Start from the mandate's functional requirements and inspect only the exact upstream components needed to satisfy them.

For each adopted capability record:
- upstream repository URL
- exact commit/tag
- license
- exact file/component/symbol
- observable behavior
- dependencies
- CAE functional requirement satisfied
- CAE contract boundary
- what is deliberately excluded

Then extract/adapt the smallest useful component or reference implementation. The result must be independently inspectable and testable without being merged into the canonical CAE architecture.

Produce:
COMPONENT_CONTRACT.yaml
AGENT_HANDOFF.md
tests/evidence
source metadata
known limitations
integration instructions

Do not silently copy provider-specific generation logic, database authority, semantic ontology, design-system authority, or unrelated UI. Do not claim the component is production-integrated.

The component will be composed later by an explicit CAE assembly mandate after compatibility review.
```
