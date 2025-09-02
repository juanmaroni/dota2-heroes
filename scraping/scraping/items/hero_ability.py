import scrapy


class HeroAbilityItem(scrapy.Item):
    asset_video = scrapy.Field()
    asset_icon = scrapy.Field()
    name = scrapy.Field()
    shard_scepter = scrapy.Field()
    description = scrapy.Field()
    info = scrapy.Field()
    modifiers = scrapy.Field()
    cooldown = scrapy.Field()
    mana = scrapy.Field()
    lore = scrapy.Field()
    hero_id = scrapy.Field()
