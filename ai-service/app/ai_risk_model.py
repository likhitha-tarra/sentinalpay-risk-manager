import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score


# ==========================================
# SENTINELPAY AI RISK ENGINE
# Random Forest + Isolation Forest
# ==========================================

data = {
    "amount": [
        500, 1200, 2500, 8000, 15000, 75000, 90000, 3000,
        450, 1800, 22000, 65000, 700, 5500, 120000, 1000,
        3500, 48000, 85000, 600, 900, 2000, 4500, 11000,
        18000, 70000, 95000, 1500, 3200, 58000, 130000, 800
    ],

    "transaction_count": [
        1, 2, 3, 4, 5, 15, 18, 2,
        1, 3, 12, 16, 2, 6, 20, 1,
        4, 10, 14, 2, 1, 3, 4, 5,
        6, 17, 19, 2, 3, 13, 22, 1
    ],

    "customer_avg_amount": [
        800, 1500, 2200, 7500, 12000, 10000, 15000, 3500,
        600, 2000, 4000, 12000, 900, 6000, 18000, 1100,
        3000, 30000, 15000, 700, 900, 1800, 4000, 10000,
        16000, 12000, 18000, 1400, 3500, 5000, 20000, 900
    ],

    "device_changed": [
        0, 0, 0, 0, 0, 1, 1, 0,
        0, 0, 1, 1, 0, 0, 1, 0,
        0, 1, 1, 0, 0, 0, 0, 0,
        0, 1, 1, 0, 0, 1, 1, 0
    ],

    "location_changed": [
        0, 0, 0, 0, 0, 1, 1, 0,
        0, 0, 1, 1, 0, 0, 1, 0,
        0, 1, 1, 0, 0, 0, 0, 0,
        0, 1, 1, 0, 0, 1, 1, 0
    ],

    "failed_attempts": [
        0, 0, 0, 1, 0, 4, 5, 0,
        0, 0, 3, 4, 0, 1, 6, 0,
        0, 2, 5, 0, 0, 0, 1, 0,
        0, 4, 5, 0, 1, 3, 6, 0
    ],

    "new_beneficiary": [
        0, 0, 0, 0, 0, 1, 1, 0,
        0, 0, 1, 1, 0, 0, 1, 0,
        0, 1, 1, 0, 0, 0, 0, 0,
        0, 1, 1, 0, 0, 1, 1, 0
    ],

    "hour": [
        10, 11, 14, 15, 12, 2, 3, 13,
        10, 16, 1, 3, 11, 14, 2, 12,
        15, 23, 1, 10, 13, 14, 15, 12,
        16, 2, 4, 11, 13, 1, 3, 14
    ],

    "location": [
        "Hyderabad", "Hyderabad", "Bangalore", "Chennai",
        "Hyderabad", "Unknown", "Unknown", "Bangalore",
        "Chennai", "Hyderabad", "Unknown", "Unknown",
        "Hyderabad", "Bangalore", "Unknown", "Chennai",
        "Hyderabad", "Unknown", "Unknown", "Chennai",
        "Hyderabad", "Bangalore", "Chennai", "Hyderabad",
        "Bangalore", "Unknown", "Unknown", "Hyderabad",
        "Chennai", "Unknown", "Unknown", "Bangalore"
    ],

    "is_fraud": [
        0, 0, 0, 0, 0, 1, 1, 0,
        0, 0, 1, 1, 0, 0, 1, 0,
        0, 1, 1, 0, 0, 0, 0, 0,
        0, 1, 1, 0, 0, 1, 1, 0
    ]
}

df = pd.DataFrame(data)


# ==========================================
# Feature engineering
# ==========================================

df["amount_deviation"] = (
        df["amount"] / df["customer_avg_amount"]
)

encoder = LabelEncoder()

df["location_encoded"] = encoder.fit_transform(
    df["location"]
)


features = [
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

X = df[features]
y = df["is_fraud"]


# ==========================================
# Random Forest - supervised learning
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)


# ==========================================
# Isolation Forest - anomaly detection
# ==========================================

anomaly_model = IsolationForest(
    n_estimators=150,
    contamination=0.25,
    random_state=42
)

anomaly_model.fit(X_train)


# ==========================================
# Model evaluation
# ==========================================

predictions = model.predict(X_test)

probabilities = model.predict_proba(X_test)[:, 1]

precision = precision_score(
    y_test,
    predictions,
    zero_division=0
)

recall = recall_score(
    y_test,
    predictions,
    zero_division=0
)

f1 = f1_score(
    y_test,
    predictions,
    zero_division=0
)

auc = roc_auc_score(
    y_test,
    probabilities
)


print()
print("======================================")
print("      SENTINELPAY AI RISK ENGINE")
print("======================================")

print("Random Forest")
print("Precision :", round(precision, 3))
print("Recall    :", round(recall, 3))
print("F1 Score  :", round(f1, 3))
print("ROC-AUC   :", round(auc, 3))

print()
print("Isolation Forest")
print("Anomaly detection : ENABLED")


# ==========================================
# Save both AI models
# ==========================================

joblib.dump(
    {
        "model": model,
        "anomaly_model": anomaly_model,
        "encoder": encoder
    },
    "fraud_model.pkl"
)

print()
print("AI models saved successfully.")


# ==========================================
# Combined AI Risk Prediction
# ==========================================

def calculate_ai_risk(
        amount,
        transaction_count,
        customer_avg_amount,
        device_changed,
        location_changed,
        failed_attempts,
        new_beneficiary,
        hour,
        location
):

    amount_deviation = (
            amount / max(customer_avg_amount, 1)
    )

    try:
        location_encoded = encoder.transform(
            [location]
        )[0]
    except ValueError:
        location_encoded = encoder.transform(
            ["Unknown"]
        )[0]


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
        columns=features
    )


    # Supervised fraud probability
    fraud_probability = model.predict_proba(
        input_data
    )[0][1]


    # Unsupervised anomaly detection
    anomaly_prediction = anomaly_model.predict(
        input_data
    )[0]

    anomaly_score = anomaly_model.decision_function(
        input_data
    )[0]


    # Convert anomaly result to 0-100
    anomaly_risk = 0

    if anomaly_prediction == -1:
        anomaly_risk = 100
    else:
        anomaly_risk = max(
            0,
            min(
                100,
                round((0.5 - anomaly_score) * 100, 2)
            )
        )


    # Combine both AI signals
    ml_score = fraud_probability * 100

    final_score = round(
        (ml_score * 0.75) +
        (anomaly_risk * 0.25),
        2
    )


    if final_score >= 70:
        risk_level = "HIGH"
    elif final_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"


    # ======================================
    # Explainable AI
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


    return {
        "riskScore": final_score,
        "riskLevel": risk_level,
        "fraudProbability": round(
            fraud_probability,
            3
        ),
        "anomalyRisk": round(
            anomaly_risk,
            2
        ),
        "reasons": reasons,
        "message":
            "AI transaction risk analysis completed"
    }


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    result = calculate_ai_risk(
        amount=75000,
        transaction_count=12,
        customer_avg_amount=10000,
        device_changed=1,
        location_changed=1,
        failed_attempts=4,
        new_beneficiary=1,
        hour=2,
        location="Unknown"
    )

    print()
    print("======================================")
    print("         TEST TRANSACTION")
    print("======================================")

    print("Risk Score        :", result["riskScore"])
    print("Risk Level        :", result["riskLevel"])
    print("Fraud Probability :", result["fraudProbability"])
    print("Anomaly Risk      :", result["anomalyRisk"])

    print()
    print("AI Reasons:")

    for reason in result["reasons"]:
        print("-", reason)

    print()
    print("Message :", result["message"])