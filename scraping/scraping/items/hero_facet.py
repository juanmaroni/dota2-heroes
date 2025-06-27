import scrapy


class HeroFacetItem(scrapy.Item):
    asset_icon = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    extra_info = scrapy.Field()
    abilities_mod = scrapy.Field() # List of dicts that becomes string
    hero_id = scrapy.Field()
