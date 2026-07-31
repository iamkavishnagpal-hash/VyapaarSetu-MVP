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
        
        # 1. Scan Inventory for Leakage
        inv_file = os.path.join(self.data_dir, "inventory.csv")
        if os.path.exists(inv_file):
            with open(inv_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    shrinkage = float(row['shrinkage_rate_pct'])
                    if shrinkage > 2.0:
                        alerts.append({
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "severity": "HIGH",
                            "category": "INVENTORY_LEAKAGE",
                            "title": f"Excessive Shrinkage in Store {row['store_id']}",
                            "details": f"Product {row['product_id']} at {row['warehouse_location']} recorded shrinkage of {shrinkage}%.",
                            "action_required": "Conduct immediate physical audit of POS logs vs shelf inventory."
                        })

        # 2. Scan Logistics for SLA Breaches
        log_file = os.path.join(self.data_dir, "logistics.csv")
        if os.path.exists(log_file):
            with open(log_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['sla_status'] == 'SLA Breached':
                        alerts.append({
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "severity": "MEDIUM",
                            "category": "LOGISTICS_BREACH",
                            "title": f"Carrier SLA Failure: {row['carrier_name']}",
                            "details": f"Order {row['order_id']} delayed by {int(row['actual_days']) - int(row['promised_days'])} days.",
                            "action_required": "Re-route subsequent shipments to alternative carrier."
                        })

        # 3. Scan Escrow for Pending High-Value Audits
        escrow_file = os.path.join(self.data_dir, "escrow_transactions.csv")
        if os.path.exists(escrow_file):
            with open(escrow_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['status'] == 'Held' and float(row['amount_inr']) >= 1000000:
                        alerts.append({
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "severity": "CRITICAL",
                            "category": "ESCROW_HIGH_VALUE",
                            "title": f"High Value Acquisition Escrow Hold",
                            "details": f"Escrow ID {row['escrow_txn_id']} holding ₹{float(row['amount_inr']):,.0f} pending P&L verification.",
                            "action_required": "Assign Senior Auditor to verify bank statement feed."
                        })

        return alerts


if __name__ == "__main__":
    base_data = os.path.join(os.path.dirname(__file__), "..", "data")
    monitor = BusinessAlertingMonitor(base_data)
    active_alerts = monitor.scan_for_critical_alerts()

    print("==================================================================")
    print("VYAPAARSETU BUSINESS ALERTING MONITOR — LIVE SYSTEM SCAN")
    print("==================================================================")
    print(f"Total Active Alerts Found: {len(active_alerts)}\n")
    print(json.dumps(active_alerts, indent=2))
