---
name: shipment_distribution_composer
description: "Passive flat skill handling distribution packaging, channel dispatch, delivery verification, and failure handling."
version: 1.0.0
authority_lane: COMPOSER
---

# Shipment Distribution Composer Skill

## Overview
This skill executes physical and distribution shipment of approved production artifacts.

## Execution Rules
1. Verify prior `RELEASE_AUTHORIZED` operator decision.
2. Package artifact and dispatch to approved distribution endpoint.
3. Emit cryptographic `ShipmentReceipt` on successful delivery.
4. Failed delivery never reports success and halts state progression.
