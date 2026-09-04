from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load trained AI model
model_data = joblib.load("fraud_model.pkl")

model = model_data["model"]
anomaly_model = model_data["anomaly_model"]
FEATURES = model_data["features"]


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    # -----------------------------
    # Frontend transaction inputs
    # -----------------------------

    amount = float(data.get("amount", 0))

    transaction_count = int(
        data.get("transactionCount", 0)
    )

    customer_avg_amount = float(
        data.get("customerAvgAmount", 1)
    )

    device_changed = int(
        data.get("deviceChanged", 0)
    )

    location_changed = int(
        data.get("locationChanged", 0)
    )

    failed_attempts = int(
        data.get("failedAttempts", 0)
    )

    new_beneficiary = int(
        data.get("newBeneficiary", 0)
    )

    hour = int(
        data.get("hour", 12)
    )

    # -----------------------------
    # ULB model input
    # -----------------------------

    feature_values = []

    for feature in FEATURES:

        if feature == "Amount":
            value = amount

        elif feature == "Time":
            value = hour * 3600

        elif feature == "hour":
            value = hour

        elif feature == "amount_log":
            value = np.log1p(max(amount, 0))

        elif feature.startswith("V"):
            value = 0.0

        else:
            value = 0.0

        feature_values.append(value)

    input_data = pd.DataFrame(
        [feature_values],
        columns=FEATURES
    )

    # -----------------------------
    # Random Forest
    # -----------------------------

    fraud_probability = model.predict_proba(
        input_data
    )[0][1]

    ml_score = fraud_probability * 100

    # -----------------------------
    # Isolation Forest
    # -----------------------------

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

    anomaly_risk = round(
        anomaly_risk,
        2
    )

    # -----------------------------
    # Additional transaction signals
    # -----------------------------

    amount_deviation = (
        amount /
        max(customer_avg_amount, 1)
    )

    rule_score = 0

    # Transaction amount risk
    if amount_deviation > 3:

        rule_score += 20

    elif amount_deviation > 1.5:

        rule_score += 10

    # Transaction velocity risk
    if transaction_count > 10:

        rule_score += 20

    elif transaction_count >= 4:

        rule_score += 10

    # Device change risk
    if device_changed == 1:

        rule_score += 15

    # Location change risk
    if location_changed == 1:

        rule_score += 15

    # Failed transaction attempts
    if failed_attempts >= 3:

        rule_score += 15

    elif failed_attempts >= 1:

        rule_score += 5

    # New beneficiary risk
    if new_beneficiary == 1:

        rule_score += 15

    # Unusual transaction hour
    if hour < 5:

        rule_score += 10

    rule_score = min(
        rule_score,
        100
    )

    # -----------------------------
    # Combined Risk Score
    # -----------------------------
    #
    # 45% Random Forest
    # 15% Isolation Forest
    # 40% Real-time transaction signals
    # -----------------------------

    risk_score = (
        ml_score * 0.45
        + anomaly_risk * 0.15
        + rule_score * 0.40
    )

    # -----------------------------
    # Risk Guardrails
    # -----------------------------
    #
    # Strong transaction signals
    # should not be classified as LOW.
    #
    # rule_score >= 60 -> HIGH
    # rule_score >= 20 -> MEDIUM
    # -----------------------------

    if rule_score >= 60:

        risk_score = max(
            risk_score,
            70
        )

    elif rule_score >= 20:

        risk_score = max(
            risk_score,
            40
        )

    risk_score = round(
        max(
            0,
            min(
                100,
                risk_score
            )
        ),
        2
    )

    # -----------------------------
    # Risk Classification
    # -----------------------------

    if risk_score >= 70:

        risk_level = "HIGH"

    elif risk_score >= 40:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    # -----------------------------
    # Explainable AI reasons
    # -----------------------------

    reasons = []

    if amount_deviation > 3:

        reasons.append(
            "Transaction amount is significantly higher than normal"
        )

    elif amount_deviation > 1.5:

        reasons.append(
            "Transaction amount is moderately higher than normal"
        )

    if transaction_count > 10:

        reasons.append(
            "Unusually high transaction velocity"
        )

    elif transaction_count >= 4:

        reasons.append(
            "Elevated transaction velocity detected"
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

    elif failed_attempts >= 1:

        reasons.append(
            "Failed transaction attempt detected"
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

    # -----------------------------
    # Response
    # -----------------------------

    return jsonify({

        "riskScore": risk_score,

        "riskLevel": risk_level,

        "fraudProbability": round(
            fraud_probability,
            4
        ),

        "anomalyRisk": anomaly_risk,

        "reasons": reasons,

        "message":
            "AI transaction risk analysis completed"
    })


@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "service":
            "SentinelPay AI Risk Engine",

        "status":
            "running",

        "models": [
            "Random Forest",
            "Isolation Forest"
        ],

        "features":
            len(FEATURES),

        "dataset":
            "ULB Credit Card Fraud Detection",

        "explainableAI":
            True,

        "message":
            "AI fraud detection service is active"
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )