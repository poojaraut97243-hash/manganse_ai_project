from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)

# Load dataset
data = pd.read_csv("data/mining_data.csv")

# Load trained models
reserve_model = joblib.load(
    "models/reserve_model.pkl"
)

production_model = joblib.load(
    "models/production_model.pkl"
)


# --------------------------------
# HOME PAGE
# --------------------------------

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# --------------------------------
# DASHBOARD DATA
# --------------------------------

@app.route("/api/dashboard")
def dashboard():

    total_reserve = data["estimated_reserve"].sum()

    today_production = int(
        data["actual_production"].iloc[-1]
    )

    expected_production = int(
        data["target_production"].iloc[-1]
    )

    shortfall = (
        expected_production -
        today_production
    )

    if shortfall < 0:
        shortfall = 0

    shortfall_percentage = (
        shortfall / expected_production
    ) * 100

    # Risk level
    if shortfall_percentage >= 15:
        risk = "HIGH"
    elif shortfall_percentage >= 8:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return jsonify({
        "total_reserve": round(
            total_reserve / 1000000, 2
        ),
        "today_production": today_production,
        "expected_production": expected_production,
        "shortfall": shortfall,
        "shortfall_percentage": round(
            shortfall_percentage, 2
        ),
        "risk": risk
    })


# --------------------------------
# RESERVE PREDICTION
# --------------------------------

@app.route(
    "/api/predict_reserve",
    methods=["POST"]
)
def predict_reserve():

    request_data = request.json

    values = [[
        float(request_data["depth"]),
        float(request_data["grade"]),
        float(request_data["ndvi"]),
        float(request_data["soil_moisture"]),
        float(request_data["temperature"])
    ]]

    prediction = reserve_model.predict(
        values
    )[0]

    return jsonify({
        "predicted_reserve": round(
            prediction, 2
        )
    })


# --------------------------------
# PRODUCTION PREDICTION
# --------------------------------

@app.route(
    "/api/predict_production",
    methods=["POST"]
)
def predict_production():

    request_data = request.json

    values = [[
        float(request_data["rainfall"]),
        float(request_data["downtime"]),
        float(request_data["blasting_delay"]),
        float(request_data["temperature"]),
        float(request_data["soil_moisture"])
    ]]

    prediction = production_model.predict(
        values
    )[0]

    target = float(
        request_data["target_production"]
    )

    shortfall = target - prediction

    if shortfall < 0:
        shortfall = 0

    risk_percentage = (
        shortfall / target
    ) * 100

    if risk_percentage >= 15:
        risk = "HIGH"
    elif risk_percentage >= 8:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return jsonify({
        "predicted_production": round(
            prediction, 2
        ),
        "shortfall": round(
            shortfall, 2
        ),
        "risk_percentage": round(
            risk_percentage, 2
        ),
        "risk": risk
    })


# --------------------------------
# RECOMMENDATION ENGINE
# --------------------------------

@app.route("/api/recommendations")
def recommendations():

    latest = data.iloc[-1]

    recommendations = []

    if latest["downtime"] >= 7:

        recommendations.append(
            "Re-deploy available equipment "
            "to reduce machine downtime."
        )

    if latest["rainfall"] >= 70:

        recommendations.append(
            "Adjust mining schedule because "
            "of heavy rainfall."
        )

    if latest["blasting_delay"] >= 3:

        recommendations.append(
            "Reschedule blasting activities "
            "to avoid production delays."
        )

    if latest["soil_moisture"] >= 70:

        recommendations.append(
            "Monitor mine roads and "
            "transport conditions."
        )

    if len(recommendations) == 0:

        recommendations.append(
            "Current conditions are normal. "
            "Continue planned operations."
        )

    return jsonify({
        "recommendations": recommendations
    })


# --------------------------------
# RUN SERVER
# --------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )