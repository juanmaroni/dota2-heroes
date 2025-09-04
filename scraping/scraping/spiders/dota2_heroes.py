import time
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from scraping.items import (
    HeroInfoItem, HeroTalentItem, HeroInnateItem, HeroFacetItem,
    HeroAbilityItem
)
from utils import CHROMEDRIVER_PATH


class Dota2HeroesSpider(scrapy.Spider):
    name = "dota2_heroes"
    allowed_domains = ["www.dota2.com"]
    start_urls = ["https://www.dota2.com/heroes"]

    def __init__(self):
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
        hero_uris_class = "_7szOnSgHiQLEyU0_owKBB"
        hero_uris_xpath = f"""
            //a[contains(@class, '{hero_uris_class}')]/@href
        """
        
        for uri in sel.xpath(hero_uris_xpath).getall():
            url = f"https://www.dota2.com{uri}"
            self.driver.get(url)
            time.sleep(2)  # Loading JS...

            hero_id = uri.split('/')[2]
            sel = Selector(text=self.driver.page_source)

            # Hero basic info
            yield self._extract_hero_info(sel, hero_id)

            # Hero Talent Tree
            for talent in self._extract_talents(sel, hero_id):
                yield talent

            # Hero Innate Ability
            yield self._extract_innate_ability(sel, hero_id)

            # Hero Facets
            for facet in self._extract_facets(sel, hero_id):
                yield facet

            # Hero Abilities
            for ability in self._extract_abilities(sel, hero_id):
                yield ability
            
            time.sleep(1)  # Wait before going next...

        self.driver.quit()

    def _extract_hero_info(self, sel, hero_id):
        hero_info = HeroInfoItem()
        hero_info["id"] = hero_id
        hero_info["name"] = self._extract_html_text(
            sel, "_2IcIujaWiO5h68dVvpO_tQ"
        )
        hero_info["main_attribute"] = self._extract_html_text(
            sel, "_3HGWJjSyOjmlUGJTIlMHc_"
        )
        hero_info["subtitle"] = self._extract_html_text(
            sel, "_2r7tdOONJnLw_6bQuNZj5b"
        )
        hero_info["lore"] = self._extract_lore(sel, "_2z0_hli1W7iUgFJB5fu5m4")

        # Click to expand lore
        self.driver.find_element(
            By.XPATH, "//div[text()='Read Full History']"
        ).click()
                
        hero_info["lore_extended"] = self._extract_lore_extended(
            sel, "_33H8icML8p8oZrGPMaWZ8o"
        )
        hero_info["attack_type"] = self._extract_html_text(
            sel, "_3ce-DKDrVB7q5LsGbJdZ3X"
        )
        hero_info["complexity"] = self._extract_complexity(
            sel, "_2VXnqvXh1TJPueaGkUNqja"
        )
        hero_info["asset_portrait_url"] = self._extract_asset_portrait_url(
            sel, "CR-BbB851VmrcN5s9HpGZ"
        )
        (
            hero_info["base_health"], hero_info["health_regeneration"],
            hero_info["base_mana"], hero_info["mana_regeneration"]
        ) = self._extract_health_mana(sel)
        (
            hero_info["base_strength"], hero_info["base_agility"],
            hero_info["base_intelligence"], hero_info["strength_gain"],
            hero_info["agility_gain"], hero_info["intelligence_gain"]
        ) = self._extract_attributes(sel)
        (
            hero_info["role_carry"], hero_info["role_support"],
            hero_info["role_nuker"], hero_info["role_disabler"],
            hero_info["role_jungler"], hero_info["role_durable"],
            hero_info["role_escape"], hero_info["role_pusher"],
            hero_info["role_initiator"]
        ) = self._extract_roles(sel)
        (
            hero_info["damage"], hero_info["attack_time"],
            hero_info["attack_range"], hero_info["projectile_speed"],
            hero_info["armor"], hero_info["magic_resist"],
            hero_info["movement_speed"], hero_info["turn_rate"],
            hero_info["vision"]
        ) = self._extract_stats(sel)

        return hero_info

    @staticmethod
    def _extract_html_text(sel, container_class):
        return sel.xpath(
            f"//div[contains(@class, '{container_class}')]/text()"
        ).get()

    @staticmethod
    def _extract_lore(sel, container_class):
        inner_class = "_1FdISYFSn4ZmiR_wS5YFOM"

        base = f"""
            //div[contains(@class, '{container_class}')]
            /div[contains(@class, '{inner_class}')]
        """
        text_parts = sel.xpath(f"{base}/text() | {base}/span/text()").getall()  # TODO: Refactor, /text => //text

        return text_parts
    
    @staticmethod
    def _extract_lore_extended(sel, container_class):
        text_parts = sel.xpath(
            f"//div[contains(@class, '{container_class}')]/div[1]//text()"
        ).getall()

        return text_parts

    @staticmethod
    def _extract_complexity(sel, container_class):
        """
        This info is showed as rombs (1, 2 or 3).
        """
        return sel.xpath(
            f"//div[contains(@class, '{container_class}')]"
        ).getall()

    @staticmethod
    def _extract_asset_portrait_url(sel, container_class):
        return sel.xpath(
            f"//img[contains(@class, '{container_class}')]/@src"
        ).get()

    @staticmethod
    def _extract_health_mana(sel):
        """
        Health and Mana info got the same classes for
        the main divs where the numbers are contained.
        """
        def extract(container_class, target_class):
            path = f"""
                //div[contains(@class, '{container_class}')]
                /div[contains(@class, '{target_class}')]
                /text()
                """
            
            return sel.xpath(path).get(default="0").strip()
        
        health_container_class = "D6gmc38sczQBtacU66_b4"
        mana_container_class = "_1aQk6qbzk9zHJ78eUNwzw1"

        container_class_base = "_1KbXKSmm_4JCzoVx_nG7HJ"
        container_class_regen = "_29Uub-BkYZWm7hCAL7QRx3"

        base_health = extract(health_container_class, container_class_base)
        health_regen = extract(health_container_class, container_class_regen)
        base_mana = extract(mana_container_class, container_class_base)
        mana_regen = extract(mana_container_class, container_class_regen)

        return base_health, health_regen, base_mana, mana_regen
        
    @staticmethod
    def _extract_attributes(sel):
        """
        Main attributes are integers. Attribute gains are decimals.
        Extracted in this order: "strength", "agility", "intelligence",
        "strength_gain", "agility_gain" and "intelligence_gain"
        """
        def extract(container_class):
            return sel.xpath(
                f"//div[contains(@class, '{container_class}')]//text()"
            ).getall()
        
        attributes_class = "_3Gsggcx9qe3qVMxUs_XeOo"
        attributes_gain_class = "DpX1zhKaVPKBeFg4KrB0B"

        attributes = extract(attributes_class)
        attributes_gain = extract(attributes_gain_class)

        return (
            attributes[0], attributes[1], attributes[2],
            attributes_gain[0], attributes_gain[1], attributes_gain[2]
        )

    @staticmethod
    def _extract_roles(sel):
        """
        They are displayed as a bar, using widths: 0%, 33.3%, 66.6% and 99.9%.
        """
        container_class = "_3zWGygZT2aKUiOyokg4h1v"
        role_name_class = "_3Fbk3tlFp8wcznxtXIx19W"
        role_bar_class = "_28Sbu0ESGRjIMkyucAEAVz"
        role_bar_value_class = "f7kjDBQOuPqiwaCTUPzLJ"

        roles = {}

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
            percentage = style.replace("width: ", "").replace("%;", "")
            role_name = container.xpath(
                f".//div[contains(@class, '{role_name_class}')]/text()"
            ).get()
            roles[role_name] = percentage

        return (
            roles["Carry"], roles["Support"], roles["Nuker"],
            roles["Disabler"], roles["Jungler"], roles["Durable"],
            roles["Escape"], roles["Pusher"], roles["Initiator"]
        )

    @staticmethod
    def _extract_stats(sel):
        """
        Extracting stats (grouped in Attack, Defense and Mobility).
        Some heroes may not have all the stats, decided to use a dict.
        Keys are extracted from images src: "damage", "attack_time",
        "attack_range", "projectile_speed", "armor", "magic_resist",
        "movement_speed", "turn_rate" and "vision".
        """
        def extract_key_from_img(img_src):
            r1 = "https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react//heroes/stats/icon_"
            r2 = ".png"
            
            return (
                img_src
                    .replace(r1, "")
                    .replace(r2, "")
            )

        container_class = "_3z1y6d2ebz2SLSb7zqA1qU"
        stats_container_class = "_3ulLBWWM4rZynWFlj9MsLe"
        stat_class = "_3783Tb-SbeUvvdBW9iSB_x"
        img_class = "FY7TWJ3yQgg0zRhmd0sjL"

        stats_xpath = (
            f"""
            //div[contains(@class, '{container_class}')]
            /div[contains(@class, '{stats_container_class}')]
            /div[contains(@class, '{stat_class}')]
            """
        )

        stats = {
            "damage": None,
            "attack_time": None,
            "attack_range": None,
            "projectile_speed": None,
            "armor": None,
            "magic_resist": None,
            "movement_speed": None,
            "turn_rate": None,
            "vision": None,
        }

        for stat in sel.xpath(stats_xpath):
            k = extract_key_from_img(
                stat.xpath(
                    f".//img[contains(@class, '{img_class}')]/@src"
                ).get()
            )
            v = stat.xpath(".//text()").get()
            stats[k] = v

        magic_resist = stats["magic_resist"]
        magic_resist = magic_resist.replace("%", "") if magic_resist else None

        return (
            stats["damage"], stats["attack_time"], stats["attack_range"],
            stats["projectile_speed"], stats["armor"], magic_resist,
            stats["movement_speed"], stats["turn_rate"], stats["vision"]
        )

    @staticmethod
    def _extract_talents(sel, hero_id):
        """
        Extract talents from Talent Tree.
        From highest level left to lowest level right.
        """
        talent_container_class = "_1SJ4JZrp7rwc6FG-vINkFn"

        containers = sel.xpath(
            f"//div[contains(@class, '{talent_container_class}')]/text()"
        ).getall()
        
        talents = []
        side = "L"  # Left or Right
        level = 25  # 25, 20, 15 or 10

        # They are extracted dupped, only first 8 results are needed
        for talent in containers[:8]:
            talent_tree_item = HeroTalentItem()
            talent_tree_item["hero_id"] = hero_id
            talent_tree_item["side"] = side
            talent_tree_item["level"] = level
            talent_tree_item["talent"] = talent

            if side == "R":
                level -= 5
                side = "L"
            else:
                side = "R"

            talents.append(talent_tree_item)
        
        return talents

    @staticmethod
    def _extract_innate_ability(sel, hero_id):
        """
        Some heroes Innate Ability is part of their set of Abilities.
        Stated as: "This hero's innate ability is <ABILITY>."
        In this case, that referenced <ABILITY> will be saved as the Innate.
        If referenced this way, it's not considered as pasive (boolean field).
        'innate_description' is returned as a list for further processing.
        """
        innate = HeroInnateItem()
        innate["hero_id"] = hero_id

        str_no_pasive = "This hero's innate ability is "

        innate_container_class = "_10lc5aoHOP5BafKhDC_AuD"
        innate_name_class = "oRzqVIPO5vD9aPxv582G9"
        innate_description_class = "_1GUxaKU8ts0aIJaMfIfMS_"

        innate_container = sel.xpath(
            f"//div[contains(@class, '{innate_container_class}')][1]"
        )

        innate_name = None
        innate_description = innate_container.xpath(
            f"./div[contains(@class, '{innate_description_class}')]/text()"
        ).get()

        if innate_description.find(str_no_pasive) != -1:
            innate["is_pasive"] = False

            # Extract Ability name
            ability_name = (
                innate_description.replace(str_no_pasive, "").replace(".", "")
            )

            # Find Ability by name and extract description ('div' sibling)
            innate_description = sel.xpath(
                f"""
                //div[contains(@class, '{innate_container_class}')]
                /div[contains(text(), '{ability_name}')]
                /following-sibling::div[1]
                /text()
                """
            ).getall()

            innate_name = ability_name
        else:
            innate["is_pasive"] = True
            innate_name = innate_container.xpath(
                f"./div[contains(@class, '{innate_name_class}')]/text()"
            ).get()
            innate_description = [innate_description]

        innate["name"] = innate_name
        innate["description"] = innate_description

        return innate

    @staticmethod
    def _extract_facets(sel, hero_id):
        """
        Tricky one, it needs a lot of structure.
        Leaving processing operations for pipeline.
        """
        def extract_text(container, text_class): #TODO: Rename?
            return container.xpath(
                f".//div[contains(@class, '{text_class}')]/text()"
            ).get()
        
        facet_container_class = "swTQdhtrGo5VPAWX79ypS"
        facet_icon_class = "_2TU3iaSQNM_bkJ0Q6b1k--"
        facet_name_class = "_2xP5NA5_6wvIi3RMr55wKs"
        facet_description_class = "_10lc5aoHOP5BafKhDC_AuD"
        facet_extra_info_class = "_2tOvRyMjowK6qLedqmX1Hg"
        ability_mod_container_class = "a_RaGMuwR0xmpXfOqqxtT"
        ability_mod_name_class = "_1rBGHCdy0eU5X2K5p3xSVY"
        ability_mod_description_class = "_3Dysl5QeWoPG896gAaaneB"
        ability_mod_modifiers_class = "-imZKoGzT42UnYw7DuttJ"
        ability_mod_values_class = "_2QMshVtQuTsk_ZU7iBaUE2"

        facet_containers = sel.xpath(
            f"//div[contains(@class, '{facet_container_class}')]"
        )

        facets = []

        for container in facet_containers:
            facet = HeroFacetItem()
            facet["asset_icon"] = container.xpath(
                f".//img[contains(@class, '{facet_icon_class}')]/@src"
            ).get()
            facet["name"] = extract_text(container, facet_name_class)
            facet["description"] = Dota2HeroesSpider.extract_every_text(
                container, facet_description_class
            )
            facet["extra_info"] = extract_text(
                container, facet_extra_info_class
            )
            facet["hero_id"] = hero_id

            abilities_mod_list = []
            abilities_mod = container.xpath(
                f".//div[contains(@class, '{ability_mod_container_class}')]"
            )

            # Abilities modifiers
            for a in abilities_mod:
                ability = {}
                ability["name"] = extract_text(a, ability_mod_name_class)
                ability["description"] = Dota2HeroesSpider.extract_every_text(
                    a, ability_mod_description_class
                )
                
                # Modifiers will be paired correctly in pipeline
                ability["modifiers"] = a.xpath(
                    f"""
                    .//div[contains(@class, '{ability_mod_modifiers_class}')]
                    /text()
                    """
                ).getall()
                ability["modifiers_values"] = a.xpath(
                    f"""
                    .//div[contains(@class, '{ability_mod_values_class}')]
                    /text()
                    """
                ).getall()

                abilities_mod_list.append(ability)

            facet["abilities_mod"] = abilities_mod_list
            facets.append(facet)

        return facets
    
    def _extract_abilities(self, sel, hero_id):
        """
        Abilities are displayed hidden behind clicks.
        """
        icon_click_container_class = "_1vjw5Sik8Zewkj5_iOhCUb"
        icon_click_class = "_3Chop4A9yz7Af_BwR1r_NW"

        click_elements = self.driver.find_elements(
            By.XPATH,
            f"""
            //div[contains(@class, '{icon_click_container_class}')]
            /div[contains(@class, '{icon_click_class}')]
            """
        )

        section_container_class = "_1yoiZcdOJEKeKgQjATrVPZ"
        video_class = "_22nJ5nsfHDS2jEscPEne0-"
        icon_img_class = "_171zqqZ6uSu-ZpGvphLmVH"
        ability_info_container_class = "_3y3LGmwmRlDIBT6U-pzn9c"
        ability_name_class = "_1rBGHCdy0eU5X2K5p3xSVY"
        ability_scepter_shard_class = "_1RDBbyc4Z_-Rjv_xphicMA"
        ability_description_class = "CjmI9ZAN4c9C4Rj-IPpzc"
        ability_info_class = "_2dsmbR3Wyt5DkOJWLbMsRh"
        ability_modifiers_class = "_1Sda402OKItT9369w-tDDA"
        ability_cooldown_class = "_22XOopr4GL5s8PQoraB4__"
        ability_mana_class = "Y2InYdEEoXxoTgGG2x3B4"
        ability_lore_class = "_1FdISYFSn4ZmiR_wS5YFOM"

        abilities = []

        for e in click_elements:
            e.click()
            refreshed_driver = self.driver
            ability = HeroAbilityItem()
            
            # Using "find_elements" because it returns a list
            # and I don't like Exceptions.
            asset_video = refreshed_driver.find_elements(
                By.XPATH,
                f"""
                //div[contains(@class, '{section_container_class}')]
                //video[contains(@class, '{video_class}')]
                """
            )
            ability["asset_video"] = (
                asset_video[0].get_attribute("poster") if asset_video else None
            )

            asset_icon = refreshed_driver.find_elements(
                By.XPATH,
                f"""
                //div[contains(@class, '{section_container_class}')]
                //img[contains(@class, '{icon_img_class}')]
                """
            )
            ability["asset_icon"] = (
                asset_icon[0].get_attribute("src") if asset_icon else None
            )

            name = refreshed_driver.find_elements(
                By.XPATH,
                f"""
                //div[contains(@class, '{ability_info_container_class}')]
                //div[contains(@class, '{ability_name_class}')]
                """
            )
            ability["name"] = name[0].text if name else None

            shard_scepter = refreshed_driver.find_elements(
                By.XPATH,
                f"""
                //div[contains(@class, '{ability_scepter_shard_class}')]
                """
            )
            ability["shard_scepter"] = (
                shard_scepter[0].text if shard_scepter else None
            )

            description = refreshed_driver.find_elements(
                By.XPATH,
                f"""
                //div[contains(@class, '{ability_info_container_class}')]
                //div[contains(@class, '{ability_description_class}')]
                """
            )
            ability["description"] = description[0].text if description else None

            info = refreshed_driver.find_elements(
                By.XPATH,
                f"""
                //div[contains(@class, '{ability_info_class}')]
                """
            )
            ability["info"] = info[0].text if info else None

            modifiers = refreshed_driver.find_elements(
                By.XPATH,
                f"""
                //div[contains(@class, '{ability_modifiers_class}')]
                """
            )
            ability["modifiers"] = modifiers[0].text if modifiers else None

            cooldown = refreshed_driver.find_elements(
                By.XPATH,
                f"""
                //div[contains(@class, '{ability_cooldown_class}')]
                """
            )
            ability["cooldown"] = cooldown[0].text if cooldown else None

            mana = refreshed_driver.find_elements(
                By.XPATH,
                f"""
                //div[contains(@class, '{ability_mana_class}')]
                """
            )
            ability["mana"] = mana[0].text if mana else None

            lore = refreshed_driver.find_elements(
                By.XPATH,
                f"""
                //div[contains(@class, '{ability_info_container_class}')]
                //div[contains(@class, '{ability_lore_class}')]
                """
            )
            ability["lore"] = lore[0].text if lore else None

            ability["hero_id"] = hero_id

            abilities.append(ability)

        return abilities
    
    @staticmethod
    def extract_every_text(selector, container):
        return selector.xpath(
            f"""
            .//div[contains(@class, '{container}')]//text()
            """
        ).getall()
