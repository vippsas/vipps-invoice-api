#!/bin/env python

import re

change_description = 'This is a change'

readme = open('README.md', 'r')
readme_content = readme.read()

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

readme_new_changelog = readme_content.replace('# Swagger changelog', f'# Swagger changelog\n\n## {next_version}\n\n* {change_description}')

print(readme_new_changelog)