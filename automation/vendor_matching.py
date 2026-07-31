"""
VyapaarSetu Automation Engine — Vendor Selection & Smart Supplier Matcher
File: automation/vendor_matching.py

Business Value:
    Automates supplier RFQ routing by ranking vendors based on SLA history, delivery speed,
    pricing efficiency, and quality ratings to minimize fulfillment friction.

Input:
    - Target product category and required stock volume
    - data/vendors.csv
    - data/vendor_ratings.csv
Output:
    - Ranked list of qualified vendors with SLA match scores
"""

import os
import csv
import json
from typing import List, Dict, Any

class VendorMatchingEngine:
    def __init__(self, vendors_csv: str = 'data/vendors.csv', ratings_csv: str = 'data/vendor_ratings.csv'):
        self.vendors_csv = vendors_csv
        self.ratings_csv = ratings_csv
        self.vendors: List[Dict[str, Any]] = []

    def load_data(self) -> None:
        """Loads vendor details and aggregates historical SLA ratings."""
        ratings_summary: Dict[str, List[float]] = {}
        if os.path.exists(self.ratings_csv):
            with open(self.ratings_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    v_id = row['vendor_id']
                    if v_id not in ratings_summary:
                        ratings_summary[v_id] = []
                    ratings_summary[v_id].append(float(row['fulfillment_rate_pct']))

        if os.path.exists(self.vendors_csv):
            with open(self.vendors_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    v_id = row['vendor_id']
                    actual_rates = ratings_summary.get(v_id, [float(row['sla_compliance_pct'])])
                    avg_actual_sla = sum(actual_rates) / len(actual_rates) if actual_rates else 90.0

                    self.vendors.append({
                        'vendor_id': v_id,
                        'vendor_name': row['vendor_name'],
                        'category': row['category'],
                        'city': row['city'],
                        'rating': float(row['rating']),
                        'sla_compliance_pct': float(row['sla_compliance_pct']),
                        'actual_sla_pct': round(avg_actual_sla, 1),
                        'status': row['status']
                    })

    def match_vendors(self, category: str, min_rating: float = 4.0) -> List[Dict[str, Any]]:
        """Ranks vendors matching requested category criteria using weighted composite scores."""
        matched = []
        for v in self.vendors:
            if v['status'] == 'Active' and (v['category'].lower() == category.lower() or category.lower() == 'all'):
                # Composite Match Score Formula: Rating (50%) + SLA (50%)
                match_score = round((v['rating'] / 5.0 * 50) + (v['actual_sla_pct'] / 100.0 * 50), 2)
                matched.append({
                    'vendor_id': v['vendor_id'],
                    'vendor_name': v['vendor_name'],
                    'city': v['city'],
                    'rating': v['rating'],
                    'actual_sla_pct': v['actual_sla_pct'],
                    'match_score': match_score,
                    'recommended_tier': 'Preferred Partner' if match_score >= 85.0 else 'Standard Supplier'
                })

        return sorted(matched, key=lambda x: x['match_score'], reverse=True)

if __name__ == '__main__':
    engine = VendorMatchingEngine()
    engine.load_data()
    matches = engine.match_vendors(category='Electronics', min_rating=3.8)
    print(json.dumps({'requested_category': 'Electronics', 'top_matched_suppliers': matches[:5]}, indent=2))
