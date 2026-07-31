# VyapaarSetu — Power BI Enterprise Dashboard Specification

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Target BI Platform:** Power BI Desktop / Power BI Service (Pro/Premium)  
**Data Architecture:** Star Schema Model over PostgreSQL / CSV Ingestion Layer  
**Refresh Schedule:** Scheduled DirectQuery / Incremental Refresh (6x daily)

---

## 1. Data Model Architecture & Star Schema

```
                           ┌─────────────────────────┐
                           │      dim_vendors        │
                           └────────────┬────────────┘
                                        │ (1:N)
┌─────────────────────────┐             ▼             ┌─────────────────────────┐
│      dim_customers      │ ──┐   ┌──────────┐   ┌──  │      dim_stores         │
└─────────────────────────┘   │   │  fact_   │   │    └─────────────────────────┘
                              ├──►│  orders  │◄──┤
┌─────────────────────────┐   │   │          │   │    ┌─────────────────────────┐
│      dim_products       │ ──┘   └────┬─────┘   └──  │      dim_calendar       │
└─────────────────────────┘            │              └─────────────────────────┘
                                       │ (1:N)
                                       ▼
                          ┌───────────────────────────┐
                          │ fact_escrow_transactions  │
                          │     fact_logistics        │
                          └───────────────────────────┘
```

---

## 2. DAX Measure Catalog (Core Formulas)

```dax
// 1. Total Platform Revenue
Total GMV = SUM(orders[total_amount_inr])

// 2. Delivered Revenue
Delivered Revenue = 
CALCULATE(
    SUM(orders[total_amount_inr]),
    orders[status] = "Delivered"
)

// 3. Gross Profit
Gross Profit = 
SUMX(
    FILTER(orders, orders[status] = "Delivered"),
    orders[total_amount_inr] - (orders[quantity] * RELATED(products[cogs_inr]))
)

// 4. Gross Margin %
Gross Margin % = 
DIVIDE([Gross Profit], [Delivered Revenue], 0) * 100

// 5. Vendor SLA Compliance Rate
Vendor SLA % = 
AVERAGE(vendor_ratings[fulfillment_rate_pct])

// 6. 90-Day Dead Stock Capital Locked
Dead Stock Capital = 
SUMX(
    FILTER(inventory, inventory[stock_age_days] > 90),
    inventory[quantity_on_hand] * RELATED(products[cogs_inr])
)

// 7. Store Valuation Estimate
Store Valuation INR = 
SUMX(
    stores,
    stores[monthly_revenue_inr] * 12 * 
    SWITCH(
        TRUE(),
        stores[health_score] >= 85, 2.8,
        stores[health_score] >= 70, 2.1,
        1.5
    )
)
```

---

## 3. Global Filter Panel & Interactivity Rules

- **Global Slicers (Top Bar):**
  - Date Range Slicer (Relative Date Slicer: YTD, Last 90 Days, Custom Range)
  - Merchant Store Tier (`Platinum`, `Gold`, `Silver`, `Bronze`)
  - Product Category Dropdown (`Electronics`, `Apparel`, `FMCG`, `Home & Kitchen`, `Industrial Hardware`)
  - Geographic Region (`Mumbai`, `Delhi`, `Bengaluru`, `Kolkata`, `Chennai`)
- **Interactivity Behavior:**
  - Cross-filtering enabled across all visuals on the same page.
  - Drill-through pathways configured:
    - *Store Card* ➔ Drill-through to **Tab 8 (Store Health & Valuation)**
    - *Vendor Bar Chart* ➔ Drill-through to **Tab 5 (Vendor SLA Deep-Dive)**
    - *Category Pie* ➔ Drill-through to **Tab 4 (Product Merchandising)**

---

## 4. Tab-by-Tab Visual Layout Specifications

### Tab 1: Executive Summary Command Center
- **Story:** Provides C-suite leadership with real-time visibility into overall platform economic health, active store GMV, profit margins, and dispute risks.
- **Visual Breakdown:**
  1. **Top KPI Card Row (4 Cards):**
     - Gross GMV (₹48.5M, +34% YoY)
     - Gross Margin (28.4%, Green Pill)
     - Active Stores (50 Stores, 94% Solvency)
     - Total Escrow Liquidity (₹14.2M Locked)
  2. **Main Visual (Left 60%):** Line & Clustered Column Combo Chart showing *Monthly Revenue vs Net Margin %* over the past 12 months.
  3. **Secondary Visual (Right 40%):** Donut Chart displaying *Revenue Contribution by Merchant Tier*.
  4. **Bottom Table:** Top 5 Performing Stores vs Bottom 5 Risk Stores.

```
┌────────────────────────────────────────────────────────────────────────┐
│ [GMV: ₹48.5M]    [Gross Margin: 28.4%]    [Stores: 50]    [Escrow: ₹14.2M]│
├──────────────────────────────────────────┬─────────────────────────────┤
│  Monthly Revenue vs Profit Margin %      │  Store Tier Revenue Share   │
│  [Combo Line + Bar Chart]                │  [Donut Chart]              │
├──────────────────────────────────────────┴─────────────────────────────┤
│  Master Executive Store Performance Leaderboard [Grid Table]           │
└────────────────────────────────────────────────────────────────────────┘
```

---

### Tab 2: Inventory & Stock Health Command
- **Story:** Empowers warehouse managers to optimize stock velocity, identify dead stock capital, and prevent SKU stockouts.
- **Visual Breakdown:**
  1. **KPI Cards:** Total Inventory Units (145,200), Dead Stock Capital (₹3.4M), Reorder Risk SKUs (24 SKUs), Avg Stock Age (42 Days).
  2. **Visual 1:** Stacked Horizontal Bar Chart — *Inventory Value by Warehouse Location & Age Bracket (0-30, 31-60, 61-90, >90 Days)*.
  3. **Visual 2:** Scatter Plot — *SKU COGS vs Turnover Rate (ABC Classification Overlay)*.
  4. **Action Table:** Automated PO Reorder Recommendations list with instant trigger status.

---

### Tab 3: Sales & Revenue Performance
- **Story:** Analyzes order volume, sales channel splits, and average order values across store networks.
- **Visual Breakdown:**
  1. **KPI Cards:** Delivered Order Volume (400 Orders), AOV (₹4,850), Return Rate (2.4%), Top Channel (Direct Storefront).
  2. **Visual 1:** Area Chart — *Daily Order Revenue Trajectory by Payment Mode (UPI, Escrow, Card, NetBanking)*.
  3. **Visual 2:** Treemap — *Sales Channel Revenue Share (B2B Portal vs Direct Storefront vs Marketplace)*.
  4. **Visual 3:** Clustered Column Chart — *AOV Comparison by Customer Segment*.

---

### Tab 4: Product Intelligence & Merchandising
- **Story:** Guides catalog managers on pricing optimization, cross-sell bundling, and product review ratings.
- **Visual Breakdown:**
  1. **KPI Cards:** Active SKUs (200), Top Profit Category (Electronics), Avg Product Rating (4.3 Stars), Return Refund Total (₹184K).
  2. **Visual 1:** Matrix Heatmap — *Category vs Margin % and Defect Return Rate*.
  3. **Visual 2:** Product Co-Purchase Association Grid — *Frequently Bought Together Bundles*.
  4. **Visual 3:** Waterfall Chart — *Price Change Elasticity (Old Price vs New Price Revenue Impact)*.

---

### Tab 5: Vendor Performance & Supply Chain
- **Story:** Evaluates supplier SLA compliance, delivery lead times, and fulfillment accuracy to eliminate supply chain bottlenecks.
- **Visual Breakdown:**
  1. **KPI Cards:** Active Vendors (50), Avg Supplier SLA (94.2%), Delayed Shipments (12%), Top Logistics Partner (BlueDart).
  2. **Visual 1:** Vendor Leaderboard Table with conditional formatting icons (Green Check = Tier 1, Red Flag = SLA Violation).
  3. **Visual 2:** Horizontal Clustered Bar — *Actual vs Estimated Transit Days by Carrier (BlueDart, Delhivery, Ecom Express)*.
  4. **Visual 3:** Scatter Chart — *Vendor Quality Rating vs Delivery Rating*.

---

### Tab 6: Customer Cohorts & LTV Analysis
- **Story:** Uncovers buyer retention behavior, RFM segmentation, and lifetime value trajectories for growth marketing.
- **Visual Breakdown:**
  1. **KPI Cards:** Total Buyers (250), Repeat Buyer Rate (44%), CAC (₹2,500), Average LTV (₹48,200), LTV/CAC (3.8x).
  2. **Visual 1:** Cohort Retention Matrix Heatmap (Month 0 to Month 6 Retention %).
  3. **Visual 2:** Stacked Bar Chart — *Customer Count & Monetary Value by RFM Segment (High Value Loyal, At Risk, Price Sensitive)*.
  4. **Visual 3:** Line Chart — *LTV Accumulation Curve over 12 Months*.

---

### Tab 7: Growth & Marketing ROI
- **Story:** Measures performance of ad channels (Meta, Google, WhatsApp) to optimize customer acquisition efficiency.
- **Visual Breakdown:**
  1. **KPI Cards:** Total Ad Spend (₹1.8M), Total Impressions (4.2M), Total Conversions (3,120), Overall ROAS (3.4x).
  2. **Visual 1:** Bar Chart — *ROAS by Campaign Channel*.
  3. **Visual 2:** Funnel Chart — *Ad Impressions ➔ Clicks ➔ Conversions ➔ Repeat Purchases*.
  4. **Visual 3:** Scatter Plot — *Campaign Spend vs Generated Revenue*.

---

### Tab 8: Operations, Escrow & Business Health
- **Story:** Tracks B2B escrow payment liquidity, dispute velocity, store solvency ratios, and M&A valuation multiples.
- **Visual Breakdown:**
  1. **KPI Cards:** Escrow Locked Vault Balance (₹14.2M), Dispute Velocity (0.8%), Avg Store Solvency (2.45x), Total Platform Store Valuation (₹142.5M).
  2. **Visual 1:** Stacked Bar Chart — *Escrow Fund Status Breakdown (Funded vs Released vs Disputed)*.
  3. **Visual 2:** Card Grid — *Store Solvency Index & Health Score Alerts*.
  4. **Visual 3:** Scatter Plot — *Store Monthly Revenue vs Estimated Valuation Multiple (M&A Marketplace)*.

---

## 5. Visual Mockup & Screenshots Fallback Note

> [!NOTE]
> To ensure this repository remains 100% understandable offline or without a Power BI license, all charts, metrics, and tab specifications are mirrored in text, SQL query outputs (`analytics/sql_queries.sql`), and static HTML preview renders (`wireframe-preview.html`).
