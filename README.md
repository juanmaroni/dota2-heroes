# Dota 2 Heroes
![Python](https://img.shields.io/badge/Python-3.11-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54&style=flat-square)
![Scrapy](https://img.shields.io/badge/scrapy-%2360a839.svg?style=for-the-badge&logo=scrapy&logoColor=d1d2d3&style=flat-square)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white&style=flat-square)

## Scraping
Extracting data from Dota 2 Heroes webpage with Scrapy and Selenium, and saving it as a CSV file.

Notes about parsing:
* "`lore`" and "`lore_extended`": paragraphs separated with "`<br>`" to allow better parsing in the future.
* "`complexity`": integer numbers 1 (low), 2 (medium) and 3 (high), representing the number of rombs.
* "`role_<ROLE_NAME>`": integer numbers 0, 1, 2 and 3, representing bar percentages 0%, 33.3%, 66.6% and 100%, respectively.
