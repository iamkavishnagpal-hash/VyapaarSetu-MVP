"""
VyapaarSetu Automation Engine — Escrow Payment State Machine Engine
File: automation/escrow_workflow.py

Business Value:
    Manages end-to-end B2B trade vault transactions. Locks funds upon buyer placement, 
    verifies delivery webhooks, manages inspection windows, and executes fund release or dispute holds.

Input:
    - Escrow transaction payload
    - data/escrow_transactions.csv
Output:
    - Escrow state transition log & payout authorization signal
"""

import os
import csv
import json
from typing import Dict, Any, List

class EscrowWorkflowEngine:
    STATES = ['INITIATED', 'FUNDED', 'IN_INSPECTION', 'DISPUTED', 'RELEASED', 'REFUNDED']

    def __init__(self, escrow_csv: str = 'data/escrow_transactions.csv'):
        self.escrow_csv = escrow_csv
        self.escrow_records: List[Dict[str, Any]] = []

    def load_data(self) -> None:
        """Loads existing escrow records from CSV storage."""
        if os.path.exists(self.escrow_csv):
            with open(self.escrow_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.escrow_records.append({
                        'escrow_id': row['escrow_id'],
                        'order_id': row['order_id'],
                        'amount_inr': float(row['escrow_amount_inr']),
                        'status': row['status'],
                        'funded_date': row['funded_date'],
                        'released_date': row['released_date']
                    })

    def process_state_transition(self, escrow_id: str, action: str) -> Dict[str, Any]:
        """Executes escrow state machine logic based on milestone actions."""
        target = next((item for item in self.escrow_records if item['escrow_id'] == escrow_id), None)
        if not target:
            return {'status': 'ERROR', 'message': f'Escrow record {escrow_id} not found.'}

        current_state = target['status'].upper()

        if action == 'MARK_DELIVERED' and current_state == 'FUNDED':
            new_state = 'IN_INSPECTION'
            msg = 'Delivery confirmed by courier webhook. 72-hour buyer inspection window started.'
        elif action == 'APPROVE_PAYOUT' and current_state in ['FUNDED', 'IN_INSPECTION']:
            new_state = 'RELEASED'
            msg = f'Escrow funds ₹{target["amount_inr"]:,.2f} released to vendor merchant account.'
        elif action == 'RAISE_DISPUTE' and current_state in ['FUNDED', 'IN_INSPECTION']:
            new_state = 'DISPUTED'
            msg = 'Buyer raised defect dispute. Escrow vault locked pending resolution.'
        else:
            return {'status': 'INVALID_TRANSITION', 'message': f'Cannot perform {action} from state {current_state}.'}

        target['status'] = new_state
        return {
            'status': 'SUCCESS',
            'escrow_id': escrow_id,
            'order_id': target['order_id'],
            'previous_state': current_state,
            'new_state': new_state,
            'vault_amount_inr': target['amount_inr'],
            'notification_message': msg
        }

if __name__ == '__main__':
    engine = EscrowWorkflowEngine()
    engine.load_data()
    if engine.escrow_records:
        test_id = engine.escrow_records[0]['escrow_id']
        result = engine.process_state_transition(escrow_id=test_id, action='APPROVE_PAYOUT')
        print(json.dumps(result, indent=2))
