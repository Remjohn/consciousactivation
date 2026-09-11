---
name: script_generation
description: Passive skill for generating script scene turns from verified editorial context and voice DNA.
version: 1.0.0
maturity: PRODUCTION
lane: COMPOSER
inputs:
  - jit_authoring_request
outputs:
  - script_proposal
---

# Script Generation Skill

This skill provides deterministic prompt templates and heuristic constraints for composing dialogue scenes and audio turns.
It is completely passive and flat; mutations are executed strictly by typed runtime operations.
