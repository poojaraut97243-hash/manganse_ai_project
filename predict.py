import joblib
import pandas as pd


# Load trained model
model = joblib.load("models/risk_model.pkl")


# New location data
data = pd.DataFrame([{
    "ndvi": 0.40,
    "ndbi": 0.65,
    "ndwi": 0.08,
    "heat": 36,
    "distance_industry": 1.0,
    "industry_density": 10
}])


# Prediction
prediction = model.predict(data)[0]


# Probability
probability = model.predict_proba(data)[0]
confidence = max(probability) * 100


print("\n===================================")
print("       🛰️ JALNASAT AI SYSTEM")
print("===================================")

print("NDVI              :", data["ndvi"][0])
print("NDBI              :", data["ndbi"][0])
print("NDWI              :", data["ndwi"][0])
print("Temperature       :", data["heat"][0], "°C")
print("Industry Distance :", data["distance_industry"][0], "km")
print("Industry Density  :", data["industry_density"][0])

print("-----------------------------------")

print("Predicted Risk     :", prediction.upper())
print("Confidence         :", round(confidence, 2), "%")

print("===================================")