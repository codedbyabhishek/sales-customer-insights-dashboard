import os
import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)


def ensure_dirs() -> None:
    os.makedirs("data/raw", exist_ok=True)


def generate_customers(n: int = 12000) -> pd.DataFrame:
    cities = ["New York", "Chicago", "Austin", "Seattle", "San Diego", "Boston"]
    segments = ["Consumer", "Corporate", "Home Office"]
    df = pd.DataFrame(
        {
            "customer_id": np.arange(1, n + 1),
            "city": RNG.choice(cities, n),
            "segment": RNG.choice(segments, n, p=[0.6, 0.25, 0.15]),
            "age": RNG.integers(18, 70, n),
        }
    )
    return df


def generate_products(n: int = 180) -> pd.DataFrame:
    categories = ["Technology", "Office Supplies", "Furniture"]
    df = pd.DataFrame(
        {
            "product_id": np.arange(1, n + 1),
            "category": RNG.choice(categories, n, p=[0.4, 0.35, 0.25]),
            "unit_price": np.round(RNG.uniform(5, 1200, n), 2),
        }
    )
    return df


def generate_orders(customers: pd.DataFrame, products: pd.DataFrame, n: int = 52000) -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", "2025-06-30", freq="D")
    qty = RNG.integers(1, 8, n)
    product_ids = RNG.choice(products["product_id"], n)
    unit_prices = products.set_index("product_id").loc[product_ids, "unit_price"].to_numpy()
    discounts = np.round(RNG.choice([0.0, 0.05, 0.1, 0.15], n, p=[0.45, 0.3, 0.2, 0.05]), 2)
    sales = np.round(qty * unit_prices * (1 - discounts), 2)

    df = pd.DataFrame(
        {
            "order_id": np.arange(1, n + 1),
            "order_date": RNG.choice(dates, n),
            "customer_id": RNG.choice(customers["customer_id"], n),
            "product_id": product_ids,
            "quantity": qty,
            "discount": discounts,
            "sales": sales,
        }
    )

    missing_idx = RNG.choice(df.index, 300, replace=False)
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
    print("Generated raw datasets with 50K+ records.")
