import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main() -> None:
    kpi = pd.read_csv("dashboards/kpi_summary.csv")
    monthly = pd.read_csv("dashboards/monthly_sales_trend.csv")
    seg = pd.read_csv("dashboards/customer_segments.csv")

    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("Sales & Customer Insights Dashboard Preview", fontsize=16, fontweight="bold")

    axes[0, 0].plot(monthly["month"], monthly["net_sales"], marker="o")
    axes[0, 0].set_title("Monthly Net Sales")
    axes[0, 0].tick_params(axis="x", rotation=45)

    top_seg = seg.sort_values("net_sales", ascending=False).head(6)
    labels = top_seg["segment"] + "-" + top_seg["region"]
    axes[0, 1].bar(labels, top_seg["net_sales"])
    axes[0, 1].set_title("Top Segment-Region Revenue")
    axes[0, 1].tick_params(axis="x", rotation=35)

    kpi_disp = kpi.copy()
    kpi_disp["value"] = kpi_disp["value"].round(2)
    axes[1, 0].axis("off")
    table = axes[1, 0].table(cellText=kpi_disp.values, colLabels=kpi_disp.columns, cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    axes[1, 0].set_title("Executive KPI Snapshot")

    axes[1, 1].text(
        0.02,
        0.9,
        "Highlights:\n- 180K orders\n- RFM scoring\n- Cohort retention\n- Channel-campaign profitability",
        fontsize=11,
        va="top",
    )
    axes[1, 1].axis("off")

    plt.tight_layout()
    plt.savefig("assets/sales_customer_dashboard_preview.png", dpi=170)


if __name__ == "__main__":
    main()
