"""
VyapaarSetu Automation Engine — Revenue & Operational Business Alerts Dispatcher
File: automation/business_alerts.py

Business Value:
    Monitors daily transaction metrics to detect anomalous drops in revenue,
    spikes in return defect rates, or merchant churn risks.

Input:
    - data/orders.csv
    - data/returns.csv
Output:
    - Alert JSON payload with severity classification
"""

import json
from automation.growth_alerts import GrowthAlertEngine

if __name__ == '__main__':
    engine = GrowthAlertEngine()
    print(json.dumps(engine.evaluate_growth_anomalies(), indent=2))
