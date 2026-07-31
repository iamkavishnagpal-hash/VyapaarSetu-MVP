-- ============================================================================
-- BUSINESS QUESTION 4: Which B2B suppliers meet quality & delivery SLAs?
-- OBJECTIVE: Calculate composite health scores to classify suppliers into Preferred vs Standard vs High Risk tiers.
-- DIALECT: ANSI SQL / PostgreSQL / BigQuery
-- ============================================================================

SELECT 
    v.vendor_id,
    v.name AS vendor_name,
    v.category,
    v.location,
    v.rating,
    v.lead_time_days,
    v.on_time_rate_pct,
    v.defect_rate_pct,
    v.escrow_verified,
    ROUND(
        (v.on_time_rate_pct * 0.40) + 
        ((100.0 - v.defect_rate_pct) * 0.40) + 
        (v.rating * 4.0) + 
        (CASE WHEN v.escrow_verified = 'TRUE' THEN 5.0 ELSE 0.0 END), 2
    ) AS composite_vendor_score,
    CASE 
        WHEN (v.on_time_rate_pct * 0.40) + ((100.0 - v.defect_rate_pct) * 0.40) + (v.rating * 4.0) + (CASE WHEN v.escrow_verified = 'TRUE' THEN 5.0 ELSE 0.0 END) >= 90.0 THEN 'TIER 1: Preferred Vendor (Auto Escrow Release)'
        WHEN (v.on_time_rate_pct * 0.40) + ((100.0 - v.defect_rate_pct) * 0.40) + (v.rating * 4.0) >= 75.0 THEN 'TIER 2: Standard Vendor'
        ELSE 'TIER 3: High Risk Vendor (Mandatory Escrow Hold & Batch QA Audit)'
    END AS supplier_tier
FROM vendors v
ORDER BY composite_vendor_score DESC;
