# VyapaarSetu — Comprehensive Platform Data Dictionary

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Storage Format:** Relational CSV Datasets (`data/`) / PostgreSQL 14 Database Schema  
**Total Entities:** 17 Interconnected Business Tables

---

## 1. Relational Entity Summary & Record Counts

| Entity Name | CSV Path | Primary Key | Key Foreign Keys | Row Count | Business Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **vendors** | `data/vendors.csv` | `vendor_id` | - | 100 | B2B supplier master profiles and SLA ratings |
| **stores** | `data/stores.csv` | `store_id` | - | 100 | Merchant retail storefront profiles and valuation |
| **products** | `data/products.csv` | `product_id` | `vendor_id` | 500 | Catalog items, COGS, MSRP, reorder thresholds |
| **customers** | `data/customers.csv` | `customer_id` | - | 1,000 | Retail & wholesale buyer profiles and RFM segments |
| **orders** | `data/orders.csv` | `order_id` | `store_id`, `customer_id`, `product_id` | 2,500 | Transactional order line items and payments |
| **inventory** | `data/inventory.csv` | `inventory_id` | `product_id` | 1,500 | Stock levels, holding age, warehouse locations |
| **sales_channels** | `data/sales_channels.csv` | `channel_id` | `store_id` | 100 | Channel revenue shares and conversion rates |
| **customer_segments**| `data/customer_segments.csv`| `segment_id` | - | 100 | RFM cohort rules and monetary thresholds |
| **vendor_ratings** | `data/vendor_ratings.csv` | `rating_id` | `vendor_id`, `store_id` | 500 | Historical supplier quality & delivery evaluations |
| **logistics** | `data/logistics.csv` | `logistics_id` | `order_id` | 1,200 | Courier shipping logs, transit days, SLA status |
| **escrow_transactions**| `data/escrow_transactions.csv`| `escrow_id` | `order_id` | 800 | Trade vault deposit, inspection, and release logs |
| **returns** | `data/returns.csv` | `return_id` | `order_id`, `product_id` | 400 | Return requests, defect reason codes, refunds |
| **marketing_campaigns**| `data/marketing_campaigns.csv`| `campaign_id`| - | 100 | Campaign spend, impressions, conversions, ROAS |
| **pricing_history** | `data/pricing_history.csv` | `pricing_id` | `product_id` | 500 | Historical price adjustments & elasticity logs |
| **inventory_movements**| `data/inventory_movements.csv`| `movement_id`| `product_id` | 1,500 | Stock transfers, shrinkage, inbound PO logs |
| **product_reviews** | `data/product_reviews.csv` | `review_id` | `product_id`, `customer_id` | 1,000 | Verified customer star ratings and review dates |
| **business_health** | `data/business_health.csv` | `health_record_id`| `store_id` | 200 | Monthly store solvency, risk, and growth index |

---

## 2. Table-by-Table Schema Definitions

### 1. `vendors`
- `vendor_id` (VARCHAR(16), PK, NOT NULL) — Unique vendor identifier (e.g. `VND-1001`).
- `vendor_name` (VARCHAR(128), NOT NULL) — Legal business name of the supplier.
- `category` (VARCHAR(64), NOT NULL) — Primary supply category (e.g., `Electronics`, `Apparel`).
- `city` (VARCHAR(64), NOT NULL) — Primary dispatch hub city (e.g., `Surat`, `Mumbai`).
- `rating` (DECIMAL(3,2), NOT NULL) — Average quality rating (1.00 to 5.00).
- `sla_compliance_pct` (DECIMAL(5,2), NOT NULL) — SLA compliance percentage (85.0 to 99.9).
- `status` (VARCHAR(32), NOT NULL) — Operational status (`Active`, `Under Review`).

---

### 2. `products`
- `product_id` (VARCHAR(16), PK, NOT NULL) — Unique SKU identifier (e.g. `PRD-3001`).
- `product_name` (VARCHAR(128), NOT NULL) — Catalog product title.
- `vendor_id` (VARCHAR(16), FK -> `vendors.vendor_id`, NOT NULL) — Primary supplier ID.
- `category` (VARCHAR(64), NOT NULL) — Product merchandising category.
- `cogs_inr` (DECIMAL(10,2), NOT NULL) — Unit Cost of Goods Sold in INR.
- `msrp_inr` (DECIMAL(10,2), NOT NULL) — Manufacturer Suggested Retail Price in INR.
- `reorder_level` (INT, NOT NULL) — Reorder threshold quantity triggering automated PO.
- `safety_stock` (INT, NOT NULL) — Buffer stock level maintained for demand spikes.

---

### 3. `orders`
- `order_id` (VARCHAR(16), PK, NOT NULL) — Unique transaction identifier (e.g. `ORD-5001`).
- `store_id` (VARCHAR(16), FK -> `stores.store_id`, NOT NULL) — Merchant storefront ID.
- `customer_id` (VARCHAR(16), FK -> `customers.customer_id`, NOT NULL) — Buyer customer ID.
- `product_id` (VARCHAR(16), FK -> `products.product_id`, NOT NULL) — Purchased SKU ID.
- `quantity` (INT, NOT NULL) — Purchased unit quantity.
- `unit_price_inr` (DECIMAL(10,2), NOT NULL) — Unit selling price in INR.
- `total_amount_inr` (DECIMAL(12,2), NOT NULL) — Gross order total (`quantity * unit_price_inr`).
- `order_date` (DATE, NOT NULL) — Order placement timestamp.
- `status` (VARCHAR(32), NOT NULL) — Order status (`Delivered`, `Shipped`, `Processing`, `Cancelled`, `Returned`).
- `payment_mode` (VARCHAR(32), NOT NULL) — Payment method (`UPI`, `Escrow`, `Credit Card`, `Net Banking`, `COD`).

---

### 4. `inventory`
- `inventory_id` (VARCHAR(16), PK, NOT NULL) — Unique inventory record ID (e.g. `INV-6001`).
- `product_id` (VARCHAR(16), FK -> `products.product_id`, NOT NULL) — SKU identifier.
- `warehouse_location` (VARCHAR(64), NOT NULL) — Fulfillment center location (e.g. `WH-West-Mumbai`).
- `quantity_on_hand` (INT, NOT NULL) — Total physical units in warehouse.
- `quantity_reserved` (INT, NOT NULL) — Units allocated to pending processing orders.
- `stock_age_days` (INT, NOT NULL) — Number of days stock has remained in warehouse.
- `last_restock_date` (DATE, NOT NULL) — Date of last inbound shipment.

---

### 5. `escrow_transactions`
- `escrow_id` (VARCHAR(16), PK, NOT NULL) — Unique escrow vault record ID (e.g. `ESC-6001`).
- `order_id` (VARCHAR(16), FK -> `orders.order_id`, NOT NULL) — Target transaction order ID.
- `escrow_amount_inr` (DECIMAL(12,2), NOT NULL) — Total funds locked in vault.
- `status` (VARCHAR(32), NOT NULL) — Vault status (`Funded`, `In Inspection`, `Disputed`, `Released`, `Refunded`).
- `funded_date` (DATE, NOT NULL) — Date buyer deposited funds into trade vault.
- `released_date` (DATE, NULLABLE) — Date funds were released to vendor bank account.

---

### 6. `logistics`
- `logistics_id` (VARCHAR(16), PK, NOT NULL) — Unique logistics record ID (e.g. `LOG-7001`).
- `order_id` (VARCHAR(16), FK -> `orders.order_id`, NOT NULL) — Associated order ID.
- `carrier_name` (VARCHAR(64), NOT NULL) — Logistics partner (`BlueDart Express`, `Delhivery Surface`, `Ecom Express`).
- `dispatch_date` (DATE, NOT NULL) — Dispatch timestamp.
- `estimated_days` (INT, NOT NULL) — SLA target transit days.
- `actual_days` (INT, NOT NULL) — Actual transit days taken.
- `shipping_cost_inr` (DECIMAL(8,2), NOT NULL) — Shipping cost in INR.
- `delivery_status` (VARCHAR(32), NOT NULL) — Delivery SLA status (`Yes`, `Delayed`).
