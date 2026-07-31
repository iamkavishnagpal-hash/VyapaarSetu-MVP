#!/usr/bin/env python3
"""
VyapaarSetu Enterprise Synthetic Data Generator
Generates realistic, relational CSV datasets for MSME commerce operations, analytics, and growth intelligence.
Schema Coverage:
- 250 Vendors across 40 Indian commerce cities
- 18 Product Categories
- 2,500 Active Product SKUs
- 4 Primary Warehouses
- 10,000+ Multi-channel Orders (POS, Shopify, Amazon, Flipkart, Instagram)
- Inventory Logs & Shrinkage Audits
- Logistics & Carrier Shipment Logs
- Multi-Sig Escrow Transaction Logs
- Channel Marketing Spend Data
- Customer Product Reviews & Return Logs
"""

import os
import csv
import random
from datetime import datetime, timedelta

# Set seed for reproducible synthetic data generation
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")
os.makedirs(DATASET_DIR, exist_ok=True)

CITIES = [
    "Jaipur RJ", "Surat GJ", "Tirupur TN", "Moradabad UP", "Kochi KL", "Kanpur UP",
    "Bengaluru KA", "Bhiwandi MH", "Mumbai MH", "Delhi NCR", "Ludhiana PB", "Agra UP",
    "Ahmedabad GJ", "Hyderabad TS", "Chennai TN", "Kolkata WB", "Indore MP", "Coimbatore TN",
    "Panipat HR", "Varanasi UP", "Dehradun UK", "Nagpur MH", "Pune MH", "Rajkot GJ",
    "Jodhpur RJ", "Salem TN", "Bareilly UP", "Meerut UP", "Nashik MH", "Guwahati AS",
    "Patna BR", "Bhubaneswar OD", "Chandigarh UT", "Jalandhar PB", "Amritsar PB", "Gwalior MP",
    "Mysuru KA", "Madurai TN", "Vijayawada AP", "Udaipur RJ"
]

CATEGORIES = [
    "Textiles & Handblock Prints", "Pure Silk & Traditional Sarees", "Knitwear & Everyday Apparel",
    "Brass & Artisan Metalcraft", "Ayurvedic Beauty & Wellness", "Leather Footwear & Travel Goods",
    "Eco-Friendly Packaging", "Consumer Electronics Accessories", "Organic Home & Kitchenware",
    "Handloom Bed Linen & Curtains", "Spices & Gourmet Food Crafts", "Jewelry & Fashion Accessories",
    "Footwear & Athletic Shoes", "Stationery & Corporate Gifting", "Pet Care & Organic Treats",
    "Kids Wear & Wooden Toys", "Fitness Gear & Yoga Accessories", "Automotive Accessories"
]

WAREHOUSES = [
    {"wh_id": "WH-101", "name": "Jaipur North Hub", "city": "Jaipur RJ", "capacity_units": 150000},
    {"wh_id": "WH-102", "name": "Surat Central Textile WH", "city": "Surat GJ", "capacity_units": 250000},
    {"wh_id": "WH-103", "name": "Bhiwandi Mega Fulfillment Center", "city": "Bhiwandi MH", "capacity_units": 500000},
    {"wh_id": "WH-104", "name": "Bengaluru South Logistics Hub", "city": "Bengaluru KA", "capacity_units": 300000}
]

CARRIERS = ["Delhivery Direct", "BlueDart Express", "Shadowfax Surface", "Ecom Express", "XpressBees Surface"]
CHANNELS = ["Shopify Storefront", "POS Counter", "Amazon IN", "Flipkart", "Myntra", "Instagram DM"]

def generate_categories():
    filepath = os.path.join(DATASET_DIR, "categories.csv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["category_id", "category_name", "avg_gross_margin_pct", "return_benchmark_pct"])
        for i, cat in enumerate(CATEGORIES, 1):
            writer.writerow([
                f"CAT-{100+i}",
                cat,
                round(random.uniform(25.0, 65.0), 2),
                round(random.uniform(1.5, 12.0), 2)
            ])
    print(f"[OK] Generated Categories: {len(CATEGORIES)}")

def generate_vendors():
    filepath = os.path.join(DATASET_DIR, "vendors.csv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "vendor_id", "name", "category", "location", "rating",
            "lead_time_days", "on_time_rate_pct", "defect_rate_pct",
            "min_order_qty", "escrow_verified", "contact_email"
        ])
        for i in range(1, 251):
            cat = random.choice(CATEGORIES)
            city = random.choice(CITIES)
            on_time = round(random.uniform(75.0, 99.5), 1)
            defect = round(random.uniform(0.2, 5.0), 1)
            rating = round(random.uniform(3.5, 5.0), 1)
            escrow = random.choice([True, True, True, False])  # 75% escrow adoption
            writer.writerow([
                f"VND-{1000+i}",
                f"{city.split()[0]} {cat.split()[0]} Enterprise {i}",
                cat,
                city,
                rating,
                random.randint(3, 15),
                on_time,
                defect,
                random.choice([25, 50, 100, 200, 500]),
                "TRUE" if escrow else "FALSE",
                f"b2b_sales_{i}@{city.split()[0].lower()}enterprise.in"
            ])
    print("[OK] Generated 250 Vendors across 40 Cities")

def generate_warehouses():
    filepath = os.path.join(DATASET_DIR, "warehouses.csv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["warehouse_id", "name", "city", "capacity_units", "active_status"])
        for wh in WAREHOUSES:
            writer.writerow([wh["wh_id"], wh["name"], wh["city"], wh["capacity_units"], "ACTIVE"])
    print("[OK] Generated Warehouses")
    
def generate_products():
    filepath = os.path.join(DATASET_DIR, "products.csv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "product_id", "sku", "name", "category", "cost_price_inr",
            "selling_price_inr", "reorder_level", "vendor_id", "is_active", "primary_channel"
        ])
        for i in range(1, 2501):
            cat = CATEGORIES[(i - 1) % len(CATEGORIES)]
            vendor_id = f"VND-{1000 + random.randint(1, 250)}"
            cost = random.randint(150, 2500)
            markup = random.uniform(1.8, 3.5)
            selling = int(cost * markup)
            writer.writerow([
                f"PRD-{5000+i}",
                f"SKU-{cat[:3].upper()}-{i:04d}",
                f"{cat.split()[0]} Premium Craft SKU #{i}",
                cat,
                cost,
                selling,
                random.randint(20, 100),
                vendor_id,
                "TRUE" if random.random() > 0.05 else "FALSE",
                random.choice(CHANNELS)
            ])
    print("[OK] Generated 2,500 Product SKUs")

def generate_orders_and_logs():
    orders_file = os.path.join(DATASET_DIR, "orders.csv")
    inv_file = os.path.join(DATASET_DIR, "inventory_logs.csv")
    ship_file = os.path.join(DATASET_DIR, "shipment_logs.csv")
    escrow_file = os.path.join(DATASET_DIR, "escrow_logs.csv")

    start_date = datetime(2025, 1, 1)

    with open(orders_file, "w", newline="", encoding="utf-8") as f_ord, \
         open(inv_file, "w", newline="", encoding="utf-8") as f_inv, \
         open(ship_file, "w", newline="", encoding="utf-8") as f_shp, \
         open(escrow_file, "w", newline="", encoding="utf-8") as f_esc:

        w_ord = csv.writer(f_ord)
        w_inv = csv.writer(f_inv)
        w_shp = csv.writer(f_shp)
        w_esc = csv.writer(f_esc)

        w_ord.writerow([
            "order_id", "store_id", "order_date", "channel", "product_id",
            "quantity", "unit_price_inr", "total_amount_inr", "shipping_cost_inr",
            "payment_method", "order_status", "escrow_txn_id"
        ])
        w_inv.writerow([
            "inventory_log_id", "store_id", "product_id", "warehouse_id",
            "offline_stock_qty", "online_stock_qty", "reserved_qty",
            "shrinkage_rate_pct", "last_sync_timestamp", "sync_status"
        ])
        w_shp.writerow([
            "shipment_id", "order_id", "carrier_name", "tracking_number",
            "promised_days", "actual_days", "shipping_cost_inr", "sla_status"
        ])
        w_esc.writerow([
            "escrow_txn_id", "reference_type", "reference_id", "buyer_id",
            "seller_or_vendor_id", "amount_inr", "hold_date", "release_date",
            "status", "milestone_trigger"
        ])

        # Generate 12,000 orders
        for i in range(1, 12001):
            order_id = f"ORD-{10000+i}"
            store_id = f"STR-{501 + (i % 5)}"
            days_offset = random.randint(0, 540)
            order_date = (start_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
            channel = random.choice(CHANNELS)
            product_id = f"PRD-{5000 + random.randint(1, 2500)}"
            qty = random.randint(1, 4)
            unit_price = random.choice([499, 699, 999, 1499, 2499, 3499])
            total_amt = qty * unit_price
            ship_cost = 0 if channel == "POS Counter" else random.choice([60, 90, 120, 150, 180])
            pay_method = "Cash" if channel == "POS Counter" else random.choice(["UPI", "Credit Card", "Net Banking", "COD"])
            
            # Status distribution
            rand_val = random.random()
            if rand_val < 0.82:
                status = "Delivered"
            elif rand_val < 0.90:
                status = "In-Transit"
            elif rand_val < 0.96:
                status = "Returned"
            else:
                status = "Cancelled"

            escrow_txn_id = f"ESC-{30000+i}"

            w_ord.writerow([
                order_id, store_id, order_date, channel, product_id,
                qty, unit_price, total_amt, ship_cost, pay_method, status, escrow_txn_id
            ])

            # Generate Logistics Log
            if channel != "POS Counter":
                promised = random.choice([2, 3, 4, 5])
                actual = promised if status == "Delivered" else promised + random.randint(1, 4)
                sla_status = "SLA Met" if actual <= promised else "SLA Breached"
                carrier = random.choice(CARRIERS)
                w_shp.writerow([
                    f"SHP-{40000+i}", order_id, carrier, f"TRK{900000+i}",
                    promised, actual, ship_cost, sla_status
                ])

            # Generate Escrow Log
            escrow_status = "Released" if status == "Delivered" else ("Held" if status == "In-Transit" else "Refunded")
            rel_date = order_date if escrow_status == "Released" else "PENDING"
            w_esc.writerow([
                escrow_txn_id, "Order Purchase", order_id, f"CUST-{1000+ (i%1000)}",
                store_id, total_amt, order_date, rel_date, escrow_status, "Delivery Audit Confirmed"
            ])

        # Generate Inventory Logs for 2,500 products
        for i in range(1, 2501):
            prd_id = f"PRD-{5000+i}"
            store_id = f"STR-{501 + (i % 5)}"
            wh_id = random.choice(WAREHOUSES)["wh_id"]
            off_qty = random.randint(5, 150)
            on_qty = random.randint(10, 400)
            res_qty = random.randint(0, 20)
            shrinkage = round(random.uniform(0.2, 4.5), 2)
            sync_status = "Synced" if shrinkage < 2.0 else "Discrepancy Warning"
            
            w_inv.writerow([
                f"INV-{80000+i}", store_id, prd_id, wh_id,
                off_qty, on_qty, res_qty, shrinkage,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), sync_status
            ])

    print("[OK] Generated 12,000 Orders, Logistics Logs, Escrow Ledger & Inventory Logs")

def generate_marketing_and_reviews():
    mkt_file = os.path.join(DATASET_DIR, "marketing_spend.csv")
    rev_file = os.path.join(DATASET_DIR, "customer_reviews.csv")

    with open(mkt_file, "w", newline="", encoding="utf-8") as f_mkt, \
         open(rev_file, "w", newline="", encoding="utf-8") as f_rev:
        
        w_mkt = csv.writer(f_mkt)
        w_rev = csv.writer(f_rev)

        w_mkt.writerow(["log_id", "month", "channel", "ad_spend_inr", "conversions", "cac_inr", "roas"])
        w_rev.writerow(["review_id", "product_id", "rating", "review_text", "sentiment", "return_reason"])

        # Marketing spend logs
        months = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
                  "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12"]
        channels = ["Meta Ads (FB/IG)", "Google Search", "Amazon Sponsored Ads", "Influencer Collaborations"]
        
        idx = 1
        for m in months:
            for ch in channels:
                spend = random.randint(45000, 250000)
                convs = random.randint(150, 1200)
                cac = round(spend / convs, 2)
                roas = round(random.uniform(2.1, 5.8), 2)
                w_mkt.writerow([f"MKT-{100+idx}", m, ch, spend, convs, cac, roas])
                idx += 1

        # Customer reviews
        reasons = ["Fit Size Issue", "Fabric Defect", "Color Mismatch", "Delayed Delivery", "Damaged Packaging", "None"]
        for r in range(1, 3001):
            prd_id = f"PRD-{5000 + random.randint(1, 2500)}"
            rating = random.choices([5, 4, 3, 2, 1], weights=[50, 25, 12, 8, 5])[0]
            sentiment = "Positive" if rating >= 4 else ("Neutral" if rating == 3 else "Negative")
            reason = random.choice(reasons) if rating <= 3 else "None"
            w_rev.writerow([
                f"REV-{7000+r}", prd_id, rating,
                f"Review content for product {prd_id}. Overall rating {rating}/5.",
                sentiment, reason
            ])

    print("[OK] Generated Marketing Spend Logs & Customer Reviews")

if __name__ == "__main__":
    print("==================================================================")
    print("VYAPAARSETU ENTERPRISE SYNTHETIC DATA GENERATOR — INITIALIZING")
    print("==================================================================")
    generate_categories()
    generate_vendors()
    generate_warehouses()
    generate_products()
    generate_orders_and_logs()
    generate_marketing_and_reviews()
    print("==================================================================")
    print("ENTERPRISE SYNTHETIC DATASET GENERATION COMPLETE!")
    print(f"Files written to: {DATASET_DIR}")
    print("==================================================================")
