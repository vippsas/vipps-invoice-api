# Swagger changelog

## 0.3.44

* Added note about state `expired` being deprecated.

## 0.3.43

* InvoiceOut: Add new field externalReference

## 0.3.42

* Added information in the issuerIconUrl description: Issuer logo is not yet supported. 

## 0.3.41

* ISP - Validation of due: Must be minimum 3 days in the future

## 0.3.40

* IPP: Add optional details about bankCode in set status to delete or pending

## 0.3.39
* Add field `scope` to `invoiceOut` model. The value is either `vipps` or `nets`
  and indicates if the invoice was originally sent as Vipps Regning or eFaktura.
  The field may be used to filter the returned list of invoices.

## 0.3.38
* Changed name from "Vipps Regninger" to "Vipps eFaktura"

## 0.3.37

* Removed statuses endpoints

## 0.3.36

* Change error type on status to match implementation

## 0.3.35

* add error type to recipient token not found response

## 0.3.34

* Added `maxLength: 40` for `issuerName`.

## 0.3.33

* ISP: Added details about `issuerIconUrl`.
* IPP: "Version number equality"

## 0.3.32

## 0.3.31

* ISP: Make Commercial invoice mandatory in create invoice

## 0.3.30

* IPP: Allow empty mime-type in get commercial invoice url and select the most suitable mime-type from the invoice

## 0.3.29

* Add an optional field bankCode to approve invoice

## 0.3.28

* Additional information on minAmount.

## 0.3.27

* fix JWK endpoint

## 0.3.26

* Added: `/public/jwk`. Deprecated: `/jwk`.

## 0.3.25

* Add details on mime-type validation for attachments

## 0.3.24

* Use correct error types

## 0.3.23

* Correct error in mimeType-definition

## 0.3.22

* fix validation errors for error/problem type

## 0.3.21

* update JWK with x5t and kid details

## 0.3.20

* Mark all endpoints as finished, add etag on invoice and fix regex

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
