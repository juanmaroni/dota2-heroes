from sys import exit
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraping.spiders import Dota2PatchSpider, Dota2HeroesSpider


def run_spiders_sequentially():
    process = CrawlerProcess(get_project_settings())  
    d = process.crawl(Dota2HeroesSpider)
    d.addCallback(lambda _: process.crawl(Dota2PatchSpider))
    d.addBoth(lambda _: process.stop())
    process.start()


if __name__ == "__main__":
    run_spiders_sequentially()

    exit(0)
