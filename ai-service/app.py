from flask import Flask, request, jsonify

app = Flask(__name__)


def calculate_ai_risk(amount, location, transaction_count):
    risk_score = 0

    if amount > 50000:
        risk_score += 40
    elif amount > 20000:
        risk_score += 20

    if transaction_count > 10:
        risk_score += 30
    elif transaction_count > 5:
        risk_score += 15

    if location.lower() not in ["hyderabad", "bangalore", "chennai"]:
        risk_score += 20

    if risk_score >= 60:
        risk_level = "HIGH"
    elif risk_score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "riskScore": risk_score,
        "riskLevel": risk_level,
        "message": "AI transaction risk analysed successfully."
    }


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    amount = data.get("amount", 0)
    location = data.get("location", "")
    transaction_count = data.get("transactionCount", 0)

    result = calculate_ai_risk(
        amount,
        location,
        transaction_count
    )

    return jsonify(result)


if __name__ == "_main_":
    app.run(host="0.0.0.0", port=5000)