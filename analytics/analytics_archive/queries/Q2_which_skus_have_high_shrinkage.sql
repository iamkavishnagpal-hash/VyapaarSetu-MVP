-- ============================================================================
-- BUSINESS QUESTION 2: Which product SKUs suffer from high inventory shrinkage leakage?
-- OBJECTIVE: Identify inventory leakage hotspots between physical store counters and warehouses.
-- DIALECT: ANSI SQL / PostgreSQL / BigQuery
-- ============================================================================

SELECT 
    i.product_id,
    p.sku,
    p.name AS product_name,
    p.category,
    i.warehouse_id,
    w.name AS warehouse_name,
    i.offline_stock_qty,
    i.online_stock_qty,
    (i.offline_stock_qty + i.online_stock_qty) AS total_book_stock,
    i.shrinkage_rate_pct,
    ROUND(((i.offline_stock_qty + i.online_stock_qty) * (i.shrinkage_rate_pct / 100.0) * p.cost_price_inr), 2) AS estimated_shrinkage_loss_inr,
    CASE 
        WHEN i.shrinkage_rate_pct >= 3.5 THEN 'ACTION: Immediate Physical POS & Shelf Audit Required'
        WHEN i.shrinkage_rate_pct >= 2.0 THEN 'WARNING: Monitor Counter Giveaway Logs'
        ELSE 'NORMAL'
    END AS operational_recommendation
FROM inventory_logs i
JOIN products p ON i.product_id = p.product_id
JOIN warehouses w ON i.warehouse_id = w.warehouse_id
WHERE i.shrinkage_rate_pct >= 2.0
ORDER BY estimated_shrinkage_loss_inr DESC;
