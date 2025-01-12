import os
import pandas as pd


def load_raw() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    customers = pd.read_csv("data/raw/customers.csv")
    products = pd.read_csv("data/raw/products.csv")
    orders = pd.read_csv("data/raw/orders.csv", parse_dates=["order_date"])
    return customers, products, orders


def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    orders = orders.copy()
    orders["discount"] = orders["discount"].fillna(0.0)
    orders = orders[(orders["quantity"] > 0) & (orders["sales"] >= 0)]
    return orders


def build_fact(customers: pd.DataFrame, products: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    fact = (
        orders.merge(customers, on="customer_id", how="left")
        .merge(products, on="product_id", how="left")
        .assign(month=lambda d: d["order_date"].dt.to_period("M").astype(str))
    )
    return fact


def export_dashboard_data(fact: pd.DataFrame) -> None:
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("dashboards", exist_ok=True)

    fact.to_csv("data/processed/fact_sales.csv", index=False)

    monthly = fact.groupby("month", as_index=False).agg(total_sales=("sales", "sum"), orders=("order_id", "nunique"))
    segments = fact.groupby("segment", as_index=False).agg(total_sales=("sales", "sum"), customers=("customer_id", "nunique"))
    products = fact.groupby(["category", "product_id"], as_index=False).agg(total_sales=("sales", "sum"), units=("quantity", "sum"))

    kpi = pd.DataFrame(
        {
            "metric": ["total_sales", "total_orders", "avg_order_value", "active_customers"],
            "value": [
                fact["sales"].sum(),
                fact["order_id"].nunique(),
                fact.groupby("order_id")["sales"].sum().mean(),
                fact["customer_id"].nunique(),
            ],
        }
    )

    monthly.to_csv("dashboards/monthly_sales_trend.csv", index=False)
    segments.to_csv("dashboards/customer_segments.csv", index=False)
    products.sort_values("total_sales", ascending=False).to_csv("dashboards/product_performance.csv", index=False)
    kpi.to_csv("dashboards/kpi_summary.csv", index=False)


if __name__ == "__main__":
    customers_df, products_df, orders_df = load_raw()
    clean_df = clean_orders(orders_df)
    fact_df = build_fact(customers_df, products_df, clean_df)
    export_dashboard_data(fact_df)
    print("Pipeline complete. Dashboard files are ready.")
