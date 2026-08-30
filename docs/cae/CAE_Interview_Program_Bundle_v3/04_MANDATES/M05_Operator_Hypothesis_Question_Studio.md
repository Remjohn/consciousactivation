# M05 — Operator Hypothesis & Question Studio

**Status:** PROPOSED
**Depends on:** M04
**Primary requirements:** FR-IP-008, FR-IP-009

## Objective

Implement the Operator control surface that reviews candidate hypotheses/questions before Brief launch.

## Required workflow

`candidate field → inspect provenance → KEEP / REJECT / EDIT / REGENERATE / DEFER / LOCK → feedback → constrained alternatives → assemble 16–24 → compile existing Brief → explicit approval → launch`

## Required UI information

Show, where supported by real data:

- upstream hypothesis reference;
- audience cognitive-island/current-state alignment;
- Guest territory;
- world/research signal;
- collision statement;
- edge/tension;
- desired evidence;
- question objective;
- mechanism coalition;
- expected response shape;
- archetype/format/narrative-role compatibility;
- diagnostics;
- provenance and current version.

## Regeneration contract

The regeneration endpoint/service must receive explicit locked dimensions. The system must preserve every locked field and only change unlocked dimensions. Return 3–5 alternatives when enough valid alternatives exist; do not manufacture five weak answers merely to satisfy a count.

## Authorization

Client-side `approved` or `selected` fields are not authoritative. Approval must be verified server-side through the current Operator identity/auth/persistence path.

## Concurrency

Handle stale-version edits, duplicate submissions, and competing Operator edits according to the repository's current versioning conventions. No silent last-write-wins behavior when it would erase an explicit newer Operator decision.

## Required tests

- real candidate retrieval;
- real persistence;
- reject/edit/regenerate/lock;
- stale write rejection;
- idempotent duplicate action;
- unauthorized approval rejection;
- rejected candidate absent from launch payload;
- fresh Brief readback after compile.

## Stop conditions

Stop if no authoritative owner exists for persistent feedback or Operator decision state.
