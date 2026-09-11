---
name: outcome_empirical_hunter
description: "Passive flat skill collecting empirical outcome performance metrics, emitting EvaluationReceipts, and applying anti-reward-hacking checks."
version: 1.0.0
authority_lane: HUNTER
---

# Outcome Empirical Hunter Skill

## Overview
This skill collects real-world performance observations from distribution channels.

## Execution Rules
1. Query distribution telemetry for empirical metrics (views, retention, completions).
2. Compute predicted vs observed delta and emit `EvaluationReceipt`.
3. Reject viral engagement without evidence truth (`EngagementWithoutTruthError`).
4. Reject sensationalized or misleading context (`MisleadingContextRewardHackError`).
5. Expose polarized disagreement spread to prevent averaging laundering.
