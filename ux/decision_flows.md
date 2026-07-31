# VyapaarSetu — Decision Flows & System Logic Trees

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Purpose:** Illustrates logical decision trees governing merchant onboarding, vendor match selection, and escrow dispute resolution.

---

## 1. Decision Flow 1: Automated Inventory Reorder Logic

```
Is Available Stock <= Reorder Threshold?
       ├── NO  ➔ Maintain Monitoring Status
       └── YES ➔ Query Demand Forecast Model (forecast_engine.py)
                     │
                     ▼
             Calculate PO Quantity: (Reorder Threshold * 2) - Available
                     │
                     ▼
             Match Preferred Vendor (vendor_matching.py)
                     │
                     ▼
             Dispatch PO payload via Notification Engine
```

---

## 2. Decision Flow 2: Buyer-Seller Escrow Dispute Resolution

```
Order Dispatched & Delivered
            │
            ▼
Buyer Raises Defect Dispute within 72 Hours?
       ├── NO  ➔ Automatic Release of Funds to Vendor Vault
       └── YES ➔ Lock Vault Funds & Trigger Dispute Protocol
                     │
                     ▼
             Prompt Buyer to Upload Defect Photos / Proof
                     │
                     ▼
             Platform Admin Evaluates Return Criteria
                     ├── Valid Defect ➔ Issue Full Refund to Buyer
                     └── Invalid Claim ➔ Dismiss Dispute & Release Vault Funds
```
