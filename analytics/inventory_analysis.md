# VyapaarSetu — Inventory Velocity & Capital Lockup Analysis

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Data Layer Source:** `data/inventory.csv`, `data/products.csv`, `data/inventory_movements.csv`

---

## 1. ABC Inventory Pareto Classification

```
┌────────────────────────────────────────────────────────────────────────┐
│                      ABC PARETO STOCK CLASSIFICATION                   │
├─────────────────────────┬─────────────────────────┬────────────────────┤
│ Class A (Top 80% Rev)   │ Class B (15% Rev)       │ Class C (5% Rev)   │
│ 75 SKUs (15% Volume)    │ 125 SKUs (25% Volume)   │ 300 SKUs (60% Vol) │
└─────────────────────────┴─────────────────────────┴────────────────────┘
```

---

## 2. Warehouse Stock Ageing & Holding Cost Breakdown

| Warehouse Location | Total Stock Units | Stock 0–60 Days | Dead Stock >90 Days | Capital Locked (INR) | Action Required |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **WH-West-Mumbai** | 450,000 units | 380,000 units | 42,000 units | ₹ 24,500,000 | Initiate 15% clearance sale |
| **WH-North-Delhi** | 380,000 units | 310,000 units | 38,000 units | ₹ 19,800,000 | Re-allocate to South hub |
| **WH-South-Bengaluru**| 320,000 units | 285,000 units | 18,000 units | ₹ 11,200,000 | Maintain current safety stock |
| **WH-East-Kolkata** | 210,000 units | 165,000 units | 28,000 units | ₹ 14,100,000 | Audit return inbound stock |
| **WH-Central-Nagpur** | 140,000 units | 122,000 units | 9,000 units | ₹ 4,800,000 | Regional fulfillment hub |

---

## 3. Inventory Shrinkage & Loss Prevention

- **Total Annual Shrinkage Loss:** ₹1.85M across 5 fulfillment centers (< 0.25% of total GMV).
- **Primary Shrinkage Cause:** Packaging damage during B2B return transport (62% of losses).
- **Remediation Action:** `automation/inventory_sync.py` flags high-shrinkage SKUs for mandatory warehouse audit upon receipt.
