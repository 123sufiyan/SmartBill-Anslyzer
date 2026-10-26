import unittest

from src.smartbill_calculations import BillInput, MonthlyBill, analyze_bill, sample_bill


class SmartBillCalculationTests(unittest.TestCase):
    def test_sample_bill_detects_anomaly_and_costs(self):
        result = analyze_bill(sample_bill())

        self.assertEqual(result.total_kwh, 412)
        self.assertGreater(result.bill_cost, 120)
        self.assertEqual(result.anomaly_month, "2026-05")
        self.assertGreater(result.standby_waste_cost, 5)

    def test_stable_usage_has_no_anomaly(self):
        data = BillInput(
            previous_reading_kwh=1000,
            current_reading_kwh=1250,
            unit_rate=0.3,
            standing_charge_daily=0.5,
            billing_days=30,
            peak_percent=50,
            offpeak_rate=0.2,
            standby_watts=5,
            monthly_history=(
                MonthlyBill("2026-01", 250, 75),
                MonthlyBill("2026-02", 248, 74),
                MonthlyBill("2026-03", 252, 76),
            ),
        )

        self.assertEqual(analyze_bill(data).anomaly_month, "None")

    def test_current_reading_must_not_be_lower(self):
        data = sample_bill()
        bad = BillInput(
            previous_reading_kwh=data.current_reading_kwh,
            current_reading_kwh=data.previous_reading_kwh,
            unit_rate=data.unit_rate,
            standing_charge_daily=data.standing_charge_daily,
            billing_days=data.billing_days,
            peak_percent=data.peak_percent,
            offpeak_rate=data.offpeak_rate,
            monthly_history=data.monthly_history,
            standby_watts=data.standby_watts,
        )

        with self.assertRaisesRegex(ValueError, "current_reading_kwh"):
            analyze_bill(bad)


if __name__ == "__main__":
    unittest.main()
