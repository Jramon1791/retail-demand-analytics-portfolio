# Retail Demand Analytics Portfolio

Hiring-focused analytics project that demonstrates:
- Data modeling and synthetic data generation.
- KPI pipeline design in Python.
- Business-oriented SQL analysis patterns.
- Reproducible outputs and basic test coverage.

## Project Story
An online retailer wants to understand:
- Revenue trends by region and month.
- Top products and margin pressure from discounts.
- Customer lifetime value distribution.

This repo creates realistic synthetic order data and builds analytics-ready datasets for decision-making.

## Tech Stack
- Python 3.13
- Pandas / NumPy
- Pytest / Ruff (dev)

## Repository Structure
```
retail-demand-analytics-portfolio/
  data/
    raw/
    processed/
  outputs/
  scripts/
    run_pipeline.py
  sql/
    business_questions.sql
  src/retail_analytics/
    data_generator.py
    pipeline.py
    insights.py
  tests/
    test_pipeline.py
```

## Quick Start
1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -e .`
   - `pip install -e ".[dev]"`
3. Run the pipeline:
   - `python scripts/run_pipeline.py`

## Produced Artifacts
- `data/raw/orders.csv`
- `data/processed/monthly_region_kpis.csv`
- `data/processed/customer_ltv.csv`
- `data/processed/product_performance.csv`
- `outputs/portfolio_summary.md`

## Hiring Notes
This project is intentionally structured like a production mini-analytics repo:
- Source-controlled pipeline code.
- Deterministic data generation with seed support.
- Explicit output contracts tested with pytest.
- Business-facing summary report.

## Next Improvements
1. Add a dashboard layer (Streamlit/Power BI/Tableau).
2. Add forecasting and cohort retention analysis.
3. Add CI pipeline for lint + tests.
