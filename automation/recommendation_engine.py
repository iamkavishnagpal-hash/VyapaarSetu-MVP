"""
VyapaarSetu Automation Engine — Product Cross-Sell & Basket Recommendation Matrix
File: automation/recommendation_engine.py

Business Value:
    Analyzes historical co-purchase patterns across customer orders to generate personalized 
    product bundle recommendations at checkout, boosting Average Order Value (AOV).

Input:
    - Target product_id
    - data/orders.csv
Output:
    - Recommended complementary products with association support confidence scores
"""

import os
import csv
import json
from typing import Dict, Any, List
from collections import defaultdict

class RecommendationEngine:
    def __init__(self, orders_csv: str = 'data/orders.csv'):
        self.orders_csv = orders_csv
        self.co_occurrences: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.product_counts: Dict[str, int] = defaultdict(int)

    def load_and_train(self) -> None:
        """Builds item co-occurrence matrix from customer order baskets."""
        order_baskets: Dict[str, List[str]] = defaultdict(list)
        if os.path.exists(self.orders_csv):
            with open(self.orders_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    order_baskets[row['order_id']].append(row['product_id'])

        for o_id, items in order_baskets.items():
            unique_items = list(set(items))
            for item in unique_items:
                self.product_counts[item] += 1
            for i in range(len(unique_items)):
                for j in range(i + 1, len(unique_items)):
                    item_a, item_b = unique_items[i], unique_items[j]
                    self.co_occurrences[item_a][item_b] += 1
                    self.co_occurrences[item_b][item_a] += 1

    def recommend(self, product_id: str, top_n: int = 3) -> Dict[str, Any]:
        """Returns top N recommended cross-sell items for a given product."""
        if product_id not in self.co_occurrences:
            # Fallback recommendations if product has no history
            top_popular = sorted(self.product_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
            recs = [{'recommended_product_id': p, 'confidence_score_pct': 70.0, 'rule_type': 'POPULARITY_FALLBACK'} for p, _ in top_popular]
            return {'product_id': product_id, 'recommendations': recs}

        related = self.co_occurrences[product_id]
        total_base = self.product_counts[product_id]

        recs = []
        for other_p, freq in related.items():
            confidence = round((freq / total_base) * 100.0, 1)
            recs.append({
                'recommended_product_id': other_p,
                'co_purchase_count': freq,
                'confidence_score_pct': confidence,
                'rule_type': 'ASSOCIATION_BASKET'
            })

        recs = sorted(recs, key=lambda x: x['confidence_score_pct'], reverse=True)[:top_n]
        return {
            'status': 'SUCCESS',
            'product_id': product_id,
            'recommendations': recs
        }

if __name__ == '__main__':
    engine = RecommendationEngine()
    engine.load_and_train()
    print(json.dumps(engine.recommend(product_id='PRD-3001'), indent=2))
