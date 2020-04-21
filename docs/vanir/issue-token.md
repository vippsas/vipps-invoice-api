# Requesting and using issue-tokens

> ⚠ WORK IN PROGRESS ⚠
> 
> **We would love to get some feedback on this documentation.** Let us know if anything is unclear or could be improved.
> 
> Among things that are uncertain and might change are:
> 
> - Support for other inputs than Norwegian social security numbers for unique lookups
> - The use/need for organization number as a part of the inputs

ℹ Examples can become outdated. Refer to the OpenAPI contract for the current version.

⚠ Issue-tokens, and related services, must not be used to "wash", clean or synchronize customer data. The token is a __short-lived proof__ that Vipps acknowledge the recipient and (s)he has consented to receive an invoice at the current time for the given organization.


## Terms

* **Issuer**: Someone who issues invoices. E.g. an electrical company.
* **Issuer identifier**: An ID that uniquely identifies an issuer. In Norway, this is 'organisasjonsnummer'.
* **ISP**: "Invoice Service Provider". Someone who receives the invoices from the issuer and forwards them to e.g. Vipps.
* **IPP**: "Invoice Payment Provider". Someone who fetches the invoices in order to present them to a recipient, e.g. a online bank or the Vipps app
* **NIN**: "National identification number". In Norway, this is 'fødselsnummer'.
* **Agreement**: A reference that identifies an agreement between the issuer and recipient. 
* **Recipient**: Someone who receives the invoice. 
* **(Unique) Recipient identifier**: NIN or Agreement (potentially in the future)
* **Issue-token**: A [_JWT_](https://en.wikipedia.org/wiki/JSON_Web_Token) that acts as proof that the recipient exists and can receive an invoice from a given _issuer_.
  The token is sent along with the invoice data when issuing an invoice. 
* **MSISDN** Globally unique phone number, see [https://en.wikipedia.org/wiki/MSISDN](https://en.wikipedia.org/wiki/MSISDN)


## Changes from v1. to v2.

* _Recipient token_ is now referred to as an _issue-token_
* The _issue-token_ is only used when issuing the invoice
    * v1. required _recipient token_ for other operations
* Lookups of _issue-token_ by MSISDN alone is no longer allowed (but will be supported in v1 until v1 is decommissioned)
* _Issue-token_ is only valid for the given issuer
    * Can send multiple invoice for the same issuer with one token
* New API endpoints and contracts
* Possible to look up _issue-token_ with other data, e.g name, address and e-mail
* IPP does not have to use tokens
* Enables access to ~400 000 new recipients

## Introduction

Vipps need to adhere to several regulations and compliance directives. One of them requires Vipps to not receive data for users that have not given explicit consent to receive electronic invoices. By requesting an issue-token _before_ sending the data, Vipps can make sure no data is received without the user having an active consent.

The issue-token is a JSON Web Token (JWT) that is signed by Vipps and only created when Vipps has checked that the user can receive invoices. The token has a short lifetime (<= 15 minutes) and should not be stored. 

**❗ Before any invoice data is sent to Vipps, the ISP _must_ successfully retrieve an issue-token.**

**❗ The ISP should not store or use the issue-token to anything besides passing it with the invoice data when issuing the invoice. The content (e.g. claims etc) of the issue-token are subject to change without notice.**

There are two ways of getting an issue-token:

1. Use of a _unique recipient identifier_ and an _issuer identifier_. 
2. Use of _possibly_ non-unique recipient data and an _issuer identifier_.
  * MSISDN _and_ email
  * (MSISDN _or_ email) _and one or more_ (name _or_ date of birth _or_ postcode _or_ address)
    
If the request successfully returns an issue-token, the ISP can proceed with issuing the invoice.
The issue-token is added as a header to the issue invoice request.

The issue-token should be retrieved right before issuing the invoice. The token is valid for _one recipient_ receiving one or more invoices from _one issuer_.

### Business rules

The rules for when to give an issue-token are the following:

* The recipient has to be registered in either Vipps or a partner's system
* The recipient has to have an active and explicit consent to 
    * receive all invoices electronically (JTTA)
    * receive an invoice for the specific issuer (JTTB) (*Not implemented yet*)

### Common mistakes

* Reusing the issue-token for different issuers
* Using this service to "wash" data
* Storing or using the token past it's expiry time
* Not having up to date recipient information when using the non-unique endpoint
* First name and last name might be switched in some of the systems - consider trying both combinations

## Requesting an issue-token with a unique identifier

> See the OpenAPI contract for details on request and response payloads.

Below is an example of requesting an issue-token for a Norwegian recipient using a 'fødselsnummer', for a given Norwegian company identified by an 'organisasjonsnummer'.
```json
{
  "recipientIdentifierType": "norwegianNIN",
  "recipientIdentifierValue": "23106029172",
  "issuerIdentifierType": "norwegianOrganizationNumber",
  "issuerIdentifierValue": "918130047"
}
```

## Requesting an issue-token with recipient data

If no unique identifier is available, the ISP can attempt finding the recipient with a combination of data that might be available. 

This approach only gives a issue-token when a unique match is found (an issue-token is not returned if the given recipient data matches more than one recipient).

The following is pseudo-code of what is done to validate the input.
```java    
// strongIdentifiers and vagueIdentifiers are both lists 
if (strongIdentifiers >= 2) { validInput() }
else if (strongIdentifiers >= 1 && vagueIdentifiers >= 1) { validInput() }
else { notEnoughData() }
```

Vipps recommend that all the available data is sent in, then Vipps will decide what data to use to identify the recipient.

Matching of vague identifiers will be an exact match (e.g no Soundex, wildcards, fuzzy matching or similar).

The following are examples of valid requests.
```json
{
  "issuerIdentifierType": "norwegianOrganizationNumber",
  "issuerIdentifierValue": "918130047",
  "msisdn": "4799912345",
  "email": "ola@example.org"
}
```

```json
{
  "issuerIdentifierType": "norwegianOrganizationNumber",
  "issuerIdentifierValue": "918130047",
  "msisdn": "4799912345",
  "dateOfBirth": "1986-03-24"
}
```

```json
{
  "issuerIdentifierType": "norwegianOrganizationNumber",
  "issuerIdentifierValue": "918130047",
  "email": "ola@example.org",
  "lastName": "Nordmann"
}
```

```json
{
  "issuerIdentifierType": "norwegianOrganizationNumber",
  "issuerIdentifierValue": "918130047",
  "msisdn": "4799912345",
  "email": "ola@example.org",
  "dateOfBirth": "1986-03-24",
  "addressLine1": "Testgata 42A",
  "addressLine2": "",
  "postCode": "8500",
  "city": "Narvik",
  "countryCode": "NO",
  "firstName": "Ola",
  "lastName": "Nordmann"
}
```

### Accepted identifiers

This set of accepted identifiers might be extended in the future.
See the OpenAPI contract for details on validation and formats.

**Unique identifiers**

* Norwegian SSN

**Strong identifiers** (aka. primary aliases):

* Phone number (MSISDN format)
* Email address

**Vague identifiers** (aka secondary aliases):

* Postcode (must be an exact match)
* Date of birth (yyyy-mm-dd format)
* Name
    * First name (must be an exact match)
    * Last name (must be an exact match)
* Address
    * Address line 1 
    * Address line 2
    * City
    * Postcode
    * Country code
