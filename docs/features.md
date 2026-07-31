# VyapaarSetu Technical & Commercial Features Matrix

This document provides a deep technical breakdown of the platform's core functional modules.

---

## 1. Core Feature Modules

### Module 1: AI Strategic Advisor (Decision Support Engine)
- **Capability**: Provides strategic business advice across all 4 modes (Start, Run, Sell, Grow).
- **Underlying Logic**: Rule-based heuristic matrix combined with LLM prompt templates tailored for MSME commerce.
- **Key Inputs**: Capital budget, category, monthly orders, shrinkage rate, asking price.
- **Output**: Actionable JSON/Markdown playbooks detailing exact capital splits, recommended vendors, and SKU liquidation steps.

### Module 2: Multi-Sig Escrow Trust Wallet
- **Capability**: Locks buyer or merchant funds in compliance-grade multi-sig escrow until defined operational milestones are satisfied.
- **Milestone Triggers**:
  - *Vendor Orders*: 100% payout released upon courier delivery confirmation + QA inspection approval.
  - *POS Sales*: Instant real-time settlement to merchant bank account.
  - *Store Acquisition*: Funds released after 7-day physical audit window.

### Module 3: Multi-Channel Inventory Reconciliation Engine
- **Capability**: Syncs inventory across physical store counters (POS) and online platforms (Shopify, Amazon, Flipkart).
- **Discrepancy Detection**: Calculates inventory shrinkage rates (`(Book Stock - Physical Stock) / Book Stock`).
- **Automated Reordering**: Triggers automated supplier purchase orders when combined stock falls below predefined threshold levels.

### Module 4: Smart Logistics & Carrier Router
- **Capability**: Dynamically routes outbound shipments to courier partners (Delhivery, BlueDart, Shadowfax, XpressBees).
- **Optimization Parameters**: Pin-code SLA reliability rate (50%), shipping cost (30%), transit speed (20%).

### Module 5: Turnkey Store Marketplace & Audit Engine
- **Capability**: Allows store owners to list businesses for sale with tamper-proof, bank-verified revenue and net margin credentials.
- **Valuation Engine**: Calculates fair asking price based on annual P/E multiples (standard range 2.0x - 3.5x).
