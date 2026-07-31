# VyapaarSetu Cohort & Growth Retention Analysis

## Executive Rationale
MSME e-commerce stores often fail not due to lack of initial traffic, but because of **channel churn, inventory leakage, supplier SLA degradation, and unmonitored unit economics**.

This analysis documents how VyapaarSetu evaluates merchant growth cohorts, customer repeat behaviors, and vendor reliability stability over 30-60-90 day cycles.

---

## 1. Merchant Revenue Cohort Analysis

```
Cohort Month | M0 (Launch) | M1 Retention | M2 Retention | M3 Retention | Net Growth Status
-------------+-------------+--------------+--------------+--------------+-------------------
Jan 2026     | ₹450,000    | 88.5%        | 82.1%        | 85.0%        | Healthy Scaling
Feb 2026     | ₹620,000    | 91.0%        | 87.4%        | 89.2%        | High Retention
Mar 2026     | ₹580,000    | 79.2%        | 71.0%        | 68.5%        | Churn Risk (SLA Issue)
```

### Key Insights & Business Observations
- **March 2026 Cohort Drop**: Investigation revealed a 71% retention rate due to logistics delays with `XpressBees Surface` (7-day delivery SLA breach). Migrating March merchants to `Delhivery Direct` restored delivery SLAs to < 3 days and recovered M4 repeat orders by +14%.

---

## 2. Underperforming Product & Leakage Diagnosis

VyapaarSetu automatically flags products that erode merchant profitability into three action tiers:

1. **Category A: Shrinkage Leakage Alert (`PRD-1006` - Leather Messenger Bag)**
   - *Symptom*: High stock shrinkage rate (4.8%) between offline counter and online warehouse.
   - *Root Cause*: Manual unrecorded counter giveaways and unbilled store samples.
   - *Fix*: Enforced automated barcode scan log requirement on physical POS before stock movement.

2. **Category B: Margin Erosion Alert (`PRD-1008` - Wireless Desk Mat)**
   - *Symptom*: High cost price (₹650) relative to selling price (₹1899) combined with high marketplace ad CAC (₹920).
   - *Root Cause*: High competition on marketplace channel.
   - *Fix*: De-listed from marketplaces; moved exclusive bundle offer to D2C storefront with zero commission.

3. **Category C: Star Revenue Driver (`PRD-1001` - Jaipur Cotton Kurta)**
   - *Symptom*: Gross margin 70%, return rate < 2%, vendor SLA 96.5%.
   - *Fix*: Scaled vendor pre-order volume via Escrow wallet financing to lock in 10% raw material bulk discount.
