import csv
from scraping.items import HeroInfoItem, HeroTalentItem, HeroInnateItem
from utils import (
    TMP_HEROES_INFO_FILENAME, TMP_HEROES_TALENTS_FILENAME,
    TMP_HEROES_INNATE_FILENAME
)


class CleanHeroInfoPipeline: # 100
    def process_item(self, item, spider):
        if isinstance(item, HeroInfoItem):
            item["lore"] = self._process_text(item["lore"])
            item["lore_extended"] = self._process_text(item["lore_extended"])
            item["complexity"] = len(item["complexity"])
            item["base_health"] = int(item["base_health"])
            item["health_regeneration"] = float(item["health_regeneration"])
            item["base_mana"] = int(item["base_mana"])
            item["mana_regeneration"] = float(item["mana_regeneration"])
            item["base_strength"] = int(item["base_strength"])
            item["base_agility"] = int(item["base_agility"])
            item["base_intelligence"] = int(item["base_intelligence"])
            item["strength_gain"] = float(item["strength_gain"])
            item["agility_gain"] = float(item["agility_gain"])
            item["intelligence_gain"] = float(item["intelligence_gain"])
            item["role_carry"] = self._process_role(item["role_carry"])
            item["role_support"] = self._process_role(item["role_support"])
            item["role_nuker"] = self._process_role(item["role_nuker"])
            item["role_disabler"] = self._process_role(item["role_disabler"])
            item["role_jungler"] = self._process_role(item["role_jungler"])
            item["role_durable"] = self._process_role(item["role_durable"])
            item["role_escape"] = self._process_role(item["role_escape"])
            item["role_pusher"] = self._process_role(item["role_pusher"])
            item["role_initiator"] = self._process_role(
                item["role_initiator"]
            )
            self._process_stat_damage(item)
            self._process_stat(item, "attack_time", "base_attack_time", float)
            self._process_stat(item, "attack_range", "base_attack_range")
            self._process_stat(
                item, "projectile_speed", "base_attack_projectile_speed"
            )
            self._process_stat(item, "armor", "base_defense_armor", float)
            self._process_stat(
                item, "magic_resist", "base_defense_magic_resist_perc"
            )
            self._process_stat(
                item, "movement_speed", "base_mobility_movement_speed"
            )
            self._process_stat(
                item, "turn_rate", "base_mobility_turn_rate", float
            )
            self._process_stat_vision(item)
        elif isinstance(item, HeroTalentItem):
            item["level"] = int(item["level"])
        elif isinstance(item, HeroInnateItem):
            item["name"] = item["name"].strip()
            item["description"] = self._process_text(item["description"])

        return item
    
    @staticmethod
    def _process_role(percentage):
        if percentage == "33.3":
            return 1
        elif percentage == "66.6":
            return 2
        elif percentage == "99.9":
            return 3
        else:
            return 0

    @staticmethod
    def _process_stat(item, old_item_stat, new_item_stat, type=int):
        item_stat = item[old_item_stat]

        if item_stat:
            item[new_item_stat] = type(item_stat)
        else:
            item[new_item_stat] = None
        
        del item[old_item_stat]

    @staticmethod
    def _process_stat_damage(item):
        damage = item["damage"]
        damage_min_str = "base_attack_damage_min"
        damage_max_str = "base_attack_damage_max"

        if damage:
            damage = damage.split('-')
            (
                item[damage_min_str], item[damage_max_str]
            ) = int(damage[0]), int(damage[1])
        else:
            (
                item[damage_min_str], item[damage_max_str]
            ) = None, None
            
        del item["damage"]

    @staticmethod
    def _process_stat_vision(item):
        vision = item["vision"]
        vision_day_str = "base_mobility_vision_day"
        vision_night_str = "base_mobility_vision_night"

        if vision:
            vision = vision.split(" / ")
            (
                item[vision_day_str], item[vision_night_str]
            ) = int(vision[0]), int(vision[1])
        else:
            (
                item[vision_day_str], item[vision_night_str]
            ) = None, None
            
        del item["vision"]

    @staticmethod
    def _process_text(text_parts):
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


class CsvExportPipeline: # 400
    def open_spider(self, spider):       
        if spider.name == "dota2_heroes":
            self.heroes_info_filename = TMP_HEROES_INFO_FILENAME
            heroes_info_headers = [
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
            self.heroes_info_file = open(
                self.heroes_info_filename,
                "w",
                newline='',
                encoding="utf-8"
            )
            self.heroes_info_writer = csv.DictWriter(
                self.heroes_info_file,
                fieldnames=heroes_info_headers,
                delimiter='|'
            )
            self.heroes_info_writer.writeheader()

            self.heroes_talents_filename = TMP_HEROES_TALENTS_FILENAME
            heroes_talents_headers = ["talent", "side", "level", "hero_id"]
            self.heroes_talents_file = open(
                self.heroes_talents_filename,
                "w",
                newline='',
                encoding="utf-8"
            )
            self.heroes_talents_writer = csv.DictWriter(
                self.heroes_talents_file,
                fieldnames=heroes_talents_headers,
                delimiter='|'
            )
            self.heroes_talents_writer.writeheader()

            self.heroes_innate_filename = TMP_HEROES_INNATE_FILENAME
            heroes_innate_headers = [
                "name", "description", "is_pasive", "hero_id"
            ]
            self.heroes_innate_file = open(
                self.heroes_innate_filename,
                "w",
                newline='',
                encoding="utf-8"
            )
            self.heroes_innate_writer = csv.DictWriter(
                self.heroes_innate_file,
                fieldnames=heroes_innate_headers,
                delimiter='|'
            )
            self.heroes_innate_writer.writeheader()

    def process_item(self, item, spider):
        if isinstance(item, HeroInfoItem):
            self.heroes_info_writer.writerow(item)
        elif isinstance(item, HeroTalentItem):
            self.heroes_talents_writer.writerow(item)
        elif isinstance(item, HeroInnateItem):
            self.heroes_innate_writer.writerow(item)

        return item

    def close_spider(self, spider):
        if spider.name == "dota2_heroes":
            self.heroes_info_file.close()
            self.heroes_talents_file.close()
            self.heroes_innate_file.close()
