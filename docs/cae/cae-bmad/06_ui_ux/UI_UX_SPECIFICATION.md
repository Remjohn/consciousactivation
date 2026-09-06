# UI/UX Specification — Conscious Activation Engine UI/UX

**Artifact ID:** CAE-ART-UIUX-001  
**Status:** APPROVED  

---

## 1. Operator Studio Views

| View ID | Title | Purpose | Primary Components |
|---|---|---|---|
| `VIEW-OPERATOR-STUDIO` | Master Operator Studio Dashboard | Central command interface for initiating programs, reviewing evidence, and managing operator gates. | ProgramNavigator, GateApprovalModal, TelemetryHUD |
| `VIEW-INTERVIEW-TELEMETRY` | Dynamic Interview Telemetry Monitor | Live visual tracking of guest psychological stance, question tension, and turn-by-turn hypothesis testing. | GuestVectorVisualizer, HypothesisHeatmap, TurnSequenceController |
| `VIEW-EVIDENCE-INSPECTOR` | Evidence & Provenance Inspector | Cryptographic receipt inspection, source hash verification, and wire-copy de-inflation inspector. | ReceiptVerificationBadge, SourceLineageViewer, RawBytesInspector |

---

## 2. Atomic Harness Design Tokens

### Color Tokens
- `color-bg-primary: #0A0D14`
- `color-surface-card: #121824`
- `color-accent-amber: #F59E0B`
- `color-status-verified: #10B981`
- `color-status-contradicted: #EF4444`

### Typography Tokens
- `font-family-mono: 'JetBrains Mono', monospace`
- `font-family-sans: 'Inter', -apple-system, sans-serif`
- `font-size-telemetry: 11px`

### Telemetry Monitors
- `Monitor-Guest-Stance: 60Hz vector refresh`
- `Monitor-CAS-Version: Optimistic lock state indicator`
- `Monitor-Gate-Status: Pulse warning on unratified promotion`

---

## 3. Interaction Flows

### Operator Gate Promotion Flow
- **Trigger:** `Agent completes mandate step and requests promotion.`
- **Steps:**
  1. Agent emits gate packet (OPERATOR_GATE_Mxx.md)
  1. UI alerts operator with pulse warning badge
  1. Operator reviews automated test output and diff matrix
  1. Operator clicks Ratify or Rejects with feedback
- **Error Handling:** If validation fails, promotion button is disabled and failure log is presented in modal.

---

## 4. Accessibility Standards

WCAG 2.1 AA compliant, full keyboard shortcut navigation, high-contrast dark telemetry theme.
