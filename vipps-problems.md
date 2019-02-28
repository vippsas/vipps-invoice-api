# Problems

Base URL: `https://vipps.no/invoice/v1/problems`

This is a list of all errors that can occure when sending an invoice, with respectively error messages and details. 

| Type | Title | Detail |
|------|-------|--------|
|`/invalid-issuer-name` | Issuer name must contain between 1 and 40 characters | See documentation for list of valid characters. |
| `/invalid-due-date` | Invalid due time | Must be between at least 48 hours into the future and at most one year into the future. |
| `/input-validation-failed` | Validation of input failed. | 1 validation error(s) occurred. Account must be a valid numeric value |
| `/input-validation-failed` | Validation of input failed | 1 validation error(s) occurred. MinAmount must be less than or equal to Amount |
|`/invalid-json` | Invalid JSON | |
|`/missing-recipient-token`| Recipient token is missing | |
|`/missing-header-if-match`| Missing Header: If-Match ||
|`/missing-header-idempotency-key`| Missing Header: Idempotency-Key ||
|`/missing-invoice-id`| Missing invoice id ||
|`/invalid-recipient-token`| Invalid recipient token ||
|`/recipient-token-expired`| Recipient token expired ||
|`/recipient-token-claims`| failed to get claims ||
|`/parsing-recipient-token`| failed to parse recipient token subject ||
|`/unknown-ident-type`| Invalid identification type while resolving a recipient. Make sure that a valid type is used. ||
|`/invalid-recipient-value-msisdn`| Invalid MSISDN in recipient value. Make sure that a valid MSISDN is used. ||
|`/invalid-recipient-value-nin`| Invalid NIN in recipient value. Make sure that a valid NIN is used. ||
|`/invalid-payment-information-type`| Payment information type is invalid ||
|`/invalid-payment-information-kid`| Invalid KID number in payment information. Check MOD10 and/or MOD11. ||
|`/missing-payment-information-message`| The field 'value' is missing from payment information ||
|`/invalid-payment-information-account`| Invalid payment information account ||
|`/invalid-invoice-type`| Invalid invoice type ||
|`/invalid-invoice-id-length`| The invoice ID cannot be more than 200 ascii characters (bytes). ||
|`/invalid-invoice-id-format`| Invalid invoice id format | The invoice ID should have the following format: {IssuerIdentType}.{IssuerIdentValue}.{InvoiceRef} |
|`/invalid-invoice-id-issuer-ident-type`| Invalid issuer ident type in invoiceId | Issuer ident type must be one of the following: [orgno-no] |
|`/invalid-invoice-id-reference-value`| Invalid invoice reference | The invoice reference in the invoice ID should only contain valid characters |
|`/invalid-due-date`| Invalid due time | Must be between today at midnight and at most one year into the future. |
|`/invalid-min-amount`| Invalid minAmount | MinAmount must be less or equal to amount. |
|`/amount-negative`| Amount is a negative amount ||
|`/missing-subject`| Missing invoice subject ||
|`/invalid-commercial-invoice-url`| Invalid commercial invoice URL ||
|`/invalid-commercial-invoice-mimetype`| Invalid commercial invoice mime type | See documentation for list of valid types. |
|`/issuer-blacklisted`| The issuer of the invoice is blacklisted ||
|`/recipient-blacklisted`| The recipient of the invoice is blacklisted ||
|`/recipient-not-whitelisted`| The recipient of the invoice is not on whitelist ||
|`/invalid-issuer-icon-url`| Invalid issuer icon Url | |
|`/unresolved-error`| Unresolved error ||
|`/invalid-invoice-status`| Invalid invoice status ||
|`/missing-mimetype`| MimeType is missing ||
|`/not-found`| Not found ||
|`/commercial-invoice-format-not-found`| Specified format was not found ||
|`/token-generation-failed`| Token generation failed ||
|`/missing-invoice-attachment-id`| AttachmentId is missing ||
|`/missing-internal-authentication`| Missing internal authentication ||
|`/invalid-authorization-token`| Invalid or missing Authorization token ||
|`/internal-server-error`| Internal server error ||
|`/status-change-createdby-mismatch`| Not allowed | You are not allowed to perform the requested state transition. The state can only be changed by the user who set the state. |
|`/invoice-status-issuer-only`| Only allowed for invoice creator ||
|`/invoice-operation-unauthorized`| Operation unauthorized ||
|`/reading-request-body`| Error reading the request body ||
|`/creating-jwk`| Could not create a JWK ||
|`/forbidden`| Forbidden||
|`/invalid-account-owner`| Account does not belong to organisation or is not primary account ||
|`/timeout`| Resource timeout | The request timed out. It is safe to try again. |
|`/marshal-json-failed`| Marshalling JSON failed ||
|`/duplicate-query-param`| Duplicate query parameter | A query parameter which is only allowed exactly once has been provided multiple times. |
|`/missing-query-param-from`| Missing query parameter | The query parameter \"from\" (in RFC3339 format) is missing and required. |
|`/from-parameter-too-far-back-in-time`| The from query parameter is too far back in time | We currently only support searching up to 30 days back in time. |
|`/metadata-key-value-length-mismatch`| Arrays in query params must have same length | The arrays of the query parameters metadataKeys and metadataValues must have the same length. |
|`/recipient-not-found`| Recipient not found | No recipient with identType %s and identValue %s could be found. |
|`/invoice-not-found`| Invoice not found | No invoice with id %s could be found. |
|`/invoice-conflict`| Invoice conflict | A different invoice with the id %s already exists, but with different content. |
|`/invoice-status-conflict`| Invoice status conflict | A different invoice status with the same idempotencyKey %s already exists, but with different content. |
|`/invoice-status-etag-mismatch`| Invoice status etag mismatch | The etag of the underlying status for invoice with id %s changed. The status may have changed. |
|`/state-transition-not-allowed`| State transition not allowed | State transition from "%s" to "%s" is not allowed. |
|`/invalid-invoice-id-issuer-ident-value`| Invalid issuer ident value in invoice id ||
|`/input-validation-failed`| Validation of input failed | %d validation error(s) occurred. %s |
|`/RFC3339-parse-error`| Error parsing input as RFC3339 | Could not parse %s as RFC3339. Make sure the format is correct. Example %s |
