# VyapaarSetu — Interactive Clickable Prototype Walkthrough

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Purpose:** Provides a step-by-step interactive testing guide for recruiters, investors, and platform evaluators testing the static showcase and prototype flows.

---

## 1. Fast 3-Minute Evaluation Walkthrough

### Step 1: Open Static Interactive Showcase
- Double click or launch [wireframe-preview.html](wireframe-preview.html) in Chrome, Edge, Safari, or Firefox.
- Observe the persistent dark-glass sidebar, live KPI metric cards (Gross GMV: ₹4.85M, Escrow Locked: ₹1.42M), and real-time SVG chart.

### Step 2: Test Navigation & View Switching
- Click `🚀 Start Business` in the left sidebar ➔ Verify GSTIN verification state (`✓ Verified: Vyapaar Electronics Retail Ltd`).
- Click `📦 Run Business` ➔ Observe live SKU stock inventory table and one-click `Dispatch PO` trigger.
- Click `🏬 Sell Store (M&A)` ➔ Evaluate store listing cards with 2.4x ARR multiple valuations.
- Click `📊 Power BI Analytics` ➔ Review 8-tab Power BI data specification canvas.

---

## 2. Test Journey Scenarios

### Scenario A: Automated Reorder PO Dispatch
1. Go to `Run Business`.
2. Find `INV-6001` (Stock: 12 units).
3. Click `Dispatch PO`.
4. System executes `automation/inventory_sync.py` and `automation/vendor_matching.py` behind the scenes, outputting preferred supplier `Vendor 12 Wholesale Ltd`.

### Scenario B: Buyer-Seller Escrow Milestone Authorization
1. Go to `Home Dashboard`.
2. Inspect `ORD-5001` in the Recent Orders table.
3. Escrow Status reads `Funded` in ICICI Trade Vault.
4. Simulating courier webhook delivery triggers `automation/escrow_workflow.py` to move status to `Released`.
