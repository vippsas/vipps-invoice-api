# Vipps Invoice API

This repository contains developer resources for the Vipps Invoice API.
For more information, see [Vipps eFaktura](https://www.vipps.no/produkter-og-tjenester/bedrift/send-regninger/send-regninger/).

See the Vipps Developers repository for
a "getting started" guide,
information about product activation,
contact information,
contribution guidelines,
etc:
https://github.com/vippsas/vipps-developers  

# API documentation for ISP and IPP

The main API documentaion is [vipps-invoice-api.md](https://github.com/vippsas/vipps-invoice-api/blob/master/vipps-invoice-api.md). This is [frequently updated](https://github.com/vippsas/vipps-invoice-api/commits/master/vipps-invoice-api.md), and issues and PRs are welcome.

## Test users

This test user can receive invoices, and approve, etc:
Payment of invoices, both for Vipps Regninger and Vipps Faktura is not possible yet.

| customerId | NIN (fødselsnummer) | MSISDN (phone number) | First name | Last name | Owner |
| ---------- | ------------------- | --------------------- | ---------- | --------- | ----- |
| 10003301	 | 01032300371         | 4797777776            | Willhelm Fos | Kluvstad | Common |

## Test issuers

The service validates that the account belongs to the issuer ([KAR](https://www.finansnorge.no/aktuelt/presentasjoner/bankenes-felles-konto--og-adresseregister-kar/)). Make sure that that you use a valid pair when testing.

| Name               | Org. number | Account number |
| ------------------ |------------ | -------------- |
| Vipps Teknologi AS | 918130047   | 15038366383    |

## ISP: Invoice Service Provider

Invoice _Service_ Providers: Actors who submit invoices. Either for themselves or on behalf of their clients.

* https://vippsas.github.io/vipps-invoice-api/isp.html
* https://vippsas.github.io/vipps-invoice-api/redoc-isp.html

## IPP: Invoice Payment Provider

Invoice _Payment_ Providers: Actors who handle invoices for the invoice recipients and execute payments, e.g. banks, the Vipps app.

* https://vippsas.github.io/vipps-invoice-api/ipp.html
* https://vippsas.github.io/vipps-invoice-api/redoc-ipp.html

# Building JSON files

After updating the YAML files you can convert them to JSON by running the `yaml2json.py` script.
If you do not have the `pyyaml` dependency installed you can either do this with a package manager or
install it using `pip`.

```pip install -r requirements.txt # Will install all requirements```

# Banks that can be used as a valid payment source in the Vipps app
- These are the banks that can be used to **pay invoies in the app**.
- A bank not mentioned on the list below will still be a place where a debtor can pay the invoice.

|Bank|Bank|
|---|---|
|BN Bank|Bulder Bank|
|DNB|Etne Sparebank|
|Fana Sparebank|Flekkefjord Sparebank|
|Handelsbanken|Haugesund Sparebank|
|Helgeland Sparebank|KLP Banken|
|Lillesands Sparebank|Luster Sparebank|
|OBOS-banken|Sbanken|
|Skudenes og Aakra Sparebank|SpareBank 1 BV|
|SpareBank 1 Gudbrandsdal|SpareBank 1 Hallingdal Valdres|
|SpareBank 1 Lom og Skjåk|SpareBank 1 Modum|
|SpareBank 1 Nord-Norge|SpareBank 1 Nordvest|
|SpareBank 1 Ringerike Hadeland|SpareBank 1 SMN|
|SpareBank 1 SR-Bank|SpareBank 1 Søre Sunnmøre|
|SpareBank 1 Telemark|SpareBank 1 Østfold Akershus|
|SpareBank 1 Østlandet|Sparebanken Møre|
|Sparebanken Sogn og Fjordane|Sparebanken Sør|
|Sparebanken Vest|Sparebanken Øst|
|Spareskillingsbanken|Søgne og Greipstad Sparebank|
|Voss Sparebank|

## Changes
### 05.11.2019 
- Updated information about when recipient token is issued
- Removed `expired` status from documentation as it's no longer used.

## Swagger Changelog
[Swagger changelog](SwaggerChangelog.md)