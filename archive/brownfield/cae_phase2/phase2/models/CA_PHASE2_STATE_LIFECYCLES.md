# Phase 2 State Lifecycles

## Tension / Webhook
latent → corroborating → active → saturated → resolved
                         ↘ blocked
                         ↘ superseded

## Evidence observation
observed → normalized → corroborated | contradicted | unresolved

## Schema hypothesis
hypothesis → candidate → validated → canonicalized
                         ↘ rejected

## Audience / Guest state
observed → inferred → active → superseded
                           ↘ resolved
                           ↘ invalidated

State transitions must be append-only in history and reconstructable from events.
