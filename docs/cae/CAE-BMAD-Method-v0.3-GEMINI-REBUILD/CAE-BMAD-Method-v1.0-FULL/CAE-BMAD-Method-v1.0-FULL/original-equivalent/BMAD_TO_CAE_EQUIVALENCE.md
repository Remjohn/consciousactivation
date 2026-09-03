# BMAD → CAE Equivalence / Override Matrix

This file answers the exact question:

**What are we retaining from the original BMAD method, what is mandatory, and what is CAE-specific?**

| Original BMAD capability | CAE treatment | Mandatory? |
|---|---|---|
| `bmad-help` | preserve and add CAE routing | YES |
| `bmad-deep-recon` | preserve; CAE reconstruction is a domain-specific front end | YES |
| `bmad-advanced-elicitation` | preserve; CAE Grill controls product decisions | YES |
| `bmad-review` | preserve; CAE review adds lineage/brownfield/proof lenses | YES |
| `bmad-customize` | preserve | YES |
| brainstorming | retain as optional tool | NO |
| forge-idea | retain as optional | NO |
| party-mode | retain as optional | NO |
| product brief | preserve artifact; CAE adds reconstruction gate | YES |
| PRD | preserve artifact; CAE makes modularity/source lineage mandatory | YES |
| spec | preserve as supporting kernel; CAE product truth does not collapse to SPEC | OPTIONAL |
| UX | preserve | CONDITIONALLY |
| architecture | preserve; CAE brownfield gate required | YES |
| epics/stories | preserve | YES |
| implementation readiness | preserve and add CAE proof/lineage checks | YES |
| create story | preserve | YES |
| dev story | preserve | YES |
| code review | preserve | YES |
| sprint planning/status | preserve for implementation operations | OPTIONAL |
| retrospective | preserve | OPTIONAL |
| project context | preserve; CAE extends it with product-history context | YES |
| documentation helpers | preserve if present; CAE product docs use their own governed structure | OPTIONAL |

## Non-negotiable

A CAE bundle must not achieve specialization by deleting the original BMAD files.

The original repository remains the foundational method library.
CAE adds a stricter product-reconstruction and brownfield entry path.
