---
name: workspace_boundary_verifier
description: Passive, flat Canonical Skill for verifying tenant workspace isolation boundaries.
version: 1.0.0
---

# Workspace Boundary Verifier Skill

## Purpose
Verifies that all tenant operations, queries, and aggregates adhere strictly to PostgreSQL RLS workspace_id scope.

## Rules
- Flat skill only: no sub-skills or subagent delegation.
- Enforce strict rejection of cross-workspace entity references.
