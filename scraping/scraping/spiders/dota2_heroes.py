import csv
import time
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class Dota2HeroesSpider(scrapy.Spider):
    name = "dota2_heroes"
    allowed_domains = ["www.dota2.com"]
    start_urls = ["https://www.dota2.com/heroes"]
    hero_uris = []

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
        for url in self.start_urls:
            self.driver.get(url)
            time.sleep(2) # Loading JS...
            
            sel = Selector(text=self.driver.page_source)

            for hero in sel.xpath("//a[contains(@class, '_7szOnSgHiQLEyU0_owKBB')]"):
                self.hero_uris.append(hero.xpath("./@href").get())

        for uri in self.hero_uris:
            url = f"https://www.dota2.com{uri}"
            self.driver.get(url)
            time.sleep(2) # Loading JS...

            sel = Selector(text=self.driver.page_source)
            lore = self._extract_lore(sel, "_2z0_hli1W7iUgFJB5fu5m4")

            # Click to expand lore
            self.driver.find_element(By.XPATH, "//div[text()='Read Full History']").click()
            
            lore_extended = self._extract_lore_extended(sel, "_33H8icML8p8oZrGPMaWZ8o")
            base_health, health_regen, base_mana, mana_regen = self._extract_health_mana(sel)

            hero_info = {
                "id": uri.split('/')[2],
                "name": self._extract_html_text(sel, "_2IcIujaWiO5h68dVvpO_tQ"),
                "main_attribute": self._extract_html_text(sel, "_3HGWJjSyOjmlUGJTIlMHc_"),
                "subtitle": self._extract_html_text(sel, "_2r7tdOONJnLw_6bQuNZj5b"),
                "lore": lore,
                "lore_extended": lore_extended,
                "attack_type": self._extract_html_text(sel, "_3ce-DKDrVB7q5LsGbJdZ3X"),
                "complexity": self._extract_complexity(sel, "_2VXnqvXh1TJPueaGkUNqja"),
                "asset_portrait_url": self._extract_asset_portrait_url(sel, "CR-BbB851VmrcN5s9HpGZ"),
                "base_health": base_health,
                "health_regeneration": health_regen,
                "base_mana": base_mana,
                "mana_regeneration": mana_regen,
                "base_strength": "",
                "strength_gain": "",
                "base_agility": "",
                "agility_gain": "",
                "base_intelligence": "",
                "intelligence_gain": "",
                "role_carry": "",
                "role_support": "",
                "role_nuker": "",
                "role_disabler": "",
                "role_jungler": "",
                "role_durable": "",
                "role_escape": "",
                "role_pusher": "",
                "role_initiator": "",
                "attack_damage": "",
                "attack_time": "",
                "attack_range": "",
                "attack_projectile_speed": "",
                "defense_armor": "",
                "defense_magic_resist": "",
                "mobility_movement_speed": "",
                "mobility_turn_rate": "",
                "mobility_vision_day": "",
                "mobility_vision_night": "",
            }

            with open("test_heroes.csv", "w", newline="") as f:
                w = csv.DictWriter(f, hero_info.keys(), delimiter='|')
                w.writeheader()
                w.writerow(hero_info)

            break

        self.driver.quit()


    @staticmethod
    def _extract_html_text(sel, html_class):
        return sel.xpath(f"//div[contains(@class, '{html_class}')]/text()").get()


    @staticmethod
    def _extract_lore(sel, container_class):
        inner_class = "_1FdISYFSn4ZmiR_wS5YFOM"

        base = f"//div[contains(@class, '{container_class}')]/div[contains(@class, '{inner_class}')]"
        text_parts = sel.xpath(f"{base}/text() | {base}/span/text()").getall()

        return process_text(text_parts)
    

    @staticmethod
    def _extract_lore_extended(sel, container_class):
        text_parts = sel.xpath(f"//div[contains(@class, '{container_class}')]/div[1]//text()").getall()

        return process_text(text_parts)


    @staticmethod
    def _extract_complexity(sel, html_class):
        """
        This info is showed as rombs (1, 2 or 3), return their count.
        """
        return len(sel.xpath(f"//div[contains(@class, '{html_class}')]").getall())
    

    @staticmethod
    def _extract_asset_portrait_url(sel, html_class):
        return sel.xpath(f"//img[contains(@class, '{html_class}')]/@src").get()
    

    @staticmethod
    def _extract_health_mana(sel):
        """
        Health and Mana info got the same classes for the main divs where the numbers are contained.
        """
        def extract(container_class, target_class):
            path = f"//div[contains(@class, '{container_class}')]/div[contains(@class, '{target_class}')]/text()"
            
            return sel.xpath(path).get(default="0").strip()
        
        html_class_health="D6gmc38sczQBtacU66_b4"
        html_class_mana="_1aQk6qbzk9zHJ78eUNwzw1"

        html_class_base = "_1KbXKSmm_4JCzoVx_nG7HJ"
        html_class_regen = "_29Uub-BkYZWm7hCAL7QRx3"

        base_health = int(extract(html_class_health, html_class_base))
        health_regen = float(extract(html_class_health, html_class_regen))
        base_mana = int(extract(html_class_mana, html_class_base))
        mana_regen = float(extract(html_class_mana, html_class_regen))

        return base_health, health_regen, base_mana, mana_regen
        
    
    @staticmethod
    def _extract_attributes():
        pass


    @staticmethod
    def _extract_vision():
        """
        Two numbers separated by inclined bar.
        """
        pass
        # return day, night


def process_text(text_parts):
        """
        Process extracted text divided in parts.
        """
        full_text = " ".join(text_parts)
        
        processed_text = (
            full_text
                .replace("\t", "")
                .replace("\r", "<br>")
                .replace("\n", "<br>")
                .strip()
                .replace(" ,", ",")
                .replace(" .", ".")
                .replace(" ;", ";")
                .replace(" !", "!")
                .replace(" ?", "?")
                .replace("<br> ", "<br>")
                .replace("  ", " ")
        )

        return processed_text
