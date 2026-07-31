# VyapaarSetu — Vendor Performance & Supply Chain SLA Analysis

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Data Layer Source:** `data/vendors.csv`, `data/vendor_ratings.csv`, `data/logistics.csv`

---

## 1. Vendor SLA Performance Summary

| Supplier Tier | Vendor Count | Declared SLA % | Actual SLA % | Avg Quality Score | Fulfillment Defect Rate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1 (Preferred)** | 42 Vendors | 98.0% | 98.4% | 4.8 / 5.0 | 0.4% |
| **Tier 2 (Reliable)** | 45 Vendors | 92.0% | 91.8% | 4.2 / 5.0 | 1.8% |
| **Tier 3 (Action Required)** | 13 Vendors | 85.0% | 79.2% | 3.4 / 5.0 | 4.8% |

---

## 2. Supply Chain Optimization Protocol

1. **Tier-3 Supplier Probation:** Vendors falling below 80% actual SLA compliance are automatically placed on 30-day probation via `vendor_matching.py`.
2. **Lead Time Variance Buffer:** Inventory safety stock formulas dynamically inflate by +15% for vendors experiencing >2 day lead-time variances.
