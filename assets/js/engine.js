/**
 * VyapaarSetu Live Business OS - Automation & Analytical Calculation Engine
 * File: assets/js/engine.js
 * Parity: All 12 Python automation engines with Business Consequence calculations
 */

const VyapaarEngine = {

  /**
   * Helper: Calculates Business Consequence statement for any operational event
   */
  getBusinessConsequence: function(eventType, data) {
    if (eventType === 'filter_change') {
      return {
        title: '📊 Decision Consequence: Multi-Dimensional Slice & Dice Active',
        body: `Filtering applied across ${data.region || 'All Regions'} for ${data.month || 'Full Year'}. Recomputed GMV, Escrow Liquidity ratio, and Vendor SLA distribution instantly.`
      };
    }
    if (eventType === 'stock_sell') {
      return {
        title: '💸 Working Capital & Inventory Consequence',
        body: `Sold 1 unit of ${data.sku}. Capital +₹${data.price.toLocaleString()} collected into Escrow Vault. Inventory carrying cost reduced by 1.8% in ${data.warehouse}.`
      };
    }
    if (eventType === 'order_automated') {
      return {
        title: '⚡ Operational Automation Consequence',
        body: `Order #${data.order_id} fully processed in 4.2 seconds. Stock auto-deducted, ₹${data.amount.toLocaleString()} locked in ICICI Escrow Vault, and BlueDart logistics AWB generated with 0 human friction.`
      };
    }
    if (eventType === 'po_dispatched') {
      return {
        title: '🤝 Supplier SLA Guarantee Consequence',
        body: `Purchase Order dispatched to ${data.name} (${data.rating}⭐, ${data.sla}% SLA). Projected 48-hour delivery prevents potential ₹45,000 stockout revenue loss.`
      };
    }
    if (eventType === 'escrow_released') {
      return {
        title: '🔒 Escrow Liquidity Consequence',
        body: `Payout for ${data.tx_id} released to Supplier. Merchant trust score increased by +0.2; vendor working capital freed for restocking.`
      };
    }
    return {
      title: '⚡ System State Updated',
      body: 'Business OS recalculated operational metrics with 0ms latency.'
    };
  },

  /**
   * Engine 1 & 2: Store Health Score & Solvency Index Calculator
   */
  evaluateStoreHealth: function(storeId) {
    let store = VyapaarData.stores.find(s => s.id === storeId) || VyapaarData.stores[0];
    let score = store.health_score;
    let rev = store.monthly_revenue;
    let annualArr = rev * 12.0;

    let rating = 'BB - Restructuring Required';
    let riskTier = 'High Risk';
    if (score >= 85) {
      rating = 'AAA - Prime Merchant Storefront';
      riskTier = 'Low Risk (Underwriting Approved)';
    } else if (score >= 70) {
      rating = 'AA - Stable Merchant Storefront';
      riskTier = 'Moderate Risk';
    }

    let arrMultiple = (store.valuation / annualArr).toFixed(2);

    return {
      store_id: store.id,
      store_name: store.name,
      city: store.city,
      tier: store.tier,
      monthly_revenue: rev,
      health_score: score,
      solvency_rating: rating,
      risk_tier: riskTier,
      estimated_valuation: store.valuation,
      arr_multiple_x: arrMultiple,
      consequence: `Valuation of ₹${(store.valuation/100000).toFixed(1)}L computed at ${arrMultiple}x ARR multiple. Solvency rating ${rating} enables instant ICICI Escrow underwriting up to ₹25 Lakhs.`,
      recommendations: score < 80 ? [
        'Margin Leak: Reduce shipping overhead in ' + store.city + ' by switching to local fulfillment hub.',
        'Inventory Velocity: 2 SKUs exceeded 30 days stock age — trigger 15% markdown.',
        'Escrow Liquidity: Increase ICICI Escrow vault coverage ratio by 12% to upgrade to AAA rating.'
      ] : [
        'Optimal Capital Efficiency: Underwriting approval granted for ₹25,00,000 credit line expansion.',
        'Growth Target: Expand B2B WhatsApp broadcast campaigns to acquire +45 regional retailers.'
      ]
    };
  },

  /**
   * Engine 3 & 12: Smart Supplier Selection & Vendor Matcher
   */
  matchVendors: function(category = 'all', sortKey = 'match_score') {
    let matched = [];
    VyapaarData.vendors.forEach(v => {
      if (category === 'all' || v.category.toLowerCase() === category.toLowerCase()) {
        let compositeScore = parseFloat(((v.rating / 5.0 * 50) + (v.sla / 100.0 * 50)).toFixed(1));
        matched.push({
          ...v,
          match_score: compositeScore,
          recommended_tier: compositeScore >= 85 ? 'Preferred Partner' : 'Standard Supplier'
        });
      }
    });

    if (sortKey === 'match_score') matched.sort((a, b) => b.match_score - a.match_score);
    if (sortKey === 'rating') matched.sort((a, b) => b.rating - a.rating);
    if (sortKey === 'sla') matched.sort((a, b) => b.sla - a.sla);
    if (sortKey === 'lead_time') matched.sort((a, b) => a.lead_time_days - b.lead_time_days);

    return matched;
  },

  /**
   * Engine 1 & 6: AI Merchant Growth & Margin Leak Advisor
   */
  runAiAdvisor: function(storeId) {
    let healthEval = this.evaluateStoreHealth(storeId);
    let lowStockItems = VyapaarData.inventory.filter(i => i.qty <= i.reorder_level);
    
    return {
      timestamp: new Date().toLocaleTimeString(),
      store_evaluated: healthEval.store_name,
      health_score: healthEval.health_score,
      solvency: healthEval.solvency_rating,
      margin_leaks: [
        { title: 'Logistics SLA Overhead', impact: '- ₹42,500/mo', text: 'Express 24h shipping used for non-urgent restocking in ' + healthEval.city + '.' },
        { title: 'Dead Stock Carrying Cost', impact: '- ₹18,200/mo', text: lowStockItems.length + ' SKUs approaching critical reorder threshold.' }
      ],
      underperforming_products: [
        { sku: 'SKU-APP-102', text: 'Stock age 34 days. Sales velocity down 22% MoM.' }
      ],
      pricing_recommendations: [
        { action: 'Bundle Pricing', detail: 'Bundle SKU-ELE-001 with POS Scanner for +18% average basket revenue.' }
      ],
      capital_allocation_advice: 'Allocate ₹3,50,000 from Escrow Vault to high-margin Electronics inventory for Q3 festival surge.'
    };
  },

  /**
   * Engine 7 & 8: Real-time Order & Logistics Automation Runner
   */
  simulateOrderWorkflow: function(orderDetails, onStepCallback, onCompleteCallback) {
    const steps = [
      { step: 1, title: 'Order Received', msg: 'New Order #' + orderDetails.order_id + ' received via ' + orderDetails.channel },
      { step: 2, title: 'Inventory Stock -1', msg: 'Deducted 1 unit of ' + orderDetails.sku + ' from ' + orderDetails.warehouse },
      { step: 3, title: 'Redis Cache Sync', msg: 'Updated Redis key `inv:stock:' + orderDetails.sku + '` in 1.4ms' },
      { step: 4, title: 'Warehouse Router', msg: 'Assigned optimal warehouse: ' + orderDetails.warehouse },
      { step: 5, title: 'Vendor SLA Match', msg: 'Assigned supplier: ' + orderDetails.vendor + ' (SLA 98.5%)' },
      { step: 6, title: 'ICICI Escrow Locked', msg: 'Locked ₹' + orderDetails.amount.toLocaleString() + ' in Escrow Vault' },
      { step: 7, title: 'Carrier Shipment Created', msg: 'Generated Waybill AWB-994821 with BlueDart Logistics' },
      { step: 8, title: 'Timeline Updated', msg: 'Pushed status update to Merchant Operations Dashboard' },
      { step: 9, title: 'Notification Sent', msg: 'Sent WhatsApp confirmation & SMS OTP to Buyer' },
      { step: 10, title: 'Dashboard Refresh', msg: 'Recomputed platform GMV & Escrow Vault KPIs' }
    ];

    let stepIdx = 0;

    function executeNextStep() {
      if (stepIdx < steps.length) {
        let stepInfo = steps[stepIdx];
        if (onStepCallback) onStepCallback(stepInfo, (stepIdx + 1) / steps.length * 100);
        stepIdx++;
        setTimeout(executeNextStep, 500);
      } else {
        VyapaarData.orders.unshift({
          id: orderDetails.order_id,
          month: '2025-08',
          date: new Date().toISOString().split('T')[0],
          store: orderDetails.store_name,
          store_id: 'STR-2001',
          region: 'West',
          category: orderDetails.category,
          channel: orderDetails.channel,
          vendor: orderDetails.vendor,
          amount: orderDetails.amount,
          escrow_status: 'Locked in Vault',
          status: 'Processing PO',
          sla_hrs: 24
        });
        if (onCompleteCallback) onCompleteCallback();
      }
    }

    executeNextStep();
  },

  /**
   * Engine 7: Interactive Inventory Sale Simulator
   */
  sellInventoryItem: function(sku) {
    let item = VyapaarData.inventory.find(i => i.sku === sku);
    if (!item) return null;

    if (item.qty > 0) {
      item.qty -= 1;
      if (item.qty <= item.reorder_level) {
        item.status = item.qty === 0 ? 'Out of Stock' : 'Low Stock Alert';
      }
      return {
        sku: item.sku,
        name: item.name,
        qty: item.qty,
        unit_price: item.unit_price,
        warehouse: item.warehouse,
        status: item.status,
        reorder_triggered: item.qty <= item.reorder_level
      };
    }
    return null;
  },

  /**
   * Engine 4: Escrow Vault Action Simulator
   */
  updateEscrowState: function(txId, newStatus) {
    let tx = VyapaarData.escrow_transactions.find(t => t.tx_id === txId);
    if (tx) {
      tx.vault_status = newStatus;
      return tx;
    }
    return null;
  }
};
