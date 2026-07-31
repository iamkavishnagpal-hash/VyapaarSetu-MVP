/**
 * VyapaarSetu Live Business OS - Master UI & Application Controller
 * File: assets/js/app.js
 */

const App = {
  state: {
    activeView: 'dashboard',
    activeMode: 'run',
    filters: {
      month: 'all',
      region: 'all',
      store: 'all',
      category: 'all',
      channel: 'all'
    },
    charts: {}
  },

  init: function() {
    this.populateFilterDropdowns();
    this.renderOnboardingModalGrid();
    this.bindEvents();
    this.renderActiveView();
    this.showToast('🚀 System Online: 12 Business OS Engines Active');
  },

  populateFilterDropdowns: function() {
    const monthSel = document.getElementById('filter-month');
    const regionSel = document.getElementById('filter-region');
    const storeSel = document.getElementById('filter-store');
    const catSel = document.getElementById('filter-category');
    const chanSel = document.getElementById('filter-channel');

    if (monthSel) monthSel.innerHTML = VyapaarData.months.map(m => `<option value="${m.id}">${m.name}</option>`).join('');
    if (regionSel) regionSel.innerHTML = VyapaarData.regions.map(r => `<option value="${r.id}">${r.name}</option>`).join('');
    if (storeSel) storeSel.innerHTML = `<option value="all">All Storefronts (18 Active)</option>` + VyapaarData.stores.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
    if (catSel) catSel.innerHTML = VyapaarData.categories.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
    if (chanSel) chanSel.innerHTML = VyapaarData.channels.map(ch => `<option value="${ch.id}">${ch.name}</option>`).join('');
  },

  renderOnboardingModalGrid: function() {
    const container = document.getElementById('onboarding-goals-grid');
    if (!container) return;

    container.innerHTML = VyapaarData.b2bOnboardingGoals.map(goal => `
      <div class="onboarding-btn" onclick="App.selectBusinessObjective('${goal.id}')">
        <div style="font-size:1.5rem;">${goal.icon}</div>
        <div>
          <div class="onboarding-btn-title">${goal.title}</div>
          <div class="onboarding-btn-desc">${goal.desc}</div>
        </div>
      </div>
    `).join('');
  },

  openOnboardingModal: function() {
    const modal = document.getElementById('modal-onboarding');
    if (modal) modal.classList.add('active');
  },

  closeOnboardingModal: function() {
    const modal = document.getElementById('modal-onboarding');
    if (modal) modal.classList.remove('active');
  },

  selectBusinessObjective: function(goalId) {
    const goal = VyapaarData.b2bOnboardingGoals.find(g => g.id === goalId);
    if (goal) {
      this.closeOnboardingModal();
      this.switchMode(goal.mode);
      this.switchView(goal.view, document.getElementById(`nav-${goal.view}`));
      
      const banner = document.getElementById('consequence-banner');
      if (banner) {
        banner.innerHTML = `
          <div class="consequence-icon">🎯</div>
          <div>
            <div class="consequence-title">Active B2B Business Objective: ${goal.title}</div>
            <div class="consequence-body">System configured to optimize ${goal.desc}. Platform telemetry and AI recommendations tuned to this goal.</div>
          </div>
        `;
        banner.style.display = 'flex';
      }
      this.showToast(`Selected Business Goal: ${goal.title}`);
    }
  },

  bindEvents: function() {
    ['month', 'region', 'store', 'category', 'channel'].forEach(filterKey => {
      const elem = document.getElementById(`filter-${filterKey}`);
      if (elem) {
        elem.addEventListener('change', (e) => {
          this.state.filters[filterKey] = e.target.value;
          this.onFilterChange();
        });
      }
    });

    const resetBtn = document.getElementById('btn-reset-filters');
    if (resetBtn) resetBtn.addEventListener('click', () => this.resetFilters());
  },

  switchView: function(viewId, navElem) {
    this.state.activeView = viewId;
    document.querySelectorAll('.view-panel').forEach(el => el.classList.remove('active'));
    
    const targetPanel = document.getElementById(`view-${viewId}`);
    if (targetPanel) targetPanel.classList.add('active');

    document.querySelectorAll('nav li').forEach(el => el.classList.remove('active'));
    if (navElem) navElem.classList.add('active');

    const titleMap = {
      'dashboard': 'Executive Command Center (Power BI Analytics)',
      'ai-advisor': 'AI Merchant Growth & Margin Leak Advisor',
      'automation': 'Live Order Workflow & Automation Runner',
      'inventory': 'Real-Time Inventory Command & Reorder Sync',
      'vendors': 'Supplier Matching & SLA Compliance Matrix',
      'escrow': 'ICICI Escrow Vault & Trade Liquidity Flow',
      'growth': 'Customer RFM Cohort & Growth Intelligence',
      'store-health': 'Store Solvency Score & M&A Marketplace',
      'logistics': 'Carrier Routing & Dispatch Control',
      'settings': 'Platform Security & Webhook Setup'
    };

    const headerTitle = document.getElementById('view-header-title');
    if (headerTitle) headerTitle.innerText = titleMap[viewId] || 'VyapaarSetu Command Center';

    this.renderActiveView();
  },

  switchMode: function(mode, btnElem) {
    this.state.activeMode = mode;
    document.querySelectorAll('.mode-btn').forEach(el => el.classList.remove('active'));
    if (btnElem) btnElem.classList.add('active');
    this.showToast(`Switched Business Mode: ${mode.toUpperCase()}`);
  },

  onFilterChange: function() {
    const consequence = VyapaarEngine.getBusinessConsequence('filter_change', this.state.filters);
    const banner = document.getElementById('consequence-banner');
    if (banner) {
      banner.innerHTML = `
        <div class="consequence-icon">📊</div>
        <div>
          <div class="consequence-title">${consequence.title}</div>
          <div class="consequence-body">${consequence.body}</div>
        </div>
      `;
      banner.style.display = 'flex';
    }

    this.showToast('🔍 Analytics recalculated for selected filters');
    this.renderActiveView();
  },

  resetFilters: function() {
    this.state.filters = { month: 'all', region: 'all', store: 'all', category: 'all', channel: 'all' };
    this.populateFilterDropdowns();
    this.onFilterChange();
    this.showToast('Filter constraints cleared');
  },

  renderActiveView: function() {
    const view = this.state.activeView;
    if (view === 'dashboard') this.renderDashboardView();
    if (view === 'ai-advisor') this.renderAiAdvisorView();
    if (view === 'automation') this.renderAutomationView();
    if (view === 'inventory') this.renderInventoryView();
    if (view === 'vendors') this.renderVendorsView();
    if (view === 'escrow') this.renderEscrowView();
    if (view === 'growth') this.renderGrowthView();
    if (view === 'store-health') this.renderStoreHealthView();
  },

  /**
   * Module 1: Executive Dashboard (Line Chart, Donut Chart, Bar Chart, Heatmap Grid)
   */
  renderDashboardView: function() {
    const filteredOrders = VyapaarData.getFilteredOrders(this.state.filters);
    
    let grossGmv = filteredOrders.reduce((sum, o) => sum + o.amount, 0);
    if (grossGmv === 0 && this.state.filters.month === 'all') grossGmv = 4850200;

    let lockedEscrow = VyapaarData.escrow_transactions
      .filter(t => t.vault_status.includes('Locked'))
      .reduce((sum, t) => sum + t.amount, 0);

    let lowStockCount = VyapaarData.inventory.filter(i => i.qty <= i.reorder_level).length;

    const gmvElem = document.getElementById('kpi-gmv');
    if (gmvElem) gmvElem.innerText = '₹ ' + grossGmv.toLocaleString();

    const escrowElem = document.getElementById('kpi-escrow');
    if (escrowElem) escrowElem.innerText = '₹ ' + lockedEscrow.toLocaleString();

    const riskElem = document.getElementById('kpi-risk-skus');
    if (riskElem) riskElem.innerText = lowStockCount + ' SKUs';

    const tableBody = document.getElementById('dashboard-orders-tbody');
    if (tableBody) {
      const displayOrders = filteredOrders.length > 0 ? filteredOrders : VyapaarData.orders;
      tableBody.innerHTML = displayOrders.map(o => `
        <tr>
          <td style="font-weight:700; color:var(--accent-indigo);">${o.id}</td>
          <td>${o.store}</td>
          <td><span class="badge badge-cyan">${o.category}</span></td>
          <td>${o.channel}</td>
          <td style="font-weight:700;">₹ ${o.amount.toLocaleString()}</td>
          <td><span class="badge ${o.escrow_status.includes('Released') ? 'badge-emerald' : 'badge-amber'}">${o.escrow_status}</span></td>
          <td><span class="badge ${o.status === 'Delivered' ? 'badge-emerald' : 'badge-indigo'}">${o.status}</span></td>
        </tr>
      `).join('');
    }

    this.renderDashboardCharts(filteredOrders);
    this.renderHeatmapGrid();
  },

  renderDashboardCharts: function(filteredOrders) {
    if (typeof Chart === 'undefined') return;

    // Line Chart
    const ctxLine = document.getElementById('chart-revenue-line');
    if (ctxLine) {
      if (this.state.charts.line) this.state.charts.line.destroy();
      this.state.charts.line = new Chart(ctxLine, {
        type: 'line',
        data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
          datasets: [
            { label: 'Gross GMV (INR)', data: [3200000, 3500000, 3900000, 4100000, 4400000, 4650000, 4850200, 5100000], borderColor: '#6366f1', backgroundColor: 'rgba(99, 102, 241, 0.1)', fill: true, tension: 0.4 },
            { label: 'Net Profit Margin (INR)', data: [420000, 480000, 520000, 580000, 640000, 690000, 740000, 810000], borderColor: '#10b981', borderDash: [5, 5], fill: false, tension: 0.4 }
          ]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#94a3b8' } } },
          scales: { x: { ticks: { color: '#94a3b8' } }, y: { ticks: { color: '#94a3b8' } } }
        }
      });
    }

    // Donut Chart
    const ctxDonut = document.getElementById('chart-channel-donut');
    if (ctxDonut) {
      if (this.state.charts.donut) this.state.charts.donut.destroy();
      this.state.charts.donut = new Chart(ctxDonut, {
        type: 'doughnut',
        data: {
          labels: ['B2B Portal', 'WhatsApp Commerce', 'Direct ERP API', 'Wholesale Hub'],
          datasets: [{ data: [45, 30, 15, 10], backgroundColor: ['#6366f1', '#10b981', '#06b6d4', '#f59e0b'], borderWidth: 0 }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8', font: { size: 10 } } } } }
      });
    }

    // Bar Chart: Storefront GMV vs Solvency
    const ctxBar = document.getElementById('chart-store-bar');
    if (ctxBar) {
      if (this.state.charts.bar) this.state.charts.bar.destroy();
      this.state.charts.bar = new Chart(ctxBar, {
        type: 'bar',
        data: {
          labels: ['Bengaluru', 'Surat', 'Hyderabad', 'Mumbai', 'Jaipur', 'Delhi'],
          datasets: [
            { label: 'Monthly GMV (₹ Lakhs)', data: [23.8, 18.0, 20.7, 11.8, 15.0, 14.5], backgroundColor: '#6366f1' },
            { label: 'Solvency Score (/100)', data: [95, 94, 91, 86, 80, 78], backgroundColor: '#10b981' }
          ]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#94a3b8' } } },
          scales: { x: { ticks: { color: '#94a3b8' } }, y: { ticks: { color: '#94a3b8' } } }
        }
      });
    }
  },

  renderHeatmapGrid: function() {
    const container = document.getElementById('heatmap-container');
    if (!container) return;

    const regions = [
      { name: 'West Region (Surat/Mumbai)', status: 'high', val: '98.2% Stock Density' },
      { name: 'North Region (Delhi/Jaipur)', status: 'med', val: '84.0% Stock Density' },
      { name: 'South Region (Blr/Hyd)', status: 'high', val: '96.5% Stock Density' },
      { name: 'East Region (Kolkata)', status: 'low', val: '68.0% Stock Density' }
    ];

    container.innerHTML = regions.map(r => `
      <div class="heatmap-cell ${r.status}">
        <div style="font-weight:700; margin-bottom:0.2rem;">${r.name}</div>
        <div>${r.val}</div>
      </div>
    `).join('');
  },

  triggerOrderSimulation: function() {
    const btn = document.getElementById('btn-run-automation');
    if (btn) btn.disabled = true;

    const sampleOrder = {
      order_id: 'ORD-' + Math.floor(1000 + Math.random() * 9000),
      channel: 'WhatsApp Business',
      sku: 'SKU-ELE-001',
      warehouse: 'WH-West-Surat',
      vendor: 'Apex Electronics Wholesale',
      store_name: 'Vyapaar Electronics (Surat)',
      category: 'Electronics',
      amount: 145000
    };

    const terminal = document.getElementById('automation-terminal');
    if (terminal) terminal.innerHTML = `<div class="terminal-line"><span class="terminal-time">[SYS INIT]</span> Launching Order Automation Pipeline...</div>`;

    VyapaarEngine.simulateOrderWorkflow(
      sampleOrder,
      (stepInfo, progressPct) => {
        const stepElem = document.getElementById(`wf-step-${stepInfo.step}`);
        if (stepElem) {
          stepElem.classList.add('active');
          if (stepInfo.step > 1) {
            const prevStep = document.getElementById(`wf-step-${stepInfo.step - 1}`);
            if (prevStep) prevStep.classList.add('completed');
          }
        }

        const trackFill = document.getElementById('wf-track-fill');
        if (trackFill) trackFill.style.width = `${progressPct}%`;

        if (terminal) {
          terminal.innerHTML += `<div class="terminal-line"><span class="terminal-time">[${new Date().toLocaleTimeString()}]</span> ${stepInfo.msg}</div>`;
          terminal.scrollTop = terminal.scrollHeight;
        }
      },
      () => {
        if (btn) btn.disabled = false;
        const consequence = VyapaarEngine.getBusinessConsequence('order_automated', sampleOrder);
        
        const banner = document.getElementById('consequence-banner');
        if (banner) {
          banner.innerHTML = `
            <div class="consequence-icon">⚡</div>
            <div>
              <div class="consequence-title">${consequence.title}</div>
              <div class="consequence-body">${consequence.body}</div>
            </div>
          `;
          banner.style.display = 'flex';
        }

        this.showToast('✅ Order Workflow Completed — Inventory & Escrow Updated');
        if (typeof confetti !== 'undefined') confetti({ particleCount: 50, spread: 60 });
        this.renderDashboardView();
      }
    );
  },

  triggerSell: function(sku) {
    const res = VyapaarEngine.sellInventoryItem(sku);
    if (res) {
      const qtyElem = document.getElementById(`qty-${sku}`);
      if (qtyElem) qtyElem.innerText = res.qty + ' units';

      const badgeElem = document.getElementById(`badge-${sku}`);
      if (badgeElem) {
        badgeElem.innerText = res.status;
        badgeElem.className = `badge ${res.qty <= 15 ? 'badge-rose' : 'badge-emerald'}`;
      }

      const consequence = VyapaarEngine.getBusinessConsequence('stock_sell', { sku: sku, price: res.unit_price, warehouse: res.warehouse });
      const banner = document.getElementById('consequence-banner');
      if (banner) {
        banner.innerHTML = `
          <div class="consequence-icon">💸</div>
          <div>
            <div class="consequence-title">${consequence.title}</div>
            <div class="consequence-body">${consequence.body}</div>
          </div>
        `;
        banner.style.display = 'flex';
      }

      this.showToast(`Sold 1 unit of ${sku}. Remaining: ${res.qty}`);
      if (res.reorder_triggered) {
        this.showToast(`⚠️ Low Stock Alert triggered for ${sku}! Reorder PO dispatched.`, 'warning');
      }
      this.renderDashboardView();
    }
  },

  renderAiAdvisorView: function() {
    const storeSel = document.getElementById('ai-store-select');
    const storeId = storeSel ? storeSel.value : 'STR-2001';
    const advice = VyapaarEngine.runAiAdvisor(storeId);

    const titleElem = document.getElementById('ai-evaluated-store');
    if (titleElem) titleElem.innerText = advice.store_evaluated + ' (Health: ' + advice.health_score + '/100)';

    const listElem = document.getElementById('ai-insights-container');
    if (listElem) {
      listElem.innerHTML = `
        <div class="ai-insight-item warning">
          <div class="ai-title">⚠️ Margin Leak Flagged</div>
          <div class="ai-desc">${advice.margin_leaks[0].title}: ${advice.margin_leaks[0].text} Impact: <strong>${advice.margin_leaks[0].impact}</strong></div>
        </div>
        <div class="ai-insight-item critical">
          <div class="ai-title">📦 Inventory Velocity Alert</div>
          <div class="ai-desc">${advice.underperforming_products[0].text}</div>
        </div>
        <div class="ai-insight-item opportunity">
          <div class="ai-title">📈 Recommended Capital Allocation</div>
          <div class="ai-desc">${advice.capital_allocation_advice}</div>
        </div>
      `;
    }
  },

  renderInventoryView: function() {
    const tbody = document.getElementById('inventory-tbody');
    if (!tbody) return;

    tbody.innerHTML = VyapaarData.inventory.map(item => `
      <tr>
        <td style="font-weight:700; color:var(--accent-cyan);">${item.sku}</td>
        <td>${item.name}</td>
        <td>${item.warehouse}</td>
        <td style="font-weight:700; font-size:1rem;" id="qty-${item.sku}">${item.qty} units</td>
        <td>₹ ${item.unit_price.toLocaleString()}</td>
        <td><span class="badge ${item.qty <= item.reorder_level ? 'badge-rose' : 'badge-emerald'}" id="badge-${item.sku}">${item.status}</span></td>
        <td>
          <button class="btn-gradient" style="padding:0.3rem 0.65rem; font-size:0.75rem;" onclick="App.triggerSell('${item.sku}')">Sell 1 Item</button>
        </td>
      </tr>
    `).join('');
  },

  renderVendorsView: function() {
    const catSel = document.getElementById('vendor-cat-filter');
    const category = catSel ? catSel.value : 'all';

    const matches = VyapaarEngine.matchVendors(category);
    const tbody = document.getElementById('vendors-tbody');
    if (!tbody) return;

    tbody.innerHTML = matches.map(v => `
      <tr>
        <td style="font-weight:700; color:var(--accent-indigo);">${v.id}</td>
        <td style="font-weight:600;">${v.name}</td>
        <td><span class="badge badge-cyan">${v.category}</span></td>
        <td>${v.city}</td>
        <td>⭐ ${v.rating}</td>
        <td style="font-weight:700; color:var(--accent-emerald);">${v.sla}%</td>
        <td><span class="badge badge-emerald" style="font-size:0.8rem; font-weight:700;">Score: ${v.match_score}</span></td>
        <td>
          <button class="btn-secondary" style="padding:0.35rem 0.65rem; font-size:0.75rem;" onclick="App.dispatchVendorPo('${v.name}', ${v.rating}, ${v.sla})">Dispatch PO</button>
        </td>
      </tr>
    `).join('');
  },

  dispatchVendorPo: function(name, rating, sla) {
    const consequence = VyapaarEngine.getBusinessConsequence('po_dispatched', { name: name, rating: rating, sla: sla });
    const banner = document.getElementById('consequence-banner');
    if (banner) {
      banner.innerHTML = `
        <div class="consequence-icon">🤝</div>
        <div>
          <div class="consequence-title">${consequence.title}</div>
          <div class="consequence-body">${consequence.body}</div>
        </div>
      `;
      banner.style.display = 'flex';
    }
    this.showToast(`PO Dispatched to ${name} with ${sla}% SLA guarantee`);
  },

  renderStoreHealthView: function() {
    const storeSel = document.getElementById('health-store-select');
    const storeId = storeSel ? storeSel.value : 'STR-2001';

    const health = VyapaarEngine.evaluateStoreHealth(storeId);

    const scoreElem = document.getElementById('health-score-val');
    if (scoreElem) scoreElem.innerText = health.health_score;

    const ratingElem = document.getElementById('health-rating-val');
    if (ratingElem) ratingElem.innerText = health.solvency_rating;

    const valElem = document.getElementById('health-valuation-val');
    if (valElem) valElem.innerText = '₹ ' + health.estimated_valuation.toLocaleString();

    const multElem = document.getElementById('health-multiple-val');
    if (multElem) multElem.innerText = health.arr_multiple_x + 'x ARR Multiple';
  },

  renderEscrowView: function() {
    const tbody = document.getElementById('escrow-tbody');
    if (!tbody) return;

    tbody.innerHTML = VyapaarData.escrow_transactions.map(t => `
      <tr>
        <td style="font-weight:700; color:var(--accent-indigo);">${t.tx_id}</td>
        <td>${t.order_id}</td>
        <td>${t.buyer}</td>
        <td>${t.supplier}</td>
        <td style="font-weight:700;">₹ ${t.amount.toLocaleString()}</td>
        <td><span class="badge ${t.vault_status.includes('Released') ? 'badge-emerald' : 'badge-amber'}">${t.vault_status}</span></td>
        <td>
          <button class="btn-secondary" style="padding:0.25rem 0.5rem; font-size:0.72rem;" onclick="App.releaseEscrow('${t.tx_id}')">Release Payout</button>
        </td>
      </tr>
    `).join('');
  },

  releaseEscrow: function(txId) {
    VyapaarEngine.updateEscrowState(txId, 'Released to Vendor');
    const consequence = VyapaarEngine.getBusinessConsequence('escrow_released', { tx_id: txId });
    const banner = document.getElementById('consequence-banner');
    if (banner) {
      banner.innerHTML = `
        <div class="consequence-icon">🔒</div>
        <div>
          <div class="consequence-title">${consequence.title}</div>
          <div class="consequence-body">${consequence.body}</div>
        </div>
      `;
      banner.style.display = 'flex';
    }
    this.showToast(`💸 Escrow Vault Payout Released for ${txId}`);
    this.renderEscrowView();
    this.renderDashboardView();
  },

  renderGrowthView: function() {
    const container = document.getElementById('rfm-cards-container');
    if (!container) return;

    container.innerHTML = VyapaarData.customer_rfm_segments.map(s => `
      <div class="card card-accent-indigo">
        <div class="card-title">${s.segment} <span class="badge badge-emerald">${s.retention_pct}% Retention</span></div>
        <div class="card-val">${s.count} Stores</div>
        <div class="card-sub text-indigo">Avg GMV: ₹ ${s.avg_gmv_inr.toLocaleString()}</div>
        <p style="font-size:0.78rem; color:var(--text-muted); margin-top:0.75rem;"><strong>AI Action:</strong> ${s.recommended_campaign}</p>
        <button class="btn-gradient" style="margin-top:1rem; width:100%; font-size:0.78rem;" onclick="App.showToast('WhatsApp Campaign Launched for ${s.segment}')">Launch Campaign</button>
      </div>
    `).join('');
  },

  runGuidedTour: function(scenario) {
    if (scenario === 'automation') {
      this.switchView('automation', document.getElementById('nav-automation'));
      setTimeout(() => this.triggerOrderSimulation(), 400);
    }
    if (scenario === 'stock') {
      this.switchView('inventory', document.getElementById('nav-inventory'));
      setTimeout(() => this.triggerSell('SKU-ELE-002'), 400);
    }
    if (scenario === 'ai') {
      this.switchView('ai-advisor', document.getElementById('nav-ai-advisor'));
    }
    if (scenario === 'health') {
      this.switchView('store-health', document.getElementById('nav-store-health'));
    }
  },

  showToast: function(msg, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span>${type === 'warning' ? '⚠️' : '⚡'}</span> <div>${msg}</div>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }
};

document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
