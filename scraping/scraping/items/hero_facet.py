import scrapy


class HeroFacetItem(scrapy.Item):
    asset_icon = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    extra_info = scrapy.Field()
    abilities_mod = scrapy.Field() # List of dicts
    hero_id = scrapy.Field()
