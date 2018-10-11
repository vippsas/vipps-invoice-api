#!/bin/env python

import re
import sys
import yaml
import json
import os

if len(sys.argv) != 2:
    print('Usage: python3 newchange.py <change description>')
    sys.exit(2)

change_description = sys.argv[1]

readme = open('README.md', 'r')
readme_content = readme.read()
readme.close()

rx = re.compile('# Swagger changelog\s+## (\d{1,3})[.](\d{1,3})[.](\d{1,3})', re.MULTILINE)
m = rx.search(readme_content)
current_version_major = m.group(1)
current_version_minor = m.group(2)
current_version_build = m.group(3)
current_version = f'{current_version_major}.{current_version_minor}.{current_version_build}'
print('Current version: ' + current_version)

next_version_build = str(int(current_version_build) + 1)
next_version = f'{current_version_major}.{current_version_minor}.{next_version_build}'
print('Next version: ' + next_version)

rx = re.compile('# Swagger changelog\s', re.MULTILINE)

new_changelog = f'## {next_version}\n\n* {change_description}'
readme_new_changelog = readme_content.replace('# Swagger changelog', f'# Swagger changelog\n\n{new_changelog}')

#print(readme_new_changelog)

print(f'\nUpdating README.md with new changelog:\n\n {new_changelog}')
readme = open('README.md', 'w')
readme.write(readme_new_changelog)
readme.close()

print(f'Updating the Swagger YAML-files with new version {next_version}')
# ISP
isp_yaml_text = open("docs/swagger-isp.yaml", "r", encoding="utf-8").read()
isp_yaml_text = isp_yaml_text.replace(f"version: '{current_version}'", f"version: '{next_version}'")
with open("docs/swagger-isp.yaml", "w", encoding="utf-8") as fp:
    fp.write(isp_yaml_text)

# IPP
ipp_yaml_text = open("docs/swagger-ipp.yaml", "r", encoding="utf-8").read()
ipp_yaml_text = ipp_yaml_text.replace(f"version: '{current_version}'", f"version: '{next_version}'")
with open("docs/swagger-ipp.yaml", "w", encoding="utf-8") as fp:
    fp.write(ipp_yaml_text)

print('Updating the Swagger JSON-files ...')
isp_yaml = yaml.safe_load(open("docs/swagger-isp.yaml", "r", encoding="utf-8"))
ipp_yaml = yaml.safe_load(open("docs/swagger-ipp.yaml", "r", encoding="utf-8"))

ipp_json = open("docs/swagger-ipp.json", "w", encoding="utf-8")
isp_json = open("docs/swagger-isp.json", "w", encoding="utf-8")

ipp_json.write(json.dumps(ipp_yaml, indent=2, ensure_ascii=False))
isp_json.write(json.dumps(isp_yaml, indent=2, ensure_ascii=False))

os.system(f'git add . && git commit -m "New version {next_version}: {change_description}"')
