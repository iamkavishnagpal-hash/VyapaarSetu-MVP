#!/usr/bin/env python3
"""
VyapaarSetu Engine — Live Operational Risk & Leakage Alert Monitor
Scans inventory, logistics, and escrow datasets for operational anomalies.
Reads directly from 02-data/datasets/.
"""

import os
import csv
import json
from datetime import datetime
from typing import List, Dict, Any

class RiskAlertingMonitor:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def scan_for_alerts(self) -> List[Dict[str, Any]]:
        alerts = []
        
        # 1. Scan Inventory Logs for Shrinkage
        inv_file = os.path.join(self.data_dir, "inventory_logs.csv")
        if os.path.exists(inv_file):
            with open(inv_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    shrinkage = float(row['shrinkage_rate_pct'])
                    if shrinkage >= 4.0 and count < 3:
                        alerts.append({
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "severity": "CRITICAL",
                            "category": "INVENTORY_LEAKAGE",
                            "title": f"Excessive Shrinkage in Store {row['store_id']}",
                            "details": f"Product {row['product_id']} at {row['warehouse_id']} recorded shrinkage of {shrinkage}%.",
                            "action_required": "Conduct immediate physical audit of POS billing counter vs shelf stock."
                        })
                        count += 1

        # 2. Scan Shipment Logs for Carrier SLA Breaches
        shp_file = os.path.join(self.data_dir, "shipment_logs.csv")
        if os.path.exists(shp_file):
            with open(shp_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    if row['sla_status'] == 'SLA Breached' and count < 2:
                        alerts.append({
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "severity": "MEDIUM",
                            "category": "LOGISTICS_BREACH",
                            "title": f"Carrier SLA Failure: {row['carrier_name']}",
                            "details": f"Order {row['order_id']} delayed by {int(row['actual_days']) - int(row['promised_days'])} days.",
                            "action_required": "Re-route subsequent shipments to primary carrier."
                        })
                        count += 1

        return alerts


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(base_dir, "02-data", "datasets")
    monitor = RiskAlertingMonitor(data_dir)
    active_alerts = monitor.scan_for_alerts()

    print("==================================================================")
    print("VYAPAARSETU RISK ALERTING MONITOR -- LIVE SYSTEM SCAN")
    print("==================================================================")
    print(f"Total Active Alerts Generated: {len(active_alerts)}\n")
    print(json.dumps(active_alerts, indent=2))
