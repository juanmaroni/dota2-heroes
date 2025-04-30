import time
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from scraping.items import PatchItem


class Dota2PatchSpider(scrapy.Spider):
    name = "dota2_patch"
    allowed_domains = ["www.dota2.com"]
    start_urls = ["https://www.dota2.com/patches"]
    version = ""

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

    def parse(self, response):
        self.driver.get(self.start_urls[0])
        time.sleep(2) # Loading JS...
        
        sel = Selector(text=self.driver.page_source)
        patch = PatchItem()
        patch_select_class = "_3e0NMgHFoFIu9xmuHWrZD1"
        patch_version = sel.xpath(
            f"""
            //select[contains(@class, '{patch_select_class}')]
            /option[1]
            /@value
            """
        ).get()

        self.version = patch_version
        yield patch
