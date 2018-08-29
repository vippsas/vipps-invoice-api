# Vipps Invoice API

This is the API for **Vipps Regninger**: https://www.vipps.no/bedrift/vipps-regninger

Please note that Vipps Regninger supersedes the older Vipps Faktura,
both as a product and API.

Status: While we have worked closely with selected partners, and believe that this is
_very_ close to production quality, we are more than happy to receive feedback,
either with GitHub's issue functionality, or by email to integration@vipps.no.

Document version: 0.1.5.

## Technical API documentation

Swagger/OAS API documentation is available on GitHub: https://github.com/vippsas/vipps-invoice-api

## Terminology: ISP and IPP

Throughout this specification we use the terms ISP and IPP to categorize two
groups of users:

* ISP, the invoice _service_ providers, are all actors who submit invoices.
Either for themselves or on behalf of their clients.

* IPP, the invoice _payment_ providers, are all actors who handle invoices
for the invoice recipients and execute payments, e.g. banks, the Vipps
app.

# Core functionality

## Send, receive and pay invoices

"Vipps Regninger" replaces the batch processing in "Vipps Faktura" with
a more speedy per-invoice processing, with improved status and progress for
each individual invoice. This means that invoices have to be posted one by one,
each invoice in a separate HTTP call.

Although it may at first seem to be an inefficient approach, we believe that
the benefits far outweigh performance considerations. In addition, our
tests have shown that, if multiple threads are used to push invoices to our
system, the performance is well on par with a batch approach.

The main benefits are that it becomes much easier to ensure and verify
idempotency of the endpoint. We insert the received invoices _synchronously_. In
case of problems (such as `HTTP 5XX` return codes or network issues), it is possible to
simply repeatedly submit invoices until a `HTTP 2XX` status code is returned. We
guarantee that any invoice is inserted exactly once.

## Invoice validation

The validation of the invoice will still be an asynchronous process since we
have no possibility to guarantee, or even estimate ,the response times for
all required validation and risk check to be performed.

Therefore, the invoice will be in a `pending` state once it is inserted.
In this state the invoice will not be visible to anyone. Only after all
validation steps are passed, will the invoice will be shown to the recipients.
ISPs who provide the invoice will have to monitor the state. We provide two
ways to do that.

## Managing and paying invoices

IPPs will mainly use the `/invoices` resources directly. The typical use case
will be to fetch all invoices for a recipient (user), identified by a national
identification number. This is provided by
[`GET:/invoices`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/get_invoices).

If a user approves an invoice, the payment provider has to mark this
individual invoice as processed so that the invoice is not displayed as an
open invoice in other services.

## Debt collection

All invoices contain information about the _invoice type_, i.e. whether it
is a regular invoice, reminder or other. This enables payment providers to
filter the allowed payment methods according to Norwegian debt collection laws.

# Invoice states

| # | State | Description |
|---|------|-------------|
| 1 | `created` | Invoice has been inserted, but not yet validated, and not yet shown to the recipient |
| 2 | `rejected` | Invoice could not be validated, and is rejected |
| 3 | `pending` | Invoice needs to be processed by the recipient |
| 4 | `expired` | Recipient did not process the invoice in time |
| 5 | `approved` | Invoice has been approved by recipient |
| 6 | `deleted` | Invoice has been deleted |
| 7 | `revoked` | Invoice has been revoked by the ISP |

# Authentication and authorization

Vipps has to ensure compliance with governing regulations, including GDPR
compliance. This means we have to make sure that Vipps:

* Does not provide information about client, explicitely or implicitely to unauthorised entities.
* Does not store information accidentally received, which we are not authorised to see.
* Propagate changes quickly if a user opts out or in to receive Vipps invoice.
* Do not store personal information, i.e. invoices, which we do not have the right to see.
* Minimize the time we have any unauthorized data; i.e. we have to delete invoices we cannot resolve.

To submit an invoice to our system, the client first has to obtain a _recipient token_
by issuing a `POST` request to `/recipients/tokens`. This token can then be used
in the request body to `PUT` an invoice to `/invoices`.

To ensure GDPR compliance, the token has a limited time to live, currently _15
minutes_. Until it's expiry, clients are free to cache the token and reuse it to
submit several invoices to the same recipient.

## Example 1: Send Invoice

| Step | Method | Endpoint | Description |
|------|--------|----------|-------------|
| 1	   | `POST` | `/recipients/tokens` | The call will resolve the provided personal data and return a `recipientToken` if the recipient could be resolved. This token is used in the subsequent call. |
| 2	   | `PUT`  | `/invoices/{invoiceId}` | The previously obtained `recipientToken` is used in the request body to identify the recipient. |

See [`POST://recipients/tokens`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/post_recipients_tokens)
and [`PUT:/invoices/{invoiceId}`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/put_invoices__invoiceId_).

The URL sent when creating an invoice should be valid as long as possible (more than 12 months is good).
The validity will be controlled with the JWT appended. The flow is the following:

1. An invoice is sent, containing the "commercial invoice" with an URL like http://invoicehotel.example.org/093891280/091238912830.pdf

2. Some time later, the end user clicks on "show invoice" in the app. The
[`GET:/invoices`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/get_invoices)
request (see below) returns a response with the URL with a JWT appended.
The returned URL would be something like `http://invoicehotel.example.org/093891280/091238912830.pdf?token=[jwt token]`.

The JWT-token will contain an expiry timestamp that should be validated by the invoice hotel.

## Example 2: Fetch Invoices for Recipient

| Step | Method | Endpoint | Description |
|------|--------|----------|-------------|
| 1	   | `POST` | `/recipients/tokens` | The call will resolve the provided personal data and return a `recipientToken` if the recipient could be resolved. This token is used in the subsequent call. |
| 2	   | `GET`  | `/invoices` | The previously obtained `recipientToken` is used as a header to fetch all invoices for the recipient. |

See [`POST://recipients/tokens`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/post_recipients_tokens)
and [`GET:/invoices`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/get_invoices).

## National identity number, or MSISDN, not available

Vipps requires either national identity number or MSISDN for
[`POST://recipients/tokens`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/post_recipients_tokens).

# Retrieving invoice documents (attachments)

Invoice documents may be additional invoice documentation,
such as commercial invoices and attachments.

The IPP should retrieve the *actual* document download URL on demand on
behalf of its user. This is typically initiated when the user clicks on a
download link in a UI. The user's request should first be made to a backend
system that in turn makes the authenticated request to this API to retrieve
the *time-limited* URL to the actual document.

The URL contains a *JWT* query parameter that is validated by the ISP.
The expiry time (i.e. TTL) is inside the JWT.

Each invoice document has one or more MIME types. This means that
[`GET:/invoices/{invoiceId}/attachments/{attachmentId}`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/get_invoices__invoiceId__attachments__attachmentId_)
must include the `mimeType` query parameter that specifies the mime type to
retrieve, i.e. document file type. The MIME type is available to the IPP when
listing all the documents, so it is not necessary to guess.

PDF is a commonly used MIME type, which can be displayed in most contexts.

There is currently no limitation to the length of the URL.

## Validating the JWT and the request

The IPP is responsible for validating the JWT. The JWT contains the
following relevant claims:

* `ISS` (issuer): Who is issuing the JWT. Typically `vipps-invoice-api`.
* `AUD` (audience): Something identifying the IPP.
* `SUB` (subject): The base URL for the document.
* `EXP` (expiration): A specific moment in time where the JWT becomes invalid.
* `ALG` (algorithm): Encryption algorithm. Vipps will use **RS256**.

The API's public key is required in order to validate the request. The public
key is available as JSON Web Key (JWK) under the
[`GET:/jwk`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/get_jwk)
endpoint. It is suggested to Use a JWK library to parse and use the key.

In addition to validating the JWT, the IPP/invoice hotel must ensure to
validate the following:

* The expired timestamp is in the future. i.e. not expired.

* Make sure that the URL is valid. One approach is to return the `SUB` and
ignore the actual path.

For details on JWT, use the [RFC](https://tools.ietf.org/html/rfc7519) or
[jwt.io](https://www.jwt.io). The latter contains a list of pre-made
libraries. We **highly** recommend using a pre-made library. It should at
the very least validate the expiry time.


# Detailed information about invoice states and transitions

![Invoice states](images/invoice-states.png)

## State transitions

| # | From       | To         | Description |
|---|------------|------------|-------------|
| 1 | `created`  | `pending`  | Successfully validated |
| 2 |            | `rejected` | Validation failed|
| 3 |            | `revoked`  | The invoice has been deleted by the ISP |
| - | `rejected` | --         | Final state |
| 4 | `pending`  | `expired`  | After grace period, the invoice cannot be modified |
| 5 |            | `deleted`  | The recipient deleted the invoice |
| 6 |            | `approved` | The recipient approved invoice and payment is scheduled |
| 7 |            | `revoked`  | The invoice has been deleted by the ISP |
| - | `expired`  | --         | Final state |
| 8 | `approved` | `approved` | The recipient has updated the payment details |
| 9 |            | `pending`  | The recipient has stopped the payment |
| 10 |           | `deleted`  | Virtual transition composed of 9 + 5 |
| - | `deleted`  | --         | Final state |
| - | `revoked`  | --         | Final state |

## Detailed state descriptions

### State 1: Created

The start state of an invoice is `created`. Invoices we receive are directly
inserted into the database with only minimal validation performed on the provided
request body.

This way, we decouple the ingestion from the actual validation and can keep the
workload on the ingesting endpoints low so that we can achieve fast response
times.

The actual validation will potentially include many calls to external services
where we cannot make any guarantees about response times. So we need this async
approach.

#### Transitions

##### Transitions 1, 2: `created` -> `pending`, `rejected`
The state transition from the initial state `created` is performed internally.
Once an invoice is inserted into our system it will be picked up by a worker
which validates the invoice and updates the status to either `rejected` or
`pending` depending on the validation result.

##### Transition 3: `created` -> `revoked`
An ISP can revoke an invoice by calling
[`PUT:/invoices/{id}/status/{revoked}`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/put_invoices__invoiceId__status_revoked)
(this endpoint is not yet in the API documentation).
It could also be a `DELETE`, but then we have to distinguish a `DELETE` , hence we decided to use `PUT` verbs consistently.

### State 2: Rejected

If the validation has failed, the invoice ends up in the `rejected` state. This is
an end state and means that the invoice was not accepted into our system and is
never shown to any recipient. This is a final state and does not allow any further state transitions.

### State 3: Pending

The invoice validated successfully and is now delivered to recipients when
IPPs fetch invoices for a recipient.

#### Transitions

#### Transition 4: `pending` -> `expired`
Without any user action, the invoice will become `expired` after the _due date_
plus a grace period of 14 days. An expired invoice _must not be paid_.

#### Transition 5: `pending` -> `deleted`
A recipient can choose to delete an invoice. This is done by calling
[`PUT:/invoice/{id}/deleted`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/put_invoices__invoiceId__status_deleted).
As described above there is a potential ambiguity to distinguish this call from
the endpoint to _revoke_ an invoice. As described above, we use `PUT` verbs
consistently.

#### Transition 6: `pending` -> `approved`
If a recipient pays an invoice, the IPP should call
[`PUT:/invoices/{id}/status/approved`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/put_invoices__invoiceId__status_approved)
to mark the invoice as approved. It accepts two fields, `due` and `amount` as
a payload in the request body.

These two fields indicate when the payment is scheduled and the amount of the
scheduled payment. The amount must be within the valid amount specified in the
invoice.

If no further actions are taken, this is the final state of the invoice.

#### Transition 7: `pending` -> `revoked`
As long as the invoice is pending, an ISP can still revoke an invoice. It will
then disappear from the recipient's list of pending invoices.

## State 4: Expired

If a pending invoice is not processed by the recipient, it will be set to `expired`
after the due date plus the grace period has passed.

This is a final state and does not allow any further state transitions.

## State 5: Approved

An approved invoice means that the recipient has actively approved the invoice
by scheduling a payment through an IPP. The payment has to be scheduled within
the allowed time, latest at the due date and the scheduled amount has to be within
the allowed range defined in the invoice.

### Transitions

All transitions from the state `approved` can only be initiated by the IPP who
set the status to `approved`. This limitation is required.

#### Transition 8: `approved` -> `approved`

If the IPP allows for changing the payment details of an approved invoice,
the status can be updated by calling
[`PUT:/invoice/{id}/status/approved`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/put_invoices__invoiceId__status_approved)
again with the updated payment details.

#### Transition 9: `approved` -> `pending`

The user may want to change an `approved` invoice back to `pending`.
This transition is not yet fully specified.

#### Transition 10: `approved` -> `deleted`

A user may directly delete an already approved invoice if the IPP allows
changing the payment. This is done by calling
[`PUT:/invoices/{id}/status/deleted`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/put_invoices__invoiceId__status_deleted).
Deleting an invoice from this state means that the linked payment was _not_
executed and/or is stopped. It is the IPPs responsibility to ensure that.

## State 6: Deleted

The invoice has been deleted by the recipient. A deleted invoice can still be
shown to a recipient once we support queries to display old/historical invoices.

This is a final state and does not allow any further state transitions.

## State 7: Revoked

The invoice has been revoked by the issuer. A `revoked` invoice becomes invisible
for the recipient.

This is a final state and does not allow any further state transitions.
