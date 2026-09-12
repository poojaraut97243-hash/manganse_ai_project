import pandas as pd
import numpy as np
import os
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Create models folder
os.makedirs("models", exist_ok=True)

# Read dataset
data = pd.read_csv("data/mining_data.csv")

# -----------------------------
# RESERVE PREDICTION MODEL
# -----------------------------

features_reserve = [
    "depth",
    "grade",
    "ndvi",
    "soil_moisture",
    "temperature"
]

X = data[features_reserve]

# Sample reserve calculation for prototype
# In a real project, this should come from geological reserve data.
data["estimated_reserve"] = (
    data["grade"] * 1000
    + data["depth"] * 20
    + (1 - data["ndvi"]) * 5000
)

y = data["estimated_reserve"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

reserve_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

reserve_model.fit(X_train, y_train)

prediction = reserve_model.predict(X_test)

print("Reserve Model MAE:",
      mean_absolute_error(y_test, prediction))

joblib.dump(
    reserve_model,
    "models/reserve_model.pkl"
)

# -----------------------------
# PRODUCTION PREDICTION MODEL
# -----------------------------

features_production = [
    "rainfall",
    "downtime",
    "blasting_delay",
    "temperature",
    "soil_moisture"
]

X2 = data[features_production]
y2 = data["actual_production"]

X2_train, X2_test, y2_train, y2_test = train_test_split(
    X2,
    y2,
    test_size=0.2,
    random_state=42
)

production_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

production_model.fit(X2_train, y2_train)

prediction2 = production_model.predict(X2_test)

print("Production Model MAE:",
      mean_absolute_error(y2_test, prediction2))

joblib.dump(
    production_model,
    "models/production_model.pkl"
)

print("\nModels successfully created!")