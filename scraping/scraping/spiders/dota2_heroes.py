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
        self.driver.get(self.start_urls[0])
        time.sleep(2) # Loading JS...
            
        sel = Selector(text=self.driver.page_source)
        hero_uris_xpath = "//a[contains(@class, '_7szOnSgHiQLEyU0_owKBB')]"

        for hero in sel.xpath(hero_uris_xpath):
            self.hero_uris.append(hero.xpath("./@href").get())

        with open("dota2_heroes_7.38c.csv", "w", newline="") as f:
            headers = [
                "id", "name", "main_attribute", "subtitle", "lore",
                "lore_extended", "attack_type", "complexity",
                "lore_extended", "attack_type", "complexity",
                "asset_portrait_url", "base_health", "health_regeneration",
                "base_mana", "mana_regeneration", "base_strength",
                "strength_gain", "base_agility", "agility_gain",
                "base_intelligence", "intelligence_gain", "role_carry",
                "role_support", "role_nuker", "role_disabler",
                "role_jungler", "role_durable", "role_escape", "role_pusher",
                "role_initiator", "base_attack_damage_min",
                "base_attack_damage_max", "base_attack_time",
                "base_attack_range", "base_attack_projectile_speed",
                "base_defense_armor", "base_defense_magic_resist_perc",
                "base_mobility_movement_speed", "base_mobility_turn_rate",
                "base_mobility_vision_day", "base_mobility_vision_night",
            ]
            
            w = csv.DictWriter(f, fieldnames=headers, delimiter='|')
            w.writeheader()
            
            for uri in self.hero_uris[:1]: # TODO: REMOVE LIMIT
                url = f"https://www.dota2.com{uri}"
                self.driver.get(url)
                time.sleep(2) # Loading JS...

                sel = Selector(text=self.driver.page_source)
                id = uri.split('/')[2]
                name = self._extract_html_text(sel, "_2IcIujaWiO5h68dVvpO_tQ")
                main_attribute = self._extract_html_text(
                    sel, "_3HGWJjSyOjmlUGJTIlMHc_"
                )
                subtitle = self._extract_html_text(
                    sel, "_2r7tdOONJnLw_6bQuNZj5b"
                )
                lore = self._extract_lore(sel, "_2z0_hli1W7iUgFJB5fu5m4")

                # Click to expand lore
                self.driver.find_element(
                    By.XPATH, "//div[text()='Read Full History']"
                ).click()
                
                lore_extended = self._extract_lore_extended(
                    sel, "_33H8icML8p8oZrGPMaWZ8o"
                )
                attack_type = self._extract_html_text(
                    sel, "_3ce-DKDrVB7q5LsGbJdZ3X"
                )
                complexity = self._extract_complexity(
                    sel, "_2VXnqvXh1TJPueaGkUNqja"
                )
                asset_portrait_url = self._extract_asset_portrait_url(
                    sel, "CR-BbB851VmrcN5s9HpGZ"
                )
                (
                    base_health, health_regen, base_mana, mana_regen
                ) = self._extract_health_mana(sel)
                (
                    strength, agility, intelligence,
                    strength_gain, agility_gain, intelligence_gain
                ) = self._extract_attributes(sel)
                (
                    role_carry, role_support, role_nuker, role_disabler,
                    role_jungler, role_durable, role_escape, role_pusher,
                    role_initiator
                ) = self._extract_roles(sel)

                (
                    base_attack_damage_min, base_attack_damage_max, base_attack_time,
                    base_attack_range, base_attack_projectile_speed,
                    base_defense_armor, base_defense_magic_resist_perc,
                    base_mobility_movement_speed, base_mobility_turn_rate,
                    base_mobility_vision_day, base_mobility_vision_night
                ) = self._extract_stats(sel)
                
                hero_info = {
                    "id": id,
                    "name": name,
                    "main_attribute": main_attribute,
                    "subtitle": subtitle,
                    "lore": lore,
                    "lore_extended": lore_extended,
                    "attack_type": attack_type,
                    "complexity": complexity,
                    "asset_portrait_url": asset_portrait_url,
                    "base_health": base_health,
                    "health_regeneration": health_regen,
                    "base_mana": base_mana,
                    "mana_regeneration": mana_regen,
                    "base_strength": strength,
                    "strength_gain": strength_gain,
                    "base_agility": agility,
                    "agility_gain": agility_gain,
                    "base_intelligence": intelligence,
                    "intelligence_gain": intelligence_gain,
                    "role_carry": role_carry,
                    "role_support": role_support,
                    "role_nuker": role_nuker,
                    "role_disabler": role_disabler,
                    "role_jungler": role_jungler,
                    "role_durable": role_durable,
                    "role_escape": role_escape,
                    "role_pusher": role_pusher,
                    "role_initiator": role_initiator,
                    "base_attack_damage_min": base_attack_damage_min,
                    "base_attack_damage_max": base_attack_damage_max,
                    "base_attack_time": base_attack_time,
                    "base_attack_range": base_attack_range,
                    "base_attack_projectile_speed": base_attack_projectile_speed,
                    "base_defense_armor": base_defense_armor,
                    "base_defense_magic_resist_perc": base_defense_magic_resist_perc,
                    "base_mobility_movement_speed": base_mobility_movement_speed,
                    "base_mobility_turn_rate": base_mobility_turn_rate,
                    "base_mobility_vision_day": base_mobility_vision_day,
                    "base_mobility_vision_night": base_mobility_vision_night,
                }

                w.writerow(hero_info)
                time.sleep(1) # Wait before going next...

        self.driver.quit()


    @staticmethod
    def _extract_html_text(sel, container_class):
        return sel.xpath(
            f"//div[contains(@class, '{container_class}')]/text()"
        ).get()


    @staticmethod
    def _extract_lore(sel, container_class):
        inner_class = "_1FdISYFSn4ZmiR_wS5YFOM"

        base = f"//div[contains(@class, '{container_class}')]/div[contains(@class, '{inner_class}')]"
        text_parts = sel.xpath(f"{base}/text() | {base}/span/text()").getall()

        return process_text(text_parts)
    

    @staticmethod
    def _extract_lore_extended(sel, container_class):
        text_parts = sel.xpath(
            f"//div[contains(@class, '{container_class}')]/div[1]//text()"
        ).getall()

        return process_text(text_parts)


    @staticmethod
    def _extract_complexity(sel, container_class):
        """
        This info is showed as rombs (1, 2 or 3), return their count.
        """
        return len(
            sel.xpath(
                f"//div[contains(@class, '{container_class}')]"
            ).getall()
        )
    

    @staticmethod
    def _extract_asset_portrait_url(sel, container_class):
        return sel.xpath(
            f"//img[contains(@class, '{container_class}')]/@src"
        ).get()
    

    @staticmethod
    def _extract_health_mana(sel):
        """
        Health and Mana info got the same classes for the main divs where the numbers are contained.
        """
        def extract(container_class, target_class):
            path = f"""
                //div[contains(@class, '{container_class}')]
                /div[contains(@class, '{target_class}')]
                /text()
                """
            
            return sel.xpath(path).get(default="0").strip()
        
        health_container_class="D6gmc38sczQBtacU66_b4"
        mana_container_class="_1aQk6qbzk9zHJ78eUNwzw1"

        container_class_base = "_1KbXKSmm_4JCzoVx_nG7HJ"
        container_class_regen = "_29Uub-BkYZWm7hCAL7QRx3"

        base_health = int(
            extract(health_container_class, container_class_base)
        )
        health_regen = float(
            extract(health_container_class, container_class_regen)
        )
        base_mana = int(
            extract(mana_container_class, container_class_base)
        )
        mana_regen = float(
            extract(mana_container_class, container_class_regen)
        )

        return base_health, health_regen, base_mana, mana_regen
        
    
    @staticmethod
    def _extract_attributes(sel):
        """
        Extracting the three main attributes, they share class. As do their gains.
        Main attributes are integers. Attribute gains are decimals.
        """
        def extract(container_class):
            return sel.xpath(
                f"//div[contains(@class, '{container_class}')]//text()"
            ).getall()
        
        attributes_class = "_3Gsggcx9qe3qVMxUs_XeOo"
        attributes_gain_class = "DpX1zhKaVPKBeFg4KrB0B"

        attributes = extract(attributes_class)
        attributes_gain = extract(attributes_gain_class)

        strength = int(attributes[0])
        agility = int(attributes[1])
        intelligence = int(attributes[2])
        strength_gain = float(attributes_gain[0])
        agility_gain = float(attributes_gain[1])
        intelligence_gain = float(attributes_gain[2])

        return (
            strength, agility, intelligence,
            strength_gain, agility_gain, intelligence_gain
        )
    

    @staticmethod
    def _extract_roles(sel):
        """
        Extracting the nine roles.
        They are displayed as a bar, using widths: 0%, 33.3%, 66.6% and 100%.
        Parsing as integers: 0, 1, 2 and 3.
        """
        container_class = "_3zWGygZT2aKUiOyokg4h1v"
        role_name_class = "_3Fbk3tlFp8wcznxtXIx19W"
        role_bar_class = "_28Sbu0ESGRjIMkyucAEAVz"
        role_bar_value_class = "f7kjDBQOuPqiwaCTUPzLJ"

        roles = {}
        match_percentage_value = {
            0.0: 0,
            33.3: 1,
            66.6: 2,
            100.0: 3,
        }

        containers = sel.xpath(
            f"//div[contains(@class, '{container_class}')]"
        )

        for container in containers:
            style = container.xpath(
                f"""
                .//div[contains(@class, '{role_bar_class}')]
                /div[contains(@class, '{role_bar_value_class}')]
                /@style
                """
            ).get()
            percentage = float(style.replace("width: ", "").replace("%;", ""))
            value = match_percentage_value[percentage]
            role_name = container.xpath(
                f".//div[contains(@class, '{role_name_class}')]/text()"
            ).get()
            roles[role_name] = value

        return (
            roles["Carry"], roles["Support"], roles["Nuker"],
            roles["Disabler"], roles["Jungler"], roles["Durable"],
            roles["Escape"], roles["Pusher"], roles["Initiator"]
        )


    @staticmethod
    def _extract_stats(sel):
        """
        Extracting stats (grouped in Attack, Defense and Mobility).
        """
        container_class = "_3z1y6d2ebz2SLSb7zqA1qU"
        stats_container_class = "_3ulLBWWM4rZynWFlj9MsLe"
        stat_class = "_3783Tb-SbeUvvdBW9iSB_x"

        stats = sel.xpath(
            f"""
            //div[contains(@class, '{container_class}')]
            /div[contains(@class, '{stats_container_class}')]
            /div[contains(@class, '{stat_class}')]
            /text()
            """
        ).getall()

        base_attack = stats[0].split('-')
        (
            base_attack_damage_min, base_attack_damage_max
        ) = int(base_attack[0]), int(base_attack[1])
        base_attack_time = float(stats[1])
        base_attack_range = int(stats[2])
        base_attack_projectile_speed = int(stats[3])
        base_defense_armor = float(stats[4])
        base_defense_magic_resist_perc = int(stats[5].replace("%", ""))
        base_mobility_movement_speed = int(stats[6])
        base_mobility_turn_rate = float(stats[7])
        vision = stats[8].split(" / ")
        (
            base_mobility_vision_day, base_mobility_vision_night
        ) = int(vision[0]), int(vision[1])

        return (
            base_attack_damage_min, base_attack_damage_max, base_attack_time,
            base_attack_range, base_attack_projectile_speed,
            base_defense_armor, base_defense_magic_resist_perc,
            base_mobility_movement_speed, base_mobility_turn_rate,
            base_mobility_vision_day, base_mobility_vision_night
        )


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
