# Vipps Invoice API

This is the API documentation for [**Vipps Regninger**]( https://www.vipps.no/bedrift/vipps-regninger).

*Please note that Vipps Regninger supersedes the older Vipps Faktura, both as a product and API.*

**Status:** 🛠 While we have worked closely with selected partners, and believe that this is
_very_ close to production quality, we are more than happy to receive feedback.

Please use GitHub's built-in functionality for
[issues](https://github.com/vippsas/vipps-invoice-api/issues),
[pull requests](https://github.com/vippsas/vipps-invoice-api/pulls),
or contact us at integration@vipps.no.

Document version: 0.2.19.

## External documentation

### Technical details about the API

Swagger/OAS API documentation is available on GitHub: https://github.com/vippsas/vipps-invoice-api

### Getting access to the Vipps Developer Portal

See
[the getting started guide](https://github.com/vippsas/vipps-developers/blob/master/vipps-developer-portal-getting-started.md)
for the Vipps eCommerce API for general information about the Vipps Developer Portal.
This is where you create keys to the API.

### Getting an access token

A valid access token is required in order to call this API. This API is provided by
a service called API Management in Azure - think of it as the gateway to the API.

The documentation for the Vipps Access Token API is at:
https://github.com/vippsas/vipps-accesstoken-api.

Shortly summarized, you will have to make the following request
(`client_id`, `client_secret` and `Ocp-Apim-Subscription-Key` placeholders must be replaced with real values):

```http
POST https://apitest.vipps.no/api/access-token/jwt-token HTTP/1.1
Host: apitest.vipps.no
Content-Type: application/json
Ocp-Apim-Subscription-Key: <Ocp-Apim-Subscription-Key>

{
	"client_id":"<client_id>",
	"client_secret":"<client_secret>",
	"resource":"https://testapivipps.no/vippsas/invoice-isp-service
}

```

The `resource` must be either `https://testapivipps.no/vippsas/invoice-isp-service` or `
https://testapivipps.no/vippsas/invoice-ipp-service`.

The request above will return a response similar to this, with the `access_token`:

```http
HTTP 200 OK
{
  "token_type": "Bearer",
  "expires_in": "86398",
  "ext_expires_in": "0",
  "expires_on": "1495271273",
  "not_before": "1495184574",
  "resource": "00000002-0000-0000-c000-000000000000",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1Ni <continued>"
}
```

Every request to the API needs to have an `Authorization` header with the generated token.

The header in the request to this API should look like this:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1Ni <continued>
```

## Terminology

| Term |  Description                                    |
|:-----|:----------------------------------------------- |
| ISP         | The invoice _service_ providers: Actors who submit invoices. Either for themselves or on behalf of their clients.  |
| IPP         | The invoice _payment_ providers: Actors who handle invoices for the invoice recipients and execute payments, e.g. banks, the Vipps app. |
| Recipient   | The end user that receives invoices, and pays them through the IPP.  |
| NIN         | A national identification number, e.g. SSN in Norway ("fødselsnummer", 11 digits).   |
| MSISDN      | A number uniquely identifying a subscription in a GSM or a UMTS mobile network. Simply put, it is the mapping of the telephone number to the SIM card in a mobile phone. See [MSISDN](https://en.wikipedia.org/wiki/MSISDN). |
| Actor       | An ISP, IPP or invoice recipient. |
| Idempotency | The property of endpoints to be called multiple times without changing the result beyond the initial application. |

# Core functionality

## Send, receive and pay invoices

*Vipps Regninger* replaces the batch processing in *Vipps Faktura* with
a more speedy per-invoice processing, with improved status and progress for
each individual invoice. This means that invoices have to be posted one by one
in separate HTTP calls.

Although it may at first seem to be an inefficient approach, we believe that
the benefits far outweigh performance considerations. In addition, our
tests have shown that, if multiple threads are used to push invoices to our
system, the performance is well on par with a batch approach.

The main benefits are that it becomes much easier to ensure and verify
idempotency of the endpoint, and that issues related to callbacks
(sometimes caused by network-related timeouts, etc - often difficult to fix)
are eliminated.

Received invoices are inserted _synchronously_. In case of problems (such as
`HTTP 5XX` return codes or network issues), it is possible to
simply repeatedly submit invoices until a `HTTP 2XX` status code is returned.
We guarantee that any correctly received invoice is inserted exactly once.

## Invoice validation

The validation of the invoice will still be an *asynchronous* process since we
have no possibility to guarantee, or even estimate, the response times for
all required validation and risk check to be performed.

Therefore, the invoice will be in a `pending` state once it is inserted.
In this state the invoice will not be visible to anyone. Only after all
validation steps are passed, will the invoice will be shown to the recipients.
ISPs who provide the invoice will have to monitor the state.

## Managing and paying invoices

IPPs will mainly use the `/invoices` resources directly. The typical use case
will be to fetch all invoices for a recipient (user), identified by a national
identification number. This is provided by
[`GET:/invoices`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/List_Invoices_v1).

If a user approves an invoice, the payment provider has to mark this
individual invoice as `approved` so that the invoice is not displayed as an
open invoice in other services.

## Debt collection

All invoices contain information about the _invoice type_, i.e. whether it
is a regular invoice, a reminder or other. This enables payment providers to
filter the allowed payment methods according to Norwegian debt collection laws.

# Invoice states

| # | State      | Description                                                                          |
|:--|:-----------|:-------------------------------------------------------------------------------------|
| 1 | `created`  | Invoice has been inserted, but not yet validated, and not yet shown to the recipient |
| 2 | `rejected` | Invoice could not be validated, and is rejected                                      |
| 3 | `pending`  | Invoice needs to be processed by the recipient                                       |
| 4 | `expired`  | Recipient did not process the invoice in time                                        |
| 5 | `approved` | Invoice has been approved by recipient                                               |
| 6 | `deleted`  | Invoice has been deleted                                                             |
| 7 | `revoked`  | Invoice has been revoked by the ISP                                                  |

See the detailed state descriptions, and state transitions, at the end of this document.

# HTTP responses

This API returns the following HTTP statuses in the responses:

| HTTP status         | Description                                 |
| ------------------- | ------------------------------------------- |
| `200 OK`            | Request successful                          |
| `201 Created`       | Request successful, resource created        |
| `204 No Content`    | Request successful, but empty result        |
| `400 Bad Request`   | Invalid request, see the error for details  |
| `401 Unauthorized`  | Invalid credentials                         |
| `403 Forbidden`     | Authentication ok, but credentials lacks authorization  |
| `404 Not Found`     | The resource was not found  |
| `409 Conflict`      | Unsuccessful due to conflicting resource   |
| `429 Too Many Requests`  | There is currently a limit of max 20 calls per second\*  |
| `500 Server Error`  | An internal Vipps problem.                  |

All error responses contains an `error` object in the body, with details of the problem.

\*: The limit is cautiously set quite low in the production environment, as we want to
monitor performance closely before increasing the limit.
We count HTTP requests per `client_id` and product (ISP and IPP).
For now, all HTTP requests are counted and rate-limited.
We have previously requested data from integrators about volume, times, etc,
but only received this from one integrator.
If you are able to provide data for your solution, please let us know.

# Authentication and authorization

Vipps has to ensure compliance with governing regulations, including
[GDPR](https://ec.europa.eu/info/law/law-topic/data-protection_en).
This means that we have to make sure that Vipps:

* Does not provide information about client, explicitly or implicitly, to unauthorised entities.
* Does not store information accidentally received, which we are not authorised to see.
* Propagate changes quickly if a user opts out or in to Vipps Regninger.
* Does not store personal information, i.e. invoices, which we do not have the right to see.
* Minimize the time we have any unauthorized data; i.e. we have to delete invoices we cannot validate.

## API access token

The first thing that is required is to get the access token to the API. This is described
in the [external documentation section](#external-documentation).

Shortly summarized, you will have to make the following request
(`client_id`, `client_secret` and `Ocp-Apim-Subscription-Key` placeholders must be replaced with real values):

```http
POST https://apitest.vipps.no/accesstoken/get
client_id: <client_id>
client_secret: <client_secret>
Ocp-Apim-Subscription-Key: <Ocp-Apim-Subscription-Key>
```

Please note: It _is_ correct that this is a `POST` request with an empty body.
This is due to some technical details of the backend solutions.

The request above will return a response similar to this, with the `access_token`:

```http
HTTP 200 OK
{
  "token_type": "Bearer",
  "expires_in": "86398",
  "ext_expires_in": "0",
  "expires_on": "1495271273",
  "not_before": "1495184574",
  "resource": "00000002-0000-0000-c000-000000000000",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1Ni <continued>"
}
```

Every request to the API, _including_ the `/jwk` endpoint, needs to have an `Authorization` header with the generated token.
*(NOTE: The `/jwk` endpoint is not possible to use with the "Try out" feature in the Swagger documentation on GitHub).*

The header in the request to this API should look like this:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1Ni <continued>
```
Please note that the JWK is _only_ used for validating the JWT.
See [The API's public key: JWK (JSON Web Key)](#the-apis-public-key-jwk-json-web-key) for more details.

## Recipient token

In addition to the general `access_token` for the API, you need to create a
`recipientToken` for the recipient.

To submit an invoice, the client first has to obtain a `recipientToken` with
[`POST://recipients/tokens`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Request_Recipient_Token_v1).
This token can then be used in the request body to
[`PUT:/invoices/{invoiceId}`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Send_Invoice_v1).

Please note that this assumes that you have already authenticated with the
API `access_token` - which is not to be confused with the `recipientToken`.

To ensure GDPR compliance, the `recipientToken` has a limited time to live, currently _15
minutes_. Until it's expiry, clients are free to cache the token and re-use it to
submit several invoices to the same recipient.

## Example 1: Send invoice

| Step | Endpoint     | Description                   |
| -----| -------------| ----------------------------- |
| 1    | [`POST://recipients/tokens`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Request_Recipient_Token_v1)    | The call will resolve the provided personal data and return a `recipientToken` if the recipient could be resolved. This token is used in the subsequent call(s). |
| 2    | [`PUT:/invoices/{invoiceId}`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Send_Invoice_v1) | The previously obtained `recipientToken` is used in the request body to identify the recipient.  |

[`PUT:/invoices/{invoiceId}`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Send_Invoice_v1) endpoint is idempotent. The idempotency key is the `invoiceId`. The endpoint may be called multiple times, but the invoice is inserted exactly once only. The endpoint will return a 200 status code if the invoice was inserted, a 200 if the invoice is already in the system and the contents are equal, and `409` if the invoice exists but the contents are not equal.

Invoices are never updated/modified. If in doubt, an invoice has to be fetched and the content must be compared by the client.

For ISPs who send invoices it means that they call the endpoint as many times as they want, until they get a `200` response, indicating that the invoice has been received.

## Example 2: Fetch invoices for recipient

| Step | Endpoint     | Description                   |
| -----| -------------| ----------------------------- |
| 1    | [`POST:/recipients/tokens`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Request_Recipient_Token_v1) | The call will resolve the provided personal data and return a `recipientToken` if the recipient could be resolved. This token is used in the subsequent call(s). |
| 2    | [`GET:/invoices`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/List_Invoices_v1).   | The previously obtained `recipientToken` is used as a header to fetch all invoices for the recipient.                                                         |

## Example 3: Get invoices, with complete requests and responses

The examples below are complete `request` and `response`examples, detailing the above examples.

### Get APIM token
~~~~
POST https://apitest.vipps.no/accessToken/get
Ocp-Apim-Subscription-Key : ***
client_secret : ***
client_id : ***

{
  "token_type":"Bearer",
  "expires_in":"86398",
  "ext_expires_in":"0",
  "expires_on":"1536840154",
  "not_before":"1536753455",
  "resource":"00000002-0000-0000-c000-00000000000",
  "access_token":"***"
}
~~~~

### Get recipient token

~~~~
POST https://apitest.vipps.no/vipps-ipp/v1/recipients/tokens
Authorization : ***
Ocp-Apim-Subscription-Key : ***
{
  "type": "nin-no",
  "value":"010298******"
}
{
  "recipientToken":"***"
}
~~~~

### Get invoices

~~~~
GET https://apitest.vipps.no/vipps-ipp/v1/invoices
Authorization : ***
Ocp-Apim-Subscription-Key : ***
vippsinvoice-recipienttoken : ***

[{
  "invoiceId": "orgno-no.123123123.047770296",
  "paymentInformation": {
    "type": "kid",
    "value": "1234567890128",
    "account": "12345678903"
  },
  "invoiceType": "invoice",
  "due": "2023-03-13T16:00:00+01:00",
  "amount": 25043,
  "minAmount": 25043,
  "subject": "Bompasseringer",
  "issuerName": "Lister Bompengeselskap",
  "recipient": {
    "identType": "nin-no",
    "identValue": "310362******",
    "resolvedAt": "2018-08-30T09:11:19Z"
  },
  "commercialInvoice": [
    {
      "mimeType": "application/pdf",
      "url": "https://www.example.com/08fd5360-e218-4658-894f-4f37649e7df7/comminv.pdf"
    }
  ],
  "attachments": [
    {
      "id": "1",
      "title": "Ferry",
      "mimeTypes": [
        "application/pdf"
      ]
    }
  ],
  "issuerIconUrl": "https://www.example.com/logos/lister.png",
  "status": {
    "created": "2018-08-30T09:11:19Z",
    "state": "pending",
    "etag": "0300536c-0000-0000-0000-5b87b4b70000",
    "createdBy": {
      "actorId": "",
      "appId": ""
    }
  },
  "created": ""
}
~~~~

## National identity number (NIN), or phone number (MSISDN), not available

Vipps requires either NIN or MSISDN for
[`POST:/recipients/tokens`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Request_Recipient_Token_v1).

# Retrieving invoice documents (attachments)

Invoice documents may be additional invoice documentation, such as
commercial invoices and attachments.

The IPP should retrieve the *actual* document download URL on-demand on
behalf of its user. This is typically initiated when the user clicks on a
download link in a UI. The user's request should first be made to a backend
system that in turn makes the authenticated request to this API to retrieve
the *time-limited* URL to the actual document.

The URL contains a JWT query parameter that is validated by the ISP.
The expiry time (`EXP`) is inside the JWT.

Each invoice document has one or more MIME types. This means that
[`GET:/invoices/{invoiceId}/attachments/{attachmentId}`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/Get_Attachment_For_Invoice_v1)
must include the `mimeType` query parameter that specifies the mime type to
retrieve, i.e. document file type. The MIME type is available to the IPP when
listing all the documents. This allows the IPP to present it in multiple ways.

PDF is a commonly used MIME type, which can be displayed in most contexts.

The Vipps app will display PDFs for now, but this may change at a later time.

There is currently no limitation to the length of the URL.

## Typical flow

1. An invoice is sent with [`PUT:/invoices/{invoiceId}`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Send_Invoice_v1),
containing the "commercial invoice" attachment, with an URL like `https://invoice-hotel.example.org/123456-abcdef-7890.pdf`
The URL sent by the ISP when creating an invoice should be valid as long as possible (more than 12 months is good).
The validity will be controlled with the JWT appended.

2. Sometime later, the end user clicks on "show invoice" in the app or online bank. The
[`GET:/invoices/{invoiceid}`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/Get_Single_Invoice_v1)
request returns a response with the URL and a JWT appended.
The returned URL would be something like `https://invoice-hotel.example.org/123456-abcdef-7890.pdf?token=[jwt_token_goes_here]`.

3. The app or online bank will redirect the user to the document. Most likely the user
will have a browser opened that loads the document.

4. The IPP/invoice hotel will receive the request directly from the end user's device,
and will need to validate the JWT token before sending the document data.

5. If the JWT is valid, the user is sent the document data (e.g. the PDF).

 It is up to the invoice hotel how long the documents are available.
 This depends on the invoice hotel's agreement with the invoice issuer,
 and can be 18 months, 10 years or something else.

## Validating the JSON Web Token (JWT) and the request

The IPP/invoice hotel is responsible for validating the JWT before returning the document.

Vipps has chosen a modern standard for validating tokens with keys, and
this is the same method used by Microsoft Azure, on which Vipps is built.
See also: [JSON Web Token Best Current Practices draft-ietf-oauth--bcp-03](https://tools.ietf.org/html/draft-ietf-oauth-jwt-bcp-03).

The JSON Web Token (JWT) contains the following relevant claims:

* `ISS` (issuer): Who is issuing the JWT. Typically `vipps.invoice.api`.
* `AUD` (audience): Something identifying the IPP.
* `SUB` (subject): The base URL for the document.
* `EXP` (expiration): A specific moment in time where the JWT becomes invalid.
* `ALG` (algorithm): Encryption algorithm. Vipps uses RS256.

## The API's public key: JWK (JSON Web Key)

The API's public key is required in order to validate the request and the JWT.
The public key is available as an array of JSON Web Keys (JWK):
[`GET:/jwk`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/get_jwk).

**IMPORTANT:** We are currently working on the logic around caching and
rotating of the JWK, and aim to use two keys: One primary key and one secondary key.
There is no immediate plan to change the JWK, but this implementation logic
allows for easy and automatic key rotation at a later stage, including
changing the encryption algorithm - without a change to the client code.
Until further notice, the JWK can be cached for 10 minutes.
See also:
[OpenID Connect Core 1.0: Rotation of Asymmetric Signing Keys](https://openid.net/specs/openid-connect-core-1_0.html#RotateSigKeys).

The response is as follows:

```json
{
  "keys": [
    {
      "e": "AQAB",
      "alg": "RS256",
      "use": "sig",
      "kid": "jwt",
      "kty": "RSA",
      "n": "5Dkax7lxzotIVx5DQidS..."
    }
  ]
}
```

Vipps _may_ rotate keys, which may result in a JWK not being usable for
validating the JWT.
In this case, the `keys` array will will contain another, valid JWK.
Should a call fail, a new call may be performed immediately with the new key.

Pseudo-code for validating the JWT:

```java
function IsValidJWT(jwt) {
  JWK[] keys = getKeysFromVipps()

  for each key in keys {
    if validate(jwt, key) {
        return true
    }
  }

  // No key could validate the JWT
  return false
}
```

It is _highly_ recommended to use a pre-made library.
The library should at least help with validating the expiry time.

In addition to validating the JWT's authenticity and basic properties,
the IPP/invoice hotel must ensure to validate the following:

* The expiration timestamp is in the future. i.e. not expired.

* Make sure that the URL is valid. One approach is to return the `SUB` and
ignore the actual path.

For details on JWT, see the [RFC 7519](https://tools.ietf.org/html/rfc7519) or
[jwt.io](https://www.jwt.io). The latter contains a list of pre-made libraries.
[RFC 7517](https://tools.ietf.org/html/rfc7517) covers JWK.

# Detailed information about invoice states and transitions

![Invoice States](images/state-machine.svg)

## State transitions

| #  | From       | To         | Description                                             |
| --- | --------- | ---------- | ------------------------------------------------------- |
| 1  | `created`  | `pending`  | Successfully validated                                  |
| 2  |            | `rejected` | Validation **failed**                                   |
| 3  |            | `revoked`  | The invoice has been deleted by the ISP                 |
| -  | `rejected` | --         | Final state                                             |
| 4  | `pending`  | `expired`  | After grace period, the invoice cannot be modified      |
| 5  |            | `deleted`  | The recipient deleted the invoice                       |
| 6  |            | `approved` | The recipient approved invoice and payment is scheduled |
| 7  |            | `revoked`  | The invoice has been deleted by the ISP                 |
| -  | `expired`  | --         | Final state                                             |
| 8  | `approved` | `approved` | The recipient has updated the payment details           |
| 9  |            | `pending`  | The recipient has stopped the payment                   |
| 10 |            | `deleted`  | Virtual transition composed of 9 + 5                    |
| -  | `deleted`  | --         | Final state                                             |
| -  | `revoked`  | --         | Final state                                             |

## Detailed state descriptions

### State 1: Created

The initial state of an invoice is `created`. Invoices received are directly
inserted into the database with only minimal validation performed on the provided
request body.

This way, the ingestion is decoupled from the actual validation and can keep the
workload on the ingesting endpoints low, so that we can achieve fast response
times.

The actual validation may include many calls to external services, and response
times can not be guaranteed. This asynchronous approach is required.

#### Transitions

**Transitions 1, 2: `created` -> `pending`, `rejected`**

The state transition from the initial state `created` is performed internally.
Once an invoice is inserted, it will be picked up by a worker
that attempts to validate the invoice, and updates the status to either `rejected` or
`pending` depending on the validation result.

**Transition 3: `created` -> `revoked`**

An ISP can revoke an invoice by calling
[`PUT:/invoices/{id}/status/{revoked}`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Revoke_Invoice_v1)
It _could_ have been a `DELETE`, but we decided to use `PUT` verbs consistently.

### State 2: Rejected

If the validation has failed, the invoice ends up in the `rejected` state. This is
an end state, and means that the invoice was not accepted into our system and is
never shown to any recipient. This is a final state and does not allow any further state transitions.

### State 3: Pending

The invoice validated successfully and is now delivered to recipients when
IPPs fetch invoices for a recipient.

#### Transitions

**Transition 4: `pending` -> `expired`**
Without any user action, the invoice will become `expired` after the _due_ timestamp.

plus a grace period of 14 days. An expired invoice _must not be paid_.

**Transition 5: `pending` -> `deleted`**

A recipient can choose to delete an invoice. This is done by calling
[`PUT:/invoice/{id}/deleted`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/Delete_Invoice_v1).
As described above there is a potential ambiguity to distinguish this call from
the endpoint to _revoke_ an invoice. As described above, we use `PUT` verbs
consistently.

**Transition 6: `pending` -> `approved`**

If a recipient pays an invoice, the IPP should call
[`PUT:/invoices/{id}/status/approved`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/Change_Status_To_Approved_v1)
to mark the invoice as `approved.` It accepts two fields, `due` and `amount` as
payload in the request body.

These two fields indicate when the payment is scheduled and the amount of the
scheduled payment. The amount must be within the valid amount specified in the
invoice.

If no further actions are taken, this is the final state of the invoice.

**Transition 7: `pending` -> `revoked`**

As long as the invoice is `pending`, an ISP can still revoke an invoice by calling
[`PUT:/invoices/{id}/status/revoked`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Revoke_Invoice_v1)
The invoice will then disappear from the recipient's list of pending invoices.

## State 4: Expired

If a pending invoice is not processed by the recipient, it will be set to `expired`
after the due timestamp plus the grace period of 14 days has passed.

This is a final state and does not allow any further state transitions.

## State 5: Approved

An `approved` invoice means that the recipient has actively approved the invoice
by scheduling a payment through an IPP. The payment has to be scheduled within
the allowed time, latest at the due timestamp and the scheduled amount has to be within
the allowed range defined in the invoice.

### Transitions

All transitions from the state `approved` can only be initiated by the same IPP
that set the status to `approved`. This limitation is required.

**Transition 8: `approved` -> `approved`**

If the IPP allows for changing the payment details of an approved invoice,
the status can be updated by calling
[`PUT:/invoice/{id}/status/approved`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/Change_Status_To_Approved_v1)
again with the updated payment details.

**Transition 9: `approved` -> `pending`**

The user may want to change an `approved` invoice back to `pending`.
_This transition is not yet fully specified._

**Transition 10: `approved` -> `deleted`**

A user may directly delete an already approved invoice if the IPP allows
changing the payment. This is done by calling
[`PUT:/invoices/{id}/status/deleted`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/Delete_Invoice_v1).
Deleting an invoice from this state means that the linked payment was _not_
executed and/or is stopped. It is the IPPs responsibility to ensure that.

## State 6: Deleted

The invoice has been deleted by the recipient. A `deleted` invoice can still be
shown to a recipient once queries to display old/historical invoices are supported.

This is a final state and does not allow any further state transitions.

## State 7: Revoked

The invoice has been revoked by the issuer. A `revoked` invoice becomes invisible
for the recipient.

This is a final state and does not allow any further state transitions.

# Questions or comments?

Please use GitHub's built-in functionality for
[issues](https://github.com/vippsas/vipps-invoice-api/issues),
[pull requests](https://github.com/vippsas/vipps-invoice-api/pulls),
or contact us at integration@vipps.no.
