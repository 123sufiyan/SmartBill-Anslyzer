import csv
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.smartbill_reports import export_sample_report


class SmartBillReportTests(unittest.TestCase):
    def test_export_sample_report(self):
        with TemporaryDirectory() as temp_dir:
            output = export_sample_report(Path(temp_dir) / "bill.csv")
            with output.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["anomaly_month"], "2026-05")


if __name__ == "__main__":
    unittest.main()
