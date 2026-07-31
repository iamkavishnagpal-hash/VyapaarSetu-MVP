# VyapaarSetu — Prototype Walkthrough & State Transition Notes

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Purpose:** Outlines screen transitions, feedback state specifications, modal behaviors, and user test paths across the platform.

---

## 1. Primary User Journey State Machine

```
[Store Onboarding] ──(KYC Passed)──► [Inventory Import] ──(Reconciled)──► [Live Storefront]
                                                                                │
                                                                       (Order Placed)
                                                                                │
                                                                                ▼
[Escrow Released] ◄──(Buyer Inspected)── [Dispatched / Routed] ◄── [Funded Escrow Vault]
```

---

## 2. Interactive Prototype Screen Paths

### Flow A: Merchant Onboarding & Escrow Vault Setup
1. User lands on `/start-business`.
2. Clicks `Begin Onboarding Wizard` ➔ Modal step 1 opens.
3. Enters GSTIN `27AAACV1234F1Z9` ➔ Synthetic validation returns green checkmark `GSTIN Verified (Vyapaar Retail Ltd)`.
4. Moves to Step 4 (`Setup Escrow Vault`) ➔ Clicks `Authorize ICICI Trade Vault` ➔ Redirects back with `Escrow Status: Active`.

### Flow B: Low-Stock Automated Reorder
1. User navigates to `/run-business` (Inventory Command).
2. Observes SKU `PRD-3005` highlighted in red (`Stock Level: 4 units < Reorder Level: 20`).
3. Clicks `Reconcile & Dispatch PO` button.
4. Drawer slides in showing `Vendor Matching Engine Output`: Top matched supplier `Vendor 12 Wholesale Ltd (SLA: 98.4%)`.
5. Clicks `Confirm Purchase Order` ➔ Toast notification `PO #PO-9081 sent via WhatsApp API to Vendor 12`.

### Flow C: M&A Store Acquisition via Escrow
1. User navigates to `/sell-store`.
2. Selects `Vyapaar Store 14` (Monthly ARR: ₹1.2M, Health Score: 94).
3. Clicks `Submit Buy Offer (Escrow)`.
4. Escrow drawer pops up displaying transaction breakdown (Purchase Price: ₹2,800,000, Platform Fee: ₹56,000, 10% Deposit: ₹280,000).
5. Clicks `Fund Escrow Deposit` ➔ Status updates to `Escrow Funded - 14-Day Due Diligence Window Active`.

---

## 3. UI State Guidelines & Feedback Micro-Interactions

- **Loading States:** Skeleton shimmer loaders on data tables during fetch operations.
- **Empty States:** Clear CTA illustrations for empty categories or zero search results (`No active disputes found`).
- **Success Feedback:** Floating dark glass toast alerts in bottom-right corner with 3-second auto-dismiss.
- **Error Handling:** Inline red border highlights with explicit field correction instructions.
