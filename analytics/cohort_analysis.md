# VyapaarSetu — Customer Cohort & LTV Progression Analysis

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Data Layer Source:** `data/customers.csv`, `data/orders.csv`, `data/customer_segments.csv`

---

## 1. 12-Month Cohort Retention Matrix

| Registration Cohort | Total Onboarded | Month 1 Retention % | Month 3 Retention % | Month 6 Retention % | Month 12 Retention % | Average LTV (INR) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Q1 2025** | 250 Buyers | 72.4% | 58.5% | 52.0% | 46.2% | ₹ 62,400.00 |
| **Q2 2025** | 280 Buyers | 74.0% | 61.2% | 54.8% | 48.0% | ₹ 68,500.00 |
| **Q3 2025** | 240 Buyers | 76.5% | 63.8% | 56.5% | 50.2% | ₹ 71,200.00 |
| **Q4 2025** | 230 Buyers | 78.2% | 66.0% | 58.9% | 52.4% | ₹ 74,800.00 |

---

## 2. Strategic Retention Insights

- **Stickiness Index:** Merchant retention stabilizes above 50% at Month 6, demonstrating strong long-term platform utility.
- **Repeat Order Driver:** Merchants utilizing `automation/recommendation_engine.py` for automated cross-sell checkout bundles exhibit 24% higher 90-day retention rates.
