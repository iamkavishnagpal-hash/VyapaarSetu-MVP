# VyapaarSetu — E-Commerce Conversion Funnel & Friction Analysis

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Data Layer Source:** `data/sales_channels.csv`, `data/orders.csv`, `data/escrow_transactions.csv`

---

## 1. End-to-End Conversion Funnel Stages

```
[100,000 Storefront Visits]
           │
           ▼ (45.0% Drop-off)
[55,000 Product Detail Views]
           │
           ▼ (60.0% Drop-off)
[22,000 Cart Additions]
           │
           ▼ (50.0% Drop-off)
[11,000 Checkout Initiated]
           │
           ▼ (18.2% Drop-off)
[9,000 Escrow Vault / Payment Funded]
           │
           ▼ (1.4% Return Rate)
[8,874 Successful Order Deliveries]
```

---

## 2. Channel Conversion Breakdown

| Channel Name | Conversion Rate % | Avg Order Value (AOV) | Cart Abandonment % | Primary Friction Point |
| :--- | :--- | :--- | :--- | :--- |
| **B2B Wholesale Portal** | 5.8% | ₹ 45,200 | 28.5% | Credit line authorization delays |
| **Direct Storefront** | 3.4% | ₹ 4,850 | 48.2% | Shipping fee visibility at checkout |
| **VyapaarSetu Marketplace** | 4.2% | ₹ 8,900 | 42.0% | Escrow milestone explanation complexity |
| **WhatsApp Commerce** | 6.5% | ₹ 2,400 | 18.0% | Manual catalog navigation |
