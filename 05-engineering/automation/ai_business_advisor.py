#!/usr/bin/env python3
"""
VyapaarSetu Engine — AI Strategic Business Advisor CLI Engine
Generates 0-to-1 capital allocation playbooks and store acquisition valuation guidance.
"""

import json
from typing import Dict, Any

class AIBusinessAdvisor:
    def advise(self, mode: str, user_input: Dict[str, Any]) -> Dict[str, Any]:
        mode_upper = mode.upper()
        if mode_upper == "START":
            capital = float(user_input.get("budget_inr", 250000))
            category = user_input.get("category", "Textiles & Handblock Prints")
            location = user_input.get("location", "Jaipur RJ")
            return {
                "mode": "START A BUSINESS",
                "playbook_summary": f"0-to-1 Launch Playbook for {category} in {location}",
                "capital_allocation": {
                    "initial_inventory_escrow": f"Rs.{capital * 0.40:,.0f} (40%)",
                    "storefront_and_branding": f"Rs.{capital * 0.25:,.0f} (25%)",
                    "performance_marketing": f"Rs.{capital * 0.25:,.0f} (25%)",
                    "emergency_reserve": f"Rs.{capital * 0.10:,.0f} (10%)"
                },
                "escrow_wallet_advice": "Lock supplier batch payments in VyapaarSetu Multi-Sig Escrow.",
                "next_step": "Register store and browse preferred suppliers."
            }
        elif mode_upper == "SELL":
            revenue = float(user_input.get("monthly_revenue_inr", 1850000))
            profit = float(user_input.get("monthly_profit_inr", 425000))
            annual_profit = profit * 12
            asking_price = annual_profit * 2.5
            return {
                "mode": "SELL A STORE / BUSINESS",
                "audit_status": "P&L Verified via VyapaarSetu Bank API",
                "valuation_metrics": {
                    "monthly_revenue": f"Rs.{revenue:,.0f}",
                    "monthly_net_profit": f"Rs.{profit:,.0f}",
                    "annual_net_profit": f"Rs.{annual_profit:,.0f}",
                    "suggested_asking_price": f"Rs.{asking_price:,.0f} (2.5x Annual P/E Multiple)"
                },
                "escrow_terms": "Buyer deposits 100% funds into Master Acquisition Escrow. 7-day physical audit window."
            }
        else:
            return {"error": "Unsupported mode. Choose START or SELL."}


if __name__ == "__main__":
    advisor = AIBusinessAdvisor()
    print("==================================================================")
    print("VYAPAARSETU AI BUSINESS ADVISOR -- STRATEGIC CONSOLE DEMO")
    print("==================================================================")
    
    start_output = advisor.advise("START", {"budget_inr": 250000, "category": "Textiles & Handblock Prints", "location": "Jaipur RJ"})
    print("\n--- [MODE 1: START A BUSINESS] ---")
    print(json.dumps(start_output, indent=2))
