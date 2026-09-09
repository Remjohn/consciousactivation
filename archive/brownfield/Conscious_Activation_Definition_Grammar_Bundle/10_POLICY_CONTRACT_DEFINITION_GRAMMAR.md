# Policy / Contract Definition Grammar Protocol

## Artifact class

`POLICY_CONTRACT`

## Purpose

Defines binding rules governing permissions, obligations, prohibitions, priorities, exceptions, validation, and failure handling.

## Definition grammar

Use:

**Jurisdiction + Purpose + Definitions + Obligations (MUST) + Permissions (MAY) + Prohibitions (MUST NOT) + Priority + Exceptions + Failure Handling + Validation**

## Legal language

Policies should preferentially use explicit deontic terms:

- `MUST`
- `MUST NOT`
- `MAY`
- `MAY NOT`
- `SHOULD`
- `SHOULD NOT`
- `ONLY IF`
- `UNLESS`

## Required sections

1. Scope
2. Definitions
3. Authority
4. Obligations
5. Permissions
6. Prohibitions
7. Priority / conflict resolution
8. Exception handling
9. Validator obligations
10. Error routing
11. Escalation
12. Audit / receipt requirement

## Examples

Civil Code articles, Directional Integrity Policies, Brand Influence Policies, Scene constraints, execution contracts.

## Hard negatives

- vague recommendation masquerading as policy
- conflicting rules without priority
- policy that cannot be validated
- policy with no failure route
