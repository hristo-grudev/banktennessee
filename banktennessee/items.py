import scrapy


class BanktennesseeItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
