# VAE Delegation + Visual Asset Runtime Governance (CAE.md)

## Authority & Non-Negotiables
1. **Four-Lane Authority Separation:**
   - `COMMANDER`: Admits visual asset demands, manages repair boundaries, and issues backend-authoritative Pipeline `ResultAcknowledgement` receipts with consumption authorization.
   - `HUNTER`: Evaluates demand obligations, binds workcell stages, and compiles the VAE production plan.
   - `COMPOSER`: Materializes multi-layer visual outputs, ComfyUI workflow execution graphs, and segmentation/matting references.
   - `ANALYST`: Conducts technical/render evaluation, geometry validation, wrong-reading lock compliance checks, and dual-axis semantic QA auditing.
2. **Consumption Authority Strict Invariant:**
   - VAE produces candidates and technical evaluation findings, but **never** asserts downstream consumption authority.
   - Downstream consumption authority belongs exclusively to the Content Harness Pipeline via `ResultAcknowledgement`.
3. **Dual-Axis QA Separation:**
   - Technical/Render QA (geometry, alpha matting, format dimensions) and Semantic QA (narrative alignment, somatic resonance, anti-centroid integrity) are evaluated on separate axes.
   - A successful render cannot override a failed semantic evaluation.
4. **Lineage Integrity & Anti-Synthetic Defense:**
   - Every delegated visual asset demand MUST trace directly to verified `EvidenceSegment` quotes and turn hashes.
   - Synthetic or mock visual demands fail closed with `SyntheticProductionBlockedError`.
5. **Fail-Closed Workspace Isolation:**
   - Cross-workspace delegation requests are rejected immediately with `WorkspaceScopeViolationError`.
