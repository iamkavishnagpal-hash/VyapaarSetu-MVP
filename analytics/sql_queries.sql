-- =============================================================================
-- VyapaarSetu Platform — Production SQL Business Analytics Pack
-- File: analytics/sql_queries.sql
-- Description: 25+ ANSI SQL business intelligence queries supporting MSME operations,
--              inventory optimization, vendor SLA tracking, financial reporting,
--              customer cohort retention, escrow monitoring, and store valuation.
-- Database Target: PostgreSQL 14+ / DuckDB / BigQuery / Snowflake
-- =============================================================================

-- -----------------------------------------------------------------------------
-- QUERY 1: Total Monthly Revenue, Cost of Goods Sold & Gross Profit Margin
-- Purpose: Executive summary metric tracking overall platform financial growth.
-- Business Decision Supported: Strategic budget allocation & quarterly financial forecasting.
-- -----------------------------------------------------------------------------
SELECT 
    DATE_TRUNC('month', order_date) AS sales_month,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(total_amount_inr) AS gross_revenue_inr,
    SUM(quantity * p.cogs_inr) AS total_cogs_inr,
    SUM(total_amount_inr) - SUM(quantity * p.cogs_inr) AS gross_profit_inr,
    ROUND(CAST((SUM(total_amount_inr) - SUM(quantity * p.cogs_inr)) / NULLIF(SUM(total_amount_inr), 0) * 100 AS NUMERIC), 2) AS gross_margin_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'Delivered'
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY sales_month DESC;

-- -----------------------------------------------------------------------------
-- QUERY 2: Top 10 Best-Selling Products by Gross Profit Contribution
-- Purpose: Identifies high-margin SKU winners for featured marketing & restock priority.
-- Business Decision Supported: Merchandising optimization & vendor volume commitment.
-- -----------------------------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    v.vendor_name,
    SUM(o.quantity) AS total_units_sold,
    SUM(o.total_amount_inr) AS revenue_generated,
    SUM(o.total_amount_inr - (o.quantity * p.cogs_inr)) AS profit_contribution_inr,
    DENSE_RANK() OVER (ORDER BY SUM(o.total_amount_inr - (o.quantity * p.cogs_inr)) DESC) AS profit_rank
FROM orders o
JOIN products p ON o.product_id = p.product_id
JOIN vendors v ON p.vendor_id = v.vendor_id
WHERE o.status = 'Delivered'
GROUP BY p.product_id, p.product_name, p.category, v.vendor_name
LIMIT 10;

-- -----------------------------------------------------------------------------
-- QUERY 3: Bottom 10 Underperforming Products & Dead Stock Exposure
-- Purpose: Pinpoints slow-moving SKUs locking up inventory capital.
-- Business Decision Supported: Target markdown discount campaigns or vendor returns.
-- -----------------------------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    i.quantity_on_hand,
    i.stock_age_days,
    COALESCE(SUM(o.quantity), 0) AS units_sold_last_90_days,
    (i.quantity_on_hand * p.cogs_inr) AS capital_locked_inr
FROM products p
JOIN inventory i ON p.product_id = i.product_id
LEFT JOIN orders o ON p.product_id = o.product_id AND o.order_date >= CURRENT_DATE - INTERVAL '90 days'
WHERE i.stock_age_days > 60
GROUP BY p.product_id, p.product_name, p.category, i.quantity_on_hand, i.stock_age_days, p.cogs_inr
ORDER BY capital_locked_inr DESC, units_sold_last_90_days ASC
LIMIT 10;

-- -----------------------------------------------------------------------------
-- QUERY 4: Vendor SLA Performance & Fulfillment Scorecard
-- Purpose: Evaluates vendor reliability, defect rates, and SLA compliance.
-- Business Decision Supported: Supplier contract renewal & preferred vendor badge award.
-- -----------------------------------------------------------------------------
SELECT 
    v.vendor_id,
    v.vendor_name,
    v.category,
    v.sla_compliance_pct AS declared_sla,
    ROUND(AVG(vr.quality_score), 2) AS avg_quality_score,
    ROUND(AVG(vr.delivery_score), 2) AS avg_delivery_score,
    ROUND(AVG(vr.fulfillment_rate_pct), 2) AS actual_fulfillment_rate_pct,
    COUNT(vr.rating_id) AS total_evaluations,
    CASE 
        WHEN AVG(vr.fulfillment_rate_pct) >= 95.0 AND AVG(vr.quality_score) >= 4.5 THEN 'Tier 1 Strategic'
        WHEN AVG(vr.fulfillment_rate_pct) >= 85.0 THEN 'Tier 2 Reliable'
        ELSE 'Tier 3 Action Required'
    END AS vendor_classification
FROM vendors v
LEFT JOIN vendor_ratings vr ON v.vendor_id = vr.vendor_id
GROUP BY v.vendor_id, v.vendor_name, v.category, v.sla_compliance_pct
ORDER BY actual_fulfillment_rate_pct DESC;

-- -----------------------------------------------------------------------------
-- QUERY 5: Inventory Ageing Breakdown (>90 Days Risk Analysis)
-- Purpose: Categorizes stock by age brackets to quantify holding risk.
-- Business Decision Supported: Working capital release & warehouse space allocation.
-- -----------------------------------------------------------------------------
SELECT 
    warehouse_location,
    SUM(CASE WHEN stock_age_days <= 30 THEN quantity_on_hand ELSE 0 END) AS stock_0_30_days,
    SUM(CASE WHEN stock_age_days BETWEEN 31 AND 60 THEN quantity_on_hand ELSE 0 END) AS stock_31_60_days,
    SUM(CASE WHEN stock_age_days BETWEEN 61 AND 90 THEN quantity_on_hand ELSE 0 END) AS stock_61_90_days,
    SUM(CASE WHEN stock_age_days > 90 THEN quantity_on_hand ELSE 0 END) AS dead_stock_over_90_days,
    SUM(quantity_on_hand) AS total_units
FROM inventory
GROUP BY warehouse_location;

-- -----------------------------------------------------------------------------
-- QUERY 6: ABC Inventory Classification (80-15-5 Pareto Analysis)
-- Purpose: Ranks SKUs into Class A (High revenue), B (Moderate), C (Low revenue).
-- Business Decision Supported: Priority stock replenishment cycles.
-- -----------------------------------------------------------------------------
WITH ProductRevenue AS (
    SELECT 
        p.product_id,
        p.product_name,
        SUM(o.total_amount_inr) AS revenue,
        SUM(SUM(o.total_amount_inr)) OVER () AS total_platform_revenue
    FROM products p
    JOIN orders o ON p.product_id = o.product_id
    WHERE o.status = 'Delivered'
    GROUP BY p.product_id, p.product_name
),
CumRevenue AS (
    SELECT 
        product_id,
        product_name,
        revenue,
        SUM(revenue) OVER (ORDER BY revenue DESC) AS cumulative_revenue,
        total_platform_revenue
    FROM ProductRevenue
)
SELECT 
    product_id,
    product_name,
    revenue,
    ROUND(CAST((cumulative_revenue / total_platform_revenue) * 100 AS NUMERIC), 2) AS cum_rev_pct,
    CASE 
        WHEN (cumulative_revenue / total_platform_revenue) <= 0.80 THEN 'Class A (80% Rev)'
        WHEN (cumulative_revenue / total_platform_revenue) <= 0.95 THEN 'Class B (15% Rev)'
        ELSE 'Class C (5% Rev)'
    END AS abc_class
FROM CumRevenue
ORDER BY revenue DESC;

-- -----------------------------------------------------------------------------
-- QUERY 7: Category Revenue & Profit Contribution Share
-- Purpose: Identifies macro product category trends across retail stores.
-- Business Decision Supported: Merchandising expansion & inventory budget planning.
-- -----------------------------------------------------------------------------
SELECT 
    p.category,
    COUNT(DISTINCT o.order_id) AS orders_count,
    SUM(o.quantity) AS total_volume_sold,
    SUM(o.total_amount_inr) AS category_revenue_inr,
    ROUND(CAST(SUM(o.total_amount_inr) * 100.0 / SUM(SUM(o.total_amount_inr)) OVER () AS NUMERIC), 2) AS revenue_share_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'Delivered'
GROUP BY p.category
ORDER BY category_revenue_inr DESC;

-- -----------------------------------------------------------------------------
-- QUERY 8: Customer Repeat Purchase Rate & Order Frequency Matrix
-- Purpose: Measures customer loyalty and repeat order behavior.
-- Business Decision Supported: Retention marketing budget allocation.
-- -----------------------------------------------------------------------------
WITH CustomerOrderCounts AS (
    SELECT 
        customer_id,
        COUNT(order_id) AS order_count,
        SUM(total_amount_inr) AS total_spent
    FROM orders
    GROUP BY customer_id
)
SELECT 
    CASE 
        WHEN order_count = 1 THEN '1 Single Purchase'
        WHEN order_count BETWEEN 2 AND 4 THEN '2-4 Repeat Orders'
        WHEN order_count BETWEEN 5 AND 9 THEN '5-9 Loyal Buyers'
        ELSE '10+ VIP Power Buyers'
    END AS buyer_cohort,
    COUNT(customer_id) AS customer_count,
    ROUND(AVG(total_spent), 2) AS avg_cohort_ltv_inr
FROM CustomerOrderCounts
GROUP BY 1
ORDER BY customer_count DESC;

-- -----------------------------------------------------------------------------
-- QUERY 9: Month-over-Month (MoM) Growth in Sales & Order Volume
-- Purpose: Tracks platform scaling velocity and seasonal trend changes.
-- Business Decision Supported: Investor updates & infrastructure capacity planning.
-- -----------------------------------------------------------------------------
WITH MonthlySales AS (
    SELECT 
        DATE_TRUNC('month', order_date) AS month,
        SUM(total_amount_inr) AS monthly_revenue,
        COUNT(order_id) AS monthly_orders
    FROM orders
    WHERE status = 'Delivered'
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT 
    month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY month) AS prev_month_revenue,
    ROUND(CAST((monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month)) / NULLIF(LAG(monthly_revenue) OVER (ORDER BY month), 0) * 100 AS NUMERIC), 2) AS mom_revenue_growth_pct,
    monthly_orders,
    LAG(monthly_orders) OVER (ORDER BY month) AS prev_month_orders
FROM MonthlySales
ORDER BY month DESC;

-- -----------------------------------------------------------------------------
-- QUERY 10: Store Benchmarking & Health Score Matrix
-- Purpose: Ranks merchant storefronts by revenue, health score, and estimated valuation.
-- Business Decision Supported: Merchant support tiering & M&A store advisory.
-- -----------------------------------------------------------------------------
SELECT 
    s.store_id,
    s.store_name,
    s.city,
    s.tier,
    s.health_score,
    s.monthly_revenue_inr,
    s.estimated_valuation_inr,
    COUNT(o.order_id) AS total_fulfilled_orders,
    ROUND(COALESCE(SUM(o.total_amount_inr), 0), 2) AS cumulative_sales_inr
FROM stores s
LEFT JOIN orders o ON s.store_id = o.store_id AND o.status = 'Delivered'
GROUP BY s.store_id, s.store_name, s.city, s.tier, s.health_score, s.monthly_revenue_inr, s.estimated_valuation_inr
ORDER BY s.health_score DESC;

-- -----------------------------------------------------------------------------
-- QUERY 11: Product Pair Co-Purchase Analysis (Basket Cross-Sell)
-- Purpose: Identifies items frequently bought together in the same order.
-- Business Decision Supported: Dynamic checkout product recommendation bundles.
-- -----------------------------------------------------------------------------
SELECT 
    o1.product_id AS item_a,
    p1.product_name AS item_a_name,
    o2.product_id AS item_b,
    p2.product_name AS item_b_name,
    COUNT(*) AS times_bought_together
FROM orders o1
JOIN orders o2 ON o1.order_id = o2.order_id AND o1.product_id < o2.product_id
JOIN products p1 ON o1.product_id = p1.product_id
JOIN products p2 ON o2.product_id = p2.product_id
GROUP BY o1.product_id, p1.product_name, o2.product_id, p2.product_name
HAVING COUNT(*) > 2
ORDER BY times_bought_together DESC
LIMIT 10;

-- -----------------------------------------------------------------------------
-- QUERY 12: Regional Sales Distribution & Delivery Delay Hotspots
-- Purpose: Maps order fulfillment efficiency across geographic zones.
-- Business Decision Supported: Regional warehouse expansion & carrier SLA negotiation.
-- -----------------------------------------------------------------------------
SELECT 
    s.city AS store_region,
    COUNT(l.logistics_id) AS total_shipments,
    ROUND(AVG(l.actual_days), 1) AS avg_actual_delivery_days,
    ROUND(AVG(l.estimated_days), 1) AS avg_target_delivery_days,
    SUM(CASE WHEN l.delivery_status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_shipments,
    ROUND(CAST(SUM(CASE WHEN l.delivery_status = 'Delayed' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(l.logistics_id), 0) AS NUMERIC), 2) AS delay_rate_pct
FROM logistics l
JOIN orders o ON l.order_id = o.order_id
JOIN stores s ON o.store_id = s.store_id
GROUP BY s.city
ORDER BY delay_rate_pct DESC;

-- -----------------------------------------------------------------------------
-- QUERY 13: Inventory Movement Leakage & Shrinkage Cost Tracking
-- Purpose: Identifies inventory losses due to damage, theft, or unaccounted transfers.
-- Business Decision Supported: Loss prevention auditing & warehouse security checks.
-- -----------------------------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    im.movement_type,
    SUM(ABS(im.quantity_changed)) AS units_affected,
    SUM(ABS(im.quantity_changed) * p.cogs_inr) AS shrinkage_cost_inr
FROM inventory_movements im
JOIN products p ON im.product_id = p.product_id
WHERE im.movement_type IN ('Shrinkage Adjustment', 'Return Inbound')
GROUP BY p.product_id, p.product_name, im.movement_type
ORDER BY shrinkage_cost_inr DESC;

-- -----------------------------------------------------------------------------
-- QUERY 14: Order Fulfillment SLA Compliance Rate
-- Purpose: Tracks the percentage of orders shipped within the promised timeframe.
-- Business Decision Supported: Merchant store tier upgrades/downgrades.
-- -----------------------------------------------------------------------------
SELECT 
    s.store_id,
    s.store_name,
    COUNT(l.logistics_id) AS total_orders,
    SUM(CASE WHEN l.actual_days <= l.estimated_days THEN 1 ELSE 0 END) AS on_time_orders,
    ROUND(CAST(SUM(CASE WHEN l.actual_days <= l.estimated_days THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(l.logistics_id), 0) AS NUMERIC), 2) AS fulfillment_sla_pct
FROM stores s
JOIN orders o ON s.store_id = o.store_id
JOIN logistics l ON o.order_id = l.order_id
GROUP BY s.store_id, s.store_name
HAVING COUNT(l.logistics_id) > 5
ORDER BY fulfillment_sla_pct DESC;

-- -----------------------------------------------------------------------------
-- QUERY 15: Escrow Funds Locked vs. Released Summary
-- Purpose: Monitors live platform escrow liquidity and payout efficiency.
-- Business Decision Supported: Treasury cash management & banking partner review.
-- -----------------------------------------------------------------------------
SELECT 
    status AS escrow_status,
    COUNT(escrow_id) AS transaction_count,
    SUM(escrow_amount_inr) AS total_vault_amount_inr,
    ROUND(AVG(escrow_amount_inr), 2) AS avg_transaction_value_inr
FROM escrow_transactions
GROUP BY status
ORDER BY total_vault_amount_inr DESC;

-- -----------------------------------------------------------------------------
-- QUERY 16: Logistics Carrier On-Time Performance Benchmarking
-- Purpose: Compares BlueDart, Delhivery, Ecom Express delivery performance.
-- Business Decision Supported: Logistics partner allocation logic.
-- -----------------------------------------------------------------------------
SELECT 
    carrier_name,
    COUNT(logistics_id) AS total_parcels,
    ROUND(AVG(actual_days), 2) AS avg_transit_days,
    SUM(CASE WHEN delivery_status = 'Yes' THEN 1 ELSE 0 END) AS on_time_count,
    ROUND(CAST(SUM(CASE WHEN delivery_status = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(logistics_id) AS NUMERIC), 2) AS on_time_delivery_pct,
    ROUND(AVG(shipping_cost_inr), 2) AS avg_shipping_cost_inr
FROM logistics
GROUP BY carrier_name
ORDER BY on_time_delivery_pct DESC;

-- -----------------------------------------------------------------------------
-- QUERY 17: Sales Channel Performance & Conversion Share
-- Purpose: Evaluates revenue contribution by channel (Direct, Marketplace, B2B).
-- Business Decision Supported: Marketing channel spend optimization.
-- -----------------------------------------------------------------------------
SELECT 
    channel_name,
    COUNT(DISTINCT store_id) AS participating_stores,
    ROUND(AVG(revenue_share_pct), 2) AS avg_revenue_share_pct,
    ROUND(AVG(conversion_rate_pct), 2) AS avg_conversion_rate_pct,
    ROUND(AVG(avg_order_value_inr), 2) AS avg_aov_inr
FROM sales_channels
GROUP BY channel_name
ORDER BY avg_revenue_share_pct DESC;

-- -----------------------------------------------------------------------------
-- QUERY 18: Store Valuation Estimator Multiple Breakdown
-- Purpose: Calculates store valuation based on ARR, margin, and health score.
-- Business Decision Supported: VyapaarSetu Store M&A marketplace listing price.
-- -----------------------------------------------------------------------------
SELECT 
    store_id,
    store_name,
    tier,
    monthly_revenue_inr,
    (monthly_revenue_inr * 12) AS annual_recurring_revenue_inr,
    health_score,
    ROUND(CAST(estimated_valuation_inr / NULLIF(monthly_revenue_inr * 12, 0) AS NUMERIC), 2) AS revenue_multiple_x,
    estimated_valuation_inr
FROM stores
ORDER BY estimated_valuation_inr DESC;

-- -----------------------------------------------------------------------------
-- QUERY 19: Comprehensive Monthly Business Health Index
-- Purpose: Tracks solvency, risk index, and growth score over time.
-- Business Decision Supported: Early warning system for distressed merchant stores.
-- -----------------------------------------------------------------------------
SELECT 
    month_period,
    COUNT(DISTINCT store_id) AS stores_evaluated,
    ROUND(AVG(solvency_ratio), 2) AS avg_solvency_ratio,
    ROUND(AVG(risk_score), 1) AS avg_risk_score,
    ROUND(AVG(growth_index), 1) AS avg_growth_index,
    CASE 
        WHEN AVG(risk_score) <= 20 THEN 'Healthy Platform Environment'
        WHEN AVG(risk_score) <= 35 THEN 'Moderate Risk Exposure'
        ELSE 'High Risk Alert'
    END AS system_health_status
FROM business_health
GROUP BY month_period
ORDER BY month_period DESC;

-- -----------------------------------------------------------------------------
-- QUERY 20: LTV to CAC Ratio by Customer Segment
-- Purpose: Evaluates marketing spend efficiency against customer lifetime value.
-- Business Decision Supported: Customer acquisition channel scaling.
-- -----------------------------------------------------------------------------
SELECT 
    segment,
    COUNT(customer_id) AS customer_count,
    ROUND(AVG(lifetime_value_inr), 2) AS avg_ltv_inr,
    ROUND(AVG(total_orders), 1) AS avg_order_frequency,
    ROUND(AVG(lifetime_value_inr) / 2500.0, 2) AS estimated_ltv_to_cac_ratio
FROM customers
GROUP BY segment
ORDER BY avg_ltv_inr DESC;

-- -----------------------------------------------------------------------------
-- QUERY 21: High-Return Product Categories & Defect Root Causes
-- Purpose: Identifies categories experiencing excessive customer return requests.
-- Business Decision Supported: Vendor quality audit & sizing guide updates.
-- -----------------------------------------------------------------------------
SELECT 
    p.category,
    r.return_reason,
    COUNT(r.return_id) AS total_returns,
    SUM(r.refund_amount_inr) AS total_refunded_inr
FROM returns r
JOIN products p ON r.product_id = p.product_id
GROUP BY p.category, r.return_reason
ORDER BY total_returns DESC;

-- -----------------------------------------------------------------------------
-- QUERY 22: Dynamic Price Elasticity & Margin Impact Analysis
-- Purpose: Monitors price changes and evaluates margin sensitivity.
-- Business Decision Supported: Dynamic markdown engine calibration.
-- -----------------------------------------------------------------------------
SELECT 
    ph.change_reason,
    COUNT(ph.pricing_id) AS price_adjustment_count,
    ROUND(AVG(ph.old_price_inr), 2) AS avg_old_price_inr,
    ROUND(AVG(ph.new_price_inr), 2) AS avg_new_price_inr,
    ROUND(AVG((ph.new_price_inr - ph.old_price_inr) / NULLIF(ph.old_price_inr, 0) * 100), 2) AS avg_price_change_pct
FROM pricing_history ph
GROUP BY ph.change_reason
ORDER BY price_adjustment_count DESC;

-- -----------------------------------------------------------------------------
-- QUERY 23: Vendor Restock Lead-Time Variance Analysis
-- Purpose: Identifies supplier delays affecting safety stock buffers.
-- Business Decision Supported: Lead-time buffer adjustment in ERP.
-- -----------------------------------------------------------------------------
SELECT 
    v.vendor_name,
    COUNT(DISTINCT p.product_id) AS supplied_skus,
    ROUND(AVG(p.reorder_level), 1) AS avg_reorder_level,
    ROUND(AVG(p.safety_stock), 1) AS avg_safety_stock,
    ROUND(AVG(v.sla_compliance_pct), 1) AS vendor_sla_pct
FROM vendors v
JOIN products p ON v.vendor_id = p.vendor_id
GROUP BY v.vendor_name
ORDER BY vendor_sla_pct ASC;

-- -----------------------------------------------------------------------------
-- QUERY 24: Quarterly Financial Performance Rollup
-- Purpose: Aggregates sales volume, top revenue, and order counts per quarter.
-- Business Decision Supported: Board reporting & investor financial statements.
-- -----------------------------------------------------------------------------
SELECT 
    EXTRACT(YEAR FROM order_date) AS sales_year,
    EXTRACT(QUARTER FROM order_date) AS sales_quarter,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(total_amount_inr) AS quarterly_revenue_inr,
    ROUND(AVG(total_amount_inr), 2) AS quarterly_aov_inr
FROM orders
WHERE status = 'Delivered'
GROUP BY EXTRACT(YEAR FROM order_date), EXTRACT(QUARTER FROM order_date)
ORDER BY sales_year DESC, sales_quarter DESC;

-- -----------------------------------------------------------------------------
-- QUERY 25: Master Executive KPI Scorecard
-- Purpose: Single-row master rollup query displaying overall platform vital metrics.
-- Business Decision Supported: Daily executive dashboard refresh.
-- -----------------------------------------------------------------------------
SELECT 
    (SELECT COUNT(*) FROM stores) AS total_active_stores,
    (SELECT COUNT(*) FROM vendors WHERE status = 'Active') AS total_active_vendors,
    (SELECT COUNT(*) FROM customers) AS total_customers,
    (SELECT SUM(total_amount_inr) FROM orders WHERE status = 'Delivered') AS total_platform_gmv_inr,
    (SELECT ROUND(AVG(total_amount_inr), 2) FROM orders WHERE status = 'Delivered') AS avg_order_value_inr,
    (SELECT COUNT(*) FROM escrow_transactions WHERE status = 'Funded') AS active_escrow_vaults,
    (SELECT SUM(escrow_amount_inr) FROM escrow_transactions WHERE status = 'Funded') AS total_escrow_locked_inr,
    (SELECT ROUND(AVG(fulfillment_rate_pct), 1) FROM vendor_ratings) AS avg_supplier_sla_pct;
