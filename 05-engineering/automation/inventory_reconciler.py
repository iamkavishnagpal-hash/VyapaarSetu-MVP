#!/usr/bin/env python3
"""
VyapaarSetu Engine — Real-Time Inventory Reconciliation & Leakage Detector
Reconciles physical counter POS sales with online storefronts and detects stock shrinkage.
Reads directly from 02-data/datasets/inventory_logs.csv and products.csv.
"""

import os
import csv
import json
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class InventoryItem:
    inventory_log_id: str
    store_id: str
    product_id: str
    warehouse_id: str
    offline_stock_qty: int
    online_stock_qty: int
    reserved_qty: int
    shrinkage_rate_pct: float
    sync_status: str

    @property
    def total_available_stock(self) -> int:
        return self.offline_stock_qty + self.online_stock_qty - self.reserved_qty


class InventoryReconciler:
    def __init__(self, inv_csv: str, prd_csv: str):
        self.inv_csv = inv_csv
        self.prd_csv = prd_csv
        self.reorder_levels: Dict[str, int] = {}
        self.product_names: Dict[str, str] = {}
        self._load_products()

    def _load_products(self):
        if os.path.exists(self.prd_csv):
            with open(self.prd_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.reorder_levels[row['product_id']] = int(row['reorder_level'])
                    self.product_names[row['product_id']] = row['name']

    def run_reconciliation(self) -> Dict[str, Any]:
        alerts = []
        synced_count = 0

        if not os.path.exists(self.inv_csv):
            raise FileNotFoundError(f"Inventory CSV missing at {self.inv_csv}")

        with open(self.inv_csv, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = InventoryItem(
                    inventory_log_id=row['inventory_log_id'],
                    store_id=row['store_id'],
                    product_id=row['product_id'],
                    warehouse_id=row['warehouse_id'],
                    offline_stock_qty=int(row['offline_stock_qty']),
                    online_stock_qty=int(row['online_stock_qty']),
                    reserved_qty=int(row['reserved_qty']),
                    shrinkage_rate_pct=float(row['shrinkage_rate_pct']),
                    sync_status=row['sync_status']
                )

                reorder_threshold = self.reorder_levels.get(item.product_id, 30)
                product_name = self.product_names.get(item.product_id, item.product_id)

                if item.total_available_stock <= reorder_threshold:
                    alerts.append({
                        "inventory_log_id": item.inventory_log_id,
                        "product": product_name,
                        "warehouse": item.warehouse_id,
                        "available_stock": item.total_available_stock,
                        "reorder_threshold": reorder_threshold,
                        "alert_type": "REORDER_TRIGGER",
                        "severity": "HIGH"
                    })

                if item.shrinkage_rate_pct >= 3.0:
                    alerts.append({
                        "inventory_log_id": item.inventory_log_id,
                        "product": product_name,
                        "warehouse": item.warehouse_id,
                        "shrinkage_rate": f"{item.shrinkage_rate_pct}%",
                        "alert_type": "HIGH_SHRINKAGE_LEAKAGE",
                        "severity": "CRITICAL"
                    })

                if item.sync_status == "Synced":
                    synced_count += 1

        return {
            "total_items_audited": synced_count + len(alerts),
            "healthy_items_count": synced_count,
            "alerts_generated_count": len(alerts),
            "sample_alerts": alerts[:5]
        }


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    inv_path = os.path.join(base_dir, "02-data", "datasets", "inventory_logs.csv")
    prd_path = os.path.join(base_dir, "02-data", "datasets", "products.csv")
    
    reconciler = InventoryReconciler(inv_path, prd_path)
    report = reconciler.run_reconciliation()
    
    print("==================================================================")
    print("VYAPAARSETU INVENTORY RECONCILER -- RECONCILIATION REPORT")
    print("==================================================================")
    print(json.dumps(report, indent=2))
