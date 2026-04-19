import pandas as pd
import numpy as np
import random, os

random.seed(42)
np.random.seed(42)

# ── Generate 5 orders per supplier (500 total) ────────────────────────────
rows = []
order_id = 1
base_date = pd.Timestamp("2026-01-01")

for supplier_id in range(1, 101):
    # Give each supplier a "personality" – some are reliably on-time, others lag
    base_delay = random.choice([0, 0, 1, 2, 3, 4, 6, 8])
    for j in range(5):
        order_date = base_date + pd.Timedelta(days=(order_id * 2) % 90)
        expected   = order_date + pd.Timedelta(days=random.randint(4, 7))
        actual_delay = max(0, int(np.random.normal(base_delay, 1.5)))
        actual     = expected + pd.Timedelta(days=actual_delay)
        rows.append({
            "order_id":          order_id,
            "supplier_id":       supplier_id,
            "order_date":        order_date.strftime("%Y-%m-%d"),
            "expected_delivery": expected.strftime("%Y-%m-%d"),
            "actual_delivery":   actual.strftime("%Y-%m-%d"),
        })
        order_id += 1

orders_df = pd.DataFrame(rows)
orders_df.to_csv("data/orders.csv", index=False)
print(f"Generated {len(orders_df)} orders for {orders_df['supplier_id'].nunique()} suppliers")
print(orders_df.head(10).to_string())
