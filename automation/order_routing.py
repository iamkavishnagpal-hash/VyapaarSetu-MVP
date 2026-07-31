"""
VyapaarSetu Automation Engine — Smart Order Routing & Fulfillment Logistics Engine
File: automation/order_routing.py

Business Value:
    Dynamically routes customer orders to the nearest warehouse or vendor stock point 
    to optimize shipping costs, reduce delivery SLA latency, and balance warehouse load.

Input:
    - Order detail with shipping destination city and product SKU
    - data/inventory.csv
    - data/logistics.csv
Output:
    - Optimal fulfillment warehouse assignment and estimated transit time
"""

import os
import csv
import json
from typing import Dict, Any, List

class OrderRoutingEngine:
    def __init__(self, inventory_csv: str = 'data/inventory.csv', logistics_csv: str = 'data/logistics.csv'):
        self.inventory_csv = inventory_csv
        self.logistics_csv = logistics_csv
        self.warehouse_stocks: Dict[str, Dict[str, int]] = {}

    def load_data(self) -> None:
        """Loads available warehouse stock by SKU."""
        if os.path.exists(self.inventory_csv):
            with open(self.inventory_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    p_id = row['product_id']
                    wh = row['warehouse_location']
                    avail = int(row['quantity_on_hand']) - int(row['quantity_reserved'])
                    if p_id not in self.warehouse_stocks:
                        self.warehouse_stocks[p_id] = {}
                    self.warehouse_stocks[p_id][wh] = avail

    def route_order(self, order_id: str, product_id: str, quantity: int, destination_city: str) -> Dict[str, Any]:
        """Assigns the best warehouse based on stock availability and regional proximity."""
        if product_id not in self.warehouse_stocks:
            return {'status': 'FAILED', 'reason': f'Product {product_id} not found in inventory catalog.'}

        available_whs = self.warehouse_stocks[product_id]
        eligible = {wh: qty for wh, qty in available_whs.items() if qty >= quantity}

        if not eligible:
            return {'status': 'BACKORDER_REQUIRED', 'reason': f'Insufficient stock across all warehouses for SKU {product_id}.'}

        # Proximity heuristic lookup
        city_wh_map = {
            'mumbai': 'WH-West-Mumbai',
            'pune': 'WH-West-Mumbai',
            'delhi': 'WH-North-Delhi',
            'jaipur': 'WH-North-Delhi',
            'bengaluru': 'WH-South-Bengaluru',
            'chennai': 'WH-South-Bengaluru',
            'kolkata': 'WH-East-Kolkata'
        }

        preferred_wh = city_wh_map.get(destination_city.lower(), 'WH-Central-Nagpur')
        selected_wh = preferred_wh if preferred_wh in eligible else list(eligible.keys())[0]

        carrier_assignment = 'BlueDart Express' if 'Mumbai' in selected_wh or 'Delhi' in selected_wh else 'Delhivery Surface'

        return {
            'status': 'ROUTED',
            'order_id': order_id,
            'product_id': product_id,
            'quantity': quantity,
            'destination_city': destination_city,
            'assigned_warehouse': selected_wh,
            'recommended_carrier': carrier_assignment,
            'estimated_transit_days': 2 if selected_wh == preferred_wh else 4,
            'estimated_shipping_cost_inr': 120.0 if selected_wh == preferred_wh else 250.0
        }

if __name__ == '__main__':
    engine = OrderRoutingEngine()
    engine.load_data()
    routing_result = engine.route_order(order_id='ORD-9999', product_id='PRD-3005', quantity=10, destination_city='Mumbai')
    print(json.dumps(routing_result, indent=2))
