# Phase 7 Runtime Contracts

## Contract: ArchetypeEligibilityAssessment

Input: EdgeProduct + state + registry  
Output: typed list of eligible/ineligible archetypes with reasons.

## Contract: ArchetypeContainerSelection

Input: eligible archetypes + scoring rules  
Output: selected archetype + rejected alternatives + score/decision trace.

## Contract: SubliminalFunctionStack

Input: Edge + archetype + state + SFL registry  
Output: bounded stack of canonical functions with weights and intended effects.

## Contract: ArchetypeProgramContract

Input: edge + archetype + SFL + depth + directives  
Output: complete structural/perceptual constraint envelope.

## Contract: SemanticProgram

Input: validated contract  
Output: Phase 8 consumable IR, free of concrete scene implementation.

## Contract: FailureRepair

Input: typed failure + affected object + evidence  
Output: targeted repair plan or escalation.

## No hidden side effects

Runtime contracts must not silently mutate canonical definitions. State changes are written to explicit dynamic/event tables.
