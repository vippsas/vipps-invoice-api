#!/bin/env python
import yaml, json

isp_yaml = yaml.safe_load(open("docs/swagger-isp.yaml", "r", encoding="utf-8"))
ipp_yaml = yaml.safe_load(open("docs/swagger-ipp.yaml", "r", encoding="utf-8"))

ipp_json = open("docs/swagger-ipp.json", "w", encoding="utf-8")
isp_json = open("docs/swagger-isp.json", "w", encoding="utf-8")

ipp_json.write(json.dumps(ipp_yaml, indent=2, ensure_ascii=False))
isp_json.write(json.dumps(isp_yaml, indent=2, ensure_ascii=False))
