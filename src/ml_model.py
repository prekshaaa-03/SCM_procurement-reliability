from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

def train_model(supplier_stats):
    # ---------------- FEATURES & TARGET ---------------- #
    X = supplier_stats[['avg_cost', 'rating', 'on_time_rate']]
    y = supplier_stats['avg_delay']

    # ---------------- HANDLE MISSING VALUES ---------------- #
    X = X.fillna(0)
    y = y.fillna(0)

    # ---------------- TRAIN-TEST SPLIT ---------------- #
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ---------------- TRAIN MODEL ---------------- #
    model = LinearRegression()
    model.fit(X_train, y_train)

    # ---------------- PREDICTION ---------------- #
    preds = model.predict(X_test)

    # ---------------- RMSE (SAFE VERSION) ---------------- #
    mse = mean_squared_error(y_test, preds)
    rmse = np.sqrt(mse)

    # ---------------- FULL DATA PREDICTION ---------------- #
    supplier_stats['predicted_delay'] = model.predict(X)

    return supplier_stats, model, rmse