"""CSV report helpers for SmartBill Analyzer."""

from __future__ import annotations

import csv
from pathlib import Path

from .smartbill_calculations import analyze_bill, result_as_dict, sample_bill


FIELDNAMES = [
    "total_kwh",
    "bill_cost",
    "cost_per_day",
    "abnormal_increase_percent",
    "standby_waste_kwh",
    "standby_waste_cost",
    "projected_annual_spend",
    "anomaly_month",
    "recommendations",
]


def export_sample_report(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    row = result_as_dict(analyze_bill(sample_bill()))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerow(row)
    return path
