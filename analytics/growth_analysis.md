# VyapaarSetu — Platform Growth & Revenue Trajectory Deep-Dive

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Data Layer Source:** `data/orders.csv`, `data/stores.csv`, `data/business_health.csv`

---

## 1. Macro Platform Growth Summary

Over the past 12 months, VyapaarSetu has demonstrated strong multi-tier growth across active merchant stores, total order volume, and gross GMV:

```
┌─────────────────────────┬─────────────────────────┬─────────────────────────┐
│     Gross GMV (12M)     │    Active Merchant      │     Monthly Order      │
│     ₹ 48.5 M (+34.2%)   │     50 Stores (94% Sol) │     400 Orders / Mo     │
└─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

---

## 2. Regional Sales & Growth Index Matrix

| Region / City | Active Stores | Quarterly GMV (INR) | MoM Growth % | Regional SLA Rate | Top Product Category |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mumbai** | 12 Stores | ₹ 14,800,000 | +18.4% | 98.2% | Electronics |
| **Delhi NCR** | 10 Stores | ₹ 12,200,000 | +15.1% | 96.5% | Apparel |
| **Bengaluru** | 11 Stores | ₹ 11,400,000 | +22.0% | 97.1% | Home & Kitchen |
| **Kolkata** | 9 Stores | ₹ 6,100,000 | +9.8% | 92.4% | FMCG |
| **Surat** | 8 Stores | ₹ 4,000,000 | +28.5% | 99.0% | Industrial Hardware |

---

## 3. Growth Strategic Action Plan

1. **Surat & Western Corridor Expansion:** High growth velocity (+28.5% MoM) in Surat hardware merchants supports opening a dedicated regional distribution center (`WH-Surat-West`).
2. **Kolkata Merchant Assistance:** Low growth (+9.8%) and SLA delay (92.4%) in Eastern zone requires deploying `automation/order_routing.py` to re-route shipments via BlueDart Express.
