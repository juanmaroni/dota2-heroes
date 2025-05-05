import scrapy


class HeroInnateItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    is_pasive = scrapy.Field()
    hero_id = scrapy.Field()
