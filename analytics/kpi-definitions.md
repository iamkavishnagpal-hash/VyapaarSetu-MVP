# VyapaarSetu KPI & Growth Metrics Specification

This document defines the core financial, operational, logistics, and marketplace Key Performance Indicators (KPIs) tracked by the VyapaarSetu Business Operating System.

---

## 1. Financial & Profitability KPIs

| KPI Metric Name | Formula / Calculation | Target Benchmark | Business Purpose |
|---|---|---|---|
| **Gross Margin Rate (%)** | `((Gross Revenue - COGS) / Gross Revenue) * 100` | ≥ 40.0% | Measures unit economics health per SKU and category before channel/shipping overhead. |
| **Net Contribution Margin (%)** | `((Gross Revenue - COGS - Shipping - Platform Fees) / Gross Revenue) * 100` | ≥ 18.0% | True bottom-line profit generated per order after channel fulfillment costs. |
| **Average Order Value (AOV)** | `Total Sales Revenue / Total Order Volume` | Product dependent | Indicates basket size and upsell/cross-sell efficiency. |
| **Inventory Shrinkage Rate (%)** | `((Recorded Stock - Physical Audit Stock) / Recorded Stock) * 100` | ≤ 1.0% | Detects theft, breakage, billing errors, or unsynced offline POS leakage. |

---

## 2. Multi-Channel & Operational KPIs

| KPI Metric Name | Formula / Calculation | Target Benchmark | Business Purpose |
|---|---|---|---|
| **Stock Turnover Ratio** | `Annualized COGS / Average Inventory Value` | ≥ 6.0x / year | Measures how efficiently capital tied up in inventory generates sales. |
| **Channel Profit Variance** | `Net Margin % (Online) - Net Margin % (Offline)` | ± 5.0% | Identifies which sales channel yields higher actual profit vs. volume. |
| **Reorder Trigger Ratio** | `(Available Stock + In-Transit Stock) / Reorder Point` | 1.0 - 1.2 | Ensures zero stockout events without over-capitalizing in safety stock. |

---

## 3. Vendor & Supply Chain KPIs

| KPI Metric Name | Formula / Calculation | Target Benchmark | Business Purpose |
|---|---|---|---|
| **Vendor On-Time Delivery Rate (%)** | `(On-Time Delivered Batches / Total Dispatched Batches) * 100` | ≥ 95.0% | Measures vendor reliability for baseline reorder planning. |
| **Vendor Defect Rate (%)** | `(Defective / Rejected Units / Total Inspected Units) * 100` | ≤ 1.5% | Protects product quality before listing on merchant storefronts. |
| **Composite Vendor Health Score** | `(OnTimeRate * 0.40) + ((100 - DefectRate) * 0.40) + (UserRating * 4.0)` | ≥ 85.0 / 100 | Determines whether a vendor qualifies for Escrow Instant Auto-Release. |

---

## 4. Escrow & Store Marketplace KPIs

| KPI Metric Name | Formula / Calculation | Target Benchmark | Business Purpose |
|---|---|---|---|
| **Escrow Settlement Velocity (Days)** | `Average(Release Date - Hold Date)` | ≤ 2.5 Days | Tracks speed of cash release to suppliers and store sellers upon milestone completion. |
| **Store Valuation Multiple (P/E)** | `Asking Price / (Monthly Profit * 12)` | 2.0x - 3.5x | Standardized valuation metric for buying and selling turnkey stores on VyapaarSetu. |
| **P&L Verification Rate (%)** | `(Audited Proven Store Revenue / Claimed Store Revenue) * 100` | 100.0% | Guarantees transparent metrics for business acquisition trust. |
