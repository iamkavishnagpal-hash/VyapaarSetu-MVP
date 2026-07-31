# VyapaarSetu User Roles & Access Control Specs

This document defines the user personas, permission matrices, and operational privileges within the VyapaarSetu platform.

---

## 1. Role Matrix & Privileges

| User Role | Primary Objectives | Core System Capabilities | Security & Access Tier |
|---|---|---|---|
| **Merchant / Store Owner** | Start, run, grow, or sell a retail/D2C business. | Full dashboard access, POS inventory sync, AI Advisor query, Store marketplace listing. | Owner Tier (Multi-Factor Auth + KYC Verified) |
| **B2B Supplier / Vendor** | Supply raw materials, finished products, or packaging. | Receive escrow PO orders, update batch fulfillment status, view supplier health ratings. | Supplier Tier (GSTIN / PAN Verified) |
| **Store Buyer / Investor** | Discover and acquire turnkey profitable stores. | Browse verified P&L store listings, place escrow acquisition deposits, access audit logs. | Buyer Tier (KYC + Bank Balance Verified) |
| **Logistics Carrier Partner** | Execute order pickup, transit, and delivery. | Receive automated delivery dispatch API webhooks, update SLA tracking events. | Integration Partner Tier (API Key / Webhook Signed) |
| **Platform Administrator** | System health, escrow dispute resolution, compliance audit. | Resolve escrow hold disputes, audit vendor defect rates, monitor platform performance. | Admin Superuser Tier |
