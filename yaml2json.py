#!/bin/env python
import sys, yaml, json

isp_yaml=yaml.safe_load(file("docs/swagger-isp.yaml","r"))

ipp_yaml=yaml.safe_load(file("docs/swagger-ipp.yaml","r"))

ipp_json = open("docs/swagger-ipp.json", "w")
isp_json = open("docs/swagger-isp.json", "w")

ipp_json.write(json.dumps(ipp_yaml,indent=2))
isp_json.write(json.dumps(isp_yaml,indent=2))


