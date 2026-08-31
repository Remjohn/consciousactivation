# Operational Instructions: Release / Ship / Outcome Program

## 1. Lifecycle Execution
1. **Initialize Session:**
   - Create session aggregate with valid candidate and artifact reference.
2. **Verify Final QA (`ANALYST` Lane):**
   - Verify Semantic QA and Render QA results against verbatim evidence quotes and wrong-reading locks.
   - Transitions state to `QA_VERIFIED`.
3. **Authorize Release (`COMMANDER` Lane):**
   - Backend-authoritative operator decision (`APPROVED`).
   - Transitions state to `RELEASE_AUTHORIZED`.
4. **Execute Shipment (`COMPOSER` Lane):**
   - Pack and dispatch artifact to target distribution channel.
   - Transitions state to `SHIPPED`.
5. **Capture Outcome (`HUNTER` Lane):**
   - Observe real-world performance metrics. Emits `EvaluationReceipt`.
   - Transitions state to `OUTCOME_CAPTURED`.
6. **Propose Learning (`ANALYST` Lane):**
   - Distill recurring performance patterns into advisory `LearningProposal` recommendations.
   - Transitions state to `LEARNING_PROPOSED`.
7. **Ratify Proposal (`COMMANDER` Lane):**
   - Operator reviews and ratifies advisory proposal.
