-- ============================================================================
-- VYAPAARSETU MVP — ANALYTICS ENGINE SQL SUITE
-- Business Intelligence & Decision Support Queries for MSME Commerce OS
-- Dialect: ANSI SQL / PostgreSQL / BigQuery Compatible
-- ============================================================================

-- ----------------------------------------------------------------------------
-- QUERY 1: Underperforming & High-Leakage SKU Identification Engine
-- Rationale: Flags products with high inventory shrinkage or negative contribution margin
-- ----------------------------------------------------------------------------
WITH product_financials AS (
    SELECT 
        p.product_id,
        p.sku,
        p.name AS product_name,
        p.category,
        p.cost_price_inr,
        p.selling_price_inr,
        (p.selling_price_inr - p.cost_price_inr) AS unit_gross_margin_inr,
        ROUND(((p.selling_price_inr - p.cost_price_inr)::NUMERIC / p.selling_price_inr::NUMERIC) * 100, 2) AS gross_margin_pct
    FROM products p
),
order_performance AS (
    SELECT 
        product_id,
        COUNT(order_id) AS total_orders,
        SUM(quantity) AS total_units_sold,
        SUM(total_amount_inr) AS gross_revenue_inr,
        SUM(CASE WHEN order_status = 'Returned' THEN quantity ELSE 0 END) AS returned_units,
        SUM(CASE WHEN order_status = 'Cancelled' THEN quantity ELSE 0 END) AS cancelled_units
    FROM orders
    GROUP BY product_id
),
stock_leakage AS (
    SELECT 
        product_id,
        SUM(offline_stock_qty + online_stock_qty) AS total_stock,
        AVG(shrinkage_rate_pct) AS avg_shrinkage_pct
    FROM inventory
    GROUP BY product_id
)
SELECT 
    pf.product_id,
    pf.sku,
    pf.product_name,
    pf.category,
    pf.gross_margin_pct,
    COALESCE(op.total_units_sold, 0) AS total_units_sold,
    COALESCE(op.gross_revenue_inr, 0) AS gross_revenue_inr,
    ROUND((COALESCE(op.returned_units, 0)::NUMERIC / NULLIF(op.total_units_sold, 0)::NUMERIC) * 100, 2) AS return_rate_pct,
    sl.avg_shrinkage_pct,
    CASE 
        WHEN sl.avg_shrinkage_pct > 3.0 THEN 'CRITICAL: High Shrinkage Risk'
        WHEN COALESCE(op.returned_units, 0)::NUMERIC / NULLIF(op.total_units_sold, 0)::NUMERIC > 0.15 THEN 'WARNING: Excessive Return Rate'
        WHEN pf.gross_margin_pct < 20.0 THEN 'ACTION: Margin Liquidation Required'
        ELSE 'PERFORMING'
    END AS strategic_recommendation
FROM product_financials pf
LEFT JOIN order_performance op ON pf.product_id = op.product_id
LEFT JOIN stock_leakage sl ON pf.product_id = sl.product_id
ORDER BY gross_revenue_inr ASC, avg_shrinkage_pct DESC;


-- ----------------------------------------------------------------------------
-- QUERY 2: Channel Profitability & Net Contribution Margin Analysis
-- Rationale: Compares offline POS counter vs. Direct D2C vs. Marketplace profit net of shipping & fees
-- ----------------------------------------------------------------------------
SELECT 
    o.channel,
    COUNT(o.order_id) AS order_volume,
    SUM(o.total_amount_inr) AS total_gross_revenue,
    SUM(o.quantity * p.cost_price_inr) AS total_cogs,
    SUM(o.shipping_cost_inr) AS total_shipping_expense,
    SUM(o.total_amount_inr - (o.quantity * p.cost_price_inr) - o.shipping_cost_inr) AS net_profit_inr,
    ROUND(
        (SUM(o.total_amount_inr - (o.quantity * p.cost_price_inr) - o.shipping_cost_inr)::NUMERIC / 
        NULLIF(SUM(o.total_amount_inr), 0)::NUMERIC) * 100, 2
    ) AS net_margin_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.order_status = 'Delivered'
GROUP BY o.channel
ORDER BY net_profit_inr DESC;


-- ----------------------------------------------------------------------------
-- QUERY 3: Vendor Reliability & SLA Performance Scorecard
-- Rationale: Scores vendor risk based on delivery on-time rate, defect rate, and lead time SLA
-- ----------------------------------------------------------------------------
SELECT 
    v.vendor_id,
    v.name AS vendor_name,
    v.category,
    v.location,
    v.rating AS user_rating,
    v.lead_time_days,
    v.on_time_rate_pct,
    v.defect_rate_pct,
    v.escrow_verified,
    COUNT(p.product_id) AS active_catalog_products,
    ROUND(
        (v.on_time_rate_pct * 0.40) + 
        ((100 - v.defect_rate_pct) * 0.40) + 
        (v.rating * 4.0), 2
    ) AS composite_vendor_health_score,
    CASE 
        WHEN (v.on_time_rate_pct * 0.40) + ((100 - v.defect_rate_pct) * 0.40) + (v.rating * 4.0) >= 85.0 THEN 'PREFERRED SUPPLIER'
        WHEN (v.on_time_rate_pct * 0.40) + ((100 - v.defect_rate_pct) * 0.40) + (v.rating * 4.0) >= 70.0 THEN 'STANDARD SUPPLIER'
        ELSE 'HIGH RISK — Escrow Audit Mandated'
    END AS vendor_tier
FROM vendors v
LEFT JOIN products p ON v.vendor_id = p.vendor_id
GROUP BY v.vendor_id, v.name, v.category, v.location, v.rating, v.lead_time_days, v.on_time_rate_pct, v.defect_rate_pct, v.escrow_verified
ORDER BY composite_vendor_health_score DESC;


-- ----------------------------------------------------------------------------
-- QUERY 4: Real-Time Inventory Discrepancy & Reorder Point Alert Engine
-- Rationale: Detects out-of-sync online/offline channels and automated stockout threats
-- ----------------------------------------------------------------------------
SELECT 
    i.inventory_id,
    s.store_name,
    p.sku,
    p.name AS product_name,
    i.offline_stock_qty,
    i.online_stock_qty,
    (i.offline_stock_qty + i.online_stock_qty) AS combined_available_stock,
    p.reorder_level,
    i.reserved_qty,
    i.sync_status,
    CASE 
        WHEN (i.offline_stock_qty + i.online_stock_qty) <= p.reorder_level THEN 'TRIGGER REORDER'
        WHEN i.sync_status = 'Discrepancy Warning' THEN 'TRIGGER INVENTORY RECONCILIATION'
        ELSE 'HEALTHY'
    END AS automation_action
FROM inventory i
JOIN products p ON i.product_id = p.product_id
JOIN stores s ON i.store_id = s.store_id
WHERE (i.offline_stock_qty + i.online_stock_qty) <= p.reorder_level 
   OR i.sync_status != 'Synced'
ORDER BY combined_available_stock ASC;


-- ----------------------------------------------------------------------------
-- QUERY 5: Store Marketplace Valuation & Acquisition Attractiveness Matrix
-- Rationale: Evaluates stores listed on VyapaarSetu Marketplace for prospective buyers
-- ----------------------------------------------------------------------------
SELECT 
    store_id,
    store_name,
    category,
    location,
    monthly_revenue_inr,
    monthly_profit_inr,
    profit_margin_pct,
    online_share_pct,
    asking_price_inr,
    valuation_multiple,
    ROUND((asking_price_inr::NUMERIC / NULLIF(monthly_profit_inr * 12, 0)::NUMERIC), 2) AS calculated_annual_pe_multiple,
    CASE 
        WHEN profit_margin_pct >= 20.0 AND valuation_multiple <= 2.5 THEN 'PRIME BUYING OPPORTUNITY'
        WHEN valuation_multiple > 3.0 THEN 'OVERVALUED — Negotiate Down'
        ELSE 'MODERATE ACQUISITION TARGET'
    END AS buyer_advisory_note
FROM stores
WHERE status = 'For Sale'
ORDER BY profit_margin_pct DESC;
