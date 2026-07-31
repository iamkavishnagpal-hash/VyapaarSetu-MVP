# VyapaarSetu — Power BI DAX Measures & Formula Catalog

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Target Platform:** Power BI Desktop / Power BI Service  

---

## 1. Executive Financial DAX Measures

```dax
// Gross Platform Revenue
Total GMV = SUM(orders[total_amount_inr])

// Delivered Net Revenue
Delivered Revenue = 
CALCULATE(
    SUM(orders[total_amount_inr]),
    orders[status] = "Delivered"
)

// Gross Profit INR
Gross Profit = 
SUMX(
    FILTER(orders, orders[status] = "Delivered"),
    orders[total_amount_inr] - (orders[quantity] * RELATED(products[cogs_inr]))
)

// Gross Margin %
Gross Margin % = 
DIVIDE([Gross Profit], [Delivered Revenue], 0) * 100
```

---

## 2. Inventory & Supply Chain DAX Measures

```dax
// Dead Stock Capital Locked (>90 Days)
Dead Stock Capital = 
SUMX(
    FILTER(inventory, inventory[stock_age_days] > 90),
    inventory[quantity_on_hand] * RELATED(products[cogs_inr])
)

// Vendor SLA Compliance Rate
Vendor SLA Rate % = 
AVERAGE(vendor_ratings[fulfillment_rate_pct])

// Order Fulfillment SLA %
Order Fulfillment SLA % = 
DIVIDE(
    CALCULATE(COUNT(logistics[logistics_id]), logistics[delivery_status] = "Yes"),
    COUNT(logistics[logistics_id]),
    0
) * 100
```

---

## 3. Store Solvency & Valuation DAX Measures

```dax
// Estimated Store Valuation INR
Store Valuation INR = 
SUMX(
    stores,
    stores[monthly_revenue_inr] * 12 * 
    SWITCH(
        TRUE(),
        stores[health_score] >= 85, 2.8,
        stores[health_score] >= 70, 2.1,
        1.5
    )
)
```
