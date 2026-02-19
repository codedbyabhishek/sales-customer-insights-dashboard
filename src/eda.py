import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def run_eda() -> None:
    fact = pd.read_csv("data/processed/fact_sales.csv", parse_dates=["order_ts"])
    os.makedirs("reports", exist_ok=True)

    summary = {
        "records": len(fact),
        "date_min": str(fact["order_ts"].min().date()),
        "date_max": str(fact["order_ts"].max().date()),
        "net_sales": round(float(fact["net_sales"].sum()), 2),
        "profit": round(float(fact["profit"].sum()), 2),
        "profit_margin": round(float(fact["profit"].sum() / max(fact["net_sales"].sum(), 1)), 4),
    }
    pd.DataFrame([summary]).to_csv("reports/eda_summary.csv", index=False)

    monthly = fact.groupby(fact["order_ts"].dt.to_period("M").astype(str))["net_sales"].sum().reset_index()
    plt.figure(figsize=(11, 4))
    plt.plot(monthly["order_ts"], monthly["net_sales"], marker="o", linewidth=2)
    plt.title("Monthly Net Sales Trend")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.35)
    plt.tight_layout()
    plt.savefig("reports/monthly_sales_trend.png", dpi=150)

    by_channel = fact.groupby("channel", as_index=False)["net_sales"].sum().sort_values("net_sales", ascending=False)
    plt.figure(figsize=(8, 4))
    plt.bar(by_channel["channel"], by_channel["net_sales"])
    plt.title("Net Sales by Channel")
    plt.tight_layout()
    plt.savefig("reports/sales_by_channel.png", dpi=150)


if __name__ == "__main__":
    run_eda()
    print("EDA artifacts generated in reports/.")
