-- ============================================================================
-- BUSINESS QUESTION 3: Which sales channel delivers the highest net contribution margin?
-- OBJECTIVE: Compare net profit across POS Counter vs Direct D2C vs Marketplaces.
-- DIALECT: ANSI SQL / PostgreSQL / BigQuery
-- ============================================================================

SELECT 
    o.channel,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount_inr) AS gross_revenue_inr,
    SUM(o.quantity * p.cost_price_inr) AS total_cogs_inr,
    SUM(o.shipping_cost_inr) AS total_shipping_inr,
    SUM(o.total_amount_inr - (o.quantity * p.cost_price_inr) - o.shipping_cost_inr) AS net_contribution_margin_inr,
    ROUND(
        (SUM(o.total_amount_inr - (o.quantity * p.cost_price_inr) - o.shipping_cost_inr) / NULLIF(SUM(o.total_amount_inr), 0)) * 100, 2
    ) AS net_margin_pct,
    CASE 
        WHEN channel = 'POS Counter' THEN 'STRATEGY: Highest Net Margin (Zero Shipping/Commission)'
        WHEN channel IN ('Shopify Storefront', 'Instagram DM') THEN 'STRATEGY: High Retention D2C Channel'
        ELSE 'STRATEGY: High Volume / High Marketplace Fee Channel'
    END AS channel_strategy_note
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.order_status = 'Delivered'
GROUP BY o.channel
ORDER BY net_margin_pct DESC;
