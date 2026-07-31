# VyapaarSetu 2026 Executive Power BI Dashboard Specification

> **Public Inspection Guide**: This document provides a complete layout blueprint, visual specification, interaction matrix, and preview layout for the VyapaarSetu Business Operating System Power BI report suite. Anyone reviewing this repository can fully evaluate the design, DAX measures, and decision-support logic without installing Power BI Desktop or requesting tenant access.

---

## 1. Dashboard Architecture (4 Core Report Tabs)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       VYAPAARSETU POWER BI SUITE                            │
├───────────────────┬───────────────────┬───────────────────┬─────────────────┤
│ Tab 1: Executive  │ Tab 2: Channel &  │ Tab 3: Vendor &   │ Tab 4: Store    │
│ Summary           │ Profitability     │ Logistics Health  │ Marketplace     │
└───────────────────┴───────────────────┴───────────────────┴─────────────────┘
```

---

## 2. Tab 1: Executive Summary & MSME Command Center

### ASCII Layout Grid Preview
```
+-----------------------------------------------------------------------------------+
| FILTERS: [Date Range: YTD v] [Store: All v] [Category: Textiles & Apparel v]       |
+-------------------+-------------------+-------------------+-----------------------+
|  TOTAL REVENUE    |    NET PROFIT     |  AVG NET MARGIN   | ESCROW FUNDS HELD     |
|   ₹18.5M (+14.2%) |   ₹4.25M (+18.1%) |     23.0%         |   ₹2.8M (12 Deals)    |
+-------------------+-------------------+-------------------+-----------------------+
| MONTHLY REVENUE & NET PROFIT TREND (LINE + COLUMN CHART)                          |
| [================================================================] Gross Revenue  |
| [----------------------------------------------------------------] Net Profit     |
+-----------------------------------------+-----------------------------------------+
| TOP PERFORMING SKUS BY CONTRIBUTION     | AI ADVISOR INSIGHT & LEAKAGE ALERTS     |
| 1. Handblock Cotton Kurta  ₹2.8M (28%)  | ⚠️ High Shrinkage Alert: Leather Bags  |
| 2. Surat Chanderi Saree    ₹1.9M (19%)  | 💡 AI Rec: Liquidate Low-Margin Cables |
| 3. Kumkumadi Oil           ₹1.2M (12%)  | ✅ Vendor Rating Surge: Jaipur Prints  |
+-----------------------------------------+-----------------------------------------+
```

### Visual Components & Data Bindings
1. **KPI Card Array (Header)**:
   - **Total Gross Revenue**: Measure `[Total Gross Sales]` formatted in INR (Millions), target delta +14.2% YoY.
   - **Net Profit**: Measure `[Net Contribution Margin INR]`, conditional formatting green if > 20%.
   - **Avg Net Margin %**: Measure `[Net Margin Pct]`, formatted as percentage.
   - **Escrow Funds Held**: Measure `[Escrow Volume Held]`, showing active escrow security protection.

2. **Main Visual (Left Center)**:
   - **Chart Type**: Clustered Column & Line Combo Chart.
   - **X-Axis**: `Calendar[MonthYear]`
   - **Y-Axis (Column)**: `[Total Gross Revenue]`
   - **Y-Axis (Line)**: `[Net Profit Margin %]`

3. **Strategic AI Alert Card (Bottom Right)**:
   - Dynamic DAX callout text rendering automated business alerts (e.g., stock shrinkage warnings, category margin dips).

---

## 3. Tab 2: Channel & Profitability Matrix

### Layout & Visual Breakdown
- **Visual 1 (Donut Chart)**: **Revenue Share by Sales Channel** (`Shopify Direct` vs `POS Counter` vs `Amazon IN` vs `Instagram DM`).
- **Visual 2 (Matrix Grid)**: **Channel Net Unit Economics**.
  - Columns: `Channel`, `Gross Orders`, `Gross Revenue`, `COGS`, `Shipping Cost`, `Net Profit`, `Net Margin %`.
  - Conditional Formatting: Background color scale from Red (0% Net Margin) to Dark Emerald Green (≥ 25% Net Margin).
- **Visual 3 (Scatter Plot)**: **Product Price vs Return Rate by Channel**.
  - X-Axis: `Average Unit Price (INR)`
  - Y-Axis: `Return Rate %`
  - Bubble Size: `Total Volume Sold`

---

## 4. Tab 3: Vendor SLA & Logistics Health Tracker

### Layout & Visual Breakdown
- **Visual 1 (Bubble Map / Gauge Matrix)**: **Vendor Composite Health Index**.
  - Displays vendor lead times, defect rates, and escrow verification badges.
- **Visual 2 (Bar Chart)**: **Logistics Carrier On-Time SLA Rate**.
  - Shows `Delhivery` (96%), `BlueDart` (98%), `Shadowfax` (88%), `Ecom Express` (78% - SLA Breached).
- **Visual 3 (Table)**: **Active Escrow Milestone Monitor**.
  - Columns: `Escrow ID`, `Vendor Name`, `Order ID`, `Amount`, `Hold Date`, `SLA Trigger Status`.

---

## 5. Tab 4: Store Marketplace & Valuation Exchange

### Layout & Visual Breakdown
- **Visual 1 (Waterfall Chart)**: **Store Asking Price vs. Annual Net Profit Breakdown**.
- **Visual 2 (Interactive Slicer Matrix)**: **Turnkey Store Listings for Acquisition**.
  - Columns: `Store Name`, `Category`, `Monthly Revenue`, `Profit Margin %`, `Online Share %`, `Asking Price`, `Valuation Multiple`.
  - Filter: Sliders for `Asking Price Range (INR)` and `Minimum Net Margin %`.

---

## 6. Slicer Interactivity Matrix

| Slicer Name | Affected Visuals | Cross-Filtering Behavior |
|---|---|---|
| **Date Range** | All Report Tabs | Filters orders, revenue trends, and SLA timestamps. |
| **Sales Channel** | Tab 1, Tab 2 | Filters product revenue, return rates, and shipping fees. |
| **Vendor Name** | Tab 1, Tab 3 | Isolates catalog products, defect rates, and escrow release status. |
| **Store Status** | Tab 4 | Filters Active vs. For Sale turnkey store listings. |
