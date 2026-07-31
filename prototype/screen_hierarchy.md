# VyapaarSetu — Screen Hierarchy & Viewport Specifications

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Purpose:** Outlines screen z-index layering, modal hierarchy, and viewport breakpoint rules.

---

## 1. Z-Index Overlay Hierarchy

1. **Base Canvas (z-index: 0):** Background grid and gradient canvas.
2. **View Panels (z-index: 10):** Primary dashboard content grids and data tables.
3. **Sticky Header & Sidebar (z-index: 50):** Navigation controls and search filter bar.
4. **Side Inspection Drawers (z-index: 100):** SKU movement history drawer, vendor rating details drawer.
5. **Modal Overlays (z-index: 500):** Escrow payment confirmation, GSTIN verification modal.
6. **Toast Alerts (z-index: 1000):** Global notification popups.
