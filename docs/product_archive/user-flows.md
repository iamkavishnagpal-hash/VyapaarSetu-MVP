# VyapaarSetu User Flows

This document details the step-by-step user interaction flows across all 4 modes.

---

## 1. Flow A: 0-to-1 Store Launch (Start Mode)

```
[User Registration & KYC]
           │
           ▼
[AI Advisor Niche Diagnostic Input] ──► (Budget, Location, Preferred Category)
           │
           ▼
[Capital Allocation Playbook Generation] ──► (40% Inv, 25% Web, 25% Marketing, 10% Reserve)
           │
           ▼
[Verified Supplier Discovery Engine] ──► (Filter: Escrow Verified, Rating >= 4.5)
           │
           ▼
[Lock Initial Batch Payment in Escrow]
           │
           ▼
[Quality Inspection & Escrow Payout Release] ──► [Store Front Live & Omnichannel Ready]
```

---

## 2. Flow B: Multi-Channel POS & Inventory Sync (Run Mode)

```
[Offline POS Cash Sale Recorded]
           │
           ▼
[VyapaarSetu Inventory Engine Intercepts Local POS Webhook]
           │
           ▼
[Deduct Offline Counter Stock (-1 Unit)]
           │
           ▼
[Real-Time API Sync Push to Shopify, Amazon & Flipkart Storefronts]
           │
           ▼
[Check Reorder Threshold] ──► (If Stock <= Threshold, Trigger Vendor Reorder Alert)
```

---

## 3. Flow C: Turnkey Store Acquisition Exchange (Sell Mode)

```
[Store Owner Requests Listing]
           │
           ▼
[Automated P&L Audit Integration] ──► (Fetches Bank Statements & Payment Gateway Data)
           │
           ▼
[Fair Market Valuation Matrix Generated]
           │
           ▼
[Listing Published on VyapaarSetu Marketplace]
           │
           ▼
[Buyer Deposits Funds in Master Acquisition Escrow]
           │
           ▼
[7-Day Physical & Inventory Audit Window] ──► [Escrow Funds Released to Seller]
```
