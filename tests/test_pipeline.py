import pandas as pd
from src.pipeline import clean_orders, build_customer_rfm


def test_clean_orders_fills_discount_and_filters_rows():
    df = pd.DataFrame(
        {
            "order_id": [1, 2],
            "quantity": [2, -1],
            "net_sales": [100.0, 50.0],
            "discount": [None, 0.2],
        }
    )
    out = clean_orders(df)
    assert len(out) == 1
    assert out.iloc[0]["discount"] == 0.0


def test_rfm_score_has_expected_columns():
    df = pd.DataFrame(
        {
            "customer_id": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
            "order_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "order_ts": pd.to_datetime([
                "2025-01-01", "2025-01-10", "2025-01-02", "2025-01-12", "2025-01-03",
                "2025-01-13", "2025-01-04", "2025-01-14", "2025-01-05", "2025-01-15",
            ]),
            "order_status": ["completed"] * 10,
            "net_sales": [100, 200, 120, 230, 90, 140, 80, 160, 110, 170],
        }
    )
    out = build_customer_rfm(df)
    assert {"r_score", "f_score", "m_score", "rfm_score"}.issubset(out.columns)
