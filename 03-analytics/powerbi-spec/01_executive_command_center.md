# Power BI Dashboard Spec 1: Executive Command Center

> **Public Inspection Blueprint**: Anyone reviewing this repository can inspect the layout, visuals, DAX data bindings, and filter interactions without signing in to Power BI.

---

## 1. ASCII Layout Preview

```
+-----------------------------------------------------------------------------------+
| FILTERS: [Date Range: 2025-2026 v] [Store: All v] [Category: Textiles v]          |
+-------------------+-------------------+-------------------+-----------------------+
|  GROSS REVENUE    |    NET PROFIT     |  AVG NET MARGIN   | ESCROW FUNDS HELD     |
|   ₹39.3M (+16.2%) |   ₹6.3M (+18.5%)  |     16.0%         |   ₹8.7M (24 Deals)    |
+-------------------+-------------------+-------------------+-----------------------+
| MONTHLY REVENUE & NET PROFIT TREND (LINE + COLUMN COMBO CHART)                    |
| [================================================================] Gross Revenue  |
| [----------------------------------------------------------------] Net Profit     |
+-----------------------------------------+-----------------------------------------+
| TOP REVENUE CATEGORIES                  | LIVE OPERATIONAL AI ALERTS              |
| 1. Textiles & Handblock  ₹6.8M (17.5%)  | ⚠️ Shrinkage Alert: Leather WH-103      |
| 2. Pure Silk Sarees      ₹6.7M (17.1%)  | 💡 AI Rec: Reallocate Meta Ad Budget   |
| 3. Knitwear Apparel      ₹6.6M (16.8%)  | ✅ Preferred Vendor Score: VND-1217    |
+-----------------------------------------+-----------------------------------------+
```

---

## 2. Visual Data Bindings & DAX Measures

1. **KPI Cards Array**:
   - `[Total Gross Revenue]`: `SUM(orders[total_amount_inr])` formatted in INR.
   - `[Net Contribution Margin]`: `[Total Gross Revenue] - [Total COGS] - [Total Shipping]`.
   - `[Avg Net Margin Pct]`: `DIVIDE([Net Contribution Margin], [Total Gross Revenue], 0)`.
   - `[Escrow Volume Held]`: `CALCULATE(SUM(escrow_logs[amount_inr]), escrow_logs[status] = "Held")`.

2. **Main Visual (Left Center)**:
   - **Chart Type**: Clustered Column & Line Combo Chart.
   - **X-Axis**: `Calendar[MonthYear]`
   - **Y-Axis (Column)**: `[Total Gross Revenue]`
   - **Y-Axis (Line)**: `[Net Margin Pct]`
