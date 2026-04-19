from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Features used for training – must match what the UI predictor sends
FEATURE_COLS = ['avg_cost', 'on_time_rate']

def train_model(supplier_stats):
    # ---------------- FEATURES & TARGET ---------------- #
    X = supplier_stats[FEATURE_COLS]
    y = supplier_stats['avg_delay']

    # ---------------- HANDLE MISSING VALUES ---------------- #
    X = X.fillna(0)
    y = y.fillna(0)

    # ---------------- TRAIN-TEST SPLIT ---------------- #
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ---------------- TRAIN MODEL (Random Forest for better accuracy) -------- #
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # ---------------- PREDICTION ---------------- #
    preds = model.predict(X_test)

    # ---------------- RMSE (SAFE VERSION) ---------------- #
    mse = mean_squared_error(y_test, preds)
    rmse = np.sqrt(mse)

    # ---------------- FULL DATA PREDICTION ---------------- #
    supplier_stats['predicted_delay'] = model.predict(X)

    return supplier_stats, model, rmse