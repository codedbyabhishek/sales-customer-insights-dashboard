import os
import numpy as np
import pandas as pd

RNG = np.random.default_rng(2025)


def ensure_dirs() -> None:
    os.makedirs("data/raw", exist_ok=True)


def generate_customers(n: int = 20000) -> pd.DataFrame:
    regions = ["North", "South", "East", "West", "Central"]
    cities = [
        "New York", "Chicago", "Austin", "Seattle", "San Diego", "Boston",
        "Atlanta", "Phoenix", "Denver", "Dallas",
    ]
    segments = ["Consumer", "Corporate", "Home Office", "Enterprise"]

    joined_dates = pd.to_datetime(RNG.choice(pd.date_range("2022-01-01", "2025-06-30", freq="D"), n))

    df = pd.DataFrame(
        {
            "customer_id": np.arange(1, n + 1),
            "region": RNG.choice(regions, n),
            "city": RNG.choice(cities, n),
            "segment": RNG.choice(segments, n, p=[0.52, 0.22, 0.16, 0.10]),
            "age": RNG.integers(18, 72, n),
            "annual_income": np.round(RNG.normal(78000, 22000, n).clip(22000, 250000), 0),
            "joined_date": joined_dates,
        }
    )
    return df


def generate_products(n: int = 450) -> pd.DataFrame:
    categories = ["Technology", "Office Supplies", "Furniture", "Accessories"]
    subcategories = {
        "Technology": ["Laptops", "Monitors", "Phones", "Printers"],
        "Office Supplies": ["Paper", "Storage", "Binders", "Art"],
        "Furniture": ["Chairs", "Tables", "Bookcases", "Desks"],
        "Accessories": ["Headphones", "Cables", "Adapters", "Bags"],
    }

    category_vals = RNG.choice(categories, n, p=[0.36, 0.28, 0.22, 0.14])
    subcat_vals = [RNG.choice(subcategories[c]) for c in category_vals]
    base_price = np.round(RNG.uniform(6, 2200, n), 2)

    df = pd.DataFrame(
        {
            "product_id": np.arange(1, n + 1),
            "category": category_vals,
            "subcategory": subcat_vals,
            "unit_price": base_price,
            "cost": np.round(base_price * RNG.uniform(0.45, 0.82, n), 2),
        }
    )
    return df


def generate_orders(customers: pd.DataFrame, products: pd.DataFrame, n: int = 180000) -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", "2025-06-30", freq="h")
    channels = ["Online", "Store", "Partner", "Marketplace"]
    payment_methods = ["Card", "UPI", "Bank Transfer", "Wallet"]
    campaign_names = ["NewYear", "Summer", "BackToOffice", "Festive", "Retention", "Organic"]

    product_ids = RNG.choice(products["product_id"], n)
    qty = RNG.integers(1, 10, n)
    discount = np.round(RNG.choice([0.0, 0.05, 0.1, 0.15, 0.2], n, p=[0.30, 0.28, 0.24, 0.13, 0.05]), 2)

    map_price = products.set_index("product_id")["unit_price"]
    map_cost = products.set_index("product_id")["cost"]
    unit_price = map_price.loc[product_ids].to_numpy()
    unit_cost = map_cost.loc[product_ids].to_numpy()

    gross_sales = qty * unit_price
    net_sales = np.round(gross_sales * (1 - discount), 2)
    total_cost = np.round(qty * unit_cost, 2)
    profit = np.round(net_sales - total_cost, 2)

    status = RNG.choice(["completed", "returned", "cancelled"], n, p=[0.9, 0.06, 0.04])
    status_adj = np.where(status == "cancelled", 0.0, 1.0)
    net_sales = np.round(net_sales * status_adj, 2)
    profit = np.where(status == "cancelled", 0.0, profit)

    df = pd.DataFrame(
        {
            "order_id": np.arange(1, n + 1),
            "order_ts": RNG.choice(dates, n),
            "customer_id": RNG.choice(customers["customer_id"], n),
            "product_id": product_ids,
            "quantity": qty,
            "discount": discount,
            "gross_sales": np.round(gross_sales, 2),
            "net_sales": net_sales,
            "cost": total_cost,
            "profit": np.round(profit, 2),
            "channel": RNG.choice(channels, n, p=[0.45, 0.30, 0.12, 0.13]),
            "payment_method": RNG.choice(payment_methods, n, p=[0.52, 0.24, 0.14, 0.10]),
            "campaign": RNG.choice(campaign_names, n),
            "order_status": status,
        }
    )

    missing_idx = RNG.choice(df.index, 1200, replace=False)
    df.loc[missing_idx, "discount"] = np.nan
    return df


if __name__ == "__main__":
    ensure_dirs()
    customers = generate_customers()
    products = generate_products()
    orders = generate_orders(customers, products)

    customers.to_csv("data/raw/customers.csv", index=False)
    products.to_csv("data/raw/products.csv", index=False)
    orders.to_csv("data/raw/orders.csv", index=False)
    print(f"Generated high-end sales datasets: customers={len(customers)}, products={len(products)}, orders={len(orders)}")
