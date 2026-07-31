#!/usr/bin/env python3
"""
VyapaarSetu EDA Engine — Vendor SLA Reliability & Risk Scoring
Scores vendor health across on-time delivery, defect rate, rating, and escrow compliance.
"""

import os
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

def analyze_vendor_reliability():
    v_file = os.path.join(DATASET_DIR, "vendors.csv")

    if not os.path.exists(v_file):
        print("[ERROR] Vendors dataset missing!")
        return

    vendors = []
    with open(v_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            on_time = float(r['on_time_rate_pct'])
            defect = float(r['defect_rate_pct'])
            rating = float(r['rating'])
            escrow = r['escrow_verified'] == 'TRUE'
            
            score = (on_time * 0.40) + ((100.0 - defect) * 0.40) + (rating * 4.0)
            if escrow:
                score += 5.0

            vendors.append({
                "vendor_id": r['vendor_id'],
                "name": r['name'],
                "location": r['location'],
                "score": round(score, 2),
                "rating": rating,
                "on_time": on_time,
                "defect": defect,
                "escrow": escrow
            })

    vendors.sort(key=lambda x: x['score'], reverse=True)

    print("==================================================================")
    print("VYAPAARSETU EDA -- TOP 10 PREFERRED SUPPLIERS BY COMPOSITE SCORE")
    print("==================================================================")
    print(f"{'ID':<10} | {'NAME':<32} | {'SCORE':<8} | {'ON-TIME %':<10} | {'DEFECT %':<8} | {'ESCROW'}")
    print("-" * 80)

    for v in vendors[:10]:
        print(f"{v['vendor_id']:<10} | {v['name'][:32]:<32} | {v['score']:<8} | {v['on_time']:<10}% | {v['defect']:<8}% | {'YES' if v['escrow'] else 'NO'}")

    print("==================================================================")

if __name__ == "__main__":
    analyze_vendor_reliability()
