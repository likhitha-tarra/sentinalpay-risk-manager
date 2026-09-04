# SentinelPay AI Risk Manager — System Architecture

```mermaid
flowchart LR

    U[User / Merchant] --> F[Web Dashboard<br/>HTML CSS JavaScript Chart.js]

    F -->|POST /risk-check| B[Spring Boot REST API<br/>Port 8080]

    B -->|HTTP JSON /predict| A[Python AI Engine<br/>Flask Port 5000]

    A --> RF[Random Forest<br/>Fraud Probability]
    A --> IF[Isolation Forest<br/>Anomaly Risk]

    RF --> S[Combined Risk Score<br/>75% Fraud + 25% Anomaly]
    IF --> S

    S --> C{Risk Classification}

    C -->|LOW| L[ALLOW]
    C -->|MEDIUM| M[STEP-UP VERIFICATION]
    C -->|HIGH| H[BLOCK / MANUAL REVIEW]

    S --> R[Explainable AI Reasons]

    R --> B

    B --> DB[(H2 Database)]

    B --> RESP[JSON Risk Response]
    RESP --> F

    DB -->|GET /transactions| F