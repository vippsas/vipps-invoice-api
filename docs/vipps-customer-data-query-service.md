# Vipps Customer Data Query Service

This is the documentation for the **Vipps Customer Data Query Service** that can be used in conjunction with the [**Vipps Invoice API**](vipps-invoice-api.md) to ensure that you send the invoice to the correct recipient.

# Overview

## Table of Contents


## External documentation

Documentation written by Evry can be found on [https://www.infotorg.no/partners-portal/main-page](https://www.infotorg.no/partners-portal/main-page)

## Getting access to the Vipps Customer Data Query Service

Applying for an account is done by going to [https://www.infotorg.no/partners-portal/main-page](https://www.infotorg.no/partners-portal/main-page) and clicking on the "Become a partner" button and filling out the form.


## Information about alternative solutions

There are two ways to utilize the Vipps Customer Data Query Service

* Online web service (SOAP)
* Batch service (Tab separated text file through SFTP)

Vipps has no preference to which of these two solutions are used, it will be entirely up to you which fits best into your workflow.

## Alternative 1: Online web service

### Testing of online web service 

Testing can be done by logging in to [https://ws-test.infotorg.no/ws/login.pl](https://ws-test.infotorg.no/ws/login.pl) and try to run your SOAP queries.
It's recommended to have "batches" of no more than 1000 entries for this particular service.

## Alternative 2: Batch services

### Testing of batch services

Upload a tab separated file to the SFTP, and should it fail you will receive an e-mail sometime later from Evry about what went wrong.
From a testing perspective this is quite a bit slower than using the online web service using SOAP. However Tab-separated files are quite a bit simpler than SOAP, and the batches can be bigger.
