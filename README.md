# Vipps Invoice API

This repository contains developer resources for the Vipps Invoice API.
For more information, see [Vipps Regninger](https://www.vipps.no/bedrift/vipps-regninger).

**IMPORTANT:** This is a work in progress. Input is appreciated, either as issues, PRs, email.
Please note that the official, stable developer resources for Vipps is still https://vipps.no/developer

Important dates (which _may_ change):
* Feature-complete version without APIM for test: 10th Aug​
* Feature-complete version with APIM for test: ~20th~ 28th Aug (see [issues](https://github.com/vippsas/vipps-invoice-api/issues))
* Feature-complete version _of the API_ with APIM authentication for production: ~7th~ 12th September
* Production access for integrators: September 13
* Vipps Regninger visible in the Vipps app: September 27 (for whitelisted users)

For the full rolout plan: Please contact us.

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

# Swagger changelog

## 0.3.19

* `vippsinvoice-recipienttoken`: Valid for 15 minutes.

## 0.3.18

* `invoiceId` regex: `^([a-zA-Z-])\\.(\\d).([a-zA-Z0-9-]+)$`

## 0.3.17

* ISP: Remove requirement for recipient token on GetInvoiceByID

## 0.3.16

* Add info about logo requirements

## 0.3.15

* Correction of the HTTP statuscode of status changes

## 0.3.14

* Added recipient token to get invoice, get commercial invoice and get attachment.

## 0.3.13

* Added validation info on invoiceId and urls.

## 0.3.12

* Added validation info to description of `due`

## 0.3.11

* Added `HTTP 401` to all operations and specify API-M specific error response

## 0.3.10

* Clarification: Added 'problems' to invoice status and `HTTP 403` for create invoice

## 0.3.9

* Added `providerId` to `invoiceOut`.

## 0.3.8

* Removed URL to commercial invoice in `invoiceOut`.

## 0.3.7

* Corrected `state` for invoices in Swagger: `[pending, approved, deleted, created, rejected, expired, revoked]
* Bugfix: ISPs can now fetch their own invoices

## 0.3.6

* `HTTP 429 Too Many Requests` added to endpoints.

## 0.3.5

* Version number bimp to make ISP and IPP juse the same.

## 0.3.4

* Bugfix: ISPs are only allowed to fetch their own invoices
* Bugfix: Resolving recipients with MSISDN now works (MSISDN is now required)
* Bugfix: `/invoices/count` returns the correct number of invoices
* Bugfix: Authorization to revoke invoice is properly parsed

## 0.3.3

* Moved verbose documentation out of Swagger files

## 0.3.2

* Improved `HTTP 409` description for `PUT:/invoice/{invoiceId}`

## 0.3.1

* Added `/jwk` (again).

## 0.3.0

* Updated authentication info for APIM (manual "merge").

## 0.2.28

* Fix: Replaced `new` with `created`, also for endpoints not implemented yet.

## 0.2.27

* Fix: Replaced `new` with `created`.

## 0.2.26

* Updated information about test users.

## 0.2.25

* Replaced introduction text with link to documentation.

## 0.2.24

* * Corrected documentation of `state` for invoices, and some minor text tweaks.

## 0.2.23

* Improved documentation for `invoiceId`.

## 0.2.22

* Fix: The token returned from `GET:/recipients/tokens` is now returned
as a proper JSON document with the field `recipientToken`
* Extended the datamodel for errors. Error returned by the API will now
include the required fields `type` and `title` plus the optional fields
`detail` and `instance`. The content of the field is according to
[RFC7807](https://tools.ietf.org/html/rfc7807)
