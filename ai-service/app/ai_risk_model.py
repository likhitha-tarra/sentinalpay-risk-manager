import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score
)
from sklearn.model_selection import train_test_split


# ---------------------------------------------------------
# 1. Load Dataset
# ---------------------------------------------------------

DATASET_PATH = "creditcard.csv"

df = pd.read_csv(DATASET_PATH)

print("==============================================")
print("SentinelPay AI Risk Manager - Model Training")
print("==============================================")

print("Dataset rows    :", len(df))
print("Dataset columns :", len(df.columns))
print("Fraud cases     :", int(df["Class"].sum()))
print("Normal cases    :", int((df["Class"] == 0).sum()))


# ---------------------------------------------------------
# 2. Feature Engineering
# ---------------------------------------------------------

df["hour"] = (
    (df["Time"] % 86400) / 3600
).astype(float)

df["amount_log"] = np.log1p(
    df["Amount"].clip(lower=0)
)


FEATURES = [
    "Time",
    "Amount",
    "hour",
    "amount_log"
] + [f"V{i}" for i in range(1, 29)]


X = df[FEATURES]
y = df["Class"]


# ---------------------------------------------------------
# 3. Train / Validation / Held-out Test Split
# ---------------------------------------------------------

# First split:
# 80% development data
# 20% completely held-out test data

X_dev, X_test, y_dev, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42
)


# Split development data again:
# 75% training
# 25% validation
#
# Final proportions:
# 60% Train
# 20% Validation
# 20% Held-out Test

X_train, X_val, y_train, y_val = train_test_split(
    X_dev,
    y_dev,
    test_size=0.25,
    stratify=y_dev,
    random_state=42
)


print()
print("Data split:")
print("Training rows       :", len(X_train))
print("Validation rows     :", len(X_val))
print("Held-out test rows  :", len(X_test))


# ---------------------------------------------------------
# 4. Random Forest Fraud Detection Model
# ---------------------------------------------------------

print()
print("Training Random Forest...")

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_leaf=2,
    class_weight="balanced_subsample",
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)


# ---------------------------------------------------------
# 5. Validation Prediction
# ---------------------------------------------------------

val_probability = model.predict_proba(
    X_val
)[:, 1]


# ---------------------------------------------------------
# 6. Select Decision Threshold Using Validation Set
# ---------------------------------------------------------

best_threshold = 0.50
best_f1 = 0.0

for threshold in np.arange(
    0.10,
    0.91,
    0.01
):

    val_prediction = (
        val_probability >= threshold
    ).astype(int)

    current_f1 = f1_score(
        y_val,
        val_prediction,
        zero_division=0
    )

    if current_f1 > best_f1:
        best_f1 = current_f1
        best_threshold = float(threshold)


print()
print(
    "Selected validation threshold:",
    round(best_threshold, 2)
)

print(
    "Validation F1:",
    round(best_f1, 4)
)


# ---------------------------------------------------------
# 7. Final Held-out Test Evaluation
# ---------------------------------------------------------

test_probability = model.predict_proba(
    X_test
)[:, 1]


test_prediction = (
    test_probability >= best_threshold
).astype(int)


precision = precision_score(
    y_test,
    test_prediction,
    zero_division=0
)

recall = recall_score(
    y_test,
    test_prediction,
    zero_division=0
)

f1 = f1_score(
    y_test,
    test_prediction,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    test_probability
)

pr_auc = average_precision_score(
    y_test,
    test_probability
)


# ---------------------------------------------------------
# 8. Print Final Metrics
# ---------------------------------------------------------

print()
print("==============================================")
print("FINAL HELD-OUT TEST RESULTS")
print("==============================================")

print(
    "Precision :",
    round(precision, 4),
    "(",
    round(precision * 100, 2),
    "%)"
)

print(
    "Recall    :",
    round(recall, 4),
    "(",
    round(recall * 100, 2),
    "%)"
)

print(
    "F1 Score  :",
    round(f1, 4),
    "(",
    round(f1 * 100, 2),
    "%)"
)

print(
    "ROC-AUC   :",
    round(roc_auc, 4),
    "(",
    round(roc_auc * 100, 2),
    "%)"
)

print(
    "PR-AUC    :",
    round(pr_auc, 4),
    "(",
    round(pr_auc * 100, 2),
    "%)"
)

print()
print("Test fraud cases   :", int(y_test.sum()))
print(
    "Test normal cases :",
    int((y_test == 0).sum())
)


# ---------------------------------------------------------
# 9. Isolation Forest Anomaly Detector
# ---------------------------------------------------------

print()
print("Training Isolation Forest...")

anomaly_model = IsolationForest(
    n_estimators=150,
    contamination=0.002,
    random_state=42
)

anomaly_model.fit(
    X_train
)


# ---------------------------------------------------------
# 10. Save Models + Evaluation Information
# ---------------------------------------------------------

joblib.dump(
    {
        "model": model,

        "anomaly_model": anomaly_model,

        "features": FEATURES,

        "dataset":
            "ULB Credit Card Fraud Detection",

        "decision_threshold":
            best_threshold,

        "evaluation": {

            "precision":
                precision,

            "recall":
                recall,

            "f1":
                f1,

            "roc_auc":
                roc_auc,

            "pr_auc":
                pr_auc,

            "evaluation_type":
                "Held-out test set",

            "train_rows":
                len(X_train),

            "validation_rows":
                len(X_val),

            "test_rows":
                len(X_test)
        }
    },

    "fraud_model.pkl"
)


print()
print("==============================================")
print("Model saved successfully!")
print("File: fraud_model.pkl")
print("==============================================")