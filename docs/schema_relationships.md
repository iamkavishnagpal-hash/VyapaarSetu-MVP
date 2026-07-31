# VyapaarSetu — Data Schema Relationships & ERD Cardinality Matrix

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Storage Target:** PostgreSQL 14 / DuckDB / CSV Data Layer (`data/`)

---

## 1. Entity Relationship & Cardinality Overview

```
[vendors] (1) ──── (N) [products] (1) ──── (N) [inventory]
                           │
                           │ (1:N)
                           ▼
[customers] (1) ──── (N) [orders] (1) ──── (1) [escrow_transactions]
                           │
                           │ (1:1)
                           ▼
                      [logistics]
```

---

## 2. Detailed Foreign Key Join Map

| Primary Entity (1) | Primary Key | Foreign Entity (N) | Foreign Key | Cardinality | Join Type | Business Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **vendors** | `vendor_id` | **products** | `vendor_id` | 1 : N | `INNER JOIN` | Links catalog items to supplying manufacturer for PO routing |
| **stores** | `store_id` | **orders** | `store_id` | 1 : N | `INNER JOIN` | Attributes customer sales to specific merchant storefront |
| **customers** | `customer_id` | **orders** | `customer_id` | 1 : N | `INNER JOIN` | Tracks buyer purchasing frequency and RFM cohorts |
| **products** | `product_id` | **orders** | `product_id` | 1 : N | `INNER JOIN` | Calculates SKU gross profit margin and volume sold |
| **products** | `product_id` | **inventory** | `product_id` | 1 : N | `INNER JOIN` | Tracks stock age and reorder thresholds across warehouses |
| **orders** | `order_id` | **escrow_transactions** | `order_id` | 1 : 1 | `LEFT JOIN` | Monitors trade vault deposit, inspection, and release |
| **orders** | `order_id` | **logistics** | `order_id` | 1 : 1 | `LEFT JOIN` | Tracks courier dispatch, shipping cost, and transit SLA |
| **products** | `product_id` | **returns** | `product_id` | 1 : N | `LEFT JOIN` | Analyzes return defect rates and refund amounts |
| **stores** | `store_id` | **business_health**| `store_id` | 1 : N | `INNER JOIN` | Tracks monthly store solvency ratios and risk index |

---

## 3. SQL Join Strategy Best Practices

1. **Analytical Rollups:** Always use `LEFT JOIN` when aggregating `escrow_transactions`, `logistics`, or `returns` to preserve orders that did not trigger returns or disputes.
2. **Indexing:** Primary keys (`vendor_id`, `product_id`, `store_id`, `order_id`, `customer_id`) are indexed with B-Tree indexes for sub-5ms query performance.
