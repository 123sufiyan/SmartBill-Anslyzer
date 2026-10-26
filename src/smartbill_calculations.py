"""Electricity bill analysis and savings calculations."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class MonthlyBill:
    month: str
    kwh: float
    cost: float


@dataclass(frozen=True)
class BillInput:
    previous_reading_kwh: float
    current_reading_kwh: float
    unit_rate: float
    standing_charge_daily: float
    billing_days: int
    peak_percent: float
    offpeak_rate: float
    monthly_history: tuple[MonthlyBill, ...]
    standby_watts: float


@dataclass(frozen=True)
class BillResult:
    total_kwh: float
    bill_cost: float
    cost_per_day: float
    abnormal_increase_percent: float
    standby_waste_kwh: float
    standby_waste_cost: float
    projected_annual_spend: float
    anomaly_month: str
    recommendations: tuple[str, ...]


def validate_bill(data: BillInput) -> None:
    if data.current_reading_kwh < data.previous_reading_kwh:
        raise ValueError("current_reading_kwh must be greater than previous_reading_kwh")
    for name, value in {
        "unit_rate": data.unit_rate,
        "standing_charge_daily": data.standing_charge_daily,
        "billing_days": data.billing_days,
        "offpeak_rate": data.offpeak_rate,
    }.items():
        if value <= 0:
            raise ValueError(f"{name} must be greater than zero")
    if not 0 <= data.peak_percent <= 100:
        raise ValueError("peak_percent must be between 0 and 100")
    if data.standby_watts < 0:
        raise ValueError("standby_watts cannot be negative")
    if len(data.monthly_history) < 2:
        raise ValueError("monthly_history must contain at least two months")


def analyze_bill(data: BillInput) -> BillResult:
    validate_bill(data)
    total_kwh = data.current_reading_kwh - data.previous_reading_kwh
    peak_kwh = total_kwh * data.peak_percent / 100
    offpeak_kwh = total_kwh - peak_kwh
    energy_cost = peak_kwh * data.unit_rate + offpeak_kwh * data.offpeak_rate
    bill_cost = energy_cost + data.standing_charge_daily * data.billing_days
    cost_per_day = bill_cost / data.billing_days
    history_avg = mean(month.kwh for month in data.monthly_history[:-1])
    latest = data.monthly_history[-1]
    abnormal_increase_percent = ((latest.kwh - history_avg) / history_avg) * 100
    anomaly_month = latest.month if abnormal_increase_percent >= 20 else "None"
    standby_waste_kwh = data.standby_watts * 24 * data.billing_days / 1000
    standby_waste_cost = standby_waste_kwh * data.unit_rate
    projected_annual_spend = cost_per_day * 365

    recommendations: list[str] = []
    if data.peak_percent > 60:
        recommendations.append("Shift laundry, heating, and charging to off-peak hours.")
    if standby_waste_cost > 5:
        recommendations.append("Use smart plugs to reduce standby power waste.")
    if abnormal_increase_percent >= 20:
        recommendations.append("Investigate the high-usage month for appliance faults or tariff changes.")
    if total_kwh / data.billing_days > 12:
        recommendations.append("Check high-load appliances such as immersion heaters, fridge/freezers, and dryers.")
    if not recommendations:
        recommendations.append("Usage is stable; keep monitoring monthly readings.")

    return BillResult(
        total_kwh=total_kwh,
        bill_cost=bill_cost,
        cost_per_day=cost_per_day,
        abnormal_increase_percent=abnormal_increase_percent,
        standby_waste_kwh=standby_waste_kwh,
        standby_waste_cost=standby_waste_cost,
        projected_annual_spend=projected_annual_spend,
        anomaly_month=anomaly_month,
        recommendations=tuple(recommendations),
    )


def sample_bill() -> BillInput:
    return BillInput(
        previous_reading_kwh=12480,
        current_reading_kwh=12892,
        unit_rate=0.31,
        standing_charge_daily=0.52,
        billing_days=30,
        peak_percent=72,
        offpeak_rate=0.18,
        standby_watts=42,
        monthly_history=(
            MonthlyBill("2026-01", 310, 108),
            MonthlyBill("2026-02", 295, 104),
            MonthlyBill("2026-03", 322, 112),
            MonthlyBill("2026-04", 318, 111),
            MonthlyBill("2026-05", 412, 137),
        ),
    )


def result_as_dict(result: BillResult) -> dict[str, float | str]:
    return {
        "total_kwh": round(result.total_kwh, 2),
        "bill_cost": round(result.bill_cost, 2),
        "cost_per_day": round(result.cost_per_day, 2),
        "abnormal_increase_percent": round(result.abnormal_increase_percent, 2),
        "standby_waste_kwh": round(result.standby_waste_kwh, 2),
        "standby_waste_cost": round(result.standby_waste_cost, 2),
        "projected_annual_spend": round(result.projected_annual_spend, 2),
        "anomaly_month": result.anomaly_month,
        "recommendations": " | ".join(result.recommendations),
    }
