# Hotfix V3.3 — Canonical-State and Authority-Stage Recovery

## Repository diagnosis

The current repository contains:

- Prompt 01 authority convergence;
- Prompt 02 reconciliation, writing queue, packets, dependency DAG, and explicit specification-work authorization;
- a committed Prompt 02B missing-input report;
- no committed `V2_1_SPEC_WRITING_FACTORY` directory.

The missing Prompt 03 controller reports were therefore ephemeral or uncommitted agent-run artifacts. They cannot be mandatory canonical recovery inputs.

The repository also records:

- V2.1 candidate authority is pending ratification;
- Prompt 02 specification work is explicitly authorized;
- Prompt 03 is the next permitted specification-writing action;
- implementation and production remain unauthorized.

## Correct workflow

- Use committed Prompt 02 records to rederive dependency stages and writing waves.
- Preserve absent Prompt 03 logs as `EPHEMERAL_EXECUTION_LOG_NOT_PERSISTED`.
- Do not reconstruct them.
- Do not require final ratification for WRITE/AUDIT/REVISE/RE-AUDIT when explicit specification-work authority exists.
- Require ratification before `ACCEPTED_FOR_BUILD`, Development Capsules, and implementation.
- Retarget VAE cross-product specs to Program Control proposals while VAE `AGENTS.md` prohibits direct Tech Spec writes.

## Immediate action

Run Prompt 02C, then corrected Prompt 03.

Do not restore nonexistent logs. Do not rerun Prompt 01 or broad Prompt 02.
