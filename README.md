# SentinelPay AI Risk Manager

AI-powered real-time transaction fraud and anomaly detection system built for the Razorpay AI Buildathon.

## 🚀 Overview

SentinelPay AI Risk Manager is an AI-driven payment risk analysis platform designed to detect suspicious and abnormal transactions in real time.

The system combines supervised fraud classification, unsupervised anomaly detection, and transaction-behaviour rules to generate a risk score, identify the risk level, explain the reasons behind the decision, and recommend an appropriate action.

The system is designed as a defense-only payment risk management prototype.

## 🎯 Problem Statement

Digital payment platforms process a large number of transactions every day. Detecting fraudulent or abnormal transactions quickly is important to reduce financial losses while avoiding unnecessary blocking of genuine customers.

SentinelPay addresses this problem by analysing transaction and behavioural signals and generating an explainable risk assessment.

## 💡 Solution

SentinelPay analyses transaction and behavioural signals such as:

- Transaction amount
- Transaction velocity
- Customer average transaction amount
- Device changes
- Location changes
- Failed transaction attempts
- New beneficiary
- Transaction hour
- Network risk input

The AI engine produces:

- Risk Score
- Fraud Probability
- Anomaly Risk
- Risk Level
- Explainable AI Reasons
- Recommended Action

The dashboard allows a user or merchant to analyse a transaction and immediately view the resulting risk assessment.

## 🤖 AI Approach

### Random Forest

Random Forest is used as the supervised fraud classification model.

It learns fraud patterns from the public ULB Credit Card Fraud Detection dataset and estimates the probability that a transaction may be fraudulent.

The final model uses:

- 300 decision trees
- Maximum tree depth of 12
- Minimum samples per leaf of 2
- Balanced subsample class weighting
- Validation-based decision threshold of 0.39

### Isolation Forest

Isolation Forest is used for unsupervised anomaly detection.

It identifies transactions that behave differently from normal transaction patterns and provides an anomaly risk signal.

The anomaly detector uses:

- 150 estimators
- Contamination parameter of 0.002

### Behavioural Risk Rules

In addition to machine learning predictions, SentinelPay applies transparent behavioural risk rules.

These rules consider:

- Significant deviation from the customer's average transaction amount
- High transaction velocity
- Device changes
- Location changes
- Failed transaction attempts
- New beneficiaries
- Unusual transaction hours

This hybrid approach improves explainability and allows the system to respond to important behavioural signals even when anonymized dataset features are not directly available from dashboard inputs.

### Combined Risk Score

The final risk score combines three components:

- Machine learning fraud score: 45%
- Anomaly risk: 15%
- Behavioural risk rules: 40%

Final Risk Score = (ML Fraud Score × 45%) + (Anomaly Risk × 15%) + (Behavioural Risk Score × 40%)

The resulting score is bounded between 0 and 100.

Behavioural guardrails are also applied so that sufficiently strong risk signals cannot result in an artificially low classification.

### Risk Classification

- LOW: 0–39.9
- MEDIUM: 40–69.9
- HIGH: 70–100

## 🔍 Explainable AI

For every analysed transaction, SentinelPay provides human-readable reasons behind the risk decision.

Example signals include:

- Transaction amount significantly higher than normal
- Transaction amount moderately higher than normal
- Unusually high transaction velocity
- Elevated transaction velocity detected
- New or changed device detected
- Transaction location differs from normal behaviour
- Multiple failed transaction attempts detected
- Failed transaction attempt detected
- New beneficiary detected
- Transaction occurred during unusual hours
- AI anomaly detector identified unusual behaviour

This makes the system easier for a risk analyst or merchant to understand and review.

## 🗂️ Dataset

The supervised fraud detection model was trained and evaluated using the public ULB Credit Card Fraud Detection dataset.

Dataset characteristics:

- 284,807 transactions
- 492 fraud transactions
- 31 original columns
- Highly imbalanced fraud classification problem
- V1–V28 are anonymized PCA-transformed features
- Time and Amount are the primary non-anonymized transaction features

The dataset is a public benchmark dataset and is not Razorpay transaction data.

Because the dataset is highly imbalanced, precision, recall, F1 Score, ROC-AUC and PR-AUC are reported instead of relying on accuracy alone.

## 🧪 Model Evaluation

The model was evaluated using a train / validation / held-out test split.

### Dataset Split

- Training set: 170,883 transactions
- Validation set: 56,962 transactions
- Held-out test set: 56,962 transactions

The decision threshold was selected using the validation set before evaluating the final model on the held-out test set.

Selected validation threshold:

- 0.39

### Held-Out Test Results

| Metric | Result |
|--------|--------|
| Precision | 83.67% |
| Recall | 83.67% |
| F1 Score | 83.67% |
| ROC-AUC | 96.67% |
| PR-AUC | 84.23% |

These are held-out test results on the public ULB benchmark dataset.

They should not be interpreted as production performance or as performance on Razorpay's internal transaction data.

Further validation using representative payment-platform data would be required before production deployment.

## 🏗️ System Architecture

User / Merchant
        ↓
Web Dashboard
        ↓
Spring Boot REST API - Port 8080
        ↓
Python Flask AI Engine - Port 5000
        ↓
┌─────────────────────────────────┐
│ Random Forest                   │
│ Isolation Forest                │
│ Behavioural Risk Rules          │
└─────────────────────────────────┘
        ↓
Combined Risk Score
        ↓
Risk Classification
        ↓
LOW / MEDIUM / HIGH
        ↓
Explainable AI Reasons
        ↓
Recommended Action
        ↓
H2 Database
        ↓
Transaction History

## 🛠️ Technology Stack

### Frontend

- HTML
- CSS
- JavaScript
- Chart.js
- VS Code Live Server

### Backend

- Java
- Spring Boot
- Spring Data JPA
- REST APIs
- Maven

### AI / Machine Learning

- Python
- Flask
- Scikit-learn
- Random Forest
- Isolation Forest
- Joblib
- Pandas
- NumPy

### Database

- H2 Database
- File-based persistence for transaction history

## 📂 Project Structure

sentinelpay-risk-manager/
│
├── README.md
│
├── ai-service/
│   └── app/
│       ├── app.py
│       ├── ai_risk_model.py
│       ├── fraud_model.pkl
│       └── creditcard.csv
│
├── frontend/
│   └── index.html
│
└── sentinelpay-risk-manager/
    ├── pom.xml
    └── src/
        └── main/
            ├── java/
            └── resources/

## 🔄 Transaction Flow

Transaction Input
        ↓
Web Dashboard
        ↓
Spring Boot REST API
        ↓
Python Flask AI Engine
        ↓
Random Forest
        +
Isolation Forest
        +
Behavioural Risk Rules
        ↓
Combined Risk Score
        ↓
Risk Classification
        ↓
Explainable AI Reasons
        ↓
Recommended Action
        ↓
Transaction Stored in H2 Database
        ↓
Transaction History Updated

## ⚡ Risk-Based Actions

| Risk Level | Score | Recommended Action |
|------------|-------|--------------------|
| LOW | 0–39.9 | ALLOW |
| MEDIUM | 40–69.9 | STEP-UP VERIFICATION |
| HIGH | 70–100 | BLOCK / MANUAL REVIEW |

## 📊 Dashboard Features

The SentinelPay dashboard provides:

- Transaction risk analysis
- Risk score visualization
- Fraud probability display
- Anomaly risk display
- AI decision-confidence style indicator
- Explainable AI reasons
- Recommended action
- Risk distribution chart
- AI risk signals chart
- Recent transaction history
- Persistent transaction storage
- Spring Boot and Python AI engine status

## 🌐 Network Risk

Network Risk is included as a transaction-risk input in the dashboard to represent a potential external risk signal.

In a production payment system, such a signal could be derived from:

- IP reputation
- Proxy or VPN detection
- Network and location consistency
- Device/network fingerprinting
- Transaction velocity from a network
- Known malicious network indicators

In the current prototype, Network Risk is a manually supplied demonstration input and is not connected to a live external network-intelligence provider.

## 🛡️ Defense-Only Design

SentinelPay is designed strictly for defensive fraud and anomaly detection.

It focuses on:

- Detecting suspicious transactions
- Identifying abnormal behaviour
- Providing explainable risk signals
- Supporting risk-based decisions
- Reducing potential financial losses

It does not provide instructions for bypassing payment security systems or committing financial fraud.

## 🌟 Key Features

- Real-time transaction risk analysis
- Supervised fraud classification
- Unsupervised anomaly detection
- Behavioural risk rules
- Explainable AI signals
- Risk-based decision recommendations
- Transaction history
- Persistent transaction storage
- Risk distribution visualization
- AI risk signal visualization
- Spring Boot and Python AI integration
- REST API based communication
- Defense-only architecture

## ▶️ Running the Project

### 1. Start the Python AI Engine

Navigate to:

ai-service/app

Run:

python app.py

The AI service runs on:

http://localhost:5000

### 2. Start the Spring Boot Backend

Navigate to:

sentinelpay-risk-manager

Run:

mvn spring-boot:run

If Maven is installed separately, use:

& "C:\Program Files\apache-maven-3.9.16\bin\mvn.cmd" spring-boot:run

The backend runs on:

http://localhost:8080

### 3. Open the Frontend

Open:

frontend/index.html

using VS Code Live Server.

The dashboard will be available through the Live Server URL.

Both the Python AI Engine and Spring Boot backend should be running while using the dashboard.

## 🧪 Example Decisions

### Low Risk

Risk Score: 3.67
Risk Level: LOW
Decision: ALLOW

### Medium Risk

Risk Score: 40.0
Risk Level: MEDIUM
Decision: STEP-UP VERIFICATION

### High Risk

Risk Score: 70.0
Risk Level: HIGH
Decision: BLOCK / MANUAL REVIEW

## 🔮 Future Improvements

- Larger and more representative payment datasets
- Model probability calibration
- Further threshold optimization based on business costs
- PostgreSQL for production-scale storage
- Redis-based real-time transaction velocity tracking
- Live network and device risk intelligence
- Continuous model monitoring
- Automated chargeback evidence generation
- Advanced fraud-ring detection
- Model drift detection
- Production authentication and access control
- Real-time alerting and case management
- Cost-sensitive risk decision optimization

## 📌 Project Status

SentinelPay AI Risk Manager is a working AI-powered payment risk management prototype with:

- Python AI fraud detection service
- Random Forest fraud classification
- Isolation Forest anomaly detection
- Behavioural risk rules
- Spring Boot REST backend
- H2 persistent transaction database
- Interactive web dashboard
- Explainable AI risk reasons
- Risk-based action recommendations
- Held-out evaluation on the public ULB fraud detection benchmark

## 👩‍💻 Project

SentinelPay AI Risk Manager

AI-powered payment risk management prototype built for the Razorpay AI Buildathon.