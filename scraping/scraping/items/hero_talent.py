import scrapy


class HeroTalentItem(scrapy.Item):
    talent = scrapy.Field()
    side = scrapy.Field()
    level = scrapy.Field()
    hero_id = scrapy.Field()
