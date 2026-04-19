import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    # Get project root directory
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # Load datasets safely
    orders = pd.read_csv(os.path.join(BASE_DIR, "data/orders.csv"))
    details = pd.read_csv(os.path.join(BASE_DIR, "data/order_details.csv"))
    suppliers = pd.read_csv(os.path.join(BASE_DIR, "data/suppliers.csv"))
    products = pd.read_csv(os.path.join(BASE_DIR, "data/products.csv"))

    # Convert date columns safely
    orders['expected_delivery'] = pd.to_datetime(
        orders['expected_delivery'], errors='coerce'
    )
    orders['actual_delivery'] = pd.to_datetime(
        orders['actual_delivery'], errors='coerce'
    )

    return orders, details, suppliers, products