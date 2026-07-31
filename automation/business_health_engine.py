"""
VyapaarSetu Automation Engine — Store Health Score & Solvency Index Calculator
File: automation/business_health_engine.py

Business Value:
    Computes a composite 0-100 store health score and valuation estimate for merchant storefronts,
    powering platform credit underwriting and M&A store acquisition listings.

Input:
    - data/stores.csv
    - data/business_health.csv
Output:
    - Ranked merchant store health report and risk classification
"""

import os
import csv
import json
from typing import Dict, Any, List

class BusinessHealthEngine:
    def __init__(self, stores_csv: str = 'data/stores.csv', health_csv: str = 'data/business_health.csv'):
        self.stores_csv = stores_csv
        self.health_csv = health_csv
        self.stores: List[Dict[str, Any]] = []

    def load_data(self) -> None:
        """Loads merchant store metadata and financial metrics."""
        if os.path.exists(self.stores_csv):
            with open(self.stores_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    monthly_rev = float(row['monthly_revenue_inr'])
                    health = int(row['health_score'])
                    valuation = float(row['estimated_valuation_inr'])

                    self.stores.append({
                        'store_id': row['store_id'],
                        'store_name': row['store_name'],
                        'city': row['city'],
                        'tier': row['tier'],
                        'monthly_revenue_inr': monthly_rev,
                        'health_score': health,
                        'estimated_valuation_inr': valuation,
                        'annual_arr_inr': monthly_rev * 12.0
                    })

    def evaluate_store_health(self) -> Dict[str, Any]:
        """Calculates store health distributions, solvency ratings, and platform M&A inventory."""
        evaluated = []
        total_platform_valuation = 0.0

        for store in self.stores:
            score = store['health_score']
            rev = store['monthly_revenue_inr']
            val = store['estimated_valuation_inr']
            total_platform_valuation += val

            # Classification rules
            if score >= 85:
                rating = 'AAA - Prime Merchant'
                risk_tier = 'Low'
            elif score >= 70:
                rating = 'AA - Stable Storefront'
                risk_tier = 'Moderate'
            else:
                rating = 'BB - Restructuring Required'
                risk_tier = 'High'

            evaluated.append({
                'store_id': store['store_id'],
                'store_name': store['store_name'],
                'tier': store['tier'],
                'monthly_revenue_inr': rev,
                'health_score': score,
                'solvency_rating': rating,
                'risk_tier': risk_tier,
                'estimated_valuation_inr': val,
                'arr_multiple_x': round(val / (rev * 12.0), 2) if rev > 0 else 0.0
            })

        evaluated = sorted(evaluated, key=lambda x: x['health_score'], reverse=True)
        return {
            'status': 'SUCCESS',
            'total_stores_evaluated': len(evaluated),
            'total_platform_store_valuation_inr': round(total_platform_valuation, 2),
            'top_healthy_stores': evaluated[:5],
            'distressed_stores_alert': [s for s in evaluated if s['risk_tier'] == 'High'][:5]
        }

if __name__ == '__main__':
    engine = BusinessHealthEngine()
    engine.load_data()
    print(json.dumps(engine.evaluate_store_health(), indent=2))
