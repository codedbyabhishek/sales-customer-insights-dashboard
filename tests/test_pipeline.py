import pandas as pd
from src.pipeline import clean_orders


def test_clean_orders_fills_discount_and_filters_rows():
    df = pd.DataFrame(
        {
            "order_id": [1, 2],
            "quantity": [2, -1],
            "sales": [100.0, 50.0],
            "discount": [None, 0.2],
        }
    )
    out = clean_orders(df)
    assert len(out) == 1
    assert out.iloc[0]["discount"] == 0.0
