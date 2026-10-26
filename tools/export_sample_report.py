#!/usr/bin/env python3
"""Export sample SmartBill analysis as CSV."""

from pathlib import Path

from src.smartbill_reports import export_sample_report


def main() -> None:
    print(export_sample_report(Path("reports/sample_bill_analysis.csv")))


if __name__ == "__main__":
    main()
