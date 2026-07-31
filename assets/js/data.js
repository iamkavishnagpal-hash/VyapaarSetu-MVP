/**
 * VyapaarSetu Live Business OS - Master Data Layer
 * File: assets/js/data.js
 * Source Parity: Extracted and structured from data/*.csv
 */

const VyapaarData = {
  months: [
    { id: 'all', name: 'All Months (Full Year)' },
    { id: '2025-01', name: 'January 2025' },
    { id: '2025-02', name: 'February 2025' },
    { id: '2025-03', name: 'March 2025' },
    { id: '2025-04', name: 'April 2025' },
    { id: '2025-05', name: 'May 2025' },
    { id: '2025-06', name: 'June 2025' },
    { id: '2025-07', name: 'July 2025' },
    { id: '2025-08', name: 'August 2025' }
  ],

  regions: [
    { id: 'all', name: 'All India Regions' },
    { id: 'West', name: 'West Region (Mumbai, Surat, Ahmedabad, Pune)' },
    { id: 'North', name: 'North Region (Delhi, Jaipur)' },
    { id: 'South', name: 'South Region (Bengaluru, Chennai, Hyderabad)' },
    { id: 'East', name: 'East Region (Kolkata)' }
  ],

  categories: [
    { id: 'all', name: 'All Product Categories' },
    { id: 'Apparel', name: 'Apparel & Garments' },
    { id: 'Electronics', name: 'Consumer Electronics' },
    { id: 'Footwear', name: 'Footwear & Shoes' },
    { id: 'FMCG', name: 'Food & FMCG Grocery' },
    { id: 'Home Decor', name: 'Home & Kitchen Decor' },
    { id: 'Health & Beauty', name: 'Personal Care & Beauty' },
    { id: 'Industrial Hardware', name: 'Industrial Supplies & Tools' }
  ],

  channels: [
    { id: 'all', name: 'All Sales Channels' },
    { id: 'B2B Portal', name: 'VyapaarSetu B2B Portal' },
    { id: 'WhatsApp Business', name: 'WhatsApp Commerce Bot' },
    { id: 'Direct ERP API', name: 'Direct ERP Integration' },
    { id: 'Wholesale Market', name: 'Physical Wholesale Hub' }
  ],

  stores: [
    { id: 'STR-2001', name: 'Vyapaar Electronics (Surat)', city: 'Surat', region: 'West', tier: 'Gold', monthly_revenue: 1802640, health_score: 94, valuation: 4850000, category: 'Electronics' },
    { id: 'STR-2002', name: 'Mumbai Apparel Hub', city: 'Mumbai', region: 'West', tier: 'Silver', monthly_revenue: 1187181, health_score: 86, valuation: 3474509, category: 'Apparel' },
    { id: 'STR-2003', name: 'Bengaluru Tech Depot', city: 'Bengaluru', region: 'South', tier: 'Platinum', monthly_revenue: 2384495, health_score: 95, valuation: 6258312, category: 'Electronics' },
    { id: 'STR-2004', name: 'Delhi Retail Traders', city: 'Delhi', region: 'North', tier: 'Gold', monthly_revenue: 1454591, health_score: 78, valuation: 3612860, category: 'Home Decor' },
    { id: 'STR-2005', name: 'Jaipur Fashion Store', city: 'Jaipur', region: 'North', tier: 'Silver', monthly_revenue: 1501843, health_score: 80, valuation: 4373731, category: 'Apparel' },
    { id: 'STR-2006', name: 'Pune FMCG Wholesale', city: 'Pune', region: 'West', tier: 'Bronze', monthly_revenue: 912226, health_score: 68, valuation: 1771785, category: 'FMCG' },
    { id: 'STR-2007', name: 'Hyderabad Beauty Outlet', city: 'Hyderabad', region: 'South', tier: 'Gold', monthly_revenue: 2078286, health_score: 91, valuation: 4656042, category: 'Health & Beauty' },
    { id: 'STR-2008', name: 'Kolkata Industrial Hub', city: 'Kolkata', region: 'East', tier: 'Silver', monthly_revenue: 1224763, health_score: 72, valuation: 2780589, category: 'Industrial Hardware' }
  ],

  vendors: [
    { id: 'VND-1001', name: 'Apex Electronics Wholesale', category: 'Electronics', city: 'Mumbai', region: 'West', rating: 4.8, sla: 98.5, status: 'Preferred Partner', lead_time_days: 2, price_index: 'Low' },
    { id: 'VND-1002', name: 'Surat Textile Mills Ltd', category: 'Apparel', city: 'Surat', region: 'West', rating: 4.6, sla: 94.2, status: 'Preferred Partner', lead_time_days: 3, price_index: 'Medium' },
    { id: 'VND-1003', name: 'TechDistro India', category: 'Electronics', city: 'Bengaluru', region: 'South', rating: 4.7, sla: 96.8, status: 'Preferred Partner', lead_time_days: 2, price_index: 'Low' },
    { id: 'VND-1004', name: 'Delhi Industrial Supply Co', category: 'Industrial Hardware', city: 'Delhi', region: 'North', rating: 4.1, sla: 89.4, status: 'Standard Supplier', lead_time_days: 5, price_index: 'Medium' },
    { id: 'VND-1005', name: 'Hyderabad Organics & Beauty', category: 'Health & Beauty', city: 'Hyderabad', region: 'South', rating: 4.5, sla: 92.1, status: 'Preferred Partner', lead_time_days: 4, price_index: 'Low' },
    { id: 'VND-1006', name: 'Kolkata Foods & Spices', category: 'FMCG', city: 'Kolkata', region: 'East', rating: 4.4, sla: 97.6, status: 'Preferred Partner', lead_time_days: 3, price_index: 'Low' },
    { id: 'VND-1007', name: 'Jaipur Footwear Crafts', category: 'Footwear', city: 'Jaipur', region: 'North', rating: 3.9, sla: 85.0, status: 'Under Review', lead_time_days: 6, price_index: 'High' }
  ],

  inventory: [
    { sku: 'SKU-ELE-001', name: 'Wireless Smart POS Terminal', category: 'Electronics', store_id: 'STR-2001', warehouse: 'WH-West-Surat', qty: 45, reorder_level: 15, unit_price: 12500, status: 'Optimal' },
    { sku: 'SKU-ELE-002', name: 'Barcode Thermal Scanner', category: 'Electronics', store_id: 'STR-2003', warehouse: 'WH-South-Blr', qty: 8, reorder_level: 10, unit_price: 4800, status: 'Low Stock Alert' },
    { sku: 'SKU-APP-101', name: 'Cotton Retail Shirts Pack (50)', category: 'Apparel', store_id: 'STR-2002', warehouse: 'WH-West-Mumbai', qty: 120, reorder_level: 30, unit_price: 18500, status: 'Optimal' },
    { sku: 'SKU-APP-102', name: 'Designer Silk Sarees Bundle', category: 'Apparel', store_id: 'STR-2005', warehouse: 'WH-North-Jaipur', qty: 14, reorder_level: 20, unit_price: 32000, status: 'Low Stock Alert' },
    { sku: 'SKU-FMC-201', name: 'Organic Spices Wholesale Box', category: 'FMCG', store_id: 'STR-2006', warehouse: 'WH-West-Pune', qty: 250, reorder_level: 50, unit_price: 3400, status: 'Optimal' },
    { sku: 'SKU-BEA-301', name: 'Herbal Skincare Kit (100 units)', category: 'Health & Beauty', store_id: 'STR-2007', warehouse: 'WH-South-Hyd', qty: 5, reorder_level: 25, unit_price: 14200, status: 'Critical Stock' },
    { sku: 'SKU-IND-401', name: 'Precision Caliper Tool Set', category: 'Industrial Hardware', store_id: 'STR-2008', warehouse: 'WH-East-Kolkata', qty: 62, reorder_level: 15, unit_price: 8900, status: 'Optimal' }
  ],

  orders: [
    { id: 'ORD-8901', month: '2025-07', date: '2025-07-28', store: 'Vyapaar Electronics (Surat)', store_id: 'STR-2001', region: 'West', category: 'Electronics', channel: 'B2B Portal', vendor: 'Apex Electronics Wholesale', amount: 145000, escrow_status: 'Locked in Vault', status: 'In Transit', sla_hrs: 18 },
    { id: 'ORD-8902', month: '2025-07', date: '2025-07-27', store: 'Bengaluru Tech Depot', store_id: 'STR-2003', region: 'South', category: 'Electronics', channel: 'Direct ERP API', vendor: 'TechDistro India', amount: 280000, escrow_status: 'Funds Released', status: 'Delivered', sla_hrs: 12 },
    { id: 'ORD-8903', month: '2025-07', date: '2025-07-25', store: 'Mumbai Apparel Hub', store_id: 'STR-2002', region: 'West', category: 'Apparel', channel: 'WhatsApp Business', vendor: 'Surat Textile Mills Ltd', amount: 92000, escrow_status: 'Inspection Hold', status: 'Quality Inspection', sla_hrs: 24 },
    { id: 'ORD-8904', month: '2025-06', date: '2025-06-18', store: 'Delhi Retail Traders', store_id: 'STR-2004', region: 'North', category: 'Home Decor', channel: 'B2B Portal', vendor: 'Delhi Industrial Supply Co', amount: 64000, escrow_status: 'Funds Released', status: 'Delivered', sla_hrs: 36 },
    { id: 'ORD-8905', month: '2025-06', date: '2025-06-12', store: 'Hyderabad Beauty Outlet', store_id: 'STR-2007', region: 'South', category: 'Health & Beauty', channel: 'WhatsApp Business', vendor: 'Hyderabad Organics & Beauty', amount: 115000, escrow_status: 'Locked in Vault', status: 'Processing PO', sla_hrs: 14 }
  ],

  escrow_transactions: [
    { tx_id: 'ESC-4001', order_id: 'ORD-8901', buyer: 'Vyapaar Electronics', supplier: 'Apex Electronics', amount: 145000, vault_status: 'Locked & Protected', funded_at: '2025-07-28 10:30', inspection_due: '2025-07-30' },
    { tx_id: 'ESC-4002', order_id: 'ORD-8902', buyer: 'Bengaluru Tech Depot', supplier: 'TechDistro India', amount: 280000, vault_status: 'Released to Vendor', funded_at: '2025-07-27 14:15', inspection_due: 'Completed' },
    { tx_id: 'ESC-4003', order_id: 'ORD-8903', buyer: 'Mumbai Apparel Hub', supplier: 'Surat Textile Mills', amount: 92000, vault_status: 'Under Inspection Hold', funded_at: '2025-07-25 09:00', inspection_due: '2025-07-29' }
  ],

  customer_rfm_segments: [
    { segment: 'Champions', count: 142, avg_gmv_inr: 450000, retention_pct: 94.2, recommended_campaign: 'Exclusive High-Volume Escalation Discounts via WhatsApp' },
    { segment: 'Loyal Merchant Buyers', count: 280, avg_gmv_inr: 210000, retention_pct: 88.5, recommended_campaign: 'Quarterly Inventory Reorder Credit Lines' },
    { segment: 'At-Risk Merchant Stores', count: 85, avg_gmv_inr: 95000, retention_pct: 54.0, recommended_campaign: 'Automated 12% Markdown Clearance Bundles' },
    { segment: 'Lapsed Storefronts', count: 42, avg_gmv_inr: 40000, retention_pct: 22.1, recommended_campaign: 'Re-engagement Working Capital Loan Assist' }
  ]
};

// Helper filtering function
VyapaarData.getFilteredOrders = function(filters) {
  return this.orders.filter(order => {
    if (filters.month && filters.month !== 'all' && order.month !== filters.month) return false;
    if (filters.region && filters.region !== 'all' && order.region !== filters.region) return false;
    if (filters.store && filters.store !== 'all' && order.store_id !== filters.store) return false;
    if (filters.category && filters.category !== 'all' && order.category !== filters.category) return false;
    if (filters.channel && filters.channel !== 'all' && order.channel !== filters.channel) return false;
    return true;
  });
};
