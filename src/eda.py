import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def run_eda() -> None:
    fact = pd.read_csv("data/processed/fact_sales.csv", parse_dates=["order_date"])
    os.makedirs("reports", exist_ok=True)

    summary = {
        "records": len(fact),
        "date_min": str(fact["order_date"].min().date()),
        "date_max": str(fact["order_date"].max().date()),
        "total_sales": round(float(fact["sales"].sum()), 2),
    }
    pd.DataFrame([summary]).to_csv("reports/eda_summary.csv", index=False)

    monthly = fact.groupby(fact["order_date"].dt.to_period("M").astype(str))["sales"].sum().reset_index()
    plt.figure(figsize=(10, 4))
    plt.plot(monthly["order_date"], monthly["sales"], marker="o", linewidth=2)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.title("Monthly Sales Trend")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("reports/monthly_sales_trend.png", dpi=150)


if __name__ == "__main__":
    run_eda()
    print("EDA artifacts generated in reports/.")
