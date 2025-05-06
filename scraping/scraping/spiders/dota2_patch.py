import time
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from scraping.items import PatchItem
from utils import (
    CHROMEDRIVER_PATH, TMP_HEROES_INFO_FILENAME,
    TMP_HEROES_TALENTS_FILENAME, TMP_HEROES_INNATE_FILENAME,
    change_filepath
)


class Dota2PatchSpider(scrapy.Spider):
    name = "dota2_patch"
    allowed_domains = ["www.dota2.com"]
    start_urls = ["https://www.dota2.com/patches"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            service=Service(CHROMEDRIVER_PATH),
            options=chrome_options
        )

    def parse(self, response):
        self.driver.get(self.start_urls[0])
        time.sleep(2)  # Loading JS...
        
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

        patch["version"] = patch_version

        # Change every temporary CSV file name and path
        new_filename = f"dota2_heroes_info_{patch_version}.csv"
        change_filepath(
            filename=TMP_HEROES_INFO_FILENAME,
            new_filename=new_filename
        )

        new_filename = f"dota2_heroes_talents_{patch_version}.csv"
        change_filepath(
            filename=TMP_HEROES_TALENTS_FILENAME,
            new_filename=new_filename
        )

        new_filename = f"dota2_heroes_innate_{patch_version}.csv"
        change_filepath(
            filename=TMP_HEROES_INNATE_FILENAME,
            new_filename=new_filename
        )
        
        # yield patch
