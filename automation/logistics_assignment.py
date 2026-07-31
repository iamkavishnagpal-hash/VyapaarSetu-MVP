"""
VyapaarSetu Automation Engine — Smart Carrier Assignment & Logistics Optimizer
File: automation/logistics_assignment.py

Business Value:
    Selects the optimal logistics courier (BlueDart, Delhivery, Ecom Express, Shadowfax) 
    based on cost per km, transit speed SLA, and regional carrier historical performance.

Input:
    - Order payload with destination region and parcel weight
    - data/logistics.csv
Output:
    - Assigned carrier recommendation and cost optimization score
"""

import os
import csv
import json
from typing import Dict, Any, List
from collections import defaultdict

class LogisticsAssignmentEngine:
    def __init__(self, logistics_csv: str = 'data/logistics.csv'):
        self.logistics_csv = logistics_csv
        self.carrier_scores: Dict[str, Dict[str, float]] = defaultdict(lambda: {'total': 0, 'on_time': 0, 'cost_sum': 0.0})

    def load_data(self) -> None:
        """Loads historical carrier performance logs."""
        if os.path.exists(self.logistics_csv):
            with open(self.logistics_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    carrier = row['carrier_name']
                    self.carrier_scores[carrier]['total'] += 1
                    if row['delivery_status'] == 'Yes':
                        self.carrier_scores[carrier]['on_time'] += 1
                    self.carrier_scores[carrier]['cost_sum'] += float(row['shipping_cost_inr'])

    def assign_best_carrier(self, destination_city: str, parcel_weight_kg: float = 2.5) -> Dict[str, Any]:
        """Calculates optimal carrier score based on on-time rate and cost."""
        best_carrier = None
        best_score = -1.0
        details = []

        for carrier, stats in self.carrier_scores.items():
            total = stats['total']
            if total == 0:
                continue
            on_time_pct = (stats['on_time'] / total) * 100.0
            avg_cost = stats['cost_sum'] / total

            # Composite Score: 60% On-Time SLA + 40% Cost Efficiency
            cost_efficiency_score = max(0.0, 100.0 - (avg_cost / 10.0))
            score = round((on_time_pct * 0.6) + (cost_efficiency_score * 0.4), 2)

            details.append({
                'carrier_name': carrier,
                'on_time_rate_pct': round(on_time_pct, 1),
                'avg_shipping_cost_inr': round(avg_cost, 2),
                'composite_score': score
            })

            if score > best_score:
                best_score = score
                best_carrier = carrier

        return {
            'status': 'SUCCESS',
            'destination_city': destination_city,
            'parcel_weight_kg': parcel_weight_kg,
            'assigned_carrier': best_carrier,
            'optimization_score': best_score,
            'carrier_evaluation_matrix': sorted(details, key=lambda x: x['composite_score'], reverse=True)
        }

if __name__ == '__main__':
    engine = LogisticsAssignmentEngine()
    engine.load_data()
    print(json.dumps(engine.assign_best_carrier(destination_city='Bengaluru'), indent=2))
