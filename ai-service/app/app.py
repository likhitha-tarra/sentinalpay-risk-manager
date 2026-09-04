from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained AI models
model_data = joblib.load("fraud_model.pkl")

model = model_data["model"]
anomaly_model = model_data["anomaly_model"]
encoder = model_data["encoder"]


FEATURES = [
    "amount",
    "transaction_count",
    "customer_avg_amount",
    "amount_deviation",
    "device_changed",
    "location_changed",
    "failed_attempts",
    "new_beneficiary",
    "hour",
    "location_encoded"
]


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    amount = float(data.get("amount", 0))
    transaction_count = int(data.get("transactionCount", 0))
    customer_avg_amount = float(
        data.get("customerAvgAmount", 1)
    )

    device_changed = int(data.get("deviceChanged", 0))
    location_changed = int(data.get("locationChanged", 0))
    failed_attempts = int(data.get("failedAttempts", 0))
    new_beneficiary = int(data.get("newBeneficiary", 0))

    hour = int(data.get("hour", 12))
    location = data.get("location", "Unknown")

    # Feature engineering
    amount_deviation = (
            amount / max(customer_avg_amount, 1)
    )

    # Location encoding
    try:
        location_encoded = encoder.transform(
            [location]
        )[0]
    except ValueError:
        location_encoded = encoder.transform(
            ["Unknown"]
        )[0]

    # Prepare AI input
    input_data = pd.DataFrame(
        [[
            amount,
            transaction_count,
            customer_avg_amount,
            amount_deviation,
            device_changed,
            location_changed,
            failed_attempts,
            new_beneficiary,
            hour,
            location_encoded
        ]],
        columns=FEATURES
    )

    # ======================================
    # AI MODEL 1: Random Forest
    # ======================================

    fraud_probability = model.predict_proba(
        input_data
    )[0][1]

    ml_score = fraud_probability * 100


    # ======================================
    # AI MODEL 2: Isolation Forest
    # ======================================

    anomaly_prediction = anomaly_model.predict(
        input_data
    )[0]

    anomaly_decision = anomaly_model.decision_function(
        input_data
    )[0]

    if anomaly_prediction == -1:
        anomaly_risk = 100
    else:
        anomaly_risk = max(
            0,
            min(
                100,
                (0.5 - anomaly_decision) * 100
            )
        )

    anomaly_risk = round(anomaly_risk, 2)


    # ======================================
    # COMBINED AI RISK SCORE
    # ======================================

    risk_score = round(
        (ml_score * 0.75) +
        (anomaly_risk * 0.25),
        2
    )


    # Risk classification
    if risk_score >= 70:
        risk_level = "HIGH"
    elif risk_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"


    # ======================================
    # EXPLAINABLE AI
    # ======================================

    reasons = []

    if amount_deviation > 3:
        reasons.append(
            "Transaction amount is significantly higher than normal"
        )

    if transaction_count > 10:
        reasons.append(
            "Unusually high transaction velocity"
        )

    if device_changed == 1:
        reasons.append(
            "New or changed device detected"
        )

    if location_changed == 1:
        reasons.append(
            "Transaction location differs from normal behaviour"
        )

    if failed_attempts >= 3:
        reasons.append(
            "Multiple failed transaction attempts detected"
        )

    if new_beneficiary == 1:
        reasons.append(
            "New beneficiary detected"
        )

    if hour < 5:
        reasons.append(
            "Transaction occurred during unusual hours"
        )

    if anomaly_prediction == -1:
        reasons.append(
            "AI anomaly detector identified unusual behaviour"
        )

    if not reasons:
        reasons.append(
            "Transaction behaviour appears normal"
        )


    return jsonify({
        "riskScore": risk_score,
        "riskLevel": risk_level,
        "fraudProbability": round(
            fraud_probability, 3
        ),
        "anomalyRisk": anomaly_risk,
        "reasons": reasons,
        "message":
            "AI transaction risk analysis completed"
    })


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "service": "SentinelPay AI Risk Engine",
        "status": "running",
        "models": [
            "Random Forest",
            "Isolation Forest"
        ],
        "features": 10,
        "explainableAI": True,
        "message":
            "AI fraud detection service is active"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )