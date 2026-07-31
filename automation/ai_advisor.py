"""
VyapaarSetu Automation Engine — AI Merchant Growth Advisor
File: automation/ai_advisor.py

Business Value:
    Provides automated operational insights for retail merchants based on stock velocity,
    vendor SLA performance, and revenue trajectory.

Input:
    - data/stores.csv
    - data/inventory.csv
Output:
    - Actionable merchant advice JSON payload
"""

import json
from automation.ai_advisor_flow import AIAdvisorFlowEngine

if __name__ == '__main__':
    engine = AIAdvisorFlowEngine()
    print(json.dumps(engine.generate_merchant_advice(), indent=2))
