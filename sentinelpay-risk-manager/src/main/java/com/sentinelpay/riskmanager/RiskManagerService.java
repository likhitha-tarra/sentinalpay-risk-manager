package com.sentinelpay.riskmanager;

import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.time.LocalDateTime;

@Service
public class RiskManagerService {

    private final RestClient restClient;
    private final TransactionRepository transactionRepository;

    public RiskManagerService(TransactionRepository transactionRepository) {

        this.transactionRepository = transactionRepository;

        this.restClient = RestClient.builder()
                .baseUrl("http://localhost:5000")
                .build();
    }

    public RiskResponse calculateRisk(RiskRequest request) {

        // ==========================================
        // SEND TRANSACTION TO AI RISK ENGINE
        // ==========================================

        RiskResponse response = restClient.post()
                .uri("/predict")
                .contentType(MediaType.APPLICATION_JSON)
                .body(request)
                .retrieve()
                .body(RiskResponse.class);


        // ==========================================
        // SAVE AI RESULT TO DATABASE
        // ==========================================

        if (response != null) {

            Transaction transaction = new Transaction();

            transaction.setAmount(request.getAmount());
            transaction.setMerchant(request.getMerchant());
            transaction.setTransactionType(
                    request.getTransactionType()
            );
            transaction.setPaymentMethod(
                    request.getPaymentMethod()
            );
            transaction.setCurrency(
                    request.getCurrency()
            );
            transaction.setLocation(
                    request.getLocation()
            );

            transaction.setRiskScore(
                    response.getRiskScore()
            );

            transaction.setRiskLevel(
                    response.getRiskLevel()
            );

            transaction.setFraudProbability(
                    response.getFraudProbability()
            );


            // Determine transaction decision

            String decision;

            if (response.getRiskScore() >= 70) {

                decision = "BLOCK";

            } else if (response.getRiskScore() >= 40) {

                decision = "STEP-UP VERIFICATION";

            } else {

                decision = "ALLOW";
            }

            transaction.setDecision(decision);

            transaction.setAnalyzedAt(
                    LocalDateTime.now()
            );


            // Save transaction

            transactionRepository.save(transaction);
        }


        return response;
    }
}