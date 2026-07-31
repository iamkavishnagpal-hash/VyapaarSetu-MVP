# VyapaarSetu User Journey Maps

This document outlines the step-by-step user interaction journeys across all 4 modes.

---

## 1. Journey 1: "Start a Business from Zero"

```mermaid
sequenceDiagram
    autonumber
    actor Founder as Ananya (Founder)
    participant UX as VyapaarSetu Web UI
    participant AI as AI Advisor Engine
    participant Escrow as Escrow Wallet
    participant Vendor as Vendor Directory

    Founder->>UX: Select "Start a Business" Mode
    UX->>AI: Trigger Niche & Capital Diagnostic Questionnaires
    AI-->>UX: Recommend Category: "Handblock Apparel" & Capital Split (40% Inv, 25% Web)
    Founder->>UX: Accept Category & Search Suppliers
    UX->>Vendor: Query Verified Suppliers (Filter: MOQ <= 50, Rating >= 4.5)
    Vendor-->>UX: Match Found: "Jaipur BlockPrints & Co"
    Founder->>UX: Place Initial Batch Order (₹45,000)
    UX->>Escrow: Lock ₹45,000 in Multi-Sig Escrow Wallet
    Escrow-->>Vendor: Notify Order Placed & Escrow Secured
    Vendor->>Founder: Ship Sample Goods via Delhivery
    Founder->>UX: Inspect Batch & Approve QA Check
    UX->>Escrow: Auto-Release ₹45,000 to Vendor Account
```

---

## 2. Journey 2: "Sell a Working Store"

```mermaid
sequenceDiagram
    autonumber
    actor Seller as Store Owner (Seller)
    participant Platform as VyapaarSetu Store Exchange
    participant Audit as P&L Verification Engine
    actor Buyer as Buyer / Investor

    Seller->>Platform: Initiate "List My Store for Sale"
    Platform->>Audit: Connect Bank Feed & Shopify / POS Gateway
    Audit-->>Platform: Verify Monthly Revenue (₹1.85M) & Net Margin (23%)
    Platform->>Platform: Calculate Fair Valuation (₹12.0M @ 2.35x P/E)
    Buyer->>Platform: Browse Marketplace & Select Store Listing
    Buyer->>Platform: Deposit ₹12.0M into Master Acquisition Escrow
    Platform->>Seller: Trigger Asset & Inventory Audit Transfer Window
    Buyer->>Platform: Confirm Ownership & Inventory Rec Complete
    Platform->>Seller: Release Escrow Balance ₹12.0M to Seller
```
