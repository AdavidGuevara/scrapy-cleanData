import scrapy


class ChocolateItem(scrapy.Item):
    nombre = scrapy.Field()
    precio = scrapy.Field()
    url = scrapy.Field()
