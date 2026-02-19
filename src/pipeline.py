import os
import pandas as pd


def load_raw() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    customers = pd.read_csv("data/raw/customers.csv", parse_dates=["joined_date"])
    products = pd.read_csv("data/raw/products.csv")
    orders = pd.read_csv("data/raw/orders.csv", parse_dates=["order_ts"])
    return customers, products, orders


def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    orders = orders.copy()
    orders["discount"] = orders["discount"].fillna(0.0)
    orders = orders[(orders["quantity"] > 0) & (orders["net_sales"] >= 0)]
    return orders


def build_fact(customers: pd.DataFrame, products: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    fact = (
        orders.merge(customers, on="customer_id", how="left")
        .merge(products, on="product_id", how="left")
        .assign(
            month=lambda d: d["order_ts"].dt.to_period("M").astype(str),
            order_date=lambda d: d["order_ts"].dt.date,
        )
    )
    return fact


def build_customer_rfm(fact: pd.DataFrame) -> pd.DataFrame:
    snapshot = fact["order_ts"].max() + pd.Timedelta(days=1)

    rfm = (
        fact[fact["order_status"] == "completed"]
        .groupby("customer_id", as_index=False)
        .agg(
            recency_days=("order_ts", lambda x: (snapshot - x.max()).days),
            frequency=("order_id", "nunique"),
            monetary=("net_sales", "sum"),
        )
    )

    rfm["r_score"] = pd.qcut(rfm["recency_days"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["rfm_score"] = rfm["r_score"] + rfm["f_score"] + rfm["m_score"]
    return rfm


def build_cohort_retention(fact: pd.DataFrame) -> pd.DataFrame:
    base = fact[fact["order_status"] == "completed"].copy()
    base["order_month"] = base["order_ts"].dt.to_period("M")
    first_purchase = base.groupby("customer_id")["order_month"].min().rename("cohort_month")
    base = base.join(first_purchase, on="customer_id")
    base["cohort_index"] = (base["order_month"] - base["cohort_month"]).apply(lambda x: x.n)

    cohorts = (
        base.groupby(["cohort_month", "cohort_index"], as_index=False)
        .agg(customers=("customer_id", "nunique"))
        .sort_values(["cohort_month", "cohort_index"])
    )
    cohort_size = cohorts[cohorts["cohort_index"] == 0][["cohort_month", "customers"]].rename(columns={"customers": "cohort_size"})
    cohorts = cohorts.merge(cohort_size, on="cohort_month", how="left")
    cohorts["retention_rate"] = (cohorts["customers"] / cohorts["cohort_size"]).round(4)
    cohorts["cohort_month"] = cohorts["cohort_month"].astype(str)
    return cohorts


def export_dashboard_data(fact: pd.DataFrame) -> None:
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("dashboards", exist_ok=True)

    fact.to_csv("data/processed/fact_sales.csv", index=False)

    monthly = fact.groupby("month", as_index=False).agg(
        net_sales=("net_sales", "sum"),
        gross_sales=("gross_sales", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
    )
    monthly["aov"] = (monthly["net_sales"] / monthly["orders"]).round(2)

    customer_segments = fact.groupby(["segment", "region"], as_index=False).agg(
        net_sales=("net_sales", "sum"),
        customers=("customer_id", "nunique"),
        profit=("profit", "sum"),
    )

    product_performance = fact.groupby(["category", "subcategory", "product_id"], as_index=False).agg(
        net_sales=("net_sales", "sum"),
        units=("quantity", "sum"),
        profit=("profit", "sum"),
    )

    channel_campaign = fact.groupby(["channel", "campaign"], as_index=False).agg(
        net_sales=("net_sales", "sum"),
        orders=("order_id", "nunique"),
        profit=("profit", "sum"),
    )

    kpi = pd.DataFrame(
        {
            "metric": [
                "net_sales",
                "gross_sales",
                "total_profit",
                "profit_margin",
                "total_orders",
                "avg_order_value",
                "active_customers",
            ],
            "value": [
                fact["net_sales"].sum(),
                fact["gross_sales"].sum(),
                fact["profit"].sum(),
                fact["profit"].sum() / max(fact["net_sales"].sum(), 1),
                fact["order_id"].nunique(),
                fact.groupby("order_id")["net_sales"].sum().mean(),
                fact["customer_id"].nunique(),
            ],
        }
    )

    rfm = build_customer_rfm(fact)
    cohorts = build_cohort_retention(fact)

    monthly.to_csv("dashboards/monthly_sales_trend.csv", index=False)
    customer_segments.to_csv("dashboards/customer_segments.csv", index=False)
    product_performance.sort_values("net_sales", ascending=False).to_csv("dashboards/product_performance.csv", index=False)
    channel_campaign.sort_values("net_sales", ascending=False).to_csv("dashboards/channel_campaign_performance.csv", index=False)
    rfm.to_csv("dashboards/customer_rfm_scores.csv", index=False)
    cohorts.to_csv("dashboards/cohort_retention.csv", index=False)
    kpi.to_csv("dashboards/kpi_summary.csv", index=False)


if __name__ == "__main__":
    customers_df, products_df, orders_df = load_raw()
    clean_df = clean_orders(orders_df)
    fact_df = build_fact(customers_df, products_df, clean_df)
    export_dashboard_data(fact_df)
    print("Pipeline complete. Advanced dashboard marts are ready.")
