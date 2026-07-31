-- ============================================================================
-- BUSINESS QUESTION 1: Why are net profits dropping despite gross revenue growth?
-- OBJECTIVE: Diagnose margin erosion by isolating shipping overhead, return costs, and channel commission fees.
-- DIALECT: ANSI SQL / PostgreSQL / BigQuery
-- ============================================================================

WITH order_financials AS (
    SELECT 
        o.order_id,
        o.order_date,
        o.channel,
        o.product_id,
        o.quantity,
        o.total_amount_inr AS gross_revenue,
        o.shipping_cost_inr AS shipping_cost,
        (o.quantity * p.cost_price_inr) AS cogs,
        CASE WHEN o.order_status = 'Returned' THEN o.total_amount_inr ELSE 0 END AS returned_revenue,
        CASE WHEN o.order_status = 'Cancelled' THEN o.total_amount_inr ELSE 0 END AS cancelled_revenue
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
),
channel_agg AS (
    SELECT 
        channel,
        COUNT(order_id) AS total_orders,
        SUM(gross_revenue) AS total_gross_revenue,
        SUM(cogs) AS total_cogs,
        SUM(shipping_cost) AS total_shipping_cost,
        SUM(returned_revenue) AS total_returned_revenue,
        SUM(gross_revenue - cogs - shipping_cost - returned_revenue) AS net_profit
    FROM order_financials
    GROUP BY channel
)
SELECT 
    channel,
    total_orders,
    total_gross_revenue,
    total_cogs,
    total_shipping_cost,
    total_returned_revenue,
    net_profit,
    ROUND((net_profit / NULLIF(total_gross_revenue, 0)) * 100, 2) AS net_margin_pct,
    ROUND((total_shipping_cost / NULLIF(total_gross_revenue, 0)) * 100, 2) AS shipping_ratio_pct,
    ROUND((total_returned_revenue / NULLIF(total_gross_revenue, 0)) * 100, 2) AS return_ratio_pct,
    CASE 
        WHEN (total_returned_revenue / NULLIF(total_gross_revenue, 0)) > 0.10 THEN 'DIAGNOSIS: High RTO / Return Fee Burn'
        WHEN (total_shipping_cost / NULLIF(total_gross_revenue, 0)) > 0.15 THEN 'DIAGNOSIS: Excessive Shipping Overhead'
        ELSE 'HEALTHY MARGIN'
    END AS business_decision_insight
FROM channel_agg
ORDER BY net_profit DESC;
