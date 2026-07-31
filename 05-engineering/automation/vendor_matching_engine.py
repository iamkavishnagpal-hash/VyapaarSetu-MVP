#!/usr/bin/env python3
"""
VyapaarSetu Engine — Multi-Criteria B2B Vendor Scoring Engine
Matches MSME merchants with optimal suppliers based on Lead Time, Defect Rate, Rating, and Escrow Verification.
Reads directly from 02-data/datasets/vendors.csv.
"""

import os
import csv
import json
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Vendor:
    vendor_id: str
    name: str
    category: str
    location: str
    rating: float
    lead_time_days: int
    on_time_rate_pct: float
    defect_rate_pct: float
    min_order_qty: int
    escrow_verified: bool

    @property
    def composite_score(self) -> float:
        score = (self.on_time_rate_pct * 0.40) + ((100.0 - self.defect_rate_pct) * 0.40) + (self.rating * 4.0)
        if self.escrow_verified:
            score += 5.0
        return round(score, 2)


class VendorMatcher:
    def __init__(self, csv_filepath: str):
        self.filepath = csv_filepath
        self.vendors: List[Vendor] = []
        self._load_vendors()

    def _load_vendors(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Vendor CSV dataset missing at {self.filepath}")

        with open(self.filepath, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                v = Vendor(
                    vendor_id=row['vendor_id'],
                    name=row['name'],
                    category=row['category'],
                    location=row['location'],
                    rating=float(row['rating']),
                    lead_time_days=int(row['lead_time_days']),
                    on_time_rate_pct=float(row['on_time_rate_pct']),
                    defect_rate_pct=float(row['defect_rate_pct']),
                    min_order_qty=int(row['min_order_qty']),
                    escrow_verified=row['escrow_verified'].upper() == 'TRUE'
                )
                self.vendors.append(v)

    def match_vendors(self, category: str, max_lead_time: int = 14, min_score: float = 80.0) -> List[Dict[str, Any]]:
        matched = []
        for v in self.vendors:
            if category.lower() in v.category.lower() and v.lead_time_days <= max_lead_time and v.composite_score >= min_score:
                matched.append({
                    "vendor_id": v.vendor_id,
                    "name": v.name,
                    "location": v.location,
                    "composite_score": v.composite_score,
                    "rating": v.rating,
                    "lead_time_days": v.lead_time_days,
                    "escrow_verified": v.escrow_verified,
                    "supplier_tier": "PREFERRED SUPPLIER" if v.composite_score >= 90.0 else "STANDARD SUPPLIER"
                })
        
        matched.sort(key=lambda x: x['composite_score'], reverse=True)
        return matched


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_path = os.path.join(base_dir, "02-data", "datasets", "vendors.csv")
    matcher = VendorMatcher(data_path)
    
    print("==================================================================")
    print("VYAPAARSETU VENDOR MATCHING ENGINE -- AI RECOMMENDATIONS")
    print("==================================================================")
    
    results = matcher.match_vendors(category="Textiles", max_lead_time=10)
    print(f"Query: Category='Textiles', Max Lead Time=10 days")
    print(f"Matched Suppliers Found: {len(results)}\n")
    print(json.dumps(results[:5], indent=2))
