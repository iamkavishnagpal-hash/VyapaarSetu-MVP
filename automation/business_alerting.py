#!/usr/bin/env python3
"""
VyapaarSetu Engine — Business Operational Alerting & Leakage Monitor
Generates real-time risk notifications for merchants and operations managers.
"""

import csv
import json
import os
from datetime import datetime
from typing import List, Dict, Any

class BusinessAlertingMonitor:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def scan_for_critical_alerts(self) -> List[Dict[str, Any]]:
        alerts = []
        
        # 1. Scan Inventory for Leakage & Ageing Stock Risk
        inv_file = os.path.join(self.data_dir, "inventory.csv")
        if os.path.exists(inv_file):
            with open(inv_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    stock_age = int(row.get('stock_age_days', 0))
                    if stock_age > 120:
                        alerts.append({
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "severity": "HIGH",
                            "category": "INVENTORY_LEAKAGE",
                            "title": f"Ageing Inventory Risk for Product {row.get('product_id')}",
                            "details": f"Product {row.get('product_id')} at {row.get('warehouse_location')} recorded stock age of {stock_age} days.",
                            "action_required": "Conduct immediate physical audit or apply markdown discount."
                        })

        # 2. Scan Logistics for SLA Breaches
        log_file = os.path.join(self.data_dir, "logistics.csv")
        if os.path.exists(log_file):
            with open(log_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('status') == 'Delayed' or row.get('carrier_status') == 'Delayed':
                        alerts.append({
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "severity": "MEDIUM",
                            "category": "LOGISTICS_BREACH",
                            "title": f"Carrier SLA Failure: {row.get('carrier_name')}",
                            "details": f"Order {row.get('order_id')} delayed.",
                            "action_required": "Re-route subsequent shipments to alternative carrier."
                        })

        # 3. Scan Escrow for Pending High-Value Audits
        escrow_file = os.path.join(self.data_dir, "escrow_transactions.csv")
        if os.path.exists(escrow_file):
            with open(escrow_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('escrow_status') == 'LOCKED' and float(row.get('escrow_amount_inr', 0)) >= 100000:
                        alerts.append({
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "severity": "CRITICAL",
                            "category": "ESCROW_HIGH_VALUE",
                            "title": "High Value Escrow Hold Alert",
                            "details": f"Escrow ID {row.get('escrow_id')} holding INR {float(row.get('escrow_amount_inr', 0)):,.0f}.",
                            "action_required": "Assign Senior Auditor to verify delivery status."
                        })

        return alerts


if __name__ == "__main__":
    base_data = os.path.join(os.path.dirname(__file__), "..", "data")
    monitor = BusinessAlertingMonitor(base_data)
    active_alerts = monitor.scan_for_critical_alerts()

    print("==================================================================")
    print("VYAPAARSETU BUSINESS ALERTING MONITOR -- LIVE SYSTEM SCAN")
    print("==================================================================")
    print(f"Total Active Alerts Found: {len(active_alerts)}\n")
    print(json.dumps(active_alerts[:5], indent=2))
