# Test Plan

Run:

```bash
python3 -m unittest discover -s tests -v
```

Browser checks:

- Dashboard loads
- Changing readings updates kWh and bill cost
- Peak usage slider updates the cost-driver chart
- Mobile layout remains readable
