package com.sentinelpay.riskmanager;

import java.util.List;

public class RiskResponse {

    private double riskScore;
    private String riskLevel;
    private double fraudProbability;
    private double anomalyRisk;
    private List<String> reasons;
    private String message;

    public RiskResponse(
            double riskScore,
            String riskLevel,
            double fraudProbability,
            double anomalyRisk,
            List<String> reasons,
            String message) {

        this.riskScore = riskScore;
        this.riskLevel = riskLevel;
        this.fraudProbability = fraudProbability;
        this.anomalyRisk = anomalyRisk;
        this.reasons = reasons;
        this.message = message;
    }

    public double getRiskScore() {
        return riskScore;
    }

    public String getRiskLevel() {
        return riskLevel;
    }

    public double getFraudProbability() {
        return fraudProbability;
    }

    public double getAnomalyRisk() {
        return anomalyRisk;
    }

    public List<String> getReasons() {
        return reasons;
    }

    public String getMessage() {
        return message;
    }
}