# SentinelPay AI Risk Manager

AI-powered real-time transaction fraud and anomaly detection system built for the Razorpay AI Buildathon.

## 🚀 Overview

SentinelPay AI Risk Manager is an AI-driven payment risk analysis platform designed to detect suspicious and abnormal transactions in real time.

The system combines supervised fraud classification and unsupervised anomaly detection to generate a risk score, identify the risk level, explain the reasons behind the decision, and recommend an appropriate action.

## 🎯 Problem Statement

Digital payment platforms process a large number of transactions every day. Detecting fraudulent or abnormal transactions quickly is important to reduce financial losses while avoiding unnecessary blocking of genuine customers.

SentinelPay addresses this problem by analysing transaction behaviour and generating an explainable risk assessment.

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
- Network risk

The AI engine produces:

- Risk Score
- Fraud Probability
- Anomaly Risk
- Risk Level
- Explainable AI Reasons
- Recommended Action

## 🤖 AI Approach

### Random Forest

Random Forest is used as the supervised fraud classification model.

It estimates the probability that a transaction may be fraudulent based on transaction and behavioural features.

### Isolation Forest

Isolation Forest is used for anomaly detection.

It identifies transactions that behave differently from normal transaction patterns, including unusual combinations of behavioural signals.

### Combined Risk Score

The final risk score combines the outputs of both models:

Final Risk Score = (Fraud Probability × 75%) + (Anomaly Risk × 25%)

### Risk Classification

- LOW: 0–39.9
- MEDIUM: 40–69.9
- HIGH: 70–100

## 🔍 Explainable AI

For every analysed transaction, SentinelPay provides human-readable reasons behind the risk decision.

Example signals include:

- Transaction amount significantly higher than normal
- Unusually high transaction velocity
- New or changed device
- Location differs from normal behaviour
- Multiple failed transaction attempts
- New beneficiary detected
- Unusual transaction hour
- AI anomaly detector identified unusual behaviour

## 🏗️ System Architecture

mermaid
flowchart LR
    U[User / Merchant] --> F[Web Dashboard]
    F -->|POST /risk-check| B[Spring Boot REST API - Port 8080]
    B -->|HTTP JSON /predict| A[Python AI Engine - Flask Port 5000]

    A --> RF[Random Forest - Fraud Probability]
    A --> IF[Isolation Forest - Anomaly Risk]

    RF --> S[Combined Risk Score]
    IF --> S

    S --> C{Risk Classification}
    C -->|LOW| AL[ALLOW]
    C -->|MEDIUM| ST[STEP-UP VERIFICATION]
    C -->|HIGH| BL[BLOCK / MANUAL REVIEW]

    A -->|AI Reasons + Risk Result| B
    B --> DB[(H2 Database)]
    B --> RESP[JSON Risk Response]
    RESP --> F
    DB -->|GET /transactions| F


## 🛠️ Technology Stack
### Frontend

- HTML
- CSS
- JavaScript
- Chart.js

### Backend

- Java
- Spring Boot
- Spring Data JPA
- REST APIs

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

## 📂 Project Structure

sentinelpay-risk-manager/
│
├── README.md
│
├── ai-service/
│   └── App/
│       ├── App.py
│       ├── ai_risk_model.py
│       └── fraud_model.pkl
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
Spring Boot API
↓
Python AI Engine
↓
Random Forest
+
Isolation Forest
↓
Risk Score Generation
↓
Risk Classification
↓
Explainable AI Reasons
↓
Recommended Action
↓
Transaction Stored in Database
↓
Dashboard Updated

## ⚡ Risk-Based Actions

| Risk Level | Score | Recommended Action |
|------------|-------|--------------------|
| LOW | 0–39.9 | ALLOW |
| MEDIUM | 40–69.9 | STEP-UP VERIFICATION |
| HIGH | 70–100 | BLOCK / MANUAL REVIEW |

## 📊 Prototype Evaluation

The current prototype was evaluated using a small synthetic transaction dataset.

The prototype evaluation produced the following results:

- Precision: 1.00
- Recall: 1.00
- F1 Score: 1.00
- ROC-AUC: 1.00

These results are prototype-level results from synthetic data and should not be interpreted as production performance.

A larger and representative real-world dataset would be required for production validation.

## 🛡️ Defense-Only Design

SentinelPay is designed strictly for defensive fraud and anomaly detection.

It does not provide instructions for bypassing payment security systems or committing financial fraud.

## 🌟 Key Features

- Real-time transaction risk analysis
- Fraud probability prediction
- Anomaly detection
- Explainable AI signals
- Risk-based decision recommendations
- Transaction history
- Risk distribution visualization
- AI risk signal visualization
- Spring Boot and Python AI integration
- Persistent transaction storage

## ▶️ Running the Project

### 1. Start the Python AI Engine

Navigate to:

ai-service/App

Run:

python App.py

The AI service runs on:

http://localhost:5000

### 2. Start the Spring Boot Backend

Navigate to:

sentinelpay-risk-manager

Run:

mvn spring-boot:run

The backend runs on:

http://localhost:8080

### 3. Open the Frontend

Open:

frontend/index.html

using VS Code Live Server.

The dashboard will be available through the Live Server URL.

## 🧪 Example Decisions

### Low Risk

Risk Score: 11.1

Risk Level: LOW

Decision: ALLOW

### Medium Risk

Risk Level: MEDIUM

Decision: STEP-UP VERIFICATION

### High Risk

Risk Score: 100.0

Risk Level: HIGH

Decision: BLOCK / MANUAL REVIEW

## 🔮 Future Improvements

- Larger real-world fraud datasets
- Model calibration and threshold optimization
- PostgreSQL for production-scale storage
- Redis-based real-time velocity tracking
- Continuous model monitoring
- Automated chargeback evidence generation
- Advanced fraud-ring detection
- Model drift detection
- Production authentication and access control

## 👩‍💻 Project

SentinelPay AI Risk Manager

AI-powered payment risk management prototype built for the Razorpay AI Buildathon.4
