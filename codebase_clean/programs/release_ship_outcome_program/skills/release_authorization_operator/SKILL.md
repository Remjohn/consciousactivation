---
name: release_authorization_operator
description: "Passive flat skill governing backend-authoritative human operator release gates and manifest signing."
version: 1.0.0
authority_lane: COMMANDER
---

# Release Authorization Operator Skill

## Overview
This skill implements the authoritative human operator gate governing candidate release.

## Execution Rules
1. Operator approval is backend-authoritative and recorded with an immutable authorization record.
2. Verify target distribution channels.
3. Compute SHA-256 release manifest digest.
4. Agent chat completion text is not evidence of authorization.
