#!/usr/bin/env python3
"""
VyapaarSetu Engine — Dynamic Courier Logistics Router
Scores carrier SLA reliability, transit cost, and delivery performance from 02-data/datasets/shipment_logs.csv.
"""

import os
import csv
import json
from typing import Dict, Any, List

class LogisticsRouter:
    def __init__(self, logistics_csv: str):
        self.logistics_csv = logistics_csv
        self.carrier_stats: Dict[str, Dict[str, Any]] = {}
        self._analyze_carriers()

    def _analyze_carriers(self):
        if not os.path.exists(self.logistics_csv):
            raise FileNotFoundError(f"Shipment logs dataset missing at {self.logistics_csv}")

        with open(self.logistics_csv, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                carrier = row['carrier_name']
                if carrier not in self.carrier_stats:
                    self.carrier_stats[carrier] = {
                        "total_shipments": 0,
                        "sla_met_count": 0,
                        "total_cost": 0.0,
                        "total_days": 0
                    }
                
                stats = self.carrier_stats[carrier]
                stats['total_shipments'] += 1
                if row['sla_status'] == 'SLA Met':
                    stats['sla_met_count'] += 1
                stats['total_cost'] += float(row['shipping_cost_inr'])
                stats['total_days'] += int(row['actual_days'])

    def select_best_carrier(self) -> List[Dict[str, Any]]:
        rankings = []
        for carrier, stats in self.carrier_stats.items():
            total = stats['total_shipments']
            sla_rate = (stats['sla_met_count'] / total) * 100.0 if total > 0 else 0.0
            avg_cost = stats['total_cost'] / total if total > 0 else 0.0
            avg_days = stats['total_days'] / total if total > 0 else 0.0

            score = (sla_rate * 0.50) + (max(0, 300 - avg_cost) * 0.10) + (max(0, 10 - avg_days) * 2.0)

            rankings.append({
                "carrier_name": carrier,
                "routing_score": round(score, 2),
                "sla_compliance_rate": f"{round(sla_rate, 1)}%",
                "avg_transit_days": round(avg_days, 1),
                "avg_cost_inr": round(avg_cost, 2),
                "recommendation": "PRIMARY CARRIER" if score >= 65.0 else "SECONDARY CARRIER"
            })

        rankings.sort(key=lambda x: x['routing_score'], reverse=True)
        return rankings


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_path = os.path.join(base_dir, "02-data", "datasets", "shipment_logs.csv")
    router = LogisticsRouter(log_path)
    rankings = router.select_best_carrier()

    print("==================================================================")
    print("VYAPAARSETU SMART LOGISTICS ROUTER -- CARRIER SELECTION MATRIX")
    print("==================================================================")
    print(json.dumps(rankings, indent=2))
