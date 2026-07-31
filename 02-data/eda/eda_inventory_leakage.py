#!/usr/bin/env python3
"""
VyapaarSetu EDA Engine — Inventory Shrinkage & Leakage Diagnostic
Identifies high shrinkage risk SKUs and warehouse discrepancy hotspots.
"""

import os
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

def analyze_inventory_shrinkage():
    inv_file = os.path.join(DATASET_DIR, "inventory_logs.csv")
    products_file = os.path.join(DATASET_DIR, "products.csv")

    if not os.path.exists(inv_file) or not os.path.exists(products_file):
        print("[ERROR] Datasets missing for inventory EDA!")
        return

    prd_names = {}
    with open(products_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            prd_names[r['product_id']] = r['name']

    high_risk_items = []

    with open(inv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            shrinkage = float(r['shrinkage_rate_pct'])
            if shrinkage >= 3.0:
                high_risk_items.append({
                    "product_id": r['product_id'],
                    "product_name": prd_names.get(r['product_id'], "Unknown"),
                    "warehouse": r['warehouse_id'],
                    "shrinkage_pct": shrinkage,
                    "sync_status": r['sync_status']
                })

    print("==================================================================")
    print("VYAPAARSETU EDA -- HIGH INVENTORY SHRINKAGE DIAGNOSTIC (>= 3.0%)")
    print("==================================================================")
    print(f"Total High Shrinkage SKUs Flagged: {len(high_risk_items)}\n")

    for item in high_risk_items[:10]:
        print(f"* [{item['product_id']}] {item['product_name'][:30]:<30} | WH: {item['warehouse']} | Shrinkage: {item['shrinkage_pct']}% | {item['sync_status']}")

    print("==================================================================")

if __name__ == "__main__":
    analyze_inventory_shrinkage()
