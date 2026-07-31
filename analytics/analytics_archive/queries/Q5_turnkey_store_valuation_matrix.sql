-- ============================================================================
-- BUSINESS QUESTION 5: How do we calculate fair store asking prices for turnkey acquisitions?
-- OBJECTIVE: Evaluate store valuation multiples against audited monthly revenue and net profit.
-- DIALECT: ANSI SQL / PostgreSQL / BigQuery
-- ============================================================================

SELECT 
    s.store_id,
    s.store_name,
    s.category,
    s.location,
    s.monthly_revenue_inr,
    s.monthly_profit_inr,
    s.profit_margin_pct,
    s.online_share_pct,
    s.asking_price_inr,
    s.valuation_multiple,
    (s.monthly_profit_inr * 12) AS annual_net_profit_inr,
    ROUND((s.asking_price_inr / NULLIF(s.monthly_profit_inr * 12, 0)), 2) AS calculated_annual_pe_multiple,
    CASE 
        WHEN s.profit_margin_pct >= 20.0 AND s.valuation_multiple <= 2.5 THEN 'PRIME BUYING OPPORTUNITY (Under-Valued)'
        WHEN s.valuation_multiple > 3.0 THEN 'OVERVALUED — Negotiate Down'
        ELSE 'FAIR MARKET VALUE'
    END AS buyer_advisory_recommendation
FROM stores s
WHERE s.status = 'For Sale'
ORDER BY profit_margin_pct DESC;
