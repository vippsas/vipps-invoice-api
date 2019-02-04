# Vipps Invoice API

This is the API documentation for [**Vipps Regninger**](https://www.vipps.no/bedrift/vipps-regninger).

_Please note that Vipps Regninger supersedes the older Vipps Faktura, both as a product and API. Vipps Faktura will be shut down on March 31 2019._

Please use GitHub's built-in functionality for
[issues](https://github.com/vippsas/vipps-invoice-api/issues),
[pull requests](https://github.com/vippsas/vipps-invoice-api/pulls),
or contact [Vipps Integration](https://github.com/vippsas/vipps-developers/blob/master/contact.md).

Document version: 0.3.12.

# Overview

## Table of contents

- [Vipps Invoice API](#vipps-invoice-api)
- [Overview](#overview)
  - [Table of contents](#table-of-contents)
  - [External documentation](#external-documentation)
    - [Technical details about the API](#technical-details-about-the-api)
    - [Getting access to the Vipps Developer Portal](#getting-access-to-the-vipps-developer-portal)
    - [Getting an access token](#getting-an-access-token)
  - [Terminology](#terminology)
  - [Time format and time zones](#time-format-and-time-zones)
- [Core functionality](#core-functionality)
  - [Send, receive and pay invoices](#send-receive-and-pay-invoices)
  - [Invoice validation](#invoice-validation)
  - [Managing and paying invoices](#managing-and-paying-invoices)
  - [Debt collection](#debt-collection)
- [Invoice states](#invoice-states)
- [HTTP responses](#http-responses)
- [Postman](#postman)
  - [Setup](#setup)
    - [Step 1: Import the Postman Collection](#step-1-import-the-postman-collection)
    - [Step 2: Import the Postman Environment](#step-2-import-the-postman-environment)
    - [Step 3: Setup Postman Environment](#step-3-setup-postman-environment)
    - [Test users](#test-users)
    - [Test issuers](#test-issuers)
  - [ISP Request Flow](#isp-request-flow)
  - [IPP Request Flow](#ipp-request-flow)
  - [Integrator checklist](#integrator-checklist)
    - [Change the status of an invoice](#change-the-status-of-an-invoice)
    - [Get commercial invoice (invoice attachment)](#get-commercial-invoice-invoice-attachment)
- [InvoiceId and variables](#invoiceid-and-variables)
  - [InvoiceId](#invoiceid)
  - [Variable Overview](#variable-overview)
- [Authentication and authorization](#authentication-and-authorization)
  - [API access token](#api-access-token)
  - [Recipient token](#recipient-token)
  - [Example 1: Send invoice](#example-1-send-invoice)
  - [Example 2: Fetch invoices for recipient](#example-2-fetch-invoices-for-recipient)
  - [Example 3: Get invoices, with complete requests and responses](#example-3-get-invoices-with-complete-requests-and-responses)
    - [Get APIM token](#get-apim-token)
    - [Get recipient token](#get-recipient-token)
    - [Get invoices](#get-invoices)
  - [National identity number (NIN), or phone number (MSISDN), not available](#national-identity-number-nin-or-phone-number-msisdn-not-available)
- [Retrieving invoice documents (attachments)](#retrieving-invoice-documents-attachments)
  - [Typical flow](#typical-flow)
  - [Validating the JSON Web Token (JWT) and the request](#validating-the-json-web-token-jwt-and-the-request)
  - [The API's public key: JWK (JSON Web Key)](#the-apis-public-key-jwk-json-web-key)
- [Detailed information about invoice states and transitions](#detailed-information-about-invoice-states-and-transitions)
  - [State transitions](#state-transitions)
  - [Detailed state descriptions](#detailed-state-descriptions)
    - [State 1: Created](#state-1-created)
      - [Transitions](#transitions)
    - [State 2: Rejected](#state-2-rejected)
    - [State 3: Pending](#state-3-pending)
      - [Transitions](#transitions-1)
  - [State 4: Expired](#state-4-expired)
  - [State 5: Approved](#state-5-approved)
    - [Transitions](#transitions-2)
  - [State 6: Deleted](#state-6-deleted)
  - [State 7: Revoked](#state-7-revoked)
- [Screenshots](#screenshots)
  - [Mapping from API to Vipps app](#screenshots-mapping-from-api-to-vipps-app)
- [Questions or comments?](#questions-or-comments)

## External documentation

### Technical details about the API

Swagger/OAS API documentation is available on GitHub: https://github.com/vippsas/vipps-invoice-api

### Getting access to the Vipps Developer Portal

See
[Vipps: Getting Started](https://github.com/vippsas/vipps-developers/blob/master/vipps-getting-started.md)
for general information, including how to retrieve the API keys.

### Getting an access token

A valid access token is required in order to call this API. This API is provided by
a service called API Management in Azure - think of it as the gateway to the API.
To get a token, follow
[the guide for Vipps eCommerce API](https://github.com/vippsas/vipps-ecom-api/blob/master/vipps-ecom-api.md).

## Terminology

| Term        | Description                                                                                                                                                                                                                  |
| :---------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ISP         | The invoice _service_ providers: Actors who submit invoices. Either for themselves or on behalf of their clients.                                                                                                            |
| IPP         | The invoice _payment_ providers: Actors who handle invoices for the invoice recipients and execute payments, e.g. banks, the Vipps app.                                                                                      |
| Recipient   | The end user that receives invoices, and pays them through the IPP.                                                                                                                                                          |
| NIN         | A national identification number, e.g. SSN in Norway ("fødselsnummer", 11 digits).                                                                                                                                           |
| MSISDN      | A number uniquely identifying a subscription in a GSM or a UMTS mobile network. Simply put, it is the mapping of the telephone number to the SIM card in a mobile phone. See [MSISDN](https://en.wikipedia.org/wiki/MSISDN). |
| Actor       | An ISP, IPP or invoice recipient.                                                                                                                                                                                            |
| Idempotency | The property of endpoints to be called multiple times without changing the result beyond the initial application.                                                                                                            |

## Time format and time zones

We use the [RFC-3339](https://www.ietf.org/rfc/rfc3339.txt) format, which is a profile of _ISO 8601_. This format includes time zone information. As an IPP/ISP this means that date and time sent to the API *must* be specify the time zone. Having time zone information implies that the API can work with date and time in a consistent and predictable manner. Internally the RFC-3339 time format is stored relative to UTC.

`1986-03-24T09:30:00.52Z` is in UTC time (denoted by the Z), while `1986-03-24T10:30:00.52+01:00` is the same time specificed with a time zone. The two examples specify the exact same point in time.

There are several benefits to this approach. It deals with daylight saving time, leap seconds and all other things that can cause edge cases when working with date and time.

# Core functionality

## Send, receive and pay invoices

_Vipps Regninger_ replaces the batch processing in _Vipps Faktura_ with
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

The validation of the invoice will still be an _asynchronous_ process since we
have no possibility to guarantee, or even estimate, the response times for
all required validation and risk check to be performed.

Therefore, the invoice will be in a `created` state once it is inserted.
In this state the invoice will not be visible to anyone. Only after all
validation steps are passed, will the invoice be in a `pending` state and shown to the recipients.
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

| #   | State      | Description                                                                          |
| :-- | :--------- | :----------------------------------------------------------------------------------- |
| 1   | `created`  | Invoice has been inserted, but not yet validated, and not yet shown to the recipient |
| 2   | `rejected` | Invoice could not be validated, and is rejected                                      |
| 3   | `pending`  | Invoice needs to be processed by the recipient                                       |
| 4   | `expired`  | Recipient did not process the invoice in time                                        |
| 5   | `approved` | Invoice has been approved by recipient                                               |
| 6   | `deleted`  | Invoice has been deleted                                                             |
| 7   | `revoked`  | Invoice has been revoked by the ISP                                                  |

See the detailed state descriptions, and state transitions, at the end of this document.

# HTTP responses

This API returns the following HTTP statuses in the responses:

| HTTP status             | Description                                             |
| ----------------------- | ------------------------------------------------------- |
| `200 OK`                | Request successful                                      |
| `201 Created`           | Request successful, resource created                    |
| `204 No Content`        | Request successful, but empty result                    |
| `400 Bad Request`       | Invalid request, see the error for details              |
| `401 Unauthorized`      | Invalid credentials                                     |
| `403 Forbidden`         | Authentication ok, but credentials lacks authorization  |
| `404 Not Found`         | The resource was not found                              |
| `409 Conflict`          | Unsuccessful due to conflicting resource                |
| `429 Too Many Requests` | There is currently a limit of max 200 calls per second\* |
| `500 Server Error`      | An internal Vipps problem.                              |

All error responses contains an `error` object in the body, with details of the problem.

\*: The limit is cautiously set quite low in the production environment, as we want to
monitor performance closely before increasing the limit.
We count HTTP requests per `client_id` and product (ISP and IPP).
For now, all HTTP requests are counted and rate-limited.
We have previously requested data from integrators about volume, times, etc,
but only received this from one integrator.
If you are able to provide data for your solution, please let us know.

# Base URL

Base URLs to which endpoint paths are appended:

MT-environment | Production environment
------------   | -------------
 `apitest.vipps.no`| `invoice-api.vipps.no`



# Postman

[Postman](https://www.getpostman.com/)
is a common tool for working with REST APIs. We offer a
[Postman Collection](https://www.getpostman.com/collection)
for Vipps Regninger to make development easier.
See the
[Postman documentation](https://www.getpostman.com/docs/)
for more information about using Postman.

By following the steps below, you can make calls to all the Vipps Regninger
endpoints, and see the full `request` and `response` for each call.

## Setup

* [Step by step](https://github.com/vippsas/vipps-developers/blob/master/postman-manual.md)
on how to set up your Postman environment, with images.

### Step 1: Import the Postman Collection

1. Click `Import` in the upper left corner.
2. Import the ISP or the IPP collection file (you can also use `Paste Raw Text`):

- [`vipps-invoice-isp-api-postman-collection.json`](https://raw.githubusercontent.com/vippsas/vipps-invoice-api/master/tools/vipps-invoice-isp-api-postman-collection.json)
- [`vipps-invoice-ipp-api-postman-collection.json`](https://raw.githubusercontent.com/vippsas/vipps-invoice-api/master/tools/vipps-invoice-ipp-api-postman-collection.json)

You should now see the full API collection in your `Collections` window.

### Step 2: Import the Postman Environment

1. Click `Import` in the upper left corner.
2. Import the ISP or IPP environment file (you can also use `Paste Raw Text`):

- [`vipps-invoice-isp-api-postman-environment.json`](https://raw.githubusercontent.com/vippsas/vipps-invoice-api/master/tools/vipps-invoice-isp-api-postman-environment.json)
- [`vipps-invoice-ipp-api-postman-environment.json`](https://raw.githubusercontent.com/vippsas/vipps-invoice-api/master/tools/vipps-invoice-ipp-api-postman-environment.json)

### Step 3: Setup Postman Environment

1. Click the "eye" icon in the top right corner.
2. In the dropdown window, click `Edit` in the top right corner.
3. Fill in the `Current Value` for the following fields to get started.
   - `access-token-key`
   - `subscription-key`
   - `client-id`
   - `client-secret`

Detailed guide on where to find the key values:
[Getting started guide](https://github.com/vippsas/vipps-developers/blob/master/vipps-developer-portal-getting-started.md#step-4).

Each recipient is identified by a MSISDN. This is set manually in the request body of `Request Recipient Token`:

```json
{
  "type": "msisdn",
  "value": "<Insert 10-digit phone number>"
}
```

Alternatively, use a NIN to identify each recipient:

```json
{
  "type": "nin-no",
  "value": "<Insert 11-digit Norwegian NIN>"
}
```

By default, both MSISDN and NIN requests are pre-populated with the test user information below.

### Test users

This test user can receive invoices, and approve, etc:

| customerId | NIN (fødselsnummer) | MSISDN (phone number) | First name   | Last name | Owner  |
| ---------- | ------------------- | --------------------- | ------------ | --------- | ------ |
| 10003301   | 01032300371         | 4797777776            | Willhelm Fos | Kluvstad  | Common |

### Test issuers

The service validates that the account belongs to the issuer ([KAR](https://www.finansnorge.no/aktuelt/presentasjoner/bankenes-felles-konto--og-adresseregister-kar/)). Make sure that that you use a valid pair when testing.

| Name               | Org. number | Account number |
| ------------------ | ----------- | -------------- |
| Vipps Teknologi AS | 918130047   | 15038366383    |

## ISP Request Flow

1. [`Fetch Authorization Token`](https://vippsas.github.io/vipps-accesstoken-api/#/Authorization_Service_(legacy)/fetchAuthorizationTokenUsingPost) to set the `{{access-token}}` variable. See [the details](#api-access-token).
2. [`Request Recipient Token`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Request_Recipient_Token_v1) to set the `{{recepient-token}}` variable. See [the details](#recipient-token).
3. [`Send Invoice`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Send_Invoice_v1)
4. [`Revoke Invoice`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Revoke_Invoice_v1)
5. [`Get Single Invoice`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Get_Single_Invoice_v1) can be called on any existing invoice.

## IPP Request Flow

1. [`Fetch Authorization Token`](https://vippsas.github.io/vipps-accesstoken-api/#/Authorization_Service_(legacy)/fetchAuthorizationTokenUsingPost)
to set the `{{access-token}}` variable. See [the details](#api-access-token).
2. [`Request Recipient Token`](https://vippsas.github.io/vipps-invoice-api/isp.html#/IPP/Request_Recipient_Token_v1) to set the `{{recepient-token}}` variable. See [the details](#recipient-token).
3. [`List Invoices`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/List_Invoices_v1)
4. [`Count Invoices For a User`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/InvoiceCount)
5. [`Get a Single Invoice`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/Get_Single_Invoice_v1)

## Sequence diagram

[Sequence diagram](vipps-sequence-diagram.md) showing ISP and IPP request flow, user interaction and invoice state transitions.

## Integrator checklist

This [checklist](vipps-integrator-checklist.md) may be useful to look at before going into production.

### Change the status of an invoice

These calls require
[`{{invoice-id}}`](https://github.com/vippsas/vipps-invoice-api/blob/master/vipps-invoice-api.md#invoiceid-and-variables),
[`{{etag}}` and `{{idempotency-key}}`](https://github.com/vippsas/vipps-invoice-api/blob/master/vipps-invoice-api.md#variable-overview).
These variables will be set when the `Get Single Invoice` call is made.

1. [`Change Status to Approved`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/Change_Status_To_Approved_v1)
2. [`Change Status to Pending`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/Change_Status_To_Pending_v1)
3. [`Delete Invoice`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/Delete_Invoice_v1)  

### Get commercial invoice (invoice attachment)

These calls require `{{invoice-id}}` and `{{mime-type}}`.
These variables will be set when the `Get Single Invoice` call is made.

1. [`Get commercial invoice document`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/Get_Commercial_Invoice_Document_v1)
2. [`Get attachment for invoice`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/Get_Attachment_For_Invoice_v1)


# InvoiceId and variables

## InvoiceId

The `invoiceId` must be constructed as `orgno-no.{issuerOrgno}.{invoiceRef}`
where `{invoiceRef}` is a URL-safe reference that is unique for each issuer.

The `invoiceId` for a test issuer with organization number `918130047`
and an `invoiceRef` abc123 would then be: `orgno-no.918130047.abc123`.

The maximal length of the complete `invoiceId` is 200 bytes, i.e. 200 characters if it consists of only ASCII characters.
We validate the `invoiceId` with this regex: `^([a-zA-Z-]+)\.(\d+)\.([a-zA-Z0-9-]+)$`.

For the sake of testing, `{invoiceRef}` could be a random number like `256203221`,
resulting in this `invoiceId`: `orgno-no.918130047.256203221`.

Please note that the organization number is validated using
[modulus 11](https://www.brreg.no/om-oss-nn/oppgavene-vare/registera-vare/om-einingsregisteret/organisasjonsnummeret/).

## Variable Overview

Following is an overview of the different variables in the Postman environments. There are som differences in the IPP and ISP APIs which requires slightly different ennvironments - indicated by the `IPP Exclusive` column.

| Name             | Located                                        |  Set                                     | IPP Exclusive |
| ---------------- | ---------------------------------------------- | ---------------------------------------- | ------------- |
| access-token-key | In developer portal under 'Your Subscriptions' | By user                                  | No            |
| subscription-key | In developer portal under 'Your Subscriptions' | By user                                  | No            |
| client-id        | In developer portal under 'Applications'       | By user                                  | No            |
| client-secret    | In developer portal under 'Applications'       | By user                                  | No            |
| access-token     | Postman Tests                                  | When 'Fetch authorization Token' is sent | No            |
| recipient-token  | Postman Tests                                  | When 'Request recipient token' is sent   | No            |
| etag             | Postman Tests                                  | When 'Get single invoice' is sent        | No            |
| idempotency-key  | Pre-request Script                             | When all `PUT` calls are sent            | No            |
| TEST-URL         | Default in Environment                         | Default                                  | No            |
| invoice-id       | Postman Tests                                  | When 'Get single invoice' is sent        | Yes           |
| mime-type        | Postman Tests                                  | When 'Get single invoice' is sent        | Yes           |
| attachment-id    | Postman Tests                                  | When 'Get single invoice' is sent        | Yes           |


# Authentication and authorization

Vipps has to ensure compliance with governing regulations, including
[GDPR](https://ec.europa.eu/info/law/law-topic/data-protection_en).
This means that we have to make sure that Vipps:

- Does not provide information about client, explicitly or implicitly, to unauthorised entities.
- Does not store information accidentally received, which we are not authorised to see.
- Propagate changes quickly if a user opts out or in to Vipps Regninger.
- Does not store personal information, i.e. invoices, which we do not have the right to see.
- Minimize the time we have any unauthorized data; i.e. we have to delete invoices we cannot validate.

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

```json
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

Every request to the API, except the [`GET:/public/jwk`](#the-apis-public-key-jwk-json-web-key) endpoint,
needs to have an `Authorization` header with the generated token.

The header in the request to this API should look like this:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1Ni <continued>
```

Please note that the JWK is _only_ used for validating the JWT.
See [The API's public key: JWK (JSON Web Key)](#the-apis-public-key-jwk-json-web-key) for more details.

## Recipient token

To submit an invoice, the client needs both an `access_token` (described above), and a `recipientToken`.

Vipps _only_ returns a `recipientToken` for Vipps users that:
* Have opted in to Vipps Regninger
* Have a bank account that can be used to pay Vipps Regninger

The `recipientToken` is obtained by calling
[`POST://recipients/tokens`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Request_Recipient_Token_v1).
This `recipientToken` can then be used in the request body to
[`PUT:/invoices/{invoiceId}`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Send_Invoice_v1)
to the specified recipient.

Please note that the calls above assumes that you have already authenticated with the
API `access_token`. See the [Postman](#postman) section for examples, etc.

To ensure GDPR compliance, the `recipientToken` has a limited time to live, currently _15
minutes_. Until it's expiry, clients are free to cache the token and re-use it to
submit several invoices to the same recipient.

## Example 1: Send invoice

| Step | Endpoint                                                                                                           | Description                                                                                                                                                      |
| ---- | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | [`POST://recipients/tokens`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Request_Recipient_Token_v1) | The call will resolve the provided personal data and return a `recipientToken` if the recipient could be resolved. This token is used in the subsequent call(s). |
| 2    | [`PUT:/invoices/{invoiceId}`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Send_Invoice_v1)           | The previously obtained `recipientToken` is used in the request body to identify the recipient.                                                                  |

[`PUT:/invoices/{invoiceId}`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Send_Invoice_v1) endpoint is idempotent. The idempotency key is a unique, user generated id. The endpoint may be called multiple times, but the invoice is inserted exactly once only. The endpoint will return a 200 status code if the invoice was inserted, a 200 if the invoice is already in the system and the contents are equal, and `409` if the invoice exists but the contents are not equal.

Invoices are never updated/modified. If in doubt, an invoice has to be fetched and the content must be compared by the client.

For ISPs who send invoices it means that they call the endpoint as many times as they want, until they get a `200` response, indicating that the invoice has been received.

## Example 2: Fetch invoices for recipient

| Step | Endpoint                                                                                                          | Description                                                                                                                                                      |
| ---- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | [`POST:/recipients/tokens`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Request_Recipient_Token_v1) | The call will resolve the provided personal data and return a `recipientToken` if the recipient could be resolved. This token is used in the subsequent call(s). |
| 2    | [`GET:/invoices`](https://vippsas.github.io/vipps-invoice-api/ipp.html#/IPP/List_Invoices_v1).                    | The previously obtained `recipientToken` is used as a header to fetch all invoices for the recipient.                                                            |

## Example 3: Get invoices, with complete requests and responses

The examples below are complete `request` and `response`examples, detailing the above examples.

### Get APIM token

```
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
```

### Get recipient token

```
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
```

### Get invoices

```
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
  "due": "2019-03-13T16:00:00+01:00",
  "amount": 25043,
  "minAmount": 25043,
  "subject": "Bompasseringer",
  "issuerName": "Lister Bompengeselskap",
  "recipient": {
    "identType": "nin-no",
    "identValue": "310362******",
    "resolvedAt": "2018-08-30T09:11:19Z"
  },
  "providerId": {
    "identType": "orgno-no",
    "identValue": "123123123"
  },
  "commercialInvoice": [
    {
      "mimeType": "application/pdf"
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
```

## National identity number (NIN), or phone number (MSISDN), not available

Vipps requires either NIN or MSISDN for
[`POST:/recipients/tokens`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/Request_Recipient_Token_v1).

# Retrieving invoice documents (attachments)

Invoice documents may be additional invoice documentation, such as
commercial invoices and attachments.

The IPP should retrieve the _actual_ document download URL on-demand on
behalf of its user. This is typically initiated when the user clicks on a
download link in a UI. The user's request should first be made to a backend
system that in turn makes the authenticated request to this API to retrieve
the _time-limited_ URL to the actual document.

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

- `ISS` (issuer): Who is issuing the JWT.E.g. `vipps.invoice.api`.
- `SUB` (subject): The base URL for the document.
- `IAT` (issued at): A specific moment in time when the JWT was issued.
- `EXP` (expiration): A specific moment in time where the JWT becomes invalid.
- `NBF` (not before): A specific moment in time where the JWT becomes valid.
- `ALG` (algorithm): Encryption algorithm. Vipps uses RS256.

In addition the `KID` (key ID), `ALG` (algorithm) and `TYP` (type of token) is available in the JWT headers.

## The API's public key: JWK (JSON Web Key)

The API's public key is required in order to validate the request and the JWT.
The public key is available as an array of JSON Web Keys (JWK):
[`GET:/public/jwk`](https://vippsas.github.io/vipps-invoice-api/isp.html#/ISP/get_public_jwk).

The API is designed to handle key rotation. There is no immediate plan to change the JWK, but it will happen at some point in time. It's strongly advised that the client implements support for this. See the pseudo-code below for how an example.

URLs:
* Test: https://apitest.vipps.no/vipps-invoice/public/jwk
* Production: https://invoice-api.vipps.no/vipps-invoice/public/jwk

See also:
[OpenID Connect Core 1.0: Rotation of Asymmetric Signing Keys](https://openid.net/specs/openid-connect-core-1_0.html#RotateSigKeys) and [RFC7515 on key rotation](https://tools.ietf.org/html/rfc7515#page-12).

The response from `/public/jwk` is an array of keys, as follows:

```json{
    "keys": [
        {
            "e": "AQAB",
            "alg": "RS256",
            "kid": "cedd7b8cbb3bfa85cba71f5001b5e09822244922",
            "use": "sig",
            "kty": "RSA",
            "n": "5Dkax7lxzotIVx5DQidS...[abbreviated]",
            "x5t": "cedd7b8cbb3bfa85cba71f5001b5e09822244922",
            "x5t#S256": "25eb881cbc57b8a953629b4065b8a7f735d8c316009e51822a710d8772a09123"
        },
        {
            "e": "AQAB",
            "alg": "RS256",
            "kid": "abb7fc35fa86b54cf4509f125a19f05455352150",
            "use": "sig",
            "kty": "RSA",
            "n": "5Dkax7lxzotIVx5DQidSa-HrQJbi_...[abbreviated]",
            "x5t": "abb7fc35fa86b54cf4509f125a19f05455352150",
            "x5t#S256": "edb47f4e719ab0f016381db6114339cc88cef1fa576beae3d72e99305a6baf91"
        }
    ]
}
```

> NOTE: As of Q4 2018, Vipps only have one key. One or more key will be added at a later time.

One of the keys in the output are always guaranteed to be valid. This enables Vipps to rotate keys if needed.

In order to validate, use the `KID` in the JWT header and find the corresponding public key in the list of `keys`.

Pseudo-code for validating the JWT:

```javascript
function IsValidJWT(jwt) {
  JWK[] keys = getKeysFromVipps()
  jwtKid = jwt.Headers["kid"]

  for each key in keys {
    if key.kid == jwtKid {
      return validate(jwt, key)
    }
  }

  // No key could validate the JWT
  // Consider refreshing the cache (if used) and retry

  return false
}
```

It is _highly_ recommended to use a pre-made library.
The library should at least help with validating the expiry time.

In addition to validating the JWT's authenticity and basic properties,
the IPP/invoice hotel must ensure to validate the following:

- The expiration timestamp is in the future. i.e. not expired.

- Make sure that the URL is valid. One approach is to return the `SUB` and
  ignore the actual path.

For details on JWT, see the [RFC 7519](https://tools.ietf.org/html/rfc7519) or
[jwt.io](https://www.jwt.io). The latter contains a list of pre-made libraries.
[RFC 7517](https://tools.ietf.org/html/rfc7517) covers JWK.

# Detailed information about invoice states and transitions

![Invoice States](images/state-machine.svg)

## State transitions

| #   | From       | To         | Description                                             |
| --- | ---------- | ---------- | ------------------------------------------------------- |
| 1   | `created`  | `pending`  | Successfully validated                                  |
| 2   |            | `rejected` | Validation **failed**                                   |
| 3   |            | `revoked`  | The invoice has been deleted by the ISP                 |
| -   | `rejected` | --         | Final state                                             |
| 4   | `pending`  | `expired`  | After grace period, the invoice cannot be modified      |
| 5   |            | `deleted`  | The recipient deleted the invoice                       |
| 6   |            | `approved` | The recipient approved invoice and payment is scheduled |
| 7   |            | `revoked`  | The invoice has been deleted by the ISP                 |
| -   | `expired`  | --         | Final state                                             |
| 8   | `approved` | `approved` | The recipient has updated the payment details           |
| 9   |            | `pending`  | The recipient has stopped the payment                   |
| 10  |            | `deleted`  | Virtual transition composed of 9 + 5                    |
| -   | `deleted`  | --         | Final state                                             |
| -   | `revoked`  | --         | Final state                                             |

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

# Screenshots   

## Mapping from API to Vipps app

![Vipps app payment screen](images/mapping-api-app.png)

| Input field            | Displayed in the app screenshot | Type | Values                               | Comment  |
| ---------------------- | ------------------------------- | ------------------------------------ | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| **1.** `issuerName`           | Vipps Socks AS                  | string |Organization name of issuer.                  |                                                                                                                              |
| **2.**`subject`                  | 918 130 047 - Vipps Socks Store                     | string | Invoice description.   | Keep it short and consistent. *Not yet supported. Use the same value as for `issuerName`. See payload below.*                                                                                                                             |
|   **3.**`due`           |  13.03.2019 | integer |     Date and time.       |                |
| **4.**`amount`              | 1050 kr.                        | integer |Amount by lowest subdivision (øre).  |                                                                                                                              |
| **5.**`minAmount`           | Press the amount to adjust minAmount.     | integer |Amount by lowest subdivision (øre).    | This is the minimum amount indicated by the issuer. Note that the user is always free to override this and pay any (positive) amount he or she wishes.|


### Example JSON payload

This is an example of the payload for `PUT:/invoices/{invoiceId}/orgno-no.947571958.abc123` for the invoice above:

```json
{
  "recipientToken": "25eb881cbc57b8a953629 <truncated>",
  "paymentInformation": {
    "type": "kid",
    "value": "1234",
    "account": "12345678903"
  },
  "invoiceType": "invoice",
  "due": "2019-03-13T00:00:00Z",
  "amount": 105000,
  "minAmount": 105000,
  "subject": "Vipps Socks AS",
  "issuerName": "Vipps Socks AS",
  "commercialInvoice": [
    {
      "mimeType": "application/pdf",
      "url": "https://www.example.com/abc123/comminv.pdf"
    }
  ],
  "attachments": [
    {
      "title": "100 pairs of socks",
      "urls": [
        {
          "url": "https://invoice-hotel.example.org/invoice/abc123.pdf",
          "mimeType": "application/pdf"
        }
      ]
    }
  ],
  "issuerIconUrl": "https://www.example.com/logos/vipps-socks-store-logo.png"
}
```

## Questions or comments?

Please use GitHub's built-in functionality for
[issues](https://github.com/vippsas/vipps-invoice-api/issues),
[pull requests](https://github.com/vippsas/vipps-invoice-api/pulls),
or contact [Vipps Integration](https://github.com/vippsas/vipps-developers/blob/master/contact.md)
