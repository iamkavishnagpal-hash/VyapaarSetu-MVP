# VyapaarSetu — Catalog Merchandising & Product Defect Analysis

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Data Layer Source:** `data/products.csv`, `data/returns.csv`, `data/product_reviews.csv`

---

## 1. Category Margin & Volume Performance

| Product Category | SKU Count | Total Sales Volume | Gross Revenue (INR) | Avg COGS % | Return Defect Rate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Electronics** | 50 SKUs | 1,420 units | ₹ 21,500,000 | 72.4% | 1.8% |
| **Apparel** | 45 SKUs | 2,850 units | ₹ 12,800,000 | 58.2% | 4.2% |
| **FMCG** | 40 SKUs | 5,200 units | ₹ 6,400,000 | 81.0% | 0.8% |
| **Home & Kitchen** | 35 SKUs | 1,100 units | ₹ 5,200,000 | 64.5% | 2.1% |
| **Industrial Hardware**| 30 SKUs | 850 units | ₹ 2,600,000 | 69.0% | 1.2% |

---

## 2. Product Return Defect Root Causes

- **Size/Color Discrepancy (Apparel - 4.2% Return Rate):** Recommended action: Implement standardized digital size charts in `/start-business` catalog view.
- **Packaging Damage in Transit (Electronics - 1.8% Return Rate):** Recommended action: Mandate double-walled corrugated boxing for high-value SKUs via `logistics_assignment.py`.
