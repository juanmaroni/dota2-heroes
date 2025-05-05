# Dota 2 Heroes
![Python](https://img.shields.io/badge/Python-3.11-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54&style=flat-square)
![Scrapy](https://img.shields.io/badge/scrapy-%2360a839.svg?style=for-the-badge&logo=scrapy&logoColor=d1d2d3&style=flat-square)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white&style=flat-square)

## Requirements
Google ChromeDriver local installation.

Python dependencies in "requirements.txt".

## Scraping
Running spiders sequentially:
1. "`dota2_heroes`" spider extracts data from Dota 2 Heroes webpage and saves it as a temporary CSV file.
2. "`dota2_patch`" spider extracts data from Dota 2 Patches webpage and uses it to change every temporary CSV file name and path.

## Parsing
### General
* Texts: paragraphs separated with "`<br>`" to allow better parsing in the future.

### Hero Basic Info
* "`complexity`": integer numbers 1 (low), 2 (medium) and 3 (high), representing the number of rombs.
* Roles: integer numbers 0, 1, 2 and 3, representing bar percentages 0%, 33.3%, 66.6% and 99.9%, respectively.
* "`base_attack_damage_min`" and "`base_attack_damage_max`" are extracted from "`damage`".
* "`base_mobility_vision_day`" and "`base_mobility_vision_night`" are extracted from "`vision`".

### Hero Talents
* "`side`": "L" (left) or "R" (right), based on the side of the tree where the talent is found.

### Hero Innate Ability
* "`is_pasive`": boolean field to distinguish if the ability is not pasive, referenced in the Innate as "This hero's innate ability is <ABILITY>.".
