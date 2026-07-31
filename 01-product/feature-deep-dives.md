# VyapaarSetu 5-Dimensional Feature Deep Dives

Every feature in VyapaarSetu is engineered through a 5-dimensional blueprint: **Problem ➔ Business Impact ➔ Data Needed ➔ UX Solution ➔ Automation**.

---

## 1. Feature 1: Omnichannel Inventory Sync Engine

### 1. Problem
Offline store counter (POS) sales and digital e-commerce storefronts (Shopify, Amazon, Flipkart, Myntra, Instagram) operate in silos. Physical counter billing staff often forget to update digital inventories.

### 2. Business Impact
- **Overselling**: Customers order items online that are already sold out at the physical store counter.
- **Financial Damage**: Cancellation penalties on marketplaces (up to 5% of order value), lost customer lifetime value (LTV), and unrecorded physical counter shrinkage (avg 3.2% net loss).

### 3. Data Needed
- `orders.csv` (Real-time order channel feeds)
- `inventory_logs.csv` (Offline stock, online stock, reserved stock, shrinkage rates)
- `products.csv` (Reorder points, SKUs)
- `warehouses.csv` (Warehouse location IDs)

### 4. UX Solution
- **Inventory Status Pills**: Real-time status indicators (`Synced` = Emerald Green, `Discrepancy Warning` = Amber Pulse, `Critical Leakage` = Coral Red).
- **Stock Movement Timeline**: Interactive visual audit log showing every physical counter scan vs web checkout.

### 5. Automation & Technical Logic
- **Daemon**: `05-engineering/automation/inventory_reconciler.py`
- **Concurrency**: Redis Distributed Lock (Redlock) locks stock for 180s during active checkout to prevent race conditions.
- **Reorder Alert**: Automated PO generation when combined stock drops below product `reorder_level`.

---

## 2. Feature 2: B2B Supplier Escrow Wallet

### 1. Problem
First-time store founders face supplier fraud and upfront payment risks when ordering raw textiles or inventory from unverified B2B suppliers in distant industrial hubs (e.g. Surat, Jaipur, Tirupur).

### 2. Business Impact
- **Seed Capital Loss**: Loss of initial capital (₹50,000 - ₹2,000,000) due to fraudulent or sub-standard goods.
- **Marketplace Inertia**: Suppliers refuse credit terms to new D2C brands, stalling business creation.

### 3. Data Needed
- `vendors.csv` (Escrow verification status, defect rates, lead times)
- `escrow_logs.csv` (Transaction IDs, hold dates, release dates, milestone triggers)

### 4. UX Solution
- **Escrow Trust Badge**: Verified Supplier badge on vendor discovery cards.
- **Milestone Hold Card**: Visual wallet holding funds in trust with real-time status updates (`Funds Locked` ➔ `In-Transit Inspection` ➔ `QA Approved & Released`).

### 5. Automation & Technical Logic
- **Engine**: Automated release trigger upon carrier API delivery confirmation + 48-hour merchant QA sign-off.

---

## 3. Feature 3: Smart Courier Logistics Router

### 1. Problem
MSME merchants rely on static shipping contracts with single logistics carriers, leading to high shipping costs and unmonitored SLA delivery breaches.

### 2. Business Impact
- High Cash-on-Delivery (COD) Return-to-Origin (RTO) rates (up to 28%), eroding net contribution margin by 14%.

### 3. Data Needed
- `shipment_logs.csv` (Promised vs actual transit days, carrier SLA status, shipping costs)
- `orders.csv` (Destination pincode, parcel weight, order total)

### 4. UX Solution
- **Logistics Health Grid**: Carrier performance scorecard displaying real-time delivery success rates.

### 5. Automation & Technical Logic
- **Router**: `05-engineering/automation/logistics_router.py` dynamically ranks carriers (`SLA Rate * 0.50 + Cost * 0.30 + Speed * 0.20`).
