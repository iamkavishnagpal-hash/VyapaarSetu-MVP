# VyapaarSetu — Interaction Patterns & Behavioral Rules

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Purpose:** Documents standard user interface behavior across inputs, tables, modals, filters, and notification states.

---

## 1. Standard Interaction Patterns

1. **Inline Validation:** All form inputs validate on blur. Invalid inputs display a red outline with descriptive error message below.
2. **Filter Persistence:** Global filter state (Date range, Store ID, Category) persists across tab switches via URL query parameters.
3. **Modal Side Drawers:** Detailed item inspections (e.g., SKU movements, vendor SLA deep-dives) open in a right-sliding drawer (380px width) rather than full page re-nav.
4. **Optimistic Updates:** Status toggle switches (e.g., Enable Automated PO Reorder) update UI immediately while dispatching background API call.
5. **Toast Notifications:** Standard 3-second auto-dismiss alerts for success/failure feedback in bottom-right corner.
