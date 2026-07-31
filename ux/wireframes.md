# VyapaarSetu — Comprehensive Wireframe Specifications

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Purpose:** Details low-fidelity and high-fidelity layout specifications for all primary platform views across desktop and mobile viewports.

---

## 1. Core Screen Layout Wireframe Specifications

### Screen 1: Home Dashboard (`/dashboard`)
- **Header:** Top navigation bar with persistent search input, notifications bell badge, currency switcher (INR/USD), and merchant store selector.
- **Top Row (4 Metric Cards):**
  - Card 1: Gross Sales (₹) with MoM delta pill (+14.2%)
  - Card 2: Orders Fulfilled with SLA completion meter (98.4%)
  - Card 3: Escrow Vault Balance with "View Vault" action button
  - Card 4: Inventory Reorder Risk counter (Badge alert: 3 items)
- **Central Region:**
  - Left (65%): Dual-axis revenue vs margin interactive line graph.
  - Right (35%): Recent activities feed & real-time webhook alerts log.
- **Footer:** Quick action buttons (`+ New Purchase Order`, `+ Add Product SKU`, `Download Financial Audit`).

---

### Screen 2: Start Business & Onboarding (`/start-business`)
- **Layout:** Stepper layout with progress indicator (Steps 1–4).
  - Step 1: Merchant KYC & Store Verification (GSTIN, PAN, Bank Details).
  - Step 2: Store Category & Target Region Selection.
  - Step 3: Initial Inventory Import (CSV drag-and-drop or Tally/Zoho integration).
  - Step 4: Payment Escrow Vault Setup & Banking Partner Authorization.
- **Micro-Interactions:** Inline GSTIN validation check mark; auto-population of merchant address from official registry.

---

### Screen 3: Run Business & Inventory Command (`/run-business`)
- **Layout:** Split-screen layout.
  - Left Panel: Categorized SKU list table with column sorting (Product Name, Stock Level, Age Days, Unit COGS, Reorder Threshold).
  - Right Side Drawer: Selected SKU deep-dive showing inventory movement logs, warehouse location map, and dynamic pricing optimizer toggle.
- **Action Triggers:** "Dispatch PO" modal trigger with automated vendor SLA matching.

---

### Screen 4: Sell Store & M&A Marketplace (`/sell-store`)
- **Layout:** Marketplace storefront listing grid with filters (Category, Monthly ARR Range, Health Score, Valuation Multiple).
- **Store Listing Card Components:**
  - Store Title & City Tag (`Platinum Tier Merchant - Mumbai`)
  - Monthly Revenue Badge (e.g., `₹850,000 / mo`)
  - Solvency & Health Score Ring (`Health Score: 92/100`)
  - Valuation Multiple (`Valuation: ₹24.5M - 2.4x ARR Multiple`)
  - Action Button: `Request Confidential Teaser` / `Submit Buy Offer (Escrow)`

---

### Screen 5: Grow Store & Marketing Intelligence (`/grow-store`)
- **Layout:** Marketing ROI command center.
  - Top Section: Campaign performance breakdown (Meta, Google, WhatsApp) with spend vs revenue waterfall chart.
  - Middle Section: Customer RFM Cohort Matrix heatmap with high-value buyer segment tags.
  - Bottom Section: AI recommendation engine suggestions (e.g., "Launch WhatsApp bundle campaign for Category: Electronics to boost AOV by ₹1,200").

---

### Screen 6: Vendor Marketplace (`/vendors`)
- **Layout:** Supplier discovery grid featuring verified vendor cards.
  - Vendor Card Details: Vendor Name, Category, Verified SLA % Badge, Quality Star Rating, Minimum Order Quantity (MOQ), Lead Time (Days).
  - Action: `Request RFQ Quote` / `Assign Fulfillment Order`.

---

### Screen 7: Analytics Command Center (`/analytics`)
- **Layout:** Embedded Power BI layout canvas with tab navigation bar (Executive, Inventory, Sales, Vendors, Cohorts, Operations).
- **Controls:** Floating date range filter bar with export to PDF/Excel controls.

---

### Screen 8: Settings & Security (`/settings`)
- **Layout:** Tabbed settings drawer covering Security & 2FA, API Webhooks, Banking Escrow Accounts, User Role Permissions (Admin, Manager, Accountant).
