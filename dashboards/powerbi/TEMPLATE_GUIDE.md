# Power BI Template Guide

## Recommended Pages
1. Executive KPI Overview
2. Sales & Profit Trends
3. Customer Segmentation and RFM
4. Campaign and Channel Efficiency
5. Cohort Retention

## Data Sources
- `dashboards/kpi_summary.csv`
- `dashboards/monthly_sales_trend.csv`
- `dashboards/customer_segments.csv`
- `dashboards/product_performance.csv`
- `dashboards/channel_campaign_performance.csv`
- `dashboards/customer_rfm_scores.csv`
- `dashboards/cohort_retention.csv`

## Suggested DAX Measures
- `Profit Margin = DIVIDE(SUM([profit]), SUM([net_sales]))`
- `AOV = DIVIDE(SUM([net_sales]), DISTINCTCOUNT([order_id]))`
- `Retention % = DIVIDE(SUM([customers]), MAX([cohort_size]))`

## Visual Layout
- Top row: KPI cards
- Middle row: monthly trend and channel-campaign matrix
- Bottom row: RFM heatmap and cohort retention chart
