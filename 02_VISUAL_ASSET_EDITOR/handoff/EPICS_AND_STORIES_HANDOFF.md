# Epics and Stories Handoff

## Prerequisites

Do not create implementation Epics until:

- PRD is approved;
- Architecture is validated;
- supervisory UX contract exists where applicable;
- representative delegation and Format 02 fixtures exist.

## Requirements extraction

The planning workflow must extract all:

- 176 Functional Requirements;
- 70 Non-Functional Requirements;
- Architecture requirements;
- UX design requirements;
- compatibility and migration requirements;
- readiness and benchmark requirements.

## Epic design principles

- Organize around operator, caller, and downstream product value—not databases, APIs, agents, UI, or infrastructure layers.
- Each Epic must deliver a usable end-to-end capability and may depend only on earlier Epics.
- Stories must be vertical, independently testable, and sized for one development-agent context.
- Create entities, infrastructure, and registries only when the first vertical Story needs them.
- Use the Format 02 reference slice as the continuous integration target.

## Likely value themes for Architecture to validate

These are not approved Epics yet:

1. Accept and validate one authoritative Visual Asset Demand.
2. Compile and execute one observable Visual Production Plan.
3. Produce and evaluate a Format 02 character asset.
4. Repair and promote an immutable composition-ready asset.
5. Operate local/cloud visual compute autonomously.
6. Retrieve syntax-aware memory and learn Steering Recipes.
7. Supervise budgets, exceptions, capabilities, and releases.
8. Certify and hand off the Release 1 reference path.

## Coverage requirements

The final Epics document must contain:

- full FR/NFR inventory;
- FR-to-Epic map;
- Architecture and UX requirements;
- Story-to-FR map;
- no forward Story dependencies;
- Given/When/Then acceptance criteria;
- hard-gate and failure examples;
- benchmark and observability acceptance;
- implementation-readiness validation.
