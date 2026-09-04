package com.sentinelpay.riskmanager;

public class RiskRequest {

    private double amount;
    private String location;
    private int transactionCount;
    private String merchant;
    private String merchantCategory;
    private String transactionType;
    private String paymentMethod;
    private String currency;
    private int networkRisk;

    private double customerAvgAmount;
    private int deviceChanged;
    private int locationChanged;
    private int failedAttempts;
    private int newBeneficiary;
    private int hour;

    public double getAmount() {
        return amount;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public int getTransactionCount() {
        return transactionCount;
    }

    public void setTransactionCount(int transactionCount) {
        this.transactionCount = transactionCount;
    }

    public String getMerchant() {
        return merchant;
    }

    public void setMerchant(String merchant) {
        this.merchant = merchant;
    }

    public String getMerchantCategory() {
        return merchantCategory;
    }

    public void setMerchantCategory(String merchantCategory) {
        this.merchantCategory = merchantCategory;
    }

    public String getTransactionType() {
        return transactionType;
    }

    public void setTransactionType(String transactionType) {
        this.transactionType = transactionType;
    }

    public String getPaymentMethod() {
        return paymentMethod;
    }

    public void setPaymentMethod(String paymentMethod) {
        this.paymentMethod = paymentMethod;
    }

    public String getCurrency() {
        return currency;
    }

    public void setCurrency(String currency) {
        this.currency = currency;
    }

    public int getNetworkRisk() {
        return networkRisk;
    }

    public void setNetworkRisk(int networkRisk) {
        this.networkRisk = networkRisk;
    }

    public double getCustomerAvgAmount() {
        return customerAvgAmount;
    }

    public void setCustomerAvgAmount(double customerAvgAmount) {
        this.customerAvgAmount = customerAvgAmount;
    }

    public int getDeviceChanged() {
        return deviceChanged;
    }

    public void setDeviceChanged(int deviceChanged) {
        this.deviceChanged = deviceChanged;
    }

    public int getLocationChanged() {
        return locationChanged;
    }

    public void setLocationChanged(int locationChanged) {
        this.locationChanged = locationChanged;
    }

    public int getFailedAttempts() {
        return failedAttempts;
    }

    public void setFailedAttempts(int failedAttempts) {
        this.failedAttempts = failedAttempts;
    }

    public int getNewBeneficiary() {
        return newBeneficiary;
    }

    public void setNewBeneficiary(int newBeneficiary) {
        this.newBeneficiary = newBeneficiary;
    }

    public int getHour() {
        return hour;
    }

    public void setHour(int hour) {
        this.hour = hour;
    }
}