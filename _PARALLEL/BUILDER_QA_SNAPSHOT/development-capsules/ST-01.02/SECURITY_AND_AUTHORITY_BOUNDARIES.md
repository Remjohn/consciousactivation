# Security and Authority Boundaries

- `LOCK_EVIDENCE_WORKSPACE` is deny-by-default. Only a registered human or
  deterministic code actor with an unexpired exact run grant may commit.
- Agents may not commit, widen policy, waive source safety, supply authority, or
  promote evidence. External and evaluator actors have no commit path.
- The adapter has read-only access to the configured repository root and no
  network, provider, secret, GPU, VAE, Delegation-runtime, or publication grant.
- Resolved source paths must remain under the configured root. Symlinks,
  reparse/root escape, absolute archive members, parent traversal, case-fold
  collisions, executables, nested archives, malformed input, and configured
  resource overflows fail closed.
- ZIP members are streamed/hashed within limits and never extracted.
- The source authority/license/privacy values come only from the hash-pinned
  source profile. The Builder does not infer or upgrade authority.
- `consent_policy_required=false` is valid only because this exact source is
  synthetic, repository-owned, and non-personal. Human Reaction material is
  prohibited and would activate HD-006 in another mode.
- The outcome is non-production and non-certified. It does not grant external
  runtime permissions or implementation authority for another Story.
