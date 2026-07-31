#!/usr/bin/env python3
"""
VyapaarSetu EDA Engine — Revenue & Channel Net Margin Analysis
Analyzes gross revenue, shipping overhead, COGS, and net contribution margins across sales channels.
"""

import os
import csv
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

def analyze_revenue_and_margins():
    orders_file = os.path.join(DATASET_DIR, "orders.csv")
    products_file = os.path.join(DATASET_DIR, "products.csv")

    if not os.path.exists(orders_file) or not os.path.exists(products_file):
        print("[ERROR] Datasets missing for EDA execution!")
        return

    product_cogs = {}
    with open(products_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            product_cogs[r['product_id']] = float(r['cost_price_inr'])

    channel_stats = defaultdict(lambda: {"orders": 0, "revenue": 0.0, "cogs": 0.0, "shipping": 0.0})

    with open(orders_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r['order_status'] == 'Delivered':
                ch = r['channel']
                total_amt = float(r['total_amount_inr'])
                ship_cost = float(r['shipping_cost_inr'])
                qty = int(r['quantity'])
                cogs = product_cogs.get(r['product_id'], 0.0) * qty

                channel_stats[ch]["orders"] += 1
                channel_stats[ch]["revenue"] += total_amt
                channel_stats[ch]["cogs"] += cogs
                channel_stats[ch]["shipping"] += ship_cost

    print("==================================================================")
    print("VYAPAARSETU EDA -- CHANNEL NET CONTRIBUTION MARGIN SUMMARY")
    print("==================================================================")
    print(f"{'CHANNEL':<25} | {'ORDERS':<8} | {'REVENUE (INR)':<15} | {'NET PROFIT':<12} | {'MARGIN %':<8}")
    print("-" * 75)

    total_rev_all = sum(s["revenue"] for s in channel_stats.values())

    for ch, stats in sorted(channel_stats.items(), key=lambda x: x[1]["revenue"], reverse=True):
        net_profit = stats["revenue"] - stats["cogs"] - stats["shipping"]
        margin_pct = (net_profit / stats["revenue"] * 100.0) if stats["revenue"] > 0 else 0.0
        print(f"{ch:<25} | {stats['orders']:<8} | Rs.{stats['revenue']:<14,.0f} | Rs.{net_profit:<11,.0f} | {margin_pct:<7.2f}%")

    print("==================================================================")
    print(f"Total Platform Delivered Revenue: Rs.{total_rev_all:,.2f}")
    print("==================================================================")

if __name__ == "__main__":
    analyze_revenue_and_margins()
