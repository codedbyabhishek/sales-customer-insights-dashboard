# Sales & Customer Insights Dashboard

End-to-end analytics project for sales and customer insights (Jan 2025 - Jun 2025).

## Highlights
- Generated and processed **50K+ sales records** across customers, products, and transactions.
- Performed EDA for customer purchase patterns and product performance.
- Built advanced SQL analysis with joins, subqueries, and CTEs.
- Exported KPI datasets for **Power BI** and **Excel** dashboards.
- Produced actionable insights that can support targeted marketing optimization.

## Project Structure
- `scripts/generate_data.py`: synthetic multi-source data generation
- `src/pipeline.py`: cleaning, validation, feature engineering, KPI extraction
- `src/eda.py`: exploratory analysis and summary artifacts
- `sql/analysis_queries.sql`: business SQL use cases (joins/subqueries/CTEs)
- `dashboards/`: exported dashboard-ready CSV outputs
- `tests/`: validation tests

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_data.py
python src/pipeline.py
python src/eda.py
```

## Outputs
- `data/processed/fact_sales.csv`
- `dashboards/kpi_summary.csv`
- `dashboards/customer_segments.csv`
- `dashboards/product_performance.csv`
- `dashboards/monthly_sales_trend.csv`

## Dashboarding
Use `dashboards/*.csv` directly in Power BI and Excel Pivot dashboards.

