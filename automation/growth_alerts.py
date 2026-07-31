"""
VyapaarSetu Automation Engine — Revenue Anomaly & Growth Alert Dispatcher
File: automation/growth_alerts.py

Business Value:
    Monitors daily/weekly transaction metrics to detect anomalous drops in revenue,
    sudden spikes in return rates, or unexpected merchant store churn risks.

Input:
    - data/orders.csv
    - data/returns.csv
Output:
    - Real-time alert feed with severity tags (CRITICAL, WARNING, INFO)
"""

import os
import csv
import json
from typing import List, Dict, Any
from collections import defaultdict

class GrowthAlertEngine:
    def __init__(self, orders_csv: str = 'data/orders.csv', returns_csv: str = 'data/returns.csv'):
        self.orders_csv = orders_csv
        self.returns_csv = returns_csv

    def evaluate_growth_anomalies(self) -> Dict[str, Any]:
        alerts = []
        store_sales = defaultdict(float)
        store_orders = defaultdict(int)
        product_returns = defaultdict(int)

        if os.path.exists(self.orders_csv):
            with open(self.orders_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['status'] == 'Delivered':
                        s_id = row['store_id']
                        store_sales[s_id] += float(row['total_amount_inr'])
                        store_orders[s_id] += 1

        if os.path.exists(self.returns_csv):
            with open(self.returns_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    product_returns[row['product_id']] += int(row['quantity'])

        # Analyze low sales stores (< ₹100,000)
        low_performing_stores = [s for s, val in store_sales.items() if val < 100000.0]
        if low_performing_stores:
            alerts.append({
                'alert_id': 'ALT-GROWTH-01',
                'severity': 'WARNING',
                'category': 'Merchant Retention Risk',
                'message': f'{len(low_performing_stores)} stores generated under ₹100,000 revenue.',
                'affected_entities': low_performing_stores[:5],
                'recommended_action': 'Trigger merchant onboarding support call.'
            })

        # Analyze high defect products
        high_return_skus = [p for p, count in product_returns.items() if count >= 5]
        if high_return_skus:
            alerts.append({
                'alert_id': 'ALT-QUALITY-02',
                'severity': 'CRITICAL',
                'category': 'Product Defect Spike',
                'message': f'{len(high_return_skus)} SKUs exceeded return threshold of 5 units.',
                'affected_entities': high_return_skus[:5],
                'recommended_action': 'Pause SKU listing and inspect vendor batch.'
            })

        return {
            'status': 'SUCCESS',
            'total_alerts_triggered': len(alerts),
            'alerts': alerts
        }

if __name__ == '__main__':
    engine = GrowthAlertEngine()
    print(json.dumps(engine.evaluate_growth_anomalies(), indent=2))
