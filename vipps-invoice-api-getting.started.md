# Vipps Invoice API: Getting Started

This is the API for **Vipps Regninger**.

Please note that Vipps Regninger supersedes the older Vipps Faktura,
both as a product and API.

While we have worked closely with selected partners, and believe that this is
_very_ close to production quality, we are more than happy to receive feedback,
either with GitHub's issue functionality, or by email.

## Technical API documentation

Swagger/OAS API documentation is available on GitHub: https://github.com/vippsas/vipps-invoice-api

## Terminology: ISP and IPP

Throughout this specification we use the terms ISP and IPP to categorize two
groups of users:

* ISP, the invoice _service_ providers, are all actors who submit invoices. Either for themselves or on behalf of their clients.

* IPP, the invoice _payment_ providers, are all actors who handle invoices
for the invoice recipients and execute payments, e.g. banks, the Vipps
app.

# Core Functionality

## Send, receive and pay invoices.

"Vipps Regninger" replaces the batch processing in "Vipps Faktura" with
a more speedy per-invoice processing, with improved status and progress for
each individual invoice

This means that invoices have to be posted one by one, each invoice in a
separate HTTP call.

Although it may at first seem to be an \"inefficient\" approach, we believe that
the benefits far outweigh performance considerations. In addition, our
tests have shown that, if multiple threads are used to push invoices to our
system, the performance is well on par with a batch approach.

The main benefits are that it becomes much easier to ensure and verify
idempotency of the endpoint. We insert the received invoices _synchronously_. In
case of problems (such as `HTTP 5XX` return codes or network issues), it is possible to
simply repeatedly submit invoices until a `HTTP 2XX` status code is returned. We
guarantee that any invoice is inserted exactly once.

The validation of the invoice will still be an asynchronous process since we
have no possibility to guarantee, or even estimate ,the response times for
all required validation and risk check to be performed.

Therefore, the invoice will be in a `pending` state once it is inserted.
In this state the invoice will not be visible to anyone. Only after all
validation steps are passed, will the invoice will be shown to the recipients.
ISPs who provide the invoice will have to monitor the state. We provide two
ways to do that.

## Managing and Paying Invoices

IPPs will mainly use the `invoices` resources directly. The typical use case
will be to fetch all invoices for a recipient (user), identified by a national identification number. This is provided by `GET:/invoices`.

If a user approves an invoice, the payment provider has to mark this
individual invoice as processed so that the invoice is not displayed as an
open invoice in other services.

## Debt Collection

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

## State Transitions

| # | From | To | Description |
|---|------|----|-------------|
| 1 | `created` | `pending` | Successfully validated |
| 2 |         | `rejected`  | Validation failed|
| 3 |         | `revoked` | The invoice has been deleted by the ISP |
| - | `rejected`  | -- | Final state |
| 4 | `pending` | `expired` | After grace period, the invoice cannot be modified |
| 5 |         | `deleted` | The recipient deleted the invoice |
| 6 |         | `approved` | The recipient approved invoice and payment is scheduled |
| 7 |         | `revoked` | The invoice has been deleted by the ISP |
| - | `expired` | -- | Final state |
| 8 | `approved` | `approved` | The recipient has updated the payment details |
| 9 |          | `pending` | The recipient has stopped the payment |
| 10 |         | `deleted` | Virtual transition composed of 9 + 5 |
| - | `deleted` | -- | Final state |
| - | `revoked` | -- | Final state |

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

##### `created` -> `pending`, `rejected` (transitions 1, 2)
The state transition from the initial state `created` is performed internally.
Once an invoice is inserted into our system it will be picked up by a worker
which validates the invoice and updates the status to either `rejected` or
`pending` depending on the validation result.

##### `created` -> `revoked` (transition 3)
An ISP can revoke an invoice by calling `PUT:/invoices/{id}/status/{revoked}`
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

#### `pending` -> `expired` (transition 4)
Without any user action, the invoice will become `expired` after the _due date_
plus a grace period of 14 days. An expired invoice _must not be paid_.

#### `pending` -> `deleted` (transition 5)
A recipient can choose to delete an invoice. This is done by calling `PUT:/invoice/{id}/deleted`.
As described above there is a potential ambiguity to distinguish this call from
the endpoint to _revoke_ an invoice. As described above, we use `PUT` verbs
consistently.

#### `pending` -> `approved` (transition 6)
If a recipient pays an invoice, the IPP should call `PUT:/invoices/{id}/status/approved`
to mark the invoice as approved. It accepts two fields, `due` and `amount` as
a payload in the request body.

These two fields indicate when the payment is scheduled and the amount of the
scheduled payment. The amount must be within the valid amount specified in the
invoice.

If no further actions are taken, this is the final state of the invoice.

#### `pending` -> `revoked` (transition 7)
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

#### `approved` -> `approved` (transition 8)

If the IPP allows for changing the payment details of an approved invoice,
the status can be updated by calling `PUT:/invoice/{id}/status/approved` again
with the updated payment details.

#### `approved` -> `pending` (transition 9)

The user may want to change an `approved` invoice back to `pending`.
This transition is not yet fully specified.

#### `approved` -> `deleted` (transition 10)

A user may directly delete an already approved invoice if the IPP allows
changing the payment. This is done by calling `PUT:/invoices/{id}/status/deleted`.
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

# Retrieving invoice documents (i.e. commercial invoice and attachments)

The IPP should retrieve the *actual* document download URL on demand on
behalf of its user. This is typically initiated when the user clicks on a
download link in a UI. The user's request should first be made to a back-end
system that in turn makes the authenticated request to this API to retrieve
the *time-limited* URL to the actual document. The URL contains a *JWT*
query parameter that is validated by the ISP. The expiry time (i.e. TTL) is
inside the JWT.

Each invoice document has one or more MIME types. This means that `GET:/invoices/{invoiceId}/attachments/{attachmentId}` must include the
`mimeType` query parameter that specifies the mime type to retrieve, i.e.
document file type. The mime type is available to the IPP when listing all
the documents, so it is not necessary to guess.

## Validating the JWT and the request

The IPP is responsible for validating the JWT. The JWT contains the
following relevant claims:

* `ISS` (issuer): Who is issuing the JWT. Typically `vipps-invoice-api`.
* `AUD` (audience): Something identifying the IPP.
* `SUB` (subject): The base URL for the document.
* `EXP` (expiration): A specific moment in time where the JWT becomes invalid.
* `ALG` (algorithm): Encryption algorithm. Vipps will use **RS256**.

The APIs public key is required in order to validate the request. The public
key is available as JSON Web Key (JWK) under the `/jwk` endpoint. It is
suggested to Use a JWK library to parse and use the key.

In addition to validating the JWT, the IPP/invoice hotel must ensure to
validate the following:
* The expired timestamp is in the future. I.e. not expired.
* Make sure that the URL is valid. One approach is to return the `SUB` and
ignore the actual path.

For details on JWT, use the [RFC](https://tools.ietf.org/html/rfc7519) or
[jwt.io](https://www.jwt.io). The latter contains a list of pre-made
libraries. We **highly** recommend using a pre-made library. It should at
the very least validate the expiry time.
