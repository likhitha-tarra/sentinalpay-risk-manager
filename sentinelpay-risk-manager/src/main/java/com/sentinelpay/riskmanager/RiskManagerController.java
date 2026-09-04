package com.sentinelpay.riskmanager;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@CrossOrigin(origins = "*")
public class RiskManagerController {

    private final RiskManagerService riskManagerService;

    public RiskManagerController(RiskManagerService riskManagerService) {
        this.riskManagerService = riskManagerService;
    }

    @GetMapping("/")
    public String home() {
        return "SentinelPay Risk Manager is Running Successfully!";
    }

    @PostMapping("/risk-check")
    public RiskResponse checkRisk(@RequestBody RiskRequest request) {
        return riskManagerService.calculateRisk(request);
    }
}