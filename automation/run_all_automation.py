"""
VyapaarSetu Automation Master Test Suite & Production Pipeline Runner
File: automation/run_all_automation.py

Executes and verifies all 12 modular Python automation engines:
 1. AI Merchant Growth Advisor
 2. Store Health & Solvency Valuation Engine
 3. Business Alerting Engine
 4. Escrow Release Workflow Engine
 5. Inventory Demand Forecasting Engine
 6. Merchant Growth Alerting Engine
 7. Inventory Auto-Reorder Sync Engine
 8. Smart Logistics Carrier Router
 9. Order Routing Engine
10. Dynamic Pricing Optimizer
11. Product Cross-Sell Recommendation Engine
12. Supplier Matching Engine
"""

import json
import os
import sys

# Reconfigure stdout for utf-8 safety on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Import all automation engines
from automation.ai_advisor_flow import AIAdvisorFlowEngine
from automation.business_health_engine import BusinessHealthEngine
from automation.business_alerting import BusinessAlertingMonitor
from automation.escrow_workflow import EscrowWorkflowEngine
from automation.forecast_engine import DemandForecastEngine
from automation.growth_alerts import GrowthAlertEngine
from automation.inventory_sync import InventorySyncEngine
from automation.logistics_assignment import LogisticsAssignmentEngine
from automation.order_routing import OrderRoutingEngine
from automation.pricing_optimizer import PricingOptimizerEngine
from automation.recommendation_engine import RecommendationEngine
from automation.vendor_matching import VendorMatchingEngine

def run_suite():
    print("==================================================================")
    print("VYAPAARSETU AUTOMATION SUITE -- PRODUCTION SIMULATION RUNNER")
    print("==================================================================")
    
    passed = 0
    total = 12
    results = {}

    # 1. AI Advisor Engine
    try:
        engine = AIAdvisorFlowEngine()
        res = engine.generate_merchant_advice()
        assert res.get('status') == 'SUCCESS'
        print(" [PASS] 1. AI Merchant Growth Advisor Engine")
        results['ai_advisor'] = res
        passed += 1
    except Exception as e:
        print(f" [FAIL] 1. AI Merchant Growth Advisor Engine: {e}")

    # 2. Store Health & Solvency Valuation Engine
    try:
        engine = BusinessHealthEngine()
        res = engine.evaluate_store_health()
        assert res.get('status') == 'SUCCESS'
        print(" [PASS] 2. Store Health & Solvency Valuation Engine")
        results['business_health'] = res
        passed += 1
    except Exception as e:
        print(f" [FAIL] 2. Store Health & Solvency Valuation Engine: {e}")

    # 3. Business Alerting Engine
    try:
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        engine = BusinessAlertingMonitor(data_dir)
        alerts = engine.scan_for_critical_alerts()
        assert isinstance(alerts, list)
        print(" [PASS] 3. Business Alerting & Risk Engine")
        results['business_alerts'] = alerts
        passed += 1
    except Exception as e:
        print(f" [FAIL] 3. Business Alerting Engine: {e}")

    # 4. Escrow Trade Release Engine
    try:
        engine = EscrowWorkflowEngine()
        engine.load_data()
        funded_id = next((e['escrow_id'] for e in engine.escrow_records if e['status'] == 'Funded'), 'ESC-6003')
        res = engine.process_state_transition(funded_id, 'MARK_DELIVERED')
        assert res.get('status') == 'SUCCESS'
        print(" [PASS] 4. Escrow Trade Vault Release Engine")
        results['escrow_workflow'] = res
        passed += 1
    except Exception as e:
        print(f" [FAIL] 4. Escrow Workflow Engine: {e}")

    # 5. Inventory Demand Forecasting Engine
    try:
        engine = DemandForecastEngine()
        res = engine.generate_30day_forecast(alpha=0.3)
        assert res.get('status') == 'SUCCESS'
        print(" [PASS] 5. Inventory Demand Forecasting Engine")
        results['demand_forecast'] = res
        passed += 1
    except Exception as e:
        print(f" [FAIL] 5. Demand Forecasting Engine: {e}")

    # 6. Merchant Growth Alerting Engine
    try:
        engine = GrowthAlertEngine()
        res = engine.evaluate_growth_anomalies()
        assert res.get('status') == 'SUCCESS'
        print(" [PASS] 6. Merchant Growth Alerting Engine")
        results['growth_alerts'] = res
        passed += 1
    except Exception as e:
        print(f" [FAIL] 6. Growth Alerting Engine: {e}")

    # 7. Inventory Auto-Reorder Sync Engine
    try:
        engine = InventorySyncEngine()
        res = engine.reconcile_and_alert()
        assert res.get('status') == 'SUCCESS'
        print(" [PASS] 7. Inventory Auto-Reorder Sync Engine")
        results['inventory_sync'] = res
        passed += 1
    except Exception as e:
        print(f" [FAIL] 7. Inventory Sync Engine: {e}")

    # 8. Smart Logistics Assignment Engine
    try:
        engine = LogisticsAssignmentEngine()
        engine.load_data()
        res = engine.assign_best_carrier(destination_city='Mumbai', parcel_weight_kg=2.5)
        assert res.get('status') == 'SUCCESS'
        print(" [PASS] 8. Smart Logistics & Carrier Assignment Engine")
        results['logistics'] = res
        passed += 1
    except Exception as e:
        print(f" [FAIL] 8. Smart Logistics Engine: {e}")

    # 9. Order Routing Engine
    try:
        engine = OrderRoutingEngine()
        engine.load_data()
        res = engine.route_order(order_id='ORD-9999', product_id='PRD-3005', quantity=10, destination_city='Mumbai')
        assert res.get('status') == 'ROUTED'
        print(" [PASS] 9. Intelligent Order Warehouse Router Engine")
        results['order_routing'] = res
        passed += 1
    except Exception as e:
        print(f" [FAIL] 9. Order Routing Engine: {e}")

    # 10. Dynamic Pricing Optimizer Engine
    try:
        engine = PricingOptimizerEngine()
        engine.load_data()
        res = engine.optimize_prices()
        assert res.get('status') == 'SUCCESS'
        print(" [PASS] 10. Dynamic Pricing & Inventory Markdown Optimizer")
        results['pricing_optimizer'] = res
        passed += 1
    except Exception as e:
        print(f" [FAIL] 10. Dynamic Pricing Optimizer: {e}")

    # 11. Product Cross-Sell Recommendation Engine
    try:
        engine = RecommendationEngine()
        engine.load_and_train()
        res = engine.recommend(product_id='PRD-3001')
        assert 'recommendations' in res
        print(" [PASS] 11. Product Cross-Sell & Basket Recommendation Matrix Engine")
        results['recommendation'] = res
        passed += 1
    except Exception as e:
        print(f" [FAIL] 11. Recommendation Engine: {e}")

    # 12. Supplier Matching Engine
    try:
        engine = VendorMatchingEngine()
        engine.load_data()
        vendors = engine.match_vendors(category='Electronics', min_rating=4.0)
        assert isinstance(vendors, list) and len(vendors) > 0
        print(" [PASS] 12. Supplier Matching & SLA Leaderboard Engine")
        results['vendor_matching'] = vendors
        passed += 1
    except Exception as e:
        print(f" [FAIL] 12. Supplier Matching Engine: {e}")

    print("==================================================================")
    print(f"RESULT: {passed}/{total} Automation Engines Passed Verification")
    print("==================================================================")

    if passed == total:
        print("SUCCESS: ALL AUTOMATION ENGINES FUNCTIONING WITH 100% PASS RATE")
        sys.exit(0)
    else:
        print("FAILURE: AUTOMATION SUITE FAILURE DETECTED")
        sys.exit(1)

if __name__ == '__main__':
    run_suite()
