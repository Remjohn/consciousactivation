# Provider Security and Cost Policy V1

Never commit provider secrets.

Logs may store payload hashes, provider request IDs, route IDs, frame profile, composition role, and normalized error codes.

Logs should avoid raw API keys, full source transcripts, identity-sensitive image URLs, private brand assets, and unredacted prompts with confidential context.

Real paid provider calls require operator approval, a trusted auto-approval policy, or fake-provider test mode.
