# Vipps Invoice API

This repo contains developer resources for the Vipps Invoice API. For more information about this product, "Vipps Regninger", please see: https://www.vipps.no/bedrift/vipps-regninger

**IMPORTANT:** This is a work in progress. Input is appreciated, either as issues, PRs, email. Pleasde note that the official, stable developer resources for Vipps is still https://vipps.no/developer

Important dates (which _may_ change):
* Feature-complete version without APIM for test: 10th Aug​
* Feature-complete version with APIM for test: ~20th~ 28th Aug (see [issues](https://github.com/vippsas/vipps-invoice-api/issues))
* Feature-complete version with APIM for production: 7th September

See the main GitHub page for Vipps contact information, etc: https://github.com/vippsas  

# API documentation for ISP and IPP

The main API documentaion is [vipps-invoice-api.md](https://github.com/vippsas/vipps-invoice-api/blob/master/vipps-invoice-api.md). This is frequently updated, and issues and PRs are welcome.

## ISP: Invoice Service Provider

Invoice _Service_ Providers: Actors who submit invoices. Either for themselves or on behalf of their clients. 

* https://vippsas.github.io/vipps-invoice-api/isp.html
* https://vippsas.github.io/vipps-invoice-api/redoc-isp.html

## IPP: Invoice Payment Provider

Invoice _Payment_ Providers: Actors who handle invoices for the invoice recipients and execute payments, e.g. banks, the Vipps app.

* https://vippsas.github.io/vipps-invoice-api/ipp.html
* https://vippsas.github.io/vipps-invoice-api/redoc-ipp.html
