package com.pfe.stockmarket.entities;

import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "SocietiesInfo")
public class Society {
    @Id
    private String id;
    private String shortName;
    private String longName;
    private String city, state, country;
    private String exchangeTimezoneName;
    private String currency, quoteType, sector;
    private String fax, phone, website, symbol;
    private String exchange;
    private String industry, logo_url, longBusinessSummary;
    private Long floatShares;
    private Double forwardEps, trailingEps, trailingPE;
    private Double forwardPE;
    private Double pegRatio;
    private Long marketCap;
    private Long enterpriseValue, volume;
    private Double payoutRatio;
    private Long fullTimeEmployees;

    public Society(String id, String symbol) {
        this.id = id;
        this.symbol = symbol;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getShortName() {
        return shortName;
    }

    public void setShortName(String shortName) {
        this.shortName = shortName;
    }

    public String getLongName() {
        return longName;
    }

    public void setLongName(String longName) {
        this.longName = longName;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public String getExchangeTimezoneName() {
        return exchangeTimezoneName;
    }

    public void setExchangeTimezoneName(String exchangeTimezoneName) {
        this.exchangeTimezoneName = exchangeTimezoneName;
    }

    public String getCurrency() {
        return currency;
    }

    public void setCurrency(String currency) {
        this.currency = currency;
    }

    public String getQuoteType() {
        return quoteType;
    }

    public void setQuoteType(String quoteType) {
        this.quoteType = quoteType;
    }

    public String getSector() {
        return sector;
    }

    public void setSector(String sector) {
        this.sector = sector;
    }

    public String getFax() {
        return fax;
    }

    public void setFax(String fax) {
        this.fax = fax;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getWebsite() {
        return website;
    }

    public void setWebsite(String website) {
        this.website = website;
    }

    public String getSymbol() {
        return symbol;
    }

    public void setSymbol(String symbol) {
        this.symbol = symbol;
    }

    public String getExchange() {
        return exchange;
    }

    public void setExchange(String exchange) {
        this.exchange = exchange;
    }

    public String getIndustry() {
        return industry;
    }

    public void setIndustry(String industry) {
        this.industry = industry;
    }

    public String getLogo_url() {
        return logo_url;
    }

    public void setLogo_url(String logo_url) {
        this.logo_url = logo_url;
    }

    public String getLongBusinessSummary() {
        return longBusinessSummary;
    }

    public void setLongBusinessSummary(String longBusinessSummary) {
        this.longBusinessSummary = longBusinessSummary;
    }

    public Long getFloatShares() {
        return floatShares;
    }

    public void setFloatShares(Long floatShares) {
        this.floatShares = floatShares;
    }

    public Double getForwardEps() {
        return forwardEps;
    }

    public void setForwardEps(Double forwardEps) {
        this.forwardEps = forwardEps;
    }

    public Double getTrailingEps() {
        return trailingEps;
    }

    public void setTrailingEps(Double trailingEps) {
        this.trailingEps = trailingEps;
    }

    public Double getTrailingPE() {
        return trailingPE;
    }

    public void setTrailingPE(Double trailingPE) {
        this.trailingPE = trailingPE;
    }

    public Double getForwardPE() {
        return forwardPE;
    }

    public void setForwardPE(Double forwardPE) {
        this.forwardPE = forwardPE;
    }

    public Double getPegRatio() {
        return pegRatio;
    }

    public void setPegRatio(Double pegRatio) {
        this.pegRatio = pegRatio;
    }

    public Long getMarketCap() {
        return marketCap;
    }

    public void setMarketCap(Long marketCap) {
        this.marketCap = marketCap;
    }

    public Long getEnterpriseValue() {
        return enterpriseValue;
    }

    public void setEnterpriseValue(Long enterpriseValue) {
        this.enterpriseValue = enterpriseValue;
    }

    public Long getVolume() {
        return volume;
    }

    public void setVolume(Long volume) {
        this.volume = volume;
    }

    public Double getPayoutRatio() {
        return payoutRatio;
    }

    public void setPayoutRatio(Double payoutRatio) {
        this.payoutRatio = payoutRatio;
    }

    public Long getFullTimeEmployees() {
        return fullTimeEmployees;
    }

    public void setFullTimeEmployees(Long fullTimeEmployees) {
        this.fullTimeEmployees = fullTimeEmployees;
    }
}
