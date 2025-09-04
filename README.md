# Dota 2 Heroes
![Python](https://img.shields.io/badge/Python-3.11-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54&style=flat-square)
![Scrapy](https://img.shields.io/badge/scrapy-%2360a839.svg?style=for-the-badge&logo=scrapy&logoColor=d1d2d3&style=flat-square)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white&style=flat-square)

## Requirements
Google ChromeDriver local installation.

Python dependencies in "requirements.txt".

## Scraping
Running spiders sequentially with "`run_spiders.py`" script:
1. "`dota2_heroes`" spider extracts data from Dota 2 Heroes webpage and saves it as temporary CSV files.
2. "`dota2_patch`" spider extracts data from Dota 2 Patches webpage and uses it to change every temporary CSV file name and path.

## Parsing
### General
* Texts: paragraphs separated with "`<br>`" to allow better parsing in the future.
* "`hero_id`": extracted from their respective URI.
* Numbers separated by spaces and inclined bars (i.e. "1 / 2"): spaces are removed.

### Hero Basic Info
* "`complexity`": integer numbers 1 (low), 2 (medium) and 3 (high), representing the number of rombs.
* Roles: integer numbers 0, 1, 2 and 3, representing bar width percentages 0%, 33.3%, 66.6% and 99.9%, respectively.
* "`base_attack_damage_min`" and "`base_attack_damage_max`" are extracted from "`damage`".
* "`base_mobility_vision_day`" and "`base_mobility_vision_night`" are extracted from "`vision`".

### Hero Talents
* "`side`": "L" (left) or "R" (right), based on the side of the tree where the talent is found.

### Hero Innate Ability
* "`is_pasive`": boolean field to distinguish if the ability is not pasive, referenced in the Innate as "This hero's innate ability is `<ABILITY>`.".

### Hero Facets
* "`abilities_mod`": a list of the abilities modified by the facet, formed as a string of list of tuples. For (I hope) easy future parsing: attribute name and attribute value are separated by comma, each attribute is separated from the next by double closing parenthesis and each ability is separated by semicolon.
```
"name,value)),description,value))extra_info,value))modifier,joined_modifier_value))modifier,joined_modifier2_value2));name,value))[...];"
```

### Hero Abilities
* "`asset_video`": two video formats available ("webm" and "mp4") that share the same filename, just append the format (".mp4" or ".webm") to the end to form the full link.
* "`shard_scepter`": contains a text if the ability is affected by or is an effect from Shard or Scepter.
* "`info`" and "`modifiers`": formed as a string, each pair name-value is separated by semicolon.
```
"name_and_value;name_and_value;[...];"
```