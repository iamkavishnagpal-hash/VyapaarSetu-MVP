"""
VyapaarSetu Automation Engine — Demand Velocity & Inventory Forecasting Model
File: automation/forecasting.py

Business Value:
    Executes exponential smoothing on historical sales to forecast 30-day SKU demand,
    preventing stockouts of high-margin goods.

Input:
    - data/orders.csv
Output:
    - 30-day demand forecast per SKU
"""

import json
from automation.forecast_engine import DemandForecastEngine

if __name__ == '__main__':
    engine = DemandForecastEngine()
    print(json.dumps(engine.generate_30day_forecast(), indent=2))
