def process_orders(orders, details):
    """
    Process raw orders and order_details to compute:
    - total_cost per order
    - delay_days (no negatives)
    - on_time flag
    """

    # ---------------- COPY DATA (SAFE PRACTICE) ---------------- #
    orders = orders.copy()
    details = details.copy()

    # ---------------- TOTAL COST ---------------- #
    details['total_cost'] = details['quantity'] * details['cost_per_unit']

    order_cost = (
        details.groupby('order_id')['total_cost']
        .sum()
        .reset_index()
    )

    # ---------------- MERGE ---------------- #
    orders = orders.merge(order_cost, on='order_id', how='left')

    # Fill missing cost (if any)
    orders['total_cost'] = orders['total_cost'].fillna(0)

    # ---------------- DELAY CALCULATION ---------------- #
    orders['delay_days'] = (
        orders['actual_delivery'] - orders['expected_delivery']
    ).dt.days

    # Handle invalid dates
    orders['delay_days'] = orders['delay_days'].fillna(0)

    # Prevent negative delay
    orders['delay_days'] = orders['delay_days'].clip(lower=0)

    # ---------------- ON-TIME FLAG ---------------- #
    orders['on_time'] = (orders['delay_days'] == 0).astype(int)

    return orders


def aggregate_supplier_stats(orders):
    """
    Aggregate order-level data into supplier-level metrics
    """

    supplier_stats = (
        orders.groupby('supplier_id')
        .agg({
            'delay_days': 'mean',
            'on_time': 'mean',
            'total_cost': 'mean'
        })
        .reset_index()
    )

    # Rename columns clearly
    supplier_stats.columns = [
        'supplier_id',
        'avg_delay',
        'on_time_rate',
        'avg_cost'
    ]

    # Safety: fill missing values
    supplier_stats = supplier_stats.fillna(0)

    return supplier_stats