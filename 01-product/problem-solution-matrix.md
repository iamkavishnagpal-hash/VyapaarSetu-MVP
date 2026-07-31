# VyapaarSetu Problem-to-Solution Matrix

This document maps every operational problem faced by MSMEs to its financial impact, data requirements, UX solution, and automation logic.

---

## Matrix Mapping

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 VYAPAARSETU PROBLEM-TO-SOLUTION MATRIX                      │
├───────────────────┬───────────────────┬───────────────────┬─────────────────┤
│ Operational Pain  │ Financial Impact  │ UX Solution       │ Automation      │
├───────────────────┼───────────────────┼───────────────────┼─────────────────┤
│ 1. POS/Web Stock  │ Overselling, lost │ Stock Timeline,   │ Redis Redlock,  │
│    Mismatch       │ revenue, bad CX   │ Real-time alerts  │ Webhook Sync    │
│                   │                   │                   │                 │
│ 2. Unverified B2B │ Capital fraud,    │ Verified Badge,   │ Multi-Sig       │
│    Suppliers      │ delayed batches   │ SLA Scorecard     │ Escrow Hold     │
│                   │                   │                   │                 │
│ 3. High Shipping  │ Net margin burn,  │ Carrier Selector  │ Dynamic Routing │
│    Costs & RTO    │ SLA breaches      │ Map & Cost Grid   │ Score Matrix    │
│                   │                   │                   │                 │
│ 4. Illiquid Store │ Distrusted P&L,   │ Audit Credentials │ Bank Gateway    │
│    Exits          │ valuation disputes│ Verified Badge    │ P&L API Audit   │
└───────────────────┴───────────────────┴───────────────────┴─────────────────┘
```

---

## Detailed 5-Point Feature Breakdown

### 1. Feature 1: Multi-Channel Inventory Reconciliation
- **Problem**: Physical store counter sales (POS) are unrecorded or delayed, leading to online overselling on Shopify/Amazon.
- **Business Impact**: High cancellation penalties, customer churn, and inventory shrinkage leakage (avg 2.5% - 4.5%).
- **Data Needed**: `orders.csv`, `inventory_logs.csv`, `warehouses.csv`, POS billing log feeds.
- **UX Solution**: Real-time stock status pills (Synced = Emerald, Discrepancy = Amber), live stock movement timeline.
- **Automation**: Python sync daemon (`inventory_reconciler.py`), Webhook receivers, Redis Redlock locks.

### 2. Feature 2: B2B Supplier Escrow Wallet
- **Problem**: New MSME store founders fear sending 100% upfront wire transfers to unverified wholesale vendors in distant cities.
- **Business Impact**: Seed capital loss, counterfeit products, stockout delays.
- **Data Needed**: `vendors.csv`, `escrow_logs.csv`, delivery tracking events.
- **UX Solution**: Multi-Sig Escrow Status Card (Held in Trust -> QA Inspection -> Funds Auto-Released).
- **Automation**: Escrow milestone trigger engine releasing funds upon courier delivery receipt.
