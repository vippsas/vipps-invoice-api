# Vipps Invoice IPP Postman Collection

## Step 1 - Import Postman Collection
1. Copy the contents of  ```vipps-invoice-ipp-postman-collection``` 
2. Open Postman and click ```Import``` in the upper left corner.
3. Select the ```Paste Raw Text``` tab and ans paste in the collection

You should now see the full API collection in your ```Collections``` window.

## Step 2 - Import Postman Environment
1. Copy the contents of ```vipps-invoice-ipp-postman-environment```
2. Open Postman and click ```Import``` in the upper left corner.
3. Select the ```Paste Raw Text``` tab and paste in the environment

## Step 3 - Setup Postman Environment
1. Click the eye icon in the top right corner.
2. In the dropdown window, click ```Edit``` in the top right corner.
3. Fill in the ``` Current Value``` for the following fields to get started. 
    * product-key
    * client-id
    * client-secret

Each recipient is identified by a NIN, this is set manually in the request body of ```Request Recipient Token```

```
{
  "type": "nin-no",
  "value": "<Insert NIN>"
}
```

You can use [this](#test-users) user for testing 

## InvoiceId

The invoiceId must be constructed as orgno-no.{issuerOrgno}.{invoiceRef} where {invoiceRef} is a URL-safe reference that is unique for each issuer.

The invoiceId for the supplied test issuer would then be: ```orgno-no.918130047.{url}``` for testing, ```{url}```could just be a random number, e.g ```orgno-no.918130047.0000```


### Variable Overview

| Name | Located | Set | Value |
| ---- | ------- | --- | ----- |
| product-key | In developer portal under 'Your Subscriptions' | By user | 32 char String |
| client-id | In developer portal under 'Applications' | By user | 36 char String | 
| client-secret | In developer portal under 'Applications' | By user | String | 
| access-token | Postman Tests | When 'Fetch authorization Token' is sent | String | 
| recipient-token | Postman Tests | When 'Request recipient token' is sent | String |
| etag | Postman Tests | When 'Get single invoice' is sent | String | 
| idempotency-key | Postman Tests | When 'Get single invoice' is sent | String | 
| invoice-id | Postman Tests | When 'Get single invoice' is sent | String |
| mime-type | Postman Tests | When 'Get single invoice' is sent | String |
| attachment-id | Postman Tests | When 'Get single invoice' is sent | 

### Postman Tests
Most of the environment variables will be set/updated automatically throughout the calls. Most of the variables will be updated with the ```Get Single Invoice``` call. This call requires an invoice-id in the URL and this has to be set manually.

For the variables to work correctly, please send a ```Get Single Invoice``` call after all ```PUT``` operations  to update the environment variables to the correct value.

#### Put operations
```Change status to approved```

```Change status to pending```

```Delete invoice```


### Test users

This test user can receive invoices, and approve, etc:

| customerId | NIN (fødselsnummer) | MSISDN (phone number) | First name | Last name | Owner |
| ---------- | ------------------- | --------------------- | ---------- | --------- | ----- |
| 10003301	 | 01032300371         | 4797777776            | Willhelm Fos | Kluvstad | Common |

### Test issuers

The service validates that the account belongs to the issuer ([KAR](https://www.finansnorge.no/aktuelt/presentasjoner/bankenes-felles-konto--og-adresseregister-kar/)). Make sure that that you use a valid pair when testing.

| Name               | Org. number | Account number |
| ------------------ |------------ | -------------- |
| Vipps Teknologi AS | 918130047   | 15038366383    |