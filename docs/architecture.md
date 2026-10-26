# Architecture

SmartBill Analyzer is a static dashboard backed by a tested Python reference
calculation layer.

- `index.html`, `styles.css`, and `app.js` implement the dashboard.
- `src/smartbill_calculations.py` calculates bill cost, anomaly detection,
  standby waste, projected annual spend, and recommendations.
- `src/smartbill_reports.py` exports a CSV report.
- GitHub Actions runs the Python unit tests.
